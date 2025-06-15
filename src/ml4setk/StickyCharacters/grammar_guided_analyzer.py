#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grammar.js rule-based Sticky Token analyzer

This analyzer parses grammar.js files, extracts Python syntax rule information,
and then uses these rules to guide more precise sticky token detection.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer


class GrammarGuidedStickyAnalyzer:
    """
    Grammar rule-based sticky token analyzer
    """
    
    def __init__(self, grammar_path: str = None):
        """
        Initialize analyzer
        
        Args:
            grammar_path: Path to grammar.js file
        """
        self.grammar_path = grammar_path or self._find_grammar_file()
        self.grammar_rules = {}
        self.operator_patterns = {}
        self.delimiter_patterns = {}
        self.sticky_node_types = set()
        
        # Parse grammar file
        self._parse_grammar_file()
        
        # Fallback standard analyzer
        self.standard_analyzer = TreeSitterStickyAnalyzer('python')
        
        print(f"✓ Grammar-guided analyzer initialization complete")
        print(f"  - Parsed grammar rules: {len(self.grammar_rules)}")
        print(f"  - Identified sticky-related nodes: {len(self.sticky_node_types)}")
    
    def _find_grammar_file(self) -> str:
        """Find grammar file"""
        current_dir = Path(__file__).parent
        possible_files = ['grammar(3).js', 'grammar.js', 'python.grammar.js']
        
        for filename in possible_files:
            path = current_dir / filename
            if path.exists():
                return str(path)
        
        raise FileNotFoundError("Grammar.js file not found")
    
    def _parse_grammar_file(self):
        """Parse grammar file and extract rule information"""
        with open(self.grammar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract operator precedence information
        self._extract_precedence_info(content)
        
        # Extract grammar rules
        self._extract_grammar_rules(content)
        
        # Identify patterns that may produce sticky tokens
        self._identify_sticky_patterns()
    
    def _extract_precedence_info(self, content: str):
        """Extract operator precedence information"""
        # Find PREC object definition
        prec_match = re.search(r'const PREC = \{([^}]+)\}', content, re.DOTALL)
        if prec_match:
            prec_content = prec_match.group(1)
            
            # Parse precedence definitions
            for line in prec_content.split('\n'):
                line = line.strip()
                if ':' in line and not line.startswith('//'):
                    parts = line.split(':')
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        value = parts[1].strip().rstrip(',')
                        try:
                            self.operator_patterns[name] = int(value)
                        except ValueError:
                            pass
        
        print(f"  - Extracted operator precedence: {len(self.operator_patterns)} entries")
    
    def _extract_grammar_rules(self, content: str):
        """Extract grammar rule definitions"""
        # Find rules section
        rules_match = re.search(r'rules:\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', content, re.DOTALL)
        if not rules_match:
            return
        
        rules_content = rules_match.group(1)
        
        # Parse individual rules
        rule_pattern = re.compile(r'(\w+):\s*\$\s*=>\s*([^,}]+(?:\{[^{}]*\}[^,}]*)*)', re.DOTALL)
        
        for match in rule_pattern.finditer(rules_content):
            rule_name = match.group(1)
            rule_body = match.group(2).strip()
            
            # Analyze rule body
            rule_info = self._analyze_rule_body(rule_body)
            rule_info['name'] = rule_name
            
            self.grammar_rules[rule_name] = rule_info
        
        print(f"  - Extracted grammar rules: {len(self.grammar_rules)} entries")
    
    def _analyze_rule_body(self, rule_body: str) -> Dict:
        """Analyze rule body and extract useful information"""
        info = {
            'has_choice': 'choice(' in rule_body,
            'has_sequence': 'seq(' in rule_body,
            'has_precedence': 'prec(' in rule_body,
            'has_operators': False,
            'has_delimiters': False,
            'operators': set(),
            'delimiters': set(),
            'field_names': set()
        }
        
        # Find operators
        operator_matches = re.findall(r"'([+\-*/%=<>!&|^~.,:;]+)'", rule_body)
        for op in operator_matches:
            info['operators'].add(op)
            info['has_operators'] = True
        
        # Find delimiters
        delimiter_matches = re.findall(r"'([\[\](){}\"']+)'", rule_body)
        for delim in delimiter_matches:
            info['delimiters'].add(delim)
            info['has_delimiters'] = True
        
        # Find field names
        field_matches = re.findall(r"field\('(\w+)'", rule_body)
        for field in field_matches:
            info['field_names'].add(field)
        
        return info
    
    def _identify_sticky_patterns(self):
        """Identify grammar patterns that may produce sticky tokens"""
        # Identify sticky-related node types based on grammar rules
        for rule_name, rule_info in self.grammar_rules.items():
            # Rules containing both operators and delimiters
            if rule_info['has_operators'] and rule_info['has_delimiters']:
                self.sticky_node_types.add(rule_name)
            
            # Specific expression types
            if any(keyword in rule_name for keyword in ['expression', 'operator', 'call', 'attribute', 'subscript']):
                self.sticky_node_types.add(rule_name)
            
            # Composite structures with multiple fields
            if len(rule_info['field_names']) > 1:
                self.sticky_node_types.add(rule_name)
        
        # Manually add known sticky-related nodes
        self.sticky_node_types.update([
            'attribute', 'subscript', 'call', 'binary_operator', 'comparison_operator',
            'assignment', 'augmented_assignment', 'string', 'concatenated_string',
            'parenthesized_expression', 'slice', 'keyword_argument'
        ])
    
    def extract_grammar_guided_segments(self, code: str) -> List[Dict]:
        """
        Extract code segments based on grammar rules
        
        Args:
            code: Source code
            
        Returns:
            List of code segments
        """
        # First use standard method to extract basic segments
        base_segments = self.standard_analyzer.extract_code_segments(code)
        
        # Enhance analysis with grammar rules
        enhanced_segments = []
        
        for segment in base_segments:
            enhanced_segment = segment.copy()
            
            # Add grammar rule information
            node_type = segment['node_type']
            enhanced_segment['grammar_rule_info'] = self.grammar_rules.get(node_type, {})
            enhanced_segment['is_sticky_relevant'] = node_type in self.sticky_node_types
            enhanced_segment['sticky_confidence'] = self._calculate_sticky_confidence(segment)
            enhanced_segment['operators_present'] = self._detect_operators_in_text(segment['text'])
            enhanced_segment['delimiters_present'] = self._detect_delimiters_in_text(segment['text'])
            
            enhanced_segments.append(enhanced_segment)
        
        # Sort by sticky relevance
        enhanced_segments.sort(key=lambda x: x['sticky_confidence'], reverse=True)
        
        return enhanced_segments
    
    def _calculate_sticky_confidence(self, segment: Dict) -> float:
        """Calculate confidence that a code segment will produce sticky tokens"""
        confidence = 0.0
        text = segment['text']
        node_type = segment['node_type']
        
        # Based on node type
        if node_type in self.sticky_node_types:
            confidence += 0.4
        
        # Based on grammar rule information
        rule_info = self.grammar_rules.get(node_type, {})
        if rule_info.get('has_operators'):
            confidence += 0.2
        if rule_info.get('has_delimiters'):
            confidence += 0.2
        if rule_info.get('has_precedence'):
            confidence += 0.1
        
        # Based on text content
        if self._detect_operators_in_text(text):
            confidence += 0.2
        if self._detect_delimiters_in_text(text):
            confidence += 0.2
        if len(text.strip()) > 3:
            confidence += 0.1
        
        # Based on complexity
        if segment.get('children_count', 0) > 1:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _detect_operators_in_text(self, text: str) -> Set[str]:
        """Detect operators in text"""
        operators = set()
        
        # Known operators from grammar rules
        for rule_info in self.grammar_rules.values():
            for op in rule_info.get('operators', set()):
                if op in text:
                    operators.add(op)
        
        # Common operators
        common_operators = {'+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', 
                          '<=', '>=', '&', '|', '^', '~', '<<', '>>', '**', '//'}
        for op in common_operators:
            if op in text:
                operators.add(op)
        
        return operators
    
    def _detect_delimiters_in_text(self, text: str) -> Set[str]:
        """Detect delimiters in text"""
        delimiters = set()
        
        delimiter_chars = {'(', ')', '[', ']', '{', '}', '"', "'", '.', ',', ';', ':'}
        for delim in delimiter_chars:
            if delim in text:
                delimiters.add(delim)
        
        return delimiters
    
    def analyze_with_grammar_guidance(self, model_name: str, code: str) -> Dict:
        """
        Perform sticky token analysis using grammar rule guidance
        
        Args:
            model_name: Tokenizer model name
            code: Source code
            
        Returns:
            Enhanced analysis results
        """
        # Extract grammar-guided code segments
        segments = self.extract_grammar_guided_segments(code)
        
        # Perform tokenization analysis on each segment
        segment_analyses = []
        all_sticky_tokens = []
        
        for segment_info in segments:
            try:
                segment_text = segment_info['text']
                
                # Skip segments that are too short
                if len(segment_text.strip()) < 2:
                    continue
                
                # Tokenization analysis
                tokenization_result = self.standard_analyzer.analyze_code_part_tokenization(
                    model_name, segment_text
                )
                
                # Grammar-enhanced analysis
                enhanced_analysis = {
                    **segment_info,
                    **tokenization_result,
                    'analysis_method': 'grammar_guided',
                    'grammar_enhanced': True
                }
                
                # Re-evaluate sticky tokens
                enhanced_sticky_tokens = self._enhance_sticky_detection(
                    tokenization_result['sticky_tokens'], segment_info
                )
                enhanced_analysis['sticky_tokens'] = enhanced_sticky_tokens
                enhanced_analysis['sticky_count'] = len(enhanced_sticky_tokens)
                
                segment_analyses.append(enhanced_analysis)
                
                # Collect enhanced sticky tokens
                for sticky_token in enhanced_sticky_tokens:
                    enhanced_sticky = {
                        **sticky_token,
                        'source_code_segment': segment_text,
                        'grammar_node_type': segment_info['node_type'],
                        'grammar_rule_info': segment_info.get('grammar_rule_info', {}),
                        'sticky_confidence': segment_info['sticky_confidence'],
                        'operators_context': list(segment_info['operators_present']),
                        'delimiters_context': list(segment_info['delimiters_present']),
                        'grammar_guided': True
                    }
                    all_sticky_tokens.append(enhanced_sticky)
                    
            except Exception as e:
                print(f"Warning: Grammar-guided analysis failed '{segment_info['text'][:50]}': {e}")
                continue
        
        # Sort sticky tokens by confidence
        all_sticky_tokens.sort(key=lambda x: x.get('sticky_confidence', 0), reverse=True)
        
        return {
            'model': model_name,
            'code': code,
            'language': 'python',
            'method': 'grammar_guided_sticky_analysis',
            'grammar_file': self.grammar_path,
            'total_segments': len(segments),
            'analyzed_segments': len(segment_analyses),
            'segment_analyses': segment_analyses,
            'sticky_tokens': all_sticky_tokens,
            'total_sticky_tokens': len(all_sticky_tokens),
            'grammar_guided': True,
            'grammar_rules_used': len(self.grammar_rules),
            'sticky_node_types': list(self.sticky_node_types)
        }
    
    def _enhance_sticky_detection(self, original_sticky_tokens: List[Dict], 
                                 segment_info: Dict) -> List[Dict]:
        """
        Enhance sticky token detection based on grammar information
        
        Args:
            original_sticky_tokens: Originally detected sticky tokens
            segment_info: Code segment information
            
        Returns:
            Enhanced sticky tokens
        """
        enhanced_tokens = []
        
        for token in original_sticky_tokens:
            enhanced_token = token.copy()
            
            # Adjust detection rules based on grammar rules
            grammar_rules = self._get_grammar_based_rules(token, segment_info)
            enhanced_token['detection_rules'].extend(grammar_rules)
            
            # Add grammar context
            enhanced_token['grammar_context'] = {
                'node_type': segment_info['node_type'],
                'has_operators': bool(segment_info['operators_present']),
                'has_delimiters': bool(segment_info['delimiters_present']),
                'confidence': segment_info['sticky_confidence']
            }
            
            enhanced_tokens.append(enhanced_token)
        
        return enhanced_tokens
    
    def _get_grammar_based_rules(self, token: Dict, segment_info: Dict) -> List[str]:
        """Generate additional detection rules based on grammar rules"""
        rules = []
        
        node_type = segment_info['node_type']
        rule_info = segment_info.get('grammar_rule_info', {})
        
        # Rules based on node type
        if node_type in ['binary_operator', 'comparison_operator']:
            rules.append('grammar_operator_context')
        elif node_type in ['attribute', 'subscript']:
            rules.append('grammar_access_context')
        elif node_type == 'call':
            rules.append('grammar_call_context')
        
        # Rules based on grammar rule features
        if rule_info.get('has_precedence'):
            rules.append('grammar_precedence_context')
        if rule_info.get('has_operators') and rule_info.get('has_delimiters'):
            rules.append('grammar_mixed_syntax')
        
        return rules
    
    def compare_with_standard(self, model_name: str, code: str) -> Dict:
        """
        Compare grammar-guided analysis with standard analysis
        
        Args:
            model_name: Tokenizer model name
            code: Source code
            
        Returns:
            Comparison results
        """
        # Grammar-guided analysis
        grammar_result = self.analyze_with_grammar_guidance(model_name, code)
        
        # Standard analysis
        standard_result = self.standard_analyzer.analyze_code_with_tree_sitter_split(model_name, code)
        
        # Extract sticky tokens
        grammar_sticky = set(t['token'] for t in grammar_result['sticky_tokens'])
        standard_sticky = set(t['token'] for t in standard_result['sticky_tokens'])
        
        # Calculate metrics
        comparison = {
            'code': code,
            'model': model_name,
            'grammar_guided': grammar_result,
            'standard_analysis': standard_result,
            'metrics': {
                'grammar_sticky_count': len(grammar_sticky),
                'standard_sticky_count': len(standard_sticky),
                'common_tokens': list(grammar_sticky & standard_sticky),
                'grammar_only': list(grammar_sticky - standard_sticky),
                'standard_only': list(standard_sticky - grammar_sticky),
                'precision_improvement': len(grammar_sticky) / max(len(standard_sticky), 1),
                'recall_ratio': len(grammar_sticky & standard_sticky) / max(len(standard_sticky), 1),
                'f1_score': self._calculate_f1_score(grammar_sticky, standard_sticky)
            }
        }
        
        return comparison
    
    def _calculate_f1_score(self, set1: Set, set2: Set) -> float:
        """Calculate F1 score"""
        if not set1 and not set2:
            return 1.0
        
        precision = len(set1 & set2) / len(set1) if set1 else 0
        recall = len(set1 & set2) / len(set2) if set2 else 0
        
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)


