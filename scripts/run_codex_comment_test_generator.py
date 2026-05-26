"""Turn Stack v2 comment judge reports into deterministic pytest tests.

This script is the second half of the optional judge workflow. The judge suite
writes Markdown reports for failing cases; this runner hands those reports to a
Codex agent whose scope is limited to generating normal pytest coverage. It does
not ask the agent to fix parser, registry, or sanitizer behavior.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from comment_judge_limits import (  # noqa: E402
    looks_like_usage_limit,
    normalize_output,
    usage_limit_exit_code,
)

DEFAULT_REPORT_DIR = Path("tmp/stack_v2_comment_judge/reports")


def parse_args() -> argparse.Namespace:
    """Parse command-line options for the test-generation runner."""

    parser = argparse.ArgumentParser(
        description="Run Codex test-generation agents for comment judge reports."
    )
    parser.add_argument(
        "reports",
        nargs="*",
        type=Path,
        help="Specific report Markdown files to process. Defaults to all reports.",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(os.environ.get("COMMENT_JUDGE_REPORT_DIR", DEFAULT_REPORT_DIR)),
        help="Directory containing judge failure reports when reports are not passed.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=_optional_int(os.environ.get("COMMENT_TESTGEN_REPORT_LIMIT")),
        help="Maximum number of reports to process.",
    )
    parser.add_argument(
        "--codex-bin",
        default=os.environ.get("CODEX_BIN", "codex"),
        help="Codex executable to run.",
    )
    parser.add_argument(
        "--cwd",
        type=Path,
        default=Path(os.environ.get("COMMENT_TESTGEN_CODEX_CWD", os.getcwd())),
        help="Repository root for Codex.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("COMMENT_TESTGEN_CODEX_MODEL")
        or os.environ.get("COMMENT_JUDGE_CODEX_MODEL"),
        help="Optional Codex model override for test generation.",
    )
    parser.add_argument(
        "--profile",
        default=os.environ.get("COMMENT_TESTGEN_CODEX_PROFILE")
        or os.environ.get("COMMENT_JUDGE_CODEX_PROFILE"),
        help="Optional Codex config profile.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("COMMENT_TESTGEN_CODEX_TIMEOUT", "600")),
        help="Timeout per Codex test-generation agent in seconds.",
    )
    parser.add_argument(
        "--codex-sandbox",
        choices=("read-only", "workspace-write", "danger-full-access"),
        default=os.environ.get("COMMENT_TESTGEN_CODEX_SANDBOX", "workspace-write"),
        help="Codex sandbox mode for the test-generation agent.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print reports that would be processed without launching Codex.",
    )
    return parser.parse_args()


def _optional_int(value: str | None) -> int | None:
    if not value:
        return None
    return int(value)


def discover_reports(report_dir: Path, reports: list[Path], limit: int | None) -> list[Path]:
    """Return report files in deterministic processing order."""

    selected = reports if reports else sorted(report_dir.glob("*.md"))
    normalized = [report for report in selected if report.exists()]
    if limit is not None:
        normalized = normalized[:limit]
    return normalized


def is_manifest_generation_report(report_text: str) -> bool:
    """Return true when a report represents a missing manifest bucket."""

    return bool(
        re.search(r"Failure type:\s*`manifest_generation`", report_text)
        or '"failure_type": "manifest_generation"' in report_text
    )


def build_test_generation_prompt(report_path: Path, report_text: str) -> str:
    """Build the prompt for one Codex test-generation agent."""

    if is_manifest_generation_report(report_text):
        raise ValueError(
            "manifest-generation reports require a feature request, not test generation"
        )

    return f"""You are a test-generation agent for ML4SE-toolkit comment extraction.

Task: read the Stack v2 judge failure report below and add deterministic pytest
coverage for the expected behavior. Stop after generating tests or fixtures.

