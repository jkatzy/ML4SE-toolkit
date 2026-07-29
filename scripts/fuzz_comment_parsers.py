#!/usr/bin/env python3
"""Run deterministic Unicode-heavy property fuzzing over comments and cleaning."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import warnings
from dataclasses import asdict, dataclass
from typing import Iterator, Sequence

from ml4setk import (
    CommentQuery,
    CommentSanitizer,
    QueryMatch,
    sanitize_comment,
    sanitize_comment_text,
)
from ml4setk.Parsing.Comments import (
    CommentExample,
    CommentSyntax,
    get_supported_comment_languages,
)

DEFAULT_SEED = 0xC0FFEE
CAMPAIGNS = ("all", "parser", "sanitizer")

_EXAMPLE_BODY_PLACEHOLDERS = (
    "Remember the bull.",
    "Visible content",
    "block note",
    "inline note",
    "+ 100",
    "note",
)

# Structured cleaner payloads intentionally avoid whitespace and delimiter-only
# runs. Those have language-specific cleaning semantics and belong in fixtures
# or judge cases rather than in a universal metamorphic oracle.
SANITIZER_PAYLOAD_TOKENS = (
    "alpha",
    "019",
    "\u6f22\u5b57",
    "\u304b\u306a",
    "\ud55c\uae00",
    "\u041f\u0440\u0438\u0432\u0435\u0442",
    "\u0645\u0631\u062d\u0628\u0627",
    "\u05e2\u05d1\u05e8\u05ea",
    "\U0001f9ea",
    "e\u0301",
    "join\u200d",
    "ltr\u200e",
    "rtl\u200f",
    "nul\x00",
)

# Tokens are deliberately biased toward delimiters, non-ASCII scripts, unusual
# whitespace, bidi controls, and malformed decoded text.
FUZZ_TOKENS = (
    "",
    "a",
    "XYZ",
    "019",
    "#",
    "//",
    "/*",
    "*/",
    "--",
    "{-",
    "-}",
    "'",
    '"',
    "`",
    "\\",
    "()",
    "[]",
    "{}",
    ";:%!@$._=+<>?&|",
    " ",
    "\t",
    "\v",
    "\f",
    "\r",
    "\n",
    "\r\n",
    "\x00",
    "\x1c",
    "\x1d",
    "\x1e",
    "\x1f",
    "\u0085",
    "\u00a0",
    "\u1680",
    "\u2003",
    "\u2007",
    "\u2028",
    "\u2029",
    "\u202f",
    "\u205f",
    "\u3000",
    "\u0301",
    "\u200c",
    "\u200d",
    "\u200e",
    "\u200f",
    "\u202a",
    "\u202c",
    "\u6f22\u5b57",
    "\u304b\u306a",
    "\ud55c\uae00",
    "\u041f\u0440\u0438\u0432\u0435\u0442",
    "\u0645\u0631\u062d\u0628\u0627",
    "\u05e2\u05d1\u05e8\u05d9\u05ea",
    "\U0001f600",
    "\U0001f9ea",
    "\ud800",
    "\udcff",
)


@dataclass(frozen=True)
class FuzzFailure:
    """One reproducible parser or sanitizer invariant failure."""

    language: str
    language_seed: int
    case_index: int
    invariant: str
    text_repr: str
    detail: str
    campaign: str = "parser"
    mutation: str = "random_text"


@dataclass(frozen=True)
class FuzzRun:
    """Summary returned by ``run_fuzz`` and printed by the CLI."""

    seed: int
    languages: int
    cases: int
    failures: tuple[FuzzFailure, ...]
    campaign: str = "all"
    parser_cases: int = 0
    sanitizer_random_cases: int = 0
    sanitizer_structured_cases: int = 0


class _InvariantFailure(AssertionError):
    def __init__(self, invariant: str, detail: str):
        self.invariant = invariant
        super().__init__(detail)


def _stable_language_seed(seed: int, language: str) -> int:
    digest = hashlib.blake2b(
        f"{seed}:{language}".encode("utf-8"),
        digest_size=8,
    ).digest()
    return int.from_bytes(digest, "big")


def _stable_campaign_seed(seed: int, language: str, campaign: str) -> int:
    """Return a stable seed without shifting the legacy parser stream."""

    if campaign == "parser":
        return _stable_language_seed(seed, language)
    return _stable_language_seed(seed, f"{campaign}:{language}")


def _random_text(rng: random.Random, max_length: int) -> str:
    target_length = rng.randrange(max_length + 1)
    pieces: list[str] = []
    current_length = 0
    while current_length < target_length:
        token = rng.choice(FUZZ_TOKENS)
        if not token:
            continue
        pieces.append(token)
        current_length += len(token)
    return "".join(pieces)[:target_length]


def _check_parser_case(language: str, query: CommentQuery, text: str) -> None:
    ranges = query.parse_ranges(text)
    iter_ranges = list(query.iter_ranges(text))
    matches = query.parse(text)

    if ranges != iter_ranges:
        raise _InvariantFailure(
            "parser_range_api_parity",
            "parse_ranges and iter_ranges disagree",
        )
    if query.contains(text) != bool(ranges):
        raise _InvariantFailure(
            "parser_contains_parity",
            "contains disagrees with parse_ranges",
        )
    if len(ranges) != len(matches):
        raise _InvariantFailure(
            "parser_match_count",
            "parse_ranges and parse returned different counts",
        )

    previous_end = 0
    for index, ((start, end), match) in enumerate(zip(ranges, matches)):
        if not 0 <= start <= end <= len(text):
            raise _InvariantFailure(
                "parser_range_bounds",
                f"match {index} has out-of-bounds range {(start, end)!r}",
            )
        if index and start < previous_end:
            raise _InvariantFailure(
                "parser_range_order",
                f"match {index} overlaps the preceding single-language match",
            )
        if match.prefix != text[:start]:
            raise _InvariantFailure(
                "parser_prefix",
                f"match {index} has an incorrect prefix",
            )
        if match.match != text[start:end]:
            raise _InvariantFailure(
                "parser_source_slice",
                f"match {index} does not equal its source slice",
            )
        if match.suffix != text[end:]:
            raise _InvariantFailure(
                "parser_suffix",
                f"match {index} has an incorrect suffix",
            )
        if match.prefix + match.match + match.suffix != text:
            raise _InvariantFailure(
                "parser_reconstruction",
                f"match {index} does not reconstruct the source",
            )
        previous_end = end


def _check_case(
    language: str,
    query: CommentQuery,
    sanitizer: CommentSanitizer,
    text: str,
) -> None:
    """Backward-compatible combined check used by older imports of this script."""

    _check_parser_case(language, query, text)
    for index, match in enumerate(query.parse(text)):
        if not isinstance(sanitizer.sanitize(match), str):
            raise _InvariantFailure(
                "sanitizer_return_type",
                f"match {index} sanitizer result is not text",
            )


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _check_sanitizer_case(
    language: str,
    sanitizer: CommentSanitizer,
    text: str,
    *,
    expected: str | None = None,
) -> None:
    """Check contracts that are safe for arbitrary extracted comment text."""

    cleaned = sanitizer.sanitize(text)
    if not isinstance(cleaned, str):
        raise _InvariantFailure(
            "sanitizer_return_type",
            f"sanitize returned {type(cleaned).__name__}, not str",
        )
    if sanitizer.sanitize(text) != cleaned:
        raise _InvariantFailure(
            "sanitizer_determinism",
            "repeated sanitizer calls returned different text",
        )

    query_match_cleaned = sanitizer.sanitize(QueryMatch("prefix", "suffix", text))
    helper_cleaned = sanitize_comment(language, text)
    legacy_helper_cleaned = sanitize_comment_text(language, text)
    if not (cleaned == query_match_cleaned == helper_cleaned == legacy_helper_cleaned):
        raise _InvariantFailure(
            "sanitizer_api_parity",
            "str, QueryMatch, sanitize_comment, and sanitize_comment_text disagree",
        )
    if "\r" in cleaned:
        raise _InvariantFailure(
            "sanitizer_newline_normalization",
            "sanitized output contains a carriage return",
        )
    if len(cleaned) > len(text):
        raise _InvariantFailure(
            "sanitizer_non_expansion",
            f"sanitized output grew from {len(text)} to {len(cleaned)} code points",
        )
    if sanitizer.syntax.sanitizer_mode == "raw" and cleaned != _normalize_newlines(text):
        raise _InvariantFailure(
            "sanitizer_raw_mode",
            "raw sanitizer mode changed more than newline representation",
        )
    if expected is not None and cleaned != expected:
        raise _InvariantFailure(
            "sanitizer_structured_oracle",
            f"expected {expected!r}, got {cleaned!r}",
        )


def _iter_registry_examples(
    syntax: CommentSyntax,
    language: str,
) -> Iterator[tuple[str, int, CommentExample]]:
    groups = (
        ("shared_regex", syntax.shared_regex_examples),
        ("shared_nested", syntax.shared_nested_examples),
        ("shared_contextual", syntax.shared_contextual_examples),
    )
    for group_name, examples in groups:
        for example_index, example in enumerate(examples):
            yield group_name, example_index, example

    if language != syntax.canonical_name:
        return

    canonical_groups = (
        ("canonical_regex", syntax.canonical_regex_examples),
        ("canonical_nested", syntax.canonical_nested_examples),
        ("canonical_contextual", syntax.canonical_contextual_examples),
    )
    for group_name, examples in canonical_groups:
        for example_index, example in enumerate(examples):
            yield group_name, example_index, example


def _example_placeholder(text: str) -> str | None:
    return next(
        (placeholder for placeholder in _EXAMPLE_BODY_PLACEHOLDERS if placeholder in text),
        None,
    )


def _random_sanitizer_payload(rng: random.Random, payload_index: int) -> str:
    pieces = [rng.choice(SANITIZER_PAYLOAD_TOKENS) for _ in range(rng.randrange(1, 5))]
    return f"FZ{payload_index}A{''.join(pieces)}Z{payload_index}END"


def _iter_structured_sanitizer_cases(
    sanitizer: CommentSanitizer,
    rng: random.Random,
    payloads_per_example: int,
) -> Iterator[tuple[str, str, str]]:
    """Yield mutation name, raw comment, and expected cleaned text."""

    syntax = sanitizer.syntax
    language = sanitizer.language
    examples = tuple(_iter_registry_examples(syntax, language))

    for group_name, example_index, example in examples:
        placeholder = _example_placeholder(example.expected_match)
        if placeholder is None:
            continue
        baseline = sanitizer.sanitize(example.expected_match)
        for payload_index in range(payloads_per_example):
            payload = _random_sanitizer_payload(rng, payload_index)
            mutation = f"placeholder:{group_name}:{example_index}:payload:{payload_index}"
            yield (
                mutation,
                example.expected_match.replace(placeholder, payload, 1),
                baseline.replace(placeholder, payload, 1),
            )

    for delimiter_index, (open_token, close_token) in enumerate(syntax.nested_delimiters):
        payload = _random_sanitizer_payload(rng, delimiter_index)
        yield (
            f"nested_wrapper:{delimiter_index}",
            f"{open_token} {payload} {close_token}",
            payload,
        )

    for opener_index, open_token in enumerate(syntax.unclosed_block_openers):
        payload = _random_sanitizer_payload(rng, opener_index)
        yield (
            f"unclosed_wrapper:{opener_index}",
            f"{open_token} {payload}",
            payload,
        )

    for group_name, example_index, example in examples:
        raw_comment = example.expected_match
        if "\n" not in raw_comment or "\r" in raw_comment:
            continue
        expected = sanitizer.sanitize(raw_comment)
        yield (
            f"newline_crlf:{group_name}:{example_index}",
            raw_comment.replace("\n", "\r\n"),
            expected,
        )
        yield (
            f"newline_cr:{group_name}:{example_index}",
            raw_comment.replace("\n", "\r"),
            expected,
        )


def run_fuzz(
    *,
    languages: Sequence[str] | None = None,
    seed: int = DEFAULT_SEED,
    cases_per_language: int = 100,
    max_length: int = 128,
    max_failures: int = 20,
    campaign: str = "all",
    sanitizer_payloads_per_example: int = 4,
) -> FuzzRun:
    """Fuzz parser and sanitizer contracts with independent stable streams.

    ``FuzzRun.cases`` retains its historical meaning: random inputs processed
    by the selected campaign (rather than the sum of parser and sanitizer
    checks). The campaign-specific counters expose the additional work.
    """

    if cases_per_language < 1:
        raise ValueError("cases_per_language must be at least 1")
    if max_length < 0:
        raise ValueError("max_length must not be negative")
    if max_failures < 1:
        raise ValueError("max_failures must be at least 1")
    if campaign not in CAMPAIGNS:
        raise ValueError(f"campaign must be one of {', '.join(CAMPAIGNS)}")
    if sanitizer_payloads_per_example < 0:
        raise ValueError("sanitizer_payloads_per_example must not be negative")

    selected = tuple(sorted(languages or get_supported_comment_languages()))
    failures: list[FuzzFailure] = []
    parser_cases = 0
    sanitizer_random_cases = 0
    sanitizer_structured_cases = 0

    def build_run() -> FuzzRun:
        random_cases = parser_cases if campaign in {"all", "parser"} else sanitizer_random_cases
        return FuzzRun(
            seed=seed,
            languages=len(selected),
            cases=random_cases,
            failures=tuple(failures),
            campaign=campaign,
            parser_cases=parser_cases,
            sanitizer_random_cases=sanitizer_random_cases,
            sanitizer_structured_cases=sanitizer_structured_cases,
        )

    def record_failure(
        *,
        language: str,
        language_seed: int,
        case_index: int,
        failure_campaign: str,
        mutation: str,
        text: str,
        exc: Exception,
    ) -> None:
        invariant = exc.invariant if isinstance(exc, _InvariantFailure) else type(exc).__name__
        failures.append(
            FuzzFailure(
                language=language,
                language_seed=language_seed,
                case_index=case_index,
                invariant=invariant,
                text_repr=repr(text),
                detail=str(exc),
                campaign=failure_campaign,
                mutation=mutation,
            )
        )

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Promela parsing only supports native",
            category=UserWarning,
        )
        for language in selected:
            if campaign in {"all", "parser"}:
                parser_seed = _stable_campaign_seed(seed, language, "parser")
                parser_rng = random.Random(parser_seed)
                query = CommentQuery(language)
                for case_index in range(cases_per_language):
                    text = _random_text(parser_rng, max_length)
                    parser_cases += 1
                    try:
                        _check_parser_case(language, query, text)
                    except Exception as exc:
                        record_failure(
                            language=language,
                            language_seed=parser_seed,
                            case_index=case_index,
                            failure_campaign="parser",
                            mutation="random_text",
                            text=text,
                            exc=exc,
                        )
                        if len(failures) >= max_failures:
                            return build_run()

            if campaign not in {"all", "sanitizer"}:
                continue

            sanitizer = CommentSanitizer(language)
            sanitizer_seed = _stable_campaign_seed(
                seed,
                language,
                "sanitizer_random",
            )
            sanitizer_rng = random.Random(sanitizer_seed)
            for case_index in range(cases_per_language):
                text = _random_text(sanitizer_rng, max_length)
                sanitizer_random_cases += 1
                try:
                    _check_sanitizer_case(language, sanitizer, text)
                except Exception as exc:
                    record_failure(
                        language=language,
                        language_seed=sanitizer_seed,
                        case_index=case_index,
                        failure_campaign="sanitizer",
                        mutation="random_text",
                        text=text,
                        exc=exc,
                    )
                    if len(failures) >= max_failures:
                        return build_run()

            structured_seed = _stable_campaign_seed(
                seed,
                language,
                "sanitizer_structured",
            )
            structured_rng = random.Random(structured_seed)
            try:
                structured_cases = tuple(
                    _iter_structured_sanitizer_cases(
                        sanitizer,
                        structured_rng,
                        sanitizer_payloads_per_example,
                    )
                )
            except Exception as exc:
                record_failure(
                    language=language,
                    language_seed=structured_seed,
                    case_index=0,
                    failure_campaign="sanitizer",
                    mutation="structured_case_generation",
                    text="",
                    exc=exc,
                )
                if len(failures) >= max_failures:
                    return build_run()
                continue

            for case_index, (mutation, text, expected) in enumerate(structured_cases):
                sanitizer_structured_cases += 1
                try:
                    _check_sanitizer_case(
                        language,
                        sanitizer,
                        text,
                        expected=expected,
                    )
                except Exception as exc:
                    record_failure(
                        language=language,
                        language_seed=structured_seed,
                        case_index=case_index,
                        failure_campaign="sanitizer",
                        mutation=mutation,
                        text=text,
                        exc=exc,
                    )
                    if len(failures) >= max_failures:
                        return build_run()

    return build_run()


def _integer(value: str) -> int:
    return int(value, 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=_integer, default=DEFAULT_SEED)
    parser.add_argument("--cases-per-language", type=int, default=100)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--max-failures", type=int, default=20)
    parser.add_argument(
        "--campaign",
        choices=CAMPAIGNS,
        default="all",
        help="Contracts to fuzz; the default runs parser and sanitizer campaigns.",
    )
    parser.add_argument(
        "--sanitizer-payloads-per-example",
        type=int,
        default=4,
        help="Structured cleaner payload mutations per seeded registry example.",
    )
    parser.add_argument(
        "--languages",
        help="Comma-separated registry keys; the default fuzzes every supported key.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    supported = set(get_supported_comment_languages())
    languages = None
    if args.languages:
        languages = tuple(
            language.strip() for language in args.languages.split(",") if language.strip()
        )
        unknown = sorted(set(languages) - supported)
        if unknown:
            raise SystemExit("Unknown comment language keys: " + ", ".join(unknown))

    run = run_fuzz(
        languages=languages,
        seed=args.seed,
        cases_per_language=args.cases_per_language,
        max_length=args.max_length,
        max_failures=args.max_failures,
        campaign=args.campaign,
        sanitizer_payloads_per_example=args.sanitizer_payloads_per_example,
    )
    for failure in run.failures:
        print(json.dumps(asdict(failure), ensure_ascii=True, sort_keys=True))
    print(
        json.dumps(
            {
                "campaign": run.campaign,
                "seed": run.seed,
                "languages": run.languages,
                "cases": run.cases,
                "parser_cases": run.parser_cases,
                "sanitizer_random_cases": run.sanitizer_random_cases,
                "sanitizer_structured_cases": run.sanitizer_structured_cases,
                "failures": len(run.failures),
            },
            sort_keys=True,
        )
    )
    return int(bool(run.failures))


if __name__ == "__main__":
    raise SystemExit(main())
