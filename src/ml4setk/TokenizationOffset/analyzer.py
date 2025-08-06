#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Multilingual Analyzer - Using existing compiled libraries
"""

import os
import json
import time
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional

from tree_sitter import Language, Parser
from transformers import AutoTokenizer
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

class QuickMultiLanguageAnalyzer:
    """Quick Multilingual Analyzer - Using compiled libraries"""
    
    def __init__(self, model_name: str = "gpt2"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Language configurations
        self.language_configs = {
            'python': {'symbol': 'python', 'extensions': ['.py']},
            'javascript': {'symbol': 'javascript', 'extensions': ['.js']},
            'typescript': {'symbol': 'typescript', 'extensions': ['.ts']},
            'java': {'symbol': 'java', 'extensions': ['.java']},
            'c': {'symbol': 'c', 'extensions': ['.c', '.h']},
            'cpp': {'symbol': 'cpp', 'extensions': ['.cpp', '.cc', '.cxx', '.hpp']},
            'csharp': {'symbol': 'c_sharp', 'extensions': ['.cs']},
            'go': {'symbol': 'go', 'extensions': ['.go']},
            'ruby': {'symbol': 'ruby', 'extensions': ['.rb']},
            'rust': {'symbol': 'rust', 'extensions': ['.rs']},
            'scala': {'symbol': 'scala', 'extensions': ['.scala']}
        }
        
        self.parsers = {}
        self.languages = {}
        self._setup_parsers()
    
    def _setup_parsers(self):
        """Set up parsers - Using existing compiled libraries"""
        build_dir = Path('./build')
        
        if not build_dir.exists():
            print("Error: build directory does not exist")
            return
        
        print("Loading compiled language libraries...")
        
        # Try to initialize each language
        for lang_name, config in self.language_configs.items():
            try:
                # Find corresponding language library file
                possible_paths = [
                    build_dir / f"languages_{lang_name}.so",
                    build_dir / f"languages.so",
                    build_dir / f"multilang_languages.so"
                ]
                
                library_path = None
                for path in possible_paths:
                    if path.exists():
                        library_path = path
                        break
                
                if not library_path:
                    print(f"✗ {lang_name} language library file does not exist")
                    continue
                
                parser = Parser()
                language = Language(str(library_path), config['symbol'])
                parser.set_language(language)
                
                self.parsers[lang_name] = parser
                self.languages[lang_name] = language
                print(f"✓ {lang_name} parser available (using {library_path.name})")
                
            except Exception as e:
                print(f"✗ {lang_name} parser unavailable: {e}")
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages"""
        return list(self.parsers.keys())
    
    def calculate_rule_level_alignment(self, code: str, language: str) -> Tuple[float, Dict]:
        """Calculate rule-level alignment score"""
        if language not in self.parsers:
            raise ValueError(f"Unsupported language: {language}")
        
        parser = self.parsers[language]
        code_bytes = code.encode('utf-8')
        
        # Parse code
        tree = parser.parse(code_bytes)
        
        # Extract rules
        def extract_rules(node, rules=None):
            if rules is None:
                rules = []
            
            if node.type and not node.type.startswith('ERROR'):
                rules.append({
                    'type': node.type,
                    'start_byte': node.start_byte,
                    'end_byte': node.end_byte,
                    'text': code_bytes[node.start_byte:node.end_byte].decode('utf-8', errors='ignore')[:50]
                })
            
            for child in node.children:
                extract_rules(child, rules)
            
            return rules
        
        rules = extract_rules(tree.root_node)
        
        # Tokenization
        try:
            tokens = self.tokenizer.encode(code)
            token_texts = [self.tokenizer.decode([token]) for token in tokens]
        except Exception as e:
            print(f"Tokenization error: {e}")
            return 0.0, {}
        
        # Calculate token boundaries
        token_boundaries = []
        current_pos = 0
        
        for token_text in token_texts:
            token_start = code.find(token_text, current_pos)
            if token_start != -1:
                token_end = token_start + len(token_text)
                token_boundaries.append((token_start, token_end))
                current_pos = token_end
            else:
                token_boundaries.append((current_pos, current_pos + 1))
                current_pos += 1
        
        # Calculate alignment
        aligned_rules = 0
        rule_details = {}
        
        for rule in rules:
            rule_start = rule['start_byte']
            rule_end = rule['end_byte']
            
            start_aligned = any(abs(rule_start - tb[0]) <= 1 for tb in token_boundaries)
            end_aligned = any(abs(rule_end - tb[1]) <= 1 for tb in token_boundaries)
            
            fully_aligned = start_aligned and end_aligned
            if fully_aligned:
                aligned_rules += 1
            
            rule_key = f"{rule['type']}_{rule['start_byte']}_{rule['end_byte']}"
            rule_details[rule_key] = {
                'type': rule['type'],
                'start_aligned': start_aligned,
                'end_aligned': end_aligned,
                'fully_aligned': fully_aligned,
                'text_preview': rule['text'][:50]
            }
        
        alignment_score = (aligned_rules / len(rules) * 100) if rules else 0
        return alignment_score, rule_details
    
    def analyze_language_files(self, code_dir: str, language: str) -> Dict:
        """Analyze all files for a specific language"""
        if language not in self.parsers:
            print(f"Skipping unsupported language: {language}")
            return {}
        
        language_dir = Path(code_dir) / language
        if not language_dir.exists():
            print(f"Language directory does not exist: {language_dir}")
            return {}
        
        # Find files
        extensions = self.language_configs[language]['extensions']
        code_files = []
        for ext in extensions:
            code_files.extend(language_dir.glob(f"*{ext}"))
        
        if not code_files:
            print(f"No {language} files found")
            return {}
        
        print(f"\nAnalyzing {language.upper()} ({len(code_files)} files)")
        print("-" * 50)
        
        # Analyze files
        file_results = []
        total_rules = 0
        total_aligned = 0
        total_code_size = 0
        start_time = time.time()
        
        # Use tqdm to create progress bar
        for file_path in tqdm(code_files, desc=f"Analyzing {language}", unit="files"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                
                if not code.strip():
                    continue
                
                code_size = len(code)
                total_code_size += code_size
                
                file_start_time = time.time()
                score, details = self.calculate_rule_level_alignment(code, language)
                file_analysis_time = time.time() - file_start_time
                
                aligned_count = sum(1 for d in details.values() if d['fully_aligned'])
                
                file_results.append({
                    'file': file_path.name,
                    'score': score,
                    'total_rules': len(details),
                    'aligned_rules': aligned_count,
                    'code_size': code_size,
                    'analysis_time': file_analysis_time,
                    'processing_speed': code_size / file_analysis_time if file_analysis_time > 0 else 0
                })
                
                total_rules += len(details)
                total_aligned += aligned_count
                
            except Exception as e:
                print(f"  {file_path.name:<20} Error: {e}")
        
        # Calculate total analysis time and speed
        total_time = time.time() - start_time
        avg_speed = total_code_size / total_time if total_time > 0 else 0
        
        if not file_results:
            return {}
        
        # Calculate statistics
        avg_score = sum(r['score'] for r in file_results) / len(file_results)
        overall_alignment = (total_aligned / total_rules * 100) if total_rules > 0 else 0
        
        result = {
            'language': language,
            'file_count': len(file_results),
            'avg_score': avg_score,
            'total_rules': total_rules,
            'total_aligned': total_aligned,
            'overall_alignment': overall_alignment,
            'total_code_size': total_code_size,
            'total_analysis_time': total_time,
            'avg_processing_speed': avg_speed,
            'files': file_results
        }
        
        print(f"\n{language.upper()} Analysis Summary:")
        print(f"  File count: {result['file_count']}")
        print(f"  Average score: {result['avg_score']:.2f}%")
        print(f"  Total rules: {result['total_rules']}")
        print(f"  Total aligned: {result['total_aligned']}")
        print(f"  Overall alignment rate: {result['overall_alignment']:.2f}%")
        print(f"  Total code size: {result['total_code_size']/1024:.2f} KB")
        print(f"  Total analysis time: {result['total_analysis_time']:.2f} seconds")
        print(f"  Average processing speed: {result['avg_processing_speed']/1024:.2f} KB/sec")
        
        return result
    
    def run_analysis(self, code_dir: str = "code_samples", 
                    target_languages: List[str] = None, 
                    output_dir: str = "results/multilang") -> Dict:
        """Run analysis"""
        available_languages = self.get_available_languages()
        
        if not available_languages:
            print("Error: No available language parsers")
            return {}
        
        if target_languages is None:
            target_languages = available_languages
        else:
            target_languages = [lang for lang in target_languages if lang in available_languages]
        
        print("=" * 80)
        print("Quick Multilingual Rule-level Alignment Score Analysis")
        print("=" * 80)
        print(f"Available languages: {' '.join(available_languages)}")
        print(f"Analyzing languages: {' '.join(target_languages)}")
        
        # Record overall analysis start time
        overall_start_time = time.time()
        
        results = {}
        for language in target_languages:
            result = self.analyze_language_files(code_dir, language)
            if result:
                results[language] = result
        
        # Calculate overall analysis time
        overall_analysis_time = time.time() - overall_start_time
        
        # Generate rankings
        rankings = []
        if results:
            print(f"\n{'='*60}")
            print("Language Rankings (by average score)")
            print(f"{'='*60}")
            
            rankings = sorted(results.items(), key=lambda x: x[1]['avg_score'], reverse=True)
            for i, (lang, result) in enumerate(rankings, 1):
                print(f"{i:2d}. {lang:<12} {result['avg_score']:6.2f}% "
                      f"(Files: {result['file_count']}, Rules: {result['total_rules']})")
            
            # Display overall analysis time
            print(f"\nTotal analysis time: {overall_analysis_time:.2f} seconds")
            
            # Calculate and display processing speed ranking for each language
            print(f"\n{'='*60}")
            print("Language Processing Speed Rankings (KB/sec)")
            print(f"{'='*60}")
            
            speed_rankings = sorted(results.items(), key=lambda x: x[1]['avg_processing_speed'], reverse=True)
            for i, (lang, result) in enumerate(speed_rankings, 1):
                print(f"{i:2d}. {lang:<12} {result['avg_processing_speed']/1024:.2f} KB/sec "
                      f"(Total size: {result['total_code_size']/1024:.2f} KB)")
        
        # Save results to files
        self._save_results(results, rankings, output_dir, overall_analysis_time)
        
        return results
    
    def _save_results(self, results: Dict, rankings: List, output_dir: str, overall_analysis_time: float):
        """Save analysis results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save detailed results
        detailed_results = {
            'model': self.model_name,
            'timestamp': str(Path().resolve()),
            'overall_analysis_time': overall_analysis_time,
            'summary': {
                'total_languages': len(results),
                'total_files': sum(r['file_count'] for r in results.values()),
                'total_rules': sum(r['total_rules'] for r in results.values()),
                'total_aligned': sum(r['total_aligned'] for r in results.values()),
                'total_code_size': sum(r['total_code_size'] for r in results.values()),
                'avg_processing_speed': sum(r['total_code_size'] for r in results.values()) / overall_analysis_time if overall_analysis_time > 0 else 0
            },
            'languages': results,
            'rankings': [
                {
                    'rank': i + 1,
                    'language': lang,
                    'avg_score': result['avg_score'],
                    'file_count': result['file_count'],
                    'total_rules': result['total_rules'],
                    'total_aligned': result['total_aligned']
                }
                for i, (lang, result) in enumerate(rankings)
            ]
        }
        
        # Save detailed report
        detailed_file = output_path / f"detailed_analysis_{self.model_name}.json"
        with open(detailed_file, 'w', encoding='utf-8') as f:
            json.dump(detailed_results, f, ensure_ascii=False, indent=2)
        
        # Save simplified ranking report
        ranking_report = {
            'model': self.model_name,
            'analysis_date': str(Path().resolve()),
            'rankings': detailed_results['rankings'],
            'summary': detailed_results['summary']
        }
        
        ranking_file = output_path / f"language_rankings_{self.model_name}.json"
        with open(ranking_file, 'w', encoding='utf-8') as f:
            json.dump(ranking_report, f, ensure_ascii=False, indent=2)
        
        # Generate cross-language report (for visualization tool)
        cross_language_report = {
            "model": self.model_name,
            "analysis_date": str(output_path),
            "language_rankings": [
                {
                    "language": lang,
                    "avg_score": result["avg_score"],
                    "total_rules": result["total_rules"],
                    "aligned_rules": result["total_aligned"],
                    "alignment_rate": (result["total_aligned"] / result["total_rules"] * 100) if result["total_rules"] > 0 else 0
                }
                for lang, result in rankings
            ],
            "analysis_summary": {
                "analyzed_languages": len(rankings),
                "total_files": sum(result["file_count"] for _, result in rankings),
                "total_rules": sum(result["total_rules"] for _, result in rankings),
                "total_aligned_rules": sum(result["total_aligned"] for _, result in rankings),
                "average_score": sum(result["avg_score"] for _, result in rankings) / len(rankings) if rankings else 0,
                "overall_alignment_rate": (sum(result["total_aligned"] for _, result in rankings) / sum(result["total_rules"] for _, result in rankings) * 100) if sum(result["total_rules"] for _, result in rankings) > 0 else 0
            }
        }
        
        cross_lang_file = output_path / f"cross_language_report_{self.model_name}.json"
        with open(cross_lang_file, 'w', encoding='utf-8') as f:
            json.dump(cross_language_report, f, ensure_ascii=False, indent=2)
        
        # Save separate detailed reports for each language
        for language, result in results.items():
            lang_dir = output_path / language
            lang_dir.mkdir(exist_ok=True)
            
            lang_file = lang_dir / f"analysis_report_{self.model_name}.json"
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 Analysis results saved to:")
        print(f"  - Detailed report: {detailed_file}")
        print(f"  - Ranking report: {ranking_file}")
        print(f"  - Language reports: {output_path}/{{language}}/analysis_report_{self.model_name}.json")

def estimate_processing_time(analyzer, language, avg_file_size, file_count):
    """Estimate time required to process a large number of files"""
    # Get current language processing speed
    print(f"\n{'='*60}")
    print(f"Large-scale Processing Time Estimation ({language})")
    print(f"{'='*60}")
    
    # Run a small test to get processing speed
    code_dir = "code_samples"
    language_dir = Path(code_dir) / language
    
    if not language_dir.exists():
        print(f"Error: {language} language directory does not exist")
        return
    
    # Find files
    extensions = analyzer.language_configs[language]['extensions']
    code_files = []
    for ext in extensions:
        code_files.extend(language_dir.glob(f"*{ext}"))
    
    if not code_files:
        print(f"Error: No {language} files found")
        return
    
    # Calculate average size of current files
    total_size = 0
    for file_path in code_files:
        total_size += file_path.stat().st_size
    
    current_avg_size = total_size / len(code_files) if code_files else 0
    
    # If no average file size provided, use current files' average size
    if avg_file_size <= 0:
        avg_file_size = current_avg_size
    
    # Run test analysis
    start_time = time.time()
    result = analyzer.analyze_language_files(code_dir, language)
    test_time = time.time() - start_time
    
    if not result:
        print(f"Error: Unable to analyze {language} files")
        return
    
    # Calculate processing speed (bytes/second)
    processing_speed = result['total_code_size'] / test_time if test_time > 0 else 0
    
    # Estimate processing time
    total_data_size = avg_file_size * file_count
    estimated_time = total_data_size / processing_speed if processing_speed > 0 else 0
    
    # Convert to more readable time format
    def format_time(seconds):
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.2f} hours"
        elif seconds < 2592000:  # 30 days
            return f"{seconds/86400:.2f} days"
        elif seconds < 31536000:  # 365 days
            return f"{seconds/2592000:.2f} months"
        else:
            return f"{seconds/31536000:.2f} years"
    
    # Display estimation results
    print(f"\nEstimation Parameters:")
    print(f"  - Current average file size: {current_avg_size/1024:.2f} KB")
    print(f"  - Used average file size: {avg_file_size/1024:.2f} KB")
    print(f"  - File count: {file_count:,}")
    print(f"  - Total data size: {total_data_size/1024/1024:.2f} MB")
    print(f"  - Processing speed: {processing_speed/1024:.2f} KB/sec")
    
    print(f"\nEstimation Results:")
    print(f"  - Estimated processing time: {format_time(estimated_time)}")
    print(f"  - Average time per file: {(estimated_time/file_count)*1000:.2f} milliseconds")
    
    # Calculate estimations for different scales
    scales = [
        (100, "100 files"),
        (1000, "1,000 files"),
        (10000, "10,000 files"),
        (100000, "100,000 files"),
        (1000000, "1,000,000 files"),
        (10000000, "10,000,000 files"),
        (100000000, "100,000,000 files")
    ]
    
    print(f"\nEstimated Times for Different Scales:")
    for scale, label in scales:
        scale_time = (avg_file_size * scale) / processing_speed if processing_speed > 0 else 0
        print(f"  - {label}: {format_time(scale_time)}")

def main():
    parser = argparse.ArgumentParser(description='Quick Multilingual Analyzer')
    parser.add_argument('--language', help='Specify language')
    parser.add_argument('--all_languages', action='store_true', help='Analyze all languages')
    parser.add_argument('--code_dir', default='code_samples', help='Code directory')
    parser.add_argument('--output_dir', default='results/multilang', help='Output directory')
    parser.add_argument('--model', default='gpt2', help='Tokenizer model')
    parser.add_argument('--no_progress_bar', action='store_true', help='Do not display progress bar')
    parser.add_argument('--estimate', action='store_true', help='Estimate large-scale processing time')
    parser.add_argument('--file_count', type=int, default=1000000, help='Number of files for estimation')
    parser.add_argument('--avg_file_size', type=float, default=0, help='Average file size for estimation (bytes)')
    
    args = parser.parse_args()
    
    # If no progress bar specified, replace tqdm with no-op version
    if args.no_progress_bar:
        import builtins
        builtins.tqdm = lambda x, **kwargs: x
    
    analyzer = QuickMultiLanguageAnalyzer(model_name=args.model)
    
    if args.estimate:
        # If estimation mode, only run estimation function
        language = args.language if args.language else 'python'
        estimate_processing_time(analyzer, language, args.avg_file_size, args.file_count)
    else:
        # Normal analysis mode
        if args.language:
            target_languages = [args.language]
        elif args.all_languages:
            target_languages = None  # Analyze all available languages
        else:
            target_languages = ['python']  # Default to analyzing only Python
        
        analyzer.run_analysis(args.code_dir, target_languages, args.output_dir)

if __name__ == "__main__":
    main()