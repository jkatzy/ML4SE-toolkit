"""
Integrated rule processor that combines rule counting with existing EBNF visualization tools.
This script provides a complete workflow from code analysis to visualization.
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List
from rule_counter import RuleCounter
try:
    from .real_data_processor import process_real_data
except ImportError:
    # 如果real_data_processor不存在，定义一个占位函数
    def process_real_data(*args, **kwargs):
        pass
import subprocess


class IntegratedRuleProcessor:
    """
    Integrated processor that combines rule counting with EBNF visualization.
    """
    
    def __init__(self, language: str = "python", work_dir: str = "results"):
        """
        Initialize the integrated processor.
        
        Args:
            language: Programming language to process
            work_dir: Working directory for outputs
        """
        self.language = language
        self.work_dir = Path(work_dir)
        self.counter = RuleCounter(language=language)
        
        # 创建工作目录结构
        self.setup_directories()
    
    def setup_directories(self):
        """Setup necessary directories for processing."""
        directories = [
            self.work_dir,
            self.work_dir / "counts",
            self.work_dir / "csv",
            self.work_dir / "colored_svg",
            self.work_dir / "reports"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def process_code_input(self, input_path: str, input_type: str = "auto") -> Dict[str, int]:
        """
        Process code input and generate rule counts.
        
        Args:
            input_path: Path to input file
            input_type: Type of input ('file', 'jsonl', or 'auto')
            
        Returns:
            Dictionary of rule counts
        """
        input_path = Path(input_path)
        
        if input_type == "auto":
            if input_path.suffix == '.jsonl':
                input_type = "jsonl"
            else:
                input_type = "file"
        
        print(f"Processing {input_type}: {input_path}")
        
        if input_type == "jsonl":
            counts = self.counter.count_rules_in_jsonl(str(input_path))
        else:
            counts = self.counter.count_rules_in_file(str(input_path))
        
        return counts
    
    def save_counts_and_csv(self, counts: Dict[str, int], base_name: str):
        """
        Save counts in both JSON and CSV formats.
        
        Args:
            counts: Rule counts dictionary
            base_name: Base name for output files
        """
        # 保存JSON格式
        json_path = self.work_dir / "counts" / f"{base_name}_counts.json"
        self.counter.save_counts_to_json(counts, str(json_path))
        
        # 保存CSV格式（兼容现有的可视化工具）
        csv_path = self.work_dir / "csv" / f"{base_name}_counts.csv"
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write("name,count\n")
            for rule, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"{rule},{count}\n")
        
        print(f"Counts saved to: {json_path}")
        print(f"CSV saved to: {csv_path}")
        
        return json_path, csv_path
    
    def generate_visualization_report(self, counts: Dict[str, int], base_name: str):
        """
        Generate a comprehensive visualization report.
        
        Args:
            counts: Rule counts dictionary
            base_name: Base name for output files
        """
        report_path = self.work_dir / "reports" / f"{base_name}_report.md"
        
        total_rules = len(counts)
        total_occurrences = sum(counts.values())
        max_count = max(counts.values()) if counts else 0
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# EBNF Rule Analysis Report: {base_name}\n\n")
            f.write(f"**Language:** {self.language}\n")
            f.write(f"**Total Unique Rules:** {total_rules}\n")
            f.write(f"**Total Rule Occurrences:** {total_occurrences}\n")
            f.write(f"**Maximum Rule Count:** {max_count}\n")
            f.write(f"**Average Occurrences per Rule:** {total_occurrences/total_rules:.2f}\n\n")
            
            f.write("## Top 20 Most Frequent Rules\n\n")
            f.write("| Rank | Rule Name | Count | Relative Score (% of max) |\n")
            f.write("|------|-----------|-------|---------------------------|\n")
            
            for i, (rule, count) in enumerate(sorted_counts[:20], 1):
                relative_score = (count / max_count) * 100 if max_count > 0 else 0
                f.write(f"| {i} | `{rule}` | {count} | {relative_score:.1f}% |\n")
            
            f.write("\n## Rule Distribution Analysis (Based on Individual Rule Counts)\n\n")
            
            # 基于最大计数的相对分析，而非总体频率
            high_count = [r for r, c in sorted_counts if c > max_count * 0.5]  # >50% of max
            medium_count = [r for r, c in sorted_counts if max_count * 0.1 < c <= max_count * 0.5]  # 10-50% of max
            low_count = [r for r, c in sorted_counts if c <= max_count * 0.1]  # <10% of max
            
            f.write(f"- **High Count Rules (>50% of max):** {len(high_count)} rules\n")
            f.write(f"- **Medium Count Rules (10-50% of max):** {len(medium_count)} rules\n")
            f.write(f"- **Low Count Rules (<10% of max):** {len(low_count)} rules\n\n")
            
            f.write("## Complete Rule List\n\n")
            f.write("| Rule Name | Count | Relative Score (% of max) |\n")
            f.write("|-----------|-------|---------------------------|\n")
            
            for rule, count in sorted_counts:
                relative_score = (count / max_count) * 100 if max_count > 0 else 0
                f.write(f"| `{rule}` | {count} | {relative_score:.2f}% |\n")
        
        print(f"Report generated: {report_path}")
        return report_path
    
    def process_complete_workflow(self, input_path: str, base_name: str = None):
        """
        Execute the complete workflow from code analysis to visualization.
        
        Args:
            input_path: Path to input file
            base_name: Base name for output files (auto-generated if None)
        """
        input_path = Path(input_path)
        
        if base_name is None:
            base_name = input_path.stem
        
        print(f"\n=== Starting Complete Workflow for {input_path} ===")
        
        # Step 1: Count rules
        print("\n1. Counting EBNF rules...")
        counts = self.process_code_input(str(input_path))
        
        if not counts:
            print("No rules found. Workflow terminated.")
            return
        
        # Step 2: Save counts and generate CSV
        print("\n2. Saving counts and generating CSV...")
        json_path, csv_path = self.save_counts_and_csv(counts, base_name)
        
        # Step 3: Generate report
        print("\n3. Generating analysis report...")
        report_path = self.generate_visualization_report(counts, base_name)
        
        # Step 4: Print summary
        print("\n4. Summary:")
        self.counter.print_summary(counts, top_n=15)
        
        print(f"\n=== Workflow Complete ===")
        print(f"Generated files:")
        print(f"  - JSON counts: {json_path}")
        print(f"  - CSV counts: {csv_path}")
        print(f"  - Analysis report: {report_path}")
        
        return {
            'counts': counts,
            'json_path': json_path,
            'csv_path': csv_path,
            'report_path': report_path
        }


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Integrated EBNF rule processor with counting and visualization"
    )
    parser.add_argument(
        "input",
        help="Input file path (source code file or JSONL file)"
    )
    parser.add_argument(
        "--language", "-l",
        help="Programming language (default: python)",
        default="python"
    )
    parser.add_argument(
        "--work-dir", "-w",
        help="Working directory for outputs (default: results)",
        default="results"
    )
    parser.add_argument(
        "--base-name", "-n",
        help="Base name for output files (default: auto-generated from input)"
    )
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' does not exist.")
        return
    
    # 创建处理器并执行工作流
    processor = IntegratedRuleProcessor(
        language=args.language,
        work_dir=args.work_dir
    )
    
    try:
        results = processor.process_complete_workflow(args.input, args.base_name)
        print("\nWorkflow completed successfully!")
        
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()