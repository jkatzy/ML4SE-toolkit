"""Tests for the local comment judge adapter."""

from __future__ import annotations

import importlib.util
from argparse import Namespace
from pathlib import Path

import pytest


def _load_local_judge():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "run_local_comment_judge.py"
    spec = importlib.util.spec_from_file_location("run_local_comment_judge", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


LOCAL_JUDGE = _load_local_judge()


def test_parse_json_object_accepts_fenced_json() -> None:
    verdict = LOCAL_JUDGE._parse_json_object(
        """```json
{"verdict":"pass","extraction_correct":true,"cleaning_correct":true,"rationale":"ok"}
```"""
    )

    assert verdict["verdict"] == "pass"
    assert verdict["extraction_correct"] is True
    assert verdict["cleaning_correct"] is True


def test_validate_verdict_rejects_bad_shape() -> None:
    with pytest.raises(ValueError, match="cleaning_correct"):
        LOCAL_JUDGE._validate_verdict(
            {
                "verdict": "pass",
                "extraction_correct": True,
                "cleaning_correct": "yes",
                "rationale": "bad",
            }
        )


def test_ollama_call_uses_chat_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake_post_json(url, payload, timeout):
        calls.append((url, payload, timeout))
        return {
            "message": {
                "content": (
                    '{"verdict":"pass","extraction_correct":true,'
                    '"cleaning_correct":true,"rationale":"ok"}'
                )
            }
        }

    monkeypatch.setattr(LOCAL_JUDGE, "_post_json", fake_post_json)

    args = Namespace(
        base_url="http://localhost:11434",
        model="gemma4:31b",
        temperature=0,
        timeout=7,
    )
    text = LOCAL_JUDGE._call_ollama(args, "judge prompt")

    assert "rationale" in text
    assert calls[0][0] == "http://localhost:11434/api/chat"
    assert calls[0][1]["model"] == "gemma4:31b"
    assert calls[0][1]["stream"] is False
    assert calls[0][2] == 7


def test_vllm_call_uses_openai_compatible_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake_post_json(url, payload, timeout):
        calls.append((url, payload, timeout))
        return {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"verdict":"pass","extraction_correct":true,'
                            '"cleaning_correct":true,"rationale":"ok"}'
                        )
                    }
                }
            ]
        }

    monkeypatch.setattr(LOCAL_JUDGE, "_post_json", fake_post_json)

    args = Namespace(
        base_url="http://localhost:8000/v1",
        model="gemma4:31b",
        temperature=0,
        timeout=11,
    )
    text = LOCAL_JUDGE._call_vllm(args, "judge prompt")

    assert "rationale" in text
    assert calls[0][0] == "http://localhost:8000/v1/chat/completions"
    assert calls[0][1]["model"] == "gemma4:31b"
    assert calls[0][1]["response_format"]["type"] == "json_schema"
    assert calls[0][2] == 11
