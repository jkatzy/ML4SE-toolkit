from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


def load_module():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "comment_judge_validation_ledger.py"
    )
    spec = importlib.util.spec_from_file_location("comment_judge_validation_ledger", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ledger = load_module()


def test_ledger_round_trips_markdown_json_payload(tmp_path: Path) -> None:
    path = tmp_path / "ledger.md"
    version = ledger.CodeVersion(
        git_commit="abc123def456",
        fingerprint="f" * 64,
        relevant_paths=("src/example.py",),
    )
    entry = ledger.build_entry(
        language="Python",
        comment_kind="Line",
        status=ledger.PASSED,
        cases=10,
        version=version,
        judge_model="gpt-5.4-mini",
        manifest="tmp/manifest.jsonl",
        case_ids=("case-1", "case-2"),
    )

    ledger.upsert_entry(path, entry)

    text = path.read_text(encoding="utf-8")
    loaded = ledger.load_entries(path)
    assert ledger.LEDGER_START in text
    assert "## Passed Coverage" in text
    assert "python" in text
    assert loaded == [entry]


def test_upsert_replaces_same_language_kind_and_fingerprint(tmp_path: Path) -> None:
    path = tmp_path / "ledger.md"
    version = ledger.CodeVersion("abc", "f" * 64, ("src/example.py",))
    passed = ledger.build_entry(
        language="python",
        comment_kind="line",
        status=ledger.PASSED,
        cases=10,
        version=version,
        judge_model="codex-default",
    )
    failed = ledger.build_entry(
        language="python",
        comment_kind="line",
        status=ledger.FAILED,
        cases=1,
        version=version,
        judge_model="codex-default",
        report="tmp/reports/failure.md",
        failure_type="extraction",
        rationale="raw comment missing",
    )

    ledger.upsert_entry(path, passed)
    ledger.upsert_entry(path, failed)

    entries = ledger.load_entries(path)
    assert len(entries) == 1
    assert entries[0].status == ledger.FAILED
    assert entries[0].report == "tmp/reports/failure.md"
    assert "[failure.md](tmp/reports/failure.md)" in path.read_text(encoding="utf-8")


def test_find_entry_matches_current_code_fingerprint() -> None:
    current = ledger.JudgeLedgerEntry(
        language="python",
        comment_kind="line",
        status=ledger.PASSED,
        cases=10,
        code_fingerprint="current",
        git_commit="abc",
        judge_model="codex-default",
        updated_at="2026-05-25T10:00:00+00:00",
    )
    old = ledger.JudgeLedgerEntry(
        language="python",
        comment_kind="line",
        status=ledger.FAILED,
        cases=1,
        code_fingerprint="old",
        git_commit="def",
        judge_model="codex-default",
        updated_at="2026-05-24T10:00:00+00:00",
    )

    assert (
        ledger.find_entry(
            [old, current],
            language="Python",
            comment_kind="Line",
            code_fingerprint="current",
        )
        == current
    )


def test_current_code_version_requires_clean_committed_relevant_paths(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    (repo / "parser.py").write_text("print('ok')\n", encoding="utf-8")
    _git(repo, "add", "parser.py")
    _git(repo, "-c", "user.email=a@example.com", "-c", "user.name=A", "commit", "-m", "init")

    version = ledger.current_code_version(repo, ("parser.py",))

    assert version.git_commit
    assert len(version.fingerprint) == 64

    (repo / "parser.py").write_text("print('dirty')\n", encoding="utf-8")
    with pytest.raises(ledger.DirtyRelevantCodeError) as exc_info:
        ledger.current_code_version(repo, ("parser.py",))
    assert "parser.py" in str(exc_info.value)


def test_status_lines_compare_manifest_to_ledger(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ledger_path = tmp_path / "ledger.md"
    manifest_path = tmp_path / "manifest.jsonl"
    version = ledger.CodeVersion("abc", "f" * 64, ("parser.py",))
    entry = ledger.build_entry(
        language="python",
        comment_kind="line",
        status=ledger.PASSED,
        cases=1,
        version=version,
        judge_model="codex-default",
    )
    ledger.write_entries(ledger_path, [entry])
    monkeypatch.setattr(ledger, "current_code_version", lambda repo_root: version)
    manifest_path.write_text(
        '{"language":"python","comment_kind":"line","case_id":"py-1"}\n'
        '{"language":"java","comment_kind":"block","case_id":"java-1"}\n',
        encoding="utf-8",
    )

    lines = ledger.status_lines(
        ledger_path=ledger_path,
        repo_root=tmp_path,
        manifest_path=manifest_path,
    )

    assert "python/line: passed cases=1" in lines
    assert "java/block: untested cases=1" in lines


def _git(repo: Path, *args: str) -> None:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
