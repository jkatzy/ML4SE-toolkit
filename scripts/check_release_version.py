#!/usr/bin/env python3
"""Verify release metadata is internally consistent."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT_PATH = REPOSITORY_ROOT / "pyproject.toml"
PACKAGE_INIT_PATH = REPOSITORY_ROOT / "src" / "ml4setk" / "__init__.py"

PYPROJECT_VERSION_PATTERN = re.compile(r'^version = "([^"]+)"$', re.MULTILINE)
PACKAGE_VERSION_PATTERN = re.compile(r'^__version__ = "([^"]+)"$', re.MULTILINE)


def read_version(path: Path, pattern: re.Pattern[str], label: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = pattern.search(text)
    if match is None:
        raise ValueError(f"Could not find {label} version in {path}")
    return match.group(1)


def normalize_tag(tag: str) -> str:
    return tag.removeprefix("refs/tags/")


def find_release_issues(tag: str | None = None) -> tuple[str, list[str]]:
    pyproject_version = read_version(
        PYPROJECT_PATH,
        PYPROJECT_VERSION_PATTERN,
        "pyproject",
    )
    package_version = read_version(
        PACKAGE_INIT_PATH,
        PACKAGE_VERSION_PATTERN,
        "package",
    )

    issues: list[str] = []

    if pyproject_version != package_version:
        issues.append(
            "Version mismatch: "
            f"pyproject.toml has {pyproject_version}, "
            f"package __version__ has {package_version}"
        )

    if tag is not None:
        normalized_tag = normalize_tag(tag)
        expected_tag = f"v{pyproject_version}"
        if normalized_tag != expected_tag:
            issues.append(
                "Tag mismatch: "
                f"expected {expected_tag} from pyproject.toml, "
                f"got {normalized_tag}"
            )

    return pyproject_version, issues


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the package version matches release metadata."
    )
    parser.add_argument(
        "--tag",
        help="Tag name to validate, for example v0.0.2 or refs/tags/v0.0.2.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    version, issues = find_release_issues(tag=args.tag)

    if issues:
        print("Release version check failed.")
        for issue in issues:
            print(f"- {issue}")
        return 1

    if args.tag is None:
        print(f"Release version check passed for version {version}.")
    else:
        print(
            "Release version check passed for "
            f"version {version} and tag {normalize_tag(args.tag)}."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
