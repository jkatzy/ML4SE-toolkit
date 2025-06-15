#!/usr/bin/env python3
"""
Test script for tree-sitter sticky character detection integration.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer


def test_basic_functionality():
    """Test basic tree-sitter sticky character detection functionality."""
    print("Testing Tree-sitter Sticky Character Detection")
    print("=" * 50)
    
    # Test code samples
    test_cases = [
        {
            'code': 'if x.value > 10: result = x.process()',
            'language': 'python',
            'description': 'Python attribute access and method call'
        },
        {
            'code': 'data["key"] = items[0].name',
            'language': 'python', 
            'description': 'Python dictionary and list access'
        },
        {
            'code': 'for i in range(len(items)): items[i] *= 2',
            'language': 'python',
            'description': 'Python loop with indexing'
        }
    ]
    
    # Test with a lightweight model (if available)
    model_name = 'bigcode/starcoder2-3b'  # Smaller model for testing
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print(f"Code: {test_case['code']}")
        print("-" * 40)
        
        try:
            # Initialize analyzer
            analyzer = TreeSitterStickyAnalyzer(test_case['language'])
            
            # Test AST parsing
            ast_contexts = analyzer.parse_code_with_ast(test_case['code'])
            print(f"AST nodes found: {len(ast_contexts)}")
            
            # Show some AST node types
            node_types = list(set(ctx['node_type'] for ctx in ast_contexts))
            print(f"Node types: {node_types[:5]}{'...' if len(node_types) > 5 else ''}")
            
        except Exception as e:
            print(f"Error during AST analysis: {e}")
            continue
        
        try:
            # Test full analysis (requires model download)
            print("Testing with tokenizer analysis...")
            result = analyzer.analyze_code_tokenization_ast(model_name, test_case['code'])
            
            print(f"Total tokens: {len(result['table'])}")
            print(f"Sticky tokens found: {len(result['sticky_tokens'])}")
            
            # Debug: Show first few tokens
            print("First 5 tokens:")
            for i, row in enumerate(result['table'][:5]):
                print(f"  {i+1}. '{row['token']}' -> '{row['code_piece']}' (sticky: {row['sticky']})")
                
                # Show detailed analysis
                analysis = row['analysis']
                print(f"      Clean token: '{analysis['clean_token']}'")
                print(f"      Has letter: {analysis['has_letter']}, Has digit: {analysis['has_digit']}, Has symbol: {analysis['has_symbol']}")
                print(f"      AST context: {analysis['ast_context']['context_info']}")
                
                if row['analysis']['detection_rules']:
                    print(f"      Rules: {', '.join(row['analysis']['detection_rules'])}")
                print()
            
            if result['sticky_tokens']:
                print("Sticky tokens:")
                for token_info in result['sticky_tokens']:
                    analysis = token_info['analysis']
                    print(f"  - '{token_info['token']}' -> '{token_info['code_piece']}'")
                    print(f"    Rules: {', '.join(analysis['detection_rules'])}")
            else:
                print("No sticky tokens detected.")
                    
        except Exception as e:
            print(f"Warning: Could not complete tokenizer analysis: {e}")
            print("(This might be due to model not being available locally)")


def test_ast_parsing_only():
    """Test just the AST parsing functionality without tokenizer."""
    print("\n" + "=" * 50)
    print("Testing AST Parsing Only")
    print("=" * 50)
    
    code = '''
def calculate_score(items):
    total = 0
    for item in items:
        if item.is_valid():
            total += item.value * item.weight
    return total / len(items)
    '''
    
    try:
        analyzer = TreeSitterStickyAnalyzer('python')
        ast_contexts = analyzer.parse_code_with_ast(code)
        
        print(f"Code length: {len(code)} characters")
        print(f"AST nodes: {len(ast_contexts)}")
        
        # Show detailed information for a few nodes
        print("\nFirst 10 AST nodes:")
        for i, ctx in enumerate(ast_contexts[:10]):
            print(f"  {i+1}. {ctx['node_type']}: '{ctx['text'][:30]}{'...' if len(ctx['text']) > 30 else ''}' "
                  f"[{ctx['start_byte']}-{ctx['end_byte']}]")
            
        # Show boundary nodes
        boundary_nodes = [ctx for ctx in ast_contexts if ctx['is_semantic_boundary']]
        print(f"\nSemantic boundary nodes: {len(boundary_nodes)}")
        for ctx in boundary_nodes[:5]:
            print(f"  - {ctx['node_type']}: '{ctx['text'][:20]}{'...' if len(ctx['text']) > 20 else ''}'")
            
    except Exception as e:
        print(f"Error during AST parsing: {e}")


if __name__ == '__main__':
    # Test AST parsing functionality (doesn't require model download)
    test_ast_parsing_only()
    
    # Test full functionality (requires model download)
    print("\n" + "=" * 60)
    print("FULL FUNCTIONALITY TEST")
    print("Note: This requires downloading models and may take time")
    print("=" * 60)
    
    try:
        test_basic_functionality()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test failed with error: {e}")
        print("This might be due to missing dependencies or model availability")
    
    print("\nTest completed!")