#!/usr/bin/env python3
"""Run deterministic Unicode-heavy property fuzzing over comment parsers."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import warnings
from dataclasses import asdict, dataclass
from typing import Sequence

from ml4setk import CommentQuery, CommentSanitizer
from ml4setk.Parsing.Comments import get_supported_comment_languages

DEFAULT_SEED = 0xC0FFEE

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
    """One reproducible parser invariant failure."""

    language: str
    language_seed: int
    case_index: int
    invariant: str
    text_repr: str
    detail: str


@dataclass(frozen=True)
class FuzzRun:
    """Summary returned by ``run_fuzz`` and printed by the CLI."""

    seed: int
    languages: int
    cases: int
    failures: tuple[FuzzFailure, ...]


class _InvariantFailure(AssertionError):
    pass


def _stable_language_seed(seed: int, language: str) -> int:
    digest = hashlib.blake2b(
        f"{seed}:{language}".encode("utf-8"),
        digest_size=8,
    ).digest()
    return int.from_bytes(digest, "big")


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


def _check_case(
    language: str,
    query: CommentQuery,
    sanitizer: CommentSanitizer,
    text: str,
) -> None:
    ranges = query.parse_ranges(text)
    iter_ranges = list(query.iter_ranges(text))
    matches = query.parse(text)

    if ranges != iter_ranges:
        raise _InvariantFailure("parse_ranges and iter_ranges disagree")
    if query.contains(text) != bool(ranges):
        raise _InvariantFailure("contains disagrees with parse_ranges")
    if len(ranges) != len(matches):
        raise _InvariantFailure("parse_ranges and parse returned different counts")

    previous_end = 0
    for index, ((start, end), match) in enumerate(zip(ranges, matches)):
        if not 0 <= start <= end <= len(text):
            raise _InvariantFailure(f"match {index} has out-of-bounds range {(start, end)!r}")
        if index and start < previous_end:
            raise _InvariantFailure(f"match {index} overlaps the preceding single-language match")
        if match.prefix != text[:start]:
            raise _InvariantFailure(f"match {index} has an incorrect prefix")
        if match.match != text[start:end]:
            raise _InvariantFailure(f"match {index} does not equal its source slice")
        if match.suffix != text[end:]:
            raise _InvariantFailure(f"match {index} has an incorrect suffix")
        if match.prefix + match.match + match.suffix != text:
            raise _InvariantFailure(f"match {index} does not reconstruct the source")
        if not isinstance(sanitizer.sanitize(match), str):
            raise _InvariantFailure(f"match {index} sanitizer result is not text")
        previous_end = end


def run_fuzz(
    *,
    languages: Sequence[str] | None = None,
    seed: int = DEFAULT_SEED,
    cases_per_language: int = 100,
    max_length: int = 128,
    max_failures: int = 20,
) -> FuzzRun:
    """Fuzz parser contracts with stable per-language random streams."""

    if cases_per_language < 1:
        raise ValueError("cases_per_language must be at least 1")
    if max_length < 0:
        raise ValueError("max_length must not be negative")
    if max_failures < 1:
        raise ValueError("max_failures must be at least 1")

    selected = tuple(sorted(languages or get_supported_comment_languages()))
    failures: list[FuzzFailure] = []
    cases_run = 0

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Promela parsing only supports native",
            category=UserWarning,
        )
        for language in selected:
            language_seed = _stable_language_seed(seed, language)
            rng = random.Random(language_seed)
            query = CommentQuery(language)
            sanitizer = CommentSanitizer(language)

            for case_index in range(cases_per_language):
                text = _random_text(rng, max_length)
                cases_run += 1
                try:
                    _check_case(language, query, sanitizer, text)
                except Exception as exc:
                    failures.append(
                        FuzzFailure(
                            language=language,
                            language_seed=language_seed,
                            case_index=case_index,
                            invariant=type(exc).__name__,
                            text_repr=repr(text),
                            detail=str(exc),
                        )
                    )
                    if len(failures) >= max_failures:
                        return FuzzRun(
                            seed=seed,
                            languages=len(selected),
                            cases=cases_run,
                            failures=tuple(failures),
                        )

    return FuzzRun(
        seed=seed,
        languages=len(selected),
        cases=cases_run,
        failures=tuple(failures),
    )


def _integer(value: str) -> int:
    return int(value, 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=_integer, default=DEFAULT_SEED)
    parser.add_argument("--cases-per-language", type=int, default=100)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--max-failures", type=int, default=20)
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
    )
    for failure in run.failures:
        print(json.dumps(asdict(failure), ensure_ascii=True, sort_keys=True))
    print(
        json.dumps(
            {
                "seed": run.seed,
                "languages": run.languages,
                "cases": run.cases,
                "failures": len(run.failures),
            },
            sort_keys=True,
        )
    )
    return int(bool(run.failures))


if __name__ == "__main__":
    raise SystemExit(main())
