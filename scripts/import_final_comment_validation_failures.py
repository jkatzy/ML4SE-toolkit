#!/usr/bin/env python3
"""Freeze the audited failures from the final focused cleaner validation.

The input run is immutable judge evidence.  Expected outputs are taken from the
post-audit sanitizer, but every output hash is independently pinned here so a
future sanitizer change cannot silently rewrite the committed fixture.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from ml4setk import sanitize_comment

SCHEMA_VERSION = 2
EXPECTED_CASE_COUNT = 30
EXPECTED_FINAL_FAILURES_SHA256 = "05bb2f7b0ef808b32f15be28208e3e33d3ea4aa90c34085bfb4545af23ece764"
EXPECTED_VALIDATION_MANIFEST_SHA256 = (
    "2009f24dea4e6e3148853737e94b462a5a068272bed9431b5343b173b8e96cce"
)
EXPECTED_SOURCE_MANIFEST_SHA256 = "1e87230b75165ae76583abdb48045e9ce9c5f4287135e8c4e564f400e230dcc0"
EXPECTED_RUN_SUMMARY_SHA256 = "12cc5c4aa52bb84309a2361bef8a5f1606c397bce825148f3b0b31cab54b76a6"
EXPECTED_CASE_ID_SET_SHA256 = "bc42d71309178d2a231d2c4819a473987a12e6fada4155922cd9fea2f8fb38ed"

DEFAULT_ROOT = Path(
    "tmp/stack_v2_comment_cleaner_all_languages_50/two_stage_repaired/final_repair_validation"
)
DEFAULT_SOURCE_MANIFEST = Path("tmp/stack_v2_comment_cleaner_all_languages_50/manifest.jsonl")
DEFAULT_OUTPUT = Path("tests/fixtures/comment_cleaning_final_validation_failures.json")

POLICY_KEEP_IDS = frozenset(
    {
        "ada-line-9c0cb77d6504d335",
        "asn_1-line-a81d4000083e6f3d",
        "ncl-line-3db4cc2d1678473d",
    }
)

EXPECTED_OUTPUT_SHA256 = {
    "ada-line-9c0cb77d6504d335": (
        "f5a835a8744192f0e651e57639ee4638708ad93bfacbb6b7d01c5aaf622b7d0d"
    ),
    "asn_1-line-a81d4000083e6f3d": (
        "f7691ed9e2436e1e929be711219d5224b9c42674872918ae1371ae475eaa1daf"
    ),
    "brightscript-line-044b596b95b848bb": (
        "859a0efc14b9ae0e7cd3232c9d892d80c594c3810556fbfe7635feab3eb0f1f5"
    ),
    "brightscript-line-a5dd33aa7f0e56bf": (
        "10a60b606a15f0aed83cfa88c22cda4e8d730bb7829ff6ad8b98be093e690aff"
    ),
    "brightscript-line-deee66b2c06be0ff": (
        "713f99a970270831c4f15e44ade9d4df9e56267fad0122b882ec114ffe6811dc"
    ),
    "curry-line-23444fdefd068fb2": (
        "d5c697c721ff70232228bb74e8cde21e185f4b73c44a729622e8e4efa2a08be7"
    ),
    "dataweave-block-176a378804208c72": (
        "e9d89590dc443a2d3dede8d1fcf1e719a1486e239e6143bf40c20e6f9367a677"
    ),
    "dataweave-block-57a44aedd448d3e4": (
        "e9d89590dc443a2d3dede8d1fcf1e719a1486e239e6143bf40c20e6f9367a677"
    ),
    "dataweave-block-7ca8f6613b33c681": (
        "e9d89590dc443a2d3dede8d1fcf1e719a1486e239e6143bf40c20e6f9367a677"
    ),
    "dataweave-block-a1cc56db6a23edfe": (
        "e9d89590dc443a2d3dede8d1fcf1e719a1486e239e6143bf40c20e6f9367a677"
    ),
    "dataweave-block-a466a5cd93c146e3": (
        "e9d89590dc443a2d3dede8d1fcf1e719a1486e239e6143bf40c20e6f9367a677"
    ),
    "dataweave-block-b6abc7d8d1b5348e": (
        "e9d89590dc443a2d3dede8d1fcf1e719a1486e239e6143bf40c20e6f9367a677"
    ),
    "eclipse-line-062ba2e6a23c345e": (
        "9bb59d94c320c29294046b2ac3582015a050a04b7acdb607fe4a90faf7307812"
    ),
    "eclipse-line-3a5ced0da115f684": (
        "fc52abcbd5ded5dcddeee523ac7b99c7bfcfa02b6485879a9bafe8d6d5ea5073"
    ),
    "eclipse-line-e43966759b3fd3af": (
        "ca3533189c7036731f8e2886da972d92d5797c862d860cc19db520427641a83b"
    ),
    "html_django-line-0dde194e6d081bd2": (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    ),
    "html_plus_django-line-79c52bf344795aba": (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    ),
    "monkey_c-block-af494f83e5638bc2": (
        "386a2e1d84acf3048122113013212ffcee77d7cd7b694c319194f08caf0b1d86"
    ),
    "ncl-line-3db4cc2d1678473d": (
        "e450c16a31243104aaa3017b1fbda5811e6675d7494e374f65e911c5485db587"
    ),
    "qml-block-363797b7722b3335": (
        "cf40e6d2e5a93d46d047a6020feb089fb6cb63ae71a36f53c80c00980dd279dd"
    ),
    "qml-block-4fa5a964d4ded78f": (
        "7ca359c714936ad7ff7f6f46e57d0b6c36c433b2fd355853ff5b48bfbb4f7c1e"
    ),
    "qml-block-6ecd753359946215": (
        "8225518fc7e5c54c5f60af4e78eb09c4415769dd35de38fddfd95093634c081e"
    ),
    "qml-block-8b7c308a7e2a43a0": (
        "f13aee06f2b5f4c15c49f64ca574b9d35d15a80aca94ccf0e6557b177cf2b467"
    ),
    "qml-block-a7c77eedd1191b90": (
        "ff4f9fdda913ade97d1a4a6a7ac1a58fef7e338a656bfd1c63d3bac6e23792af"
    ),
    "qml-block-b6cdbae637a76e4a": (
        "a74893821390e595fe4d9b30edb99f801d2acf22ec8be9e46bd9a213616faad9"
    ),
    "qml-block-cd69ffe74ed096b8": (
        "0d0a81c72f52c8923939eb0af00ae75b5775f3eaaec48853d1011ac455e5e62f"
    ),
    "sourcepawn-block-9778f04d187560fa": (
        "5fd9223c64f49bb7dc181ad2bdcaa5c2975607e9ef31afdca902d008c50b4f3b"
    ),
    "sourcepawn-block-de77cb7be550c318": (
        "fe7c0fa5164b5b87cc4fa6f816e31ed53726d120c566ba6a880ed8750a0d134d"
    ),
    "stata-line-8474c8b9c0900aa4": (
        "1c3d52b5ce2c1d5a42dc592338c860d8352956068617196348a4ad68d99758e6"
    ),
    "xbase-block-e6a93f23568f0866": (
        "9d384cd0b6f89c6b05b71ad17a6ce19a22bc3d023aad68c4f39bd93ff03c9b01"
    ),
}


class ImportError(ValueError):
    """Raised when final validation evidence fails an integrity check."""


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _iter_jsonl(path: Path):
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ImportError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ImportError(f"{path}:{line_number}: record must be an object")
            yield row


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return list(_iter_jsonl(path))


def _case_id_set_sha256(case_ids: list[str]) -> str:
    return _sha256_text("".join(f"{case_id}\n" for case_id in sorted(case_ids)))


def _normalized_subsequence(expected: str, raw: str) -> bool:
    raw_iter = iter(raw.replace("\r\n", "\n").replace("\r", "\n"))
    return all(any(char == raw_char for raw_char in raw_iter) for char in expected)


def _load_source_cases(
    path: Path,
    case_ids: set[str],
) -> dict[str, dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    for row in _iter_jsonl(path):
        case_id = row.get("case_id")
        if case_id not in case_ids:
            continue
        if case_id in selected:
            raise ImportError(f"{path}: duplicate source case ID {case_id!r}")
        selected[case_id] = row
    if set(selected) != case_ids:
        missing = sorted(case_ids - set(selected))
        raise ImportError(f"{path}: missing source cases: {missing!r}")
    return selected


def _is_lower_hex(value: object, length: int) -> bool:
    return (
        isinstance(value, str)
        and len(value) == length
        and all(char in "0123456789abcdef" for char in value)
    )


def build_fixture(root: Path, source_manifest_path: Path) -> dict[str, Any]:
    failures_path = root / "two_stage" / "final_failures.jsonl"
    validation_manifest_path = root / "manifest.jsonl"
    summary_path = root / "two_stage" / "run_summary.json"

    observed_hashes = {
        "final_failures_sha256": _sha256_file(failures_path),
        "run_summary_sha256": _sha256_file(summary_path),
        "source_manifest_sha256": _sha256_file(source_manifest_path),
        "validation_manifest_sha256": _sha256_file(validation_manifest_path),
    }
    expected_hashes = {
        "final_failures_sha256": EXPECTED_FINAL_FAILURES_SHA256,
        "run_summary_sha256": EXPECTED_RUN_SUMMARY_SHA256,
        "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        "validation_manifest_sha256": EXPECTED_VALIDATION_MANIFEST_SHA256,
    }
    if observed_hashes != expected_hashes:
        raise ImportError(
            f"source validation artifacts changed: {observed_hashes!r} != {expected_hashes!r}"
        )

    failures = _load_jsonl(failures_path)
    case_ids = [row["case"]["case_id"] for row in failures]
    if len(failures) != EXPECTED_CASE_COUNT or len(set(case_ids)) != EXPECTED_CASE_COUNT:
        raise ImportError("expected exactly 30 unique final failures")
    if set(case_ids) != set(EXPECTED_OUTPUT_SHA256):
        raise ImportError("final failure IDs do not match the pinned output map")
    if _case_id_set_sha256(case_ids) != EXPECTED_CASE_ID_SET_SHA256:
        raise ImportError("final failure case-ID fingerprint changed")

    case_id_set = set(case_ids)
    validation_manifest = _load_source_cases(validation_manifest_path, case_id_set)
    source_manifest = _load_source_cases(source_manifest_path, case_id_set)

    cases = []
    for failure in failures:
        case = failure["case"]
        case_id = case["case_id"]
        manifest_case = validation_manifest[case_id]
        source_case = source_manifest[case_id]
        for field in ("comment_kind", "language", "raw_comment"):
            expected_value = failure["raw_comment"] if field == "raw_comment" else case[field]
            if manifest_case.get(field) != expected_value:
                raise ImportError(f"{case_id}: validation manifest {field} changed")
            if source_case.get(field) != expected_value:
                raise ImportError(f"{case_id}: source manifest {field} changed")

        source_id = source_case.get("source_id")
        if not _is_lower_hex(source_id, 40):
            raise ImportError(f"{case_id}: invalid 40-hex source ID")
        if manifest_case.get("source_id") != source_id:
            raise ImportError(f"{case_id}: validation source ID changed")
        source_excerpt = source_case.get("source_excerpt")
        if not isinstance(source_excerpt, str):
            raise ImportError(f"{case_id}: source excerpt must be text")
        if manifest_case.get("source_excerpt") != source_excerpt:
            raise ImportError(f"{case_id}: validation source excerpt changed")

        expected_cleaned = sanitize_comment(case["language"], failure["raw_comment"])
        expected_sha256 = _sha256_text(expected_cleaned)
        if expected_sha256 != EXPECTED_OUTPUT_SHA256[case_id]:
            raise ImportError(f"{case_id}: audited expected output changed")
        if not _normalized_subsequence(expected_cleaned, failure["raw_comment"]):
            raise ImportError(f"{case_id}: expected output is not deletion-only")

        adjudication = (
            "judge_or_policy_conflict_keep_current"
            if case_id in POLICY_KEEP_IDS
            else "genuine_sanitizer_bug"
        )
        candidate = failure["candidate_cleaned_comment"]
        if adjudication == "genuine_sanitizer_bug" and expected_cleaned == candidate:
            raise ImportError(f"{case_id}: genuine bug still matches the failing candidate")
        if adjudication != "genuine_sanitizer_bug" and expected_cleaned != candidate:
            raise ImportError(f"{case_id}: policy-keep output changed")

        cases.append(
            {
                "adjudication": adjudication,
                "candidate_cleaned_sha256": _sha256_text(candidate),
                "case_id": case_id,
                "comment_kind": case["comment_kind"],
                "expected_cleaned": expected_cleaned,
                "expected_cleaned_sha256": expected_sha256,
                "language": case["language"],
                "prior_final_pass": manifest_case["prior_final_pass"],
                "raw_comment": failure["raw_comment"],
                "raw_comment_sha256": _sha256_text(failure["raw_comment"]),
                "secondary_input_sha256": failure["secondary"]["input_sha256"],
                "source_excerpt_sha256": _sha256_text(source_excerpt),
                "source_id": source_id,
                "validation_origin": manifest_case["validation_origin"],
            }
        )

    decision_counts = Counter(case["adjudication"] for case in cases)
    return {
        "schema_version": SCHEMA_VERSION,
        "case_count": len(cases),
        "case_id_set_sha256": _case_id_set_sha256(case_ids),
        "decision_counts": dict(sorted(decision_counts.items())),
        "language_counts": dict(sorted(Counter(case["language"] for case in cases).items())),
        "source": {
            "dataset": "bigcode/the-stack-v2-dedup",
            **observed_hashes,
        },
        "cases": cases,
    }


def write_fixture(fixture: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        json.dumps(
            fixture,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        dir=output.parent,
        prefix=f".{output.name}.",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=DEFAULT_SOURCE_MANIFEST,
        help="frozen all-language Stack v2 manifest used for compact provenance",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    fixture = build_fixture(args.root, args.source_manifest)
    write_fixture(fixture, args.output)
    print(
        json.dumps(
            {
                "case_count": fixture["case_count"],
                "output": str(args.output),
                "sha256": _sha256_bytes(args.output.read_bytes()),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
