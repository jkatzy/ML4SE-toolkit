"""Generate one explicit comment-cleaning oracle per registry syntax family."""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ml4setk.Parsing.Comments import iter_comment_syntaxes
from ml4setk.Parsing.Comments.registry import CommentExample, CommentSyntax

FIXTURE_DIR = Path("tests/fixtures/comment_cleaning")
FIXTURE_SUFFIX = ".json"
SCHEMA_VERSION = 1

_PAYLOAD_PLACEHOLDERS = (
    "block note",
    "inline note",
    "note",
    "Visible content",
    "+ 100",
    "Remember the bull.",
)


@dataclass(frozen=True)
class CleaningFixtureCase:
    """One raw comment and its independently specified cleaned text."""

    case_id: str
    source: str
    kind: str
    raw_comment: str
    expected_cleaned: str
    payload_marker: Optional[str] = None

    def as_dict(self) -> dict:
        return {
            "id": self.case_id,
            "source": self.source,
            "kind": self.kind,
            "raw_comment": self.raw_comment,
            "expected_cleaned": self.expected_cleaned,
            "payload_marker": self.payload_marker,
        }


@dataclass(frozen=True)
class CommentCleaningFixture:
    """The cleaning contract shared by every alias in one syntax family."""

    family_name: str
    canonical_language: str
    language_keys: tuple[str, ...]
    sanitizer_mode: str
    cases: tuple[CleaningFixtureCase, ...]

    @property
    def filename(self) -> str:
        return family_fixture_filename(self.family_name)

    def as_dict(self) -> dict:
        return {
            "schema_version": SCHEMA_VERSION,
            "family_name": self.family_name,
            "canonical_language": self.canonical_language,
            "language_keys": list(self.language_keys),
            "sanitizer_mode": self.sanitizer_mode,
            "cases": [case.as_dict() for case in self.cases],
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed one comment-cleaning JSON fixture per registry syntax family."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rewrite fixtures and remove stale family files.",
    )
    return parser.parse_args()


def family_fixture_filename(family_name: str) -> str:
    """Return the stable JSON filename for a registry family."""

    if re.fullmatch(r"[a-z0-9_]+", family_name) is None:
        raise ValueError(f"Unsafe comment family name: {family_name!r}")
    return f"{family_name}{FIXTURE_SUFFIX}"


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _split_payload_placeholder(text: str) -> Optional[tuple[str, str]]:
    for placeholder in _PAYLOAD_PLACEHOLDERS:
        if placeholder in text:
            return tuple(text.split(placeholder, 1))
    return None


def _payload_marker(source_group: str, index: int) -> str:
    return f"cleaning_payload_{source_group}_{index:03d}"


def _example_source(attribute_name: str, index: int) -> str:
    return f"registry:{attribute_name}[{index}]"


def _matches_wrapper(text: str, open_delimiter: str, close_delimiter: str) -> bool:
    if any(char.isalpha() for char in open_delimiter + close_delimiter):
        return (
            text[: len(open_delimiter)].lower() == open_delimiter.lower()
            and text[len(text) - len(close_delimiter) :].lower() == close_delimiter.lower()
        )
    return text.startswith(open_delimiter) and text.endswith(close_delimiter)


def _normalize_expected_body(body: str) -> str:
    body = _normalize_newlines(body).strip("\n")
    if "\n" not in body:
        return body.strip()

    normalized = textwrap.dedent(body)
    return "\n".join(line.rstrip() for line in normalized.split("\n")).strip("\n")


def _normalize_block_inner(inner: str) -> str:
    inner = _normalize_newlines(inner)
    if inner.startswith("\n"):
        inner = inner[1:]
    else:
        inner = inner.lstrip(" \t")
    if inner.endswith("\n"):
        inner = inner[:-1]
    return _normalize_expected_body(inner)


