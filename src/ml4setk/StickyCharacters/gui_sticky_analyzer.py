"""
GUI for the Integrated Sticky Character Analyzer.
Provides a user-friendly interface for analyzing code tokenization.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import threading
import os
from typing import Dict, List, Any
from pathlib import Path

from integrated_sticky_analyzer import IntegratedStickyAnalyzer


class StickyCharacterGUI:
    """GUI application for sticky character analysis."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sticky Character Analyzer")
        self.root.geometry("1000x700")
        
        # Initialize the analyzer
        self.analyzer = IntegratedStickyAnalyzer()
        
        # GUI state
        self.current_results = None
        self.analysis_running = False
        
        # Create GUI elements
        self.create_widgets()
        self.refresh_input_files()
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Sticky Character Analyzer", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Input Files", padding="10")
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
        model_frame = ttk.LabelFrame(main_frame, text="Model Configuration", padding="10")
        model_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        model_frame.columnconfigure(1, weight=1)
        
        ttk.Label(model_frame, text="Model Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.model_var = tk.StringVar(value="codellama/CodeLLaMA-7b-hf")
        self.model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, width=50)
        self.model_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Populate model dropdown
        self.model_combo['values'] = self.analyzer.supported_models
        
        ttk.Button(model_frame, text="Refresh Models", command=self.refresh_models).grid(row=0, column=2)
        
        # Analysis options
        options_frame = ttk.LabelFrame(main_frame, text="Analysis Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.tree_sitter_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Use Tree-sitter Analysis", 
                       variable=self.tree_sitter_var).grid(row=0, column=0, sticky=tk.W)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.analyze_button = ttk.Button(control_frame, text="Analyze Selected Files", 
                                        command=self.start_analysis, style="Accent.TButton")
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(control_frame, text="Save Results", 
                                     command=self.save_results, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_button = ttk.Button(control_frame, text="Export Report", 
                                       command=self.export_report, state=tk.DISABLED)
        self.export_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           mode='determinate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=6, column=0, columnspan=3, sticky=tk.W)
        
        # Results display
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, 
                                                     width=80, height=15)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
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
            
            self.update_progress(100)
            
            # Update GUI in main thread
            self.root.after(0, self.analysis_completed, results)
            
        except Exception as e:
            self.root.after(0, self.analysis_failed, str(e))
    
    def analysis_completed(self, results: Dict[str, Any]):
        """Handle completed analysis (called in main thread)."""
        self.current_results = results
        self.analysis_running = False
        
        # Re-enable controls
        self.analyze_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.NORMAL)
        
        # Display results
        self.display_results(results)
        self.update_status("Analysis completed successfully")
        
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
    
    def display_results(self, results: Dict[str, Any]):
        """Display analysis results in the text area."""
        self.results_text.delete(1.0, tk.END)
        
        try:
            # Format and display summary
            summary = results.get("summary", {})
            
            output = []
            output.append("ANALYSIS SUMMARY")
            output.append("=" * 50)
            output.append(f"Model: {summary.get('model_name', 'Unknown')}")
            output.append(f"Total Files: {summary.get('total_files', 0)}")
            output.append(f"Successful Analyses: {summary.get('successful_analyses', 0)}")
            output.append(f"Failed Analyses: {summary.get('failed_analyses', 0)}")
            output.append(f"Languages Detected: {', '.join(summary.get('languages_detected', []))}")
            output.append(f"Total Sticky Tokens: {summary.get('total_sticky_tokens', 0)}")
            output.append("")
            
            # Display individual results
            output.append("INDIVIDUAL RESULTS")
            output.append("=" * 50)
            
            for result in results.get("individual_results", []):
                if "error" in result:
                    output.append(f"❌ {result.get('filename', 'Unknown')}: {result['error']}")
                else:
                    filename = result.get('filename', 'Unknown')
                    language = result.get('language', 'Unknown')
                    basic_analysis = result.get('basic_analysis', {})
                    sticky_count = len(basic_analysis.get('sticky_tokens', []))
                    
                    output.append(f"✅ {filename} ({language})")
                    output.append(f"   Sticky Tokens: {sticky_count}")
                    
                    if sticky_count > 0:
                        sticky_tokens = basic_analysis.get('sticky_tokens', [])
                        sample_tokens = sticky_tokens[:5]  # Show first 5
                        output.append(f"   Sample Tokens: {sample_tokens}")
                        if len(sticky_tokens) > 5:
                            output.append(f"   ... and {len(sticky_tokens) - 5} more")
                    
                    output.append("")
            
            # Display the formatted output
            self.results_text.insert(tk.END, "\\n".join(output))
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Error displaying results: {e}")
    
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


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    
    # Set up the style
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    
    # Create the application
    app = StickyCharacterGUI(root)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()