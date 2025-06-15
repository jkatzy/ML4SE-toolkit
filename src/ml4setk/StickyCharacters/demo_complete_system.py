#!/usr/bin/env python3
"""
Complete demo of the Integrated Sticky Character Analyzer System.
This script demonstrates all the key features of the system.
"""

import os
import sys
import json
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from integrated_sticky_analyzer import IntegratedStickyAnalyzer
from language_detector import LanguageDetector


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{title}")
    print("-" * len(title))


def demo_language_detection():
    """Demonstrate language detection capabilities."""
    print_header("LANGUAGE DETECTION DEMO")
    
    detector = LanguageDetector()
    
    print_section("File Extension Detection")
    test_files = [
        "web_scraper.py", "calculator.js", "HelloWorld.java", 
        "math_utils.cpp", "database.sql", "grammar.g4",
        "analysis.r", "blockchain.go", "neural_net.jl"
    ]
    
    for filename in test_files:
        language = detector.detect_from_filename(filename)
        print(f"  📄 {filename:<20} -> {language or 'Unknown'}")
    
    print_section("Available Languages & Grammars")
    languages = detector.get_available_languages()
    print(f"  Supported Languages: {len(languages)}")
    for lang in sorted(languages):
        grammar_file = detector.get_grammar_file(lang)
        status = "✅" if grammar_file else "❌"
        print(f"    {status} {lang}")


def demo_file_analysis():
    """Demonstrate file analysis capabilities."""
    print_header("FILE ANALYSIS DEMO")
    
    analyzer = IntegratedStickyAnalyzer()
    
    print_section("Available Input Files")
    files = analyzer.get_available_input_files()
    if not files:
        print("  ⚠️  No input files found. Please add files to the inputs/ directory.")
        return
    
    for filename in files:
        language = analyzer.detect_language_from_file(filename)
        print(f"  📁 {filename:<15} ({language or 'unknown'})")
    
    print_section("Single File Analysis")
    
    # Find a Python file for demonstration
    python_files = [f for f in files if f.endswith('.py')]
    demo_file = python_files[0] if python_files else files[0]
    
    print(f"  Analyzing: {demo_file}")
    print(f"  Model: bigcode/santacoder (lightweight for demo)")
    
    try:
        result = analyzer.analyze_file(demo_file, "bigcode/santacoder", use_tree_sitter=False)
        
        if "error" in result:
            print(f"  ❌ Analysis failed: {result['error']}")
        else:
            print(f"  ✅ Analysis completed successfully")
            print(f"     Language: {result['language']}")
            print(f"     File size: {result['file_size']} characters")
            
            basic_analysis = result.get('basic_analysis', {})
            total_tokens = len(basic_analysis.get('table', []))
            sticky_tokens = basic_analysis.get('sticky_tokens', [])
            sticky_count = len(sticky_tokens)
            
            print(f"     Total tokens: {total_tokens}")
            print(f"     Sticky tokens: {sticky_count}")
            
            if sticky_count > 0:
                print(f"     Sticky ratio: {sticky_count/total_tokens:.2%}")
                print(f"     Sample sticky tokens:")
                for i, token_info in enumerate(sticky_tokens[:5]):
                    token = token_info.get('token', '')
                    code_piece = token_info.get('code_piece', '')
                    print(f"       {i+1}. '{token}' -> '{code_piece}'")
                
                if sticky_count > 5:
                    print(f"       ... and {sticky_count - 5} more")
    
    except Exception as e:
        print(f"  ❌ Error during analysis: {e}")


