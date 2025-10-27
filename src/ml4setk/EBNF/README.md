# EBNF Utilities (Rule-level Counting + Railroad Visualization)

This folder contains comprehensive tools for analyzing programming language syntax patterns through EBNF (Extended Backus-Naur Form) grammar visualization and rule frequency analysis.

## Features

### 🔍 Rule-level Counting (Tree-sitter Based)
- **Multi-language Support**: Parse source code using Tree-sitter for accurate syntax analysis
- **Dataset Processing**: Handle single files or JSONL datasets (e.g., HumanEval, LCA datasets)
- **Comprehensive Output**: Generate JSON with rule counts, metadata, and optional CSV/Markdown reports
- **Language Coverage**: Support for Python, JavaScript, TypeScript, Java, Go, C/C++, C#, Rust, Ruby, Scala

### 🚂 Railroad Diagram Generation
- **EBNF to SVG**: Convert EBNF grammar files to visual railroad diagrams
- **Batch Processing**: Generate diagrams for multiple languages simultaneously
- **Combined Views**: Compose individual rule SVGs into comprehensive combined diagrams

### 🎨 Frequency-based Visualization
- **Position-aware Coloring**: Color diagram elements based on actual usage frequency in real code
- **Adaptive Labeling**: Dynamic badges showing rule names, counts, and global frequency percentages
- **Smart Matching**: Robust rule name normalization and alias mapping for accurate visualization

### 📊 Integrated Analysis Workflow
- **Complete Pipeline**: From raw code to colored visualizations in a single command
- **Multiple Output Formats**: JSON, CSV, SVG, and Markdown reports
- **Comparative Analysis**: Support for analyzing multiple datasets with consistent methodology

## Installation

### Prerequisites
- Python 3.9+ recommended
- Required packages:
```bash
pip install tree-sitter-languages
pip install tree-sitter tree-sitter-python  # Optional fallbacks
```

### Verification
Test your installation:
```bash
python src/ml4setk/EBNF/rule_counter.py --help
```

## Quick Start

### 1. Basic Rule Counting

**Single File Analysis:**
```bash
python src/ml4setk/EBNF/rule_counter.py path/to/file.py \
    --language python \
    --output counts.json
```

**JSONL Dataset Analysis:**
```bash
python src/ml4setk/EBNF/rule_counter.py data/HumanEval.jsonl \
    --language python \
    --output humaneval_treesitter.json \
    --code-fields prompt canonical_solution
```

### 2. Complete Analysis Workflow

**Using Integrated Processor:**
```bash
python src/ml4setk/EBNF/integrated_rule_processor.py data/dataset.jsonl \
    --language python \
    --work-dir results \
    --base-name dataset_analysis
```

### 3. Visualization Generation

**Basic Railroad Diagrams:**
```bash
python src/ml4setk/EBNF/visualize_grammars.py --languages python
```

**Frequency-colored Diagrams:**
```bash
python src/ml4setk/EBNF/visualize_grammars.py \
    --languages python \
    --counts-json path/to/counts.json
```

## Complete Workflow Example

Here's a complete example analyzing a dataset from start to finish:

```bash
# Step 1: Prepare your JSONL file (ensure proper JSON format)
# Each line should be valid JSON with a "code" field

# Step 2: Count rules using tree-sitter
cd src/ml4setk/EBNF
python rule_counter.py data/your_dataset.jsonl \
    --output ../../../your_dataset_treesitter.json \
    --language python \
    --code-fields code

# Step 3: Generate colored visualizations
python visualize_grammars.py \
    --languages python \
    --counts-json ../../../your_dataset_treesitter.json

# Step 4: View results
# - Tree-sitter counts: your_dataset_treesitter.json
# - Standard diagrams: visualization/python/combined.svg
# - Colored diagrams: visualization/python/colored_combined.svg
```

## Output Structure

### Generated Files
```
├── your_dataset_treesitter.json          # Rule counts with metadata
├── visualization/python/
│   ├── rules/                            # Individual rule SVGs
│   ├── combined.svg                      # All rules in one diagram
│   ├── colored/                          # Frequency-colored rule SVGs
│   └── colored_combined.svg              # Colored complete diagram
└── results/                              # Optional detailed reports
    ├── counts/
    ├── csv/
    └── reports/
```

### JSON Output Format
```json
{
  "metadata": {
    "language": "python",
    "total_rules": 171,
    "total_occurrences": 498657,
    "parser_used": "tree-sitter (tree-sitter-languages:python)"
  },
  "rule_counts": {
    "identifier": 106342,
    "\"": 33784,
    ",": 24094,
    ...
  }
}
```

## CLI Reference

### rule_counter.py
**Purpose**: Count grammar rules in source code using tree-sitter

**Usage**:
```bash
python rule_counter.py INPUT [OPTIONS]
```

**Arguments**:
- `INPUT`: Source file or JSONL dataset path

**Options**:
- `--language LANG`: Target language (python, javascript, java, etc.)
- `--output FILE`: Output JSON file path
- `--code-fields FIELD [FIELD ...]`: JSONL fields containing code (default: prompt, canonical_solution)
- `--top-n N`: Number of top rules to display in summary

### visualize_grammars.py
**Purpose**: Generate railroad diagrams with optional frequency coloring

**Usage**:
```bash
python visualize_grammars.py [OPTIONS]
```

**Options**:
- `--languages LANG1,LANG2`: Comma-separated language list (default: all available)
- `--counts-json FILE`: Rule counts JSON for frequency-based coloring

### integrated_rule_processor.py
**Purpose**: Complete analysis workflow from code to reports

