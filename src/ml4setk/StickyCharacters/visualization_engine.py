"""
Visualization engine for sticky character analysis results.
Generates comprehensive charts and graphs for analysis results.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
import os
from datetime import datetime
from collections import defaultdict, Counter
import json


class StickyVisualizationEngine:
    """
    Comprehensive visualization engine for sticky character analysis.
    """
    
    def __init__(self, output_dir: str = "visualizations"):
        """
        Initialize the visualization engine.
        
        Args:
            output_dir: Directory to save visualization files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up matplotlib and seaborn styling
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Configure matplotlib for better display
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        
        self.color_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
    
    def create_sticky_tokens_summary(self, results: Dict[str, Any], 
                                   save_path: Optional[str] = None) -> str:
        """
        Create a summary visualization of sticky tokens across files.
        
        Args:
            results: Analysis results from integrated analyzer
            save_path: Optional custom save path
            
        Returns:
            Path to saved visualization
        """
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"sticky_tokens_summary_{timestamp}.png")
        
        # Extract data
        individual_results = results.get('individual_results', [])
        if not individual_results:
            raise ValueError("No individual results found in data")
        
        # Prepare data for visualization
        file_data = []
        for result in individual_results:
            if 'error' not in result:
                filename = result.get('filename', 'Unknown')
                language = result.get('language', 'Unknown')
                basic_analysis = result.get('basic_analysis', {})
                
                total_tokens = len(basic_analysis.get('table', []))
                sticky_tokens = len(basic_analysis.get('sticky_tokens', []))
                
                file_data.append({
                    'filename': filename,
                    'language': language,
                    'total_tokens': total_tokens,
                    'sticky_tokens': sticky_tokens,
                    'sticky_ratio': sticky_tokens / max(total_tokens, 1) * 100
                })
        
        if not file_data:
            raise ValueError("No valid analysis results found")
        
        # Create subplot layout
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Sticky Tokens Analysis Summary', fontsize=16, fontweight='bold')
        
        # 1. Sticky tokens count by file
        filenames = [data['filename'] for data in file_data]
        sticky_counts = [data['sticky_tokens'] for data in file_data]
        colors = [self.color_palette[i % len(self.color_palette)] for i in range(len(filenames))]
        
        bars1 = ax1.bar(range(len(filenames)), sticky_counts, color=colors)
        ax1.set_title('Sticky Tokens Count by File')
        ax1.set_xlabel('Files')
        ax1.set_ylabel('Number of Sticky Tokens')
        ax1.set_xticks(range(len(filenames)))
        ax1.set_xticklabels(filenames, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, count in zip(bars1, sticky_counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom')
        
        # 2. Sticky ratio by file
        sticky_ratios = [data['sticky_ratio'] for data in file_data]
        bars2 = ax2.bar(range(len(filenames)), sticky_ratios, color=colors)
        ax2.set_title('Sticky Token Ratio by File (%)')
        ax2.set_xlabel('Files')
        ax2.set_ylabel('Sticky Token Ratio (%)')
        ax2.set_xticks(range(len(filenames)))
        ax2.set_xticklabels(filenames, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, ratio in zip(bars2, sticky_ratios):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{ratio:.1f}%', ha='center', va='bottom')
        
        # 3. Language distribution
        language_counts = Counter([data['language'] for data in file_data])
        languages = list(language_counts.keys())
        counts = list(language_counts.values())
        
        wedges, texts, autotexts = ax3.pie(counts, labels=languages, autopct='%1.1f%%',
                                          startangle=90, colors=self.color_palette[:len(languages)])
        ax3.set_title('Distribution by Programming Language')
        
        # 4. Total vs Sticky tokens scatter
        total_tokens = [data['total_tokens'] for data in file_data]
        ax4.scatter(total_tokens, sticky_counts, c=colors, s=100, alpha=0.7)
        ax4.set_title('Total Tokens vs Sticky Tokens')
        ax4.set_xlabel('Total Tokens')
        ax4.set_ylabel('Sticky Tokens')
        
        # Add file labels to scatter plot
        for i, data in enumerate(file_data):
            ax4.annotate(data['filename'], (data['total_tokens'], data['sticky_tokens']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def create_language_comparison(self, results: Dict[str, Any],
                                 save_path: Optional[str] = None) -> str:
        """
        Create language comparison visualization.
        """
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"language_comparison_{timestamp}.png")
        
        # Extract language data
        individual_results = results.get('individual_results', [])
        language_data = defaultdict(lambda: {'total_tokens': 0, 'sticky_tokens': 0, 'files': 0})
        
        for result in individual_results:
            if 'error' not in result:
                language = result.get('language', 'Unknown')
                basic_analysis = result.get('basic_analysis', {})
                
                total_tokens = len(basic_analysis.get('table', []))
                sticky_tokens = len(basic_analysis.get('sticky_tokens', []))
                
                language_data[language]['total_tokens'] += total_tokens
                language_data[language]['sticky_tokens'] += sticky_tokens
                language_data[language]['files'] += 1
        
        if not language_data:
            raise ValueError("No language data found")
        
        # Prepare data for plotting
        languages = list(language_data.keys())
        avg_sticky_ratios = []
        total_sticky_counts = []
        file_counts = []
        
        for lang in languages:
            data = language_data[lang]
            total = data['total_tokens']
            sticky = data['sticky_tokens']
            ratio = (sticky / max(total, 1)) * 100
            avg_sticky_ratios.append(ratio)
            total_sticky_counts.append(sticky)
            file_counts.append(data['files'])
        
        # Create visualization
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Programming Language Comparison', fontsize=16, fontweight='bold')
        
        colors = [self.color_palette[i % len(self.color_palette)] for i in range(len(languages))]
        
        # 1. Average sticky ratio by language
        bars1 = ax1.bar(languages, avg_sticky_ratios, color=colors)
        ax1.set_title('Average Sticky Token Ratio by Language')
        ax1.set_ylabel('Sticky Token Ratio (%)')
        ax1.set_xticklabels(languages, rotation=45, ha='right')
        
        for bar, ratio in zip(bars1, avg_sticky_ratios):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{ratio:.1f}%', ha='center', va='bottom')
        
        # 2. Total sticky tokens by language
        bars2 = ax2.bar(languages, total_sticky_counts, color=colors)
        ax2.set_title('Total Sticky Tokens by Language')
        ax2.set_ylabel('Total Sticky Tokens')
        ax2.set_xticklabels(languages, rotation=45, ha='right')
        
        for bar, count in zip(bars2, total_sticky_counts):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom')
        
        # 3. Number of files by language
        bars3 = ax3.bar(languages, file_counts, color=colors)
        ax3.set_title('Number of Files by Language')
        ax3.set_ylabel('Number of Files')
        ax3.set_xticklabels(languages, rotation=45, ha='right')
        
        for bar, count in zip(bars3, file_counts):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def create_token_distribution_heatmap(self, results: Dict[str, Any],
                                        save_path: Optional[str] = None) -> str:
        """
        Create a heatmap showing token distribution patterns.
        """
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"token_distribution_heatmap_{timestamp}.png")
        
        # Extract token data
        individual_results = results.get('individual_results', [])
        token_data = []
        
        for result in individual_results:
            if 'error' not in result:
                filename = result.get('filename', 'Unknown')
                language = result.get('language', 'Unknown')
                basic_analysis = result.get('basic_analysis', {})
                
                # Count different types of tokens
                table = basic_analysis.get('table', [])
                sticky_tokens = basic_analysis.get('sticky_tokens', [])
                
                total_tokens = len(table)
                sticky_count = len(sticky_tokens)
                non_sticky_count = total_tokens - sticky_count
                
                # Calculate token length distribution
                if table:
                    token_lengths = [len(row.get('token', '')) for row in table]
                    avg_token_length = np.mean(token_lengths)
                    max_token_length = np.max(token_lengths)
                else:
                    avg_token_length = 0
                    max_token_length = 0
                
                token_data.append({
                    'File': filename,
                    'Language': language,
                    'Total Tokens': total_tokens,
                    'Sticky Tokens': sticky_count,
                    'Non-Sticky Tokens': non_sticky_count,
                    'Avg Token Length': avg_token_length,
                    'Max Token Length': max_token_length,
                    'Sticky Ratio': (sticky_count / max(total_tokens, 1)) * 100
                })
        
        if not token_data:
            raise ValueError("No token data found")
        
        # Create DataFrame for heatmap
        df = pd.DataFrame(token_data)
        
        # Select numeric columns for heatmap
        numeric_columns = ['Total Tokens', 'Sticky Tokens', 'Non-Sticky Tokens', 
                          'Avg Token Length', 'Max Token Length', 'Sticky Ratio']
        heatmap_data = df[numeric_columns].T
        heatmap_data.columns = df['File']
        
        # Normalize data for better visualization
        heatmap_data_normalized = heatmap_data.div(heatmap_data.max(axis=1), axis=0)
        
        # Create heatmap
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        fig.suptitle('Token Distribution Analysis', fontsize=16, fontweight='bold')
        
        # Raw values heatmap
        sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd', 
                   ax=ax1, cbar_kws={'label': 'Count/Value'})
        ax1.set_title('Raw Token Statistics by File')
        ax1.set_ylabel('Metrics')
        
        # Normalized heatmap
        sns.heatmap(heatmap_data_normalized, annot=True, fmt='.2f', cmap='viridis',
                   ax=ax2, cbar_kws={'label': 'Normalized Value (0-1)'})
        ax2.set_title('Normalized Token Statistics by File')
        ax2.set_ylabel('Metrics')
        ax2.set_xlabel('Files')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def create_detailed_token_analysis(self, results: Dict[str, Any],
                                     save_path: Optional[str] = None) -> str:
        """
        Create detailed analysis of individual tokens.
        """
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"detailed_token_analysis_{timestamp}.png")
        
        # Extract all sticky tokens
        all_sticky_tokens = []
        individual_results = results.get('individual_results', [])
        
        for result in individual_results:
            if 'error' not in result:
                filename = result.get('filename', 'Unknown')
                language = result.get('language', 'Unknown')
                basic_analysis = result.get('basic_analysis', {})
                sticky_tokens = basic_analysis.get('sticky_tokens', [])
                
                for token_info in sticky_tokens:
                    token = token_info.get('token', '')
                    code_piece = token_info.get('code_piece', '')
                    all_sticky_tokens.append({
                        'token': token,
                        'code_piece': code_piece,
                        'filename': filename,
                        'language': language,
                        'length': len(token)
                    })
        
        if not all_sticky_tokens:
            raise ValueError("No sticky tokens found")
        
        # Analyze token patterns
        token_counter = Counter([t['token'] for t in all_sticky_tokens])
        length_counter = Counter([t['length'] for t in all_sticky_tokens])
        language_token_counter = defaultdict(lambda: Counter())
        
        for token_info in all_sticky_tokens:
            language_token_counter[token_info['language']][token_info['token']] += 1
        
        # Create visualization
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        fig.suptitle('Detailed Sticky Token Analysis', fontsize=16, fontweight='bold')
        
        # 1. Most common sticky tokens
        ax1 = fig.add_subplot(gs[0, :2])
        if token_counter:
            most_common = token_counter.most_common(15)
            tokens, counts = zip(*most_common)
            bars = ax1.barh(range(len(tokens)), counts, color=self.color_palette[0])
            ax1.set_yticks(range(len(tokens)))
            ax1.set_yticklabels(tokens)
            ax1.set_xlabel('Frequency')
            ax1.set_title('Most Common Sticky Tokens')
            ax1.invert_yaxis()
            
            # Add value labels
            for i, (bar, count) in enumerate(zip(bars, counts)):
                ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                        f'{count}', ha='left', va='center')
        
        # 2. Token length distribution
        ax2 = fig.add_subplot(gs[0, 2])
        if length_counter:
            lengths = sorted(length_counter.keys())
            counts = [length_counter[l] for l in lengths]
            ax2.bar(lengths, counts, color=self.color_palette[1], alpha=0.7)
            ax2.set_xlabel('Token Length')
            ax2.set_ylabel('Count')
            ax2.set_title('Token Length Distribution')
        
        # 3. Language-specific token patterns
        ax3 = fig.add_subplot(gs[1, :])
        if language_token_counter:
            # Create matrix for language-token heatmap
            all_unique_tokens = set()
            for lang_counter in language_token_counter.values():
                all_unique_tokens.update(lang_counter.keys())
            
            # Limit to most common tokens for readability
            all_unique_tokens = list(all_unique_tokens)[:20]
            languages = list(language_token_counter.keys())
            
            matrix = np.zeros((len(languages), len(all_unique_tokens)))
            for i, lang in enumerate(languages):
                for j, token in enumerate(all_unique_tokens):
                    matrix[i, j] = language_token_counter[lang][token]
            
            im = ax3.imshow(matrix, cmap='Blues', aspect='auto')
            ax3.set_xticks(range(len(all_unique_tokens)))
            ax3.set_xticklabels(all_unique_tokens, rotation=45, ha='right')
            ax3.set_yticks(range(len(languages)))
            ax3.set_yticklabels(languages)
            ax3.set_title('Sticky Token Patterns by Language')
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax3, shrink=0.8)
            cbar.set_label('Token Frequency')
        
        # 4. Token diversity by file
        ax4 = fig.add_subplot(gs[2, :])
        file_diversity = defaultdict(set)
        for token_info in all_sticky_tokens:
            file_diversity[token_info['filename']].add(token_info['token'])
        
        if file_diversity:
            filenames = list(file_diversity.keys())
            diversity_counts = [len(file_diversity[f]) for f in filenames]
            
            bars = ax4.bar(range(len(filenames)), diversity_counts, 
                          color=[self.color_palette[i % len(self.color_palette)] 
                                for i in range(len(filenames))])
            ax4.set_xticks(range(len(filenames)))
            ax4.set_xticklabels(filenames, rotation=45, ha='right')
            ax4.set_ylabel('Unique Sticky Tokens')
            ax4.set_title('Token Diversity by File')
            
            # Add value labels
            for bar, count in zip(bars, diversity_counts):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{count}', ha='center', va='bottom')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def create_model_comparison(self, multiple_results: List[Dict[str, Any]],
                              save_path: Optional[str] = None) -> str:
        """
        Create visualization comparing results across different models.
        
        Args:
            multiple_results: List of analysis results from different models
            save_path: Optional custom save path
            
        Returns:
            Path to saved visualization
        """
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.output_dir, f"model_comparison_{timestamp}.png")
        
        model_data = []
        for results in multiple_results:
            summary = results.get('summary', {})
            model_name = summary.get('model_name', 'Unknown')
            
            model_data.append({
                'model': model_name.split('/')[-1] if '/' in model_name else model_name,
                'total_files': summary.get('total_files', 0),
                'successful_analyses': summary.get('successful_analyses', 0),
                'total_sticky_tokens': summary.get('total_sticky_tokens', 0),
                'languages': len(summary.get('languages_detected', []))
            })
        
        if not model_data:
            raise ValueError("No model comparison data available")
        
        # Create comparison visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
        
        models = [data['model'] for data in model_data]
        colors = [self.color_palette[i % len(self.color_palette)] for i in range(len(models))]
        
        # 1. Total sticky tokens by model
        sticky_counts = [data['total_sticky_tokens'] for data in model_data]
        bars1 = ax1.bar(models, sticky_counts, color=colors)
        ax1.set_title('Total Sticky Tokens by Model')
        ax1.set_ylabel('Total Sticky Tokens')
        ax1.set_xticklabels(models, rotation=45, ha='right')
        
        for bar, count in zip(bars1, sticky_counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom')
        
        # 2. Success rate by model
        success_rates = [data['successful_analyses'] / max(data['total_files'], 1) * 100 
                        for data in model_data]
        bars2 = ax2.bar(models, success_rates, color=colors)
        ax2.set_title('Analysis Success Rate by Model (%)')
        ax2.set_ylabel('Success Rate (%)')
        ax2.set_xticklabels(models, rotation=45, ha='right')
        ax2.set_ylim(0, 100)
        
        for bar, rate in zip(bars2, success_rates):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{rate:.1f}%', ha='center', va='bottom')
        
        # 3. Languages detected by model
        lang_counts = [data['languages'] for data in model_data]
        bars3 = ax3.bar(models, lang_counts, color=colors)
        ax3.set_title('Languages Detected by Model')
        ax3.set_ylabel('Number of Languages')
        ax3.set_xticklabels(models, rotation=45, ha='right')
        
        for bar, count in zip(bars3, lang_counts):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom')
        
        # 4. Model efficiency (sticky tokens per successful analysis)
        efficiency = [data['total_sticky_tokens'] / max(data['successful_analyses'], 1)
                     for data in model_data]
        bars4 = ax4.bar(models, efficiency, color=colors)
        ax4.set_title('Average Sticky Tokens per File')
        ax4.set_ylabel('Avg Sticky Tokens per File')
        ax4.set_xticklabels(models, rotation=45, ha='right')
        
        for bar, eff in zip(bars4, efficiency):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{eff:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def generate_all_visualizations(self, results: Dict[str, Any]) -> List[str]:
        """
        Generate all available visualizations for the given results.
        
        Args:
            results: Analysis results from integrated analyzer
            
        Returns:
            List of paths to generated visualization files
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = results.get('summary', {}).get('model_name', 'unknown').replace('/', '_')
        
        generated_files = []
        
        try:
            # 1. Summary visualization
            summary_path = self.create_sticky_tokens_summary(
                results, 
                os.path.join(self.output_dir, f"summary_{model_name}_{timestamp}.png")
            )
            generated_files.append(summary_path)
            
            # 2. Language comparison
            lang_comp_path = self.create_language_comparison(
                results,
                os.path.join(self.output_dir, f"language_comparison_{model_name}_{timestamp}.png")
            )
            generated_files.append(lang_comp_path)
            
            # 3. Token distribution heatmap
            heatmap_path = self.create_token_distribution_heatmap(
                results,
                os.path.join(self.output_dir, f"token_heatmap_{model_name}_{timestamp}.png")
            )
            generated_files.append(heatmap_path)
            
            # 4. Detailed token analysis
            detailed_path = self.create_detailed_token_analysis(
                results,
                os.path.join(self.output_dir, f"detailed_analysis_{model_name}_{timestamp}.png")
            )
            generated_files.append(detailed_path)
            
        except Exception as e:
            print(f"Warning: Some visualizations could not be generated: {e}")
        
        return generated_files
    
    def save_visualization_metadata(self, visualization_paths: List[str], 
                                   results: Dict[str, Any]) -> str:
        """
        Save metadata about generated visualizations.
        
        Args:
            visualization_paths: List of paths to generated visualizations
            results: Original analysis results
            
        Returns:
            Path to metadata file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metadata_path = os.path.join(self.output_dir, f"visualization_metadata_{timestamp}.json")
        
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "model_name": results.get('summary', {}).get('model_name', 'unknown'),
            "total_files_analyzed": results.get('summary', {}).get('total_files', 0),
            "total_sticky_tokens": results.get('summary', {}).get('total_sticky_tokens', 0),
            "languages_detected": results.get('summary', {}).get('languages_detected', []),
            "visualizations": [
                {
                    "filename": os.path.basename(path),
                    "full_path": path,
                    "type": self._get_visualization_type(path),
                    "file_size": os.path.getsize(path) if os.path.exists(path) else 0
                }
                for path in visualization_paths
            ]
        }
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return metadata_path
    
    def _get_visualization_type(self, path: str) -> str:
        """Determine visualization type from filename."""
        filename = os.path.basename(path).lower()
        if 'summary' in filename:
            return 'Summary Dashboard'
        elif 'language_comparison' in filename:
            return 'Language Comparison'
        elif 'heatmap' in filename:
            return 'Token Distribution Heatmap'
        elif 'detailed' in filename:
            return 'Detailed Token Analysis'
        elif 'model_comparison' in filename:
            return 'Model Comparison'
        else:
            return 'General Visualization'