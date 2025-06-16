#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tree-sitter Split-then-Tokenize method demonstration script

This script demonstrates our new method:
1. Use tree-sitter AST to split code into meaningful parts
2. Tokenize each part separately
3. Detect sticky tokens in each part

"""

import os
import sys
import json
from typing import List, Dict
from tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer


def print_section_header(title: str, width: int = 80):
    """Print section title"""
    print("\n" + "="*width)
    print(f" {title} ")
    print("="*width)


def print_subsection_header(title: str, width: int = 60):
    """Print subsection title"""
    print(f"\n{'-'*width}")
    print(f" {title} ")
    print(f"{'-'*width}")


def demo_code_splitting():
    """Demo 1: Tree-sitter code splitting functionality"""
    print_section_header("Demo 1: Tree-sitter code splitting functionality")
    
    analyzer = TreeSitterStickyAnalyzer('python')
    
    test_cases = [
        'x.value',
        'data["key"]', 
        'items[0].process()',
        'if x.value > 10: result = x.data'
    ]
    
    for i, code in enumerate(test_cases, 1):
        print_subsection_header(f"Test case {i}: {code}")
        
        try:
            code_segments = analyzer.extract_code_segments(code)
            print(f"Original code: {code}")
            print(f"Number of extracted code segments: {len(code_segments)}")
            print("\nCode segment details:")
            
            for j, segment in enumerate(code_segments, 1):
                flags = []
                if segment.get('is_semantic_boundary'):
                    flags.append("Semantic boundary")
                if segment.get('is_operator'):
                    flags.append("Operator")
                if segment.get('is_identifier'):
                    flags.append("Identifier")
                if segment.get('is_meaningful_segment'):
                    flags.append("Meaningful segment")
                
                flag_str = ", ".join(flags) if flags else "None"
                
                # Verify if this is a code fragment rather than an individual identifier
                segment_text = segment['text'].strip()
                is_code_fragment = ('.' in segment_text or '[' in segment_text or '(' in segment_text or 
                                  '>' in segment_text or '=' in segment_text or '"' in segment_text or
                                  len(segment_text) > 3)
                
                status = "✓ Code fragment" if is_code_fragment else "→ Basic element"
                
                print(f"  {j:2d}. '{segment['text']:<20}' | {segment['node_type']:<18} | Position: {segment['start_byte']:2d}-{segment['end_byte']:2d} | {status}")
                print(f"      Attributes: {flag_str}")
                
        except Exception as e:
            print(f"Error: {e}")


def demo_new_approach():
    """Demo 2: New segment-then-tokenize method"""
    print_section_header("Demo 2: New Segment-then-Tokenize method")
    
    analyzer = TreeSitterStickyAnalyzer('python')
    model_name = 'bigcode/starcoder2-3b'  # Use a smaller model for demonstration
    
    test_cases = [
        'x.value',
        'data["key"]',
        'items[0].process()',
        'if x.value > threshold: result = process(x.data)'
    ]
    
    print(f"Using model: {model_name}")
    print("Note: First run requires model download, may take some time...")
    print("New method: First use tree-sitter to extract code segments, then tokenize each segment")
    
    all_results = []
    
    for i, code in enumerate(test_cases, 1):
        print_subsection_header(f"Test case {i}: {code}")
        
        try:
            result = analyzer.analyze_code_with_tree_sitter_split(model_name, code)
            all_results.append(result)
            
            print(f"Code: {code}")
            print(f"Number of extracted code segments: {result['total_code_segments']}")
            print(f"Number of successfully analyzed segments: {result['analyzed_segments']}")
            print(f"Total sticky tokens found: {result['total_sticky_tokens']}")
            
            print("\nAnalysis results for each code segment:")
            for j, segment_analysis in enumerate(result['segment_analyses'], 1):
                tokens_str = ", ".join([f"'{t}'" for t in segment_analysis['tokens']])
                if len(tokens_str) > 60:
                    tokens_str = tokens_str[:57] + "..."
                
                # Check if this is a meaningful code segment
                segment_text = segment_analysis['text'].strip()
                is_code_fragment = ('.' in segment_text or '[' in segment_text or '(' in segment_text or 
                                  '>' in segment_text or '=' in segment_text or '"' in segment_text)
                status = "✓ Code fragment" if is_code_fragment else "→ Basic element"
                
                print(f"  Segment {j}: '{segment_analysis['text']}' ({status})")
                print(f"    AST node type: {segment_analysis['node_type']}")
                print(f"    Token count: {segment_analysis['token_count']}")
                print(f"    Tokens: {tokens_str}")
                print(f"    Sticky token count: {segment_analysis['sticky_count']}")
                
                if segment_analysis['sticky_tokens']:
                    for sticky in segment_analysis['sticky_tokens']:
                        rules_str = ", ".join(sticky['detection_rules'])
                        print(f"      -> Sticky: '{sticky['token']}' (Detection rules: {rules_str})")
            
            if result['sticky_tokens']:
                print(f"\nAll sticky tokens summary:")
                for j, sticky in enumerate(result['sticky_tokens'], 1):
                    print(f"  {j}. '{sticky['token']}' from code segment '{sticky['source_code_segment']}'")
                    print(f"     AST node type: {sticky['ast_node_type']}")
                    print(f"     Detection rules: {', '.join(sticky['detection_rules'])}")
            else:
                print(f"\nNo sticky tokens found")
                
        except Exception as e:
            print(f"Analysis error: {e}")
            print("This may be due to model download issues or network connection problems")
    
    return all_results


def demo_comparison():
    """Demo 3: New vs old method comparison"""
    print_section_header("Demo 3: New vs old method comparison")
    
    analyzer = TreeSitterStickyAnalyzer('python')
    model_name = 'bigcode/starcoder2-3b'
    test_code = 'if x.value > threshold: result = process(x.data)'
    
    print(f"Comparison test code: {test_code}")
    print(f"Using model: {model_name}")
    
    try:
        # Old method: First tokenize the entire code, then analyze with AST
        print_subsection_header("Old method: AST-enhanced tokenization")
        old_result = analyzer.analyze_code_tokenization_ast(model_name, test_code)
        old_sticky_tokens = [t['token'] for t in old_result['sticky_tokens']]
        
        print(f"Total token count: {len(old_result['table'])}")
        print(f"Sticky token count: {len(old_sticky_tokens)}")
        print(f"Found sticky tokens: {old_sticky_tokens}")
        
        if old_result['sticky_tokens']:
            print("Detailed information:")
            for i, token_info in enumerate(old_result['sticky_tokens'], 1):
                analysis = token_info['analysis']
                print(f"  {i}. '{token_info['token']}' -> '{token_info['code_piece']}'")
                print(f"      Detection rules: {', '.join(analysis['detection_rules'])}")
        
        # New method: First split with tree-sitter, then tokenize each part
        print_subsection_header("New method: Split-then-Tokenize")
        new_result = analyzer.analyze_code_with_tree_sitter_split(model_name, test_code)
        new_sticky_tokens = [t['token'] for t in new_result['sticky_tokens']]
        
        print(f"Number of code parts: {new_result['total_code_parts']}")
        print(f"Sticky token count: {len(new_sticky_tokens)}")
        print(f"Found sticky tokens: {new_sticky_tokens}")
        
        if new_result['sticky_tokens']:
            print("Detailed information:")
            for i, sticky in enumerate(new_result['sticky_tokens'], 1):
                print(f"  {i}. '{sticky['token']}' from part '{sticky['source_code_part']}'")
                print(f"     AST node type: {sticky['ast_node_type']}")
                print(f"      Detection rules: {', '.join(sticky['detection_rules'])}")
        
        # Comparison analysis
        print_subsection_header("Comparison analysis results")
        old_set = set(old_sticky_tokens)
        new_set = set(new_sticky_tokens)
        
        print(f"Old method found sticky token count: {len(old_set)}")
        print(f"New method found sticky token count: {len(new_set)}")
        print(f"Common found token count: {len(old_set & new_set)}")
        
        if old_set & new_set:
            print(f"Common found tokens: {list(old_set & new_set)}")
        if old_set - new_set:
            print(f"Only old method found: {list(old_set - new_set)}")
        if new_set - old_set:
            print(f"Only new method found: {list(new_set - old_set)}")
        
        agreement_rate = len(old_set & new_set) / max(len(old_set), len(new_set), 1) * 100
        print(f"Agreement rate: {agreement_rate:.1f}%")
        
        return {
            'old_result': old_result,
            'new_result': new_result,
            'comparison': {
                'old_count': len(old_set),
                'new_count': len(new_set),
                'common_count': len(old_set & new_set),
                'agreement_rate': agreement_rate
            }
        }
        
    except Exception as e:
        print(f"Comparison analysis error: {e}")
        return None


def demo_step_by_step():
    """Demo 4: Step-by-step detailed explanation of new method"""
    print_section_header("Demo 4: Step-by-step detailed explanation of new method")
    
    analyzer = TreeSitterStickyAnalyzer('python')
    model_name = 'bigcode/starcoder2-3b'
    test_code = 'obj.method().attribute[index]'
    
    print(f"Detailed analysis code: {test_code}")
    
    try:
        print_subsection_header("Step 1: Parse AST structure")
        ast_contexts = analyzer.parse_code_with_ast(test_code)
        print(f"Total AST nodes: {len(ast_contexts)}")
        print("Main AST nodes:")
        for i, ctx in enumerate(ast_contexts[:10], 1):
            text_preview = ctx['text'][:20] + ('...' if len(ctx['text']) > 20 else '')
            print(f"  {i:2d}. {ctx['node_type']:<20} | '{text_preview}' | [{ctx['start_byte']}-{ctx['end_byte']}]")
        
        print_subsection_header("Step 2: Extract code parts")
        code_parts = analyzer.extract_code_parts(test_code)
        print(f"Number of extracted code parts: {len(code_parts)}")
        print("Code part details:")
        for i, part in enumerate(code_parts, 1):
            print(f"  {i:2d}. '{part['text']:<15}' | {part['node_type']:<15} | Depth: {part['depth']}")
        
        print_subsection_header("Step 3: Tokenize each part")
        for i, part in enumerate(code_parts[:8], 1):  # Only show first 8 parts
            try:
                tokenization = analyzer.analyze_code_part_tokenization(model_name, part['text'])
                print(f"\nPart {i}: '{part['text']}' ({part['node_type']})")
                print(f"  Tokens: {tokenization['tokens']}")
                print(f"  Token count: {tokenization['token_count']}")
                print(f"  Sticky token count: {tokenization['sticky_count']}")
                
                if tokenization['sticky_tokens']:
                    for sticky in tokenization['sticky_tokens']:
                        print(f"    -> Sticky: '{sticky['token']}' (Rules: {', '.join(sticky['detection_rules'])})")
                        
            except Exception as e:
                print(f"\nPart {i}: '{part['text']}' - Analysis error: {e}")
        
        print_subsection_header("Step 4: Summarize final results")
        final_result = analyzer.analyze_code_with_tree_sitter_split(model_name, test_code)
        print(f"Final sticky token count: {final_result['total_sticky_tokens']}")
        
        if final_result['sticky_tokens']:
            print("Final sticky token list:")
            for i, sticky in enumerate(final_result['sticky_tokens'], 1):
                print(f"  {i}. '{sticky['token']}' from '{sticky['source_code_part']}' ({sticky['ast_node_type']})")
        
    except Exception as e:
        print(f"Detailed analysis error: {e}")


def save_demo_results(results: List[Dict]):
    """Save demo results"""
    print_section_header("Save demo results")
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    demo_data = {
        'demo_info': {
            'method': 'tree_sitter_split_then_tokenize',
            'language': 'python',
            'total_samples': len(results)
        },
        'results': results
    }
    
    output_file = 'results/demo_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize(output_file) / 1024
    print(f"Demo results saved to: {output_file}")
    print(f"File size: {file_size:.1f} KB")


def main():
    """Main function"""
    print_section_header("Tree-sitter Split-then-Tokenize method demonstration", 100)
    print("This demo script shows our new sticky token detection method:")
    print("1. Use tree-sitter to parse code AST")
    print("2. Split code into meaningful parts")
    print("3. Tokenize each part separately") 
    print("4. Detect sticky tokens in each part")
    print("\nPlease ensure the necessary dependencies are installed: transformers, tree-sitter related packages")
    
    
    try:
        # Demo 1: Code splitting functionality
        demo_code_splitting()
        
        # Demo 2: New method complete workflow
        results = demo_new_approach()
        
        # Demo 3: New vs old method comparison
        comparison = demo_comparison()
        
        # Demo 4: Step-by-step detailed explanation
        demo_step_by_step()
        
        # Save results
        if results:
            save_demo_results(results)
        
        print_section_header("Demo completed", 100)
        print("🎉 All demos completed successfully!")
        print("If you encounter issues, please check error messages or verify network connection and dependencies.")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nError occurred during demo: {e}")
        print("Please check dependency installation and network connection")


if __name__ == '__main__':
    main()