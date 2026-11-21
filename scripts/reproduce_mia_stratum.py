"""Regenerate scores for the FSE 2026 StarCoder2-3B Mid-Low Java stratum.

Koohestani et al., doi:10.1145/3803437.3805588. Fixed benchmark inputs and
published neighbors from doi:10.5281/zenodo.18348152. Prints aggregates only.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from statistics import mean

import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from ml4setk.MIA import evaluate_ast_pac_scores, evaluate_loss_scores, evaluate_pac_scores

EVALUATORS = {
    "loss": evaluate_loss_scores,
    "pac": evaluate_pac_scores,
    "pac_ast": evaluate_ast_pac_scores,
}
MODEL = "bigcode/starcoder2-3b"
REVISION = "733247c55e3f73af49ce8e9c7949bf14af205928"


def cohort(root):
    filters = [("alpha_bucket", "=", "Mid-Low"), ("type", "in", ["member", "non_member"])]
    results = root / "results/results_sc2_3b_new_approach_orig_m_worker_0.parquet"
    # Match the complete-row population used in the notebooks before projection.
    rows = pd.read_parquet(results, filters=filters).dropna()
    keys = ["id", "repo_name", "file_path", "type"]
    data = pd.read_parquet(
        root / "dataset/full.parquet", columns=[*keys, "content"], filters=filters
    )
    data["id"] = data["id"].astype(str)
    joined = rows.merge(data, on=keys, how="left", validate="one_to_one")
    if joined.content.isna().any() or joined.type.value_counts().to_dict() != {
        "member": 132,
        "non_member": 93,
    }:
        raise ValueError("Incomplete FSE comparison cohort")
    return joined


def polarized_gap(values):
    ordered = np.sort(values.astype(np.float64))
    length = len(ordered)
    low, high = min(30, length), min(5, length)
    scale = min(1.0, length / (low + high))
    return ordered[-max(1, int(high * scale)) :].mean() - ordered[: max(1, int(low * scale))].mean()


@torch.inference_mode()
def model_statistics(text, tokenizer, model, device, *, original):
    ids = tokenizer(text, truncation=True, max_length=8192, return_tensors="pt").input_ids.to(
        device
    )
    if ids.shape[1] < 2:
        raise ValueError("Missing next-token targets")
    logits = model(ids, use_cache=False).logits[0, :-1]
    targets = ids[0, 1:, None]
    # Chunk over positions to bound the vocabulary-sized intermediates.
    parts = []
    log_sum = 0.0
    for chunk, labels in zip(logits.split(256), targets.split(256)):
        logs = chunk.log_softmax(-1).gather(1, labels)
        parts.append(logs.flatten().cpu().numpy())
        if original:
            log_sum += chunk.float().log_softmax(-1).gather(1, labels).double().sum().item()
    return log_sum / len(targets), polarized_gap(np.concatenate(parts))


@torch.inference_mode()
def run_partition(rows, tokenizer, model, device):
    result = []
    for index, row in enumerate(rows.itertuples()):
        cache = {}
        variants = [row.pac_perturbed_samples, row.pac_ast_perturbed_samples]
        if any(len(group) != 5 for group in variants):
            raise ValueError("Expected five deposited neighbors per method")
        for text in [row.content, *variants[0], *variants[1]]:
            if text in cache:
                continue
            cache[text] = model_statistics(
                text, tokenizer, model, device, original=text == row.content
            )
        loss, original_gap = cache[row.content]
        result.append(
            (row.Index, loss, *(original_gap - mean(cache[t][1] for t in v) for v in variants))
        )
        if (index + 1) % 25 == 0:
            print(device, index + 1, "/", len(rows), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument(
        "--checkpoint", default=MODEL, help="Pinned Hub model or its local snapshot"
    )
    parser.add_argument("--gpus", type=int, choices=[1, 2], default=1)
    args = parser.parse_args()
    rows = cohort(args.artifact)
    with ThreadPoolExecutor(args.gpus) as pool:
        tokenizer = AutoTokenizer.from_pretrained(args.checkpoint, revision=REVISION)
        jobs = []
        for i in range(args.gpus):
            device = f"cuda:{i}"
            model = (
                AutoModelForCausalLM.from_pretrained(
                    args.checkpoint,
                    revision=REVISION,
                    torch_dtype=torch.float16,
                    attn_implementation="sdpa",
                )
                .eval()
                .to(device)
            )
            jobs.append(
                pool.submit(run_partition, rows.iloc[i :: args.gpus], tokenizer, model, device)
            )
        scores = pd.DataFrame(
            [r for job in jobs for r in job.result()], columns=["index", *EVALUATORS]
        ).set_index("index")
    member = rows.type == "member"
    for method, evaluate in EVALUATORS.items():
        fresh = scores[method].reindex(rows.index)
        recorded = rows[method + "_score"]
        for label, series in [("regenerated", fresh), ("archive", recorded)]:
            areas = evaluate(members=series[member], nonmembers=series[~member])
            print(method, label, f"ROC {areas.roc_auc:.9f} PR {areas.pr_auc:.9f}")
        delta = (fresh - recorded).abs()
        print(method, f"absolute score error: median {delta.median():.9f} max {delta.max():.9f}")


if __name__ == "__main__":
    main()
