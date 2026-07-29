"""Compact one-case-per-failure accounting for the repaired all-language run."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures" / "comment_cleaning_repaired_failures"
MANIFEST_PATH = FIXTURE_DIR / "_manifest.json"
SENTINEL_PATH = FIXTURE_DIR / ".generated-by-import_repaired_comment_failures"

SCHEMA_VERSION = 2
EXPECTED_CASE_COUNT = 569
EXPECTED_EXECUTABLE_COUNT = 420
EXPECTED_EXACT_EXECUTABLE_COUNT = 418
EXPECTED_MINIMIZED_EXECUTABLE_COUNT = 2
EXPECTED_ACCOUNTING_ONLY_COUNT = 149
EXPECTED_NO_ORACLE_COUNT = 128
EXPECTED_SUPERSEDED_COUNT = 21
EXPECTED_CASE_ID_SET_SHA256 = "fbce7ffaf1fc07858fd92c4d3c621720545140df1e3d49341251b1d916320d85"
EXPECTED_CLASSIFICATION_SHA256 = "1882604637de5107a85b5a1f7d671eb8565bb34bcb2f2d1d60c5442cc7b9a2c1"
EXPECTED_MANIFEST_SHA256 = "fdfa93a333aa6684ecd3bc42d94f3ce4d74676ea30a31c65bfe308377e653394"
EXPECTED_CATEGORY_COUNTS = {
    "approved_oracle_match": 3,
    "extractor_or_source_invalid": 92,
    "needs_manual_review": 27,
    "policy_or_judge_conflict": 61,
    "sanitizer_regression": 386,
}
EXPECTED_SOURCE_COUNTS = {
    "current": 52,
    "manifest_old": 386,
    "null": 128,
    "oracle": 3,
}
EXPECTED_DISPOSITION_COUNTS = {
    "accounting_only_no_oracle": EXPECTED_NO_ORACLE_COUNT,
    "accounting_only_superseded": EXPECTED_SUPERSEDED_COUNT,
    "executable_regression": EXPECTED_EXECUTABLE_COUNT,
}
EXPECTED_PROVENANCE_COUNTS = {
    "exact_classification_literal": EXPECTED_EXACT_EXECUTABLE_COUNT,
    "reviewed_minimized_reproduction": EXPECTED_MINIMIZED_EXECUTABLE_COUNT,
}

COMMON_FIXTURE_KEYS = frozenset(
    {
        "schema_version",
        "case_id",
        "language",
        "category",
        "cluster",
        "disposition",
        "original_expected_output_source",
        "original_integrity",
        "source_provenance",
        "source_record_sha256",
    }
)
REGRESSION_KEYS = frozenset({"raw_comment", "expected_output", "provenance"})
INTEGRITY_KEYS = frozenset({"sha256", "utf8_length"})
SOURCE_PROVENANCE_KEYS = frozenset({"dataset", "source_excerpt_sha256", "source_id"})
DESCRIPTOR_KEYS = frozenset(
    {
        "case_id",
        "filename",
        "sha256",
        "category",
        "disposition",
        "original_expected_output_source",
        "source_record_sha256",
    }
)
SUPERSEDED_IDS = frozenset(
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
MINIMIZED_IDS = frozenset(
    {
        "aspectj-line-e228da2958374c9a",
        "openstep_property_list-line-63f4c6020d2b8342",
    }
)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _canonical_record(record) -> str:
    return json.dumps(
        record,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )


def _case_id_set_sha256(case_ids) -> str:
    payload = "".join(f"{case_id}\n" for case_id in sorted(case_ids))
    return _sha256_text(payload)


def _load_importer():
    path = PROJECT_ROOT / "scripts" / "import_repaired_comment_failures.py"
    spec = importlib.util.spec_from_file_location(
        "import_repaired_comment_failures",
        path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _classification_record(
    *,
    case_id: str = "fixture-line-deterministic",
) -> dict:
    raw_comment = "// retained payload"
    old_output = "retained payload"
    current_output = "/ retained payload"
    return {
        "case_id": case_id,
        "language": "c",
        "category": "sanitizer_regression",
        "reason": "Synthetic importer contract record.",
        "evidence": {
            "raw_comment_sha256": _sha256_text(raw_comment),
            "source_excerpt_sha256": "2" * 64,
            "source_id": "3" * 40,
        },
        "old_output_sha": _sha256_text(old_output),
        "current_output_sha": _sha256_text(current_output),
        "recommended_expected_output_source": "manifest_old",
        "cluster": "test:deterministic",
        "raw_comment": raw_comment,
        "manifest_old_output": old_output,
        "current_output": current_output,
        "recommended_expected_output": old_output,
    }


def _write_classification(path: Path, record: dict) -> None:
    path.write_text(_canonical_record(record) + "\n", encoding="utf-8")


MANIFEST = _load_json(MANIFEST_PATH)
DESCRIPTORS = tuple(MANIFEST["fixtures"])
EXECUTABLE_DESCRIPTORS = tuple(
    descriptor for descriptor in DESCRIPTORS if descriptor["disposition"] == "executable_regression"
)
ACCOUNTING_ONLY_DESCRIPTORS = tuple(
    descriptor for descriptor in DESCRIPTORS if descriptor["disposition"] != "executable_regression"
)
NO_ORACLE_DESCRIPTORS = tuple(
    descriptor
    for descriptor in DESCRIPTORS
    if descriptor["disposition"] == "accounting_only_no_oracle"
)
SUPERSEDED_DESCRIPTORS = tuple(
    descriptor
    for descriptor in DESCRIPTORS
    if descriptor["disposition"] == "accounting_only_superseded"
)


def test_repaired_failure_manifest_freezes_complete_569_case_accounting():
    assert _sha256_bytes(MANIFEST_PATH.read_bytes()) == EXPECTED_MANIFEST_SHA256
    assert MANIFEST["schema_version"] == SCHEMA_VERSION
    assert MANIFEST["case_count"] == EXPECTED_CASE_COUNT
    assert MANIFEST["case_id_set_sha256"] == EXPECTED_CASE_ID_SET_SHA256
    assert MANIFEST["category_counts"] == EXPECTED_CATEGORY_COUNTS
    assert MANIFEST["recommended_expected_output_source_counts"] == EXPECTED_SOURCE_COUNTS
    assert MANIFEST["disposition_counts"] == EXPECTED_DISPOSITION_COUNTS
    assert MANIFEST["regression_provenance_counts"] == EXPECTED_PROVENANCE_COUNTS
    assert MANIFEST["unresolved_count"] == 27
    assert len(MANIFEST["unresolved_ids"]) == 27
    assert MANIFEST["unresolved_ids"] == sorted(MANIFEST["unresolved_ids"])
    assert MANIFEST["source_classification"] == {
        "record_count": EXPECTED_CASE_COUNT,
        "sha256": EXPECTED_CLASSIFICATION_SHA256,
    }

    assert len(DESCRIPTORS) == EXPECTED_CASE_COUNT
    assert len(EXECUTABLE_DESCRIPTORS) == EXPECTED_EXECUTABLE_COUNT
    assert len(ACCOUNTING_ONLY_DESCRIPTORS) == EXPECTED_ACCOUNTING_ONLY_COUNT
    assert len(NO_ORACLE_DESCRIPTORS) == EXPECTED_NO_ORACLE_COUNT
    assert len(SUPERSEDED_DESCRIPTORS) == EXPECTED_SUPERSEDED_COUNT
    assert {item["case_id"] for item in SUPERSEDED_DESCRIPTORS} == SUPERSEDED_IDS
    assert len({item["case_id"] for item in DESCRIPTORS}) == EXPECTED_CASE_COUNT
    assert _case_id_set_sha256(item["case_id"] for item in DESCRIPTORS) == (
        EXPECTED_CASE_ID_SET_SHA256
    )
    assert Counter(item["category"] for item in DESCRIPTORS) == (EXPECTED_CATEGORY_COUNTS)

    expected_files = {
        "_manifest.json",
        ".generated-by-import_repaired_comment_failures",
        "NOTICE.md",
    } | {descriptor["filename"] for descriptor in DESCRIPTORS}
    assert {path.name for path in FIXTURE_DIR.iterdir()} == expected_files


@pytest.mark.parametrize(
    "descriptor",
    DESCRIPTORS,
    ids=[descriptor["case_id"] for descriptor in DESCRIPTORS],
)
def test_each_repaired_failure_has_one_compact_integrity_fixture(descriptor):
    assert set(descriptor) == DESCRIPTOR_KEYS
    assert descriptor["filename"] == f"{descriptor['case_id']}.json"

    path = FIXTURE_DIR / descriptor["filename"]
    fixture_bytes = path.read_bytes()
    fixture = json.loads(fixture_bytes)
    assert _sha256_bytes(fixture_bytes) == descriptor["sha256"]
    expected_keys = set(COMMON_FIXTURE_KEYS)
    if descriptor["disposition"] == "executable_regression":
        expected_keys.add("regression")
    assert set(fixture) == expected_keys
    assert fixture["schema_version"] == SCHEMA_VERSION
    assert fixture["case_id"] == descriptor["case_id"]
    assert fixture["category"] == descriptor["category"]
    assert fixture["disposition"] == descriptor["disposition"]
    assert (
        fixture["original_expected_output_source"] == descriptor["original_expected_output_source"]
    )
    assert fixture["source_record_sha256"] == descriptor["source_record_sha256"]
    assert len(fixture["source_record_sha256"]) == 64
    provenance = fixture["source_provenance"]
    assert set(provenance) == SOURCE_PROVENANCE_KEYS
    assert provenance["dataset"] == "bigcode/the-stack-v2-dedup"
    assert len(provenance["source_id"]) == 40
    assert len(provenance["source_excerpt_sha256"]) == 64

    integrity = fixture["original_integrity"]
    expected_integrity_keys = {
        "raw_comment",
        "manifest_old_output",
        "current_output",
    }
    if fixture["original_expected_output_source"] is not None:
        expected_integrity_keys.add("recommended_expected_output")
    assert set(integrity) == expected_integrity_keys
    for literal_integrity in integrity.values():
        assert set(literal_integrity) == INTEGRITY_KEYS
        assert len(literal_integrity["sha256"]) == 64
        assert literal_integrity["utf8_length"] >= 0

    # Evidence prose, repository/path provenance, source context, and unused
    # original literals are intentionally absent from every committed record.
    assert not (
        {
            "reason",
            "evidence",
            "repo",
            "path",
            "source_context_before",
            "source_context_after",
            "manifest_old_output",
            "current_output",
            "recommended_expected_output",
        }
        & fixture.keys()
    )


@pytest.mark.parametrize(
    "descriptor",
    EXECUTABLE_DESCRIPTORS,
    ids=[descriptor["case_id"] for descriptor in EXECUTABLE_DESCRIPTORS],
)
def test_each_active_literal_is_an_executable_sanitizer_regression(descriptor):
    fixture = _load_json(FIXTURE_DIR / descriptor["filename"])
    regression = fixture["regression"]

    assert set(regression) == REGRESSION_KEYS
    assert (
        sanitize_comment(
            fixture["language"],
            regression["raw_comment"],
        )
        == regression["expected_output"]
    )

    if descriptor["case_id"] in MINIMIZED_IDS:
        assert regression["provenance"] == "reviewed_minimized_reproduction"
        assert (
            _sha256_text(regression["raw_comment"])
            != (fixture["original_integrity"]["raw_comment"]["sha256"])
        )
    else:
        assert regression["provenance"] == "exact_classification_literal"
        assert (
            _sha256_text(regression["raw_comment"])
            == (fixture["original_integrity"]["raw_comment"]["sha256"])
        )
        assert (
            _sha256_text(regression["expected_output"])
            == (fixture["original_integrity"]["recommended_expected_output"]["sha256"])
        )


def test_only_two_oversized_executable_literals_were_replaced_by_reviewed_minima():
    provenance_counts = Counter()
    literal_sizes = []
    minimized_ids = set()
    for descriptor in EXECUTABLE_DESCRIPTORS:
        fixture = _load_json(FIXTURE_DIR / descriptor["filename"])
        regression = fixture["regression"]
        provenance_counts[regression["provenance"]] += 1
        literal_sizes.extend(
            [
                len(regression["raw_comment"].encode("utf-8")),
                len(regression["expected_output"].encode("utf-8")),
            ]
        )
        if regression["provenance"] == "reviewed_minimized_reproduction":
            minimized_ids.add(descriptor["case_id"])

    assert provenance_counts == EXPECTED_PROVENANCE_COUNTS
    assert minimized_ids == MINIMIZED_IDS
    assert max(literal_sizes) <= 4096


def test_fixture_notice_documents_stack_v2_provenance_and_license_limit():
    notice = SENTINEL_PATH.with_name("NOTICE.md").read_text(encoding="utf-8")

    assert "bigcode/the-stack-v2-dedup" in notice
    assert "Software Heritage" in notice
    assert "source identifier" in notice
    assert "did not include exact per-file license metadata" in notice


@pytest.mark.parametrize(
    "descriptor",
    ACCOUNTING_ONLY_DESCRIPTORS,
    ids=[descriptor["case_id"] for descriptor in ACCOUNTING_ONLY_DESCRIPTORS],
)
def test_each_accounting_only_failure_omits_all_corpus_literals(descriptor):
    fixture = _load_json(FIXTURE_DIR / descriptor["filename"])

    assert "regression" not in fixture
    if fixture["disposition"] == "accounting_only_no_oracle":
        assert fixture["original_expected_output_source"] is None
    else:
        assert fixture["disposition"] == "accounting_only_superseded"
        assert fixture["original_expected_output_source"] is not None


def test_importer_is_byte_deterministic_for_compact_schema(tmp_path):
    classification = tmp_path / "failures.jsonl"
    record = _classification_record()
    _write_classification(classification, record)
    importer = _load_importer()

    generated_a = tmp_path / "generated-a"
    generated_b = tmp_path / "generated-b"
    manifest_a = importer.import_classification(
        classification,
        generated_a,
        expected_count=1,
    )
    manifest_b = importer.import_classification(
        classification,
        generated_b,
        expected_count=1,
    )

    assert manifest_a == manifest_b
    assert {path.name for path in generated_a.iterdir()} == {
        path.name for path in generated_b.iterdir()
    }
    for path in generated_a.iterdir():
        assert path.read_bytes() == (generated_b / path.name).read_bytes()

    fixture = _load_json(generated_a / f"{record['case_id']}.json")
    assert set(fixture) == COMMON_FIXTURE_KEYS | {"regression"}
    assert fixture["regression"] == {
        "expected_output": record["recommended_expected_output"],
        "provenance": "exact_classification_literal",
        "raw_comment": record["raw_comment"],
    }
    assert "reason" not in fixture
    assert "evidence" not in fixture
    assert (generated_a / importer.SENTINEL_NAME).read_bytes() == (importer.SENTINEL_CONTENT)
    assert (generated_a / importer.NOTICE_NAME).read_text(encoding="utf-8") == (
        importer.NOTICE_TEXT
    )


def test_force_refuses_arbitrary_existing_directory_without_sentinel(tmp_path):
    classification = tmp_path / "failures.jsonl"
    _write_classification(classification, _classification_record())
    unsafe_target = tmp_path / "tests" / "src"
    unsafe_target.mkdir(parents=True)
    victim = unsafe_target / "must-survive.txt"
    victim.write_text("user data", encoding="utf-8")
    importer = _load_importer()

    with pytest.raises(
        importer.ImportValidationError,
        match="without importer sentinel",
    ):
        importer.import_classification(
            classification,
            unsafe_target,
            expected_count=1,
            force=True,
        )

    assert victim.read_text(encoding="utf-8") == "user data"


def test_force_refuses_existing_directory_with_invalid_sentinel(tmp_path):
    classification = tmp_path / "failures.jsonl"
    _write_classification(classification, _classification_record())
    unsafe_target = tmp_path / "generated"
    unsafe_target.mkdir()
    (unsafe_target / ".generated-by-import_repaired_comment_failures").write_text(
        "not this importer\n",
        encoding="utf-8",
    )
    victim = unsafe_target / "must-survive.txt"
    victim.write_text("user data", encoding="utf-8")
    importer = _load_importer()

    with pytest.raises(
        importer.ImportValidationError,
        match="without importer sentinel",
    ):
        importer.import_classification(
            classification,
            unsafe_target,
            expected_count=1,
            force=True,
        )

    assert victim.read_text(encoding="utf-8") == "user data"


def test_force_replaces_only_a_sentinel_protected_generated_directory(tmp_path):
    classification = tmp_path / "failures.jsonl"
    _write_classification(classification, _classification_record())
    generated = tmp_path / "generated"
    importer = _load_importer()
    importer.import_classification(classification, generated, expected_count=1)
    stale = generated / "stale-generated-file"
    stale.write_text("stale", encoding="utf-8")

    importer.import_classification(
        classification,
        generated,
        expected_count=1,
        force=True,
    )

    assert not stale.exists()
    assert (generated / importer.SENTINEL_NAME).read_bytes() == (importer.SENTINEL_CONTENT)


def test_force_refuses_symlinked_target_even_with_valid_sentinel(tmp_path):
    classification = tmp_path / "failures.jsonl"
    _write_classification(classification, _classification_record())
    real_target = tmp_path / "real"
    real_target.mkdir()
    victim = real_target / "must-survive.txt"
    victim.write_text("user data", encoding="utf-8")
    importer = _load_importer()
    (real_target / importer.SENTINEL_NAME).write_bytes(importer.SENTINEL_CONTENT)
    symlink_target = tmp_path / "linked"
    symlink_target.symlink_to(real_target, target_is_directory=True)

    with pytest.raises(
        importer.ImportValidationError,
        match="symlinked",
    ):
        importer.import_classification(
            classification,
            symlink_target,
            expected_count=1,
            force=True,
        )

    assert victim.read_text(encoding="utf-8") == "user data"
