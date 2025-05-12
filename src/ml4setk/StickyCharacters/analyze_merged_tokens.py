import re
import json
import os
from typing import List, Dict, Set
from transformers import AutoTokenizer

# Language configurations
LANGUAGE_CONFIGS = {
    'python': {
        'symbols': set('()[]{}.:=+-*/><%&|^~!,;'),
        'operators': set('+-*/><=%&|^~!'),
        'keywords': {
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
            'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
            'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
            'try', 'while', 'with', 'yield'
        }
    },
    'javascript': {
        'symbols': set('()[]{}.:=+-*/><%&|^~!,;?'),
        'operators': set('+-*/><=%&|^~!?'),
        'keywords': {
            'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger',
            'default', 'delete', 'do', 'else', 'export', 'extends', 'finally',
            'for', 'function', 'if', 'import', 'in', 'instanceof', 'new', 'return',
            'super', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void',
            'while', 'with', 'yield', 'let', 'static', 'async', 'await'
        }
    },
    'java': {
        'symbols': set('()[]{}.:=+-*/><%&|^~!,;?'),
        'operators': set('+-*/><=%&|^~!?'),
        'keywords': {
            'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
            'char', 'class', 'const', 'continue', 'default', 'do', 'double',
            'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
            'if', 'implements', 'import', 'instanceof', 'int', 'interface',
            'long', 'native', 'new', 'package', 'private', 'protected',
            'public', 'return', 'short', 'static', 'strictfp', 'super',
            'switch', 'synchronized', 'this', 'throw', 'throws', 'transient',
            'try', 'void', 'volatile', 'while'
        }
    }
}

def is_sticky_token(token: str, language: str = 'python') -> bool:
    """
    Determine if a token is sticky based on the specified language's rules.
    
    Args:
        token: The token to check
        language: The programming language to use for rules (default: 'python')
    
    Returns:
        bool: True if the token is sticky, False otherwise
    """
    if language not in LANGUAGE_CONFIGS:
        raise ValueError(f"Unsupported language: {language}. Supported languages: {list(LANGUAGE_CONFIGS.keys())}")
    
    config = LANGUAGE_CONFIGS[language]
    # Remove common space prefix markers (SentencePiece's ▁, GPT-BPE's Ġ)
    clean_tok = token.lstrip('▁Ġ')
    
    has_letter_or_underscore = bool(re.search(r'[A-Za-z_]', clean_tok))
    has_digit = any(ch.isdigit() for ch in clean_tok)
    has_keyword = any(clean_tok.startswith(kw) for kw in config['keywords'])
    has_symbol = any(ch in config['symbols'] for ch in clean_tok)
    has_operator = any(ch in config['operators'] for ch in clean_tok)

    textual_part = has_letter_or_underscore or has_digit or has_keyword
    symbolic_part = has_symbol or has_operator
    return textual_part and symbolic_part

def analyze_code_tokenization(model_name: str, code: str, language: str = 'python') -> Dict:
    """
    Analyze code tokenization for a specific language.
    
    Args:
        model_name: The name of the tokenizer model
        code: The code to analyze
        language: The programming language of the code (default: 'python')
    
    Returns:
        Dict containing the analysis results
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    use_offsets = getattr(tokenizer, 'is_fast', False)

    if use_offsets:
        encoding = tokenizer(code, return_offsets_mapping=True, add_special_tokens=False)
        tokens = tokenizer.convert_ids_to_tokens(encoding['input_ids'])
        offsets = encoding['offset_mapping']
    else:
        ids = tokenizer.encode(code, add_special_tokens=False)
        tokens = tokenizer.convert_ids_to_tokens(ids)
        offsets = []
        idx = 0
        for t in tokens:
            piece = tokenizer.convert_tokens_to_string([t])
            offsets.append((idx, idx + len(piece)))
            idx += len(piece)

    table, sticky_tokens = [], []
    for token, (start, end) in zip(tokens, offsets):
        code_piece = code[start:end]
        sticky = is_sticky_token(token, language)
        row = {
            'code_piece': code_piece,
            'token': token,
            'token_id': tokenizer.convert_tokens_to_ids(token),
            'offset': (start, end),
            'sticky': sticky
        }
        table.append(row)
        if sticky:
            sticky_tokens.append(row)

    return {
        'model': model_name,
        'code': code,
        'language': language,
        'table': table,
        'sticky_tokens': sticky_tokens
    }

def run_experiment(model_names: List[str], code_samples: List[str],
                  languages: List[str] = ['python'],
                  output_prefix: str = 'tokenization_exp'):
    """
    Run tokenization experiments for multiple models and languages.
    
    Args:
        model_names: List of model names to test
        code_samples: List of code samples to analyze
        languages: List of programming languages to analyze (default: ['python'])
        output_prefix: Prefix for output files
    """
    # Create results directory if it doesn't exist
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    all_results = []
    for model in model_names:
        print(f'>>> Processing model: {model}')
        for lang in languages:
            print(f'  · Language: {lang}')
            for idx, code in enumerate(code_samples, start=1):
                result = analyze_code_tokenization(model, code, lang)
                out_json = os.path.join(results_dir, f'{output_prefix}_{model.replace("/", "_")}_{lang}_sample{idx}.json')
                with open(out_json, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f'    - Sample {idx}: Sticky tokens count = {len(result["sticky_tokens"])}, Results saved to {out_json}')
                all_results.append(result)

    summary = [
        {
            'model': r['model'],
            'language': r['language'],
            'code': r['code'],
            'sticky_token_count': len(r['sticky_tokens']),
            'sticky_tokens': [t['token'] for t in r['sticky_tokens']]
        }
        for r in all_results
    ]
    summary_file = os.path.join(results_dir, f'{output_prefix}_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f'\n>>> Experiment summary saved: {summary_file}')

if __name__ == '__main__':
    model_names = [
        'codellama/CodeLLaMA-7b-hf',
        'WizardLM/WizardCoder-15B-V1.0',
        'bigcode/starcoder2-3b'
    ]
    code_samples = [
        'if (a + b > c): x = a else: x = b',  # Python
        'if (a + b > c) { x = a; } else { x = b; }',  # JavaScript/Java
    ]
    languages = ['python', 'javascript', 'java']
    run_experiment(model_names, code_samples, languages)
