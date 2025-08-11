#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Memory Usage Analysis Tool
For analyzing memory usage of various components in the project
"""

import os
import time
import psutil
import gc
import argparse
import matplotlib.pyplot as plt
import numpy as np
from memory_profiler import profile
from pathlib import Path

# Import analyzer
from analyzer import QuickMultiLanguageAnalyzer

class MemoryProfiler:
    """Memory profiler class for measuring and recording memory usage"""
    
    def __init__(self, output_dir="memory_profiles"):
        """Initialize memory profiler"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.process = psutil.Process(os.getpid())
        self.baseline_memory = self.get_memory_usage()
        self.snapshots = []
    
    def get_memory_usage(self):
        """Get current memory usage (MB)"""
        gc.collect()  # Force garbage collection
        return self.process.memory_info().rss / 1024 / 1024
    
    def take_snapshot(self, label=""):
        """Record current memory usage"""
        current_memory = self.get_memory_usage()
        delta = current_memory - self.baseline_memory
        timestamp = time.time()
        
        snapshot = {
            "timestamp": timestamp,
            "label": label,
            "memory_mb": current_memory,
            "delta_mb": delta
        }
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def measure_function(self, func, *args, label="", **kwargs):
        """Measure memory usage during function execution"""
        # Force garbage collection
        gc.collect()
        
        # Record initial state
        start_time = time.time()
        start_memory = self.get_memory_usage()
        start_snapshot = self.take_snapshot(f"{label} - Start")
        
        # Execute function
        result = func(*args, **kwargs)
        
        # Force garbage collection
        gc.collect()
        
        # Record final state
        end_time = time.time()
        end_memory = self.get_memory_usage()
        end_snapshot = self.take_snapshot(f"{label} - End")
        
        # Calculate differences
        execution_time = end_time - start_time
        memory_increase = end_memory - start_memory
        
        # Record results
        print(f"\n{'='*60}")
        print(f"Memory Analysis Results: {label}")
        print(f"{'='*60}")
        print(f"Execution time: {execution_time:.2f} seconds")
        print(f"Start memory: {start_memory:.2f} MB")
        print(f"End memory: {end_memory:.2f} MB")
        print(f"Memory increase: {memory_increase:.2f} MB")
        print(f"{'='*60}")
        
        return {
            "result": result,
            "execution_time": execution_time,
            "start_memory": start_memory,
            "end_memory": end_memory,
            "memory_increase": memory_increase
        }
    
    def continuous_monitor(self, func, *args, interval=0.1, label="", **kwargs):
        """Continuously monitor memory usage during function execution"""
        import threading
        
        # Monitoring flag
        monitoring = True
        memory_data = []
        
        # Monitoring thread
        def monitor_thread():
            start_time = time.time()
            while monitoring:
                current_time = time.time() - start_time
                current_memory = self.get_memory_usage()
                memory_data.append((current_time, current_memory))
                time.sleep(interval)
        
        # Start monitoring thread
        thread = threading.Thread(target=monitor_thread)
        thread.daemon = True
        thread.start()
        
        try:
            # Execute function
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Stop monitoring
            monitoring = False
            thread.join()
            
            # Analyze results
            if memory_data:
                times, memories = zip(*memory_data)
                peak_memory = max(memories)
                initial_memory = memories[0]
                final_memory = memories[-1]
                memory_increase = final_memory - initial_memory
                
                # Print results
                print(f"\n{'='*60}")
                print(f"Continuous Memory Monitoring Results: {label}")
                print(f"{'='*60}")
                print(f"Execution time: {execution_time:.2f} seconds")
                print(f"Initial memory: {initial_memory:.2f} MB")
                print(f"Peak memory: {peak_memory:.2f} MB")
                print(f"Final memory: {final_memory:.2f} MB")
                print(f"Memory increase: {memory_increase:.2f} MB")
                print(f"Sample points: {len(memory_data)}")
                print(f"{'='*60}")
                
                # Plot memory usage chart
                self.plot_memory_usage(times, memories, label)
            
            return result, memory_data
        
        except Exception as e:
            monitoring = False
            if thread.is_alive():
                thread.join()
            raise e
    
    def plot_memory_usage(self, times, memories, label=""):
        """Plot memory usage chart"""
        plt.figure(figsize=(12, 6))
        plt.plot(times, memories, 'b-')
        plt.title(f'Memory Usage Over Time - {label}')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Memory Usage (MB)')
        plt.grid(True)
        
        # Add peak marker
        peak_idx = memories.index(max(memories))
        plt.plot(times[peak_idx], memories[peak_idx], 'ro')
        plt.annotate(f'Peak: {memories[peak_idx]:.2f} MB', 
                    xy=(times[peak_idx], memories[peak_idx]),
                    xytext=(times[peak_idx]+0.5, memories[peak_idx]+2),
                    arrowprops=dict(facecolor='black', shrink=0.05))
        
        # Save chart
        filename = f"memory_usage_{label.replace(' ', '_')}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath)
        plt.close()
        
        print(f"Memory usage chart saved as: {filepath}")
        
        return filepath
    
    def generate_report(self, title="Memory Usage Analysis Report"):
        """Generate memory usage report"""
        if not self.snapshots:
            print("No memory snapshot data available")
            return
        
        # Extract data
        timestamps = [s["timestamp"] - self.snapshots[0]["timestamp"] for s in self.snapshots]
        memories = [s["memory_mb"] for s in self.snapshots]
        deltas = [s["delta_mb"] for s in self.snapshots]
        labels = [s["label"] for s in self.snapshots]
        
        # Plot memory usage chart
        plt.figure(figsize=(12, 8))
        
        # Plot total memory usage
        plt.subplot(2, 1, 1)
        plt.plot(timestamps, memories, 'b-o')
        plt.title(f'{title} - Total Memory Usage')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Memory Usage (MB)')
        plt.grid(True)
        
        # Add labels
        for i, (t, m, l) in enumerate(zip(timestamps, memories, labels)):
            if l:  # Only add annotations for points with labels
                plt.annotate(l, xy=(t, m), xytext=(t+0.1, m+0.5),
                            textcoords='data', fontsize=8,
                            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
        
        # Plot memory growth
        plt.subplot(2, 1, 2)
        plt.plot(timestamps, deltas, 'r-o')
        plt.title(f'{title} - Memory Growth Relative to Baseline')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Memory Growth (MB)')
        plt.grid(True)
        
        # Save chart
        filename = f"memory_report_{int(time.time())}.png"
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        
        print(f"Memory usage report saved as: {filepath}")
        
        # Generate text report
        report_file = self.output_dir / f"memory_report_{int(time.time())}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n")
            f.write(f"{'='*60}\n")
            f.write(f"Baseline memory: {self.baseline_memory:.2f} MB\n")
            f.write(f"Number of snapshots: {len(self.snapshots)}\n\n")
            
            f.write(f"{'Time(sec)':<12} {'Label':<30} {'Memory(MB)':<12} {'Growth(MB)':<12}\n")
            f.write(f"{'-'*70}\n")
            
            for i, snapshot in enumerate(self.snapshots):
                t = snapshot["timestamp"] - self.snapshots[0]["timestamp"]
                f.write(f"{t:<12.2f} {snapshot['label']:<30} {snapshot['memory_mb']:<12.2f} {snapshot['delta_mb']:<+12.2f}\n")
        
        print(f"Memory usage text report saved as: {report_file}")
        
        return filepath, report_file


