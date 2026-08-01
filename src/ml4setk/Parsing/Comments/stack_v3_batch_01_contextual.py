"""Context-sensitive comment scanners for reviewed Stack v3 batch 01."""

from __future__ import annotations

from collections.abc import Callable

_LINE_ENDINGS = "\r\n"


def _line_end(text: str, start: int) -> int:
    index = start
    while index < len(text) and text[index] not in _LINE_ENDINGS:
        index += 1
    return index


def _next_line_start(text: str, line_end: int) -> int:
    if line_end >= len(text):
        return len(text)
    if text.startswith("\r\n", line_end):
        return line_end + 2
    return line_end + 1


def _escaped_quote_end(text: str, start: int, quote: str) -> int | None:
    """Return the end of a matching quote with escaped quote characters."""

    index = start + 1
    while index < len(text):
        if text[index] == "\\" and index + 1 < len(text) and text[index + 1] == quote:
            index += 2
            continue
        if text[index] == quote:
            return index + 1
        index += 1
    return None


def clue_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Clue comments outside its three quoted string forms."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char in {"'", '"', "`"}:
            end = _escaped_quote_end(text, index, char)
            if end is None:
                break
            index = end
            continue
        if text.startswith("//", index):
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            end = len(text) if close < 0 else close + 2
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _cylc_jinja_directive(text: str, marker: int) -> bool:
    line_start = max(text.rfind("\n", 0, marker), text.rfind("\r", 0, marker)) + 1
    if text[line_start:marker].strip(" \t"):
        return False
    directive = "#!jinja2"
    if not text.startswith(directive, marker):
        return False
    following = text[marker + len(directive) : marker + len(directive) + 1]
    return not following or following in " \t\r\n"


def cylc_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return native Cylc hash comments outside quoted and Jinja regions."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("{#", index):
            close = text.find("#}", index + 2)
            if close < 0:
                break
            index = close + 2
            continue
        triple = text[index : index + 3]
        if triple in {"'''", '"""'}:
            close = text.find(triple, index + 3)
            if close < 0:
                break
            index = close + 3
            continue
        char = text[index]
        if char in {"'", '"'}:
            end = _escaped_quote_end(text, index, char)
            if end is None:
                break
            index = end
            continue
        if char == "#":
            end = _line_end(text, index)
            if not _cylc_jinja_directive(text, index):
                ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _d2_quoted_end(text: str, start: int, quote: str) -> int | None:
    index = start + 1
    while index < len(text):
        if quote == "'" and text.startswith("''", index):
            index += 2
            continue
        if text[index] == "\\":
            index = min(index + 2, len(text))
            continue
        if text[index] == quote:
            return index + 1
        if quote == "'" and text[index] in _LINE_ENDINGS:
            return None
        index += 1
    return None


def _d2_block_string_end(text: str, start: int) -> int | None:
    """Return the end of a D2 ``|...|`` block string."""

    index = start + 1
    quote_start = index
    while index < len(text):
        char = text[index]
        if char.isspace() or char.isalnum() or char == "_":
            break
        index += 1
    quote = text[quote_start:index]

    while index < len(text) and not text[index].isspace():
        index += 1
    while index < len(text) and text[index] not in _LINE_ENDINGS:
        if not text[index].isspace():
            break
        index += 1
    if index < len(text) and text[index] in _LINE_ENDINGS:
        index = _next_line_start(text, index)

    closing = quote + "|"
    close = text.find(closing, index)
    return None if close < 0 else close + len(closing)


def d2_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return D2 hash comments and structural triple-quote block comments."""

    ranges: list[tuple[int, int]] = []
    index = 0
    at_map_node = True
    while index < len(text):
        char = text[index]
        if char.isspace():
            if char in _LINE_ENDINGS:
                at_map_node = True
            index += 1
            continue
        if char == "#":
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith('"""', index) and at_map_node:
            close = text.find('"""', index + 3)
            if close < 0:
                break
            end = close + 3
            ranges.append((index, end))
            index = end
            at_map_node = True
            continue
        if char in {"'", '"'}:
            end = _d2_quoted_end(text, index, char)
            if end is None:
                break
            index = end
            at_map_node = False
            continue
        if char == "|":
            end = _d2_block_string_end(text, index)
            if end is None:
                break
            index = end
            at_map_node = False
            continue
        if char in "{;":
            at_map_node = True
            index += 1
            continue
        at_map_node = False
        index += 1
    return tuple(ranges)


def _dotenv_key_char(char: str) -> bool:
    return char.isascii() and (char.isalnum() or char in "-._")


def _dotenv_quote_end(text: str, start: int, quote: str) -> int | None:
    index = start + 1
    while index < len(text):
        if text[index] == "\\" and index + 1 < len(text) and text[index + 1] == quote:
            index += 2
            continue
        if text[index] == quote:
            return index + 1
        index += 1
    return None


def dotenv_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Node dotenv >=15 comment ranges from valid assignment lines."""

    ranges: list[tuple[int, int]] = []
    line_start = 1 if text.startswith("\ufeff") else 0
    while line_start < len(text):
        line_end = _line_end(text, line_start)
        index = line_start
        while index < line_end and text[index] in " \t":
            index += 1

        if index == line_end:
            line_start = _next_line_start(text, line_end)
            continue
        if text[index] == "#":
            ranges.append((index, line_end))
            line_start = _next_line_start(text, line_end)
            continue

        if text.startswith("export", index) and text[index + 6 : index + 7] in {
            " ",
            "\t",
        }:
            index += 6
            while index < line_end and text[index] in " \t":
                index += 1

        key_start = index
        while index < line_end and _dotenv_key_char(text[index]):
            index += 1
        if index == key_start:
            line_start = _next_line_start(text, line_end)
            continue
        while index < line_end and text[index] in " \t":
            index += 1

        if index < line_end and text[index] == "=":
            index += 1
        elif index + 1 < line_end and text[index] == ":" and text[index + 1] in " \t":
            index += 1
        else:
            line_start = _next_line_start(text, line_end)
            continue
        while index < line_end and text[index] in " \t":
            index += 1

        if index < line_end and text[index] in {"'", '"', "`"}:
            quote = text[index]
            close = _dotenv_quote_end(text, index, quote)
            if close is None:
                hash_start = text.find("#", index, line_end)
                if hash_start >= 0:
                    ranges.append((hash_start, line_end))
                line_start = _next_line_start(text, line_end)
                continue

            close_line_end = _line_end(text, close)
            index = close
            while index < close_line_end and text[index] in " \t":
                index += 1
            if index < close_line_end and text[index] == "#":
                ranges.append((index, close_line_end))
            line_start = _next_line_start(text, close_line_end)
            continue

        hash_start = text.find("#", index, line_end)
        if hash_start >= 0:
            ranges.append((hash_start, line_end))
        line_start = _next_line_start(text, line_end)
    return tuple(ranges)


STACK_V3_BATCH_01_CONTEXTUAL_EXTRACTORS: dict[str, Callable[[str], tuple[tuple[int, int], ...]]] = {
    "clue_comments": clue_comment_ranges,
    "cylc_comments": cylc_comment_ranges,
    "d2_comments": d2_comment_ranges,
    "dotenv_comments": dotenv_comment_ranges,
}

__all__ = [
    "STACK_V3_BATCH_01_CONTEXTUAL_EXTRACTORS",
    "clue_comment_ranges",
    "cylc_comment_ranges",
    "d2_comment_ranges",
    "dotenv_comment_ranges",
]
