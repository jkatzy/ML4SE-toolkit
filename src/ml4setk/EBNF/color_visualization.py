#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from pathlib import Path
from typing import Dict, Tuple, Optional, Iterable, List
import xml.etree.ElementTree as ET

# 非线性拉伸参数：频率 f -> f_adj = f ** GAMMA，使中高频更偏绿
DEFAULT_GAMMA = 0.35


def _load_counts(path: str) -> Dict[str, int]:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    # 支持 {rule:count} 或 {"rule_counts": {...}} 或 {"counts": {...}}
    if isinstance(data, dict) and "rule_counts" in data and isinstance(data["rule_counts"], dict):
        return {str(k): int(v) for k, v in data["rule_counts"].items()}
    if isinstance(data, dict) and "counts" in data and isinstance(data["counts"], dict):
        return {str(k): int(v) for k, v in data["counts"].items()}
    if isinstance(data, dict):
        return {str(k): int(v) for k, v in data.items()}
    raise ValueError("Unsupported counts json format")


def _parse_viewbox_size(root: ET.Element) -> Tuple[Optional[float], Optional[float]]:
    vb = root.get("viewBox") or root.get("viewbox")
    if not vb:
        return None, None
    try:
        parts = [float(x) for x in vb.replace(",", " ").split()]
        if len(parts) == 4:
            return parts[2], parts[3]
    except Exception:
        pass
    return None, None


def _svg_size(root: ET.Element) -> Tuple[Optional[float], Optional[float]]:
    # 优先用 viewBox
    w, h = _parse_viewbox_size(root)
    if w and h:
        return w, h
    # 回退解析 width/height（可能含 px）
    def _num(val: Optional[str]) -> Optional[float]:
        if not val:
            return None
        try:
            return float(re.sub(r"[^\d.]+", "", val))
        except Exception:
            return None
    w = _num(root.get("width"))
    h = _num(root.get("height"))
    return w, h


def _hsl_to_hex(h: float, s: float, l: float) -> str:
    # h[0..360), s,l in [0..1]
    c = (1 - abs(2 * l - 1)) * s
    hp = (h % 360) / 60.0
    x = c * (1 - abs(hp % 2 - 1))
    r = g = b = 0.0
    if   0 <= hp < 1: r, g, b = c, x, 0
    elif 1 <= hp < 2: r, g, b = x, c, 0
    elif 2 <= hp < 3: r, g, b = 0, c, x
    elif 3 <= hp < 4: r, g, b = 0, x, c
    elif 4 <= hp < 5: r, g, b = x, 0, c
    elif 5 <= hp < 6: r, g, b = c, 0, x
    m = l - c / 2
    r, g, b = (r + m), (g + m), (b + m)
    to255 = lambda v: max(0, min(255, int(round(v * 255))))
    return "#{:02X}{:02X}{:02X}".format(to255(r), to255(g), to255(b))


def _freq_to_color_nonlinear(count: int, max_count: int, gamma: float = DEFAULT_GAMMA) -> str:
    # 基于单个规则计数而非总体频率进行着色
    # count: 当前规则的计数
    # max_count: 所有规则中的最大计数
    if max_count == 0:
        return _hsl_to_hex(0.0, 0.85, 0.55)  # 红色（无计数）
    
    # 计算相对频率：当前计数 / 最大计数
    f = count / max_count
    if f < 0.0: f = 0.0
    if f > 1.0: f = 1.0
    
    # 非线性拉伸
    f_adj = f ** gamma
    return _hsl_to_hex(120.0 * f_adj, 0.85, 0.55)


def _get_ns(root: ET.Element) -> str:
    m = re.match(r"\{(.+)\}", root.tag)
    return m.group(1) if m else ""


def _norm_key(s: str) -> str:
    # 去前后空白、小写、把空格/连字符替换为下划线，去除起始下划线（兼容 _statement）
    t = s.strip()
    t = t.replace("-", " ")
    t = re.sub(r"\s+", "_", t)
    t = t.lower()
    t = t.lstrip("_")
    return t


def _singularize(nk: str) -> str:
    # 简单单复数回退
    if nk.endswith("ies"):
        return nk[:-3] + "y"
    if nk.endswith("sses"):
        return nk[:-2]
    if nk.endswith("s") and len(nk) > 1:
        return nk[:-1]
    return nk


def _language_from_rules_dir(rules_dir: Path) -> str:
    # visualization/<lang>/rules
    try:
        return rules_dir.parent.name.lower()
    except Exception:
        return "unknown"


