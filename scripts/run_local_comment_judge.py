"""Run a local OpenAI-compatible or Ollama model as a JSON comment judge.

This adapter reads the judge prompt from stdin and prints the JSON verdict
expected by ``tests/test_stack_v2_comment_judge.py`` to stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

VERDICT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "verdict",
        "extraction_correct",
        "cleaning_correct",
        "rationale",
    ],
    "properties": {
        "verdict": {"type": "string", "enum": ["pass", "fail"]},
        "extraction_correct": {"type": "boolean"},
        "cleaning_correct": {"type": "boolean"},
        "rationale": {"type": "string"},
    },
}


def parse_args() -> argparse.Namespace:
    """Parse command-line options for the local judge adapter."""

    parser = argparse.ArgumentParser(description="Run a local model as a comment judge.")
    parser.add_argument(
        "--provider",
        choices=("ollama", "vllm"),
        default=os.environ.get("COMMENT_JUDGE_LOCAL_PROVIDER", "ollama"),
        help="Local inference server to call.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("COMMENT_JUDGE_LOCAL_MODEL", "gemma4:31b"),
        help="Model name served by Ollama or vLLM.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("COMMENT_JUDGE_LOCAL_BASE_URL"),
        help="Server base URL. Defaults to Ollama or vLLM localhost URLs.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("COMMENT_JUDGE_LOCAL_TIMEOUT", "180")),
        help="HTTP request timeout in seconds.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=float(os.environ.get("COMMENT_JUDGE_LOCAL_TEMPERATURE", "0")),
        help="Sampling temperature for the judge request.",
    )
    return parser.parse_args()


def main() -> int:
    """Call the configured local model and print a validated verdict."""

    args = parse_args()
    prompt = sys.stdin.read()
    if not prompt.strip():
        print("No judge prompt received on stdin", file=sys.stderr)
        return 2

    try:
        if args.provider == "ollama":
            text = _call_ollama(args, prompt)
        else:
            text = _call_vllm(args, prompt)
        verdict = _parse_json_object(text)
        _validate_verdict(verdict)
    except (OSError, urllib.error.URLError, ValueError, json.JSONDecodeError) as exc:
        print(f"local judge failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(verdict, ensure_ascii=False))
    return 0


def _call_ollama(args: argparse.Namespace, prompt: str) -> str:
    base_url = (args.base_url or "http://localhost:11434").rstrip("/")
    payload = {
        "model": args.model,
        "messages": _messages(prompt),
        "stream": False,
        "format": "json",
        "options": {"temperature": args.temperature},
    }
    response = _post_json(f"{base_url}/api/chat", payload, args.timeout)
    message = response.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise ValueError("Ollama response missing message.content")
    return message["content"]


def _call_vllm(args: argparse.Namespace, prompt: str) -> str:
    base_url = (args.base_url or "http://localhost:8000/v1").rstrip("/")
    payload = {
        "model": args.model,
        "messages": _messages(prompt),
        "temperature": args.temperature,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "comment_judge_verdict",
                "schema": VERDICT_SCHEMA,
                "strict": True,
            },
        },
    }
    response = _post_json(f"{base_url}/chat/completions", payload, args.timeout)
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("vLLM response missing choices")
    message = choices[0].get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise ValueError("vLLM response missing choices[0].message.content")
    return message["content"]


def _messages(prompt: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "Return only a JSON object with verdict, extraction_correct, "
                "cleaning_correct, and rationale. Do not include markdown."
            ),
        },
        {"role": "user", "content": prompt},
    ]


def _post_json(url: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8")
    value = json.loads(body)
    if not isinstance(value, dict):
        raise ValueError("local judge response must be a JSON object")
    return value


def _parse_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`").strip()
        if stripped.startswith("json"):
            stripped = stripped[4:].strip()

    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end <= start:
            raise
        value = json.loads(stripped[start : end + 1])

    if not isinstance(value, dict):
        raise ValueError("local judge output must be a JSON object")
    return value


def _validate_verdict(verdict: dict[str, Any]) -> None:
    if verdict.get("verdict") not in {"pass", "fail"}:
        raise ValueError("verdict must be 'pass' or 'fail'")
    for field in ("extraction_correct", "cleaning_correct"):
        if not isinstance(verdict.get(field), bool):
            raise ValueError(f"{field} must be a boolean")
    if not isinstance(verdict.get("rationale"), str):
        raise ValueError("rationale must be a string")


if __name__ == "__main__":
    raise SystemExit(main())
