"""Validate the public API on the three published FSE benchmark rows.

Koohestani et al., doi:10.1145/3803437.3805588. Requires the pinned inputs and
the external Java augmentation module from doi:10.5281/zenodo.18348152.
"""

import argparse
import hashlib
import math
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import torch
from check_mia_reproduction import archived_strata
from fse_scoring import BenchmarkScorer, token_neighbors
from reproduce_mia_stratum import EVALUATORS, MODEL, REVISION
from sklearn.metrics import auc, precision_recall_curve, roc_auc_score
from transformers import AutoModelForCausalLM, AutoTokenizer

from ml4setk.MIA import evaluate_membership_scores


def corpus(root):
    frame = pd.read_parquet(
        root / "dataset/full.parquet",
        columns=["id", "content", "type"],
        filters=[("alpha_bucket", "=", "Mid-Low"), ("type", "in", ["member", "non_member"])],
    )
    if frame.type.value_counts().to_dict() != {"member": 132, "non_member": 93}:
        raise ValueError("Unexpected FSE cohort")
    if frame.content.isna().any() or not frame.id.is_unique:
        raise ValueError("Missing source or duplicate IDs in FSE comparison")
    return frame


def run_partition(rows, neighbors, tokenizer, model, device):
    output = {}
    for method in EVALUATORS:
        scorer = BenchmarkScorer(method, neighbors[method], tokenizer, device)
        output[method] = scorer.score_many(model, rows.content)
        print(device, method, len(rows), "files scored", flush=True)
    return pd.DataFrame(output, index=rows.index)


def compare(root, rows, scores):
    positive = rows.type == "member"
    if not scores.index.is_unique or set(scores.index) != set(rows.index):
        raise ValueError("Incomplete API outputs")
    for method, evaluate_raw in EVALUATORS.items():
        series = scores[method].reindex(rows.index)
        joint = evaluate_membership_scores(members=series[positive], nonmembers=series[~positive])
        raw = series if method == "loss" else -series
        specific = evaluate_raw(members=raw[positive], nonmembers=raw[~positive])
        precision, recall, _ = precision_recall_curve(positive, series)
        oracle = [roc_auc_score(positive, series), auc(recall, precision)]
        if joint != specific or (joint.n_members, joint.n_nonmembers) != (132, 93):
            raise AssertionError(f"{method} API agreement or cohort counts failed")
        estimates = [joint.roc_auc, joint.pr_auc]
        if not all(math.isclose(a, b, rel_tol=0, abs_tol=1e-12) for a, b in zip(estimates, oracle)):
            raise AssertionError(f"{method} differs from independent metric implementation")
        rq = "RQ3" if method == "pac_ast" else "RQ2"
        table = root / "analysis" / rq / f"{rq.lower()}_table_ME_vs_NM.tex"
        reference = dict(archived_strata(table))["SC2-3B", method, "alpha_bucket", "Mid-Low"]
        for name, actual, check, target in zip(["ROC-AUC", "PR-AUC"], estimates, oracle, reference):
            print(
                method,
                name,
                f"joint={actual:.9f} sklearn={check:.9f} published={target}",
                "MATCH" if f"{actual:.3f}" == target else "DIFFERENT",
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--checkpoint", default=MODEL)
    parser.add_argument("--gpus", type=int, choices=[1, 2], default=1)
    args = parser.parse_args()
    sys.path.insert(0, str(args.artifact.resolve()))
    from attacks.pac_ast_attack import TS_AVAILABLE, generate_adjacent_samples_ts

    if not TS_AVAILABLE:
        raise RuntimeError("The FSE Java parser is required")
    rows = corpus(args.artifact)
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint, revision=REVISION)
    neighbors = {method: {} for method in EVALUATORS}
    for row in rows.itertuples():
        # Identical sources receive the same draws regardless of GPU assignment.
        seed = int.from_bytes(hashlib.sha256(row.content.encode()).digest()[:8], "big")
        neighbors["loss"][row.content] = ()
        neighbors["pac"][row.content] = token_neighbors(row.content, tokenizer, seed)
        neighbors["pac_ast"][row.content] = generate_adjacent_samples_ts(
            row.content, tokenizer, seed=seed
        )
    for method in ["pac", "pac_ast"]:
        groups = [neighbors[method][text] for text in rows.content]
        if any(len(group) != 5 for group in groups):
            raise ValueError(f"Incomplete {method} perturbation group")
        changed = sum(
            variant != text for text, group in zip(rows.content, groups) for variant in group
        )
        print(method, changed, "changed neighbors out of", 5 * len(groups), flush=True)
    with ThreadPoolExecutor(args.gpus) as pool:
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
                pool.submit(
                    run_partition, rows.iloc[i :: args.gpus], neighbors, tokenizer, model, device
                )
            )
        scores = pd.concat(job.result() for job in jobs)
    compare(args.artifact, rows, scores)


if __name__ == "__main__":
    main()
