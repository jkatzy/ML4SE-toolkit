from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest


def _load_module() -> Any:
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "build_comment_research_packets.py"
    )
    spec = importlib.util.spec_from_file_location("stack_v3_comment_research_packets", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


PACKETS = _load_module()


def _row(language: str, count: int = 1) -> dict[str, int | str]:
    return {
        "language": language,
        "repo_count": count,
        "file_count": count * 2,
        "total_size_bytes": count * 3,
        "estimated_tokens": count * 4,
    }


def test_inventory_separates_supported_new_and_carryover_labels() -> None:
    records = PACKETS.build_inventory(
        [_row("Python"), _row("F*"), _row("Brand New"), _row("JSON")],
        ["Python", "F-Star", "JSON"],
    )
    by_language = {record.language: record for record in records}

    assert by_language["Python"].registry_status == "direct_canonical"
    assert by_language["F*"].registry_status == "direct_alias"
    assert by_language["F*"].v2_status == "new_or_renamed"
    assert by_language["Brand New"].v2_status == "new_or_renamed"
    assert by_language["JSON"].v2_status == "present"
    assert [record.language for record in PACKETS.research_queue(records)] == [
        "Brand New",
        "F*",
    ]


def test_inventory_discrepancy_labels_receive_a_separate_review() -> None:
    records = PACKETS.build_inventory(
        [_row("Befunge"), _row("Python"), _row("Python traceback")],
        ["Befunge", "Python", "Python_traceback"],
    )

    assert [
        record.language for record in PACKETS.inventory_discrepancy_queue(records)
    ] == ["Befunge", "Python traceback"]


def test_inventory_rejects_duplicate_labels() -> None:
    with pytest.raises(ValueError, match="duplicate Stack v3 language label"):
        PACKETS.build_inventory([_row("New"), _row("New")], ["Python"])


def test_chunk_records_is_deterministic_and_complete() -> None:
    records = PACKETS.build_inventory(
        [_row(f"New {index}", index + 1) for index in range(7)],
        ["Python"],
    )

    chunks = PACKETS.chunk_records(PACKETS.research_queue(records), 3)

    assert [name for name, _ in chunks] == ["batch_00", "batch_01", "batch_02"]
    assigned = [record.language for _, chunk in chunks for record in chunk]
    assert assigned == [record.language for record in PACKETS.research_queue(records)]
    assert len(assigned) == len(set(assigned)) == 7


def test_pinned_intake_queue_keeps_labels_after_they_become_supported() -> None:
    records = PACKETS.build_inventory(
        [_row("Python"), _row("Brand New")],
        ["Python"],
    )

    queue = PACKETS.research_queue(records, ("Python", "Brand New"))

    assert [record.language for record in queue] == ["Python", "Brand New"]


def test_primary_intake_scope_is_unique_and_includes_mapping_reviews() -> None:
    labels = PACKETS.STACK_V3_PRIMARY_INTAKE_LABELS

    assert len(labels) == len(set(labels)) == 116
    assert set(PACKETS.MAPPING_REVIEW_LABELS).issubset(labels)


def test_write_outputs_keeps_packets_below_selected_output_root(tmp_path: Path) -> None:
    records = PACKETS.build_inventory(
        [_row("Python"), _row("Brand New", 2)],
        ["Python"],
    )
    chunks = PACKETS.chunk_records(PACKETS.research_queue(records), 1)

    PACKETS.write_outputs(tmp_path, records, chunks)

    inventory = json.loads((tmp_path / "inventory.json").read_text(encoding="utf-8"))
    assignments = json.loads((tmp_path / "assignments.json").read_text(encoding="utf-8"))
    prompt = (tmp_path / "prompts" / "batch_00.md").read_text(encoding="utf-8")
    assert inventory["summary"]["new_or_renamed_missing_languages"] == 1
    assert assignments["batches"] == {"batch_00": ["Brand New"]}
    assert "docs/comment_research/stack_v3_full/batch_00.md" in prompt
    assert PACKETS.STACK_V3_REVISION in prompt
