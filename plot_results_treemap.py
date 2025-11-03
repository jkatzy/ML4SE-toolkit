#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px


def load_counts_json(json_path: Path) -> pd.DataFrame:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and 'rule_counts' in data:
        rc = data['rule_counts']
    else:
        rc = data
    items = [(str(k), int(v)) for k, v in rc.items() if int(v) > 0]
    return pd.DataFrame(items, columns=['rule', 'count'])


def load_counts_csv(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    cols = {c.lower(): c for c in df.columns}
    rule_col = cols.get('rule') or cols.get('name')
    cnt_col = cols.get('count')
    if not rule_col or not cnt_col:
        raise ValueError(f'CSV缺少必要列: {csv_path}')
    df = df[[rule_col, cnt_col]].rename(columns={rule_col: 'rule', cnt_col: 'count'})
    df['rule'] = df['rule'].astype(str)
    df['count'] = pd.to_numeric(df['count'], errors='coerce').fillna(0).astype(int)
    df = df[df['count'] > 0]
    return df


def is_symbol(rule: str) -> bool:
    # 定义“符号”判定：全由非字母数字下划线组成，或常见标点合集
    if rule == '' or rule is None:
        return False
    rule = str(rule)
    common = set('(){}[],:;.+-*/%&|^!~=<>\'\"`?@#')
    if all(ch in common for ch in rule):
        return True
    # 允许像 ", ',' 这样的计数键
    if len(rule) == 1 and not rule.isalnum() and rule != '_':
        return True
    return False


def aggregate_language_counts(lang_dir: Path) -> pd.DataFrame:
    counts_dir = lang_dir / 'counts'
    csv_dir = lang_dir / 'csv'

    frames = []
    if counts_dir.exists():
        for p in sorted(counts_dir.glob('*.json')):
            try:
                frames.append(load_counts_json(p))
            except Exception as e:
                print(f'[WARN] 读取JSON失败: {p} ({e})')
    if not frames and csv_dir.exists():
        for p in sorted(csv_dir.glob('*_counts.csv')):
            try:
                frames.append(load_counts_csv(p))
            except Exception as e:
                print(f'[WARN] 读取CSV失败: {p} ({e})')

    if not frames:
        return pd.DataFrame(columns=['rule', 'count'])

    df = pd.concat(frames, ignore_index=True)
    df = df.groupby('rule', as_index=False)['count'].sum()
    return df


def make_treemap(df: pd.DataFrame, language: str, out_html: Path, include_symbols: bool, top_n: int | None):
    if df.empty:
        print(f'[SKIP] {language} 无有效数据')
        return

    if not include_symbols:
        df = df[~df['rule'].apply(is_symbol)]
    if df.empty:
        print(f'[SKIP] {language} 过滤符号后无数据')
        return

    if top_n:
        df = df.sort_values('count', ascending=False).head(top_n)

    mid = float(np.mean(df['count'])) if not df['count'].empty else 0.0
    fig = px.treemap(
        df,
        path=[px.Constant(language), 'rule'],
        values='count',
        color='count',
        hover_data=['rule', 'count'],
        color_continuous_scale='RdBu',
        color_continuous_midpoint=mid
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), title=f'{language} rule usage treemap' + ('' if include_symbols else ' (no symbols)'))
    out_html.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(out_html))
    print(f'[OK] {language} treemap -> {out_html}')


def main():
    parser = argparse.ArgumentParser(description='Generate treemap from results folder with optional symbol toggle')
    parser.add_argument('--results-root', type=str, default='results', help='results 目录（包含各语言子目录）')
    parser.add_argument('--output-dir', type=str, default='treemap_outputs', help='输出HTML目录')
    parser.add_argument('--top-n', type=int, default=None, help='每个语言只显示前N个规则')
    parser.add_argument('--include-symbols', action='store_true', help='是否包含符号(如 ( { , 等) 的计数')
    args = parser.parse_args()

    results_root = Path(args.results_root).resolve()
    out_root = Path(args.output_dir).resolve()
    if not results_root.exists():
        raise SystemExit(f'目录不存在: {results_root}')

    per_lang_frames = []
    for sub in sorted(results_root.iterdir()):
        if not sub.is_dir():
            continue
        lang = sub.name
        df = aggregate_language_counts(sub)
        if df.empty:
            print(f'[INFO] 跳过 {lang}（未找到 counts/csv 或无数据）')
            continue
        suffix = 'with_symbols' if args.include_symbols else 'no_symbols'
        out_html = out_root / f'{lang}_treemap_{suffix}.html'
        make_treemap(df, lang, out_html, include_symbols=args.include_symbols, top_n=args.top_n)
        df_lang = df.copy()
        df_lang['language'] = lang
        per_lang_frames.append(df_lang)

    # 生成全语言汇总 Treemap
    if per_lang_frames:
        all_df = pd.concat(per_lang_frames, ignore_index=True)
        if not args.include_symbols:
            all_df = all_df[~all_df['rule'].apply(is_symbol)]
        if args.top_n:
            # 按语言内Top-N
            all_df = (all_df.sort_values(['language', 'count'], ascending=[True, False])
                              .groupby('language', as_index=False)
                              .head(args.top_n))
        mid = float(np.mean(all_df['count'])) if not all_df['count'].empty else 0.0
        fig = px.treemap(
            all_df,
            path=[px.Constant('all_languages'), 'language', 'rule'],
            values='count',
            color='count',
            hover_data=['language', 'rule', 'count'],
            color_continuous_scale='RdBu',
            color_continuous_midpoint=mid
        )
        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            title='All languages rule usage treemap' + ('' if args.include_symbols else ' (no symbols)')
        )
        suffix = 'with_symbols' if args.include_symbols else 'no_symbols'
        out_root.mkdir(parents=True, exist_ok=True)
        out_all = out_root / f'all_languages_treemap_{suffix}.html'
        fig.write_html(str(out_all))
        print(f'[OK] all_languages treemap -> {out_all}')


if __name__ == '__main__':
    main()


