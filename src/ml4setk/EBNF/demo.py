#!/usr/bin/env python3
"""
演示脚本：展示EBNF规则计数功能的完整工作流程
"""

import os
import json
from rule_counter import RuleCounter
from integrated_rule_processor import IntegratedRuleProcessor


def demo_basic_counting():
    """演示基本的规则计数功能"""
    print("=" * 60)
    print("演示1: 基本规则计数功能")
    print("=" * 60)
    
    counter = RuleCounter(language="python")
    
    # 示例代码：包含多种Python语法结构
    demo_code = """
class Calculator:
    '''一个简单的计算器类'''
    
    def __init__(self):
        self.history = []
        self.result = 0
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def factorial(self, n):
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)
    
    def fibonacci_sequence(self, n):
        sequence = [0, 1]
        for i in range(2, n):
            sequence.append(sequence[i-1] + sequence[i-2])
        return sequence
    
    def is_prime(self, num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    def get_primes(self, limit):
        return [n for n in range(2, limit) if self.is_prime(n)]

# 使用计算器
calc = Calculator()
print(f"5 + 3 = {calc.add(5, 3)}")
print(f"5! = {calc.factorial(5)}")
print(f"前10个斐波那契数: {calc.fibonacci_sequence(10)}")
print(f"100以内的质数: {calc.get_primes(100)}")

# 使用列表推导式和lambda函数
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [x**2 for x in numbers]
evens = list(filter(lambda x: x % 2 == 0, numbers))
doubled = list(map(lambda x: x * 2, numbers))

# 异常处理
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"错误: {e}")
finally:
    print("计算完成")

# 字典和集合操作
data = {
    'name': 'Python',
    'version': 3.9,
    'features': ['dynamic', 'interpreted', 'object-oriented']
}

unique_chars = set("hello world")
print(f"唯一字符: {unique_chars}")
"""
    
    print("分析的代码包含:")
    print("- 类定义和方法")
    print("- 递归函数")
    print("- 循环和条件语句")
    print("- 列表推导式")
    print("- Lambda函数")
    print("- 异常处理")
    print("- 字典和集合操作")
    print()
    
    # 统计规则
    counts = counter.count_rules_in_code(demo_code)
    counter.print_summary(counts, top_n=20)
    
    return counts


def demo_file_analysis():
    """演示文件分析功能"""
    print("\n" + "=" * 60)
    print("演示2: 文件分析功能")
    print("=" * 60)
    
    # 检查是否存在HumanEval数据文件
    humaneval_path = "data/HumanEval.jsonl"
    if os.path.exists(humaneval_path):
        print(f"分析HumanEval数据集: {humaneval_path}")
        
        counter = RuleCounter(language="python")
        counts = counter.count_rules_in_jsonl(humaneval_path)
        
        print(f"\nHumanEval数据集包含 {len(counts)} 种不同的语法规则")
        counter.print_summary(counts, top_n=15)
        
        # 保存结果
        counter.save_counts_to_json(counts, "demo_humaneval_counts.json")
        
        return counts
    else:
        print(f"未找到HumanEval数据文件: {humaneval_path}")
        print("创建示例JSONL文件进行演示...")
        
        # 创建示例数据
        sample_data = [
            {
                "prompt": "def quicksort(arr):",
                "canonical_solution": "    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)"
            },
            {
                "prompt": "def binary_search(arr, target):",
                "canonical_solution": "    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1"
            },
            {
                "prompt": "def merge_sort(arr):",
                "canonical_solution": "    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result"
            }
        ]
        
        # 写入临时文件
        temp_jsonl = "demo_sample.jsonl"
        with open(temp_jsonl, 'w', encoding='utf-8') as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        # 分析示例数据
        counter = RuleCounter(language="python")
        counts = counter.count_rules_in_jsonl(temp_jsonl)
        
        print("示例算法代码分析结果:")
        counter.print_summary(counts, top_n=15)
        
        # 清理临时文件
        os.remove(temp_jsonl)
        
        return counts


