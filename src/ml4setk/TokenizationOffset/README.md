# Tree-sitter Rule-level Alignment Score Analysis Tool User Guide

This document provides detailed instructions on how to use the Tree-sitter Rule-level Alignment Score analysis tool.

## Project Introduction

This project is a multilingual Tree-sitter rule-level alignment score analyzer, used to calculate the alignment degree between code syntax rules and tokenization boundaries. The tool supports 11 programming languages and can generate detailed analysis reports and visualization charts.

## Environment Setup

### 1. Install Dependencies

First, you need to install all necessary dependency packages:

```bash
pip install -r requirements.txt
```

Main dependencies include:
- tree-sitter: Tree-sitter Python bindings
- transformers: Hugging Face model library
- torch: PyTorch deep learning framework
- pandas: Data processing
- matplotlib: Chart drawing
- seaborn: Statistical charts

### 2. Ensure Language Libraries are Compiled

The project uses pre-compiled Tree-sitter language libraries, which should be located in the `build/` directory.

## Usage Instructions

### 1. Run Environment Test

Before starting analysis, it is recommended to run the test script to ensure the environment is configured correctly:

```bash
python test.py
```

This command will test core functionality and the code sample directory to ensure everything works properly.

### 2. Run Analysis

#### Basic Analysis (Python only by default)

```bash
python analyzer.py
```

#### Analyze a Specific Language

```bash
python analyzer.py --language javascript
```

#### Analyze All Supported Languages

```bash
python analyzer.py --all_languages
```

#### Specify Code Sample Directory and Output Directory

```bash
python analyzer.py --code_dir path/to/code --output_dir path/to/output
### 2. Read Code From HuggingFace Datasets (New)

You can analyze code loaded directly from HuggingFace Datasets via new CLI flags. This supports both fixed-language mode and per-sample language fields, and works in streaming mode by default to save memory.

- Basic flags:
  - `--hf_dataset`: dataset name on the Hub (e.g., `code_x_glue_ct_code_to_text`, `mbpp`)
  - `--hf_config`: optional dataset config name (e.g., `python`, `java`)
  - `--hf_split`: split to analyze (default: `train`)
  - `--hf_text_column`: column containing code text (defaults to `content`; many datasets use `code`)
  - `--hf_language`: fixed language for all samples (e.g., `python`, `javascript`)
  - `--hf_language_field`: per-sample field name containing language label (choose one of `--hf_language` or `--hf_language_field`)
  - `--hf_limit`: limit number of samples for quick runs
  - `--hf_streaming` / `--no_hf_streaming`: enable/disable streaming (default: enabled)
  - `--hf_token`: auth token if the dataset is gated

- Example: CodeXGLUE code-to-text (open dataset), Python split:
  ```bash
  python analyzer.py \
    --hf_dataset code_x_glue_ct_code_to_text \
    --hf_config python \
    --hf_split train \
    --hf_text_column code \
    --hf_language python \
    --hf_limit 500
  ```

- Example: CodeXGLUE code-to-text, Java split:
  ```bash
  python analyzer.py \
    --hf_dataset code_x_glue_ct_code_to_text \
    --hf_config java \
    --hf_split train \
    --hf_text_column code \
    --hf_language java \
    --hf_limit 500
  ```

- Example: MBPP (Python, open dataset):
  ```bash
  python analyzer.py \
    --hf_dataset mbpp \
    --hf_split train \
    --hf_text_column code \
    --hf_language python \
    --hf_limit 200
  ```

Notes:
- Language aliases are normalized: `js`→`javascript`, `c++/cpp/cxx`→`cpp`, `c#/cs`→`csharp`, `golang`→`go`, etc. Only languages with available compiled parsers will be analyzed.
- Results, rankings, and saved reports share the same format and output directory as local-file analysis (`results/multilang`).
- For gated datasets, request access on the dataset page or pass `--hf_token` if you already have access.

```

### 3. Generate Visualization Charts

After analysis is complete, you can generate visualization charts:

```bash
python visualize_multilang_results.py
```

This will generate various charts, including language ranking charts, rule count vs. alignment rate scatter plots, language category analysis charts, and a comprehensive dashboard.

### 4. Use the Unified Run Script

The project provides a unified run script `run.py` that integrates testing, analysis, and visualization functions:

```bash
# Run environment test
python run.py --test

# Run analysis for all languages
python run.py --analyze

# Analyze only a specific language
python run.py --language python

# Generate visualization charts
python run.py --visualize

# Run all functions
python run.py --all

# Analyze a specific language and generate charts
python run.py --language python --visualize
```

## Analysis Results

The analyzer will output the following information:

### Console Output
- Alignment scores and rankings for each language
- Detailed rule matching information
- Cross-language comparative analysis
- Real-time progress display

### Generated Files
- **Detailed Report**: `results/multilang/detailed_analysis_gpt2.json`
- **Ranking Report**: `results/multilang/language_rankings_gpt2.json`
- **Cross-language Comparison**: `results/multilang/cross_language_report_gpt2.json`
- **Language-specific Reports**: `results/multilang/{language}/analysis_report_gpt2.json`
- **Visualization Charts**: 
  - `results/multilang/language_ranking_chart.png`
  - `results/multilang/rules_vs_alignment_scatter.png`
  - `results/multilang/language_category_analysis.png`
  - `results/multilang/comprehensive_dashboard.png`

## Supported Languages

The tool supports the following 11 programming languages:

1. Python (.py)
2. JavaScript (.js)
3. TypeScript (.ts)
4. Java (.java)
5. C (.c, .h)
6. C++ (.cpp, .cc, .cxx, .hpp)
7. C# (.cs)
8. Go (.go)
9. Ruby (.rb)
10. Rust (.rs)
11. Scala (.scala)

## Project File Structure

```
TokenizationOffset/
├── analyzer.py                # Main analyzer
├── visualize_multilang_results.py  # Visualization tool
├── test.py                   # Basic test script
├── run.py                    # Unified run script
├── README_multilang.md       # Usage documentation
├── requirements.txt          # Dependencies list
├── build/                    # Compiled language libraries
├── code_samples/             # Test code samples
└── results/                  # Analysis results
```

## Troubleshooting Common Issues

1. **Language library not found**: Ensure that the compiled language library files are present in the `build/` directory.

2. **Code samples do not exist**: Ensure that the `code_samples/` directory contains code samples for each language.

3. **Dependency installation issues**: Ensure that all dependencies are correctly installed with `pip install -r requirements.txt`.

4. **Visualization chart generation failure**: Check if the necessary analysis result files exist in the `results/multilang/` directory.

## Advanced Usage

### Custom Tokenizer Models

By default, the GPT-2 tokenizer is used. You can specify other models:

```bash
python analyzer.py --model bert-base-uncased
```

### Adding Support for New Programming Languages

To add support for a new programming language:

1. Obtain the corresponding Tree-sitter language library
2. Compile the language library to the `build/` directory
3. Add language configuration to the `language_configs` dictionary in `analyzer.py`
4. Prepare test code samples
5. Verify analysis functionality