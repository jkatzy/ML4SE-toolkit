"""Model revisions and complete labeled cohorts for the FSE benchmark."""

import pandas as pd
import pyarrow.parquet as pq
from check_mia_reproduction import MODELS

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