def _line_wrapper_expected(
    syntax: CommentSyntax,
    raw_comment: str,
) -> Optional[str]:
    normalized = _normalize_newlines(raw_comment)
    if syntax.canonical_name == "slang":
        physical_lines = normalized.split("\n")
        if (
            normalized.startswith("//")
            and len(physical_lines) >= 2
            and all(line.endswith("\\") for line in physical_lines[:-1])
        ):
            body = normalized[2:]
            if body.startswith((" ", "\t")):
                body = body[1:]
            return _normalize_expected_body(body)

    if "\n" in normalized:
        return None

    if syntax.canonical_name == "bluespec_bh":
        dash_run = re.fullmatch(r"-{2,}(.*)", raw_comment)
        if dash_run is not None:
            return _normalize_expected_body(dash_run.group(1))

    if syntax.canonical_name == "linear_programming" and raw_comment.startswith("\\"):
        return _normalize_newlines(raw_comment[1:]).rstrip()

    for open_delimiter, close_delimiter in sorted(
        syntax.sanitizer_line_wrappers,
        key=lambda wrapper: len(wrapper[0]) + len(wrapper[1]),
        reverse=True,
    ):
        if not _matches_wrapper(raw_comment, open_delimiter, close_delimiter):
            continue
        inner_end = len(raw_comment) - len(close_delimiter) if close_delimiter else None
        inner = _normalize_newlines(raw_comment[len(open_delimiter) : inner_end])
        if inner.startswith((" ", "\t")):
            inner = inner[1:]
        return _normalize_expected_body(inner)

    return None


def _explicit_wrapper_expected(
    syntax: CommentSyntax,
    kind: str,
    raw_comment: str,
) -> Optional[str]:
    if kind in {"line", "directive"}:
        return _line_wrapper_expected(syntax, raw_comment)
    if kind in {"block", "nested"}:
        if syntax.canonical_name == "lua":
            lua_long = re.fullmatch(
                r"--\[(?P<equals>=*)\[(?P<body>[\s\S]*)\](?P=equals)\]",
                raw_comment,
            )
            if lua_long is not None:
                return _normalize_block_inner(lua_long.group("body"))
        wrappers = tuple(
            dict.fromkeys((*syntax.sanitizer_block_wrappers, *syntax.nested_delimiters))
        )
    else:
        return None

    for open_delimiter, close_delimiter in sorted(
        wrappers,
        key=lambda wrapper: len(wrapper[0]) + len(wrapper[1]),
        reverse=True,
    ):
        if not _matches_wrapper(raw_comment, open_delimiter, close_delimiter):
            continue
        inner_end = len(raw_comment) - len(close_delimiter) if close_delimiter else None
        inner = raw_comment[len(open_delimiter) : inner_end]
        return _normalize_block_inner(inner)

    return None


def _unclosed_wrapper_expected(
    syntax: CommentSyntax,
    raw_comment: str,
) -> Optional[str]:
    for open_delimiter in sorted(syntax.unclosed_block_openers, key=len, reverse=True):
        if any(char.isalpha() for char in open_delimiter):
            matches = raw_comment[: len(open_delimiter)].lower() == open_delimiter.lower()
        else:
            matches = raw_comment.startswith(open_delimiter)
        if matches:
            return _normalize_block_inner(raw_comment[len(open_delimiter) :])
    return None


def _example_case(
    syntax: CommentSyntax,
    example: CommentExample,
    attribute_name: str,
    index: int,
) -> CleaningFixtureCase:
    source_group = attribute_name.removesuffix("_examples")
    marker = _payload_marker(source_group, index)
    placeholder_parts = _split_payload_placeholder(example.expected_match)
    can_substitute = placeholder_parts is not None
    prefix = ""
    if can_substitute:
        prefix, suffix = placeholder_parts
        raw_comment = f"{prefix}{marker}{suffix}"
    else:
        raw_comment = example.expected_match

    has_inferred_regex_wrapper = (
        syntax.sanitizer_mode == "wrapped"
        and example.kind in {"line", "block", "directive"}
        and attribute_name.endswith("regex_examples")
        and can_substitute
        and bool(prefix.strip())
    )
    explicit_expected = _explicit_wrapper_expected(
        syntax,
        example.kind,
        raw_comment,
    )
    if (
        explicit_expected is None
        and not has_inferred_regex_wrapper
        and example.kind in {"block", "nested"}
    ):
        explicit_expected = _unclosed_wrapper_expected(syntax, raw_comment)
    if explicit_expected is not None:
        expected_cleaned = explicit_expected
    elif has_inferred_regex_wrapper:
        expected_cleaned = marker
    else:
        expected_cleaned = _normalize_newlines(raw_comment)

    return CleaningFixtureCase(
        case_id=f"{source_group}-{index:03d}-{example.kind}",
        source=_example_source(attribute_name, index),
        kind=example.kind,
        raw_comment=raw_comment,
        expected_cleaned=expected_cleaned,
        payload_marker=marker if can_substitute else None,
    )


