import os
import json
import argparse
import glob
from tree_sitter import Language, Parser
from transformers import AutoTokenizer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

SUPPORTED_LANGUAGES = {
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

DEFAULT_MODELS = [
    "gpt2",       
    "codellama/CodeLlama-7b-hf", 
    "bigcode/starcoder2-3b"
]

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Detailed analysis of alignment between LLM tokenizers and grammar boundaries")
    parser.add_argument("--model", "-m", type=str, help="Specify model name to test, e.g. gpt2")
    parser.add_argument("--code_path", "-c", type=str, default="code_samples/python", 
                        help="Specify code file or directory path (default: code_samples/python)")
    parser.add_argument("--language", "-l", type=str, default="python",
                        help=f"Specify code language (default: python, supported: {', '.join(SUPPORTED_LANGUAGES.keys())})")
    return parser.parse_args()

def get_file_extension(language):
    """Return the file extension corresponding to the language name"""
    return SUPPORTED_LANGUAGES.get(language, f".{language}")

def get_tree_sitter_repo_info(language):
    """Get Tree-sitter repository information for the specified language"""
    default_info = {
        'repo_url': f"https://github.com/tree-sitter/tree-sitter-{language}.git",
        'local_name': f"tree-sitter-{language}",
        'version': None,
        'custom_build': False
    }

    special_cases = {
        "cpp": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-cpp.git",
            'local_name': "tree-sitter-cpp",
            'version': None,
            'custom_build': False
        },
        "csharp": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-c-sharp.git",
            'local_name': "tree-sitter-c-sharp",
            'version': None,
            'custom_build': False
        },
        "typescript": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-typescript.git",
            'local_name': "tree-sitter-typescript",
            'version': None,
            'custom_build': False
        },
        "c": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-c.git",
            'local_name': "tree-sitter-c",
            'version': "v0.20.2", 
            'custom_build': False
        },
        "rust": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-rust.git",
            'local_name': "tree-sitter-rust",
            'version': "v0.20.3",
            'custom_build': False
        },
        "scala": {
            'repo_url': "https://github.com/tree-sitter/tree-sitter-scala.git",
            'local_name': "tree-sitter-scala",
            'version': None,
            'custom_build': False
        }
    }
    
    return special_cases.get(language, default_info)

def setup_tree_sitter_parser(language_name: str) -> Parser:
    """Compile and load tree-sitter parser for the specified language"""
    library_path = f'build/languages_{language_name}.so'
    
    repo_info = get_tree_sitter_repo_info(language_name)
    repo_path = f'vendor/{repo_info["local_name"]}'
    
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"Tree-sitter grammar for {language_name} not found in {repo_path}")
    
    if language_name == "typescript":
        Language.build_library(
            library_path,
            [
                f"{repo_path}/typescript",
                f"{repo_path}/tsx"
            ]
        )
        lang = Language(library_path, "typescript")
    else:
        if os.path.exists(library_path):
            os.remove(library_path)
            
        try:
            Language.build_library(
                library_path,
                [repo_path]
            )
            
            if language_name == "csharp":
                lang = Language(library_path, "c_sharp")
            else:
                lang = Language(library_path, language_name)
        except Exception as e:
            print(f"Error building language library: {e}")
            print("Trying compatibility mode...")
            current_dir = os.getcwd()
            os.chdir(repo_path)
            os.system("make")
            os.chdir(current_dir)
            
            dylib_path = os.path.join(repo_path, f"libtree-sitter-{language_name}.dylib")
            so_path = os.path.join(repo_path, f"libtree-sitter-{language_name}.so")
            
            if os.path.exists(dylib_path):
                os.system(f"cp {dylib_path} {library_path}")
            elif os.path.exists(so_path):
                os.system(f"cp {so_path} {library_path}")
            else:
                raise FileNotFoundError(f"Could not find built library file: {dylib_path} or {so_path}")
            
            if language_name == "csharp":
                lang = Language(library_path, "c_sharp")
            else:
                lang = Language(library_path, language_name)
    
    parser = Parser()
    parser.set_language(lang)
    return parser

def get_node_details(node, code_bytes):
    """Get detailed information about a node"""
    return {
        "type": node.type,
        "start_byte": node.start_byte,
        "end_byte": node.end_byte,
        "start_point": (node.start_point[0], node.start_point[1]),
        "end_point": (node.end_point[0], node.end_point[1]),
        "text": code_bytes[node.start_byte:node.end_byte].decode('utf-8')
    }

