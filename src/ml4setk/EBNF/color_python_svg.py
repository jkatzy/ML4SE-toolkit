import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import argparse

def color_python_svg_with_humaneval_stats(svg_dir: str, global_csv_path: str, out_dir: str):
    """
    Color Python SVG files using global grammar statistics from HumanEval.
    
    Args:
        svg_dir: Directory containing input SVG files
        global_csv_path: Path to the global grammar counts CSV file
        out_dir: Directory to save colored SVG files
    """
    SVG_DIR = Path(svg_dir)
    OUT_DIR = Path(out_dir)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    grammar_counts = {}
    global_max = 0
    
    with open(global_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name'].strip()
            count = int(row['count'])
            grammar_counts[name] = count
            global_max = max(global_max, count)

    if global_max == 0:
        raise ValueError("No counts read from the global CSV file!")

    print(f"Global max count = {global_max}")

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
    parser = argparse.ArgumentParser(description='Color Python SVG files using HumanEval global grammar statistics.')
    parser.add_argument('--svg-dir', type=str, required=True,
                      help='Directory containing input SVG files')
    parser.add_argument('--global-csv', type=str, required=True,
                      help='Path to the global grammar counts CSV file')
    parser.add_argument('--out-dir', type=str, required=True,
                      help='Directory to save colored SVG files')
    
    args = parser.parse_args()
    
    color_python_svg_with_humaneval_stats(
        svg_dir=args.svg_dir,
        global_csv_path=args.global_csv,
        out_dir=args.out_dir
    ) 