# Imports
from tqdm import tqdm
import os
import csv
from results.code_gen.code_gen_util import *
from ml4setk.Parsing.Code.TreeSitterQuery import TreeSitterQuery
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import StoppingCriteriaList
import torch
import math

language = "java"
tree_query = TreeSitterQuery(language=language)

amount_method = 500
smell_index = -1  # Default to -1 for multiple out-smell cases
distances = [0, -1]  # Distances for out-smell
version = "v2-ds-all-1"  # Version of the input-target dataset
output_dir_input_target = f"/scratch/lcwitte/input-target/{version}"
cases = [
    f"multi({smell_index})_out_smell_distance({distances[0]})_{amount_method}",
    f"multi({smell_index})_out_smell_distance({distances[1]})_{amount_method}",
    f"preprocessed_multi({smell_index})_out_smell_distance({distances[0]})_{amount_method}",
    f"preprocessed_multi({smell_index})_out_smell_distance({distances[1]})_{amount_method}",
]

model_name = sys.argv[1]
print(f"Using model: {model_name}")
checkpoint = f"/scratch/lcwitte/models/{model_name}"
device = "cuda" # cuda for GPU usage or "cpu" for CPU usage
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# for multiple GPUs install accelerate and do `model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")`
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

max_tokens_method = math.ceil(load_threshold(f"method_stats_all_{model_name}.json")["method"]["threshold"])
max_context = model.config.max_position_embeddings
if model_name == "SmolLM135M":
    max_context = 2048
    max_tokens_method = math.ceil(load_threshold(f"method_stats_all_{model_name}.json")["method"]["mean"] + load_threshold(f"method_stats_all_{model_name}.json")["method"]["std"])
print(f"Max context size: {max_context}")
available_context_method = max_context - max_tokens_method

def generate_fim_completion_method(prefix: str, suffix: str, filename: str) -> str:
    fim_input_ids = get_fim_input_ids(tokenizer, prefix, suffix, available_context_method, filename).to(model.device)
    attention_mask = torch.ones_like(fim_input_ids)
    inputs = {
        "input_ids": fim_input_ids,
        "attention_mask": attention_mask
    }

    # Calculate where the generation starts (token-wise)
    start_len = inputs["input_ids"].shape[1]
    
    stopping_criteria = StoppingCriteriaList([
        StopOnMethodTreeSitter(tree_query, tokenizer, start_len),
        LineRepetitionStoppingCriteria(tokenizer, start_len, filename),
        RepetitionInLongSingleLine(tokenizer, start_len, filename)
    ])

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=max_tokens_method,
            pad_token_id=tokenizer.eos_token_id,
            stopping_criteria=stopping_criteria
        )

    generated_ids = outputs[0][start_len:]
    # Check if last token is end of text token
    if generated_ids[-1].item() == tokenizer.eos_token_id:
        print("Last token is EOS, the generation was stopped by the model for file:", filename)
    completion = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

    methods = tree_query.parse(completion, '(method_declaration) @method')
    if methods:
        method_code = methods[0][2].strip()
        return method_code
    else:
        return completion

output_dir_gen = f"/scratch/lcwitte/results/{model_name}/{version}/fim"
if not os.path.exists(output_dir_gen):
        os.makedirs(output_dir_gen, exist_ok=True)

for case in cases:
    samples = load_jsonl_gz(os.path.join(output_dir_input_target, f"{case}.jsonl.gz"))
    output_file_gen = f"{case}-{model_name}.csv"
    with open(os.path.join(output_dir_gen, output_file_gen), mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "target", "prediction"])

        for sample in tqdm(samples, desc=f"Processing {case} samples"):
            filename = sample["file_name"]
            prefix = sample["prefix"]
            target = sample["target"]
            suffix = sample["suffix"]
            
            try:
                # Generate the completion
                pred = generate_fim_completion_method(prefix, suffix, filename)
            except Exception as e:
                print(f"Error generating completion for {filename}: {e}")
                continue
            writer.writerow([filename, target, pred])
            file.flush()
            os.fsync(file.fileno())
        