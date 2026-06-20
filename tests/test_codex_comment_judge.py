"""Tests for the Codex comment judge adapter."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_codex_judge():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "run_codex_comment_judge.py"
    spec = importlib.util.spec_from_file_location("run_codex_comment_judge", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CODEX_JUDGE = _load_codex_judge()


def test_parse_json_object_accepts_fenced_json() -> None:
    verdict = CODEX_JUDGE._parse_json_object(
        """```json
{"verdict":"pass","extraction_correct":true,"cleaning_correct":true,"rationale":"ok"}
```"""
    )

    assert verdict["verdict"] == "pass"
    assert verdict["extraction_correct"] is True
    assert verdict["cleaning_correct"] is True


def test_forwarded_output_is_limited_with_digest() -> None:
    oversized_output = (
        "codex-prefix-"
        + ("prefix-body-" * 1_000)
        + "OMITTED_SENTINEL"
        + ("suffix-body-" * 1_000)
        + "codex-suffix"
    )

    limited = CODEX_JUDGE._limit_forwarded_output(oversized_output)

    assert limited.startswith("codex-prefix-")
    assert limited.endswith("codex-suffix")
    assert "OMITTED_SENTINEL" not in limited
    assert "truncated" in limited
    assert "sha256=" in limited
