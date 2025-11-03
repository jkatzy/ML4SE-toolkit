"""
Example usage of the rule counting functionality.
"""

from rule_counter import RuleCounter
from integrated_rule_processor import IntegratedRuleProcessor


def example_basic_usage():
    """Basic usage example."""
    print("=== Basic Usage Example ===")
    
    # 创建规则计数器
    counter = RuleCounter(language="python")
    
    # 示例代码
    sample_code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

# 测试
numbers = [3, 6, 8, 10, 1, 2, 1]
sorted_numbers = quicksort(numbers)
print(sorted_numbers)
"""
    
    # 统计规则
    counts = counter.count_rules_in_code(sample_code)
    counter.print_summary(counts)
    
    return counts


def example_file_processing():
    """File processing example."""
    print("\n=== File Processing Example ===")
    
    # 使用集成处理器
    processor = IntegratedRuleProcessor(language="python", work_dir="example_results")
    
    # 处理现有的数据文件
    data_file = "data/HumanEval.jsonl"
    
    try:
        results = processor.process_complete_workflow(data_file, "humaneval_example")
        print("Processing completed successfully!")
        return results
    except FileNotFoundError:
        print(f"Data file {data_file} not found. Creating a sample instead...")
        return create_sample_processing()


def create_sample_processing():
    """Create and process a sample file."""
    import tempfile
    import json
    
    # 创建示例JSONL数据
    sample_data = [
        {
            "prompt": "def fibonacci(n):",
            "canonical_solution": "    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
        },
        {
            "prompt": "def factorial(n):",
            "canonical_solution": "    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
        {
            "prompt": "def is_palindrome(s):",
            "canonical_solution": "    s = s.lower().replace(' ', '')\n    return s == s[::-1]"
        }
    ]
    
    # 写入临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for item in sample_data:
            f.write(json.dumps(item) + '\n')
        temp_file = f.name
    
    # 处理文件
    processor = IntegratedRuleProcessor(language="python", work_dir="example_results")
    results = processor.process_complete_workflow(temp_file, "sample_functions")
    
    # 清理临时文件
    import os
    os.unlink(temp_file)
    
    return results


def main():
    """Run all examples."""
    print("EBNF Rule Counter - Usage Examples\n")
    
    try:
        # 基本用法示例
        example_basic_usage()
        
        # 文件处理示例
        example_file_processing()
        
        print("\n=== All Examples Completed ===")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()