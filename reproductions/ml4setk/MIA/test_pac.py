"""Ye et al. (ACL 2024), Tables 1, 5, and 6 and the GPT-Neo panel in Figure 7."""

import json
import random
from bisect import bisect_left
from collections import Counter
from statistics import mean

import pytest
from paper_tolerance import within_one_percent

from ml4setk.MIA import evaluate_loss_scores, evaluate_pac_scores
from ml4setk.MIA.pac import _polarized_distance


def test_stackmia_table5():
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(
        "darklight03/StackMIAsub",
        "StackMIAsub.jsonl",
        repo_type="dataset",
        revision="c87c55d8b93fcf525fbf5fbf9b3bff6808b30ac6",
    )
    counts = Counter()
    with open(path, encoding="utf-8") as source:
        for line in source:
            row = json.loads(line)
            length = len(row["snippet"].split())
            assert length > 32 and row["label"] in (0, 1)
            bucket = (32, 64, 128, 256)[bisect_left((64, 128, 256), length)]
            counts[bucket, row["label"]] += 1
    for bucket, member, nonmember in [
        (32, 1596, 1615),
        (64, 1740, 1740),
        (128, 680, 720),
        (256, 90, 86),
    ]:
        print(f"Table 5, {bucket}: {counts[bucket, 1]} members, {counts[bucket, 0]} nonmembers")
        assert (counts[bucket, 1], counts[bucket, 0]) == (member, nonmember)


@pytest.fixture(scope="module")
def wikimia_cohort():
    import pandas as pd
    from huggingface_hub import hf_hub_download

    parts = []
    for length, suffix, member, nonmember in [
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
        frame = pd.read_parquet(path, columns=["input", "label"])
        assert len(frame) == member + nonmember and frame.input.notna().all()
        assert frame.label.value_counts().to_dict() == {1: member, 0: nonmember}
        parts.append(frame.assign(length_group=length))
    return pd.concat(parts, ignore_index=True)


def test_wikimia_table6(wikimia_cohort):
    assert wikimia_cohort.label.value_counts().to_dict() == {1: 861, 0: 789}


@pytest.fixture(scope="module")
def wikimia_areas(wikimia_cohort):
    """Score the pinned cohort for Table 1 and the length groups in Figure 7."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    cohort = wikimia_cohort
    name = "EleutherAI/gpt-neo-2.7B"
    rev = "e24fa291132763e59f4a5422741b424fb5d59056"
    tok = AutoTokenizer.from_pretrained(name, revision=rev)
    tok.pad_token = tok.eos_token
    model = (
        AutoModelForCausalLM.from_pretrained(name, revision=rev, torch_dtype=torch.float32)
        .eval()
        .to("cuda")
    )
    rng = random.Random(42)
    raw, negative_loss = [], []
    with torch.inference_mode():
        for text in cohort.input:
            words = text.split(" ")
            variants = [text]
            for _ in range(5):
                permutation = words.copy()
                for _ in range(max(1, int(0.3 * len(words)))):
                    a, b = rng.sample(range(len(words)), 2)
                    permutation[a], permutation[b] = permutation[b], permutation[a]
                variants.append(" ".join(permutation))
            batch = tok(variants, padding=True, return_tensors="pt").to("cuda")
            targets = batch.input_ids[:, 1:]
            logits = model(**batch, use_cache=False).logits[:, :-1]
            values = logits.log_softmax(-1).gather(2, targets.unsqueeze(-1)).squeeze(-1)
            gaps = []
            for i, (row, mask) in enumerate(zip(values, batch.attention_mask[:, 1:])):
                log_probs = row[mask.bool()].tolist()
                n = len(log_probs)
                gaps.append(
                    _polarized_distance(
                        log_probs, low_count=max(1, int(0.30 * n)), high_count=max(1, int(0.05 * n))
                    )
                )
                if i == 0:
                    negative_loss.append(mean(log_probs))
            raw.append(gaps[0] - mean(gaps[1:]))
    cohort = cohort.assign(pac=raw, loss=negative_loss)

    def areas(group):
        pos, neg = group[group.label == 1], group[group.label == 0]
        pac = evaluate_pac_scores(members=pos.pac, nonmembers=neg.pac).roc_auc
        loss = evaluate_loss_scores(members=pos.loss, nonmembers=neg.loss).roc_auc
        return pac, loss

    for length, group in cohort.groupby("length_group"):
        pac, loss = areas(group)
        print(f"Figure 7, GPT-Neo length {length}: PAC {pac:.9f}, PPL {loss:.9f}")
    pac, loss = areas(cohort)
    print(
        f"ACL Table 1, GPT-Neo, original WikiMIA: PAC {pac:.9f} (paper 0.666), "
        f"PPL {loss:.9f} (paper 0.616)"
    )
    return pac, loss


def test_acl_perplexity_control_and_pac_order(wikimia_areas):
    pac, loss = wikimia_areas
    assert within_one_percent(loss, 0.616), loss
    assert pac > loss


def test_acl_pac_table1_within_one_percent(wikimia_areas):
    pac, _ = wikimia_areas
    assert within_one_percent(pac, 0.666), pac