def _grouped_line_case(
    syntax: CommentSyntax,
    example: CommentExample,
    attribute_name: str,
    index: int,
) -> Optional[CleaningFixtureCase]:
    if example.kind != "line" or not example.grouped_line_compatible:
        return None

    placeholder_parts = _split_payload_placeholder(example.expected_match)
    if placeholder_parts is None:
        return None
    prefix, suffix = placeholder_parts
    if not prefix.strip():
        return None

    source_group = attribute_name.removesuffix("_examples")
    marker = _payload_marker(f"grouped_{source_group}", index)
    first_marker = f"{marker}_first"
    second_marker = f"{marker}_second"
    raw_comment = f"{prefix}{first_marker}{suffix}\n{prefix}{second_marker}{suffix}"
    expected_lines = []
    for raw_line, marker_text in (
        (f"{prefix}{first_marker}{suffix}", first_marker),
        (f"{prefix}{second_marker}{suffix}", second_marker),
    ):
        explicit_expected = _explicit_wrapper_expected(
            syntax,
            example.kind,
            raw_line,
        )
        expected_lines.append(marker_text if explicit_expected is None else explicit_expected)
    return CleaningFixtureCase(
        case_id=f"grouped-{source_group}-{index:03d}-line",
        source=f"generated-group:{_example_source(attribute_name, index)}",
        kind="grouped_line",
        raw_comment=raw_comment,
        expected_cleaned="\n".join(expected_lines),
        payload_marker=marker,
    )


def _nested_case(
    open_delimiter: str,
    close_delimiter: str,
    index: int,
) -> CleaningFixtureCase:
    marker = _payload_marker("nested_delimiter", index)
    before_marker = f"{marker}_outer_before"
    inner_marker = f"{marker}_inner"
    after_marker = f"{marker}_outer_after"
    raw_comment = (
        f"{open_delimiter} {before_marker} "
        f"{open_delimiter} {inner_marker} {close_delimiter} "
        f"{after_marker} {close_delimiter}"
    )
    expected_cleaned = (
        f"{before_marker} {open_delimiter} {inner_marker} {close_delimiter} {after_marker}"
    )
    return CleaningFixtureCase(
        case_id=f"nested-delimiter-{index:03d}",
        source=f"registry:nested_delimiters[{index}]",
        kind="nested",
        raw_comment=raw_comment,
        expected_cleaned=expected_cleaned,
        payload_marker=marker,
    )


def _explicit_wrapper_case(
    wrapper_kind: str,
    open_delimiter: str,
    close_delimiter: str,
    index: int,
) -> CleaningFixtureCase:
    marker = _payload_marker(f"sanitizer_{wrapper_kind}_wrapper", index)
    if wrapper_kind == "line":
        open_padding = " " if open_delimiter[-1].isalnum() else ""
        close_padding = " " if close_delimiter[:1].isalnum() else ""
    else:
        open_padding = "\n" if open_delimiter[-1].isalnum() else " "
        close_padding = "\n" if close_delimiter[:1].isalnum() else " "

    raw_comment = f"{open_delimiter}{open_padding}{marker}{close_padding}{close_delimiter}"
    return CleaningFixtureCase(
        case_id=f"sanitizer-{wrapper_kind}-wrapper-{index:03d}",
        source=f"registry:sanitizer_{wrapper_kind}_wrappers[{index}]",
        kind=f"sanitizer_{wrapper_kind}_wrapper",
        raw_comment=raw_comment,
        expected_cleaned=marker,
        payload_marker=marker,
    )


def _unclosed_block_case(open_delimiter: str, index: int) -> CleaningFixtureCase:
    marker = _payload_marker("unclosed_block", index)
    raw_comment = f"{open_delimiter}{marker}_first\r\n{marker}_second"
    return CleaningFixtureCase(
        case_id=f"unclosed-block-{index:03d}",
        source=f"registry:unclosed_block_openers[{index}]",
        kind="unclosed_block",
        raw_comment=raw_comment,
        expected_cleaned=f"{marker}_first\n{marker}_second",
        payload_marker=marker,
    )


