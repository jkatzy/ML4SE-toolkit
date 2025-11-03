import csv
import re
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
import argparse

def color_svg_files(svg_dir: str, csv_dir: str, out_dir: str):
    """
    Color SVG files based on count data from CSV files.
    
    Args:
        svg_dir: Directory containing input SVG files
        csv_dir: Directory containing CSV files with count data
        out_dir: Directory to save colored SVG files
    """
    SVG_DIR = Path(svg_dir)
    CSV_DIR = Path(csv_dir)
    OUT_DIR = Path(out_dir)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    counts_map = defaultdict(dict)
    global_max = 0

    for svg_path in SVG_DIR.rglob("*.svg"):
        base = svg_path.stem
        csv_path = CSV_DIR / f"{base}.csv"
        if not csv_path.exists():
            print(f"CSV not found for {base}, skipped")
            continue

        with csv_path.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name'].strip()
                count = int(row['count'])
                counts_map[base][name] = count
                global_max = max(global_max, count)

    if global_max == 0:
        raise ValueError("No counts read from any CSV!")

    print(f"Global max count = {global_max}")

    def to_color(cnt, mx=global_max):
        ratio = min(max(cnt / mx, 0), 1)
        r = int((1 - ratio) * 255)
        g = int(ratio * 255)
        return f"#{r:02X}{g:02X}00"

    for svg_path in SVG_DIR.rglob("*.svg"):
        base = svg_path.stem
        if base not in counts_map:
            continue

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
                cnt = counts_map[base].get(key)
                if cnt is None:
                    continue

                rect.attrib.pop("fill", None)
                style = rect.get("style") or ""
                style = re.sub(r"fill\s*:\s*[^;]+;?", "", style)
                style += f"fill:{to_color(cnt)};"
                rect.set("style", style)

        out_file = OUT_DIR / f"{base}.svg"
        ET.ElementTree(root).write(out_file, encoding="utf-8", xml_declaration=True)
        print(f"Colored {out_file}")

    print("All Done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Color SVG files based on count data from CSV files.')
    parser.add_argument('--svg-dir', type=str, required=True,
                      help='Directory containing input SVG files')
    parser.add_argument('--csv-dir', type=str, required=True,
                      help='Directory containing CSV files with count data')
    parser.add_argument('--out-dir', type=str, required=True,
                      help='Directory to save colored SVG files')
    
    args = parser.parse_args()
    
    color_svg_files(
        svg_dir=args.svg_dir,
        csv_dir=args.csv_dir,
        out_dir=args.out_dir
    ) 