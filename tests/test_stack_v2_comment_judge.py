"""Optional LLM-as-judge tests for Stack v2 comment extraction cases."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
import time
from hashlib import sha1
from pathlib import Path
from typing import Any

import pytest

from ml4setk.Parsing.Comments import CommentQuery, CommentSanitizer


def _load_comment_judge_limits():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "comment_judge_limits.py"
    spec = importlib.util.spec_from_file_location("comment_judge_limits", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _load_comment_judge_validation_ledger():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "comment_judge_validation_ledger.py"
    )
    spec = importlib.util.spec_from_file_location(
        "comment_judge_validation_ledger", script_path
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_COMMENT_JUDGE_LIMITS = _load_comment_judge_limits()
_COMMENT_JUDGE_LEDGER = _load_comment_judge_validation_ledger()
looks_like_usage_limit = _COMMENT_JUDGE_LIMITS.looks_like_usage_limit
usage_limit_exit_code = _COMMENT_JUDGE_LIMITS.usage_limit_exit_code

pytestmark = [pytest.mark.integration, pytest.mark.optional_dependency]

MANIFEST_ENV = "STACK_V2_COMMENT_JUDGE_MANIFEST"
FAILURES_ENV = "STACK_V2_COMMENT_JUDGE_FAILURES"
REPORT_DIR_ENV = "STACK_V2_COMMENT_JUDGE_REPORT_DIR"
AGENT_CMD_ENV = "COMMENT_JUDGE_AGENT_CMD"
USE_CODEX_ENV = "COMMENT_JUDGE_USE_CODEX"
CASE_LIMIT_ENV = "COMMENT_JUDGE_CASE_LIMIT"
TIMEOUT_ENV = "COMMENT_JUDGE_TIMEOUT"
PROGRESS_ENV = "COMMENT_JUDGE_PROGRESS"
LEDGER_ENV = "COMMENT_JUDGE_LEDGER"
FORCE_LEDGER_ENV = "COMMENT_JUDGE_FORCE"


def _manifest_path() -> Path | None:
    """Return the configured manifest path, if one was provided."""

    manifest = os.environ.get(MANIFEST_ENV)
    return Path(manifest) if manifest else None


def _failure_path() -> Path | None:
    configured = os.environ.get(FAILURES_ENV)
    if configured:
        return Path(configured)
    manifest_path = _manifest_path()
    if manifest_path is None:
        return None
    default_failure_path = manifest_path.with_name("failures.jsonl")
    return default_failure_path if default_failure_path.exists() else None


def _report_dir() -> Path | None:
    """Return the directory used for per-case failure reports."""

    configured = os.environ.get(REPORT_DIR_ENV)
    if configured:
        return Path(configured)

    manifest_path = _manifest_path()
    if manifest_path is not None:
        return manifest_path.with_name("reports")

    failure_path = _failure_path()
    if failure_path is not None:
        return failure_path.with_name("reports")

    return None


def _load_cases() -> list[dict[str, Any]]:
    manifest_path = _manifest_path()
    if manifest_path is None:
        return []
    if not manifest_path.exists():
        raise FileNotFoundError(f"{MANIFEST_ENV} points to missing file: {manifest_path}")

    cases = []
    with manifest_path.open(encoding="utf-8") as infile:
        for line in infile:
            if line.strip():
                cases.append(json.loads(line))

    limit = os.environ.get(CASE_LIMIT_ENV)
    if limit:
        cases = cases[: int(limit)]

    total = len(cases)
    for index, case in enumerate(cases, start=1):
        case["_judge_progress_index"] = index
        case["_judge_progress_total"] = total
    return cases


def _load_failures() -> list[dict[str, Any]]:
    failure_path = _failure_path()
    if failure_path is None:
        return []
    if not failure_path.exists():
        return []

    failures = []
    with failure_path.open(encoding="utf-8") as infile:
        for line in infile:
            if line.strip():
                failures.append(json.loads(line))
    return failures



def _case_bucket(item: dict[str, Any]) -> tuple[str, str]:
    """Return the ledger bucket for a manifest case or generation failure."""

    return (
        str(item.get("language", "unknown")).lower(),
        str(item.get("comment_kind", "unknown")).lower(),
    )


def _bucket_case_ids(cases: list[dict[str, Any]]) -> dict[tuple[str, str], set[str]]:
    """Return manifest case IDs grouped by language/comment kind."""

    grouped: dict[tuple[str, str], set[str]] = {}
    for case in cases:
        grouped.setdefault(_case_bucket(case), set()).add(_case_id(case))
    return grouped


def _case_id(case: dict[str, Any]) -> str:
    """Return a stable case identifier for ledger bookkeeping."""

    return str(case.get("case_id") or f"{case.get('repo', '')}:{case.get('path', '')}")


STACK_V2_MANIFEST_PATH = _manifest_path()
STACK_V2_CASES = _load_cases()
STACK_V2_FAILURES = _load_failures()
STACK_V2_BUCKET_CASE_IDS = _bucket_case_ids(STACK_V2_CASES)
STACK_V2_PASSED_CASE_IDS: dict[tuple[str, str], set[str]] = {}
STACK_V2_FAILED_BUCKETS: set[tuple[str, str]] = set()
_LEDGER_VERSION_CACHE = None



def _judge_command() -> list[str] | None:
    """Return the configured judge command, or the Codex adapter command."""

    command = os.environ.get(AGENT_CMD_ENV)
    if command:
        return shlex.split(command)

    if os.environ.get(USE_CODEX_ENV, "").lower() in {"1", "true", "yes", "codex"}:
        repo_root = Path(__file__).resolve().parents[1]
        return [sys.executable, str(repo_root / "scripts" / "run_codex_comment_judge.py")]

    return None


def _repo_root() -> Path:
    """Return the repository root for judge helper scripts."""

    return Path(__file__).resolve().parents[1]


def _truthy_env(name: str) -> bool:
    """Return true when an environment flag is explicitly enabled."""

    return os.environ.get(name, "").lower() in {"1", "true", "yes", "on"}


def _ledger_enabled() -> bool:
    """Return whether the judge validation ledger is active."""

    value = os.environ.get(LEDGER_ENV)
    if value is None:
        return True
    return value.lower() not in {"", "0", "false", "no", "off"}


def _ledger_path() -> Path | None:
    """Return the configured validation ledger path."""

    if not _ledger_enabled():
        return None
    configured = os.environ.get(LEDGER_ENV)
    if configured:
        return Path(configured)
    return _repo_root() / _COMMENT_JUDGE_LEDGER.DEFAULT_LEDGER_PATH


def _ledger_force_enabled() -> bool:
    """Return whether cached pass/fail entries should be ignored."""

    return _truthy_env(FORCE_LEDGER_ENV)


def _ledger_recording_enabled() -> bool:
    """Return whether this pytest invocation may record full bucket coverage."""

    return (
        _ledger_enabled()
        and STACK_V2_MANIFEST_PATH is not None
        and not os.environ.get(CASE_LIMIT_ENV)
    )


def _judge_model_label() -> str:
    """Return a short label for the configured judge implementation."""

    if os.environ.get(USE_CODEX_ENV, "").lower() in {"1", "true", "yes", "codex"}:
        return os.environ.get("COMMENT_JUDGE_CODEX_MODEL") or "codex-default"
    if os.environ.get(AGENT_CMD_ENV):
        return "custom-agent-command"
    return "unknown"


def _current_ledger_version():
    """Return the clean committed code version used for ledger lookups."""

    global _LEDGER_VERSION_CACHE
    if _LEDGER_VERSION_CACHE is None:
        try:
            _LEDGER_VERSION_CACHE = _COMMENT_JUDGE_LEDGER.current_code_version(_repo_root())
        except _COMMENT_JUDGE_LEDGER.DirtyRelevantCodeError as exc:
            pytest.fail(str(exc))
        except _COMMENT_JUDGE_LEDGER.LedgerError as exc:
            pytest.fail(f"could not read Stack v2 comment judge code version: {exc}")
    return _LEDGER_VERSION_CACHE


def _ledger_manifest_label() -> str:
    """Return the current manifest path for ledger entries."""

    return str(STACK_V2_MANIFEST_PATH or "")


def _ledger_report_label(report_note: str | None) -> str:
    """Return a report path suitable for the ledger."""

    if not report_note or report_note.startswith("unavailable"):
        return ""
    return report_note


def _ledger_preflight_for_case(case: dict[str, Any]) -> None:
    """Skip or fail before launching an expensive judge for cached coverage."""

    ledger_path = _ledger_path()
    if ledger_path is None:
        return

    version = _current_ledger_version()
    if _ledger_force_enabled():
        return

    entries = _COMMENT_JUDGE_LEDGER.load_entries(ledger_path)
    language, comment_kind = _case_bucket(case)
    entry = _COMMENT_JUDGE_LEDGER.find_entry(
        entries,
        language=language,
        comment_kind=comment_kind,
        code_fingerprint=version.fingerprint,
    )
    if entry is None:
        return

    if entry.status == _COMMENT_JUDGE_LEDGER.PASSED:
        pytest.skip(
            f"Stack v2 judge already passed {language}/{comment_kind} "
            f"for code fingerprint {version.fingerprint[:12]} in {ledger_path}"
        )
    if entry.status == _COMMENT_JUDGE_LEDGER.FAILED:
        report = f" Prior report: {entry.report}." if entry.report else ""
        pytest.fail(
            f"Stack v2 judge previously failed {language}/{comment_kind} "
            f"for code fingerprint {version.fingerprint[:12]} in {ledger_path}."
            f"{report} Use {FORCE_LEDGER_ENV}=1 to rerun intentionally."
        )


def _record_case_pass_in_ledger(case: dict[str, Any], verdict: dict[str, Any]) -> None:
    """Record a passed bucket once all manifest cases for that bucket pass."""

    if not _ledger_recording_enabled() or not _verdict_passed(verdict):
        return

    bucket = _case_bucket(case)
    if bucket in STACK_V2_FAILED_BUCKETS:
        return

    STACK_V2_PASSED_CASE_IDS.setdefault(bucket, set()).add(_case_id(case))
    expected_case_ids = STACK_V2_BUCKET_CASE_IDS.get(bucket, set())
    if not expected_case_ids or not expected_case_ids.issubset(
        STACK_V2_PASSED_CASE_IDS[bucket]
    ):
        return

    language, comment_kind = bucket
    entry = _COMMENT_JUDGE_LEDGER.build_entry(
        language=language,
        comment_kind=comment_kind,
        status=_COMMENT_JUDGE_LEDGER.PASSED,
        cases=len(expected_case_ids),
        version=_current_ledger_version(),
        judge_model=_judge_model_label(),
        manifest=_ledger_manifest_label(),
        case_ids=tuple(sorted(expected_case_ids)),
    )
    _write_ledger_entry_or_fail(entry)


def _record_judge_failure_in_ledger(
    failure_type: str,
    case: dict[str, Any],
    verdict: dict[str, Any] | None,
    report_note: str | None,
    *,
    rationale: str = "",
) -> None:
    """Record a failed language/comment-kind bucket in the validation ledger."""

    if not _ledger_recording_enabled():
        return

    bucket = _case_bucket(case)
    case_id = _case_id(case)
    expected_case_ids = STACK_V2_BUCKET_CASE_IDS.get(bucket, set())
    if case_id not in expected_case_ids:
        return

    STACK_V2_FAILED_BUCKETS.add(bucket)
    language, comment_kind = bucket
    entry = _COMMENT_JUDGE_LEDGER.build_entry(
        language=language,
        comment_kind=comment_kind,
        status=_COMMENT_JUDGE_LEDGER.FAILED,
        cases=len(expected_case_ids),
        version=_current_ledger_version(),
        judge_model=_judge_model_label(),
        manifest=_ledger_manifest_label(),
        report=_ledger_report_label(report_note),
        failure_type=failure_type,
        rationale=rationale or str((verdict or {}).get("rationale", "")),
        case_ids=(case_id,),
    )
    _write_ledger_entry_or_fail(entry)


def _record_generation_failure_in_ledger(
    failure: dict[str, Any], report_note: str | None
) -> str | None:
    """Record an incomplete manifest bucket when a clean version is available."""

    if not _ledger_enabled():
        return None

    try:
        version = _COMMENT_JUDGE_LEDGER.current_code_version(_repo_root())
    except _COMMENT_JUDGE_LEDGER.LedgerError as exc:
        return f"Ledger note: {exc}"

    language, comment_kind = _case_bucket(failure)
    entry = _COMMENT_JUDGE_LEDGER.build_entry(
        language=language,
        comment_kind=comment_kind,
        status=_COMMENT_JUDGE_LEDGER.FAILED,
        cases=int(failure.get("observed_count", 0)),
        version=version,
        judge_model="manifest-generator",
        manifest=_ledger_manifest_label(),
        report=_ledger_report_label(report_note),
        failure_type="manifest_generation",
        rationale=str(failure.get("reason", "")),
    )
    try:
        _COMMENT_JUDGE_LEDGER.upsert_entry(_ledger_path(), entry)
    except (OSError, _COMMENT_JUDGE_LEDGER.LedgerError) as exc:
        return f"Ledger note: could not update validation ledger: {exc}"
    return None


def _write_ledger_entry_or_fail(entry) -> None:
    """Write a ledger entry, failing the pytest case if tracking breaks."""

    ledger_path = _ledger_path()
    if ledger_path is None:
        return
    try:
        _COMMENT_JUDGE_LEDGER.upsert_entry(ledger_path, entry)
    except (OSError, _COMMENT_JUDGE_LEDGER.LedgerError) as exc:
        pytest.fail(f"could not update Stack v2 comment judge validation ledger: {exc}")


def _format_ledger_note(note: str | None) -> str:
    """Format an optional ledger note for pytest failure output."""

    return f"\n{note}" if note else ""


@pytest.mark.skipif(
    not STACK_V2_FAILURES,
    reason="no Stack v2 manifest-generation failures were reported",
)
@pytest.mark.parametrize(
    "failure",
    STACK_V2_FAILURES,
    ids=lambda failure: (
        f"{failure.get('language', 'unknown')}-{failure.get('comment_kind', 'unknown')}"
    ),
)
def test_stack_v2_manifest_generation_has_no_missing_comment_kinds(
    failure: dict[str, Any],
) -> None:
    """Fail explicitly for language/kind buckets that could not be sampled."""

    report_note = _write_generation_failure_report(failure)
    ledger_note = _record_generation_failure_in_ledger(failure, report_note)
    pytest.fail(
        f"{_format_generation_failure(failure)}"
        f"{_format_report_note(report_note)}"
        f"{_format_ledger_note(ledger_note)}"
    )


def _format_generation_failure(failure: dict[str, Any]) -> str:
    language = failure.get("language", "unknown")
    comment_kind = failure.get("comment_kind", "unknown")
    observed = failure.get("observed_count", "?")
    expected = failure.get("expected_count", "?")
    scanned = failure.get("scanned_records", "?")
    reason = failure.get("reason", "missing generation failure reason")
    recommendation = failure.get("recommendation", "review the registry syntax and corpus samples")
    expected_actual = {
        "expected": {
            "comment_kind": comment_kind,
            "count": expected,
            "syntax_examples": failure.get("syntax_examples", []),
        },
        "actual": {
            "count": observed,
            "observed_kinds": failure.get("observed_kinds", {}),
            "scanned_records": scanned,
        },
    }
    return (
        f"Stack v2 manifest generation did not find enough {comment_kind} "
        f"comments for {language}: {observed}/{expected} after {scanned} "
        f"scanned record(s). {reason} {recommendation}\n"
        f"Expected vs actual:\n{json.dumps(expected_actual, ensure_ascii=False, indent=2)}"
    )


@pytest.mark.skipif(
    not STACK_V2_CASES,
    reason=f"set {MANIFEST_ENV} to a Stack v2 judge-case manifest",
)
@pytest.mark.skipif(
    _judge_command() is None,
    reason=(
        f"set {AGENT_CMD_ENV} to an agent command or set "
        f"{USE_CODEX_ENV}=1 to run Codex agents"
    ),
)
@pytest.mark.parametrize(
    "case",
    STACK_V2_CASES,
    ids=lambda case: case.get("case_id", "stack-v2-comment-case"),
)
def test_stack_v2_comment_extraction_and_cleaning_with_llm_judge(
    case: dict[str, Any],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Delegate extraction and cleaning correctness to an external judge agent."""

    started_at = time.monotonic()
    _emit_progress(capsys, f"{_progress_prefix(case)} start")
    _ledger_preflight_for_case(case)

    content = _read_case_content(case)
    language = case["language"]
    matches = CommentQuery(language).parse(content)
    actual = _observed_comments_near_target(content, language, matches, case)

    prompt = _build_judge_prompt(case, actual)
    _emit_progress(
        capsys,
        f"{_progress_prefix(case)} judge-start observed_comments={len(actual)}",
    )
    try:
        verdict = _run_judge(prompt, case=case, actual=actual)
    except Exception:
        elapsed = time.monotonic() - started_at
        _emit_progress(capsys, f"{_progress_prefix(case)} judge-error elapsed={elapsed:.1f}s")
        raise

    elapsed = time.monotonic() - started_at
    _emit_progress(
        capsys,
        f"{_progress_prefix(case)} judge-done elapsed={elapsed:.1f}s "
        f"verdict={verdict.get('verdict')} "
        f"extraction={verdict.get('extraction_correct')} "
        f"cleaning={verdict.get('cleaning_correct')}",
    )
    _assert_extraction_verdict(case, verdict, actual)
    _assert_cleaning_verdict(case, verdict, actual)
    _assert_overall_verdict(case, verdict, actual)
    _record_case_pass_in_ledger(case, verdict)


