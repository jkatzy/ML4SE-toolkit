from __future__ import annotations

import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PIPELINE = PROJECT_ROOT / "scripts" / "run_stack_v2_comment_judge_pipeline.sh"


def _install_fake_make(tmp_path: Path) -> tuple[Path, Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    call_log = tmp_path / "make-calls.tsv"
    fake_make = bin_dir / "make"
    fake_make.write_text(
        """#!/usr/bin/env bash
set -euo pipefail

target="${1:?target}"
printf '%s\\t%s\\t%s\\t%s\\n' \\
  "${target}" \\
  "${COMMENT_JUDGE_LANGUAGES:-}" \\
  "${COMMENT_JUDGE_OUTPUT_ROOT:-}" \\
  "${COMMENT_JUDGE_REPORT_DIR:-}" >> "${CALL_LOG}"

case "${target}" in
  comment-judge-manifest)
    mkdir -p \\
      "${COMMENT_JUDGE_OUTPUT_ROOT}" \\
      "$(dirname "${COMMENT_JUDGE_MANIFEST}")" \\
      "$(dirname "${COMMENT_JUDGE_FAILURES}")"
    printf '{"language":"%s","comment_kind":"line"}\\n' \\
      "${COMMENT_JUDGE_LANGUAGES}" > "${COMMENT_JUDGE_MANIFEST}"
    : > "${COMMENT_JUDGE_FAILURES}"
    ;;
  comment-judge-test)
    if [[ "${COMMENT_JUDGE_LANGUAGES}" == "${FAIL_LANGUAGE:-}" ]]; then
      mkdir -p "${COMMENT_JUDGE_REPORT_DIR}"
      printf '# failure for %s\\n' "${COMMENT_JUDGE_LANGUAGES}" \\
        > "${COMMENT_JUDGE_REPORT_DIR}/${COMMENT_JUDGE_LANGUAGES}.md"
      exit 7
    fi
    ;;
  comment-judge-generate-tests)
    ;;
  *)
    echo "unexpected make target: ${target}" >&2
    exit 99
    ;;
esac
""",
        encoding="utf-8",
    )
    fake_make.chmod(0o755)
    return bin_dir, call_log


def _pipeline_env(tmp_path: Path, bin_dir: Path, call_log: Path) -> dict[str, str]:
    output_root = tmp_path / "out"
    env = os.environ.copy()
    env.update(
        {
            "CALL_LOG": str(call_log),
            "COMMENT_JUDGE_FAILURES": str(output_root / "failures.jsonl"),
            "COMMENT_JUDGE_LANGUAGE_COUNT": "",
            "COMMENT_JUDGE_LANGUAGES": "python,java,coffeescript",
            "COMMENT_JUDGE_LEDGER": "0",
            "COMMENT_JUDGE_MANIFEST": str(output_root / "manifest.jsonl"),
            "COMMENT_JUDGE_OUTPUT_ROOT": str(output_root),
            "COMMENT_JUDGE_PIPELINE_RESUME": "1",
            "COMMENT_JUDGE_REPORT_DIR": str(output_root / "reports"),
            "PATH": f"{bin_dir}{os.pathsep}{env['PATH']}",
            "RUN_TESTGEN": "0",
        }
    )
    return env


def test_stack_v2_comment_judge_pipeline_keeps_later_languages_after_failure(
    tmp_path: Path,
) -> None:
    bin_dir, call_log = _install_fake_make(tmp_path)
    env = _pipeline_env(tmp_path, bin_dir, call_log)
    env["COMMENT_JUDGE_PIPELINE_RESUME"] = "0"
    env["FAIL_LANGUAGE"] = "java"

    result = subprocess.run(
        ["bash", str(PIPELINE)],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1, result.stdout + result.stderr
    assert (tmp_path / "out" / "languages" / "python" / "manifest.jsonl").exists()
    assert (tmp_path / "out" / "languages" / "java" / "manifest.jsonl").exists()
    assert (
        tmp_path / "out" / "languages" / "coffeescript" / "manifest.jsonl"
    ).exists()
    assert (tmp_path / "out" / "reports" / "java.md").exists()

    aggregate_rows = (tmp_path / "out" / "manifest.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    assert len(aggregate_rows) == 3
    assert '"language":"coffeescript"' in aggregate_rows[-1]

    status = (tmp_path / "out" / "pipeline_status.tsv").read_text(encoding="utf-8")
    assert "\tpassed\t0\t0\tskipped\t" in status
    assert "java\tjudge_failed\t0\t7\tskipped\t" in status
    assert "coffeescript\tpassed\t0\t0\tskipped\t" in status

    calls = call_log.read_text(encoding="utf-8")
    assert "comment-judge-test\tcoffeescript\t" in calls


def test_stack_v2_comment_judge_pipeline_skips_saved_passes(tmp_path: Path) -> None:
    bin_dir, call_log = _install_fake_make(tmp_path)
    env = _pipeline_env(tmp_path, bin_dir, call_log)
    env["COMMENT_JUDGE_LANGUAGES"] = "python,java"

    saved_root = tmp_path / "out" / "languages" / "python"
    saved_root.mkdir(parents=True)
    (saved_root / "manifest.jsonl").write_text(
        '{"language":"python","comment_kind":"line"}\n',
        encoding="utf-8",
    )
    (saved_root / "pipeline.status").write_text("status=passed\n", encoding="utf-8")

    result = subprocess.run(
        ["bash", str(PIPELINE)],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    calls = call_log.read_text(encoding="utf-8")
    assert "comment-judge-manifest\tpython\t" not in calls
    assert "comment-judge-test\tpython\t" not in calls
    assert "comment-judge-test\tjava\t" in calls

    aggregate = (tmp_path / "out" / "manifest.jsonl").read_text(encoding="utf-8")
    assert '"language":"python"' in aggregate
    assert '"language":"java"' in aggregate

    status = (tmp_path / "out" / "pipeline_status.tsv").read_text(encoding="utf-8")
    assert "python\tskipped\t0\t0\tskipped\t" in status