def analyze_grammar_structure(parser, code_bytes):
    """Analyze code grammar structure and return detailed node information"""
    tree = parser.parse(code_bytes)
    nodes_info = []
    
    def traverse(node, depth=0):
        if node.start_byte != node.end_byte: 
            nodes_info.append({
                **get_node_details(node, code_bytes),
                "depth": depth
            })
        
        for child in node.children:
            traverse(child, depth + 1)
    
    traverse(tree.root_node)
    return nodes_info

def analyze_tokenization(model_name, code_string):
    """Analyze model tokenization results"""
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    encoding = tokenizer(code_string, return_offsets_mapping=True)
    
    tokens_info = []
    for i, (start, end) in enumerate(encoding['offset_mapping']):
        if start != end: 
            token = tokenizer.convert_ids_to_tokens([encoding['input_ids'][i]])[0]
            tokens_info.append({
                "token": token,
                "start_byte": start,
                "end_byte": end,
                "text": code_string[start:end]
            })
    
    return tokens_info

def find_misalignments(grammar_nodes, token_boundaries):
    """Find misalignments between grammar nodes and tokenization boundaries"""
    token_boundary_points = set()
    for start, end in token_boundaries:
        token_boundary_points.add(start)
        token_boundary_points.add(end)
    
    misalignments = []
    
    for node in grammar_nodes:
        start_misaligned = node["start_byte"] not in token_boundary_points
        end_misaligned = node["end_byte"] not in token_boundary_points
        
        if start_misaligned or end_misaligned:
            misalignments.append({
                **node,
                "start_misaligned": start_misaligned,
                "end_misaligned": end_misaligned
            })
    
    return misalignments

def analyze_node_types(misalignments):
    """Analyze which types of nodes are most frequently misaligned"""
    type_counts = {}
    for node in misalignments:
        node_type = node["type"]
        if node_type not in type_counts:
            type_counts[node_type] = 0
        type_counts[node_type] += 1
    
    return type_counts

