"""
Test script for the integrated sticky character analyzer system.
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from language_detector import LanguageDetector
    from integrated_sticky_analyzer import IntegratedStickyAnalyzer
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required files are in the current directory")
    sys.exit(1)


def test_language_detector():
    """Test the language detection functionality."""
    print("Testing Language Detector...")
    print("-" * 40)
    
    detector = LanguageDetector()
    
    # Test file extension detection
    test_files = [
        "test.py", "script.js", "Main.java", "program.cpp", 
        "data.sql", "grammar.g4", "unknown.xyz"
    ]
    
    successful_detections = 0
    for filename in test_files:
        language = detector.detect_from_filename(filename)
        print(f"  {filename:<12} -> {language or 'Not detected'}")
        if language and filename != "unknown.xyz":  # unknown.xyz should not be detected
            successful_detections += 1
        elif not language and filename == "unknown.xyz":  # unknown.xyz should not be detected
            successful_detections += 1
    
    print(f"\\nSupported languages: {detector.get_available_languages()}")
    print()
    
    # Return True if most detections worked (6 out of 7 should work)
    return successful_detections >= 6


def test_input_files():
    """Test input file detection and language recognition."""
    print("Testing Input Files...")
    print("-" * 40)
    
    analyzer = IntegratedStickyAnalyzer()
    
    # Check if inputs directory exists
    if not os.path.exists(analyzer.inputs_dir):
        print(f"  ❌ Inputs directory not found: {analyzer.inputs_dir}")
        return False
    
    # Get available files
    files = analyzer.get_available_input_files()
    if not files:
        print(f"  ❌ No input files found in {analyzer.inputs_dir}")
        return False
    
    print(f"  Found {len(files)} input files:")
    for filename in files:
        language = analyzer.detect_language_from_file(filename)
        status = "✅" if language else "❌"
        print(f"    {status} {filename:<15} ({language or 'unknown'})")
    
    print()
    return True


def test_grammar_files():
    """Test grammar file availability."""
    print("Testing Grammar Files...")
    print("-" * 40)
    
    detector = LanguageDetector()
    
    # Check if grammars directory exists
    grammars_dir = "grammars"
    if not os.path.exists(grammars_dir):
        print(f"  ❌ Grammars directory not found: {grammars_dir}")
        return False
    
    # Check grammar files for supported languages
    languages = detector.get_available_languages()
    found_grammars = 0
    
    for language in languages:
        grammar_file = detector.get_grammar_file(language, grammars_dir)
        if grammar_file:
            print(f"  ✅ {language:<12} -> {grammar_file}")
            found_grammars += 1
        else:
            print(f"  ❌ {language:<12} -> No grammar file found")
    
    print(f"\\n  Found {found_grammars}/{len(languages)} grammar files")
    print()
    return found_grammars > 0


def test_basic_analysis():
    """Test basic analysis functionality."""
    print("Testing Basic Analysis...")
    print("-" * 40)
    
    analyzer = IntegratedStickyAnalyzer()
    
    # Get first available file
    files = analyzer.get_available_input_files()
    if not files:
        print("  ❌ No input files available for testing")
        return False
    
    test_file = files[0]
    print(f"  Testing with file: {test_file}")
    
    # Test with a lightweight model (if available)
    test_models = [
        "bigcode/santacoder",  # Smaller model
        "codellama/CodeLLaMA-7b-hf",
        "bigcode/starcoder2-3b"
    ]
    
    for model_name in test_models:
        print(f"\\n  Trying model: {model_name}")
        try:
            # Try analysis with tree-sitter disabled for faster testing
            result = analyzer.analyze_file(test_file, model_name, use_tree_sitter=False)
            
            if "error" in result:
                print(f"    ❌ Analysis failed: {result['error']}")
                continue
            else:
                print(f"    ✅ Analysis successful!")
                print(f"       Language: {result.get('language', 'Unknown')}")
                basic_analysis = result.get('basic_analysis', {})
                sticky_count = len(basic_analysis.get('sticky_tokens', []))
                print(f"       Sticky tokens: {sticky_count}")
                
                if sticky_count > 0:
                    sample_tokens = basic_analysis.get('sticky_tokens', [])[:3]
                    print(f"       Sample tokens: {sample_tokens}")
                
                return True
                
        except Exception as e:
            print(f"    ❌ Exception: {str(e)[:100]}...")
            continue
    
    print("  ❌ No models worked for testing")
    return False


def test_gui_imports():
    """Test if GUI dependencies are available."""
    print("Testing GUI Dependencies...")
    print("-" * 40)
    
    try:
        import tkinter as tk
        from tkinter import ttk
        print("  ✅ tkinter available")
        
        # Try creating a test window (don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("  ✅ tkinter functional")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ tkinter not available: {e}")
        return False
    except Exception as e:
        print(f"  ❌ tkinter error: {e}")
        return False


def run_all_tests():
    """Run all tests and provide summary."""
    print("INTEGRATED STICKY CHARACTER ANALYZER TESTS")
    print("=" * 50)
    print()
    
    tests = [
        ("Language Detector", test_language_detector),
        ("Input Files", test_input_files), 
        ("Grammar Files", test_grammar_files),
        ("GUI Dependencies", test_gui_imports),
        ("Basic Analysis", test_basic_analysis),  # This one might take longer
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            if test_name == "Basic Analysis":
                print("⚠️  Note: Basic Analysis test may take time due to model downloading...")
            
            result = test_func()
            results[test_name] = result
            
        except Exception as e:
            print(f"  ❌ Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status:<10} {test_name}")
    
    print(f"\\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\\n🎉 All tests passed! The system is ready to use.")
        print("\\nTo start the GUI, run: python gui_sticky_analyzer.py")
    else:
        print("\\n⚠️  Some tests failed. Check the output above for details.")
        print("\\nYou may still be able to use parts of the system.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()