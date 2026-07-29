"""Hash-only accounting plus synthetic probes for invalid extraction/source cases."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from ml4setk import CommentQuery

pytestmark = pytest.mark.unit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures" / "comment_cleaning_repaired_failures"
GENERATOR_PATH = PROJECT_ROOT / "scripts" / "build_stack_v2_comment_judge_cases.py"

EXPECTED_CASE_COUNT = 92
EXPECTED_CASE_ID_SET_SHA256 = "02bb0ebed6d63d379476d91b0b7914ae11e5664784b9dd4c3b4cb2c0e91a28e5"
EXPECTED_RANGE_ABSENCE_COUNT = 87
EXPECTED_RANGE_ABSENCE_ID_SET_SHA256 = (
    "8aff27e6ab39a09587129d1a98ff8729af77d796e838315c0e8f5c993eec1c87"
)
SCHEMA_VERSION = 2
COMMON_FIXTURE_KEYS = frozenset(
    {
        "case_id",
        "category",
        "cluster",
        "disposition",
        "language",
        "original_expected_output_source",
        "original_integrity",
        "schema_version",
        "source_provenance",
        "source_record_sha256",
    }
)
INTEGRITY_KEYS = frozenset(
    {
        "current_output",
        "manifest_old_output",
        "raw_comment",
    }
)
HASH_AND_LENGTH_KEYS = frozenset({"sha256", "utf8_length"})
SOURCE_PROVENANCE_KEYS = frozenset(
    {
        "dataset",
        "source_excerpt_sha256",
        "source_id",
    }
)

# These intentionally synthetic probes exercise the shared collision signatures
# without retaining or reconstructing any corpus source literal or path.
SOURCE_FILTER_SIGNATURE_PROBES = {
    "cobol-line-0345a550d577378d": (
        "codecharge-ccp-xml",
        "source_invalid:mislabeled_xml_code",
        "synthetic.ccp",
        '<Page Name="Header"><Components /></Page>',
    ),
    "cobol-line-4cc6fc04c647201d": (
        "codecharge-ccp-xml",
        "source_invalid:mislabeled_xml_code",
        "synthetic.ccp",
        '<?xml version="1.0"?><Page Name="Customer"><Events /></Page>',
    ),
    "mirc_script-line-112a24da87b41074": (
        "iso-2709-marc",
        "source_invalid:mislabeled_marc_data",
        "synthetic.mrc",
        ("00045cpcaa2200037Ii 4500001000700000\x1evalue?\x1e\x1d"),
    ),
    "mirc_script-line-f1d67ed1511082e4": (
        "iso-2709-marc",
        "source_invalid:mislabeled_marc_data",
        "synthetic.mrc",
        ("00045cam a2200037Ii 41y0001000700000\x1evalue?\x1e\x1d"),
    ),
}
EXPECTED_SOURCE_FILTER_ID_SET_SHA256 = (
    "88a852051330bed34bbc8b281343e675f4c1932f3763beababd242106f868f6a"
)

# This boundary is context-sensitive: braces are valid Genero comments outside
# a screen body. A synthetic minimal layout proves the contextual extractor
# behavior without retaining the original source context.
CONTEXTUAL_EXTRACTOR_CASE_IDS = frozenset({"genero_forms-block-c2731952d8a3345f"})
EXPECTED_CONTEXTUAL_ID_SET_SHA256 = (
    "e6360225489048c426df70010762627522d9c52d25d289c9627f30da7e59a979"
)
SYNTHETIC_GENERO_SCREEN_LAYOUT = "screen\n{\n  [field]\n}\n"


def _load_generator() -> Any:
    spec = importlib.util.spec_from_file_location(
        "repaired_failure_manifest_generator",
        GENERATOR_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_invalid_cases() -> dict[str, dict[str, Any]]:
    cases = {}
    for path in FIXTURE_DIR.glob("*.json"):
        if path.name == "_manifest.json":
            continue
        fixture = json.loads(path.read_text(encoding="utf-8"))
        if fixture["category"] != "extractor_or_source_invalid":
            continue
        case_id = fixture["case_id"]
        assert case_id not in cases
        cases[case_id] = fixture
    return cases


def _case_id_set_sha256(case_ids) -> str:
    payload = "".join(f"{case_id}\n" for case_id in sorted(case_ids))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _assert_lowercase_hex(value: str, length: int) -> None:
    assert len(value) == length
    assert all(character in "0123456789abcdef" for character in value)


GENERATOR = _load_generator()
INVALID_CASES = _load_invalid_cases()
SOURCE_FILTER_CASE_IDS = frozenset(SOURCE_FILTER_SIGNATURE_PROBES)
RANGE_ABSENCE_CASE_IDS = (
    INVALID_CASES.keys() - SOURCE_FILTER_CASE_IDS - CONTEXTUAL_EXTRACTOR_CASE_IDS
)


def test_invalid_extraction_coverage_partitions_all_92_failures_exactly():
    all_case_ids = set(INVALID_CASES)
    partitions = (
        set(RANGE_ABSENCE_CASE_IDS),
        set(SOURCE_FILTER_CASE_IDS),
        set(CONTEXTUAL_EXTRACTOR_CASE_IDS),
    )

    assert len(all_case_ids) == EXPECTED_CASE_COUNT
    assert _case_id_set_sha256(all_case_ids) == EXPECTED_CASE_ID_SET_SHA256
    assert all(
        left.isdisjoint(right) for left in partitions for right in partitions if left is not right
    )
    assert set().union(*partitions) == all_case_ids

    assert len(RANGE_ABSENCE_CASE_IDS) == EXPECTED_RANGE_ABSENCE_COUNT
    assert _case_id_set_sha256(RANGE_ABSENCE_CASE_IDS) == EXPECTED_RANGE_ABSENCE_ID_SET_SHA256
    assert _case_id_set_sha256(SOURCE_FILTER_CASE_IDS) == EXPECTED_SOURCE_FILTER_ID_SET_SHA256
    assert _case_id_set_sha256(CONTEXTUAL_EXTRACTOR_CASE_IDS) == EXPECTED_CONTEXTUAL_ID_SET_SHA256


@pytest.mark.parametrize(
    "case_id",
    sorted(INVALID_CASES),
)
def test_each_invalid_case_is_hash_only_accounting(case_id: str):
    fixture = INVALID_CASES[case_id]

    assert set(fixture) == COMMON_FIXTURE_KEYS
    assert fixture["schema_version"] == SCHEMA_VERSION
    assert fixture["case_id"] == case_id
    assert fixture["category"] == "extractor_or_source_invalid"
    assert fixture["disposition"] == "accounting_only_no_oracle"
    assert fixture["original_expected_output_source"] is None
    assert "regression" not in fixture

    integrity = fixture["original_integrity"]
    assert set(integrity) == INTEGRITY_KEYS
    for literal_integrity in integrity.values():
        assert set(literal_integrity) == HASH_AND_LENGTH_KEYS
        _assert_lowercase_hex(literal_integrity["sha256"], 64)
        assert isinstance(literal_integrity["utf8_length"], int)
        assert literal_integrity["utf8_length"] >= 0

    provenance = fixture["source_provenance"]
    assert set(provenance) == SOURCE_PROVENANCE_KEYS
    assert provenance["dataset"] == "bigcode/the-stack-v2-dedup"
    _assert_lowercase_hex(provenance["source_id"], 40)
    _assert_lowercase_hex(provenance["source_excerpt_sha256"], 64)
    _assert_lowercase_hex(fixture["source_record_sha256"], 64)


@pytest.mark.parametrize(
    (
        "case_id",
        "signature_name",
        "expected_cluster",
        "probe_path",
        "signature_probe",
    ),
    [
        (case_id, *SOURCE_FILTER_SIGNATURE_PROBES[case_id])
        for case_id in sorted(SOURCE_FILTER_CASE_IDS)
    ],
)
def test_collision_source_signature_is_rejected_before_extraction(
    case_id: str,
    signature_name: str,
    expected_cluster: str,
    probe_path: str,
    signature_probe: str,
):
    fixture = INVALID_CASES[case_id]

    assert signature_name in {"codecharge-ccp-xml", "iso-2709-marc"}
    assert fixture["cluster"] == expected_cluster
    assert not GENERATOR._record_is_eligible_source(
        {"path": probe_path},
        fixture["language"],
        signature_probe,
    )


@pytest.mark.parametrize(
    "case_id",
    sorted(CONTEXTUAL_EXTRACTOR_CASE_IDS),
)
def test_synthetic_screen_layout_excludes_context_sensitive_false_boundary(
    case_id: str,
):
    fixture = INVALID_CASES[case_id]

    assert fixture["cluster"] == "source_invalid:genero_form_code"
    assert fixture["language"] == "genero_forms"
    assert CommentQuery(fixture["language"]).parse(SYNTHETIC_GENERO_SCREEN_LAYOUT) == []
