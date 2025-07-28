# Grammar-Tokenization Alignment Analysis

This project quantifies the misalignment between programming language grammar boundaries (as defined by tree-sitter) and tokenization boundaries of various Large Language Models (LLMs). This analysis is crucial for understanding how well different LLMs handle code structure, which impacts their code generation and understanding capabilities.

## Problem Statement

When we use tree-sitter to parse code into syntactic blocks and feed these blocks to LLMs, the block boundaries may fall in the middle of an LLM token. This misalignment can potentially affect the quality of model generation and understanding. This project measures this misalignment across different programming languages and LLM models.

## Supported Languages

The analysis currently supports the following programming languages:
- Python
- JavaScript
- TypeScript
- Java
- C
- C++
- C# (csharp)
- Go
- Ruby
- Rust
- Scala

## Supported Models

By default, the analysis tests the following models:
- `gpt2` (as a baseline general-purpose model)
- `codellama/CodeLlama-7b-hf` (Meta's code-optimized model)
- `bigcode/starcoder2-3b` (BigCode project by ServiceNow & Hugging Face)

You can specify any Hugging Face model that has a tokenizer with offset mapping support.

## Project Structure

```
grammar-tokenization-alignment/
├── main.py                   # Main analysis script
├── visualize_tokens.py       # Script to visualize tokenization
├── detailed_analysis.py      # Script for detailed analysis
├── code_samples/             # Sample code files for different languages
│   ├── python/
│   ├── javascript/
│   ├── typescript/
│   └── ...
├── requirements.txt          # Project dependencies
├── results/                  # Analysis results (CSV, charts)
└── vendor/                   # Tree-sitter language repositories
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/grammar-tokenization-alignment.git
cd grammar-tokenization-alignment
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Analysis

Run the basic analysis with default settings (Python language, default models):

```bash
python main.py
```

Specify a different language:

```bash
python main.py --language javascript
```

Specify a specific model:

```bash
python main.py --model codellama/CodeLlama-7b-hf
```

Specify a custom code path:

```bash
python main.py --code_path path/to/your/code
```

Combine options:

```bash
python main.py --language java --model gpt2 --code_path code_samples/java
```

### Token Visualization

Visualize how a model tokenizes code:

```bash
python visualize_tokens.py --model gpt2 --language python
```

You can also specify a specific file to visualize:

```bash
python visualize_tokens.py --model codellama/CodeLlama-7b-hf --file code_samples/rust/example.rs
```

### Detailed Analysis

For a more in-depth analysis of misalignments:

```bash
python detailed_analysis.py --language typescript
```

This will generate detailed reports about which types of syntax nodes are most frequently misaligned with tokenization boundaries.

## Understanding the Results

### Alignment Score

The alignment score is calculated as:
```
alignment_score = (1 - mismatched_boundaries / grammar_boundaries) * 100
```

A higher score indicates better alignment between the model's tokenization and the language's grammar structure.

### Output Files

The analysis generates several output files in the `results/` directory:

1. **CSV Reports**:
   - `alignment_report_{language}.csv`: Contains alignment scores for each model and file

2. **Charts**:
   - `alignment_chart_{language}_by_model.png`: Bar chart comparing models' alignment scores
   - `alignment_chart_{language}_by_file.png`: Bar chart comparing alignment across different files

3. **Detailed Analysis** (when using `detailed_analysis.py`):
   - JSON files with detailed information about each misalignment
   - Charts showing which syntax node types are most frequently misaligned
   - Summary statistics in `results/{language}_detailed/summary.csv`

## Interpreting the Results

- **Higher alignment scores** indicate that the model's tokenization better respects the syntactic structure of the code.
- **Code-specialized models** (like CodeLlama and StarCoder) typically show better alignment than general-purpose models.
- **Different languages** may show varying degrees of alignment with the same model, reflecting how well the model's tokenization strategy works for that language.
- **Certain syntax constructs** may consistently show misalignment across models, indicating fundamental challenges in tokenizing those structures.

## Adding New Languages

To add support for a new language:

1. Add the language to the `SUPPORTED_LANGUAGES` dictionary in the scripts
2. Add appropriate Tree-sitter repository information in `get_tree_sitter_repo_info()`
3. Create sample code files in `code_samples/{language}/`
4. Run the analysis with the new language

## Adding New Models

To test with a new model:

```bash
python main.py --model organization/model-name --language python
```

The model must be available on Hugging Face and have a tokenizer that supports offset mapping.

## Troubleshooting

### Common Issues

1. **Tree-sitter compilation errors**:
   - Make sure you have a C compiler installed
   - Check if the specified language version is compatible with your tree-sitter version

2. **Model loading errors**:
   - Ensure you have sufficient disk space for model downloads
   - Check your internet connection for downloading models

3. **Memory issues with large models**:
   - Use smaller models or reduce the batch size
   - Consider using a machine with more RAM

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.