def main():
    """Demonstrate grammar-guided analyzer"""
    print("Grammar.js-Guided Sticky Token Analyzer Demo")
    print("="*60)
    
    try:
        analyzer = GrammarGuidedStickyAnalyzer()
        model_name = 'bigcode/starcoder2-3b'
        
        test_codes = [
            'x.value',
            'data["key"]',
            'items[0].process()',
            'if x.value > threshold: result = process(x.data)',
            'obj.method().attribute[index] += value * 2'
        ]
        
        for i, code in enumerate(test_codes, 1):
            print(f"\nTest case {i}: {code}")
            print("-" * 50)
            
            comparison = analyzer.compare_with_standard(model_name, code)
            metrics = comparison['metrics']
            
            print(f"Grammar-guided detected: {metrics['grammar_sticky_count']} sticky tokens")
            print(f"Standard method detected: {metrics['standard_sticky_count']} sticky tokens")
            print(f"Common detections: {len(metrics['common_tokens'])} tokens")
            print(f"Grammar-guided only: {metrics['grammar_only']}")
            print(f"Standard method only: {metrics['standard_only']}")
            print(f"Precision improvement: {metrics['precision_improvement']:.2f}")
            print(f"Recall ratio: {metrics['recall_ratio']:.2f}")
            print(f"F1 score: {metrics['f1_score']:.2f}")
        
    except Exception as e:
        print(f"Demo failed: {e}")


if __name__ == '__main__':
    main()