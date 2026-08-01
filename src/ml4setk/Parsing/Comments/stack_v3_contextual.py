"""Context-sensitive scanners for reviewed Stack v3 language labels.

The public comment extractors return sorted, non-overlapping half-open ranges.
The literal helpers return protected ranges consumed by ``CommentQuery`` before
its registry regexes are evaluated.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable

_LINE_ENDINGS = "\r\n\u0085\u2028\u2029"
_BH_ASCII_SYMBOLS = frozenset("!@#$%&*+./<=>?\\^|:-~,")
_YAML_BLOCK_HEADER = re.compile(
    r"(?:^|[?:-][ \t]+|:[ \t]*)(?P<style>[|>])(?P<mods>[1-9+-]{0,2})[ \t]*\Z"
)


def _line_end(text: str, start: int) -> int:
    """Return the end of the physical line containing ``start``."""

    index = start
    while index < len(text) and text[index] not in _LINE_ENDINGS:
        index += 1
    return index


def _next_line_start(text: str, line_end: int) -> int:
    """Return the offset after the physical line ending at ``line_end``."""

    if line_end >= len(text):
        return len(text)
    if text.startswith("\r\n", line_end):
        return line_end + 2
    return line_end + 1


def _scan_backslash_quote(text: str, start: int, quote: str) -> int:
    """Return the end of a backslash-escaped quote, protecting malformed EOF."""

    index = start + 1
    while index < len(text):
        char = text[index]
        if char == "\\":
            index = min(index + 2, len(text))
            continue
        if char == quote:
            return index + 1
        if char in _LINE_ENDINGS:
            return len(text)
        index += 1
    return len(text)


def _scan_nested_delimiter(
    text: str,
    start: int,
    open_delimiter: str,
    close_delimiter: str,
    *,
    percent_line_mask: bool = False,
) -> int | None:
    """Return the end of a complete nested delimiter region."""

    depth = 1
    index = start + len(open_delimiter)
    while index < len(text):
        if percent_line_mask and text[index] == "%" and not text.startswith("%*", index):
            index = _line_end(text, index)
            continue
        if text.startswith(open_delimiter, index):
            depth += 1
            index += len(open_delimiter)
            continue
        if text.startswith(close_delimiter, index):
            depth -= 1
            index += len(close_delimiter)
            if depth == 0:
                return index
            continue
        index += 1
    return None


def answer_set_programming_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return clingo-style ASP line comments and nested block comments."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == '"':
            index = _scan_backslash_quote(text, index, '"')
            continue
        if text.startswith("#script", index):
            directive_end = _line_end(text, index)
            body_start = _next_line_start(text, directive_end)
            script_end = text.find("#end", body_start)
            if script_end < 0:
                break
            index = script_end + len("#end")
            continue
        if text.startswith("%*", index):
            end = _scan_nested_delimiter(
                text,
                index,
                "%*",
                "*%",
                percent_line_mask=True,
            )
            if end is None:
                break
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("#!", index) or text[index] == "%":
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def b4x_string_ranges(text: str) -> list[tuple[int, int]]:
    """Return ordinary and smart B4X string ranges."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == "'":
            index = _line_end(text, index)
            continue
        if text.startswith('$"', index):
            start = index
            close = text.find('"$', index + 2)
            end = len(text) if close < 0 else close + 2
            ranges.append((start, end))
            index = end
            continue
        if text[index] != '"':
            index += 1
            continue

        start = index
        index += 1
        while index < len(text):
            if text[index] in _LINE_ENDINGS:
                ranges.append((start, len(text)))
                return ranges
            if text[index] != '"':
                index += 1
                continue
            if index + 1 < len(text) and text[index + 1] == '"':
                index += 2
                continue
            index += 1
            break
        ranges.append((start, index))
    return ranges


def _is_bh_symbol(char: str) -> bool:
    return char in _BH_ASCII_SYMBOLS or unicodedata.category(char).startswith("S")


def _scan_bh_quote(text: str, start: int, quote: str) -> int:
    index = start + 1
    while index < len(text):
        if text[index] == "\\":
            index = min(index + 2, len(text))
            continue
        if text[index] == quote:
            return index + 1
        if text[index] in _LINE_ENDINGS:
            return len(text)
        index += 1
    return len(text)


