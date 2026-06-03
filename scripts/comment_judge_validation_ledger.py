"""Track Stack v2 LLM judge validation by committed comment-code version.

The ledger is a Markdown file with an embedded JSON payload. Humans review the
tables; tools read and update the JSON block so expensive judge runs can skip
language/comment-kind buckets that already passed for the same committed parser,
sanitizer, registry, and judge-contract code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
LEDGER_START = "<!-- STACK_V2_COMMENT_JUDGE_LEDGER_START"
LEDGER_END = "STACK_V2_COMMENT_JUDGE_LEDGER_END -->"
DEFAULT_LEDGER_PATH = Path("docs/comment_testing/stack_v2_judge_validation_ledger.md")
DEFAULT_RELEVANT_PATHS = (
    "src/ml4setk/Parsing/Query.py",
    "src/ml4setk/Parsing/Comments/__init__.py",
    "src/ml4setk/Parsing/Comments/CommentQuery.py",
    "src/ml4setk/Parsing/Comments/CommentSanitizer.py",
    "src/ml4setk/Parsing/Comments/registry.py",
    "scripts/build_stack_v2_comment_judge_cases.py",
    "scripts/comment_judge_limits.py",
    "scripts/run_codex_comment_judge.py",
    "tests/test_stack_v2_comment_judge.py",
)
PASSED = "passed"
FAILED = "failed"


class LedgerError(RuntimeError):
    """Base class for ledger read/write and versioning failures."""


class DirtyRelevantCodeError(LedgerError):
    """Raised when a validation version cannot be recorded from a clean commit.

    Args:
        paths: Relevant paths that are staged, modified, untracked, missing from
            ``HEAD``, or otherwise not represented by the committed version.
    """

    def __init__(self, paths: list[str]):
        self.paths = tuple(paths)
        message = (
            "Stack v2 comment judge validation requires relevant comment-code "
            "files to be committed before LLM judges run or ledger entries are "
            f"recorded. Dirty or uncommitted relevant path(s): {', '.join(self.paths)}"
        )
        super().__init__(message)


@dataclass(frozen=True)
class CodeVersion:
    """Committed code identity used to key judge validation entries.

    Attributes:
        git_commit: Full ``HEAD`` commit SHA.
        fingerprint: SHA-256 over the committed blobs of relevant files.
        relevant_paths: Paths included in the fingerprint.
    """

    git_commit: str
    fingerprint: str
    relevant_paths: tuple[str, ...]


@dataclass(frozen=True)
class JudgeLedgerEntry:
    """One language/comment-kind validation result for one code fingerprint.

    Attributes:
        language: Registry language key from the manifest.
        comment_kind: Comment bucket such as ``line``, ``block``, or ``nested``.
        status: ``passed`` or ``failed``.
        cases: Number of sampled cases represented by the entry.
        code_fingerprint: Fingerprint returned by ``current_code_version``.
        git_commit: Commit used to compute the fingerprint.
        judge_model: Judge model or command label.
        updated_at: UTC ISO-8601 timestamp.
        manifest: Manifest path used for the run.
        report: Optional Markdown failure-report path.
        failure_type: Optional failure type from the judge harness.
        rationale: Optional short reason or judge rationale.
        case_ids: Manifest case identifiers represented by the entry.
    """

    language: str
    comment_kind: str
    status: str
    cases: int
    code_fingerprint: str
    git_commit: str
    judge_model: str
    updated_at: str
    manifest: str = ""
    report: str = ""
    failure_type: str = ""
    rationale: str = ""
    case_ids: tuple[str, ...] = ()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "JudgeLedgerEntry":
        """Build an entry from the machine-readable ledger payload.

        Args:
            data: JSON object from the embedded ledger block.

        Returns:
            A normalized ledger entry.
        """

        return cls(
            language=str(data.get("language", "")).lower(),
            comment_kind=str(data.get("comment_kind", "")).lower(),
            status=str(data.get("status", "")),
            cases=int(data.get("cases", 0)),
            code_fingerprint=str(data.get("code_fingerprint", "")),
            git_commit=str(data.get("git_commit", "")),
            judge_model=str(data.get("judge_model", "")),
            updated_at=str(data.get("updated_at", "")),
            manifest=str(data.get("manifest", "")),
            report=str(data.get("report", "")),
            failure_type=str(data.get("failure_type", "")),
            rationale=str(data.get("rationale", "")),
            case_ids=tuple(str(case_id) for case_id in data.get("case_ids", ())),
        )

    def to_json(self) -> dict[str, Any]:
        """Return a stable JSON object for this entry."""

        return {
            "language": self.language,
            "comment_kind": self.comment_kind,
            "status": self.status,
            "cases": self.cases,
            "code_fingerprint": self.code_fingerprint,
            "git_commit": self.git_commit,
            "judge_model": self.judge_model,
            "updated_at": self.updated_at,
            "manifest": self.manifest,
            "report": self.report,
            "failure_type": self.failure_type,
            "rationale": self.rationale,
            "case_ids": list(self.case_ids),
        }


def current_code_version(
    repo_root: Path, relevant_paths: tuple[str, ...] = DEFAULT_RELEVANT_PATHS
) -> CodeVersion:
    """Return the clean committed code identity for judge validation.

    Args:
        repo_root: Repository root containing ``.git``.
        relevant_paths: Repository-relative paths included in the fingerprint.

    Returns:
        The current committed code version.

    Raises:
        DirtyRelevantCodeError: If relevant paths are not clean and committed.
        LedgerError: If git metadata cannot be read.
    """

    repo_root = repo_root.resolve()
    git_commit = _git(repo_root, "rev-parse", "HEAD").strip()
    dirty_paths = _dirty_relevant_paths(repo_root, relevant_paths)
    if dirty_paths:
        raise DirtyRelevantCodeError(dirty_paths)

    missing_paths = []
    hasher = hashlib.sha256()
    for path in relevant_paths:
        blob = _git_bytes(repo_root, "show", f"HEAD:{path}", check=False)
        if blob is None:
            missing_paths.append(path)
            continue
        hasher.update(path.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(blob)
        hasher.update(b"\0")

    if missing_paths:
        raise DirtyRelevantCodeError(missing_paths)

    return CodeVersion(
        git_commit=git_commit,
        fingerprint=hasher.hexdigest(),
        relevant_paths=tuple(relevant_paths),
    )


def load_entries(path: Path) -> list[JudgeLedgerEntry]:
    """Read ledger entries from ``path``.

    Args:
        path: Markdown ledger path.

    Returns:
        Ledger entries, or an empty list when the file does not exist or has no
        embedded payload.
    """

    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8")
    payload = _extract_payload(text)
    if payload is None:
        return []
    if int(payload.get("schema_version", 0)) != SCHEMA_VERSION:
        raise LedgerError(
            f"Unsupported comment judge ledger schema: {payload.get('schema_version')}"
        )
    entries = payload.get("entries", [])
    if not isinstance(entries, list):
        raise LedgerError("Comment judge ledger entries must be a list")
    return [JudgeLedgerEntry.from_json(entry) for entry in entries]


def find_entry(
    entries: list[JudgeLedgerEntry],
    *,
    language: str,
    comment_kind: str,
    code_fingerprint: str,
) -> JudgeLedgerEntry | None:
    """Return the latest entry for one language/kind/code version.

    Args:
        entries: Loaded ledger entries.
        language: Registry language key.
        comment_kind: Comment bucket.
        code_fingerprint: Current code fingerprint.

    Returns:
        Matching entry, or ``None``.
    """

    language = language.lower()
    comment_kind = comment_kind.lower()
    matches = [
        entry
        for entry in entries
        if entry.language == language
        and entry.comment_kind == comment_kind
        and entry.code_fingerprint == code_fingerprint
    ]
    if not matches:
        return None
    return sorted(matches, key=lambda entry: entry.updated_at)[-1]


def upsert_entry(path: Path, entry: JudgeLedgerEntry) -> None:
    """Insert or replace an entry in the Markdown ledger.

    Args:
        path: Markdown ledger path.
        entry: Entry to write.
    """

    entries = [
        existing
        for existing in load_entries(path)
        if not (
            existing.language == entry.language
            and existing.comment_kind == entry.comment_kind
            and existing.code_fingerprint == entry.code_fingerprint
        )
    ]
    entries.append(entry)
    write_entries(path, entries)


def write_entries(path: Path, entries: list[JudgeLedgerEntry]) -> None:
    """Write ``entries`` to the Markdown ledger.

    Args:
        path: Markdown ledger path.
        entries: Entries to render.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_ledger(entries), encoding="utf-8")


