"""Score the complete labeled FSE 2026 cohorts through the shared ML4SETK API.

Uses result-file missingness and metadata to select the published cohorts. Each SQLite batch
contains freshly derived quantities and is committed after all three methods.
"""

import argparse
import hashlib
import json
import sqlite3
import sys
import time
from pathlib import Path
from statistics import mean

import pandas as pd
import pyarrow.parquet as pq
import torch
from check_mia_reproduction import MODELS
from Levenshtein import ratio
from transformers import AutoModelForCausalLM, AutoTokenizer
from validate_mia_api import EVALUATORS, BenchmarkScorer, token_neighbors

SNAPSHOTS = {
    "SC2-3B": ("bigcode/starcoder2-3b", "733247c55e3f73af49ce8e9c7949bf14af205928"),
    "SC2-7B": ("bigcode/starcoder2-7b", "bb9afde76d7945da5745592525db122d4d729eb1"),
    "mellum": ("JetBrains/Mellum-4b-base", "83cce2605fbdf6a3868627e9b0a5924e0072b94d"),
    "smollm": ("HuggingFaceTB/SmolLM3-3B", "a07cc9a04f16550a088caea529712d1d335b0ac1"),
}
KEYS = ["id", "type", "repo_name", "file_path"]
BUCKETS = ["alpha_bucket", "size_bucket", "complexity_bucket"]


def complete_cases(root, model):
    slug = MODELS[model]
    archive = pq.ParquetFile(
        root / "results" / f"results_{slug}_new_approach_orig_m_worker_0.parquet"
    )
    # The notebook drops any row with a missing column. Use validity masks only.
    parts = []
    for batch in archive.iter_batches(batch_size=256):
        frame = batch.to_pandas()
        parts.append(frame.loc[frame.notna().all(axis=1), KEYS + BUCKETS])
    meta = pd.concat(parts, ignore_index=True)
    data = pd.read_parquet(root / "dataset/full.parquet", columns=[*KEYS, "content"])
    data["id"] = data.id.astype(str)
    rows = meta.merge(data, on=KEYS, how="left", validate="one_to_one")
    if rows.content.isna().any() or rows.type.value_counts().to_dict() != {
        "member": 4193,
        "member_near": 4014,
        "non_member": 4215,
    }:
        raise ValueError("Incomplete FSE model cohort")
    return rows


def open_run(path, stamp):
    db = sqlite3.connect(path, timeout=90)
    db.execute("PRAGMA journal_mode=WAL")
    with db:
        db.execute("CREATE TABLE IF NOT EXISTS metadata (id INTEGER PRIMARY KEY, stamp TEXT)")
        db.execute(
            "INSERT OR IGNORE INTO metadata VALUES (1, ?)", (json.dumps(stamp, sort_keys=True),)
        )
        if json.loads(db.execute("SELECT stamp FROM metadata WHERE id=1").fetchone()[0]) != stamp:
            raise ValueError("Existing results belong to a different run")
        db.execute("""CREATE TABLE IF NOT EXISTS fresh (
            row_id INTEGER PRIMARY KEY, loss REAL NOT NULL, pac REAL NOT NULL,
            pac_ast REAL NOT NULL, pac_change_ratio REAL NOT NULL,
            pac_ast_change_ratio REAL NOT NULL
        )""")
    return db


def measure(rows, tokenizer, model, device, ast_neighbors):
    neighbors = {method: {} for method in EVALUATORS}
    changes = {}
    for text in rows.content:
        seed = int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")
        neighbors["loss"][text] = ()
        neighbors["pac"][text] = token_neighbors(text, tokenizer, seed)
        neighbors["pac_ast"][text] = ast_neighbors(text, tokenizer, seed=seed)
        for method in ("pac", "pac_ast"):
            variants = neighbors[method][text]
            if len(variants) != 5:
                raise ValueError("Expected five generated neighbors")
            changes[text, method] = mean(1 - ratio(text, v) for v in variants)
    scores = {}
    original_stats = {}
    for method in EVALUATORS:
        scorer = BenchmarkScorer(method, neighbors[method], tokenizer, device, original_stats)
        scores[method] = scorer.score_many(model, rows.content)
    return [
        (
            int(idx),
            scores["loss"][i],
            scores["pac"][i],
            scores["pac_ast"][i],
            changes[text, "pac"],
            changes[text, "pac_ast"],
        )
        for i, (idx, text) in enumerate(rows.content.items())
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("output", type=Path, help="Persistent, untracked directory for this run")
    parser.add_argument("model", choices=SNAPSHOTS)
    parser.add_argument("--checkpoint", help="Local snapshot of the specified pinned model")
    parser.add_argument("--shards", type=int, default=1)
    parser.add_argument("--shard", type=int, default=0)
    args = parser.parse_args()
    if not 0 <= args.shard < args.shards:
        parser.error("Require 0 <= shard < shards")
    sys.path.insert(0, str(args.artifact.resolve()))
    from attacks.pac_ast_attack import TS_AVAILABLE, generate_adjacent_samples_ts

    if not TS_AVAILABLE:
        raise RuntimeError("Java tree-sitter unavailable")
    # The published Java traversal is recursive. The corpus contains ASTs
    # deeper than Python's default limit (maximum named-node depth 1,506).
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 4096))
    rows = complete_cases(args.artifact, args.model)
    name, revision = SNAPSHOTS[args.model]
    cohort_hash = hashlib.sha256(pd.util.hash_pandas_object(rows).values.tobytes()).hexdigest()
    stamp = dict(model=name, revision=revision, cohort=cohort_hash, protocol=1)
    args.output.mkdir(parents=True, exist_ok=True)
    db = open_run(args.output / f"{MODELS[args.model]}.sqlite", stamp)
    done = {r[0] for r in db.execute("SELECT row_id FROM fresh")}
    rows = rows.iloc[args.shard :: args.shards]
    rows = rows.loc[~rows.index.isin(done)]
    if rows.empty:
        return
    checkpoint = args.checkpoint or name
    tokenizer = AutoTokenizer.from_pretrained(checkpoint, revision=revision)
    device = "cuda:0"
    model = (
        AutoModelForCausalLM.from_pretrained(
            checkpoint, revision=revision, torch_dtype=torch.float16, attn_implementation="sdpa"
        )
        .eval()
        .to(device)
    )
    start = time.monotonic()
    for offset in range(0, len(rows), 8):
        batch = rows.iloc[offset : offset + 8]
        values = measure(batch, tokenizer, model, device, generate_adjacent_samples_ts)
        with db:
            db.executemany("INSERT INTO fresh VALUES (?,?,?,?,?,?)", values)
        if offset % 128 == 0 or offset + 8 >= len(rows):
            print(
                args.model,
                offset + len(batch),
                "/",
                len(rows),
                f"{time.monotonic() - start:.1f}s",
                flush=True,
            )
    db.close()


if __name__ == "__main__":
    main()
