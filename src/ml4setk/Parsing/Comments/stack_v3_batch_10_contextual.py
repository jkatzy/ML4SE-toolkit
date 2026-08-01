"""Contextual comment extractors for Stack v3 full research batch 10."""

from __future__ import annotations

from collections.abc import Callable

_TYPESPEC_LINE_BREAKS = "\r\n\u2028\u2029"
_TYPST_LINE_BREAKS = "\n\v\f\r\u0085\u2028\u2029"


def _line_end(text: str, start: int, endings: str) -> int:
    index = start
    while index < len(text) and text[index] not in endings:
        index += 1
    return index


def _skip_quoted(
    text: str,
    start: int,
    quote: str,
    *,
    line_breaks: str = "",
) -> int | None:
    index = start + len(quote)
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text.startswith(quote, index):
            return index + len(quote)
        if line_breaks and text[index] in line_breaks:
            return None
        index += 1
    return None


def textgrid_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return explicit Praat TextGrid exclamation comments outside values."""

    ranges: list[tuple[int, int]] = []
    index = 0
    in_string = False
    while index < len(text):
        char = text[index]
        if in_string:
            if char != '"':
                index += 1
                continue
            if text[index + 1 : index + 2] == '"':
                index += 2
                continue
            in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            index += 1
            continue
        if char == "!":
            end = _line_end(text, index, "\r\n")
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _toit_block_end(text: str, start: int) -> int | None:
    depth = 1
    index = start + 2
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text.startswith("/*", index):
            depth += 1
            index += 2
            continue
        if text.startswith("*/", index):
            depth -= 1
            index += 2
            if depth == 0:
                return index
            continue
        index += 1
    return None


def _scan_toit_string(
    text: str,
    start: int,
    ranges: list[tuple[int, int]],
) -> int:
    index = start + 1
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == '"':
            return index + 1
        if text.startswith("$(", index):
            interpolation_end = _scan_toit_code(
                text,
                index + 2,
                ranges,
                interpolation=True,
            )
            if interpolation_end is None:
                return len(text)
            index = interpolation_end
            continue
        index += 1
    return len(text)


def _scan_toit_code(
    text: str,
    start: int,
    ranges: list[tuple[int, int]],
    *,
    interpolation: bool,
) -> int | None:
    index = start
    paren_depth = 1 if interpolation else 0
    while index < len(text):
        if text.startswith("//", index):
            end = _line_end(text, index, "\r\n")
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            end = _toit_block_end(text, index)
            if end is None:
                return None if interpolation else len(text)
            ranges.append((index, end))
            index = end
            continue
        char = text[index]
        if char == '"':
            index = _scan_toit_string(text, index, ranges)
            continue
        if char == "'":
            end = _skip_quoted(text, index, "'", line_breaks="\r\n")
            index = _line_end(text, index, "\r\n") if end is None else end
            continue
        if interpolation and char == "(":
            paren_depth += 1
        elif interpolation and char == ")":
            paren_depth -= 1
            if paren_depth == 0:
                return index + 1
        index += 1
    return None if interpolation else len(text)


def toit_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Toit line and escape-aware nested block comments."""

    ranges: list[tuple[int, int]] = []
    _scan_toit_code(text, 0, ranges, interpolation=False)
    return tuple(ranges)


def tor_config_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return torrc hash comments outside quoted and escaped value text."""

    ranges: list[tuple[int, int]] = []
    index = 0
    in_quote = False
    while index < len(text):
        char = text[index]
        if char == "\\":
            if text[index + 1 : index + 3] == "\r\n":
                index += 3
            else:
                index += 2
            continue
        if char == '"':
            in_quote = not in_quote
            index += 1
            continue
        if char == "#" and not in_quote:
            lf = text.find("\n", index)
            if lf < 0:
                ranges.append((index, len(text)))
                break
            end = lf - 1 if lf > index and text[lf - 1] == "\r" else lf
            ranges.append((index, end))
            index = lf + 1
            continue
        index += 1
    return tuple(ranges)


def tree_sitter_query_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Tree-sitter query semicolon comments outside string literals."""

    ranges: list[tuple[int, int]] = []
    index = 0
    in_string = False
    while index < len(text):
        char = text[index]
        if in_string:
            if char == "\\":
                index += 2
                continue
            if char == '"':
                in_string = False
            elif char == "\n":
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            index += 1
            continue
        if char == ";":
            lf = text.find("\n", index)
            end = len(text) if lf < 0 else lf
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _typespec_block_end(text: str, start: int) -> int | None:
    close = text.find("*/", start + 2)
    return None if close < 0 else close + 2


