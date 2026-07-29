"""Executable fixture for the repaired-run policy/oracle audit."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "comment_cleaning_policy_oracle_audit.json"
MANUAL_FIXTURE_PATH = (
    PROJECT_ROOT / "tests" / "fixtures" / "comment_cleaning_manual_adjudication.json"
)
SOURCE_FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures" / "comment_cleaning_repaired_failures"

SCHEMA_VERSION = 2
EXPECTED_CASE_COUNT = 64
EXPECTED_FIXTURE_SHA256 = "a20be45cd7a75bcb0b740d450f243a0702d62b2a841078db11298e26773b9d84"
EXPECTED_CASE_ID_SET_SHA256 = "0da023bca1e7c3ff419f5aa57344e03ad45a63dc060ab252ef64a3afeb7181bf"
EXPECTED_POLICY_ORACLE_AUDIT_SHA256 = (
    "f30a8fd8f940a7dfa4098cb28f456ba6ae48418bf016a28a0ed3e764d88941c6"
)
EXPECTED_REPAIRED_FAILURE_MANIFEST_SHA256 = (
    "fdfa93a333aa6684ecd3bc42d94f3ce4d74676ea30a31c65bfe308377e653394"
)
EXPECTED_DISPOSITION_COUNTS = {
    "genuine_bug_exact_literal": 14,
    "irreducibly_ambiguous": 1,
    "safe_current_policy": 49,
}
EXPECTED_EXPECTED_BASIS_COUNTS = {
    "current_output": 49,
    "manual_deletion_literal": 14,
    "null": 1,
}
EXPECTED_KIND_COUNTS = {
    "accounting_only": 1,
    "sanitizer_exact": 63,
}
EXPECTED_AMBIGUOUS_CASE_ID = "debian_package_control_file-line-c20841d96d377616"
EXPECTED_DUPLICATE_INPUT_GROUPS = {
    (
        "dns_zone",
        "4b2b470ca0fee88a3547788209d8cc146f0c7d51c6a53e186ff803dc1022035e",
    ): (
        2,
        "0e87f2c85d33088f161c949a380a03514f31818ffa12fae8cc8ed5f02a3cd1c3",
    ),
    (
        "lasso",
        "a12175c37ba1c0a93ebaf0f8664ec691819410d9211ba61f94741efbb9a7748f",
    ): (
        8,
        "119ef8acbbf36ee761765398ad60fe882e09fcb11bb4d0391d1cfb4d0c5e1859",
    ),
    (
        "x10",
        "8b1d75e72de34df3cb73c60815d7b1fdbf68efcf2c476df6d129d1f913bc0090",
    ): (
        5,
        "6631a9fccfdf41059aabb8a28944e57995d629824aa710ba60cd9c357ebe74e2",
    ),
}

FIXTURE_KEYS = frozenset(
    {
        "case_count",
        "case_id_set_sha256",
        "cases",
        "disposition_counts",
        "expected_basis_counts",
        "kind_counts",
        "schema_version",
        "source",
    }
)
COMMON_CASE_KEYS = frozenset(
    {
        "accounting_reason",
        "audit_record_sha256",
        "case_id",
        "disposition",
        "expected_basis",
        "expected_cleaned",
        "expected_cleaned_sha256",
        "kind",
        "language",
        "raw_comment_sha256",
        "raw_comment_utf8_length",
        "source_record_sha256",
    }
)
SANITIZER_CASE_KEYS = COMMON_CASE_KEYS | {"raw_comment"}


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _case_id_set_sha256(case_ids) -> str:
    payload = "".join(f"{case_id}\n" for case_id in sorted(case_ids))
    return _sha256_text(payload)


def _is_normalized_subsequence(expected: str, raw: str) -> bool:
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw_iterator = iter(raw)
    return all(
        any(raw_char == expected_char for raw_char in raw_iterator) for expected_char in expected
    )


FIXTURE_BYTES = FIXTURE_PATH.read_bytes()
FIXTURE = json.loads(FIXTURE_BYTES)
CASES = tuple(FIXTURE["cases"])
SANITIZER_CASES = tuple(case for case in CASES if case["kind"] == "sanitizer_exact")
ACCOUNTING_CASES = tuple(case for case in CASES if case["kind"] == "accounting_only")


def test_policy_oracle_fixture_pins_complete_64_case_audit():
    assert _sha256_bytes(FIXTURE_BYTES) == EXPECTED_FIXTURE_SHA256
    assert set(FIXTURE) == FIXTURE_KEYS
    assert FIXTURE["schema_version"] == SCHEMA_VERSION
    assert FIXTURE["case_count"] == EXPECTED_CASE_COUNT
    assert FIXTURE["case_id_set_sha256"] == EXPECTED_CASE_ID_SET_SHA256
    assert FIXTURE["disposition_counts"] == EXPECTED_DISPOSITION_COUNTS
    assert FIXTURE["expected_basis_counts"] == (EXPECTED_EXPECTED_BASIS_COUNTS)
    assert FIXTURE["kind_counts"] == EXPECTED_KIND_COUNTS
    assert FIXTURE["source"] == {
        "policy_oracle_audit_sha256": (EXPECTED_POLICY_ORACLE_AUDIT_SHA256),
        "repaired_failure_manifest_sha256": (EXPECTED_REPAIRED_FAILURE_MANIFEST_SHA256),
    }

    assert len(CASES) == EXPECTED_CASE_COUNT
    assert len({case["case_id"] for case in CASES}) == EXPECTED_CASE_COUNT
    assert _case_id_set_sha256(case["case_id"] for case in CASES) == (EXPECTED_CASE_ID_SET_SHA256)
    assert Counter(case["disposition"] for case in CASES) == (EXPECTED_DISPOSITION_COUNTS)
    assert (
        Counter(case["expected_basis"] or "null" for case in CASES)
        == EXPECTED_EXPECTED_BASIS_COUNTS
    )
    assert Counter(case["kind"] for case in CASES) == EXPECTED_KIND_COUNTS


@pytest.mark.parametrize(
    "case",
    CASES,
    ids=[case["case_id"] for case in CASES],
)
def test_each_policy_oracle_case_has_integrity_checked_source_evidence(case):
    expected_keys = SANITIZER_CASE_KEYS if case["kind"] == "sanitizer_exact" else COMMON_CASE_KEYS
    assert set(case) == expected_keys
    assert len(case["audit_record_sha256"]) == 64

    source_path = SOURCE_FIXTURE_DIR / f"{case['case_id']}.json"
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)

    assert source["case_id"] == case["case_id"]
    assert source["language"] == case["language"]
    assert source["source_record_sha256"] == case["source_record_sha256"]
    assert source["original_integrity"]["raw_comment"] == {
        "sha256": case["raw_comment_sha256"],
        "utf8_length": case["raw_comment_utf8_length"],
    }


@pytest.mark.parametrize(
    "case",
    SANITIZER_CASES,
    ids=[case["case_id"] for case in SANITIZER_CASES],
)
def test_each_policy_oracle_exact_literal_is_executable(case):
    assert case["accounting_reason"] is None
    expected = case["expected_cleaned"]
    raw_comment = case["raw_comment"]
    assert isinstance(expected, str)
    if case["expected_basis"] == "manual_deletion_literal":
        assert case["disposition"] == "genuine_bug_exact_literal"
    else:
        assert case["expected_basis"] == "current_output"
        assert case["disposition"] == "safe_current_policy"

    assert _sha256_text(raw_comment) == case["raw_comment_sha256"]
    assert len(raw_comment.encode("utf-8")) == case["raw_comment_utf8_length"]
    assert "\r" not in expected
    assert _sha256_text(expected) == case["expected_cleaned_sha256"]
    assert _is_normalized_subsequence(expected, raw_comment)
    assert sanitize_comment(case["language"], raw_comment) == expected


def test_ambiguous_policy_record_is_explicitly_accounting_only():
    assert len(ACCOUNTING_CASES) == 1
    case = ACCOUNTING_CASES[0]

    assert case["case_id"] == EXPECTED_AMBIGUOUS_CASE_ID
    assert case["disposition"] == "irreducibly_ambiguous"
    assert case["expected_basis"] is None
    assert case["expected_cleaned"] is None
    assert case["expected_cleaned_sha256"] is None
    assert "raw_comment" not in case
    assert len(case["raw_comment_sha256"]) == 64
    assert case["raw_comment_utf8_length"] > 0
    assert "multiple contract-plausible" in case["accounting_reason"]


def test_manual_and_policy_oracles_have_no_duplicate_input_conflicts():
    manual_cases = json.loads(MANUAL_FIXTURE_PATH.read_bytes())["cases"]
    all_cases = [*manual_cases, *CASES]
    by_input = defaultdict(list)
    for case in all_cases:
        by_input[(case["language"], case["raw_comment_sha256"])].append(case)

    assert len(all_cases) == 91
    assert len({case["case_id"] for case in all_cases}) == 91
    assert len(by_input) == 79

    duplicate_groups = {key: cases for key, cases in by_input.items() if len(cases) > 1}
    observed = {}
    for key, cases in duplicate_groups.items():
        expected_shas = {
            case["expected_cleaned_sha256"] for case in cases if case["kind"] == "sanitizer_exact"
        }
        assert len(expected_shas) == 1, (
            f"conflicting exact oracles for language/raw SHA {key}: {sorted(expected_shas)}"
        )
        observed[key] = (len(cases), expected_shas.pop())

    assert observed == EXPECTED_DUPLICATE_INPUT_GROUPS
