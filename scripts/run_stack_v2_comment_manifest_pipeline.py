"""Run resumable per-language Stack v2 comment manifest shards.

The underlying manifest builder can sample more than one language, but a
long-running all-language job is easier to resume and audit when each registry
language owns an isolated output shard. This orchestrator invokes the builder
once per language, validates terminal shard output, and writes deterministic
aggregate files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections.abc import Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ml4setk.Parsing.Comments import (
    get_comment_syntax,
    get_supported_comment_languages,
)

SCHEMA_VERSION = 1
DEFAULT_DATASET = "bigcode/the-stack-v2-dedup"
DEFAULT_OUTPUT_ROOT = Path("tmp/stack_v2_comment_manifest_pipeline")
DEFAULT_FILES_PER_LANGUAGE = 50
DEFAULT_LANGUAGE_WORKERS = 1
DEFAULT_SCAN_MULTIPLIER = 500
DEFAULT_CONTENT_PREFETCH_WORKERS = 8
DEFAULT_CONTENT_PREFETCH_BUFFER_SIZE = 128
DEFAULT_MAX_CONTENT_CHARS = 1_000_000
DEFAULT_MAX_LINE_COMMENT_CHARS = 12_000
DEFAULT_CONTEXT_CHARS = 1200
DEFAULT_S3_CONTENT_PREFIX = "s3://softwareheritage/content"
DEFAULT_DATASET_CONFIG_OVERRIDES = {
    "hyphy": "HyPhy",
    "purescript": "PureScript",
}
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUILDER_SCRIPT = REPO_ROOT / "scripts" / "build_stack_v2_comment_judge_cases.py"
TERMINAL_STATUSES = frozenset({"success", "source_files_shortfall"})
COLLECTION_ERROR_REASON_PREFIX = "Could not finish collecting "
COLLECTION_ERROR_RECOMMENDATION_PREFIX = "Resolve the corpus access or streaming error"
SKIPPED_CONTENT_MARKER = re.compile(
    r"\[stack-v2 manifest\] language=(?P<language>[^\s=]+) "
    r"skipped-content record=(?P<record>[1-9][0-9]*) error=(?P<error>.+)"
)
SHARD_PERFORMANCE_CONFIG_KEYS = frozenset(
    {
        "content_prefetch_workers",
        "content_prefetch_buffer_size",
    }
)
SHARD_NON_SEMANTIC_CONFIG_KEYS = frozenset(
    {
        *SHARD_PERFORMANCE_CONFIG_KEYS,
        "python_executable",
    }
)
SHARD_PERFORMANCE_COMMAND_OPTIONS = frozenset(
    {
        "--content-prefetch-workers",
        "--content-prefetch-buffer-size",
    }
)


class ShardValidationError(ValueError):
    """Raised when a builder shard is not a valid terminal result."""


@dataclass(frozen=True)
class LanguageResult:
    """Validated output and status for one requested language."""

    status: dict[str, Any]
    manifest_rows: list[dict[str, Any]]
    failure_rows: list[dict[str, Any]]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the manifest pipeline command line."""

    parser = argparse.ArgumentParser(
        description=(
            "Build resumable per-language Stack v2 comment-manifest shards and "
            "deterministically aggregate their outputs."
        )
    )
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument(
        "--all-languages",
        action="store_true",
        help="Explicitly run every supported comment-language registry key.",
    )
    scope.add_argument(
        "--languages",
        help="Comma-separated exact registry language keys to run.",
    )
    parser.add_argument(
        "--dataset",
        default=DEFAULT_DATASET,
        help="Hugging Face dataset passed to each manifest-builder shard.",
    )
    parser.add_argument(
        "--dataset-revision",
        default=None,
        help=(
            "Optional Hugging Face dataset revision passed to every shard. Use an "
            "immutable commit SHA when exact corpus regeneration is required."
        ),
    )
    parser.add_argument("--split", default="train", help="Dataset split to stream.")
    parser.add_argument(
        "--dataset-config",
        default=None,
        help="Optional dataset config applied to every requested language.",
    )
    parser.add_argument(
        "--dataset-config-template",
        default="{stack_label}",
        help="Per-language dataset-config template passed to the builder.",
    )
    parser.add_argument(
        "--language-map",
        type=Path,
        default=None,
        help="Optional builder JSON language-map path.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Root for isolated language shards and aggregate files.",
    )
    parser.add_argument(
        "--builder-script",
        type=Path,
        default=DEFAULT_BUILDER_SCRIPT,
        help="Manifest builder to invoke once for each language.",
    )
    parser.add_argument(
        "--python-executable",
        default="python",
        help=(
            "Python executable used to invoke the manifest builder. The stable "
            "command name avoids invalidating resume fingerprints when uv uses "
            "a different ephemeral environment path."
        ),
    )
    parser.add_argument(
        "--files-per-language",
        type=int,
        default=DEFAULT_FILES_PER_LANGUAGE,
        help="Required distinct source-file quota for every language.",
    )
    parser.add_argument(
        "--language-workers",
        type=int,
        default=DEFAULT_LANGUAGE_WORKERS,
        help=(
            "Number of isolated language shards to run concurrently. This affects "
            "orchestration only and does not invalidate completed shards."
        ),
    )
    parser.add_argument(
        "--max-records-per-language",
        type=int,
        default=None,
        help=(
            "Maximum records scanned by each shard. Defaults to "
            "--files-per-language multiplied by 500."
        ),
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=10,
        help="Builder scan-progress interval.",
    )
    parser.add_argument(
        "--content-prefetch-workers",
        type=int,
        default=DEFAULT_CONTENT_PREFETCH_WORKERS,
        help="Builder source-content prefetch worker count.",
    )
    parser.add_argument(
        "--content-prefetch-buffer-size",
        type=int,
        default=DEFAULT_CONTENT_PREFETCH_BUFFER_SIZE,
        help="Builder source-content prefetch queue size.",
    )
    parser.add_argument(
        "--max-content-chars",
        type=int,
        default=DEFAULT_MAX_CONTENT_CHARS,
        help="Builder decoded source-file size limit; use 0 for no limit.",
    )
    parser.add_argument(
        "--max-line-comment-chars",
        type=int,
        default=DEFAULT_MAX_LINE_COMMENT_CHARS,
        help=(
            "Maximum builder line-comment match size; over-limit line candidates "
            "are skipped. Use 0 to disable."
        ),
    )
    parser.add_argument(
        "--context-chars",
        type=int,
        default=DEFAULT_CONTEXT_CHARS,
        help="Characters retained on each side of a sampled comment.",
    )
    parser.add_argument(
        "--s3-content-prefix",
        default=DEFAULT_S3_CONTENT_PREFIX,
        help="Software Heritage S3 content prefix passed to the builder.",
    )
    parser.add_argument(
        "--s3-sign-requests",
        action="store_true",
        help="Ask the builder to sign S3 content requests.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Suppress orchestrator and builder progress messages.",
    )
    return parser.parse_args(argv)