def _progress_enabled() -> bool:
    value = os.environ.get(PROGRESS_ENV, "1").lower()
    return value not in {"0", "false", "no", "off"}


def _progress_prefix(case: dict[str, Any]) -> str:
    index = case.get("_judge_progress_index", "?")
    total = case.get("_judge_progress_total", "?")
    return (
        f"[stack-v2 judge {index}/{total}] "
        f"case={case.get('case_id', 'unknown')} "
        f"language={case.get('language', 'unknown')} "
        f"kind={case.get('comment_kind', 'unknown')}"
    )


def _emit_progress(capsys: pytest.CaptureFixture[str], message: str) -> None:
    if not _progress_enabled():
        return
    with capsys.disabled():
        print(message, file=sys.stderr, flush=True)


def _read_case_content(case: dict[str, Any]) -> str:
    if "content" in case:
        return case["content"]

    source_file = Path(case["source_file"])
    if not source_file.is_absolute() and STACK_V2_MANIFEST_PATH is not None:
        source_file = STACK_V2_MANIFEST_PATH.parent / source_file
    with source_file.open(encoding="utf-8", newline="") as infile:
        return infile.read()


def _observed_comments_near_target(
    content: str,
    language: str,
    matches,
    case: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return observed comments in or near the target span."""

    target_start = int(case.get("match_start", -1))
    target_end = int(case.get("match_end", -1))
    sanitizer = CommentSanitizer(language)
    observed = []
    for index, match in enumerate(matches):
        start = len(match.prefix)
        end = len(content) - len(match.suffix)
        item = {
            "index": index,
            "raw_comment": match.match,
            "cleaned_comment": sanitizer.sanitize(match),
            "start": start,
            "end": end,
            "overlaps_sampled_target": _spans_overlap(start, end, target_start, target_end),
        }
        if item["overlaps_sampled_target"] or match.match == case.get("raw_comment"):
            observed.append(item)

    if observed:
        return observed

    return [
        {
            "index": index,
            "raw_comment": match.match,
            "cleaned_comment": sanitizer.sanitize(match),
            "start": len(match.prefix),
            "end": len(content) - len(match.suffix),
            "overlaps_sampled_target": False,
        }
        for index, match in enumerate(matches[:10])
    ]


def _spans_overlap(start: int, end: int, target_start: int, target_end: int) -> bool:
    return target_start >= 0 and target_end >= 0 and start < target_end and target_start < end


def _build_judge_prompt(case: dict[str, Any], actual: list[dict[str, Any]]) -> str:
    expected = {
        "case_id": case.get("case_id"),
        "language": case.get("language"),
        "comment_kind": case.get("comment_kind"),
        "syntax_label": case.get("syntax_label"),
        "repo": case.get("repo"),
        "path": case.get("path"),
        "sampled_raw_comment": case.get("raw_comment"),
        "sampled_cleaned_comment": case.get("cleaned_comment"),
    }
    observed = {"actual_extracted_comments": _content_only_actual_comments(actual)}

    return (
        "You are an LLM-as-a-judge for a comment extraction library.\n"
        "Judge one Stack v2 source-file case. The test harness has run the "
        "current parser and sanitizer; you decide whether the behavior is correct.\n\n"
        "Compare the sampled expected content against the actual returned content. "
        "Judge only raw and cleaned comment text. Do not validate character offsets, "
        "line/column numbers, span overlap, parser positioning metadata, or marked "
        "source excerpts; those are not part of this LLM judge test. Correct "
        "extraction means the actual extracted comments include the full sampled raw "
        "comment content and do not trim delimiters, omit lines, or absorb unrelated "
        "source code. Correct cleaning means the cleaned comment removes only "
        "comment syntax scaffolding, decorative gutters, delimiter-only edges, "
        "and padding while preserving content-bearing text, punctuation, "
        "examples, TODO tags, Markdown, and code-like text.\n\n"
        "Return JSON only, with this shape:\n"
        "{\n"
        '  "verdict": "pass" | "fail",\n'
        '  "extraction_correct": true | false,\n'
        '  "cleaning_correct": true | false,\n'
        '  "rationale": "short explanation"\n'
        "}\n\n"
        "Sampled case data:\n"
        f"{json.dumps(expected, ensure_ascii=False, indent=2)}\n\n"
        "Observed parser/sanitizer output:\n"
        f"{json.dumps(observed, ensure_ascii=False, indent=2)}\n"
    )



def _content_only_actual_comments(
    actual: list[dict[str, Any]], *, include_cleaned: bool = True
) -> list[dict[str, Any]]:
    """Return judge-visible parser output without location metadata."""

    actual_items = []
    for item in actual:
        actual_item = {
            "index": item.get("index"),
            "raw_comment": item.get("raw_comment"),
        }
        if include_cleaned:
            actual_item["cleaned_comment"] = item.get("cleaned_comment")
        actual_items.append(actual_item)
    return actual_items


def _assert_extraction_verdict(
    case: dict[str, Any], verdict: dict[str, Any], actual: list[dict[str, Any]]
) -> None:
    """Fail with an extraction-specific message when the judge rejects parsing."""

    if verdict.get("extraction_correct") is not True:
        report_note = _write_judge_failure_report("extraction", case, actual, verdict)
        _record_judge_failure_in_ledger("extraction", case, verdict, report_note)
        pytest.fail(
            "Stack v2 extraction judge rejected case "
            f"{case.get('case_id')}: {verdict.get('rationale', verdict)}\n"
            f"{_format_expected_actual(case, actual, include_cleaned=False)}"
            f"{_format_report_note(report_note)}"
        )


def _assert_cleaning_verdict(
    case: dict[str, Any], verdict: dict[str, Any], actual: list[dict[str, Any]]
) -> None:
    """Fail with a sanitation-specific message when the judge rejects cleaning."""

    if verdict.get("cleaning_correct") is not True:
        report_note = _write_judge_failure_report("sanitation", case, actual, verdict)
        _record_judge_failure_in_ledger("sanitation", case, verdict, report_note)
        pytest.fail(
            "Stack v2 sanitation judge rejected case "
            f"{case.get('case_id')}: {verdict.get('rationale', verdict)}\n"
            f"{_format_expected_actual(case, actual, include_cleaned=True)}"
            f"{_format_report_note(report_note)}"
        )


def _assert_overall_verdict(
    case: dict[str, Any], verdict: dict[str, Any], actual: list[dict[str, Any]]
) -> None:
    """Fail when the judge booleans pass but the overall verdict disagrees."""

    if verdict.get("verdict") != "pass":
        report_note = _write_judge_failure_report("overall", case, actual, verdict)
        _record_judge_failure_in_ledger("overall", case, verdict, report_note)
        pytest.fail(
            "Stack v2 judge returned non-pass verdict for case "
            f"{case.get('case_id')}: {verdict.get('rationale', verdict)}\n"
            f"{_format_expected_actual(case, actual, include_cleaned=True)}"
            f"{_format_report_note(report_note)}"
        )


def _format_expected_actual(
    case: dict[str, Any], actual: list[dict[str, Any]], *, include_cleaned: bool
) -> str:
    payload = _judge_expected_actual_payload(
        case, actual, include_cleaned=include_cleaned
    )
    return f"Expected vs actual:\n{json.dumps(payload, ensure_ascii=False, indent=2)}"


def _judge_expected_actual_payload(
    case: dict[str, Any], actual: list[dict[str, Any]], *, include_cleaned: bool
) -> dict[str, Any]:
    expected = {"raw_comment": case.get("raw_comment")}
    if include_cleaned:
        expected["cleaned_comment"] = case.get("cleaned_comment")

    return {
        "expected": expected,
        "actual": _content_only_actual_comments(actual, include_cleaned=include_cleaned),
    }


def _generation_expected_actual_payload(failure: dict[str, Any]) -> dict[str, Any]:
    return {
        "expected": {
            "comment_kind": failure.get("comment_kind", "unknown"),
            "count": failure.get("expected_count", "?"),
            "syntax_examples": failure.get("syntax_examples", []),
        },
        "actual": {
            "count": failure.get("observed_count", "?"),
            "observed_kinds": failure.get("observed_kinds", {}),
            "scanned_records": failure.get("scanned_records", "?"),
        },
    }


def _write_generation_failure_report(failure: dict[str, Any]) -> str | None:
    expected_actual = _generation_expected_actual_payload(failure)
    payload = {
        "failure_type": "manifest_generation",
        "language": failure.get("language", "unknown"),
        "comment_kind": failure.get("comment_kind", "unknown"),
        "reason": failure.get("reason", "missing generation failure reason"),
        "recommendation": failure.get(
            "recommendation", "review the registry syntax and corpus samples"
        ),
        "expected_behavior": expected_actual["expected"],
        "actual_behavior": expected_actual["actual"],
    }
    slug = _safe_report_slug(
        "manifest",
        payload["language"],
        payload["comment_kind"],
        payload["failure_type"],
    )
    return _write_failure_report(slug, payload)


def _write_judge_failure_report(
    failure_type: str,
    case: dict[str, Any],
    actual: list[dict[str, Any]],
    verdict: dict[str, Any] | None,
    *,
    judge_error: dict[str, Any] | None = None,
) -> str | None:
    include_cleaned = failure_type != "extraction"
    expected_actual = _judge_expected_actual_payload(
        case, actual, include_cleaned=include_cleaned
    )
    payload = {
        "failure_type": failure_type,
        "case": {
            "case_id": case.get("case_id"),
            "language": case.get("language"),
            "comment_kind": case.get("comment_kind"),
            "syntax_label": case.get("syntax_label"),
            "repo": case.get("repo"),
            "path": case.get("path"),
        },
        "expected_behavior": expected_actual["expected"],
        "actual_behavior": expected_actual["actual"],
        "judge_verdict": verdict,
        "judge_error": judge_error,
        "marked_source_excerpt": case.get("source_excerpt"),
    }
    slug = _safe_report_slug(
        case.get("case_id", "case"),
        case.get("language", "unknown"),
        case.get("comment_kind", "unknown"),
        failure_type,
    )
    return _write_failure_report(slug, payload)


def _write_failure_report(slug: str, payload: dict[str, Any]) -> str | None:
    report_dir = _report_dir()
    if report_dir is None:
        return None

    try:
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"{slug}.md"
        report_path.write_text(_render_failure_report(payload), encoding="utf-8")
    except OSError as exc:
        return f"unavailable ({exc})"

    return str(report_path)


def _render_failure_report(payload: dict[str, Any]) -> str:
    return (
        "# Stack v2 Comment Judge Failure Report\n\n"
        f"- Failure type: `{payload.get('failure_type', 'unknown')}`\n"
        f"- Case ID: `{_payload_case_id(payload)}`\n"
        f"- Language: `{_payload_language(payload)}`\n"
        f"- Comment kind: `{_payload_comment_kind(payload)}`\n\n"
        "## Expected Behavior\n\n"
        f"```json\n{_json_dump(payload.get('expected_behavior'))}\n```\n\n"
        "## Actual Behavior\n\n"
        f"```json\n{_json_dump(payload.get('actual_behavior'))}\n```\n\n"
        "## Judge Context\n\n"
        f"```json\n{_json_dump(_judge_context_payload(payload))}\n```\n\n"
        f"{_render_followup_task(payload)}\n\n"
        "## Machine Payload\n\n"
        f"```json\n{_json_dump(payload)}\n```\n"
    )


def _render_followup_task(payload: dict[str, Any]) -> str:
    if payload.get("failure_type") == "manifest_generation":
        return (
            "## Feature Request Task\n\n"
            "This is a missing language/comment-kind bucket, not a failed "
            "extraction or sanitizer assertion. Do not convert this report "
            "directly into a deterministic parser regression test. Create or "
            "update a feature request that asks for syntax research and registry "
            "review for this language/kind pair. If the syntax is valid for the "
            "language and corpus, add support and then add deterministic coverage; "
            "if it is not valid for this corpus, remove or exclude the kind with "
            "an explicit research note."
        )

    return (
        "## Test Generation Agent Task\n\n"
        "Create or update deterministic pytest coverage for this behavior. "
        "Do not add an LLM assertion for this regression. Use the expected "
        "behavior above as the final assertion target. Use the actual "
        "behavior to understand the current failure and verify the new test "
        "fails before the fix, then add the test to the closest comment "
        "extraction or sanitizer test module."
    )


def _judge_context_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "reason": payload.get("reason"),
        "recommendation": payload.get("recommendation"),
        "case": payload.get("case"),
        "judge_verdict": payload.get("judge_verdict"),
        "judge_error": payload.get("judge_error"),
        "marked_source_excerpt": payload.get("marked_source_excerpt"),
    }


def _payload_case_id(payload: dict[str, Any]) -> str:
    case = payload.get("case") or {}
    return str(case.get("case_id") or "n/a")


def _payload_language(payload: dict[str, Any]) -> str:
    case = payload.get("case") or {}
    return str(case.get("language") or payload.get("language") or "unknown")


def _payload_comment_kind(payload: dict[str, Any]) -> str:
    case = payload.get("case") or {}
    return str(case.get("comment_kind") or payload.get("comment_kind") or "unknown")


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def _safe_report_slug(*parts: Any) -> str:
    text_parts = [str(part) for part in parts if part is not None and str(part) != ""]
    identity = "::".join(text_parts)
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", identity).strip("-").lower()
    slug = slug[:90] or "stack-v2-comment-judge-failure"
    digest = sha1(identity.encode("utf-8")).hexdigest()[:8]
    return f"{slug}-{digest}"


def _format_report_note(report_note: str | None) -> str:
    if report_note is None:
        return ""
    if report_note.startswith("unavailable"):
        return f"\nFailure report {report_note}"
    return f"\nFailure report: {report_note}"


def _verdict_passed(verdict: dict[str, Any]) -> bool:
    """Return true only when every judge contract field agrees."""

    return (
        verdict.get("verdict") == "pass"
        and verdict.get("extraction_correct") is True
        and verdict.get("cleaning_correct") is True
    )


def _run_judge(
    prompt: str,
    *,
    case: dict[str, Any] | None = None,
    actual: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    command = _judge_command()
    if command is None:
        pytest.skip(f"set {AGENT_CMD_ENV} to an agent command or set {USE_CODEX_ENV}=1")

    timeout = int(os.environ.get(TIMEOUT_ENV, "120"))
    try:
        result = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = _process_output_text(exc.stdout)
        stderr = _process_output_text(exc.stderr)
        _exit_for_usage_limit_if_present(
            case=case,
            actual=actual,
            returncode=None,
            stdout=stdout,
            stderr=stderr,
            timeout=timeout,
        )
        report_note = _write_judge_failure_report(
            "judge_command",
            case or {},
            actual or [],
            None,
            judge_error={
                "timeout": timeout,
                "stdout": stdout,
                "stderr": stderr,
            },
        )
        _record_judge_failure_in_ledger(
            "judge_command",
            case or {},
            None,
            report_note,
            rationale=f"judge command timed out after {timeout}s",
        )
        pytest.fail(
            f"judge command timed out after {timeout}s"
            f"{_format_report_note(report_note)}"
        )
    _exit_for_usage_limit_if_present(
        case=case,
        actual=actual,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )
    if result.returncode != 0:
        report_note = _write_judge_failure_report(
            "judge_command",
            case or {},
            actual or [],
            None,
            judge_error={
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
        _record_judge_failure_in_ledger(
            "judge_command",
            case or {},
            None,
            report_note,
            rationale=f"judge command failed with exit code {result.returncode}",
        )
        pytest.fail(
            f"judge command failed with exit code {result.returncode}\n"
            f"stderr:\n{result.stderr}\nstdout:\n{result.stdout}"
            f"{_format_report_note(report_note)}"
        )
    try:
        return _parse_judge_json(result.stdout)
    except (json.JSONDecodeError, ValueError) as exc:
        report_note = _write_judge_failure_report(
            "judge_output",
            case or {},
            actual or [],
            None,
            judge_error={
                "error": str(exc),
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
        _record_judge_failure_in_ledger(
            "judge_output",
            case or {},
            None,
            report_note,
            rationale=str(exc),
        )
        pytest.fail(f"judge output was invalid: {exc}{_format_report_note(report_note)}")


def _exit_for_usage_limit_if_present(
    *,
    case: dict[str, Any] | None,
    actual: list[dict[str, Any]] | None,
    returncode: int | None,
    stdout: Any,
    stderr: Any,
    timeout: int | None = None,
) -> None:
    """Abort the pytest session when the external judge has exhausted LLM usage."""

    exit_code = usage_limit_exit_code()
    usage_limit_seen = looks_like_usage_limit(stderr)
    if returncode is None or returncode != 0:
        usage_limit_seen = usage_limit_seen or looks_like_usage_limit(stdout)
    if returncode != exit_code and not usage_limit_seen:
        return

    judge_error = {
        "returncode": returncode,
        "timeout": timeout,
        "stdout": _process_output_text(stdout),
        "stderr": _process_output_text(stderr),
    }
    report_note = _write_judge_failure_report(
        "judge_usage_limit",
        case or {},
        actual or [],
        None,
        judge_error=judge_error,
    )
    pytest.exit(
        "LLM judge usage limit was reached; aborting the Stack v2 judge suite."
        f"{_format_report_note(report_note)}",
        returncode=exit_code,
    )


def _process_output_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _parse_judge_json(stdout: str) -> dict[str, Any]:
    text = stdout.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()

    try:
        verdict = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        verdict = json.loads(text[start : end + 1])

    _validate_verdict(verdict)
    return verdict


def _validate_verdict(verdict: dict[str, Any]) -> None:
    if not isinstance(verdict, dict):
        raise ValueError("judge verdict must be a JSON object")

    required_fields = (
        "verdict",
        "extraction_correct",
        "cleaning_correct",
        "rationale",
    )
    missing = [field for field in required_fields if field not in verdict]
    if missing:
        raise ValueError(f"judge verdict missing required field(s): {', '.join(missing)}")

    if verdict["verdict"] not in {"pass", "fail"}:
        raise ValueError("judge verdict must be 'pass' or 'fail'")
    for field in ("extraction_correct", "cleaning_correct"):
        if not isinstance(verdict[field], bool):
            raise ValueError(f"judge {field} must be a boolean")
    if not isinstance(verdict["rationale"], str):
        raise ValueError("judge rationale must be a string")


def test_parse_judge_json_requires_consistent_shape() -> None:
    valid = _parse_judge_json(
        '{"verdict":"pass","extraction_correct":true,'
        '"cleaning_correct":true,"rationale":"ok"}'
    )
    assert _verdict_passed(valid)

    with pytest.raises(ValueError):
        _parse_judge_json(
            '{"verdict":"pass","extraction_correct":false,'
            '"cleaning_correct":"yes","rationale":"bad"}'
        )

    with pytest.raises(ValueError, match="JSON object"):
        _parse_judge_json("[]")


def test_judge_command_can_use_codex_adapter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(AGENT_CMD_ENV, raising=False)
    monkeypatch.setenv(USE_CODEX_ENV, "1")

    command = _judge_command()

    assert command is not None
    assert command[0] == sys.executable
    assert command[-1].endswith("scripts/run_codex_comment_judge.py")


def test_read_case_content_resolves_manifest_relative_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    source_dir = tmp_path / "files"
    source_dir.mkdir()
    source = source_dir / "case.txt"
    source.write_text("# note\n", encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "STACK_V2_MANIFEST_PATH", manifest)

    assert _read_case_content({"source_file": "files/case.txt"}) == "# note\n"


def test_read_case_content_preserves_source_newlines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    source_dir = tmp_path / "files"
    source_dir.mkdir()
    source = source_dir / "case.txt"
    source.write_bytes(b"# note\r\nnext\r")
    monkeypatch.setattr(sys.modules[__name__], "STACK_V2_MANIFEST_PATH", manifest)

    assert _read_case_content({"source_file": "files/case.txt"}) == "# note\r\nnext\r"


def test_progress_prefix_includes_case_position_and_identity() -> None:
    case = {
        "_judge_progress_index": 3,
        "_judge_progress_total": 12,
        "case_id": "python-line-sample",
        "language": "python",
        "comment_kind": "line",
    }

    assert _progress_prefix(case) == (
        "[stack-v2 judge 3/12] "
        "case=python-line-sample language=python kind=line"
    )


def test_progress_can_be_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(PROGRESS_ENV, raising=False)
    assert _progress_enabled()

    monkeypatch.setenv(PROGRESS_ENV, "0")
    assert not _progress_enabled()

    monkeypatch.setenv(PROGRESS_ENV, "false")
    assert not _progress_enabled()


def test_judge_prompt_and_failure_payload_hide_span_metadata() -> None:
    case = {
        "case_id": "python-line-sample",
        "language": "python",
        "comment_kind": "line",
        "syntax_label": "hash",
        "repo": "owner/repo",
        "path": "pkg/example.py",
        "raw_comment": "# expected raw",
        "cleaned_comment": "expected raw",
        "match_start": 10,
        "match_end": 24,
        "match_line": 3,
        "match_column": 1,
        "source_excerpt": "<<<TARGET_COMMENT_START>>># expected raw<<<TARGET_COMMENT_END>>>",
    }
    actual = [
        {
            "index": 0,
            "raw_comment": "# actual raw",
            "cleaned_comment": "actual raw",
            "start": 11,
            "end": 23,
            "overlaps_sampled_target": True,
        }
    ]

    prompt = _build_judge_prompt(case, actual)
    payload = _judge_expected_actual_payload(case, actual, include_cleaned=True)

    assert "Do not validate character offsets" in prompt
    for hidden_field in (
        "match_start",
        "match_end",
        "match_line",
        "match_column",
        "marked_source_excerpt",
        "source_excerpt",
        "TARGET_COMMENT_START",
        "TARGET_COMMENT_END",
        "overlaps_sampled_target",
        '"start":',
        '"end":',
    ):
        assert hidden_field not in prompt
        assert hidden_field not in json.dumps(payload)
    assert payload == {
        "expected": {
            "raw_comment": "# expected raw",
            "cleaned_comment": "expected raw",
        },
        "actual": [
            {
                "index": 0,
                "raw_comment": "# actual raw",
                "cleaned_comment": "actual raw",
            }
        ],
    }


def test_usage_limit_output_aborts_judge_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(REPORT_DIR_ENV, str(tmp_path))
    monkeypatch.setenv("COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE", "91")

    with pytest.raises(pytest.exit.Exception) as exc_info:
        _exit_for_usage_limit_if_present(
            case={
                "case_id": "python-line-sample",
                "language": "python",
                "comment_kind": "line",
            },
            actual=[],
            returncode=None,
            stdout="",
            stderr="Usage limit reached for this account.",
        )

    assert exc_info.value.returncode == 91
    assert "usage limit" in str(exc_info.value).lower()
    reports = list(tmp_path.glob("*.md"))
    assert len(reports) == 1
    report_text = reports[0].read_text(encoding="utf-8")
    assert "judge_usage_limit" in report_text
    assert "Usage limit reached" in report_text


def test_usage_limit_phrase_in_successful_stdout_does_not_abort() -> None:
    _exit_for_usage_limit_if_present(
        case={},
        actual=[],
        returncode=0,
        stdout='{"rationale": "comment text mentions a usage limit"}',
        stderr="",
    )


def test_generation_failure_message_is_specific() -> None:
    message = _format_generation_failure(
        {
            "language": "coffeescript",
            "comment_kind": "block",
            "observed_count": 0,
            "expected_count": 10,
            "scanned_records": 1000,
            "syntax_examples": ["###\nnote\n###"],
            "observed_kinds": {"line": 10},
            "reason": "No block comments were sampled.",
            "recommendation": "Review the CoffeeScript block syntax.",
        }
    )

    assert "coffeescript" in message
    assert "block" in message
    assert "0/10" in message
    assert "1000" in message
    assert "Expected vs actual" in message
    assert "###\\nnote\\n###" in message
    assert '"line": 10' in message


def test_load_failures_treats_missing_configured_path_as_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(FAILURES_ENV, str(tmp_path / "missing-failures.jsonl"))

    assert _load_failures() == []


def test_load_failures_uses_manifest_sibling_by_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    manifest.write_text("", encoding="utf-8")
    failure_path = tmp_path / "failures.jsonl"
    failure_path.write_text(
        '{"language":"coffeescript","comment_kind":"block"}\n',
        encoding="utf-8",
    )
    monkeypatch.setenv(MANIFEST_ENV, str(manifest))
    monkeypatch.delenv(FAILURES_ENV, raising=False)

    assert _load_failures() == [{"language": "coffeescript", "comment_kind": "block"}]


def test_report_dir_defaults_to_manifest_sibling(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = tmp_path / "manifest.jsonl"
    monkeypatch.setenv(MANIFEST_ENV, str(manifest))
    monkeypatch.delenv(REPORT_DIR_ENV, raising=False)
    monkeypatch.delenv(FAILURES_ENV, raising=False)

    assert _report_dir() == tmp_path / "reports"


def test_judge_failure_report_includes_expected_actual_and_agent_task(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(REPORT_DIR_ENV, str(tmp_path))
    case = {
        "case_id": "python-line-sample",
        "language": "python",
        "comment_kind": "line",
        "syntax_label": "hash",
        "repo": "owner/repo",
        "path": "pkg/example.py",
        "raw_comment": "# expected raw",
        "cleaned_comment": "expected raw",
        "match_start": 10,
        "match_end": 24,
        "match_line": 3,
        "match_column": 1,
        "source_excerpt": "x = 1\n<<<TARGET_COMMENT_START>>># expected raw",
    }
    actual = [
        {
            "index": 0,
            "raw_comment": "# actual raw",
            "cleaned_comment": "actual raw",
            "start": 11,
            "end": 23,
            "overlaps_sampled_target": True,
        }
    ]
    verdict = {
        "verdict": "fail",
        "extraction_correct": True,
        "cleaning_correct": False,
        "rationale": "cleaned text differs",
    }

    report = _write_judge_failure_report("sanitation", case, actual, verdict)

    assert report is not None
    report_path = Path(report)
    report_text = report_path.read_text(encoding="utf-8")
    assert report_path.parent == tmp_path
    assert "## Expected Behavior" in report_text
    assert "## Actual Behavior" in report_text
    assert "## Test Generation Agent Task" in report_text
    assert "deterministic pytest coverage" in report_text
    assert "# expected raw" in report_text
    assert "# actual raw" in report_text
    assert "expected raw" in report_text
    assert "actual raw" in report_text


def test_generation_failure_report_includes_bucket_counts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(REPORT_DIR_ENV, str(tmp_path))
    failure = {
        "language": "coffeescript",
        "comment_kind": "block",
        "observed_count": 0,
        "expected_count": 10,
        "scanned_records": 1000,
        "syntax_examples": ["###\nnote\n###"],
        "observed_kinds": {"line": 10},
        "reason": "No block comments were sampled.",
        "recommendation": "Review the CoffeeScript block syntax.",
    }

    report = _write_generation_failure_report(failure)

    assert report is not None
    report_text = Path(report).read_text(encoding="utf-8")
    assert "manifest_generation" in report_text
    assert "## Feature Request Task" in report_text
    assert "not a failed extraction or sanitizer assertion" in report_text
    assert "deterministic parser regression test" in report_text
    assert "## Test Generation Agent Task" not in report_text
    assert "coffeescript" in report_text
    assert "block" in report_text
    assert '"count": 10' in report_text
    assert '"count": 0' in report_text
    assert '"line": 10' in report_text
    assert "###\\nnote\\n###" in report_text


def test_verdict_assertions_fail_independently() -> None:
    case = {
        "case_id": "sample",
        "raw_comment": "# expected raw",
        "cleaned_comment": "expected cleaned",
        "match_start": 4,
        "match_end": 18,
    }
    actual = [
        {
            "index": 0,
            "raw_comment": "# actual raw",
            "cleaned_comment": "actual cleaned",
            "start": 5,
            "end": 17,
            "overlaps_sampled_target": True,
        }
    ]

    with pytest.raises(pytest.fail.Exception, match="extraction judge rejected") as exc_info:
        _assert_extraction_verdict(
            case,
            {
                "verdict": "fail",
                "extraction_correct": False,
                "cleaning_correct": True,
                "rationale": "raw match is truncated",
            },
            actual,
        )
    extraction_message = str(exc_info.value)
    assert "Expected vs actual" in extraction_message
    assert "# expected raw" in extraction_message
    assert "# actual raw" in extraction_message

    with pytest.raises(pytest.fail.Exception, match="sanitation judge rejected") as exc_info:
        _assert_cleaning_verdict(
            case,
            {
                "verdict": "fail",
                "extraction_correct": True,
                "cleaning_correct": False,
                "rationale": "cleaned text lost content",
            },
            actual,
        )
    cleaning_message = str(exc_info.value)
    assert "expected cleaned" in cleaning_message
    assert "actual cleaned" in cleaning_message

    with pytest.raises(pytest.fail.Exception, match="non-pass verdict") as exc_info:
        _assert_overall_verdict(
            case,
            {
                "verdict": "fail",
                "extraction_correct": True,
                "cleaning_correct": True,
                "rationale": "overall disagreement",
            },
            actual,
        )
    assert "Expected vs actual" in str(exc_info.value)


def test_parse_judge_json_reports_missing_required_fields() -> None:
    with pytest.raises(ValueError, match="extraction_correct"):
        _parse_judge_json(
            '{"verdict":"pass","cleaning_correct":true,"rationale":"missing"}'
        )

    with pytest.raises(ValueError, match="cleaning_correct"):
        _parse_judge_json(
            '{"verdict":"pass","extraction_correct":true,"rationale":"missing"}'
        )



def test_ledger_preflight_skips_already_passed_bucket(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ledger_path = tmp_path / "ledger.md"
    version = _COMMENT_JUDGE_LEDGER.CodeVersion("abc", "f" * 64, ("parser.py",))
    entry = _COMMENT_JUDGE_LEDGER.build_entry(
        language="python",
        comment_kind="line",
        status=_COMMENT_JUDGE_LEDGER.PASSED,
        cases=10,
        version=version,
        judge_model="codex-default",
    )
    _COMMENT_JUDGE_LEDGER.write_entries(ledger_path, [entry])
    monkeypatch.setenv(LEDGER_ENV, str(ledger_path))
    monkeypatch.delenv(FORCE_LEDGER_ENV, raising=False)
    monkeypatch.setattr(sys.modules[__name__], "_LEDGER_VERSION_CACHE", version)

    with pytest.raises(pytest.skip.Exception, match="already passed"):
        _ledger_preflight_for_case({"language": "python", "comment_kind": "line"})


def test_ledger_preflight_fails_known_failed_bucket(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ledger_path = tmp_path / "ledger.md"
    version = _COMMENT_JUDGE_LEDGER.CodeVersion("abc", "f" * 64, ("parser.py",))
    entry = _COMMENT_JUDGE_LEDGER.build_entry(
        language="python",
        comment_kind="line",
        status=_COMMENT_JUDGE_LEDGER.FAILED,
        cases=1,
        version=version,
        judge_model="codex-default",
        report="tmp/reports/python-line.md",
        failure_type="extraction",
    )
    _COMMENT_JUDGE_LEDGER.write_entries(ledger_path, [entry])
    monkeypatch.setenv(LEDGER_ENV, str(ledger_path))
    monkeypatch.delenv(FORCE_LEDGER_ENV, raising=False)
    monkeypatch.setattr(sys.modules[__name__], "_LEDGER_VERSION_CACHE", version)

    with pytest.raises(pytest.fail.Exception, match="previously failed") as exc_info:
        _ledger_preflight_for_case({"language": "python", "comment_kind": "line"})

    assert "tmp/reports/python-line.md" in str(exc_info.value)


def test_ledger_force_bypasses_cached_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ledger_path = tmp_path / "ledger.md"
    version = _COMMENT_JUDGE_LEDGER.CodeVersion("abc", "f" * 64, ("parser.py",))
    entry = _COMMENT_JUDGE_LEDGER.build_entry(
        language="python",
        comment_kind="line",
        status=_COMMENT_JUDGE_LEDGER.PASSED,
        cases=10,
        version=version,
        judge_model="codex-default",
    )
    _COMMENT_JUDGE_LEDGER.write_entries(ledger_path, [entry])
    monkeypatch.setenv(LEDGER_ENV, str(ledger_path))
    monkeypatch.setenv(FORCE_LEDGER_ENV, "1")
    monkeypatch.setattr(sys.modules[__name__], "_LEDGER_VERSION_CACHE", version)

    _ledger_preflight_for_case({"language": "python", "comment_kind": "line"})


def test_ledger_records_pass_after_all_bucket_cases_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ledger_path = tmp_path / "ledger.md"
    manifest_path = tmp_path / "manifest.jsonl"
    version = _COMMENT_JUDGE_LEDGER.CodeVersion("abc", "f" * 64, ("parser.py",))
    bucket = ("python", "line")
    verdict = {
        "verdict": "pass",
        "extraction_correct": True,
        "cleaning_correct": True,
        "rationale": "ok",
    }
    monkeypatch.setenv(LEDGER_ENV, str(ledger_path))
    monkeypatch.delenv(CASE_LIMIT_ENV, raising=False)
    monkeypatch.setattr(sys.modules[__name__], "STACK_V2_MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(
        sys.modules[__name__], "STACK_V2_BUCKET_CASE_IDS", {bucket: {"case-1", "case-2"}}
    )
    monkeypatch.setattr(sys.modules[__name__], "STACK_V2_PASSED_CASE_IDS", {})
    monkeypatch.setattr(sys.modules[__name__], "STACK_V2_FAILED_BUCKETS", set())
    monkeypatch.setattr(sys.modules[__name__], "_LEDGER_VERSION_CACHE", version)

    _record_case_pass_in_ledger(
        {"case_id": "case-1", "language": "python", "comment_kind": "line"}, verdict
    )
    assert not ledger_path.exists()

    _record_case_pass_in_ledger(
        {"case_id": "case-2", "language": "python", "comment_kind": "line"}, verdict
    )

    entries = _COMMENT_JUDGE_LEDGER.load_entries(ledger_path)
    assert len(entries) == 1
    assert entries[0].status == _COMMENT_JUDGE_LEDGER.PASSED
    assert entries[0].cases == 2
    assert entries[0].case_ids == ("case-1", "case-2")
