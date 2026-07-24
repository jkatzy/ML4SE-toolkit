"""Context-dependent comment range extractors.

These extractors cover formats whose comments are identified by file structure
rather than by a lexical delimiter.
"""

from __future__ import annotations

import re
from collections.abc import Callable

_SIGNED_DECIMAL = re.compile(r"[+-]?[0-9]{1,9}\Z")
_FIGLET_HEADER_WHITESPACE = " \t\v\f"


def _physical_line_bounds(
    text: str, start: int, *, allow_eof: bool = False
) -> tuple[int, int] | None:
    """Return one physical line's content end and next-line start."""

    for index in range(start, len(text)):
        char = text[index]
        if char == "\n":
            return index, index + 1
        if char == "\r":
            if index + 1 < len(text) and text[index + 1] == "\n":
                return index, index + 2
            return index, index + 1
    if allow_eof and start < len(text):
        return len(text), len(text)
    return None


def _figlet_comment_line_count(header: str) -> int | None:
    """Return the FIGfont header's declared comment-line count."""

    if not header.startswith("flf2a") or len(header) < 7:
        return None

    hardblank = header[5]
    if hardblank in {" ", "\0", "\r", "\n"}:
        return None
    try:
        if len(hardblank.encode("utf-8")) != 1:
            return None
    except UnicodeEncodeError:
        return None

    remainder = header[6:]
    if not remainder or remainder[0] not in _FIGLET_HEADER_WHITESPACE:
        return None

    fields = re.split(
        rf"[{re.escape(_FIGLET_HEADER_WHITESPACE)}]+",
        remainder.strip(_FIGLET_HEADER_WHITESPACE),
    )
    if len(fields) < 5:
        return None
    if any(_SIGNED_DECIMAL.fullmatch(field) is None for field in fields[:5]):
        return None

    comment_lines = int(fields[4])
    return comment_lines if comment_lines >= 0 else None


def figlet_header_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return the header-declared FIGfont comment region, if complete."""

    header_bounds = _physical_line_bounds(text, 0)
    if header_bounds is None:
        return ()

    header_end, comment_start = header_bounds
    comment_lines = _figlet_comment_line_count(text[:header_end])
    if not comment_lines:
        return ()

    line_start = comment_start
    for line_index in range(comment_lines):
        line_bounds = _physical_line_bounds(text, line_start, allow_eof=True)
        if line_bounds is None:
            return ()

        line_end, next_line_start = line_bounds
        if line_index == comment_lines - 1:
            return ((comment_start, line_end),)
        line_start = next_line_start

    return ()


_CONTEXTUAL_EXTRACTORS: dict[str, Callable[[str], tuple[tuple[int, int], ...]]] = {
    "figlet_header_comments": figlet_header_comment_ranges,
}
SUPPORTED_CONTEXTUAL_EXTRACTORS = frozenset(_CONTEXTUAL_EXTRACTORS)


def contextual_comment_ranges(extractor_name: str, text: str) -> tuple[tuple[int, int], ...]:
    """Dispatch a named contextual extractor."""

    try:
        extractor = _CONTEXTUAL_EXTRACTORS[extractor_name]
    except KeyError as exc:
        raise ValueError(f"Unknown contextual comment extractor: {extractor_name}") from exc
    return extractor(text)


__all__ = [
    "SUPPORTED_CONTEXTUAL_EXTRACTORS",
    "contextual_comment_ranges",
    "figlet_header_comment_ranges",
]