def _validate_args(args: argparse.Namespace) -> None:
    """Normalize numeric defaults and reject invalid run configuration."""

    if args.files_per_language < 1:
        raise SystemExit("--files-per-language must be at least 1")
    if args.language_workers < 1:
        raise SystemExit("--language-workers must be at least 1")
    if args.max_records_per_language is None:
        args.max_records_per_language = args.files_per_language * DEFAULT_SCAN_MULTIPLIER
    if args.max_records_per_language < 1:
        raise SystemExit("--max-records-per-language must be at least 1")
    if args.progress_every < 0:
        raise SystemExit("--progress-every must be non-negative")
    if args.content_prefetch_workers < 1:
        raise SystemExit("--content-prefetch-workers must be at least 1")
    if args.content_prefetch_buffer_size < 1:
        raise SystemExit("--content-prefetch-buffer-size must be at least 1")
    if args.max_content_chars < 0:
        raise SystemExit("--max-content-chars must be non-negative")
    if args.max_line_comment_chars < 0:
        raise SystemExit("--max-line-comment-chars must be non-negative")
    if args.context_chars < 0:
        raise SystemExit("--context-chars must be non-negative")
    if not args.dataset.strip():
        raise SystemExit("--dataset must not be empty")
    if args.dataset_revision is not None and not args.dataset_revision.strip():
        raise SystemExit("--dataset-revision must not be empty")
    if not args.python_executable.strip():
        raise SystemExit("--python-executable must not be empty")
    if not args.builder_script.is_file():
        raise SystemExit(f"--builder-script does not exist: {args.builder_script}")
    if args.language_map is not None and not args.language_map.is_file():
        raise SystemExit(f"--language-map does not exist: {args.language_map}")