def _alias_map(lang: str) -> Dict[str, Iterable[str]]:
    # 返回：归一化后的 EBNF 名 → 一组 tree-sitter 节点名（原样，不归一化）
    if lang == "python":
        statement_all = [
            "expression_statement", "return_statement", "if_statement",
            "for_statement", "while_statement", "try_statement", "with_statement",
            "class_definition", "function_definition", "import_statement",
            "raise_statement", "pass_statement", "break_statement", "continue_statement",
            "delete_statement", "global_statement", "nonlocal_statement",
            "assert_statement", "type_alias_statement", "exec_statement",
        ]
        simple_stmt = [
            "expression_statement", "return_statement", "raise_statement",
            "pass_statement", "break_statement", "continue_statement",
            "delete_statement", "global_statement", "nonlocal_statement",
            "assert_statement", "type_alias_statement", "exec_statement",
        ]
        compound_stmt = [
            "if_statement", "for_statement", "while_statement",
            "try_statement", "with_statement",
            "class_definition", "function_definition",
        ]
        return {
            "suite": ["block"],
            "statement": statement_all,
            "simple_statement": simple_stmt,
            "compound_statement": compound_stmt,
            "dotted_name": ["identifier"],
        }
    # 其它语言可后续扩展
    return {}


def _build_counts_index(raw_counts: Dict[str, int]) -> Tuple[Dict[str, int], Dict[str, int]]:
    # raw：原始键；norm：归一化键聚合（多个原始键可能归到同一归一化键）
    norm_counts: Dict[str, int] = {}
    for k, v in raw_counts.items():
        nk = _norm_key(k)
        norm_counts[nk] = norm_counts.get(nk, 0) + int(v)
    return raw_counts, norm_counts


def _resolve_count(lang: str, key: str, raw_counts: Dict[str, int], norm_counts: Dict[str, int]) -> int:
    if not key:
        return 0
    # 精确匹配（原始键）
    if key in raw_counts:
        return int(raw_counts[key])
    nk = _norm_key(key)
    # 归一化匹配
    if nk in norm_counts:
        return int(norm_counts[nk])
    # 单复数回退
    sk = _singularize(nk)
    if sk in norm_counts:
        return int(norm_counts[sk])
    # 别名汇总（对 nk 与 sk 都尝试）
    aliases = _alias_map(lang).get(nk) or _alias_map(lang).get(sk)
    if aliases:
        s = 0
        for a in aliases:
            if a in raw_counts:
                s += int(raw_counts[a])
            else:
                na = _norm_key(a)
                s += int(norm_counts.get(na, 0))
        return s
    return 0


_noise_re = re.compile(r"^[^A-Za-z_]+$")  # 全符号或数字等
def _is_noise_key(k: str) -> bool:
    if not k:
        return True
    k = k.strip()
    if k.startswith("~"):
        return True
    if _noise_re.match(k):
        return True
    return False


def _collect_group_keys(ns: str, g: ET.Element) -> List[str]:
    rect_tag = f"{{{ns}}}rect" if ns else "rect"
    text_tag = f"{{{ns}}}text" if ns else "text"
    keys: List[str] = []
    # 优先收集 rect 的 data-text
    for r in g.findall(rect_tag):
        dt = r.get("data-text")
        if dt and dt.strip() and not _is_noise_key(dt):
            keys.append(dt.strip())
    # 递归收集所有 text 的内容
    for txt_el in g.findall(f".//{text_tag}"):
        val = (txt_el.text or "").strip()
        if val and not _is_noise_key(val):
            keys.append(val)
    return keys


def _all_rects_iter(ns: str, root: ET.Element):
    rect_tag = f"{{{ns}}}rect" if ns else "rect"
    for r in root.iter(rect_tag):
        yield r


def _set_rect_color(rect: ET.Element, color: str):
    # 双保险：style + fill，并增加 stroke 提升可见度
    rect.attrib.pop("fill", None)
    style = rect.get("style") or ""
    style = re.sub(r"fill\s*:\s*[^;]+;?", "", style)
    if style and not style.endswith(";"):
        style += ";"
    rect.set("style", f"{style}fill:{color};")
    rect.set("fill", color)
    if not rect.get("stroke"):
        rect.set("stroke", "#333")


def _add_badge(ns: str, root: ET.Element, text: str, color: str):
    # 自适应徽标：根据文本长度估算宽度；小字体、半透明背景，减少遮挡
    w, _ = _svg_size(root)
    margin = 8.0
    font_size = 11.0
    char_w = font_size * 0.62
    pad_x = 8.0
    pad_y = 6.0
    min_w = 80.0
    text_w = len(text) * char_w
    badge_w = max(min_w, text_w + 2 * pad_x)
    if w:
        badge_w = min(badge_w, w - 2 * margin)
    badge_h = font_size + 2 * pad_y

    g_tag   = f"{{{ns}}}g" if ns else "g"
    rect_tag= f"{{{ns}}}rect" if ns else "rect"
    text_tag= f"{{{ns}}}text" if ns else "text"

    badge_group = ET.Element(g_tag)
    ET.SubElement(badge_group, rect_tag, {
        "x": str(margin),
        "y": str(margin),
        "width": f"{badge_w:.1f}",
        "height": f"{badge_h:.1f}",
        "rx": "4", "ry": "4",
        "style": f"fill:{color};fill-opacity:0.20;stroke:black;stroke-width:1;",
    })
    tx = ET.SubElement(badge_group, text_tag, {
        "x": f"{margin + badge_w / 2:.1f}",
        "y": f"{margin + badge_h - pad_y:.1f}",
        "style": f"font: bold {int(font_size)}px sans-serif; text-anchor: middle; fill:black;",
    })
    tx.text = text
    root.append(badge_group)


