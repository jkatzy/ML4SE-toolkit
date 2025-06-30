from datasets import load_from_disk
import numpy as np
from tqdm import tqdm
import json
from ml4setk.Parsing.Code.TreeSitterQuery import TreeSitterQuery
from transformers import AutoTokenizer
import os

# Load local dataset
ds = load_from_disk(f"/scratch/lcwitte/the_heap/HeapJava")
print(len(ds))

# Ensure the directory exists
output_dir = "/scratch/lcwitte/results/mean-2std-all"
os.makedirs(output_dir, exist_ok=True)

def save_threshold(stats, filepath):
    with open(os.path.join(output_dir, filepath), "w") as f:
        json.dump(stats, f, indent=4)

# Tokenizer and model setup
checkpoint_smol = "/scratch/lcwitte/models/SmolLM135M"
checkpoint_star = "/scratch/lcwitte/models/StarCoder2_3B"
checkpoint_mellum = "/scratch/lcwitte/models/MellumBase4B"
tokenizer_smol = AutoTokenizer.from_pretrained(checkpoint_smol)
tokenizer_star = AutoTokenizer.from_pretrained(checkpoint_star)
tokenizer_mellum = AutoTokenizer.from_pretrained(checkpoint_mellum)

# Define models and their tokenizers
models = {
    "SmolLM135M": tokenizer_smol,
    "StarCoder2_3B": tokenizer_star,
    "MellumBase4B": tokenizer_mellum,
}

language = 'Java'
tree_query = TreeSitterQuery(language=language.lower())

def calculate_stats(lengths):
    """
    Calculate mean, standard deviation, and threshold for a list of lengths.
    """
    mean_len = np.mean(lengths)
    std_len = np.std(lengths)
    threshold = mean_len + 2 * std_len
    return mean_len, std_len, threshold

def get_method_stats(dataset):
    lengths = {}
    for model_name, _ in models.items():
        lengths[model_name] = {
            "method": []
        }

    for file in tqdm(dataset, miniters=10000, maxinterval=float('inf'), desc="Processing comments"):
        content = file["content"]

        # Parse methods
        methods = tree_query.parse(content, '(method_declaration) @decl')
        for (_, _, method) in methods:
            for model_name, tokenizer in models.items():
                len_tokens = len(tokenizer(method, return_tensors="pt")["input_ids"][0])
                lengths[model_name]["method"].append(len_tokens)

    results = {}
    for model_name, _ in models.items():
        method_mean, method_std, method_threshold = calculate_stats(lengths[model_name]["method"])

        results[model_name] = {
            "method": {
                "mean": method_mean,
                "std": method_std,
                "threshold": method_threshold
            }
        }
    return results

# Get stats for methods
method_stats = get_method_stats(ds)

# Save the stats to separate files
for model_name, stats in method_stats.items():
    save_threshold(stats, f"method_stats_all_{model_name}.json")

