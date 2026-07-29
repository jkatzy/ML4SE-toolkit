#!/usr/bin/env python3
"""Import independently reviewed comment-cleaning regressions.

The two-stage LLM judge records whether a sanitizer candidate is correct, but it
does not provide an exact expected string.  This importer therefore requires a
separate reviewed-oracle JSONL file containing literal expected outputs plus the
oracle runner's exception JSONL.  It never imports or calls
``CommentSanitizer``.

Each annotation line has this exact shape::

    {
      "case_id": "...",
      "raw_sha256": "...",
      "expected_cleaned": "literal exact output",
      "expected_cleaned_sha256": "...",
      "disposition": "confirmed_bug",
      "oracle": {
        "method": "independent_consensus",
        "note": "why this exact edit satisfies the cleaning contract",
        "review_status": "approved",
        "reviewers": ["oracle-author", "oracle-reviewer"]
      }
    }

``disposition`` may instead be ``judge_false_positive`` only when the reviewed
literal exactly equals the frozen sanitizer candidate.  Expected text must use
LF newlines and be obtainable from the newline-normalized raw text by deletion;
these checks prevent an oracle from silently adding or rewriting content.

The oracle runner deliberately writes non-literal outcomes such as
``extraction_invalid`` and ``ambiguous`` to ``oracle_exceptions.jsonl`` instead
of fabricating an expected sanitizer result.  Schema-v5 fixtures preserve that
separation: exact literals become executable sanitizer regressions, invalid
boundaries become small synthetic structural probes, and all remaining exception
statuses remain explicit accounting-only cases. Original boundary hashes and
byte lengths remain pinned without retaining source-sized overcaptures.
Every rendered case also retains only its Stack v2 source ID and a SHA-256 of
the source excerpt. Rendered fixtures omit repository paths, source context,
and review/judge prose; the frozen input hashes preserve the audit trail
without copying that material into the test corpus. The two oracle files must
be disjoint and their case-ID union must exactly equal the frozen failure set.

The July 2026 all-language run is frozen by default.  The expected source hashes
can be overridden explicitly when importing a later reviewed run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence

SCHEMA_VERSION = 5
ORACLE_EXCEPTION_SCHEMA_VERSION = 1
DEFAULT_OUTPUT_DIR = Path("tests/fixtures/comment_cleaning_regressions")
DEFAULT_FAMILY_FIXTURE_DIR = Path("tests/fixtures/comment_cleaning")
DEFAULT_SOURCE_MANIFEST = Path("tmp/stack_v2_comment_cleaner_all_languages_50/manifest.jsonl")
EXPECTED_OUTPUT_DIR = (Path(__file__).resolve().parents[1] / DEFAULT_OUTPUT_DIR).resolve()
SENTINEL_NAME = ".generated-by-import_comment_cleaning_regressions"
SENTINEL_CONTENT = (
    f"schema={SCHEMA_VERSION}\nowner=scripts/import_comment_cleaning_regressions.py\n"
)
NOTICE_NAME = "NOTICE.md"
NOTICE_TEXT = """# Comment-cleaning regression fixture provenance

These fixtures were generated from comment candidates sampled from
`bigcode/the-stack-v2-dedup`. Its source content is archived by Software Heritage.
The manifest pins the frozen run, candidate set, and reviewed oracle inputs by
SHA-256.

Every case stores the 40-hex Stack v2 source ID and the SHA-256 of its source
excerpt selected from the pinned source manifest.
Executable sanitizer cases keep exact raw and expected comment text. Invalid
extraction cases retain the original raw SHA-256 and UTF-8 byte length but use
small synthetic structural probes instead of source-sized overcaptures.
Accounting-only cases retain hashes and dispositions without raw literals.
Repository names, paths, surrounding source, and judge/reviewer prose are
intentionally omitted.

