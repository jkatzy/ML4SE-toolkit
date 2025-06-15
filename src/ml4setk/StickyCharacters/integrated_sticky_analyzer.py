"""
Integrated sticky character analyzer that combines language detection,
tree-sitter parsing, and tokenization analysis.
"""

import os
import json
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from language_detector import LanguageDetector
from tree_sitter_sticky_analyzer import TreeSitterStickyAnalyzer
from analyze_merged_tokens import analyze_code_tokenization, is_sticky_token


class IntegratedStickyAnalyzer:
    """
    Main analyzer that integrates language detection, tree-sitter parsing,
    and sticky character detection.
    """
    
    def __init__(self, inputs_dir: str = "inputs", grammars_dir: str = "grammars"):
        """
        Initialize the integrated analyzer.
        
        Args:
            inputs_dir: Directory containing input code files
            grammars_dir: Directory containing tree-sitter grammar files
        """
        self.inputs_dir = inputs_dir
        self.grammars_dir = grammars_dir
        self.language_detector = LanguageDetector()
        
        # Cache for tree-sitter analyzers
        self._tree_sitter_cache = {}
        
        # Supported models (can be extended)
        self.supported_models = [
            "codellama/CodeLLaMA-7b-hf",
            "bigcode/starcoder2-3b", 
            "WizardLM/WizardCoder-15B-V1.0",
            "Qwen/Qwen2.5-Coder-7B",
            "bigcode/santacoder"
        ]
    
    def get_available_input_files(self) -> List[str]:
        """Get list of available input files."""
        if not os.path.exists(self.inputs_dir):
            return []
        
        files = []
        for filename in os.listdir(self.inputs_dir):
            if os.path.isfile(os.path.join(self.inputs_dir, filename)):
                files.append(filename)
        
        return sorted(files)
    
    def detect_language_from_file(self, filename: str) -> Optional[str]:
        """
        Detect programming language from input file.
        
        Args:
            filename: Name of the input file
            
        Returns:
            Detected language or None
        """
        file_path = os.path.join(self.inputs_dir, filename)
        
        if not os.path.exists(file_path):
            return None
        
        # Try detection from filename first
        language = self.language_detector.detect_from_filename(filename)
        
        # If not detected, try content-based detection
        if not language:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                language = self.language_detector.detect_from_content(content, filename)
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
                return None
        
        return language
    
    def get_tree_sitter_analyzer(self, language: str) -> Optional[TreeSitterStickyAnalyzer]:
        """
        Get or create a tree-sitter analyzer for the specified language.
        
        Args:
            language: Programming language name
            
        Returns:
            TreeSitterStickyAnalyzer instance or None if not supported
        """
        if language in self._tree_sitter_cache:
            return self._tree_sitter_cache[language]
        
        # Check if grammar file exists
        grammar_file = self.language_detector.get_grammar_file(language, self.grammars_dir)
        if not grammar_file:
            print(f"Grammar file not found for language: {language}")
            return None
        
        try:
            analyzer = TreeSitterStickyAnalyzer(language)
            self._tree_sitter_cache[language] = analyzer
            return analyzer
        except Exception as e:
            print(f"Failed to create tree-sitter analyzer for {language}: {e}")
            return None
    
    def analyze_file(self, filename: str, model_name: str, 
                    use_tree_sitter: bool = True) -> Dict[str, Any]:
        """
        Analyze a single input file for sticky characters.
        
        Args:
            filename: Input file to analyze
            model_name: Model to use for tokenization
            use_tree_sitter: Whether to use tree-sitter analysis
            
        Returns:
            Analysis results dictionary
        """
        file_path = os.path.join(self.inputs_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return {"error": f"File not found: {filename}"}
        
        # Detect language
        language = self.detect_language_from_file(filename)
        if not language:
            return {"error": f"Could not detect language for file: {filename}"}
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
        except Exception as e:
            return {"error": f"Error reading file {filename}: {e}"}
        
        # Basic tokenization analysis
        try:
            basic_analysis = analyze_code_tokenization(model_name, code_content, language)
        except Exception as e:
            return {"error": f"Error in tokenization analysis: {e}"}
        
        result = {
            "filename": filename,
            "language": language,
            "model_name": model_name,
            "file_size": len(code_content),
            "basic_analysis": basic_analysis
        }
        
        # Tree-sitter enhanced analysis (if requested and available)
        if use_tree_sitter:
            tree_analyzer = self.get_tree_sitter_analyzer(language)
            if tree_analyzer:
                try:
                    tree_analysis = tree_analyzer.analyze_with_tree_sitter(
                        code_content, model_name
                    )
                    result["tree_sitter_analysis"] = tree_analysis
                except Exception as e:
                    result["tree_sitter_error"] = str(e)
            else:
                result["tree_sitter_error"] = "Tree-sitter analyzer not available"
        
        return result
    
    def analyze_multiple_files(self, filenames: List[str], model_name: str,
                              use_tree_sitter: bool = True) -> Dict[str, Any]:
        """
        Analyze multiple files and generate a comprehensive report.
        
        Args:
            filenames: List of filenames to analyze
            model_name: Model to use for tokenization
            use_tree_sitter: Whether to use tree-sitter analysis
            
        Returns:
            Comprehensive analysis results
        """
        results = []
        summary = {
            "total_files": len(filenames),
            "successful_analyses": 0,
            "failed_analyses": 0,
            "languages_detected": set(),
            "total_sticky_tokens": 0,
            "model_name": model_name
        }
        
        for filename in filenames:
            print(f"Analyzing {filename}...")
            result = self.analyze_file(filename, model_name, use_tree_sitter)
            
            if "error" in result:
                summary["failed_analyses"] += 1
                print(f"  Failed: {result['error']}")
            else:
                summary["successful_analyses"] += 1
                summary["languages_detected"].add(result["language"])
                
                # Count sticky tokens
                if "basic_analysis" in result:
                    sticky_count = len(result["basic_analysis"].get("sticky_tokens", []))
                    summary["total_sticky_tokens"] += sticky_count
                    print(f"  Success: {sticky_count} sticky tokens found")
            
            results.append(result)
        
        # Convert set to list for JSON serialization
        summary["languages_detected"] = list(summary["languages_detected"])
        
        return {
            "summary": summary,
            "individual_results": results,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
    
    def save_results(self, results: Dict[str, Any], output_file: str = None) -> str:
        """
        Save analysis results to a JSON file.
        
        Args:
            results: Analysis results to save
            output_file: Output filename (auto-generated if None)
            
        Returns:
            Path to the saved file
        """
        if output_file is None:
            timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = results.get("summary", {}).get("model_name", "unknown").replace("/", "_")
            output_file = f"analysis_results_{model_name}_{timestamp}.json"
        
        # Ensure results directory exists
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        
        output_path = os.path.join(results_dir, output_file)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Results saved to: {output_path}")
            return output_path
        except Exception as e:
            print(f"Error saving results: {e}")
            return ""
    
    def get_model_suggestions(self, partial_name: str = "") -> List[str]:
        """
        Get model name suggestions based on partial input.
        
        Args:
            partial_name: Partial model name to match
            
        Returns:
            List of matching model names
        """
        if not partial_name:
            return self.supported_models
        
        partial_lower = partial_name.lower()
        matches = []
        
        for model in self.supported_models:
            if partial_lower in model.lower():
                matches.append(model)
        
        return matches if matches else self.supported_models


# Example usage functions for testing
def example_single_file_analysis():
    """Example of analyzing a single file."""
    analyzer = IntegratedStickyAnalyzer()
    
    # Get available files
    files = analyzer.get_available_input_files()
    if not files:
        print("No input files found in inputs/ directory")
        return
    
    print("Available files:", files)
    
    # Analyze first Python file found
    python_files = [f for f in files if f.endswith('.py')]
    if python_files:
        filename = python_files[0]
        model_name = "codellama/CodeLLaMA-7b-hf"
        
        print(f"\nAnalyzing {filename} with {model_name}...")
        result = analyzer.analyze_file(filename, model_name)
        
        if "error" not in result:
            print(f"Language detected: {result['language']}")
            basic_analysis = result.get('basic_analysis', {})
            sticky_tokens = basic_analysis.get('sticky_tokens', [])
            print(f"Sticky tokens found: {len(sticky_tokens)}")
            
            if sticky_tokens:
                print("Sample sticky tokens:", sticky_tokens[:5])
        else:
            print(f"Analysis failed: {result['error']}")


def example_batch_analysis():
    """Example of batch analysis."""
    analyzer = IntegratedStickyAnalyzer()
    
    # Get all available files
    files = analyzer.get_available_input_files()
    if not files:
        print("No input files found")
        return
    
    model_name = "bigcode/starcoder2-3b"
    print(f"\nRunning batch analysis with {model_name}")
    print(f"Files to analyze: {files}")
    
    # Analyze all files
    results = analyzer.analyze_multiple_files(files, model_name)
    
    # Print summary
    summary = results["summary"]
    print(f"\nAnalysis Summary:")
    print(f"Total files: {summary['total_files']}")
    print(f"Successful: {summary['successful_analyses']}")
    print(f"Failed: {summary['failed_analyses']}")
    print(f"Languages: {summary['languages_detected']}")
    print(f"Total sticky tokens: {summary['total_sticky_tokens']}")
    
    # Save results
    output_file = analyzer.save_results(results)
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    print("Integrated Sticky Character Analyzer")
    print("=====================================")
    
    # Run examples
    example_single_file_analysis()
    print("\n" + "="*50 + "\n")
    example_batch_analysis()