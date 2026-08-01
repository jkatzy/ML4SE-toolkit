"""Build comment-judge cases from a local Stack v3 full contents export.

This entry point is intentionally local-only. It accepts one flat JSON object
per source file, rejects repository rows containing nested ``files[]`` data,
and reuses the existing comment-judge sampler and manifest schema.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

STACK_V3_FULL_DATASET = "HuggingFaceCode/stack-v3-full"
STACK_V3_FULL_REVISION = "716a043a6c2adc34a2032b159364908a09ffe4ec"
STACK_V3_FULL_TABLE = "contents"
DEFAULT_OUTPUT_ROOT = Path("tmp/stack_v3_full_comment_judge")
DEFAULT_PROVENANCE_NAME = "provenance.json"


def _load_stack_v2_builder() -> Any:
    """Load the existing dataset-agnostic sampling implementation."""

    module_name = "stack_v2_comment_judge_cases"
    existing = sys.modules.get(module_name)
    if existing is not None:
        return existing

    script_path = Path(__file__).with_name("build_stack_v2_comment_judge_cases.py")
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load shared judge builder: {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


STACK_V2_BUILDER = _load_stack_v2_builder()


class FlatExportError(ValueError):
    """Raised when an input is not a Stack v3 full flat contents export."""


@dataclass(frozen=True)
class ExportInspection:
    """Validated identity and schema summary for a local JSONL export."""

    sha256: str
    row_count: int
    content_fields: tuple[str, ...]
    language_fields: tuple[str, ...]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse local Stack v3 full manifest-builder arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-jsonl",
        type=Path,
        required=True,
        help=(
            "Local flat JSONL exported from the gated Stack v3 full contents "
            "table at the pinned revision."
        ),
    )
    parser.add_argument(
        "--dataset-revision",
        default=STACK_V3_FULL_REVISION,
        choices=(STACK_V3_FULL_REVISION,),
        help="Immutable Stack v3 full revision asserted for the local export.",
    )
    parser.add_argument(
        "--languages",
        default=None,
        help="Comma-separated registry languages. Defaults to all supported languages.",
    )
    parser.add_argument(
        "--language-count",
        type=int,
        default=None,
        help="Use only the first N selected registry languages.",
    )
    parser.add_argument(
        "--language-map",
        type=Path,
        default=None,
        help=("Optional JSON mapping from registry keys to exact Stack v3 full language labels."),
    )
    parser.add_argument(
        "--per-kind",
        type=int,
        default=STACK_V2_BUILDER.DEFAULT_PER_KIND,
        help="Distinct source files to collect for each supported comment kind.",
    )
    parser.add_argument(
        "--files-per-language",
        type=int,
        default=None,
        help="Collect at most one case from exactly this many files per language.",
    )
    parser.add_argument(
        "--max-records-per-language",
        type=int,
        default=None,
        help="Maximum flat export rows scanned for each requested language.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=10,
        help="Emit progress after this many scanned rows; zero disables progress.",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=1,
        help="Number of requested languages sampled concurrently.",
    )
    parser.add_argument(
        "--content-prefetch-workers",
        type=int,
        default=4,
        help="Workers used to read matching flat-row content.",
    )
    parser.add_argument(
        "--content-prefetch-buffer-size",
        type=int,
        default=None,
        help="Maximum prefetched records; defaults to the prefetch worker count.",
    )
    parser.add_argument(
        "--content-field",
        default=None,
        help="Exact source-content field; otherwise content, text, and code are checked.",
    )
    parser.add_argument(
        "--language-field",
        default=None,
        help=(
            "Exact language-label field; otherwise language, lang, and "
            "programming_language are checked."
        ),
    )
    parser.add_argument(
        "--max-content-chars",
        type=int,
        default=STACK_V2_BUILDER.DEFAULT_MAX_CONTENT_CHARS,
        help="Skip source text above this character count; zero disables the cap.",
    )
    parser.add_argument(
        "--max-line-comment-chars",
        type=int,
        default=STACK_V2_BUILDER.DEFAULT_MAX_LINE_COMMENT_CHARS,
        help="Skip longer line-comment candidates; zero disables the cap.",
    )
    parser.add_argument(
        "--context-chars",
        type=int,
        default=1200,
        help="Source characters retained on each side of the target comment.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Ignored tmp directory for manifests, sources, failures, and provenance.",
    )
    parser.add_argument("--manifest-name", default="manifest.jsonl")
    parser.add_argument("--failure-name", default="failures.jsonl")
    parser.add_argument("--provenance-name", default=DEFAULT_PROVENANCE_NAME)
    parser.add_argument(
        "--fail-on-incomplete",
        action="store_true",
        help="Exit nonzero when any requested sampling quota is incomplete.",
    )
    return parser.parse_args(argv)


def inspect_flat_export(
    path: Path,
    *,
    content_field: str | None = None,
    language_field: str | None = None,
) -> ExportInspection:
    """Validate a one-file-per-row Stack v3 full contents JSONL export."""

    if not path.is_file():
        raise FlatExportError(f"Stack v3 full export does not exist: {path}")

    digest = hashlib.sha256()
    row_count = 0
    content_fields: set[str] = set()
    language_fields: set[str] = set()

    with path.open("rb") as infile:
        for line_number, raw_line in enumerate(infile, start=1):
            digest.update(raw_line)
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped.decode("utf-8"))
            except UnicodeDecodeError as exc:
                raise FlatExportError(f"Invalid UTF-8 on {path}:{line_number}") from exc
            except json.JSONDecodeError as exc:
                raise FlatExportError(f"Invalid JSON on {path}:{line_number}") from exc
            if not isinstance(row, dict):
                raise FlatExportError(f"Expected one JSON object per file on {path}:{line_number}")
            if isinstance(row.get("files"), list):
                raise FlatExportError(
                    f"Rejected train-style repository row on {path}:{line_number}: "
                    "nested files[] is not a Stack v3 full contents-table row"
                )
            _validate_optional_provenance(row, path, line_number)
            content_fields.add(
                _required_text_field(
                    row,
                    explicit=content_field,
                    candidates=STACK_V2_BUILDER.CONTENT_FIELDS,
                    field_role="source content",
                    path=path,
                    line_number=line_number,
                )
            )
            resolved_language_field = _required_text_field(
                row,
                explicit=language_field,
                candidates=STACK_V2_BUILDER.LANGUAGE_FIELDS,
                field_role="language label",
                path=path,
                line_number=line_number,
            )
            if not row[resolved_language_field].strip():
                raise FlatExportError(
                    f"Empty language label on {path}:{line_number} "
                    f"in field {resolved_language_field!r}"
                )
            language_fields.add(resolved_language_field)
            row_count += 1

    if row_count == 0:
        raise FlatExportError(f"Stack v3 full export contains no rows: {path}")
    return ExportInspection(
        sha256=digest.hexdigest(),
        row_count=row_count,
        content_fields=tuple(sorted(content_fields)),
        language_fields=tuple(sorted(language_fields)),
    )


def _validate_optional_provenance(row: dict[str, Any], path: Path, line_number: int) -> None:
    expected = {
        "dataset": STACK_V3_FULL_DATASET,
        "dataset_name": STACK_V3_FULL_DATASET,
        "dataset_revision": STACK_V3_FULL_REVISION,
        "dataset_table": STACK_V3_FULL_TABLE,
    }
    for field, expected_value in expected.items():
        if field in row and row[field] != expected_value:
            raise FlatExportError(
                f"Unexpected {field} on {path}:{line_number}: "
                f"expected {expected_value!r}, got {row[field]!r}"
            )


def _required_text_field(
    row: dict[str, Any],
    *,
    explicit: str | None,
    candidates: Sequence[str],
    field_role: str,
    path: Path,
    line_number: int,
) -> str:
    fields = (explicit,) if explicit else candidates
    for field in fields:
        if field and isinstance(row.get(field), str):
            return field
    expected = explicit or ", ".join(candidates)
    raise FlatExportError(
        f"Missing string {field_role} on {path}:{line_number}; expected {expected}"
    )


def _shared_builder_args(args: argparse.Namespace) -> argparse.Namespace:
    shared = argparse.Namespace(
        content_field=args.content_field,
        content_prefetch_buffer_size=args.content_prefetch_buffer_size,
        content_prefetch_workers=args.content_prefetch_workers,
        context_chars=args.context_chars,
        dataset=STACK_V3_FULL_DATASET,
        dataset_config=None,
        dataset_config_template="",
        dataset_revision=STACK_V3_FULL_REVISION,
        fail_on_incomplete=args.fail_on_incomplete,
        failure_name=args.failure_name,
        fetch_stack_v2_content=False,
        files_per_language=args.files_per_language,
        input_jsonl=args.input_jsonl,
        language_count=args.language_count,
        language_field=args.language_field,
        language_map=args.language_map,
        languages=args.languages,
        manifest_name=args.manifest_name,
        manifest_progress_label="stack-v3-full manifest",
        max_content_chars=args.max_content_chars,
        max_line_comment_chars=args.max_line_comment_chars,
        max_records_per_language=args.max_records_per_language,
        no_progress=args.progress_every == 0,
        num_workers=args.num_workers,
        output_root=args.output_root,
        per_kind=args.per_kind,
        progress_every=args.progress_every,
        s3_content_prefix="",
        s3_sign_requests=False,
        split=STACK_V3_FULL_TABLE,
    )
    STACK_V2_BUILDER._normalize_sampling_limits(shared)
    if shared.num_workers < 1:
        raise SystemExit("--num-workers must be at least 1")
    if shared.content_prefetch_workers < 1:
        raise SystemExit("--content-prefetch-workers must be at least 1")
    if shared.content_prefetch_buffer_size is None:
        shared.content_prefetch_buffer_size = shared.content_prefetch_workers
    if shared.content_prefetch_buffer_size < 1:
        raise SystemExit("--content-prefetch-buffer-size must be at least 1")
    if shared.max_content_chars < 0:
        raise SystemExit("--max-content-chars must be non-negative")
    return shared


def build_manifest(args: argparse.Namespace) -> int:
    """Validate the export, sample cases, and write pinned provenance."""

    if args.dataset_revision != STACK_V3_FULL_REVISION:
        raise SystemExit(f"Stack v3 full judge input must use revision {STACK_V3_FULL_REVISION}")
    try:
        inspection = inspect_flat_export(
            args.input_jsonl,
            content_field=args.content_field,
            language_field=args.language_field,
        )
    except FlatExportError as exc:
        raise SystemExit(str(exc)) from exc

    shared = _shared_builder_args(args)
    languages = STACK_V2_BUILDER._selected_languages(shared.languages, shared.language_count)
    STACK_V2_BUILDER._validate_selected_languages(languages)
    language_map = STACK_V2_BUILDER._load_language_map(shared.language_map)
    source_root = shared.output_root / "files"
    source_root.mkdir(parents=True, exist_ok=True)

    print(
        f"[stack-v3-full manifest] dataset={STACK_V3_FULL_DATASET} "
        f"revision={STACK_V3_FULL_REVISION} table={STACK_V3_FULL_TABLE} "
        f"rows={inspection.row_count} languages={len(languages)}"
    )
    results = STACK_V2_BUILDER._collect_requested_languages(
        args=shared,
        languages=languages,
        language_map=language_map,
        source_root=source_root,
    )
    cases = [case for result in results for case in result.cases]
    failures = [failure for result in results for failure in result.failures]

    manifest_path = shared.output_root / shared.manifest_name
    failure_path = shared.output_root / shared.failure_name
    provenance_path = shared.output_root / args.provenance_name
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    _write_jsonl(
        manifest_path,
        [_manifest_row(case.to_json(), inspection.sha256) for case in cases],
    )
    _write_failure_rows(failure_path, failures, inspection.sha256)
    manifest_sha256 = _sha256_file(manifest_path)
    provenance = {
        "schema_version": 1,
        "dataset": STACK_V3_FULL_DATASET,
        "dataset_revision": STACK_V3_FULL_REVISION,
        "dataset_table": STACK_V3_FULL_TABLE,
        "input_jsonl": str(args.input_jsonl.resolve()),
        "input_sha256": inspection.sha256,
        "input_rows": inspection.row_count,
        "content_fields": list(inspection.content_fields),
        "language_fields": list(inspection.language_fields),
        "selected_languages": languages,
        "manifest": str(manifest_path.resolve()),
        "manifest_sha256": manifest_sha256,
        "case_count": len(cases),
        "failure_count": len(failures),
    }
    provenance_path.write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {manifest_path} ({len(cases)} cases)")
    print(f"Wrote {provenance_path}")
    if failures:
        print(f"Wrote {failure_path} ({len(failures)} incomplete buckets)", file=sys.stderr)
    return 1 if failures and shared.fail_on_incomplete else 0


def _manifest_row(row: dict[str, Any], input_sha256: str) -> dict[str, Any]:
    return {
        **row,
        "dataset": STACK_V3_FULL_DATASET,
        "dataset_revision": STACK_V3_FULL_REVISION,
        "dataset_table": STACK_V3_FULL_TABLE,
        "dataset_export_sha256": input_sha256,
    }


def _write_failure_rows(path: Path, failures: Sequence[Any], input_sha256: str) -> None:
    if not failures:
        if path.exists():
            path.unlink()
        return
    rows = []
    for failure in failures:
        row = _manifest_row(failure.to_json(), input_sha256)
        for field in ("reason", "recommendation"):
            row[field] = row[field].replace("Stack v2", "Stack v3 full")
        rows.append(row)
    _write_jsonl(path, rows)


def _write_jsonl(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as outfile:
        for row in rows:
            outfile.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as infile:
        for chunk in iter(lambda: infile.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    return build_manifest(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
