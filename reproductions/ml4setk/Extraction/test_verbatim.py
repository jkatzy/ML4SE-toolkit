"""Carlini et al., ICLR 2023, GPT-Neo-2.7B comparison in Section 6 (150-token context)."""

import hashlib
import os
from pathlib import Path
from zipfile import ZipFile

from ml4setk.Extraction import verify_suffixes


def test_known_suffix_rate():
    import numpy as np
    import torch
    from transformers import AutoModelForCausalLM

    path = Path(os.environ["ML4SETK_MEMORIZATION_ZIP"])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "6641751b281ea54294979e87bfdf9afe3cc6581fd89ae717e28b5741a3722a64"
    )
    with ZipFile(path) as archive:
        rows = np.load(archive.open("data/prompts_200.npy"), allow_pickle=False)
        counts = np.load(archive.open("data/counts_200.npy"), allow_pickle=False)
    # Authors sample blocks of 1,000 by duplication. Show both the nearest
    # block (median 105) and all examples with exactly 100 occurrences.
    block = np.arange(len(rows)) // 1000 == 22
    groups = {"nearest bucket": block & (counts > 0), "exactly 100": counts == 100}
    selected = np.flatnonzero(groups["nearest bucket"] | groups["exactly 100"])
    model = (
        AutoModelForCausalLM.from_pretrained(
            "EleutherAI/gpt-neo-2.7B", revision="e24fa291132763e59f4a5422741b424fb5d59056"
        )
        .eval()
        .to("cuda" if torch.cuda.is_available() else "cpu")
    )
    matches = np.zeros(len(rows), dtype=bool)
    for batch in np.array_split(selected, (len(selected) + 7) // 8):
        matches[batch] = verify_suffixes(rows[batch], prefix_length=150, model=model)
    assert verify_suffixes(rows[selected[:1]], prefix_length=150) == matches[selected[:1]].tolist()
    for label, mask in groups.items():
        print(f"{label}: {matches[mask].sum()} / {mask.sum()} = {matches[mask].mean():.6f}")
    assert groups["nearest bucket"].sum() == 999 and groups["exactly 100"].sum() == 66
    # One source row is missing. Bound the possible complete-block rate using both outcomes.
    matched = int(matches[groups["nearest bucket"]].sum())
    missing = int((block & (counts == 0)).sum())
    assert matched <= 0.536 * block.sum() <= matched + missing
