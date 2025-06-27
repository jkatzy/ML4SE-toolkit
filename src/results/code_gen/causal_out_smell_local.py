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
base_dir = "../../../data"

amount_method = 500
distances = [0, 1, -1]  # Distances for out-smell
version = "v1-ds100k"  # Version of the input-target dataset
output_dir_input_target = f"{base_dir}/input-target/{version}"
cases = [
    f"out_smell_distance(0)_{amount_method}",
    f"out_smell_distance(1)_{amount_method}",
    f"out_smell_distance(-1)_{amount_method}",
    f"no_smell_method_{amount_method}",
]

model_name = "SmolLM135M"
print(f"Using model: {model_name}")
checkpoint = "HuggingFaceTB/SmolLM2-135M"
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

def generate_completion_method(input: str, filename: str) -> str:
    inputs = tokenizer(input, return_tensors="pt").to(model.device)
    # Ensure the input does not exceed the available context
    if inputs["input_ids"].shape[1] > available_context_method:
        # Truncate the input to fit within the available context
        inputs["input_ids"] = inputs["input_ids"][:, -available_context_method:]
        print(f"Input truncated to fit within available context, file: {filename}")

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
    
output_dir_gen = f"{base_dir}/results/{model_name}/{version}"
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
            
            try:
                # Generate the completion
                pred = generate_completion_method(prefix, filename)
            except Exception as e:
                print(f"Error generating completion for {filename}: {e}")
                continue
            writer.writerow([filename, target, pred])
            file.flush()
            os.fsync(file.fileno())
        