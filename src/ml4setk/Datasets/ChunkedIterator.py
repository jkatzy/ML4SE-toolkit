"""
Restartable, multi-worker iteration over datasets stored as many files.

Each file of a dataset is one chunk. A ``ChunkedIterator`` applies a row
function to every row of a chunk and writes the results to one output file per
chunk. Progress lives on disk under ``state_dir/run_name``, so a run survives
restarts and any number of workers can share it.
"""

from __future__ import annotations

import glob
import gzip
import hashlib
import json
import os
import re
import socket
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Optional, Sequence, Union

Row = dict
RowFunction = Callable[[Row], Union[Row, Iterable[Row], None]]

_OUTPUT_FORMATS = {"jsonl": ".jsonl", "parquet": ".parquet"}
_PARQUET_BATCH_ROWS = 1024


@dataclass(frozen=True)
class ChunkResult:
    """Outcome of one chunk processed by this worker."""

    chunk: str
    output: Path
    rows_read: int
    rows_written: int


def read_rows(path: Union[str, Path], columns: Optional[Sequence[str]] = None) -> Iterator[Row]:
    """Yield the rows of a ``.parquet``, ``.jsonl``, ``.jsonl.gz`` or ``.json.gz`` file."""
    path = Path(path)
    name = path.name.lower()
    if name.endswith(".parquet"):
        pq = _import_pyarrow_parquet()
        parquet_file = pq.ParquetFile(path)
        for batch in parquet_file.iter_batches(columns=columns):
            yield from batch.to_pylist()
        return
    if name.endswith((".jsonl", ".jsonl.gz", ".json.gz")):
        opener = gzip.open if name.endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    row = json.loads(line)
                    yield {key: row.get(key) for key in columns} if columns else row
        return
    raise ValueError(f"No default reader for {path.name}; pass reader= to ChunkedIterator.")


