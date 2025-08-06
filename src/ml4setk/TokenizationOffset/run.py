#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tree-sitter Rule-level Alignment Score Analysis Run Script
Provides a simple command-line interface to run various analysis functions
"""

import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run command and display results"""
    print(f"\n{'='*60}")
    print(f"Executing: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed")
            return True
        else:
            print(f"❌ {description} failed")
            return False
    except Exception as e:
        print(f"❌ Execution error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Tree-sitter Rule-level Alignment Score Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python run.py --test                    # Run environment test
  python run.py --analyze                 # Run analysis for all languages
  python run.py --language python         # Analyze only specified language
  python run.py --visualize               # Generate visualization charts
  python run.py --all                     # Run all functions
  python run.py --language python --visualize  # Analyze specified language and generate charts
        """
    )
    
    parser.add_argument('--test', action='store_true', 
                       help='Run simple test script')
    parser.add_argument('--analyze', action='store_true', 
                       help='Run complete multilingual analysis')
    parser.add_argument('--visualize', action='store_true', 
                       help='Generate visualization charts')
    parser.add_argument('--all', action='store_true', 
                       help='Run all functions (test + analysis + visualization)')
    parser.add_argument('--language', type=str, 
                       help='Specify language to analyze (e.g.: python, javascript)')
    
    args = parser.parse_args()
    
    # Check if required files exist
    required_files = ['analyzer.py', 'test.py', 'visualize_multilang_results.py']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return 1
    
    print("Tree-sitter Rule-level Alignment Score Analysis Tool")
    print("=" * 60)
    
    success_count = 0
    total_count = 0
    
    # If language is specified but no operation, default to analysis
    if args.language and not any([args.test, args.analyze, args.visualize, args.all]):
        args.analyze = True
    
    # If no parameters specified, show help
    if not any([args.test, args.analyze, args.visualize, args.all]):
        parser.print_help()
        return 0
    
    # Run test
    if args.test or args.all:
        total_count += 1
        if run_command("python test.py", "Environment test"):
            success_count += 1
    
    # Run analysis
    if args.analyze or args.all:
        total_count += 1
        if args.language:
            command = f"python analyzer.py --language {args.language}"
            description = f"{args.language} language analysis"
        elif args.all:
            command = "python analyzer.py --all_languages"
            description = "All languages analysis"
        else:
            command = "python analyzer.py"
            description = "Multilingual analysis"
        
        if run_command(command, description):
            success_count += 1
    
    # Generate visualization
    if args.visualize or args.all:
        total_count += 1
        if run_command("python visualize_multilang_results.py", "Generate visualization charts"):
            success_count += 1
    
    # Show summary
    print(f"\n{'='*60}")
    print("Execution Summary")
    print(f"{'='*60}")
    print(f"Success: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All tasks executed successfully!")
        
        if args.all or args.analyze:
            print("\n📊 Analysis results location:")
            print("  - Detailed reports: results/multilang/")
            print("  - Visualization charts: results/multilang/ (if generated)")
        
        print("\n📖 For more information, please check:")
        print("  - README_multilang.md - Detailed usage instructions")
        print("  - project_status.md - Project status report")
        
        return 0
    else:
        print("⚠️  Some tasks failed, please check error messages")
        return 1

if __name__ == "__main__":
    sys.exit(main())