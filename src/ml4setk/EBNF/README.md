# EBNF Utilities (Rule-level Counting + Railroad Visualization)

This folder contains tools to:
- Parse source code with Tree-sitter and count grammar rules at the rule-level
- Support multiple languages via a single `--language` switch
- Generate Railroad diagrams from EBNF grammars
- Color Railroad diagrams by per-rule frequency (position-aware), with adaptive labels

All outputs are designed to be machine-friendly (JSON/CSV) and human-friendly (SVG/Markdown).

## Features

- Rule-level counting (Tree-sitter only)
  - Parse source code to Tree-sitter AST and count node types (rules)
  - Single file or JSONL datasets (e.g., HumanEval) supported
  - Multi-language via `--language` (e.g., `python`, `javascript`, ...)
  - Outputs JSON with rule counts and metadata, optional summary printing/CSV

- Railroad diagram generation
  - Generate per-rule SVGs from EBNF (`src/ml4setk/EBNF/ebnfs/*.ebnf`)
  - Compose all rule SVGs into a combined SVG for quick browsing

- Frequency-based diagram coloring (position-aware)
  - Read a counts JSON and color each rule diagram
  - Position-aware: color terminals/nonterminals inside each rule based on their own (or group/alias) frequencies
  - Adaptive top-left badges show “rule_name: count (global frequency%)”
  - Robust matching: case/underscore normalization, simple singularization, alias mapping (Python included)

## Installation

Prerequisites:
- Python 3.9+ recommended
- pip packages:
  - Tree-sitter bindings and language pack
    - `pip install tree-sitter-languages`
    - Optionally: `pip install tree-sitter tree-sitter-python` (fallbacks where applicable)

Notes:
- The tools prefer `tree-sitter-languages` to load multiple languages easily.
- EBNF to Railroad pipeline is implemented in this repo; no extra installation should be needed.

## Quick Start

Count rules for a single file:
```bash
python src/ml4setk/EBNF/rule_counter.py path/to/file.py --language python --output counts.json
```

Count rules for a JSONL dataset (default fields include prompt/canonical_solution):
```bash
python src/ml4setk/EBNF/rule_counter.py data/HumanEval.jsonl --language python --output humaneval_counts.json --top-n 15
```

Generate Railroad diagrams for one or more languages (based on EBNF files present):
```bash
python src/ml4setk/EBNF/visualize_grammars.py --languages python
```

Generate and color Railroad diagrams using rule counts:
```bash
python src/ml4setk/EBNF/visualize_grammars.py --languages python --counts-json src/ml4setk/EBNF/humaneval_rule_counts_treesitter.json
```

Outputs will be placed under:
- `visualization/<language>/rules/*.svg` (per-rule)
- `visualization/<language>/combined.svg`
- `visualization/<language>/colored/*.svg` (frequency-colored)
- `visualization/<language>/colored_combined.svg`

## CLI Reference

rule_counter.py:
- Positional:
  - `INPUT_PATH`: source file or JSONL
- Options:
  - `--language <lang>`: e.g., `python`, `javascript`, `typescript`, `java`, `go`, `cpp`, `c`, `csharp`, `rust`, `ruby`, `scala` (availability depends on `tree-sitter-languages`)
  - `--output <file.json>`: where to write counts JSON
  - `--top-n <int>`: print top-N summary (console)
  - Other defaults: counts JSON may include metadata for provenance

visualize_grammars.py:
- Options:
  - `--languages <lang1,lang2,...>`: select subset to visualize (default: all EBNFs found)
  - `--counts-json <file.json>`: if provided, color each rule SVG based on frequencies; also generate `colored_combined.svg`

## Output Formats

Counts JSON (accepted/produced):
- Either a flat dictionary `{ "rule": count, ... }`
- Or nested `{ "rule_counts": { ... } }`
- Or `{ "counts": { ... }, "metadata": { ... } }`
- The coloring pipeline supports all three forms transparently

Colored SVGs:
- Per-rule SVGs are modified in-place for coloring (style fill + fill attribute + stroke safeguard)
- Top-left adaptive badge shows `rule_name: total_count (global_frequency%)`
- Position-aware coloring applies to terminals/nonterminals inside each rule

## Coloring Details

