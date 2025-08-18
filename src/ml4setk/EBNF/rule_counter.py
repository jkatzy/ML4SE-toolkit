"""
Rule-level based counting via tree-sitter (multi-language).
- Enforces tree-sitter only (no AST fallback).
- Supports multiple languages via tree-sitter-languages (preferred) or local .so.
"""

import json
import os
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple
import argparse

from tree_sitter import Parser, Language

# Optional providers
try:
    from tree_sitter_languages import get_language as _get_language
except Exception:
    _get_language = None

try:
    from tree_sitter_python import language as _ts_python_language
except Exception:
    _ts_python_language = None


# Language alias normalization
_ALIAS_MAP: Dict[str, Tuple[str, str]] = {
    # canonical -> (ts_languages_key, canonical)
    "python": ("python", "python"),
    "javascript": ("javascript", "javascript"),
    "typescript": ("typescript", "typescript"),
    "java": ("java", "java"),
    "go": ("go", "go"),
    "cpp": ("cpp", "cpp"),
    "c": ("c", "c"),
    "csharp": ("c_sharp", "csharp"),
    "rust": ("rust", "rust"),
    "ruby": ("ruby", "ruby"),
    "scala": ("scala", "scala"),  # often not in tree_sitter_languages; rely on local .so if present
}

# Extra aliases mapping to canonical keys
_EXTRA_ALIASES: Dict[str, str] = {
    "py": "python",
    "node": "javascript",
    "js": "javascript",
    "ts": "typescript",
    "c++": "cpp",
    "cs": "csharp",
    "c#": "csharp",
    "golang": "go",
    "c_sharp": "csharp",
}


def normalize_language(lang: str) -> Tuple[str, str]:
    lang = (lang or "").strip().lower()
    if lang in _ALIAS_MAP:
        ts_key, canonical = _ALIAS_MAP[lang]
        return ts_key, canonical
    if lang in _EXTRA_ALIASES:
        canonical = _EXTRA_ALIASES[lang]
        ts_key, canonical2 = _ALIAS_MAP[canonical]
        return ts_key, canonical2
    # Fallback assume exact name is supported in ts-languages
    return lang, lang


