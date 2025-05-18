# EBNF Tools

## EBNF Railroad Diagram Generator

The `ebnf.py` script generates railroad diagrams from EBNF grammar files.

### Usage

```bash
python ebnf.py input_path
```

### Arguments

- `input_path`: Path to the EBNF grammar file

### Example

```bash
python ebnf.py grammars/scala.ebnf
```

This will:
1. Read the EBNF grammar file
2. Generate railroad diagrams for each grammar rule
3. Save individual SVG files in the `results/[grammar_name]` directory
4. Display the diagrams in Jupyter notebook (if running in Jupyter)

## SVG Diagram Combiner

The `combine_svg.py` script combines multiple SVG files into a single large SVG file, which is useful for viewing and sharing EBNF grammar diagrams.

### Usage

```bash
python combine_svg.py input_directory output_path
```

### Arguments

- `input_directory`: Directory containing the individual SVG files to be combined
- `output_path`: Path where the combined SVG file will be saved

### Example

```bash
python combine_svg.py results/lua results/lua/combined.svg
```

This will:
1. Read all SVG files from the `results/lua` directory
2. Combine them into a single SVG file
3. Save the result as `combined.svg` in the `results/lua` directory

### Features

- Automatically arranges diagrams vertically
- Adds titles for each grammar rule
- Maintains original styling and formatting
- Preserves diagram readability
- Handles errors gracefully

## SVG Coloring Tool

The `svg_coloring.py` script colors SVG diagrams based on usage count data from CSV files. This is useful for visualizing the frequency of different grammar rules in your codebase.

### Usage

```bash
python svg_coloring.py --svg-dir <svg_directory> --csv-dir <csv_directory> --out-dir <output_directory>
```

### Arguments

- `--svg-dir`: Directory containing the input SVG files
- `--csv-dir`: Directory containing CSV files with count data
- `--out-dir`: Directory where the colored SVG files will be saved

### Example

```bash
python svg_coloring.py --svg-dir results/lua --csv-dir data/lua --out-dir results/lua_colored
```

This will:
1. Read SVG files from the `results/lua` directory
2. Read corresponding count data from CSV files in the `data/lua` directory
3. Color the SVG diagrams based on the count data (higher counts = more green, lower counts = more red)
4. Save the colored SVG files in the `results/lua_colored` directory

### CSV Format

The CSV files should have the following format:
```csv
name,count
rule_name,count_value
```

Each CSV file should correspond to an SVG file with the same base name.

## Fake Data Generator

The `fake_data_generator.py` script generates fake count data for SVG files and saves them as CSV files. This is useful for testing and demonstration purposes when you don't have real usage data.

### Usage

```bash
python fake_data_generator.py --svg-dir <svg_directory> --fake-csv-dir <csv_directory> [--global-max <max_count>] [--random-seed <seed>]
```

### Arguments

- `--svg-dir`: Directory containing the input SVG files (required)
- `--fake-csv-dir`: Directory where the generated CSV files will be saved (required)
- `--global-max`: Maximum count value (optional, if not specified, will be randomly generated between 20 and 100)
- `--random-seed`: Random seed for reproducibility (optional)

### Example

```bash
python fake_data_generator.py --svg-dir results/lua --fake-csv-dir fake_csv/lua --global-max 50 --random-seed 42
```

This will:
1. Read SVG files from the `results/lua` directory
2. Extract grammar rule names from the SVG files
3. Generate random count data for each rule (between 1 and global_max)
4. Save the generated data as CSV files in the `fake_csv/lua` directory

The generated CSV files will have the same base names as their corresponding SVG files and will follow the same format as required by the SVG Coloring Tool.

## Real Data Processor

The `real_data_processor.py` script processes real code data from JSONL files (like HumanEval), extracts AST node types, and colors SVG diagrams based on the frequency of grammar rules in the code.

### Usage

```bash
python real_data_processor.py --jsonl-path <jsonl_file> --svg-dir <svg_directory> --csv-dir <csv_directory> --out-dir <output_directory>
```

### Arguments

- `--jsonl-path`: Path to the JSONL file containing real code data (required)
- `--svg-dir`: Directory containing input SVG files (required)
- `--csv-dir`: Directory to save generated CSV files with counts (required)
- `--out-dir`: Directory to save colored SVG files (required)

### Example

```bash
python real_data_processor.py --jsonl-path data/humaneval.jsonl --svg-dir results/python --csv-dir real_csv/humaneval --out-dir results/humaneval_colored
```

This will:
1. Read the JSONL file containing real code data
2. Extract and count AST node types from the code
3. Generate a CSV file with grammar rule counts
4. Color the SVG diagrams based on the frequency of each grammar rule
   - Higher frequency = more green
   - Lower frequency = more red
5. Save the colored SVG files in the output directory

### Features

- Processes real code data from JSONL files
- Extracts AST node types and their frequencies
- Generates grammar rule counts
- Colors SVG diagrams based on usage frequency
- Handles errors gracefully
- Preserves original SVG styling and formatting

# EBNF Conversion Tools

This directory contains tools for working with EBNF (Extended Backus-Naur Form) grammars.

## Converting Tree-sitter Grammars to EBNF

The `tree-sitter-ebnf-generator` directory contains a Node.js script that converts tree-sitter grammar files (`.js`) to EBNF format. To convert all grammar files:

1. Make sure you have Node.js installed
2. Run the conversion script:
   ```bash
   ./convert_grammars.sh
   ```

This will:
- Install necessary dependencies if they're not already installed
- Convert all `.js` files in the `grammars` directory to EBNF format
- Save the converted files in the `ebnfs` directory with `.ebnf` extension

## Manual Conversion

If you need to convert a single grammar file manually:

1. Navigate to the js directory:
   ```bash
   cd tree-sitter-ebnf-generator/src/js
   ```

2. Install dependencies (if not already installed):
   ```bash
   npm install
   ```

3. Run the conversion script:
   ```bash
   node tree_sitter_to_ebnf_new.js /path/to/grammar.js > output.ebnf
   ```

## Directory Structure

- `grammars/`: Contains tree-sitter grammar files (`.js`)
- `ebnfs/`: Contains converted EBNF files
- `tree-sitter-ebnf-generator/`: Contains the conversion script and its dependencies 