"""Biderman et al., NeurIPS 2023. Read the index column from the pinned positive splits."""

import os
from pathlib import Path

import pytest

from ml4setk.Extraction import memorization_overlap, memorization_score

SIZES = ["70m", "160m", "410m", "1b", "1.4b", "2.8b", "6.9b"]
STEPS = [23000, 43000, 63000, 83000, 103000, 123000]
COMMON = 23000 * 1024
TOTAL = 143000 * 1024


def shards(split):
    paths = sorted(Path(os.environ["ML4SETK_PYTHIA_EVALS"]).glob(f"{split}-*.parquet"))
    assert paths and len(paths) == int(paths[0].name.split("-of-")[1][:5]), split
    return paths


def read_ids(split):
    import numpy as np
    import pyarrow.parquet as pq

    ids = np.concatenate(
        [pq.read_table(p, columns=["index"]).column(0).to_numpy() for p in shards(split)]
    )
    assert len(np.unique(ids)) == len(ids)
    return ids


def test_paper_examples():
    # Binary agreement masks transcribed from the four illustrations in Table 1.
    for mask, expected in [
        ("0110111101", 0.7),
        ("0000000000", 0.0),
        ("1110000000", 0.3),
        ("1111111111", 1.0),
    ]:
        assert memorization_score("1" * 10, mask) == expected


def test_released_checkpoints():
    for suite in ("duped", "deduped"):
        final = read_ids(f"{suite}.12b")
        final_common = final[final < COMMON]
        print(f"{suite},12b,rate,{len(final) / TOTAL:.8f},{len(final)}")
        for size in SIZES:
            ids = read_ids(f"{suite}.{size}")
            p, r = memorization_overlap(ids, final)
            cp, cr = memorization_overlap(ids[ids < COMMON], final_common)
            print(f"{suite},{size},scale,{p:.6f},{r:.6f},{cp:.6f},{cr:.6f},{len(ids)}")
        for step in STEPS:
            ids = read_ids(f"{suite}.12b.{step}")
            p, r = memorization_overlap(ids[ids < COMMON], final_common)
            print(f"{suite},{step},time,{p:.6f},{r:.6f}")


@pytest.mark.parametrize(
    ("name", "revision"),
    [
        ("EleutherAI/pythia-2.8b-v0", "b9d8cace80b1a97f5ed380711aea31f2d1b24310"),
        ("EleutherAI/pythia-2.8b", "2a259cdd96a4beb1cdf467512e3904197345f6a9"),
    ],
)
def test_pythia_checkpoint_on_released_positives(name, revision):
    """An independent positive control on the public 2.8B checkpoint."""
    import numpy as np
    import pyarrow.parquet as pq
    import torch
    from transformers import AutoModelForCausalLM

    from ml4setk.Extraction import verify_pythia_records

    model = (
        AutoModelForCausalLM.from_pretrained(name, revision=revision, torch_dtype=torch.float16)
        .eval()
        .to("cuda" if torch.cuda.is_available() else "cpu")
    )
    files = [pq.ParquetFile(p) for p in shards("duped.2.8b")]
    total = sum(f.metadata.num_rows for f in files)
    selected = np.sort(np.random.default_rng(19).choice(total, 128, replace=False))
    offset, flags = 0, []
    for part in files:
        for group in range(part.num_row_groups):
            end = offset + part.metadata.row_group(group).num_rows
            local = selected[(selected >= offset) & (selected < end)] - offset
            if len(local):
                rows = part.read_row_group(group, columns=["tokens"]).take(local).column(0)
                ids = [row.as_py()[:64] for row in rows]
                assert all(len(row) == 64 for row in ids)
                if not flags and name.endswith("-v0"):
                    assert verify_pythia_records(ids[:1]) == verify_pythia_records(
                        ids[:1], model=model
                    )
                flags.extend(verify_pythia_records(ids, model=model))
            offset = end
    print(f"{name} public positive control: {sum(flags)} / {len(flags)} verified")
    assert len(flags) == 128
    if name.endswith("-v0"):
        assert all(flags)


def test_table_two_6b_from_archived_confusion_matrices():
    import re
    import tarfile

    archive = Path(os.environ["ML4SETK_PYTHIA_ARTIFACT"])
    stages = ["23m", "44m", "65m", "85m", "105m", "126m"]
    published = [
        (0.919, 0.513),
        (0.913, 0.587),
        (0.910, 0.658),
        (0.910, 0.721),
        (0.915, 0.816),
        (0.945, 0.918),
    ]
    with tarfile.open(archive, "r:gz") as bundle:
        for stage, expected in zip(stages, published):
            suffix = (
                "predictable-memorization/graphs/memorization_early_checkpoint_predict_last_checkpoint/"
                f"graph_6.7b_{stage}.svg"
            )
            (entry,) = [name for name in bundle.getnames() if name.endswith(suffix)]
            svg = bundle.extractfile(entry).read().decode()
            tp, fn, fp, _ = map(float, re.findall(r"<!-- ([0-9.]+)% -->", svg))
            precision, recall = tp / (tp + fp), tp / (tp + fn)
            print(f"6.9b,{stage},svg,{precision:.6f},{recall:.6f}")
            assert (round(precision, 3), round(recall, 3)) == expected
