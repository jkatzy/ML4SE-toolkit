import gzip
import json
import multiprocessing
import os
import shutil
import time
from pathlib import Path

import pytest

from ml4setk import ChunkedIterator, ChunkResult
from ml4setk.Datasets import read_rows


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


def make_chunks(root, count=3, rows_per_chunk=4):
    data = root / "data"
    data.mkdir()
    for chunk in range(count):
        rows = [{"id": chunk * rows_per_chunk + i, "text": f"x{i}"} for i in range(rows_per_chunk)]
        write_jsonl(data / f"part-{chunk}.jsonl", rows)
    return data


def double(row):
    return {"id": row["id"], "double": row["id"] * 2}


def read_output(paths):
    return [row for path in paths for row in read_rows(path)]


class FakeRemoteFileSystem:
    """fsspec-style filesystem that serves files from a local directory."""

    def __init__(self, root):
        self.root = root
        self.downloads = []

    def glob(self, pattern):
        return [str(path.relative_to(self.root)) for path in self.root.glob(pattern)]

    def get(self, remote, local):
        self.downloads.append(local)
        shutil.copyfile(self.root / remote, local)


@pytest.mark.unit
def test_processes_every_chunk_into_one_output_file_each(tmp_path):
    data = make_chunks(tmp_path)
    iterator = ChunkedIterator(str(data / "*.jsonl"), double, "run", tmp_path / "state")

    results = list(iterator)

    assert len(iterator) == 3
    assert [Path(result.chunk).name for result in results] == [
        "part-0.jsonl",
        "part-1.jsonl",
        "part-2.jsonl",
    ]
    assert all(isinstance(result, ChunkResult) for result in results)
    assert [(r.rows_read, r.rows_written) for r in results] == [(4, 4)] * 3
    assert iterator.output_files() == [result.output for result in results]
    assert [row["double"] for row in read_output(iterator.output_files())] == list(range(0, 24, 2))
    assert iterator.status() == {"total": 3, "done": 3, "claimed": 0, "pending": 0}
    assert list(iterator.claims_dir.iterdir()) == []


@pytest.mark.unit
def test_row_function_can_drop_rows_or_emit_several(tmp_path):
    data = make_chunks(tmp_path, count=1)

    def explode(row):
        if row["id"] % 2:
            return None
        return [{"id": row["id"], "part": part} for part in range(3)]

    [result] = list(ChunkedIterator([data / "part-0.jsonl"], explode, "run", tmp_path))

    assert (result.rows_read, result.rows_written) == (4, 6)
    assert [row["id"] for row in read_rows(result.output)] == [0, 0, 0, 2, 2, 2]


@pytest.mark.unit
def test_restart_skips_finished_chunks_and_retries_failed_one(tmp_path):
    data = make_chunks(tmp_path)
    calls = []

    def fail_on_chunk_one(row):
        calls.append(row["id"])
        if row["id"] == 5:
            raise RuntimeError("boom")
        return row

    first = ChunkedIterator(str(data / "*.jsonl"), fail_on_chunk_one, "run", tmp_path / "s")
    with pytest.raises(RuntimeError, match="boom"):
        list(first)
    assert first.status() == {"total": 3, "done": 1, "claimed": 0, "pending": 2}
    assert not any(first.output_dir.glob(".*.tmp"))

    calls.clear()
    second = ChunkedIterator(str(data / "*.jsonl"), double, "run", tmp_path / "s")
    results = list(second)

    assert [Path(result.chunk).name for result in results] == ["part-1.jsonl", "part-2.jsonl"]
    assert calls == []
    assert len(read_output(second.output_files())) == 12


@pytest.mark.unit
def test_stopping_early_releases_the_claim(tmp_path):
    data = make_chunks(tmp_path)
    iterator = ChunkedIterator(str(data / "*.jsonl"), double, "run", tmp_path / "s")

    for _ in iterator:
        break

    assert iterator.status() == {"total": 3, "done": 1, "claimed": 0, "pending": 2}


@pytest.mark.unit
def test_runs_are_kept_apart_by_name(tmp_path):
    data = make_chunks(tmp_path)
    one = ChunkedIterator(str(data / "*.jsonl"), double, "one", tmp_path / "s")
    two = ChunkedIterator(str(data / "*.jsonl"), lambda row: row, "two", tmp_path / "s")
    list(one)

    assert two.status()["done"] == 0
    assert len(list(two)) == 3
    assert "double" not in next(read_rows(two.output_files()[0]))


@pytest.mark.unit
def test_chunk_list_is_frozen_on_first_start(tmp_path):
    data = make_chunks(tmp_path)
    pattern = str(data / "*.jsonl")
    ChunkedIterator(pattern, double, "run", tmp_path / "s")
    write_jsonl(data / "part-9.jsonl", [{"id": 99}])

    assert len(ChunkedIterator(pattern, double, "run", tmp_path / "s")) == 3
    with pytest.raises(ValueError, match="different chunks"):
        ChunkedIterator([str(data / "part-9.jsonl")], double, "run", tmp_path / "s")


