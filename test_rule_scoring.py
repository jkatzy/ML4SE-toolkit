#!/usr/bin/env python3
"""
测试修改后的规则计分系统
从overall count改为每个rule的counting
"""

import json
from pathlib import Path
from src.ml4setk.EBNF.rule_counter import RuleCounter
from src.ml4setk.EBNF.integrated_rule_processor import IntegratedRuleProcessor

def test_rule_scoring_changes():
    """测试规则计分方式的改变"""
    
    print("=== 测试规则计分系统修改 ===\n")
    
    # 创建测试用的Python代码
    test_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        return x + y
    
    def multiply(self, x, y):
        return x * y

# 测试代码
calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 6))
print(fibonacci(10))
'''
    
    # 保存测试代码到文件
    test_file = Path("test_code.py")
    test_file.write_text(test_code, encoding='utf-8')
    
    try:
        # 1. 使用RuleCounter进行计数
        print("1. 使用RuleCounter进行规则计数...")
        counter = RuleCounter(language="python")
        counts = counter.count_rules_in_code(test_code)
        
        if not counts:
            print("错误：没有找到任何规则")
            return
        
        # 计算统计信息
        total_occurrences = sum(counts.values())
        max_count = max(counts.values())
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        print(f"总规则数: {len(counts)}")
        print(f"总出现次数: {total_occurrences}")
        print(f"最大计数: {max_count}")
        print()
        
        # 2. 显示新旧计分方式的对比
        print("2. 新旧计分方式对比:")
        print("规则名称".ljust(25) + "计数".ljust(8) + "旧方式(总体频率%)".ljust(18) + "新方式(相对最大值%)")
        print("-" * 70)
        
        for rule, count in sorted_counts[:10]:  # 显示前10个
            old_score = (count / total_occurrences) * 100  # 旧方式：基于总体频率
            new_score = (count / max_count) * 100          # 新方式：基于最大计数
            
            print(f"{rule:<25} {count:<8} {old_score:<18.1f} {new_score:<.1f}")
        
        print()
        
        # 3. 测试IntegratedRuleProcessor
        print("3. 测试IntegratedRuleProcessor...")
        processor = IntegratedRuleProcessor(language="python", work_dir="test_results")
        
        # 处理完整工作流
        results = processor.process_complete_workflow(str(test_file), "test_scoring")
        
        print("\n4. 验证生成的文件...")
        
        # 检查生成的JSON文件
        json_path = results['json_path']
        if Path(json_path).exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            print(f"✓ JSON文件已生成: {json_path}")
            print(f"  - 包含 {len(json_data.get('rule_counts', {}))} 个规则")
            print(f"  - 最大计数: {json_data['metadata']['total_occurrences']}")
        
        # 检查生成的报告
        report_path = results['report_path']
        if Path(report_path).exists():
            print(f"✓ 报告文件已生成: {report_path}")
            
            # 读取报告内容的前几行
            with open(report_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:15]  # 读取前15行
            
            print("  报告内容预览:")
            for line in lines:
                if line.strip():
                    print(f"    {line.rstrip()}")
        
        print("\n5. 计分方式修改总结:")
        print("✓ 已将计分方式从 overall count (总体频率) 改为 individual rule counting (单个规则计数)")
        print("✓ 颜色映射现在基于每个规则相对于最大计数的比例")
        print("✓ 报告中显示相对分数而非总体频率百分比")
        print("✓ 徽标显示相对于最大值的百分比")
        
    finally:
        # 清理测试文件
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    test_rule_scoring_changes()