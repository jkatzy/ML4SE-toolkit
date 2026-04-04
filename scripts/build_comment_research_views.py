#!/usr/bin/env python3
"""Build derived backlog and candidate views from Stack v2 comment research."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Sequence

from ml4setk import get_supported_comment_languages

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = ROOT / "docs" / "comment_research"
ASSIGNMENTS_PATH = RESEARCH_DIR / "agent_chunk_assignments.json"
REPORT_GLOB = "chunk_*_report.md"
BACKLOG_MD_PATH = RESEARCH_DIR / "not_done_backlog.md"
BACKLOG_CSV_PATH = RESEARCH_DIR / "not_done_backlog.csv"
CANDIDATES_MD_PATH = RESEARCH_DIR / "registry_ready_candidates.md"
CANDIDATES_CSV_PATH = RESEARCH_DIR / "registry_ready_candidates.csv"

FIELD_NAMES = (
    "Registry key",
    "Version scope",
    "Version-specific syntax",
    "Line comments",
    "Block comments",
    "Termination behavior",
    "Nested comments",
    "Confidence",
    "Docs source",
    "Implementation source",
    "Recommended action",
    "Notes",
)
SECTION_RE = re.compile(r"^##\s+(?P<name>.+?)\s*$")
BULLET_RE = re.compile(r"^-\s+(?P<field>[^:]+):\s*(?P<value>.*)$")
READY_CONFIDENCE = {"high", "verified", "cross-checked"}
BLOCKER_KEYWORDS = (
    "research",
    "verify",
    "confirm",
    "manual",
    "clarify",
    "unresolved",
    "investigate",
    "follow up",
)
UNSUPPORTED_MARKERS = {
    "",
    "unsupported",
    "unresolved",
    "none",
    "n/a",
    "not applicable",
    "commentless",
}


@dataclass(frozen=True)
class LanguageRecord:
    language: str
    registry_key: str
    version_scope: str
    version_specific_syntax: str
    line_comments: str
    block_comments: str
    termination_behavior: str
    nested_comments: str
    confidence: str
    docs_source: str
    implementation_source: str
    recommended_action: str
    notes: str
    report_file: str

    @property
    def supported(self) -> bool:
        return any(
            is_supported_syntax(value)
            for value in (self.line_comments, self.block_comments, self.nested_comments)
        )

    @property
    def confidence_key(self) -> str:
        return self.confidence.strip().lower()


def normalize_text(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        value = value[1:-1]
    return value.strip()


def normalize_language_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def is_supported_syntax(value: str) -> bool:
    compact = normalize_text(value).lower()
    return compact not in UNSUPPORTED_MARKERS


def action_has_blocker(action: str) -> bool:
    lowered = action.lower()
    return any(keyword in lowered for keyword in BLOCKER_KEYWORDS)


def load_expected_languages() -> List[str]:
    payload = json.loads(ASSIGNMENTS_PATH.read_text(encoding="utf-8"))
    languages: List[str] = []
    for chunk in payload["chunks"].values():
        languages.extend(chunk)
    return sorted(dict.fromkeys(languages))


def load_supported_registry_keys() -> set[str]:
    return set(get_supported_comment_languages())


def parse_reports(expected_languages: Sequence[str]) -> Dict[str, LanguageRecord]:
    expected_exact = set(expected_languages)
    expected_by_normalized = {
        normalize_language_key(language): language for language in expected_languages
    }
    parsed: Dict[str, LanguageRecord] = {}

    for report_path in sorted(RESEARCH_DIR.glob(REPORT_GLOB)):
        current_name: str | None = None
        current_fields: Dict[str, str] = {}

        def flush_current() -> None:
            nonlocal current_name, current_fields
            if not current_name or "Registry key" not in current_fields:
                current_name = None
                current_fields = {}
                return

            language = current_name
            if language not in expected_exact:
                language = expected_by_normalized.get(normalize_language_key(language), "")
            if not language:
                current_name = None
                current_fields = {}
                return

            record = LanguageRecord(
                language=language,
                registry_key=normalize_text(current_fields.get("Registry key", "")),
                version_scope=normalize_text(current_fields.get("Version scope", "")),
                version_specific_syntax=normalize_text(
                    current_fields.get("Version-specific syntax", "")
                ),
                line_comments=normalize_text(current_fields.get("Line comments", "")),
                block_comments=normalize_text(current_fields.get("Block comments", "")),
                termination_behavior=normalize_text(
                    current_fields.get("Termination behavior", "unresolved")
                ),
                nested_comments=normalize_text(current_fields.get("Nested comments", "")),
                confidence=normalize_text(current_fields.get("Confidence", "")),
                docs_source=normalize_text(current_fields.get("Docs source", "")),
                implementation_source=normalize_text(
                    current_fields.get("Implementation source", "")
                ),
                recommended_action=normalize_text(
                    current_fields.get("Recommended action", "")
                ),
                notes=normalize_text(current_fields.get("Notes", "")),
                report_file=str(report_path.relative_to(ROOT)),
            )
            parsed[language] = record
            current_name = None
            current_fields = {}

        for raw_line in report_path.read_text(encoding="utf-8").splitlines():
            section_match = SECTION_RE.match(raw_line)
            if section_match:
                flush_current()
                current_name = section_match.group("name")
                continue

            if current_name is None:
                continue

            bullet_match = BULLET_RE.match(raw_line)
            if bullet_match:
                field = bullet_match.group("field").strip()
                if field in FIELD_NAMES:
                    current_fields[field] = bullet_match.group("value").strip()

        flush_current()

    return parsed


def classify_status(record: LanguageRecord) -> str:
    if record.confidence_key in READY_CONFIDENCE:
        if record.supported and not action_has_blocker(record.recommended_action):
            return "ready_to_implement"
        if not record.supported:
            return "resolved_non_actionable"
    return "needs_research_or_confirmation"


def build_backlog_rows(
    expected_languages: Sequence[str], parsed_records: Dict[str, LanguageRecord]
) -> List[dict]:
    rows: List[dict] = []
    for language in expected_languages:
        record = parsed_records.get(language)
        if record is None:
            rows.append(
                {
                    "language": language,
                    "registry_key": "",
                    "status": "missing_research_record",
                    "confidence": "",
                    "version_scope": "unresolved",
                    "version_specific_syntax": "unresolved",
                    "line_comments": "unresolved",
                    "block_comments": "unresolved",
                    "termination_behavior": "unresolved",
                    "nested_comments": "unresolved",
                    "recommended_action": "Add a research record for this language.",
                    "docs_source": "",
                    "implementation_source": "",
                    "report_file": "",
                }
            )
            continue

        rows.append(
            {
                "language": record.language,
                "registry_key": record.registry_key,
                "status": classify_status(record),
                "confidence": record.confidence,
                "version_scope": record.version_scope,
                "version_specific_syntax": record.version_specific_syntax,
                "line_comments": record.line_comments,
                "block_comments": record.block_comments,
                "termination_behavior": record.termination_behavior,
                "nested_comments": record.nested_comments,
                "recommended_action": record.recommended_action,
                "docs_source": record.docs_source,
                "implementation_source": record.implementation_source,
                "report_file": record.report_file,
            }
        )

    return rows


def filter_unimplemented_rows(rows: Sequence[dict], supported_keys: set[str]) -> List[dict]:
    return [row for row in rows if row["registry_key"] not in supported_keys]


def write_csv(path: Path, rows: Sequence[dict]) -> None:
    fieldnames = [
        "language",
        "registry_key",
        "status",
        "confidence",
        "version_scope",
        "version_specific_syntax",
        "line_comments",
        "block_comments",
        "termination_behavior",
        "nested_comments",
        "recommended_action",
        "docs_source",
        "implementation_source",
        "report_file",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def format_table(rows: Sequence[dict]) -> List[str]:
    header = (
        (
            "| Language | Registry key | Confidence | Version scope | Version syntax | "
            "Line | Block | Termination | Nested | Action | Report |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    )
    body = []
    for row in rows:
        body.append(
            "| {language} | {registry_key} | {confidence} | {version_scope} | "
            "{version_specific_syntax} | {line_comments} | {block_comments} | "
            "{termination_behavior} | {nested_comments} | {recommended_action} | "
            "{report_file} |".format(
                language=escape_cell(row["language"]),
                registry_key=escape_cell(row["registry_key"]),
                confidence=escape_cell(row["confidence"]),
                version_scope=escape_cell(row["version_scope"]),
                version_specific_syntax=escape_cell(row["version_specific_syntax"]),
                line_comments=escape_cell(row["line_comments"]),
                block_comments=escape_cell(row["block_comments"]),
                termination_behavior=escape_cell(row["termination_behavior"]),
                nested_comments=escape_cell(row["nested_comments"]),
                recommended_action=escape_cell(row["recommended_action"]),
                report_file=escape_cell(row["report_file"]),
            )
        )
    return [*header, *body]


def write_backlog_markdown(path: Path, rows: Sequence[dict]) -> None:
    grouped = {
        "ready_to_implement": sorted(
            (row for row in rows if row["status"] == "ready_to_implement"),
            key=lambda row: row["language"].lower(),
        ),
        "needs_research_or_confirmation": sorted(
            (row for row in rows if row["status"] == "needs_research_or_confirmation"),
            key=lambda row: row["language"].lower(),
        ),
        "resolved_non_actionable": sorted(
            (row for row in rows if row["status"] == "resolved_non_actionable"),
            key=lambda row: row["language"].lower(),
        ),
        "missing_research_record": sorted(
            (row for row in rows if row["status"] == "missing_research_record"),
            key=lambda row: row["language"].lower(),
        ),
    }

    lines = [
        "# Stack v2 Comment Backlog",
        "",
        "Generated by `scripts/build_comment_research_views.py`. Do not edit this file by hand.",
        "",
        (
            "This backlog covers Stack v2 public languages that are still not represented in the "
            "current comment registry."
        ),
        "",
        "## Summary",
        "",
        f"- Generated on: `{date.today().isoformat()}`",
        f"- Total uncovered languages tracked: `{len(rows)}`",
        f"- Ready to implement now: `{len(grouped['ready_to_implement'])}`",
        f"- Needs research or confirmation: `{len(grouped['needs_research_or_confirmation'])}`",
        f"- Resolved non-actionable: `{len(grouped['resolved_non_actionable'])}`",
        f"- Missing research records: `{len(grouped['missing_research_record'])}`",
        "",
        "Status definitions:",
        (
            "- `ready_to_implement`: high-confidence syntax with at least one supported comment "
            "form and no explicit research blocker in the recommendation."
        ),
        (
            "- `needs_research_or_confirmation`: still needs verification, disambiguation, or "
            "stronger evidence before adding to the registry."
        ),
        (
            "- `resolved_non_actionable`: high-confidence result that the format is commentless "
            "or otherwise unsupported by the current parser model."
        ),
        (
            "- `missing_research_record`: the language is in the Stack v2 uncovered inventory "
            "but has no parsed report entry yet."
        ),
        "",
        "## Ready To Implement",
        "",
    ]
    lines.extend(format_table(grouped["ready_to_implement"]))
    lines.extend(
        [
            "",
            "## Needs Research Or Confirmation",
            "",
        ]
    )
    lines.extend(format_table(grouped["needs_research_or_confirmation"]))
    lines.extend(
        [
            "",
            "## Resolved Non-Actionable",
            "",
        ]
    )
    lines.extend(format_table(grouped["resolved_non_actionable"]))
    if grouped["missing_research_record"]:
        lines.extend(
            [
                "",
                "## Missing Research Records",
                "",
            ]
        )
        lines.extend(format_table(grouped["missing_research_record"]))

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_candidate_markdown(path: Path, rows: Sequence[dict]) -> None:
    lines = [
        "# Registry-Ready Comment Candidates",
        "",
        "Generated by `scripts/build_comment_research_views.py`. Do not edit this file by hand.",
        "",
        (
            "These languages are not yet implemented in the current registry, but the research "
            "reports indicate they are the strongest next candidates for implementation and test "
            "generation."
        ),
        "",
        "## Summary",
        "",
        f"- Generated on: `{date.today().isoformat()}`",
        f"- Candidate count: `{len(rows)}`",
        "",
        "## Candidates",
        "",
    ]
    lines.extend(format_table(rows))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    expected_languages = load_expected_languages()
    supported_keys = load_supported_registry_keys()
    parsed_records = parse_reports(expected_languages)
    backlog_rows = filter_unimplemented_rows(
        build_backlog_rows(expected_languages, parsed_records),
        supported_keys,
    )

    ready_rows = sorted(
        (row for row in backlog_rows if row["status"] == "ready_to_implement"),
        key=lambda row: row["language"].lower(),
    )

    write_csv(BACKLOG_CSV_PATH, backlog_rows)
    write_csv(CANDIDATES_CSV_PATH, ready_rows)
    write_backlog_markdown(BACKLOG_MD_PATH, backlog_rows)
    write_candidate_markdown(CANDIDATES_MD_PATH, ready_rows)

    print(f"Wrote {BACKLOG_MD_PATH.relative_to(ROOT)}")
    print(f"Wrote {BACKLOG_CSV_PATH.relative_to(ROOT)}")
    print(f"Wrote {CANDIDATES_MD_PATH.relative_to(ROOT)}")
    print(f"Wrote {CANDIDATES_CSV_PATH.relative_to(ROOT)}")
    print(f"Tracked uncovered languages: {len(backlog_rows)}")
    print(f"Registry-ready candidates: {len(ready_rows)}")


if __name__ == "__main__":
    main()