**Usage**:
```bash
python integrated_rule_processor.py INPUT [OPTIONS]
```

**Options**:
- `--language LANG`: Programming language
- `--work-dir DIR`: Output directory for all results
- `--base-name NAME`: Base name for output files

## Supported Languages

| Language   | Aliases        | Tree-sitter Support | EBNF Available |
|------------|----------------|-------------------|----------------|
| Python     | py             | ✅                | ✅             |
| JavaScript | js, node       | ✅                | ✅             |
| TypeScript | ts             | ✅                | ❌             |
| Java       | -              | ✅                | ✅             |
| Go         | golang         | ✅                | ✅             |
| C          | -              | ✅                | ✅             |
| C++        | cpp            | ✅                | ✅             |
| C#         | csharp, cs     | ✅                | ✅             |
| Rust       | -              | ✅                | ❌             |
| Ruby       | -              | ✅                | ❌             |
| Scala      | -              | ✅                | ✅             |

## Advanced Features

### Frequency-based Coloring
The visualization system uses sophisticated coloring algorithms:

1. **Global Frequency Calculation**: `f = count / total_occurrences`
2. **Nonlinear Boost**: `f_adj = f ** 0.35` for better visual distinction
3. **HSL Color Mapping**: `hue = 120 * f_adj` (red → yellow → green)
4. **Position-aware Application**: Colors applied to specific diagram elements

### Rule Name Normalization
Robust matching system for accurate coloring:
- Case normalization (lowercase)
- Underscore prefix removal
- Space/dash to underscore conversion
- Simple singularization (statements → statement)
- Language-specific alias mapping

### Python-specific Aliases
```python
aliases = {
    "suite": "block",
    "statement": ["expression_statement", "return_statement", "if_statement", ...],
    "simple_statement": ["expression_statement", "assignment", "pass_statement", ...],
    "compound_statement": ["if_statement", "for_statement", "while_statement", ...],
    "dotted_name": "identifier"
}
```

## Data Processing Guidelines

### JSONL Format Requirements
Ensure your JSONL files have proper format:
```json
{"code": "def example():\n    return 42", "id": "sample_1"}
{"code": "print('hello world')", "id": "sample_2"}
```

### Common Issues and Solutions

**Issue**: "No rules were counted"
- **Solution**: Check JSONL format, ensure `--code-fields` matches your data structure

**Issue**: Tree-sitter language not found
- **Solution**: Install `tree-sitter-languages` or verify language name spelling

**Issue**: Colors appear too red/uniform
- **Solution**: Verify counts JSON matches target language, check rule name alignment

## Examples

### HumanEval Dataset Analysis
```bash
# Complete analysis of HumanEval dataset
python rule_counter.py data/HumanEval.jsonl \
    --language python \
    --output humaneval_treesitter.json \
    --code-fields prompt canonical_solution

python visualize_grammars.py \
    --languages python \
    --counts-json humaneval_treesitter.json
```

### Custom Dataset Processing
```bash
# For datasets with "code" field
python rule_counter.py data/custom_dataset.jsonl \
    --language python \
    --output custom_treesitter.json \
    --code-fields code

# For datasets with multiple code fields
python rule_counter.py data/multi_field_dataset.jsonl \
    --language python \
    --output multi_treesitter.json \
    --code-fields solution test_code example_code
```

### Multi-language Analysis
```bash
# Analyze the same dataset for different languages
python rule_counter.py data/polyglot_dataset.jsonl \
    --language python \
    --output python_analysis.json

python rule_counter.py data/polyglot_dataset.jsonl \
    --language javascript \
    --output javascript_analysis.json

# Generate comparative visualizations
python visualize_grammars.py \
    --languages python,javascript \
    --counts-json python_analysis.json
```

## Extending the System

### Adding New Languages

1. **For Counting**: Ensure tree-sitter support via `tree-sitter-languages`
2. **For Visualization**: Add `<language>.ebnf` file to `ebnfs/` directory
3. **For Better Coloring**: Extend alias mapping in `color_visualization.py`

### Custom Analysis Workflows

Create custom processors by extending `integrated_rule_processor.py`:
```python
from integrated_rule_processor import IntegratedRuleProcessor

class CustomProcessor(IntegratedRuleProcessor):
    def custom_analysis(self, counts):
        # Your custom analysis logic
        pass
```

## Repository Structure

```
src/ml4setk/EBNF/
├── rule_counter.py              # Core tree-sitter rule counting
├── visualize_grammars.py        # Railroad diagram generation
├── integrated_rule_processor.py # Complete workflow processor
├── color_visualization.py       # Frequency-based coloring
├── combine_svg.py              # SVG composition utilities
├── ebnf.py                     # EBNF to SVG conversion
├── ebnfs/                      # EBNF grammar definitions
│   ├── python.ebnf
│   ├── javascript.ebnf
│   └── ...
├── data/                       # Sample datasets
├── results/                    # Generated analysis results
└── RRD/                       # Railroad diagram library
```

## Performance Notes

- **Large Datasets**: Processing time scales linearly with dataset size
- **Memory Usage**: Tree-sitter parsing is memory-efficient for most datasets
- **Visualization**: SVG generation may be slow for very large grammars
- **Optimization**: Use `--top-n` for quick summaries of large analyses

## Contributing

To contribute new features or improvements:

1. **Language Support**: Add EBNF files and test with sample code
2. **Visualization**: Enhance coloring algorithms or diagram layouts  
3. **Analysis**: Extend reporting capabilities or add new metrics
4. **Documentation**: Improve examples and troubleshooting guides

## License

This project is part of the ML4SE-toolkit. See the main repository LICENSE for details.