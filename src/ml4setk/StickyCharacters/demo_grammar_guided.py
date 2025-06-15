#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grammar-Guided Sticky Token Analysis Demo

Demonstrates how to use grammar.js files to guide more precise sticky token detection
"""

import sys
import os
from grammar_guided_analyzer import GrammarGuidedStickyAnalyzer


def print_section_header(title: str, width: int = 80):
    """Print section header"""
    print("\n" + "="*width)
    print(f" {title} ")
    print("="*width)


def print_subsection_header(title: str, width: int = 60):
    """Print subsection header"""
    print(f"\n{'-'*width}")
    print(f" {title} ")
    print(f"{'-'*width}")


def demo_grammar_parsing():
    """Demo 1: Grammar file parsing"""
    print_section_header("Demo 1: Grammar.js File Parsing")
    
    try:
        analyzer = GrammarGuidedStickyAnalyzer()
        
        print(f"Grammar file path: {analyzer.grammar_path}")
        print(f"Parsed grammar rules: {len(analyzer.grammar_rules)}")
        print(f"Identified sticky-related nodes: {len(analyzer.sticky_node_types)}")
        print(f"Operator precedence rules: {len(analyzer.operator_patterns)}")
        
        print("\nMain sticky-related node types:")
        for i, node_type in enumerate(sorted(analyzer.sticky_node_types)[:10], 1):
            rule_info = analyzer.grammar_rules.get(node_type, {})
            operators = rule_info.get('operators', set())
            delimiters = rule_info.get('delimiters', set())
            
            print(f"  {i:2d}. {node_type:<20} | Operators: {len(operators)} | Delimiters: {len(delimiters)}")
            if operators:
                print(f"      Operators: {', '.join(sorted(operators))}")
            if delimiters:
                print(f"      Delimiters: {', '.join(sorted(delimiters))}")
        
        print("\nOperator precedence (partial):")
        for name, precedence in list(analyzer.operator_patterns.items())[:8]:
            print(f"  {name:<20}: {precedence}")
            
    except Exception as e:
        print(f"Grammar parsing failed: {e}")


def demo_grammar_guided_segmentation():
    """Demo 2: Grammar-guided code segmentation"""
    print_section_header("Demo 2: Grammar-Guided Code Segmentation")
    
    try:
        analyzer = GrammarGuidedStickyAnalyzer()
        
        test_cases = [
            'x.value',
            'data["key"]',
            'items[0].process()',
            'if x.value > threshold: result = x.data + 1'
        ]
        
        for i, code in enumerate(test_cases, 1):
            print_subsection_header(f"Test Case {i}: {code}")
            
            segments = analyzer.extract_grammar_guided_segments(code)
            
            print(f"Extracted code segments: {len(segments)}")
            print("Segment details:")
            
            for j, segment in enumerate(segments, 1):
                confidence = segment['sticky_confidence']
                operators = segment['operators_present']
                delimiters = segment['delimiters_present']
                
                print(f"  {j:2d}. '{segment['text']:<25}' | {segment['node_type']:<20}")
                print(f"      Confidence: {confidence:.2f} | Operators: {len(operators)} | Delimiters: {len(delimiters)}")
                
                if operators:
                    print(f"      Operators: {', '.join(sorted(operators))}")
                if delimiters:
                    print(f"      Delimiters: {', '.join(sorted(delimiters))}")
                
                if segment['is_sticky_relevant']:
                    print(f"      ✓ High sticky relevance")
                    
    except Exception as e:
        print(f"Grammar-guided segmentation failed: {e}")


def demo_grammar_guided_analysis():
    """Demo 3: Grammar-guided sticky token analysis"""
    print_section_header("Demo 3: Grammar-Guided Sticky Token Analysis")
    
    try:
        analyzer = GrammarGuidedStickyAnalyzer()
        model_name = 'bigcode/starcoder2-3b'
        
        test_cases = [
            'x.value',
            'data["key"]',
            'items[0].process()',
            'if x.value > threshold: result = process(x.data)'
        ]
        
        print(f"Using model: {model_name}")
        print("Note: First run requires model download...")
        
        for i, code in enumerate(test_cases, 1):
            print_subsection_header(f"Test Case {i}: {code}")
            
            result = analyzer.analyze_with_grammar_guidance(model_name, code)
            
            print(f"Code segments: {result['total_segments']}")
            print(f"Successfully analyzed: {result['analyzed_segments']}")
            print(f"Sticky tokens: {result['total_sticky_tokens']}")
            print(f"Grammar rules used: {result['grammar_rules_used']}")
            
            if result['sticky_tokens']:
                print("\nDiscovered sticky tokens:")
                for j, sticky in enumerate(result['sticky_tokens'], 1):
                    confidence = sticky.get('sticky_confidence', 0)
                    operators = sticky.get('operators_context', [])
                    rules = sticky.get('detection_rules', [])
                    
                    print(f"  {j}. '{sticky['token']}' from segment '{sticky['source_code_segment']}'")
                    print(f"     Node type: {sticky['grammar_node_type']}")
                    print(f"     Confidence: {confidence:.2f}")
                    print(f"     Detection rules: {', '.join(rules)}")
                    if operators:
                        print(f"     Operator context: {', '.join(operators)}")
            else:
                print("  No sticky tokens found")
                
    except Exception as e:
        print(f"Grammar-guided analysis failed: {e}")


def demo_comparison():
    """Demo 4: Grammar-guided vs standard method comparison"""
    print_section_header("Demo 4: Grammar-Guided vs Standard Method Comparison")
    
    try:
        analyzer = GrammarGuidedStickyAnalyzer()
        model_name = 'bigcode/starcoder2-3b'
        
        test_cases = [
            'data["key"]',
            'items[0].process()',
            'if x.value > threshold: result = process(x.data)',
            'obj.method().attribute[index] += value * 2'
        ]
        
        for i, code in enumerate(test_cases, 1):
            print_subsection_header(f"Comparison Case {i}: {code}")
            
            comparison = analyzer.compare_with_standard(model_name, code)
            metrics = comparison['metrics']
            
            print(f"Grammar-guided method:")
            print(f"  - Sticky tokens: {metrics['grammar_sticky_count']} found")
            print(f"  - Unique discoveries: {metrics['grammar_only']}")
            
            print(f"Standard method:")
            print(f"  - Sticky tokens: {metrics['standard_sticky_count']} found")
            print(f"  - Unique discoveries: {metrics['standard_only']}")
            
            print(f"Comparison metrics:")
            print(f"  - Common discoveries: {len(metrics['common_tokens'])} tokens {metrics['common_tokens']}")
            print(f"  - Precision improvement: {metrics['precision_improvement']:.2f}")
            print(f"  - Recall ratio: {metrics['recall_ratio']:.2f}")
            print(f"  - F1 score: {metrics['f1_score']:.2f}")
            
            # Show additional grammar-guided information
            grammar_result = comparison['grammar_guided']
            if grammar_result['sticky_tokens']:
                print(f"Additional grammar-guided information:")
                for sticky in grammar_result['sticky_tokens'][:3]:  # Show only first 3
                    if sticky.get('grammar_guided'):
                        confidence = sticky.get('sticky_confidence', 0)
                        grammar_rules = [r for r in sticky.get('detection_rules', []) 
                                      if r.startswith('grammar_')]
                        
                        print(f"  - '{sticky['token']}': confidence {confidence:.2f}")
                        if grammar_rules:
                            print(f"    Grammar rules: {', '.join(grammar_rules)}")
                            
    except Exception as e:
        print(f"Comparison analysis failed: {e}")


def demo_detailed_analysis():
    """Demo 5: Detailed analysis of a complex example"""
    print_section_header("Demo 5: Detailed Analysis of Complex Code")
    
    try:
        analyzer = GrammarGuidedStickyAnalyzer()
        model_name = 'bigcode/starcoder2-3b'
        
        complex_code = 'result = obj.method(arg1, arg2).attribute[index] + data["key"] * 2'
        
        print(f"Complex code example: {complex_code}")
        
        # Grammar-guided analysis
        result = analyzer.analyze_with_grammar_guidance(model_name, complex_code)
        
        print(f"\nGrammar-guided analysis result:")
        print(f"Code segments: {result['total_segments']}")
        print(f"Sticky tokens: {result['total_sticky_tokens']}")
        
        print(f"\nDetailed segment analysis:")
        for i, segment in enumerate(result['segment_analyses'], 1):
            print(f"Segment {i}: '{segment['text']}'")
            print(f"  Node type: {segment['node_type']}")
            print(f"  Confidence: {segment['sticky_confidence']:.2f}")
            print(f"  Tokens: {segment['tokens']}")
            print(f"  Sticky count: {segment['sticky_count']}")
            
            if segment['sticky_tokens']:
                for sticky in segment['sticky_tokens']:
                    print(f"    -> Sticky: '{sticky['token']}' (rules: {', '.join(sticky['detection_rules'])})")
        
        print(f"\nAll sticky tokens (sorted by confidence):")
        for i, sticky in enumerate(result['sticky_tokens'], 1):
            confidence = sticky.get('sticky_confidence', 0)
            node_type = sticky.get('grammar_node_type', 'unknown')
            
            print(f"  {i}. '{sticky['token']}' | Confidence: {confidence:.2f} | Node: {node_type}")
            print(f"     Source: '{sticky['source_code_segment']}'")
            
            # Show grammar context
            grammar_context = sticky.get('grammar_context', {})
            if grammar_context:
                print(f"     Grammar context: operators={grammar_context.get('has_operators', False)}, "
                      f"delimiters={grammar_context.get('has_delimiters', False)}")
                      
    except Exception as e:
        print(f"Detailed analysis failed: {e}")


def main():
    """Main function"""
    print_section_header("Grammar.js-Guided Sticky Token Analysis Demo", 100)
    print("This demo shows how to use Python grammar file (grammar.js) to guide sticky token detection")
    print("Grammar rules provide more precise code structure understanding, thus improving detection quality")
    
    try:
        # Demo 1: Grammar file parsing
        demo_grammar_parsing()
        
        # Demo 2: Grammar-guided code segmentation
        demo_grammar_guided_segmentation()
        
        # Demo 3: Grammar-guided analysis
        demo_grammar_guided_analysis()
        
        # Demo 4: Comparison analysis
        demo_comparison()
        
        # Demo 5: Detailed analysis
        demo_detailed_analysis()
        
        print_section_header("Demo Complete", 100)
        print("✓ Grammar-guided analyzer demo completed successfully!")
        print("Key advantages:")
        print("  1. Utilize complete Python grammar rules to guide analysis")
        print("  2. Calculate sticky token confidence based on grammar context")
        print("  3. Identify grammar roles of operators and delimiters")
        print("  4. Provide more precise detection results than standard methods")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nError occurred during demo: {e}")
        print("Please check dependency installation and network connection")


if __name__ == '__main__':
    main()