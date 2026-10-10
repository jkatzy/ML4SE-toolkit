# Chunked datasets

Large code corpora such as The Stack v1, v2 and v3 are published as thousands
of separate files. `ChunkedIterator` treats each file as one chunk: it fetches a
chunk, applies your function to every row, writes the results to one output file
for that chunk, and moves on. You never need the whole dataset on disk, and the
output is a new dataset split the same way as the input.

Progress is stored on disk under a run name, so a run survives restarts and any
number of workers, on one machine or several sharing a filesystem, can process
the same run at the same time or one after another.

```bash
pip install "ml4setk[datasets]"   # pyarrow for Parquet, huggingface_hub for the Hub
```

Local JSON Lines input and output need no extra.

## Quick start

```python
from huggingface_hub import HfFileSystem
from ml4setk import ChunkedIterator, CommentQuery

query = CommentQuery("python")

def comments(row):
    return [{"path": row["path"], "comment": m.match} for m in query.parse(row["content"])]

iterator = ChunkedIterator(
    "datasets/bigcode/the-stack/data/python/*.parquet",
    comments,
    run_name="stack-v1-python-comments",
    state_dir="runs",
    filesystem=HfFileSystem(),  # uses HF_TOKEN for gated datasets
)

for result in iterator:
    print(result.chunk, result.rows_read, result.rows_written)
```

Run the same script in more terminals, jobs or machines to add workers. Each one
picks up chunks nobody else has taken. Stop any of them and start it again; it
skips the chunks that are already done.

A runnable version that needs no network is in
[`examples/chunked_iterator.py`](https://github.com/jkatzy/ML4SE-toolkit/blob/main/examples/chunked_iterator.py).

## How it works

A run lives in `state_dir/run_name/`:

| Path | Contents |
| --- | --- |
| `run.json` | The chunk list, resolved once when the run starts. |
| `claims/<key>.claim` | One file per chunk a worker is processing right now. |
| `done/<key>.json` | One marker per finished chunk, with row counts and the worker id. |
| `output/<key>.jsonl` or `.parquet` | The output of each finished chunk. |
| `scratch/` | Remote chunks while they are being processed. |

`<key>` is the chunk's position in the list followed by a short hash of its
path, so output files sort in input order.

1. The first worker to start a run lists the chunks (a glob on the filesystem or
   your explicit list) and saves them to `run.json`. Every later worker reads
   that file, so all workers agree on the chunks without listing the remote
   repository again. Starting an existing run with a different `chunks`
   argument raises `ValueError`; pick a new `run_name` instead.
2. For each chunk in order, a worker skips it if a `done` marker exists, then
   claims it by creating its claim file atomically. If the file already exists,
   another worker has it and this worker moves on.
3. The worker downloads the chunk to `scratch/` (remote filesystems only), reads
   its rows, calls your function on each row, and streams the results to a
   temporary output file. While it works, it refreshes the claim file's
   modification time.
4. When the chunk is finished, the temporary file is renamed to its final name,
   the `done` marker is written, and the claim and downloaded chunk are deleted.

A chunk is the unit of restart. If a worker stops mid-chunk, or your function
raises, the chunk has no `done` marker and is processed again from its first
row. If your function raises, the error propagates and the claim is released
right away. If a worker is killed, its claim stays behind until it is older
than `stale_after` seconds (default 600), after which any worker may take it
over. A worker started again with the same `worker_id` takes back its own
claims immediately, which is useful with job schedulers that reuse an index.

Claims prevent duplicate work; they do not need to be perfect. In the rare case
that a worker stalls past `stale_after` and another takes over its chunk, both
write the same output and the final rename keeps one copy.

## API

### `ChunkedIterator`

```python
ChunkedIterator(
    chunks,
    fn,
    run_name,
    state_dir="runs",
    *,
    filesystem=None,
    reader=read_rows,
    output_format="jsonl",
    worker_id=None,
    stale_after=600.0,
)
```

| Argument | Meaning |
| --- | --- |
| `chunks` | A glob pattern, or a list of file paths, one per chunk. |
| `fn` | Called with each row as a `dict`. Return a `dict` to write one row, a list of dicts to write several, or `None` to drop the row. |
| `run_name` | Separates runs under the same `state_dir`. Letters, digits, `.`, `_` and `-`. |
| `state_dir` | Where run state and outputs are stored. All workers of a run must share it. |
| `filesystem` | `None` reads local files in place. Any object with fsspec-style `glob(pattern)` and `get(remote, local)`, such as `huggingface_hub.HfFileSystem` or an `s3fs.S3FileSystem`, makes chunks remote. |
| `reader` | Turns a local chunk path into rows. Defaults to `read_rows`. |
| `output_format` | `"jsonl"` (no extra needed) or `"parquet"`. |
| `worker_id` | Identifies this worker in claims and `done` markers. Defaults to host name, process id and a random suffix. |
| `stale_after` | Seconds after which an unrefreshed claim counts as abandoned. |

Iterating yields a `ChunkResult(chunk, output, rows_read, rows_written)` for
each chunk this worker finished, and stops when no unclaimed chunks are left.
Breaking out of the loop releases the current claim.

| Method | Returns |
| --- | --- |
| `len(iterator)` | The number of chunks in the run. |
| `status()` | `{"total", "done", "claimed", "pending"}` counts across all workers. |
| `output_files()` | Output paths of finished chunks, in chunk order. |

### `read_rows(path, columns=None)`

Yields the rows of a `.parquet`, `.jsonl`, `.jsonl.gz` or `.json.gz` file as
dicts. `columns` keeps only the named fields; for Parquet it also avoids
reading the other columns. Pass your own reader for other formats, or to select
columns:

```python
from functools import partial
from ml4setk.Datasets import read_rows

reader = partial(read_rows, columns=["blob_id", "path", "language"])
```

## Using the output

Each output file is a split of the new dataset. Load them together with
Hugging Face `datasets`:

```python
from datasets import load_dataset

files = [str(path) for path in iterator.output_files()]
dataset = load_dataset("json", data_files=files, split="train")  # "parquet" for Parquet output
```

## Dataset recipes

The Stack v1 and The Stack v2 are Hugging Face dataset repositories whose
`data/<language>/` folders hold Parquet files. The Stack v3 is a Hugging Face
storage bucket, which `HfFileSystem` exposes under `buckets/`.

```python
from huggingface_hub import HfFileSystem

fs = HfFileSystem()
stack_v1 = "datasets/bigcode/the-stack/data/python/*.parquet"
stack_v2 = "datasets/bigcode/the-stack-v2/data/Python/*.parquet"
stack_v3 = "buckets/HuggingFaceCode/stack-v3-full/contents/language=Python/*.parquet"
```

The Stack v2 rows carry only metadata; the file contents live in the Software
Heritage S3 bucket under `content/<blob_id>`. Fetch them inside your function:

```python
import gzip

import boto3
from botocore import UNSIGNED
from botocore.config import Config

s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))

def with_content(row):
    obj = s3.get_object(Bucket="softwareheritage", Key=f"content/{row['blob_id']}")
    text = gzip.decompress(obj["Body"].read()).decode(row["src_encoding"])
    return {"blob_id": row["blob_id"], "comments": [m.match for m in query.parse(text)]}
```
