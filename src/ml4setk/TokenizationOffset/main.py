import os
import argparse
import glob
from tree_sitter import Language, Parser
from transformers import AutoTokenizer
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DEFAULT_MODELS = [
    "gpt2",   
    "codellama/CodeLlama-7b-hf", 
    "bigcode/starcoder2-3b" 
]
DEFAULT_CODE_PATH = "code_samples/python"
DEFAULT_LANGUAGE = "python"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Analyze alignment between LLM tokenizers and grammar boundaries")
    parser.add_argument("--model", "-m", type=str, help="Specify model name to test, e.g. gpt2")
    parser.add_argument("--code_path", "-c", type=str, default=DEFAULT_CODE_PATH, 
                        help=f"Specify code file or directory path (default: {DEFAULT_CODE_PATH})")
    parser.add_argument("--language", "-l", type=str, default=DEFAULT_LANGUAGE,
                        help=f"Specify code language (default: {DEFAULT_LANGUAGE})")
    return parser.parse_args()


def setup_tree_sitter_parser(language_name: str) -> Parser:
    library_path = f'build/languages_{language_name}.so'
    repo_info = get_tree_sitter_repo_info(language_name)
    repo_path = f'vendor/{repo_info["local_name"]}'
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"Tree-sitter grammar for {language_name} not found in {repo_path}")
    repo_info = get_tree_sitter_repo_info(language_name)
    if os.path.exists(library_path):
        os.remove(library_path)
    if language_name == "typescript":
        Language.build_library(
            library_path,
            [
                f"{repo_path}/typescript",
                f"{repo_path}/tsx"
            ]
        )
        lang = Language(library_path, "typescript")
    elif repo_info.get('custom_build', False):
        print(f"Using custom build process for {language_name} language library...")
        os.makedirs(os.path.dirname(library_path), exist_ok=True)
        build_commands = [
            f"cd {repo_path} && npm install",
            f"cd {repo_path} && npx tree-sitter generate",
            f"cd {repo_path} && gcc -shared -o {os.path.abspath(library_path)} -fPIC src/parser.c -I./src"
        ]
        
        for cmd in build_commands:
            print(f"Executing: {cmd}")
            result = os.system(cmd)
            if result != 0:
                raise Exception(f"Command execution failed: {cmd}")
        lang = Language(library_path, language_name)
    else:
        try:
            Language.build_library(
                library_path,
                [repo_path]
            )
        except Exception as e:
            print(f"Error building language library: {e}")
            print("Trying compatibility mode...")
            try:
                os.system(f"cd {repo_path} && npm install")
                os.system(f"cd {repo_path} && npx tree-sitter generate")
                os.system(f"cd {repo_path} && gcc -shared -o {os.path.abspath(library_path)} -fPIC src/parser.c -I./src")
            except Exception:
                os.system(f"cd {repo_path} && make")
                for ext in ['.so', '.dylib', '.dll']:
                    lib_file = f"{repo_path}/libtree-sitter-{language_name}{ext}"
                    if os.path.exists(lib_file):
                        os.system(f"cp {lib_file} {library_path}")
                        break
        if language_name == "csharp":
            lang = Language(library_path, "c_sharp")
        else:
            lang = Language(library_path, language_name)
    
    parser = Parser()
    parser.set_language(lang)
    return parser

def get_grammar_node_boundaries(parser: Parser, code_bytes: bytes) -> set:
    tree = parser.parse(code_bytes)
    boundaries = set()
    cursor = tree.walk()
    nodes_to_visit = [tree.root_node]
    while nodes_to_visit:
        node = nodes_to_visit.pop(0)
        if node.start_byte != node.end_byte:
            boundaries.add(node.start_byte)
            boundaries.add(node.end_byte)
        nodes_to_visit.extend(node.children)
    return boundaries

def get_tokenizer_token_boundaries(model_name: str, code_string: str) -> set:
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    encoding = tokenizer(code_string, return_offsets_mapping=True)
    boundaries = set()
    for start, end in encoding['offset_mapping']:
        if start != end:
            boundaries.add(start)
            boundaries.add(end)       
    return boundaries

def analyze_file(file_path, parser, models_to_test, language):
    print(f"\nAnalyzing file: {file_path}")
    with open(file_path, "rb") as f:
        code_bytes = f.read()
    code_string = code_bytes.decode("utf-8")
    grammar_boundaries = get_grammar_node_boundaries(parser, code_bytes)
    print(f"Found {len(grammar_boundaries)} unique grammar boundaries from tree-sitter.")
    
    file_results = []
    
    for model_name in models_to_test:
        print(f"\n--- Analyzing model: {model_name} ---")
        try:
            tokenizer_boundaries = get_tokenizer_token_boundaries(model_name, code_string)
            print(f"Found {len(tokenizer_boundaries)} unique token boundaries for {model_name}.")

            mismatched_boundaries = grammar_boundaries.difference(tokenizer_boundaries)
            
            alignment_score = 0
            if grammar_boundaries:
                alignment_score = (1 - len(mismatched_boundaries) / len(grammar_boundaries)) * 100
            
            file_results.append({
                "file_name": os.path.basename(file_path),
                "model_name": model_name,
                "language": language,
                "grammar_boundaries": len(grammar_boundaries),
                "tokenizer_boundaries": len(tokenizer_boundaries),
                "mismatched_boundaries": len(mismatched_boundaries),
                "alignment_score_percent": alignment_score
            })
            
            print(f"Alignment score: {alignment_score:.2f}%")
        except Exception as e:
            print(f"Could not process {model_name}. Error: {e}")
    return file_results

