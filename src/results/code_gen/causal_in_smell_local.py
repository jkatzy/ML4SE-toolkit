# Imports
from tqdm import tqdm
import os
import csv
from results.code_gen.code_gen_util import *
from ml4setk.Parsing.Code.TreeSitterQuery import TreeSitterQuery
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import StoppingCriteriaList
import torch
import math

language = "java"
tree_query = TreeSitterQuery(language=language)

amount_comment = 2000
version = "v2-ds-all-1"  # Version of the input-target dataset
output_dir_input_target = f"../../../data/input-target/{version}"
cases = [
    f"in_smell_{amount_comment}",
    f"no_smell_comment_{amount_comment}",
]

model_name = "SmolLM135M"
print(f"Using model: {model_name}")
checkpoint = "HuggingFaceTB/SmolLM2-135M"
device = "cuda" # cuda for GPU usage or "cpu" for CPU usage
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# for multiple GPUs install accelerate and do `model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")`
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

max_tokens_comment = math.ceil(load_threshold(f"comment_stats_all_{model_name}.json")["all"]["threshold"])
max_context = model.config.max_position_embeddings
if model_name == "SmolLM135M":
    max_context = 2048
print(f"Max context size: {max_context}")
available_context_comment = max_context - max_tokens_comment

def generate_completion_comment(input: str, comment_syntax: str, filename: str) -> str:
    inputs = tokenizer(input, return_tensors="pt", truncation=False).to(model.device)
    # Ensure the input does not exceed the available context
    if inputs["input_ids"].shape[1] > available_context_comment:
        # Truncate the input to fit within the available context
        inputs["input_ids"] = inputs["input_ids"][:, -available_context_comment:]
        print(f"Input truncated to fit within available context, file: {filename}")

    # Calculate where the generation starts (token-wise)
    start_len = inputs["input_ids"].shape[1]

    stopping_criteria = StoppingCriteriaList()

    # Choose appropriate stop tokens
    if comment_syntax.startswith("//"):
        stop_strings = ["\n"]
        stopping_criteria.append(StopOnSubstrings(stop_strings, tokenizer, start_len))
        stopping_criteria.append(RepetitionInSingleLineComment(tokenizer, start_len, filename))
    elif comment_syntax.startswith("/*") or comment_syntax.startswith("/**"):
        stop_strings = ["*/"]
        stopping_criteria.append(StopOnSubstrings(stop_strings, tokenizer, start_len))
        stopping_criteria.append(LineRepetitionStoppingCriteria(tokenizer, start_len, filename))

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=max_tokens_comment,
            pad_token_id=tokenizer.eos_token_id,
            stopping_criteria=stopping_criteria
        )

    generated_ids = outputs[0][start_len:]
    if generated_ids[-1].item() == tokenizer.eos_token_id:
        print("Last token is EOS, the generation was stopped by the model for file:", filename)
    completion = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    return completion
    
output_dir_gen = f"../../../data/results/{model_name}/{version}"
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
            comment_syntax = sample["comment_syntax"]
            
            try:
                # Generate the completion
                pred = generate_completion_comment(prefix, comment_syntax, filename)
            except Exception as e:
                print(f"Error generating completion for {filename}: {e}")
                continue
            writer.writerow([filename, target, pred])
            file.flush()
            os.fsync(file.fileno())
        