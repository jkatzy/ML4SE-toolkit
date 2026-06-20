"""Run Codex CLI as a JSON-only comment judge.

This adapter reads the judge prompt from stdin, invokes ``codex exec`` in
read-only mode, and prints the agent's final JSON verdict to stdout. It is used
by ``tests/test_stack_v2_comment_judge.py`` when ``COMMENT_JUDGE_USE_CODEX=1``.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from hashlib import sha256
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from comment_judge_limits import (  # noqa: E402
    looks_like_usage_limit,
    normalize_output,
    usage_limit_exit_code,
)

VERDICT_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
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
MAX_FORWARDED_OUTPUT_CHARS = 24_000
FORWARDED_OUTPUT_EDGE_CHARS = 4_000


def parse_args() -> argparse.Namespace:
    """Parse command-line options for the Codex judge adapter."""

    parser = argparse.ArgumentParser(description="Run Codex as a comment judge.")
    parser.add_argument(
        "--codex-bin",
        default=os.environ.get("CODEX_BIN", "codex"),
        help="Codex executable to run.",
    )
    parser.add_argument(
        "--cwd",
        default=os.environ.get("COMMENT_JUDGE_CODEX_CWD", os.getcwd()),
        help="Repository directory to give Codex as its working root.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("COMMENT_JUDGE_CODEX_MODEL"),
        help="Optional Codex model override.",
    )
    parser.add_argument(
        "--profile",
        default=os.environ.get("COMMENT_JUDGE_CODEX_PROFILE"),
        help="Optional Codex config profile.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("COMMENT_JUDGE_CODEX_TIMEOUT", "180")),
        help="Codex process timeout in seconds.",
    )
    return parser.parse_args()


def main() -> int:
    """Invoke Codex and print a validated JSON verdict."""

    args = parse_args()
    prompt = sys.stdin.read()
    if not prompt.strip():
        print("No judge prompt received on stdin", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="comment-judge-codex-") as temp_dir:
        temp_path = Path(temp_dir)
        schema_path = temp_path / "verdict.schema.json"
        output_path = temp_path / "last_message.json"
        schema_path.write_text(json.dumps(VERDICT_SCHEMA), encoding="utf-8")

        command = [
            args.codex_bin,
            "--ask-for-approval",
            "never",
            "--sandbox",
            "read-only",
            "exec",
            "--cd",
            args.cwd,
            "--ephemeral",
            "--color",
            "never",
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(output_path),
            "-",
        ]
        if args.model:
            command.extend(["--model", args.model])
        if args.profile:
            command.extend(["--profile", args.profile])

        try:
            result = subprocess.run(
                command,
                input=prompt,
                text=True,
                capture_output=True,
                timeout=args.timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = normalize_output(exc.stdout)
            stderr = normalize_output(exc.stderr)
            if looks_like_usage_limit(stdout, stderr):
                _print_usage_limit_abort(stdout, stderr)
                return usage_limit_exit_code()
            print(f"Codex judge timed out after {args.timeout}s", file=sys.stderr)
            _print_if_present(stderr)
            _print_if_present(stdout)
            return 124

        if result.returncode != 0:
            if looks_like_usage_limit(result.stdout, result.stderr):
                _print_usage_limit_abort(result.stdout, result.stderr)
                return usage_limit_exit_code()
            _print_if_present(result.stderr)
            _print_if_present(result.stdout)
            return result.returncode

        verdict_text = output_path.read_text(encoding="utf-8").strip()
        try:
            verdict = _parse_json_object(verdict_text)
        except json.JSONDecodeError:
            if looks_like_usage_limit(verdict_text, result.stdout, result.stderr):
                _print_usage_limit_abort(verdict_text, result.stderr)
                return usage_limit_exit_code()
            raise
        _validate_verdict(verdict)
        print(json.dumps(verdict, ensure_ascii=False))
        return 0


def _print_usage_limit_abort(stdout: Any, stderr: Any) -> None:
    """Print a clear reason before returning the special usage-limit exit code."""

    print(
        "Codex judge usage limit was reached; aborting the judge process.",
        file=sys.stderr,
    )
    normalized_stderr = normalize_output(stderr)
    normalized_stdout = normalize_output(stdout)
    _print_if_present(normalized_stderr)
    _print_if_present(normalized_stdout)


def _print_if_present(value: Any) -> None:
    """Print external process output after limiting echoed prompt payloads."""

    text = _limit_forwarded_output(value)
    if text:
        print(text, file=sys.stderr)


def _limit_forwarded_output(value: Any) -> str | None:
    """Return process output capped to an inspectable prefix/suffix summary."""

    text = normalize_output(value)
    if text is None or len(text) <= MAX_FORWARDED_OUTPUT_CHARS:
        return text

    prefix = text[:FORWARDED_OUTPUT_EDGE_CHARS]
    suffix = text[-FORWARDED_OUTPUT_EDGE_CHARS:]
    omitted = len(text) - len(prefix) - len(suffix)
    digest = sha256(text.encode("utf-8", errors="surrogatepass")).hexdigest()
    return (
        f"{prefix}\n"
        f"... [truncated {omitted} chars; sha256={digest}] ...\n"
        f"{suffix}"
    )


def _parse_json_object(text: str) -> dict[str, Any]:
    """Parse a JSON object, tolerating fenced final answers."""

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
        raise ValueError("Codex judge output must be a JSON object")
    return value


def _validate_verdict(verdict: dict[str, Any]) -> None:
    """Validate the minimal verdict shape expected by pytest."""

    if verdict.get("verdict") not in {"pass", "fail"}:
        raise ValueError("verdict must be 'pass' or 'fail'")
    for field in ("extraction_correct", "cleaning_correct"):
        if not isinstance(verdict.get(field), bool):
            raise ValueError(f"{field} must be a boolean")
    if not isinstance(verdict.get("rationale"), str):
        raise ValueError("rationale must be a string")


if __name__ == "__main__":
    raise SystemExit(main())
