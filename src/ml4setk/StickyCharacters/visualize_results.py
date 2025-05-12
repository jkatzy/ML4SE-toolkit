import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import pandas as pd
import re

def load_results(results_dir: str = 'results') -> Dict:
    results = {}
    for filename in os.listdir(results_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(results_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                results[filename] = json.load(f)
    return results

def create_sticky_tokens_plot(results: Dict, output_dir: str = 'visualizations'):
    os.makedirs(output_dir, exist_ok=True)
    data = []
    for filename, result in results.items():
        if 'summary' in filename:
            continue
        model_name = result['model']
        language = result['language']
        sticky_count = len(result['sticky_tokens'])
        data.append({
            'Model': model_name,
            'Language': language,
            'Sticky Tokens': sticky_count,
            'Code Sample': result['code']
        })
    df = pd.DataFrame(data)
    if df.empty:
        print("Warning: No data available for sticky tokens plot")
        return
    languages = df['Language'].unique()
    n_languages = len(languages)
    fig, axes = plt.subplots(n_languages, 1, figsize=(12, 6 * n_languages))
    if n_languages == 1:
        axes = [axes]
    for ax, language in zip(axes, languages):
        lang_data = df[df['Language'] == language]
        sns.barplot(data=lang_data, x='Model', y='Sticky Tokens', ax=ax)
        ax.set_title(f'Number of Sticky Tokens by Model - {language.capitalize()}')
        ax.tick_params(axis='x', rotation=45)
        for i, v in enumerate(lang_data['Sticky Tokens']):
            ax.text(i, v, str(v), ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sticky_tokens_by_language.png'))
    plt.close()
    plt.figure(figsize=(15, 8))
    ax = sns.barplot(data=df, x='Model', y='Sticky Tokens', hue='Language')
    plt.title('Sticky Tokens Comparison Across Languages and Models')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Language', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sticky_tokens_comparison.png'))
    plt.close()

def create_token_distribution_plot(results: Dict, output_dir: str = 'visualizations'):
    os.makedirs(output_dir, exist_ok=True)
    for filename, result in results.items():
        if 'summary' in filename:
            continue
        model_name = result['model']
        language = result['language']
        tokens = result['table']
        df = pd.DataFrame(tokens)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 15))
        token_lengths = df['token'].str.len()
        sns.histplot(data=token_lengths, ax=ax1, bins=30)
        ax1.set_title(f'Token Length Distribution - {model_name} ({language})')
        ax1.set_xlabel('Token Length')
        ax1.set_ylabel('Count')
        sticky_counts = df['sticky'].value_counts()
        labels = ['Sticky' if idx else 'Non-sticky' for idx in sticky_counts.index]
        ax2.pie(sticky_counts, labels=labels, autopct='%1.1f%%')
        ax2.set_title(f'Sticky vs Non-sticky Tokens - {model_name} ({language})')
        token_types = []
        for token in df['token']:
            clean_tok = token.lstrip('▁Ġ')
            has_letter = bool(re.search(r'[A-Za-z_]', clean_tok))
            has_digit = any(ch.isdigit() for ch in clean_tok)
            has_symbol = any(ch in '()[]{}.:=+-*/><%&|^~!,;?' for ch in clean_tok)
            if has_letter and not has_digit and not has_symbol:
                token_types.append('Letters')
            elif has_digit and not has_letter and not has_symbol:
                token_types.append('Digits')
            elif has_symbol and not has_letter and not has_digit:
                token_types.append('Symbols')
            else:
                token_types.append('Mixed')
        type_counts = pd.Series(token_types).value_counts()
        ax3.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%')
        ax3.set_title(f'Token Type Distribution - {model_name} ({language})')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'token_distribution_{model_name.replace("/", "_")}_{language}.png'))
        plt.close()

def create_language_comparison_plot(results: Dict, output_dir: str = 'visualizations'):
    os.makedirs(output_dir, exist_ok=True)
    language_data = {}
    for filename, result in results.items():
        if 'summary' in filename:
            continue
        language = result['language']
        if language not in language_data:
            language_data[language] = []
        language_data[language].extend(result['sticky_tokens'])
    if not language_data:
        print("Warning: No data available for language comparison plot")
        return
    plt.figure(figsize=(15, 8))
    data = []
    for language, tokens in language_data.items():
        for token in tokens:
            data.append({
                'Language': language,
                'Token Length': len(token['token']),
                'Token': token['token']
            })
    df = pd.DataFrame(data)
    if df.empty:
        print("Warning: No token data available for language comparison plot")
        return
    sns.boxplot(data=df, x='Language', y='Token Length')
    plt.title('Sticky Token Length Distribution by Language')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'language_comparison.png'))
    plt.close()

def main():
    results = load_results()
    create_sticky_tokens_plot(results)
    create_token_distribution_plot(results)
    create_language_comparison_plot(results)
    print("Visualizations have been created in the 'visualizations' directory.")

if __name__ == '__main__':
    main() 