@pytest.mark.unit
def test_live_claims_are_skipped_and_stale_or_own_claims_are_taken(tmp_path):
    data = make_chunks(tmp_path)
    kwargs = {"state_dir": tmp_path / "s", "stale_after": 60}
    iterator = ChunkedIterator(str(data / "*.jsonl"), double, "run", worker_id="me", **kwargs)
    keys = [iterator._key(i, chunk) for i, chunk in enumerate(iterator.chunks)]

    live, stale, mine = (iterator._claim_path(key) for key in keys)
    live.write_text(json.dumps({"worker": "other"}))
    stale.write_text(json.dumps({"worker": "dead"}))
    old = time.time() - 120
    os.utime(stale, (old, old))
    mine.write_text(json.dumps({"worker": "me"}))

    assert iterator.status() == {"total": 3, "done": 0, "claimed": 2, "pending": 1}
    results = list(iterator)

    assert [Path(result.chunk).name for result in results] == ["part-1.jsonl", "part-2.jsonl"]
    assert live.exists()


@pytest.mark.unit
def test_half_written_claim_counts_as_live(tmp_path):
    data = make_chunks(tmp_path, count=1)
    iterator = ChunkedIterator(str(data / "*.jsonl"), double, "run", tmp_path / "s")
    iterator._claim_path(iterator._key(0, iterator.chunks[0])).write_text("")

    assert list(iterator) == []


@pytest.mark.unit
def test_claim_is_refreshed_while_a_long_chunk_runs(tmp_path):
    data = make_chunks(tmp_path, count=1)
    seen = []

    def slow(row):
        time.sleep(0.15)
        seen.append(iterator.status()["claimed"])
        return row

    iterator = ChunkedIterator(str(data / "*.jsonl"), slow, "run", tmp_path / "s", stale_after=0.4)
    list(iterator)

    assert seen == [1, 1, 1, 1]


@pytest.mark.unit
def test_remote_chunks_are_downloaded_to_scratch_and_removed(tmp_path):
    make_chunks(tmp_path)
    fs = FakeRemoteFileSystem(tmp_path)
    iterator = ChunkedIterator("data/*.jsonl", double, "run", tmp_path / "s", filesystem=fs)

    results = list(iterator)

    assert [result.chunk for result in results] == [f"data/part-{i}.jsonl" for i in range(3)]
    assert len(fs.downloads) == 3
    assert list(iterator.scratch_dir.iterdir()) == []


@pytest.mark.unit
def test_read_rows_handles_gzip_and_column_selection(tmp_path):
    path = tmp_path / "rows.jsonl.gz"
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        handle.write('{"a": 1, "b": 2}\n\n{"a": 3, "b": 4}\n')

    assert list(read_rows(path, columns=["a"])) == [{"a": 1}, {"a": 3}]
    with pytest.raises(ValueError, match="No default reader"):
        list(read_rows(tmp_path / "rows.csv"))


@pytest.mark.unit
@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"run_name": "a/b"}, "run_name"),
        ({"output_format": "csv"}, "output_format"),
        ({"stale_after": 0}, "stale_after"),
        ({"chunks": []}, "No chunks"),
    ],
)
def test_rejects_invalid_arguments(tmp_path, kwargs, message):
    arguments = {"chunks": ["x.jsonl"], "fn": double, "run_name": "run", "state_dir": tmp_path}
    arguments.update(kwargs)
    with pytest.raises(ValueError, match=message):
        ChunkedIterator(**arguments)


def _worker(pattern, state_dir, worker_id):
    iterator = ChunkedIterator(pattern, double, "shared", state_dir, worker_id=worker_id)
    return [result.chunk for result in iterator]


@pytest.mark.integration
def test_parallel_workers_split_chunks_without_overlap(tmp_path):
    data = make_chunks(tmp_path, count=12)
    pattern = str(data / "*.jsonl")
    ChunkedIterator(pattern, double, "shared", tmp_path / "s")

    with multiprocessing.get_context("spawn").Pool(4) as pool:
        processed = pool.starmap(_worker, [(pattern, tmp_path / "s", f"w{i}") for i in range(4)])

    chunks = [chunk for worker_chunks in processed for chunk in worker_chunks]
    assert sorted(chunks) == sorted(str(path) for path in data.glob("*.jsonl"))
    final = ChunkedIterator(pattern, double, "shared", tmp_path / "s")
    assert final.status()["done"] == 12
    assert sorted(row["id"] for row in read_output(final.output_files())) == list(range(48))


@pytest.mark.optional_dependency
def test_parquet_chunks_in_and_out(tmp_path):
    pa = pytest.importorskip("pyarrow")
    pq = pytest.importorskip("pyarrow.parquet")
    data = tmp_path / "data"
    data.mkdir()
    for chunk in range(2):
        ids = list(range(chunk * 1500, (chunk + 1) * 1500))
        pq.write_table(
            pa.table({"id": ids, "text": [str(i) for i in ids]}), data / f"{chunk}.parquet"
        )

    iterator = ChunkedIterator(
        str(data / "*.parquet"),
        lambda row: double(row) if row["id"] % 3 else None,
        "run",
        tmp_path / "s",
        output_format="parquet",
    )
    results = list(iterator)

    assert [result.rows_written for result in results] == [1000, 1000]
    table = pq.read_table(results[0].output)
    assert table.column_names == ["id", "double"]
    assert table.num_rows == 1000
    assert list(read_rows(data / "0.parquet", columns=["id"]))[:2] == [{"id": 0}, {"id": 1}]


@pytest.mark.optional_dependency
def test_parquet_output_of_empty_chunk(tmp_path):
    pq = pytest.importorskip("pyarrow.parquet")
    data = make_chunks(tmp_path, count=1)

    iterator = ChunkedIterator(
        str(data / "*.jsonl"), lambda row: None, "run", tmp_path / "s", output_format="parquet"
    )
    [result] = list(iterator)

    assert result.rows_written == 0
    assert pq.read_table(result.output).num_rows == 0
