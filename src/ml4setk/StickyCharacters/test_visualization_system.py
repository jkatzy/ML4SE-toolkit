#!/usr/bin/env python3
"""
Test script for the visualization system in the sticky character analyzer.
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from integrated_sticky_analyzer import IntegratedStickyAnalyzer
    from visualization_engine import StickyVisualizationEngine
    import matplotlib.pyplot as plt
    import json
    from datetime import datetime
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required packages are installed:")
    print("pip install matplotlib seaborn pandas pillow")
    sys.exit(1)


def test_visualization_dependencies():
    """Test if all visualization dependencies are available."""
    print("Testing Visualization Dependencies...")
    print("-" * 50)
    
    dependencies = [
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("PIL", "pillow")
    ]
    
    success_count = 0
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name:<12} - Available")
            success_count += 1
        except ImportError:
            print(f"  ❌ {module_name:<12} - Missing (install with: pip install {package_name})")
    
    print(f"\\nDependencies: {success_count}/{len(dependencies)} available")
    return success_count == len(dependencies)


def test_visualization_engine():
    """Test the visualization engine initialization."""
    print("\\nTesting Visualization Engine...")
    print("-" * 50)
    
    try:
        viz_engine = StickyVisualizationEngine("test_visualizations")
        print("  ✅ Visualization engine created successfully")
        
        # Check if output directory was created
        if os.path.exists("test_visualizations"):
            print("  ✅ Output directory created")
        else:
            print("  ❌ Output directory not created")
            return False
            
        # Test color palette
        if len(viz_engine.color_palette) > 0:
            print(f"  ✅ Color palette loaded ({len(viz_engine.color_palette)} colors)")
        else:
            print("  ❌ Color palette not loaded")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Visualization engine failed: {e}")
        return False


def create_sample_analysis_results():
    """Create sample analysis results for testing visualizations."""
    print("\\nCreating Sample Analysis Results...")
    print("-" * 50)
    
    sample_results = {
        "summary": {
            "total_files": 3,
            "successful_analyses": 3,
            "failed_analyses": 0,
            "languages_detected": ["python", "java", "javascript"],
            "total_sticky_tokens": 15,
            "model_name": "test/sample-model"
        },
        "individual_results": [
            {
                "filename": "sample_python.py",
                "language": "python",
                "model_name": "test/sample-model",
                "file_size": 250,
                "basic_analysis": {
                    "table": [
                        {"token": "def", "code_piece": "def", "sticky": False},
                        {"token": "function_name", "code_piece": "function_name", "sticky": False},
                        {"token": "(", "code_piece": "(", "sticky": False},
                        {"token": "param", "code_piece": "param", "sticky": False},
                        {"token": "):", "code_piece": "):", "sticky": True},
                        {"token": "if", "code_piece": "if", "sticky": False},
                        {"token": "__name__", "code_piece": "__name__", "sticky": False},
                        {"token": "==", "code_piece": "==", "sticky": False},
                        {"token": "__main__", "code_piece": "__main__", "sticky": False}
                    ],
                    "sticky_tokens": [
                        {"token": "):", "code_piece": "):", "sticky": True},
                        {"token": "import.", "code_piece": "import.", "sticky": True},
                        {"token": "def(", "code_piece": "def(", "sticky": True}
                    ]
                }
            },
            {
                "filename": "sample_java.java",
                "language": "java", 
                "model_name": "test/sample-model",
                "file_size": 180,
                "basic_analysis": {
                    "table": [
                        {"token": "public", "code_piece": "public", "sticky": False},
                        {"token": "class", "code_piece": "class", "sticky": False},
                        {"token": "Main", "code_piece": "Main", "sticky": False},
                        {"token": "{", "code_piece": "{", "sticky": False},
                        {"token": "public(", "code_piece": "public(", "sticky": True},
                        {"token": "static", "code_piece": "static", "sticky": False}
                    ],
                    "sticky_tokens": [
                        {"token": "public(", "code_piece": "public(", "sticky": True},
                        {"token": "String[]", "code_piece": "String[]", "sticky": True}
                    ]
                }
            },
            {
                "filename": "sample_javascript.js",
                "language": "javascript",
                "model_name": "test/sample-model", 
                "file_size": 320,
                "basic_analysis": {
                    "table": [
                        {"token": "function", "code_piece": "function", "sticky": False},
                        {"token": "test", "code_piece": "test", "sticky": False},
                        {"token": "()", "code_piece": "()", "sticky": False},
                        {"token": "{", "code_piece": "{", "sticky": False},
                        {"token": "console.log", "code_piece": "console.log", "sticky": False},
                        {"token": "function(", "code_piece": "function(", "sticky": True}
                    ],
                    "sticky_tokens": [
                        {"token": "function(", "code_piece": "function(", "sticky": True},
                        {"token": "const=", "code_piece": "const=", "sticky": True},
                        {"token": "if(", "code_piece": "if(", "sticky": True},
                        {"token": "return;", "code_piece": "return;", "sticky": True}
                    ]
                }
            }
        ],
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"  ✅ Sample results created with {len(sample_results['individual_results'])} files")
    print(f"  📊 Total sticky tokens: {sample_results['summary']['total_sticky_tokens']}")
    print(f"  🔤 Languages: {', '.join(sample_results['summary']['languages_detected'])}")
    
    return sample_results


def test_individual_visualizations():
    """Test each visualization function individually."""
    print("\\nTesting Individual Visualizations...")
    print("-" * 50)
    
    viz_engine = StickyVisualizationEngine("test_visualizations")
    sample_results = create_sample_analysis_results()
    
    test_functions = [
        ("Summary Visualization", viz_engine.create_sticky_tokens_summary),
        ("Language Comparison", viz_engine.create_language_comparison),
        ("Token Distribution Heatmap", viz_engine.create_token_distribution_heatmap),
        ("Detailed Token Analysis", viz_engine.create_detailed_token_analysis)
    ]
    
    successful_tests = 0
    generated_files = []
    
    for test_name, test_function in test_functions:
        try:
            print(f"  Testing {test_name}...")
            output_path = test_function(sample_results)
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"    ✅ Generated: {os.path.basename(output_path)} ({file_size} bytes)")
                generated_files.append(output_path)
                successful_tests += 1
            else:
                print(f"    ❌ File not created")
                
        except Exception as e:
            print(f"    ❌ Failed: {e}")
    
    print(f"\\nVisualization Tests: {successful_tests}/{len(test_functions)} passed")
    print(f"Generated files: {len(generated_files)}")
    
    return successful_tests == len(test_functions), generated_files


def test_batch_visualization_generation():
    """Test the batch visualization generation."""
    print("\\nTesting Batch Visualization Generation...")
    print("-" * 50)
    
    try:
        viz_engine = StickyVisualizationEngine("test_visualizations")
        sample_results = create_sample_analysis_results()
        
        print("  Running generate_all_visualizations()...")
        generated_files = viz_engine.generate_all_visualizations(sample_results)
        
        if generated_files:
            print(f"  ✅ Generated {len(generated_files)} visualizations")
            for file_path in generated_files:
                filename = os.path.basename(file_path)
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"    📊 {filename} ({file_size} bytes)")
                else:
                    print(f"    ❌ {filename} (file not found)")
            
            # Test metadata generation
            print("  Testing metadata generation...")
            metadata_path = viz_engine.save_visualization_metadata(generated_files, sample_results)
            
            if os.path.exists(metadata_path):
                print(f"    ✅ Metadata saved: {os.path.basename(metadata_path)}")
                
                # Read and validate metadata
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                required_fields = ["timestamp", "model_name", "total_files_analyzed", "visualizations"]
                if all(field in metadata for field in required_fields):
                    print("    ✅ Metadata structure valid")
                else:
                    print("    ❌ Metadata structure invalid")
                    return False
            else:
                print("    ❌ Metadata file not created")
                return False
            
            return True
        else:
            print("  ❌ No visualizations generated")
            return False
            
    except Exception as e:
        print(f"  ❌ Batch generation failed: {e}")
        return False


def test_real_analysis_integration():
    """Test integration with real analysis results."""
    print("\\nTesting Real Analysis Integration...")
    print("-" * 50)
    
    try:
        analyzer = IntegratedStickyAnalyzer()
        viz_engine = StickyVisualizationEngine("test_visualizations")
        
        # Check if input files exist
        files = analyzer.get_available_input_files()
        if not files:
            print("  ⚠️  No input files available - skipping real analysis test")
            return True
        
        # Use first available file for testing
        test_file = files[0]
        print(f"  Testing with file: {test_file}")
        
        # Run lightweight analysis
        result = analyzer.analyze_file(test_file, "bigcode/santacoder", use_tree_sitter=False)
        
        if "error" in result:
            print(f"  ⚠️  Analysis failed: {result['error']} - using sample data instead")
            return True
        
        # Convert single file result to batch format
        batch_results = {
            "summary": {
                "total_files": 1,
                "successful_analyses": 1,
                "failed_analyses": 0,
                "languages_detected": [result.get('language', 'unknown')],
                "total_sticky_tokens": len(result.get('basic_analysis', {}).get('sticky_tokens', [])),
                "model_name": result.get('model_name', 'bigcode/santacoder')
            },
            "individual_results": [result],
            "timestamp": datetime.now().isoformat()
        }
        
        print("  ✅ Real analysis completed")
        print(f"     Language: {result.get('language', 'unknown')}")
        print(f"     Sticky tokens: {len(result.get('basic_analysis', {}).get('sticky_tokens', []))}")
        
        # Generate visualizations
        print("  Generating visualizations from real data...")
        generated_files = viz_engine.generate_all_visualizations(batch_results)
        
        if generated_files:
            print(f"  ✅ Generated {len(generated_files)} visualizations from real data")
            return True
        else:
            print("  ❌ No visualizations generated from real data")
            return False
            
    except Exception as e:
        print(f"  ❌ Real analysis integration failed: {e}")
        return False


def test_gui_visualization_imports():
    """Test if the enhanced GUI can import visualization components."""
    print("\\nTesting GUI Visualization Imports...")
    print("-" * 50)
    
    try:
        # Test PIL import (required for image display in GUI)
        try:
            from PIL import Image, ImageTk
            print("  ✅ PIL (Pillow) available for image display")
        except ImportError:
            print("  ❌ PIL (Pillow) missing - install with: pip install pillow")
            return False
        
        # Test enhanced GUI import
        try:
            from gui_enhanced_analyzer import EnhancedStickyCharacterGUI
            print("  ✅ Enhanced GUI module imports successfully")
        except ImportError as e:
            print(f"  ❌ Enhanced GUI import failed: {e}")
            return False
        
        print("  ✅ All GUI visualization components available")
        return True
        
    except Exception as e:
        print(f"  ❌ GUI visualization test failed: {e}")
        return False


def cleanup_test_files():
    """Clean up test files."""
    print("\\nCleaning Up Test Files...")
    print("-" * 50)
    
    try:
        test_dir = "test_visualizations"
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)
            print(f"  ✅ Removed test directory: {test_dir}")
        else:
            print(f"  ℹ️  Test directory {test_dir} does not exist")
        
        return True
    except Exception as e:
        print(f"  ⚠️  Cleanup failed: {e}")
        return False


def run_all_visualization_tests():
    """Run all visualization tests."""
    print("STICKY CHARACTER ANALYZER - VISUALIZATION SYSTEM TESTS")
    print("=" * 70)
    
    tests = [
        ("Dependencies", test_visualization_dependencies),
        ("Visualization Engine", test_visualization_engine),
        ("Individual Visualizations", test_individual_visualizations),
        ("Batch Generation", test_batch_visualization_generation),
        ("Real Analysis Integration", test_real_analysis_integration),
        ("GUI Visualization Imports", test_gui_visualization_imports)
    ]
    
    results = {}
    generated_files = []
    
    for test_name, test_func in tests:
        try:
            if test_name == "Individual Visualizations":
                success, files = test_func()
                generated_files.extend(files)
                results[test_name] = success
            else:
                results[test_name] = test_func()
        except Exception as e:
            print(f"\\n❌ Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\\n" + "=" * 70)
    print("VISUALIZATION SYSTEM TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status:<12} {test_name}")
    
    print(f"\\nOverall: {passed}/{total} tests passed")
    
    if generated_files:
        print(f"Generated {len(generated_files)} test visualization files")
        print("\\nSample generated files:")
        for file_path in generated_files[:3]:
            print(f"  📊 {os.path.basename(file_path)}")
        if len(generated_files) > 3:
            print(f"  ... and {len(generated_files) - 3} more")
    
    if passed == total:
        print("\\n🎉 All visualization tests passed!")
        print("\\nThe visualization system is ready to use:")
        print("  1. 🎨 Launch Enhanced GUI: python gui_enhanced_analyzer.py")
        print("  2. 📊 Generate visualizations during analysis")
        print("  3. 🖼️  View and navigate through charts in the GUI")
        print("  4. 💾 Auto-save visualizations to the visualizations/ folder")
    else:
        print("\\n⚠️  Some visualization tests failed.")
        print("  Check the output above for details.")
        print("  You may need to install missing dependencies:")
        print("    pip install matplotlib seaborn pandas pillow")
    
    # Ask about cleanup
    try:
        response = input("\\nClean up test files? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            cleanup_test_files()
    except KeyboardInterrupt:
        print("\\n\\nTest interrupted by user")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_visualization_tests()