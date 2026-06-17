"""Sample Stack v2 files for comment extraction and cleaning judge tests.

The generated manifest is intentionally external to normal unit fixtures. Stack
v2 source files can be large and may be gated or locally cached, so this script
creates a JSONL manifest plus per-case source files under a caller-controlled
output directory. The pytest judge harness consumes that manifest through
``STACK_V2_COMMENT_JUDGE_MANIFEST``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import threading
from collections import defaultdict
from collections.abc import Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from ml4setk.Parsing.Comments import (
    CommentQuery,
    CommentSanitizer,
    CommentSyntax,
    get_comment_syntax,
    get_supported_comment_languages,
)

DEFAULT_DATASET = "bigcode/the-stack-v2"
DEFAULT_OUTPUT_ROOT = Path("tmp/stack_v2_comment_judge")
DEFAULT_PER_KIND = 20
DEFAULT_SCAN_MULTIPLIER = 500
DEFAULT_MAX_CONTENT_CHARS = 1_000_000
CONTENT_FIELDS = ("content", "text", "code")
LANGUAGE_FIELDS = ("language", "lang", "programming_language")
PATH_FIELDS = ("path", "max_stars_repo_path", "file_name")
REPO_FIELDS = ("repo", "repo_name", "max_stars_repo_name")
ID_FIELDS = ("id", "blob_id", "hexsha", "sha")
STACK_CONFIG_OVERRIDES = {
    "c#": "C-Sharp",
    "f#": "F-Sharp",
    "f_star": "F-Star",
    "four_d": "4D",
    "qsharp": "Q-Sharp",
}
STACK_LABEL_OVERRIDES = {
    "c#": "C#",
    "c++": "C++",
    "f#": "F#",
    "f_star": "F*",
    "four_d": "4D",
    "objective-c": "Objective-C",
    "qsharp": "Q#",
}
REQUESTED_LANGUAGE_ALIASES = {
    "c_plus_plus": "c++",
    "cplusplus": "c++",
    "cpp": "c++",
    "c_sharp": "c#",
    "csharp": "c#",
    "f_sharp": "f#",
    "fsharp": "f#",
    "objective_c": "objective-c",
}
_HUGGINGFACE_DATASET_OPEN_LOCK = threading.Lock()
_HUGGINGFACE_DATASET_ITERATION_LOCK = threading.Lock()


class _CorpusCollectionError(Exception):
    """Raised when corpus access fails during manifest sampling."""


@dataclass(frozen=True)
class StackFailure:
    """One language/comment-kind bucket that could not be sampled."""

    language: str
    comment_kind: str
    expected_count: int
    observed_count: int
    scanned_records: int
    max_records_per_language: int
    dataset: str
    dataset_config: str | None
    dataset_language: str
    syntax_examples: list[str]
    observed_kinds: dict[str, int]
    reason: str
    recommendation: str

    def to_json(self) -> dict[str, Any]:
        """Return a JSON-serializable failure row."""

        return {
            "language": self.language,
            "comment_kind": self.comment_kind,
            "expected_count": self.expected_count,
            "observed_count": self.observed_count,
            "scanned_records": self.scanned_records,
            "max_records_per_language": self.max_records_per_language,
            "dataset": self.dataset,
            "dataset_config": self.dataset_config,
            "dataset_language": self.dataset_language,
            "syntax_examples": self.syntax_examples,
            "observed_kinds": self.observed_kinds,
            "reason": self.reason,
            "recommendation": self.recommendation,
        }


@dataclass(frozen=True)
class StackCollectionResult:
    """Sampled cases plus corpus scan metadata for one language."""

    cases: list[StackCase]
    scanned_records: int
    dataset_config: str | None
    dataset_language: str
    collection_error: str | None = None


@dataclass(frozen=True)
class StackCase:
    """One sampled source file/comment pair for LLM judging."""

    case_id: str
    language: str
    comment_kind: str
    syntax_label: str
    source_file: str
    source_id: str
    repo: str
    path: str
    match_start: int
    match_end: int
    match_line: int
    match_column: int
    raw_comment: str
    cleaned_comment: str
    source_excerpt: str

    def to_json(self) -> dict[str, Any]:
        """Return a JSON-serializable manifest row."""

        return {
            "case_id": self.case_id,
            "language": self.language,
            "comment_kind": self.comment_kind,
            "syntax_label": self.syntax_label,
            "source_file": self.source_file,
            "source_id": self.source_id,
            "repo": self.repo,
            "path": self.path,
            "match_start": self.match_start,
            "match_end": self.match_end,
            "match_line": self.match_line,
            "match_column": self.match_column,
            "raw_comment": self.raw_comment,
            "cleaned_comment": self.cleaned_comment,
            "source_excerpt": self.source_excerpt,
        }


@dataclass(frozen=True)
class LanguageCollectionResult:
    """Sampled cases and failures for one requested language."""

    language_index: int
    language: str
    cases: list[StackCase]
    failures: list[StackFailure]


@dataclass(frozen=True)
class PrefetchedRecord:
    """One corpus record with source text fetched before parser processing."""

    record_index: int
    record: dict[str, Any]
    content: str


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Build Stack v2 comment extraction/cleaning cases for the optional "
            "LLM-as-judge pytest harness."
        )
    )
    parser.add_argument(
        "--dataset",
        default=DEFAULT_DATASET,
        help="Hugging Face dataset name used when --input-jsonl is not supplied.",
    )
    parser.add_argument("--split", default="train", help="Dataset split to stream.")
    parser.add_argument(
        "--dataset-config",
        default=None,
        help="Single Hugging Face dataset config to use for every requested language.",
    )
    parser.add_argument(
        "--dataset-config-template",
        default="{stack_label}",
        help=(
            "Template for per-language dataset configs. Available fields: "
            "{language}, {stack_label}. Use '' to disable configs."
        ),
    )
    parser.add_argument(
        "--language-map",
        type=Path,
        default=None,
        help=(
            "Optional JSON mapping from registry language key to a Stack v2 label "
            "or an object with dataset_config and dataset_language fields."
        ),
    )
    parser.add_argument(
        "--input-jsonl",
        type=Path,
        default=None,
        help="Read records from a local JSONL file instead of Hugging Face datasets.",
    )
    parser.add_argument(
        "--languages",
        default=None,
        help="Comma-separated registry languages to sample. Defaults to all supported languages.",
    )
    parser.add_argument(
        "--language-count",
        type=int,
        default=None,
        help=(
            "Sample only the first N selected registry languages. Applies after "
            "--languages when a list is provided, otherwise to all supported languages."
        ),
    )
    parser.add_argument(
        "--per-kind",
        type=int,
        default=DEFAULT_PER_KIND,
        help="Number of distinct source files to collect for each supported comment kind.",
    )
    parser.add_argument(
        "--max-records-per-language",
        type=int,
        default=None,
        help=(
            "Stop scanning a language after this many candidate records. Defaults "
            f"to --per-kind * {DEFAULT_SCAN_MULTIPLIER}."
        ),
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=10,
        help="Print manifest-generation progress after this many scanned records.",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=1,
        help=(
            "Number of languages to sample concurrently. Increase this when "
            "candidate discovery is I/O-bound."
        ),
    )
    parser.add_argument(
        "--content-prefetch-workers",
        type=int,
        default=4,
        help=(
            "Number of per-language worker threads used to fetch Stack v2 source "
            "files ahead of parsing. Set to 1 to disable content prefetching."
        ),
    )
    parser.add_argument(
        "--content-prefetch-buffer-size",
        type=int,
        default=None,
        help=(
            "Maximum number of records kept in the per-language prefetch queue. "
            "Defaults to --content-prefetch-workers."
        ),
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Suppress manifest-generation progress messages.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Directory for manifest and sampled source files.",
    )
    parser.add_argument(
        "--manifest-name",
        default="manifest.jsonl",
        help="Manifest filename under --output-root.",
    )
    parser.add_argument(
        "--failure-name",
        default="failures.jsonl",
        help="Failure filename under --output-root for incomplete language/kind buckets.",
    )
    parser.add_argument(
        "--context-chars",
        type=int,
        default=1200,
        help="Characters to keep on each side of the sampled comment for judge context.",
    )
    parser.add_argument(
        "--content-field",
        default=None,
        help="Override source-content field. Defaults to auto-detecting common fields.",
    )
    parser.add_argument(
        "--max-content-chars",
        type=int,
        default=DEFAULT_MAX_CONTENT_CHARS,
        help=(
            "Skip source files larger than this many decoded characters. Set to "
            "0 to disable the content-size cap."
        ),
    )
    parser.add_argument(
        "--language-field",
        default=None,
        help="Override language field for unconfigured datasets or JSONL input.",
    )
    parser.add_argument(
        "--fetch-stack-v2-content",
        action="store_true",
        help=(
            "Fetch source text for official Stack v2 ID records from the "
            "public Software Heritage S3 bucket. Requires boto3 and smart_open."
        ),
    )
    parser.add_argument(
        "--s3-sign-requests",
        action="store_true",
        help=(
            "Sign S3 requests with the local AWS credential chain. By default, "
            "Stack v2 content fetches use unsigned requests for the public bucket."
        ),
    )
    parser.add_argument(
        "--s3-content-prefix",
        default="s3://softwareheritage/content",
        help="S3 prefix used with --fetch-stack-v2-content.",
    )
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help=(
            "Deprecated compatibility flag. Incomplete language/kind buckets "
            "are now written to failures.jsonl and do not fail generation."
        ),
    )
    parser.add_argument(
        "--fail-on-incomplete",
        action="store_true",
        help=(
            "Return a non-zero exit code when any language/kind bucket has fewer "
            "than --per-kind cases. By default, pytest reports these rows as "
            "test failures from failures.jsonl."
        ),
    )
    return parser.parse_args()


def main() -> int:
    """Run the Stack v2 sampling workflow."""

    args = parse_args()
    _normalize_sampling_limits(args)
    if args.num_workers < 1:
        raise SystemExit("--num-workers must be at least 1")
    if args.content_prefetch_workers < 1:
        raise SystemExit("--content-prefetch-workers must be at least 1")
    if args.content_prefetch_buffer_size is None:
        args.content_prefetch_buffer_size = args.content_prefetch_workers
    if args.content_prefetch_buffer_size < 1:
        raise SystemExit("--content-prefetch-buffer-size must be at least 1")
    if args.max_content_chars < 0:
        raise SystemExit("--max-content-chars must be non-negative")
    languages = _selected_languages(args.languages, args.language_count)
    language_map = _load_language_map(args.language_map)
    manifest_path = args.output_root / args.manifest_name
    failure_path = args.output_root / args.failure_name
    source_root = args.output_root / "files"
    source_root.mkdir(parents=True, exist_ok=True)

    _emit_manifest_progress(
        args,
        f"[stack-v2 manifest] start languages={len(languages)} "
        f"per_kind={args.per_kind} output_root={args.output_root}",
    )

    _validate_selected_languages(languages)

    language_results = _collect_requested_languages(
        args=args,
        languages=languages,
        language_map=language_map,
        source_root=source_root,
    )

    all_cases: list[StackCase] = []
    failures: list[StackFailure] = []
    for language_result in language_results:
        all_cases.extend(language_result.cases)
        failures.extend(language_result.failures)

    _emit_manifest_progress(
        args,
        f"[stack-v2 manifest] writing manifest cases={len(all_cases)} path={manifest_path}",
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8") as outfile:
        for case in all_cases:
            outfile.write(json.dumps(case.to_json(), ensure_ascii=False) + "\n")

    _write_failures(failure_path, failures)
    _print_summary(manifest_path, failure_path, all_cases, failures, args.per_kind)
    if failures and args.fail_on_incomplete:
        return 1
    return 0


def _normalize_sampling_limits(args: argparse.Namespace) -> None:
    """Normalize sampling count defaults after CLI parsing.

    Args:
        args: Parsed manifest-builder arguments. ``max_records_per_language``
            is filled in when omitted.
    """

    if args.per_kind < 1:
        raise SystemExit("--per-kind must be at least 1")
    if args.max_records_per_language is None:
        args.max_records_per_language = args.per_kind * DEFAULT_SCAN_MULTIPLIER
    if args.max_records_per_language < 1:
        raise SystemExit("--max-records-per-language must be at least 1")


def _collect_requested_languages(
    *,
    args: argparse.Namespace,
    languages: list[str],
    language_map: dict[str, Any],
    source_root: Path,
) -> list[LanguageCollectionResult]:
    worker_count = min(args.num_workers, len(languages))
    if worker_count <= 1:
        return [
            _collect_requested_language(
                args=args,
                language_index=language_index,
                language_count=len(languages),
                language=language,
                language_map=language_map,
                source_root=source_root,
            )
            for language_index, language in enumerate(languages, start=1)
        ]

    _emit_manifest_progress(
        args,
        f"[stack-v2 manifest] sampling languages concurrently num_workers={worker_count}",
    )
    language_results = []
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [
            executor.submit(
                _collect_requested_language,
                args=args,
                language_index=language_index,
                language_count=len(languages),
                language=language,
                language_map=language_map,
                source_root=source_root,
            )
            for language_index, language in enumerate(languages, start=1)
        ]
        for future in as_completed(futures):
            language_results.append(future.result())

    return sorted(language_results, key=lambda result: result.language_index)


def _collect_requested_language(
    *,
    args: argparse.Namespace,
    language_index: int,
    language_count: int,
    language: str,
    language_map: dict[str, Any],
    source_root: Path,
) -> LanguageCollectionResult:
    syntax = get_comment_syntax(language)
    target_kinds = _supported_comment_kinds(syntax, language)
    if not target_kinds:
        _emit_manifest_progress(
            args,
            f"[stack-v2 manifest] language {language_index}/{language_count} "
            f"{language} skipped no-supported-comment-kinds",
        )
        return LanguageCollectionResult(
            language_index=language_index,
            language=language,
            cases=[],
            failures=[],
        )

    _emit_manifest_progress(
        args,
        f"[stack-v2 manifest] language {language_index}/{language_count} "
        f"{language} start kinds={','.join(target_kinds)}",
    )
    result = _collect_language_cases(
        args=args,
        language=language,
        syntax=syntax,
        target_kinds=target_kinds,
        language_map=language_map,
        source_root=source_root,
    )
    counts = _counts_by_kind(result.cases)
    _emit_manifest_progress(
        args,
        f"[stack-v2 manifest] language {language_index}/{language_count} "
        f"{language} done scanned={result.scanned_records} "
        f"{_format_progress_counts(counts, target_kinds, args.per_kind)}",
    )

    return LanguageCollectionResult(
        language_index=language_index,
        language=language,
        cases=result.cases,
        failures=_build_failures(
            args=args,
            language=language,
            syntax=syntax,
            target_kinds=target_kinds,
            counts=counts,
            result=result,
        ),
    )

def _selected_languages(
    raw_languages: str | None, language_count: int | None = None
) -> list[str]:
    if language_count is not None and language_count < 1:
        raise SystemExit("--language-count must be at least 1")
    if raw_languages is None:
        languages = get_supported_comment_languages()
    else:
        languages = [
            _normalize_requested_language(language)
            for language in raw_languages.split(",")
            if language.strip()
        ]
    if language_count is not None:
        return languages[:language_count]
    return languages


def _normalize_requested_language(language: str) -> str:
    key = language.strip().lower()
    return REQUESTED_LANGUAGE_ALIASES.get(key, key)


def _validate_selected_languages(languages: list[str]) -> None:
    unsupported = []
    for language in languages:
        try:
            get_comment_syntax(language)
        except NotImplementedError:
            unsupported.append(language)
    if unsupported:
        supported = ", ".join(get_supported_comment_languages())
        requested = ", ".join(unsupported)
        raise SystemExit(
            f"Unsupported comment language(s): {requested}. "
            f"Use registry keys such as c++, c#, or f#. "
            f"Supported keys: {supported}"
        )


def _load_language_map(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    with path.open(encoding="utf-8") as infile:
        data = json.load(infile)
    return {key.lower(): value for key, value in data.items()}


def _emit_manifest_progress(args: argparse.Namespace, message: str) -> None:
    if args.no_progress:
        return
    print(message, file=sys.stderr, flush=True)


def _should_emit_record_progress(args: argparse.Namespace, record_index: int) -> bool:
    return args.progress_every > 0 and record_index % args.progress_every == 0


def _format_progress_counts(
    counts: dict[str, int], target_kinds: tuple[str, ...], per_kind: int
) -> str:
    return " ".join(f"{kind}={counts.get(kind, 0)}/{per_kind}" for kind in target_kinds)


def _supported_comment_kinds(syntax: CommentSyntax, language: str) -> tuple[str, ...]:
    kinds = []
    examples = [*syntax.shared_regex_examples, *syntax.shared_nested_examples]
    if language == syntax.canonical_name:
        examples.extend(syntax.canonical_regex_examples)
        examples.extend(syntax.canonical_nested_examples)
    else:
        if not syntax.shared_regex_examples:
            examples.extend(syntax.canonical_regex_examples)
        if not syntax.shared_nested_examples:
            examples.extend(syntax.canonical_nested_examples)

    for example in examples:
        if example.kind not in kinds:
            kinds.append(example.kind)
    return tuple(kinds)


def _collect_language_cases(
    *,
    args: argparse.Namespace,
    language: str,
    syntax: CommentSyntax,
    target_kinds: tuple[str, ...],
    language_map: dict[str, Any],
    source_root: Path,
) -> StackCollectionResult:
    query = CommentQuery(language)
    sanitizer = CommentSanitizer(language)
    collected: dict[str, list[StackCase]] = {kind: [] for kind in target_kinds}
    seen_sources: set[tuple[str, str]] = set()

    dataset_language = _dataset_language_for(language, language_map)
    available_configs = (
        None if args.input_jsonl is not None else _safe_dataset_config_names(args.dataset)
    )
    dataset_config = _dataset_config_for(args, language, language_map, available_configs)
    records = _iter_records(args, language, language_map)
    prefetched_records = _iter_prefetched_records(
        records=records,
        args=args,
        language=language,
        dataset_language=dataset_language,
    )
    scanned_records = 0
    collection_error = None
    try:
        for prefetched in prefetched_records:
            scanned_records = prefetched.record_index
            if prefetched.record_index > args.max_records_per_language:
                scanned_records = args.max_records_per_language
                break
            if _should_emit_record_progress(args, prefetched.record_index):
                progress_counts = _format_collected_progress(
                    collected, target_kinds, args.per_kind
                )
                _emit_manifest_progress(
                    args,
                    f"[stack-v2 manifest] language={language} "
                    f"scanned={prefetched.record_index} {progress_counts}",
                )
            record = prefetched.record
            content = prefetched.content
            if not content:
                continue

            source_identity = _source_identity(record, prefetched.record_index)
            matches = query.parse(content)
            if not matches:
                continue

            for match_index, match in enumerate(matches):
                kind, syntax_label = _classify_comment(syntax, match.match)
                if kind not in collected or len(collected[kind]) >= args.per_kind:
                    continue
                if (kind, source_identity) in seen_sources:
                    continue

                match_start = len(match.prefix)
                match_end = len(content) - len(match.suffix)
                case = _build_case(
                    language=language,
                    kind=kind,
                    syntax_label=syntax_label,
                    record=record,
                    record_index=prefetched.record_index,
                    match_index=match_index,
                    content=content,
                    match_start=match_start,
                    match_end=match_end,
                    raw_comment=match.match,
                    cleaned_comment=sanitizer.sanitize(match),
                    source_root=source_root,
                    context_chars=args.context_chars,
                )
                collected[kind].append(case)
                seen_sources.add((kind, source_identity))
                progress_counts = _format_collected_progress(
                    collected, target_kinds, args.per_kind
                )
                _emit_manifest_progress(
                    args,
                    f"[stack-v2 manifest] language={language} collected "
                    f"kind={kind} case={case.case_id} {progress_counts}",
                )

            if all(len(cases) >= args.per_kind for cases in collected.values()):
                break
    except _CorpusCollectionError as exc:
        collection_error = str(exc)
        _emit_manifest_progress(
            args,
            f"[stack-v2 manifest] language={language} collection-error "
            f"scanned={scanned_records} error={collection_error}",
        )
    finally:
        close_prefetch = getattr(prefetched_records, "close", None)
        if close_prefetch is not None:
            close_prefetch()
        close = getattr(records, "close", None)
        if close is not None:
            close()

    return StackCollectionResult(
        cases=[case for kind in target_kinds for case in collected[kind]],
        scanned_records=scanned_records,
        dataset_config=dataset_config,
        dataset_language=dataset_language,
        collection_error=collection_error,
    )


def _build_failures(
    *,
    args: argparse.Namespace,
    language: str,
    syntax: CommentSyntax,
    target_kinds: tuple[str, ...],
    counts: dict[str, int],
    result: StackCollectionResult,
) -> list[StackFailure]:
    failures = []
    for kind in target_kinds:
        observed_count = counts.get(kind, 0)
        if observed_count >= args.per_kind:
            continue
        if result.collection_error is None:
            reason = (
                f"Only found {observed_count}/{args.per_kind} {kind} comment "
                f"case(s) for {language} after scanning {result.scanned_records} "
                "record(s)."
            )
            recommendation = _manifest_failure_recommendation(kind)
        else:
            reason = (
                f"Could not finish collecting {kind} comment case(s) for {language}: "
                f"{result.collection_error}. Found {observed_count}/{args.per_kind} "
                f"before aborting after scanning {result.scanned_records} record(s)."
            )
            recommendation = (
                "Resolve the corpus access or streaming error and rerun the manifest "
                "builder for this language. Treat observed counts as partial samples."
            )

        failures.append(
            StackFailure(
                language=language,
                comment_kind=kind,
                expected_count=args.per_kind,
                observed_count=observed_count,
                scanned_records=result.scanned_records,
                max_records_per_language=args.max_records_per_language,
                dataset=args.dataset,
                dataset_config=result.dataset_config,
                dataset_language=result.dataset_language,
                syntax_examples=_syntax_examples_for_kind(syntax, kind),
                observed_kinds=counts,
                reason=reason,
                recommendation=recommendation,
            )
        )
    return failures


def _manifest_failure_recommendation(kind: str) -> str:
    """Return review guidance for an incomplete manifest bucket.

    Args:
        kind: Missing comment kind such as ``line``, ``block``, or ``nested``.

    Returns:
        Human guidance for interpreting the missing bucket.
    """

    if kind == "nested":
        return (
            "Treat this as a corpus coverage review signal first: nested comment "
            "examples can be rare in Stack v2, so an incomplete bucket does not "
            "by itself prove a parser or registry bug. Inspect samples and "
            "syntax evidence before deciding whether to lower --per-kind, raise "
            "--max-records-per-language, exclude the nested bucket with a "
            "research note, or make a code change."
        )

    return (
        "Treat this as a corpus-backed syntax failure until reviewed: verify "
        "the registry syntax against Stack v2 samples, lower --per-kind for "
        "this language, or exclude the kind with an explicit registry/research "
        "note if the syntax is not valid for this corpus."
    )


def _syntax_examples_for_kind(syntax: CommentSyntax, kind: str) -> list[str]:
    examples = [*syntax.shared_regex_examples, *syntax.canonical_regex_examples]
    examples.extend(syntax.shared_nested_examples)
    examples.extend(syntax.canonical_nested_examples)
    return [example.expected_match for example in examples if example.kind == kind]


def _iter_records(
    args: argparse.Namespace, language: str, language_map: dict[str, Any]
) -> Iterator[dict[str, Any]]:
    if args.input_jsonl is not None:
        yield from _iter_jsonl_records(args.input_jsonl)
        return

    if _needs_stack_v2_content_source(args):
        raise SystemExit(_stack_v2_content_source_message())

    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit(
            "The Hugging Face 'datasets' package is required for Stack v2 streaming. "
            "Install it or pass --input-jsonl with locally exported Stack v2 records."
        ) from exc

    available_configs = _safe_dataset_config_names(args.dataset)
    dataset_config = _dataset_config_for(args, language, language_map, available_configs)
    try:
        dataset = _load_streaming_dataset(
            load_dataset=load_dataset,
            dataset=args.dataset,
            dataset_config=dataset_config,
            split=args.split,
        )
    except ValueError as exc:
        raise SystemExit(
            _format_dataset_config_error(
                dataset=args.dataset,
                language=language,
                dataset_config=dataset_config,
                available_configs=available_configs,
                original_error=exc,
            )
        ) from exc
    except Exception as exc:
        raise _CorpusCollectionError(
            _format_corpus_access_error(
                dataset=args.dataset,
                language=language,
                dataset_config=dataset_config,
                split=args.split,
                original_error=exc,
            )
        ) from exc

    iterator = None
    try:
        iterator = iter(dataset)
        for row in iterator:
            yield dict(row)
    except Exception as exc:
        raise _CorpusCollectionError(
            _format_corpus_access_error(
                dataset=args.dataset,
                language=language,
                dataset_config=dataset_config,
                split=args.split,
                original_error=exc,
            )
        ) from exc
    finally:
        if iterator is not None:
            close = getattr(iterator, "close", None)
            if close is not None:
                close()


def _load_streaming_dataset(
    *,
    load_dataset: Any,
    dataset: str,
    dataset_config: str | None,
    split: str,
):
    """Open a Hugging Face streaming dataset under a metadata lock.

    Args:
        load_dataset: Imported ``datasets.load_dataset`` callable.
        dataset: Hugging Face dataset name.
        dataset_config: Optional dataset config.
        split: Dataset split to stream.

    Returns:
        The streaming dataset object.
    """

    with _HUGGINGFACE_DATASET_OPEN_LOCK:
        if dataset_config:
            return load_dataset(dataset, dataset_config, split=split, streaming=True)
        return load_dataset(dataset, split=split, streaming=True)


def _iter_jsonl_records(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as infile:
        for line_number, line in enumerate(infile, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on {path}:{line_number}") from exc


def _dataset_config_for(
    args: argparse.Namespace,
    language: str,
    language_map: dict[str, Any],
    available_configs: tuple[str, ...] | None = None,
) -> str | None:
    mapped = language_map.get(language)
    if isinstance(mapped, dict) and mapped.get("dataset_config") is not None:
        return _resolve_dataset_config(str(mapped["dataset_config"]), available_configs)
    if isinstance(mapped, str):
        return _resolve_dataset_config(mapped, available_configs)
    if args.dataset_config is not None:
        return _resolve_dataset_config(args.dataset_config, available_configs)
    if args.dataset_config_template == "":
        return None

    candidates = [
        args.dataset_config_template.format(
            language=language,
            stack_label=_default_stack_label(language),
            stack_config=_default_stack_config(language),
        ),
        _default_stack_config(language),
        _default_stack_label(language),
        language,
    ]
    for candidate in candidates:
        resolved = _resolve_dataset_config(candidate, available_configs)
        if resolved is not None and (available_configs is None or resolved in available_configs):
            return resolved
    return candidates[0]


def _safe_dataset_config_names(dataset: str) -> tuple[str, ...] | None:
    try:
        return _dataset_config_names(dataset)
    except Exception:
        return None


@lru_cache(maxsize=None)
def _dataset_config_names(dataset: str) -> tuple[str, ...]:
    from datasets import get_dataset_config_names

    with _HUGGINGFACE_DATASET_OPEN_LOCK:
        return tuple(get_dataset_config_names(dataset))


def _resolve_dataset_config(config: str, available_configs: tuple[str, ...] | None) -> str:
    if available_configs is None or config in available_configs:
        return config

    lookup = _dataset_config_lookup(available_configs)
    for key in _dataset_config_lookup_keys(config):
        resolved = lookup.get(key)
        if resolved is not None:
            return resolved
    return config


def _dataset_config_lookup(available_configs: tuple[str, ...]) -> dict[str, str]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for config in available_configs:
        for key in _dataset_config_lookup_keys(config):
            grouped[key].append(config)
    return {
        key: configs[0]
        for key, configs in grouped.items()
        if len(set(configs)) == 1
    }


def _dataset_config_lookup_keys(config: str) -> tuple[str, ...]:
    normalized = _normalize_language(config)
    compact = "".join(char.lower() for char in config if char.isalnum())
    keys = [config, normalized]
    if len(compact) >= 3:
        keys.append(compact)
    return tuple(dict.fromkeys(keys))


def _format_dataset_config_error(
    *,
    dataset: str,
    language: str,
    dataset_config: str | None,
    available_configs: tuple[str, ...] | None,
    original_error: ValueError,
) -> str:
    message = (
        f"Could not open dataset '{dataset}' for language '{language}'"
        f" with config '{dataset_config}'."
    )
    if available_configs:
        close_matches = _close_dataset_config_matches(language, available_configs)
        if close_matches:
            message += f" Close Stack v2 config matches: {', '.join(close_matches)}."
        message += (
            " Pass --language-map with an explicit dataset_config if this language "
            "uses a non-obvious Stack v2 config name."
        )
    return f"{message}\nOriginal datasets error: {original_error}"


def _format_corpus_access_error(
    *,
    dataset: str,
    language: str,
    dataset_config: str | None,
    split: str,
    original_error: Exception,
) -> str:
    """Format a corpus open/read failure for manifest failure rows.

    Args:
        dataset: Hugging Face dataset name.
        language: Registry language being sampled.
        dataset_config: Optional dataset config.
        split: Dataset split being streamed.
        original_error: Exception raised by the streaming dataset layer.

    Returns:
        A compact one-line error summary suitable for progress and JSONL output.
    """

    error_text = " ".join(str(original_error).split())
    error_summary = type(original_error).__name__
    if error_text:
        error_summary = f"{error_summary}: {error_text}"
    return (
        f"Could not open/read dataset '{dataset}' for language '{language}' "
        f"with config '{dataset_config}' split '{split}': {error_summary}"
    )


def _close_dataset_config_matches(
    language: str, available_configs: tuple[str, ...], limit: int = 8
) -> list[str]:
    target_keys = (
        set(_dataset_config_lookup_keys(language))
        | set(_dataset_config_lookup_keys(_default_stack_label(language)))
        | set(_dataset_config_lookup_keys(_default_stack_config(language)))
    )
    matches = [
        config
        for config in available_configs
        if target_keys.intersection(_dataset_config_lookup_keys(config))
    ]
    return matches[:limit]


def _default_stack_config(language: str) -> str:
    if language in STACK_CONFIG_OVERRIDES:
        return STACK_CONFIG_OVERRIDES[language]
    return _default_stack_label(language).replace(" ", "_")


def _dataset_language_for(language: str, language_map: dict[str, Any]) -> str:
    mapped = language_map.get(language)
    if isinstance(mapped, dict) and mapped.get("dataset_language") is not None:
        return str(mapped["dataset_language"])
    if isinstance(mapped, str):
        return mapped
    return _default_stack_label(language)


def _default_stack_label(language: str) -> str:
    if language in STACK_LABEL_OVERRIDES:
        return STACK_LABEL_OVERRIDES[language]
    return " ".join(part.capitalize() for part in language.replace("-", "_").split("_"))


def _record_matches_language(
    record: dict[str, Any],
    args: argparse.Namespace,
    language: str,
    dataset_language: str,
) -> bool:
    language_field = args.language_field or _first_existing_field(record, LANGUAGE_FIELDS)
    if language_field is None:
        return True
    value = record.get(language_field)
    if value is None:
        return True
    expected_keys = _language_match_keys(language) | _language_match_keys(dataset_language)
    return bool(_language_match_keys(value).intersection(expected_keys))


def _record_content(record: dict[str, Any], args: argparse.Namespace) -> str:
    content = _first_text_field(record, [args.content_field, *CONTENT_FIELDS])
    if content:
        return _content_within_size_limit(content, args.max_content_chars)
    if args.fetch_stack_v2_content:
        return _download_stack_v2_content(
            record,
            args.s3_content_prefix,
            sign_requests=args.s3_sign_requests,
            max_content_chars=args.max_content_chars,
        )
    if _has_stack_v2_content_pointer(record):
        raise SystemExit(_stack_v2_content_source_message())
    return ""


def _content_within_size_limit(content: str, max_content_chars: int) -> str:
    """Return content only when it is within the configured size cap.

    Args:
        content: Decoded source text.
        max_content_chars: Maximum decoded characters to keep, or ``0`` for no
            cap.

    Returns:
        The content when allowed; otherwise an empty string so the caller skips
        the record.
    """

    if max_content_chars and len(content) > max_content_chars:
        return ""
    return content


def _iter_prefetched_records(
    *,
    records: Iterator[dict[str, Any]],
    args: argparse.Namespace,
    language: str,
    dataset_language: str,
) -> Iterator[PrefetchedRecord]:
    """Yield records with language-matching source content fetched ahead.

    Args:
        records: Corpus record iterator.
        args: Manifest builder arguments.
        language: Registry language currently being sampled.
        dataset_language: Stack v2 language label accepted for this registry key.

    Returns:
        Ordered prefetched records. Non-matching language rows are yielded with
        empty content so scan counts and progress remain unchanged.
    """

    worker_count = args.content_prefetch_workers
    buffer_size = max(args.content_prefetch_buffer_size, worker_count)
    record_iterator = enumerate(records, start=1)
    if worker_count <= 1:
        while True:
            try:
                record_index, record = _next_record(record_iterator, args)
            except StopIteration:
                return
            if record_index > args.max_records_per_language:
                yield PrefetchedRecord(record_index, record, "")
                return
            content = ""
            if _record_matches_language(record, args, language, dataset_language):
                content = _record_content_or_empty(
                    record,
                    args,
                    language,
                    record_index,
                )
            yield PrefetchedRecord(record_index, record, content)
        return

    executor = ThreadPoolExecutor(max_workers=worker_count)
    pending: list[tuple[int, dict[str, Any], Any]] = []
    exhausted = False

    def fill_pending() -> None:
        nonlocal exhausted
        while not exhausted and len(pending) < buffer_size:
            try:
                record_index, record = _next_record(record_iterator, args)
            except StopIteration:
                exhausted = True
                return

            if record_index > args.max_records_per_language:
                pending.append((record_index, record, None))
                exhausted = True
                return

            if _record_matches_language(record, args, language, dataset_language):
                future = executor.submit(
                    _record_content_or_empty,
                    record,
                    args,
                    language,
                    record_index,
                )
            else:
                future = None
            pending.append((record_index, record, future))

    try:
        fill_pending()
        while pending:
            record_index, record, future = pending.pop(0)
            content = "" if future is None else future.result()
            fill_pending()
            yield PrefetchedRecord(record_index, record, content)
    finally:
        for _, _, future in pending:
            if future is not None:
                future.cancel()
        executor.shutdown(wait=True, cancel_futures=True)


def _record_content_or_empty(
    record: dict[str, Any],
    args: argparse.Namespace,
    language: str,
    record_index: int,
) -> str:
    """Return record content, skipping records with transient fetch failures.

    Args:
        record: Corpus record to fetch or inspect.
        args: Manifest builder arguments.
        language: Registry language currently being sampled.
        record_index: One-based corpus record index for progress output.

    Returns:
        Source content, or an empty string when this single record could not be
        fetched.
    """

    try:
        return _record_content(record, args)
    except _CorpusCollectionError as exc:
        _emit_manifest_progress(
            args,
            f"[stack-v2 manifest] language={language} skipped-content "
            f"record={record_index} error={exc}",
        )
        return ""


def _next_record(
    record_iterator: Iterator[tuple[int, dict[str, Any]]],
    args: argparse.Namespace,
) -> tuple[int, dict[str, Any]]:
    """Return the next corpus record, serializing Hugging Face stream reads.

    Args:
        record_iterator: Enumerated corpus iterator.
        args: Manifest builder arguments.

    Returns:
        The next ``(record_index, record)`` pair.
    """

    if args.input_jsonl is not None:
        return next(record_iterator)
    with _HUGGINGFACE_DATASET_ITERATION_LOCK:
        return next(record_iterator)


def _needs_stack_v2_content_source(args: argparse.Namespace) -> bool:
    return args.dataset == DEFAULT_DATASET and not args.fetch_stack_v2_content


def _stack_v2_content_source_message() -> str:
    return (
        "The official bigcode/the-stack-v2 stream contains file IDs, not source text. "
        "Generate the manifest from a JSONL export with a content/code/text field, "
        "or pass --fetch-stack-v2-content after installing boto3 plus smart_open. "
        "Unsigned public S3 requests are used by default."
    )


def _download_stack_v2_content(
    record: dict[str, Any],
    s3_content_prefix: str,
    *,
    sign_requests: bool,
    max_content_chars: int,
) -> str:
    blob_id = record.get("blob_id")
    if not blob_id:
        return ""

    try:
        from smart_open import open as smart_open
    except ImportError as exc:
        raise SystemExit(
            "--fetch-stack-v2-content requires smart_open. Install smart_open[s3], "
            "or use --input-jsonl with source content."
        ) from exc

    encoding = str(record.get("src_encoding") or "utf-8")
    s3_url = f"{s3_content_prefix.rstrip('/')}/{blob_id}"
    try:
        s3_client = _stack_v2_s3_client(sign_requests=sign_requests)
        with smart_open(
            s3_url,
            "rb",
            compression=".gz",
            transport_params={"client": s3_client},
        ) as infile:
            read_size = -1 if max_content_chars == 0 else max_content_chars + 1
            content = infile.read(read_size).decode(encoding, errors="replace")
            return _content_within_size_limit(content, max_content_chars)
    except Exception as exc:
        raise _CorpusCollectionError(
            f"Could not fetch Stack v2 content for {blob_id}: {exc}"
        ) from exc


def _stack_v2_s3_client(*, sign_requests: bool):
    try:
        import boto3
    except ImportError as exc:
        raise SystemExit(
            "--fetch-stack-v2-content requires boto3. Install boto3, or use "
            "--input-jsonl with source content."
        ) from exc

    if sign_requests:
        return boto3.Session().client("s3")

    from botocore import UNSIGNED
    from botocore.client import Config

    return boto3.client(
        "s3",
        region_name="us-east-1",
        config=Config(signature_version=UNSIGNED),
    )


def _has_stack_v2_content_pointer(record: dict[str, Any]) -> bool:
    return isinstance(record.get("blob_id"), str) and isinstance(record.get("src_encoding"), str)


def _first_text_field(record: dict[str, Any], fields: Iterable[str | None]) -> str:
    for field in fields:
        if field and isinstance(record.get(field), str):
            return record[field]
    return ""


def _first_existing_field(record: dict[str, Any], fields: Iterable[str]) -> str | None:
    return next((field for field in fields if field in record), None)


def _normalize_language(value: Any) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def _language_match_keys(value: Any) -> set[str]:
    """Return normalized keys for comparing Stack v2 language labels.

    Args:
        value: Registry key, configured Stack label, or corpus row language.

    Returns:
        The conventional normalized label plus a punctuation-insensitive key
        for labels long enough to avoid short C-family collisions.
    """

    normalized = _normalize_language(value)
    compact = "".join(char for char in normalized if char.isalnum())
    keys = {normalized}
    if len(compact) >= 3:
        keys.add(compact)
    return keys


def _source_identity(record: dict[str, Any], record_index: int) -> str:
    for fields in (ID_FIELDS, PATH_FIELDS):
        value = _first_text_field(record, fields)
        if value:
            return value
    return f"record-{record_index}"


def _classify_comment(syntax: CommentSyntax, raw_comment: str) -> tuple[str, str]:
    stripped = raw_comment.strip()
    examples = [*syntax.shared_regex_examples, *syntax.canonical_regex_examples]
    examples.extend(syntax.shared_nested_examples)
    examples.extend(syntax.canonical_nested_examples)

    matching_nested_delimiters = []
    for open_delim, close_delim in syntax.nested_delimiters:
        if stripped.startswith(open_delim) and stripped.endswith(close_delim):
            if _contains_nested_opener(stripped, open_delim):
                return "nested", f"{open_delim}...{close_delim}"
            matching_nested_delimiters.append((open_delim, close_delim))

    for example in examples:
        if example.kind != "block":
            continue
        wrapper = _block_wrapper(example.expected_match)
        if wrapper is not None and stripped.startswith(wrapper[0]) and stripped.endswith(
            wrapper[1]
        ):
            return "block", f"{wrapper[0]}...{wrapper[1]}"

    if matching_nested_delimiters:
        open_delim, close_delim = matching_nested_delimiters[0]
        return "nested", f"{open_delim}...{close_delim}"

    for example in _examples_by_opener_length(examples):
        if example.kind == "line":
            continue
        opener = _line_opener(example.expected_match)
        if opener and stripped.startswith(opener):
            return example.kind, opener

    for example in _examples_by_opener_length(examples):
        if example.kind != "line":
            continue
        opener = _line_opener(example.expected_match)
        if opener and stripped.startswith(opener):
            return "line", opener

    if "\n" in raw_comment:
        return "block", "multiline"
    return "line", "single-line"


def _contains_nested_opener(raw_comment: str, open_delim: str) -> bool:
    """Return ``True`` when a wrapped comment contains another opener.

    Args:
        raw_comment: Stripped raw comment text.
        open_delim: Opening delimiter already matched at the start.

    Returns:
        Whether the same opener appears again inside the comment body.
    """

    return raw_comment.find(open_delim, len(open_delim)) != -1


def _examples_by_opener_length(examples: Iterable[Any]) -> list[Any]:
    """Return examples ordered so specific line-like openers win first.

    Args:
        examples: Comment examples whose expected matches may share opener
            prefixes.

    Returns:
        Examples sorted by descending opener length.
    """

    return sorted(
        examples,
        key=lambda example: len(_line_opener(example.expected_match)),
        reverse=True,
    )


def _line_opener(expected_match: str) -> str:
    first_line = expected_match.strip().splitlines()[0]
    if "note" in first_line:
        return first_line.split("note", 1)[0].strip()
    return first_line.split(maxsplit=1)[0] if first_line else ""


def _block_wrapper(expected_match: str) -> tuple[str, str] | None:
    for marker in ("block note", "note", "outer", "inner"):
        if marker in expected_match:
            start = expected_match.index(marker)
            end = expected_match.rindex(marker) + len(marker)
            opener = expected_match[:start].strip()
            closer = expected_match[end:].strip()
            if opener and closer:
                return opener, closer
    return None


def _build_case(
    *,
    language: str,
    kind: str,
    syntax_label: str,
    record: dict[str, Any],
    record_index: int,
    match_index: int,
    content: str,
    match_start: int,
    match_end: int,
    raw_comment: str,
    cleaned_comment: str,
    source_root: Path,
    context_chars: int,
) -> StackCase:
    start = match_start
    end = match_end
    case_id = _case_id(language, kind, record, record_index, match_index, raw_comment)
    source_file = (source_root / f"{case_id}.txt").resolve()
    source_file.write_text(content, encoding="utf-8")
    line, column = _line_column(content, start)

    return StackCase(
        case_id=case_id,
        language=language,
        comment_kind=kind,
        syntax_label=syntax_label,
        source_file=str(source_file),
        source_id=_first_text_field(record, ID_FIELDS),
        repo=_first_text_field(record, REPO_FIELDS),
        path=_first_text_field(record, PATH_FIELDS),
        match_start=start,
        match_end=end,
        match_line=line,
        match_column=column,
        raw_comment=raw_comment,
        cleaned_comment=cleaned_comment,
        source_excerpt=_excerpt(content, start, end, context_chars),
    )


def _case_id(
    language: str,
    kind: str,
    record: dict[str, Any],
    record_index: int,
    match_index: int,
    raw_comment: str,
) -> str:
    identity = "|".join(
        [
            language,
            kind,
            _source_identity(record, record_index),
            str(match_index),
            raw_comment,
        ]
    )
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]
    return f"{_safe_slug(language)}-{kind}-{digest}"


def _safe_slug(value: str) -> str:
    return "".join(char if char.isalnum() else "_" for char in value.lower()).strip("_")


def _excerpt(content: str, start: int, end: int, context_chars: int) -> str:
    excerpt_start = max(0, start - context_chars)
    excerpt_end = min(len(content), end + context_chars)
    relative_start = start - excerpt_start
    relative_end = end - excerpt_start
    excerpt = content[excerpt_start:excerpt_end]
    marked_excerpt = (
        excerpt[:relative_start]
        + "<<<TARGET_COMMENT_START>>>"
        + excerpt[relative_start:relative_end]
        + "<<<TARGET_COMMENT_END>>>"
        + excerpt[relative_end:]
    )
    prefix = "" if excerpt_start == 0 else "[... omitted prefix ...]\n"
    suffix = "" if excerpt_end == len(content) else "\n[... omitted suffix ...]"
    return prefix + marked_excerpt + suffix


def _line_column(content: str, offset: int) -> tuple[int, int]:
    """Return one-based line and column for ``offset``."""

    line = content.count("\n", 0, offset) + 1
    line_start = content.rfind("\n", 0, offset) + 1
    column = offset - line_start + 1
    return line, column


def _format_collected_progress(
    collected: dict[str, list[StackCase]], target_kinds: tuple[str, ...], per_kind: int
) -> str:
    counts = _counts_by_kind(_flatten_cases(collected))
    return _format_progress_counts(counts, target_kinds, per_kind)


def _flatten_cases(collected: dict[str, list[StackCase]]) -> list[StackCase]:
    return [case for cases in collected.values() for case in cases]


def _counts_by_kind(cases: Iterable[StackCase]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for case in cases:
        counts[case.comment_kind] += 1
    return dict(counts)


def _write_failures(failure_path: Path, failures: list[StackFailure]) -> None:
    if not failures:
        if failure_path.exists():
            failure_path.unlink()
        return
    failure_path.parent.mkdir(parents=True, exist_ok=True)
    with failure_path.open("w", encoding="utf-8") as outfile:
        for failure in failures:
            outfile.write(json.dumps(failure.to_json(), ensure_ascii=False) + "\n")


def _print_summary(
    manifest_path: Path,
    failure_path: Path,
    cases: list[StackCase],
    failures: list[StackFailure],
    per_kind: int,
) -> None:
    print(f"Wrote {manifest_path}")
    print(f"Collected {len(cases)} judge cases")
    if failures:
        print(f"Wrote {failure_path}", file=sys.stderr)
        print("Incomplete buckets:", file=sys.stderr)
        for failure in failures:
            print(
                f"  {failure.language}/{failure.comment_kind}: "
                f"{failure.observed_count}/{per_kind} "
                f"after {failure.scanned_records} scanned records",
                file=sys.stderr,
            )


def _exit_cli(status: int) -> None:
    """Exit the standalone CLI without running fragile streaming finalizers.

    Hugging Face streaming over pyarrow can leave background iterator state that
    crashes during normal interpreter shutdown after early termination. The
    manifest and source files are already flushed by this point, so the CLI uses
    a direct process exit after flushing standard streams.
    """

    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(status)


if __name__ == "__main__":
    _exit_cli(main())
