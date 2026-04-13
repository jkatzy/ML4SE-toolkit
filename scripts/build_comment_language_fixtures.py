"""Generate one parser fixture code file per implemented comment language."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ml4setk.Parsing.Comments import SUPPORTED_LANGUAGES, get_comment_syntax

FIXTURE_DIR = Path("tests/fixtures/comment_languages")
FIXTURE_SUFFIX = ".code"


@dataclass(frozen=True)
class FixtureCase:
    content: str
    expected_match: Optional[str] = None
    forbidden_sentinel: Optional[str] = None


@dataclass(frozen=True)
class CommentLanguageFixture:
    language: str
    filename: str
    content: str
    expected_matches: tuple[str, ...]
    forbidden_sentinels: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed one parser fixture code file per implemented comment language."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rewrite existing fixture files from registry examples.",
    )
    return parser.parse_args()


def language_fixture_stem(language: str) -> str:
    """Return a stable filesystem-safe stem for a registry language key."""

    parts = []
    for char in language:
        if char.isascii() and char.isalnum():
            parts.append(char.lower())
        elif char == "+":
            parts.append("_plus_")
        elif char == "#":
            parts.append("_sharp_")
        else:
            parts.append("_")

    stem = re.sub(r"_+", "_", "".join(parts)).strip("_")
    if not stem:
        raise ValueError(f"Cannot build fixture filename for language: {language!r}")
    return stem


def language_fixture_filename(language: str) -> str:
    return f"{language_fixture_stem(language)}{FIXTURE_SUFFIX}"


def language_fixture_path(language: str, fixture_dir: Path = FIXTURE_DIR) -> Path:
    return fixture_dir / language_fixture_filename(language)


def expected_matches_for_language(language: str) -> tuple[str, ...]:
    return tuple(
        case.expected_match
        for case in build_fixture_cases(language)
        if case.expected_match is not None
    )


def forbidden_sentinels_for_language(language: str) -> tuple[str, ...]:
    return tuple(
        case.forbidden_sentinel
        for case in build_fixture_cases(language)
        if case.forbidden_sentinel is not None
    )


def build_fixture_cases(language: str) -> tuple[FixtureCase, ...]:
    examples = _registry_examples_for_language(language)
    cases = _seeded_cases_for_examples(examples)
    cases.extend(_repeated_opener_cases_for_examples(examples))
    cases.extend(_inline_block_cases_for_examples(examples))
    cases.extend(_star_prefixed_block_cases_for_examples(examples))
    cases.extend(_grouped_line_cases_for_examples(examples))
    cases.extend(_string_probe_cases_for_examples(examples))
    return tuple(cases)


def _registry_examples_for_language(language: str):
    syntax = get_comment_syntax(language)

    examples = [*syntax.shared_regex_examples]
    if language == syntax.canonical_name:
        examples.extend(syntax.canonical_regex_examples)
    elif not syntax.shared_regex_examples:
        examples.extend(syntax.canonical_regex_examples)

    examples.extend(syntax.shared_nested_examples)
    if language == syntax.canonical_name:
        examples.extend(syntax.canonical_nested_examples)
    elif not syntax.shared_nested_examples:
        examples.extend(syntax.canonical_nested_examples)

    return tuple(examples)


def _seeded_cases_for_examples(examples) -> list[FixtureCase]:
    cases = []
    for index, example in enumerate(examples, start=1):
        expected_match = _unique_fixture_match(
            example.expected_match,
            f"fixture_{index}",
            example.kind,
        )
        cases.append(FixtureCase(content=expected_match, expected_match=expected_match))
    return cases


def _repeated_opener_cases_for_examples(examples) -> list[FixtureCase]:
    cases = []
    for index, example in enumerate(examples, start=1):
        if example.kind != "line":
            continue

        expected_match = _repeated_line_opener_match(
            example.expected_match,
            f"repeated_open_{index}",
        )
        if expected_match is None:
            continue
        cases.append(FixtureCase(content=expected_match, expected_match=expected_match))

        odd_expected_match = _odd_repeated_line_opener_match(
            example.expected_match,
            f"odd_repeated_open_{index}",
        )
        if odd_expected_match is not None:
            cases.append(
                FixtureCase(content=odd_expected_match, expected_match=odd_expected_match)
            )
    return cases


def _inline_block_cases_for_examples(examples) -> list[FixtureCase]:
    cases = []
    for index, example in enumerate(examples, start=1):
        if example.kind not in {"block", "nested"} or not example.inline_compatible:
            continue

        expected_match = _unique_fixture_match(
            example.expected_match,
            f"inline_block_{index}",
            example.kind,
        )
        cases.append(
            FixtureCase(
                content=f"value_inline_{index} = 1 {expected_match} + 2",
                expected_match=expected_match,
            )
        )
    return cases


def _star_prefixed_block_cases_for_examples(examples) -> list[FixtureCase]:
    cases = []
    for index, example in enumerate(examples, start=1):
        if example.kind not in {"block", "nested"}:
            continue

        expected_match = _star_prefixed_block_match(
            example.expected_match,
            f"star_doc_{index}",
        )
        if expected_match is None:
            continue
        cases.append(FixtureCase(content=expected_match, expected_match=expected_match))
    return cases


def _grouped_line_cases_for_examples(examples) -> list[FixtureCase]:
    cases = []
    for index, example in enumerate(examples, start=1):
        if example.kind != "line" or not example.grouped_line_compatible:
            continue

        first_line = _unique_fixture_match(
            example.expected_match,
            f"grouped_line_{index}_a",
            example.kind,
        )
        second_line = _unique_fixture_match(
            example.expected_match,
            f"grouped_line_{index}_b",
            example.kind,
        )
        expected_match = f"{first_line}\n{second_line}"
        cases.append(FixtureCase(content=expected_match, expected_match=expected_match))
    return cases


def _string_probe_cases_for_examples(examples) -> list[FixtureCase]:
    cases = []
    comment_start_chars = _comment_start_characters(examples)
    for index, example in enumerate(examples, start=1):
        expected_match = _unique_fixture_match(
            example.expected_match,
            f"string_probe_{index}",
            example.kind,
        )
        quote = _quote_for_string_probe(expected_match, comment_start_chars)
        if quote is None:
            continue
        if f"string_probe_{index}" not in expected_match:
            continue

        cases.append(
            FixtureCase(
                content=f"value_string_{index} = {quote}not {expected_match}{quote};",
                forbidden_sentinel=f"string_probe_{index}",
            )
        )
    return cases


def build_fixture_content(language: str) -> str:
    chunks = [_code_separator(0)]
    for index, case in enumerate(build_fixture_cases(language), start=1):
        chunks.append(case.content)
        chunks.append(_code_separator(index))
    return "\n".join(chunks) + "\n"


def build_language_fixtures() -> tuple[CommentLanguageFixture, ...]:
    filenames = {}
    fixtures = []
    for language in SUPPORTED_LANGUAGES:
        filename = language_fixture_filename(language)
        if filename in filenames:
            raise ValueError(
                "Fixture filename collision: "
                f"{filenames[filename]!r} and {language!r} both map to {filename!r}"
            )

        filenames[filename] = language
        fixtures.append(
            CommentLanguageFixture(
                language=language,
                filename=filename,
                content=build_fixture_content(language),
                expected_matches=expected_matches_for_language(language),
                forbidden_sentinels=forbidden_sentinels_for_language(language),
            )
        )

    return tuple(fixtures)


def write_language_fixtures(project_root: Path = Path("."), *, force: bool = False) -> None:
    fixture_dir = project_root / FIXTURE_DIR
    fixture_dir.mkdir(parents=True, exist_ok=True)

    fixtures = build_language_fixtures()
    if force:
        expected_filenames = {fixture.filename for fixture in fixtures}
        for stale_path in fixture_dir.glob(f"*{FIXTURE_SUFFIX}"):
            if stale_path.name not in expected_filenames:
                stale_path.unlink()

    for fixture in fixtures:
        fixture_path = fixture_dir / fixture.filename
        if force or not fixture_path.exists():
            fixture_path.write_text(fixture.content, encoding="utf-8")


def _code_separator(index: int) -> str:
    return f"value_{index} = {index}"


def _unique_fixture_match(expected_match: str, marker: str, kind: str) -> str:
    """Keep delimiters intact while making fixture payloads unambiguous."""

    if "note" in expected_match:
        return expected_match.replace("note", marker)
    if "outer" in expected_match or "inner" in expected_match:
        return expected_match.replace("outer", f"{marker}_outer").replace(
            "inner", f"{marker}_inner"
        )
    if kind == "line" and "\n" not in expected_match:
        return f"{expected_match} {marker}"
    if expected_match.endswith((")", "]", "}")):
        return f"{expected_match[:-1]} {marker}{expected_match[-1]}"
    return expected_match


def _repeated_line_opener_match(expected_match: str, marker: str) -> Optional[str]:
    parts = _line_comment_parts(expected_match)
    if parts is None:
        return None

    indent, opener = parts
    if not _is_symbol_opener(opener):
        return None

    repeated_opener = _repeat_symbol_opener(opener)
    return f"{indent}{repeated_opener} {marker}"


def _odd_repeated_line_opener_match(expected_match: str, marker: str) -> Optional[str]:
    parts = _line_comment_parts(expected_match)
    if parts is None:
        return None

    indent, opener = parts
    if not _is_even_repeated_symbol_opener(opener):
        return None

    repeated_opener = f"{opener}{opener[0]}"
    return f"{indent}{repeated_opener} {marker}"


def _line_comment_parts(expected_match: str) -> Optional[tuple[str, str]]:
    if "note" in expected_match:
        prefix, suffix = expected_match.split("note", 1)
        if suffix.strip():
            return None
        return _split_indent_and_opener(prefix)

    stripped = expected_match.rstrip()
    if not stripped:
        return None

    prefix = stripped.split(maxsplit=1)[0]
    return _split_indent_and_opener(prefix)


def _split_indent_and_opener(prefix: str) -> Optional[tuple[str, str]]:
    prefix = prefix.rstrip()
    if not prefix:
        return None

    opener_start = len(prefix)
    for index, char in enumerate(prefix):
        if not char.isspace():
            opener_start = index
            break

    indent = prefix[:opener_start]
    opener = prefix[opener_start:]
    if not opener:
        return None
    return indent, opener


def _is_symbol_opener(opener: str) -> bool:
    if opener == "\\":
        return False
    if opener == "/":
        return False
    return any(not char.isalnum() for char in opener) and all(
        not char.isalnum() and not char.isspace() for char in opener
    )


def _repeat_symbol_opener(opener: str) -> str:
    repeat_count = max(4, (8 + len(opener) - 1) // len(opener))
    return opener * repeat_count


def _is_even_repeated_symbol_opener(opener: str) -> bool:
    return (
        len(opener) > 1
        and len(opener) % 2 == 0
        and len(set(opener)) == 1
        and _is_symbol_opener(opener)
    )


def _star_prefixed_block_match(expected_match: str, marker: str) -> Optional[str]:
    bounds = _comment_payload_bounds(expected_match)
    if bounds is None:
        return None

    open_delim, close_delim = bounds
    if open_delim == "/*" and close_delim == "*/":
        open_delim = "/**"
        close_delim = " */"

    return f"{open_delim}\n{_star_prefixed_doc_body(marker)}\n{close_delim}"


def _comment_payload_bounds(expected_match: str) -> Optional[tuple[str, str]]:
    payload_markers = ("note", "outer", "inner")
    payload_starts = [
        expected_match.index(marker) for marker in payload_markers if marker in expected_match
    ]
    if payload_starts:
        payload_start = min(payload_starts)
        payload_end = max(
            expected_match.rindex(marker) + len(marker)
            for marker in payload_markers
            if marker in expected_match
        )
        open_delim = expected_match[:payload_start].rstrip()
        close_delim = expected_match[payload_end:].lstrip()
        if open_delim and close_delim:
            return open_delim, close_delim

    if len(expected_match) >= 2 and expected_match[0] in "([{" and expected_match[-1] in ")]}":
        return expected_match[0], expected_match[-1]
    return None


def _star_prefixed_doc_body(marker: str) -> str:
    return "\n".join(
        (
            f" * {marker} Description of what the method does.",
            " *",
            " * @param input Description of parameter.",
            " * @return Description of return value.",
            " * @throws Exception Description of exception.",
        )
    )


def _comment_start_characters(examples) -> set[str]:
    start_chars = set()
    for example in examples:
        expected_match = example.expected_match.lstrip()
        if expected_match:
            start_chars.add(expected_match[0])
    return start_chars


def _quote_for_string_probe(expected_match: str, comment_start_chars: set[str]) -> Optional[str]:
    if "\n" in expected_match or "\r" in expected_match:
        return None

    for quote in ('"', "'", "`"):
        if quote not in expected_match and quote not in comment_start_chars:
            return quote
    return None


def main() -> None:
    args = parse_args()
    write_language_fixtures(force=args.force)


if __name__ == "__main__":
    main()