def get_tree_sitter_repo_info(language):
    default_info = {
        'repo_url': f"https://github.com/tree-sitter/tree-sitter-{language}.git",
        'local_name': f"tree-sitter-{language}",
        'specific_version': None,  
        'custom_build': False 
    }
    
    special_cases = {
        "c": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-c.git",
            'local_name': "tree-sitter-c",
            'specific_version': "v0.20.2",  
            'custom_build': False
        },
        "cpp": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-cpp.git",
            'local_name': "tree-sitter-cpp",
            'specific_version': "v0.20.0",  
            'custom_build': False
        },
        "csharp": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-c-sharp.git",
            'local_name': "tree-sitter-c-sharp",
            'custom_build': False
        },
        "typescript": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-typescript.git",
            'local_name': "tree-sitter-typescript",
            'custom_build': False
        },
        "scala": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-scala.git",
            'local_name': "tree-sitter-scala",
            'custom_build': False
        },
        "rust": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-rust.git",
            'local_name': "tree-sitter-rust",
            'specific_version': "v0.20.3", 
            'custom_build': False
        }
    }
    return special_cases.get(language, default_info)

def get_file_extension(language):
    """Return the file extension corresponding to the language name"""
    extension_map = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "java": ".java",
        "c": ".c",
        "cpp": ".cpp",
        "csharp": ".cs",
        "go": ".go",
        "ruby": ".rb",
        "rust": ".rs",
        "scala": ".scala"
    }
    return extension_map.get(language, f".{language}")

def main():
    """Main function, perform analysis and generate report"""
    args = parse_args()
    print("Starting analysis...")
    print(f"Using model: {args.model if args.model else 'default model list'}")
    print(f"Code path: {args.code_path}")
    print(f"Code language: {args.language}")
    os.makedirs("build", exist_ok=True)
    models_to_test = [args.model] if args.model else DEFAULT_MODELS
    language = args.language
    repo_info = get_tree_sitter_repo_info(language)
    repo_path = f"vendor/{repo_info['local_name']}"
    os.makedirs("vendor", exist_ok=True)

    if not os.path.exists(repo_path):
        print(f"Cloning {repo_info['repo_url']} repository...")
        os.system(f"git clone {repo_info['repo_url']} {repo_path}")
        if repo_info['specific_version']:
            print(f"Switching to version: {repo_info['specific_version']}...")
            current_dir = os.getcwd()
            os.chdir(repo_path)
            os.system(f"git checkout {repo_info['specific_version']}")
            os.chdir(current_dir)

    if repo_info.get('custom_build', False):
        if os.path.exists(os.path.join(repo_path, "package.json")):
            print(f"Installing Node.js dependencies for {language}...")
            os.system(f"cd {repo_path} && npm install")
    
    parser = setup_tree_sitter_parser(language)
    code_path = args.code_path
    all_results = []
    
    if os.path.isdir(code_path):
        file_extension = get_file_extension(language)
        if "code_samples" in code_path:
            language_specific_path = os.path.join("code_samples", language)
            if os.path.exists(language_specific_path) and os.path.isdir(language_specific_path):
                code_path = language_specific_path
                print(f"Automatically switched to language-specific folder: {code_path}")
        
        code_files = glob.glob(os.path.join(code_path, f"*{file_extension}"))
        if not code_files:
            print(f"No {file_extension} files found in {code_path}")
            return   
        for file_path in code_files:
            file_results = analyze_file(file_path, parser, models_to_test, language)
            all_results.extend(file_results)
    else:
        if not os.path.exists(code_path):
            print(f"File {code_path} does not exist")
            return
        file_results = analyze_file(code_path, parser, models_to_test, language)
        all_results.extend(file_results)
    if not all_results:
        print("No results to report.")
        return
        
    df = pd.DataFrame(all_results)
    os.makedirs("results", exist_ok=True)
    language = args.language
    for result in all_results:
        result["language"] = language
    
    report_path = f"results/alignment_report_{language}.csv"
    df.to_csv(report_path, index=False)
    print(f"\nComplete report has been saved to {report_path}")

    model_avg = df.groupby('model_name')['alignment_score_percent'].mean().reset_index()
    model_avg_sorted = model_avg.sort_values("alignment_score_percent", ascending=False)
    
    plt.figure(figsize=(12, 7))
    sns.barplot(x="alignment_score_percent", y="model_name", data=model_avg_sorted, palette="viridis", hue="model_name", dodge=False)
    plt.title(f"{language.upper()} Language - LLM Tokenizer and Tree-sitter Grammar Boundary Alignment Analysis")
    plt.xlabel("Alignment Score (%)")
    plt.ylabel("Model")
    plt.xlim(0, 100)
    plt.tight_layout()
    
    chart_path = f"results/alignment_chart_{language}_by_model.png"
    plt.savefig(chart_path)
    print(f"Model comparison chart has been saved to {chart_path}")

    if len(df['file_name'].unique()) > 1:
        plt.figure(figsize=(14, 8))
        sns.barplot(x="alignment_score_percent", y="file_name", hue="model_name", data=df, palette="viridis")
        plt.title(f"{language.upper()} Language - Model Alignment Score Comparison by File")
        plt.xlabel("Alignment Score (%)")
        plt.ylabel("File")
        plt.xlim(0, 100)
        plt.tight_layout()
        
        file_chart_path = f"results/alignment_chart_{language}_by_file.png"
        plt.savefig(file_chart_path)
        print(f"File comparison chart has been saved to {file_chart_path}")



if __name__ == "__main__":
    main()