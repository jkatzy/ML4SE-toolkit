"""Shared handling for LLM usage-limit failures in comment judge tooling."""

from __future__ import annotations

import os
from typing import Any

USAGE_LIMIT_EXIT_CODE_ENV = "COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE"
DEFAULT_USAGE_LIMIT_EXIT_CODE = 88

USAGE_LIMIT_PHRASES = (
    "usage limit",
    "usage_limit",
    "usage cap",
    "usage_cap",
    "rate limit",
    "rate_limit",
    "quota exceeded",
    "insufficient_quota",
    "exceeded your current quota",
    "billing hard limit",
    "too many requests",
    "resource_exhausted",
)


def usage_limit_exit_code() -> int:
    """Return the process exit code used for usage-limit aborts."""

    configured = os.environ.get(USAGE_LIMIT_EXIT_CODE_ENV)
    if not configured:
        return DEFAULT_USAGE_LIMIT_EXIT_CODE

    try:
        return int(configured)
    except ValueError:
        return DEFAULT_USAGE_LIMIT_EXIT_CODE


def looks_like_usage_limit(*values: Any) -> bool:
    """Return true when command output looks like an LLM usage-limit failure."""

    text = "\n".join(
        normalized
        for value in values
        if (normalized := normalize_output(value)) is not None
    ).lower()
    return any(phrase in text for phrase in USAGE_LIMIT_PHRASES)


def normalize_output(value: Any) -> str | None:
    """Decode process output to text while preserving missing output as ``None``."""

    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)
