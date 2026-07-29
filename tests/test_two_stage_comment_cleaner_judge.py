"""Tests for the scalable two-stage comment-cleaner judge runner."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import threading
from dataclasses import replace
from pathlib import Path

import pytest


def _load_runner():
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "run_two_stage_comment_cleaner_judge.py"
    )
    spec = importlib.util.spec_from_file_location(
        "run_two_stage_comment_cleaner_judge",
        script_path,
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = _load_runner()


def _manifest_row(
    case_id: str,
    *,
    language: str = "python",
    raw_comment: str = "# keep me",
) -> dict:
    return {
        "case_id": case_id,
        "language": language,
        "comment_kind": "line",
        "syntax_label": "line",
        "repo": "owner/repo",
        "path": f"src/{case_id}.py",
        "raw_comment": raw_comment,
        "cleaned_comment": "UNTRUSTED MANIFEST ORACLE",
    }


def _write_manifest(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )


def _config(
    tmp_path: Path,
    manifest: Path,
    *,
    batch_size: int = 50,
    max_prompt_chars: int = 80_000,
    workers: int = 2,
) -> object:
    return RUNNER.RunnerConfig(
        manifest=manifest,
        output_root=tmp_path / "judge-output",
        codex_bin="codex",
        codex_cwd=tmp_path,
        batch_size=batch_size,
        max_prompt_chars=max_prompt_chars,
        max_text_chars=12_000,
        text_edge_chars=2_000,
        workers=workers,
        timeout=30,
        malformed_single_retries=1,
    )


def _passing_payload(cases) -> dict:
    return {
        "verdicts": [
            {
                "case_id": case.case_id,
                "verdict": "pass",
                "cleaning_correct": True,
                "rationale": "correct",
            }
            for case in cases
        ]
    }


def test_manifest_recomputes_sanitizer_output_instead_of_using_oracle(
    tmp_path: Path,
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(manifest, [_manifest_row("case-1")])

    loaded = RUNNER.load_manifest(manifest)

    assert loaded.cases[0].candidate_cleaned_comment == "keep me"
    assert loaded.cases[0].candidate_cleaned_comment != "UNTRUSTED MANIFEST ORACLE"


def test_language_batches_respect_case_and_prompt_caps(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(
        manifest,
        [
            _manifest_row("py-1"),
            _manifest_row("java-1", language="java", raw_comment="// first"),
            _manifest_row("py-2"),
            _manifest_row("java-2", language="java", raw_comment="// second"),
            _manifest_row("py-3"),
        ],
    )
    cases = RUNNER.load_manifest(manifest).cases
    config = _config(tmp_path, manifest, batch_size=2)

    batches = RUNNER.build_language_batches(cases, config)

    assert [len(batch) for batch in batches] == [2, 1, 2]
    assert all(len({case.language for case in batch}) == 1 for batch in batches)

    python_cases = [case for case in cases if case.language == "python"][:2]
    one_case_size = len(RUNNER.build_judge_prompt(python_cases[:1], config))
    two_case_size = len(RUNNER.build_judge_prompt(python_cases, config))
    capped = replace(
        config,
        batch_size=50,
        max_prompt_chars=(one_case_size + two_case_size) // 2,
    )
    assert [len(batch) for batch in RUNNER.build_language_batches(python_cases, capped)] == [
        1,
        1,
    ]


def test_oversized_case_uses_complete_strings_in_singleton_and_summary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    middle = "MIDDLE_CONTENT_MUST_BE_JUDGED"
    raw_comment = f"# {'a' * 6_100}{middle}{'b' * 6_100}"
    _write_manifest(
        manifest,
        [
            _manifest_row("before"),
            _manifest_row("oversized", raw_comment=raw_comment),
            _manifest_row("after"),
        ],
    )
    cases = RUNNER.load_manifest(manifest).cases
    oversized = cases[1]
    base_config = _config(tmp_path, manifest)
    oversized_prompt_chars = len(RUNNER.build_judge_prompt([oversized], base_config))
    config = replace(
        base_config,
        max_prompt_chars=oversized_prompt_chars - 1,
    )

    prompt_case = RUNNER._prompt_case(oversized, config)
    assert prompt_case["raw_comment"] == raw_comment
    assert prompt_case["candidate_cleaned_comment"] == raw_comment.removeprefix("# ")
    assert middle in prompt_case["raw_comment"]
    assert middle in prompt_case["candidate_cleaned_comment"]
    assert [
        tuple(case.case_id for case in batch)
        for batch in RUNNER.build_language_batches(
            cases,
            config,
        )
    ] == [("before",), ("oversized",), ("after",)]

    captured_prompt = ""

    def fake_run(command, **kwargs):
        nonlocal captured_prompt
        captured_prompt = kwargs["input"]
        output_index = command.index("--output-last-message") + 1
        Path(command[output_index]).write_text(
            json.dumps(_passing_payload([oversized])),
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(RUNNER.subprocess, "run", fake_run)
    assert RUNNER._invoke_codex_batch(
        [oversized],
        RUNNER.PRIMARY_MODEL,
        config,
    ) == _passing_payload([oversized])
    assert len(captured_prompt) > config.max_prompt_chars
    assert raw_comment in captured_prompt
    assert middle in captured_prompt
    assert '"truncated":true' not in captured_prompt

    assert (
        RUNNER.run_pipeline(
            config,
            invoke=lambda batch, model, runner_config: _passing_payload(batch),
        )
        == 0
    )
    summary = json.loads((config.output_root / "run_summary.json").read_text())
    assert summary["full_judgment_input_strings"] is True
    assert summary["oversized_case_policy"] == "full_fidelity_singleton"
    assert summary["full_fidelity_singleton_cases"] == 1
    metadata = json.loads((config.output_root / "run_metadata.json").read_text())
    assert metadata["full_judgment_input_strings"] is True
    assert metadata["oversized_case_policy"] == "full_fidelity_singleton"
    assert metadata["model_working_directory"] == "ephemeral_empty_directory"
    final_results = [
        json.loads(line)
        for line in (config.output_root / "final_results.jsonl").read_text().splitlines()
    ]
    assert next(row for row in final_results if row["case_id"] == "oversized")["final_pass"] is True


@pytest.mark.parametrize(
    "payload, error",
    [
        ({"verdicts": []}, "missing verdict"),
        (
            {
                "verdicts": [
                    {
                        "case_id": "case-1",
                        "verdict": "pass",
                        "cleaning_correct": True,
                        "rationale": "ok",
                    },
                    {
                        "case_id": "case-1",
                        "verdict": "pass",
                        "cleaning_correct": True,
                        "rationale": "again",
                    },
                ]
            },
            "duplicate verdict",
        ),
        (
            {
                "verdicts": [
                    {
                        "case_id": "unknown",
                        "verdict": "pass",
                        "cleaning_correct": True,
                        "rationale": "ok",
                    }
                ]
            },
            "unexpected case_id",
        ),
    ],
)
def test_batch_response_requires_exactly_one_verdict_per_case(
    tmp_path: Path,
    payload: dict,
    error: str,
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(manifest, [_manifest_row("case-1")])
    cases = RUNNER.load_manifest(manifest).cases

    with pytest.raises(RUNNER.InvalidJudgeOutput, match=error):
        RUNNER.validate_batch_response(payload, cases)


def test_malformed_batch_is_recursively_split_and_saved(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(manifest, [_manifest_row("case-1"), _manifest_row("case-2")])
    cases = RUNNER.load_manifest(manifest).cases
    config = _config(tmp_path, manifest)
    store = RUNNER.ResultStore(
        config.output_root / "primary_results.jsonl",
        stage=RUNNER.PRIMARY_STAGE,
        model=RUNNER.PRIMARY_MODEL,
        cases_by_id={case.case_id: case for case in cases},
    )
    call_sizes = []

    def invoke(batch, model, runner_config):
        assert model == RUNNER.PRIMARY_MODEL
        assert runner_config == config
        call_sizes.append(len(batch))
        if len(batch) > 1:
            return {"verdicts": []}
        return _passing_payload(batch)

    RUNNER._judge_batch_resilient(
        cases,
        stage=RUNNER.PRIMARY_STAGE,
        model=RUNNER.PRIMARY_MODEL,
        config=config,
        store=store,
        invoke=invoke,
        abort_event=threading.Event(),
    )

    assert call_sizes == [2, 1, 1]
    assert set(store.results) == {"case-1", "case-2"}


def test_pipeline_escalates_only_primary_failures_and_resumes(
    tmp_path: Path,
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(
        manifest,
        [
            _manifest_row("pass-primary"),
            _manifest_row("fail-primary"),
            _manifest_row("pass-java", language="java", raw_comment="// java"),
        ],
    )
    config = _config(tmp_path, manifest)
    calls: list[tuple[str, tuple[str, ...]]] = []

    def invoke(cases, model, runner_config):
        assert runner_config == config
        calls.append((model, tuple(case.case_id for case in cases)))
        verdicts = []
        for case in cases:
            primary_failure = model == RUNNER.PRIMARY_MODEL and case.case_id == "fail-primary"
            verdicts.append(
                {
                    "case_id": case.case_id,
                    "verdict": "fail" if primary_failure else "pass",
                    "cleaning_correct": not primary_failure,
                    "rationale": "needs review" if primary_failure else "correct",
                }
            )
        return {"verdicts": verdicts}

    assert RUNNER.run_pipeline(config, invoke=invoke) == 0

    secondary_calls = [case_ids for model, case_ids in calls if model == RUNNER.SECONDARY_MODEL]
    assert secondary_calls == [("fail-primary",)]
    assert len((config.output_root / "primary_results.jsonl").read_text().splitlines()) == 3
    assert len((config.output_root / "secondary_results.jsonl").read_text().splitlines()) == 1
    summary = json.loads((config.output_root / "run_summary.json").read_text())
    assert summary["primary_failures"] == 1
    assert summary["final_failures"] == 0
    metadata = json.loads((config.output_root / "run_metadata.json").read_text())
    assert metadata["judge_protocol_sha256"] == RUNNER._judge_protocol_sha256()

    def unexpected_call(cases, model, runner_config):
        raise AssertionError(f"resume unexpectedly called {model} for {cases}")

    assert RUNNER.run_pipeline(config, invoke=unexpected_call) == 0
    with pytest.raises(RUNNER.ResumeError, match="batch_size"):
        RUNNER.run_pipeline(replace(config, batch_size=10), invoke=unexpected_call)


def test_changed_judge_protocol_digest_rejects_resume(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(manifest, [_manifest_row("case-1")])
    config = _config(tmp_path, manifest)

    assert RUNNER.run_pipeline(config, invoke=lambda cases, model, _: _passing_payload(cases)) == 0
    saved_metadata = json.loads((config.output_root / "run_metadata.json").read_text())
    assert saved_metadata["judge_protocol_sha256"] == RUNNER._judge_protocol_sha256()

    monkeypatch.setattr(RUNNER, "_judge_protocol_sha256", lambda: "changed-protocol-digest")

    def unexpected_call(cases, model, runner_config):
        raise AssertionError(f"unsafe resume unexpectedly called {model} for {cases}")

    with pytest.raises(RUNNER.ResumeError, match="judge_protocol_sha256"):
        RUNNER.run_pipeline(config, invoke=unexpected_call)


def test_final_failure_has_machine_and_human_reports(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(manifest, [_manifest_row("bad-cleaning")])
    config = _config(tmp_path, manifest)

    def reject(cases, model, runner_config):
        return {
            "verdicts": [
                {
                    "case_id": cases[0].case_id,
                    "verdict": "fail",
                    "cleaning_correct": False,
                    "rationale": f"rejected by {model}",
                }
            ]
        }

    assert RUNNER.run_pipeline(config, invoke=reject) == 1

    failures = [
        json.loads(line)
        for line in (config.output_root / "final_failures.jsonl").read_text().splitlines()
    ]
    assert failures[0]["case"]["case_id"] == "bad-cleaning"
    assert failures[0]["primary"]["model"] == RUNNER.PRIMARY_MODEL
    assert failures[0]["secondary"]["model"] == RUNNER.SECONDARY_MODEL
    report = (config.output_root / "final_failures.md").read_text()
    assert "Two-stage Comment Cleaner Judge Failures" in report
    assert '"case_id": "bad-cleaning"' in report


def test_failure_report_fence_is_longer_than_backticks_in_payload(
    tmp_path: Path,
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    raw_comment = "// triple ``` and long ```````` fence-like content"
    _write_manifest(
        manifest,
        [_manifest_row("backtick-cleaning", raw_comment=raw_comment)],
    )
    config = _config(tmp_path, manifest)

    def reject(cases, model, runner_config):
        return {
            "verdicts": [
                {
                    "case_id": cases[0].case_id,
                    "verdict": "fail",
                    "cleaning_correct": False,
                    "rationale": f"rejected by {model}",
                }
            ]
        }

    assert RUNNER.run_pipeline(config, invoke=reject) == 1

    failure_line = (config.output_root / "final_failures.jsonl").read_text().strip()
    failure = json.loads(failure_line)
    assert failure["raw_comment"] == raw_comment
    machine_payload = json.dumps(
        failure,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    expected_fence = "`" * 9
    assert RUNNER._markdown_backtick_fence(machine_payload) == expected_fence

    report = (config.output_root / "final_failures.md").read_text()
    assert f"\n{expected_fence}json\n{machine_payload}\n{expected_fence}\n" in report


def test_codex_invocation_is_read_only_approval_never_and_exact_model(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(manifest, [_manifest_row("case-1")])
    case = RUNNER.load_manifest(manifest).cases[0]
    config = _config(tmp_path, manifest)
    captured_command: list[str] = []
    captured_launch_cwd: Path | None = None
    captured_model_cwd: Path | None = None

    def fake_run(command, **kwargs):
        nonlocal captured_launch_cwd, captured_model_cwd
        captured_command.extend(command)
        captured_launch_cwd = kwargs["cwd"]
        captured_model_cwd = Path(command[command.index("--cd") + 1])
        assert captured_model_cwd.is_dir()
        assert list(captured_model_cwd.iterdir()) == []
        output_index = command.index("--output-last-message") + 1
        Path(command[output_index]).write_text(
            json.dumps(_passing_payload([case])),
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(RUNNER.subprocess, "run", fake_run)

    payload = RUNNER._invoke_codex_batch([case], RUNNER.PRIMARY_MODEL, config)

    assert payload == _passing_payload([case])
    assert captured_command[captured_command.index("--ask-for-approval") + 1] == "never"
    assert captured_command[captured_command.index("--sandbox") + 1] == "read-only"
    assert captured_command[captured_command.index("--model") + 1] == "gpt-5.6-luna"
    assert "--ignore-user-config" in captured_command
    assert "--ignore-rules" in captured_command
    assert "--skip-git-repo-check" in captured_command
    assert "--ephemeral" in captured_command
    assert captured_launch_cwd == config.codex_cwd
    assert captured_model_cwd != config.codex_cwd


def test_usage_limit_aborts_with_dedicated_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(manifest, [_manifest_row("case-1")])
    case = RUNNER.load_manifest(manifest).cases[0]
    config = _config(tmp_path, manifest)

    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(
            command,
            1,
            stdout="",
            stderr="quota exceeded",
        )

    monkeypatch.setattr(RUNNER.subprocess, "run", fake_run)

    with pytest.raises(RUNNER.UsageLimitError, match="usage limit"):
        RUNNER._invoke_codex_batch([case], RUNNER.PRIMARY_MODEL, config)


def test_resume_repairs_only_a_truncated_final_journal_line(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.jsonl"
    _write_manifest(manifest, [_manifest_row("case-1")])
    case = RUNNER.load_manifest(manifest).cases[0]
    path = tmp_path / "primary_results.jsonl"
    row = {
        "schema_version": RUNNER.SCHEMA_VERSION,
        "stage": RUNNER.PRIMARY_STAGE,
        "model": RUNNER.PRIMARY_MODEL,
        "case_id": case.case_id,
        "input_sha256": case.input_sha256,
        "batch_id": "batch",
        "verdict": "pass",
        "cleaning_correct": True,
        "rationale": "correct",
        "judged_at": "2026-07-27T00:00:00Z",
    }
    path.write_bytes((json.dumps(row) + "\n" + '{"partial":').encode())

    store = RUNNER.ResultStore(
        path,
        stage=RUNNER.PRIMARY_STAGE,
        model=RUNNER.PRIMARY_MODEL,
        cases_by_id={case.case_id: case},
    )

    assert store.results == {case.case_id: row}
    assert path.read_bytes().endswith(b"\n")
