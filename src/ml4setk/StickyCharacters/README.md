# StickyCharacters Analysis Toolkit

This toolkit provides tools for analyzing tokenization patterns in code, with a focus on identifying "sticky tokens" - tokens that combine both textual and symbolic elements. The toolkit supports multiple programming languages including Python, JavaScript, Java, and ANTLR.

## Files Overview

### 1. analyze_merged_tokens.py
The main analysis tool that examines code tokenization patterns using various language models.

**Features:**
- Supports multiple programming languages (Python, JavaScript, Java, ANTLR)
- Analyzes tokenization using different language models
- Identifies sticky tokens in code
- Generates detailed analysis reports

**Usage:**
```python
# Direct script execution
python analyze_merged_tokens.py

# As a module
from ml4setk.StickyCharacters.analyze_merged_tokens import analyze_code_tokenization, run_experiment

# Analyze single code snippet
result = analyze_code_tokenization(
    model_name="codellama/CodeLLaMA-7b-hf",
    code="your_code_here",
    language="antlr"  # or 'python', 'javascript', 'java'
)

# Run full experiment
run_experiment(
    model_names=["codellama/CodeLLaMA-7b-hf"],
    code_samples=["your_code_here"],
    languages=["antlr"],
    output_prefix="your_analysis"
)
```

### 2. save_vocab.py
A utility tool for saving model vocabularies to text files.

**Features:**
- Extracts vocabulary from specified language models
- Saves tokens and their IDs to a text file
- Supports any model from the Hugging Face transformers library

**Usage:**
```bash
# Command line usage
python save_vocab.py --model_name "bigcode/starcoder2-3b"

# As a module
from ml4setk.StickyCharacters.save_vocab import save_vocab_to_file
save_vocab_to_file("bigcode/starcoder2-3b")
```

### 3. visualize_results.py
A visualization tool for analyzing and displaying tokenization results.

**Features:**
- Creates various plots for token analysis
- Generates sticky tokens comparison charts
- Shows token distribution patterns
- Provides language-specific comparisons

**Usage:**
```bash
# Direct execution
python visualize_results.py

# As a module
from ml4setk.StickyCharacters.visualize_results import main
main()
```

## Output Structure

The toolkit generates several types of outputs:

1. **Analysis Results** (`results/` directory):
   - JSON files containing detailed tokenization analysis
   - Summary files with aggregated results

2. **Visualizations** (`visualizations/` directory):
   - Sticky tokens comparison plots
   - Token distribution charts
   - Language-specific analysis graphs

3. **Vocabulary Files**:
   - Text files containing model vocabularies
   - Format: `token\tid`

## Dependencies

- transformers
- matplotlib
- seaborn
- pandas
- numpy

## Installation

```bash
pip install transformers matplotlib seaborn pandas numpy
```

## Example Workflow

1. Analyze code tokenization:
```bash
python analyze_merged_tokens.py
```

2. Save model vocabulary:
```bash
python save_vocab.py --model_name "codellama/CodeLLaMA-7b-hf"
```

3. Generate visualizations:
```bash
python visualize_results.py
```

## Notes

- First-time usage will download the specified language models
- Ensure sufficient disk space for model storage
- Results are saved in the `results/` directory
- Visualizations are saved in the `visualizations/` directory 