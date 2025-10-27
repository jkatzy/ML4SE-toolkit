#!/usr/bin/env python3
"""
Batch analyze all code files under a directory using RuleCounter and generate
colored railroad diagrams based on aggregated counts.

Usage examples:
  python batch_directory_analysis.py /path/to/src --language python \
    --work-dir results --extensions .py --top-n 20

Notes:
  - Aggregates counts across all matched files
  - Saves JSON and CSV under <work-dir>/counts and <work-dir>/csv
  - Invokes visualize_grammars.py to build combined.svg and colored_combined.svg
"""

import argparse
import os
from pathlib import Path
from typing import Dict, Iterable, List
from collections import Counter
import subprocess
import sys
import json

# Allow running from repo root without install
THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parent
SRC_DIR = REPO_ROOT / "src"
sys.path.append(str(SRC_DIR))

from ml4setk.EBNF.rule_counter import RuleCounter


def iter_code_files(root: Path, exts: Iterable[str]) -> Iterable[Path]:
    exts_lower = {e.lower() for e in exts}
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() in exts_lower:
                yield p


def aggregate_counts(counter: RuleCounter, files: List[Path]) -> Dict[str, int]:
    total = Counter()
    for idx, fp in enumerate(files, 1):
        try:
            counts = counter.count_rules_in_file(str(fp))
            if counts:
                total.update(counts)
        except Exception as e:
            print(f"[WARN] Failed to analyze {fp}: {e}")
        if idx % 50 == 0:
            print(f"Processed {idx}/{len(files)} files...")
    return dict(total)


def save_json(counter: RuleCounter, counts: Dict[str, int], out_json: Path) -> None:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    counter.save_counts_to_json(counts, str(out_json))


def save_csv(counts: Dict[str, int], out_csv: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write("name,count\n")
        for rule, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{rule},{cnt}\n")
    print(f"CSV saved to: {out_csv}")


def run_visualization(language: str, counts_json: Path) -> None:
    vis_script = REPO_ROOT / "src/ml4setk/EBNF/visualize_grammars.py"
    cmd = [sys.executable, str(vis_script), "--languages", language, "--counts-json", str(counts_json)]
    print(f"[RUN] {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if proc.returncode != 0:
        print("[ERROR] Visualization failed.")
    else:
        print("[OK] Visualization generated.")


def main():
    parser = argparse.ArgumentParser(description="Batch directory EBNF rule counting and visualization")
    parser.add_argument("directory", help="Root directory to scan for code files")
    parser.add_argument("--language", "-l", default="python", help="Programming language (default: python)")
    parser.add_argument("--extensions", "-e", nargs="+", default=[".py"], help="File extensions to include (e.g., .py .js)")
    parser.add_argument("--work-dir", "-w", default="results", help="Working directory for outputs (default: results)")
    parser.add_argument("--base-name", "-n", default=None, help="Base name for output files (default: derived from directory name)")
    parser.add_argument("--top-n", type=int, default=20, help="Top N to print in summary")
    args = parser.parse_args()

    root = Path(args.directory).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Error: directory '{root}' not found or not a directory")
        return 1

    base_name = args.base_name or root.name

    # Prepare output paths
    work_dir = Path(args.work_dir)
    counts_json = work_dir / "counts" / f"{base_name}_counts.json"
    counts_csv = work_dir / "csv" / f"{base_name}_counts.csv"

    # Collect files
    files = list(iter_code_files(root, args.extensions))
    if not files:
        print("No files matched the given extensions.")
        return 0
    print(f"Found {len(files)} files under {root} with extensions {args.extensions}")

    # Count
    counter = RuleCounter(language=args.language)
    counts = aggregate_counts(counter, files)

    if not counts:
        print("No rules were counted. Exiting.")
        return 0

    # Summary and save
    counter.print_summary(counts, top_n=args.top_n)
    save_json(counter, counts, counts_json)
    save_csv(counts, counts_csv)

    # Visualization
    run_visualization(args.language, counts_json)

    # Print key outputs
    print("\nOutputs:")
    print(f"- JSON: {counts_json}")
    print(f"- CSV:  {counts_csv}")
    print(f"- SVGs: visualization/{args.language}/combined.svg and colored_combined.svg")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


