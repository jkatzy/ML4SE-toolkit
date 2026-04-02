#!/usr/bin/env python3
"""Fail when development-only artifacts are tracked on a main-ready branch."""

from __future__ import annotations

import subprocess
import sys
from pathlib import PurePosixPath

DISALLOWED_MAIN_PATTERNS = (
    "AGENTS.md",
    "docs/comment_research/**",
    "docs/comment_syntax_matrix.md",
    "docs/comment_syntax_stack_v2.md",
    "scratch/**",
    "tmp/**",
    "*.tmp",
    "*.bak",
    "*.orig",
    "*.rej",
    "*.swp",
)


def list_tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def is_disallowed_on_main(path: str) -> bool:
    pure_path = PurePosixPath(path)
    return any(pure_path.match(pattern) for pattern in DISALLOWED_MAIN_PATTERNS)


def find_disallowed_paths(paths: list[str]) -> list[str]:
    return sorted(path for path in paths if is_disallowed_on_main(path))


def main() -> int:
    disallowed_paths = find_disallowed_paths(list_tracked_files())
    if not disallowed_paths:
        print("Main-branch policy check passed.")
        return 0

    print("Main-branch policy check failed. Remove these development-only artifacts:")
    for path in disallowed_paths:
        print(f"- {path}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
