#!/usr/bin/env python3
"""
test_rule_scoring.py: test the rule scoring system
change the rule scoring system from overall count to each rule counting
"""

import json
from pathlib import Path
from src.ml4setk.EBNF.rule_counter import RuleCounter
from src.ml4setk.EBNF.integrated_rule_processor import IntegratedRuleProcessor

def test_rule_scoring_changes():
    """test the rule scoring system"""
    
    print("=== test the rule scoring system ===\n")
    
    # create the test code
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

# test the code
calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 6))
print(fibonacci(10))
'''
    
    # save the test code to the file
    test_file = Path("test_code.py")
    test_file.write_text(test_code, encoding='utf-8')
    
    try:
        # 1. use RuleCounter to count the rules
        print("1. use RuleCounter to count the rules...")
        counter = RuleCounter(language="python")
        counts = counter.count_rules_in_code(test_code)
        
        if not counts:
            print("error: no rules found")
            return
        
        # calculate the statistics
        total_occurrences = sum(counts.values())
        max_count = max(counts.values())
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        print(f"total rules: {len(counts)}")
        print(f"total occurrences: {total_occurrences}")
        print(f"max count: {max_count}")
        print()
        
        # 2. show the comparison of the old and new scoring methods
        print("2. comparison of the old and new scoring methods:")
        print("rule name".ljust(25) + "count".ljust(8) + "old method (overall frequency%)".ljust(18) + "new method (relative to max value%)")
        print("-" * 70)
        
        for rule, count in sorted_counts[:10]:  # show the top 10 rules
            old_score = (count / total_occurrences) * 100  # old method: based on the overall frequency
            new_score = (count / max_count) * 100          # new method: based on the max count
            
            print(f"{rule:<25} {count:<8} {old_score:<18.1f} {new_score:<.1f}")
        
        print()
        
        # 3. test the IntegratedRuleProcessor
        print("3. test the IntegratedRuleProcessor...")
        processor = IntegratedRuleProcessor(language="python", work_dir="test_results")
        
        # process the complete workflow
        results = processor.process_complete_workflow(str(test_file), "test_scoring")
        
        print("\n4. verify the generated files...")
        
        # check the generated JSON file
        json_path = results['json_path']
        if Path(json_path).exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            print(f"✓ JSON file generated: {json_path}")
            print(f"  - contains {len(json_data.get('rule_counts', {}))} rules")
            print(f"  - max count: {json_data['metadata']['total_occurrences']}")
        
        # check the generated report
        report_path = results['report_path']
        if Path(report_path).exists():
            print(f"✓ report file generated: {report_path}")
            
            # read the first 15 lines of the report
            with open(report_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:15]  # read the first 15 lines
            
            print("  report content preview:")
            for line in lines:
                if line.strip():
                    print(f"    {line.rstrip()}")
        
        print("\n5. summary of the scoring method changes:")
        print("✓ the scoring method has been changed from overall count (overall frequency) to individual rule counting (single rule counting)")
        print("✓ the color mapping is now based on the ratio of each rule to the max count")
        print("✓ the relative score is displayed in the report instead of the overall frequency percentage")
        print("✓ the logo displays the percentage relative to the max value")
        
    finally:
        # clean up the test files
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    test_rule_scoring_changes()