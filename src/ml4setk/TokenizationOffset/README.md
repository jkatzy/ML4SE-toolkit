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