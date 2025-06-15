#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的tree-sitter代码分割功能

这个脚本验证新的代码分割方式是否能正确保持代码结构，
而不是提取出像"object", "data"这样的单个标识符。
"""

import sys
import os
from tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer


def test_code_segmentation():
    """测试代码分割功能"""
    print("="*80)
    print(" 测试修复后的代码分割功能 ")
    print("="*80)
    
    analyzer = TreeSitterStickyAnalyzer('python')
    
    test_cases = [
        {
            'code': 'x.value',
            'description': '属性访问',
            'expected_segments': ['x.value']
        },
        {
            'code': 'data["key"]',
            'description': '字典访问',
            'expected_segments': ['data["key"]']
        },
        {
            'code': 'items[0].process()',
            'description': '索引访问和方法调用',
            'expected_segments': ['items[0].process()', 'items[0]', 'process()']
        },
        {
            'code': 'if x.value > threshold: result = process(x.data)',
            'description': '条件语句',
            'expected_segments': ['x.value > threshold', 'x.value', 'result = process(x.data)', 'process(x.data)', 'x.data']
        },
        {
            'code': 'obj.method().attribute[index]',
            'description': '链式调用',
            'expected_segments': ['obj.method().attribute[index]', 'obj.method().attribute', 'obj.method()', 'method()']
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'-'*60}")
        print(f"测试案例 {i}: {test_case['description']}")
        print(f"代码: {test_case['code']}")
        print(f"{'-'*60}")
        
        try:
            segments = analyzer.extract_code_segments(test_case['code'])
            
            print(f"提取的代码段数量: {len(segments)}")
            print("提取的代码段:")
            
            for j, segment in enumerate(segments, 1):
                print(f"  {j:2d}. '{segment['text']:<25}' | {segment['node_type']:<20} | 位置: {segment['start_byte']:2d}-{segment['end_byte']:2d}")
                
                # 验证这是完整的代码片段，而不是单个标识符
                segment_text = segment['text'].strip()
                if len(segment_text) > 1:
                    if ('.' in segment_text or '[' in segment_text or '(' in segment_text or 
                        '>' in segment_text or '=' in segment_text or '"' in segment_text):
                        print(f"      ✓ 这是一个有意义的代码片段")
                    elif segment['node_type'] in ['identifier', 'string', 'integer']:
                        print(f"      → 基础元素: {segment['node_type']}")
                    else:
                        print(f"      ? 其他类型: {segment['node_type']}")
                
            # 验证是否包含预期的代码段
            segment_texts = [s['text'] for s in segments]
            print(f"\n预期包含的代码段: {test_case.get('expected_segments', '未指定')}")
            
            if 'expected_segments' in test_case:
                found_expected = []
                for expected in test_case['expected_segments']:
                    if any(expected in text for text in segment_texts):
                        found_expected.append(expected)
                print(f"找到的预期代码段: {found_expected}")
                
        except Exception as e:
            print(f"错误: {e}")


def test_tokenization_of_segments():
    """测试代码段的tokenization"""
    print("\n" + "="*80)
    print(" 测试代码段tokenization ")
    print("="*80)
    
    analyzer = TreeSitterStickyAnalyzer('python')
    model_name = 'bigcode/starcoder2-3b'
    
    test_codes = [
        'x.value',
        'data["key"]',
        'items[0].process()'
    ]
    
    print(f"使用模型: {model_name}")
    print("注意: 首次运行需要下载模型...")
    
    for i, code in enumerate(test_codes, 1):
        print(f"\n{'-'*50}")
        print(f"测试代码 {i}: {code}")
        print(f"{'-'*50}")
        
        try:
            # 提取代码段
            segments = analyzer.extract_code_segments(code)
            print(f"提取的代码段: {len(segments)}个")
            
            for j, segment in enumerate(segments, 1):
                segment_text = segment['text']
                print(f"\n段 {j}: '{segment_text}' ({segment['node_type']})")
                
                try:
                    # 对这个代码段进行tokenization
                    tokenization = analyzer.analyze_code_part_tokenization(model_name, segment_text)
                    
                    print(f"  Tokens: {tokenization['tokens']}")
                    print(f"  Token数量: {tokenization['token_count']}")
                    print(f"  Sticky tokens: {tokenization['sticky_count']}")
                    
                    if tokenization['sticky_tokens']:
                        for sticky in tokenization['sticky_tokens']:
                            print(f"    -> Sticky: '{sticky['token']}' (规则: {', '.join(sticky['detection_rules'])})")
                    else:
                        print(f"    -> 无sticky tokens")
                        
                except Exception as e:
                    print(f"  tokenization错误: {e}")
                    
        except Exception as e:
            print(f"代码段提取错误: {e}")


def test_full_analysis():
    """测试完整的新方法分析"""
    print("\n" + "="*80)
    print(" 测试完整的新方法分析 ")
    print("="*80)
    
    analyzer = TreeSitterStickyAnalyzer('python')
    model_name = 'bigcode/starcoder2-3b'
    
    test_code = 'if x.value > threshold: result = process(x.data)'
    
    print(f"测试代码: {test_code}")
    print(f"使用模型: {model_name}")
    
    try:
        result = analyzer.analyze_code_with_tree_sitter_split(model_name, test_code)
        
        print(f"\n分析结果:")
        print(f"总代码段数: {result['total_code_segments']}")
        print(f"成功分析的段数: {result['analyzed_segments']}")
        print(f"发现的sticky tokens: {result['total_sticky_tokens']}")
        
        print(f"\n代码段详情:")
        for i, segment_analysis in enumerate(result['segment_analyses'], 1):
            print(f"  段 {i}: '{segment_analysis['text']}'")
            print(f"    AST节点: {segment_analysis['node_type']}")
            print(f"    Tokens: {segment_analysis['tokens']}")
            print(f"    Sticky count: {segment_analysis['sticky_count']}")
            
            if segment_analysis['sticky_tokens']:
                for sticky in segment_analysis['sticky_tokens']:
                    print(f"      -> '{sticky['token']}' (规则: {', '.join(sticky['detection_rules'])})")
        
        print(f"\n所有sticky tokens:")
        if result['sticky_tokens']:
            for i, sticky in enumerate(result['sticky_tokens'], 1):
                print(f"  {i}. '{sticky['token']}' 来自段 '{sticky['source_code_segment']}'")
                print(f"     AST节点: {sticky['ast_node_type']}")
        else:
            print("  未发现sticky tokens")
            
    except Exception as e:
        print(f"完整分析错误: {e}")


def main():
    """主函数"""
    print("Tree-sitter代码分割修复验证")
    print("这个测试验证修复后的代码分割是否能正确保持代码结构")
    
    try:
        # 测试1: 代码分割功能
        test_code_segmentation()
        
        # 测试2: 代码段tokenization
        test_tokenization_of_segments()
        
        # 测试3: 完整分析流程
        test_full_analysis()
        
        print("\n" + "="*80)
        print(" 测试完成 ")
        print("="*80)
        print("✓ 如果看到有意义的代码段（如'x.value', 'data[\"key\"]'等）而不是单个标识符，")
        print("  说明修复成功！")
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试出现错误: {e}")


if __name__ == '__main__':
    main()