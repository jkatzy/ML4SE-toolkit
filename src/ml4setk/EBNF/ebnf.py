from tree_sitter import Language, Parser
from RRD.railroad import Diagram, Sequence, Choice, Optional, OneOrMore, ZeroOrMore, Terminal
from IPython.display import SVG, display
import os, io, re
from xml.sax.saxutils import escape
import argparse

Language.build_library(
    './build/my-ebnf3.so',  
    ['./tree-sitter-ebnf']   
)
MY_LANGUAGE = Language('./build/my-ebnf3.so', 'EBNF')
ts_parser = Parser()
ts_parser.set_language(MY_LANGUAGE)


def visit(node):
    text = node.text.decode()
    if node.type == "ERROR" or node.type.endswith("Content"):
        return Terminal(escape(text))
    match node.type:
        case 'source_file':
            blocks = []
            for child in node.children:
                if child.type != "rule":
                    blocks.append(visit(child))
            return Sequence(*blocks)
        case 'rhs':
            return visit(node.children[0])
        case 'sequence':
            return Sequence(*(visit(c) for c in node.children))
        case 'statements' | 'statementsNoSelection':
            return visit(node.children[0])
        case 'sequenceNoSelection':
            return Sequence(*(visit(c) for c in node.children))
        case 'parenthesizedStatement':
            return visit(node.children[1])
        case 'quantifiedStatement':
            return visit(node.children[0])
        case 'selectionStatement':
            opts = [visit(c) for c in node.children if c.type == 'sequenceNoSelection']
            return Choice(len(opts)//2, *opts)
        case 'optional':
            return Optional(visit(node.children[0]))
        case 'oneOrMore':
            return OneOrMore(visit(node.children[0]))
        case 'zeroOrMore':
            return ZeroOrMore(visit(node.children[0]))
        case 'quantifierBase':
            return visit(node.children[0])
        case 'identifier':
            return text
        case 'terminal':
            t = text.strip('"\'')
            return Terminal(escape(t))
        case _:
            if node.children:
                return visit(node.children[0])
            else:
                return Terminal(escape(text))

def process_rule(rule_node):
    rule_name = rule_node.children[0].text.decode()
    structure = visit(rule_node.children[2])
    return rule_name, Diagram(structure)

def main(input_path):
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'rules:' not in content:
        raise ValueError("No 'rules:' section found in the EBNF file.")
    rules_block = content.split('rules:', 1)[1]

    pattern = re.compile(r'^\s*(?P<name>\w+)\s*::=\s*(?P<expr>.*?)(?=^\s*\w+\s*::=|\Z)', re.M | re.S)
    matches = pattern.finditer(rules_block)

    diagrams = {}
    for m in matches:
        name = m.group('name')
        expr = m.group('expr').strip()
        if not expr.endswith(';'):
            expr += ';'
        rule_source = f"{name} ::= {expr}"
        try:
            tree = ts_parser.parse(rule_source.encode())
            root = tree.root_node
            for child in root.children:
                if child.type == 'rule':
                    try:
                        _, diagram = process_rule(child)
                        diagrams[name] = diagram
                    except Exception as e:
                        print(f"Error processing rule '{name}': {e}")
        except Exception as e:
            print(f"Error parsing source for rule '{name}': {e}")

    output_dir = os.path.join('results', base_name)
    os.makedirs(output_dir, exist_ok=True)

    for name, diagram in diagrams.items():
        try:
            print(f"### Rule: {name}")
            stream = io.StringIO()
            diagram.writeStandalone(stream.write)
            svg = stream.getvalue()
            display(SVG(data=svg))
            with open(os.path.join(output_dir, f"{name}.svg"), 'w', encoding='utf-8') as out:
                out.write(svg)
            print(f"Saved: {os.path.join(output_dir, name + '.svg')}\n")
        except Exception as e:
            print(f"Error displaying/saving diagram for '{name}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate EBNF railroad diagrams')
    parser.add_argument('input_path', help='Path to the EBNF file')
    args = parser.parse_args()
    main(args.input_path)