class RuleCounter:
    """
    Count tree-sitter grammar rules (node types) in source code for multiple languages.
    """

    def __init__(self, language: str = "python"):
        self.ts_key, self.language = normalize_language(language)
        self.parser: Parser | None = None
        self.parser_source: str | None = None
        self.rule_mapping: Dict[str, str] = {}
        self._init_tree_sitter()
        self._load_rule_mapping()

    def _init_tree_sitter(self) -> None:
        """
        Initialize a tree-sitter parser for the requested language.
        Tries in order:
        1) tree_sitter_languages.get_language(ts_key)
        2) language-specific package (only python)
        3) Local prebuilt .so in TokenizationOffset/build
        """
        errors: list[str] = []

        # 1) Prefer tree_sitter_languages
        if _get_language is not None:
            try:
                lang = _get_language(self.ts_key)
                p = Parser()
                p.set_language(lang)
                self.parser = p
                self.parser_source = f"tree-sitter-languages:{self.ts_key}"
                return
            except Exception as e:
                errors.append(f"tree_sitter_languages({self.ts_key}) failed: {e}")

        # 2) Fallback to language-specific package (we only try python)
        if self.language == "python" and _ts_python_language is not None:
            try:
                lang_ptr = _ts_python_language()
                p = Parser()
                p.set_language(lang_ptr)
                self.parser = p
                self.parser_source = "tree-sitter-python"
                return
            except Exception as e:
                errors.append(f"tree_sitter_python failed: {e}")

        # 3) Try local .so libraries
        try:
            # Compute repo root: rule_counter.py -> EBNF -> ml4setk -> src
            # parents[2] points to src/ml4setk
            ml4setk_dir = Path(__file__).resolve().parents[2]
            build_dir = ml4setk_dir / "TokenizationOffset" / "build"

            # Candidate .so filenames for each language
            so_candidates: Dict[str, List[str]] = {
                "python": ["python.so", "languages_python.so", "multilang_languages.so"],
                "javascript": ["javascript.so", "languages_javascript.so", "multilang_languages.so"],
                "typescript": ["typescript.so", "languages_typescript.so", "multilang_languages.so"],
                "java": ["java.so", "languages_java.so", "multilang_languages.so"],
                "go": ["go.so", "languages_go.so", "multilang_languages.so"],
                "cpp": ["cpp.so", "languages_cpp.so", "multilang_languages.so"],
                "c": ["c.so", "languages_c.so", "multilang_languages.so"],
                "csharp": ["csharp.so", "languages_csharp.so", "multilang_languages.so"],
                "rust": ["rust.so", "languages_rust.so", "multilang_languages.so"],
                "ruby": ["ruby.so", "languages_ruby.so", "multilang_languages.so"],
                "scala": ["scala.so", "languages_scala.so", "multilang_languages.so"],
            }

            # Possible embedded names in the library for csharp
            name_variants = [self.ts_key, self.language]
            if self.language == "csharp":
                name_variants.extend(["c_sharp", "csharp"])

            for fname in so_candidates.get(self.language, []):
                so_path = build_dir / fname
                if not so_path.exists():
                    continue
                for name_variant in name_variants:
                    try:
                        lang = Language(str(so_path), name_variant)
                        p = Parser()
                        p.set_language(lang)
                        self.parser = p
                        self.parser_source = f"local-so:{fname}:{name_variant}"
                        return
                    except Exception as e:
                        errors.append(f"{fname} ({name_variant}) failed: {e}")
        except Exception as e:
            errors.append(f"local .so discovery failed: {e}")

        # If we get here, initialization failed
        raise RuntimeError(
            f"Failed to initialize tree-sitter for language '{self.language}'. "
            + " | ".join(errors)
            + " | Hints: pip install 'tree-sitter-languages' or provide local .so in TokenizationOffset/build."
        )

    def _load_rule_mapping(self) -> None:
        """
        Optional mapping from node.type to normalized rule names.
        For most languages we use node.type directly.
        """
        if self.language == "python":
            self.rule_mapping = {
                # statements
                "module": "module",
                "expression_statement": "expression_statement",
                "assignment": "assignment",
                "augmented_assignment": "augmented_assignment",
                "return_statement": "return_statement",
                "import_statement": "import_statement",
                "import_from_statement": "import_from_statement",
                "if_statement": "if_statement",
                "for_statement": "for_statement",
                "while_statement": "while_statement",
                "try_statement": "try_statement",
                "with_statement": "with_statement",
                "function_definition": "function_definition",
                "class_definition": "class_definition",
                "decorated_definition": "decorated_definition",
                # expressions
                "binary_operator": "binary_operator",
                "unary_operator": "unary_operator",
                "boolean_operator": "boolean_operator",
                "comparison_operator": "comparison_operator",
                "call": "call",
                "attribute": "attribute",
                "subscript": "subscript",
                "list": "list",
                "tuple": "tuple",
                "dictionary": "dictionary",
                "set": "set",
                "list_comprehension": "list_comprehension",
                "dictionary_comprehension": "dictionary_comprehension",
                "set_comprehension": "set_comprehension",
                "generator_expression": "generator_expression",
                "lambda": "lambda",
                "conditional_expression": "conditional_expression",
                # literals & names
                "identifier": "identifier",
                "string": "string",
                "integer": "integer",
                "float": "float",
                "true": "true",
                "false": "false",
                "none": "none",
                # misc
                "parameters": "parameters",
                "argument_list": "argument_list",
                "keyword_argument": "keyword_argument",
                "comment": "comment",
                "block": "block",
                "pass_statement": "pass_statement",
                "break_statement": "break_statement",
                "continue_statement": "continue_statement",
                "global_statement": "global_statement",
                "nonlocal_statement": "nonlocal_statement",
                "assert_statement": "assert_statement",
                "delete_statement": "delete_statement",
                "raise_statement": "raise_statement",
                "yield": "yield",
                "await": "await",
            }
        else:
            # For other languages, default to node.type as rule name
            self.rule_mapping = {}

    def _traverse_tree(self, node, rule_counts: Counter) -> None:
        node_type = node.type
        rule_name = self.rule_mapping.get(node_type, node_type)
        rule_counts[rule_name] += 1
        for child in node.children:
            self._traverse_tree(child, rule_counts)

    def count_rules_in_code(self, code: str) -> Dict[str, int]:
        """
        Count rule occurrences via tree-sitter only.
        """
        if not code.strip():
            return {}
        if self.parser is None:
            raise RuntimeError("Tree-sitter parser is not initialized.")

        tree = self.parser.parse(code.encode("utf-8"))
        root = tree.root_node
        counts = Counter()
        self._traverse_tree(root, counts)
        return dict(counts)

    def count_rules_in_file(self, file_path: str) -> Dict[str, int]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            return self.count_rules_in_code(code)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return {}

    def count_rules_in_jsonl(self, jsonl_path: str, code_fields: List[str] | None = None) -> Dict[str, int]:
        if code_fields is None:
            code_fields = ["prompt", "canonical_solution"]

        total = Counter()
        try:
            with open(jsonl_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        data = json.loads(line)
                        code = "\n".join(str(data.get(k, "")) for k in code_fields if data.get(k))
                        if code.strip():
                            c = self.count_rules_in_code(code)
                            total.update(c)
                    except Exception as e:
                        print(f"[line {line_num}] error: {e}")
        except Exception as e:
            print(f"Error reading JSONL file {jsonl_path}: {e}")
        return dict(total)

    def save_counts_to_json(self, counts: Dict[str, int], output_path: str) -> None:
        try:
            out_dir = os.path.dirname(output_path)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)

            sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
            output_data = {
                "metadata": {
                    "language": self.language,
                    "total_rules": len(sorted_counts),
                    "total_occurrences": sum(sorted_counts.values()),
                    "parser_used": f"tree-sitter ({self.parser_source})",
                },
                "rule_counts": sorted_counts,
            }
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"Rule counts saved to: {output_path}")
        except Exception as e:
            print(f"Error saving counts to {output_path}: {e}")

    def print_summary(self, counts: Dict[str, int], top_n: int = 20) -> None:
        if not counts:
            print("No rules found.")
            return
        total_occurrences = sum(counts.values())
        total_rules = len(counts)
        print("\n=== Rule Count Summary ===")
        print(f"Language: {self.language}")
        print(f"Parser: tree-sitter ({self.parser_source})")
        print(f"Total unique rules: {total_rules}")
        print(f"Total rule occurrences: {total_occurrences}")
        print(f"\nTop {min(top_n, total_rules)} most frequent rules:")
        print("-" * 50)
        for i, (rule, cnt) in enumerate(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n], 1):
            pct = (cnt / total_occurrences) * 100
            print(f"{i:2d}. {rule:<30} {cnt:>6} ({pct:5.1f}%)")


