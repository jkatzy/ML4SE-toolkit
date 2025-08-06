#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified Test Script - Works with quick_analyzer.py
Tests basic Tree-sitter parsing and alignment score calculation functionality
"""

import os
import sys
from pathlib import Path
from tree_sitter import Language, Parser
from transformers import AutoTokenizer

def test_quick_analyzer_functionality():
    """Test core functionality of quick_analyzer.py"""
    print("=" * 60)
    print("Quick Analyzer Functionality Test")
    print("=" * 60)
    
    try:
        # Check compiled language libraries
        build_dir = Path('./build')
        python_library_path = build_dir / 'languages_python.so'
        
        if not python_library_path.exists():
            print("❌ Python language library not found")
            print("Please run quick_analyzer.py first to compile language libraries")
            return False
        
        print("✓ Found Python language library")
        
        # Test Python parser
        print("\nTesting Python parser...")
        parser = Parser()
        
        try:
            python_language = Language(str(python_library_path), 'python')
            parser.set_language(python_language)
            print("✓ Python parser loaded successfully")
        except Exception as e:
            print(f"❌ Python parser loading failed: {e}")
            return False
        
        # Initialize tokenizer
        print("\nInitializing tokenizer...")
        try:
            tokenizer = AutoTokenizer.from_pretrained('gpt2')
            print("✓ GPT-2 tokenizer loaded successfully")
        except Exception as e:
            print(f"❌ Tokenizer loading failed: {e}")
            return False
        
        # Test code sample
        test_code = '''
def fibonacci(n):
    """Calculate Fibonacci sequence"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test function
for i in range(10):
    result = fibonacci(i)
    print(f"fibonacci({i}) = {result}")
'''
        
        print("\nAnalyzing test code...")
        
        # Parse code
        code_bytes = test_code.encode('utf-8')
        tree = parser.parse(code_bytes)
        
        if tree.root_node.has_error:
            print("❌ Code parsing error")
            return False
        
        print("✓ Code parsed successfully")
        
        # Extract syntax rules
        def extract_rules(node, rules=None):
            if rules is None:
                rules = []
            
            if node.type and not node.type.startswith('ERROR'):
                rules.append({
                    'type': node.type,
                    'start_byte': node.start_byte,
                    'end_byte': node.end_byte,
                    'start_point': node.start_point,
                    'end_point': node.end_point,
                    'text': code_bytes[node.start_byte:node.end_byte].decode('utf-8', errors='ignore')[:30]
                })
            
            for child in node.children:
                extract_rules(child, rules)
            
            return rules
        
        rules = extract_rules(tree.root_node)
        print(f"✓ Extracted {len(rules)} syntax rules")
        
        # Tokenization
        tokens = tokenizer.encode(test_code)
        token_texts = [tokenizer.decode([token]) for token in tokens]
        print(f"✓ Generated {len(tokens)} tokens")
        
        # Calculate token boundaries
        token_boundaries = []
        current_pos = 0
        
        for token_text in token_texts:
            # Handle special characters
            if token_text.strip():
                token_start = test_code.find(token_text, current_pos)
                if token_start != -1:
                    token_end = token_start + len(token_text)
                    token_boundaries.append((token_start, token_end))
                    current_pos = token_end
                else:
                    # If not found, use current position
                    token_boundaries.append((current_pos, current_pos + 1))
                    current_pos += 1
            else:
                token_boundaries.append((current_pos, current_pos + 1))
                current_pos += 1
        
        print(f"✓ Token boundary calculation completed")
        
        # Calculate alignment score
        aligned_rules = 0
        tolerance = 1  # Allow 1 character error margin
        
        for rule in rules:
            rule_start = rule['start_byte']
            rule_end = rule['end_byte']
            
            # Check start position alignment
            start_aligned = any(abs(rule_start - tb[0]) <= tolerance for tb in token_boundaries)
            # Check end position alignment
            end_aligned = any(abs(rule_end - tb[1]) <= tolerance for tb in token_boundaries)
            
            if start_aligned and end_aligned:
                aligned_rules += 1
        
        # Calculate final score
        alignment_score = (aligned_rules / len(rules) * 100) if rules else 0
        
        print("\n" + "=" * 40)
        print("Test Results")
        print("=" * 40)
        print(f"Rule-level Alignment Score: {alignment_score:.2f}%")
        print(f"Total syntax rules: {len(rules)}")
        print(f"Aligned rules: {aligned_rules}")
        print(f"Total tokens: {len(tokens)}")
        print(f"Token boundaries: {len(token_boundaries)}")
        
        # Display rule type statistics
        rule_types = {}
        for rule in rules:
            rule_type = rule['type']
            rule_types[rule_type] = rule_types.get(rule_type, 0) + 1
        
        print(f"\nSyntax rule type statistics (top 10):")
        sorted_rules = sorted(rule_types.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (rule_type, count) in enumerate(sorted_rules, 1):
            print(f"  {i:2d}. {rule_type}: {count}")
        
        # Display some example rules
        print(f"\nExample syntax rules (first 5):")
        for i, rule in enumerate(rules[:5], 1):
            text_preview = rule['text'].replace('\n', '\\n')
            print(f"  {i}. {rule['type']}: '{text_preview}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_code_samples():
    """Test files in the code_samples directory"""
    print("\n" + "=" * 60)
    print("Testing Code Samples Directory")
    print("=" * 60)
    
    code_samples_dir = Path('./code_samples')
    if not code_samples_dir.exists():
        print("❌ code_samples directory does not exist")
        return False
    
    print("✓ code_samples directory exists")
    
    # Check sample file directories for each language
    expected_dirs = {
        'python': 'python',
        'javascript': 'javascript', 
        'typescript': 'typescript',
        'java': 'java',
        'c': 'c',
        'cpp': 'cpp',
        'csharp': 'csharp',
        'go': 'go',
        'ruby': 'ruby',
        'rust': 'rust',
        'scala': 'scala'
    }
    
    found_files = 0
    total_files = 0
    
    for lang, dirname in expected_dirs.items():
        dir_path = code_samples_dir / dirname
        if dir_path.exists() and dir_path.is_dir():
            # Count files in directory
            files = list(dir_path.glob('*'))
            file_count = len([f for f in files if f.is_file()])
            if file_count > 0:
                print(f"✓ {dirname}/ ({file_count} files)")
                found_files += 1
                total_files += file_count
            else:
                print(f"⚠️  {dirname}/ (directory is empty)")
        else:
            print(f"❌ {dirname}/ directory does not exist")
    
    print(f"\nFound {found_files}/{len(expected_dirs)} language directories, {total_files} sample files in total")
    return found_files > 0

def main():
    """Main test function"""
    print("Quick Analyzer Simplified Test")
    print("Testing Tree-sitter rule-level alignment score calculation functionality")
    
    # Test core functionality
    core_test_passed = test_quick_analyzer_functionality()
    
    # Test code samples
    samples_test_passed = test_code_samples()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if core_test_passed:
        print("✓ Core functionality test passed")
    else:
        print("❌ Core functionality test failed")
    
    if samples_test_passed:
        print("✓ Code samples test passed")
    else:
        print("❌ Code samples test failed")
    
    if core_test_passed and samples_test_passed:
        print("\n🎉 All tests passed! You can use analyzer.py for complete analysis")
        print("\nRecommended command:")
        print("  python analyzer.py")
    else:
        print("\n⚠️  Some tests failed, please check your environment configuration")
        if not core_test_passed:
            print("  - Make sure all dependencies are installed: pip install -r requirements.txt")
            print("  - Run analyzer.py first to compile language libraries")
    
    return core_test_passed and samples_test_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)