def _scan_typespec_string(
    text: str,
    start: int,
    ranges: list[tuple[int, int]],
) -> int:
    delimiter = '"""' if text.startswith('"""', start) else '"'
    index = start + len(delimiter)
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text.startswith(delimiter, index):
            return index + len(delimiter)
        if text.startswith("${", index):
            interpolation_end = _scan_typespec_code(
                text,
                index + 2,
                ranges,
                interpolation=True,
            )
            if interpolation_end is None:
                return len(text)
            index = interpolation_end
            continue
        if delimiter == '"' and text[index] in _TYPESPEC_LINE_BREAKS:
            return index
        index += 1
    return len(text)


def _scan_typespec_code(
    text: str,
    start: int,
    ranges: list[tuple[int, int]],
    *,
    interpolation: bool,
) -> int | None:
    index = start
    brace_depth = 1 if interpolation else 0
    while index < len(text):
        if text.startswith("//", index):
            end = _line_end(text, index, _TYPESPEC_LINE_BREAKS)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            end = _typespec_block_end(text, index)
            if end is None:
                return None if interpolation else len(text)
            ranges.append((index, end))
            index = end
            continue
        char = text[index]
        if char == '"':
            index = _scan_typespec_string(text, index, ranges)
            continue
        if interpolation and char == "{":
            brace_depth += 1
        elif interpolation and char == "}":
            brace_depth -= 1
            if brace_depth == 0:
                return index + 1
        index += 1
    return None if interpolation else len(text)


def typespec_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return TypeSpec comments while shielding only template literal spans."""

    ranges: list[tuple[int, int]] = []
    _scan_typespec_code(text, 0, ranges, interpolation=False)
    return tuple(ranges)


def _typst_block_end(text: str, start: int) -> int:
    depth = 1
    index = start + 2
    while index < len(text):
        if text.startswith("/*", index):
            depth += 1
            index += 2
            continue
        if text.startswith("*/", index):
            depth -= 1
            index += 2
            if depth == 0:
                return index
            continue
        index += 1
    return len(text)


def _typst_raw_end(text: str, start: int) -> int:
    width = 1
    while text[start + width : start + width + 1] == "`":
        width += 1
    if width == 2:
        return start + width
    marker = "`" * width
    close = text.find(marker, start + width)
    return len(text) if close < 0 else close + width


def _typst_url_end(text: str, start: int) -> int:
    index = start
    while index < len(text) and not text[index].isspace() and text[index] not in '<>"':
        index += 1
    return index


def typst_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Typst comments outside raw, string, URL, escape, and shebang spans."""

    ranges: list[tuple[int, int]] = []
    index = 0
    if text.startswith("#!"):
        index = _line_end(text, 0, _TYPST_LINE_BREAKS)

    while index < len(text):
        if text.startswith(("https://", "http://"), index):
            index = _typst_url_end(text, index)
            continue
        char = text[index]
        if char == "`":
            index = _typst_raw_end(text, index)
            continue
        if char == '"':
            end = _skip_quoted(text, index, '"')
            index = len(text) if end is None else end
            continue
        if char == "\\":
            index += 2
            continue
        if text.startswith("//", index):
            end = _line_end(text, index, _TYPST_LINE_BREAKS)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            end = _typst_block_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


STACK_V3_BATCH_10_CONTEXTUAL_EXTRACTORS: dict[str, Callable[[str], tuple[tuple[int, int], ...]]] = {
    "textgrid_comments": textgrid_comment_ranges,
    "toit_comments": toit_comment_ranges,
    "tor_config_comments": tor_config_comment_ranges,
    "tree_sitter_query_comments": tree_sitter_query_comment_ranges,
    "typespec_comments": typespec_comment_ranges,
    "typst_comments": typst_comment_ranges,
}


__all__ = [
    "STACK_V3_BATCH_10_CONTEXTUAL_EXTRACTORS",
    "textgrid_comment_ranges",
    "toit_comment_ranges",
    "tor_config_comment_ranges",
    "tree_sitter_query_comment_ranges",
    "typespec_comment_ranges",
    "typst_comment_ranges",
]
