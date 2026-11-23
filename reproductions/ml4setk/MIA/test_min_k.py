"""Shi et al. (ICLR 2024), original WikiMIA, Pythia-2.8B, Tables 1 and 5."""

from statistics import fmean

import pytest

from ml4setk.MIA import evaluate_membership_scores, min_k_score


@pytest.fixture(scope="module")
def pythia_original_wikimia():
    import pyarrow.parquet as pq
    import torch
    from huggingface_hub import hf_hub_download
    from sklearn.metrics import roc_curve
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_id = "EleutherAI/pythia-2.8b"
    revision = "2a259cdd96a4beb1cdf467512e3904197345f6a9"
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = (
        AutoModelForCausalLM.from_pretrained(model_id, revision=revision, torch_dtype=torch.float32)
        .to(device)
        .eval()
    )

    comparison = {}
    for length, suffix, n_members, n_nonmembers in [
        (32, "6d31a92f6d59bcdc", 387, 389),
        (64, "c337a02056685c1a", 284, 258),
        (128, "fff31bd5ed612836", 139, 111),
        (256, "e984cf40f6c5b556", 51, 31),
    ]:
        path = hf_hub_download(
            "swj0419/WikiMIA",
            f"data/WikiMIA_length{length}-00000-of-00001-{suffix}.parquet",
            repo_type="dataset",
            revision="a89ab76d88f704e9bc5870ac39cc9d458a2a70ac",
        )
        rows = pq.read_table(path, columns=["input", "label"]).to_pylist()
        labels = [row["label"] for row in rows]
        assert (labels.count(1), labels.count(0)) == (n_members, n_nonmembers)
        assert len(labels) == n_members + n_nonmembers
        scores = {"Min-K%": [], "PPL": []}
        with torch.inference_mode():
            for row in rows:
                ids = tokenizer(row["input"], return_tensors="pt").input_ids.to(device)
                logits = model(ids, use_cache=False).logits[:, :-1]
                observed = logits.log_softmax(-1).gather(-1, ids[:, 1:, None]).flatten().tolist()
                scores["Min-K%"].append(min_k_score(observed))
                scores["PPL"].append(fmean(observed))
        for method, values in scores.items():
            metrics = evaluate_membership_scores(
                members=(v for v, label in zip(values, labels) if label == 1),
                nonmembers=(v for v, label in zip(values, labels) if label == 0),
            )
            fpr, tpr, _ = roc_curve(labels, values, drop_intermediate=False)
            low_fpr_tpr = max(tpr[fpr < 0.05])
            print(
                f"{length} {method}: AUROC {metrics.roc_auc:.9f}, TPR@5%FPR {low_fpr_tpr:.9f}",
                flush=True,
            )
            if length == 128:
                comparison[method] = round(metrics.roc_auc, 2), round(100 * low_fpr_tpr, 1)

    return comparison


@pytest.mark.parametrize(
    ("method", "metric_index", "published"),
    [("Min-K%", 0, 0.67), ("Min-K%", 1, 13.7), ("PPL", 0, 0.61), ("PPL", 1, 9.4)],
    ids=["min-k-table1-auc", "min-k-table5-tpr", "ppl-table1-auc", "ppl-table5-tpr"],
)
def test_published_pythia_result(pythia_original_wikimia, method, metric_index, published):
    assert pythia_original_wikimia[method][metric_index] == published
