import sys
import os
import argparse
from transformers import AutoTokenizer
import colorama
from colorama import Fore, Style

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

def get_file_extension(language):
    """Return the file extension corresponding to the language name"""
    return SUPPORTED_LANGUAGES.get(language, f".{language}")

def visualize_tokens(model_name, code_string, language=None):
    """Visualize how a model tokenizes code"""
    colorama.init()
    
    language_info = f"({language} language)" if language else ""
    print(f"\n{Fore.CYAN}===== Model {model_name} {language_info} Tokenization Visualization ====={Style.RESET_ALL}")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

        encoding = tokenizer(code_string, return_offsets_mapping=True)
        tokens = tokenizer.convert_ids_to_tokens(encoding['input_ids'])
        offsets = encoding['offset_mapping']
        print(f"\n{Fore.WHITE}Original Code:{Style.RESET_ALL}")
        print(code_string)

        print(f"\n{Fore.WHITE}Tokenization Results:{Style.RESET_ALL}")

        start_idx = 0
        while start_idx < len(tokens) and offsets[start_idx] == (0, 0):
            start_idx += 1

        colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA]
        
        for i in range(start_idx, len(tokens)):
            token = tokens[i]
            start, end = offsets[i]
            
            if start == end: 
                continue
                
            color = colors[(i - start_idx) % len(colors)]
            print(f"{color}[{token}]{Style.RESET_ALL}", end=" ")
            if (i - start_idx + 1) % 10 == 0:
                print()
                
        print("\n")
        print(f"\n{Fore.WHITE}Code with Boundary Markers:{Style.RESET_ALL}")
 
        chars = list(code_string)
        boundaries = set()
        for start, end in offsets:
            if start != end: 
                boundaries.add(start)
                boundaries.add(end)

        for pos in sorted(boundaries, reverse=True):
            if pos > 0 and pos < len(chars):
                chars.insert(pos, f"{Fore.RED}|{Style.RESET_ALL}")
        
        print(''.join(chars))
        
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def get_sample_code(language):
    """Return sample code for the specified language"""
    samples = {
        "python": """
def hello_world():
    print("Hello, world!")
    return 42
""",
        "javascript": """
function helloWorld() {
    console.log("Hello, world!");
    return 42;
}
""",
        "typescript": """
function helloWorld(): number {
    console.log("Hello, world!");
    return 42;
}
""",
        "java": """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
    
    public static int getValue() {
        return 42;
    }
}
""",
        "c": """
#include <stdio.h>

int main() {
    printf("Hello, world!\\n");
    return 0;
}

int get_value() {
    return 42;
}
""",
        "cpp": """
#include <iostream>

int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;
}

int get_value() {
    return 42;
}
""",
        "csharp": """
using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, world!");
    }
    
    static int GetValue() {
        return 42;
    }
}
""",
        "go": """
package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}

func getValue() int {
    return 42
}
""",
        "ruby": """
def hello_world
  puts "Hello, world!"
  return 42
end

hello_world
""",
        "rust": """
fn main() {
    println!("Hello, world!");
}

fn get_value() -> i32 {
    42
}
""",
        "scala": """
object HelloWorld {
  def main(args: Array[String]): Unit = {
    println("Hello, world!")
  }
  
  def getValue(): Int = {
    42
  }
}
"""
    }
    
    return samples.get(language, samples["python"])

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Visualize LLM tokenizer's tokenization of code")
    parser.add_argument("--model", "-m", type=str, default="gpt2", 
                        help="Model name to use (default: gpt2)")
    parser.add_argument("--file", "-f", type=str, 
                        help="Path to code file to analyze")
    parser.add_argument("--language", "-l", type=str, default="python",
                        help=f"Code language (default: python, supported: {', '.join(SUPPORTED_LANGUAGES.keys())})")
    return parser.parse_args()

def find_language_specific_file(language):
    """Find a language-specific sample file in the code_samples directory"""
    language_dir = os.path.join("code_samples", language)
    if os.path.exists(language_dir) and os.path.isdir(language_dir):
        file_ext = get_file_extension(language)
        files = [f for f in os.listdir(language_dir) if f.endswith(file_ext)]
        if files:
            return os.path.join(language_dir, files[0])
    return None

if __name__ == "__main__":
    args = parse_arguments()
    
    model_name = args.model
    language = args.language.lower()

    if language not in SUPPORTED_LANGUAGES:
        print(f"Warning: Unsupported language '{language}'. Using default language 'python'.")
        print(f"Supported languages: {', '.join(SUPPORTED_LANGUAGES.keys())}")
        language = "python"
    
    if args.file:
        try:
            with open(args.file, 'r') as f:
                code = f.read()
        except Exception as e:
            print(f"Error: Cannot read file '{args.file}': {e}")
            sys.exit(1)
    else:
    
        language_file = find_language_specific_file(language)
        if language_file:
            print(f"Using sample file: {language_file}")
            with open(language_file, 'r') as f:
                code = f.read()
        else:
            print(f"Using built-in {language} sample code")
            code = get_sample_code(language)
    
    visualize_tokens(model_name, code, language)