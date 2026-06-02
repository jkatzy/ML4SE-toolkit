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
_DECORATIVE_RULER_CHARS = frozenset("#-=*_")


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


def _line_open_pattern(open_token: str) -> str:
    """Return a regex fragment for a line-comment opener.

    Args:
        open_token: Registry-derived line-comment opener.

    Returns:
        Regex text that strips the opener. Multi-character homogeneous openers
        such as ``//`` also strip documentation/ruler variants like ``///`` or
        ``////``. Single-character openers stay exact so Markdown headings inside
        ``#`` comments remain content.
    """

    if len(open_token) > 1 and len(set(open_token)) == 1:
        return rf"{re.escape(open_token[0])}{{{len(open_token)},}}"
    return re.escape(open_token)


def _strip_grouped_line_wrappers(
    raw_comment: str, line_wrappers: tuple[tuple[str, str], ...]
) -> str | None:
    if not line_wrappers:
        return None

    stripped_lines = []
    matched_open_tokens = []
    for line in raw_comment.split("\n"):
        if line == "":
            stripped_lines.append("")
            continue

        wrapper = None
        stripped = None
        for open_token, close_token in line_wrappers:
            flags = re.IGNORECASE if _is_case_insensitive_token(open_token + close_token) else 0
            pattern = re.compile(
                rf"^[ \t]*(?:{_line_open_pattern(open_token)})(.*){re.escape(close_token)}$",
                flags,
            )
            match = pattern.match(line)
            if match is not None:
                wrapper = (open_token, close_token)
                matched_open_tokens.append(open_token)
                stripped = match.group(1)
                if stripped.startswith((" ", "\t")):
                    stripped = stripped[1:]
                break

        if wrapper is None or stripped is None:
            return None

        stripped_lines.append(stripped.rstrip())

    stripped_lines = _strip_residual_single_char_gutter(
        stripped_lines, tuple(matched_open_tokens)
    )
    stripped_lines = _strip_decorative_edge_rulers(stripped_lines)
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


def _is_decorative_ruler_line(line: str) -> bool:
    stripped = line.strip()
    return (
        len(stripped) >= 3
        and len(set(stripped)) == 1
        and stripped[0] in _DECORATIVE_RULER_CHARS
    )


def _has_framed_content_line(lines: list[str], frame_char: str) -> bool:
    """Return whether a ruler character frames content in the remaining body.

    Args:
        lines: Sanitized body lines after delimiter removal.
        frame_char: Candidate decorative ruler character.

    Returns:
        True when a non-ruler line starts and ends with the same character,
        indicating an ASCII title card whose frame should be preserved.
    """

    for line in lines:
        stripped = line.strip()
        if not stripped or _is_decorative_ruler_line(stripped):
            continue
        if (
            stripped.startswith(frame_char)
            and stripped.endswith(frame_char)
            and any(char != frame_char for char in stripped)
        ):
            return True
    return False


def _strip_decorative_edge_rulers(lines: list[str]) -> list[str]:
    """Remove delimiter-created ruler-only edge lines while preserving banners.

    Args:
        lines: Comment body lines after language delimiter stripping.

    Returns:
        Lines with leading and trailing ruler-only scaffolding removed unless
        the same ruler character frames an interior title-card line.
    """

    non_empty = [line for line in lines if line.strip()]
    if non_empty and all(_is_decorative_ruler_line(line) for line in non_empty):
        return lines

    stripped = list(lines)
    while stripped:
        first = stripped[0]
        first_text = first.strip()
        if not _is_decorative_ruler_line(first):
            break
        if _has_framed_content_line(stripped[1:], first_text[0]):
            break
        stripped.pop(0)

    while stripped:
        last = stripped[-1]
        last_text = last.strip()
        if not _is_decorative_ruler_line(last):
            break
        if _has_framed_content_line(stripped[:-1], last_text[0]):
            break
        stripped.pop()

    return stripped


def _strip_space_padding_before_tabs(lines: list[str]) -> list[str]:
    """Strip space padding from aligned text when tab-indented lines coexist.

    Args:
        lines: Comment body lines before final normalization.

    Returns:
        Lines with common leading spaces removed from space-indented lines when
        every non-empty line is indented by spaces or tabs.
    """

    non_empty = [line for line in lines if line.strip()]
    if not non_empty or not all(line.startswith((" ", "\t")) for line in non_empty):
        return lines

    space_indented = [line for line in non_empty if line.startswith(" ")]
    if not space_indented or not any(line.startswith("\t") for line in non_empty):
        return lines

    common_spaces = min(len(line) - len(line.lstrip(" ")) for line in space_indented)
    if common_spaces == 0:
        return lines

    stripped = []
    for line in lines:
        if line.startswith(" "):
            stripped.append(line[common_spaces:])
        else:
            stripped.append(line)
    return stripped


def _strip_residual_single_char_gutter(
    lines: list[str], matched_open_tokens: tuple[str, ...]
) -> list[str]:
    """Strip a second repeated single-character gutter from line comments.

    Args:
        lines: Lines after one registered line-comment opener has been removed.
        matched_open_tokens: Openers matched while removing each non-empty line.

    Returns:
        Lines with one residual gutter character removed when every non-empty
        line still starts with that same character and the result is not a
        framed ASCII title card.
    """

    unique_tokens = set(matched_open_tokens)
    if len(unique_tokens) != 1:
        return lines

    (token,) = unique_tokens
    if len(token) != 1:
        return lines

    non_empty = [line for line in lines if line.strip()]
    if not non_empty or not all(line.lstrip().startswith(token) for line in non_empty):
        return lines
    if _has_framed_content_line(lines, token):
        return lines

    stripped_lines = []
    for line in lines:
        prefix_len = len(line) - len(line.lstrip())
        stripped = line[prefix_len:]
        if stripped.startswith(token):
            stripped = stripped[1:]
        stripped_lines.append(line[:prefix_len] + stripped)
    return stripped_lines


def _normalize_sanitized_body(body: str) -> str:
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    body = body.strip("\n")

    if "\n" not in body:
        return body.strip()

    normalized = textwrap.dedent("\n".join(_strip_space_padding_before_tabs(body.split("\n"))))
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
    lines = _strip_decorative_edge_rulers(lines)

    return _normalize_sanitized_body("\n".join(lines))


class CommentSanitizer:
    """Normalize one extracted comment to its content-bearing text."""

    def __init__(self, language: str):
        self.language = language
        self.syntax = get_comment_syntax(language)
        self._sanitizer_syntax = _build_sanitizer_syntax(self.syntax)

    def sanitize(self, comment: str | QueryMatch) -> str:
        raw_comment = _coerce_comment_text(comment)

        block_result = _strip_block_wrapper(raw_comment, self._sanitizer_syntax.block_wrappers)
        if block_result is not None:
            inner, wrapper = block_result
            return _sanitize_block_body(inner, wrapper)

        line_result = _strip_grouped_line_wrappers(
            raw_comment, self._sanitizer_syntax.line_wrappers
        )
        if line_result is not None:
            return line_result

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