def clear_entries(path: Path) -> None:
    """Reset the ledger to an empty entry set.

    Args:
        path: Markdown ledger path to overwrite with an empty ledger.
    """

    write_entries(path, [])


def render_ledger(entries: list[JudgeLedgerEntry]) -> str:
    """Render the human and machine-readable ledger Markdown."""

    entries = sorted(
        entries,
        key=lambda entry: (
            entry.language,
            entry.comment_kind,
            entry.status,
            entry.updated_at,
        ),
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "entries": [entry.to_json() for entry in entries],
    }
    passed = [entry for entry in entries if entry.status == PASSED]
    failed = [entry for entry in entries if entry.status == FAILED]
    return (
        "# Stack v2 Comment Judge Validation Ledger\n\n"
        "This development-only ledger records which real-corpus Stack v2 LLM "
        "judge buckets have already run for a committed comment extraction and "
        "sanitization code version. The JSON block is the source of truth for "
        "tooling; edit entries through the judge workflow whenever possible.\n\n"
        f"{LEDGER_START}\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)}\n"
        f"{LEDGER_END}\n\n"
        "## Passed Coverage\n\n"
        f"{_render_table(passed)}\n\n"
        "## Failed Coverage\n\n"
        f"{_render_table(failed)}\n"
    )


def build_entry(
    *,
    language: str,
    comment_kind: str,
    status: str,
    cases: int,
    version: CodeVersion,
    judge_model: str,
    manifest: str = "",
    report: str = "",
    failure_type: str = "",
    rationale: str = "",
    case_ids: tuple[str, ...] = (),
) -> JudgeLedgerEntry:
    """Build a timestamped ledger entry for the current run."""

    return JudgeLedgerEntry(
        language=language.lower(),
        comment_kind=comment_kind.lower(),
        status=status,
        cases=cases,
        code_fingerprint=version.fingerprint,
        git_commit=version.git_commit,
        judge_model=judge_model,
        updated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        manifest=manifest,
        report=report,
        failure_type=failure_type,
        rationale=rationale,
        case_ids=case_ids,
    )


