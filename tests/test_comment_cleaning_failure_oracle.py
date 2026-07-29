"""Tests for the independent exact-output cleaning-failure oracle runner."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import threading
import time
from collections import Counter
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest


def _load_runner():
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "run_comment_cleaning_failure_oracle.py"
    )
    spec = importlib.util.spec_from_file_location(
        "run_comment_cleaning_failure_oracle",
        script_path,
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = _load_runner()


def _load_importer():
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "import_comment_cleaning_regressions.py"
    )
    spec = importlib.util.spec_from_file_location(
        "import_comment_cleaning_regressions_for_oracle_test",
        script_path,
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


IMPORTER = _load_importer()


def _failure_row(
    case_id: str,
    *,
    language: str = "python",
    comment_kind: str = "line",
    syntax_label: str = "#",
    raw_comment: str = "# raw",
    candidate: str = "REJECTED CANDIDATE MUST NEVER APPEAR",
    primary_model: str = "frozen-primary-reviewer",
    secondary_model: str = "frozen-secondary-reviewer",
) -> dict:
    return {
        "case": {
            "case_id": case_id,
            "language": language,
            "comment_kind": comment_kind,
            "syntax_label": syntax_label,
            "repo": "owner/repo",
            "path": f"src/{case_id}.py",
        },
        "raw_comment": raw_comment,
        "candidate_cleaned_comment": candidate,
        "cleaning_contract": (
            "Remove only comment syntax scaffolding and preserve content exactly."
        ),
        "primary": {
            "cleaning_correct": False,
            "model": primary_model,
            "rationale": "Primary says remove the marker.",
            "verdict": "fail",
        },
        "secondary": {
            "cleaning_correct": False,
            "model": secondary_model,
            "rationale": "Secondary says preserve the body.",
            "verdict": "fail",
        },
    }


def _write_failures(path: Path, rows: list[dict]) -> None:
    path.write_bytes(
        b"".join(json.dumps(row, ensure_ascii=True).encode("ascii") + b"\n" for row in rows)
    )


def _config(
    tmp_path: Path,
    failures: Path,
    *,
    batch_size: int = 4,
    max_prompt_chars: int = 250_000,
    workers: int = 2,
) -> object:
    return RUNNER.OracleConfig(
        failures=failures,
        output_root=tmp_path / "oracle-output",
        codex_bin="codex",
        codex_cwd=tmp_path,
        batch_size=batch_size,
        max_prompt_chars=max_prompt_chars,
        workers=workers,
        timeout=30,
        command_retries=1,
        malformed_single_retries=1,
        retry_delay_seconds=0,
    )


def _clean_payload(cases) -> dict:
    return {
        "oracles": [
            {
                "case_id": case.case_id,
                "expected_cleaned": f"cleaned:{case.case_id}",
                "disposition": "clean",
                "rationale": "Unique exact cleaning.",
                "confidence": 0.9,
            }
            for case in cases
        ]
    }


def _proposal_payload(cases, expected: dict[str, str]) -> dict:
    return {
        "oracles": [
            {
                "case_id": case.case_id,
                "expected_cleaned": expected[case.case_id],
                "disposition": "clean",
                "rationale": "Unique exact cleaning.",
                "confidence": 0.9,
            }
            for case in reversed(cases)
        ]
    }


def _approval_payload(cases, proposals) -> dict:
    return {
        "reviews": [
            {
                "case_id": case.case_id,
                "decision": "approve",
                "expected_cleaned": proposals[case.case_id]["expected_cleaned"],
                "disposition": proposals[case.case_id]["disposition"],
                "rationale": "Independently derived and exact.",
                "confidence": 0.91,
            }
            for case in reversed(cases)
        ]
    }


def test_prompt_uses_full_oracle_inputs_but_never_rejected_candidate(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    raw = "# Καλημέρα\x00\tline\r\nnext 😀"
    rejected = "SECRET REJECTED OUTPUT"
    _write_failures(
        failures,
        [_failure_row("unicode-control", raw_comment=raw, candidate=rejected)],
    )

    case = RUNNER.load_failures(failures).cases[0]
    prompt_case = RUNNER._prompt_case(case)
    prompt = RUNNER.build_oracle_prompt([case])

    assert prompt_case["raw_comment"] == raw
    assert "primary_rationale" not in prompt_case
    assert "secondary_rationale" not in prompt_case
    assert "Primary says remove the marker." not in prompt
    assert "Secondary says preserve the body." not in prompt
    assert case.primary_model not in prompt
    assert case.secondary_model not in prompt
    assert "cleaning_correct" not in prompt
    assert rejected not in prompt
    assert case.baseline_cleaned_comment == rejected
    assert "baseline_cleaned_comment" not in prompt_case
    assert "\\u0000" in prompt
    assert "\\ud83d\\ude00" in prompt
    assert json.loads(json.dumps(prompt_case))["raw_comment"] == raw

    proposal = {
        "disposition": "clean",
        "expected_cleaned": "Καλημέρα\x00\tline\nnext 😀",
        "rationale": "Exact.",
        "confidence": 0.9,
    }
    review_prompt = RUNNER.build_review_prompt(
        [case],
        {case.case_id: proposal},
    )
    assert rejected not in review_prompt
    assert "Primary says remove the marker." in review_prompt
    assert "Secondary says preserve the body." in review_prompt
    escaped_expected = json.dumps(proposal["expected_cleaned"], ensure_ascii=True)
    assert escaped_expected in review_prompt

    review = {
        "decision": "replace",
        "disposition": "clean",
        "expected_cleaned": "replacement",
        "rationale": "Different.",
        "confidence": 0.8,
    }
    resolution_prompt = RUNNER.build_resolution_prompt(
        [case],
        {case.case_id: proposal},
        {case.case_id: review},
    )
    assert rejected not in resolution_prompt
    assert "Primary says remove the marker." in resolution_prompt
    assert "Secondary says preserve the body." in resolution_prompt


def test_batching_preserves_full_oversized_single_case(tmp_path: Path) -> None:
    failures = tmp_path / "failures.jsonl"
    huge_raw = "#" + ("α\n\x00" * 10_000) + "END"
    _write_failures(
        failures,
        [
            _failure_row("huge", raw_comment=huge_raw),
            _failure_row("small"),
        ],
    )
    config = _config(tmp_path, failures, max_prompt_chars=1_000)
    cases = RUNNER.load_failures(failures).cases

    batches = RUNNER.build_batches(cases, config)

    assert [tuple(case.case_id for case in batch) for batch in batches] == [
        ("huge",),
        ("small",),
    ]
    huge_prompt = RUNNER.build_oracle_prompt(batches[0])
    assert len(huge_prompt) > config.max_prompt_chars
    assert huge_raw == RUNNER._prompt_case(batches[0][0])["raw_comment"]
    assert '"truncated"' not in huge_prompt
    assert "END" in huge_prompt


@pytest.mark.parametrize(
    "oracle,error",
    [
        (
            {
                "case_id": "case-1",
                "expected_cleaned": "guess",
                "disposition": "ambiguous",
                "rationale": "Not unique.",
                "confidence": 0.4,
            },
            "must be empty",
        ),
        (
            {
                "case_id": "case-1",
                "expected_cleaned": "ok",
                "disposition": "clean",
                "rationale": "Exact.",
                "confidence": True,
            },
            "confidence",
        ),
        (
            {
                "case_id": "case-1",
                "expected_cleaned": "ok",
                "disposition": "unknown",
                "rationale": "Exact.",
                "confidence": 0.8,
            },
            "disposition",
        ),
    ],
)
def test_response_validation_enforces_disposition_contract(
    tmp_path: Path,
    oracle: dict,
    error: str,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(failures, [_failure_row("case-1")])
    cases = RUNNER.load_failures(failures).cases

    with pytest.raises(RUNNER.InvalidOracleOutput, match=error):
        RUNNER.validate_batch_response({"oracles": [oracle]}, cases)


@pytest.mark.parametrize(
    ("decision", "literal", "error"),
    [
        ("approve", "different", "does not exactly copy"),
        ("replace", "raw", "must differ"),
    ],
)
def test_review_validation_requires_semantically_exact_decisions(
    tmp_path: Path,
    decision: str,
    literal: str,
    error: str,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(failures, [_failure_row("case-1")])
    cases = RUNNER.load_failures(failures).cases
    proposal = {
        "disposition": "clean",
        "expected_cleaned": "raw",
        "rationale": "Exact.",
        "confidence": 0.9,
    }
    payload = {
        "reviews": [
            {
                "case_id": "case-1",
                "decision": decision,
                "expected_cleaned": literal,
                "disposition": "clean",
                "rationale": "Reviewed.",
                "confidence": 0.8,
            }
        ]
    }

    with pytest.raises(RUNNER.InvalidOracleOutput, match=error):
        RUNNER.validate_review_response(
            payload,
            cases,
            {"case-1": proposal},
        )


def test_response_validation_rejects_unhashable_case_id_and_surrogate(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(failures, [_failure_row("case-1")])
    cases = RUNNER.load_failures(failures).cases
    malformed = {
        "case_id": [],
        "expected_cleaned": "\ud800",
        "disposition": "clean",
        "rationale": "Invalid.",
        "confidence": 0.8,
    }

    with pytest.raises(RUNNER.InvalidOracleOutput, match="unexpected case_id"):
        RUNNER.validate_batch_response({"oracles": [malformed]}, cases)
    malformed["case_id"] = "case-1"
    with pytest.raises(RUNNER.InvalidOracleOutput, match="valid UTF-8"):
        RUNNER.validate_batch_response({"oracles": [malformed]}, cases)


def test_malformed_batch_splits_and_single_command_failure_retries(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(
        failures,
        [_failure_row("case-1"), _failure_row("case-2")],
    )
    cases = RUNNER.load_failures(failures).cases
    config = _config(tmp_path, failures)
    calls: list[tuple[str, ...]] = []
    failed_once = False

    def invoke(batch, runner_config):
        nonlocal failed_once
        assert runner_config == config
        calls.append(tuple(case.case_id for case in batch))
        if len(batch) > 1:
            return {"oracles": []}
        if batch[0].case_id == "case-1" and not failed_once:
            failed_once = True
            raise RUNNER.OracleCommandError("transient")
        return _clean_payload(batch)

    rows = RUNNER._generate_batch_resilient(
        cases,
        config=config,
        invoke=invoke,
    )

    assert calls == [
        ("case-1", "case-2"),
        ("case-1",),
        ("case-1",),
        ("case-2",),
    ]
    assert [row["case_id"] for row in rows] == ["case-1", "case-2"]


def test_review_and_resolution_batches_split_and_retry_independently(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(
        failures,
        [
            _failure_row("case-1", raw_comment="# one"),
            _failure_row("case-2", raw_comment="# two"),
        ],
    )
    cases = RUNNER.load_failures(failures).cases
    config = _config(tmp_path, failures)
    proposals = {
        row["case_id"]: row
        for row in RUNNER._generate_batch_resilient(
            cases,
            config=config,
            invoke=lambda batch, _: _proposal_payload(
                batch,
                {"case-1": "one", "case-2": "two"},
            ),
        )
    }
    review_calls: list[tuple[str, ...]] = []
    review_failed_once = False

    def review_invoke(batch, proposal_rows, runner_config):
        nonlocal review_failed_once
        review_calls.append(tuple(case.case_id for case in batch))
        if len(batch) > 1:
            return {"reviews": []}
        if batch[0].case_id == "case-1" and not review_failed_once:
            review_failed_once = True
            raise RUNNER.OracleCommandError("transient Luna failure")
        return {
            "reviews": [
                {
                    "case_id": batch[0].case_id,
                    "decision": "replace",
                    "disposition": "clean",
                    "expected_cleaned": "",
                    "rationale": "Empty is the exact replacement.",
                    "confidence": 0.8,
                }
            ]
        }

    review_rows = RUNNER._generate_review_batch_resilient(
        cases,
        proposals=proposals,
        config=config,
        invoke=review_invoke,
    )
    assert review_calls == [
        ("case-1", "case-2"),
        ("case-1",),
        ("case-1",),
        ("case-2",),
    ]
    reviews = {row["case_id"]: row for row in review_rows}
    resolution_calls: list[tuple[str, ...]] = []

    def resolution_invoke(batch, proposal_rows, review_results, runner_config):
        resolution_calls.append(tuple(case.case_id for case in batch))
        if len(batch) > 1:
            return {"resolutions": []}
        return {
            "resolutions": [
                {
                    "case_id": batch[0].case_id,
                    "decision": "accept_reviewer",
                    "rationale": "Replacement accepted exactly.",
                    "confidence": 0.85,
                }
            ]
        }

    resolution_rows = RUNNER._generate_resolution_batch_resilient(
        cases,
        proposals=proposals,
        reviews=reviews,
        config=config,
        invoke=resolution_invoke,
    )
    assert resolution_calls == [
        ("case-1", "case-2"),
        ("case-1",),
        ("case-2",),
    ]
    assert [row["case_id"] for row in resolution_rows] == ["case-1", "case-2"]


def test_pipeline_writes_exact_strings_in_input_order_and_resumes(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(
        failures,
        [
            _failure_row("first", raw_comment="# α", candidate="α"),
            _failure_row("second", raw_comment="# \x00\r\n\t😀"),
            _failure_row("third", raw_comment="# decorative"),
        ],
    )
    config = _config(tmp_path, failures, batch_size=2, workers=2)
    expected = {
        "first": "α",
        "second": "\x00\n\t😀",
        "third": "",
    }
    proposal_calls: list[tuple[str, ...]] = []
    review_calls: list[tuple[str, ...]] = []
    resolution_calls: list[tuple[str, ...]] = []

    def propose(cases, runner_config):
        assert runner_config == config
        proposal_calls.append(tuple(case.case_id for case in cases))
        return _proposal_payload(cases, expected)

    def review(cases, proposals, runner_config):
        assert runner_config == config
        review_calls.append(tuple(case.case_id for case in cases))
        return _approval_payload(cases, proposals)

    def resolve(cases, proposals, reviews, runner_config):
        resolution_calls.append(tuple(case.case_id for case in cases))
        raise AssertionError("approval-only run must not invoke resolution")

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=propose,
            review_invoke=review,
            resolution_invoke=resolve,
        )
        == 0
    )
    assert proposal_calls == [("first", "second"), ("third",)]
    assert review_calls == [("first", "second"), ("third",)]
    assert resolution_calls == []
    rows = [
        json.loads(line)
        for line in (config.output_root / "reviewed_annotations.jsonl").read_bytes().splitlines()
    ]
    assert [row["case_id"] for row in rows] == ["first", "second", "third"]
    assert [row["expected_cleaned"] for row in rows] == [
        expected["first"],
        expected["second"],
        expected["third"],
    ]
    assert [row["disposition"] for row in rows] == [
        "judge_false_positive",
        "confirmed_bug",
        "confirmed_bug",
    ]
    assert all(
        set(row)
        == {
            "case_id",
            "raw_sha256",
            "expected_cleaned",
            "expected_cleaned_sha256",
            "disposition",
            "oracle",
        }
        for row in rows
    )
    assert all(
        set(row["oracle"]) == {"method", "note", "review_status", "reviewers"} for row in rows
    )
    assert all(
        row["expected_cleaned_sha256"] == RUNNER._sha256_text(row["expected_cleaned"])
        for row in rows
    )
    assert all(
        row["oracle"]["reviewers"] == ["gpt-5.6-luna", "gpt-5.6-sol"]
        and row["oracle"]["review_status"] == "approved"
        for row in rows
    )
    assert (config.output_root / "oracle_exceptions.jsonl").read_bytes() == b""
    metadata = json.loads((config.output_root / "run_metadata.json").read_bytes())
    assert metadata["proposal_model"] == "gpt-5.6-sol"
    assert metadata["review_model"] == "gpt-5.6-luna"
    assert metadata["minimum_distinct_reviewers"] == 2
    assert metadata["rejected_candidate_in_prompt"] is False
    assert metadata["prior_judge_evidence_in_proposal_prompt"] is False
    assert metadata["full_input_strings"] is True
    summary = json.loads((config.output_root / "run_summary.json").read_bytes())
    assert summary["import_ready"] is True
    assert summary["annotation_count"] == 3
    assert summary["exception_count"] == 0
    derived_paths = [
        config.output_root / "reviewed_annotations.jsonl",
        config.output_root / "oracle_exceptions.jsonl",
        config.output_root / "run_summary.json",
    ]
    before_resume = {path: path.read_bytes() for path in derived_paths}

    def unexpected(*args, **kwargs):
        raise AssertionError(f"resume called model with args={args!r}, kwargs={kwargs!r}")

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=unexpected,
            review_invoke=unexpected,
            resolution_invoke=unexpected,
        )
        == 0
    )
    assert {path: path.read_bytes() for path in derived_paths} == before_resume
    with pytest.raises(RUNNER.ResumeError, match="batch_size"):
        RUNNER.run_pipeline(
            replace(config, batch_size=1),
            proposal_invoke=unexpected,
            review_invoke=unexpected,
            resolution_invoke=unexpected,
        )


def test_same_reviewers_cannot_reverse_frozen_failure_into_executable_false_positive(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(
        failures,
        [
            _failure_row(
                "same-reviewers",
                raw_comment="# body",
                candidate="body",
                primary_model=RUNNER.REVIEW_MODEL,
                secondary_model=RUNNER.ORACLE_MODEL,
            ),
            _failure_row(
                "independent-reviewers",
                raw_comment="# other",
                candidate="other",
            ),
        ],
    )
    config = _config(tmp_path, failures, batch_size=2, workers=1)
    expected = {
        "same-reviewers": "body",
        "independent-reviewers": "other",
    }

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=lambda cases, _: _proposal_payload(cases, expected),
            review_invoke=lambda cases, proposals, _: _approval_payload(
                cases,
                proposals,
            ),
            resolution_invoke=lambda *_: pytest.fail("approval-only run must not resolve"),
        )
        == 1
    )
    annotations_path = config.output_root / "reviewed_annotations.jsonl"
    exceptions_path = config.output_root / "oracle_exceptions.jsonl"
    annotations = [json.loads(line) for line in annotations_path.read_bytes().splitlines()]
    exceptions = [json.loads(line) for line in exceptions_path.read_bytes().splitlines()]
    assert [row["case_id"] for row in annotations] == ["independent-reviewers"]
    assert annotations[0]["disposition"] == "judge_false_positive"
    assert [row["case_id"] for row in exceptions] == ["same-reviewers"]
    assert exceptions[0]["status"] == "cross_run_reviewer_conflict"
    assert exceptions[0]["proposal"]["expected_cleaned"] == "body"
    assert exceptions[0]["review"]["decision"] == "approve"
    assert exceptions[0]["resolution"] is None

    loaded_annotations = IMPORTER._load_reviewed_oracles(annotations_path)
    loaded_exceptions = IMPORTER._load_oracle_exceptions(exceptions_path)
    IMPORTER._validate_case_partition(
        {
            "same-reviewers": SimpleNamespace(
                language="python",
                raw_comment="# body",
            ),
            "independent-reviewers": SimpleNamespace(
                language="python",
                raw_comment="# other",
            ),
        },
        loaded_annotations,
        loaded_exceptions,
    )
    IMPORTER._validate_exception_matches_failure(
        IMPORTER.SourceFailure(
            case_id="same-reviewers",
            language="python",
            family_name="hash_style",
            comment_kind="line",
            syntax_label="#",
            repo="owner/repo",
            path="src/same-reviewers.py",
            raw_comment="# body",
            candidate_cleaned_comment="body",
            cleaning_contract=(
                "Remove only comment syntax scaffolding and preserve content exactly."
            ),
            judge_input_sha256="0" * 64,
            judge_rationale="Both frozen reviewers rejected the baseline.",
            primary_model=RUNNER.REVIEW_MODEL,
            secondary_model=RUNNER.ORACLE_MODEL,
            primary_cleaning_correct=False,
            secondary_cleaning_correct=False,
        ),
        loaded_exceptions["same-reviewers"],
    )

    before_resume = {
        path: path.read_bytes()
        for path in (
            annotations_path,
            exceptions_path,
            config.output_root / "run_summary.json",
        )
    }

    def unexpected(*args, **kwargs):
        raise AssertionError(f"finalization-only resume called a model: {args!r}")

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=unexpected,
            review_invoke=unexpected,
            resolution_invoke=unexpected,
        )
        == 1
    )
    assert {path: path.read_bytes() for path in before_resume} == before_resume


def test_cleaning_policy_disputes_are_exact_identity_pinned_accounting_cases(
    tmp_path: Path,
) -> None:
    expected_ids = {
        "abap_cds-line-bced7abdf245bf3d",
        "abap_cds-line-be44644a06c6d23a",
        "click-block-1d9ab161b43f027d",
        "literate_haskell-nested-762fdebeedc338fb",
        "metal-block-f81afe598c049d75",
        "moocode-block-0d312c0deb49121a",
        "powerbuilder-nested-2fee93e4074c3191",
        "powerbuilder-nested-df42c6b65e91a169",
        "propeller_spin-block-189589f644925d3d",
        "win32_message_file-directive-29b9fc01dd8a2fec",
        "win32_message_file-directive-34d12e114699e434",
        "win32_message_file-directive-48b4e07259b92b78",
        "win32_message_file-directive-4979b3181a921780",
        "win32_message_file-directive-4fa02c036ebaf3ec",
        "win32_message_file-directive-52dacc5b1b50ff39",
        "win32_message_file-directive-5833ef003c797086",
        "win32_message_file-directive-5b91f9c4b962d7a6",
        "win32_message_file-directive-745134bc5dfcb6a1",
        "win32_message_file-directive-a2adfa284a1c6595",
        "win32_message_file-directive-ac6c29e0ea184679",
        "win32_message_file-directive-b3cc78d98d8ff041",
        "win32_message_file-directive-c51c344493dcf2e8",
        "win32_message_file-directive-d924d32d0b7c5058",
        "x_bit_map-block-7aab0cb7d5f2e143",
        "x_bit_map-block-86708f0043fbb654",
        "x_bit_map-block-9d0db1b03af112a0",
        "x_bitmap-block-63519f13afd78a86",
        "x_bitmap-block-76553f7a089df85f",
        "x_bitmap-block-d40eae17460a16a0",
    }
    assert set(RUNNER.CLEANING_POLICY_DISPUTES) == expected_ids
    assert IMPORTER.CLEANING_POLICY_DISPUTES == {
        case_id: decision[:5] for case_id, decision in RUNNER.CLEANING_POLICY_DISPUTES.items()
    }
    assert Counter(decision[4] for decision in RUNNER.CLEANING_POLICY_DISPUTES.values()) == {
        "content_or_syntax": 8,
        "normalization": 21,
    }

    raw = "///EY1/SAV_I_PR_G2S_YB_LCGC\r"
    failures = tmp_path / "failures.jsonl"
    _write_failures(
        failures,
        [
            _failure_row(
                "abap_cds-line-bced7abdf245bf3d",
                language="abap_cds",
                syntax_label="//",
                raw_comment=raw,
                candidate="/EY1/SAV_I_PR_G2S_YB_LCGC",
            )
        ],
    )
    config = _config(tmp_path, failures, workers=1)
    expected = {
        "abap_cds-line-bced7abdf245bf3d": "/EY1/SAV_I_PR_G2S_YB_LCGC\n",
    }

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=lambda cases, _: _proposal_payload(cases, expected),
            review_invoke=lambda cases, proposals, _: _approval_payload(cases, proposals),
            resolution_invoke=lambda *_: pytest.fail("approval-only run must not resolve"),
        )
        == 1
    )
    assert (config.output_root / "reviewed_annotations.jsonl").read_bytes() == b""
    exceptions_path = config.output_root / "oracle_exceptions.jsonl"
    [exception_row] = [json.loads(line) for line in exceptions_path.read_bytes().splitlines()]
    assert exception_row["status"] == "cleaning_policy_dispute"
    assert (
        exception_row["proposal"]["expected_cleaned"] == expected["abap_cds-line-bced7abdf245bf3d"]
    )
    assert exception_row["detail"].startswith("Policy subkind normalization:")

    [case] = RUNNER.load_failures(failures).cases
    assert RUNNER._cleaning_policy_dispute_detail(case) == exception_row["detail"]
    assert RUNNER._cleaning_policy_dispute_detail(replace(case, language="abap")) is None
    assert RUNNER._cleaning_policy_dispute_detail(replace(case, raw_comment=raw + " ")) is None

    loaded = IMPORTER._load_oracle_exceptions(exceptions_path)[case.case_id]
    source = IMPORTER.SourceFailure(
        case_id=case.case_id,
        language=case.language,
        family_name="abap_cds_style",
        comment_kind=case.comment_kind,
        syntax_label=case.syntax_label,
        repo="owner/repo",
        path="src/example.ddls",
        raw_comment=case.raw_comment,
        candidate_cleaned_comment=case.baseline_cleaned_comment,
        cleaning_contract=case.cleaning_contract,
        judge_input_sha256="0" * 64,
        judge_rationale="The frozen candidate was rejected.",
        primary_model=case.primary_model,
        secondary_model=case.secondary_model,
        primary_cleaning_correct=False,
        secondary_cleaning_correct=False,
    )
    IMPORTER._validate_exception_matches_failure(source, loaded)
    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="cleaning_policy_identity",
    ):
        IMPORTER._validate_exception_matches_failure(
            replace(source, raw_comment=source.raw_comment + " "),
            loaded,
        )


def test_identical_raw_conflicting_literals_make_every_group_member_exceptional(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(
        failures,
        [
            _failure_row("conflict-a", raw_comment="# body"),
            _failure_row("conflict-b", raw_comment="# body"),
            _failure_row("conflict-c", raw_comment="# body"),
            _failure_row("unique", raw_comment="# unique"),
        ],
    )
    config = _config(tmp_path, failures, batch_size=4, workers=1)
    expected = {
        "conflict-a": "body",
        "conflict-b": " body",
        "conflict-c": "body",
        "unique": "unique",
    }

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=lambda cases, _: _proposal_payload(cases, expected),
            review_invoke=lambda cases, proposals, _: _approval_payload(
                cases,
                proposals,
            ),
            resolution_invoke=lambda *_: pytest.fail("approval-only run must not resolve"),
        )
        == 1
    )
    annotations_path = config.output_root / "reviewed_annotations.jsonl"
    exceptions_path = config.output_root / "oracle_exceptions.jsonl"
    annotations = [json.loads(line) for line in annotations_path.read_bytes().splitlines()]
    exceptions = [json.loads(line) for line in exceptions_path.read_bytes().splitlines()]
    assert [row["case_id"] for row in annotations] == ["unique"]
    assert [row["case_id"] for row in exceptions] == [
        "conflict-a",
        "conflict-b",
        "conflict-c",
    ]
    assert {row["status"] for row in exceptions} == {"intra_corpus_oracle_conflict"}
    assert all("conflict-a, conflict-b, conflict-c" in row["detail"] for row in exceptions)
    assert {row["proposal"]["expected_cleaned"] for row in exceptions} == {"body", " body"}

    loaded_annotations = IMPORTER._load_reviewed_oracles(annotations_path)
    loaded_exceptions = IMPORTER._load_oracle_exceptions(exceptions_path)
    source_failures = {
        case_id: IMPORTER.SourceFailure(
            case_id=case_id,
            language="python",
            family_name="hash_style",
            comment_kind="line",
            syntax_label="#",
            repo="owner/repo",
            path=f"src/{case_id}.py",
            raw_comment=("# unique" if case_id == "unique" else "# body"),
            candidate_cleaned_comment="rejected",
            cleaning_contract=(
                "Remove only comment syntax scaffolding and preserve content exactly."
            ),
            judge_input_sha256="0" * 64,
            judge_rationale="The frozen candidate was rejected.",
            primary_model="frozen-primary-reviewer",
            secondary_model="frozen-secondary-reviewer",
            primary_cleaning_correct=False,
            secondary_cleaning_correct=False,
        )
        for case_id in expected
    }
    IMPORTER._validate_case_partition(
        source_failures,
        loaded_annotations,
        loaded_exceptions,
    )
    incomplete_annotations = {
        **loaded_annotations,
        "conflict-c": IMPORTER.ReviewedOracle(
            case_id="conflict-c",
            raw_sha256=RUNNER._sha256_text("# body"),
            expected_cleaned="body",
            expected_cleaned_sha256=RUNNER._sha256_text("body"),
            disposition="confirmed_bug",
            method="invalid-partial-group",
            note="Deliberately incomplete group for validation.",
            reviewers=(RUNNER.REVIEW_MODEL, RUNNER.ORACLE_MODEL),
        ),
    }
    incomplete_exceptions = {
        case_id: exception
        for case_id, exception in loaded_exceptions.items()
        if case_id != "conflict-c"
    }
    with pytest.raises(
        IMPORTER.RegressionImportError,
        match="must classify every clean-consensus member",
    ):
        IMPORTER._validate_case_partition(
            source_failures,
            incomplete_annotations,
            incomplete_exceptions,
        )


def test_conflicting_literals_group_symmetrically_across_registry_aliases(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    rows = [
        _failure_row(
            "asp-a",
            language="asp",
            comment_kind="block",
            syntax_label="/*...*/",
            raw_comment="/* body */",
        ),
        _failure_row(
            "asp-net",
            language="asp_net",
            comment_kind="block",
            syntax_label="/*...*/",
            raw_comment="/* body */",
        ),
        _failure_row(
            "aspnet",
            language="aspnet",
            comment_kind="block",
            syntax_label="/*...*/",
            raw_comment="/* body */",
        ),
        _failure_row("perl6", language="perl6", raw_comment="# item"),
        _failure_row("raku", language="raku", raw_comment="# item"),
        _failure_row(
            "x-bit-map",
            language="x_bit_map",
            comment_kind="block",
            syntax_label="/*...*/",
            raw_comment="/* bitmap */",
        ),
        _failure_row(
            "x-bitmap",
            language="x_bitmap",
            comment_kind="block",
            syntax_label="/*...*/",
            raw_comment="/* bitmap */",
        ),
        _failure_row(
            "agree-asp",
            language="asp",
            comment_kind="block",
            syntax_label="/*...*/",
            raw_comment="/* agreed */",
        ),
        _failure_row(
            "agree-aspnet",
            language="aspnet",
            comment_kind="block",
            syntax_label="/*...*/",
            raw_comment="/* agreed */",
        ),
        _failure_row("different-perl6", language="perl6", raw_comment="# first"),
        _failure_row("different-raku", language="raku", raw_comment="# second"),
    ]
    _write_failures(failures, rows)
    config = _config(tmp_path, failures, batch_size=len(rows), workers=1)
    expected = {
        "asp-a": "body",
        "asp-net": " body",
        "aspnet": "body",
        "perl6": "item",
        "raku": " item",
        "x-bit-map": "bitmap",
        "x-bitmap": " bitmap",
        "agree-asp": "agreed",
        "agree-aspnet": "agreed",
        "different-perl6": "first",
        "different-raku": " second",
    }

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=lambda cases, _: _proposal_payload(cases, expected),
            review_invoke=lambda cases, proposals, _: _approval_payload(cases, proposals),
            resolution_invoke=lambda *_: pytest.fail("approval-only run must not resolve"),
        )
        == 1
    )
    annotations = [
        json.loads(line)
        for line in (config.output_root / "reviewed_annotations.jsonl").read_bytes().splitlines()
    ]
    exceptions_path = config.output_root / "oracle_exceptions.jsonl"
    exceptions = [json.loads(line) for line in exceptions_path.read_bytes().splitlines()]
    expected_conflict_ids = {
        "asp-a",
        "asp-net",
        "aspnet",
        "perl6",
        "raku",
        "x-bit-map",
        "x-bitmap",
    }
    assert {row["case_id"] for row in exceptions} == expected_conflict_ids
    assert {row["status"] for row in exceptions} == {"intra_corpus_oracle_conflict"}
    assert {row["case_id"] for row in annotations} == {
        "agree-asp",
        "agree-aspnet",
        "different-perl6",
        "different-raku",
    }
    assert all("canonical language family" in row["detail"] for row in exceptions)

    loaded_annotations = IMPORTER._load_reviewed_oracles(
        config.output_root / "reviewed_annotations.jsonl"
    )
    loaded_exceptions = IMPORTER._load_oracle_exceptions(exceptions_path)
    source_failures = {
        row["case"]["case_id"]: IMPORTER.SourceFailure(
            case_id=row["case"]["case_id"],
            language=row["case"]["language"],
            family_name="synthetic_alias",
            comment_kind=row["case"]["comment_kind"],
            syntax_label=row["case"]["syntax_label"],
            repo=row["case"]["repo"],
            path=row["case"]["path"],
            raw_comment=row["raw_comment"],
            candidate_cleaned_comment=row["candidate_cleaned_comment"],
            cleaning_contract=row["cleaning_contract"],
            judge_input_sha256="0" * 64,
            judge_rationale="The frozen candidate was rejected.",
            primary_model=row["primary"]["model"],
            secondary_model=row["secondary"]["model"],
            primary_cleaning_correct=False,
            secondary_cleaning_correct=False,
        )
        for row in rows
    }
    IMPORTER._validate_case_partition(
        source_failures,
        loaded_annotations,
        loaded_exceptions,
    )


@pytest.mark.parametrize("comment_kind", ["block", "nested"])
def test_retired_portugol_brace_boundary_is_extraction_invalid(
    tmp_path: Path,
    comment_kind: str,
) -> None:
    failures = tmp_path / "failures.jsonl"
    raw_program = "{\n/* note */\nfuncao inicio() {\n}\n}"
    case_id = f"portugol-{comment_kind}-program"
    _write_failures(
        failures,
        [
            _failure_row(
                case_id,
                language="portugol",
                comment_kind=comment_kind,
                syntax_label="{...}",
                raw_comment=raw_program,
                candidate="/* note */\nfuncao inicio() {",
            )
        ],
    )
    config = _config(tmp_path, failures, batch_size=1, workers=1)
    expected = "/* note */\nfuncao inicio() {\n}"

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=lambda cases, _: _proposal_payload(
                cases,
                {case_id: expected},
            ),
            review_invoke=lambda cases, proposals, _: _approval_payload(
                cases,
                proposals,
            ),
            resolution_invoke=lambda *_: pytest.fail("approval-only run must not resolve"),
        )
        == 1
    )
    annotations_path = config.output_root / "reviewed_annotations.jsonl"
    exceptions_path = config.output_root / "oracle_exceptions.jsonl"
    assert annotations_path.read_bytes() == b""
    exceptions = [json.loads(line) for line in exceptions_path.read_bytes().splitlines()]
    assert [row["status"] for row in exceptions] == ["extraction_invalid"]
    assert exceptions[0]["extraction_boundary_invalid"] is True
    assert exceptions[0]["proposal"]["disposition"] == "clean"
    assert exceptions[0]["review"]["decision"] == "approve"
    assert "whole Portugol program" in exceptions[0]["detail"]

    loaded_exception = IMPORTER._load_oracle_exceptions(exceptions_path)[case_id]
    source_failure = IMPORTER.SourceFailure(
        case_id=case_id,
        language="portugol",
        family_name="portugol_style",
        comment_kind=comment_kind,
        syntax_label="{...}",
        repo="owner/repo",
        path="src/program.por",
        raw_comment=raw_program,
        candidate_cleaned_comment="/* note */\nfuncao inicio() {",
        cleaning_contract=("Remove only comment syntax scaffolding and preserve content exactly."),
        judge_input_sha256="0" * 64,
        judge_rationale="The frozen parser treated program braces as comments.",
        primary_model="frozen-primary-reviewer",
        secondary_model="frozen-secondary-reviewer",
        primary_cleaning_correct=False,
        secondary_cleaning_correct=False,
    )
    IMPORTER._validate_exception_matches_failure(
        source_failure,
        loaded_exception,
    )
    assert IMPORTER._reconstruct_boundary_assertion(source_failure) == {
        "expected_match": "/* note */",
        "expected_match_sha256": RUNNER._sha256_text("/* note */"),
        "kind": "comment_query_first_embedded_match",
    }


def test_malformed_luna_approval_is_journaled_nonfatally_and_resumes(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(
        failures,
        [
            _failure_row("slow-malformed", raw_comment="# slow"),
            _failure_row("fast-valid", raw_comment="# fast"),
        ],
    )
    config = _config(tmp_path, failures, batch_size=1, workers=2)
    expected = {
        "slow-malformed": "slow",
        "fast-valid": "fast",
    }
    fast_returned = threading.Event()
    valid_review_persisted_before_slow_finished = threading.Event()
    review_calls: list[str] = []

    def propose(cases, runner_config):
        return _proposal_payload(cases, expected)

    def review(cases, proposals, runner_config):
        case = cases[0]
        review_calls.append(case.case_id)
        if case.case_id == "fast-valid":
            fast_returned.set()
            return _approval_payload(cases, proposals)

        assert fast_returned.wait(timeout=2)
        review_journal = config.output_root / "luna_reviews.journal.jsonl"
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            if review_journal.exists() and review_journal.read_bytes().strip():
                valid_review_persisted_before_slow_finished.set()
                break
            time.sleep(0.005)
        proposal = proposals[case.case_id]
        return {
            "reviews": [
                {
                    "case_id": case.case_id,
                    "decision": "approve",
                    "expected_cleaned": proposal["expected_cleaned"] + " altered",
                    "disposition": proposal["disposition"],
                    "rationale": "Malformed approval changed the exact literal.",
                    "confidence": 0.9,
                }
            ]
        }

    def unexpected_resolution(*args, **kwargs):
        raise AssertionError("terminal review failures must not be resolved")

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=propose,
            review_invoke=review,
            resolution_invoke=unexpected_resolution,
        )
        == 1
    )
    assert valid_review_persisted_before_slow_finished.is_set()
    assert review_calls.count("slow-malformed") == 2
    assert review_calls.count("fast-valid") == 1

    review_rows = [
        json.loads(line)
        for line in (config.output_root / "luna_reviews.journal.jsonl").read_bytes().splitlines()
    ]
    assert [row["case_id"] for row in review_rows] == ["fast-valid"]
    failure_rows = [
        json.loads(line)
        for line in (config.output_root / "luna_review_failures.journal.jsonl")
        .read_bytes()
        .splitlines()
    ]
    assert [row["case_id"] for row in failure_rows] == ["slow-malformed"]
    assert failure_rows[0]["status"] == RUNNER.MALFORMED_MODEL_OUTPUT
    assert failure_rows[0]["attempt_count"] == 2
    assert "does not exactly copy" in failure_rows[0]["detail"]

    annotations = [
        json.loads(line)
        for line in (config.output_root / "reviewed_annotations.jsonl").read_bytes().splitlines()
    ]
    exceptions = [
        json.loads(line)
        for line in (config.output_root / "oracle_exceptions.jsonl").read_bytes().splitlines()
    ]
    assert [row["case_id"] for row in annotations] == ["fast-valid"]
    assert [row["case_id"] for row in exceptions] == ["slow-malformed"]
    assert exceptions[0]["status"] == "reviewer_disagreement"
    assert exceptions[0]["review"]["decision"] == "replace"
    assert exceptions[0]["review"]["disposition"] != exceptions[0]["proposal"]["disposition"]
    assert "terminal, non-consensus oracle exception" in exceptions[0]["detail"]
    assert {row["case_id"] for row in [*annotations, *exceptions]} == {
        "slow-malformed",
        "fast-valid",
    }
    loaded_annotations = IMPORTER._load_reviewed_oracles(
        config.output_root / "reviewed_annotations.jsonl"
    )
    loaded_exceptions = IMPORTER._load_oracle_exceptions(
        config.output_root / "oracle_exceptions.jsonl"
    )
    IMPORTER._validate_case_partition(
        {
            "slow-malformed": SimpleNamespace(
                language="python",
                raw_comment="# slow",
            ),
            "fast-valid": SimpleNamespace(
                language="python",
                raw_comment="# fast",
            ),
        },
        loaded_annotations,
        loaded_exceptions,
    )

    artifact_paths = [
        config.output_root / "luna_reviews.journal.jsonl",
        config.output_root / "luna_review_failures.journal.jsonl",
        config.output_root / "reviewed_annotations.jsonl",
        config.output_root / "oracle_exceptions.jsonl",
        config.output_root / "run_summary.json",
    ]
    before_resume = {path: path.read_bytes() for path in artifact_paths}

    def unexpected(*args, **kwargs):
        raise AssertionError(f"resume called a model: args={args!r}, kwargs={kwargs!r}")

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=unexpected,
            review_invoke=unexpected,
            resolution_invoke=unexpected,
        )
        == 1
    )
    assert {path: path.read_bytes() for path in artifact_paths} == before_resume


def test_known_operational_protocol_revision_migrates_but_unknown_one_rejects(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(failures, [_failure_row("case-1", raw_comment="# body")])
    config = _config(tmp_path, failures, batch_size=1, workers=1)
    loaded = RUNNER.load_failures(failures)
    expected_metadata = RUNNER._expected_metadata(loaded, config)
    metadata = RUNNER._ensure_run_metadata(
        config.output_root,
        expected_metadata,
    )
    legacy_digest = "9e95189b2e0754c7d137dcd47127b1b5d26371f67d8f7c3db51dbb86a1ab83e1"
    assert legacy_digest in RUNNER.COMPATIBLE_LEGACY_PROTOCOL_SHA256S

    unmarked_root = tmp_path / "legacy-without-isolation-marker"
    unmarked_metadata = {
        **expected_metadata,
        "oracle_protocol_sha256": legacy_digest,
    }
    unmarked_metadata.pop("prior_judge_evidence_in_proposal_prompt")
    RUNNER._atomic_write_json(unmarked_root / "run_metadata.json", unmarked_metadata)
    with pytest.raises(
        RUNNER.ResumeError,
        match="prior_judge_evidence_in_proposal_prompt",
    ):
        RUNNER._ensure_run_metadata(unmarked_root, expected_metadata)

    RUNNER._atomic_write_json(
        config.output_root / "run_metadata.json",
        {**metadata, "oracle_protocol_sha256": legacy_digest},
    )

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=lambda cases, _: _proposal_payload(
                cases,
                {"case-1": "body"},
            ),
            review_invoke=lambda cases, proposals, _: _approval_payload(
                cases,
                proposals,
            ),
            resolution_invoke=lambda *_: pytest.fail("approval-only run must not resolve"),
        )
        == 0
    )
    migrated = json.loads((config.output_root / "run_metadata.json").read_bytes())
    assert migrated["protocol_migrated_from_sha256"] == legacy_digest
    assert migrated["oracle_protocol_sha256"] == RUNNER._oracle_protocol_sha256()

    unknown_root = tmp_path / "unknown"
    unknown_root.mkdir()
    unknown_failures = unknown_root / "failures.jsonl"
    _write_failures(unknown_failures, [_failure_row("case-1")])
    unknown_config = _config(unknown_root, unknown_failures)
    unknown_loaded = RUNNER.load_failures(unknown_failures)
    unknown_metadata = RUNNER._ensure_run_metadata(
        unknown_config.output_root,
        RUNNER._expected_metadata(unknown_loaded, unknown_config),
    )
    RUNNER._atomic_write_json(
        unknown_config.output_root / "run_metadata.json",
        {**unknown_metadata, "oracle_protocol_sha256": "0" * 64},
    )
    with pytest.raises(RUNNER.ResumeError, match="oracle_protocol_sha256"):
        RUNNER.run_pipeline(
            unknown_config,
            proposal_invoke=lambda *_: pytest.fail("unsafe resume invoked a model"),
            review_invoke=lambda *_: pytest.fail("unsafe resume invoked a model"),
            resolution_invoke=lambda *_: pytest.fail("unsafe resume invoked a model"),
        )


@pytest.mark.parametrize("partial_stage", ["proposal", "review", "resolution"])
def test_partial_stage_resume_reuses_original_full_batch(
    tmp_path: Path,
    partial_stage: str,
) -> None:
    stage_root = tmp_path / partial_stage
    stage_root.mkdir()
    failures = stage_root / "failures.jsonl"
    _write_failures(
        failures,
        [
            _failure_row("case-1", raw_comment="# one"),
            _failure_row("case-2", raw_comment="# two"),
        ],
    )
    config = _config(stage_root, failures, batch_size=2, workers=1)
    loaded = RUNNER.load_failures(failures)
    RUNNER._ensure_run_metadata(
        config.output_root,
        RUNNER._expected_metadata(loaded, config),
    )
    cases = loaded.cases
    cases_by_id = {case.case_id: case for case in cases}
    expected = {"case-1": "one", "case-2": "two"}
    proposal_rows = RUNNER._generate_batch_resilient(
        cases,
        config=config,
        invoke=lambda batch, _: _proposal_payload(batch, expected),
    )
    proposals = {row["case_id"]: row for row in proposal_rows}
    proposal_store = RUNNER.OracleResultStore(
        config.output_root / "sol_proposals.journal.jsonl",
        cases_by_id=cases_by_id,
    )
    proposal_store.append_many(proposal_rows[:1] if partial_stage == "proposal" else proposal_rows)

    review_decision = "replace" if partial_stage == "resolution" else "approve"

    def review_payload(batch, proposal_results):
        rows = []
        for case in batch:
            proposal = proposal_results[case.case_id]
            rows.append(
                {
                    "case_id": case.case_id,
                    "decision": review_decision,
                    "disposition": "clean",
                    "expected_cleaned": (
                        "" if review_decision == "replace" else proposal["expected_cleaned"]
                    ),
                    "rationale": "Independent exact review.",
                    "confidence": 0.9,
                }
            )
        return {"reviews": rows}

    reviews: dict[str, dict] = {}
    if partial_stage in {"review", "resolution"}:
        review_rows = RUNNER._generate_review_batch_resilient(
            cases,
            proposals=proposals,
            config=config,
            invoke=lambda batch, proposal_results, _: review_payload(
                batch,
                proposal_results,
            ),
        )
        reviews = {row["case_id"]: row for row in review_rows}
        review_store = RUNNER.ReviewResultStore(
            config.output_root / "luna_reviews.journal.jsonl",
            cases_by_id=cases_by_id,
            proposals=proposals,
        )
        review_store.append_many(review_rows[:1] if partial_stage == "review" else review_rows)

    if partial_stage == "resolution":
        resolution_rows = RUNNER._generate_resolution_batch_resilient(
            cases,
            proposals=proposals,
            reviews=reviews,
            config=config,
            invoke=lambda batch, _proposals, _reviews, _: {
                "resolutions": [
                    {
                        "case_id": case.case_id,
                        "decision": "accept_reviewer",
                        "rationale": "Accepted exactly.",
                        "confidence": 0.9,
                    }
                    for case in batch
                ]
            },
        )
        resolution_store = RUNNER.ResolutionResultStore(
            config.output_root / "sol_resolutions.journal.jsonl",
            cases_by_id=cases_by_id,
            proposals=proposals,
            reviews=reviews,
        )
        resolution_store.append_many(resolution_rows[:1])

    calls = {"proposal": [], "review": [], "resolution": []}

    def propose(batch, runner_config):
        calls["proposal"].append(tuple(case.case_id for case in batch))
        return _proposal_payload(batch, expected)

    def review(batch, proposal_results, runner_config):
        calls["review"].append(tuple(case.case_id for case in batch))
        return review_payload(batch, proposal_results)

    def resolve(batch, proposal_results, review_results, runner_config):
        calls["resolution"].append(tuple(case.case_id for case in batch))
        return {
            "resolutions": [
                {
                    "case_id": case.case_id,
                    "decision": "accept_reviewer",
                    "rationale": "Accepted exactly.",
                    "confidence": 0.9,
                }
                for case in batch
            ]
        }

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=propose,
            review_invoke=review,
            resolution_invoke=resolve,
        )
        == 0
    )
    assert calls[partial_stage] == [("case-1", "case-2")]
    earlier_stages = {
        "proposal": set(),
        "review": {"proposal"},
        "resolution": {"proposal", "review"},
    }[partial_stage]
    assert all(calls[stage] == [] for stage in earlier_stages)


def test_pipeline_escalates_replacements_and_flags_nonimportable_cases(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(
        failures,
        [
            _failure_row("accepted-replacement", raw_comment="# correct"),
            _failure_row("unresolved", raw_comment="# disputed"),
            _failure_row("bad-boundary", raw_comment="code # comment"),
            _failure_row("ambiguous", raw_comment="# maybe"),
            _failure_row("not-deletion-only", raw_comment="# body"),
        ],
    )
    config = _config(tmp_path, failures, batch_size=5, workers=1)

    def propose(cases, runner_config):
        values = {
            "accepted-replacement": ("clean", "orrect"),
            "unresolved": ("clean", "disputed"),
            "bad-boundary": ("extraction_invalid", ""),
            "ambiguous": ("ambiguous", ""),
            "not-deletion-only": ("clean", "invented"),
        }
        return {
            "oracles": [
                {
                    "case_id": case.case_id,
                    "disposition": values[case.case_id][0],
                    "expected_cleaned": values[case.case_id][1],
                    "rationale": "Initial exact derivation.",
                    "confidence": 0.8,
                }
                for case in cases
            ]
        }

    def review(cases, proposals, runner_config):
        replacements = {
            "accepted-replacement": ("clean", "correct"),
            "unresolved": ("clean", "dispute"),
        }
        rows = []
        for case in cases:
            proposal = proposals[case.case_id]
            if case.case_id in replacements:
                disposition, literal = replacements[case.case_id]
                decision = "replace"
            else:
                disposition = proposal["disposition"]
                literal = proposal["expected_cleaned"]
                decision = "approve"
            rows.append(
                {
                    "case_id": case.case_id,
                    "decision": decision,
                    "disposition": disposition,
                    "expected_cleaned": literal,
                    "rationale": "Independent review.",
                    "confidence": 0.9,
                }
            )
        return {"reviews": rows}

    resolution_calls: list[tuple[str, ...]] = []

    def resolve(cases, proposals, reviews, runner_config):
        resolution_calls.append(tuple(case.case_id for case in cases))
        return {
            "resolutions": [
                {
                    "case_id": case.case_id,
                    "decision": (
                        "accept_reviewer"
                        if case.case_id == "accepted-replacement"
                        else "unresolved"
                    ),
                    "rationale": "Rechecked both exact literals.",
                    "confidence": 0.85,
                }
                for case in cases
            ]
        }

    assert (
        RUNNER.run_pipeline(
            config,
            proposal_invoke=propose,
            review_invoke=review,
            resolution_invoke=resolve,
        )
        == 1
    )
    assert resolution_calls == [("accepted-replacement", "unresolved")]
    annotations = [
        json.loads(line)
        for line in (config.output_root / "reviewed_annotations.jsonl").read_bytes().splitlines()
    ]
    assert [row["case_id"] for row in annotations] == ["accepted-replacement"]
    assert annotations[0]["expected_cleaned"] == "correct"
    assert annotations[0]["oracle"]["method"] == "luna_replacement_sol_exact_acceptance"

    exceptions = [
        json.loads(line)
        for line in (config.output_root / "oracle_exceptions.jsonl").read_bytes().splitlines()
    ]
    assert [row["case_id"] for row in exceptions] == [
        "unresolved",
        "bad-boundary",
        "ambiguous",
        "not-deletion-only",
    ]
    assert [row["status"] for row in exceptions] == [
        "reviewer_disagreement",
        "extraction_invalid",
        "ambiguous",
        "oracle_not_deletion_only",
    ]
    boundary = exceptions[1]
    assert boundary["extraction_boundary_invalid"] is True
    assert "boundary is invalid" in boundary["detail"]
    summary = json.loads((config.output_root / "run_summary.json").read_bytes())
    assert summary["import_ready"] is False
    assert summary["annotation_count"] == 1
    assert summary["exception_count"] == 4


def test_inspect_only_is_non_mutating_and_reports_oversized_case(
    tmp_path: Path,
) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(
        failures,
        [_failure_row("large", raw_comment="#" + ("x" * 2_000))],
    )
    config = _config(tmp_path, failures, max_prompt_chars=500)

    inspection = RUNNER.inspect_pipeline(config)

    assert inspection["case_count"] == 1
    assert inspection["proposal_oversized_singleton_batches"] == 1
    assert inspection["minimum_review_stages"] == 2
    assert inspection["maximum_review_stages"] == 3
    assert inspection["model_calls_made"] == 0
    assert inspection["files_written"] == 0
    assert not config.output_root.exists()
    assert RUNNER.parse_args(
        [
            "--failures",
            str(failures),
            "--output-root",
            str(config.output_root),
            "--dry-run",
        ]
    ).inspect_only


def test_codex_invocations_are_isolated_ephemeral_and_candidate_free(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    failures = tmp_path / "failures.jsonl"
    rejected = "NEVER SEND THIS REJECTED CANDIDATE"
    _write_failures(
        failures,
        [_failure_row("case-1", candidate=rejected)],
    )
    case = RUNNER.load_failures(failures).cases[0]
    config = _config(tmp_path, failures)
    captured: list[tuple[list[str], str, Path]] = []
    proposal = {
        "disposition": "clean",
        "expected_cleaned": "raw",
        "rationale": "Exact.",
        "confidence": 0.9,
    }
    review = {
        "decision": "replace",
        "disposition": "clean",
        "expected_cleaned": "ra",
        "rationale": "Replacement.",
        "confidence": 0.8,
    }

    def fake_run(command, **kwargs):
        captured.append((command, kwargs["input"], kwargs["cwd"]))
        model = command[command.index("--model") + 1]
        prompt = kwargs["input"]
        if model == RUNNER.REVIEW_MODEL:
            payload = {
                "reviews": [
                    {
                        "case_id": case.case_id,
                        "decision": "replace",
                        "expected_cleaned": review["expected_cleaned"],
                        "disposition": review["disposition"],
                        "rationale": review["rationale"],
                        "confidence": review["confidence"],
                    }
                ]
            }
        elif "Resolution cases:" in prompt:
            payload = {
                "resolutions": [
                    {
                        "case_id": case.case_id,
                        "decision": "accept_reviewer",
                        "rationale": "Exact agreement.",
                        "confidence": 0.9,
                    }
                ]
            }
        else:
            payload = _clean_payload([case])
        output_index = command.index("--output-last-message") + 1
        Path(command[output_index]).write_text(
            json.dumps(payload),
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(RUNNER.subprocess, "run", fake_run)

    assert RUNNER._invoke_codex_batch([case], config) == _clean_payload([case])
    assert (
        RUNNER._invoke_luna_review_batch(
            [case],
            {case.case_id: proposal},
            config,
        )["reviews"][0]["decision"]
        == "replace"
    )
    assert (
        RUNNER._invoke_sol_resolution_batch(
            [case],
            {case.case_id: proposal},
            {case.case_id: review},
            config,
        )["resolutions"][0]["decision"]
        == "accept_reviewer"
    )

    assert [command[command.index("--model") + 1] for command, _, _ in captured] == [
        "gpt-5.6-sol",
        "gpt-5.6-luna",
        "gpt-5.6-sol",
    ]
    for command, prompt, launch_cwd in captured:
        assert command[command.index("--ask-for-approval") + 1] == "never"
        assert command[command.index("--sandbox") + 1] == "read-only"
        assert "--ephemeral" in command
        assert "--ignore-user-config" in command
        assert "--ignore-rules" in command
        assert "--skip-git-repo-check" in command
        model_cwd = Path(command[command.index("--cd") + 1])
        assert model_cwd.name == "empty-model-workdir"
        assert model_cwd != config.codex_cwd
        assert launch_cwd == config.codex_cwd
        assert rejected not in prompt


def test_resume_repairs_only_truncated_final_journal_line(tmp_path: Path) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(failures, [_failure_row("case-1")])
    case = RUNNER.load_failures(failures).cases[0]
    path = tmp_path / "journal.jsonl"
    row = {
        "schema_version": RUNNER.SCHEMA_VERSION,
        "stage": RUNNER.PROPOSAL_STAGE,
        "model": RUNNER.ORACLE_MODEL,
        "case_id": case.case_id,
        "input_sha256": case.input_sha256,
        "batch_id": "batch",
        "disposition": "clean",
        "expected_cleaned": "\x00α\n",
        "rationale": "Exact.",
        "confidence": 0.9,
        "generated_at": "2026-07-28T00:00:00Z",
    }
    path.write_bytes(RUNNER._canonical_json_bytes(row) + b"\n" + b'{"partial":')

    store = RUNNER.OracleResultStore(
        path,
        cases_by_id={case.case_id: case},
    )

    assert store.results == {case.case_id: row}
    assert path.read_bytes().endswith(b"\n")


def test_review_resume_rejects_stale_proposal_dependency(tmp_path: Path) -> None:
    failures = tmp_path / "failures.jsonl"
    _write_failures(failures, [_failure_row("case-1")])
    case = RUNNER.load_failures(failures).cases[0]
    config = _config(tmp_path, failures)
    proposal = RUNNER._generate_batch_resilient(
        [case],
        config=config,
        invoke=lambda batch, _: _proposal_payload(batch, {"case-1": "raw"}),
    )[0]
    review = RUNNER._generate_review_batch_resilient(
        [case],
        proposals={"case-1": proposal},
        config=config,
        invoke=lambda batch, proposals, _: _approval_payload(batch, proposals),
    )[0]
    review["proposal_sha256"] = "0" * 64
    path = tmp_path / "reviews.jsonl"
    path.write_bytes(RUNNER._canonical_json_bytes(review) + b"\n")

    with pytest.raises(RUNNER.ResumeError, match="proposal fingerprint mismatch"):
        RUNNER.ReviewResultStore(
            path,
            cases_by_id={"case-1": case},
            proposals={"case-1": proposal},
        )
