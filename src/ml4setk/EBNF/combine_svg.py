import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
import argparse

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def combine_svgs(input_dir, output_path):
    """Combine multiple SVG files into one large SVG file."""
    root = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "class": "railroad-diagram"
    })
    
    title_elem = ET.SubElement(root, "title")
    title_elem.text = "EBNF Grammar Diagrams"

    style = ET.SubElement(root, "style")
    style.text = """
    svg.railroad-diagram {
        background-color: hsl(30,20%,95%);
    }
    svg.railroad-diagram path {
        stroke-width: 3;
        stroke: black;
        fill: rgba(0,0,0,0);
    }
    svg.railroad-diagram text {
        font: bold 14px monospace;
        text-anchor: middle;
    }
    svg.railroad-diagram text.label {
        text-anchor: start;
    }
    svg.railroad-diagram text.comment {
        font: italic 12px monospace;
    }
    svg.railroad-diagram rect {
        stroke-width: 3;
        stroke: black;
        fill: hsl(120,100%,90%);
    }
    .rule-title {
        font: bold 16px sans-serif;
        fill: #333;
    }
    """
    
    current_y = 50 
    max_width = 0
    
    svg_files = sorted([f for f in Path(input_dir).glob("*.svg")])
    
    if not svg_files:
        print(f"No SVG files found in {input_dir}")
        return

    for svg_file in svg_files:
        try:
            tree = ET.parse(svg_file)
            svg_root = tree.getroot()

            viewbox = svg_root.get('viewBox', '0 0 100 100')
            _, _, width, height = map(float, viewbox.split())
            
            rule_name = svg_file.stem
            title = ET.SubElement(root, "text", {
                "x": "80",
                "y": str(current_y - 20),
                "class": "rule-title"
            })
            title.text = rule_name
            
            g = ET.SubElement(root, "g", {
                "transform": f"translate(80, {current_y})"
            })
            
            for elem in svg_root:
                if elem.tag != "style":
                    g.append(elem)

            max_width = max(max_width, width + 40)
            current_y += height + 80 
            
            print(f"Processed {rule_name}")
            
        except Exception as e:
            print(f"Error processing {svg_file}: {e}")
    
    root.set("width", str(max_width))
    root.set("height", str(current_y))
    root.set("viewBox", f"0 0 {max_width} {current_y}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prettify(root))
    
    print(f"\nCombined SVG saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine multiple SVG files into one large SVG file')
    parser.add_argument('input_dir', help='Directory containing individual SVG files')
    parser.add_argument('output_path', help='Path for the combined SVG output')
    
    args = parser.parse_args()
    
    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
    
    combine_svgs(args.input_dir, args.output_path) 