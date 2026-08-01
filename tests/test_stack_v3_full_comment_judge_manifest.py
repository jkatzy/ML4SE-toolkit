from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import pytest


def _load_builder() -> Any:
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "build_stack_v3_full_comment_judge_cases.py"
    )
    spec = importlib.util.spec_from_file_location("stack_v3_full_comment_judge_cases", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BUILDER = _load_builder()


def _write_jsonl(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def test_cli_is_pinned_to_stack_v3_full_revision(tmp_path: Path) -> None:
    export = tmp_path / "contents.jsonl"
    _write_jsonl(export, [{"language": "Java", "content": "// note\n"}])

    args = BUILDER.parse_args(["--input-jsonl", str(export)])

    assert args.dataset_revision == BUILDER.STACK_V3_FULL_REVISION
    with pytest.raises(SystemExit):
        BUILDER.parse_args(
            [
                "--input-jsonl",
                str(export),
                "--dataset-revision",
                "moving-main",
            ]
        )


def test_flat_export_inspection_records_exact_schema_and_hash(tmp_path: Path) -> None:
    export = tmp_path / "contents.jsonl"
    _write_jsonl(
        export,
        [
            {
                "dataset": BUILDER.STACK_V3_FULL_DATASET,
                "dataset_revision": BUILDER.STACK_V3_FULL_REVISION,
                "dataset_table": BUILDER.STACK_V3_FULL_TABLE,
                "language": "Java",
                "content": "class A {} // note\n",
                "blob_id": "one",
            },
            {
                "language": "Java",
                "content": "/* block */ class B {}\n",
                "blob_id": "two",
            },
        ],
    )

    inspection = BUILDER.inspect_flat_export(export)

    assert inspection.row_count == 2
    assert inspection.sha256 == hashlib.sha256(export.read_bytes()).hexdigest()
    assert inspection.content_fields == ("content",)
    assert inspection.language_fields == ("language",)


def test_flat_export_rejects_nested_train_repository_rows(tmp_path: Path) -> None:
    export = tmp_path / "repository_rows.jsonl"
    _write_jsonl(
        export,
        [
            {
                "repo_name": "owner/project",
                "files": [
                    {
                        "language": "Java",
                        "content": "// nested and forbidden\n",
                    }
                ],
            }
        ],
    )

    with pytest.raises(BUILDER.FlatExportError, match=r"nested files\[\]"):
        BUILDER.inspect_flat_export(export)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("dataset", "HuggingFaceCode/stack-v3-train"),
        ("dataset_revision", "moving-main"),
        ("dataset_table", "repositories"),
    ],
)
def test_flat_export_rejects_conflicting_provenance(tmp_path: Path, field: str, value: str) -> None:
    export = tmp_path / "wrong_provenance.jsonl"
    _write_jsonl(
        export,
        [{"language": "Java", "content": "// note\n", field: value}],
    )

    with pytest.raises(BUILDER.FlatExportError, match=field):
        BUILDER.inspect_flat_export(export)


def test_manifest_reuses_judge_schema_and_stamps_full_provenance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    export = tmp_path / "contents.jsonl"
    output_root = tmp_path / "judge"
    _write_jsonl(
        export,
        [
            {
                "language": "Java",
                "content": "class A { // line note\n  /* block note */ int x;\n}\n",
                "blob_id": "blob-one",
                "repo_name": "owner/project",
                "path": "src/A.java",
            }
        ],
    )

    def reject_network(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("Stack v3 full local manifest builder attempted network access")

    monkeypatch.setattr(BUILDER.STACK_V2_BUILDER, "_load_streaming_dataset", reject_network)
    status = BUILDER.main(
        [
            "--input-jsonl",
            str(export),
            "--languages",
            "java",
            "--per-kind",
            "1",
            "--max-records-per-language",
            "10",
            "--content-prefetch-workers",
            "1",
            "--progress-every",
            "0",
            "--output-root",
            str(output_root),
        ]
    )

    assert status == 0
    manifest = _read_jsonl(output_root / "manifest.jsonl")
    assert {row["comment_kind"] for row in manifest} == {"line", "block"}
    assert {row["dataset"] for row in manifest} == {BUILDER.STACK_V3_FULL_DATASET}
    assert {row["dataset_revision"] for row in manifest} == {BUILDER.STACK_V3_FULL_REVISION}
    assert {row["dataset_table"] for row in manifest} == {BUILDER.STACK_V3_FULL_TABLE}
    input_sha256 = hashlib.sha256(export.read_bytes()).hexdigest()
    assert {row["dataset_export_sha256"] for row in manifest} == {input_sha256}
    assert all(Path(row["source_file"]).is_file() for row in manifest)
    assert not (output_root / "failures.jsonl").exists()

    provenance = json.loads((output_root / "provenance.json").read_text(encoding="utf-8"))
    assert provenance["dataset"] == BUILDER.STACK_V3_FULL_DATASET
    assert provenance["dataset_revision"] == BUILDER.STACK_V3_FULL_REVISION
    assert provenance["dataset_table"] == BUILDER.STACK_V3_FULL_TABLE
    assert provenance["input_sha256"] == input_sha256
    assert provenance["input_rows"] == 1
    assert provenance["case_count"] == 2
    assert provenance["failure_count"] == 0


def test_manifest_progress_uses_stack_v3_full_label(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    export = tmp_path / "contents.jsonl"
    _write_jsonl(export, [{"language": "Java", "content": "// note\n"}])

    status = BUILDER.main(
        [
            "--input-jsonl",
            str(export),
            "--languages",
            "java",
            "--per-kind",
            "1",
            "--max-records-per-language",
            "1",
            "--content-prefetch-workers",
            "1",
            "--progress-every",
            "1",
            "--output-root",
            str(tmp_path / "judge"),
        ]
    )

    captured = capsys.readouterr()
    assert status == 0
    assert "[stack-v3-full manifest]" in captured.err
    assert "[stack-v2 manifest]" not in captured.err


def test_nested_rows_fail_before_output_is_created(tmp_path: Path) -> None:
    export = tmp_path / "repository_rows.jsonl"
    output_root = tmp_path / "judge"
    _write_jsonl(
        export,
        [{"repo": "owner/project", "files": [{"language": "Java"}]}],
    )

    with pytest.raises(SystemExit, match=r"nested files\[\]"):
        BUILDER.main(
            [
                "--input-jsonl",
                str(export),
                "--languages",
                "java",
                "--output-root",
                str(output_root),
            ]
        )

    assert not output_root.exists()
