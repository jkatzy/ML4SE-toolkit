import json
import csv
import re
import os
import ast
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict, Counter
import argparse

ALL_AST_NODE_TYPES = set()

def extract_ast_node_types_from_jsonl(jsonl_path):
    node_types = Counter()
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                code = (data.get('prompt', '') + data.get('canonical_solution', ''))
                if not code.strip():
                    continue
                try:
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        node_type = type(node).__name__
                        node_types[node_type] += 1
                except Exception:
                    continue
            except Exception:
                continue
    return node_types

def map_to_grammar_rules(node):
    """
    Map AST nodes to grammar rules (using AST node type names directly).
    Returns a list of grammar rule names that correspond to the node.
    """
    return [type(node).__name__]

def process_real_data(jsonl_path: str, svg_dir: str, csv_dir: str, out_dir: str):
    """
    Process real data from JSONL files, generate counts, and color SVG files.
    Args:
        jsonl_path: Path to the JSONL file containing real data
        svg_dir: Directory containing input SVG files
        csv_dir: Directory to save generated CSV files with counts
        out_dir: Directory to save colored SVG files
    """
    JSONL_PATH = Path(jsonl_path)
    SVG_DIR = Path(svg_dir)
    CSV_DIR = Path(csv_dir)
    OUT_DIR = Path(out_dir)
    
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\n[INFO] Counting all AST node types in HumanEval canonical_solution...")
    node_types = extract_ast_node_types_from_jsonl(str(JSONL_PATH))
    print(f"[INFO] AST node types and their frequencies in HumanEval:")
    for k, v in node_types.most_common():
        print(f"  {k}: {v}")
    print(f"[INFO] Total of {len(node_types)} AST node types\n")

    grammar_counts = defaultdict(int)
    print(f"Reading data from {JSONL_PATH}...")
    
    with JSONL_PATH.open('r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                code = (data.get('prompt', '') + data.get('canonical_solution', ''))
                if not code.strip():
                    continue
                try:
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        for rule in map_to_grammar_rules(node):
                            grammar_counts[rule] += 1
                except Exception:
                    continue
            except Exception:
                continue

    if not grammar_counts:
        raise ValueError("No grammar rules found in the JSONL file!")

    global_max = max(grammar_counts.values())
    print(f"Global max count = {global_max}")

    csv_path = CSV_DIR / "grammar_counts.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "count"])
        writer.writerows(grammar_counts.items())
    print(f"✓ Generated {csv_path}")

    def to_color(cnt, mx=global_max):
        ratio = min(max(cnt / mx, 0), 1)
        r = int((1 - ratio) * 255)
        g = int(ratio * 255)
        return f"#{r:02X}{g:02X}00"

    for svg_path in SVG_DIR.rglob("*.svg"):
        base = svg_path.stem
        svg_text = svg_path.read_text(encoding='utf-8')

        m = re.search(r'xmlns="([^"]+)"', svg_text)
        ns = m.group(1) if m else None
        g_tag = f"{{{ns}}}g" if ns else "g"
        rect_tag = f"{{{ns}}}rect" if ns else "rect"

        root = ET.fromstring(svg_text)

        for g in root.iter(g_tag):
            if "terminal" not in (g.get("class") or ""):
                continue
            for rect in g.findall(rect_tag):
                key = rect.get("data-text")
                if not key:
                    continue
                cnt = grammar_counts.get(key, 0)

                rect.attrib.pop("fill", None)
                style = rect.get("style") or ""
                style = re.sub(r"fill\s*:\s*[^;]+;?", "", style)
                style += f"fill:{to_color(cnt)};"
                rect.set("style", style)

        out_file = OUT_DIR / f"{base}.svg"
        ET.ElementTree(root).write(out_file, encoding="utf-8", xml_declaration=True)
        print(f"Colored {out_file}")

    print("All Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process real data from JSONL files and color SVG files based on grammar rule counts.')
    parser.add_argument('--jsonl-path', type=str, required=True,
                      help='Path to the JSONL file containing real data')
    parser.add_argument('--svg-dir', type=str, required=True,
                      help='Directory containing input SVG files')
    parser.add_argument('--csv-dir', type=str, required=True,
                      help='Directory to save generated CSV files with counts')
    parser.add_argument('--out-dir', type=str, required=True,
                      help='Directory to save colored SVG files')
    
    args = parser.parse_args()
    
    process_real_data(
        jsonl_path=args.jsonl_path,
        svg_dir=args.svg_dir,
        csv_dir=args.csv_dir,
        out_dir=args.out_dir
    ) 