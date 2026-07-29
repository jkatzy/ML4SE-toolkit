from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import threading
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import pytest


def _load_pipeline_module() -> Any:
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "run_stack_v2_comment_manifest_pipeline.py"
    )
    spec = importlib.util.spec_from_file_location(
        "stack_v2_comment_manifest_pipeline",
        script_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


PIPELINE = _load_pipeline_module()


def _option_value(command: Sequence[str], option: str) -> str:
    index = command.index(option)
    return command[index + 1]


def _write_jsonl(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )


def _write_terminal_shard(
    command: Sequence[str],
    *,
    count: int,
    returned_language: str | None = None,
) -> None:
    requested_language = _option_value(command, "--languages")
    language = returned_language or requested_language
    shard_root = Path(_option_value(command, "--output-root"))
    quota = int(_option_value(command, "--files-per-language"))
    source_root = shard_root / "files"
    source_root.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    for index in range(count):
        source_file = (source_root / f"{language}-{index}.txt").resolve()
        source_file.write_text(f"// {language} comment {index}\n", encoding="utf-8")
        manifest_rows.append(
            {
                "case_id": f"{language}-case-{index}",
                "language": language,
                "comment_kind": "line",
                "source_id": f"{language}-source-{index}",
                "source_file": str(source_file),
            }
        )
    _write_jsonl(shard_root / "manifest.jsonl", manifest_rows)
    failure_path = shard_root / "failures.jsonl"
    if count == quota:
        if failure_path.exists():
            failure_path.unlink()
        return
    _write_jsonl(
        failure_path,
        [
            {
                "language": language,
                "comment_kind": "source_files",
                "expected_count": quota,
                "observed_count": count,
                "scanned_records": 123,
                "max_records_per_language": int(
                    _option_value(command, "--max-records-per-language")
                ),
                "reason": f"Only found {count}/{quota} source files.",
                "recommendation": "Review corpus coverage.",
            }
        ],
    )


def _fake_builder(
    outcomes: dict[str, int | str],
    calls: list[list[str]],
) -> Callable[[Sequence[str], Path, Path], subprocess.CompletedProcess[str]]:
    def run(
        command: Sequence[str],
        stdout_path: Path,
        stderr_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        command_list = list(command)
        calls.append(command_list)
        language = _option_value(command, "--languages")
        assert stdout_path.parent == Path(_option_value(command, "--output-root"))
        assert stderr_path.parent == stdout_path.parent
        outcome = outcomes[language]
        if outcome == "error":
            return subprocess.CompletedProcess(command_list, 7)
        assert isinstance(outcome, int)
        _write_terminal_shard(command_list, count=outcome)
        return subprocess.CompletedProcess(command_list, 0)

    return run


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def test_parse_args_requires_explicit_language_scope() -> None:
    with pytest.raises(SystemExit):
        PIPELINE.parse_args([])

    with pytest.raises(SystemExit):
        PIPELINE.parse_args(["--all-languages", "--languages", "java"])


def test_language_workers_default_and_validation() -> None:
    args = PIPELINE.parse_args(["--languages", "java"])
    assert args.language_workers == 1
    assert args.dataset_revision is None
    assert args.max_line_comment_chars == 12_000
    PIPELINE._validate_args(args)

    invalid = PIPELINE.parse_args(["--languages", "java", "--language-workers", "0"])
    with pytest.raises(SystemExit, match="--language-workers"):
        PIPELINE._validate_args(invalid)

    empty_revision = PIPELINE.parse_args(["--languages", "java", "--dataset-revision", ""])
    with pytest.raises(SystemExit, match="--dataset-revision"):
        PIPELINE._validate_args(empty_revision)

    negative_line_limit = PIPELINE.parse_args(
        ["--languages", "java", "--max-line-comment-chars", "-1"]
    )
    with pytest.raises(SystemExit, match="--max-line-comment-chars"):
        PIPELINE._validate_args(negative_line_limit)


def test_language_workers_do_not_change_per_shard_fingerprint(
    tmp_path: Path,
) -> None:
    source_fingerprint = {"digest": "source-digest"}
    first = PIPELINE.parse_args(
        [
            "--languages",
            "java",
            "--output-root",
            str(tmp_path),
            "--language-workers",
            "1",
        ]
    )
    second = PIPELINE.parse_args(
        [
            "--languages",
            "java",
            "--output-root",
            str(tmp_path),
            "--language-workers",
            "8",
        ]
    )
    PIPELINE._validate_args(first)
    PIPELINE._validate_args(second)
    shard_root = tmp_path / "languages" / "java"

    first_config = PIPELINE._language_config(first, "java", shard_root)
    second_config = PIPELINE._language_config(second, "java", shard_root)

    assert "language_workers" not in first_config
    assert first_config == second_config
    assert PIPELINE._config_fingerprint(
        first_config, source_fingerprint
    ) == PIPELINE._config_fingerprint(second_config, source_fingerprint)


def test_prefetch_tuning_does_not_change_shard_fingerprint(
    tmp_path: Path,
) -> None:
    source_fingerprint = {"digest": "source-digest"}
    first = PIPELINE.parse_args(
        [
            "--languages",
            "java",
            "--output-root",
            str(tmp_path),
            "--content-prefetch-workers",
            "8",
            "--content-prefetch-buffer-size",
            "64",
        ]
    )
    second = PIPELINE.parse_args(
        [
            "--languages",
            "java",
            "--output-root",
            str(tmp_path),
            "--content-prefetch-workers",
            "32",
            "--content-prefetch-buffer-size",
            "128",
        ]
    )
    PIPELINE._validate_args(first)
    PIPELINE._validate_args(second)
    shard_root = tmp_path / "languages" / "java"

    first_config = PIPELINE._language_config(first, "java", shard_root)
    second_config = PIPELINE._language_config(second, "java", shard_root)

    assert first_config != second_config
    assert PIPELINE._shard_config_fingerprint(
        first_config, source_fingerprint
    ) == PIPELINE._shard_config_fingerprint(second_config, source_fingerprint)
    assert PIPELINE._config_fingerprint(
        first_config, source_fingerprint
    ) != PIPELINE._config_fingerprint(second_config, source_fingerprint)


def test_python_executable_does_not_change_shard_fingerprint(
    tmp_path: Path,
) -> None:
    source_fingerprint = {"digest": "source-digest"}
    first_args = PIPELINE.parse_args(
        [
            "--languages",
            "java",
            "--output-root",
            str(tmp_path),
            "--python-executable",
            "/tmp/uv-a/python",
        ]
    )
    second_args = PIPELINE.parse_args(
        [
            "--languages",
            "java",
            "--output-root",
            str(tmp_path),
            "--python-executable",
            "/tmp/uv-b/python",
        ]
    )
    PIPELINE._validate_args(first_args)
    PIPELINE._validate_args(second_args)
    shard_root = tmp_path / "languages" / PIPELINE._safe_language_slug("java")
    first_config = PIPELINE._language_config(first_args, "java", shard_root)
    second_config = PIPELINE._language_config(second_args, "java", shard_root)

    assert PIPELINE._shard_config_fingerprint(
        first_config, source_fingerprint
    ) == PIPELINE._shard_config_fingerprint(second_config, source_fingerprint)
    assert PIPELINE._config_fingerprint(
        first_config, source_fingerprint
    ) != PIPELINE._config_fingerprint(second_config, source_fingerprint)


def test_builder_command_passes_quota_fetch_scan_and_prefetch_settings(
    tmp_path: Path,
) -> None:
    args = PIPELINE.parse_args(
        [
            "--languages",
            "java",
            "--output-root",
            str(tmp_path),
            "--files-per-language",
            "61",
            "--max-records-per-language",
            "4567",
            "--progress-every",
            "23",
            "--content-prefetch-workers",
            "9",
            "--content-prefetch-buffer-size",
            "77",
            "--max-content-chars",
            "765432",
            "--max-line-comment-chars",
            "23456",
            "--dataset-revision",
            "0123456789abcdef",
        ]
    )
    PIPELINE._validate_args(args)
    shard_root = tmp_path / "languages" / "java"

    command = PIPELINE._builder_command(args, "java", shard_root)

    assert _option_value(command, "--dataset") == "bigcode/the-stack-v2-dedup"
    assert _option_value(command, "--dataset-revision") == "0123456789abcdef"
    assert _option_value(command, "--languages") == "java"
    assert _option_value(command, "--files-per-language") == "61"
    assert _option_value(command, "--max-records-per-language") == "4567"
    assert _option_value(command, "--progress-every") == "23"
    assert _option_value(command, "--num-workers") == "1"
    assert _option_value(command, "--content-prefetch-workers") == "9"
    assert _option_value(command, "--content-prefetch-buffer-size") == "77"
    assert _option_value(command, "--max-content-chars") == "765432"
    assert _option_value(command, "--max-line-comment-chars") == "23456"
    assert _option_value(command, "--output-root") == str(shard_root.resolve())
    assert "--fetch-stack-v2-content" in command


def test_dataset_revision_is_fingerprinted_and_invalidates_completed_shard(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": 1}, calls),
    )
    common_argv = [
        "--languages",
        "java",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "1",
        "--no-progress",
    ]

    assert PIPELINE.main([*common_argv, "--dataset-revision", "revision-a"]) == 0
    first_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    first_fingerprint = first_status["languages"][0]["fingerprint"]
    assert _option_value(calls[0], "--dataset-revision") == "revision-a"
    assert first_status["config"]["dataset_revision"] == "revision-a"

    calls.clear()
    assert PIPELINE.main([*common_argv, "--dataset-revision", "revision-a"]) == 0
    assert calls == []

    assert PIPELINE.main([*common_argv, "--dataset-revision", "revision-b"]) == 0
    second_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    assert [_option_value(command, "--dataset-revision") for command in calls] == ["revision-b"]
    assert second_status["config"]["dataset_revision"] == "revision-b"
    assert second_status["languages"][0]["fingerprint"] != first_fingerprint


def test_line_comment_limit_is_fingerprinted_and_invalidates_completed_shard(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": 1}, calls),
    )
    common_argv = [
        "--languages",
        "java",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "1",
        "--no-progress",
    ]

    assert PIPELINE.main([*common_argv, "--max-line-comment-chars", "12000"]) == 0
    first_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    first_fingerprint = first_status["languages"][0]["fingerprint"]
    assert _option_value(calls[0], "--max-line-comment-chars") == "12000"
    assert first_status["config"]["max_line_comment_chars"] == 12_000

    calls.clear()
    assert PIPELINE.main([*common_argv, "--max-line-comment-chars", "12000"]) == 0
    assert calls == []

    assert PIPELINE.main([*common_argv, "--max-line-comment-chars", "0"]) == 0
    second_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    assert [_option_value(command, "--max-line-comment-chars") for command in calls] == ["0"]
    assert second_status["config"]["max_line_comment_chars"] == 0
    assert second_status["languages"][0]["fingerprint"] != first_fingerprint


@pytest.mark.parametrize(
    ("language", "dataset_config"),
    [
        ("hyphy", "HyPhy"),
        ("purescript", "PureScript"),
    ],
)
def test_default_dataset_uses_exact_config_override_and_resumes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    language: str,
    dataset_config: str,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({language: 1}, calls),
    )
    argv = [
        "--languages",
        language,
        "--output-root",
        str(output_root),
        "--files-per-language",
        "1",
        "--no-progress",
    ]

    assert PIPELINE.main(argv) == 0
    assert _option_value(calls[0], "--dataset-config") == dataset_config
    status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    shard_status = json.loads(
        Path(status["languages"][0]["shard"], "status.json").read_text(encoding="utf-8")
    )
    assert shard_status["config"]["dataset_config"] == dataset_config
    assert _option_value(shard_status["command"], "--dataset-config") == dataset_config
    assert shard_status["fingerprint"] == PIPELINE._shard_config_fingerprint(
        shard_status["config"],
        shard_status["source_fingerprint"],
    )

    calls.clear()
    assert PIPELINE.main(argv) == 0
    assert calls == []


@pytest.mark.parametrize("language", ["hyphy", "purescript"])
def test_explicit_dataset_config_wins_over_default_override(
    tmp_path: Path,
    language: str,
) -> None:
    args = PIPELINE.parse_args(
        [
            "--languages",
            language,
            "--output-root",
            str(tmp_path),
            "--dataset-config",
            "ExplicitDatasetConfig",
        ]
    )
    PIPELINE._validate_args(args)
    shard_root = tmp_path / "languages" / PIPELINE._safe_language_slug(language)

    config = PIPELINE._language_config(args, language, shard_root)
    command = PIPELINE._builder_command(args, language, shard_root)

    assert config["dataset_config"] == "ExplicitDatasetConfig"
    assert _option_value(command, "--dataset-config") == "ExplicitDatasetConfig"


@pytest.mark.parametrize("language", ["hyphy", "purescript"])
def test_default_config_override_is_not_applied_to_another_dataset(
    tmp_path: Path,
    language: str,
) -> None:
    args = PIPELINE.parse_args(
        [
            "--languages",
            language,
            "--dataset",
            "example/custom-code-dataset",
            "--output-root",
            str(tmp_path),
        ]
    )
    PIPELINE._validate_args(args)
    shard_root = tmp_path / "languages" / PIPELINE._safe_language_slug(language)

    config = PIPELINE._language_config(args, language, shard_root)
    command = PIPELINE._builder_command(args, language, shard_root)

    assert config["dataset_config"] is None
    assert "--dataset-config" not in command


def test_default_dataset_config_override_does_not_change_other_languages(
    tmp_path: Path,
) -> None:
    args = PIPELINE.parse_args(
        [
            "--languages",
            "java",
            "--output-root",
            str(tmp_path),
        ]
    )
    PIPELINE._validate_args(args)
    shard_root = tmp_path / "languages" / PIPELINE._safe_language_slug("java")

    config = PIPELINE._language_config(args, "java", shard_root)
    command = PIPELINE._builder_command(args, "java", shard_root)

    assert config == {
        **PIPELINE._common_config(args),
        "language": "java",
        "output_root": str(shard_root.resolve()),
    }
    assert "--dataset-config" not in command


def test_pipeline_resumes_success_and_explicit_shortfall_deterministically(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": 2, "python": 1}, calls),
    )
    argv = [
        "--languages",
        "java,python",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "2",
        "--no-progress",
    ]

    assert PIPELINE.main(argv) == 0
    assert [_option_value(command, "--languages") for command in calls] == [
        "java",
        "python",
    ]
    manifest_rows = _read_jsonl(output_root / "manifest.jsonl")
    failure_rows = _read_jsonl(output_root / "failures.jsonl")
    status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    assert [row["language"] for row in manifest_rows] == ["java", "java", "python"]
    assert [(row["language"], row["comment_kind"]) for row in failure_rows] == [
        ("python", "source_files")
    ]
    assert [entry["status"] for entry in status["languages"]] == [
        "success",
        "source_files_shortfall",
    ]
    assert status["summary"] == {
        "language_count": 2,
        "success_count": 1,
        "source_files_shortfall_count": 1,
        "error_count": 0,
        "manifest_count": 3,
        "failure_count": 1,
    }

    aggregate_before = {
        name: (output_root / name).read_bytes()
        for name in ("manifest.jsonl", "failures.jsonl", "status.json")
    }
    shard_status_before = {
        entry["language"]: Path(entry["shard"], "status.json").read_bytes()
        for entry in status["languages"]
    }
    calls.clear()

    assert PIPELINE.main(argv) == 0
    assert calls == []
    assert {
        name: (output_root / name).read_bytes()
        for name in ("manifest.jsonl", "failures.jsonl", "status.json")
    } == aggregate_before
    assert {
        entry["language"]: Path(entry["shard"], "status.json").read_bytes()
        for entry in status["languages"]
    } == shard_status_before


def test_operational_collection_failure_is_error_and_not_resumable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []

    def operational_then_success(
        command: Sequence[str],
        stdout_path: Path,
        stderr_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        command_list = list(command)
        calls.append(command_list)
        _write_terminal_shard(
            command_list,
            count=0 if len(calls) == 1 else 1,
        )
        if len(calls) == 1:
            failure_path = Path(_option_value(command_list, "--output-root")) / "failures.jsonl"
            failure = _read_jsonl(failure_path)[0]
            failure.update(
                {
                    "reason": (
                        "Could not finish collecting distinct source files for java: "
                        "endpoint unavailable. Found 0/1 before aborting."
                    ),
                    "recommendation": (
                        "Resolve the corpus access or streaming error and rerun the "
                        "manifest builder for this language."
                    ),
                }
            )
            _write_jsonl(failure_path, [failure])
        return subprocess.CompletedProcess(command_list, 0)

    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        operational_then_success,
    )
    argv = [
        "--languages",
        "java",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "1",
        "--no-progress",
    ]

    assert PIPELINE.main(argv) == 1
    shard_root = output_root / "languages" / PIPELINE._safe_language_slug("java")
    shard_status_path = shard_root / "status.json"
    shard_status = json.loads(shard_status_path.read_text(encoding="utf-8"))
    assert shard_status["status"] == "error"
    assert "operational corpus collection error" in shard_status["error"]

    # Emulate a status written by the buggy orchestrator. The operational
    # failure row itself must still invalidate this otherwise-matching shard.
    shard_status["status"] = "source_files_shortfall"
    shard_status["failure_count"] = 1
    shard_status.pop("error")
    shard_status_path.write_text(
        json.dumps(shard_status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    assert PIPELINE.main(argv) == 0
    assert len(calls) == 2
    final_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    assert final_status["languages"][0]["status"] == "success"


def test_genuine_source_file_shortfall_remains_resumable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": 0}, calls),
    )
    argv = [
        "--languages",
        "java",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "1",
        "--no-progress",
    ]

    assert PIPELINE.main(argv) == 0
    assert PIPELINE.main(argv) == 0
    assert len(calls) == 1
    status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    assert status["languages"][0]["status"] == "source_files_shortfall"


def test_49_of_50_clean_source_file_shortfall_is_accepted(
    tmp_path: Path,
) -> None:
    args = PIPELINE.parse_args(
        [
            "--languages",
            "java",
            "--output-root",
            str(tmp_path),
            "--files-per-language",
            "50",
        ]
    )
    PIPELINE._validate_args(args)
    shard_root = tmp_path / "languages" / PIPELINE._safe_language_slug("java")
    command = PIPELINE._builder_command(args, "java", shard_root)
    _write_terminal_shard(command, count=49)
    (shard_root / "stderr.log").write_text(
        "prefix [stack-v2 manifest] language=java skipped-content "
        "record=12 error=not-an-exact-marker\n"
        "[stack-v2 manifest] language=python skipped-content "
        "record=12 error=wrong-language\n"
        "[stack-v2 manifest] language=java skipped-content "
        "record=not-an-integer error=wrong-record\n",
        encoding="utf-8",
    )

    status, manifest_rows, failure_rows = PIPELINE._validate_shard_outputs(
        shard_root,
        language="java",
        quota=50,
    )

    assert status == "source_files_shortfall"
    assert len(manifest_rows) == 49
    assert len(failure_rows) == 1


def test_49_of_50_shortfall_with_skipped_content_is_error_and_not_resumable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []

    def tainted_alias_builder(
        command: Sequence[str],
        stdout_path: Path,
        stderr_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        command_list = list(command)
        calls.append(command_list)
        _write_terminal_shard(
            command_list,
            count=49,
            returned_language="c#",
        )
        stderr_path.write_text(
            "[stack-v2 manifest] language=c# skipped-content "
            "record=123 error=transient content fetch failure\n",
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command_list, 0)

    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        tainted_alias_builder,
    )
    argv = [
        "--languages",
        "c_sharp",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "50",
        "--no-progress",
    ]

    assert PIPELINE.main(argv) == 1
    shard_root = output_root / "languages" / PIPELINE._safe_language_slug("c_sharp")
    first_status = json.loads((shard_root / "status.json").read_text(encoding="utf-8"))
    assert first_status["status"] == "error"
    assert "skipped-content records" in first_status["error"]

    assert PIPELINE.main(argv) == 1
    assert len(calls) == 2


def test_50_of_50_with_skipped_content_is_success_and_resumable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []

    def complete_tainted_builder(
        command: Sequence[str],
        stdout_path: Path,
        stderr_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        command_list = list(command)
        calls.append(command_list)
        _write_terminal_shard(command_list, count=50)
        stderr_path.write_text(
            "[stack-v2 manifest] language=java skipped-content "
            "record=123 error=transient content fetch failure\n",
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command_list, 0)

    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        complete_tainted_builder,
    )
    argv = [
        "--languages",
        "java",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "50",
        "--no-progress",
    ]

    assert PIPELINE.main(argv) == 0
    assert PIPELINE.main(argv) == 0
    assert len(calls) == 1
    status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    assert status["languages"][0]["status"] == "success"
    assert status["languages"][0]["manifest_count"] == 50


def test_pipeline_restores_requested_alias_and_makes_case_ids_unique(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []

    def normalized_builder(
        command: Sequence[str],
        stdout_path: Path,
        stderr_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        command_list = list(command)
        calls.append(command_list)
        requested_language = _option_value(command_list, "--languages")
        count = 2 if requested_language == "c#" else 1
        _write_terminal_shard(
            command_list,
            count=count,
            returned_language="c#",
        )
        return subprocess.CompletedProcess(command_list, 0)

    monkeypatch.setattr(PIPELINE, "_run_builder_process", normalized_builder)
    argv = [
        "--languages",
        "c#,c_sharp",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "2",
        "--no-progress",
    ]

    assert PIPELINE.main(argv) == 0
    manifest_rows = _read_jsonl(output_root / "manifest.jsonl")
    failure_rows = _read_jsonl(output_root / "failures.jsonl")
    assert [row["language"] for row in manifest_rows] == ["c#", "c#", "c_sharp"]
    assert len({row["case_id"] for row in manifest_rows}) == 3
    alias_row = next(row for row in manifest_rows if row["language"] == "c_sharp")
    assert alias_row["case_id"] == PIPELINE._alias_unique_case_id(
        "c#-case-0",
        "c_sharp",
    )
    assert [row["language"] for row in failure_rows] == ["c_sharp"]

    alias_shard = output_root / "languages" / PIPELINE._safe_language_slug("c_sharp")
    assert _read_jsonl(alias_shard / "manifest.jsonl")[0] == {
        **alias_row,
        "case_id": "c#-case-0",
        "language": "c#",
    }
    assert _read_jsonl(alias_shard / "failures.jsonl")[0]["language"] == "c#"

    aggregate_before = {
        name: (output_root / name).read_bytes()
        for name in ("manifest.jsonl", "failures.jsonl", "status.json")
    }
    calls.clear()
    assert PIPELINE.main(argv) == 0
    assert calls == []
    assert {
        name: (output_root / name).read_bytes()
        for name in ("manifest.jsonl", "failures.jsonl", "status.json")
    } == aggregate_before


def test_shard_validation_rejects_unrelated_returned_language(
    tmp_path: Path,
) -> None:
    args = PIPELINE.parse_args(
        [
            "--languages",
            "c_sharp",
            "--output-root",
            str(tmp_path),
            "--files-per-language",
            "1",
        ]
    )
    PIPELINE._validate_args(args)
    shard_root = tmp_path / "languages" / PIPELINE._safe_language_slug("c_sharp")
    command = PIPELINE._builder_command(args, "c_sharp", shard_root)
    _write_terminal_shard(command, count=1, returned_language="python")

    with pytest.raises(
        PIPELINE.ShardValidationError,
        match="does not share comment syntax",
    ):
        PIPELINE._validate_shard_outputs(
            shard_root,
            language="c_sharp",
            quota=1,
        )


def test_changing_language_workers_reuses_completed_shards(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": 1, "python": 1}, calls),
    )
    common_argv = [
        "--languages",
        "java,python",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "1",
        "--no-progress",
    ]

    assert PIPELINE.main([*common_argv, "--language-workers", "1"]) == 0
    first_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    first_fingerprints = {
        entry["language"]: entry["fingerprint"] for entry in first_status["languages"]
    }
    calls.clear()

    assert PIPELINE.main([*common_argv, "--language-workers", "2"]) == 0
    second_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))

    assert calls == []
    assert {
        entry["language"]: entry["fingerprint"] for entry in second_status["languages"]
    } == first_fingerprints
    assert second_status["config"]["language_workers"] == 2
    assert [row["language"] for row in _read_jsonl(output_root / "manifest.jsonl")] == [
        "java",
        "python",
    ]


def test_changing_prefetch_tuning_reuses_completed_shards(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": 1}, calls),
    )
    common_argv = [
        "--languages",
        "java",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "1",
        "--no-progress",
    ]

    assert (
        PIPELINE.main(
            [
                *common_argv,
                "--content-prefetch-workers",
                "8",
                "--content-prefetch-buffer-size",
                "64",
            ]
        )
        == 0
    )
    first_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    first_fingerprint = first_status["languages"][0]["fingerprint"]
    shard_status_path = Path(first_status["languages"][0]["shard"]) / "status.json"
    shard_status = json.loads(shard_status_path.read_text(encoding="utf-8"))
    legacy_fingerprint = PIPELINE._config_fingerprint(
        shard_status["config"],
        shard_status["source_fingerprint"],
    )
    assert legacy_fingerprint != first_fingerprint
    shard_status["fingerprint"] = legacy_fingerprint
    shard_status_path.write_text(
        json.dumps(shard_status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    calls.clear()

    assert (
        PIPELINE.main(
            [
                *common_argv,
                "--content-prefetch-buffer-size",
                "128",
                "--content-prefetch-workers",
                "32",
            ]
        )
        == 0
    )
    second_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))

    assert calls == []
    assert second_status["languages"][0]["fingerprint"] == first_fingerprint
    assert second_status["config"]["content_prefetch_workers"] == 32
    assert second_status["config"]["content_prefetch_buffer_size"] == 128
    migrated_shard_status = json.loads(shard_status_path.read_text(encoding="utf-8"))
    assert migrated_shard_status["fingerprint"] == first_fingerprint
    assert migrated_shard_status["config"]["content_prefetch_workers"] == 8
    assert migrated_shard_status["config"]["content_prefetch_buffer_size"] == 64


def test_semantic_setting_still_invalidates_prefetch_normalized_shard(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": 1}, calls),
    )
    common_argv = [
        "--languages",
        "java",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "1",
        "--no-progress",
    ]

    assert PIPELINE.main([*common_argv, "--context-chars", "1200"]) == 0
    calls.clear()

    assert (
        PIPELINE.main(
            [
                *common_argv,
                "--context-chars",
                "2400",
                "--content-prefetch-workers",
                "32",
                "--content-prefetch-buffer-size",
                "128",
            ]
        )
        == 0
    )

    assert [_option_value(command, "--languages") for command in calls] == ["java"]


def test_changing_ephemeral_python_path_reuses_completed_shards(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": 1}, calls),
    )
    common_argv = [
        "--languages",
        "java",
        "--output-root",
        str(output_root),
        "--files-per-language",
        "1",
        "--no-progress",
    ]

    assert PIPELINE.main([*common_argv, "--python-executable", "/tmp/uv-a/python"]) == 0
    first_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    first_fingerprint = first_status["languages"][0]["fingerprint"]
    shard_status_path = Path(first_status["languages"][0]["shard"]) / "status.json"
    shard_status = json.loads(shard_status_path.read_text(encoding="utf-8"))
    legacy_fingerprint = PIPELINE._config_fingerprint(
        shard_status["config"],
        shard_status["source_fingerprint"],
    )
    assert legacy_fingerprint != first_fingerprint
    shard_status["fingerprint"] = legacy_fingerprint
    shard_status_path.write_text(
        json.dumps(shard_status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    calls.clear()

    assert PIPELINE.main([*common_argv, "--python-executable", "/tmp/uv-b/python"]) == 0
    assert calls == []
    second_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    assert second_status["languages"][0]["fingerprint"] == first_fingerprint
    assert second_status["config"]["python_executable"] == "/tmp/uv-b/python"
    migrated_shard_status = json.loads(shard_status_path.read_text(encoding="utf-8"))
    assert migrated_shard_status["fingerprint"] == first_fingerprint
    assert migrated_shard_status["config"]["python_executable"] == "/tmp/uv-a/python"
    assert migrated_shard_status["command"][0] == "/tmp/uv-a/python"


def test_concurrent_languages_continue_errors_and_aggregate_in_request_order(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    rendezvous = threading.Barrier(2)
    python_finished = threading.Event()
    active_lock = threading.Lock()
    active_count = 0
    max_active_count = 0

    def concurrent_builder(
        command: Sequence[str],
        stdout_path: Path,
        stderr_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        nonlocal active_count, max_active_count
        command_list = list(command)
        language = _option_value(command_list, "--languages")
        with active_lock:
            active_count += 1
            max_active_count = max(max_active_count, active_count)
        try:
            if language == "ruby":
                return subprocess.CompletedProcess(command_list, 7)
            rendezvous.wait(timeout=5)
            if language == "java":
                assert python_finished.wait(timeout=5)
            _write_terminal_shard(command_list, count=1)
            if language == "python":
                python_finished.set()
            return subprocess.CompletedProcess(command_list, 0)
        finally:
            with active_lock:
                active_count -= 1

    monkeypatch.setattr(PIPELINE, "_run_builder_process", concurrent_builder)

    return_code = PIPELINE.main(
        [
            "--languages",
            "java,ruby,python",
            "--output-root",
            str(output_root),
            "--files-per-language",
            "1",
            "--language-workers",
            "3",
            "--no-progress",
        ]
    )

    assert return_code == 1
    assert max_active_count >= 2
    assert [row["language"] for row in _read_jsonl(output_root / "manifest.jsonl")] == [
        "java",
        "python",
    ]
    status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    assert [entry["language"] for entry in status["languages"]] == [
        "java",
        "ruby",
        "python",
    ]
    assert [entry["status"] for entry in status["languages"]] == [
        "success",
        "error",
        "success",
    ]
    assert status["summary"]["error_count"] == 1


def test_config_fingerprint_mismatch_reruns_terminal_shard(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    outcomes = {"java": 2}
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder(outcomes, calls),
    )

    assert (
        PIPELINE.main(
            [
                "--languages",
                "java",
                "--output-root",
                str(output_root),
                "--files-per-language",
                "2",
                "--no-progress",
            ]
        )
        == 0
    )
    first_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    first_fingerprint = first_status["languages"][0]["fingerprint"]

    calls.clear()
    outcomes["java"] = 3
    assert (
        PIPELINE.main(
            [
                "--languages",
                "java",
                "--output-root",
                str(output_root),
                "--files-per-language",
                "3",
                "--no-progress",
            ]
        )
        == 0
    )
    second_status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))

    assert [_option_value(command, "--languages") for command in calls] == ["java"]
    assert second_status["languages"][0]["fingerprint"] != first_fingerprint
    assert second_status["languages"][0]["manifest_count"] == 3


def test_pipeline_continues_after_language_error_and_aggregates_later_shards(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": "error", "python": 1, "ruby": 0}, calls),
    )

    return_code = PIPELINE.main(
        [
            "--languages",
            "java,python,ruby",
            "--output-root",
            str(output_root),
            "--files-per-language",
            "1",
            "--no-progress",
        ]
    )

    assert return_code == 1
    assert [_option_value(command, "--languages") for command in calls] == [
        "java",
        "python",
        "ruby",
    ]
    assert [row["language"] for row in _read_jsonl(output_root / "manifest.jsonl")] == ["python"]
    assert [
        (row["language"], row["comment_kind"])
        for row in _read_jsonl(output_root / "failures.jsonl")
    ] == [("ruby", "source_files")]
    status = json.loads((output_root / "status.json").read_text(encoding="utf-8"))
    assert status["status"] == "error"
    assert [entry["status"] for entry in status["languages"]] == [
        "error",
        "success",
        "source_files_shortfall",
    ]
    assert status["summary"]["error_count"] == 1
    assert status["summary"]["manifest_count"] == 1
    assert status["summary"]["failure_count"] == 1


def test_all_languages_uses_every_registry_key(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_root = tmp_path / "pipeline"
    calls: list[list[str]] = []
    monkeypatch.setattr(
        PIPELINE,
        "get_supported_comment_languages",
        lambda: ["java", "python"],
    )
    monkeypatch.setattr(
        PIPELINE,
        "_run_builder_process",
        _fake_builder({"java": 1, "python": 1}, calls),
    )

    assert (
        PIPELINE.main(
            [
                "--all-languages",
                "--output-root",
                str(output_root),
                "--files-per-language",
                "1",
                "--no-progress",
            ]
        )
        == 0
    )
    assert [_option_value(command, "--languages") for command in calls] == [
        "java",
        "python",
    ]