def summarize_manifest(path: Path) -> dict[tuple[str, str], list[str]]:
    """Return case IDs grouped by language/comment kind for a manifest."""

    grouped: dict[tuple[str, str], list[str]] = {}
    with path.open(encoding="utf-8") as infile:
        for line in infile:
            if not line.strip():
                continue
            item = json.loads(line)
            key = (
                str(item.get("language", "")).lower(),
                str(item.get("comment_kind", "")).lower(),
            )
            grouped.setdefault(key, []).append(str(item.get("case_id", "")))
    return grouped


def status_lines(
    *,
    ledger_path: Path,
    repo_root: Path,
    manifest_path: Path | None = None,
) -> list[str]:
    """Return CLI-readable status lines for the current code version."""

    version = current_code_version(repo_root)
    entries = load_entries(ledger_path)
    lines = [
        f"commit={version.git_commit}",
        f"fingerprint={version.fingerprint}",
        f"entries={len(entries)}",
    ]
    if manifest_path is None:
        return lines

    for (language, kind), case_ids in sorted(summarize_manifest(manifest_path).items()):
        entry = find_entry(
            entries,
            language=language,
            comment_kind=kind,
            code_fingerprint=version.fingerprint,
        )
        status = entry.status if entry is not None else "untested"
        report = f" report={entry.report}" if entry is not None and entry.report else ""
        lines.append(f"{language}/{kind}: {status} cases={len(case_ids)}{report}")
    return lines


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for ledger inspection."""

    parser = argparse.ArgumentParser(description="Inspect the comment judge validation ledger.")
    parser.add_argument(
        "command",
        choices=("clear", "fingerprint", "status"),
        help="Ledger operation to run.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root, defaulting to the current directory.",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=DEFAULT_LEDGER_PATH,
        help=f"Markdown ledger path. Defaults to {DEFAULT_LEDGER_PATH}.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Optional manifest to summarize against the current ledger.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirm destructive ledger reset for the clear command.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the ledger inspection CLI."""

    args = parse_args()
    try:
        if args.command == "clear":
            if not args.yes:
                print("Refusing to clear ledger without --yes")
                return 2
            clear_entries(args.ledger)
            print(f"cleared ledger: {args.ledger}")
            return 0
        if args.command == "fingerprint":
            version = current_code_version(args.repo_root)
            print(version.git_commit)
            print(version.fingerprint)
            return 0
        for line in status_lines(
            ledger_path=args.ledger,
            repo_root=args.repo_root,
            manifest_path=args.manifest,
        ):
            print(line)
        return 0
    except LedgerError as exc:
        print(exc)
        return 2


