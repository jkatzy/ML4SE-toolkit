from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def _load_module() -> Any:
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "validate_comment_research.py"
    spec = importlib.util.spec_from_file_location("validate_comment_research", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_module()


def _report(
    label: str,
    action: str = "alias",
    *,
    reviewed: bool = False,
) -> str:
    review_status = "reviewed" if reviewed else "draft"
    reviewer = "/root/reviewer" if reviewed else "unassigned"
    review_date = "2026-08-01" if reviewed else "unreviewed"
    return f"""# Batch

## Dataset provenance

- Revision: pinned
- Review status: `{review_status}`

## {label}

### Identity and scope

- Raw dataset label: `{label}`

### Syntax contract

- Line comments: `//`

### Evidence

- Official documentation permalink: https://example.test/spec

### Representative examples

```text
// note
```

### Adversarial boundaries

- Negative cases: strings

### Decision

- Recommended action: `{action}`
- Reviewer: {reviewer}
- Review date: {review_date}
"""


def test_validate_report_accepts_complete_exact_label(tmp_path: Path) -> None:
    path = tmp_path / "batch_00.md"
    path.write_text(_report("New Language"), encoding="utf-8")

    assert VALIDATOR.validate_report(path, ["New Language"]) == []


def test_validate_report_rejects_missing_or_invalid_decisions(tmp_path: Path) -> None:
    path = tmp_path / "batch_00.md"
    path.write_text(
        _report("Wrong Label", action="guess").replace("### Adversarial boundaries", ""),
        encoding="utf-8",
    )

    errors = VALIDATOR.validate_report(path, ["Expected Label"])

    assert any("missing section for Expected Label" in error for error in errors)
    assert any("unexpected section Wrong Label" in error for error in errors)


def test_validate_all_can_allow_batches_still_in_progress(tmp_path: Path) -> None:
    assignments = {"batch_00": ["One"], "batch_01": ["Two"]}
    (tmp_path / "batch_00.md").write_text(_report("One"), encoding="utf-8")

    assert VALIDATOR.validate_all(assignments, tmp_path, allow_missing=True) == []
    assert VALIDATOR.validate_all(assignments, tmp_path, allow_missing=False) == [
        f"missing report: {tmp_path / 'batch_01.md'}"
    ]


def test_review_gate_rejects_draft_and_accepts_reviewed_report(tmp_path: Path) -> None:
    path = tmp_path / "batch_00.md"
    path.write_text(_report("One"), encoding="utf-8")

    errors = VALIDATOR.validate_report(path, ["One"], require_reviewed=True)

    assert f"{path.name}: report is not marked reviewed" in errors
    assert f"{path.name}: One: missing reviewer" in errors
    assert f"{path.name}: One: missing ISO review date" in errors

    path.write_text(_report("One", reviewed=True), encoding="utf-8")

    assert VALIDATOR.validate_report(path, ["One"], require_reviewed=True) == []


def test_load_assignments_rejects_duplicate_ownership(tmp_path: Path) -> None:
    path = tmp_path / "assignments.json"
    path.write_text(
        json.dumps({"batches": {"batch_00": ["Same"], "batch_01": ["Same"]}}),
        encoding="utf-8",
    )

    try:
        VALIDATOR.load_assignments(path)
    except ValueError as error:
        assert "assigned more than once" in str(error)
    else:
        raise AssertionError("duplicate assignments should fail validation")