Hard constraints:
- Do not implement the parser, registry, sanitizer, or manifest-generator fix.
- Do not modify production code under src/.
- Do not modify the judge report, generated Stack v2 source files, or tmp data.
- Do not add another LLM-as-judge assertion for this known behavior.
- Prefer the closest existing deterministic test module, such as
  tests/test_comment_queries.py, tests/test_comment_sanitizer.py,
  tests/test_comment_registry.py, tests/test_comment_language_fixtures.py, or a
  focused new test file under tests/ when no existing module fits.
- Keep extraction and sanitation coverage as separate assertions or separate
  tests when the report separates them.
- Use Expected Behavior as the assertion target. Use Actual Behavior only to
  understand why the new test should fail before the implementation is fixed.
- You may run the narrowest relevant pytest target to check that the new test is
  syntactically valid, but do not fix production behavior if that test fails.

Final response: list changed files, the deterministic test(s) added, and any
pytest command you ran with its result.

Report path: {report_path}

Report contents:
```markdown
{report_text}
```
"""


def codex_command(args: argparse.Namespace, output_path: Path) -> list[str]:
    """Return the Codex command used for test generation."""

    command = [
        args.codex_bin,
        "--ask-for-approval",
        "never",
        "--sandbox",
        args.codex_sandbox,
        "exec",
        "--cd",
        str(args.cwd),
        "--ephemeral",
        "--color",
        "never",
        "--output-last-message",
        str(output_path),
        "-",
    ]
    if args.model:
        command.extend(["--model", args.model])
    if args.profile:
        command.extend(["--profile", args.profile])
    return command


def run_report(args: argparse.Namespace, report: Path) -> int:
    """Run one Codex test-generation agent for one report."""

    report_text = report.read_text(encoding="utf-8")
    if is_manifest_generation_report(report_text):
        print(
            "[comment-testgen] skipping manifest-generation report; "
            f"create a feature request instead: {report}",
            file=sys.stderr,
        )
        return 0
    prompt = build_test_generation_prompt(report, report_text)
    with tempfile.TemporaryDirectory(prefix="comment-testgen-codex-") as temp_dir:
        output_path = Path(temp_dir) / "last_message.txt"
        try:
            result = subprocess.run(
                codex_command(args, output_path),
                input=prompt,
                text=True,
                capture_output=True,
                timeout=args.timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = normalize_output(exc.stdout)
            stderr = normalize_output(exc.stderr)
            if looks_like_usage_limit(stdout, stderr):
                print(
                    "[comment-testgen] Codex usage limit was reached; aborting.",
                    file=sys.stderr,
                )
                if stderr:
                    print(stderr, file=sys.stderr, end="")
                if stdout:
                    print(stdout, file=sys.stderr, end="")
                return usage_limit_exit_code()
            raise
        if result.stdout:
            print(result.stdout, file=sys.stderr, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        output_text = (
            output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        )
        if output_text:
            print(output_text, file=sys.stderr)
        usage_limit_seen = looks_like_usage_limit(result.stderr)
        if result.returncode != 0:
            usage_limit_seen = usage_limit_seen or looks_like_usage_limit(
                result.stdout,
                output_text,
            )
        if usage_limit_seen:
            print(
                "[comment-testgen] Codex usage limit was reached; aborting.",
                file=sys.stderr,
            )
            return usage_limit_exit_code()
        return result.returncode


def main() -> int:
    """Run test-generation agents for discovered judge failure reports."""

    args = parse_args()
    reports = discover_reports(args.report_dir, args.reports, args.limit)
    if not reports:
        print(f"No judge failure reports found in {args.report_dir}", file=sys.stderr)
        return 0

    for report in reports:
        print(f"[comment-testgen] report={report}", file=sys.stderr, flush=True)
        if args.dry_run:
            continue
        returncode = run_report(args, report)
        if returncode != 0:
            print(
                f"[comment-testgen] Codex failed for {report} with exit code {returncode}",
                file=sys.stderr,
            )
            return returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