def _raw_mode_case() -> CleaningFixtureCase:
    marker = _payload_marker("raw_mode", 0)
    return CleaningFixtureCase(
        case_id="raw-mode-newline-normalization",
        source="generated:sanitizer_mode=raw",
        kind="raw",
        raw_comment=f"  {marker}_first\r\n\t{marker}_second\r{marker}_third",
        expected_cleaned=f"  {marker}_first\n\t{marker}_second\n{marker}_third",
        payload_marker=marker,
    )


def _iter_example_groups(syntax: CommentSyntax):
    for attribute_name in (
        "shared_regex_examples",
        "canonical_regex_examples",
        "shared_contextual_examples",
        "canonical_contextual_examples",
    ):
        yield attribute_name, getattr(syntax, attribute_name)


def build_cleaning_cases(syntax: CommentSyntax) -> tuple[CleaningFixtureCase, ...]:
    """Build an explicit oracle without calling ``CommentSanitizer``."""

    cases = []
    for attribute_name, examples in _iter_example_groups(syntax):
        for index, example in enumerate(examples):
            cases.append(_example_case(syntax, example, attribute_name, index))
            if syntax.sanitizer_mode == "wrapped":
                grouped_case = _grouped_line_case(
                    syntax,
                    example,
                    attribute_name,
                    index,
                )
                if grouped_case is not None:
                    cases.append(grouped_case)

    for index, (open_delimiter, close_delimiter) in enumerate(syntax.sanitizer_line_wrappers):
        cases.append(
            _explicit_wrapper_case(
                "line",
                open_delimiter,
                close_delimiter,
                index,
            )
        )

    for index, (open_delimiter, close_delimiter) in enumerate(syntax.sanitizer_block_wrappers):
        cases.append(
            _explicit_wrapper_case(
                "block",
                open_delimiter,
                close_delimiter,
                index,
            )
        )

    for index, (open_delimiter, close_delimiter) in enumerate(syntax.nested_delimiters):
        cases.append(_nested_case(open_delimiter, close_delimiter, index))

    for index, open_delimiter in enumerate(syntax.unclosed_block_openers):
        cases.append(_unclosed_block_case(open_delimiter, index))

    if syntax.sanitizer_mode == "raw":
        cases.append(_raw_mode_case())

    case_ids = [case.case_id for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError(f"Duplicate cleaning case id in {syntax.family_name}")
    if not cases:
        raise ValueError(f"Comment family has no cleaning cases: {syntax.family_name}")
    return tuple(cases)


def build_cleaning_fixtures() -> tuple[CommentCleaningFixture, ...]:
    fixtures = []
    filenames = set()
    for syntax in iter_comment_syntaxes():
        fixture = CommentCleaningFixture(
            family_name=syntax.family_name,
            canonical_language=syntax.canonical_name,
            language_keys=syntax.language_names,
            sanitizer_mode=syntax.sanitizer_mode,
            cases=build_cleaning_cases(syntax),
        )
        if fixture.filename in filenames:
            raise ValueError(f"Duplicate cleaning fixture filename: {fixture.filename}")
        filenames.add(fixture.filename)
        fixtures.append(fixture)
    return tuple(fixtures)


def render_cleaning_fixture(fixture: CommentCleaningFixture) -> str:
    return (
        json.dumps(
            fixture.as_dict(),
            ensure_ascii=True,
            indent=2,
        )
        + "\n"
    )


def write_cleaning_fixtures(
    project_root: Path = Path("."),
    *,
    force: bool = False,
) -> None:
    fixture_dir = project_root / FIXTURE_DIR
    fixture_dir.mkdir(parents=True, exist_ok=True)
    fixtures = build_cleaning_fixtures()

    if force:
        expected_filenames = {fixture.filename for fixture in fixtures}
        for stale_path in fixture_dir.glob(f"*{FIXTURE_SUFFIX}"):
            if stale_path.name not in expected_filenames:
                stale_path.unlink()

    for fixture in fixtures:
        fixture_path = fixture_dir / fixture.filename
        if force or not fixture_path.exists():
            fixture_path.write_text(
                render_cleaning_fixture(fixture),
                encoding="utf-8",
            )


def main() -> None:
    args = parse_args()
    write_cleaning_fixtures(force=args.force)


if __name__ == "__main__":
    main()
