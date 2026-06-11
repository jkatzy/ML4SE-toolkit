#!/usr/bin/env python3
"""Build implementation-confirmation prompt packets from comment backlog rows."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = ROOT / "docs" / "comment_research"
ASSIGNMENTS_PATH = RESEARCH_DIR / "agent_chunk_assignments.json"
BACKLOG_PATH = RESEARCH_DIR / "not_done_backlog.csv"
PACKET_DIR = RESEARCH_DIR / "confirmation_packets"
REPORT_DIR = RESEARCH_DIR / "confirmation_reports"
PLAYBOOK_PATH = RESEARCH_DIR / "implementation_confirmation_playbook.md"
TEMPLATE_PATH = RESEARCH_DIR / "confirmation_report_template.md"
TARGET_STATUS = "needs_research_or_confirmation"


@dataclass(frozen=True)
class BacklogEntry:
    language: str
    registry_key: str
    status: str
    confidence: str
    version_scope: str
    version_specific_syntax: str
    line_comments: str
    block_comments: str
    termination_behavior: str
    nested_comments: str
    recommended_action: str
    docs_source: str
    implementation_source: str
    report_file: str


def load_assignments() -> dict[str, list[str]]:
    payload = json.loads(ASSIGNMENTS_PATH.read_text(encoding="utf-8"))
    return payload["chunks"]


def load_backlog() -> dict[str, BacklogEntry]:
    backlog: dict[str, BacklogEntry] = {}
    with BACKLOG_PATH.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            entry = BacklogEntry(
                language=row["language"],
                registry_key=row["registry_key"],
                status=row["status"],
                confidence=row["confidence"],
                version_scope=row.get("version_scope", "unresolved"),
                version_specific_syntax=row.get(
                    "version_specific_syntax", "unresolved"
                ),
                line_comments=row["line_comments"],
                block_comments=row["block_comments"],
                termination_behavior=row.get(
                    "termination_behavior", "unresolved"
                ),
                nested_comments=row["nested_comments"],
                recommended_action=row["recommended_action"],
                docs_source=row["docs_source"],
                implementation_source=row["implementation_source"],
                report_file=row["report_file"],
            )
            backlog[entry.language] = entry
    return backlog


def format_cell(value: str) -> str:
    if not value:
        return "unresolved"
    return value.replace("|", "\\|").replace("\n", " ")


def confirmation_report_path(chunk_name: str) -> str:
    return f"docs/comment_research/confirmation_reports/{chunk_name}_confirmation.md"


def build_chunk_packet(chunk_name: str, entries: list[BacklogEntry]) -> str:
    output_path = confirmation_report_path(chunk_name)
    lines = [
        f"# Implementation Confirmation Prompt: `{chunk_name}`",
        "",
        "Use this packet together with:",
        f"- [implementation_confirmation_playbook.md]({PLAYBOOK_PATH.relative_to(ROOT)})",
        f"- [confirmation_report_template.md]({TEMPLATE_PATH.relative_to(ROOT)})",
        "",
        "## Mission",
        "",
        (
            "Confirm only the `needs_research_or_confirmation` entries in this "
            "packet by downloading a real language implementation, locating a "
            "designated hello-world or equivalent parser fixture, adding scratch "
            "comment probes, and parsing or tokenizing those scratch files with "
            "the implementation."
        ),
        "",
        "Target output file:",
        f"- `{output_path}`",
        "",
        "Allowed committed edit scope:",
        f"- `{output_path}`",
        "",
        "Scratch/output scope:",
        f"- `tmp/comment_research_confirmation/{chunk_name}/`",
        "",
        "Do not edit `src/`, `tests/`, `registry.py`, original chunk reports, "
        "backlog/candidate views, or other confirmation reports.",
        "",
        "## Required Workflow",
        "",
        "1. Read the playbook and template completely.",
        "2. For each language, read the current source report entry first.",
        (
            "3. Download or clone the official implementation, grammar, lexer, "
            "parser, or syntax tool into the chunk scratch directory."
        ),
        (
            "4. Locate the designated hello-world file using the playbook's "
            "source order. If none exists, record `blocked` with searched paths."
        ),
        (
            "5. Build minimal scratch copies of the hello-world file with line, "
            "block, nested, and negative probes as applicable."
        ),
        (
            "6. Run a parse-only, tokenize-only, syntax-check, or "
            "compile-without-run command from the downloaded implementation."
        ),
        (
            "7. Record exact commands, local scratch paths, result summaries, "
            "and a verdict: `confirmed`, `partially-confirmed`, `contradicted`, "
            "or `blocked`."
        ),
        (
            "8. If contradicted, recommend the smallest next action without "
            "changing production code or registry entries."
        ),
        "",
        "## Language Queue",
        "",
        (
            "| Language | Registry key | Confidence | Current version scope | "
            "Current version syntax | Current line | Current block | "
            "Current termination | Current nested | Source report | Docs source | "
            "Implementation source | Current recommendation |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for entry in sorted(entries, key=lambda item: item.language.lower()):
        lines.append(
            "| {language} | {registry_key} | {confidence} | {version_scope} | "
            "{version_syntax} | {line} | {block} | {termination} | {nested} | "
            "{report} | {docs} | {impl} | {action} |".format(
                language=format_cell(entry.language),
                registry_key=format_cell(entry.registry_key),
                confidence=format_cell(entry.confidence),
                version_scope=format_cell(entry.version_scope),
                version_syntax=format_cell(entry.version_specific_syntax),
                line=format_cell(entry.line_comments),
                block=format_cell(entry.block_comments),
                termination=format_cell(entry.termination_behavior),
                nested=format_cell(entry.nested_comments),
                report=format_cell(entry.report_file),
                docs=format_cell(entry.docs_source),
                impl=format_cell(entry.implementation_source),
                action=format_cell(entry.recommended_action),
            )
        )

    lines.extend(
        [
            "",
            "## Output Constraints",
            "",
            "- Use one `## <Language>` section per assigned language.",
            (
                "- Keep every field from `confirmation_report_template.md`, "
                "including blocked fields."
            ),
            (
                "- Do not claim confirmation from source inspection alone; the "
                "implementation must parse or tokenize the scratch file."
            ),
            (
                "- Keep downloaded implementations and full command logs under "
                "`tmp/comment_research_confirmation/`."
            ),
            "- Leave unrelated worktree changes untouched.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_index(chunks: dict[str, list[BacklogEntry]]) -> str:
    lines = [
        "# Implementation Confirmation Packets",
        "",
        (
            "Generated by `scripts/build_comment_confirmation_packets.py`. Do "
            "not edit this directory by hand."
        ),
        "",
        (
            "These packets are for the implementation-confirmation researcher. "
            "They include only backlog entries whose current status is "
            "`needs_research_or_confirmation`."
        ),
        "",
        "## Packets",
        "",
        "| Chunk | Languages | Prompt | Confirmation report |",
        "| --- | --- | --- | --- |",
    ]

    for chunk_name, entries in chunks.items():
        packet_path = f"{chunk_name}_confirmation_prompt.md"
        report_path = confirmation_report_path(chunk_name)
        lines.append(
            f"| {chunk_name} | {len(entries)} | "
            f"[{packet_path}]({packet_path}) | "
            f"`{report_path}` |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    assignments = load_assignments()
    backlog = load_backlog()
    chunks: dict[str, list[BacklogEntry]] = {}

    for chunk_name, languages in assignments.items():
        entries = [
            backlog[language]
            for language in languages
            if language in backlog and backlog[language].status == TARGET_STATUS
        ]
        if entries:
            chunks[chunk_name] = entries

    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    for chunk_name, entries in chunks.items():
        packet_path = PACKET_DIR / f"{chunk_name}_confirmation_prompt.md"
        packet_path.write_text(build_chunk_packet(chunk_name, entries), encoding="utf-8")
        print(f"Wrote {packet_path.relative_to(ROOT)}")

    index_path = PACKET_DIR / "README.md"
    index_path.write_text(build_index(chunks), encoding="utf-8")
    print(f"Wrote {index_path.relative_to(ROOT)}")
    print(f"Confirmation chunks: {len(chunks)}")
    print(f"Confirmation languages: {sum(len(entries) for entries in chunks.values())}")


if __name__ == "__main__":
    main()
