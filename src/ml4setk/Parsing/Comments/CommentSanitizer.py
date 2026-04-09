"""Comment sanitization helpers built on the comment registry."""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass

from ..Query import QueryMatch
from .registry import CommentSyntax, get_comment_syntax

_EXAMPLE_BODY_PLACEHOLDERS = (
    "block note",
    "inline note",
    "note",
    "Visible content",
    "+ 100",
    "Remember the bull.",
)


@dataclass(frozen=True)
class _SanitizerSyntax:
    line_wrappers: tuple[tuple[str, str], ...]
    block_wrappers: tuple[tuple[str, str], ...]


def _split_example_placeholder(example_text: str) -> tuple[str, str, str] | None:
    for placeholder in _EXAMPLE_BODY_PLACEHOLDERS:
        if placeholder not in example_text:
            continue
        prefix, suffix = example_text.split(placeholder, 1)
        return prefix, placeholder, suffix
    return None


def _iter_regex_examples(syntax: CommentSyntax):
    yield from syntax.shared_regex_examples
    yield from syntax.canonical_regex_examples


def _build_sanitizer_syntax(syntax: CommentSyntax) -> _SanitizerSyntax:
    line_wrappers = []
    for example in _iter_regex_examples(syntax):
        if example.kind != "line":
            continue
        parts = _split_example_placeholder(example.expected_match)
        if parts is None:
            continue
        wrapper = (parts[0].strip(), parts[2])
        if wrapper not in line_wrappers:
            line_wrappers.append(wrapper)

    block_wrappers = []
    for open_delim, close_delim in syntax.nested_delimiters:
        wrapper = (open_delim, close_delim)
        if wrapper not in block_wrappers:
            block_wrappers.append(wrapper)

    for example in _iter_regex_examples(syntax):
        if example.kind != "block":
            continue
        parts = _split_example_placeholder(example.expected_match)
        if parts is None:
            continue
        for wrapper in (
            (parts[0], parts[2]),
            (parts[0].rstrip(), parts[2].lstrip()),
        ):
            if wrapper not in block_wrappers:
                block_wrappers.append(wrapper)

    block_wrappers.sort(key=lambda wrapper: len(wrapper[0]) + len(wrapper[1]), reverse=True)
    line_wrappers.sort(key=lambda wrapper: len(wrapper[0]) + len(wrapper[1]), reverse=True)
    return _SanitizerSyntax(tuple(line_wrappers), tuple(block_wrappers))


def _coerce_comment_text(comment: str | QueryMatch) -> str:
    if isinstance(comment, QueryMatch):
        return comment.match
    if isinstance(comment, str):
        return comment
    raise TypeError("comment must be a string or QueryMatch")


def _is_case_insensitive_token(token: str) -> bool:
    return any(char.isalpha() for char in token)


def _strip_grouped_line_wrappers(
    raw_comment: str, line_wrappers: tuple[tuple[str, str], ...]
) -> str | None:
    if not line_wrappers:
        return None

    stripped_lines = []
    matched_wrapper = None
    for line in raw_comment.split("\n"):
        if line == "":
            stripped_lines.append("")
            continue

        wrapper = None
        stripped = None
        for open_token, close_token in line_wrappers:
            flags = re.IGNORECASE if _is_case_insensitive_token(open_token + close_token) else 0
            pattern = re.compile(
                rf"^[ \t]*{re.escape(open_token)}(?=[ \t]|$)(.*){re.escape(close_token)}$",
                flags,
            )
            match = pattern.match(line)
            if match is not None:
                wrapper = (open_token, close_token)
                stripped = match.group(1)
                if stripped.startswith((" ", "\t")):
                    stripped = stripped[1:]
                break

        if wrapper is None or stripped is None:
            return None

        if matched_wrapper is None:
            matched_wrapper = wrapper
        elif wrapper != matched_wrapper:
            return None

        stripped_lines.append(stripped.rstrip())

    return _normalize_sanitized_body("\n".join(stripped_lines))


def _wrapper_matches(raw_comment: str, open_text: str, close_text: str) -> bool:
    if raw_comment.startswith(open_text) and raw_comment.endswith(close_text):
        return True

    if not (_is_case_insensitive_token(open_text) or _is_case_insensitive_token(close_text)):
        return False

    return raw_comment[: len(open_text)].lower() == open_text.lower() and raw_comment[
        len(raw_comment) - len(close_text) :
    ].lower() == close_text.lower()


def _strip_block_wrapper(
    raw_comment: str, block_wrappers: tuple[tuple[str, str], ...]
) -> tuple[str, tuple[str, str]] | None:
    for open_text, close_text in block_wrappers:
        if not _wrapper_matches(raw_comment, open_text, close_text):
            continue

        inner = raw_comment[len(open_text) : len(raw_comment) - len(close_text)]
        return inner, (open_text, close_text)
    return None


def _strip_c_style_gutter_lines(lines: list[str]) -> list[str]:
    non_empty = [line for line in lines if line.strip()]
    if not non_empty:
        return lines

    for leader in ("*", "!"):
        pattern = re.compile(rf"^[ \t]*{re.escape(leader)}(?:[ \t]|$)")
        if not all(pattern.match(line) for line in non_empty):
            continue

        stripped = []
        for line in lines:
            if not line.strip():
                stripped.append("")
                continue
            match = pattern.match(line)
            stripped.append(line[match.end() :] if match is not None else line)
        return stripped

    return lines


def _normalize_sanitized_body(body: str) -> str:
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    body = body.strip("\n")

    if "\n" not in body:
        return body.strip()

    normalized = textwrap.dedent(body)
    normalized_lines = [line.rstrip() for line in normalized.split("\n")]
    return "\n".join(normalized_lines).strip("\n")


def _sanitize_block_body(body: str, wrapper: tuple[str, str]) -> str:
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    if body.startswith("\n"):
        body = body[1:]
    if body.endswith("\n"):
        body = body[:-1]

    lines = body.split("\n")
    if wrapper[0].startswith("/*") and wrapper[1].endswith("*/"):
        lines = _strip_c_style_gutter_lines(lines)

    return _normalize_sanitized_body("\n".join(lines))


class CommentSanitizer:
    """Normalize one extracted comment to its content-bearing text."""

    def __init__(self, language: str):
        self.language = language
        self.syntax = get_comment_syntax(language)
        self._sanitizer_syntax = _build_sanitizer_syntax(self.syntax)

    def sanitize(self, comment: str | QueryMatch) -> str:
        raw_comment = _coerce_comment_text(comment)

        line_result = _strip_grouped_line_wrappers(
            raw_comment, self._sanitizer_syntax.line_wrappers
        )
        if line_result is not None:
            return line_result

        block_result = _strip_block_wrapper(raw_comment, self._sanitizer_syntax.block_wrappers)
        if block_result is not None:
            inner, wrapper = block_result
            return _sanitize_block_body(inner, wrapper)

        return _normalize_sanitized_body(raw_comment)


def sanitize_comment(language: str, comment: str | QueryMatch) -> str:
    """Return sanitized comment text for ``language``."""

    return CommentSanitizer(language).sanitize(comment)


def sanitize_comment_text(language: str, comment: str | QueryMatch) -> str:
    """Backward-compatible alias for ``sanitize_comment``."""

    return sanitize_comment(language, comment)


__all__ = [
    "CommentSanitizer",
    "sanitize_comment",
    "sanitize_comment_text",
]
