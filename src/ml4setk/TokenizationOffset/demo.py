#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Alignment Score Calculation Demo
Clearly demonstrates the alignment calculation process between AST rules and tokenizer
"""

import sys
from pathlib import Path
from tree_sitter import Language, Parser
from transformers import AutoTokenizer
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

def main():
    """Demonstrates the calculation process of alignment score"""
    print("=" * 60)
    print("Simple Alignment Score Calculation Demo")
    print("=" * 60)
    
    # Initialize Tree-sitter parser
    build_dir = Path('./build')
    python_library_path = build_dir / 'languages_python.so'
    
    if not python_library_path.exists():
        print("❌ Python language library not found")
        print("Please run analyzer.py first to compile language libraries")
        return False
    
    # Initialize parser and tokenizer
    parser = Parser()
    python_language = Language(str(python_library_path), 'python')
    parser.set_language(python_language)
    tokenizer = AutoTokenizer.from_pretrained('gpt2')
    
    # Use a very simple code example
    test_code = '''
def merge_sort(arr):
    """
    Sorts a list in ascending order using the merge sort algorithm.

    Args:
        arr: The list to be sorted.
    """
    if len(arr) > 1:
        # Find the middle of the list
        mid = len(arr) // 2
        
        # Divide the list into two halves
        L = arr[:mid]  # Left half
        R = arr[mid:]  # Right half

        # Recursively sort both halves
        merge_sort(L)
        merge_sort(R)

        # Merge the sorted halves back together
        i = j = k = 0
        
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Check if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
'''
    
    print("\nAnalyzing code example:")
    print(test_code)
    
    # 1. Parse code to get AST
    code_bytes = test_code.encode('utf-8')
    tree = parser.parse(code_bytes)
    
    # 2. Extract syntax rules
    rules = []
    
    def extract_rules(node, parent_id=None, rule_id=0):
        current_id = rule_id
        
        if node.type and not node.type.startswith('ERROR'):
            rule = {
                'id': current_id,
                'parent_id': parent_id,
                'type': node.type,
                'start_byte': node.start_byte,
                'end_byte': node.end_byte,
                'text': code_bytes[node.start_byte:node.end_byte].decode('utf-8', errors='ignore')
            }
            rules.append(rule)
            parent_id = current_id
            rule_id += 1
        
        for child in node.children:
            rule_id = extract_rules(child, parent_id, rule_id)
        
        return rule_id
    
    extract_rules(tree.root_node)
    
    # 3. Tokenize the code
    tokens = tokenizer.encode(test_code)
    token_texts = [tokenizer.decode([token]) for token in tokens]
    
    # 4. Calculate token boundaries (consistently using byte offsets)
    token_boundaries = []
    current_pos = 0
    
    # Convert code string to byte array to consistently use byte offsets
    code_bytes = test_code.encode('utf-8')
    
    for token_text in token_texts:
        token_bytes = token_text.encode('utf-8')
        if token_bytes.strip():
            # Search for tokenization at byte level
            token_start = -1
            for i in range(current_pos, len(code_bytes) - len(token_bytes) + 1):
                if code_bytes[i:i+len(token_bytes)] == token_bytes:
                    token_start = i
                    break
            
            if token_start != -1:
                token_end = token_start + len(token_bytes)
                token_boundaries.append((token_start, token_end))
                current_pos = token_end
            else:
                token_boundaries.append((current_pos, current_pos + 1))
                current_pos += 1
        else:
            token_boundaries.append((current_pos, current_pos + 1))
            current_pos += 1
    
    # 5. Create token table
    token_data = []
    for i, (token, (start, end)) in enumerate(zip(token_texts, token_boundaries)):
        token_data.append({
            'Token ID': i,
            'Token': repr(token),
            'Start Position': start,
            'End Position': end,
            'Text': repr(test_code[start:end]) if start < len(test_code) and end <= len(test_code) else 'N/A'
        })
    
    print("\nTokenization Results:")
    print(tabulate(token_data, headers='keys', tablefmt='grid'))
    
    # 6. Create rule table
    rule_data = []
    for rule in rules:
        rule_data.append({
            'Rule ID': rule['id'],
            'Rule Type': rule['type'],
            'Start Position': rule['start_byte'],
            'End Position': rule['end_byte'],
            'Text': repr(rule['text'])
        })
    
    print("\nAST Rules:")
    print(tabulate(rule_data, headers='keys', tablefmt='grid'))
    
    # 7. Calculate alignment (using analyzer.py method)
    tolerance = 1  # Allow 1 byte error margin
    alignment_results = []
    
    for rule in rules:
        rule_start = rule['start_byte']
        rule_end = rule['end_byte']
        
        # Use the method from analyzer.py to check alignment
        # Use list comprehension to quickly check if any token boundary aligns with rule boundary
        start_aligned = any(abs(rule_start - tb[0]) <= tolerance for tb in token_boundaries)
        end_aligned = any(abs(rule_end - tb[1]) <= tolerance for tb in token_boundaries)
        
        # Keep detailed information records - find the closest token and distance
        start_closest_token = None
        start_closest_distance = float('inf')
        end_closest_token = None
        end_closest_distance = float('inf')
        
        # Find the closest token (even if already aligned, calculate the closest token)
        for i, (tb_start, tb_end) in enumerate(token_boundaries):
            # Calculate starting position distance
            start_distance = abs(rule_start - tb_start)
            if start_distance < start_closest_distance:
                start_closest_token = i
                start_closest_distance = start_distance
            
            # Calculate ending position distance
            end_distance = abs(rule_end - tb_end)
            if end_distance < end_closest_distance:
                end_closest_token = i
                end_closest_distance = end_distance
        
        # Record alignment results
        alignment_results.append({
            'Rule ID': rule['id'],
            'Rule Type': rule['type'],
            'Rule Text': repr(rule['text']),
            'Start Position': rule['start_byte'],
            'Closest Token (Start)': start_closest_token,
            'Start Distance': start_closest_distance,
            'Start Aligned': '✓' if start_aligned else '✗',
            'End Position': rule['end_byte'],
            'Closest Token (End)': end_closest_token,
            'End Distance': end_closest_distance,
            'End Aligned': '✓' if end_aligned else '✗',
            'Fully Aligned': '✓' if (start_aligned and end_aligned) else '✗'
        })
    
    print("\nAlignment Analysis Results:")
    print(tabulate(alignment_results, headers='keys', tablefmt='grid'))
    
    # 8. Calculate final score
    aligned_rules = sum(1 for r in alignment_results if r['Fully Aligned'] == '✓')
    alignment_score = (aligned_rules / len(rules) * 100) if rules else 0
    
    print("\n" + "=" * 40)
    print("Final Alignment Score")
    print("=" * 40)
    print(f"Rule-level Alignment Score: {alignment_score:.2f}%")
    print(f"Total Syntax Rules: {len(rules)}")
    print(f"Aligned Rules: {aligned_rules}")
    print(f"Total Tokens: {len(tokens)}")
    
    # 9. Visualize code, rules and tokens
    try:
        plt.figure(figsize=(12, 6))
        
        # Draw code character positions
        plt.plot([i for i in range(len(test_code))], [0 for _ in range(len(test_code))], 'k-', alpha=0.3)
        
        # Draw token boundaries
        for i, (start, end) in enumerate(token_boundaries):
            plt.plot([start, start], [-0.1, 0.1], 'b-', linewidth=2)
            plt.plot([end, end], [-0.1, 0.1], 'b-', linewidth=2)
            plt.text(start + (end - start) / 2, -0.2, f'T{i}', ha='center')
        
        # Draw rule boundaries
        for i, rule in enumerate(rules):
            start = rule['start_byte']
            end = rule['end_byte']
            is_aligned = any(r['Rule ID'] == rule['id'] and r['Fully Aligned'] == '✓' for r in alignment_results)
            color = 'green' if is_aligned else 'red'
            plt.plot([start, end], [0.2 + i * 0.1, 0.2 + i * 0.1], color=color, linewidth=3)
            plt.text(start + (end - start) / 2, 0.2 + i * 0.1 + 0.05, f'R{rule["id"]}:{rule["type"]}', ha='center')
        
        plt.title('Alignment between Code Rules and Tokens')
        plt.xlabel('Byte Position')
        plt.yticks([])
        plt.grid(True, alpha=0.3)
        
        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='green', linewidth=3, label='Aligned Rules'),
            Line2D([0], [0], color='red', linewidth=3, label='Unaligned Rules'),
            Line2D([0], [0], color='blue', linewidth=2, label='Token Boundaries')
        ]
        plt.legend(handles=legend_elements)
        
        plt.tight_layout()
        plt.savefig('simple_alignment_visualization.png')
        print("\n✓ Alignment visualization saved to simple_alignment_visualization.png")
    except Exception as e:
        print(f"\n❌ Visualization generation failed: {e}")
    
    return True

if __name__ == "__main__":
    main()