class ChunkedIterator:
    """Apply ``fn`` to every row of a file-chunked dataset, one chunk at a time.

    ``chunks`` is a glob pattern or an explicit list of file paths. With
    ``filesystem=None`` they are local files, read in place. Any object with
    fsspec-style ``glob(pattern)`` and ``get(remote, local)`` methods, such as
    ``huggingface_hub.HfFileSystem``, makes them remote: each chunk is downloaded
    to the run's scratch directory, processed, and deleted.

    Iterating processes every chunk that is neither done nor claimed by a live
    worker and yields a ``ChunkResult`` for each one this worker finished.
    """

    def __init__(
        self,
        chunks: Union[str, Sequence[Union[str, Path]]],
        fn: RowFunction,
        run_name: str,
        state_dir: Union[str, Path] = "runs",
        *,
        filesystem: Any = None,
        reader: Callable[[Path], Iterable[Row]] = read_rows,
        output_format: str = "jsonl",
        worker_id: Optional[str] = None,
        stale_after: float = 600.0,
    ):
        if not run_name or not re.fullmatch(r"[A-Za-z0-9._-]+", run_name):
            raise ValueError(
                "run_name must be non-empty and use only letters, digits, '.', '_', '-'."
            )
        if output_format not in _OUTPUT_FORMATS:
            raise ValueError(f"output_format must be one of {sorted(_OUTPUT_FORMATS)}.")
        if stale_after <= 0:
            raise ValueError("stale_after must be positive.")

        self.fn = fn
        self.run_name = run_name
        self.filesystem = filesystem
        self.reader = reader
        self.output_format = output_format
        self.worker_id = worker_id or f"{socket.gethostname()}-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        self.stale_after = stale_after

        self.run_dir = Path(state_dir) / run_name
        self.claims_dir = self.run_dir / "claims"
        self.done_dir = self.run_dir / "done"
        self.output_dir = self.run_dir / "output"
        self.scratch_dir = self.run_dir / "scratch"
        for directory in (self.claims_dir, self.done_dir, self.output_dir, self.scratch_dir):
            directory.mkdir(parents=True, exist_ok=True)

        self.chunks = self._load_or_list_chunks(chunks)

    def __len__(self) -> int:
        return len(self.chunks)

    def __iter__(self) -> Iterator[ChunkResult]:
        for index, chunk in enumerate(self.chunks):
            key = self._key(index, chunk)
            if self._is_done(key) or not self._claim(key):
                continue
            try:
                # Another worker may have finished between the check and the claim.
                if self._is_done(key):
                    continue
                yield self._process(key, chunk)
            finally:
                self._claim_path(key).unlink(missing_ok=True)

    def status(self) -> dict:
        """Count chunks that are done, claimed by a live worker, or pending."""
        done = claimed = 0
        for index, chunk in enumerate(self.chunks):
            key = self._key(index, chunk)
            if self._is_done(key):
                done += 1
            elif self._live_claim_exists(key):
                claimed += 1
        return {
            "total": len(self.chunks),
            "done": done,
            "claimed": claimed,
            "pending": len(self.chunks) - done - claimed,
        }

    def output_files(self) -> list:
        """Output files of finished chunks, in chunk order."""
        files = []
        for index, chunk in enumerate(self.chunks):
            key = self._key(index, chunk)
            if self._is_done(key):
                files.append(self._output_path(key))
        return files

    def _load_or_list_chunks(self, spec: Union[str, Sequence[Union[str, Path]]]) -> list:
        spec = spec if isinstance(spec, str) else [str(path) for path in spec]
        manifest = self.run_dir / "run.json"
        if manifest.exists():
            saved = json.loads(manifest.read_text(encoding="utf-8"))
            if saved["spec"] != spec:
                raise ValueError(
                    f"Run '{self.run_name}' already exists with different chunks; "
                    "use a new run_name."
                )
            return saved["chunks"]

        if isinstance(spec, str):
            listed = self.filesystem.glob(spec) if self.filesystem else glob.glob(spec)
            chunks = sorted(str(path) for path in listed)
        else:
            chunks = spec
        if not chunks:
            raise ValueError(f"No chunks found for {spec!r}.")
        _write_atomic(manifest, json.dumps({"spec": spec, "chunks": chunks}, indent=2))
        return chunks

    def _process(self, key: str, chunk: str) -> ChunkResult:
        local = Path(chunk)
        if self.filesystem is not None:
            local = self.scratch_dir / f"{key}-{Path(chunk).name}"
            self.filesystem.get(chunk, str(local))
        output = self._output_path(key)
        temp = output.with_name(f".{output.name}.{self.worker_id}.tmp")
        counts = {"read": 0}
        try:
            rows = self._mapped_rows(key, local, counts)
            if self.output_format == "jsonl":
                written = _write_jsonl(temp, rows)
            else:
                written = _write_parquet(temp, rows)
            os.replace(temp, output)
        finally:
            temp.unlink(missing_ok=True)
            if self.filesystem is not None:
                local.unlink(missing_ok=True)

        result = ChunkResult(chunk, output, counts["read"], written)
        _write_atomic(
            self.done_dir / f"{key}.json",
            json.dumps(
                {
                    "chunk": chunk,
                    "output": output.name,
                    "rows_read": result.rows_read,
                    "rows_written": result.rows_written,
                    "worker": self.worker_id,
                    "finished_at": time.time(),
                },
                indent=2,
            ),
        )
        return result

    def _mapped_rows(self, key: str, local: Path, counts: dict) -> Iterator[Row]:
        claim = self._claim_path(key)
        heartbeat = time.monotonic()
        for row in self.reader(local):
            counts["read"] += 1
            produced = self.fn(row)
            if isinstance(produced, dict):
                yield produced
            elif produced is not None:
                yield from produced
            if time.monotonic() - heartbeat > self.stale_after / 4:
                os.utime(claim)
                heartbeat = time.monotonic()

    def _claim(self, key: str) -> bool:
        path = self._claim_path(key)
        if path.exists():
            if not self._is_stale_or_mine(path):
                return False
            path.unlink(missing_ok=True)
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            return False
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump({"worker": self.worker_id, "claimed_at": time.time()}, handle)
        return True

    def _is_stale_or_mine(self, path: Path) -> bool:
        try:
            if time.time() - path.stat().st_mtime > self.stale_after:
                return True
            return json.loads(path.read_text(encoding="utf-8")).get("worker") == self.worker_id
        except FileNotFoundError:
            return True
        except ValueError:
            # A claim being written right now reads as empty; treat it as live.
            return False

    def _live_claim_exists(self, key: str) -> bool:
        try:
            return time.time() - self._claim_path(key).stat().st_mtime <= self.stale_after
        except FileNotFoundError:
            return False

    def _is_done(self, key: str) -> bool:
        return (self.done_dir / f"{key}.json").exists()

    def _claim_path(self, key: str) -> Path:
        return self.claims_dir / f"{key}.claim"

    def _output_path(self, key: str) -> Path:
        return self.output_dir / f"{key}{_OUTPUT_FORMATS[self.output_format]}"

    @staticmethod
    def _key(index: int, chunk: str) -> str:
        digest = hashlib.sha1(chunk.encode("utf-8")).hexdigest()[:8]
        return f"{index:06d}-{digest}"


def _write_atomic(path: Path, text: str) -> None:
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temp.write_text(text, encoding="utf-8")
    os.replace(temp, path)


def _write_jsonl(path: Path, rows: Iterable[Row]) -> int:
    written = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            written += 1
    return written


def _write_parquet(path: Path, rows: Iterable[Row]) -> int:
    pq = _import_pyarrow_parquet()
    import pyarrow as pa

    writer = None
    written = 0
    batch: list = []

    def flush() -> None:
        nonlocal writer
        table = pa.Table.from_pylist(batch, schema=writer.schema if writer else None)
        if writer is None:
            writer = pq.ParquetWriter(path, table.schema)
        writer.write_table(table)
        batch.clear()

    try:
        for row in rows:
            batch.append(row)
            written += 1
            if len(batch) >= _PARQUET_BATCH_ROWS:
                flush()
        if batch or writer is None:
            flush()
    finally:
        if writer is not None:
            writer.close()
    return written


def _import_pyarrow_parquet():
    try:
        import pyarrow.parquet as pq
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Parquet chunks need pyarrow. Install it with: pip install 'ml4setk[datasets]'"
        ) from exc
    return pq
