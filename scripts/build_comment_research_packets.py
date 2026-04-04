#!/usr/bin/env python3
"""Build online-first comment research prompt packets from chunk assignments."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = ROOT / "docs" / "comment_research"
ASSIGNMENTS_PATH = RESEARCH_DIR / "agent_chunk_assignments.json"
BACKLOG_PATH = RESEARCH_DIR / "not_done_backlog.csv"
PACKET_DIR = RESEARCH_DIR / "prompt_packets"
PLAYBOOK_PATH = RESEARCH_DIR / "online_research_playbook.md"
TEMPLATE_PATH = RESEARCH_DIR / "report_template.md"

STATUS_PRIORITY = {
    "missing_research_record": 0,
    "needs_research_or_confirmation": 1,
    "ready_to_implement": 2,
    "resolved_non_actionable": 3,
}


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

    @property
    def priority_label(self) -> str:
        if self.status in {"missing_research_record", "needs_research_or_confirmation"}:
            return "high"
        if self.status == "ready_to_implement":
            return "medium"
        return "low"


def load_assignments() -> dict:
    return json.loads(ASSIGNMENTS_PATH.read_text(encoding="utf-8"))


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
                version_specific_syntax=row.get("version_specific_syntax", "unresolved"),
                line_comments=row["line_comments"],
                block_comments=row["block_comments"],
                termination_behavior=row.get("termination_behavior", "unresolved"),
                nested_comments=row["nested_comments"],
                recommended_action=row["recommended_action"],
                docs_source=row["docs_source"],
                implementation_source=row["implementation_source"],
                report_file=row["report_file"],
            )
            backlog[entry.language] = entry
    return backlog


def status_sort_key(entry: BacklogEntry) -> tuple[int, str]:
    return STATUS_PRIORITY.get(entry.status, 99), entry.language.lower()


def format_cell(value: str) -> str:
    if not value:
        return "unresolved"
    return value.replace("|", "\\|").replace("\n", " ")


def build_chunk_packet(chunk_name: str, entries: list[BacklogEntry]) -> str:
    status_counts: dict[str, int] = {}
    for entry in entries:
        status_counts[entry.status] = status_counts.get(entry.status, 0) + 1

    lines = [
        f"# Online Comment Research Prompt: `{chunk_name}`",
        "",
        "Use this packet together with:",
        f"- [online_research_playbook.md]({PLAYBOOK_PATH.relative_to(ROOT)})",
        f"- [report_template.md]({TEMPLATE_PATH.relative_to(ROOT)})",
        "",
        "## Mission",
        "",
        (
            "Go online for every language in this chunk. Search official documentation first "
            "to find the language's definition of comments. If that fails or remains ambiguous, "
            "inspect an implementation source. If that still leaves uncertainty, use a search "
            "engine with the language name plus `programming language` and `comment` to find "
            "secondary sources such as Stack Overflow answers or blog posts. If that still "
            "does not resolve the syntax, download real files for the language and inspect "
            "them for likely comments. Do not stop at a single source: reconcile multiple "
            "sources and explicitly look for version-specific or dialect-specific differences."
        ),
        "",
        "Target output file:",
        f"- `docs/comment_research/{chunk_name}_report.md`",
        "",
        "## Priority Summary",
        "",
        f"- Assigned languages: `{len(entries)}`",
        (
            "- Needs research or confirmation: "
            f"`{status_counts.get('needs_research_or_confirmation', 0)}`"
        ),
        (
            "- Ready to implement but should be strengthened with source evidence: "
            f"`{status_counts.get('ready_to_implement', 0)}`"
        ),
        f"- Resolved non-actionable: `{status_counts.get('resolved_non_actionable', 0)}`",
        "",
        "## Required Workflow",
        "",
        "1. Search official docs for comment syntax.",
        "2. Check more than one source whenever possible.",
        (
            "3. If the language has versioned docs, historical manuals, standards, or dialects, "
            "compare current syntax with at least one older or alternate version source."
        ),
        "4. Cross-check with an implementation source when available.",
        (
            "5. If syntax is still unclear, search the web with the language name plus "
            "`programming language` and `comment` to find Stack Overflow answers, blog posts, "
            "tutorials, or issue threads."
        ),
        (
            "6. If syntax is still unclear after that, download real source files "
            "and inspect them directly."
        ),
        (
            "7. For every language, explicitly classify line comments, block comments, "
            "block-comment delimiter behavior, and version-specific variants."
        ),
        (
            "8. Record whether block comments terminate at the first closer, support true "
            "nesting, or use depth-qualified delimiters."
        ),
        (
            "9. When versions differ, record the exact version scope and recommend whether "
            "the registry should implement the union of all confirmed forms."
        ),
        "10. Keep real surrounding-code examples for each supported comment form.",
        "11. Do not guess. Mark unresolved when the evidence is not strong enough.",
        "",
        "## Language Queue",
        "",
        (
            "| Priority | Language | Registry key | Current status | Confidence | "
            "Current version scope | Current version syntax | Current line | Current block | "
            "Current termination | Current nested | Existing docs source | Existing impl source | "
            "Current recommendation |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for entry in sorted(entries, key=status_sort_key):
        lines.append(
            "| {priority} | {language} | {registry_key} | {status} | {confidence} | "
            "{version_scope} | {version_syntax} | {line} | {block} | {termination} | "
            "{nested} | {docs} | {impl} | {action} |".format(
                priority=format_cell(entry.priority_label),
                language=format_cell(entry.language),
                registry_key=format_cell(entry.registry_key),
                status=format_cell(entry.status),
                confidence=format_cell(entry.confidence),
                version_scope=format_cell(entry.version_scope),
                version_syntax=format_cell(entry.version_specific_syntax),
                line=format_cell(entry.line_comments),
                block=format_cell(entry.block_comments),
                termination=format_cell(entry.termination_behavior),
                nested=format_cell(entry.nested_comments),
                docs=format_cell(entry.docs_source),
                impl=format_cell(entry.implementation_source),
                action=format_cell(entry.recommended_action),
            )
        )

    lines.extend(
        [
            "",
            "## Search Guidance",
            "",
            "For each language, try at least these query patterns before falling back:",
            '- `"<Language> programming language comments syntax"`',
            '- `"<Language> programming language reference comments"`',
            '- `"<Language> programming language lexical grammar comments"`',
            '- `"<Language> programming language line comment block comment"`',
            '- `"<Language> programming language nested comments"`',
            '- `"<Language> programming language block comment delimiter"`',
            '- `"<Language> programming language version comment syntax"`',
            '- `"<Language> programming language legacy comment syntax"`',
            '- `"<Language> programming language old version comments"`',
            "",
            "If the docs are unclear, search for:",
            "- lexer or tokenizer definitions",
            "- parser or grammar rules",
            "- archived docs or versioned manuals",
            "- release notes or standards editions",
            "- official examples or language test corpora",
            "",
            "If official sources are still unclear, run a search-engine pass such as:",
            '- `"<Language> programming language comment"`',
            '- `"<Language> programming language comments"`',
            '- `"<Language> programming language block comment"`',
            '- `"<Language> programming language nested comment"`',
            '- `"<Language> programming language version comment syntax"`',
            '- `"<Language> programming language legacy comment syntax"`',
            '- `"site:stackoverflow.com <Language> programming language comment"`',
            '- `"site:stackoverflow.com <Language> programming language block comment"`',
            '- `"site:stackoverflow.com <Language> programming language nested comment"`',
            '- `"<Language> programming language comment blog"`',
            '- `"<Language> programming language comment tutorial"`',
            "",
            "When you use Stack Overflow or blog posts:",
            "- prefer answers with concrete code examples",
            "- treat them as corroboration, not as the strongest source",
            "- note contradictions with official docs explicitly",
            "- note which version or dialect the answer is describing",
            "",
            (
                "If you still cannot resolve the syntax, download multiple real files "
                "and inspect them."
            ),
            "",
            "## Output Constraints",
            "",
            "- Preserve the per-language markdown section format from `report_template.md`.",
            (
                "- Every language entry must state line comments, block comments, "
                "termination behavior, nested-comment support, version scope, and "
                "version-specific differences explicitly."
            ),
            (
                "- Keep the core fields used by the backlog scripts: `Registry key`, "
                "`Version scope`, `Version-specific syntax`, `Line comments`, "
                "`Block comments`, `Nested comments`, `Confidence`, `Docs source`, "
                "`Implementation source`, `Recommended action`, and `Notes`."
            ),
            (
                "- You may add `Evidence mode`, `Community source`, and "
                "`Corpus fallback source`; "
                "downstream scripts will ignore those extra fields safely."
            ),
            (
                "- You may also add `Termination behavior`; downstream scripts will ignore "
                "that extra field safely."
            ),
            "- Prefer direct source URLs over generic site homepages.",
        ]
    )

    return "\n".join(lines) + "\n"


def build_index(assignments: dict, backlog: dict[str, BacklogEntry]) -> str:
    lines = [
        "# Prompt Packets",
        "",
        (
            "Generated by `scripts/build_comment_research_packets.py`. Do not edit "
            "this directory by hand."
        ),
        "",
        (
            "These packets are for the stronger online-first research workflow. "
            "Each packet tells a worker to search official documentation first, "
            "then implementation sources, then downloaded real files when necessary, "
            "while also checking for version-specific comment syntax differences."
        ),
        "",
        "## Packets",
        "",
        (
            "| Chunk | Languages | Needs research | Ready to implement | "
            "Resolved non-actionable | Prompt |"
        ),
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for chunk_name, languages in assignments["chunks"].items():
        entries = [backlog[language] for language in languages if language in backlog]
        counts = {
            "needs_research_or_confirmation": 0,
            "ready_to_implement": 0,
            "resolved_non_actionable": 0,
        }
        for entry in entries:
            if entry.status in counts:
                counts[entry.status] += 1
        prompt_path = f"docs/comment_research/prompt_packets/{chunk_name}_prompt.md"
        lines.append(
            f"| {chunk_name} | {len(entries)} | "
            f"{counts['needs_research_or_confirmation']} | "
            f"{counts['ready_to_implement']} | "
            f"{counts['resolved_non_actionable']} | "
            f"[{chunk_name}_prompt.md](/home/jonathan/Documents/PhD/ML4SE-toolkit/{prompt_path}) |"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    assignments = load_assignments()
    backlog = load_backlog()
    PACKET_DIR.mkdir(parents=True, exist_ok=True)

    for chunk_name, languages in assignments["chunks"].items():
        entries = [backlog[language] for language in languages if language in backlog]
        packet_path = PACKET_DIR / f"{chunk_name}_prompt.md"
        packet_path.write_text(build_chunk_packet(chunk_name, entries), encoding="utf-8")
        print(f"Wrote {packet_path.relative_to(ROOT)}")

    index_path = PACKET_DIR / "README.md"
    index_path.write_text(build_index(assignments, backlog), encoding="utf-8")
    print(f"Wrote {index_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
