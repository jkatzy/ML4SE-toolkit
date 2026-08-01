"""Contextual comment helpers for Stack v3 full research batch 05."""

from __future__ import annotations

import re
from collections.abc import Callable

_ECMASCRIPT_LINE_ENDINGS = "\r\n\u2028\u2029"
_RAW_MDSVEX_TAG = re.compile(r"<(script|style|pre)\b", re.IGNORECASE)
_ESM_START = re.compile(r"(?:import|export)(?:\s|\{|\*)")


def _line_bounds(text: str, start: int) -> tuple[int, int]:
    """Return a physical line's content end and next-line start."""

    index = start
    while index < len(text) and text[index] not in "\r\n":
        index += 1
    if text[index : index + 2] == "\r\n":
        return index, index + 2
    if index < len(text):
        return index, index + 1
    return index, index


def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def _containing_range(index: int, ranges: list[tuple[int, int]]) -> tuple[int, int] | None:
    for start, end in ranges:
        if start <= index < end:
            return start, end
        if start > index:
            break
    return None


def _front_matter_range(text: str) -> tuple[int, int] | None:
    start = 1 if text.startswith("\ufeff") else 0
    first_end, line_start = _line_bounds(text, start)
    if text[start:first_end].strip(" \t") != "---":
        return None

    while line_start < len(text):
        line_end, next_line = _line_bounds(text, line_start)
        if text[line_start:line_end].strip(" \t") in {"---", "..."}:
            return 0, next_line
        if next_line == line_start:
            break
        line_start = next_line
    return 0, len(text)


def _fence_marker(line: str) -> tuple[str, int] | None:
    indent = len(line) - len(line.lstrip(" "))
    if indent > 3 or indent == len(line):
        return None
    marker = line[indent]
    if marker not in {"`", "~"}:
        return None
    width = 1
    while indent + width < len(line) and line[indent + width] == marker:
        width += 1
    return (marker, width) if width >= 3 else None


def _is_fence_close(line: str, marker: str, minimum_width: int) -> bool:
    indent = len(line) - len(line.lstrip(" "))
    if indent > 3 or indent == len(line) or line[indent] != marker:
        return False
    width = 1
    while indent + width < len(line) and line[indent + width] == marker:
        width += 1
    return width >= minimum_width and not line[indent + width :].strip(" \t")


