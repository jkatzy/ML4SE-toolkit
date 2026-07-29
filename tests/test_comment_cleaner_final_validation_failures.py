"""Exact oracles for every failure from the final focused judge validation."""

from __future__ import annotations

import hashlib
import json
import random
import string
from collections import Counter
from pathlib import Path

import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit

FIXTURE_PATH = (
    Path(__file__).parent / "fixtures" / "comment_cleaning_final_validation_failures.json"
)
EXPECTED_FIXTURE_SHA256 = "d323e686a42a231495effc4b68582980e402e0ce4f194df58f1040371c55e89e"
EXPECTED_CASE_ID_SET_SHA256 = "bc42d71309178d2a231d2c4819a473987a12e6fada4155922cd9fea2f8fb38ed"
EXPECTED_SOURCE = {
    "dataset": "bigcode/the-stack-v2-dedup",
    "final_failures_sha256": ("05bb2f7b0ef808b32f15be28208e3e33d3ea4aa90c34085bfb4545af23ece764"),
    "run_summary_sha256": ("12cc5c4aa52bb84309a2361bef8a5f1606c397bce825148f3b0b31cab54b76a6"),
    "source_manifest_sha256": ("1e87230b75165ae76583abdb48045e9ce9c5f4287135e8c4e564f400e230dcc0"),
    "validation_manifest_sha256": (
        "2009f24dea4e6e3148853737e94b462a5a068272bed9431b5343b173b8e96cce"
    ),
}
EXPECTED_DECISION_COUNTS = {
    "genuine_sanitizer_bug": 27,
    "judge_or_policy_conflict_keep_current": 3,
}
EXPECTED_LANGUAGE_COUNTS = {
    "ada": 1,
    "asn_1": 1,
    "brightscript": 3,
    "curry": 1,
    "dataweave": 6,
    "eclipse": 3,
    "html_django": 1,
    "html_plus_django": 1,
    "monkey_c": 1,
    "ncl": 1,
    "qml": 7,
    "sourcepawn": 2,
    "stata": 1,
    "xbase": 1,
}
POLICY_KEEP_IDS = {
    "ada-line-9c0cb77d6504d335",
    "asn_1-line-a81d4000083e6f3d",
    "ncl-line-3db4cc2d1678473d",
}
FIXTURE_KEYS = {
    "case_count",
    "case_id_set_sha256",
    "cases",
    "decision_counts",
    "language_counts",
    "schema_version",
    "source",
}
CASE_KEYS = {
    "adjudication",
    "candidate_cleaned_sha256",
    "case_id",
    "comment_kind",
    "expected_cleaned",
    "expected_cleaned_sha256",
    "language",
    "prior_final_pass",
    "raw_comment",
    "raw_comment_sha256",
    "secondary_input_sha256",
    "source_excerpt_sha256",
    "source_id",
    "validation_origin",
}


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _case_id_set_sha256(case_ids) -> str:
    return _sha256_text("".join(f"{case_id}\n" for case_id in sorted(case_ids)))


def _is_normalized_subsequence(expected: str, raw: str) -> bool:
    raw_iter = iter(raw.replace("\r\n", "\n").replace("\r", "\n"))
    return all(any(char == raw_char for raw_char in raw_iter) for char in expected)


FIXTURE_BYTES = FIXTURE_PATH.read_bytes()
FIXTURE = json.loads(FIXTURE_BYTES)
CASES = tuple(FIXTURE["cases"])


def test_final_validation_fixture_accounts_for_all_30_sol_failures():
    assert _sha256_bytes(FIXTURE_BYTES) == EXPECTED_FIXTURE_SHA256
    assert set(FIXTURE) == FIXTURE_KEYS
    assert FIXTURE["schema_version"] == 2
    assert FIXTURE["case_count"] == 30
    assert FIXTURE["case_id_set_sha256"] == EXPECTED_CASE_ID_SET_SHA256
    assert FIXTURE["decision_counts"] == EXPECTED_DECISION_COUNTS
    assert FIXTURE["language_counts"] == EXPECTED_LANGUAGE_COUNTS
    assert FIXTURE["source"] == EXPECTED_SOURCE

    case_ids = [case["case_id"] for case in CASES]
    assert len(CASES) == 30
    assert len(set(case_ids)) == 30
    assert _case_id_set_sha256(case_ids) == EXPECTED_CASE_ID_SET_SHA256
    assert Counter(case["adjudication"] for case in CASES) == EXPECTED_DECISION_COUNTS
    assert Counter(case["language"] for case in CASES) == EXPECTED_LANGUAGE_COUNTS
    assert sum(case["prior_final_pass"] for case in CASES) == 17
    assert {case["validation_origin"] for case in CASES} == {"changed_since_repaired_two_stage_run"}