def _selected_languages(args: argparse.Namespace) -> list[str]:
    """Resolve and validate the explicitly selected registry languages."""

    supported = list(get_supported_comment_languages())
    if args.all_languages:
        if not supported:
            raise SystemExit("the comment-language registry is empty")
        return supported

    requested = [item.strip() for item in (args.languages or "").split(",") if item.strip()]
    if not requested:
        raise SystemExit("--languages must contain at least one registry language")
    unknown = [language for language in requested if language not in supported]
    if unknown:
        raise SystemExit(
            "unsupported --languages value(s): "
            + ", ".join(unknown)
            + "; use exact comment-language registry keys"
        )
    return list(dict.fromkeys(requested))


def _safe_language_slug(language: str) -> str:
    """Return a readable, collision-resistant language shard name."""

    readable = re.sub(r"[^a-z0-9]+", "-", language.lower()).strip("-") or "language"
    digest = hashlib.sha256(language.encode("utf-8")).hexdigest()[:10]
    return f"{readable}-{digest}"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as infile:
        for chunk in iter(lambda: infile.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError:
        return str(resolved)


def _source_fingerprint(builder_script: Path) -> dict[str, Any]:
    """Fingerprint builder, parser, cleaner, and registry source inputs."""

    candidates = {
        builder_script.resolve(),
        (REPO_ROOT / "src" / "ml4setk" / "Parsing" / "Query.py").resolve(),
    }
    comments_root = REPO_ROOT / "src" / "ml4setk" / "Parsing" / "Comments"
    candidates.update(path.resolve() for path in comments_root.glob("*.py"))
    files = [
        {"path": _display_path(path), "sha256": _sha256_file(path)}
        for path in sorted(candidates, key=lambda item: str(item))
        if path.is_file()
    ]
    payload = {"algorithm": "sha256", "files": files}
    payload["digest"] = _json_fingerprint(files)
    return payload


def _language_map_config(path: Path | None) -> dict[str, str] | None:
    if path is None:
        return None
    return {"path": str(path.resolve()), "sha256": _sha256_file(path)}


def _common_config(args: argparse.Namespace) -> dict[str, Any]:
    """Return the exact non-language builder configuration."""

    return {
        "builder_script": str(args.builder_script.resolve()),
        "python_executable": args.python_executable,
        "dataset": args.dataset,
        "dataset_revision": args.dataset_revision,
        "split": args.split,
        "dataset_config": args.dataset_config,
        "dataset_config_template": args.dataset_config_template,
        "language_map": _language_map_config(args.language_map),
        "files_per_language": args.files_per_language,
        "max_records_per_language": args.max_records_per_language,
        "progress_every": args.progress_every,
        "content_prefetch_workers": args.content_prefetch_workers,
        "content_prefetch_buffer_size": args.content_prefetch_buffer_size,
        "max_content_chars": args.max_content_chars,
        "max_line_comment_chars": args.max_line_comment_chars,
        "context_chars": args.context_chars,
        "fetch_stack_v2_content": True,
        "s3_content_prefix": args.s3_content_prefix,
        "s3_sign_requests": args.s3_sign_requests,
        "no_progress": args.no_progress,
        "num_workers": 1,
        "manifest_name": "manifest.jsonl",
        "failure_name": "failures.jsonl",
    }


def _effective_dataset_config(
    args: argparse.Namespace,
    language: str,
) -> str | None:
    """Resolve a narrowly scoped per-language dataset config override."""

    if args.dataset_config is not None:
        return args.dataset_config
    if args.dataset == DEFAULT_DATASET:
        return DEFAULT_DATASET_CONFIG_OVERRIDES.get(language)
    return None


def _language_config(
    args: argparse.Namespace,
    language: str,
    shard_root: Path,
) -> dict[str, Any]:
    config = _common_config(args)
    config.update(
        {
            "language": language,
            "output_root": str(shard_root.resolve()),
            "dataset_config": _effective_dataset_config(args, language),
        }
    )
    return config


def _json_fingerprint(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _config_fingerprint(
    config: dict[str, Any],
    source_fingerprint: dict[str, Any],
) -> str:
    return _json_fingerprint({"config": config, "source_fingerprint": source_fingerprint})


def _shard_config_fingerprint(
    config: dict[str, Any],
    source_fingerprint: dict[str, Any],
) -> str:
    """Fingerprint shard semantics while excluding execution-only settings."""

    semantic_config = {
        key: value for key, value in config.items() if key not in SHARD_NON_SEMANTIC_CONFIG_KEYS
    }
    return _config_fingerprint(semantic_config, source_fingerprint)


def _builder_command(
    args: argparse.Namespace,
    language: str,
    shard_root: Path,
) -> list[str]:
    """Construct the exact single-language builder command."""

    command = [
        args.python_executable,
        str(args.builder_script.resolve()),
        "--dataset",
        args.dataset,
        "--split",
        args.split,
        "--dataset-config-template",
        args.dataset_config_template,
        "--languages",
        language,
        "--files-per-language",
        str(args.files_per_language),
        "--max-records-per-language",
        str(args.max_records_per_language),
        "--progress-every",
        str(args.progress_every),
        "--num-workers",
        "1",
        "--content-prefetch-workers",
        str(args.content_prefetch_workers),
        "--content-prefetch-buffer-size",
        str(args.content_prefetch_buffer_size),
        "--output-root",
        str(shard_root.resolve()),
        "--manifest-name",
        "manifest.jsonl",
        "--failure-name",
        "failures.jsonl",
        "--context-chars",
        str(args.context_chars),
        "--max-content-chars",
        str(args.max_content_chars),
        "--max-line-comment-chars",
        str(args.max_line_comment_chars),
        "--fetch-stack-v2-content",
        "--s3-content-prefix",
        args.s3_content_prefix,
    ]
    if args.dataset_revision is not None:
        command.extend(["--dataset-revision", args.dataset_revision])
    dataset_config = _effective_dataset_config(args, language)
    if dataset_config is not None:
        command.extend(["--dataset-config", dataset_config])
    if args.language_map is not None:
        command.extend(["--language-map", str(args.language_map.resolve())])
    if args.s3_sign_requests:
        command.append("--s3-sign-requests")
    if args.no_progress:
        command.append("--no-progress")
    return command


def _run_builder_process(
    command: Sequence[str],
    stdout_path: Path,
    stderr_path: Path,
) -> subprocess.CompletedProcess[str]:
    """Run one builder shard with bounded-memory log capture."""

    with (
        stdout_path.open("w", encoding="utf-8") as stdout,
        stderr_path.open("w", encoding="utf-8") as stderr,
    ):
        return subprocess.run(
            list(command),
            cwd=REPO_ROOT,
            stdout=stdout,
            stderr=stderr,
            text=True,
            check=False,
        )


def _read_jsonl(path: Path, *, required: bool) -> list[dict[str, Any]]:
    if not path.exists():
        if required:
            raise ShardValidationError(f"missing required output: {path.name}")
        return []

    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as infile:
        for line_number, line in enumerate(infile, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ShardValidationError(f"invalid JSON in {path.name}:{line_number}") from exc
            if not isinstance(row, dict):
                raise ShardValidationError(f"expected an object in {path.name}:{line_number}")
            rows.append(row)
    return rows


def _path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _shares_comment_syntax(returned_language: Any, requested_language: str) -> bool:
    """Return whether two labels resolve to the same registry syntax entry."""

    if not isinstance(returned_language, str) or not returned_language.strip():
        return False
    try:
        return get_comment_syntax(returned_language) is get_comment_syntax(requested_language)
    except NotImplementedError:
        return False


def _normalize_shard_row_language(
    row: dict[str, Any],
    *,
    index: int,
    row_kind: str,
    requested_language: str,
) -> tuple[dict[str, Any], bool]:
    """Copy a row and restore a builder-normalized language alias."""

    returned_language = row.get("language")
    if returned_language == requested_language:
        return dict(row), False
    if not _shares_comment_syntax(returned_language, requested_language):
        raise ShardValidationError(
            f"{row_kind} row {index} has language {returned_language!r}, "
            f"which does not share comment syntax with requested language "
            f"{requested_language!r}"
        )
    normalized = dict(row)
    normalized["language"] = requested_language
    return normalized, True


def _alias_unique_case_id(case_id: str, requested_language: str) -> str:
    """Namespace a normalized builder case ID by its requested registry alias."""

    return f"{case_id}--requested-{_safe_language_slug(requested_language)}"


def _validate_manifest_rows(
    rows: list[dict[str, Any]],
    *,
    language: str,
    shard_root: Path,
    quota: int,
) -> None:
    if len(rows) > quota:
        raise ShardValidationError(
            f"manifest has {len(rows)} rows, exceeding the {quota}-file quota"
        )

    case_ids: set[str] = set()
    source_ids: set[str] = set()
    resolved_shard = shard_root.resolve()
    for index, row in enumerate(rows, start=1):
        if row.get("language") != language:
            raise ShardValidationError(
                f"manifest row {index} has language {row.get('language')!r}, expected {language!r}"
            )
        case_id = row.get("case_id")
        source_id = row.get("source_id")
        source_file = row.get("source_file")
        if not isinstance(case_id, str) or not case_id:
            raise ShardValidationError(f"manifest row {index} has no case_id")
        if not isinstance(source_id, str) or not source_id:
            raise ShardValidationError(f"manifest row {index} has no source_id")
        if not isinstance(source_file, str) or not source_file:
            raise ShardValidationError(f"manifest row {index} has no source_file")
        if case_id in case_ids:
            raise ShardValidationError(f"duplicate case_id in manifest: {case_id}")
        if source_id in source_ids:
            raise ShardValidationError(f"duplicate source_id in manifest: {source_id}")
        case_ids.add(case_id)
        source_ids.add(source_id)

        resolved_source = Path(source_file).resolve()
        if not _path_is_within(resolved_source, resolved_shard):
            raise ShardValidationError(f"manifest source_file is outside its shard: {source_file}")
        if not resolved_source.is_file():
            raise ShardValidationError(f"manifest source_file is missing: {source_file}")


def _is_operational_collection_failure(failure: dict[str, Any]) -> bool:
    """Return whether a builder failure reports an interrupted corpus read."""

    reason = failure.get("reason")
    recommendation = failure.get("recommendation")
    return (isinstance(reason, str) and reason.startswith(COLLECTION_ERROR_REASON_PREFIX)) or (
        isinstance(recommendation, str)
        and recommendation.startswith(COLLECTION_ERROR_RECOMMENDATION_PREFIX)
    )


def _has_skipped_content_marker(
    stderr_path: Path,
    *,
    languages: set[str],
) -> bool:
    """Return whether stderr has an exact builder skipped-content marker."""

    if not stderr_path.is_file():
        return False
    with stderr_path.open(encoding="utf-8", errors="replace") as stderr:
        for raw_line in stderr:
            match = SKIPPED_CONTENT_MARKER.fullmatch(raw_line.rstrip("\r\n"))
            if match is not None and match.group("language") in languages:
                return True
    return False


def _validate_shard_outputs(
    shard_root: Path,
    *,
    language: str,
    quota: int,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate one successful builder invocation as a terminal shard."""

    raw_manifest_rows = _read_jsonl(shard_root / "manifest.jsonl", required=True)
    raw_failure_rows = _read_jsonl(shard_root / "failures.jsonl", required=False)
    manifest_rows: list[dict[str, Any]] = []
    for index, row in enumerate(raw_manifest_rows, start=1):
        normalized, alias_was_normalized = _normalize_shard_row_language(
            row,
            index=index,
            row_kind="manifest",
            requested_language=language,
        )
        case_id = normalized.get("case_id")
        if alias_was_normalized and isinstance(case_id, str) and case_id:
            normalized["case_id"] = _alias_unique_case_id(case_id, language)
        manifest_rows.append(normalized)

    failure_rows = [
        _normalize_shard_row_language(
            row,
            index=index,
            row_kind="failure",
            requested_language=language,
        )[0]
        for index, row in enumerate(raw_failure_rows, start=1)
    ]
    _validate_manifest_rows(
        manifest_rows,
        language=language,
        shard_root=shard_root,
        quota=quota,
    )

    for index, row in enumerate(failure_rows, start=1):
        if row.get("language") != language:
            raise ShardValidationError(
                f"failure row {index} has language {row.get('language')!r}, expected {language!r}"
            )

    if not failure_rows:
        if len(manifest_rows) != quota:
            raise ShardValidationError(
                f"manifest has {len(manifest_rows)}/{quota} rows without an "
                "explicit source_files failure"
            )
        return "success", manifest_rows, failure_rows

    if len(failure_rows) != 1:
        raise ShardValidationError(f"expected one source_files failure, found {len(failure_rows)}")
    failure = failure_rows[0]
    expected = failure.get("expected_count")
    observed = failure.get("observed_count")
    if failure.get("comment_kind") != "source_files":
        raise ShardValidationError(
            "the only accepted terminal failure has comment_kind='source_files'"
        )
    if _is_operational_collection_failure(failure):
        raise ShardValidationError(
            "source_files failure reports an operational corpus collection error"
        )
    if type(expected) is not int or expected != quota:
        raise ShardValidationError(f"source_files expected_count is {expected!r}, expected {quota}")
    if type(observed) is not int or observed != len(manifest_rows):
        raise ShardValidationError(
            "source_files observed_count does not match the manifest row count"
        )
    if observed >= quota:
        raise ShardValidationError("source_files failure does not describe a shortfall")
    marker_languages = {language}
    raw_failure_language = raw_failure_rows[0].get("language")
    if isinstance(raw_failure_language, str):
        marker_languages.add(raw_failure_language)
    if _has_skipped_content_marker(
        shard_root / "stderr.log",
        languages=marker_languages,
    ):
        raise ShardValidationError(
            "source_files shortfall includes skipped-content records; "
            "rerun the shard before accepting a corpus coverage shortfall"
        )
    return "source_files_shortfall", manifest_rows, failure_rows


def _status_record(
    *,
    language: str,
    status: str,
    config: dict[str, Any],
    source_fingerprint: dict[str, Any],
    fingerprint: str,
    command: list[str],
    return_code: int | None,
    manifest_count: int,
    failure_count: int,
    error: str | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "language": language,
        "status": status,
        "config": config,
        "source_fingerprint": source_fingerprint,
        "fingerprint": fingerprint,
        "command": command,
        "return_code": return_code,
        "manifest_count": manifest_count,
        "failure_count": failure_count,
    }
    if error is not None:
        record["error"] = error
    return record


def _read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def _command_without_options(
    command: Sequence[Any],
    options: frozenset[str],
) -> list[Any]:
    """Remove named CLI options and their values without relying on positions."""

    normalized: list[Any] = []
    index = 0
    while index < len(command):
        token = command[index]
        if isinstance(token, str):
            if token in options:
                index += 2
                continue
            if any(token.startswith(f"{option}=") for option in options):
                index += 1
                continue
        normalized.append(token)
        index += 1
    return normalized


def _resume_comparison_status(status: dict[str, Any]) -> dict[str, Any]:
    """Normalize execution-only resume metadata."""

    normalized = json.loads(json.dumps(status))
    normalized.pop("fingerprint", None)
    config = normalized.get("config")
    if isinstance(config, dict):
        for key in SHARD_NON_SEMANTIC_CONFIG_KEYS:
            config.pop(key, None)
    command = normalized.get("command")
    if isinstance(command, list) and command:
        command = _command_without_options(
            command,
            SHARD_PERFORMANCE_COMMAND_OPTIONS,
        )
        command[0] = "<python-executable>"
        normalized["command"] = command
    return normalized


def _resumable_result(
    *,
    shard_root: Path,
    language: str,
    quota: int,
    config: dict[str, Any],
    source_fingerprint: dict[str, Any],
    fingerprint: str,
    command: list[str],
) -> LanguageResult | None:
    status_path = shard_root / "status.json"
    if not status_path.is_file():
        return None
    try:
        existing = _read_json_object(status_path)
        if existing.get("status") not in TERMINAL_STATUSES:
            return None
        terminal_status, manifest_rows, failure_rows = _validate_shard_outputs(
            shard_root,
            language=language,
            quota=quota,
        )
        expected = _status_record(
            language=language,
            status=terminal_status,
            config=config,
            source_fingerprint=source_fingerprint,
            fingerprint=fingerprint,
            command=command,
            return_code=0,
            manifest_count=len(manifest_rows),
            failure_count=len(failure_rows),
        )
        if _resume_comparison_status(existing) != _resume_comparison_status(expected):
            return None
    except (OSError, ValueError, json.JSONDecodeError):
        return None

    # Keep the original config and command as truthful builder provenance, but
    # migrate legacy path/performance-derived fingerprints to the canonical
    # semantic fingerprint used by new shards and aggregate status entries.
    canonical_status = dict(existing)
    canonical_status["fingerprint"] = fingerprint
    if canonical_status != existing:
        try:
            _write_json(status_path, canonical_status)
        except OSError:
            return None
    return LanguageResult(canonical_status, manifest_rows, failure_rows)


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _write_json(path: Path, value: Any) -> None:
    content = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    _atomic_write_text(path, content)


def _write_jsonl(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    content = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    _atomic_write_text(path, content)


def _normalize_error(exc: Exception) -> str:
    text = " ".join(str(exc).split())
    return f"{type(exc).__name__}: {text}" if text else type(exc).__name__


def _run_language(
    *,
    args: argparse.Namespace,
    language: str,
    shard_root: Path,
    source_fingerprint: dict[str, Any],
) -> tuple[LanguageResult, bool]:
    """Resume or run one language; return its result and resume flag."""

    shard_root.mkdir(parents=True, exist_ok=True)
    config = _language_config(args, language, shard_root)
    fingerprint = _shard_config_fingerprint(config, source_fingerprint)
    command = _builder_command(args, language, shard_root)
    resumable = _resumable_result(
        shard_root=shard_root,
        language=language,
        quota=args.files_per_language,
        config=config,
        source_fingerprint=source_fingerprint,
        fingerprint=fingerprint,
        command=command,
    )
    if resumable is not None:
        return resumable, True

    for path in (shard_root / "manifest.jsonl", shard_root / "failures.jsonl"):
        if path.exists():
            path.unlink()

    return_code: int | None = None
    try:
        completed = _run_builder_process(
            command,
            shard_root / "stdout.log",
            shard_root / "stderr.log",
        )
        return_code = completed.returncode
        if return_code != 0:
            raise RuntimeError(
                f"builder exited with return code {return_code}; see {shard_root / 'stderr.log'}"
            )
        terminal_status, manifest_rows, failure_rows = _validate_shard_outputs(
            shard_root,
            language=language,
            quota=args.files_per_language,
        )
    except Exception as exc:
        status = _status_record(
            language=language,
            status="error",
            config=config,
            source_fingerprint=source_fingerprint,
            fingerprint=fingerprint,
            command=command,
            return_code=return_code,
            manifest_count=0,
            failure_count=0,
            error=_normalize_error(exc),
        )
        _write_json(shard_root / "status.json", status)
        return LanguageResult(status, [], []), False

    status = _status_record(
        language=language,
        status=terminal_status,
        config=config,
        source_fingerprint=source_fingerprint,
        fingerprint=fingerprint,
        command=command,
        return_code=0,
        manifest_count=len(manifest_rows),
        failure_count=len(failure_rows),
    )
    _write_json(shard_root / "status.json", status)
    return LanguageResult(status, manifest_rows, failure_rows), False


def _unexpected_language_error_result(
    *,
    args: argparse.Namespace,
    language: str,
    shard_root: Path,
    source_fingerprint: dict[str, Any],
    exc: Exception,
) -> LanguageResult:
    """Return a durable error result for failures outside normal shard handling."""

    error = _normalize_error(exc)
    try:
        config = _language_config(args, language, shard_root)
        fingerprint = _shard_config_fingerprint(config, source_fingerprint)
        command = _builder_command(args, language, shard_root)
    except Exception as config_exc:
        config = {
            "language": language,
            "output_root": str(shard_root.resolve()),
        }
        fingerprint = _json_fingerprint(
            {
                "config": config,
                "source_fingerprint": source_fingerprint,
            }
        )
        command = []
        error = f"{error}; status reconstruction failed: {_normalize_error(config_exc)}"

    status = _status_record(
        language=language,
        status="error",
        config=config,
        source_fingerprint=source_fingerprint,
        fingerprint=fingerprint,
        command=command,
        return_code=None,
        manifest_count=0,
        failure_count=0,
        error=error,
    )
    try:
        _write_json(shard_root / "status.json", status)
    except Exception as write_exc:
        status["error"] = (
            f"{status['error']}; could not write shard status: {_normalize_error(write_exc)}"
        )
    return LanguageResult(status, [], [])


def _run_language_safely(
    *,
    args: argparse.Namespace,
    language: str,
    shard_root: Path,
    source_fingerprint: dict[str, Any],
) -> tuple[LanguageResult, bool]:
    """Run one shard without allowing its failure to cancel other languages."""

    try:
        return _run_language(
            args=args,
            language=language,
            shard_root=shard_root,
            source_fingerprint=source_fingerprint,
        )
    except Exception as exc:
        return (
            _unexpected_language_error_result(
                args=args,
                language=language,
                shard_root=shard_root,
                source_fingerprint=source_fingerprint,
                exc=exc,
            ),
            False,
        )


def _run_requested_languages(
    *,
    args: argparse.Namespace,
    languages: Sequence[str],
    output_root: Path,
    source_fingerprint: dict[str, Any],
) -> list[tuple[str, Path, LanguageResult, bool]]:
    """Run isolated shards concurrently and return them in request order."""

    tasks = [
        (
            index,
            language,
            output_root / "languages" / _safe_language_slug(language),
        )
        for index, language in enumerate(languages, start=1)
    ]
    completed: dict[int, tuple[str, Path, LanguageResult, bool]] = {}

    def record(
        index: int,
        language: str,
        shard_root: Path,
        result: LanguageResult,
        resumed: bool,
    ) -> None:
        completed[index] = (language, shard_root, result, resumed)
        _emit(
            args,
            f"[manifest pipeline] language={language} index={index}/{len(tasks)} "
            f"status={result.status['status']} resumed={str(resumed).lower()}",
        )

    if args.language_workers == 1 or len(tasks) <= 1:
        for index, language, shard_root in tasks:
            result, resumed = _run_language_safely(
                args=args,
                language=language,
                shard_root=shard_root,
                source_fingerprint=source_fingerprint,
            )
            record(index, language, shard_root, result, resumed)
    else:
        worker_count = min(args.language_workers, len(tasks))
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures: dict[
                Future[tuple[LanguageResult, bool]],
                tuple[int, str, Path],
            ] = {
                executor.submit(
                    _run_language_safely,
                    args=args,
                    language=language,
                    shard_root=shard_root,
                    source_fingerprint=source_fingerprint,
                ): (index, language, shard_root)
                for index, language, shard_root in tasks
            }
            for future in as_completed(futures):
                index, language, shard_root = futures[future]
                result, resumed = future.result()
                record(index, language, shard_root, result, resumed)

    return [completed[index] for index, _, _ in tasks]


def _sorted_manifest_rows(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: (str(row.get("case_id", "")), str(row["source_id"])))


def _sorted_failure_rows(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            str(row.get("comment_kind", "")),
            str(row.get("reason", "")),
        ),
    )


def _aggregate_status_entry(
    language: str,
    shard_root: Path,
    status: dict[str, Any],
) -> dict[str, Any]:
    entry = {
        "language": language,
        "shard": str(shard_root.resolve()),
        "status": status["status"],
        "fingerprint": status["fingerprint"],
        "return_code": status["return_code"],
        "manifest_count": status["manifest_count"],
        "failure_count": status["failure_count"],
    }
    if "error" in status:
        entry["error"] = status["error"]
    return entry


def _emit(args: argparse.Namespace, message: str) -> None:
    if not args.no_progress:
        print(message, flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    """Run requested shards and write deterministic aggregate output."""

    args = parse_args(argv)
    _validate_args(args)
    languages = _selected_languages(args)
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    source_fingerprint = _source_fingerprint(args.builder_script)

    aggregate_manifest: list[dict[str, Any]] = []
    aggregate_failures: list[dict[str, Any]] = []
    aggregate_languages: list[dict[str, Any]] = []
    error_count = 0

    _emit(
        args,
        f"[manifest pipeline] start languages={len(languages)} "
        f"files_per_language={args.files_per_language} "
        f"language_workers={args.language_workers} output_root={output_root}",
    )
    language_results = _run_requested_languages(
        args=args,
        languages=languages,
        output_root=output_root,
        source_fingerprint=source_fingerprint,
    )
    for language, shard_root, result, _resumed in language_results:
        state = result.status["status"]
        if state == "error":
            error_count += 1
        else:
            aggregate_manifest.extend(_sorted_manifest_rows(result.manifest_rows))
            aggregate_failures.extend(_sorted_failure_rows(result.failure_rows))
        aggregate_languages.append(_aggregate_status_entry(language, shard_root, result.status))

    aggregate_config = _common_config(args)
    aggregate_config.update(
        {
            "scope": "all_languages" if args.all_languages else "languages",
            "languages": languages,
            "language_workers": args.language_workers,
            "output_root": str(output_root),
        }
    )
    aggregate_fingerprint = _config_fingerprint(
        aggregate_config,
        source_fingerprint,
    )
    aggregate_status = {
        "schema_version": SCHEMA_VERSION,
        "status": "error" if error_count else "complete",
        "config": aggregate_config,
        "source_fingerprint": source_fingerprint,
        "fingerprint": aggregate_fingerprint,
        "summary": {
            "language_count": len(languages),
            "success_count": sum(entry["status"] == "success" for entry in aggregate_languages),
            "source_files_shortfall_count": sum(
                entry["status"] == "source_files_shortfall" for entry in aggregate_languages
            ),
            "error_count": error_count,
            "manifest_count": len(aggregate_manifest),
            "failure_count": len(aggregate_failures),
        },
        "languages": aggregate_languages,
    }
    _write_jsonl(output_root / "manifest.jsonl", aggregate_manifest)
    _write_jsonl(output_root / "failures.jsonl", aggregate_failures)
    _write_json(output_root / "status.json", aggregate_status)
    _emit(
        args,
        f"[manifest pipeline] complete manifest={len(aggregate_manifest)} "
        f"failures={len(aggregate_failures)} errors={error_count}",
    )
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
