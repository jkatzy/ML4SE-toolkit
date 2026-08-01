#!/usr/bin/env python3
"""Build reproducible Stack v3 full comment-research packets.

The downloaded inventories, assignments, and prompts are run artifacts and are
written below ``tmp/`` by default. Reviewed research records belong under
``docs/comment_research``; raw provider data and agent transcripts do not.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from ml4setk.Parsing.Comments.registry import (
    COMMENT_SYNTAXES,
    LANGUAGE_SYNTAX,
    _language_lookup_candidates,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "tmp" / "stack_v3_comment_research"

STACK_V3_DATASET = "HuggingFaceCode/stack-v3-full"
STACK_V3_STATS_REPOSITORY = "HuggingFaceCode/stack-v3-train"
STACK_V3_REVISION = "716a043a6c2adc34a2032b159364908a09ffe4ec"
STACK_V3_FULL_STATS_SHA256 = (
    "804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45"
)
STACK_V3_FULL_STATS_URL = (
    "https://huggingface.co/datasets/"
    f"{STACK_V3_STATS_REPOSITORY}/resolve/{STACK_V3_REVISION}/"
    "stats/full/stats_by_language.json"
)

STACK_V2_DATASET = "bigcode/the-stack-v2"
STACK_V2_REVISION = "73b0f1021c37437752281cf0736003f0c987ccc1"
STACK_V2_METADATA_URL = (
    f"https://huggingface.co/api/datasets/{STACK_V2_DATASET}/revision/{STACK_V2_REVISION}"
)

EXPECTED_FULL_LANGUAGE_COUNT = 770
DEFAULT_CHUNK_COUNT = 12

# The original Stack v2 public inventory used by this repository contained 607
# exact labels. These five are absent there but present in the later 658-config
# Hub catalog, so they receive an explicit discrepancy review instead of being
# silently classified as old or new by whichever v2 source happens to be used.
STACK_V2_PUBLIC_INVENTORY_REVISION = "92027cf260319374d2c7dae4ced6d7d0c43fd5b2"
STACK_V2_PUBLIC_INVENTORY_SHA256 = (
    "38bad9d6b614f684ac4a83a9bb9bdf776fa92ed992de515c8bbf1f69ebb8438b"
)
INVENTORY_DISCREPANCY_LABELS = (
    "Befunge",
    "C-ObjDump",
    "Darcs Patch",
    "Gemini",
    "Python traceback",
)

# Keep confirmed mapping defects in the research handoff even after their small
# runtime fix lands, so the evidence review remains auditable.
MAPPING_REVIEW_LABELS = (
    "F*",
    "Genero 4gl",
    "Genero per",
    "Go Workspace",
    "Gradle Kotlin DSL",
    "Lean 4",
    "Rocq Prover",
    "Visual Basic 6.0",
)

# This is the immutable primary queue produced from the registry baseline
# recorded in docs/comment_research/stack_v3_full/README.md. Keep it pinned so
# implementing a label does not erase its research assignment on the next run.
STACK_V3_PRIMARY_INTAKE_LABELS = (
    "Aiken",
    "Answer Set Programming",
    "B4X",
    "BibTeX Style",
    "Bluespec BH",
    "BQN",
    "BuildStream",
    "Caddyfile",
    "Cairo Zero",
    "Carbon",
    "Circom",
    "Clue",
    "Cpp-ObjDump",
    "crontab",
    "Cylc",
    "Cypher",
    "D-ObjDump",
    "D2",
    "Daslang",
    "Dotenv",
    "Dune",
    "Ecmarkup",
    "Edge",
    "EdgeQL",
    "F*",
    "FIRRTL",
    "GDShader",
    "Genero 4gl",
    "Genero per",
    "Glimmer JS",
    "Glimmer TS",
    "Go Workspace",
    "Godot Resource",
    "Gradle Kotlin DSL",
    "Hare",
    "HIP",
    "Hosts File",
    "iCalendar",
    "Imba",
    "Ink",
    "ISPC",
    "Jai",
    "Java Template Engine",
    "JCL",
    "Just",
    "KDL",
    "KerboScript",
    "Kickstart",
    "Koka",
    "Lean 4",
    "Leo",
    "Linear Programming",
    "LiveCode Script",
    "Luau",
    "M3U",
    "mdsvex",
    "MDX",
    "Mermaid",
    "MiniZinc",
    "MiniZinc Data",
    "Mojo",
    "MoonBit",
    "NMODL",
    "Noir",
    "Nushell",
    "OASv2-json",
    "OASv2-yaml",
    "OASv3-json",
    "OASv3-yaml",
    "Oberon",
    "OMNeT++ MSG",
    "OMNeT++ NED",
    "Option List",
    "OverpassQL",
    "Pact",
    "PDDL",
    "Pip Requirements",
    "Pkl",
    "Polar",
    "Praat",
    "Pyret",
    "QuickBASIC",
    "RBS",
    "Rez",
    "Roc",
    "Rocq Prover",
    "RON",
    "Sail",
    "Scenic",
    "Simple File Verification",
    "Slang",
    "Slint",
    "Smithy",
    "Snakemake",
    "Survex data",
    "Sway",
    "Sweave",
    "Tact",
    "templ",
    "Terraform Template",
    "TextGrid",
    "TL-Verilog",
    "Toit",
    "Tor Config",
    "Tree-sitter Query",
    "TSPLIB data",
    "TypeSpec",
    "Typst",
    "Untyped Plutus Core",
    "vCard",
    "Vento",
    "Visual Basic 6.0",
    "WebAssembly Interface Type",
    "WGSL",
    "Xmake",
    "Zmodel",
)


@dataclass(frozen=True)
class LanguageRecord:
    """One exact Stack v3 label and its local registry disposition."""

    language: str
    repo_count: int
    file_count: int
    total_size_bytes: int
    estimated_tokens: int
    registry_status: str
    registry_key: str | None
    v2_status: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build pinned Stack v3 full comment-research packets."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Untracked output directory for inventories, assignments, and prompts.",
    )
    parser.add_argument(
        "--chunk-count",
        type=int,
        default=DEFAULT_CHUNK_COUNT,
        help="Number of deterministic research batches.",
    )
    parser.add_argument(
        "--stats-json",
        type=Path,
        help="Read a previously downloaded full statistics payload instead of fetching it.",
    )
    parser.add_argument(
        "--v2-metadata-json",
        type=Path,
        help="Read pinned Stack v2 Hub metadata from disk instead of fetching it.",
    )
    parser.add_argument(
        "--skip-stats-hash-check",
        action="store_true",
        help="Allow a local fixture payload whose hash differs from the official pinned payload.",
    )
    return parser.parse_args(argv)


def _read_url(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "ml4setk-research/1"})
    with urllib.request.urlopen(request) as response:  # noqa: S310 - pinned HTTPS source
        return response.read()


def _read_payload(path: Path | None, url: str) -> bytes:
    return path.read_bytes() if path is not None else _read_url(url)


def _load_json(payload: bytes, source: str) -> Any:
    try:
        return json.loads(payload)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON from {source}: {error}") from error


def _registry_match(label: str) -> tuple[str, str | None]:
    canonical_names = {syntax.canonical_name for syntax in COMMENT_SYNTAXES}
    candidates = _language_lookup_candidates(label)
    match = next((key for key in candidates if key in LANGUAGE_SYNTAX), None)
    if match is None:
        return "missing", None
    directness = "direct" if match == candidates[0] else "normalized"
    key_kind = "canonical" if match in canonical_names else "alias"
    return f"{directness}_{key_kind}", match


def _language_identity(label: str) -> str:
    """Return the comparison identity used by the prior Stack v2 pipeline.

    Stack v2 encoded sharp-family config names as ``*-Sharp`` while go-enry
    emits symbols in row labels. Keep those known transport renames together.
    Other punctuation changes remain in the research queue so mapping failures,
    such as ``F*`` versus ``f_star``, are reviewed explicitly.
    """

    key = _language_lookup_candidates(label)[-1]
    return {
        "c_sharp": "csharp",
        "f_sharp": "fsharp",
        "q_sharp": "qsharp",
    }.get(key, key)


def _v2_config_names(metadata: Any) -> list[str]:
    try:
        configs = metadata["cardData"]["configs"]
    except (KeyError, TypeError) as error:
        raise ValueError("Stack v2 metadata has no cardData.configs list") from error
    names = [
        item["config_name"]
        for item in configs
        if isinstance(item, dict) and item.get("config_name") != "default"
    ]
    if not names:
        raise ValueError("Stack v2 metadata contains no language configs")
    return names


def build_inventory(stats_rows: Any, v2_config_names: Iterable[str]) -> list[LanguageRecord]:
    if not isinstance(stats_rows, list):
        raise ValueError("Stack v3 statistics payload must be a JSON list")

    v2_identities = {_language_identity(name) for name in v2_config_names}
    records: list[LanguageRecord] = []
    seen: set[str] = set()
    numeric_fields = ("repo_count", "file_count", "total_size_bytes", "estimated_tokens")

    for row in stats_rows:
        if not isinstance(row, dict) or not isinstance(row.get("language"), str):
            raise ValueError("every Stack v3 statistics row must have a string language")
        label = row["language"]
        if label in seen:
            raise ValueError(f"duplicate Stack v3 language label: {label}")
        seen.add(label)
        try:
            values = {field: int(row[field]) for field in numeric_fields}
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"invalid statistics for Stack v3 language {label!r}") from error

        registry_status, registry_key = _registry_match(label)
        v2_status = "present" if _language_identity(label) in v2_identities else "new_or_renamed"
        records.append(
            LanguageRecord(
                language=label,
                registry_status=registry_status,
                registry_key=registry_key,
                v2_status=v2_status,
                **values,
            )
        )

    return sorted(records, key=lambda record: (record.language.casefold(), record.language))


def research_queue(
    records: Iterable[LanguageRecord],
    intake_labels: Sequence[str] | None = None,
) -> list[LanguageRecord]:
    records = list(records)
    if intake_labels is not None:
        by_language = {record.language: record for record in records}
        missing_labels = [label for label in intake_labels if label not in by_language]
        if missing_labels:
            raise ValueError(
                "pinned Stack v3 intake labels missing from inventory: "
                + ", ".join(missing_labels)
            )
        return [by_language[label] for label in intake_labels]

    return [
        record
        for record in records
        if (
            record.registry_status == "missing" and record.v2_status == "new_or_renamed"
        )
        or record.language in MAPPING_REVIEW_LABELS
    ]


def inventory_discrepancy_queue(records: Iterable[LanguageRecord]) -> list[LanguageRecord]:
    by_language = {record.language: record for record in records}
    return [
        by_language[label]
        for label in INVENTORY_DISCREPANCY_LABELS
        if label in by_language and by_language[label].registry_status == "missing"
    ]


def chunk_records(
    records: Sequence[LanguageRecord], chunk_count: int
) -> list[tuple[str, list[LanguageRecord]]]:
    if chunk_count < 1:
        raise ValueError("chunk_count must be at least 1")
    if not records:
        return []
    chunk_size = math.ceil(len(records) / chunk_count)
    chunks = []
    for index, start in enumerate(range(0, len(records), chunk_size)):
        chunk = list(records[start : start + chunk_size])
        chunks.append((f"batch_{index:02d}", chunk))
    return chunks


def _render_prompt(batch_name: str, records: Sequence[LanguageRecord]) -> str:
    report_path = f"docs/comment_research/stack_v3_full/{batch_name}.md"
    table = [
        "| Exact label | Files | Tokens |",
        "| --- | ---: | ---: |",
        *[
            f"| `{record.language}` | {record.file_count} | {record.estimated_tokens} |"
            for record in records
        ],
    ]
    return "\n".join(
        [
            f"# Stack v3 Full Comment Research: {batch_name}",
            "",
            "## Ownership",
            "",
            f"Write the reviewed research record to `{report_path}`.",
            "Do not edit the registry, parser, sanitizer, or tests in this research stage.",
            "Keep downloads, probes, model output, and transcripts under `tmp/`.",
            "",
            "## Dataset Provenance",
            "",
            f"- Dataset: `{STACK_V3_DATASET}`",
            f"- Statistics repository: `{STACK_V3_STATS_REPOSITORY}`",
            f"- Immutable revision: `{STACK_V3_REVISION}`",
            f"- Full statistics SHA-256: `{STACK_V3_FULL_STATS_SHA256}`",
            "- Label field: `files[].language` (aggregated by the pinned statistics table)",
            "",
            "## Required Method",
            "",
            "Follow `docs/comment_research/README.md` and use",
            "`docs/comment_research/report_template.md` for every assigned label.",
            "Use pinned official specifications and implementation grammars before secondary",
            "sources. Do not infer syntax from the label, file extension, related language,",
            "or go-enry grouping. Record version and dialect scope, false-positive boundaries,",
            "sanitizer behavior, and representative examples. A format with no source-comment",
            "contract must be marked `unsupported`; insufficient evidence is `defer`.",
            "",
            "Finish every label with exactly one recommendation: `alias`, `implement`,",
            "`separate-family`, `contextual-helper`, `unsupported`, or `defer`.",
            "",
            "## Assigned Labels",
            "",
            *table,
            "",
        ]
    )


def _summary(records: Sequence[LanguageRecord]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    for record in records:
        status_counts[record.registry_status] = status_counts.get(record.registry_status, 0) + 1
    missing = [record for record in records if record.registry_status == "missing"]
    new_missing = [record for record in missing if record.v2_status == "new_or_renamed"]
    return {
        "total_languages": len(records),
        "supported_languages": len(records) - len(missing),
        "missing_languages": len(missing),
        "new_or_renamed_missing_languages": len(new_missing),
        "carryover_missing_languages": len(missing) - len(new_missing),
        "mapping_review_languages": len(
            [record for record in records if record.language in MAPPING_REVIEW_LABELS]
        ),
        "inventory_discrepancy_languages": len(inventory_discrepancy_queue(records)),
        "registry_status_counts": dict(sorted(status_counts.items())),
    }


def write_outputs(
    output_root: Path,
    records: Sequence[LanguageRecord],
    chunks: Sequence[tuple[str, list[LanguageRecord]]],
) -> None:
    prompt_dir = output_root / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "schema_version": 1,
        "dataset": STACK_V3_DATASET,
        "statistics_repository": STACK_V3_STATS_REPOSITORY,
        "revision": STACK_V3_REVISION,
        "statistics_sha256": STACK_V3_FULL_STATS_SHA256,
        "statistics_url": STACK_V3_FULL_STATS_URL,
        "v2_dataset": STACK_V2_DATASET,
        "v2_revision": STACK_V2_REVISION,
        "v2_public_inventory_revision": STACK_V2_PUBLIC_INVENTORY_REVISION,
        "v2_public_inventory_sha256": STACK_V2_PUBLIC_INVENTORY_SHA256,
        "summary": _summary(records),
        "languages": [asdict(record) for record in records],
    }
    (output_root / "inventory.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    assignments = {
        "schema_version": 1,
        "dataset": STACK_V3_DATASET,
        "revision": STACK_V3_REVISION,
        "batches": {
            name: [record.language for record in batch] for name, batch in chunks
        },
    }
    (output_root / "assignments.json").write_text(
        json.dumps(assignments, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    for name, batch in chunks:
        (prompt_dir / f"{name}.md").write_text(_render_prompt(name, batch), encoding="utf-8")

    lines = [
        "# Stack v3 Full Research Packets",
        "",
        "Generated run artifacts. Do not commit this directory.",
        "",
        f"- Revision: `{STACK_V3_REVISION}`",
        f"- Full inventory: `{len(records)}` labels",
        f"- Research queue: `{sum(len(batch) for _, batch in chunks)}` labels",
        "",
        "| Batch | Labels | Prompt | Reviewed record |",
        "| --- | ---: | --- | --- |",
    ]
    for name, batch in chunks:
        lines.append(
            f"| `{name}` | {len(batch)} | `prompts/{name}.md` | "
            f"`docs/comment_research/stack_v3_full/{name}.md` |"
        )
    (output_root / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    if args.chunk_count < 1:
        raise SystemExit("--chunk-count must be at least 1")

    stats_payload = _read_payload(args.stats_json, STACK_V3_FULL_STATS_URL)
    stats_digest = hashlib.sha256(stats_payload).hexdigest()
    if not args.skip_stats_hash_check and stats_digest != STACK_V3_FULL_STATS_SHA256:
        raise SystemExit(
            "Stack v3 full statistics hash mismatch: "
            f"expected {STACK_V3_FULL_STATS_SHA256}, got {stats_digest}"
        )
    stats_rows = _load_json(stats_payload, str(args.stats_json or STACK_V3_FULL_STATS_URL))

    v2_payload = _read_payload(args.v2_metadata_json, STACK_V2_METADATA_URL)
    v2_metadata = _load_json(v2_payload, str(args.v2_metadata_json or STACK_V2_METADATA_URL))
    records = build_inventory(stats_rows, _v2_config_names(v2_metadata))
    if not args.skip_stats_hash_check and len(records) != EXPECTED_FULL_LANGUAGE_COUNT:
        raise SystemExit(
            f"expected {EXPECTED_FULL_LANGUAGE_COUNT} Stack v3 full labels, got {len(records)}"
        )

    queue = research_queue(records, STACK_V3_PRIMARY_INTAKE_LABELS)
    chunks = chunk_records(queue, args.chunk_count)
    discrepancy = inventory_discrepancy_queue(records)
    if discrepancy:
        chunks.append(("inventory_discrepancy_00", discrepancy))
    write_outputs(args.output_root, records, chunks)

    summary = _summary(records)
    summary["research_decision_languages"] = sum(len(batch) for _, batch in chunks)
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"Wrote {len(chunks)} research packets below {args.output_root}")


if __name__ == "__main__":
    main()
