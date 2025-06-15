#!/usr/bin/env python3
"""
Enhanced sticky character analysis using Tree-sitter AST information.
This script extends the original analyze_merged_tokens.py with tree-sitter capabilities.
"""

import json
import os
from typing import List, Dict
from .tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer
from .analyze_merged_tokens import run_experiment as run_original_experiment


def compare_detection_methods(model_names: List[str], code_samples: List[str], 
                            languages: List[str] = ['python'],
                            output_prefix: str = 'comparison_exp'):
    """
    Compare original rule-based detection with tree-sitter AST-based detection.
    
    Args:
        model_names: List of model names to test
        code_samples: List of code samples to analyze  
        languages: List of programming languages
        output_prefix: Prefix for output files
    """
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    comparison_results = []
    
    for model in model_names:
        print(f'>>> Processing model: {model}')
        for lang in languages:
            print(f'  · Language: {lang}')
            
            # Initialize tree-sitter analyzer
            try:
                ts_analyzer = TreeSitterStickyAnalyzer(lang)
            except Exception as e:
                print(f'    Warning: Could not initialize tree-sitter for {lang}: {e}')
                continue
                
            for idx, code in enumerate(code_samples, start=1):
                print(f'    - Processing sample {idx}...')
                
                # Run tree-sitter analysis
                try:
                    ts_result = ts_analyzer.analyze_code_tokenization_ast(model, code)
                    ts_sticky_count = len(ts_result['sticky_tokens'])
                    ts_tokens = [t['token'] for t in ts_result['sticky_tokens']]
                    
                    # Save detailed tree-sitter results
                    ts_out_file = os.path.join(
                        results_dir, 
                        f'{output_prefix}_{model.replace("/", "_")}_{lang}_sample{idx}_treesitter.json'
                    )
                    with open(ts_out_file, 'w', encoding='utf-8') as f:
                        json.dump(ts_result, f, ensure_ascii=False, indent=2)
                    
                except Exception as e:
                    print(f'      Error with tree-sitter analysis: {e}')
                    ts_sticky_count = 0
                    ts_tokens = []
                    ts_out_file = None
                
                # Store comparison result
                comparison_result = {
                    'model': model,
                    'language': lang,
                    'sample_index': idx,
                    'code': code,
                    'tree_sitter': {
                        'sticky_count': ts_sticky_count,
                        'sticky_tokens': ts_tokens,
                        'output_file': ts_out_file
                    }
                }
                
                comparison_results.append(comparison_result)
                print(f'      Tree-sitter sticky tokens: {ts_sticky_count}')
    
    # Save comparison summary
    summary_file = os.path.join(results_dir, f'{output_prefix}_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(comparison_results, f, ensure_ascii=False, indent=2)
    
    print(f'\n>>> Comparison summary saved: {summary_file}')
    return comparison_results


def analyze_single_sample_detailed(model_name: str, code: str, language: str = 'python'):
    """
    Perform detailed analysis of a single code sample with both methods.
    
    Args:
        model_name: Model name for tokenization
        code: Code sample to analyze
        language: Programming language
        
    Returns:
        Dictionary with detailed comparison results
    """
    print(f"Analyzing code sample with model {model_name} (language: {language})")
    
    # Tree-sitter analysis
    ts_analyzer = TreeSitterStickyAnalyzer(language)
    ts_result = ts_analyzer.analyze_code_tokenization_ast(model_name, code)
    
    # Print detailed results
    print(f"\n=== Tree-sitter Analysis Results ===")
    print(f"Model: {model_name}")
    print(f"Language: {language}")
    print(f"Total tokens: {len(ts_result['table'])}")
    print(f"Sticky tokens found: {len(ts_result['sticky_tokens'])}")
    
    print(f"\nSticky tokens with detection rules:")
    for i, token_info in enumerate(ts_result['sticky_tokens'], 1):
        analysis = token_info['analysis']
        print(f"  {i}. Token: '{token_info['token']}' -> Code: '{token_info['code_piece']}'")
        print(f"     Rules: {', '.join(analysis['detection_rules'])}")
        print(f"     AST nodes: {analysis['ast_context']['context_info'].get('all_node_types', [])}")
    
    return ts_result


def analyze_with_new_tree_sitter_split(model_name: str, code: str, language: str = 'python'):
    """
    Analyze using the new tree-sitter split approach:
    1. Use tree-sitter to split code into parts
    2. Tokenize each part separately  
    3. Check for sticky tokens in each part
    
    Args:
        model_name: Model name for tokenization
        code: Code sample to analyze
        language: Programming language
        
    Returns:
        Dictionary with analysis results
    """
    print(f"Analyzing with NEW tree-sitter split approach")
    print(f"Model: {model_name}, Language: {language}")
    print(f"Code: {code}")
    
    # Initialize analyzer
    ts_analyzer = TreeSitterStickyAnalyzer(language)
    
    # Use the new split-then-tokenize approach
    result = ts_analyzer.analyze_code_with_tree_sitter_split(model_name, code)
    
    # Print detailed results
    print(f"\n=== NEW Tree-sitter Split Analysis Results ===")
    print(f"Total code parts extracted: {result['total_code_parts']}")
    print(f"Successfully analyzed parts: {result['analyzed_parts']}")
    print(f"Total sticky tokens found: {result['total_sticky_tokens']}")
    
    print(f"\nCode parts analysis:")
    for i, part_analysis in enumerate(result['part_analyses'], 1):
        print(f"  Part {i}: '{part_analysis['text']}'")
        print(f"    AST node type: {part_analysis['node_type']}")
        print(f"    Tokens: {part_analysis['tokens']}")
        print(f"    Token count: {part_analysis['token_count']}")
        print(f"    Sticky tokens: {part_analysis['sticky_count']}")
        
        if part_analysis['sticky_tokens']:
            for sticky in part_analysis['sticky_tokens']:
                print(f"      -> Sticky: '{sticky['token']}' (clean: '{sticky['clean_token']}')")
                print(f"         Rules: {', '.join(sticky['detection_rules'])}")
    
    print(f"\nAll sticky tokens summary:")
    if result['sticky_tokens']:
        for i, sticky in enumerate(result['sticky_tokens'], 1):
            print(f"  {i}. '{sticky['token']}' from code part '{sticky['source_code_part']}'")
            print(f"     AST node type: {sticky['ast_node_type']}")
            print(f"     Detection rules: {', '.join(sticky['detection_rules'])}")
    else:
        print("  No sticky tokens found.")
    
    return result


def compare_both_approaches(model_name: str, code: str, language: str = 'python'):
    """
    Compare the old AST-based approach with the new split-then-tokenize approach.
    
    Args:
        model_name: Model name for tokenization
        code: Code sample to analyze
        language: Programming language
    """
    print(f"\n{'='*80}")
    print(f"COMPARISON: OLD vs NEW TREE-SITTER APPROACHES")
    print(f"{'='*80}")
    print(f"Code: {code}")
    print(f"Model: {model_name}")
    print(f"Language: {language}")
    
    ts_analyzer = TreeSitterStickyAnalyzer(language)
    
    try:
        # Old approach: tokenize whole code, then use AST for context
        print(f"\n--- OLD APPROACH (AST-enhanced tokenization) ---")
        old_result = ts_analyzer.analyze_code_tokenization_ast(model_name, code)
        print(f"Total tokens: {len(old_result['table'])}")
        print(f"Sticky tokens: {len(old_result['sticky_tokens'])}")
        
        old_sticky_tokens = [t['token'] for t in old_result['sticky_tokens']]
        print(f"Sticky tokens found: {old_sticky_tokens}")
        
    except Exception as e:
        print(f"Old approach failed: {e}")
        old_result = None
        old_sticky_tokens = []
    
    try:
        # New approach: split with tree-sitter, then tokenize each part
        print(f"\n--- NEW APPROACH (Split-then-tokenize) ---")
        new_result = ts_analyzer.analyze_code_with_tree_sitter_split(model_name, code)
        print(f"Code parts: {new_result['total_code_parts']}")
        print(f"Sticky tokens: {new_result['total_sticky_tokens']}")
        
        new_sticky_tokens = [t['token'] for t in new_result['sticky_tokens']]
        print(f"Sticky tokens found: {new_sticky_tokens}")
        
        print(f"\nCode parts breakdown:")
        for i, part in enumerate(new_result['part_analyses'], 1):
            print(f"  {i}. '{part['text']}' ({part['node_type']}) -> {len(part['tokens'])} tokens")
            if part['sticky_tokens']:
                for sticky in part['sticky_tokens']:
                    print(f"     Sticky: '{sticky['token']}'")
        
    except Exception as e:
        print(f"New approach failed: {e}")
        new_result = None
        new_sticky_tokens = []
    
    # Compare results
    print(f"\n--- COMPARISON SUMMARY ---")
    if old_result and new_result:
        old_set = set(old_sticky_tokens)
        new_set = set(new_sticky_tokens)
        
        print(f"Old approach sticky tokens: {len(old_set)}")
        print(f"New approach sticky tokens: {len(new_set)}")
        print(f"Common sticky tokens: {len(old_set & new_set)}")
        print(f"Only in old: {old_set - new_set}")
        print(f"Only in new: {new_set - old_set}")
    
    return {
        'old_result': old_result,
        'new_result': new_result,
        'old_sticky_tokens': old_sticky_tokens,
        'new_sticky_tokens': new_sticky_tokens
    }


def run_tree_sitter_experiment(model_names: List[str], code_samples: List[str],
                              languages: List[str] = ['python'],
                              output_prefix: str = 'treesitter_exp'):
    """
    Run experiments using only tree-sitter analysis.
    
    Args:
        model_names: List of model names to test
        code_samples: List of code samples to analyze
        languages: List of programming languages
        output_prefix: Prefix for output files
    """
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    all_results = []
    
    for model in model_names:
        print(f'>>> Processing model: {model}')
        for lang in languages:
            print(f'  · Language: {lang}')
            
            try:
                analyzer = TreeSitterStickyAnalyzer(lang)
            except Exception as e:
                print(f'    Error: Could not initialize tree-sitter for {lang}: {e}')
                continue
                
            for idx, code in enumerate(code_samples, start=1):
                try:
                    result = analyzer.analyze_code_tokenization_ast(model, code)
                    
                    # Save detailed results
                    out_json = os.path.join(
                        results_dir, 
                        f'{output_prefix}_{model.replace("/", "_")}_{lang}_sample{idx}.json'
                    )
                    with open(out_json, 'w', encoding='utf-8') as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    
                    print(f'    - Sample {idx}: Sticky tokens = {len(result["sticky_tokens"])}, '
                          f'Saved to {out_json}')
                    all_results.append(result)
                    
                except Exception as e:
                    print(f'    - Sample {idx}: Error - {e}')
    
    # Create summary
    summary = []
    for r in all_results:
        summary.append({
            'model': r['model'],
            'language': r['language'],
            'method': r['method'],
            'sticky_token_count': len(r['sticky_tokens']),
            'sticky_tokens': [t['token'] for t in r['sticky_tokens']],
            'detection_methods': [
                rule for token in r['sticky_tokens'] 
                for rule in token['analysis']['detection_rules']
            ]
        })
    
    summary_file = os.path.join(results_dir, f'{output_prefix}_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f'\n>>> Tree-sitter experiment summary saved: {summary_file}')


if __name__ == '__main__':
    # Example usage
    model_names = [
        'codellama/CodeLLaMA-7b-hf',
        'WizardLM/WizardCoder-15B-V1.0', 
        'bigcode/starcoder2-3b'
    ]
    
    code_samples = [
        # Python examples
        'if x.value > threshold: result = process(x.data)',
        'for item in items: item.update({"status": "processed"})',
        'lambda x: x.attr if x.is_valid() else default_value',
        
        # More complex examples
        '''
def calculate_metrics(data):
    result = {}
    for key, values in data.items():
        result[key] = {
            'mean': sum(values) / len(values),
            'max': max(values),
            'min': min(values)
        }
    return result
        ''',
        
        # JavaScript-style (if supported)
        'const result = items.filter(x => x.active).map(x => x.value);',
    ]
    
    languages = ['python']  # Start with Python
    
    print("Running tree-sitter sticky character analysis...")
    
    # Run tree-sitter only experiment
    run_tree_sitter_experiment(model_names, code_samples, languages)
    
    # Run detailed analysis on a single sample
    print("\n" + "="*60)
    print("DETAILED ANALYSIS EXAMPLE")
    print("="*60)
    analyze_single_sample_detailed(
        'codellama/CodeLLaMA-7b-hf',
        'if x.value > threshold: result = process(x.data)',
        'python'
    )
    
    # Test the NEW tree-sitter split approach
    print("\n" + "="*60)
    print("NEW TREE-SITTER SPLIT APPROACH DEMO")
    print("="*60)
    
    test_code = 'if x.value > threshold: result = process(x.data)'
    model = 'bigcode/starcoder2-3b'  # Use smaller model for demo
    
    print(f"Testing new approach with: {test_code}")
    analyze_with_new_tree_sitter_split(model, test_code, 'python')
    
    # Compare both approaches
    print("\n" + "="*60)
    print("COMPARING OLD vs NEW APPROACHES")
    print("="*60)
    compare_both_approaches(model, test_code, 'python')