@pytest.mark.parametrize("case", CASES, ids=[case["case_id"] for case in CASES])
def test_each_final_validation_failure_has_an_exact_audited_oracle(case):
    assert set(case) == CASE_KEYS
    assert case["comment_kind"] in {"block", "line"}
    assert len(case["source_id"]) == 40
    assert set(case["source_id"]) <= set(string.hexdigits.lower())
    assert len(case["source_excerpt_sha256"]) == 64
    assert set(case["source_excerpt_sha256"]) <= set(string.hexdigits.lower())
    assert "\r" not in case["expected_cleaned"]
    assert case["raw_comment_sha256"] == _sha256_text(case["raw_comment"])
    assert case["expected_cleaned_sha256"] == _sha256_text(case["expected_cleaned"])
    assert _is_normalized_subsequence(case["expected_cleaned"], case["raw_comment"])
    assert sanitize_comment(case["language"], case["raw_comment"]) == case["expected_cleaned"]

    candidate_matches = case["candidate_cleaned_sha256"] == case["expected_cleaned_sha256"]
    if case["case_id"] in POLICY_KEEP_IDS:
        assert case["adjudication"] == "judge_or_policy_conflict_keep_current"
        assert candidate_matches
    else:
        assert case["adjudication"] == "genuine_sanitizer_bug"
        assert not candidate_matches


def test_qml_qt_frame_removes_only_the_proven_double_star_gutter():
    raw = (
        "/********\n"
        "**\n"
        "** Title **inside**\n"
        "**   * Markdown bullet\n"
        "** $QT_BEGIN_LICENSE$ https://example.test/a*b\n"
        "**\n"
        "********/"
    )
    assert sanitize_comment("qml", raw) == (
        "Title **inside**\n  * Markdown bullet\n$QT_BEGIN_LICENSE$ https://example.test/a*b"
    )
    assert sanitize_comment("qml", "/**\n * **bold content**\n */") == "**bold content**"


def test_dataweave_nested_line_gutter_requires_complete_symmetric_proof():
    raw = (
        "/*\n"
        "* //========\n"
        "* // Alpha // value\n"
        "* //\n"
        "* //  https://example.test/a//b\n"
        "* //========\n"
        "*/"
    )
    assert sanitize_comment("dataweave", raw) == ("Alpha // value\n https://example.test/a//b")
    assert (
        sanitize_comment(
            "dataweave",
            "/*\n* // literal operator\n* // remains content\n*/",
        )
        == "// literal operator\n// remains content"
    )


@pytest.mark.parametrize(
    ("language", "raw", "expected"),
    [
        ("html_django", "{## JR C sn ##}", "# JR C sn #"),
        ("html_plus_django", "{## JR C sn ##}", "# JR C sn #"),
        ("html_plusdjango", "{## JR C sn ##}", "JR C sn"),
        ("xbase", "/*/{Other.doc}\n/*/", "/{Other.doc}"),
        ("stata", "* ordinary emphasis *", "ordinary emphasis *"),
    ],
)
def test_final_failure_fixes_do_not_broaden_neighboring_delimiters(
    language,
    raw,
    expected,
):
    assert sanitize_comment(language, raw) == expected


def test_qml_and_dataweave_validated_gutters_survive_seeded_payload_fuzz():
    rng = random.Random(0xF17A1)
    alphabet = string.ascii_letters + string.digits + " :/@$*#=+-_.()[]{}"
    for _ in range(100):
        payloads = [
            f"id{index} " + "".join(rng.choice(alphabet) for _ in range(rng.randrange(1, 48)))
            for index in range(3)
        ]

        qml_raw = (
            "/********\n"
            "**\n" + "\n".join(f"** {payload}" for payload in payloads) + "\n**\n********/"
        )
        assert sanitize_comment("qml", qml_raw) == "\n".join(
            payload.rstrip() for payload in payloads
        )

        dataweave_raw = (
            "/*\n"
            "* //========\n"
            "* //\n" + "\n".join(f"* // {payload}" for payload in payloads) + "\n* //========\n*/"
        )
        assert sanitize_comment("dataweave", dataweave_raw) == "\n".join(
            payload.rstrip() for payload in payloads
        )
