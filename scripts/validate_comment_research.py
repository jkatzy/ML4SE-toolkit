#!/usr/bin/env python3
"""Validate Stack v3 full research records before implementation handoff."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ASSIGNMENTS = ROOT / "tmp" / "stack_v3_comment_research" / "assignments.json"
DEFAULT_REPORT_DIR = ROOT / "docs" / "comment_research" / "stack_v3_full"
ALLOWED_ACTIONS = frozenset(
    {
        "alias",
        "implement",
        "separate-family",
        "contextual-helper",
        "unsupported",
        "defer",
    }
)
REQUIRED_SUBHEADINGS = (
    "### Identity and scope",
    "### Syntax contract",
    "### Evidence",
    "### Representative examples",
    "### Adversarial boundaries",
    "### Decision",
)
ACTION_PATTERN = re.compile(r"(?m)^- Recommended action: `([^`]+)`[ \t]*$")
REVIEWER_PATTERN = re.compile(r"(?m)^- Reviewer: (?P<reviewer>\S.*?)[ \t]*$")
REVIEW_DATE_PATTERN = re.compile(
    r"(?m)^- Review date: (?P<date>\d{4}-\d{2}-\d{2})[ \t]*$"
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assignments", type=Path, default=DEFAULT_ASSIGNMENTS)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Validate existing reports without failing for batches still in progress.",
    )
    parser.add_argument(
        "--require-reviewed",
        action="store_true",
        help="Require a reviewed report status and per-label reviewer metadata.",
    )
    return parser.parse_args(argv)


def load_assignments(path: Path) -> dict[str, list[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    batches = payload.get("batches")
    if not isinstance(batches, dict) or not batches:
        raise ValueError("assignments must contain a non-empty batches object")
    result: dict[str, list[str]] = {}
    assigned: set[str] = set()
    for batch, labels in batches.items():
        if not isinstance(batch, str) or not isinstance(labels, list) or not labels:
            raise ValueError("each assignment batch must contain at least one label")
        if any(not isinstance(label, str) or not label for label in labels):
            raise ValueError(f"batch {batch!r} contains an invalid label")
        duplicates = assigned.intersection(labels)
        if duplicates:
            raise ValueError(
                "labels assigned more than once: " + ", ".join(sorted(duplicates))
            )
        assigned.update(labels)
        result[batch] = labels
    return result


def _sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^## (?P<label>[^\r\n]+)[ \t]*$", text))
    sections = {}
    for index, match in enumerate(matches):
        label = match.group("label").strip().strip("`")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[label] = text[match.start() : end]
    return sections


def validate_report(
    path: Path,
    expected_labels: Sequence[str],
    require_reviewed: bool = False,
) -> list[str]:
    text = path.read_text(encoding="utf-8")
    sections = _sections(text)
    errors: list[str] = []
    expected = set(expected_labels)
    actual = set(sections).difference({"Dataset provenance"})

    if require_reviewed and not re.search(
        r"(?m)^- Review status: `reviewed`[ \t]*$", text
    ):
        errors.append(f"{path.name}: report is not marked reviewed")

    for label in sorted(expected.difference(actual), key=str.casefold):
        errors.append(f"{path.name}: missing section for {label}")
    for label in sorted(actual.difference(expected), key=str.casefold):
        errors.append(f"{path.name}: unexpected section {label}")

    for label in expected_labels:
        section = sections.get(label)
        if section is None:
            continue
        for heading in REQUIRED_SUBHEADINGS:
            if heading not in section:
                errors.append(f"{path.name}: {label}: missing {heading}")
        if f"- Raw dataset label: `{label}`" not in section and not re.search(
            rf"(?m)^- Raw dataset label: `{re.escape(label)}`(?:[ \t]|$)", section
        ):
            errors.append(f"{path.name}: {label}: missing exact raw-label field")
        actions = ACTION_PATTERN.findall(section)
        if len(actions) != 1:
            errors.append(
                f"{path.name}: {label}: expected one recommendation, found {len(actions)}"
            )
        elif actions[0] not in ALLOWED_ACTIONS:
            errors.append(
                f"{path.name}: {label}: unsupported recommendation {actions[0]!r}"
            )
        if section.count("https://") < 1:
            errors.append(f"{path.name}: {label}: no HTTPS evidence link")
        if require_reviewed:
            reviewer_match = REVIEWER_PATTERN.search(section)
            if reviewer_match is None or reviewer_match.group("reviewer").lower() in {
                "unassigned",
                "unreviewed",
            }:
                errors.append(f"{path.name}: {label}: missing reviewer")
            if REVIEW_DATE_PATTERN.search(section) is None:
                errors.append(f"{path.name}: {label}: missing ISO review date")
    return errors


def validate_all(
    assignments: dict[str, list[str]],
    report_dir: Path,
    allow_missing: bool,
    require_reviewed: bool = False,
) -> list[str]:
    errors: list[str] = []
    for batch, labels in assignments.items():
        path = report_dir / f"{batch}.md"
        if not path.is_file():
            if not allow_missing:
                errors.append(f"missing report: {path}")
            continue
        errors.extend(validate_report(path, labels, require_reviewed=require_reviewed))
    return errors


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    assignments = load_assignments(args.assignments)
    errors = validate_all(
        assignments,
        args.report_dir,
        args.allow_missing,
        require_reviewed=args.require_reviewed,
    )
    if errors:
        raise SystemExit("Research validation failed:\n- " + "\n- ".join(errors))
    report_count = sum(
        (args.report_dir / f"{batch}.md").is_file() for batch in assignments
    )
    print(
        f"Validated {report_count}/{len(assignments)} Stack v3 full research reports"
    )


if __name__ == "__main__":
    main()
