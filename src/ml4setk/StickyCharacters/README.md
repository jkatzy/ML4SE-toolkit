# StickyCharacters Analysis Toolkit

A comprehensive toolkit for analyzing tokenization patterns in code, with a focus on identifying "sticky tokens" - tokens that combine both textual and symbolic elements. The toolkit provides multiple analysis methods, GUI interfaces, and automated visualization generation.

## Overview

The StickyCharacters toolkit consists of three main analysis approaches:

1. **Rule-based Analysis** - Traditional pattern matching using predefined rules
2. **Tree-sitter AST Analysis** - Syntax-aware analysis using Abstract Syntax Trees
3. **Grammar-guided Analysis** - Advanced analysis using complete language grammar rules

## Core Features

### Analysis Capabilities
- **Multi-language Support**: Python, JavaScript, Java, C/C++, Go, Rust, Julia, R, SQL, ANTLR
- **Multi-model Support**: CodeLLaMA, StarCoder, WizardCoder, Qwen2.5-Coder, SantaCoder
- **Sticky Token Detection**: Identifies tokens mixing textual and symbolic elements
- **Syntactic Context**: Provides AST-based context for enhanced accuracy
- **Batch Processing**: Analyze multiple files simultaneously

### GUI Interfaces

#### GUI (`gui.py`)
- **Tabbed Interface**: Analysis, Visualization, Results, and Settings tabs
- **Integrated Visualization**: Built-in chart viewer with navigation controls
- **Auto-visualization**: Automatically generates four types of comprehensive charts
- **Advanced Configuration**: Customizable output directories and settings

### Visualization System

The enhanced toolkit automatically generates four types of visualizations:

1. **Summary Dashboard**
   - Bar chart of sticky tokens per file
   - Percentage chart showing sticky token ratios
   - Pie chart of language distribution
   - Scatter plot correlating total vs sticky tokens

2. **Language Comparison**
   - Average sticky ratios across programming languages
   - Total sticky tokens by language
   - File count distribution by language

3. **Token Distribution Heatmap**
   - Raw token statistics heatmap
   - Normalized heatmap for pattern comparison
   - Cross-file analysis of token distribution

4. **Detailed Token Analysis**
   - Most common sticky tokens (horizontal bar chart)
   - Token length distribution histogram
   - Language-specific token patterns matrix
   - Token diversity analysis by file

## Installation

### Core Dependencies
```bash
pip install transformers
pip install tree-sitter
pip install tree-sitter-languages  # or individual language packages
```

### Enhanced Visualization Dependencies
```bash
pip install matplotlib seaborn pandas pillow numpy
```

### Optional Tree-sitter Language Packages
```bash
pip install tree-sitter-python tree-sitter-javascript tree-sitter-java
```

## Usage

### GUI Applications

#### GUI with Visualizations
```bash
python gui.py
```

### GUI Workflow

1. **File Selection**
   - Files are automatically loaded from the `inputs/` directory
   - Select one or more files for analysis
   - Programming language is detected automatically (shown in parentheses)

2. **Model Configuration**
   - Choose from dropdown of common models or enter custom model name
   - Supported models include CodeLLaMA, StarCoder, WizardCoder, etc.

3. **Analysis Options**
   - **Tree-sitter Analysis**: Enable for more accurate syntactic analysis
   - **Auto-visualization**: (Enhanced GUI) Automatically generate charts

4. **Run Analysis**
   - Click "Analyze Selected Files" to start processing
   - Progress bar shows analysis status
   - Results appear in real-time

5. **View Results**
   - **Analysis Tab**: Quick summary and controls
   - **Visualization Tab**: (Enhanced GUI) Integrated chart viewer with navigation
   - **Results Tab**: Detailed analysis results with formatting

6. **Export Results**
   - Save raw JSON data with detailed analysis results
   - Export formatted text reports
   - (Enhanced GUI) Visualizations auto-saved to `visualizations/` directory

### Command Line Usage

#### Basic Analysis
```python
from integrated_sticky_analyzer import IntegratedStickyAnalyzer

analyzer = IntegratedStickyAnalyzer()

# Single file analysis
result = analyzer.analyze_file("python.py", "codellama/CodeLLaMA-7b-hf")

# Multiple files
files = ["python.py", "java.java", "javascript.js"]
results = analyzer.analyze_multiple_files(files, "bigcode/starcoder2-3b")
```

#### Tree-sitter Analysis
```python
from tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer

analyzer = TreeSitterStickyAnalyzer('python')
result = analyzer.analyze_code_tokenization_ast(
    model_name="codellama/CodeLLaMA-7b-hf",
    code="if x.value > threshold: result = process(x.data)"
)
```

#### Grammar-guided Analysis
```python
from grammar_guided_analyzer import GrammarGuidedStickyAnalyzer

analyzer = GrammarGuidedStickyAnalyzer()
result = analyzer.analyze_with_grammar_guidance(
    model_name="bigcode/starcoder2-3b",
    code="if x.value > threshold: result = process(x.data)"
)
```

## Analysis Methods

### 1. Rule-based Analysis (`analyze_merged_tokens.py`)
- Uses predefined pattern matching rules
- Fast processing for large codebases
- Good baseline for comparison studies