def _extract_payload(text: str) -> dict[str, Any] | None:
    start = text.find(LEDGER_START)
    if start == -1:
        return None
    start += len(LEDGER_START)
    end = text.find(LEDGER_END, start)
    if end == -1:
        raise LedgerError("Comment judge ledger JSON block is missing its end marker")
    raw_payload = text[start:end].strip()
    if not raw_payload:
        return {"schema_version": SCHEMA_VERSION, "entries": []}
    return json.loads(raw_payload)


def _render_table(entries: list[JudgeLedgerEntry]) -> str:
    header = (
        "| Language | Kind | Status | Cases | Model | Commit | Fingerprint | "
        "Report | Updated |\n"
        "| --- | --- | --- | ---: | --- | --- | --- | --- | --- |"
    )
    if not entries:
        return f"{header}\n| _none_ |  |  |  |  |  |  |  |  |"

    rows = []
    for entry in entries:
        report = _markdown_link(entry.report) if entry.report else ""
        rows.append(
            "| "
            + " | ".join(
                [
                    _escape_table(entry.language),
                    _escape_table(entry.comment_kind),
                    _escape_table(entry.status),
                    str(entry.cases),
                    _escape_table(entry.judge_model),
                    f"`{entry.git_commit[:12]}`",
                    f"`{entry.code_fingerprint[:12]}`",
                    report,
                    _escape_table(entry.updated_at),
                ]
            )
            + " |"
        )
    return "\n".join([header, *rows])


def _markdown_link(path: str) -> str:
    label = Path(path).name
    return f"[{_escape_table(label)}]({_escape_table(path)})"


def _escape_table(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _dirty_relevant_paths(repo_root: Path, relevant_paths: tuple[str, ...]) -> list[str]:
    status = _git(repo_root, "status", "--porcelain", "--", *relevant_paths)
    dirty_paths = []
    for line in status.splitlines():
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        dirty_paths.append(path)
    return dirty_paths


def _git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise LedgerError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def _git_bytes(repo_root: Path, *args: str, check: bool = True) -> bytes | None:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout
    if check:
        raise LedgerError(
            result.stderr.decode("utf-8", errors="replace").strip()
            or result.stdout.decode("utf-8", errors="replace").strip()
        )
    return None


if __name__ == "__main__":
    raise SystemExit(main())