def main():
    parser = argparse.ArgumentParser(description="Count EBNF grammar rules via tree-sitter (multi-language)")
    parser.add_argument("input", help="Input file path (source code or JSONL)")
    parser.add_argument("--output", "-o", default="rule_counts.json", help="Output JSON file")
    parser.add_argument("--language", "-l", default="python",
                        help="Language (python|javascript|typescript|java|go|cpp|c|csharp|rust|ruby|scala). Aliases: js, ts, c#, cs, golang, c++")
    parser.add_argument("--code-fields", nargs="+", default=["prompt", "canonical_solution"],
                        help="Fields for code in JSONL (default: prompt canonical_solution)")
    parser.add_argument("--top-n", type=int, default=20, help="Top N rules to print")
    args = parser.parse_args()

    counter = RuleCounter(language=args.language)
    in_path = Path(args.input)
    if not in_path.exists():
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    if in_path.suffix == ".jsonl":
        print(f"Processing JSONL file: {args.input}")
        counts = counter.count_rules_in_jsonl(args.input, args.code_fields)
    else:
        print(f"Processing source code file: {args.input}")
        counts = counter.count_rules_in_file(args.input)

    if counts:
        counter.print_summary(counts, args.top_n)
        counter.save_counts_to_json(counts, args.output)
    else:
        print("No rules were counted. Please check your input file.")


if __name__ == "__main__":
    main()