def main():
    """Main function, perform detailed analysis"""
    args = parse_args()
    print("Starting detailed analysis...")
    print(f"Using model: {args.model if args.model else 'default model list'}")
    print(f"Code path: {args.code_path}")
    print(f"Code language: {args.language}")
    os.makedirs("build", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    models = [args.model] if args.model else DEFAULT_MODELS
    
    language = args.language
    
    repo_info = get_tree_sitter_repo_info(language)
    repo_path = f"vendor/{repo_info['local_name']}"

    os.makedirs("vendor", exist_ok=True)
    
    if not os.path.exists(repo_path):
        print(f"Cloning {repo_info['repo_url']} repository...")
        os.system(f"git clone {repo_info['repo_url']} {repo_path}")
        if repo_info['version']:
            print(f"Switching to version: {repo_info['version']}")
            os.system(f"cd {repo_path} && git checkout {repo_info['version']}")

    parser = setup_tree_sitter_parser(language)
    
    code_path = args.code_path
    all_file_results = []
    
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
            print(f"\nAnalyzing file: {file_path}")
            analyze_file(file_path, parser, models, language, all_file_results)
    else:
        if not os.path.exists(code_path):
            print(f"File {code_path} does not exist")
            return
            
        analyze_file(code_path, parser, models, language, all_file_results)
    
    if all_file_results:
        generate_summary_report(all_file_results, language)
    
    print(f"\nDetailed analysis complete. Results saved in results/{language}_detailed directory.")

def analyze_file(file_path, parser, models, language, all_results):
    """Analyze a single file"""
    try:
        with open(file_path, "rb") as f:
            code_bytes = f.read()
        code_string = code_bytes.decode("utf-8")
        print("Analyzing grammar structure...")
        grammar_nodes = analyze_grammar_structure(parser, code_bytes)
        print(f"Found {len(grammar_nodes)} grammar nodes")
        file_results = []
        
        for model_name in models:
            print(f"\nAnalyzing model: {model_name}")
            try:
                tokens_info = analyze_tokenization(model_name, code_string)
                token_boundaries = [(token["start_byte"], token["end_byte"]) for token in tokens_info]
                misalignments = find_misalignments(grammar_nodes, token_boundaries)
                type_counts = analyze_node_types(misalignments)
                misalignment_rate = len(misalignments) / len(grammar_nodes) * 100
                
                result = {
                    "file": os.path.basename(file_path),
                    "model": model_name,
                    "language": language,
                    "total_nodes": len(grammar_nodes),
                    "misaligned_nodes": len(misalignments),
                    "misalignment_rate": misalignment_rate,
                    "type_counts": type_counts
                }
                
                file_results.append(result)
                all_results.append(result)
                
                print(f"Total nodes: {len(grammar_nodes)}")
                print(f"Misaligned nodes: {len(misalignments)}")
                print(f"Misalignment rate: {misalignment_rate:.2f}%")
                os.makedirs(f"results/{language}_detailed", exist_ok=True)
                
                with open(f"results/{language}_detailed/{model_name.replace('/', '_')}_{os.path.basename(file_path)}.json", "w") as f:
                    json.dump({
                        "file": os.path.basename(file_path),
                        "language": language,
                        "grammar_nodes": grammar_nodes,
                        "tokens": tokens_info,
                        "misalignments": misalignments,
                        "type_counts": type_counts
                    }, f, indent=2)
                
            except Exception as e:
                print(f"Error analyzing {model_name}: {e}")
        
        if file_results:
            create_file_charts(file_results, os.path.basename(file_path), language)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def create_file_charts(file_results, file_name, language):
    """Create comparison charts for a single file"""
    plt.figure(figsize=(10, 6))
    df = pd.DataFrame([(r["model"], r["misalignment_rate"]) for r in file_results], 
                      columns=["Model", "Misalignment Rate (%)"])
    sns.barplot(x="Misalignment Rate (%)", y="Model", data=df, palette="viridis")
    plt.title(f"{language.upper()} - {file_name} - Grammar-Tokenization Misalignment Rate by Model")
    plt.tight_layout()
    plt.savefig(f"results/{language}_detailed/{file_name}_misalignment_rates.png")

    for result in file_results:
        model = result["model"].replace('/', '_')
        if result["type_counts"]:
            plt.figure(figsize=(12, 8))
            types = list(result["type_counts"].keys())
            counts = list(result["type_counts"].values())

            sorted_indices = sorted(range(len(counts)), key=lambda i: counts[i], reverse=True)
            types = [types[i] for i in sorted_indices]
            counts = [counts[i] for i in sorted_indices]
            
            if len(types) > 15:
                types = types[:15]
                counts = counts[:15]
            
            sns.barplot(x=counts, y=types, palette="viridis")
            plt.title(f"{language.upper()} - {file_name} - Most Frequently Misaligned Node Types in {model} Model")
            plt.xlabel("Misaligned Node Count")
            plt.tight_layout()
            plt.savefig(f"results/{language}_detailed/{file_name}_{model}_node_types.png")

def generate_summary_report(all_results, language):
    """Generate summary report"""
    os.makedirs(f"results/{language}_detailed", exist_ok=True)

    model_groups = {}
    for result in all_results:
        model = result["model"]
        if model not in model_groups:
            model_groups[model] = []
        model_groups[model].append(result["misalignment_rate"])
    
    model_avg = [(model, sum(rates)/len(rates)) for model, rates in model_groups.items()]
    plt.figure(figsize=(10, 6))
    df = pd.DataFrame(model_avg, columns=["Model", "Average Misalignment Rate (%)"])
    df = df.sort_values("Average Misalignment Rate (%)", ascending=False)
    sns.barplot(x="Average Misalignment Rate (%)", y="Model", data=df, palette="viridis")
    plt.title(f"{language.upper()} Language - Average Grammar-Tokenization Misalignment Rate by Model")
    plt.tight_layout()
    plt.savefig(f"results/{language}_detailed/average_misalignment_rates.png")

    summary_df = pd.DataFrame(all_results)
    summary_df.to_csv(f"results/{language}_detailed/summary.csv", index=False)

    for model in model_groups.keys():
        combined_type_counts = {}
        for result in all_results:
            if result["model"] == model:
                for node_type, count in result["type_counts"].items():
                    if node_type not in combined_type_counts:
                        combined_type_counts[node_type] = 0
                    combined_type_counts[node_type] += count
        
        if combined_type_counts:
            plt.figure(figsize=(12, 8))
            types = list(combined_type_counts.keys())
            counts = list(combined_type_counts.values())
            sorted_indices = sorted(range(len(counts)), key=lambda i: counts[i], reverse=True)
            types = [types[i] for i in sorted_indices]
            counts = [counts[i] for i in sorted_indices]
            if len(types) > 15:
                types = types[:15]
                counts = counts[:15]
            
            sns.barplot(x=counts, y=types, palette="viridis")
            plt.title(f"{language.upper()} Language - Most Frequently Misaligned Node Types in {model.replace('/', '_')} Model")
            plt.xlabel("Misaligned Node Count")
            plt.tight_layout()
            plt.savefig(f"results/{language}_detailed/{model.replace('/', '_')}_combined_node_types.png")

if __name__ == "__main__":
    main()