def analyze_analyzer_memory_usage(code_dir="code_samples", language="python", model="gpt2"):
    """Analyze memory usage of the analyzer"""
    profiler = MemoryProfiler()
    
    # Initialize analyzer
    def init_analyzer():
        return QuickMultiLanguageAnalyzer(model_name=model)
    
    analyzer_result = profiler.measure_function(init_analyzer, label="Initialize Analyzer")
    analyzer = analyzer_result["result"]
    
    # Analyze single file
    def analyze_single_file():
        file_path = f"{code_dir}/{language}/example.py"
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        return analyzer.calculate_rule_level_alignment(code, language)
    
    profiler.measure_function(analyze_single_file, label="Analyze Single File")
    
    # Analyze multiple files
    def analyze_multiple_files():
        return analyzer.analyze_language_files(code_dir, language)
    
    profiler.measure_function(analyze_multiple_files, label="Analyze Multiple Files")
    
    # Analyze all languages
    def analyze_all_languages():
        available_languages = analyzer.get_available_languages()
        return analyzer.run_analysis(code_dir, available_languages)
    
    profiler.continuous_monitor(analyze_all_languages, interval=0.2, label="Analyze All Languages")
    
    # Generate report
    profiler.generate_report(title=f"Analyzer Memory Usage Analysis (Model: {model})")


