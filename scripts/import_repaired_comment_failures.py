#!/usr/bin/env python3
"""Generate one compact, deterministic fixture per repaired-run failure.

The input is the one-record-per-failure classification produced from the
completed all-language two-stage run.  Every generated fixture retains the
source record hash, the failure disposition, and hashes plus byte lengths for
the original raw/old/current values.  Only active sanitizer regressions retain
literal text, and those fixtures contain only the executable raw/expected pair.

Records without a safe literal oracle and cases superseded by later
adjudication remain accounting-only.  Repository paths, source context, judge
prose, and unused output literals intentionally stay in the ignored analysis
input rather than being copied into the test corpus.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence

SCHEMA_VERSION = 2
DEFAULT_CLASSIFICATION = Path(
    "tmp/stack_v2_comment_cleaner_all_languages_50/"
    "two_stage_repaired/repair_analysis/failures.jsonl"
)
DEFAULT_OUTPUT_DIR = Path("tests/fixtures/comment_cleaning_repaired_failures")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_OUTPUT_DIR = (PROJECT_ROOT / DEFAULT_OUTPUT_DIR).resolve()
SENTINEL_NAME = ".generated-by-import_repaired_comment_failures"
SENTINEL_CONTENT = b"schema=2\nowner=scripts/import_repaired_comment_failures.py\n"
NOTICE_NAME = "NOTICE.md"
NOTICE_TEXT = """# Repaired comment-failure fixture provenance

These fixtures were generated from comment candidates sampled from
`bigcode/the-stack-v2-dedup`. The Stack v2 corpus is backed by source content
archived by Software Heritage.

Each case keeps the 40-hex source identifier and source-excerpt SHA-256 supplied
by the frozen classification, plus hashes and UTF-8 byte lengths for the
original raw and output literals. Repository names, paths, surrounding source
context, and judge prose are intentionally omitted. Active regressions keep
only the raw/expected text needed to execute the test; two oversized cases use
reviewed minimal reproductions and retain hashes for their original literals.

