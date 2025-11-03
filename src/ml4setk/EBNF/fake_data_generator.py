import re
import csv
import random
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import OrderedDict
import argparse

def generate_fake_data(svg_dir: str, fake_csv_dir: str, global_max: int = None, random_seed: int = None):
    """
    Generate fake count data for SVG files and save as CSV files.
    
    Args:
        svg_dir: Directory containing SVG files
        fake_csv_dir: Directory to save generated CSV files
        global_max: Maximum count value (if None, will be randomly generated)
        random_seed: Random seed for reproducibility
    """
    SVG_DIR = Path(svg_dir)
    FAKE_CSV_DIR = Path(fake_csv_dir)
    FAKE_CSV_DIR.mkdir(parents=True, exist_ok=True)

    if random_seed is not None:
        random.seed(random_seed)

    if global_max is None:
        global_max = random.randint(20, 100)
    print(f"GLOBAL_MAX = {global_max}")

    def parse_tokens(svg_text: str):
        m = re.search(r'xmlns="([^"]+)"', svg_text)
        ns = m.group(1) if m else None
        g_tag = f"{{{ns}}}g" if ns else "g"
        rect_tag = f"{{{ns}}}rect" if ns else "rect"

        root = ET.fromstring(svg_text)
        tokens = OrderedDict()
        for g in root.iter(g_tag):
            if "terminal" not in (g.get("class") or ""):
                continue
            for rect in g.findall(rect_tag):
                tok = rect.get("data-text")
                if tok:
                    tokens.setdefault(tok, None)
        return list(tokens.keys())

    svg_files = list(SVG_DIR.rglob("*.svg"))
    if not svg_files:
        raise RuntimeError("No SVG files found.")

    for svg_path in svg_files:
        base = svg_path.stem
        svg_text = svg_path.read_text(encoding="utf-8")
        tokens = parse_tokens(svg_text)

        if not tokens:
            print(f"No tokens found in {svg_path.name}, skipped.")
            continue

        fake_rows = [(t, random.randint(1, global_max)) for t in tokens]

        csv_path = FAKE_CSV_DIR / f"{base}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "count"])
            writer.writerows(fake_rows)

        print(f"✓ Generated {csv_path}")

    print("All done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate fake count data for SVG files and save as CSV files.')
    parser.add_argument('--svg-dir', type=str, required=True,
                      help='Directory containing SVG files')
    parser.add_argument('--fake-csv-dir', type=str, required=True,
                      help='Directory to save generated CSV files')
    parser.add_argument('--global-max', type=int, default=None,
                      help='Maximum count value (if not specified, will be randomly generated)')
    parser.add_argument('--random-seed', type=int, default=None,
                      help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    generate_fake_data(
        svg_dir=args.svg_dir,
        fake_csv_dir=args.fake_csv_dir,
        global_max=args.global_max,
        random_seed=args.random_seed
    ) 