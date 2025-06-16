#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test fixed tree-sitter code segmentation functionality

This script verifies whether the new code segmentation method can correctly maintain code structure,
instead of extracting individual identifiers like "object", "data".
"""

import sys
import os
from tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer


def test_code_segmentation():
    """Test code segmentation functionality"""
    print("="*80)
    print(" Testing Fixed Code Segmentation Functionality ")
    print("="*80)
    
    analyzer = TreeSitterStickyAnalyzer('python')
    
    test_cases = [
        {
            'code': 'x.value',
            'description': 'Attribute access',
            'expected_segments': ['x.value']
        },
        {
            'code': 'data["key"]',
            'description': 'Dictionary access',
            'expected_segments': ['data["key"]']
        },
        {
            'code': 'items[0].process()',
            'description': 'Index access and method call',
            'expected_segments': ['items[0].process()', 'items[0]', 'process()']
        },
        {
            'code': 'if x.value > threshold: result = process(x.data)',
            'description': 'Conditional statement',
            'expected_segments': ['x.value > threshold', 'x.value', 'result = process(x.data)', 'process(x.data)', 'x.data']
        },
        {
            'code': 'obj.method().attribute[index]',
            'description': 'Method chaining',
            'expected_segments': ['obj.method().attribute[index]', 'obj.method().attribute', 'obj.method()', 'method()']
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'-'*60}")
        print(f"Test case {i}: {test_case['description']}")
        print(f"Code: {test_case['code']}")
        print(f"{'-'*60}")
        
        try:
            segments = analyzer.extract_code_segments(test_case['code'])
            
            print(f"Number of extracted code segments: {len(segments)}")
            print("Extracted code segments:")
            
            for j, segment in enumerate(segments, 1):
                print(f"  {j:2d}. '{segment['text']:<25}' | {segment['node_type']:<20} | Position: {segment['start_byte']:2d}-{segment['end_byte']:2d}")
                
                # Verify this is a complete code fragment, not a single identifier
                segment_text = segment['text'].strip()
                if len(segment_text) > 1:
                    if ('.' in segment_text or '[' in segment_text or '(' in segment_text or 
                        '>' in segment_text or '=' in segment_text or '"' in segment_text):
                        print(f"      ✓ This is a meaningful code fragment")
                    elif segment['node_type'] in ['identifier', 'string', 'integer']:
                        print(f"      → Basic element: {segment['node_type']}")
                    else:
                        print(f"      ? Other type: {segment['node_type']}")
                
            # Verify if expected code segments are included
            segment_texts = [s['text'] for s in segments]
            print(f"\nExpected code segments: {test_case.get('expected_segments', 'Not specified')}")
            
            if 'expected_segments' in test_case:
                found_expected = []
                for expected in test_case['expected_segments']:
                    if any(expected in text for text in segment_texts):
                        found_expected.append(expected)
                print(f"Found expected code segments: {found_expected}")
                
        except Exception as e:
            print(f"Error: {e}")


def test_tokenization_of_segments():
    """Test tokenization of code segments"""
    print("\n" + "="*80)
    print(" Testing Code Segment Tokenization ")
    print("="*80)
    
    analyzer = TreeSitterStickyAnalyzer('python')
    model_name = 'bigcode/starcoder2-3b'
    
    test_codes = [
        'x.value',
        'data["key"]',
        'items[0].process()'
    ]
    
    print(f"Using model: {model_name}")
    print("Note: First run requires model download...")
    
    for i, code in enumerate(test_codes, 1):
        print(f"\n{'-'*50}")
        print(f"Test code {i}: {code}")
        print(f"{'-'*50}")
        
        try:
            # Extract code segments
            segments = analyzer.extract_code_segments(code)
            print(f"Extracted code segments: {len(segments)}")
            
            for j, segment in enumerate(segments, 1):
                segment_text = segment['text']
                print(f"\nSegment {j}: '{segment_text}' ({segment['node_type']})")
                
                try:
                    # Tokenize this code segment
                    tokenization = analyzer.analyze_code_part_tokenization(model_name, segment_text)
                    
                    print(f"  Tokens: {tokenization['tokens']}")
                    print(f"  Token count: {tokenization['token_count']}")
                    print(f"  Sticky tokens: {tokenization['sticky_count']}")
                    
                    if tokenization['sticky_tokens']:
                        for sticky in tokenization['sticky_tokens']:
                            print(f"    -> Sticky: '{sticky['token']}' (Rules: {', '.join(sticky['detection_rules'])})")
                    else:
                        print(f"    -> No sticky tokens")
                        
                except Exception as e:
                    print(f"  Tokenization error: {e}")
                    
        except Exception as e:
            print(f"Code segment extraction error: {e}")


def test_full_analysis():
    """Test complete new method analysis"""
    print("\n" + "="*80)
    print(" Testing Complete New Method Analysis ")
    print("="*80)
    
    analyzer = TreeSitterStickyAnalyzer('python')
    model_name = 'bigcode/starcoder2-3b'
    
    test_code = 'if x.value > threshold: result = process(x.data)'
    
    print(f"Test code: {test_code}")
    print(f"Using model: {model_name}")
    
    try:
        result = analyzer.analyze_code_with_tree_sitter_split(model_name, test_code)
        
        print(f"\nAnalysis results:")
        print(f"Total code segments: {result['total_code_segments']}")
        print(f"Successfully analyzed segments: {result['analyzed_segments']}")
        print(f"Sticky tokens found: {result['total_sticky_tokens']}")
        
        print(f"\nCode segment details:")
        for i, segment_analysis in enumerate(result['segment_analyses'], 1):
            print(f"  Segment {i}: '{segment_analysis['text']}'")
            print(f"    AST node: {segment_analysis['node_type']}")
            print(f"    Tokens: {segment_analysis['tokens']}")
            print(f"    Sticky count: {segment_analysis['sticky_count']}")
            
            if segment_analysis['sticky_tokens']:
                for sticky in segment_analysis['sticky_tokens']:
                    print(f"      -> '{sticky['token']}' (Rules: {', '.join(sticky['detection_rules'])})")
        
        print(f"\nAll sticky tokens:")
        if result['sticky_tokens']:
            for i, sticky in enumerate(result['sticky_tokens'], 1):
                print(f"  {i}. '{sticky['token']}' from segment '{sticky['source_code_segment']}'")
                print(f"     AST node: {sticky['ast_node_type']}")
        else:
            print("  No sticky tokens found")
            
    except Exception as e:
        print(f"Complete analysis error: {e}")


def main():
    """Main function"""
    print("Tree-sitter Code Segmentation Fix Verification")
    print("This test verifies whether the fixed code segmentation can correctly maintain code structure")
    
    try:
        # Test 1: Code segmentation functionality
        test_code_segmentation()
        
        # Test 2: Code segment tokenization
        test_tokenization_of_segments()
        
        # Test 3: Complete analysis workflow
        test_full_analysis()
        
        print("\n" + "="*80)
        print(" Testing Complete ")
        print("="*80)
        print("✓ If you see meaningful code segments (like 'x.value', 'data[\"key\"]', etc.) instead of single identifiers,")
        print("  the fix is successful!")
        
    except KeyboardInterrupt:
        print("\nTesting interrupted by user")
    except Exception as e:
        print(f"\nTesting error occurred: {e}")


if __name__ == '__main__':
    main()