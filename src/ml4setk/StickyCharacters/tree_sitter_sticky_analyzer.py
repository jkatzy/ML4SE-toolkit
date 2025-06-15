from typing import List, Dict, Set, Tuple, Optional
import re
try:
    # Try the newer tree-sitter-languages approach first
    from tree_sitter_languages import get_language, get_parser
    USE_TREE_SITTER_LANGUAGES = True
except ImportError:
    # Fallback to individual language parsers
    USE_TREE_SITTER_LANGUAGES = False
    try:
        import tree_sitter
        import tree_sitter_python
        import tree_sitter_javascript
        import tree_sitter_java
    except ImportError as e:
        print(f"Warning: Tree-sitter not available: {e}")
        tree_sitter = None

from transformers import AutoTokenizer


class TreeSitterStickyAnalyzer:
    """
    Tree-sitter based sticky character analyzer that uses AST information
    to more accurately identify sticky tokens in code.
    """
    
    def __init__(self, language: str = 'python'):
        """
        Initialize the analyzer with a specific language.
        
        Args:
            language: Programming language to analyze ('python', 'javascript', 'java')
        """
        self.language_name = language
        self.language = None
        self.parser = None
        
        # Initialize tree-sitter with fallback options
        self._init_tree_sitter(language)
        
        # Language-specific node types that indicate semantic boundaries
        self.semantic_boundary_nodes = self._get_semantic_boundary_nodes(language)
        self.operator_nodes = self._get_operator_nodes(language)
        self.identifier_nodes = self._get_identifier_nodes(language)
    
    def _init_tree_sitter(self, language: str):
        """Initialize tree-sitter parser with fallback options."""
        try:
            if USE_TREE_SITTER_LANGUAGES:
                # Try the tree-sitter-languages approach
                try:
                    self.language = get_language(language)
                    self.parser = get_parser(language)
                except Exception as e:
                    print(f"Warning: tree-sitter-languages failed ({e}), trying fallback...")
                    self._init_fallback_parser(language)
            else:
                self._init_fallback_parser(language)
                
        except Exception as e:
            print(f"Error initializing tree-sitter: {e}")
            print("Tree-sitter functionality will be disabled.")
            
    def _init_fallback_parser(self, language: str):
        """Initialize using individual tree-sitter language packages."""
        if tree_sitter is None:
            raise ImportError("Tree-sitter not available")
            
        language_modules = {
            'python': tree_sitter_python,
            'javascript': tree_sitter_javascript, 
            'java': tree_sitter_java
        }
        
        if language not in language_modules:
            raise ValueError(f"Unsupported language: {language}")
            
        try:
            # Get language from the specific module
            lang_module = language_modules[language]
            
            # Try different API approaches
            try:
                # New API approach
                self.language = tree_sitter.Language(lang_module.language())
                self.parser = tree_sitter.Parser(self.language)
            except (TypeError, AttributeError):
                # Older API approach
                self.language = tree_sitter.Language(lang_module.language())
                self.parser = tree_sitter.Parser()
                self.parser.set_language(self.language)
                
        except Exception as e:
            print(f"Failed to initialize {language} parser: {e}")
            self.language = None
            self.parser = None
    
    def _get_semantic_boundary_nodes(self, language: str) -> Set[str]:
        """Get node types that represent semantic boundaries for each language."""
        boundaries = {
            'python': {
                'function_definition', 'class_definition', 'if_statement', 'for_statement',
                'while_statement', 'with_statement', 'try_statement', 'assignment',
                'expression_statement', 'import_statement', 'return_statement',
                'call', 'attribute', 'subscript', 'binary_operator', 'comparison_operator'
            },
            'javascript': {
                'function_declaration', 'function_expression', 'class_declaration',
                'if_statement', 'for_statement', 'while_statement', 'try_statement',
                'assignment_expression', 'call_expression', 'member_expression',
                'binary_expression', 'unary_expression', 'update_expression'
            },
            'java': {
                'method_declaration', 'class_declaration', 'interface_declaration',
                'if_statement', 'for_statement', 'while_statement', 'try_statement',
                'assignment_expression', 'method_invocation', 'field_access',
                'binary_expression', 'unary_expression', 'update_expression'
            }
        }
        return boundaries.get(language, set())
    
    def _get_operator_nodes(self, language: str) -> Set[str]:
        """Get node types that represent operators."""
        operators = {
            'python': {
                'binary_operator', 'unary_operator', 'comparison_operator',
                'boolean_operator', 'assignment'
            },
            'javascript': {
                'binary_expression', 'unary_expression', 'update_expression',
                'assignment_expression'
            },
            'java': {
                'binary_expression', 'unary_expression', 'update_expression',
                'assignment_expression'
            }
        }
        return operators.get(language, set())
    
    def _get_identifier_nodes(self, language: str) -> Set[str]:
        """Get node types that represent identifiers."""
        identifiers = {
            'python': {'identifier', 'attribute'},
            'javascript': {'identifier', 'property_identifier'},
            'java': {'identifier', 'field_access'}
        }
        return identifiers.get(language, set())
    
    def parse_code_with_ast(self, code: str) -> List[Dict]:
        """
        Parse code and extract AST node information for each character position.
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of dictionaries containing AST context for each position
        """
        if self.parser is None:
            raise RuntimeError("Tree-sitter parser not available. Check initialization errors.")
            
        try:
            tree = self.parser.parse(code.encode())
            ast_contexts = []
            
            def traverse_node(node, depth=0):
                """Recursively traverse AST nodes to collect context information."""
                context = {
                    'node_type': node.type,
                    'start_byte': node.start_byte,
                    'end_byte': node.end_byte,
                    'start_point': node.start_point,
                    'end_point': node.end_point,
                    'depth': depth,
                    'text': code[node.start_byte:node.end_byte],
                    'is_semantic_boundary': node.type in self.semantic_boundary_nodes,
                    'is_operator': node.type in self.operator_nodes,
                    'is_identifier': node.type in self.identifier_nodes,
                    'parent_type': node.parent.type if node.parent else None,
                    'children_types': [child.type for child in node.children]
                }
                ast_contexts.append(context)
                
                for child in node.children:
                    traverse_node(child, depth + 1)
            
            traverse_node(tree.root_node)
            return ast_contexts
            
        except Exception as e:
            raise RuntimeError(f"Failed to parse code with AST: {e}")
    
    def get_ast_context_for_token(self, token_start: int, token_end: int, 
                                 ast_contexts: List[Dict]) -> Dict:
        """
        Get AST context information for a specific token position.
        
        Args:
            token_start: Token start byte position
            token_end: Token end byte position
            ast_contexts: List of AST contexts from parse_code_with_ast
            
        Returns:
            Dictionary containing relevant AST context information
        """
        relevant_contexts = []
        
        for context in ast_contexts:
            # Find nodes that contain or overlap with the token
            if (context['start_byte'] <= token_start < context['end_byte'] or
                context['start_byte'] < token_end <= context['end_byte'] or
                (token_start <= context['start_byte'] and token_end >= context['end_byte'])):
                relevant_contexts.append(context)
        
        if not relevant_contexts:
            return {'node_types': [], 'is_at_boundary': False, 'context_info': {}}
        
        # Sort by depth (deepest first) to get most specific context
        relevant_contexts.sort(key=lambda x: x['depth'], reverse=True)
        
        return {
            'node_types': [ctx['node_type'] for ctx in relevant_contexts],
            'deepest_node': relevant_contexts[0],
            'is_at_boundary': any(ctx['is_semantic_boundary'] for ctx in relevant_contexts),
            'crosses_operator': any(ctx['is_operator'] for ctx in relevant_contexts),
            'crosses_identifier': any(ctx['is_identifier'] for ctx in relevant_contexts),
            'context_info': {
                'spans_multiple_nodes': len(set(ctx['node_type'] for ctx in relevant_contexts)) > 1,
                'deepest_node_type': relevant_contexts[0]['node_type'],
                'parent_node_type': relevant_contexts[0]['parent_type'],
                'all_node_types': list(set(ctx['node_type'] for ctx in relevant_contexts))
            }
        }
    
    def is_sticky_token_ast(self, token: str, token_start: int, token_end: int,
                           ast_contexts: List[Dict]) -> Tuple[bool, Dict]:
        """
        Determine if a token is sticky using AST-based analysis.
        
        Args:
            token: The token string
            token_start: Token start position in code
            token_end: Token end position in code
            ast_contexts: AST context information
            
        Returns:
            Tuple of (is_sticky: bool, analysis_info: Dict)
        """
        # Clean token (remove tokenizer prefixes)
        clean_token = token.lstrip('▁Ġ')
        
        # Get AST context for this token
        ast_context = self.get_ast_context_for_token(token_start, token_end, ast_contexts)
        
        # Basic character analysis
        has_letter = bool(re.search(r'[A-Za-z_]', clean_token))
        has_digit = any(ch.isdigit() for ch in clean_token)
        has_symbol = bool(re.search(r'[^\w\s]', clean_token))
        
        # AST-based sticky detection rules
        analysis_info = {
            'token': token,
            'clean_token': clean_token,
            'has_letter': has_letter,
            'has_digit': has_digit,
            'has_symbol': has_symbol,
            'ast_context': ast_context,
            'detection_rules': []
        }
        
        is_sticky = False
        
        # Skip pure whitespace tokens
        if len(clean_token.strip()) == 0:
            return False, analysis_info
            
        # Rule 1: Clear sticky patterns - tokens with mixed char types
        if len(clean_token) > 1:
            # Pattern 1a: Alphanumeric mixed with symbols
            if (has_letter or has_digit) and has_symbol:
                if (re.search(r'[A-Za-z_]\W', clean_token) or  # identifier followed by non-word
                    re.search(r'\W[A-Za-z_]', clean_token) or  # non-word followed by identifier
                    re.search(r'\d\W', clean_token) or         # digit followed by non-word
                    re.search(r'\W\d', clean_token)):          # non-word followed by digit
                    is_sticky = True
                    analysis_info['detection_rules'].append('mixed_alphanumeric_symbols')
            
            # Pattern 1b: Multiple different symbols combined
            if has_symbol and not has_letter and not has_digit:
                symbol_types = set()
                for char in clean_token:
                    if char in '[](){}':
                        symbol_types.add('bracket')
                    elif char in '"\'`':
                        symbol_types.add('quote')
                    elif char in '+-*/%=<>!&|^~':
                        symbol_types.add('operator')
                    elif char in '.,;:':
                        symbol_types.add('punctuation')
                
                if len(symbol_types) > 1:
                    is_sticky = True
                    analysis_info['detection_rules'].append('mixed_symbol_types')
        
        # Rule 2: AST-based detection - spans multiple meaningful nodes
        if ast_context['context_info'].get('spans_multiple_nodes', False):
            node_types = set(ast_context['context_info'].get('all_node_types', []))
            # Only flag if spanning different semantic categories
            semantic_types = {'identifier', 'string', 'integer', 'float', 'attribute', 'subscript'}
            operator_types = {'.', '[', ']', '(', ')', '=', '+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '"', "'"}
            
            has_semantic = any(nt in semantic_types for nt in node_types)
            has_operator = any(nt in operator_types for nt in node_types)
            
            if has_semantic and has_operator and len(clean_token) > 1:
                is_sticky = True
                analysis_info['detection_rules'].append('spans_semantic_operator_boundary')
        
        # Rule 3: Crosses identifier and operator boundaries
        if ast_context['crosses_identifier'] and ast_context['crosses_operator']:
            if len(clean_token) > 1:
                is_sticky = True
                analysis_info['detection_rules'].append('crosses_identifier_operator')
        
        # Rule 4: Token at semantic boundaries with mixed content
        if ast_context['is_at_boundary'] and len(clean_token) > 1:
            if has_symbol:  # Any symbol at boundary is potentially interesting
                is_sticky = True
                analysis_info['detection_rules'].append('at_semantic_boundary_with_symbols')
        
        return is_sticky, analysis_info
    
    def extract_code_segments(self, code: str) -> List[Dict]:
        """
        Extract meaningful code segments that preserve syntactic structure.
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of dictionaries containing code segments with their AST context
        """
        if self.parser is None:
            raise RuntimeError("Tree-sitter parser not available. Check initialization errors.")
            
        try:
            tree = self.parser.parse(code.encode())
            code_segments = []
            
            def extract_syntactic_segments(node, depth=0):
                """Extract syntactically meaningful code segments."""
                node_text = code[node.start_byte:node.end_byte]
                
                # Skip empty nodes
                if not node_text.strip():
                    return
                
                # Define what constitutes a meaningful code segment
                meaningful_node_types = {
                    # Expressions that could contain sticky tokens
                    'attribute', 'subscript', 'call', 'binary_operator', 'comparison_operator',
                    'member_expression', 'field_access', 'method_invocation',
                    # Complete syntactic units
                    'assignment', 'expression_statement', 'if_statement', 'for_statement',
                    'while_statement', 'function_definition', 'class_definition',
                    # Composite expressions
                    'parenthesized_expression', 'list', 'dictionary', 'tuple',
                    # String and numeric literals with operators
                    'string', 'integer', 'float', 'identifier'
                }
                
                # Check if this node represents a meaningful segment
                is_meaningful_segment = (
                    node.type in meaningful_node_types or
                    node.type in self.semantic_boundary_nodes or
                    # Include nodes that span multiple tokens and might contain sticky patterns
                    (len(node.children) > 1 and len(node_text.strip()) > 1)
                )
                
                segment_info = {
                    'text': node_text,
                    'node_type': node.type,
                    'start_byte': node.start_byte,
                    'end_byte': node.end_byte,
                    'depth': depth,
                    'parent_type': node.parent.type if node.parent else None,
                    'children_count': len(node.children),
                    'is_semantic_boundary': node.type in self.semantic_boundary_nodes,
                    'is_operator': node.type in self.operator_nodes,
                    'is_identifier': node.type in self.identifier_nodes,
                    'is_meaningful_segment': is_meaningful_segment
                }
                
                # Add meaningful segments
                if is_meaningful_segment and len(node_text.strip()) > 0:
                    code_segments.append(segment_info)
                
                # For composite nodes, also process children
                # But only if the current node is not already a good segment
                if not is_meaningful_segment or node.type in ['module', 'program', 'source_file']:
                    for child in node.children:
                        extract_syntactic_segments(child, depth + 1)
            
            extract_syntactic_segments(tree.root_node)
            
            # Filter and deduplicate segments
            filtered_segments = []
            seen_ranges = set()
            
            for segment in code_segments:
                # Skip very short or single-character segments unless they're operators
                if len(segment['text'].strip()) < 2 and not segment['is_operator']:
                    continue
                    
                # Skip pure whitespace
                if not segment['text'].strip():
                    continue
                
                # Avoid duplicate ranges
                range_key = (segment['start_byte'], segment['end_byte'])
                if range_key in seen_ranges:
                    continue
                seen_ranges.add(range_key)
                
                filtered_segments.append(segment)
            
            # Sort by position and remove nested duplicates
            filtered_segments.sort(key=lambda x: (x['start_byte'], x['end_byte']))
            
            # Remove segments that are completely contained within other segments
            final_segments = []
            for i, segment in enumerate(filtered_segments):
                is_contained = False
                for j, other in enumerate(filtered_segments):
                    if i != j and (other['start_byte'] <= segment['start_byte'] and 
                                 segment['end_byte'] <= other['end_byte'] and
                                 other['text'] != segment['text']):
                        is_contained = True
                        break
                if not is_contained:
                    final_segments.append(segment)
            
            return final_segments
            
        except Exception as e:
            raise RuntimeError(f"Failed to extract code segments: {e}")

    def extract_code_parts(self, code: str) -> List[Dict]:
        """
        Legacy method - now calls extract_code_segments for backward compatibility.
        """
        return self.extract_code_segments(code)
    
    def analyze_code_part_tokenization(self, model_name: str, code_part: str) -> Dict:
        """
        Analyze tokenization of a single code part.
        
        Args:
            model_name: Name of the tokenizer model
            code_part: Code part to analyze
            
        Returns:
            Dictionary containing tokenization analysis
        """
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Tokenize the code part
        ids = tokenizer.encode(code_part, add_special_tokens=False)
        tokens = tokenizer.convert_ids_to_tokens(ids)
        
        # Check for sticky tokens using simple heuristics
        sticky_tokens = []
        for i, token in enumerate(tokens):
            clean_token = token.lstrip('▁Ġ')
            
            # Basic sticky detection: mixed character types
            has_letter = bool(re.search(r'[A-Za-z_]', clean_token))
            has_digit = any(ch.isdigit() for ch in clean_token)
            has_symbol = bool(re.search(r'[^\w\s]', clean_token))
            
            is_sticky = False
            detection_rules = []
            
            if len(clean_token) > 1:
                # Mixed alphanumeric and symbols
                if (has_letter or has_digit) and has_symbol:
                    if (re.search(r'[A-Za-z_]\W', clean_token) or
                        re.search(r'\W[A-Za-z_]', clean_token) or
                        re.search(r'\d\W', clean_token) or
                        re.search(r'\W\d', clean_token)):
                        is_sticky = True
                        detection_rules.append('mixed_alphanumeric_symbols')
                
                # Multiple symbol types
                if has_symbol and not has_letter and not has_digit:
                    symbol_types = set()
                    for char in clean_token:
                        if char in '[](){}':
                            symbol_types.add('bracket')
                        elif char in '"\'`':
                            symbol_types.add('quote')
                        elif char in '+-*/%=<>!&|^~':
                            symbol_types.add('operator')
                        elif char in '.,;:':
                            symbol_types.add('punctuation')
                    
                    if len(symbol_types) > 1:
                        is_sticky = True
                        detection_rules.append('mixed_symbol_types')
            
            if is_sticky:
                sticky_tokens.append({
                    'token': token,
                    'clean_token': clean_token,
                    'position': i,
                    'detection_rules': detection_rules
                })
        
        return {
            'code_part': code_part,
            'tokens': tokens,
            'token_count': len(tokens),
            'sticky_tokens': sticky_tokens,
            'sticky_count': len(sticky_tokens)
        }
    
    def analyze_code_with_tree_sitter_split(self, model_name: str, code: str) -> Dict:
        """
        Analyze code using the new tree-sitter split approach:
        1. Use tree-sitter to split code into syntactically meaningful segments
        2. Tokenize each code segment separately
        3. Check for sticky tokens in each segment
        
        Args:
            model_name: Name of the tokenizer model
            code: Source code to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        # Step 1: Extract code segments using tree-sitter
        code_segments = self.extract_code_segments(code)
        
        # Step 2: Analyze tokenization for each segment
        segment_analyses = []
        all_sticky_tokens = []
        
        for segment_info in code_segments:
            try:
                # Get the actual code text for this segment
                segment_text = segment_info['text']
                
                # Skip very short segments that are unlikely to contain sticky tokens
                if len(segment_text.strip()) < 2:
                    continue
                
                # Analyze this code segment
                tokenization_result = self.analyze_code_part_tokenization(
                    model_name, segment_text
                )
                
                # Combine segment info with tokenization result
                segment_analysis = {
                    **segment_info,
                    **tokenization_result,
                    'segment_type': 'code_segment'  # Mark as code segment vs individual token
                }
                segment_analyses.append(segment_analysis)
                
                # Collect sticky tokens with full context
                for sticky_token in tokenization_result['sticky_tokens']:
                    sticky_token_full = {
                        **sticky_token,
                        'source_code_segment': segment_text,
                        'ast_node_type': segment_info['node_type'],
                        'ast_context': segment_info,
                        'segment_start_byte': segment_info['start_byte'],
                        'segment_end_byte': segment_info['end_byte']
                    }
                    all_sticky_tokens.append(sticky_token_full)
                    
            except Exception as e:
                print(f"Warning: Failed to analyze code segment '{segment_info['text'][:50]}': {e}")
                continue
        
        return {
            'model': model_name,
            'code': code,
            'language': self.language_name,
            'method': 'tree_sitter_segment_then_tokenize',
            'total_code_segments': len(code_segments),
            'analyzed_segments': len(segment_analyses),
            'segment_analyses': segment_analyses,
            'sticky_tokens': all_sticky_tokens,
            'total_sticky_tokens': len(all_sticky_tokens),
            'analysis_type': 'syntactic_code_segments'
        }

    def analyze_code_tokenization_ast(self, model_name: str, code: str) -> Dict:
        """
        Analyze code tokenization using AST-based sticky token detection.
        
        Args:
            model_name: Name of the tokenizer model
            code: Source code to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        # Get tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        use_offsets = getattr(tokenizer, 'is_fast', False)
        
        # Tokenize with offsets
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
        
        # Parse AST
        ast_contexts = self.parse_code_with_ast(code)
        
        # Analyze each token
        analysis_table = []
        sticky_tokens = []
        
        for token, (start, end) in zip(tokens, offsets):
            code_piece = code[start:end]
            is_sticky, analysis_info = self.is_sticky_token_ast(
                token, start, end, ast_contexts
            )
            
            row = {
                'code_piece': code_piece,
                'token': token,
                'token_id': tokenizer.convert_tokens_to_ids(token),
                'offset': (start, end),
                'sticky': is_sticky,
                'analysis': analysis_info
            }
            
            analysis_table.append(row)
            if is_sticky:
                sticky_tokens.append(row)
        
        return {
            'model': model_name,
            'code': code,
            'language': self.language_name,
            'method': 'tree_sitter_ast',
            'table': analysis_table,
            'sticky_tokens': sticky_tokens,
            'ast_contexts': ast_contexts
        }