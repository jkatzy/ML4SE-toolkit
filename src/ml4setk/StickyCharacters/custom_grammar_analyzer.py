#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sticky token analyzer using custom tree-sitter grammar

This analyzer uses the grammar.js file in the project to build a custom Python grammar parser,
providing more precise syntax-aware sticky token detection.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import json
from tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer

try:
    import tree_sitter
except ImportError:
    tree_sitter = None


class CustomGrammarStickyAnalyzer:
    """
    Sticky token analyzer based on custom tree-sitter grammar
    """
    
    def __init__(self, grammar_path: str = None):
        """
        Initialize analyzer
        
        Args:
            grammar_path: Path to grammar.js file, defaults to grammar(3).js in current directory
        """
        self.grammar_path = grammar_path or self._find_grammar_file()
        self.parser = None
        self.language = None
        self.temp_dir = None
        
        # Node type information extracted from grammar file
        self.grammar_rules = {}
        self.sticky_relevant_nodes = set()
        
        # Initialize grammar parser
        self._init_custom_parser()
        
        # Fallback analyzer
        self.fallback_analyzer = TreeSitterStickyAnalyzer('python')
    
    def _find_grammar_file(self) -> str:
        """Find grammar file"""
        current_dir = Path(__file__).parent
        possible_files = ['grammar(3).js', 'grammar.js', 'python.grammar.js']
        
        for filename in possible_files:
            path = current_dir / filename
            if path.exists():
                return str(path)
        
        raise FileNotFoundError("Grammar.js file not found, please ensure the file exists")
    
    def _init_custom_parser(self):
        """Initialize custom grammar parser"""
        if tree_sitter is None:
            print("Warning: tree-sitter not available, will use fallback analyzer")
            return
            
        try:
            # Parse grammar file to get rule information
            self._analyze_grammar_file()
            
            # Try to compile grammar file
            self._compile_grammar()
            
        except Exception as e:
            print(f"Warning: Custom grammar initialization failed: {e}")
            print("Will use standard tree-sitter analyzer")
    
    def _analyze_grammar_file(self):
        """Analyze grammar file and extract relevant information"""
        with open(self.grammar_path, 'r', encoding='utf-8') as f:
            grammar_content = f.read()
        
        # Extract grammar rules related to sticky tokens
        # These are grammar structures that may produce sticky tokens
        self.sticky_relevant_nodes.update([
            'attribute', 'subscript', 'call', 'binary_operator', 'comparison_operator',
            'assignment', 'augmented_assignment', 'string', 'concatenated_string',
            'list', 'dictionary', 'tuple', 'list_comprehension', 'dictionary_comprehension',
            'slice', 'keyword_argument', 'parenthesized_expression'
        ])
        
        print(f"✓ Identified {len(self.sticky_relevant_nodes)} node types that may produce sticky tokens from grammar file")
    
    def _compile_grammar(self):
        """Compile grammar file to tree-sitter language"""
        # Create temporary directory for compilation
        self.temp_dir = tempfile.mkdtemp(prefix='ts_grammar_')
        
        try:
            # Copy grammar file to temporary directory
            temp_grammar = os.path.join(self.temp_dir, 'grammar.js')
            shutil.copy2(self.grammar_path, temp_grammar)
            
            # Try to compile using tree-sitter CLI
            # Note: This requires tree-sitter CLI tool to be installed
            result = subprocess.run(
                ['tree-sitter', 'generate'],
                cwd=self.temp_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Compilation successful, load language
                self._load_compiled_language()
                print("✓ Custom grammar compiled successfully")
            else:
                print(f"Warning: Grammar compilation failed: {result.stderr}")
                
        except FileNotFoundError:
            print("Warning: tree-sitter CLI not installed, cannot compile custom grammar")
        except Exception as e:
            print(f"Warning: Error during grammar compilation: {e}")
    
    def _load_compiled_language(self):
        """Load compiled language"""
        try:
            # Find compiled .so file or other formats
            lib_path = None
            for ext in ['.so', '.dylib', '.dll']:
                potential_path = os.path.join(self.temp_dir, f'tree-sitter-python{ext}')
                if os.path.exists(potential_path):
                    lib_path = potential_path
                    break
            
            if lib_path:
                # Use tree-sitter to load custom language
                self.language = tree_sitter.Language(lib_path, 'python')
                self.parser = tree_sitter.Parser()
                self.parser.set_language(self.language)
                print("✓ Custom language loaded successfully")
            else:
                print("Warning: Compiled language file not found")
                
        except Exception as e:
            print(f"Warning: Language loading failed: {e}")
    
    def extract_grammar_aware_segments(self, code: str) -> List[Dict]:
        """
        Extract code segments using custom grammar
        
        Args:
            code: Source code
            
        Returns:
            List of code segments with grammar information
        """
        if self.parser is None:
            # Use fallback analyzer
            return self.fallback_analyzer.extract_code_segments(code)
        
        try:
            tree = self.parser.parse(code.encode())
            segments = []
            
            def extract_sticky_segments(node, depth=0):
                """Extract code segments that may contain sticky tokens"""
                node_text = code[node.start_byte:node.end_byte]
                
                if not node_text.strip():
                    return
                
                # Determine relevance based on grammar rules
                is_relevant = (
                    node.type in self.sticky_relevant_nodes or
                    self._is_composite_expression(node) or
                    self._contains_operators(node_text)
                )
                
                segment_info = {
                    'text': node_text,
                    'node_type': node.type,
                    'start_byte': node.start_byte,
                    'end_byte': node.end_byte,
                    'depth': depth,
                    'parent_type': node.parent.type if node.parent else None,
                    'children_count': len(node.children),
                    'is_sticky_relevant': is_relevant,
                    'grammar_rule': self._get_grammar_rule_info(node.type),
                    'contains_operators': self._contains_operators(node_text),
                    'contains_delimiters': self._contains_delimiters(node_text)
                }
                
                # Add relevant code segments
                if is_relevant and len(node_text.strip()) > 1:
                    segments.append(segment_info)
                
                # Recursively process child nodes
                if not is_relevant or node.type in ['module', 'program', 'expression_statement']:
                    for child in node.children:
                        extract_sticky_segments(child, depth + 1)
            
            extract_sticky_segments(tree.root_node)
            
            # Deduplicate and sort
            return self._deduplicate_segments(segments, code)
            
        except Exception as e:
            print(f"Warning: Custom grammar analysis failed: {e}")
            return self.fallback_analyzer.extract_code_segments(code)
    
    def _is_composite_expression(self, node) -> bool:
        """Determine if it's a composite expression"""
        composite_types = {
            'binary_operator', 'comparison_operator', 'boolean_operator',
            'unary_operator', 'conditional_expression', 'lambda',
            'call', 'attribute', 'subscript'
        }
        return node.type in composite_types or len(node.children) > 2
    
    def _contains_operators(self, text: str) -> bool:
        """Check if text contains operators"""
        operators = {'.', '[', ']', '(', ')', '+', '-', '*', '/', '%', '=', 
                    '>', '<', '!', '&', '|', '^', '~', ':', ';', ','}
        return any(op in text for op in operators)
    
    def _contains_delimiters(self, text: str) -> bool:
        """Check if text contains delimiters"""
        delimiters = {'"', "'", '[', ']', '(', ')', '{', '}'}
        return any(delim in text for delim in delimiters)
    
    def _get_grammar_rule_info(self, node_type: str) -> Dict:
        """Get grammar rule information"""
        # Provide additional information based on rules in grammar file
        rule_info = {
            'precedence': 0,
            'associativity': 'none',
            'produces_tokens': False
        }
        
        # Provide specific information based on node type
        if node_type in ['binary_operator', 'comparison_operator']:
            rule_info.update({
                'precedence': 10,
                'associativity': 'left',
                'produces_tokens': True
            })
        elif node_type in ['attribute', 'subscript', 'call']:
            rule_info.update({
                'precedence': 20,
                'associativity': 'left',
                'produces_tokens': True
            })
        
        return rule_info
    
    def _deduplicate_segments(self, segments: List[Dict], code: str) -> List[Dict]:
        """Deduplicate and filter code segments"""
        # Sort by position
        segments.sort(key=lambda x: (x['start_byte'], x['end_byte']))
        
        # Remove nested and duplicate segments
        filtered_segments = []
        seen_ranges = set()
        
        for segment in segments:
            # Skip segments that are too short
            if len(segment['text'].strip()) < 2:
                continue
            
            # Skip pure whitespace
            if not segment['text'].strip():
                continue
            
            # Check for duplicates
            range_key = (segment['start_byte'], segment['end_byte'])
            if range_key in seen_ranges:
                continue
            seen_ranges.add(range_key)
            
            # Check if contained by other segments
            is_contained = False
            for other in filtered_segments:
                if (other['start_byte'] <= segment['start_byte'] and 
                    segment['end_byte'] <= other['end_byte'] and
                    other['text'] != segment['text']):
                    is_contained = True
                    break
            
            if not is_contained:
                filtered_segments.append(segment)
        
        return filtered_segments
    
    def analyze_with_custom_grammar(self, model_name: str, code: str) -> Dict:
        """
        Perform sticky token analysis using custom grammar
        
        Args:
            model_name: Tokenizer model name
            code: Source code
            
        Returns:
            Analysis results
        """
        # Extract grammar-aware code segments
        segments = self.extract_grammar_aware_segments(code)
        
        # Perform tokenization analysis on each segment
        segment_analyses = []
        all_sticky_tokens = []
        
        for segment_info in segments:
            try:
                segment_text = segment_info['text']
                
                # Use fallback analyzer's tokenization method
                tokenization_result = self.fallback_analyzer.analyze_code_part_tokenization(
                    model_name, segment_text
                )
                
                # Enhance analysis results
                enhanced_analysis = {
                    **segment_info,
                    **tokenization_result,
                    'analysis_method': 'custom_grammar',
                    'grammar_enhanced': True
                }
                segment_analyses.append(enhanced_analysis)
                
                # Collect sticky tokens with grammar information
                for sticky_token in tokenization_result['sticky_tokens']:
                    enhanced_sticky = {
                        **sticky_token,
                        'source_code_segment': segment_text,
                        'grammar_node_type': segment_info['node_type'],
                        'grammar_rule_info': segment_info['grammar_rule'],
                        'segment_context': segment_info,
                        'detection_confidence': self._calculate_confidence(sticky_token, segment_info)
                    }
                    all_sticky_tokens.append(enhanced_sticky)
                    
            except Exception as e:
                print(f"Warning: Failed to analyze code segment '{segment_info['text'][:50]}': {e}")
                continue
        
        return {
            'model': model_name,
            'code': code,
            'language': 'python',
            'method': 'custom_grammar_sticky_analysis',
            'grammar_file': self.grammar_path,
            'total_segments': len(segments),
            'analyzed_segments': len(segment_analyses),
            'segment_analyses': segment_analyses,
            'sticky_tokens': all_sticky_tokens,
            'total_sticky_tokens': len(all_sticky_tokens),
            'grammar_enhanced': True
        }
    
    def _calculate_confidence(self, sticky_token: Dict, segment_info: Dict) -> float:
        """Calculate confidence of sticky token detection"""
        confidence = 0.5  # Base confidence
        
        # Adjust confidence based on grammar node type
        if segment_info['node_type'] in self.sticky_relevant_nodes:
            confidence += 0.2
        
        # Based on number of detection rules
        rule_count = len(sticky_token.get('detection_rules', []))
        confidence += min(rule_count * 0.1, 0.2)
        
        # Based on grammar rule information
        if segment_info['grammar_rule'].get('produces_tokens', False):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def compare_with_standard_analysis(self, model_name: str, code: str) -> Dict:
        """
        Compare custom grammar analysis with standard analysis results
        
        Args:
            model_name: Tokenizer model name
            code: Source code
            
        Returns:
            Comparison results
        """
        # Custom grammar analysis
        custom_result = self.analyze_with_custom_grammar(model_name, code)
        
        # Standard analysis
        standard_result = self.fallback_analyzer.analyze_code_with_tree_sitter_split(model_name, code)
        
        # Comparison analysis
        custom_sticky = set(t['token'] for t in custom_result['sticky_tokens'])
        standard_sticky = set(t['token'] for t in standard_result['sticky_tokens'])
        
        comparison = {
            'code': code,
            'model': model_name,
            'custom_analysis': custom_result,
            'standard_analysis': standard_result,
            'comparison': {
                'custom_sticky_count': len(custom_sticky),
                'standard_sticky_count': len(standard_sticky),
                'common_sticky': list(custom_sticky & standard_sticky),
                'custom_only': list(custom_sticky - standard_sticky),
                'standard_only': list(standard_sticky - custom_sticky),
                'improvement_ratio': len(custom_sticky) / max(len(standard_sticky), 1),
                'agreement_ratio': len(custom_sticky & standard_sticky) / max(len(custom_sticky | standard_sticky), 1)
            }
        }
        
        return comparison
    
    def __del__(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass


def main():
    """Demonstrate custom grammar analyzer"""
    print("Custom Grammar.js Sticky Token Analyzer Demo")
    print("="*60)
    
    try:
        analyzer = CustomGrammarStickyAnalyzer()
        model_name = 'bigcode/starcoder2-3b'
        
        test_codes = [
            'x.value',
            'data["key"]',
            'items[0].process()',
            'if x.value > threshold: result = process(x.data)',
            'obj.method().attribute[index] = value'
        ]
        
        for i, code in enumerate(test_codes, 1):
            print(f"\nTest case {i}: {code}")
            print("-" * 50)
            
            comparison = analyzer.compare_with_standard_analysis(model_name, code)
            comp = comparison['comparison']
            
            print(f"Custom grammar detected: {comp['custom_sticky_count']} sticky tokens")
            print(f"Standard method detected: {comp['standard_sticky_count']} sticky tokens")
            print(f"Common detections: {len(comp['common_sticky'])} tokens")
            print(f"Custom only: {comp['custom_only']}")
            print(f"Standard only: {comp['standard_only']}")
            print(f"Improvement ratio: {comp['improvement_ratio']:.2f}")
            print(f"Agreement ratio: {comp['agreement_ratio']:.2f}")
        
    except Exception as e:
        print(f"Demo failed: {e}")


if __name__ == '__main__':
    main()