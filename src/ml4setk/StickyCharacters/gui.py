"""
Enhanced GUI for the Integrated Sticky Character Analyzer with Visualization Support.
Provides a comprehensive interface for analyzing code tokenization with visual charts.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import threading
import os
from typing import Dict, List, Any
from pathlib import Path
import webbrowser
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from integrated_sticky_analyzer import IntegratedStickyAnalyzer
from visualization_engine import StickyVisualizationEngine


class EnhancedStickyCharacterGUI:
    """Enhanced GUI application for sticky character analysis with visualization support."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sticky Character Analyzer - Enhanced Edition")
        self.root.geometry("1400x900")
        
        # Initialize components
        self.analyzer = IntegratedStickyAnalyzer()
        self.visualizer = StickyVisualizationEngine()
        
        # GUI state
        self.current_results = None
        self.analysis_running = False
        self.current_visualizations = []
        self.current_viz_index = 0
        
        # Create notebook for tabbed interface
        self.create_tabbed_interface()
        self.refresh_input_files()
        
    def create_tabbed_interface(self):
        """Create the main tabbed interface."""
        # Create notebook widget
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_analysis_tab()
        self.create_visualization_tab()
        self.create_results_tab()
        self.create_settings_tab()
        
    def create_analysis_tab(self):
        """Create the main analysis tab."""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="📊 Analysis")
        
        # Configure grid
        analysis_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(analysis_frame, text="Sticky Character Analysis", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(analysis_frame, text="Input Files", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Available Files:").grid(row=0, column=0, sticky=tk.W)
        
        # File listbox with scrollbar
        file_list_frame = ttk.Frame(file_frame)
        file_list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        file_list_frame.columnconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(file_list_frame, selectmode=tk.EXTENDED, height=6)
        file_scrollbar = ttk.Scrollbar(file_list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        file_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # File control buttons
        file_button_frame = ttk.Frame(file_frame)
        file_button_frame.grid(row=2, column=0, columnspan=3, pady=(5, 0))
        
        ttk.Button(file_button_frame, text="Refresh", command=self.refresh_input_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_button_frame, text="Select All", command=self.select_all_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_button_frame, text="Clear Selection", command=self.clear_file_selection).pack(side=tk.LEFT)
        
        # Model selection section
        model_frame = ttk.LabelFrame(analysis_frame, text="Model Configuration", padding="10")
        model_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        model_frame.columnconfigure(1, weight=1)
        
        ttk.Label(model_frame, text="Model Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.model_var = tk.StringVar(value="bigcode/santacoder")
        self.model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, width=50)
        self.model_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Populate model dropdown
        self.model_combo['values'] = self.analyzer.supported_models
        
        ttk.Button(model_frame, text="Refresh Models", command=self.refresh_models).grid(row=0, column=2)
        
        # Analysis options
        options_frame = ttk.LabelFrame(analysis_frame, text="Analysis Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.tree_sitter_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Use Tree-sitter Analysis", 
                       variable=self.tree_sitter_var).grid(row=0, column=0, sticky=tk.W)
        
        self.auto_visualize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Auto-generate Visualizations", 
                       variable=self.auto_visualize_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Control buttons
        control_frame = ttk.Frame(analysis_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.analyze_button = ttk.Button(control_frame, text="🔍 Analyze Selected Files", 
                                        command=self.start_analysis, style="Accent.TButton")
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(control_frame, text="💾 Save Results", 
                                     command=self.save_results, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.visualize_button = ttk.Button(control_frame, text="📈 Generate Visualizations", 
                                          command=self.generate_visualizations, state=tk.DISABLED)
        self.visualize_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_button = ttk.Button(control_frame, text="📄 Export Report", 
                                       command=self.export_report, state=tk.DISABLED)
        self.export_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(analysis_frame, variable=self.progress_var, 
                                           mode='determinate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(analysis_frame, textvariable=self.status_var)
        self.status_label.grid(row=6, column=0, columnspan=3, sticky=tk.W)
        
        # Quick results summary
        summary_frame = ttk.LabelFrame(analysis_frame, text="Quick Summary", padding="10")
        summary_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        analysis_frame.rowconfigure(7, weight=1)
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD, 
                                                     width=80, height=8)
        self.summary_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.rowconfigure(0, weight=1)
    
    def create_visualization_tab(self):
        """Create the visualization tab."""
        viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(viz_frame, text="📈 Visualizations")
        
        # Configure grid
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(1, weight=1)
        
        # Control frame
        viz_control_frame = ttk.Frame(viz_frame)
        viz_control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        ttk.Label(viz_control_frame, text="Generated Visualizations:", 
                 font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Navigation buttons
        nav_frame = ttk.Frame(viz_control_frame)
        nav_frame.pack(side=tk.RIGHT)
        
        self.prev_viz_button = ttk.Button(nav_frame, text="⬅ Previous", 
                                         command=self.previous_visualization, state=tk.DISABLED)
        self.prev_viz_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.viz_counter_label = ttk.Label(nav_frame, text="No visualizations")
        self.viz_counter_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.next_viz_button = ttk.Button(nav_frame, text="Next ➡", 
                                         command=self.next_visualization, state=tk.DISABLED)
        self.next_viz_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(nav_frame, text="📁 Open Folder", 
                  command=self.open_visualizations_folder).pack(side=tk.LEFT, padx=(5, 0))
        
        # Visualization display frame
        viz_display_frame = ttk.Frame(viz_frame)
        viz_display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))
        viz_display_frame.columnconfigure(0, weight=1)
        viz_display_frame.rowconfigure(0, weight=1)
        
        # Canvas for matplotlib figures or image display
        self.viz_canvas_frame = ttk.Frame(viz_display_frame)
        self.viz_canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.viz_canvas_frame.columnconfigure(0, weight=1)
        self.viz_canvas_frame.rowconfigure(0, weight=1)
        
        # Default message
        self.no_viz_label = ttk.Label(self.viz_canvas_frame, 
                                     text="No visualizations available\\nRun analysis with 'Auto-generate Visualizations' enabled",
                                     font=('Arial', 12), foreground='gray')
        self.no_viz_label.grid(row=0, column=0)
    
    def create_results_tab(self):
        """Create the detailed results tab."""
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="📋 Detailed Results")
        
        # Configure grid
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area with better formatting
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, 
                                                     font=('Consolas', 10))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
    
    def create_settings_tab(self):
        """Create the settings tab."""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Visualization settings
        viz_settings_frame = ttk.LabelFrame(settings_frame, text="Visualization Settings", padding="10")
        viz_settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        self.auto_save_viz_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(viz_settings_frame, text="Auto-save visualizations", 
                       variable=self.auto_save_viz_var).grid(row=0, column=0, sticky=tk.W)
        
        self.high_dpi_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(viz_settings_frame, text="High DPI visualizations (300 DPI)", 
                       variable=self.high_dpi_var).grid(row=1, column=0, sticky=tk.W)
        
        # Output directories
        dirs_frame = ttk.LabelFrame(settings_frame, text="Output Directories", padding="10")
        dirs_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        dirs_frame.columnconfigure(1, weight=1)
        
        ttk.Label(dirs_frame, text="Visualizations:").grid(row=0, column=0, sticky=tk.W)
        self.viz_dir_var = tk.StringVar(value=self.visualizer.output_dir)
        ttk.Entry(dirs_frame, textvariable=self.viz_dir_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(dirs_frame, text="Browse", command=self.browse_viz_dir).grid(row=0, column=2)
        
        ttk.Label(dirs_frame, text="Results:").grid(row=1, column=0, sticky=tk.W)
        self.results_dir_var = tk.StringVar(value="results")
        ttk.Entry(dirs_frame, textvariable=self.results_dir_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(dirs_frame, text="Browse", command=self.browse_results_dir).grid(row=1, column=2)
        
        # About section
        about_frame = ttk.LabelFrame(settings_frame, text="About", padding="10")
        about_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        about_text = """Enhanced Sticky Character Analyzer v2.0
        
Features:
• Automatic language detection
• Multi-model tokenization analysis  
• Tree-sitter syntactic analysis
• Comprehensive visualizations
• Batch processing
• Export capabilities

Supported Languages: Python, JavaScript, Java, C++, C, Go, Rust, Julia, R, SQL
Supported Models: CodeLLaMA, StarCoder, WizardCoder, Qwen, SantaCoder"""
        
        about_label = ttk.Label(about_frame, text=about_text, font=('Arial', 9))
        about_label.grid(row=0, column=0, sticky=tk.W)
    
    def refresh_input_files(self):
        """Refresh the list of available input files."""
        self.file_listbox.delete(0, tk.END)
        
        try:
            files = self.analyzer.get_available_input_files()
            for file in files:
                language = self.analyzer.detect_language_from_file(file)
                display_text = f"{file} ({language or 'unknown'})"
                self.file_listbox.insert(tk.END, display_text)
            
            if not files:
                self.file_listbox.insert(tk.END, "No input files found in inputs/ directory")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh input files: {e}")
    
    def refresh_models(self):
        """Refresh the model dropdown with suggestions."""
        partial_name = self.model_var.get()
        suggestions = self.analyzer.get_model_suggestions(partial_name)
        self.model_combo['values'] = suggestions
    
    def select_all_files(self):
        """Select all files in the listbox."""
        self.file_listbox.select_set(0, tk.END)
    
    def clear_file_selection(self):
        """Clear file selection."""
        self.file_listbox.selection_clear(0, tk.END)
    
    def get_selected_files(self) -> List[str]:
        """Get list of selected filenames."""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return []
        
        files = []
        for index in selected_indices:
            display_text = self.file_listbox.get(index)
            # Extract filename from display text (before the language part)
            filename = display_text.split(' (')[0]
            files.append(filename)
        
        return files
    
    def start_analysis(self):
        """Start the analysis process in a separate thread."""
        if self.analysis_running:
            messagebox.showwarning("Analysis Running", "Analysis is already in progress.")
            return
        
        selected_files = self.get_selected_files()
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select files to analyze.")
            return
        
        model_name = self.model_var.get().strip()
        if not model_name:
            messagebox.showwarning("No Model", "Please specify a model name.")
            return
        
        # Disable controls during analysis
        self.analyze_button.config(state=tk.DISABLED)
        self.analysis_running = True
        
        # Start analysis in background thread
        thread = threading.Thread(target=self.run_analysis, 
                                 args=(selected_files, model_name))
        thread.daemon = True
        thread.start()
    
    def run_analysis(self, selected_files: List[str], model_name: str):
        """Run the analysis (called in background thread)."""
        try:
            self.update_status("Starting analysis...")
            self.update_progress(0)
            
            # Run the analysis
            use_tree_sitter = self.tree_sitter_var.get()
            results = self.analyzer.analyze_multiple_files(
                selected_files, model_name, use_tree_sitter
            )
            
            self.update_progress(50)
            
            # Generate visualizations if enabled
            visualizations = []
            if self.auto_visualize_var.get():
                self.update_status("Generating visualizations...")
                try:
                    # Update visualizer output directory
                    self.visualizer.output_dir = self.viz_dir_var.get()
                    os.makedirs(self.visualizer.output_dir, exist_ok=True)
                    
                    visualizations = self.visualizer.generate_all_visualizations(results)
                    
                    # Save metadata
                    if visualizations:
                        metadata_path = self.visualizer.save_visualization_metadata(visualizations, results)
                        visualizations.append(metadata_path)
                        
                except Exception as e:
                    print(f"Visualization generation failed: {e}")
            
            self.update_progress(100)
            
            # Update GUI in main thread
            self.root.after(0, self.analysis_completed, results, visualizations)
            
        except Exception as e:
            self.root.after(0, self.analysis_failed, str(e))
    
    def analysis_completed(self, results: Dict[str, Any], visualizations: List[str]):
        """Handle completed analysis (called in main thread)."""
        self.current_results = results
        self.current_visualizations = [v for v in visualizations if v.endswith('.png')]
        self.current_viz_index = 0
        self.analysis_running = False
        
        # Re-enable controls
        self.analyze_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.visualize_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.NORMAL)
        
        # Display results
        self.display_summary(results)
        self.display_detailed_results(results)
        
        # Update visualization display
        self.update_visualization_display()
        
        self.update_status("Analysis completed successfully")
        
        # Switch to visualization tab if visualizations were generated
        if self.current_visualizations and self.auto_visualize_var.get():
            self.notebook.select(1)  # Switch to visualization tab
        
    def analysis_failed(self, error_message: str):
        """Handle failed analysis (called in main thread)."""
        self.analysis_running = False
        self.analyze_button.config(state=tk.NORMAL)
        self.update_status(f"Analysis failed: {error_message}")
        messagebox.showerror("Analysis Failed", f"Error during analysis: {error_message}")
    
    def update_status(self, message: str):
        """Update status label."""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def update_progress(self, value: float):
        """Update progress bar."""
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def display_summary(self, results: Dict[str, Any]):
        """Display analysis summary in the summary text area."""
        self.summary_text.delete(1.0, tk.END)
        
        try:
            summary = results.get("summary", {})
            
            output = []
            output.append("📊 ANALYSIS SUMMARY")
            output.append("=" * 40)
            output.append(f"🤖 Model: {summary.get('model_name', 'Unknown')}")
            output.append(f"📁 Total Files: {summary.get('total_files', 0)}")
            output.append(f"✅ Successful: {summary.get('successful_analyses', 0)}")
            output.append(f"❌ Failed: {summary.get('failed_analyses', 0)}")
            output.append(f"🔤 Languages: {', '.join(summary.get('languages_detected', []))}")
            output.append(f"🔗 Sticky Tokens: {summary.get('total_sticky_tokens', 0)}")
            
            if self.current_visualizations:
                output.append(f"📈 Visualizations: {len(self.current_visualizations)} generated")
            
            self.summary_text.insert(tk.END, "\\n".join(output))
            
        except Exception as e:
            self.summary_text.insert(tk.END, f"Error displaying summary: {e}")
    
    def display_detailed_results(self, results: Dict[str, Any]):
        """Display detailed analysis results."""
        self.results_text.delete(1.0, tk.END)
        
        try:
            # Format and display detailed results
            summary = results.get("summary", {})
            
            output = []
            output.append("DETAILED ANALYSIS RESULTS")
            output.append("=" * 80)
            output.append(f"Model: {summary.get('model_name', 'Unknown')}")
            output.append(f"Analysis Date: {results.get('timestamp', 'Unknown')}")
            output.append(f"Total Files Processed: {summary.get('total_files', 0)}")
            output.append(f"Successful Analyses: {summary.get('successful_analyses', 0)}")
            output.append(f"Failed Analyses: {summary.get('failed_analyses', 0)}")
            output.append(f"Languages Detected: {', '.join(summary.get('languages_detected', []))}")
            output.append(f"Total Sticky Tokens Found: {summary.get('total_sticky_tokens', 0)}")
            output.append("")
            
            # Individual file results
            output.append("INDIVIDUAL FILE RESULTS")
            output.append("-" * 80)
            
            for result in results.get("individual_results", []):
                if "error" in result:
                    output.append(f"❌ {result.get('filename', 'Unknown')}")
                    output.append(f"   Error: {result['error']}")
                else:
                    filename = result.get('filename', 'Unknown')
                    language = result.get('language', 'Unknown')
                    file_size = result.get('file_size', 0)
                    basic_analysis = result.get('basic_analysis', {})
                    
                    total_tokens = len(basic_analysis.get('table', []))
                    sticky_tokens = basic_analysis.get('sticky_tokens', [])
                    sticky_count = len(sticky_tokens)
                    
                    output.append(f"✅ {filename} ({language})")
                    output.append(f"   File size: {file_size} characters")
                    output.append(f"   Total tokens: {total_tokens}")
                    output.append(f"   Sticky tokens: {sticky_count}")
                    
                    if total_tokens > 0:
                        ratio = (sticky_count / total_tokens) * 100
                        output.append(f"   Sticky ratio: {ratio:.2f}%")
                    
                    if sticky_count > 0:
                        output.append("   Sample sticky tokens:")
                        for i, token_info in enumerate(sticky_tokens[:5]):
                            token = token_info.get('token', '')
                            code_piece = token_info.get('code_piece', '')
                            output.append(f"     {i+1}. '{token}' -> '{code_piece}'")
                        
                        if sticky_count > 5:
                            output.append(f"     ... and {sticky_count - 5} more")
                    
                    # Tree-sitter analysis if available
                    if 'tree_sitter_analysis' in result:
                        tree_analysis = result['tree_sitter_analysis']
                        output.append(f"   Tree-sitter enhanced analysis available")
                    
                    output.append("")
            
            # Display the formatted output
            self.results_text.insert(tk.END, "\\n".join(output))
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Error displaying results: {e}")
    
    def update_visualization_display(self):
        """Update the visualization display tab."""
        # Clear previous content
        for widget in self.viz_canvas_frame.winfo_children():
            widget.destroy()
        
        if not self.current_visualizations:
            self.no_viz_label = ttk.Label(self.viz_canvas_frame, 
                                         text="No visualizations available\\nRun analysis with 'Auto-generate Visualizations' enabled",
                                         font=('Arial', 12), foreground='gray')
            self.no_viz_label.grid(row=0, column=0)
            
            self.prev_viz_button.config(state=tk.DISABLED)
            self.next_viz_button.config(state=tk.DISABLED)
            self.viz_counter_label.config(text="No visualizations")
            return
        
        # Display current visualization
        if 0 <= self.current_viz_index < len(self.current_visualizations):
            viz_path = self.current_visualizations[self.current_viz_index]
            self.display_image_in_canvas(viz_path)
            
            # Update navigation
            total = len(self.current_visualizations)
            self.viz_counter_label.config(text=f"{self.current_viz_index + 1} of {total}")
            
            self.prev_viz_button.config(state=tk.NORMAL if self.current_viz_index > 0 else tk.DISABLED)
            self.next_viz_button.config(state=tk.NORMAL if self.current_viz_index < total - 1 else tk.DISABLED)
    
    def display_image_in_canvas(self, image_path: str):
        """Display an image in the visualization canvas."""
        try:
            # Load and display image
            image = Image.open(image_path)
            
            # Calculate size to fit canvas while maintaining aspect ratio
            canvas_width = self.viz_canvas_frame.winfo_width()
            canvas_height = self.viz_canvas_frame.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 800, 600
            
            # Resize image to fit
            img_width, img_height = image.size
            ratio = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * ratio * 0.9)  # 90% of available space
            new_height = int(img_height * ratio * 0.9)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Display in label
            image_label = ttk.Label(self.viz_canvas_frame, image=photo)
            image_label.image = photo  # Keep a reference
            image_label.grid(row=0, column=0, padx=10, pady=10)
            
            # Add filename label
            filename = os.path.basename(image_path)
            filename_label = ttk.Label(self.viz_canvas_frame, text=filename, 
                                      font=('Arial', 10, 'bold'))
            filename_label.grid(row=1, column=0, pady=(0, 10))
            
        except Exception as e:
            error_label = ttk.Label(self.viz_canvas_frame, 
                                   text=f"Error loading image: {e}",
                                   foreground='red')
            error_label.grid(row=0, column=0)
    
    def previous_visualization(self):
        """Show previous visualization."""
        if self.current_viz_index > 0:
            self.current_viz_index -= 1
            self.update_visualization_display()
    
    def next_visualization(self):
        """Show next visualization."""
        if self.current_viz_index < len(self.current_visualizations) - 1:
            self.current_viz_index += 1
            self.update_visualization_display()
    
    def generate_visualizations(self):
        """Generate visualizations for current results."""
        if not self.current_results:
            messagebox.showwarning("No Results", "No analysis results available for visualization.")
            return
        
        try:
            self.update_status("Generating visualizations...")
            
            # Update visualizer output directory
            self.visualizer.output_dir = self.viz_dir_var.get()
            os.makedirs(self.visualizer.output_dir, exist_ok=True)
            
            # Generate visualizations
            visualizations = self.visualizer.generate_all_visualizations(self.current_results)
            
            if visualizations:
                # Save metadata
                metadata_path = self.visualizer.save_visualization_metadata(visualizations, self.current_results)
                
                self.current_visualizations = visualizations
                self.current_viz_index = 0
                self.update_visualization_display()
                
                # Switch to visualization tab
                self.notebook.select(1)
                
                messagebox.showinfo("Success", f"Generated {len(visualizations)} visualizations")
            else:
                messagebox.showwarning("No Visualizations", "No visualizations could be generated")
            
            self.update_status("Visualizations generated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate visualizations: {e}")
            self.update_status("Visualization generation failed")
    
    def open_visualizations_folder(self):
        """Open the visualizations folder in file explorer."""
        viz_dir = self.viz_dir_var.get()
        if os.path.exists(viz_dir):
            if os.name == 'nt':  # Windows
                os.startfile(viz_dir)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{viz_dir}"' if os.uname().sysname == 'Darwin' else f'xdg-open "{viz_dir}"')
        else:
            messagebox.showwarning("Directory Not Found", f"Directory does not exist: {viz_dir}")
    
    def save_results(self):
        """Save current results to a JSON file."""
        if not self.current_results:
            messagebox.showwarning("No Results", "No analysis results to save.")
            return
        
        try:
            # Ask user for filename
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save Analysis Results"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.current_results, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"Results saved to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {e}")
    
    def export_report(self):
        """Export a formatted text report."""
        if not self.current_results:
            messagebox.showwarning("No Results", "No analysis results to export.")
            return
        
        try:
            # Ask user for filename
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Export Analysis Report"
            )
            
            if filename:
                # Get the current results text
                report_content = self.results_text.get(1.0, tk.END)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                
                messagebox.showinfo("Success", f"Report exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")
    
    def browse_viz_dir(self):
        """Browse for visualization directory."""
        directory = filedialog.askdirectory(title="Select Visualizations Directory")
        if directory:
            self.viz_dir_var.set(directory)
            self.visualizer.output_dir = directory
    
    def browse_results_dir(self):
        """Browse for results directory."""
        directory = filedialog.askdirectory(title="Select Results Directory")
        if directory:
            self.results_dir_var.set(directory)


def main():
    """Main function to run the enhanced GUI application."""
    root = tk.Tk()
    
    # Set up the style
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    
    # Configure custom styles
    style.configure("Accent.TButton", font=('Arial', 10, 'bold'))
    
    # Create the application
    app = EnhancedStickyCharacterGUI(root)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()