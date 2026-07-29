"""Deterministic oracles for independently reviewed real-world cleaner failures."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping, Optional

import pytest

from ml4setk import (
    CommentQuery,
    CommentSanitizer,
    LineCommentQuery,
    QueryMatch,
    sanitize_comment,
    sanitize_comment_text,
)
from ml4setk.Parsing.Comments import get_comment_syntax

pytestmark = pytest.mark.unit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures" / "comment_cleaning_regressions"
MANIFEST_PATH = FIXTURE_DIR / "_manifest.json"

SCHEMA_VERSION = 5
ORACLE_EXCEPTION_SCHEMA_VERSION = 1
EXPECTED_CASE_COUNT = 1986
EXPECTED_FAILURES_SHA256 = "ef06ad5770587e095b01d75c110a0d36da9812fb4a80109c89c75f30a4632cfc"
EXPECTED_RUN_SUMMARY_SHA256 = "d7f9862148c5e555603557043a47c9c751a905003d160e0f9e1c51d8391a8cd0"
EXPECTED_SOURCE_MANIFEST_SHA256 = "1e87230b75165ae76583abdb48045e9ce9c5f4287135e8c4e564f400e230dcc0"
EXPECTED_CASE_ID_SET_SHA256 = "8e854fb306bd97bf73cb756bd5b8f8cf8f5c25b29bd97a3541f7140042d01fd5"
EXPECTED_PRIMARY_MODEL = "gpt-5.6-luna"
EXPECTED_SECONDARY_MODEL = "gpt-5.6-sol"

ALLOWED_DISPOSITIONS = frozenset({"adjudicated_override", "confirmed_bug", "judge_false_positive"})
ADJUDICATED_OVERRIDE_IDS = frozenset(
    {
        "cuda-line-9be1a4d25d76a815",
        "makefile-line-04aa358fc4ea11c8",
    }
)
ORACLE_DISPOSITIONS = frozenset({"clean", "extraction_invalid", "ambiguous"})
ALLOWED_EXCEPTION_STATUSES = frozenset(
    {
        "ambiguous",
        "cleaning_policy_dispute",
        "cross_run_reviewer_conflict",
        "extraction_invalid",
        "intra_corpus_oracle_conflict",
        "oracle_contains_cr",
        "oracle_expected_not_utf8",
        "oracle_not_deletion_only",
        "reviewer_disagreement",
    }
)
CASE_CATEGORIES = (
    "sanitizer",
    "extractor_boundary",
    "oracle_exception",
)
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
SOURCE_ID_PATTERN = re.compile(r"[0-9a-f]{40}")
SAFE_FAMILY_PATTERN = re.compile(r"[a-z0-9_]+")

MANIFEST_KEYS = frozenset(
    {
        "case_count",
        "case_category_counts",
        "case_category_id_set_sha256",
        "case_id_set_sha256",
        "comment_kind_counts",
        "disposition_counts",
        "exception_status_counts",
        "schema_version",
        "shards",
        "source",
    }
)
MANIFEST_SOURCE_KEYS = frozenset(
    {
        "annotations_sha256",
        "candidate_set_sha256",
        "dataset",
        "failures_sha256",
        "manifest_sha256",
        "oracle_exceptions_sha256",
        "primary_model",
        "run_summary_sha256",
        "secondary_model",
    }
)
SHARD_DESCRIPTOR_KEYS = frozenset(
    {
        "case_count",
        "extractor_boundary_case_count",
        "family_name",
        "filename",
        "oracle_exception_case_count",
        "sanitizer_case_count",
        "sha256",
    }
)
SHARD_KEYS = frozenset(
    {
        "extractor_boundary_cases",
        "family_name",
        "oracle_exception_cases",
        "sanitizer_cases",
        "schema_version",
    }
)
COMMON_CASE_KEYS = frozenset(
    {
        "baseline_cleaned_sha256",
        "case_id",
        "comment_kind",
        "language",
        "raw_sha256",
        "raw_utf8_length",
        "source_provenance",
        "syntax_label",
    }
)
SOURCE_PROVENANCE_KEYS = frozenset(
    {
        "source_excerpt_sha256",
        "source_id",
    }
)
SANITIZER_CASE_KEYS = frozenset(
    COMMON_CASE_KEYS
    | {
        "disposition",
        "expected_cleaned",
        "expected_cleaned_sha256",
        "raw_comment",
    }
)
EXCEPTION_CASE_KEYS = frozenset(
    COMMON_CASE_KEYS
    | {
        "disposition",
        "exception_status",
        "oracle_exception_record_sha256",
    }
)
EXECUTABLE_EXCEPTION_CASE_KEYS = frozenset(
    EXCEPTION_CASE_KEYS
    | {
        "expected_cleaned",
        "expected_cleaned_sha256",
        "raw_comment",
    }
)
EXTRACTOR_BOUNDARY_CASE_KEYS = frozenset(EXCEPTION_CASE_KEYS | {"boundary_assertion"})
EXECUTABLE_EXTRACTOR_BOUNDARY_CASE_KEYS = frozenset(
    EXTRACTOR_BOUNDARY_CASE_KEYS | {"boundary_probe"}
)
ORACLE_EXCEPTION_KEYS = frozenset(
    {
        "case_id",
        "comment_kind",
        "detail",
        "extraction_boundary_invalid",
        "language",
        "proposal",
        "raw_sha256",
        "resolution",
        "review",
        "reviewers",
        "schema_version",
        "status",
        "syntax_label",
    }
)
PROPOSAL_RESULT_KEYS = frozenset(
    {
        "confidence",
        "disposition",
        "expected_cleaned",
        "model",
        "rationale",
    }
)
REVIEW_RESULT_KEYS = frozenset(PROPOSAL_RESULT_KEYS | {"decision"})
RESOLUTION_RESULT_KEYS = frozenset({"confidence", "decision", "model", "rationale"})
BOUNDARY_ASSERTION_KEYS = frozenset({"expected_match", "expected_match_sha256", "kind"})
BOUNDARY_PROBE_KEYS = frozenset(
    {
        "kind",
        "raw_comment",
        "raw_sha256",
        "raw_utf8_length",
    }
)


@dataclass(frozen=True)
class SanitizerRegressionCase:
    """One exact raw-to-cleaned oracle loaded from a reviewed fixture shard."""

    case_id: str
    language: str
    family_name: str
    comment_kind: str
    raw_comment: str
    expected_cleaned: str


@dataclass(frozen=True)
class ExtractorBoundaryCase:
    """One invalid extraction with an optional executable corrected boundary."""

    case_id: str
    language: str
    family_name: str
    comment_kind: str
    raw_comment: str
    expected_match: str | None
    query_kind: str | None
    disposition: str


@dataclass(frozen=True)
class OracleExceptionCase:
    """One non-literal oracle outcome retained for exact corpus accounting."""

    case_id: str
    language: str
    family_name: str
    comment_kind: str
    status: str
    disposition: str


@dataclass(frozen=True)
class RegressionCorpus:
    """The validated committed regression manifest and all of its cases."""

    manifest: Mapping[str, Any]
    sanitizer_cases: tuple[SanitizerRegressionCase, ...]
    extractor_boundary_cases: tuple[ExtractorBoundaryCase, ...]
    oracle_exception_cases: tuple[OracleExceptionCase, ...]


def _load_importer_module():
    script_path = PROJECT_ROOT / "scripts" / "import_comment_cleaning_regressions.py"
    spec = importlib.util.spec_from_file_location(
        "import_comment_cleaning_regressions",
        script_path,
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


IMPORTER = _load_importer_module()


def _duplicate_rejecting_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AssertionError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _load_json_text(text: str, context: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=_duplicate_rejecting_object)
    except (json.JSONDecodeError, AssertionError) as exc:
        raise AssertionError(f"{context}: invalid JSON: {exc}") from exc
    assert isinstance(value, dict), f"{context}: expected a JSON object"
    return value


def _canonical_json(value: Any) -> str:
    return (
        json.dumps(
            value,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def _load_canonical_json(path: Path) -> tuple[dict[str, Any], str]:
    raw_bytes = path.read_bytes()
    text = raw_bytes.decode("utf-8")
    value = _load_json_text(text, str(path))
    assert text == _canonical_json(value), f"{path}: JSON is not canonical"
    return value, hashlib.sha256(raw_bytes).hexdigest()


def _require_exact_keys(
    value: Mapping[str, Any],
    expected: frozenset[str],
    context: str,
) -> None:
    actual = frozenset(value)
    assert actual == expected, (
        f"{context}: keys differ; missing={sorted(expected - actual)!r} "
        f"extra={sorted(actual - expected)!r}"
    )


def _require_string(
    value: Mapping[str, Any],
    key: str,
    context: str,
    *,
    allow_empty: bool = False,
) -> str:
    result = value.get(key)
    assert isinstance(result, str), f"{context}.{key}: expected a string"
    if not allow_empty:
        assert result, f"{context}.{key}: expected a non-empty string"
    return result


def _require_sha256(value: Mapping[str, Any], key: str, context: str) -> str:
    result = _require_string(value, key, context)
    assert SHA256_PATTERN.fullmatch(result), (
        f"{context}.{key}: expected lowercase hexadecimal SHA-256"
    )
    return result


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _case_id_set_sha256(case_ids) -> str:
    ordered = sorted(case_ids)
    assert all(case_id and "\n" not in case_id and "\r" not in case_id for case_id in ordered)
    return _sha256_text("".join(f"{case_id}\n" for case_id in ordered))


def _normalize_newlines(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def _is_subsequence(expected: str, normalized_raw: str) -> bool:
    position = 0
    for character in expected:
        position = normalized_raw.find(character, position)
        if position < 0:
            return False
        position += 1
    return True


def _validated_common_case(
    row: Mapping[str, Any],
    *,
    expected_keys: frozenset[str],
    family_name: str,
    context: str,
    require_raw: bool,
) -> tuple[str, str, str, str]:
    _require_exact_keys(row, expected_keys, context)
    case_id = _require_string(row, "case_id", context)
    language = _require_string(row, "language", context)
    comment_kind = _require_string(row, "comment_kind", context)
    syntax_label = _require_string(row, "syntax_label", context, allow_empty=True)
    del syntax_label

    raw_sha256 = _require_sha256(row, "raw_sha256", context)
    _require_sha256(row, "baseline_cleaned_sha256", context)
    source_provenance = row.get("source_provenance")
    assert isinstance(source_provenance, dict), f"{context}.source_provenance: expected an object"
    _require_exact_keys(
        source_provenance,
        SOURCE_PROVENANCE_KEYS,
        f"{context}.source_provenance",
    )
    source_id = _require_string(
        source_provenance,
        "source_id",
        f"{context}.source_provenance",
    )
    assert SOURCE_ID_PATTERN.fullmatch(source_id), (
        f"{context}.source_provenance.source_id: expected 40 lowercase hexadecimal characters"
    )
    _require_sha256(
        source_provenance,
        "source_excerpt_sha256",
        f"{context}.source_provenance",
    )
    raw_utf8_length = row.get("raw_utf8_length")
    assert isinstance(raw_utf8_length, int) and raw_utf8_length >= 0
    if require_raw:
        raw_comment = _require_string(row, "raw_comment", context, allow_empty=True)
        assert raw_sha256 == _sha256_text(raw_comment), (
            f"{context}: raw_sha256 does not match raw_comment"
        )
        assert raw_utf8_length == len(raw_comment.encode("utf-8"))
    else:
        assert "raw_comment" not in row
        raw_comment = ""

    syntax = get_comment_syntax(language)
    assert syntax.family_name == family_name, (
        f"{context}: registry family {syntax.family_name!r} does not match "
        f"shard family {family_name!r}"
    )
    return case_id, language, comment_kind, raw_comment


def _validated_sanitizer_case(
    row: Mapping[str, Any],
    *,
    family_name: str,
    context: str,
) -> SanitizerRegressionCase:
    case_id, language, comment_kind, raw_comment = _validated_common_case(
        row,
        expected_keys=SANITIZER_CASE_KEYS,
        family_name=family_name,
        context=context,
        require_raw=True,
    )
    disposition = _require_string(row, "disposition", context)
    assert disposition in ALLOWED_DISPOSITIONS, (
        f"{context}.disposition: unsupported value {disposition!r}"
    )
    expected_cleaned = _require_string(row, "expected_cleaned", context, allow_empty=True)
    expected_sha256 = _require_sha256(row, "expected_cleaned_sha256", context)
    baseline_sha256 = _require_sha256(row, "baseline_cleaned_sha256", context)
    assert expected_sha256 == _sha256_text(expected_cleaned), (
        f"{context}: expected_cleaned_sha256 does not match expected_cleaned"
    )
    assert "\r" not in expected_cleaned, f"{context}: expected_cleaned must use LF newlines"
    assert _is_subsequence(expected_cleaned, _normalize_newlines(raw_comment)), (
        f"{context}: expected_cleaned is not a deletion-only cleaning of raw_comment"
    )
    if disposition == "confirmed_bug":
        assert expected_sha256 != baseline_sha256, (
            f"{context}: confirmed bug equals the frozen baseline"
        )
    elif disposition == "judge_false_positive":
        assert expected_sha256 == baseline_sha256, (
            f"{context}: false-positive oracle differs from the frozen baseline"
        )
    else:
        assert disposition == "adjudicated_override"
        assert case_id in ADJUDICATED_OVERRIDE_IDS

    return SanitizerRegressionCase(
        case_id=case_id,
        language=language,
        family_name=family_name,
        comment_kind=comment_kind,
        raw_comment=raw_comment,
        expected_cleaned=expected_cleaned,
    )


def _validated_compact_exception(
    row: Mapping[str, Any],
    *,
    context: str,
) -> tuple[str, str]:
    status = _require_string(row, "exception_status", context)
    assert status in ALLOWED_EXCEPTION_STATUSES
    source_record_sha256 = _require_sha256(
        row,
        "oracle_exception_record_sha256",
        context,
    )
    return status, source_record_sha256


def _validated_extractor_boundary_case(
    row: Mapping[str, Any],
    *,
    family_name: str,
    context: str,
) -> ExtractorBoundaryCase:
    disposition = _require_string(row, "disposition", context)
    executable = disposition == "executable_regression"
    assert disposition in {"accounting_only", "executable_regression"}
    case_id, language, comment_kind, raw_comment = _validated_common_case(
        row,
        expected_keys=(
            EXECUTABLE_EXTRACTOR_BOUNDARY_CASE_KEYS if executable else EXTRACTOR_BOUNDARY_CASE_KEYS
        ),
        family_name=family_name,
        context=context,
        require_raw=False,
    )
    status, _ = _validated_compact_exception(
        row,
        context=context,
    )
    assert status == "extraction_invalid"

    assertion = row.get("boundary_assertion")
    if assertion is None:
        assert not executable
        expected_match = None
    else:
        assert executable
        probe = row.get("boundary_probe")
        assert isinstance(probe, dict)
        _require_exact_keys(
            probe,
            BOUNDARY_PROBE_KEYS,
            f"{context}.boundary_probe",
        )
        assert probe.get("kind") == "synthetic_structural_probe"
        raw_comment = _require_string(
            probe,
            "raw_comment",
            f"{context}.boundary_probe",
        )
        assert _require_sha256(
            probe,
            "raw_sha256",
            f"{context}.boundary_probe",
        ) == _sha256_text(raw_comment)
        assert probe.get("raw_utf8_length") == len(raw_comment.encode("utf-8"))
        assert isinstance(assertion, dict)
        _require_exact_keys(
            assertion,
            BOUNDARY_ASSERTION_KEYS,
            f"{context}.boundary_assertion",
        )
        query_kind = assertion.get("kind")
        assert query_kind in {
            "comment_query_first_embedded_match",
            "comment_query_first_match",
            "line_query_first_match",
        }
        expected_match = _require_string(
            assertion,
            "expected_match",
            f"{context}.boundary_assertion",
        )
        assert _require_sha256(
            assertion,
            "expected_match_sha256",
            f"{context}.boundary_assertion",
        ) == _sha256_text(expected_match)
        if query_kind == "comment_query_first_embedded_match":
            assert expected_match in raw_comment
            assert not raw_comment.startswith(expected_match)
        else:
            assert raw_comment.startswith(expected_match)
        assert len(raw_comment) > len(expected_match)
    if assertion is None:
        query_kind = None

    return ExtractorBoundaryCase(
        case_id=case_id,
        language=language,
        family_name=family_name,
        comment_kind=comment_kind,
        raw_comment=raw_comment,
        expected_match=expected_match,
        query_kind=query_kind,
        disposition=disposition,
    )


def _validated_oracle_exception_case(
    row: Mapping[str, Any],
    *,
    family_name: str,
    context: str,
) -> OracleExceptionCase:
    disposition = _require_string(row, "disposition", context)
    executable = disposition == "executable_regression"
    assert disposition in {"accounting_only", "executable_regression"}
    case_id, language, comment_kind, raw_comment = _validated_common_case(
        row,
        expected_keys=(EXECUTABLE_EXCEPTION_CASE_KEYS if executable else EXCEPTION_CASE_KEYS),
        family_name=family_name,
        context=context,
        require_raw=executable,
    )
    status, _ = _validated_compact_exception(
        row,
        context=context,
    )
    if executable:
        expected_cleaned = _require_string(
            row,
            "expected_cleaned",
            context,
            allow_empty=True,
        )
        assert _require_sha256(
            row,
            "expected_cleaned_sha256",
            context,
        ) == _sha256_text(expected_cleaned)
        assert _is_subsequence(expected_cleaned, _normalize_newlines(raw_comment))
    return OracleExceptionCase(
        case_id=case_id,
        language=language,
        family_name=family_name,
        comment_kind=comment_kind,
        status=status,
        disposition=disposition,
    )


def _load_regression_corpus() -> Optional[RegressionCorpus]:
    if not FIXTURE_DIR.exists():
        return None
    json_paths = sorted(FIXTURE_DIR.glob("*.json"))
    if not MANIFEST_PATH.exists():
        assert not json_paths, f"{FIXTURE_DIR}: fixture JSON exists without _manifest.json"
        return None

    manifest, _ = _load_canonical_json(MANIFEST_PATH)
    _require_exact_keys(manifest, MANIFEST_KEYS, str(MANIFEST_PATH))
    assert manifest.get("schema_version") == SCHEMA_VERSION
    assert manifest.get("case_count") == EXPECTED_CASE_COUNT
    assert manifest.get("case_id_set_sha256") == EXPECTED_CASE_ID_SET_SHA256

    source = manifest.get("source")
    assert isinstance(source, dict), f"{MANIFEST_PATH}.source: expected an object"
    _require_exact_keys(source, MANIFEST_SOURCE_KEYS, f"{MANIFEST_PATH}.source")
    assert source.get("failures_sha256") == EXPECTED_FAILURES_SHA256
    assert source.get("run_summary_sha256") == EXPECTED_RUN_SUMMARY_SHA256
    assert source.get("manifest_sha256") == EXPECTED_SOURCE_MANIFEST_SHA256
    assert source.get("dataset") == "bigcode/the-stack-v2-dedup"
    assert source.get("primary_model") == EXPECTED_PRIMARY_MODEL
    assert source.get("secondary_model") == EXPECTED_SECONDARY_MODEL
    for key in (
        "annotations_sha256",
        "candidate_set_sha256",
        "oracle_exceptions_sha256",
    ):
        _require_sha256(source, key, f"{MANIFEST_PATH}.source")

    descriptors = manifest.get("shards")
    assert isinstance(descriptors, list) and descriptors, (
        f"{MANIFEST_PATH}.shards: expected a non-empty array"
    )
    descriptor_families = []
    expected_filenames = {"_manifest.json"}
    sanitizer_cases = []
    extractor_boundary_cases = []
    oracle_exception_cases = []
    seen_case_ids = set()
    case_ids_by_category = {category: set() for category in CASE_CATEGORIES}
    case_category_counts: Counter[str] = Counter()
    disposition_counts: Counter[str] = Counter()
    exception_status_counts: Counter[str] = Counter()
    comment_kind_counts: Counter[str] = Counter()

    for descriptor_index, descriptor in enumerate(descriptors):
        descriptor_context = f"{MANIFEST_PATH}.shards[{descriptor_index}]"
        assert isinstance(descriptor, dict), f"{descriptor_context}: expected an object"
        _require_exact_keys(
            descriptor,
            SHARD_DESCRIPTOR_KEYS,
            descriptor_context,
        )
        family_name = _require_string(descriptor, "family_name", descriptor_context)
        assert SAFE_FAMILY_PATTERN.fullmatch(family_name), (
            f"{descriptor_context}: unsafe family name {family_name!r}"
        )
        filename = _require_string(descriptor, "filename", descriptor_context)
        assert filename == f"{family_name}.json", (
            f"{descriptor_context}: filename does not match family_name"
        )
        descriptor_families.append(family_name)
        expected_filenames.add(filename)

        shard_path = FIXTURE_DIR / filename
        shard, shard_sha256 = _load_canonical_json(shard_path)
        assert shard_sha256 == _require_sha256(descriptor, "sha256", descriptor_context)
        _require_exact_keys(shard, SHARD_KEYS, str(shard_path))
        assert shard.get("schema_version") == SCHEMA_VERSION
        assert shard.get("family_name") == family_name
        shard_case_count = 0
        category_specs = (
            (
                "sanitizer",
                "sanitizer_cases",
                "sanitizer_case_count",
                _validated_sanitizer_case,
                sanitizer_cases,
            ),
            (
                "extractor_boundary",
                "extractor_boundary_cases",
                "extractor_boundary_case_count",
                _validated_extractor_boundary_case,
                extractor_boundary_cases,
            ),
            (
                "oracle_exception",
                "oracle_exception_cases",
                "oracle_exception_case_count",
                _validated_oracle_exception_case,
                oracle_exception_cases,
            ),
        )
        for (
            category,
            shard_key,
            descriptor_key,
            validator,
            destination,
        ) in category_specs:
            shard_rows = shard.get(shard_key)
            assert isinstance(shard_rows, list), f"{shard_path}.{shard_key}: expected an array"
            assert descriptor.get(descriptor_key) == len(shard_rows)
            shard_case_count += len(shard_rows)

            shard_cases = []
            for case_index, row in enumerate(shard_rows):
                context = f"{shard_path}.{shard_key}[{case_index}]"
                assert isinstance(row, dict), f"{context}: expected an object"
                case = validator(
                    row,
                    family_name=family_name,
                    context=context,
                )
                assert case.case_id not in seen_case_ids, (
                    f"{context}: duplicate case_id {case.case_id!r}"
                )
                seen_case_ids.add(case.case_id)
                case_ids_by_category[category].add(case.case_id)
                case_category_counts[category] += 1
                comment_kind_counts.update([case.comment_kind])
                shard_cases.append(case)
                if category == "sanitizer":
                    disposition_counts.update([row["disposition"]])
                else:
                    exception_status_counts.update([row["exception_status"]])
            assert shard_cases == sorted(
                shard_cases,
                key=lambda case: (case.language, case.case_id),
            ), f"{shard_path}.{shard_key}: cases are not in canonical order"
            destination.extend(shard_cases)
        assert descriptor.get("case_count") == shard_case_count
        assert shard_case_count > 0, f"{shard_path}: shard contains no cases"

    assert descriptor_families == sorted(descriptor_families), (
        f"{MANIFEST_PATH}: shards are not in canonical family order"
    )
    actual_filenames = {path.name for path in json_paths}
    assert actual_filenames == expected_filenames, (
        f"{FIXTURE_DIR}: JSON file set differs; "
        f"missing={sorted(expected_filenames - actual_filenames)!r} "
        f"extra={sorted(actual_filenames - expected_filenames)!r}"
    )
    all_cases = sanitizer_cases + extractor_boundary_cases + oracle_exception_cases
    assert len(all_cases) == EXPECTED_CASE_COUNT
    assert _case_id_set_sha256(seen_case_ids) == EXPECTED_CASE_ID_SET_SHA256
    assert manifest.get("case_category_counts") == {
        category: case_category_counts[category] for category in CASE_CATEGORIES
    }
    assert manifest.get("case_category_id_set_sha256") == {
        category: _case_id_set_sha256(case_ids_by_category[category])
        for category in CASE_CATEGORIES
    }
    assert manifest.get("disposition_counts") == dict(sorted(disposition_counts.items()))
    assert manifest.get("exception_status_counts") == dict(sorted(exception_status_counts.items()))
    assert manifest.get("comment_kind_counts") == dict(sorted(comment_kind_counts.items()))
    return RegressionCorpus(
        manifest=manifest,
        sanitizer_cases=tuple(sanitizer_cases),
        extractor_boundary_cases=tuple(extractor_boundary_cases),
        oracle_exception_cases=tuple(oracle_exception_cases),
    )


REGRESSION_CORPUS = _load_regression_corpus()
SANITIZER_REGRESSION_CASES = (
    REGRESSION_CORPUS.sanitizer_cases if REGRESSION_CORPUS is not None else ()
)
EXTRACTOR_BOUNDARY_CASES = (
    REGRESSION_CORPUS.extractor_boundary_cases if REGRESSION_CORPUS is not None else ()
)
EXECUTABLE_EXTRACTOR_BOUNDARY_CASES = tuple(
    case for case in EXTRACTOR_BOUNDARY_CASES if case.expected_match is not None
)
ACCOUNTING_ONLY_EXTRACTOR_BOUNDARY_CASES = tuple(
    case for case in EXTRACTOR_BOUNDARY_CASES if case.expected_match is None
)


def test_comment_cleaning_regression_corpus_is_complete_and_integral():
    if REGRESSION_CORPUS is None:
        pytest.skip("reviewed comment-cleaning regression fixtures are not imported yet")

    assert (
        len(REGRESSION_CORPUS.sanitizer_cases)
        + len(REGRESSION_CORPUS.extractor_boundary_cases)
        + len(REGRESSION_CORPUS.oracle_exception_cases)
        == EXPECTED_CASE_COUNT
    )


def test_rendered_cases_keep_only_executable_literals_and_compact_integrity():
    executable_exception_ids = set()
    adjudicated_override_ids = set()
    provenance_case_ids = set()
    boundary_probe_count = 0
    for path in FIXTURE_DIR.glob("*.json"):
        if path.name == "_manifest.json":
            continue
        shard = json.loads(path.read_text(encoding="utf-8"))
        for section in (
            "sanitizer_cases",
            "extractor_boundary_cases",
            "oracle_exception_cases",
        ):
            for row in shard[section]:
                assert row["case_id"] not in provenance_case_ids
                provenance_case_ids.add(row["case_id"])
                assert set(row["source_provenance"]) == SOURCE_PROVENANCE_KEYS
                assert SOURCE_ID_PATTERN.fullmatch(row["source_provenance"]["source_id"])
                assert SHA256_PATTERN.fullmatch(row["source_provenance"]["source_excerpt_sha256"])
                assert "source" not in row
                assert "repo" not in row
                assert "path" not in row
                assert "source_excerpt" not in row
                assert "judge" not in row
                assert "oracle" not in row
                assert "oracle_exception" not in row
                if row.get("disposition") == "accounting_only":
                    assert "raw_comment" not in row
                    assert "expected_cleaned" not in row
                    assert "boundary_probe" not in row
                if (
                    section == "extractor_boundary_cases"
                    and row.get("disposition") == "executable_regression"
                ):
                    boundary_probe_count += 1
                    assert "raw_comment" not in row
                    assert row["boundary_probe"]["kind"] == "synthetic_structural_probe"
                    assert row["boundary_probe"]["raw_utf8_length"] <= 32
                if row.get("disposition") == "adjudicated_override":
                    adjudicated_override_ids.add(row["case_id"])
                if (
                    section == "oracle_exception_cases"
                    and row.get("disposition") == "executable_regression"
                ):
                    executable_exception_ids.add(row["case_id"])

    assert executable_exception_ids == {"ant_build_system-block-a4061d3caf4c1257"}
    assert adjudicated_override_ids == ADJUDICATED_OVERRIDE_IDS
    assert boundary_probe_count == 32
    assert len(provenance_case_ids) == EXPECTED_CASE_COUNT
    assert _case_id_set_sha256(provenance_case_ids) == EXPECTED_CASE_ID_SET_SHA256


def test_regression_fixture_provenance_and_importer_sentinel_are_committed():
    notice = (FIXTURE_DIR / IMPORTER.NOTICE_NAME).read_text(encoding="utf-8")
    sentinel = (FIXTURE_DIR / IMPORTER.SENTINEL_NAME).read_text(encoding="utf-8")

    assert "`bigcode/the-stack-v2-dedup`" in notice
    assert "Software Heritage" in notice
    assert "40-hex Stack v2 source ID" in notice
    assert "SHA-256 of its source" in notice
    assert "exact per-file license metadata" in notice
    assert "synthetic structural probes" in notice
    assert sentinel == IMPORTER.SENTINEL_CONTENT


@pytest.mark.parametrize(
    "case",
    SANITIZER_REGRESSION_CASES,
    ids=[case.case_id for case in SANITIZER_REGRESSION_CASES],
)
def test_comment_cleaning_regression_matches_all_public_sanitizer_apis(case):
    raw_match = QueryMatch("", "", case.raw_comment)
    sanitizer = CommentSanitizer(case.language)

    assert sanitizer.sanitize(case.raw_comment) == case.expected_cleaned
    assert sanitizer.sanitize(raw_match) == case.expected_cleaned
    assert sanitize_comment(case.language, case.raw_comment) == case.expected_cleaned
    assert sanitize_comment_text(case.language, raw_match) == case.expected_cleaned


@pytest.mark.parametrize(
    "case",
    EXECUTABLE_EXTRACTOR_BOUNDARY_CASES,
    ids=[case.case_id for case in EXECUTABLE_EXTRACTOR_BOUNDARY_CASES],
)
def test_invalid_extraction_stops_at_reconstructed_boundary(case):
    if case.query_kind == "comment_query_first_embedded_match":
        matches = CommentQuery(case.language).parse(case.raw_comment)

        assert matches
        assert matches[0].prefix
        assert matches[0].match == case.expected_match
        assert all(match.match != case.raw_comment for match in matches)
        return

    query_type = (
        CommentQuery if case.query_kind == "comment_query_first_match" else LineCommentQuery
    )
    matches = query_type(case.language).parse(case.raw_comment)

    assert matches
    assert matches[0].prefix == ""
    assert matches[0].match == case.expected_match


@pytest.mark.parametrize(
    "case",
    ACCOUNTING_ONLY_EXTRACTOR_BOUNDARY_CASES,
    ids=[case.case_id for case in ACCOUNTING_ONLY_EXTRACTOR_BOUNDARY_CASES],
)
def test_nonreconstructable_extractor_regression_is_hash_only_accounting(case):
    assert case.disposition == "accounting_only"
    assert case.raw_comment == ""


def _source_failure(
    case_id: str,
    raw_comment: str,
) -> Any:
    return IMPORTER.SourceFailure(
        case_id=case_id,
        language="python",
        family_name="hash_style",
        comment_kind="line",
        syntax_label="#",
        repo="owner/repo",
        path=f"src/{case_id}.py",
        raw_comment=raw_comment,
        candidate_cleaned_comment=f"baseline:{case_id}",
        cleaning_contract="Delete syntax scaffolding; preserve content.",
        judge_input_sha256="1" * 64,
        judge_rationale="The rejected candidate retained scaffolding.",
        primary_model=EXPECTED_PRIMARY_MODEL,
        secondary_model=EXPECTED_SECONDARY_MODEL,
        primary_cleaning_correct=False,
        secondary_cleaning_correct=False,
    )


def _source_provenance_for(
    failures: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        case_id: IMPORTER.SourceProvenance(
            source_id=_sha256_text(f"source-id:{case_id}")[:40],
            source_excerpt_sha256=_sha256_text(f"source-excerpt:{case_id}"),
        )
        for case_id in failures
    }


def _source_manifest_row(
    failure: Any,
    *,
    source_id: str,
    source_excerpt: str,
) -> dict[str, Any]:
    return {
        "case_id": failure.case_id,
        "comment_kind": failure.comment_kind,
        "language": failure.language,
        "raw_comment": failure.raw_comment,
        "source_excerpt": source_excerpt,
        "source_id": source_id,
        "syntax_label": failure.syntax_label,
    }


def _write_source_manifest(path: Path, rows: list[Mapping[str, Any]]) -> bytes:
    payload = "".join(
        json.dumps(
            row,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n"
        for row in rows
    ).encode("utf-8")
    path.write_bytes(payload)
    return payload


def test_source_manifest_streaming_selects_exact_failure_provenance_and_hash(
    tmp_path: Path,
):
    first = _source_failure("first", "# first")
    second = _source_failure("second", "# second")
    unrelated = _source_failure("unrelated", "# unrelated")
    failures = {first.case_id: first, second.case_id: second}
    path = tmp_path / "manifest.jsonl"
    payload = _write_source_manifest(
        path,
        [
            _source_manifest_row(
                first,
                source_id="1" * 40,
                source_excerpt="before\u2028after",
            ),
            _source_manifest_row(
                unrelated,
                source_id="2" * 40,
                source_excerpt="not selected",
            ),
            _source_manifest_row(
                second,
                source_id="3" * 40,
                source_excerpt="before\u2029after",
            ),
        ],
    )

    provenance, source_manifest_sha256 = IMPORTER._load_source_provenance(
        path,
        failures,
    )

    assert source_manifest_sha256 == hashlib.sha256(payload).hexdigest()
    assert provenance == {
        "first": IMPORTER.SourceProvenance(
            source_id="1" * 40,
            source_excerpt_sha256=_sha256_text("before\u2028after"),
        ),
        "second": IMPORTER.SourceProvenance(
            source_id="3" * 40,
            source_excerpt_sha256=_sha256_text("before\u2029after"),
        ),
    }


def test_source_manifest_identity_tamper_is_rejected(tmp_path: Path):
    failure = _source_failure("case", "# case")
    row = _source_manifest_row(
        failure,
        source_id="1" * 40,
        source_excerpt="excerpt",
    )
    row["raw_comment"] = "# tampered"
    path = tmp_path / "manifest.jsonl"
    _write_source_manifest(path, [row])

    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="identity differs.*raw_comment",
    ):
        IMPORTER._load_source_provenance(path, {failure.case_id: failure})


def test_source_manifest_missing_failure_is_rejected(tmp_path: Path):
    failure = _source_failure("missing", "# missing")
    unrelated = _source_failure("unrelated", "# unrelated")
    path = tmp_path / "manifest.jsonl"
    _write_source_manifest(
        path,
        [
            _source_manifest_row(
                unrelated,
                source_id="1" * 40,
                source_excerpt="excerpt",
            )
        ],
    )

    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="does not cover every frozen failure.*missing_count=1",
    ):
        IMPORTER._load_source_provenance(path, {failure.case_id: failure})


def test_source_manifest_duplicate_case_id_is_rejected_after_selected_rows(
    tmp_path: Path,
):
    failure = _source_failure("selected", "# selected")
    unrelated = _source_failure("duplicate", "# duplicate")
    duplicate_row = _source_manifest_row(
        unrelated,
        source_id="2" * 40,
        source_excerpt="duplicate excerpt",
    )
    path = tmp_path / "manifest.jsonl"
    _write_source_manifest(
        path,
        [
            _source_manifest_row(
                failure,
                source_id="1" * 40,
                source_excerpt="selected excerpt",
            ),
            duplicate_row,
            duplicate_row,
        ],
    )

    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="duplicate case_id 'duplicate'",
    ):
        IMPORTER._load_source_provenance(path, {failure.case_id: failure})


def _smalltalk_source_failure(
    case_id: str,
    raw_comment: str,
) -> Any:
    return IMPORTER.SourceFailure(
        case_id=case_id,
        language="smalltalk",
        family_name="smalltalk_style",
        comment_kind="line",
        syntax_label='"..."',
        repo="owner/repo",
        path=f"src/{case_id}.st",
        raw_comment=raw_comment,
        candidate_cleaned_comment=f"baseline:{case_id}",
        cleaning_contract="Delete syntax scaffolding; preserve content.",
        judge_input_sha256="1" * 64,
        judge_rationale="The rejected extraction swallowed source after the closing quote.",
        primary_model=EXPECTED_PRIMARY_MODEL,
        secondary_model=EXPECTED_SECONDARY_MODEL,
        primary_cleaning_correct=False,
        secondary_cleaning_correct=False,
    )


@pytest.mark.parametrize("comment_kind", ["block", "nested"])
def test_portugol_whole_program_boundary_reconstructs_first_embedded_comment(
    comment_kind: str,
):
    raw_program = "{\n/* real comment */\nfuncao inicio() {\n}\n}"
    failure = replace(
        _source_failure("portugol-whole-program", raw_program),
        language="portugol",
        family_name="portugol_style",
        comment_kind=comment_kind,
        syntax_label="{...}",
    )

    assertion = IMPORTER._reconstruct_boundary_assertion(failure)
    matches = CommentQuery("portugol").parse(raw_program)

    assert assertion == {
        "expected_match": "/* real comment */",
        "expected_match_sha256": _sha256_text("/* real comment */"),
        "kind": "comment_query_first_embedded_match",
    }
    assert matches[0].prefix == "{\n"
    assert matches[0].match == assertion["expected_match"]
    assert all(match.match != raw_program for match in matches)


@pytest.mark.parametrize(
    ("case_id", "expected_match", "following_source"),
    [
        (
            "smalltalk-line-2e6632a531961deb",
            '"cm3"',
            " ]! !\r\r\x0c\rPasajero subclass: #PasajeroModerado",
        ),
        (
            "smalltalk-line-3d38075168c16eed",
            '"\r\tClosureTests new testIsClean\r\t"',
            "\r\t| tempVar |\r\ttempVar _ 1.",
        ),
        (
            "smalltalk-line-5789174dcc00f651",
            (
                '"Change Set:\t\tcruftRemoval\rDate:\t\t\t12 April 2001\r'
                "Author:\t\t\tBob Arning\r\rremoves some unneeded cruft from "
                'ButtonProperties"'
            ),
            "!\r\rButtonProperties class removeSelector: #additionsToViewerCategories!",
        ),
        (
            "smalltalk-line-7edd7c6c125d30e9",
            '"-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- "',
            "!\r\rSmaCCDefinitionParser class\r\tinstanceVariableNames: ''!",
        ),
        (
            "smalltalk-line-8d5cceb396799450",
            (
                '"Change Set:\t\tredCar-sw\rDate:\t\t\t25 May 2000\r'
                "Author:\t\t\tScott Wallace\r\rUnrelated fixes to prolems "
                'encountered with a simulation project sent by bj allen-conn"'
            ),
            "!\r\r\r!TileMorph methodsFor: 'misc'!",
        ),
        (
            "smalltalk-line-b2a2da20a949ab9a",
            (
                '"Change Set:\t\tSundryFixes-di\rDate:\t\t\t4 October 1999\r'
                "Author:\t\t\tDan Ingalls\r\rRestores proper operation of "
                "roundTo: and amends its comment (reported by Andrew Greenberg).\r"
                "Fixes a Interpreter>>printNameOfClass:count: for the third time "
                "(reported by Tom Morgan).\rFixes a bug in AcornFileDirectory root "
                "testing exposed by RISC OS4 (fixed by Tim Rowledge).\r"
                '"'
            ),
            "!\r\r\r!AcornFileDirectory methodsFor: 'testing'!",
        ),
        (
            "smalltalk-line-d79ebcfe84b46841",
            (
                '"Change Set:\t\tbetterThumbGIF\rDate:\t\t\t27 September 2000\r'
                "Author:\t\t\tBob Arning\r\r- fix project publish failures when "
                'thumbnail has more than 256 colors"'
            ),
            "!\r\r\r!Project methodsFor: 'file in/out'!",
        ),
        (
            "smalltalk-line-efc3bb48ec86d76e",
            (
                '"Change Set:\t\tFilePathFixes\rDate:\t\t\t18 December 1999\r'
                "Author:\t\t\tAndreas Raab\r\rFixes some of the confusion with "
                "returned values from #fullPathFor:. Should now consistently "
                "return a fully qualified path even for relative path names."
                '"'
            ),
            "!\r\r\r!FileDirectory methodsFor: 'path access'!",
        ),
    ],
)
def test_smalltalk_extraction_exceptions_reconstruct_paired_boundaries(
    case_id: str,
    expected_match: str,
    following_source: str,
):
    failure = _smalltalk_source_failure(
        case_id,
        expected_match + following_source,
    )

    assertion = IMPORTER._reconstruct_boundary_assertion(failure)

    assert assertion == {
        "expected_match": expected_match,
        "expected_match_sha256": _sha256_text(expected_match),
        "kind": "comment_query_first_match",
    }
    assert CommentQuery("smalltalk").parse(failure.raw_comment)[0].match == expected_match


@pytest.mark.parametrize(
    ("case_id", "language", "family_name", "comment_kind", "raw_comment"),
    [
        (
            "m-line-b3fd332a7a0d9dbc",
            "m",
            "semicolon_style",
            "line",
            ";\r  J=0;\r  %初始化\r  J = sum((x*theta-y).^2)/(2*m);\r  %计算损失\rend\r",
        ),
        (
            "moocode-block-2a9397d581c78266",
            "moocode",
            "c_block_style",
            "block",
            (
                "/**************************************************************************\r\n"
                "// IMAGE #2 - mislabeled C source\r\n"
                '#include "ri.h"\r\n'
                "/* nested-looking source */"
            ),
        ),
    ],
)
def test_language_misclassifications_remain_accounting_only(
    case_id: str,
    language: str,
    family_name: str,
    comment_kind: str,
    raw_comment: str,
):
    failure = replace(
        _source_failure(case_id, raw_comment),
        language=language,
        family_name=family_name,
        comment_kind=comment_kind,
    )

    assert IMPORTER._reconstruct_boundary_assertion(failure) is None


def _exception_payload(
    failure: Any,
    *,
    status: str,
    expected_cleaned: str = "",
    detail: str | None = None,
) -> dict[str, Any]:
    disposition = status if status in ORACLE_DISPOSITIONS else "clean"
    proposal = {
        "confidence": 0.9,
        "disposition": disposition,
        "expected_cleaned": expected_cleaned,
        "model": "gpt-5.6-sol",
        "rationale": f"Consensus status is {status}.",
    }
    review = {
        **proposal,
        "decision": "approve",
        "model": "gpt-5.6-luna",
    }
    return {
        "case_id": failure.case_id,
        "comment_kind": failure.comment_kind,
        "detail": detail or f"Reviewed {status} reason.",
        "extraction_boundary_invalid": status == "extraction_invalid",
        "language": failure.language,
        "proposal": proposal,
        "raw_sha256": _sha256_text(failure.raw_comment),
        "resolution": None,
        "review": review,
        "reviewers": ["gpt-5.6-luna", "gpt-5.6-sol"],
        "schema_version": ORACLE_EXCEPTION_SCHEMA_VERSION,
        "status": status,
        "syntax_label": failure.syntax_label,
    }


def test_schema_v5_renderer_partitions_every_failure_without_source_sized_literals(
    tmp_path: Path,
):
    exact_failure = _source_failure("exact", "# exact")
    boundary_failure = _source_failure("boundary", "# heading\rcode = 1")
    ambiguous_failure = _source_failure("ambiguous", "# maybe")
    failures = {
        failure.case_id: failure
        for failure in (
            exact_failure,
            boundary_failure,
            ambiguous_failure,
        )
    }
    expected = "exact"
    annotations = {
        "exact": IMPORTER.ReviewedOracle(
            case_id="exact",
            raw_sha256=_sha256_text(exact_failure.raw_comment),
            expected_cleaned=expected,
            expected_cleaned_sha256=_sha256_text(expected),
            disposition="confirmed_bug",
            method="sol_proposal_luna_exact_approval",
            note="Both reviewers agreed on the exact literal.",
            reviewers=("gpt-5.6-luna", "gpt-5.6-sol"),
        )
    }

    exceptions_path = tmp_path / "oracle_exceptions.jsonl"
    exception_payloads = [
        _exception_payload(
            boundary_failure,
            status="extraction_invalid",
        ),
        _exception_payload(
            ambiguous_failure,
            status="ambiguous",
        ),
    ]
    exceptions_path.write_text(
        "".join(json.dumps(payload, sort_keys=True) + "\n" for payload in exception_payloads),
        encoding="utf-8",
    )
    exceptions = IMPORTER._load_oracle_exceptions(exceptions_path)

    rendered = IMPORTER.build_rendered_fixtures(
        failures,
        _source_provenance_for(failures),
        annotations,
        exceptions,
        failures_sha256="2" * 64,
        run_summary_sha256="3" * 64,
        annotations_sha256="4" * 64,
        oracle_exceptions_sha256="5" * 64,
        source_summary={
            "candidate_set_sha256": "6" * 64,
            "manifest_sha256": "7" * 64,
            "primary_model": EXPECTED_PRIMARY_MODEL,
            "secondary_model": EXPECTED_SECONDARY_MODEL,
        },
    )

    manifest = json.loads(rendered["_manifest.json"])
    assert manifest["case_count"] == 3
    assert manifest["case_category_counts"] == {
        "sanitizer": 1,
        "extractor_boundary": 1,
        "oracle_exception": 1,
    }
    assert manifest["source"]["annotations_sha256"] == "4" * 64
    assert manifest["source"]["oracle_exceptions_sha256"] == "5" * 64
    assert manifest["case_id_set_sha256"] == _case_id_set_sha256(failures)
    assert manifest["case_category_id_set_sha256"] == {
        "sanitizer": _case_id_set_sha256(["exact"]),
        "extractor_boundary": _case_id_set_sha256(["boundary"]),
        "oracle_exception": _case_id_set_sha256(["ambiguous"]),
    }

    shard = json.loads(rendered["hash_style.json"])
    assert [row["case_id"] for row in shard["sanitizer_cases"]] == ["exact"]
    assert [row["case_id"] for row in shard["extractor_boundary_cases"]] == ["boundary"]
    assert [row["case_id"] for row in shard["oracle_exception_cases"]] == ["ambiguous"]
    boundary = shard["extractor_boundary_cases"][0]
    for section in (
        "sanitizer_cases",
        "extractor_boundary_cases",
        "oracle_exception_cases",
    ):
        for row in shard[section]:
            assert row["source_provenance"] == {
                "source_excerpt_sha256": _sha256_text(f"source-excerpt:{row['case_id']}"),
                "source_id": _sha256_text(f"source-id:{row['case_id']}")[:40],
            }
    assert boundary["boundary_assertion"] == {
        "expected_match": "# boundary",
        "expected_match_sha256": _sha256_text("# boundary"),
        "kind": "line_query_first_match",
    }
    assert boundary["boundary_probe"] == {
        "kind": "synthetic_structural_probe",
        "raw_comment": "# boundary\rsource",
        "raw_sha256": _sha256_text("# boundary\rsource"),
        "raw_utf8_length": len("# boundary\rsource".encode()),
    }
    assert boundary["raw_sha256"] == _sha256_text(boundary_failure.raw_comment)
    assert boundary["raw_utf8_length"] == len(boundary_failure.raw_comment.encode())
    assert "raw_comment" not in boundary
    assert boundary["disposition"] == "executable_regression"
    ambiguous = shard["oracle_exception_cases"][0]
    assert "expected_cleaned" not in ambiguous
    assert "raw_comment" not in ambiguous
    assert ambiguous["disposition"] == "accounting_only"
    assert ambiguous["exception_status"] == "ambiguous"
    assert len(ambiguous["oracle_exception_record_sha256"]) == 64


def test_cleaning_policy_dispute_is_clean_consensus_accounting_only_and_tamper_safe(
    tmp_path: Path,
):
    raw = "///EY1/SAV_I_PR_G2S_YB_LCGC\r"
    failure = replace(
        _source_failure("abap_cds-line-bced7abdf245bf3d", raw),
        language="abap_cds",
        family_name="abap_cds_style",
        syntax_label="//",
    )
    detail = (
        "Policy subkind normalization: the independent clean-output consensus "
        "is retained verbatim, but terminal newline handling is a "
        "normalization-policy choice."
    )
    payload = _exception_payload(
        failure,
        status="cleaning_policy_dispute",
        expected_cleaned="/EY1/SAV_I_PR_G2S_YB_LCGC\n",
        detail=detail,
    )
    exceptions_path = tmp_path / "oracle_exceptions.jsonl"
    exceptions_path.write_text(
        json.dumps(payload, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    exceptions = IMPORTER._load_oracle_exceptions(exceptions_path)

    rendered = IMPORTER.build_rendered_fixtures(
        {failure.case_id: failure},
        _source_provenance_for({failure.case_id: failure}),
        {},
        exceptions,
        failures_sha256="2" * 64,
        run_summary_sha256="3" * 64,
        annotations_sha256="4" * 64,
        oracle_exceptions_sha256="5" * 64,
        source_summary={
            "candidate_set_sha256": "6" * 64,
            "manifest_sha256": "7" * 64,
            "primary_model": EXPECTED_PRIMARY_MODEL,
            "secondary_model": EXPECTED_SECONDARY_MODEL,
        },
    )

    manifest = json.loads(rendered["_manifest.json"])
    assert manifest["case_category_counts"] == {
        "sanitizer": 0,
        "extractor_boundary": 0,
        "oracle_exception": 1,
    }
    assert manifest["exception_status_counts"] == {"cleaning_policy_dispute": 1}
    [accounting_case] = json.loads(rendered["abap_cds_style.json"])["oracle_exception_cases"]
    assert "expected_cleaned" not in accounting_case
    assert "raw_comment" not in accounting_case
    assert accounting_case["disposition"] == "accounting_only"
    assert accounting_case["exception_status"] == "cleaning_policy_dispute"
    assert accounting_case["raw_sha256"] == _sha256_text(raw)
    assert accounting_case["raw_utf8_length"] == len(raw.encode("utf-8"))

    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="cleaning_policy_identity",
    ):
        IMPORTER.build_rendered_fixtures(
            {failure.case_id: replace(failure, raw_comment=raw + " ")},
            _source_provenance_for({failure.case_id: failure}),
            {},
            exceptions,
            failures_sha256="2" * 64,
            run_summary_sha256="3" * 64,
            annotations_sha256="4" * 64,
            oracle_exceptions_sha256="5" * 64,
            source_summary={
                "candidate_set_sha256": "6" * 64,
                "manifest_sha256": "7" * 64,
                "primary_model": EXPECTED_PRIMARY_MODEL,
                "secondary_model": EXPECTED_SECONDARY_MODEL,
            },
        )

    tampered_payload = {
        **payload,
        "detail": "Policy subkind content_or_syntax: tampered classification.",
    }
    tampered_path = tmp_path / "tampered-exceptions.jsonl"
    tampered_path.write_text(
        json.dumps(tampered_payload, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tampered_exceptions = IMPORTER._load_oracle_exceptions(tampered_path)
    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="cleaning_policy_subkind",
    ):
        IMPORTER.build_rendered_fixtures(
            {failure.case_id: failure},
            _source_provenance_for({failure.case_id: failure}),
            {},
            tampered_exceptions,
            failures_sha256="2" * 64,
            run_summary_sha256="3" * 64,
            annotations_sha256="4" * 64,
            oracle_exceptions_sha256="5" * 64,
            source_summary={
                "candidate_set_sha256": "6" * 64,
                "manifest_sha256": "7" * 64,
                "primary_model": EXPECTED_PRIMARY_MODEL,
                "secondary_model": EXPECTED_SECONDARY_MODEL,
            },
        )

    non_consensus_payload = {
        **payload,
        "proposal": {
            **payload["proposal"],
            "disposition": "ambiguous",
            "expected_cleaned": "",
        },
        "review": {
            **payload["review"],
            "disposition": "ambiguous",
            "expected_cleaned": "",
        },
    }
    non_consensus_path = tmp_path / "non-consensus-exceptions.jsonl"
    non_consensus_path.write_text(
        json.dumps(non_consensus_payload, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="requires a clean within-run consensus",
    ):
        IMPORTER._load_oracle_exceptions(non_consensus_path)


def test_importer_requires_annotations_and_exceptions_to_partition_ids():
    failures = {"case": _source_failure("case", "# case")}
    annotation = object()
    exception = object()

    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="do not partition",
    ):
        IMPORTER._validate_case_partition(
            failures,
            {"case": annotation},
            {"case": exception},
        )
    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="do not partition",
    ):
        IMPORTER._validate_case_partition(failures, {}, {})


def test_empty_oracle_exception_file_is_a_valid_partition_input(
    tmp_path: Path,
):
    exceptions_path = tmp_path / "oracle_exceptions.jsonl"
    exceptions_path.write_bytes(b"")

    assert IMPORTER._load_oracle_exceptions(exceptions_path) == {}


def test_force_refuses_to_prune_arbitrary_json_directory(tmp_path: Path):
    unsafe_target = tmp_path / "tests" / "src"
    unsafe_target.mkdir(parents=True)
    victim = unsafe_target / "must-survive.json"
    victim.write_text('{"user":"data"}\n', encoding="utf-8")
    rendered = {
        "_manifest.json": "{}\n",
        IMPORTER.NOTICE_NAME: IMPORTER.NOTICE_TEXT,
        IMPORTER.SENTINEL_NAME: IMPORTER.SENTINEL_CONTENT,
    }

    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="without importer sentinel",
    ):
        IMPORTER._write_or_check(
            unsafe_target,
            rendered,
            check=False,
            force=True,
        )

    assert victim.read_text(encoding="utf-8") == '{"user":"data"}\n'
    assert set(path.name for path in unsafe_target.iterdir()) == {"must-survive.json"}


def test_force_can_update_a_directory_previously_created_by_importer(tmp_path: Path):
    generated = tmp_path / "generated"
    initial = {
        "_manifest.json": '{"version":1}\n',
        IMPORTER.NOTICE_NAME: IMPORTER.NOTICE_TEXT,
        IMPORTER.SENTINEL_NAME: IMPORTER.SENTINEL_CONTENT,
    }
    IMPORTER._write_or_check(generated, initial, check=False, force=False)
    stale = generated / "stale.json"
    stale.write_text("{}\n", encoding="utf-8")
    replacement = {
        **initial,
        "_manifest.json": '{"version":2}\n',
    }

    IMPORTER._write_or_check(generated, replacement, check=False, force=True)

    assert not stale.exists()
    assert (generated / "_manifest.json").read_text(encoding="utf-8") == '{"version":2}\n'
