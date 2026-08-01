"""Lexical helpers for reviewed Stack v3 batch 11 languages."""

from __future__ import annotations

from collections.abc import Sequence


def _long_bracket_opener_end(text: str, start: int) -> int | None:
    if start >= len(text) or text[start] != "[":
        return None

    index = start + 1
    while index < len(text) and text[index] == "=":
        index += 1
    return index + 1 if index < len(text) and text[index] == "[" else None


def _long_bracket_end(text: str, start: int, opener_end: int) -> int:
    equals = text[start + 1 : opener_end - 1]
    close = "]" + equals + "]"
    close_start = text.find(close, opener_end)
    return len(text) if close_start < 0 else close_start + len(close)


def lua_long_bracket_string_ranges(
    text: str,
    quoted_ranges: Sequence[tuple[int, int]] = (),
) -> list[tuple[int, int]]:
    """Return Lua long-bracket strings outside quotes and comments."""

    ranges: list[tuple[int, int]] = []
    index = 0
    quoted_index = 0
    while index < len(text):
        while quoted_index < len(quoted_ranges) and quoted_ranges[quoted_index][1] <= index:
            quoted_index += 1
        if quoted_index < len(quoted_ranges):
            quoted_start, quoted_end = quoted_ranges[quoted_index]
            if quoted_start <= index < quoted_end:
                index = quoted_end
                continue

        if text.startswith("--", index):
            opener_start = index + 2
            opener_end = _long_bracket_opener_end(text, opener_start)
            if opener_end is not None:
                index = _long_bracket_end(text, opener_start, opener_end)
                continue
            line_feed = text.find("\n", index + 2)
            carriage_return = text.find("\r", index + 2)
            line_ends = (end for end in (line_feed, carriage_return) if end >= 0)
            index = min(line_ends, default=len(text))
            continue

        opener_end = _long_bracket_opener_end(text, index)
        if opener_end is None:
            index += 1
            continue

        end = _long_bracket_end(text, index, opener_end)
        ranges.append((index, end))
        index = end

    return ranges


__all__ = ["lua_long_bracket_string_ranges"]