def bluespec_bh_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return BH comments while respecting operator and pragma tokens."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("{-#", index):
            end = text.find("#-}", index + 3)
            if end < 0:
                break
            index = end + 3
            continue
        if text.startswith("{-", index):
            end = _scan_nested_delimiter(text, index, "{-", "-}")
            if end is None:
                break
            ranges.append((index, end))
            index = end
            continue
        if text[index] in {'"', "'"}:
            index = _scan_bh_quote(text, index, text[index])
            continue
        if text.startswith("--", index):
            dash_end = index + 2
            while dash_end < len(text) and text[dash_end] == "-":
                dash_end += 1
            following = text[dash_end : dash_end + 1]
            line_end = _line_end(text, dash_end)
            has_physical_lf = line_end < len(text) and (
                text[line_end] == "\n" or text.startswith("\r\n", line_end)
            )
            if following == "@" or not following or not _is_bh_symbol(following):
                if has_physical_lf:
                    ranges.append((index, line_end))
                index = line_end
                continue

            index = dash_end
            while index < len(text) and _is_bh_symbol(text[index]):
                index += 1
            continue
        index += 1
    return tuple(ranges)


def bqn_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return BQN hash comments outside strings and character literals."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == '"':
            index += 1
            while index < len(text):
                if text[index] != '"':
                    index += 1
                    continue
                run_end = index + 1
                while run_end < len(text) and text[run_end] == '"':
                    run_end += 1
                if (run_end - index) % 2:
                    index = run_end
                    break
                index = run_end
            else:
                break
            continue
        if text[index] == "'" and index + 2 < len(text) and text[index + 2] == "'":
            index += 3
            continue
        if text[index] == "#":
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _yaml_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _yaml_block_scalar_end(
    text: str,
    header_start: int,
    header_end: int,
    explicit_indent: int | None,
) -> int:
    """Return the first offset following one YAML block scalar body."""

    header_indent = _yaml_indent(text[header_start:header_end])
    required_indent = header_indent + explicit_indent if explicit_indent else None
    line_start = _next_line_start(text, header_end)
    while line_start < len(text):
        line_end = _line_end(text, line_start)
        line = text[line_start:line_end]
        if not line.strip(" "):
            line_start = _next_line_start(text, line_end)
            continue
        indent = _yaml_indent(line)
        if required_indent is None:
            if indent <= header_indent:
                return line_start
            required_indent = indent
        if indent < required_indent:
            return line_start
        line_start = _next_line_start(text, line_end)
    return len(text)


def _yaml_scan_line(
    text: str,
    line_start: int,
    line_end: int,
    quote: str | None,
) -> tuple[int | None, tuple[int, int | None] | None, str | None]:
    """Return a YAML comment start and optional block-scalar header metadata."""

    index = line_start
    comment_start: int | None = None
    while index < line_end:
        char = text[index]
        if quote == "'":
            if char == "'" and index + 1 < line_end and text[index + 1] == "'":
                index += 2
                continue
            if char == "'":
                quote = None
            index += 1
            continue
        if quote == '"':
            if char == "\\":
                index = min(index + 2, line_end)
                continue
            if char == '"':
                quote = None
            index += 1
            continue
        if char in {"'", '"'}:
            quote = char
            index += 1
            continue
        if char == "#" and (index == line_start or text[index - 1] in " \t"):
            comment_start = index
            break
        index += 1

    if quote is not None:
        return comment_start, None, quote

    content_end = comment_start if comment_start is not None else line_end
    uncommented = text[line_start:content_end].rstrip(" \t")
    match = _YAML_BLOCK_HEADER.search(uncommented)
    if match is None:
        return comment_start, None, None
    mods = match.group("mods")
    explicit = next((int(char) for char in mods if char.isdigit()), None)
    return comment_start, (line_start, explicit), None


def yaml_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return structural YAML comments, excluding block scalar content."""

    ranges: list[tuple[int, int]] = []
    line_start = 0
    quote: str | None = None
    while line_start < len(text):
        line_end = _line_end(text, line_start)
        comment_start, scalar, quote = _yaml_scan_line(
            text,
            line_start,
            line_end,
            quote,
        )
        if comment_start is not None:
            ranges.append((comment_start, line_end))
        if scalar is not None:
            _, explicit_indent = scalar
            quote = None
            line_start = _yaml_block_scalar_end(
                text,
                line_start,
                line_end,
                explicit_indent,
            )
            continue
        if line_end == len(text):
            break
        line_start = _next_line_start(text, line_end)
    return tuple(ranges)


def caddyfile_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Caddyfile comments that begin at lexer token boundaries."""

    ranges: list[tuple[int, int]] = []
    index = 1 if text.startswith("\ufeff") else 0
    token_start = True
    while index < len(text):
        char = text[index]
        if char.isspace():
            token_start = True
            index += 1
            continue
        if token_start and char == "#":
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        if token_start and text.startswith("<<", index):
            marker_end = index + 2
            while marker_end < len(text) and not text[marker_end].isspace():
                marker_end += 1
            marker = text[index + 2 : marker_end]
            if not marker:
                break
            header_end = _line_end(text, marker_end)
            body_start = _next_line_start(text, header_end)
            terminator = re.search(
                rf"(?m)^[ \t]*{re.escape(marker)}[ \t]*(?:\r?$)",
                text[body_start:],
            )
            if terminator is None:
                break
            absolute_end = body_start + terminator.end()
            index = absolute_end
            token_start = True
            continue
        if token_start and char in {'"', "`"}:
            quote = char
            index += 1
            while index < len(text):
                if quote == '"' and text[index] == "\\":
                    index = min(index + 2, len(text))
                    continue
                if text[index] == quote:
                    index += 1
                    token_start = False
                    break
                index += 1
            else:
                break
            continue
        if char == "\\" and index + 1 < len(text) and text[index + 1] in "\r\n":
            index = _next_line_start(text, index + 1)
            token_start = False
            continue
        token_start = False
        index += 1
    return tuple(ranges)


def cairo_zero_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Cairo Zero slash comments outside hints and literals."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("%{", index):
            end = text.find("%}", index + 2)
            if end < 0:
                break
            index = end + 2
            continue
        if text[index] in {'"', "'"}:
            quote = text[index]
            end = text.find(quote, index + 1, _line_end(text, index))
            if end < 0:
                break
            index = end + 1
            continue
        if text.startswith("//", index):
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _carbon_literal_at(text: str, start: int) -> tuple[int, str, int] | None:
    """Return ``(quote_start, quote, hash_count)`` for a Carbon literal."""

    index = start
    while index < len(text) and text[index] == "#":
        index += 1
    if index >= len(text) or text[index] not in {'"', "'"}:
        return None
    return index, text[index], index - start


def _carbon_simple_literal_end(
    text: str,
    start: int,
    quote_start: int,
    quote: str,
    hash_count: int,
) -> int:
    closing = quote + ("#" * hash_count)
    index = quote_start + 1
    while index < len(text):
        if text.startswith(closing, index):
            return index + len(closing)
        if not hash_count and text[index] == "\\":
            index = min(index + 2, len(text))
            continue
        if text[index] in _LINE_ENDINGS:
            return len(text)
        index += 1
    return len(text)


def _carbon_line_comment_at(text: str, start: int) -> bool:
    if not text.startswith("//", start) or (start > 0 and text[start - 1] == "/"):
        return False
    following = start + 2
    return following == len(text) or text[following] in " \t\n"


def carbon_string_ranges(text: str) -> list[tuple[int, int]]:
    """Return Carbon simple, raw, and block string/character literal ranges."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if _carbon_line_comment_at(text, index):
            index = _line_end(text, index)
            continue
        literal = _carbon_literal_at(text, index)
        if literal is None:
            index += 1
            continue
        quote_start, quote, hash_count = literal
        triple = quote * 3
        if not text.startswith(triple, quote_start):
            end = _carbon_simple_literal_end(
                text,
                index,
                quote_start,
                quote,
                hash_count,
            )
            ranges.append((index, end))
            index = end
            continue

        header_end = _line_end(text, quote_start + 3)
        header_comment = text.find("//", quote_start + 3, header_end)
        body_start = _next_line_start(text, header_end)
        closing = triple + ("#" * hash_count)
        close = text.find(closing, body_start)
        end = len(text) if close < 0 else close + len(closing)
        if header_comment < 0:
            ranges.append((index, end))
        else:
            ranges.append((index, header_comment))
            if body_start < end:
                ranges.append((body_start - 1, end))
        index = end
    return ranges


STACK_V3_CONTEXTUAL_EXTRACTORS: dict[str, Callable[[str], tuple[tuple[int, int], ...]]] = {
    "answer_set_programming_comments": answer_set_programming_comment_ranges,
    "bluespec_bh_comments": bluespec_bh_comment_ranges,
    "bqn_comments": bqn_comment_ranges,
    "yaml_comments": yaml_comment_ranges,
    "caddyfile_comments": caddyfile_comment_ranges,
    "cairo_zero_comments": cairo_zero_comment_ranges,
}

__all__ = [
    "STACK_V3_CONTEXTUAL_EXTRACTORS",
    "answer_set_programming_comment_ranges",
    "b4x_string_ranges",
    "bluespec_bh_comment_ranges",
    "bqn_comment_ranges",
    "caddyfile_comment_ranges",
    "cairo_zero_comment_ranges",
    "carbon_string_ranges",
    "yaml_comment_ranges",
]
