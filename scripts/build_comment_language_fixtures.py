"""Generate one parser fixture code file per implemented comment language."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from ml4setk.Parsing.Comments import SUPPORTED_LANGUAGES, get_comment_syntax

FIXTURE_DIR = Path("tests/fixtures/comment_languages")
FIXTURE_SUFFIX = ".code"


@dataclass(frozen=True)
class CommentLanguageFixture:
    language: str
    filename: str
    content: str
    expected_matches: tuple[str, ...]


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

    return tuple(
        _unique_fixture_match(example.expected_match, index)
        for index, example in enumerate(examples, start=1)
    )


def build_fixture_content(language: str) -> str:
    chunks = [_code_separator(0)]
    for index, expected_match in enumerate(expected_matches_for_language(language), start=1):
        chunks.append(expected_match)
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


def _unique_fixture_match(expected_match: str, index: int) -> str:
    """Keep delimiters intact while making fixture payloads unambiguous."""

    marker = f"fixture_{index}"
    if "note" in expected_match:
        return expected_match.replace("note", marker)
    if "outer" in expected_match or "inner" in expected_match:
        return expected_match.replace("outer", f"outer_{index}").replace(
            "inner", f"inner_{index}"
        )
    return expected_match


def main() -> None:
    args = parse_args()
    write_language_fixtures(force=args.force)


if __name__ == "__main__":
    main()