- Frequency basis: global frequency
  - For any key, `f = count / total_occurrences` (across the entire dataset)
  - Nonlinear boost for visual clarity: `f_adj = f ** 0.35`
  - Hue mapping: `h = 120 * f_adj` (HSL), higher frequency → greener
- Position-aware key resolution per element:
  1) Use `rect[data-text]` if present and meaningful
  2) Otherwise, use the nearest group text(s) (recursively collected)
  3) Normalize keys: lowercase, strip leading `_`, spaces/dashes → `_`, simple singularization (e.g., `statements → statement`)
  4) Alias mapping (per language). For Python:
     - `suite → block`
     - `statement →` union of many statement node types (expression_statement, return_statement, if_statement, for_statement, while_statement, try_statement, with_statement, class_definition, function_definition, import_statement, raise_statement, pass_statement, break_statement, continue_statement, delete_statement, global_statement, nonlocal_statement, assert_statement, type_alias_statement, exec_statement)
     - `simple_statement →` simple statement subset
     - `compound_statement →` compound statement subset
     - `dotted_name → identifier`
  5) Fallback: rule-file name’s total count
- “Noisy” keys (e.g., `~1` or purely symbol/number text) are ignored as non-semantic

## Multi-language Support

Counting:
- `rule_counter.py` uses Tree-sitter for all languages; no AST fallback. If the language cannot be loaded, it will raise an error.
- Language normalization is supported (e.g., `js → javascript`, `c# → csharp`, `c++ → cpp`).

Visualization:
- Requires a corresponding EBNF file under `src/ml4setk/EBNF/ebnfs/<language>.ebnf`
- To add a new language visualization:
  1) Provide `<language>.ebnf` in `ebnfs/`
  2) Run `visualize_grammars.py --languages <language>`
  3) Optionally provide counts via `--counts-json` for coloring

Coloring alias maps:
- Extend `src/ml4setk/EBNF/color_visualization.py` function `_alias_map(lang)` to add language-specific rule mappings, so diagram nodes align with Tree-sitter node types.

## Troubleshooting

- Tree-sitter cannot load the language
  - Ensure `pip install tree-sitter-languages`
  - If still failing, install language-specific packages (e.g., `tree-sitter-python`) or ensure the project’s prebuilt `.so` is available.
- Colors do not change
  - Make sure `--counts-json` is provided
  - Ensure the counts file matches the target language
  - Consider extending `_alias_map` for better rule name alignment
- Colors seem “too red”
  - This is often due to unmatched keys falling back to small totals; improve alignment via aliasing
  - We also apply a nonlinear boost (`f ** 0.35`) to make mid-high frequencies more green
- Badge overlaps content
  - Badge is adaptive to viewBox and text length, with smaller font and semi-transparent background. If still intrusive, relocate or tune margins in `_add_badge`.

## Examples

HumanEval (Python):
```bash
# Count
python src/ml4setk/EBNF/rule_counter.py data/HumanEval.jsonl --language python --output src/ml4setk/EBNF/humaneval_rule_counts_treesitter.json --top-n 15

# Visualize + Color
python src/ml4setk/EBNF/visualize_grammars.py --languages python --counts-json src/ml4setk/EBNF/humaneval_rule_counts_treesitter.json
```

Inspect outputs:
- `visualization/python/combined.svg`
- `visualization/python/colored/*.svg`
- `visualization/python/colored_combined.svg`

## Extending

- Add new languages to counting
  - Ensure Tree-sitter grammar is available via `tree-sitter-languages`
- Add new languages to visualization
  - Supply `<language>.ebnf` under `ebnfs/`
- Improve aliasing/normalization
  - Edit `_alias_map` and normalization utilities in `color_visualization.py`
  - Add tests/fixtures as needed

## Repository Layout (relevant)

- `rule_counter.py` — Tree-sitter based rule counting (multi-language)
- `visualize_grammars.py` — Batch EBNF → Railroad → Combined; optional coloring
- `color_visualization.py` — Position-aware coloring and adaptive badges
- `ebnfs/` — Language EBNF definitions
- `results/` — Raw per-language rule SVGs generated by `ebnf.py`
- `visualization/` — Final per-language outputs (rules, combined, colored, colored_combined)