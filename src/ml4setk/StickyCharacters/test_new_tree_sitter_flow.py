#!/usr/bin/env python3
"""
Test script for the new tree-sitter split-then-tokenize approach.
"""

import os
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer


def test_code_part_extraction():
    """Test the code part extraction functionality."""
    print("Testing Code Part Extraction")
    print("=" * 50)
    
    test_cases = [
        {
            'code': 'if x.value > 10: result = x.process()',
            'description': 'Python attribute access and method call'
        },
        {
            'code': 'data["key"] = items[0].name',
            'description': 'Python dictionary and list access'
        },
        {
            'code': 'for i in range(len(items)): print(items[i])',
            'description': 'Python loop with function calls'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print(f"Code: {test_case['code']}")
        print("-" * 40)
        
        try:
            analyzer = TreeSitterStickyAnalyzer('python')
            code_parts = analyzer.extract_code_parts(test_case['code'])
            
            print(f"Total code parts extracted: {len(code_parts)}")
            print("Code parts:")
            for j, part in enumerate(code_parts, 1):
                print(f"  {j}. '{part['text']}' ({part['node_type']}) "
                      f"[{part['start_byte']}-{part['end_byte']}]")
                if part['is_semantic_boundary']:
                    print(f"     -> Semantic boundary")
                if part['is_operator']:
                    print(f"     -> Operator")
                if part['is_identifier']:
                    print(f"     -> Identifier")
                    
        except Exception as e:
            print(f"Error: {e}")


def test_new_analysis_flow():
    """Test the complete new analysis flow."""
    print("\n" + "=" * 60)
    print("Testing New Tree-sitter Split-then-Tokenize Flow")
    print("=" * 60)
    
    # Use a smaller model for testing
    model_name = 'bigcode/starcoder2-3b'
    
    test_cases = [
        {
            'code': 'x.value',
            'description': 'Simple attribute access'
        },
        {
            'code': 'data["key"]',
            'description': 'Dictionary access'
        },
        {
            'code': 'items[0].process()',
            'description': 'Method call on indexed item'
        },
        {
            'code': 'if x > 10:',
            'description': 'Conditional with comparison'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print(f"Code: {test_case['code']}")
        print("-" * 50)
        
        try:
            analyzer = TreeSitterStickyAnalyzer('python')
            result = analyzer.analyze_code_with_tree_sitter_split(model_name, test_case['code'])
            
            print(f"Total code parts: {result['total_code_parts']}")
            print(f"Successfully analyzed parts: {result['analyzed_parts']}")
            print(f"Total sticky tokens found: {result['total_sticky_tokens']}")
            
            print("\nCode part analysis:")
            for j, part_analysis in enumerate(result['part_analyses'], 1):
                print(f"  Part {j}: '{part_analysis['text']}'")
                print(f"    Node type: {part_analysis['node_type']}")
                print(f"    Tokens: {part_analysis['tokens']}")
                print(f"    Sticky tokens: {part_analysis['sticky_count']}")
                
                if part_analysis['sticky_tokens']:
                    for sticky in part_analysis['sticky_tokens']:
                        print(f"      -> '{sticky['token']}' (rules: {sticky['detection_rules']})")
            
            if result['sticky_tokens']:
                print(f"\nAll sticky tokens found:")
                for sticky in result['sticky_tokens']:
                    print(f"  - '{sticky['token']}' from '{sticky['source_code_part']}' "
                          f"({sticky['ast_node_type']})")
                    print(f"    Rules: {sticky['detection_rules']}")
            else:
                print("\nNo sticky tokens found.")
                
        except Exception as e:
            print(f"Error: {e}")


def compare_old_vs_new_approach():
    """Compare the old and new approaches."""
    print("\n" + "=" * 60)
    print("Comparing Old vs New Approach")
    print("=" * 60)
    
    model_name = 'bigcode/starcoder2-3b'
    test_code = 'if x.value > threshold: result = process(x.data)'
    
    try:
        analyzer = TreeSitterStickyAnalyzer('python')
        
        print(f"Test code: {test_code}")
        print("\n--- OLD APPROACH (Tokenize whole code, then use AST) ---")
        old_result = analyzer.analyze_code_tokenization_ast(model_name, test_code)
        print(f"Total tokens: {len(old_result['table'])}")
        print(f"Sticky tokens: {len(old_result['sticky_tokens'])}")
        
        for sticky in old_result['sticky_tokens']:
            print(f"  - '{sticky['token']}' -> '{sticky['code_piece']}'")
            print(f"    Rules: {sticky['analysis']['detection_rules']}")
        
        print("\n--- NEW APPROACH (Tree-sitter split, then tokenize each part) ---")
        new_result = analyzer.analyze_code_with_tree_sitter_split(model_name, test_code)
        print(f"Code parts: {new_result['total_code_parts']}")
        print(f"Sticky tokens: {new_result['total_sticky_tokens']}")
        
        for sticky in new_result['sticky_tokens']:
            print(f"  - '{sticky['token']}' from part '{sticky['source_code_part']}'")
            print(f"    AST node: {sticky['ast_node_type']}")
            print(f"    Rules: {sticky['detection_rules']}")
        
        # Save detailed comparison
        comparison_data = {
            'test_code': test_code,
            'old_approach': old_result,
            'new_approach': new_result
        }
        
        with open('results/approach_comparison.json', 'w', encoding='utf-8') as f:
            json.dump(comparison_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nDetailed comparison saved to: results/approach_comparison.json")
        
    except Exception as e:
        print(f"Error during comparison: {e}")


if __name__ == '__main__':
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # Test code part extraction (doesn't require model)
    test_code_part_extraction()
    
    # Test new analysis flow (requires model download)
    try:
        test_new_analysis_flow()
        compare_old_vs_new_approach()
    except Exception as e:
        print(f"\nModel-based tests failed: {e}")
        print("This might be due to model availability or network issues.")
    
    print(f"\nTesting completed!")