"""
Language detection module for automatic grammar selection.
"""

import os
from typing import Dict, Optional, List


class LanguageDetector:
    """Detects programming language from file extensions and content."""
    
    # File extension to language mapping
    EXTENSION_MAP = {
        '.py': 'python',
        '.js': 'javascript', 
        '.jsx': 'javascript',
        '.ts': 'javascript',
        '.tsx': 'javascript',
        '.java': 'java',
        '.c': 'c',
        '.cc': 'c++',
        '.cpp': 'c++',
        '.cxx': 'c++',
        '.c++': 'c++',
        '.go': 'go',
        '.rs': 'rust',
        '.jl': 'julia',
        '.r': 'r',
        '.R': 'r',
        '.sql': 'sql',
        '.g4': 'antlr'
    }
    
    # Language priority order for ambiguous cases
    LANGUAGE_PRIORITY = [
        'python', 'javascript', 'java', 'c++', 'c', 'go', 
        'rust', 'julia', 'r', 'sql', 'antlr'
    ]
    
    @classmethod
    def detect_from_filename(cls, filename: str) -> Optional[str]:
        """
        Detect language from filename extension.
        
        Args:
            filename: Name of the file
            
        Returns:
            Detected language name or None if not detected
        """
        _, ext = os.path.splitext(filename.lower())
        return cls.EXTENSION_MAP.get(ext)
    
    @classmethod
    def detect_from_content(cls, content: str, filename: str = "") -> Optional[str]:
        """
        Detect language from file content with filename as fallback.
        
        Args:
            content: File content
            filename: Optional filename for extension detection
            
        Returns:
            Detected language name or None if not detected
        """
        # First try filename extension
        if filename:
            lang = cls.detect_from_filename(filename)
            if lang:
                return lang
        
        # Content-based detection patterns
        content_patterns = {
            'python': [
                r'def\s+\w+\s*\(',
                r'import\s+\w+',
                r'from\s+\w+\s+import',
                r'if\s+__name__\s*==\s*["\']__main__["\']',
                r'#.*python',
                r'print\s*\('
            ],
            'javascript': [
                r'function\s+\w+\s*\(',
                r'const\s+\w+\s*=',
                r'let\s+\w+\s*=',
                r'var\s+\w+\s*=',
                r'=>\s*{',
                r'console\.log\s*\(',
                r'require\s*\(',
                r'module\.exports'
            ],
            'java': [
                r'public\s+class\s+\w+',
                r'public\s+static\s+void\s+main',
                r'import\s+java\.',
                r'System\.out\.print',
                r'@Override',
                r'extends\s+\w+'
            ],
            'c++': [
                r'#include\s*<.*>',
                r'std::\w+',
                r'using\s+namespace\s+std',
                r'cout\s*<<',
                r'cin\s*>>',
                r'int\s+main\s*\('
            ],
            'c': [
                r'#include\s*<.*\.h>',
                r'printf\s*\(',
                r'scanf\s*\(',
                r'malloc\s*\(',
                r'int\s+main\s*\('
            ]
        }
        
        # Score each language based on pattern matches
        scores = {}
        for lang, patterns in content_patterns.items():
            score = 0
            for pattern in patterns:
                import re
                if re.search(pattern, content, re.IGNORECASE):
                    score += 1
            if score > 0:
                scores[lang] = score
        
        # Return language with highest score
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return None
    
    @classmethod
    def get_available_languages(cls) -> List[str]:
        """Get list of all supported languages."""
        return list(set(cls.EXTENSION_MAP.values()))
    
    @classmethod
    def get_grammar_file(cls, language: str, grammars_dir: str = "grammars") -> Optional[str]:
        """
        Get the tree-sitter grammar file path for a language.
        
        Args:
            language: Programming language name
            grammars_dir: Directory containing grammar files
            
        Returns:
            Path to grammar file or None if not found
        """
        grammar_filename = f"{language}.js"
        grammar_path = os.path.join(grammars_dir, grammar_filename)
        
        if os.path.exists(grammar_path):
            return grammar_path
        
        return None