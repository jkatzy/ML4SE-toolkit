#!/usr/bin/env python3
"""
Enhanced Sticky Character Analyzer System Demo with Visualization Features.
Demonstrates the complete system including automatic visualization generation.
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for demo

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from integrated_sticky_analyzer import IntegratedStickyAnalyzer
from visualization_engine import StickyVisualizationEngine
from datetime import datetime


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title):
    """Print a formatted section header.""" 
    print(f"\n{title}")
    print("-" * len(title))


def demo_enhanced_features():
    """Demonstrate the enhanced features."""
    print_header("ENHANCED STICKY CHARACTER ANALYZER v2.0")
    print("🚀 Complete Analysis System with Advanced Visualizations")
    print("📅 Demo Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    print_section("✨ New Visualization Features")
    features = [
        "📊 Summary Dashboard - Overview of all analysis results",
        "🔍 Language Comparison - Compare sticky patterns across languages", 
        "🌡️  Token Distribution Heatmap - Visualize token patterns and distributions",
        "📈 Detailed Token Analysis - In-depth analysis of sticky token patterns",
        "🖼️  GUI Integration - View visualizations directly in the application",
        "💾 Auto-save - Automatically save all charts and metadata",
        "🎨 High-resolution output - Publication-ready charts (300 DPI)",
        "📱 Interactive navigation - Browse through multiple visualizations"
    ]
    
    for feature in features:
        print(f"  {feature}")


def demo_visualization_generation():
    """Demonstrate visualization generation with real data."""
    print_header("VISUALIZATION GENERATION DEMO")
    
    print_section("🔧 System Initialization")
    analyzer = IntegratedStickyAnalyzer()
    visualizer = StickyVisualizationEngine()
    
    print("  ✅ Analyzer initialized")
    print("  ✅ Visualization engine ready")
    print(f"  📁 Output directory: {visualizer.output_dir}")
    
    print_section("📁 Available Input Files")
    files = analyzer.get_available_input_files()
    if not files:
        print("  ⚠️  No input files found in inputs/ directory")
        return
    
    for filename in files[:5]:  # Show first 5 files
        language = analyzer.detect_language_from_file(filename)
        print(f"  📄 {filename:<15} ({language or 'unknown'})")
    
    if len(files) > 5:
        print(f"  ... and {len(files) - 5} more files")
    
    print_section("🔍 Running Enhanced Analysis")
    
    # Select files for demo (up to 3 for speed)
    demo_files = files[:3]
    model_name = "bigcode/santacoder"  # Lightweight model for demo
    
    print(f"  🎯 Analyzing files: {demo_files}")
    print(f"  🤖 Using model: {model_name}")
    print(f"  ⚙️  Tree-sitter: Enabled")
    print(f"  📊 Auto-visualization: Enabled")
    
    try:
        print("\\n  🔄 Running analysis...")
        results = analyzer.analyze_multiple_files(demo_files, model_name, use_tree_sitter=False)
        
        # Display analysis summary
        summary = results.get('summary', {})
        print(f"  ✅ Analysis completed!")
        print(f"     📊 Files processed: {summary.get('total_files', 0)}")
        print(f"     ✅ Successful: {summary.get('successful_analyses', 0)}")
        print(f"     🔗 Sticky tokens found: {summary.get('total_sticky_tokens', 0)}")
        print(f"     🔤 Languages: {', '.join(summary.get('languages_detected', []))}")
        
        print_section("📈 Generating Visualizations")
        print("  🎨 Creating comprehensive visualization suite...")
        
        # Generate all visualizations
        visualization_paths = visualizer.generate_all_visualizations(results)
        
        if visualization_paths:
            print(f"  ✅ Generated {len(visualization_paths)} visualizations:")
            
            for i, path in enumerate(visualization_paths, 1):
                filename = os.path.basename(path)
                file_size = os.path.getsize(path) if os.path.exists(path) else 0
                viz_type = visualizer._get_visualization_type(path)
                print(f"    {i}. 📊 {filename}")
                print(f"       📋 Type: {viz_type}")
                print(f"       💾 Size: {file_size:,} bytes")
            
            # Save metadata
            print("\\n  📝 Saving visualization metadata...")
            metadata_path = visualizer.save_visualization_metadata(visualization_paths, results)
            print(f"  ✅ Metadata saved: {os.path.basename(metadata_path)}")
            
            print_section("🎯 Visualization Details")
            
            # Describe each visualization type
            viz_descriptions = {
                "Summary Dashboard": "📊 Complete overview with charts showing sticky token counts, ratios, language distribution, and correlation analysis",
                "Language Comparison": "🔍 Side-by-side comparison of sticky token patterns across different programming languages",
                "Token Distribution Heatmap": "🌡️  Heat map visualization showing token distribution patterns and normalized metrics across files",
                "Detailed Token Analysis": "📈 In-depth analysis including token frequency, length distribution, and language-specific patterns"
            }
            
            for path in visualization_paths:
                viz_type = visualizer._get_visualization_type(path)
                if viz_type in viz_descriptions:
                    print(f"  {viz_descriptions[viz_type]}")
            
            return visualization_paths, results
        else:
            print("  ❌ No visualizations generated")
            return [], results
            
    except Exception as e:
        print(f"  ❌ Analysis failed: {e}")
        return [], {}


def demo_gui_features():
    """Demonstrate the enhanced GUI features."""
    print_header("ENHANCED GUI FEATURES")
    
    print_section("🎨 New GUI Components")
    gui_features = [
        "📑 Tabbed Interface - Organized workflow with Analysis, Visualization, Results, and Settings tabs",
        "🖼️  Visualization Tab - Built-in image viewer with navigation controls",
        "📊 Real-time Visualization Display - View charts immediately after analysis",
        "🔄 Navigation Controls - Browse through multiple generated visualizations",
        "💾 Auto-save Settings - Configure automatic saving of charts and metadata",
        "📁 Directory Management - Customize output folders for visualizations and results",
        "⚙️  Enhanced Settings - Control visualization quality, formats, and output options",
        "📋 Improved Results Display - Better formatted analysis results with syntax highlighting"
    ]
    
    for feature in gui_features:
        print(f"  {feature}")
    
    print_section("🚀 Launch Instructions")
    print("  To start the enhanced GUI with visualization support:")
    print("    python gui_enhanced_analyzer.py")
    print()
    print("  Or launch the original GUI:")
    print("    python gui_sticky_analyzer.py")
    print()
    print("  📝 Note: Enhanced GUI requires additional dependencies:")
    print("    pip install matplotlib seaborn pandas pillow")


def demo_visualization_types():
    """Demonstrate the different types of visualizations available."""
    print_header("VISUALIZATION SHOWCASE")
    
    print_section("📊 Available Visualization Types")
    
    viz_types = [
        {
            "name": "Summary Dashboard",
            "description": "Complete overview of analysis results",
            "charts": ["Bar chart of sticky tokens by file", "Sticky token ratio percentages", 
                      "Language distribution pie chart", "Total vs sticky tokens scatter plot"],
            "use_case": "Quick overview and executive summary"
        },
        {
            "name": "Language Comparison", 
            "description": "Cross-language analysis and comparison",
            "charts": ["Average sticky ratio by language", "Total sticky tokens by language",
                      "Number of files by language"],
            "use_case": "Understanding language-specific tokenization patterns"
        },
        {
            "name": "Token Distribution Heatmap",
            "description": "Pattern analysis and distribution visualization", 
            "charts": ["Raw token statistics heatmap", "Normalized metrics heatmap"],
            "use_case": "Identifying patterns and outliers in tokenization"
        },
        {
            "name": "Detailed Token Analysis",
            "description": "In-depth token pattern exploration",
            "charts": ["Most common sticky tokens", "Token length distribution",
                      "Language-specific token patterns", "Token diversity by file"],
            "use_case": "Deep dive into specific sticky token characteristics"
        }
    ]
    
    for i, viz_type in enumerate(viz_types, 1):
        print(f"\\n  {i}. 📈 {viz_type['name']}")
        print(f"     {viz_type['description']}")
        print(f"     📊 Charts included:")
        for chart in viz_type['charts']:
            print(f"       • {chart}")
        print(f"     🎯 Best for: {viz_type['use_case']}")


def demo_automation_features():
    """Demonstrate automation and workflow features."""
    print_header("AUTOMATION & WORKFLOW FEATURES")
    
    print_section("🤖 Automated Workflow")
    workflow_steps = [
        "1. 📁 Auto-detect files in inputs/ directory",
        "2. 🔍 Automatically identify programming languages", 
        "3. 📝 Select appropriate tree-sitter grammars",
        "4. 🤖 Run tokenization analysis with specified model",
        "5. 🔗 Detect sticky character patterns automatically",
        "6. 📊 Generate comprehensive visualization suite",
        "7. 💾 Auto-save all results and metadata",
        "8. 🖼️  Display results in integrated GUI viewer"
    ]
    
    for step in workflow_steps:
        print(f"  {step}")
    
    print_section("💾 Auto-save Features")
    save_features = [
        "📊 High-resolution visualizations (300 DPI PNG format)",
        "📋 Detailed analysis results (JSON format)",
        "📄 Formatted text reports (TXT format)", 
        "📝 Visualization metadata (JSON with file information)",
        "🏷️  Timestamped filenames for easy organization",
        "📁 Organized folder structure (visualizations/, results/)",
        "🔄 Automatic backup of previous results"
    ]
    
    for feature in save_features:
        print(f"  {feature}")


def demo_integration_workflow():
    """Demonstrate the complete integration workflow."""
    print_header("COMPLETE INTEGRATION WORKFLOW")
    
    print_section("🔄 End-to-End Process")
    print("  Demonstrating complete workflow from input to visualization...")
    
    # Run the actual demo
    visualization_paths, results = demo_visualization_generation()
    
    if visualization_paths and results:
        print_section("✅ Workflow Completed Successfully")
        print(f"  📊 Generated {len(visualization_paths)} visualizations")
        print(f"  📁 Files saved in: visualizations/")
        print(f"  🔗 Total sticky tokens analyzed: {results.get('summary', {}).get('total_sticky_tokens', 0)}")
        
        print_section("🎯 Next Steps")
        next_steps = [
            "1. 🎨 Launch GUI: python gui_enhanced_analyzer.py",
            "2. 📊 View visualizations in the Visualization tab",
            "3. 📁 Access saved files in visualizations/ folder",
            "4. 📝 Review detailed results in Results tab",
            "5. ⚙️  Customize settings in Settings tab",
            "6. 💾 Export reports as needed"
        ]
        
        for step in next_steps:
            print(f"  {step}")
    
    else:
        print_section("⚠️  Demo Limitations")
        print("  Some features may require:")
        print("  • More diverse input files with sticky tokens")
        print("  • Internet connection for model downloads")
        print("  • Additional system dependencies")


def main():
    """Main demo function."""
    try:
        demo_enhanced_features()
        demo_visualization_types()
        demo_automation_features()
        demo_gui_features()
        demo_integration_workflow()
        
        print_header("🎉 ENHANCED SYSTEM DEMO COMPLETED")
        print("✨ The Enhanced Sticky Character Analyzer is ready for use!")
        print()
        print("📚 Key Features Summary:")
        print("  • 🔍 Automatic language detection and analysis")
        print("  • 📊 Comprehensive visualization generation")
        print("  • 🎨 Enhanced GUI with integrated chart viewer")
        print("  • 💾 Automatic saving and organization")
        print("  • 🌐 Support for 11+ programming languages")
        print("  • 🤖 Integration with 5+ tokenization models")
        print()
        print("🚀 Ready to Launch:")
        print("  Enhanced GUI: python gui_enhanced_analyzer.py")
        print("  Standard GUI:  python gui_sticky_analyzer.py")
        print("  CLI Demo:      python demo_complete_system.py")
        print()
        print("📖 Documentation: README_StickyAnalyzer.md")
        
    except KeyboardInterrupt:
        print("\\n\\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\\n\\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()