"""
Test script for the rule_counter module.
"""

import os
import tempfile
from rule_counter import RuleCounter


def test_basic_functionality():
    """Test basic rule counting functionality."""
    print("=== Testing Basic Functionality ===")
    
    # 创建规则计数器
    counter = RuleCounter(language="python")
    
    # 测试代码示例
    test_code = """
def hello_world(name):
    '''A simple greeting function'''
    if name:
        message = f"Hello, {name}!"
        print(message)
        return message
    else:
        print("Hello, World!")
        return "Hello, World!"

# 测试函数调用
result = hello_world("Alice")
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers if x % 2 == 0]
"""
    
    # 统计规则
    counts = counter.count_rules_in_code(test_code)
    
    # 打印结果
    counter.print_summary(counts, top_n=15)
    
    return counts


def test_file_processing():
    """Test file processing functionality."""
    print("\n=== Testing File Processing ===")
    
    # 创建临时文件
    test_code = """
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 7))
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        counter = RuleCounter(language="python")
        counts = counter.count_rules_in_file(temp_file)
        counter.print_summary(counts, top_n=10)
        
        # 保存到JSON文件
        json_output = temp_file.replace('.py', '_counts.json')
        counter.save_counts_to_json(counts, json_output)
        
        print(f"Results saved to: {json_output}")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_jsonl_processing():
    """Test JSONL file processing functionality."""
    print("\n=== Testing JSONL Processing ===")
    
    # 创建测试JSONL文件
    jsonl_content = '''{"prompt": "def fibonacci(n):", "canonical_solution": "    if n <= 1:\\n        return n\\n    return fibonacci(n-1) + fibonacci(n-2)"}
{"prompt": "def factorial(n):", "canonical_solution": "    if n == 0:\\n        return 1\\n    return n * factorial(n-1)"}
{"prompt": "def is_prime(n):", "canonical_solution": "    if n < 2:\\n        return False\\n    for i in range(2, int(n**0.5) + 1):\\n        if n % i == 0:\\n            return False\\n    return True"}'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write(jsonl_content)
        temp_jsonl = f.name
    
    try:
        counter = RuleCounter(language="python")
        counts = counter.count_rules_in_jsonl(temp_jsonl)
        counter.print_summary(counts, top_n=15)
        
        # 保存结果
        json_output = temp_jsonl.replace('.jsonl', '_rule_counts.json')
        counter.save_counts_to_json(counts, json_output)
        
        print(f"JSONL processing results saved to: {json_output}")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_jsonl):
            os.unlink(temp_jsonl)


def main():
    """Run all tests."""
    print("Starting Rule Counter Tests...\n")
    
    try:
        test_basic_functionality()
        test_file_processing()
        test_jsonl_processing()
        
        print("\n=== All Tests Completed Successfully! ===")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()