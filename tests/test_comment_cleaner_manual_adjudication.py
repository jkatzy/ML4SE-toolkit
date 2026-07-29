"""Executable oracles for every manually adjudicated repaired-run failure."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "comment_cleaning_manual_adjudication.json"
SOURCE_FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures" / "comment_cleaning_repaired_failures"
CORPUS_NOTICE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "COMMENT_CLEANING_CORPUS_NOTICE.md"

SCHEMA_VERSION = 2
EXPECTED_CASE_COUNT = 27
EXPECTED_FIXTURE_SHA256 = "87b06c07f78e8d69bc95a5307ee9dd253464b25081e4bf58d1ce4a41bfd8e47b"
EXPECTED_CASE_ID_SET_SHA256 = "891ceaf694b3299f73a3f942c71adb1ebc5d4a90eed40c2470b6d297d15e8e0b"
EXPECTED_ORACLE_DESCRIPTOR_SET_SHA256 = (
    "11729d025826bb40cb5d0ea2e63579a4b70665a36066a4ed7e4e9ea3b3ee7015"
)
EXPECTED_MANUAL_ADJUDICATION_SHA256 = (
    "c422dcbcbacd82e72aa09b7ae516d7e222fda68775c7b6ad7e49f31c016dc7b5"
)
EXPECTED_REPAIRED_FAILURE_MANIFEST_SHA256 = (
    "fdfa93a333aa6684ecd3bc42d94f3ce4d74676ea30a31c65bfe308377e653394"
)
EXPECTED_DECISION_COUNTS = {
    "genuine_sanitizer_bug": 22,
    "invalid_or_unproven_source": 1,
    "judge_or_policy_conflict_keep_current": 4,
}
EXPECTED_KIND_COUNTS = {
    "sanitizer_exact": 26,
    "source_eligibility_rejection": 1,
}

FIXTURE_KEYS = frozenset(
    {
        "schema_version",
        "case_count",
        "case_id_set_sha256",
        "decision_counts",
        "kind_counts",
        "oracle_descriptor_set_sha256",
        "source",
        "cases",
    }
)
COMMON_CASE_KEYS = frozenset(
    {
        "adjudication",
        "case_id",
        "kind",
        "language",
        "raw_comment_sha256",
        "raw_comment_utf8_length",
        "source_record_sha256",
    }
)
SANITIZER_CASE_KEYS = COMMON_CASE_KEYS | {
    "expected_cleaned",
    "expected_cleaned_sha256",
    "raw_comment",
}
SOURCE_ELIGIBILITY_CASE_KEYS = COMMON_CASE_KEYS | {
    "expected_eligible",
    "source_excerpt_sha256",
}


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )


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


def test_manual_adjudication_fixture_pins_all_27_cases_and_oracles():
    assert _sha256_bytes(FIXTURE_BYTES) == EXPECTED_FIXTURE_SHA256
    assert set(FIXTURE) == FIXTURE_KEYS
    assert FIXTURE["schema_version"] == SCHEMA_VERSION
    assert FIXTURE["case_count"] == EXPECTED_CASE_COUNT
    assert FIXTURE["case_id_set_sha256"] == EXPECTED_CASE_ID_SET_SHA256
    assert FIXTURE["oracle_descriptor_set_sha256"] == EXPECTED_ORACLE_DESCRIPTOR_SET_SHA256
    assert FIXTURE["decision_counts"] == EXPECTED_DECISION_COUNTS
    assert FIXTURE["kind_counts"] == EXPECTED_KIND_COUNTS
    assert FIXTURE["source"] == {
        "manual_adjudication_sha256": EXPECTED_MANUAL_ADJUDICATION_SHA256,
        "repaired_failure_manifest_sha256": (EXPECTED_REPAIRED_FAILURE_MANIFEST_SHA256),
    }

    assert len(CASES) == EXPECTED_CASE_COUNT
    assert len({case["case_id"] for case in CASES}) == EXPECTED_CASE_COUNT
    assert _case_id_set_sha256(case["case_id"] for case in CASES) == (EXPECTED_CASE_ID_SET_SHA256)
    assert Counter(case["adjudication"] for case in CASES) == (EXPECTED_DECISION_COUNTS)
    assert Counter(case["kind"] for case in CASES) == EXPECTED_KIND_COUNTS

    descriptors = []
    for case in CASES:
        outcome_sha256 = case.get(
            "expected_cleaned_sha256",
            _sha256_text("false"),
        )
        descriptors.append(
            {
                "case_id": case["case_id"],
                "kind": case["kind"],
                "outcome_sha256": outcome_sha256,
                "source_record_sha256": case["source_record_sha256"],
            }
        )
    descriptor_payload = "".join(_canonical_json(descriptor) + "\n" for descriptor in descriptors)
    assert _sha256_text(descriptor_payload) == (EXPECTED_ORACLE_DESCRIPTOR_SET_SHA256)


def test_manual_and_policy_fixture_provenance_is_discoverable():
    notice = CORPUS_NOTICE_PATH.read_text(encoding="utf-8")

    assert "`bigcode/the-stack-v2-dedup`" in notice
    assert "Software Heritage" in notice
    assert "manual-adjudication" in notice
    assert "policy-oracle" in notice
    assert "final-validation" in notice
    assert "exact per-file license metadata" in notice
    assert "source-excerpt" in notice
    assert "hash-pinned all-language source manifest" in notice


@pytest.mark.parametrize(
    "case",
    CASES,
    ids=[case["case_id"] for case in CASES],
)
def test_each_manual_adjudication_is_executable(case):
    source = json.loads(
        (SOURCE_FIXTURE_DIR / f"{case['case_id']}.json").read_text(encoding="utf-8")
    )
    assert source["case_id"] == case["case_id"]
    assert source["language"] == case["language"]
    assert source["source_record_sha256"] == case["source_record_sha256"]
    assert source["original_integrity"]["raw_comment"] == {
        "sha256": case["raw_comment_sha256"],
        "utf8_length": case["raw_comment_utf8_length"],
    }

    if case["kind"] == "sanitizer_exact":
        assert set(case) == SANITIZER_CASE_KEYS
        expected = case["expected_cleaned"]
        raw_comment = case["raw_comment"]
        assert case["adjudication"] in {
            "genuine_sanitizer_bug",
            "judge_or_policy_conflict_keep_current",
        }
        assert _sha256_text(raw_comment) == case["raw_comment_sha256"]
        assert len(raw_comment.encode("utf-8")) == case["raw_comment_utf8_length"]
        assert "\r" not in expected
        assert _sha256_text(expected) == case["expected_cleaned_sha256"]
        assert _is_normalized_subsequence(expected, raw_comment)
        assert sanitize_comment(case["language"], raw_comment) == expected
        return

    assert case["kind"] == "source_eligibility_rejection"
    assert set(case) == SOURCE_ELIGIBILITY_CASE_KEYS
    assert case["adjudication"] == "invalid_or_unproven_source"
    assert case["expected_eligible"] is False
    assert "raw_comment" not in case
    assert len(case["source_excerpt_sha256"]) == 64