def compare_models_memory_usage(code_dir="code_samples", language="python", models=None):
    """Compare memory usage of different models"""
    if models is None:
        models = ["gpt2", "bert-base-uncased", "roberta-base"]
    
    results = {}
    
    for model in models:
        print(f"\n{'='*60}")
        print(f"Testing model: {model}")
        print(f"{'='*60}")
        
        profiler = MemoryProfiler(output_dir=f"memory_profiles/{model}")
        
        # Initialize analyzer
        def init_analyzer():
            return QuickMultiLanguageAnalyzer(model_name=model)
        
        try:
            analyzer_result = profiler.measure_function(init_analyzer, label=f"Initialize Analyzer ({model})")
            analyzer = analyzer_result["result"]
            
            # Analyze single file
            def analyze_single_file():
                file_path = f"{code_dir}/{language}/example.py"
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                return analyzer.calculate_rule_level_alignment(code, language)
            
            file_result = profiler.measure_function(analyze_single_file, label=f"Analyze Single File ({model})")
            
            # Analyze multiple files
            def analyze_multiple_files():
                return analyzer.analyze_language_files(code_dir, language)
            
            multi_result = profiler.measure_function(analyze_multiple_files, label=f"Analyze Multiple Files ({model})")
            
            # Save results
            results[model] = {
                "init": analyzer_result,
                "single_file": file_result,
                "multiple_files": multi_result
            }
            
            # Generate report
            profiler.generate_report(title=f"Analyzer Memory Usage Analysis (Model: {model})")
            
        except Exception as e:
            print(f"Error testing model {model}: {e}")
    
    # Compare results
    print(f"\n{'='*60}")
    print(f"Model Memory Usage Comparison")
    print(f"{'='*60}")
    print(f"{'Model':<20} {'Init Memory(MB)':<20} {'Single File(MB)':<20} {'Multiple Files(MB)':<20}")
    print(f"{'-'*80}")
    
    for model, result in results.items():
        init_mem = result["init"]["memory_increase"]
        single_mem = result["single_file"]["memory_increase"]
        multi_mem = result["multiple_files"]["memory_increase"]
        print(f"{model:<20} {init_mem:<20.2f} {single_mem:<20.2f} {multi_mem:<20.2f}")
    
    # Plot comparison chart
    plt.figure(figsize=(12, 8))
    
    # Extract data
    model_names = list(results.keys())
    init_mems = [results[m]["init"]["memory_increase"] for m in model_names]
    single_mems = [results[m]["single_file"]["memory_increase"] for m in model_names]
    multi_mems = [results[m]["multiple_files"]["memory_increase"] for m in model_names]
    
    # Set x-axis positions
    x = np.arange(len(model_names))
    width = 0.25
    
    # Plot bar chart
    plt.bar(x - width, init_mems, width, label='Initialization')
    plt.bar(x, single_mems, width, label='Single File Analysis')
    plt.bar(x + width, multi_mems, width, label='Multiple Files Analysis')
    
    plt.xlabel('Model')
    plt.ylabel('Memory Growth (MB)')
    plt.title('Memory Usage Comparison Between Different Models')
    plt.xticks(x, model_names)
    plt.legend()
    plt.grid(True, axis='y')
    
    # Save chart
    output_dir = Path("memory_profiles")
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / "model_comparison.png"
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    
    print(f"\nModel comparison chart saved as: {filepath}")


def main():
    parser = argparse.ArgumentParser(description='Memory Usage Analysis Tool')
    parser.add_argument('--code_dir', default='code_samples', help='Code directory')
    parser.add_argument('--language', default='python', help='Analysis language')
    parser.add_argument('--model', default='gpt2', help='Tokenizer model')
    parser.add_argument('--compare_models', action='store_true', help='Compare memory usage of different models')
    parser.add_argument('--models', nargs='+', default=['gpt2', 'bert-base-uncased', 'roberta-base'], 
                        help='List of models to compare')
    
    args = parser.parse_args()
    
    if args.compare_models:
        compare_models_memory_usage(args.code_dir, args.language, args.models)
    else:
        analyze_analyzer_memory_usage(args.code_dir, args.language, args.model)


if __name__ == "__main__":
    main()