The frozen classification did not include exact per-file license metadata.
Treat these as test-only excerpts and use the recorded source identifier to
consult the underlying Stack v2/Software Heritage source before any reuse
outside regression testing.
"""

DISPOSITION_EXECUTABLE = "executable_regression"
DISPOSITION_NO_ORACLE = "accounting_only_no_oracle"
DISPOSITION_SUPERSEDED = "accounting_only_superseded"

# These original expectations were replaced by focused policy-oracle or final
# validation fixtures.  Retaining another raw/expected copy here adds corpus
# material without adding executable coverage.
SUPERSEDED_EXECUTABLE_CASE_IDS = frozenset(
    {
        "curry-line-23444fdefd068fb2",
        "cuda-line-9be1a4d25d76a815",
        "dataweave-block-176a378804208c72",
        "dataweave-block-57a44aedd448d3e4",
        "dataweave-block-7ca8f6613b33c681",
        "dataweave-block-a1cc56db6a23edfe",
        "dataweave-block-a466a5cd93c146e3",
        "dataweave-block-b6abc7d8d1b5348e",
        "dircolors-line-7584f27f1d223ba4",
        "dm-line-d411f3f58b36b13d",
        "gams-line-3424ffb6abad3895",
        "genero_forms-block-58eab17332f7cdab",
        "makefile-line-04aa358fc4ea11c8",
        "monkey_c-block-af494f83e5638bc2",
        "qml-block-a7c77eedd1191b90",
        "xbase-block-e6a93f23568f0866",
        "yasnippet-line-5ec1ebbdb4bd17d7",
        "yasnippet-line-64f7278bb268116f",
        "yasnippet-line-a7b84299d22f1280",
        "yasnippet-line-d7be757b6b96c29a",
        "yasnippet-line-fbf05106c07d8732",
    }
)

# The original literals for these two active regressions were unusually large
# (19,352 and 7,144 characters).  These reviewed reproductions exercise the
# same language-specific four-slash wrapper behavior without embedding an
# AspectJ source file or base64-encoded image payload in the committed fixture.
REVIEWED_MINIMIZED_REGRESSIONS = {
    "aspectj-line-e228da2958374c9a": {
        "raw_comment": "////package rollback;\n////import java.util.Set;",
        "expected_output": "package rollback;\nimport java.util.Set;",
    },
    "openstep_property_list-line-63f4c6020d2b8342": {
        "raw_comment": "////encoded-payload",
        "expected_output": "encoded-payload",
    },
}

ALLOWED_CATEGORIES = frozenset(
    {
        "sanitizer_regression",
        "extractor_or_source_invalid",
        "policy_or_judge_conflict",
        "approved_oracle_match",
        "needs_manual_review",
    }
)
ALLOWED_EXPECTED_SOURCES = frozenset({"manifest_old", "current", "oracle"})
CASE_ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9_.+-]*")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
SOURCE_ID_PATTERN = re.compile(r"[0-9a-f]{40}")

REQUIRED_CLASSIFICATION_KEYS = frozenset(
    {
        "case_id",
        "language",
        "category",
        "reason",
        "evidence",
        "old_output_sha",
        "current_output_sha",
        "recommended_expected_output_source",
        "cluster",
        "raw_comment",
        "manifest_old_output",
        "current_output",
        "recommended_expected_output",
    }
)


class ImportValidationError(ValueError):
    """Raised when classification input cannot safely become a fixture."""


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _canonical_json(value: Any, *, pretty: bool) -> str:
    if pretty:
        return (
            json.dumps(
                value,
                ensure_ascii=True,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ImportValidationError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _case_id_set_sha256(case_ids: Iterable[str]) -> str:
    payload = "".join(f"{case_id}\n" for case_id in sorted(case_ids))
    return _sha256_text(payload)


def _require_string(record: Mapping[str, Any], key: str, context: str) -> str:
    value = record.get(key)
    if not isinstance(value, str):
        raise ImportValidationError(f"{context}: {key} must be a string")
    return value


def _validate_record(record: Mapping[str, Any], context: str) -> None:
    missing = REQUIRED_CLASSIFICATION_KEYS - record.keys()
    if missing:
        raise ImportValidationError(f"{context}: missing required keys: {sorted(missing)}")

    case_id = _require_string(record, "case_id", context)
    if not CASE_ID_PATTERN.fullmatch(case_id):
        raise ImportValidationError(f"{context}: unsafe case_id {case_id!r}")
    if not _require_string(record, "language", context):
        raise ImportValidationError(f"{context}: language must not be empty")
    if not _require_string(record, "reason", context):
        raise ImportValidationError(f"{context}: reason must not be empty")
    if not _require_string(record, "cluster", context):
        raise ImportValidationError(f"{context}: cluster must not be empty")
    if not isinstance(record.get("evidence"), dict):
        raise ImportValidationError(f"{context}: evidence must be an object")
    evidence = record["evidence"]
    source_id = evidence.get("source_id")
    if not isinstance(source_id, str) or SOURCE_ID_PATTERN.fullmatch(source_id) is None:
        raise ImportValidationError(f"{context}: evidence.source_id must be 40-hex")
    source_excerpt_sha256 = evidence.get("source_excerpt_sha256")
    if (
        not isinstance(source_excerpt_sha256, str)
        or SHA256_PATTERN.fullmatch(source_excerpt_sha256) is None
    ):
        raise ImportValidationError(f"{context}: evidence.source_excerpt_sha256 must be a SHA-256")

    category = _require_string(record, "category", context)
    if category not in ALLOWED_CATEGORIES:
        raise ImportValidationError(f"{context}: unsupported category {category!r}")

    old_output = _require_string(record, "manifest_old_output", context)
    current_output = _require_string(record, "current_output", context)
    old_sha = _require_string(record, "old_output_sha", context)
    current_sha = _require_string(record, "current_output_sha", context)
    for key, value in (
        ("old_output_sha", old_sha),
        ("current_output_sha", current_sha),
    ):
        if not SHA256_PATTERN.fullmatch(value):
            raise ImportValidationError(f"{context}: invalid {key}")
    if old_sha != _sha256_text(old_output):
        raise ImportValidationError(f"{context}: old output SHA-256 mismatch")
    if current_sha != _sha256_text(current_output):
        raise ImportValidationError(f"{context}: current output SHA-256 mismatch")

    expected_source = record.get("recommended_expected_output_source")
    expected = record.get("recommended_expected_output")
    if expected_source is None:
        if expected is not None:
            raise ImportValidationError(f"{context}: null expected source requires a null literal")
    else:
        if expected_source not in ALLOWED_EXPECTED_SOURCES:
            raise ImportValidationError(
                f"{context}: unsupported expected source {expected_source!r}"
            )
        if not isinstance(expected, str):
            raise ImportValidationError(
                f"{context}: a recommended source requires a string literal"
            )

    if category == "sanitizer_regression":
        if expected_source != "manifest_old" or expected != old_output:
            raise ImportValidationError(f"{context}: sanitizer regressions must use manifest_old")
    elif category == "approved_oracle_match":
        if expected_source != "oracle" or not isinstance(expected, str):
            raise ImportValidationError(f"{context}: approved oracle matches must use oracle")
    elif category in {
        "extractor_or_source_invalid",
        "needs_manual_review",
    }:
        if expected_source is not None or expected is not None:
            raise ImportValidationError(
                f"{context}: accounting-only categories cannot pin a literal"
            )
    elif expected_source not in {None, "current"}:
        raise ImportValidationError(
            f"{context}: policy conflicts may only retain current or stay unresolved"
        )
    elif expected_source == "current" and expected != current_output:
        raise ImportValidationError(f"{context}: current expected source must equal current_output")


def load_classification(path: Path) -> list[dict[str, Any]]:
    """Load and validate a classification JSONL without mutating the repository."""

    records = []
    seen_case_ids = set()
    with path.open("r", encoding="utf-8", newline="") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                raise ImportValidationError(
                    f"{path}:{line_number}: blank JSONL records are not allowed"
                )
            try:
                record = json.loads(
                    line,
                    object_pairs_hook=_reject_duplicate_keys,
                )
            except (json.JSONDecodeError, ImportValidationError) as exc:
                raise ImportValidationError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(record, dict):
                raise ImportValidationError(f"{path}:{line_number}: record must be an object")
            context = f"{path}:{line_number}"
            _validate_record(record, context)
            case_id = record["case_id"]
            if case_id in seen_case_ids:
                raise ImportValidationError(f"{context}: duplicate case_id {case_id!r}")
            seen_case_ids.add(case_id)
            records.append(record)

    if not records:
        raise ImportValidationError(f"{path}: classification must not be empty")
    return records


def _literal_integrity(value: str) -> dict[str, Any]:
    encoded = value.encode("utf-8")
    return {
        "sha256": _sha256_bytes(encoded),
        "utf8_length": len(encoded),
    }


def _fixture_disposition(record: Mapping[str, Any]) -> str:
    case_id = record["case_id"]
    expected_source = record["recommended_expected_output_source"]
    if case_id in SUPERSEDED_EXECUTABLE_CASE_IDS:
        if expected_source is None:
            raise ImportValidationError(
                f"{case_id}: superseded executable case no longer has an expected source"
            )
        return DISPOSITION_SUPERSEDED
    if expected_source is None:
        return DISPOSITION_NO_ORACLE
    return DISPOSITION_EXECUTABLE


def _fixture_record(record: Mapping[str, Any]) -> dict[str, Any]:
    canonical_record = _canonical_json(record, pretty=False)
    expected = record["recommended_expected_output"]
    original_integrity = {
        "raw_comment": _literal_integrity(record["raw_comment"]),
        "manifest_old_output": _literal_integrity(record["manifest_old_output"]),
        "current_output": _literal_integrity(record["current_output"]),
    }
    if expected is not None:
        original_integrity["recommended_expected_output"] = _literal_integrity(expected)

    disposition = _fixture_disposition(record)
    fixture = {
        "schema_version": SCHEMA_VERSION,
        "case_id": record["case_id"],
        "language": record["language"],
        "category": record["category"],
        "cluster": record["cluster"],
        "disposition": disposition,
        "original_expected_output_source": record["recommended_expected_output_source"],
        "original_integrity": original_integrity,
        "source_provenance": {
            "dataset": "bigcode/the-stack-v2-dedup",
            "source_excerpt_sha256": record["evidence"]["source_excerpt_sha256"],
            "source_id": record["evidence"]["source_id"],
        },
        "source_record_sha256": _sha256_text(canonical_record),
    }
    if disposition != DISPOSITION_EXECUTABLE:
        return fixture

    minimized = REVIEWED_MINIMIZED_REGRESSIONS.get(record["case_id"])
    if minimized is None:
        raw_comment = record["raw_comment"]
        expected_output = expected
        provenance = "exact_classification_literal"
    else:
        raw_comment = minimized["raw_comment"]
        expected_output = minimized["expected_output"]
        provenance = "reviewed_minimized_reproduction"
    if not isinstance(expected_output, str):
        raise ImportValidationError(
            f"{record['case_id']}: executable fixture requires expected output"
        )
    fixture["regression"] = {
        "raw_comment": raw_comment,
        "expected_output": expected_output,
        "provenance": provenance,
    }
    return fixture


def _safe_force_target(output_dir: Path) -> None:
    if output_dir.is_symlink():
        raise ImportValidationError(f"refusing symlinked destructive --force target: {output_dir}")
    if not output_dir.exists():
        return
    resolved = output_dir.resolve()
    if not output_dir.is_dir():
        raise ImportValidationError(
            f"refusing non-directory destructive --force target: {output_dir}"
        )
    if resolved == EXPECTED_OUTPUT_DIR:
        return

    sentinel = output_dir / SENTINEL_NAME
    if sentinel.is_symlink() or not sentinel.is_file() or sentinel.read_bytes() != SENTINEL_CONTENT:
        raise ImportValidationError(
            f"refusing destructive --force target without importer sentinel: {output_dir}"
        )


def import_classification(
    classification_path: Path,
    output_dir: Path,
    *,
    expected_count: Optional[int] = None,
    force: bool = False,
) -> dict[str, Any]:
    """Validate classification and atomically emit one JSON file per case."""

    classification_path = Path(classification_path)
    output_dir = Path(output_dir)
    records = load_classification(classification_path)
    if expected_count is not None and len(records) != expected_count:
        raise ImportValidationError(
            f"{classification_path}: expected {expected_count} records, found {len(records)}"
        )
    if output_dir.exists() and not force:
        raise ImportValidationError(f"{output_dir} already exists; pass --force to replace it")
    if force:
        _safe_force_target(output_dir)

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{output_dir.name}.",
            dir=output_dir.parent,
        )
    )
    try:
        descriptors = []
        category_counts = Counter()
        source_counts = Counter()
        disposition_counts = Counter()
        regression_provenance_counts = Counter()
        unresolved_ids = []
        for record in sorted(records, key=lambda item: item["case_id"]):
            fixture = _fixture_record(record)
            filename = f"{record['case_id']}.json"
            fixture_bytes = _canonical_json(fixture, pretty=True).encode("utf-8")
            (staging / filename).write_bytes(fixture_bytes)
            expected_source = record["recommended_expected_output_source"]
            source_counts["null" if expected_source is None else expected_source] += 1
            category_counts[record["category"]] += 1
            disposition_counts[fixture["disposition"]] += 1
            regression = fixture.get("regression")
            if regression is not None:
                regression_provenance_counts[regression["provenance"]] += 1
            if record["category"] == "needs_manual_review":
                unresolved_ids.append(record["case_id"])
            descriptors.append(
                {
                    "case_id": record["case_id"],
                    "filename": filename,
                    "sha256": _sha256_bytes(fixture_bytes),
                    "category": record["category"],
                    "disposition": fixture["disposition"],
                    "original_expected_output_source": expected_source,
                    "source_record_sha256": fixture["source_record_sha256"],
                }
            )

        manifest = {
            "schema_version": SCHEMA_VERSION,
            "case_count": len(records),
            "case_id_set_sha256": _case_id_set_sha256(record["case_id"] for record in records),
            "category_counts": dict(sorted(category_counts.items())),
            "recommended_expected_output_source_counts": dict(sorted(source_counts.items())),
            "disposition_counts": dict(sorted(disposition_counts.items())),
            "regression_provenance_counts": dict(sorted(regression_provenance_counts.items())),
            "unresolved_count": len(unresolved_ids),
            "unresolved_ids": sorted(unresolved_ids),
            "source_classification": {
                "sha256": _sha256_bytes(classification_path.read_bytes()),
                "record_count": len(records),
            },
            "fixtures": descriptors,
        }
        (staging / "_manifest.json").write_text(
            _canonical_json(manifest, pretty=True),
            encoding="utf-8",
        )
        (staging / SENTINEL_NAME).write_bytes(SENTINEL_CONTENT)
        (staging / NOTICE_NAME).write_text(NOTICE_TEXT, encoding="utf-8")

        if output_dir.exists():
            shutil.rmtree(output_dir)
        os.replace(staging, output_dir)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--classification",
        type=Path,
        default=DEFAULT_CLASSIFICATION,
        help="one-record-per-failure classification JSONL",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="directory receiving one JSON fixture per case",
    )
    parser.add_argument(
        "--expected-count",
        type=int,
        default=569,
        help="refuse input with a different record count (use 0 to disable)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing, narrowly scoped output directory",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    expected_count = args.expected_count or None
    manifest = import_classification(
        args.classification,
        args.output_dir,
        expected_count=expected_count,
        force=args.force,
    )
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "case_count": manifest["case_count"],
                "case_id_set_sha256": manifest["case_id_set_sha256"],
                "category_counts": manifest["category_counts"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
