"""Restartable, multi-worker iteration over datasets split into files."""

from .ChunkedIterator import ChunkedIterator, ChunkResult, read_rows

__all__ = ["ChunkResult", "ChunkedIterator", "read_rows"]
