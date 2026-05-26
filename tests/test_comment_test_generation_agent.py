from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


def _load_script():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "run_codex_comment_test_generator.py"
    )
    spec = importlib.util.spec_from_file_location("comment_test_generator", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_discover_reports_uses_sorted_report_dir(tmp_path: Path) -> None:
    module = _load_script()
    (tmp_path / "b.md").write_text("b", encoding="utf-8")
    (tmp_path / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "ignore.txt").write_text("ignore", encoding="utf-8")

    reports = module.discover_reports(tmp_path, [], None)

    assert [report.name for report in reports] == ["a.md", "b.md"]


def test_discover_reports_respects_explicit_reports_and_limit(tmp_path: Path) -> None:
    module = _load_script()
    first = tmp_path / "first.md"
    second = tmp_path / "second.md"
    missing = tmp_path / "missing.md"
    first.write_text("first", encoding="utf-8")
    second.write_text("second", encoding="utf-8")

    reports = module.discover_reports(tmp_path, [second, missing, first], 1)

    assert reports == [second]


def test_prompt_stops_at_deterministic_test_generation() -> None:
    module = _load_script()

    prompt = module.build_test_generation_prompt(
        Path("tmp/report.md"),
        "## Expected Behavior\nraw comment\n## Actual Behavior\nmissing comment",
    )

    assert "Do not implement the parser" in prompt
    assert "Do not modify production code under src/" in prompt
    assert "Do not add another LLM-as-judge assertion" in prompt
    assert "Use Expected Behavior as the assertion target" in prompt
    assert "raw comment" in prompt
    assert "missing comment" in prompt


def test_manifest_generation_reports_are_not_testgen_inputs(tmp_path: Path) -> None:
    module = _load_script()
    report_text = """# Stack v2 Comment Judge Failure Report

- Failure type: `manifest_generation`
- Language: `coffeescript`
- Comment kind: `block`
"""

    assert module.is_manifest_generation_report(report_text)
    try:
        module.build_test_generation_prompt(tmp_path / "report.md", report_text)
    except ValueError as exc:
        assert "feature request" in str(exc)
    else:
        raise AssertionError("manifest-generation report should not build a testgen prompt")


def test_run_report_skips_manifest_generation_without_codex(
    tmp_path: Path, monkeypatch: object
) -> None:
    module = _load_script()
    report = tmp_path / "manifest.md"
    report.write_text(
        "- Failure type: `manifest_generation`\n- Language: `coffeescript`\n",
        encoding="utf-8",
    )

    class Args:
        codex_bin = "codex"
        codex_sandbox = "read-only"
        cwd = tmp_path
        model = None
        profile = None
        timeout = 10

    def fail_run(*args, **kwargs):
        raise AssertionError("Codex should not run for manifest-generation reports")

    monkeypatch.setattr(module.subprocess, "run", fail_run)

    assert module.run_report(Args(), report) == 0


def test_codex_command_uses_configured_sandbox(tmp_path: Path) -> None:
    module = _load_script()

    class Args:
        codex_bin = "codex"
        codex_sandbox = "danger-full-access"
        cwd = tmp_path
        model = None
        profile = None

    command = module.codex_command(Args(), tmp_path / "last.txt")

    assert command[command.index("--sandbox") + 1] == "danger-full-access"


def test_testgen_usage_limit_returns_special_exit(
    tmp_path: Path, monkeypatch: object
) -> None:
    module = _load_script()
    report = tmp_path / "report.md"
    report.write_text("# report", encoding="utf-8")
    monkeypatch.setenv("COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE", "92")

    class Args:
        codex_bin = "codex"
        codex_sandbox = "read-only"
        cwd = tmp_path
        model = None
        profile = None
        timeout = 10

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args[0],
            1,
            stdout="",
            stderr="Usage limit reached for this account.",
        )

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    assert module.run_report(Args(), report) == 92