### 2. Tree-sitter AST Analysis (`tree_sitter_sticky_analyzer.py`)
- Leverages Abstract Syntax Tree information
- More accurate detection using syntactic context
- Better handling of semantic boundaries

### 3. Grammar-guided Analysis (`grammar_guided_analyzer.py`)
- Uses complete language grammar rules (126 Python rules)
- Identifies 26 types of sticky-related syntax nodes
- Provides confidence scores and detailed context
- Highest accuracy for complex code structures

## Sticky Token Definition

A token is considered "sticky" if it contains both:
1. **Textual elements**: Letters, digits, or keywords
2. **Symbolic elements**: Operators, punctuation, or delimiters

### Examples
- `def(` - keyword + parenthesis
- `import.` - keyword + dot
- `x.value` - identifier + dot + identifier
- `if__name__` - keyword + underscore + identifier
- `process()` - identifier + parentheses

## Output Structure

### Analysis Results
```json
{
  "summary": {
    "total_files": 3,
    "successful_analyses": 3,
    "languages_detected": ["python", "java", "javascript"],
    "total_sticky_tokens": 42,
    "model_name": "codellama/CodeLLaMA-7b-hf"
  },
  "individual_results": [
    {
      "filename": "python.py",
      "language": "python",
      "basic_analysis": {
        "total_tokens": 156,
        "sticky_tokens": ["def(", "import.", "if__name__"],
        "sticky_count": 3
      },
      "tree_sitter_analysis": {
        "sticky_tokens_with_context": [
          {
            "token": "def(",
            "ast_context": "function_definition",
            "detection_rules": ["mixed_alphanumeric_symbols"]
          }
        ]
      }
    }
  ]
}
```

### Visualization Files (Enhanced GUI)
- `summary_[model]_[timestamp].png` - Summary dashboard
- `language_comparison_[model]_[timestamp].png` - Language comparison
- `token_heatmap_[model]_[timestamp].png` - Token distribution heatmap
- `detailed_analysis_[model]_[timestamp].png` - Detailed token analysis
- `visualization_metadata_[timestamp].json` - Chart metadata

## File Structure
```
StickyCharacters/
├── inputs/                          # Input code files
│   ├── python.py, java.java, etc.
├── grammars/                        # Grammar files for analysis
├── results/                         # Analysis results (JSON)
├── visualizations/                  # Auto-generated charts (PNG)
├── analyze_merged_tokens.py         # Rule-based analysis
├── tree_sitter_sticky_analyzer.py  # AST-based analysis
├── grammar_guided_analyzer.py       # Grammar-guided analysis
├── integrated_sticky_analyzer.py   # Unified analysis engine
├── language_detector.py             # Language detection
├── visualization_engine.py          # Chart generation
├── gui_sticky_analyzer.py           # Standard GUI
├── gui_enhanced_analyzer.py         # Enhanced GUI with visualizations
├── demo.py                          # Basic demo
├── demo_enhanced_system.py          # Enhanced system demo
└── test_*.py                        # Test files
```

## Why It Works

### Technical Foundation
1. **Tokenization Analysis**: Uses transformer tokenizers to understand how models split code
2. **Syntactic Context**: Tree-sitter provides accurate AST information
3. **Grammar Rules**: Complete language grammars ensure comprehensive analysis
4. **Multi-modal Detection**: Combines rule-based, AST-based, and grammar-based methods

### Research Applications
- **Model Evaluation**: Compare tokenization behavior across different models
- **Language Analysis**: Study tokenization patterns in different programming languages
- **Syntax Understanding**: Analyze how tokenizers handle complex syntax structures
- **Quality Assessment**: Identify potential tokenization issues in code generation models

## Troubleshooting

### Common Issues
1. **No input files found**: Place files in `inputs/` directory
2. **Tree-sitter errors**: Install language-specific packages
3. **Model loading errors**: Check internet connection and model names
4. **GUI issues**: Ensure tkinter and PIL are installed
5. **Visualization errors**: Install matplotlib, seaborn, and pandas

### Performance Tips
- Use tree-sitter analysis for better accuracy
- Analyze files in batches for efficiency
- Choose appropriate models based on requirements
- Enable auto-visualization only when needed

## Demo Scripts

```bash
# Basic functionality demo
python demo.py

# Enhanced system with visualizations
python demo_enhanced_system.py

# Grammar-guided analysis demo
python demo_grammar_guided.py

# Test visualization system
python test_visualization_system.py
```

## Research Value

The toolkit is designed for Machine Learning for Software Engineering (ML4SE) research:

- **Tokenization Studies**: Understand how different models handle code tokenization
- **Cross-language Analysis**: Compare tokenization patterns across programming languages
- **Model Comparison**: Evaluate tokenization quality across different language models
- **Syntax-aware Analysis**: Study the relationship between code syntax and tokenization
- **Publication-ready Results**: Generate high-quality visualizations for research papers

## Technical Architecture

The system follows a modular design:
- **Analysis Engine**: Core tokenization and detection logic
- **Language Detection**: Automatic programming language identification
- **Visualization Engine**: Comprehensive chart generation system
- **GUI Framework**: User-friendly interfaces for different use cases
- **Export System**: Multiple output formats for different needs

This comprehensive toolkit provides researchers, developers, and students with powerful tools for understanding and analyzing code tokenization patterns in modern language models.