The frozen run did not include exact per-file license metadata. Treat retained
literals as test-only excerpts and consult the underlying Stack v2/Software
Heritage record before reuse outside regression testing.
"""

FROZEN_FAILURES_SHA256 = "ef06ad5770587e095b01d75c110a0d36da9812fb4a80109c89c75f30a4632cfc"
FROZEN_RUN_SUMMARY_SHA256 = "d7f9862148c5e555603557043a47c9c751a905003d160e0f9e1c51d8391a8cd0"
FROZEN_SOURCE_MANIFEST_SHA256 = "1e87230b75165ae76583abdb48045e9ce9c5f4287135e8c4e564f400e230dcc0"
FROZEN_CASE_ID_SET_SHA256 = "8e854fb306bd97bf73cb756bd5b8f8cf8f5c25b29bd97a3541f7140042d01fd5"
FROZEN_CASE_COUNT = 1986

APPROVED_REVIEW_STATUS = "approved"
ALLOWED_DISPOSITIONS = frozenset({"confirmed_bug", "judge_false_positive"})
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
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
SOURCE_ID_PATTERN = re.compile(r"[0-9a-f]{40}")
SAFE_FAMILY_PATTERN = re.compile(r"[a-z0-9_]+")

# Frozen policy exceptions are accepted only for these complete identities.
# Values are ``(language, kind, syntax, raw_sha256, policy_subkind)``.
CLEANING_POLICY_DISPUTES = {
    "abap_cds-line-bced7abdf245bf3d": (
        "abap_cds",
        "line",
        "//",
        "577911ee3a00ddeed7ad953218d443b1d50b907f548c81227e81f05c390476c8",
        "normalization",
    ),
    "abap_cds-line-be44644a06c6d23a": (
        "abap_cds",
        "line",
        "//",
        "b0cfe56a8374c9886ed4aaf3b7856de02463342b4a60ad7c3102e79e697e4c21",
        "normalization",
    ),
    "click-block-1d9ab161b43f027d": (
        "click",
        "block",
        "/*...*/",
        "cb20f83b6d90ac40b98585d2b753d7b4520d65223e4472621b6dd77929cc7bce",
        "content_or_syntax",
    ),
    "literate_haskell-nested-762fdebeedc338fb": (
        "literate_haskell",
        "nested",
        "{-...-}",
        "b7a69c320c65e3db93c27d02f457c67cd88770fec7446356e460fe06bfdb28c0",
        "content_or_syntax",
    ),
    "metal-block-f81afe598c049d75": (
        "metal",
        "block",
        "/*...*/",
        "7e62026c34ed31e508f19038807e588644cf245a9d305222d81db19e36a86774",
        "normalization",
    ),
    "moocode-block-0d312c0deb49121a": (
        "moocode",
        "block",
        "/*...*/",
        "9ae80400f399e703c3b8f62e16e1b141bb890150073ddd9a394f44db80ffb02f",
        "normalization",
    ),
    "powerbuilder-nested-2fee93e4074c3191": (
        "powerbuilder",
        "nested",
        "/*...*/",
        "b90b6a5f6ad948c9a979b3fcb1e33c233b5eb93cc327000b524eb388ccb358b2",
        "normalization",
    ),
    "powerbuilder-nested-df42c6b65e91a169": (
        "powerbuilder",
        "nested",
        "/*...*/",
        "b90b6a5f6ad948c9a979b3fcb1e33c233b5eb93cc327000b524eb388ccb358b2",
        "normalization",
    ),
    "propeller_spin-block-189589f644925d3d": (
        "propeller_spin",
        "block",
        "{...}",
        "af0b2afce5ffcb1ceae7cf67c290b73ea235f046de72f88132d5ea1cd85d34f4",
        "normalization",
    ),
    "win32_message_file-directive-29b9fc01dd8a2fec": (
        "win32_message_file",
        "directive",
        ";/*",
        "17180b94340a349642c0c0104350abafea9d963b569c64374b294d3e187204e3",
        "normalization",
    ),
    "win32_message_file-directive-34d12e114699e434": (
        "win32_message_file",
        "directive",
        ";/*",
        "ebd6a18cb1118f2df1f6e9173af5fec677fdd6283c1c625fb4ace92a18a8cdd0",
        "normalization",
    ),
    "win32_message_file-directive-48b4e07259b92b78": (
        "win32_message_file",
        "directive",
        ";/*",
        "d70a9842e1f39aaaedb15e720375a6720285a51d6d4406d97b1c10021f9d54bc",
        "normalization",
    ),
    "win32_message_file-directive-4979b3181a921780": (
        "win32_message_file",
        "directive",
        ";/*",
        "c33e87e9cc260a622d5b295e19264c3f4e47125ab4988a079cad2cf33eee06f7",
        "normalization",
    ),
    "win32_message_file-directive-4fa02c036ebaf3ec": (
        "win32_message_file",
        "directive",
        ";/*",
        "01aca75a0532c62a910a03ea192956c3d28890424b43d4e846bc14597f702357",
        "normalization",
    ),
    "win32_message_file-directive-52dacc5b1b50ff39": (
        "win32_message_file",
        "directive",
        ";/*",
        "64edf49ec35cd1ee5a1abd74b103cc3f1a574ac8ccd2973ebd087f8bf494f547",
        "normalization",
    ),
    "win32_message_file-directive-5833ef003c797086": (
        "win32_message_file",
        "directive",
        ";/*",
        "bde2f563c723951206fc81a4ff04910f77f6de816d620efb4a00794922bd13b2",
        "normalization",
    ),
    "win32_message_file-directive-5b91f9c4b962d7a6": (
        "win32_message_file",
        "directive",
        ";/*",
        "a7313ede344020a6ab0519ff7dfd0cef1b6d59f3673953963c9d73e8b179fa16",
        "normalization",
    ),
    "win32_message_file-directive-745134bc5dfcb6a1": (
        "win32_message_file",
        "directive",
        ";/*",
        "2b45f6efbca51f6c7e8edc5c1af3851d2bfd4e87f43f9886888e47356800897f",
        "normalization",
    ),
    "win32_message_file-directive-a2adfa284a1c6595": (
        "win32_message_file",
        "directive",
        ";/*",
        "2859add13421db171edc5c12f8b2af5687ad3f6a6dac72c8f71dc1257596f36a",
        "normalization",
    ),
    "win32_message_file-directive-ac6c29e0ea184679": (
        "win32_message_file",
        "directive",
        ";/*",
        "d7f268044ab28e0e3d22f84c0f17824e26a0f47634e5536dd3b7052a1cda0892",
        "normalization",
    ),
    "win32_message_file-directive-b3cc78d98d8ff041": (
        "win32_message_file",
        "directive",
        ";/*",
        "c18cd019e3f5fdf0b791fc1ae908ee7d979d98054f8a8d65d3ca9d43a5e39a4a",
        "normalization",
    ),
    "win32_message_file-directive-c51c344493dcf2e8": (
        "win32_message_file",
        "directive",
        ";/*",
        "ed92119222204e06d241def71ecc03cb252dbbebca1bb4427362b8186bdb8548",
        "normalization",
    ),
    "win32_message_file-directive-d924d32d0b7c5058": (
        "win32_message_file",
        "directive",
        ";/*",
        "1d46ed1d3c0b9db997ce43b394d1bf57380f322042acae5d7f06ff7e25bcbf50",
        "normalization",
    ),
    "x_bit_map-block-7aab0cb7d5f2e143": (
        "x_bit_map",
        "block",
        "/*...*/",
        "8dfbe2a3db755dcca4156b88ffbf5e2d0d702d7d6f26a13b66bed7f3a74717bb",
        "content_or_syntax",
    ),
    "x_bit_map-block-86708f0043fbb654": (
        "x_bit_map",
        "block",
        "/*...*/",
        "eee84d521496ec9c66e8eb87a42ba960a22c9ee42cc97cbcfb38fc2ff911527a",
        "content_or_syntax",
    ),
    "x_bit_map-block-9d0db1b03af112a0": (
        "x_bit_map",
        "block",
        "/*...*/",
        "23a3051a5015ea98a31533e0008afcbbbae15e030b4d70ff980fc5553460afac",
        "content_or_syntax",
    ),
    "x_bitmap-block-63519f13afd78a86": (
        "x_bitmap",
        "block",
        "/*...*/",
        "eee84d521496ec9c66e8eb87a42ba960a22c9ee42cc97cbcfb38fc2ff911527a",
        "content_or_syntax",
    ),
    "x_bitmap-block-76553f7a089df85f": (
        "x_bitmap",
        "block",
        "/*...*/",
        "23a3051a5015ea98a31533e0008afcbbbae15e030b4d70ff980fc5553460afac",
        "content_or_syntax",
    ),
    "x_bitmap-block-d40eae17460a16a0": (
        "x_bitmap",
        "block",
        "/*...*/",
        "8dfbe2a3db755dcca4156b88ffbf5e2d0d702d7d6f26a13b66bed7f3a74717bb",
        "content_or_syntax",
    ),
}

CONFLICT_LANGUAGE_ALIASES = {
    "asp": "asp",
    "asp_net": "asp",
    "aspnet": "asp",
    "perl6": "perl6",
    "raku": "perl6",
    "x_bit_map": "x_bitmap",
    "x_bitmap": "x_bitmap",
}

ANNOTATION_KEYS = frozenset(
    {
        "case_id",
        "disposition",
        "expected_cleaned",
        "expected_cleaned_sha256",
        "oracle",
        "raw_sha256",
    }
)
ORACLE_KEYS = frozenset({"method", "note", "review_status", "reviewers"})
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
RESOLUTION_RESULT_KEYS = frozenset(
    {
        "confidence",
        "decision",
        "model",
        "rationale",
    }
)

SANITIZER_CATEGORY = "sanitizer"
EXTRACTOR_BOUNDARY_CATEGORY = "extractor_boundary"
ORACLE_EXCEPTION_CATEGORY = "oracle_exception"
CASE_CATEGORIES = (
    SANITIZER_CATEGORY,
    EXTRACTOR_BOUNDARY_CATEGORY,
    ORACLE_EXCEPTION_CATEGORY,
)

# This disagreement was separately SHA-pinned as an executable sanitizer
# regression. Keep its proposal literal for that focused test while every other
# unresolved exception remains accounting-only.
EXECUTABLE_EXCEPTION_REGRESSION_IDS = frozenset({"ant_build_system-block-a4061d3caf4c1257"})

# A later policy-oracle audit superseded two literals from the original
# annotation file. The importer remains sanitizer-independent, so the reviewed
# replacement literals are frozen here instead of recomputed from current code.
ADJUDICATED_EXPECTED_OUTPUTS = {
    "cuda-line-9be1a4d25d76a815": (
        "===------------ omp_data.cu - NVPTX OpenMP GPU objects --------- CUDA -*-===\n"
        "\n"
        "Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.\n"
        "See https://llvm.org/LICENSE.txt for license information.\n"
        "SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception\n"
        "\n"
        "===----------------------------------------------------------------------===\n"
        "\n"
        "This file contains the data objects used on the GPU device.\n"
    ),
    "makefile-line-04aa358fc4ea11c8": (
        "License\n"
        "\n"
        "Copyright 2000-2002.  SpeechWorks International, Inc.  All rights reserved.\n"
        "\n"
        "Use of this software is subject to certain restrictions and limitations\n"
        "set forth in a license agreement entered into between SpeechWorks\n"
        "International Inc. and the licensee of this software.  Please refer\n"
        "to the license agreement for license use rights and restrictions.\n"
        "\n"
        "SpeechWorks is a registered trademark, and SpeechWorks Here,\n"
        "DialogModules and the SpeechWorks logo are trademarks of SpeechWorks\n"
        "International, Inc. in the United States and other countries.\n"
        "\n"
        "\n"
        "SBjsi, OpenSpeech Browser implementation of the VXIjsi interface\n"
        "UNIX make file"
    ),
}


class RegressionImportError(ValueError):
    """Raised when source data or reviewed annotations are invalid."""


@dataclass(frozen=True)
class SourceFailure:
    """One frozen failure emitted by the two-stage judge."""

    case_id: str
    language: str
    family_name: str
    comment_kind: str
    syntax_label: str
    repo: str
    path: str
    raw_comment: str
    candidate_cleaned_comment: str
    cleaning_contract: str
    judge_input_sha256: str
    judge_rationale: str
    primary_model: str
    secondary_model: str
    primary_cleaning_correct: bool
    secondary_cleaning_correct: bool


@dataclass(frozen=True)
class SourceProvenance:
    """Compact provenance selected from one frozen source-manifest row."""

    source_id: str
    source_excerpt_sha256: str


@dataclass(frozen=True)
class ReviewedOracle:
    """One independently reviewed literal cleaning oracle."""

    case_id: str
    raw_sha256: str
    expected_cleaned: str
    expected_cleaned_sha256: str
    disposition: str
    method: str
    note: str
    reviewers: tuple[str, ...]


@dataclass(frozen=True)
class OracleException:
    """One exact exception row emitted by the independent oracle pipeline."""

    case_id: str
    language: str
    comment_kind: str
    syntax_label: str
    raw_sha256: str
    status: str
    extraction_boundary_invalid: bool
    detail: str
    reviewers: tuple[str, ...]
    payload: Mapping[str, Any]


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse the explicit source, annotation, and output paths."""

    parser = argparse.ArgumentParser(
        description=(
            "Validate reviewed exact comment-cleaning oracles and import them "
            "as deterministic family-sharded regression fixtures."
        )
    )
    parser.add_argument(
        "--failures",
        type=Path,
        required=True,
        help="Frozen two-stage final_failures.jsonl.",
    )
    parser.add_argument(
        "--run-summary",
        type=Path,
        required=True,
        help="Frozen run_summary.json corresponding to --failures.",
    )
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=DEFAULT_SOURCE_MANIFEST,
        help=(
            "Frozen Stack v2 source manifest used to validate failure identity "
            f"and attach compact provenance (default: {DEFAULT_SOURCE_MANIFEST})."
        ),
    )
    parser.add_argument(
        "--annotations",
        type=Path,
        required=True,
        help=(
            "reviewed_annotations.jsonl containing exact outputs for clean "
            "consensus cases; may be empty when every case is exceptional."
        ),
    )
    parser.add_argument(
        "--oracle-exceptions",
        type=Path,
        required=True,
        help=(
            "oracle_exceptions.jsonl emitted beside --annotations; may be empty, "
            "but its IDs and annotation IDs must partition every frozen failure."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Fixture output directory (default: {DEFAULT_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--family-fixture-dir",
        type=Path,
        default=DEFAULT_FAMILY_FIXTURE_DIR,
        help=(
            "Generated registry-family fixture directory used only to map "
            f"languages to families (default: {DEFAULT_FAMILY_FIXTURE_DIR})."
        ),
    )
    parser.add_argument(
        "--expected-failures-sha256",
        default=FROZEN_FAILURES_SHA256,
        help="Required SHA-256 of --failures.",
    )
    parser.add_argument(
        "--expected-run-summary-sha256",
        default=FROZEN_RUN_SUMMARY_SHA256,
        help="Required SHA-256 of --run-summary.",
    )
    parser.add_argument(
        "--expected-source-manifest-sha256",
        default=FROZEN_SOURCE_MANIFEST_SHA256,
        help="Required source-manifest SHA-256 recorded by --run-summary.",
    )
    parser.add_argument(
        "--expected-case-id-set-sha256",
        default=FROZEN_CASE_ID_SET_SHA256,
        help="Required SHA-256 of sorted case IDs joined by newline.",
    )
    parser.add_argument(
        "--expected-case-count",
        type=int,
        default=FROZEN_CASE_COUNT,
        help=(
            "Required failure count and required size of the annotation/exception case-ID union."
        ),
    )
    output_mode = parser.add_mutually_exclusive_group()
    output_mode.add_argument(
        "--check",
        action="store_true",
        help="Validate that existing fixture files equal the deterministic import.",
    )
    output_mode.add_argument(
        "--force",
        action="store_true",
        help="Replace differing fixture JSON and prune stale JSON in the output directory.",
    )
    return parser.parse_args(argv)


def _duplicate_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RegressionImportError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _loads_json(text: str, context: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_duplicate_rejecting_object)
    except (json.JSONDecodeError, RegressionImportError) as exc:
        raise RegressionImportError(f"{context}: invalid JSON: {exc}") from exc


def _load_json_file(path: Path) -> dict[str, Any]:
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise RegressionImportError(f"cannot read UTF-8 JSON file {path}: {exc}") from exc
    value = _loads_json(text, str(path))
    return _require_object(value, str(path))


def _load_jsonl(
    path: Path,
    *,
    allow_empty: bool = False,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for line_number, line in enumerate(handle, 1):
                context = f"{path}:{line_number}"
                if not line.strip():
                    raise RegressionImportError(f"{context}: blank JSONL lines are forbidden")
                value = _loads_json(line, context)
                rows.append(_require_object(value, context))
    except (OSError, UnicodeDecodeError) as exc:
        raise RegressionImportError(f"cannot read UTF-8 JSONL file {path}: {exc}") from exc
    if not rows and not allow_empty:
        raise RegressionImportError(f"{path}: JSONL file is empty")
    return rows


def _require_object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RegressionImportError(f"{context}: expected a JSON object")
    return value


def _require_exact_keys(value: Mapping[str, Any], expected: frozenset[str], context: str) -> None:
    actual = frozenset(value)
    if actual == expected:
        return
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    raise RegressionImportError(
        f"{context}: object keys differ; missing={missing!r} extra={extra!r}"
    )


def _require_string(
    value: Mapping[str, Any],
    key: str,
    context: str,
    *,
    allow_empty: bool = False,
) -> str:
    result = value.get(key)
    if not isinstance(result, str) or (not allow_empty and not result):
        requirement = "a string" if allow_empty else "a non-empty string"
        raise RegressionImportError(f"{context}.{key}: expected {requirement}")
    return result


def _require_integer(value: Mapping[str, Any], key: str, context: str) -> int:
    result = value.get(key)
    if not isinstance(result, int) or isinstance(result, bool):
        raise RegressionImportError(f"{context}.{key}: expected an integer")
    return result


def _require_confidence(
    value: Mapping[str, Any],
    context: str,
) -> float:
    result = value.get("confidence")
    if not isinstance(result, (int, float)) or isinstance(result, bool) or not 0 <= result <= 1:
        raise RegressionImportError(f"{context}.confidence: expected a number from 0 through 1")
    return float(result)


def _require_sha256(value: Mapping[str, Any], key: str, context: str) -> str:
    result = _require_string(value, key, context)
    if SHA256_PATTERN.fullmatch(result) is None:
        raise RegressionImportError(f"{context}.{key}: expected a lowercase hexadecimal SHA-256")
    return result


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise RegressionImportError(f"string cannot be encoded as UTF-8: {exc}") from exc
    return _sha256_bytes(encoded)


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                hasher.update(chunk)
    except OSError as exc:
        raise RegressionImportError(f"cannot hash {path}: {exc}") from exc
    return hasher.hexdigest()


def _case_id_set_sha256(case_ids: Iterable[str]) -> str:
    ordered = sorted(case_ids)
    if any(not case_id or "\n" in case_id or "\r" in case_id for case_id in ordered):
        raise RegressionImportError("case IDs must be non-empty single-line strings")
    return _sha256_text("".join(f"{case_id}\n" for case_id in ordered))


def _normalize_newlines(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def _is_subsequence(expected: str, normalized_raw: str) -> bool:
    """Return whether cleaning can produce ``expected`` only by deleting text."""

    position = 0
    for character in expected:
        position = normalized_raw.find(character, position)
        if position < 0:
            return False
        position += 1
    return True


def _load_language_families(fixture_dir: Path) -> dict[str, str]:
    """Load language-to-family metadata without importing cleaner code."""

    paths = sorted(fixture_dir.glob("*.json")) if fixture_dir.is_dir() else []
    if not paths:
        raise RegressionImportError(
            f"{fixture_dir}: no generated comment-cleaning family fixtures found"
        )

    language_families: dict[str, str] = {}
    seen_families: set[str] = set()
    for path in paths:
        payload = _load_json_file(path)
        context = str(path)
        family_name = _require_string(payload, "family_name", context)
        if SAFE_FAMILY_PATTERN.fullmatch(family_name) is None:
            raise RegressionImportError(f"{context}: unsafe registry family name {family_name!r}")
        if family_name in seen_families:
            raise RegressionImportError(f"{context}: duplicate registry family {family_name!r}")
        seen_families.add(family_name)

        languages = payload.get("language_keys")
        if not isinstance(languages, list) or not languages:
            raise RegressionImportError(f"{context}.language_keys: expected a non-empty JSON array")
        for language in languages:
            if not isinstance(language, str) or not language:
                raise RegressionImportError(f"{context}.language_keys: expected non-empty strings")
            if language in language_families:
                raise RegressionImportError(f"{context}: duplicate registry language {language!r}")
            language_families[language] = family_name
    return language_families


def _load_source_failures(
    path: Path,
    language_families: Mapping[str, str],
) -> dict[str, SourceFailure]:
    failures: dict[str, SourceFailure] = {}
    cleaning_contract: str | None = None
    for line_number, row in enumerate(_load_jsonl(path), 1):
        context = f"{path}:{line_number}"
        case = _require_object(row.get("case"), f"{context}.case")
        case_id = _require_string(case, "case_id", f"{context}.case")
        if case_id in failures:
            raise RegressionImportError(f"{context}: duplicate case_id {case_id!r}")

        language = _require_string(case, "language", f"{context}.case")
        family_name = language_families.get(language)
        if family_name is None:
            raise RegressionImportError(f"{context}: unsupported registry language {language!r}")
        if SAFE_FAMILY_PATTERN.fullmatch(family_name) is None:
            raise RegressionImportError(f"{context}: unsafe registry family name {family_name!r}")

        final_decision = _require_object(row.get("final_decision"), f"{context}.final_decision")
        decided_by = _require_string(final_decision, "decided_by", f"{context}.final_decision")
        if (
            final_decision.get("verdict") != "fail"
            or final_decision.get("cleaning_correct") is not False
        ):
            raise RegressionImportError(f"{context}: final decision is not a cleaning failure")
        deciding_result = _require_object(row.get(decided_by), f"{context}.{decided_by}")

        row_contract = _require_string(row, "cleaning_contract", context)
        if cleaning_contract is None:
            cleaning_contract = row_contract
        elif cleaning_contract != row_contract:
            raise RegressionImportError(
                f"{context}: cleaning contract differs from previous failures"
            )

        primary = _require_object(row.get("primary"), f"{context}.primary")
        secondary = _require_object(row.get("secondary"), f"{context}.secondary")
        for stage_name, result in (
            ("primary", primary),
            ("secondary", secondary),
        ):
            if result.get("verdict") != "fail" or result.get("cleaning_correct") is not False:
                raise RegressionImportError(
                    f"{context}.{stage_name}: expected a frozen cleaning failure"
                )
        failures[case_id] = SourceFailure(
            case_id=case_id,
            language=language,
            family_name=family_name,
            comment_kind=_require_string(case, "comment_kind", f"{context}.case"),
            syntax_label=_require_string(case, "syntax_label", f"{context}.case", allow_empty=True),
            repo=_require_string(case, "repo", f"{context}.case", allow_empty=True),
            path=_require_string(case, "path", f"{context}.case", allow_empty=True),
            raw_comment=_require_string(row, "raw_comment", context, allow_empty=True),
            candidate_cleaned_comment=_require_string(
                row, "candidate_cleaned_comment", context, allow_empty=True
            ),
            cleaning_contract=row_contract,
            judge_input_sha256=_require_sha256(
                deciding_result, "input_sha256", f"{context}.{decided_by}"
            ),
            judge_rationale=_require_string(
                deciding_result, "rationale", f"{context}.{decided_by}"
            ),
            primary_model=_require_string(primary, "model", f"{context}.primary"),
            secondary_model=_require_string(secondary, "model", f"{context}.secondary"),
            primary_cleaning_correct=primary["cleaning_correct"],
            secondary_cleaning_correct=secondary["cleaning_correct"],
        )
    return failures


def _load_source_provenance(
    path: Path,
    failures: Mapping[str, SourceFailure],
) -> tuple[dict[str, SourceProvenance], str]:
    """Stream and validate the frozen source manifest.

    Every row is parsed and every case ID participates in duplicate detection.
    Only provenance for the selected failure set is retained in memory.
    """

    selected: dict[str, SourceProvenance] = {}
    seen_case_ids: set[str] = set()
    hasher = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for line_number, raw_line in enumerate(handle, 1):
                context = f"{path}:{line_number}"
                hasher.update(raw_line)
                if not raw_line.strip():
                    raise RegressionImportError(f"{context}: blank JSONL lines are forbidden")
                try:
                    line = raw_line.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise RegressionImportError(
                        f"{context}: invalid UTF-8 JSONL row: {exc}"
                    ) from exc
                row = _require_object(_loads_json(line, context), context)
                case_id = _require_string(row, "case_id", context)
                if case_id in seen_case_ids:
                    raise RegressionImportError(f"{context}: duplicate case_id {case_id!r}")
                seen_case_ids.add(case_id)

                source_id = _require_string(row, "source_id", context)
                if SOURCE_ID_PATTERN.fullmatch(source_id) is None:
                    raise RegressionImportError(
                        f"{context}.source_id: expected 40 lowercase hexadecimal characters"
                    )
                source_excerpt = _require_string(
                    row,
                    "source_excerpt",
                    context,
                    allow_empty=True,
                )

                failure = failures.get(case_id)
                if failure is None:
                    continue
                identity_fields = (
                    ("language", False),
                    ("comment_kind", False),
                    ("syntax_label", True),
                    ("raw_comment", True),
                )
                mismatches = []
                for field_name, allow_empty in identity_fields:
                    source_value = _require_string(
                        row,
                        field_name,
                        context,
                        allow_empty=allow_empty,
                    )
                    if source_value != getattr(failure, field_name):
                        mismatches.append(field_name)
                if mismatches:
                    raise RegressionImportError(
                        f"{context}: source manifest identity differs from frozen "
                        f"failure {case_id!r} in {', '.join(mismatches)}"
                    )
                selected[case_id] = SourceProvenance(
                    source_id=source_id,
                    source_excerpt_sha256=_sha256_text(source_excerpt),
                )
    except OSError as exc:
        raise RegressionImportError(f"cannot read UTF-8 JSONL file {path}: {exc}") from exc

    if not seen_case_ids:
        raise RegressionImportError(f"{path}: JSONL file is empty")
    missing = sorted(set(failures) - set(selected))
    if missing:
        raise RegressionImportError(
            "source manifest does not cover every frozen failure; "
            f"missing={missing[:10]!r} missing_count={len(missing)}"
        )
    if set(selected) != set(failures):
        raise RegressionImportError(
            "source manifest selected provenance does not exactly cover failures"
        )
    return selected, hasher.hexdigest()


def _load_reviewed_oracles(path: Path) -> dict[str, ReviewedOracle]:
    annotations: dict[str, ReviewedOracle] = {}
    for line_number, row in enumerate(
        _load_jsonl(path, allow_empty=True),
        1,
    ):
        context = f"{path}:{line_number}"
        _require_exact_keys(row, ANNOTATION_KEYS, context)
        case_id = _require_string(row, "case_id", context)
        if case_id in annotations:
            raise RegressionImportError(f"{context}: duplicate case_id {case_id!r}")

        disposition = _require_string(row, "disposition", context)
        if disposition not in ALLOWED_DISPOSITIONS:
            raise RegressionImportError(
                f"{context}.disposition: expected one of {sorted(ALLOWED_DISPOSITIONS)!r}"
            )

        oracle = _require_object(row.get("oracle"), f"{context}.oracle")
        _require_exact_keys(oracle, ORACLE_KEYS, f"{context}.oracle")
        review_status = _require_string(oracle, "review_status", f"{context}.oracle")
        if review_status != APPROVED_REVIEW_STATUS:
            raise RegressionImportError(
                f"{context}.oracle.review_status: expected {APPROVED_REVIEW_STATUS!r}"
            )
        reviewers_value = oracle.get("reviewers")
        if not isinstance(reviewers_value, list):
            raise RegressionImportError(f"{context}.oracle.reviewers: expected a JSON array")
        if any(not isinstance(reviewer, str) or not reviewer for reviewer in reviewers_value):
            raise RegressionImportError(
                f"{context}.oracle.reviewers: reviewer names must be non-empty strings"
            )
        reviewers = tuple(sorted(reviewers_value))
        if len(reviewers) < 2 or len(reviewers) != len(set(reviewers)):
            raise RegressionImportError(
                f"{context}.oracle.reviewers: expected at least two distinct "
                "non-empty reviewer names"
            )

        expected_cleaned = _require_string(row, "expected_cleaned", context, allow_empty=True)
        expected_sha256 = _require_sha256(row, "expected_cleaned_sha256", context)
        if _sha256_text(expected_cleaned) != expected_sha256:
            raise RegressionImportError(
                f"{context}: expected_cleaned_sha256 does not match the literal"
            )

        annotations[case_id] = ReviewedOracle(
            case_id=case_id,
            raw_sha256=_require_sha256(row, "raw_sha256", context),
            expected_cleaned=expected_cleaned,
            expected_cleaned_sha256=expected_sha256,
            disposition=disposition,
            method=_require_string(oracle, "method", f"{context}.oracle"),
            note=_require_string(oracle, "note", f"{context}.oracle"),
            reviewers=reviewers,
        )
    return annotations


def _validate_oracle_stage_result(
    value: Any,
    *,
    stage: str,
    context: str,
) -> dict[str, Any]:
    result = _require_object(value, context)
    if stage == "proposal":
        expected_keys = PROPOSAL_RESULT_KEYS
    elif stage == "review":
        expected_keys = REVIEW_RESULT_KEYS
    elif stage == "resolution":
        expected_keys = RESOLUTION_RESULT_KEYS
    else:
        raise AssertionError(f"unsupported oracle stage: {stage}")
    _require_exact_keys(result, expected_keys, context)
    _require_string(result, "model", context)
    _require_string(result, "rationale", context)
    _require_confidence(result, context)

    if stage in {"proposal", "review"}:
        disposition = _require_string(result, "disposition", context)
        if disposition not in ORACLE_DISPOSITIONS:
            raise RegressionImportError(
                f"{context}.disposition: expected one of {sorted(ORACLE_DISPOSITIONS)!r}"
            )
        expected_cleaned = _require_string(
            result,
            "expected_cleaned",
            context,
            allow_empty=True,
        )
        if disposition != "clean" and expected_cleaned:
            raise RegressionImportError(
                f"{context}.expected_cleaned: expected an empty string for {disposition!r}"
            )

    if stage == "review":
        decision = _require_string(result, "decision", context)
        if decision not in {"approve", "replace"}:
            raise RegressionImportError(f"{context}.decision: expected 'approve' or 'replace'")
    elif stage == "resolution":
        decision = _require_string(result, "decision", context)
        if decision not in {"accept_reviewer", "unresolved"}:
            raise RegressionImportError(
                f"{context}.decision: expected 'accept_reviewer' or 'unresolved'"
            )
    return result


def _load_oracle_exceptions(path: Path) -> dict[str, OracleException]:
    """Load the oracle runner's documented exception rows without reinterpretation."""

    exceptions: dict[str, OracleException] = {}
    for line_number, row in enumerate(_load_jsonl(path, allow_empty=True), 1):
        context = f"{path}:{line_number}"
        _require_exact_keys(row, ORACLE_EXCEPTION_KEYS, context)
        if _require_integer(row, "schema_version", context) != (ORACLE_EXCEPTION_SCHEMA_VERSION):
            raise RegressionImportError(
                f"{context}.schema_version: expected {ORACLE_EXCEPTION_SCHEMA_VERSION}"
            )

        case_id = _require_string(row, "case_id", context)
        if case_id in exceptions:
            raise RegressionImportError(f"{context}: duplicate case_id {case_id!r}")
        language = _require_string(row, "language", context)
        comment_kind = _require_string(row, "comment_kind", context)
        syntax_label = _require_string(
            row,
            "syntax_label",
            context,
            allow_empty=True,
        )
        status = _require_string(row, "status", context)
        if status not in ALLOWED_EXCEPTION_STATUSES:
            raise RegressionImportError(
                f"{context}.status: expected one of {sorted(ALLOWED_EXCEPTION_STATUSES)!r}"
            )

        boundary_invalid = row.get("extraction_boundary_invalid")
        if not isinstance(boundary_invalid, bool):
            raise RegressionImportError(
                f"{context}.extraction_boundary_invalid: expected a boolean"
            )
        if boundary_invalid != (status == "extraction_invalid"):
            raise RegressionImportError(
                f"{context}: extraction_boundary_invalid must be true exactly "
                "when status is 'extraction_invalid'"
            )

        reviewers_value = row.get("reviewers")
        if not isinstance(reviewers_value, list):
            raise RegressionImportError(f"{context}.reviewers: expected a JSON array")
        if any(not isinstance(reviewer, str) or not reviewer for reviewer in reviewers_value):
            raise RegressionImportError(
                f"{context}.reviewers: reviewer names must be non-empty strings"
            )
        reviewers = tuple(reviewers_value)
        if (
            list(reviewers) != sorted(reviewers)
            or len(reviewers) < 2
            or len(reviewers) != len(set(reviewers))
        ):
            raise RegressionImportError(
                f"{context}.reviewers: expected canonical sorted order and at "
                "least two distinct reviewers"
            )

        proposal = _validate_oracle_stage_result(
            row.get("proposal"),
            stage="proposal",
            context=f"{context}.proposal",
        )
        review = _validate_oracle_stage_result(
            row.get("review"),
            stage="review",
            context=f"{context}.review",
        )
        resolution_value = row.get("resolution")
        resolution = (
            None
            if resolution_value is None
            else _validate_oracle_stage_result(
                resolution_value,
                stage="resolution",
                context=f"{context}.resolution",
            )
        )
        if review["decision"] == "approve":
            if (
                review["disposition"] != proposal["disposition"]
                or review["expected_cleaned"] != proposal["expected_cleaned"]
            ):
                raise RegressionImportError(
                    f"{context}: approved review does not exactly copy proposal"
                )
            if resolution is not None:
                raise RegressionImportError(
                    f"{context}: approved review must not have a resolution"
                )
            consensus = proposal
        elif resolution is not None and resolution["decision"] == "accept_reviewer":
            consensus = review
        else:
            consensus = None

        retired_portugol_boundary = (
            status == "extraction_invalid"
            and language == "portugol"
            and comment_kind in {"block", "nested"}
            and syntax_label == "{...}"
        )
        if status in {"extraction_invalid", "ambiguous"}:
            if not retired_portugol_boundary and (
                consensus is None or consensus["disposition"] != status
            ):
                raise RegressionImportError(
                    f"{context}: status {status!r} does not match the converged oracle disposition"
                )
        elif status == "reviewer_disagreement":
            if consensus is not None:
                raise RegressionImportError(
                    f"{context}: reviewer_disagreement unexpectedly has consensus"
                )
        elif status == "cross_run_reviewer_conflict":
            if consensus is None or consensus["disposition"] != "clean":
                raise RegressionImportError(
                    f"{context}: cross_run_reviewer_conflict requires a clean within-run consensus"
                )
        elif status == "intra_corpus_oracle_conflict":
            if consensus is None or consensus["disposition"] != "clean":
                raise RegressionImportError(
                    f"{context}: intra_corpus_oracle_conflict requires a clean within-run consensus"
                )
        elif status == "cleaning_policy_dispute":
            if consensus is None or consensus["disposition"] != "clean":
                raise RegressionImportError(
                    f"{context}: cleaning_policy_dispute requires a clean within-run consensus"
                )
        elif consensus is None or consensus["disposition"] != "clean":
            raise RegressionImportError(
                f"{context}: validation exception {status!r} requires a clean consensus literal"
            )

        exceptions[case_id] = OracleException(
            case_id=case_id,
            language=language,
            comment_kind=comment_kind,
            syntax_label=syntax_label,
            raw_sha256=_require_sha256(row, "raw_sha256", context),
            status=status,
            extraction_boundary_invalid=boundary_invalid,
            detail=_require_string(row, "detail", context),
            reviewers=reviewers,
            payload=dict(row),
        )
    return exceptions


def _validate_case_partition(
    failures: Mapping[str, SourceFailure],
    annotations: Mapping[str, ReviewedOracle],
    exceptions: Mapping[str, OracleException],
) -> None:
    failure_ids = set(failures)
    annotation_ids = set(annotations)
    exception_ids = set(exceptions)
    overlap = annotation_ids & exception_ids
    union_ids = annotation_ids | exception_ids
    if not overlap and failure_ids == union_ids:
        _validate_intra_corpus_oracle_conflicts(
            failures,
            annotations,
            exceptions,
        )
        return
    missing = sorted(failure_ids - union_ids)
    extra = sorted(union_ids - failure_ids)
    raise RegressionImportError(
        "reviewed annotations and oracle exceptions do not partition failures; "
        f"missing={missing[:10]!r} ({len(missing)} total) "
        f"extra={extra[:10]!r} ({len(extra)} total) "
        f"overlap={sorted(overlap)[:10]!r} ({len(overlap)} total)"
    )


def _validate_intra_corpus_oracle_conflicts(
    failures: Mapping[str, SourceFailure],
    annotations: Mapping[str, ReviewedOracle],
    exceptions: Mapping[str, OracleException],
) -> None:
    agreed_groups: defaultdict[
        tuple[str, str],
        dict[str, str],
    ] = defaultdict(dict)
    actual_conflict_groups: defaultdict[
        tuple[str, str],
        set[str],
    ] = defaultdict(set)
    for case_id, failure in failures.items():
        key = (
            _canonical_conflict_language(failure.language),
            _sha256_text(failure.raw_comment),
        )
        annotation = annotations.get(case_id)
        if annotation is not None:
            agreed_groups[key][case_id] = annotation.expected_cleaned
            continue
        exception = exceptions[case_id]
        if exception.status == "intra_corpus_oracle_conflict":
            actual_conflict_groups[key].add(case_id)
        if exception.status == "extraction_invalid":
            continue
        consensus = _oracle_exception_consensus(exception)
        if consensus is not None and consensus["disposition"] == "clean":
            agreed_groups[key][case_id] = consensus["expected_cleaned"]

    expected_conflict_groups = {
        key: set(agreed_literals)
        for key, agreed_literals in agreed_groups.items()
        if len({_sha256_text(expected) for expected in agreed_literals.values()}) > 1
    }
    if dict(actual_conflict_groups) != expected_conflict_groups:
        all_keys = sorted(set(actual_conflict_groups) | set(expected_conflict_groups))
        for key in all_keys:
            actual_ids = actual_conflict_groups.get(key, set())
            expected_ids = expected_conflict_groups.get(key, set())
            if actual_ids == expected_ids:
                continue
            raise RegressionImportError(
                "intra_corpus_oracle_conflict must classify every clean-consensus "
                f"member of identical-raw group {key!r}; "
                f"expected={sorted(expected_ids)!r} "
                f"actual={sorted(actual_ids)!r}"
            )
        raise AssertionError("conflict-group comparison differed without a key mismatch")


def _canonical_conflict_language(language: str) -> str:
    """Return a stable equivalence key only for audited registry aliases."""

    return CONFLICT_LANGUAGE_ALIASES.get(language, language)


def _oracle_exception_consensus(
    exception: OracleException,
) -> Mapping[str, Any] | None:
    proposal = exception.payload["proposal"]
    review = exception.payload["review"]
    resolution = exception.payload["resolution"]
    if review["decision"] == "approve":
        return proposal
    if resolution is not None and resolution["decision"] == "accept_reviewer":
        return review
    return None


def _validate_source_summary(
    summary: Mapping[str, Any],
    failures: Mapping[str, SourceFailure],
    expected_source_manifest_sha256: str,
) -> dict[str, str]:
    context = "run summary"
    case_count = len(failures)
    if _require_integer(summary, "final_failures", context) != case_count:
        raise RegressionImportError(
            "run summary final_failures does not equal the loaded failure count"
        )
    manifest_sha256 = _require_sha256(summary, "manifest_sha256", context)
    if manifest_sha256 != expected_source_manifest_sha256:
        raise RegressionImportError(
            "run summary manifest_sha256 does not match --expected-source-manifest-sha256"
        )

    primary_model = _require_string(summary, "primary_model", context)
    secondary_model = _require_string(summary, "secondary_model", context)
    if {failure.primary_model for failure in failures.values()} != {primary_model}:
        raise RegressionImportError("failure primary models do not match the run summary")
    if {failure.secondary_model for failure in failures.values()} != {secondary_model}:
        raise RegressionImportError("failure secondary models do not match the run summary")
    return {
        "candidate_set_sha256": _require_sha256(summary, "candidate_set_sha256", context),
        "manifest_sha256": manifest_sha256,
        "primary_model": primary_model,
        "secondary_model": secondary_model,
    }


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


def _canonical_record(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )


def _build_common_case_payload(
    failure: SourceFailure,
    provenance: SourceProvenance,
    *,
    include_raw: bool,
) -> dict[str, Any]:
    raw_sha256 = _sha256_text(failure.raw_comment)
    payload = {
        "baseline_cleaned_sha256": _sha256_text(failure.candidate_cleaned_comment),
        "case_id": failure.case_id,
        "comment_kind": failure.comment_kind,
        "language": failure.language,
        "raw_sha256": raw_sha256,
        "raw_utf8_length": len(failure.raw_comment.encode("utf-8")),
        "source_provenance": {
            "source_excerpt_sha256": provenance.source_excerpt_sha256,
            "source_id": provenance.source_id,
        },
        "syntax_label": failure.syntax_label,
    }
    if include_raw:
        payload["raw_comment"] = failure.raw_comment
    return payload


def _build_case_payload(
    failure: SourceFailure,
    oracle: ReviewedOracle,
    provenance: SourceProvenance,
) -> dict[str, Any]:
    raw_sha256 = _sha256_text(failure.raw_comment)
    if oracle.raw_sha256 != raw_sha256:
        raise RegressionImportError(
            f"{failure.case_id}: reviewed raw_sha256 does not match the frozen failure"
        )
    if "\r" in oracle.expected_cleaned:
        raise RegressionImportError(
            f"{failure.case_id}: expected_cleaned must use LF newlines only"
        )
    if not _is_subsequence(
        oracle.expected_cleaned,
        _normalize_newlines(failure.raw_comment),
    ):
        raise RegressionImportError(
            f"{failure.case_id}: expected_cleaned is not a subsequence of the "
            "newline-normalized raw comment"
        )

    baseline_sha256 = _sha256_text(failure.candidate_cleaned_comment)
    expected_matches_baseline = (
        oracle.expected_cleaned_sha256 == baseline_sha256
        and oracle.expected_cleaned == failure.candidate_cleaned_comment
    )
    if oracle.disposition == "confirmed_bug" and expected_matches_baseline:
        raise RegressionImportError(
            f"{failure.case_id}: confirmed_bug oracle equals the failed baseline"
        )
    if oracle.disposition == "judge_false_positive" and not expected_matches_baseline:
        raise RegressionImportError(
            f"{failure.case_id}: judge_false_positive oracle must equal the baseline"
        )

    adjudicated_expected = ADJUDICATED_EXPECTED_OUTPUTS.get(failure.case_id)
    rendered_expected = (
        oracle.expected_cleaned if adjudicated_expected is None else adjudicated_expected
    )
    rendered_disposition = (
        oracle.disposition if adjudicated_expected is None else "adjudicated_override"
    )
    return {
        **_build_common_case_payload(
            failure,
            provenance,
            include_raw=True,
        ),
        "disposition": rendered_disposition,
        "expected_cleaned": rendered_expected,
        "expected_cleaned_sha256": _sha256_text(rendered_expected),
    }


def _validate_exception_matches_failure(
    failure: SourceFailure,
    exception: OracleException,
) -> None:
    mismatches = []
    for field_name in ("case_id", "language", "comment_kind", "syntax_label"):
        if getattr(exception, field_name) != getattr(failure, field_name):
            mismatches.append(field_name)
    if exception.raw_sha256 != _sha256_text(failure.raw_comment):
        mismatches.append("raw_sha256")
    if exception.status == "cross_run_reviewer_conflict":
        proposal = exception.payload["proposal"]
        review = exception.payload["review"]
        resolution = exception.payload["resolution"]
        consensus = (
            proposal
            if review["decision"] == "approve"
            else review
            if resolution is not None and resolution["decision"] == "accept_reviewer"
            else None
        )
        if (
            consensus is None
            or consensus["disposition"] != "clean"
            or consensus["expected_cleaned"] != failure.candidate_cleaned_comment
        ):
            mismatches.append("cross_run_consensus")
        if set(exception.reviewers) != {
            failure.primary_model,
            failure.secondary_model,
        }:
            mismatches.append("cross_run_reviewer_identities")
        if failure.primary_cleaning_correct or failure.secondary_cleaning_correct:
            mismatches.append("cross_run_frozen_verdicts")
    if exception.status == "cleaning_policy_dispute":
        decision = CLEANING_POLICY_DISPUTES.get(failure.case_id)
        if decision is None:
            mismatches.append("cleaning_policy_identity")
        else:
            language, comment_kind, syntax_label, raw_sha256, subkind = decision
            if (
                failure.language,
                failure.comment_kind,
                failure.syntax_label,
                _sha256_text(failure.raw_comment),
            ) != (language, comment_kind, syntax_label, raw_sha256):
                mismatches.append("cleaning_policy_identity")
            if not exception.detail.startswith(f"Policy subkind {subkind}:"):
                mismatches.append("cleaning_policy_subkind")
    if mismatches:
        raise RegressionImportError(
            f"{failure.case_id}: oracle exception differs from the frozen "
            f"failure in {', '.join(mismatches)}"
        )


def _reconstruct_boundary_assertion(
    failure: SourceFailure,
) -> dict[str, Any] | None:
    """Build a conservative executable assertion for a proven overcapture.

    Smalltalk comments are paired double-quoted regions.  When an invalid
    frozen match begins with a complete pair, its first closing quote proves
    the corrected boundary independently of physical line endings.

    Other reconstructable failures are lone-CR files accidentally swallowed by
    a regex that treated only LF as a line ending.  In that narrow case, the
    prefix before the first CR is a source span that a line-comment query must
    return without swallowing the terminator or following source.  LF-first
    and unsupported shapes remain accounting-only rather than guessing. M and
    MOO corpus rows are known language-classification errors, not evidence for
    changing those languages' valid comment syntax, so they stay
    accounting-only. Legacy Portugol brace spans are whole programs; the first
    real ``/* ... */`` or ``//`` comment inside each span proves both that the
    outer brace is source and where the current parser's first match belongs.
    """

    if failure.language in {"m", "moocode"}:
        return None

    if (
        failure.language == "portugol"
        and failure.comment_kind in {"block", "nested"}
        and failure.syntax_label == "{...}"
    ):
        candidates: list[tuple[int, str]] = []
        block_start = failure.raw_comment.find("/*")
        if block_start >= 0:
            block_end = failure.raw_comment.find("*/", block_start + 2)
            if block_end >= 0:
                candidates.append(
                    (
                        block_start,
                        failure.raw_comment[block_start : block_end + 2],
                    )
                )
        line_start = failure.raw_comment.find("//")
        if line_start >= 0:
            line_end_candidates = [
                end
                for end in (
                    failure.raw_comment.find("\r", line_start + 2),
                    failure.raw_comment.find("\n", line_start + 2),
                )
                if end >= 0
            ]
            line_end = min(line_end_candidates) if line_end_candidates else len(failure.raw_comment)
            candidates.append(
                (
                    line_start,
                    failure.raw_comment[line_start:line_end],
                )
            )
        if candidates:
            _, expected_match = min(candidates, key=lambda candidate: candidate[0])
            return {
                "expected_match": expected_match,
                "expected_match_sha256": _sha256_text(expected_match),
                "kind": "comment_query_first_embedded_match",
            }

    if failure.language == "smalltalk" and failure.raw_comment.startswith('"'):
        closing_quote = failure.raw_comment.find('"', 1)
        if closing_quote >= 1 and closing_quote + 1 < len(failure.raw_comment):
            expected_match = failure.raw_comment[: closing_quote + 1]
            return {
                "expected_match": expected_match,
                "expected_match_sha256": _sha256_text(expected_match),
                "kind": "comment_query_first_match",
            }

    if failure.comment_kind != "line":
        return None
    carriage_return = failure.raw_comment.find("\r")
    line_feed = failure.raw_comment.find("\n")
    if carriage_return < 0 or (line_feed >= 0 and line_feed < carriage_return):
        return None
    boundary_end = carriage_return
    if boundary_end <= 0:
        return None
    expected_match = failure.raw_comment[:boundary_end]
    return {
        "expected_match": expected_match,
        "expected_match_sha256": _sha256_text(expected_match),
        "kind": "line_query_first_match",
    }


def _build_minimal_boundary_probe(
    failure: SourceFailure,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Replace a source-sized overcapture with a small structural regression.

    The original raw hash and byte length remain in the case's common payload.
    The literal below exists only to exercise the already-reviewed boundary
    shape without redistributing the surrounding corpus file.
    """

    original_assertion = _reconstruct_boundary_assertion(failure)
    if original_assertion is None:
        return None

    query_kind = original_assertion["kind"]
    if query_kind == "line_query_first_match":
        expected_match = f"{failure.syntax_label} boundary"
        raw_comment = expected_match + "\rsource"
    elif query_kind == "comment_query_first_match":
        expected_match = '"boundary"'
        raw_comment = expected_match + "\rsource"
    else:
        assert query_kind == "comment_query_first_embedded_match"
        expected_match = "/* boundary */"
        raw_comment = "{\n/* boundary */\nsource\n}"

    probe = {
        "kind": "synthetic_structural_probe",
        "raw_comment": raw_comment,
        "raw_sha256": _sha256_text(raw_comment),
        "raw_utf8_length": len(raw_comment.encode("utf-8")),
    }
    assertion = {
        "expected_match": expected_match,
        "expected_match_sha256": _sha256_text(expected_match),
        "kind": query_kind,
    }
    return probe, assertion


def _build_exception_case_payload(
    failure: SourceFailure,
    exception: OracleException,
    provenance: SourceProvenance,
    *,
    extraction_boundary: bool,
) -> dict[str, Any]:
    _validate_exception_matches_failure(failure, exception)
    boundary_regression = _build_minimal_boundary_probe(failure) if extraction_boundary else None
    promoted_exception = failure.case_id in EXECUTABLE_EXCEPTION_REGRESSION_IDS
    include_raw = promoted_exception
    payload = {
        **_build_common_case_payload(
            failure,
            provenance,
            include_raw=include_raw,
        ),
        "disposition": (
            "executable_regression"
            if boundary_regression is not None or promoted_exception
            else "accounting_only"
        ),
        "exception_status": exception.status,
        "oracle_exception_record_sha256": _sha256_text(_canonical_record(exception.payload)),
    }
    if extraction_boundary:
        if boundary_regression is None:
            payload["boundary_assertion"] = None
        else:
            boundary_probe, boundary_assertion = boundary_regression
            payload["boundary_assertion"] = boundary_assertion
            payload["boundary_probe"] = boundary_probe
    if promoted_exception:
        proposal = exception.payload["proposal"]
        if proposal["disposition"] != "clean":
            raise RegressionImportError(
                f"{failure.case_id}: promoted exception proposal is not clean"
            )
        expected_cleaned = proposal["expected_cleaned"]
        payload["expected_cleaned"] = expected_cleaned
        payload["expected_cleaned_sha256"] = _sha256_text(expected_cleaned)
    return payload


def build_rendered_fixtures(
    failures: Mapping[str, SourceFailure],
    source_provenance: Mapping[str, SourceProvenance],
    annotations: Mapping[str, ReviewedOracle],
    exceptions: Mapping[str, OracleException],
    *,
    failures_sha256: str,
    run_summary_sha256: str,
    annotations_sha256: str,
    oracle_exceptions_sha256: str,
    source_summary: Mapping[str, str],
) -> dict[str, str]:
    """Return every deterministic output file as UTF-8 JSON text."""

    _validate_case_partition(failures, annotations, exceptions)
    missing_provenance = sorted(set(failures) - set(source_provenance))
    extra_provenance = sorted(set(source_provenance) - set(failures))
    if missing_provenance or extra_provenance:
        raise RegressionImportError(
            "source provenance does not exactly cover failures; "
            f"missing={missing_provenance!r} extra={extra_provenance!r}"
        )
    for case_id, provenance in source_provenance.items():
        if SOURCE_ID_PATTERN.fullmatch(provenance.source_id) is None:
            raise RegressionImportError(f"{case_id}: source provenance has an invalid source_id")
        if SHA256_PATTERN.fullmatch(provenance.source_excerpt_sha256) is None:
            raise RegressionImportError(
                f"{case_id}: source provenance has an invalid source_excerpt_sha256"
            )
    grouped: defaultdict[
        str,
        dict[str, list[dict[str, Any]]],
    ] = defaultdict(lambda: {category: [] for category in CASE_CATEGORIES})
    cleaning_contracts = {failure.cleaning_contract for failure in failures.values()}
    if len(cleaning_contracts) != 1:
        raise RegressionImportError("failures do not share exactly one cleaning contract")

    for case_id in sorted(failures):
        failure = failures[case_id]
        if case_id in annotations:
            grouped[failure.family_name][SANITIZER_CATEGORY].append(
                _build_case_payload(
                    failure,
                    annotations[case_id],
                    source_provenance[case_id],
                )
            )
            continue
        exception = exceptions[case_id]
        if exception.extraction_boundary_invalid:
            category = EXTRACTOR_BOUNDARY_CATEGORY
        else:
            category = ORACLE_EXCEPTION_CATEGORY
        grouped[failure.family_name][category].append(
            _build_exception_case_payload(
                failure,
                exception,
                source_provenance[case_id],
                extraction_boundary=(category == EXTRACTOR_BOUNDARY_CATEGORY),
            )
        )

    rendered: dict[str, str] = {}
    shard_descriptors: list[dict[str, Any]] = []
    disposition_counts: Counter[str] = Counter()
    exception_status_counts: Counter[str] = Counter()
    case_category_counts: Counter[str] = Counter()
    comment_kind_counts: Counter[str] = Counter()
    case_ids_by_category: defaultdict[str, list[str]] = defaultdict(list)
    for family_name in sorted(grouped):
        filename = f"{family_name}.json"
        cases_by_category = {
            category: sorted(
                grouped[family_name][category],
                key=lambda case: (case["language"], case["case_id"]),
            )
            for category in CASE_CATEGORIES
        }
        payload = {
            "extractor_boundary_cases": cases_by_category[EXTRACTOR_BOUNDARY_CATEGORY],
            "family_name": family_name,
            "oracle_exception_cases": cases_by_category[ORACLE_EXCEPTION_CATEGORY],
            "sanitizer_cases": cases_by_category[SANITIZER_CATEGORY],
            "schema_version": SCHEMA_VERSION,
        }
        text = _canonical_json(payload)
        rendered[filename] = text
        sanitizer_cases = cases_by_category[SANITIZER_CATEGORY]
        extractor_cases = cases_by_category[EXTRACTOR_BOUNDARY_CATEGORY]
        oracle_exception_cases = cases_by_category[ORACLE_EXCEPTION_CATEGORY]
        disposition_counts.update(case["disposition"] for case in sanitizer_cases)
        exception_status_counts.update(
            case["exception_status"] for case in extractor_cases + oracle_exception_cases
        )
        for category, cases in cases_by_category.items():
            case_category_counts[category] += len(cases)
            case_ids_by_category[category].extend(case["case_id"] for case in cases)
            comment_kind_counts.update(case["comment_kind"] for case in cases)
        shard_case_count = sum(len(cases) for cases in cases_by_category.values())
        shard_descriptors.append(
            {
                "case_count": shard_case_count,
                "extractor_boundary_case_count": len(extractor_cases),
                "family_name": family_name,
                "filename": filename,
                "oracle_exception_case_count": len(oracle_exception_cases),
                "sanitizer_case_count": len(sanitizer_cases),
                "sha256": _sha256_text(text),
            }
        )

    normalized_category_counts = {
        category: case_category_counts[category] for category in CASE_CATEGORIES
    }
    category_id_set_sha256 = {
        category: _case_id_set_sha256(case_ids_by_category[category])
        for category in CASE_CATEGORIES
    }
    manifest = {
        "case_count": len(failures),
        "case_category_counts": normalized_category_counts,
        "case_category_id_set_sha256": category_id_set_sha256,
        "case_id_set_sha256": _case_id_set_sha256(failures),
        "comment_kind_counts": dict(sorted(comment_kind_counts.items())),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "exception_status_counts": dict(sorted(exception_status_counts.items())),
        "schema_version": SCHEMA_VERSION,
        "shards": shard_descriptors,
        "source": {
            "annotations_sha256": annotations_sha256,
            "candidate_set_sha256": source_summary["candidate_set_sha256"],
            "dataset": "bigcode/the-stack-v2-dedup",
            "failures_sha256": failures_sha256,
            "manifest_sha256": source_summary["manifest_sha256"],
            "oracle_exceptions_sha256": oracle_exceptions_sha256,
            "primary_model": source_summary["primary_model"],
            "run_summary_sha256": run_summary_sha256,
            "secondary_model": source_summary["secondary_model"],
        },
    }
    rendered["_manifest.json"] = _canonical_json(manifest)
    rendered[NOTICE_NAME] = NOTICE_TEXT
    rendered[SENTINEL_NAME] = SENTINEL_CONTENT
    return rendered


def _atomic_write_text(path: Path, text: str) -> None:
    encoded = text.encode("utf-8")
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temporary_path = Path(handle.name)
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(temporary_path, path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def _safe_force_target(output_dir: Path) -> None:
    if output_dir.is_symlink():
        raise RegressionImportError(f"refusing symlinked destructive --force target: {output_dir}")
    if not output_dir.exists():
        return
    if not output_dir.is_dir():
        raise RegressionImportError(
            f"refusing non-directory destructive --force target: {output_dir}"
        )
    if output_dir.resolve() == EXPECTED_OUTPUT_DIR:
        return

    sentinel = output_dir / SENTINEL_NAME
    if (
        sentinel.is_symlink()
        or not sentinel.is_file()
        or sentinel.read_bytes() != SENTINEL_CONTENT.encode("utf-8")
    ):
        raise RegressionImportError(
            f"refusing destructive --force target without importer sentinel: {output_dir}"
        )


def _write_or_check(
    output_dir: Path,
    rendered: Mapping[str, str],
    *,
    check: bool,
    force: bool,
) -> None:
    expected_names = set(rendered)
    actual_names = (
        {path.name for path in output_dir.glob("*.json")} if output_dir.is_dir() else set()
    )
    if output_dir.is_dir():
        actual_names.update(
            filename
            for filename in (NOTICE_NAME, SENTINEL_NAME)
            if (output_dir / filename).exists()
        )

    if check:
        if actual_names != expected_names:
            raise RegressionImportError(
                f"{output_dir}: fixture file set differs; "
                f"missing={sorted(expected_names - actual_names)!r} "
                f"extra={sorted(actual_names - expected_names)!r}"
            )
        for filename in sorted(expected_names):
            path = output_dir / filename
            try:
                actual = path.read_bytes().decode("utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise RegressionImportError(f"cannot read fixture {path}: {exc}") from exc
            if actual != rendered[filename]:
                raise RegressionImportError(f"{path}: content differs from deterministic import")
        return

    if force:
        _safe_force_target(output_dir)

    conflicting = []
    for filename in sorted(expected_names & actual_names):
        path = output_dir / filename
        try:
            actual = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise RegressionImportError(f"cannot read fixture {path}: {exc}") from exc
        if actual != rendered[filename]:
            conflicting.append(filename)
    stale = sorted(actual_names - expected_names)
    if (conflicting or stale) and not force:
        raise RegressionImportError(
            f"{output_dir}: refusing to replace existing fixtures without --force; "
            f"differing={conflicting!r} stale={stale!r}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    for filename in sorted(expected_names - {"_manifest.json"}):
        path = output_dir / filename
        if not path.exists() or path.read_bytes().decode("utf-8") != rendered[filename]:
            _atomic_write_text(path, rendered[filename])
    if force:
        for filename in stale:
            (output_dir / filename).unlink()
    _atomic_write_text(output_dir / "_manifest.json", rendered["_manifest.json"])


def _validate_expected_source_options(args: argparse.Namespace) -> None:
    for option_name in (
        "expected_failures_sha256",
        "expected_run_summary_sha256",
        "expected_source_manifest_sha256",
        "expected_case_id_set_sha256",
    ):
        value = getattr(args, option_name)
        if SHA256_PATTERN.fullmatch(value) is None:
            raise RegressionImportError(
                f"--{option_name.replace('_', '-')} must be a lowercase hexadecimal SHA-256"
            )
    if args.expected_case_count < 1:
        raise RegressionImportError("--expected-case-count must be positive")


def run(args: argparse.Namespace) -> None:
    """Validate all inputs, render fixtures, and perform the selected output mode."""

    _validate_expected_source_options(args)
    failures_sha256 = _sha256_file(args.failures)
    if failures_sha256 != args.expected_failures_sha256:
        raise RegressionImportError(
            f"{args.failures}: SHA-256 {failures_sha256} does not match --expected-failures-sha256"
        )
    run_summary_sha256 = _sha256_file(args.run_summary)
    if run_summary_sha256 != args.expected_run_summary_sha256:
        raise RegressionImportError(
            f"{args.run_summary}: SHA-256 {run_summary_sha256} does not match "
            "--expected-run-summary-sha256"
        )

    language_families = _load_language_families(args.family_fixture_dir)
    failures = _load_source_failures(args.failures, language_families)
    if len(failures) != args.expected_case_count:
        raise RegressionImportError(
            f"failure count {len(failures)} does not match --expected-case-count "
            f"{args.expected_case_count}"
        )
    case_id_set_sha256 = _case_id_set_sha256(failures)
    if case_id_set_sha256 != args.expected_case_id_set_sha256:
        raise RegressionImportError(
            f"case-ID set SHA-256 {case_id_set_sha256} does not match --expected-case-id-set-sha256"
        )

    source_provenance, source_manifest_sha256 = _load_source_provenance(
        args.source_manifest,
        failures,
    )
    if source_manifest_sha256 != args.expected_source_manifest_sha256:
        raise RegressionImportError(
            f"{args.source_manifest}: SHA-256 {source_manifest_sha256} does not match "
            "--expected-source-manifest-sha256"
        )

    annotations_sha256 = _sha256_file(args.annotations)
    oracle_exceptions_sha256 = _sha256_file(args.oracle_exceptions)
    annotations = _load_reviewed_oracles(args.annotations)
    exceptions = _load_oracle_exceptions(args.oracle_exceptions)
    _validate_case_partition(failures, annotations, exceptions)
    summary = _load_json_file(args.run_summary)
    source_summary = _validate_source_summary(
        summary,
        failures,
        args.expected_source_manifest_sha256,
    )
    rendered = build_rendered_fixtures(
        failures,
        source_provenance,
        annotations,
        exceptions,
        failures_sha256=failures_sha256,
        run_summary_sha256=run_summary_sha256,
        annotations_sha256=annotations_sha256,
        oracle_exceptions_sha256=oracle_exceptions_sha256,
        source_summary=source_summary,
    )
    _write_or_check(
        args.output_dir,
        rendered,
        check=args.check,
        force=args.force,
    )
    action = "verified" if args.check else "wrote"
    extractor_count = sum(
        exception.extraction_boundary_invalid for exception in exceptions.values()
    )
    other_exception_count = len(exceptions) - extractor_count
    print(
        f"{action} {len(failures)} reviewed regressions "
        f"({len(annotations)} sanitizer, {extractor_count} extractor boundary, "
        f"{other_exception_count} oracle exception) in "
        f"{sum(name.endswith('.json') and name != '_manifest.json' for name in rendered)} "
        f"family shards at {args.output_dir}"
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        run(args)
    except RegressionImportError as exc:
        print(f"comment-cleaning regression import failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