def demo_integrated_workflow():
    """演示集成工作流程"""
    print("\n" + "=" * 60)
    print("演示3: 集成工作流程")
    print("=" * 60)
    
    # 创建示例Python文件
    sample_code = """
import math
import random
from typing import List, Dict, Optional

class DataProcessor:
    '''数据处理器类，展示各种Python语法特性'''
    
    def __init__(self, data: List[float] = None):
        self.data = data or []
        self.processed = False
    
    @property
    def size(self) -> int:
        return len(self.data)
    
    @staticmethod
    def generate_random_data(n: int) -> List[float]:
        return [random.uniform(0, 100) for _ in range(n)]
    
    def add_data(self, *values: float) -> None:
        self.data.extend(values)
        self.processed = False
    
    def process_data(self) -> Dict[str, float]:
        if not self.data:
            raise ValueError("No data to process")
        
        result = {
            'mean': sum(self.data) / len(self.data),
            'min': min(self.data),
            'max': max(self.data),
            'std': math.sqrt(sum((x - sum(self.data)/len(self.data))**2 for x in self.data) / len(self.data))
        }
        
        self.processed = True
        return result
    
    def filter_outliers(self, threshold: float = 2.0) -> List[float]:
        if not self.processed:
            stats = self.process_data()
        else:
            stats = self.process_data()
        
        mean, std = stats['mean'], stats['std']
        return [x for x in self.data if abs(x - mean) <= threshold * std]
    
    def __str__(self) -> str:
        return f"DataProcessor(size={self.size}, processed={self.processed})"
    
    def __len__(self) -> int:
        return len(self.data)

# 使用示例
if __name__ == "__main__":
    # 创建处理器实例
    processor = DataProcessor()
    
    # 生成随机数据
    random_data = DataProcessor.generate_random_data(100)
    processor.add_data(*random_data)
    
    print(f"处理器: {processor}")
    
    # 处理数据
    try:
        stats = processor.process_data()
        print("统计信息:")
        for key, value in stats.items():
            print(f"  {key}: {value:.2f}")
        
        # 过滤异常值
        filtered_data = processor.filter_outliers()
        print(f"过滤后数据点数: {len(filtered_data)}")
        
    except ValueError as e:
        print(f"处理错误: {e}")
    
    # 使用上下文管理器
    with open("temp_data.txt", "w") as f:
        f.write("\\n".join(map(str, processor.data)))
    
    # 清理
    import os
    if os.path.exists("temp_data.txt"):
        os.remove("temp_data.txt")
"""
    
    # 写入临时文件
    temp_file = "demo_sample.py"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(sample_code)
    
    print("创建了包含以下特性的示例Python文件:")
    print("- 类型注解")
    print("- 属性装饰器")
    print("- 静态方法")
    print("- 异常处理")
    print("- 上下文管理器")
    print("- 列表推导式")
    print("- 魔术方法")
    print()
    
    # 使用集成处理器
    processor = IntegratedRuleProcessor(
        language="python", 
        work_dir="demo_results"
    )
    
    try:
        results = processor.process_complete_workflow(temp_file, "demo_sample")
        print("\n集成工作流程完成！")
        print("生成的文件:")
        print(f"- JSON计数: {results['json_path']}")
        print(f"- CSV计数: {results['csv_path']}")
        print(f"- 分析报告: {results['report_path']}")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    return results


def main():
    """运行所有演示"""
    print("EBNF规则计数器 - 完整功能演示")
    print("=" * 60)
    print("这个工具可以:")
    print("1. 解析Python代码并识别语法结构")
    print("2. 统计各种EBNF语法规则的使用频率")
    print("3. 生成详细的分析报告")
    print("4. 支持单文件和批量文件处理")
    print("5. 导出JSON和CSV格式的结果")
    print()
    
    try:
        # 运行所有演示
        demo1_results = demo_basic_counting()
        demo2_results = demo_file_analysis()
        demo3_results = demo_integrated_workflow()
        
        print("\n" + "=" * 60)
        print("演示完成总结")
        print("=" * 60)
        print("✓ 基本规则计数功能正常")
        print("✓ 文件分析功能正常")
        print("✓ 集成工作流程正常")
        print("\n所有功能都已成功验证！")
        print("您现在可以使用这些工具来分析您自己的代码了。")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()