def _fenced_code_ranges(text: str, protected: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    line_start = 0
    while line_start < len(text):
        line_end, next_line = _line_bounds(text, line_start)
        containing = _containing_range(line_start, protected)
        if containing is not None:
            line_start = max(next_line, containing[1])
            continue

        marker = _fence_marker(text[line_start:line_end])
        if marker is None:
            if next_line == line_start:
                break
            line_start = next_line
            continue

        fence_char, width = marker
        fence_start = line_start
        line_start = next_line
        while line_start < len(text):
            line_end, next_line = _line_bounds(text, line_start)
            if _is_fence_close(text[line_start:line_end], fence_char, width):
                ranges.append((fence_start, next_line))
                line_start = next_line
                break
            if next_line == line_start:
                break
            line_start = next_line
        else:
            ranges.append((fence_start, len(text)))
        if line_start >= len(text) and (not ranges or ranges[-1][0] != fence_start):
            ranges.append((fence_start, len(text)))
    return ranges


def _indented_code_ranges(text: str, protected: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    line_start = 0
    while line_start < len(text):
        line_end, next_line = _line_bounds(text, line_start)
        if _containing_range(line_start, protected) is None and text.startswith(
            ("    ", "\t"), line_start
        ):
            ranges.append((line_start, line_end))
        if next_line == line_start:
            break
        line_start = next_line
    return ranges


def _inline_code_ranges(text: str, protected: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        containing = _containing_range(index, protected)
        if containing is not None:
            index = containing[1]
            continue
        if text[index] != "`":
            index += 1
            continue

        width = 1
        while index + width < len(text) and text[index + width] == "`":
            width += 1
        marker = "`" * width
        search_from = index + width
        while True:
            close = text.find(marker, search_from)
            if close < 0:
                index += width
                break
            if (close == 0 or text[close - 1] != "`") and (
                close + width == len(text) or text[close + width] != "`"
            ):
                ranges.append((index, close + width))
                index = close + width
                break
            search_from = close + 1
    return ranges


def _html_tag_end(text: str, start: int) -> int | None:
    quote: str | None = None
    escaped = False
    index = start + 1
    while index < len(text):
        char = text[index]
        if quote is not None:
            if char == "\\" and not escaped:
                escaped = True
                index += 1
                continue
            if char == quote and not escaped:
                quote = None
            escaped = False
            index += 1
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == ">":
            return index + 1
        index += 1
    return None


def _raw_mdsvex_ranges(text: str, protected: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    search_from = 0
    while True:
        match = _RAW_MDSVEX_TAG.search(text, search_from)
        if match is None:
            break
        containing = _containing_range(match.start(), protected)
        if containing is not None:
            search_from = containing[1]
            continue
        tag_end = _html_tag_end(text, match.start())
        if tag_end is None:
            ranges.append((match.start(), len(text)))
            break
        close_match = re.search(
            rf"</{re.escape(match.group(1))}\s*>",
            text[tag_end:],
            re.IGNORECASE,
        )
        end = len(text) if close_match is None else tag_end + close_match.end()
        ranges.append((match.start(), end))
        search_from = end
    return ranges


def _markup_tag_ranges(text: str, protected: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        containing = _containing_range(index, protected)
        if containing is not None:
            index = containing[1]
            continue
        if text[index] != "<" or text.startswith("<!--", index):
            index += 1
            continue
        next_char = text[index + 1 : index + 2]
        if not next_char or not (next_char.isalpha() or next_char in {"/", ">"}):
            index += 1
            continue
        end = _html_tag_end(text, index)
        if end is None:
            ranges.append((index, len(text)))
            break
        ranges.append((index, end))
        index = end
    return ranges


def _balanced_brace_end(text: str, start: int) -> int:
    depth = 1
    index = start + 1
    quote: str | None = None
    escaped = False
    while index < len(text):
        char = text[index]
        if quote is not None:
            if char == "\\" and not escaped:
                escaped = True
                index += 1
                continue
            if char == quote and not escaped:
                quote = None
            escaped = False
            index += 1
            continue
        if char in {'"', "'", "`"}:
            quote = char
            index += 1
            continue
        if text.startswith("//", index):
            while index < len(text) and text[index] not in _ECMASCRIPT_LINE_ENDINGS:
                index += 1
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            if close < 0:
                return len(text)
            index = close + 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index + 1
        index += 1
    return len(text)


def _svelte_expression_ranges(text: str, protected: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        containing = _containing_range(index, protected)
        if containing is not None:
            index = containing[1]
            continue
        if text[index] != "{":
            index += 1
            continue
        end = _balanced_brace_end(text, index)
        ranges.append((index, end))
        index = end
    return ranges


def _markdown_code_ranges(text: str, *, front_matter: bool) -> list[tuple[int, int]]:
    protected: list[tuple[int, int]] = []
    if front_matter and (front_matter_range := _front_matter_range(text)) is not None:
        protected.append(front_matter_range)
    protected.extend(_fenced_code_ranges(text, protected))
    protected = _merge_ranges(protected)
    protected.extend(_indented_code_ranges(text, protected))
    protected = _merge_ranges(protected)
    protected.extend(_inline_code_ranges(text, protected))
    return _merge_ranges(protected)


def mdsvex_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return ordinary host HTML comments from default MDsveX source."""

    protected = _markdown_code_ranges(text, front_matter=True)
    protected.extend(_raw_mdsvex_ranges(text, protected))
    protected = _merge_ranges(protected)
    protected.extend(_markup_tag_ranges(text, protected))
    protected = _merge_ranges(protected)
    protected.extend(_svelte_expression_ranges(text, protected))
    protected = _merge_ranges(protected)

    ranges: list[tuple[int, int]] = []
    search_from = 0
    while True:
        start = text.find("<!--", search_from)
        if start < 0:
            break
        containing = _containing_range(start, protected)
        if containing is not None:
            search_from = containing[1]
            continue
        close = text.find("-->", start + 4)
        if close < 0:
            break
        end = close + 3
        payload = text[start + 4 : close]
        if re.match(r"^\s*svelte-ignore\s", payload) is None:
            ranges.append((start, end))
        search_from = end
    return tuple(ranges)


def _javascript_string_end(text: str, start: int, limit: int) -> int | None:
    quote = text[start]
    index = start + 1
    while index < limit:
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == quote:
            return index + 1
        if quote != "`" and char in _ECMASCRIPT_LINE_ENDINGS:
            return None
        index += 1
    return None


def _javascript_regex_end(text: str, start: int, limit: int) -> int | None:
    index = start + 1
    in_class = False
    while index < limit:
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char in _ECMASCRIPT_LINE_ENDINGS:
            return None
        if char == "[":
            in_class = True
        elif char == "]":
            in_class = False
        elif char == "/" and not in_class:
            index += 1
            while index < limit and (text[index].isalpha() or text[index].isdigit()):
                index += 1
            return index
        index += 1
    return None


def _scan_javascript_comments(
    text: str,
    start: int,
    limit: int,
    *,
    expression: bool,
) -> tuple[int, list[tuple[int, int]]] | None:
    comments: list[tuple[int, int]] = []
    index = start + 1 if expression else start
    depth = 1 if expression else 0
    regex_allowed = True

    while index < limit:
        char = text[index]
        if char.isspace():
            index += 1
            continue
        if char in {'"', "'", "`"}:
            end = _javascript_string_end(text, index, limit)
            if end is None:
                return None
            index = end
            regex_allowed = False
            continue
        if text.startswith("//", index):
            end = index + 2
            while end < limit and text[end] not in _ECMASCRIPT_LINE_ENDINGS:
                end += 1
            comments.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2, limit)
            if close < 0:
                return None
            end = close + 2
            comments.append((index, end))
            index = end
            continue
        if char == "/":
            if regex_allowed:
                end = _javascript_regex_end(text, index, limit)
                if end is None:
                    return None
                index = end
                regex_allowed = False
            else:
                index += 1
                regex_allowed = True
            continue
        if char == "{":
            depth += 1
            index += 1
            regex_allowed = True
            continue
        if char == "}":
            if expression:
                depth -= 1
                if depth == 0:
                    return index + 1, comments
            index += 1
            regex_allowed = False
            continue
        if char.isalpha() or char in {"_", "$"}:
            index += 1
            while index < limit and (text[index].isalnum() or text[index] in {"_", "$"}):
                index += 1
            regex_allowed = False
            continue
        if char.isdigit():
            index += 1
            while index < limit and (text[index].isalnum() or text[index] in {".", "_"}):
                index += 1
            regex_allowed = False
            continue
        regex_allowed = char in "([,:;=!?&|+-*%^~<>"
        index += 1

    if expression:
        return None
    return limit, comments


def _mdx_esm_ranges(text: str, protected: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    line_start = 0
    while line_start < len(text):
        line_end, next_line = _line_bounds(text, line_start)
        containing = _containing_range(line_start, protected)
        if containing is not None:
            line_start = max(next_line, containing[1])
            continue
        if _ESM_START.match(text[line_start:line_end]) is None:
            if next_line == line_start:
                break
            line_start = next_line
            continue

        region_start = line_start
        region_end = line_end
        cursor = next_line
        while cursor < len(text):
            current_end, following = _line_bounds(text, cursor)
            if not text[cursor:current_end].strip(" \t"):
                break
            region_end = current_end
            cursor = following
        ranges.append((region_start, region_end))
        line_start = cursor
    return ranges


def _mdx_brace_context(text: str, brace: int, tag_range: tuple[int, int] | None) -> str:
    if tag_range is None:
        return "content"
    tag_start, _ = tag_range
    quote: str | None = None
    index = tag_start + 1
    while index < brace:
        char = text[index]
        if quote is not None:
            if char == "\\":
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char in {'"', "'"}:
            quote = char
        index += 1
    if quote is not None:
        return "quoted"

    previous = brace - 1
    while previous > tag_start and text[previous] in " \t\r\n":
        previous -= 1
    if text[previous : previous + 1] == "=":
        return "value"
    if text[brace + 1 :].lstrip().startswith("..."):
        return "spread"
    return "invalid"


def mdx_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return JavaScript comments from valid default MDX regions."""

    protected = _markdown_code_ranges(text, front_matter=True)
    tag_ranges = _markup_tag_ranges(text, protected)
    esm_ranges = _mdx_esm_ranges(text, protected)
    comments: list[tuple[int, int]] = []

    for start, end in esm_ranges:
        result = _scan_javascript_comments(text, start, end, expression=False)
        if result is None:
            return ()
        comments.extend(result[1])

    skipped = _merge_ranges([*protected, *esm_ranges])
    index = 0
    while index < len(text):
        containing = _containing_range(index, skipped)
        if containing is not None:
            index = containing[1]
            continue
        if text[index] != "{":
            index += 1
            continue

        tag_range = _containing_range(index, tag_ranges)
        context = _mdx_brace_context(text, index, tag_range)
        if context == "quoted":
            index += 1
            continue
        result = _scan_javascript_comments(text, index, len(text), expression=True)
        if result is None:
            return ()
        expression_end, expression_comments = result
        if context == "invalid":
            return ()
        comments.extend(expression_comments)
        index = expression_end

    return tuple(_merge_ranges(comments))


def mermaid_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return portable Mermaid own-line comments in original source offsets."""

    front_matter = _front_matter_range(text)
    ranges: list[tuple[int, int]] = []
    line_start = 0
    while line_start < len(text):
        line_end, next_line = _line_bounds(text, line_start)
        if front_matter is None or not (front_matter[0] <= line_start < front_matter[1]):
            marker = line_start
            while marker < line_end and text[marker] in " \t":
                marker += 1
            if text.startswith("%%", marker) and marker + 2 < line_end and text[marker + 2] != "{":
                ranges.append((marker, line_end))
        if next_line == line_start:
            break
        line_start = next_line
    return tuple(ranges)


def _long_bracket_end(text: str, start: int) -> int | None:
    if text[start : start + 1] != "[":
        return None
    index = start + 1
    while text[index : index + 1] == "=":
        index += 1
    if text[index : index + 1] != "[":
        return None
    close = "]" + "=" * (index - start - 1) + "]"
    close_start = text.find(close, index + 1)
    return len(text) if close_start < 0 else close_start + len(close)


def luau_string_ranges(text: str) -> list[tuple[int, int]]:
    """Return Luau quoted, interpolated, and long-string ranges."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("--", index):
            long_comment_end = _long_bracket_end(text, index + 2)
            if long_comment_end is not None:
                index = long_comment_end
            else:
                index = _line_bounds(text, index)[0]
            continue
        char = text[index]
        if char in {'"', "'", "`"}:
            end = _javascript_string_end(text, index, len(text))
            if end is None:
                line_end = index + 1
                while line_end < len(text) and text[line_end] not in "\r\n":
                    line_end += 1
                end = line_end
            ranges.append((index, end))
            index = end
            continue
        if char == "[":
            end = _long_bracket_end(text, index)
            if end is not None:
                ranges.append((index, end))
                index = end
                continue
        index += 1
    return ranges


def minizinc_string_ranges(text: str) -> list[tuple[int, int]]:
    """Return MiniZinc string and backtick-identifier ranges, including errors."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == "%":
            while index < len(text) and text[index] != "\n":
                index += 1
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            index = len(text) if close < 0 else close + 2
            continue
        if text[index] not in {'"', "`"}:
            index += 1
            continue
        start = index
        quote = text[index]
        index += 1
        while index < len(text):
            if text[index] == "\\":
                index += 2
                continue
            if text[index] == quote:
                index += 1
                break
            index += 1
        ranges.append((start, min(index, len(text))))
    return ranges


STACK_V3_BATCH_05_CONTEXTUAL_EXTRACTORS: dict[str, Callable[[str], tuple[tuple[int, int], ...]]] = {
    "mdsvex_comments": mdsvex_comment_ranges,
    "mdx_comments": mdx_comment_ranges,
    "mermaid_comments": mermaid_comment_ranges,
}


__all__ = [
    "STACK_V3_BATCH_05_CONTEXTUAL_EXTRACTORS",
    "luau_string_ranges",
    "mdsvex_comment_ranges",
    "mdx_comment_ranges",
    "mermaid_comment_ranges",
    "minizinc_string_ranges",
]