def _collect_groups(ns: str, root: ET.Element):
    g_tag = f"{{{ns}}}g" if ns else "g"
    for g in root.iter(g_tag):
        cls = (g.get("class") or "").strip()
        yield g, cls


def _rule_name_from_filename(svg_path: Path) -> str:
    return svg_path.stem


def color_svgs(rules_dir: str, counts_json: str, out_dir: str) -> Tuple[int, int, int]:
    """
    对 visualization/<lang>/rules 下的 SVG 进行按位置着色，并在左上角添加规则计数徽标。
    - 着色依据：基于每个规则的计数相对于最大计数的比例（而非总体频率）
    - 计数解析顺序：rect.data-text / 所有文本 → 单复数回退/别名 → 文件名（规则名）
    - 分组（terminal/nonterminal）内每个 rect 单独上色；未匹配则使用组和或规则总计
    返回: (colored_files, total_files, global_max_for_compat_print)
    """
    rules_dir_p = Path(rules_dir)
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)

    raw_counts = _load_counts(counts_json)
    raw_counts, norm_counts = _build_counts_index(raw_counts)
    total_occ = sum(raw_counts.values()) if raw_counts else 1
    global_max = max(raw_counts.values()) if raw_counts else 1  # 用于计算相对分数

    lang = _language_from_rules_dir(rules_dir_p)

    total_files = 0
    colored_files = 0

    for svg_path in sorted(rules_dir_p.glob("*.svg")):
        total_files += 1
        try:
            tree = ET.parse(str(svg_path))
            root = tree.getroot()
            ns = _get_ns(root)
            rect_tag = f"{{{ns}}}rect" if ns else "rect"

            rule_name = _rule_name_from_filename(svg_path)
            rule_total = _resolve_count(lang, rule_name, raw_counts, norm_counts)
            # 计算相对于最大计数的比例，而非总体频率
            rule_ratio = (rule_total / global_max) if global_max > 0 else 0.0
            rule_color = _freq_to_color_nonlinear(rule_total, global_max)

            colored_any = False

            # 遍历分组，定位并逐 rect 上色
            for g, cls in _collect_groups(ns, root):
                if "terminal" in cls or "nonterminal" in cls:
                    # 该组候选键（已过滤噪声，递归收集文本）
                    cand_keys = _collect_group_keys(ns, g)

                    # 组和计数（汇总候选键）
                    group_sum = 0
                    for k in cand_keys:
                        group_sum += _resolve_count(lang, k, raw_counts, norm_counts)

                    # 若组和仍为 0，使用"规则名别名集合"的汇总作为回退（例如 dotted_name -> identifier）
                    if group_sum == 0:
                        rn = _norm_key(rule_name)
                        aliases = _alias_map(lang).get(rn) or _alias_map(lang).get(_singularize(rn))
                        if aliases:
                            for a in aliases:
                                if a in raw_counts:
                                    group_sum += int(raw_counts[a])
                                else:
                                    na = _norm_key(a)
                                    group_sum += int(norm_counts.get(na, 0))

                    # 逐 rect 单独上色
                    for r in g.findall(rect_tag):
                        key = r.get("data-text")
                        if not key or not key.strip() or _is_noise_key(key):
                            # 回退：用 cand_keys 首个可用键，否则用规则名
                            key = cand_keys[0] if cand_keys else rule_name
                        cnt = _resolve_count(lang, key, raw_counts, norm_counts)
                        if cnt == 0:
                            cnt = group_sum if group_sum > 0 else rule_total
                        # 使用基于最大计数的相对着色
                        color = _freq_to_color_nonlinear(cnt, global_max)
                        _set_rect_color(r, color)
                        colored_any = True

            # 若没有任何匹配分组，整图 rect 用规则总计颜色
            if not colored_any:
                for r in _all_rects_iter(ns, root):
                    _set_rect_color(r, rule_color)

            # 徽标（规则名：计数与相对于最大值的比例）
            badge_text = f"{rule_name}: {rule_total} ({rule_ratio:.1%} of max)"
            _add_badge(ns, root, badge_text, rule_color)

            # 保存
            out_path = out_dir_p / svg_path.name
            tree.write(str(out_path), encoding="utf-8", xml_declaration=True)
            colored_files += 1

        except Exception:
            # 失败则复制原图，不中断流程
            try:
                out_path = out_dir_p / svg_path.name
                out_path.write_bytes(svg_path.read_bytes())
            except Exception:
                pass

    return colored_files, total_files, global_max