def demo_batch_analysis():
    """Demonstrate batch analysis capabilities."""
    print_header("BATCH ANALYSIS DEMO")
    
    analyzer = IntegratedStickyAnalyzer()
    files = analyzer.get_available_input_files()
    
    if not files:
        print("  ⚠️  No input files found for batch analysis.")
        return
    
    print_section("Batch Analysis Setup")
    # Select a few files for demonstration (max 3 to keep demo quick)
    demo_files = files[:3]
    model_name = "bigcode/santacoder"
    
    print(f"  Files to analyze: {demo_files}")
    print(f"  Model: {model_name}")
    print(f"  Tree-sitter: Disabled (for faster demo)")
    
    print_section("Running Batch Analysis")
    try:
        results = analyzer.analyze_multiple_files(demo_files, model_name, use_tree_sitter=False)
        
        print_section("Batch Results Summary")
        summary = results.get('summary', {})
        print(f"  📊 Total files processed: {summary.get('total_files', 0)}")
        print(f"  ✅ Successful analyses: {summary.get('successful_analyses', 0)}")
        print(f"  ❌ Failed analyses: {summary.get('failed_analyses', 0)}")
        print(f"  🔤 Languages detected: {', '.join(summary.get('languages_detected', []))}")
        print(f"  🔗 Total sticky tokens: {summary.get('total_sticky_tokens', 0)}")
        
        print_section("Individual File Results")
        for result in results.get('individual_results', []):
            filename = result.get('filename', 'Unknown')
            if 'error' in result:
                print(f"  ❌ {filename}: {result['error']}")
            else:
                language = result.get('language', 'Unknown')
                basic_analysis = result.get('basic_analysis', {})
                sticky_count = len(basic_analysis.get('sticky_tokens', []))
                print(f"  ✅ {filename} ({language}): {sticky_count} sticky tokens")
        
        # Save results
        output_file = analyzer.save_results(results)
        if output_file:
            print(f"\\n  💾 Results saved to: {output_file}")
    
    except Exception as e:
        print(f"  ❌ Batch analysis failed: {e}")


def demo_gui_launch():
    """Demonstrate GUI capabilities."""
    print_header("GUI DEMO")
    
    print_section("GUI Features")
    features = [
        "📁 File selection with language detection",
        "🤖 Model selection and configuration", 
        "⚙️  Analysis options (Tree-sitter toggle)",
        "📊 Real-time progress tracking",
        "📋 Formatted results display",
        "💾 Save results in JSON format",
        "📄 Export formatted text reports",
        "🎨 Modern, user-friendly interface"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print_section("Launch Instructions")
    print("  To start the GUI application:")
    print("    python gui_sticky_analyzer.py")
    print()
    print("  Or run this demo script with --gui flag:")
    print("    python demo_complete_system.py --gui")


def demo_advanced_features():
    """Demonstrate advanced features."""
    print_header("ADVANCED FEATURES")
    
    print_section("Supported Models")
    analyzer = IntegratedStickyAnalyzer()
    for model in analyzer.supported_models:
        print(f"  🤖 {model}")
    
    print_section("Language Coverage")
    detector = LanguageDetector()
    languages = sorted(detector.get_available_languages())
    
    for lang in languages:
        grammar_status = "✅" if detector.get_grammar_file(lang) else "❌"
        print(f"  {grammar_status} {lang:<12} - Grammar support")
    
    print_section("Sticky Token Detection")
    print("  A token is considered 'sticky' if it contains both:")
    print("    📝 Textual elements (letters, digits, keywords)")
    print("    🔣 Symbolic elements (operators, punctuation)")
    print()
    print("  Examples of sticky tokens:")
    examples = [
        ("def(", "Python function definition with parenthesis"),
        ("import.", "Import statement with dot accessor"),
        ("if__name__", "Python main guard with underscores"),
        ("class{", "Class declaration with opening brace"),
        ("for(", "For loop with parenthesis")
    ]
    
    for token, description in examples:
        print(f"    '{token}' - {description}")


def main():
    """Main demo function."""
    print_header("INTEGRATED STICKY CHARACTER ANALYZER")
    print("🚀 Comprehensive Code Tokenization Analysis System")
    print("📅 Demo Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Check if GUI launch is requested
    if "--gui" in sys.argv:
        try:
            from gui_sticky_analyzer import main as gui_main
            print("\\n🎨 Launching GUI...")
            gui_main()
            return
        except Exception as e:
            print(f"❌ Failed to launch GUI: {e}")
            return
    
    # Run all demos
    try:
        demo_language_detection()
        demo_file_analysis()
        demo_batch_analysis()
        demo_advanced_features()
        demo_gui_launch()
        
        print_header("DEMO COMPLETED")
        print("✨ All demonstrations completed successfully!")
        print()
        print("Next steps:")
        print("  1. 🎨 Launch the GUI: python gui_sticky_analyzer.py")
        print("  2. 📁 Add your own code files to inputs/ directory")
        print("  3. 🤖 Try different models for comparison")
        print("  4. 📊 Analyze results and generate reports")
        print()
        print("For detailed documentation, see: README_StickyAnalyzer.md")
        
    except KeyboardInterrupt:
        print("\\n\\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\\n\\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()