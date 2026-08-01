"""Reviewed Stack v3 batch 06 and 07 comment scanners."""

from __future__ import annotations

import re
from collections.abc import Callable

_MOONBIT_LINE_ENDINGS = "\r\n\u2028\u2029"
_ASCII_HORIZONTAL_SPACE = " \t"


def _line_end(text: str, start: int, endings: str = "\r\n") -> int:
    index = start
    while index < len(text) and text[index] not in endings:
        index += 1
    return index


def _quoted_end(
    text: str,
    start: int,
    quote: str,
    *,
    doubled: bool = False,
    escaped: bool = True,
    multiline: bool = True,
) -> int:
    """Return a quoted token's end, protecting malformed input through EOF."""

    index = start + len(quote)
    while index < len(text):
        if doubled and text.startswith(quote + quote, index):
            index += len(quote) * 2
            continue
        if escaped and text[index] == "\\":
            index = min(index + 2, len(text))
            continue
        if text.startswith(quote, index):
            return index + len(quote)
        if not multiline and text[index] in "\r\n":
            return len(text)
        index += 1
    return len(text)


def _ordinary_literal_end(text: str, start: int) -> int | None:
    if text.startswith(('"""', "'''"), start):
        token = text[start : start + 3]
        return _quoted_end(text, start, token)
    if text[start] == '"':
        return _quoted_end(text, start, '"')
    if text[start] != "'":
        return None

    # A source-language lifetime or apostrophe identifier is not a character
    # literal unless a close appears before a physical newline.
    index = start + 1
    if index < len(text) and text[index] == "\\":
        index += 2
    else:
        index += 1
    return index + 1 if index < len(text) and text[index] == "'" else None


def _raw_hash_string_end(text: str, start: int) -> int | None:
    """Return Rust/Nushell-style raw string end when one starts at ``start``."""

    if text[start : start + 1].lower() != "r":
        return None
    index = start + 1
    while index < len(text) and text[index] == "#":
        index += 1
    if index >= len(text) or text[index] not in {"'", '"'}:
        return None
    quote = text[index]
    hashes = text[start + 1 : index]
    close_token = quote + hashes
    close = text.find(close_token, index + 1)
    return len(text) if close < 0 else close + len(close_token)


def rust_noir_literal_ranges(text: str) -> list[tuple[int, int]]:
    """Return ordinary, byte, format, and hash-delimited literal ranges."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("//", index):
            index = _line_end(text, index)
            continue
        if text.startswith("/*", index):
            depth = 1
            index += 2
            while index < len(text) and depth:
                if text.startswith("/*", index):
                    depth += 1
                    index += 2
                elif text.startswith("*/", index):
                    depth -= 1
                    index += 2
                else:
                    index += 1
            continue
        raw_end = _raw_hash_string_end(text, index)
        if raw_end is not None:
            ranges.append((index, raw_end))
            index = raw_end
            continue
        literal_end = _ordinary_literal_end(text, index)
        if literal_end is not None:
            ranges.append((index, literal_end))
            index = literal_end
            continue
        index += 1
    return ranges


def mojo_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Mojo hash comments outside all quote widths."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        literal_end = _ordinary_literal_end(text, index)
        if literal_end is not None:
            index = literal_end
            continue
        if text[index] == "#":
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


_MOONBIT_PRAGMAS = ("@alert", "@intrinsic", "@gen_js", "@coverage.skip")


def _moonbit_semantic_comment(text: str, start: int, end: int) -> bool:
    line_start = (
        max(
            text.rfind("\n", 0, start),
            text.rfind("\r", 0, start),
            text.rfind("\u2028", 0, start),
            text.rfind("\u2029", 0, start),
        )
        + 1
    )
    own_line = not text[line_start:start].strip(_ASCII_HORIZONTAL_SPACE)
    comment = text[start:end]
    if own_line and re.match(r"//![-A-Za-z0-9_.]+:", comment):
        return True
    payload = comment.lstrip("/").lstrip(_ASCII_HORIZONTAL_SPACE)
    return any(
        payload == pragma or payload.startswith(pragma + " ") or payload.startswith(pragma + "\t")
        for pragma in _MOONBIT_PRAGMAS
    )


def moonbit_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return MoonBit prose comments while excluding semantic directives."""

    ranges: list[tuple[int, int]] = []
    index = 0
    line_start = True
    while index < len(text):
        char = text[index]
        if char in _MOONBIT_LINE_ENDINGS:
            line_start = True
            index += 1
            continue
        if line_start and char in _ASCII_HORIZONTAL_SPACE:
            index += 1
            continue
        if line_start and text.startswith(("#|", "$|"), index):
            index = _line_end(text, index, _MOONBIT_LINE_ENDINGS)
            continue
        line_start = False

        literal_end = _ordinary_literal_end(text, index)
        if literal_end is not None:
            index = literal_end
            continue
        if text.startswith("//", index):
            end = _line_end(text, index, _MOONBIT_LINE_ENDINGS)
            if not _moonbit_semantic_comment(text, index, end):
                ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _nushell_raw_string_end(text: str, start: int) -> int | None:
    raw_end = _raw_hash_string_end(text, start)
    if raw_end is not None:
        return raw_end
    return None


def nushell_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Nushell boundary-qualified comments outside literal items."""

    ranges: list[tuple[int, int]] = []
    index = 0
    depth = 0
    if text.startswith("#!"):
        index = _line_end(text, 0, "\n")

    while index < len(text):
        raw_end = _nushell_raw_string_end(text, index)
        if raw_end is not None:
            index = raw_end
            continue
        if text[index] in {"'", '"', "`"}:
            index = _quoted_end(text, index, text[index])
            continue

        char = text[index]
        if char in "([{":
            depth += 1
            index += 1
            continue
        if char in ")]}":
            depth = max(depth - 1, 0)
            index += 1
            continue
        if char == "#":
            previous = text[index - 1 : index]
            at_item_boundary = index == 0 or previous in _ASCII_HORIZONTAL_SPACE + "\r\n([{,;|"
            if at_item_boundary:
                endings = "\r\n" if depth else "\n"
                end = _line_end(text, index, endings)
                ranges.append((index, end))
                index = end
                continue
        index += 1
    return tuple(ranges)


def _keyword_at(text: str, index: int, keyword: str) -> bool:
    if not text.startswith(keyword, index):
        return False
    before = text[index - 1 : index]
    after = text[index + len(keyword) : index + len(keyword) + 1]
    return not (before and (before.isalnum() or before == "_")) and not (
        after and (after.isalnum() or after == "_")
    )


def _nmodl_identifier_colon(text: str, index: int) -> bool:
    before = text[index - 1 : index]
    after = text[index + 1 : index + 2]
    return bool(before and after and (before.isalnum() or before == "_") and after.isalnum())


def nmodl_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return punctuation and keyword comments outside NMODL copy modes."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == '"':
            index = _quoted_end(text, index, '"')
            continue
        if _keyword_at(text, index, "VERBATIM"):
            close = text.find("ENDVERBATIM", index + len("VERBATIM"))
            wrong_close = text.find("ENDCOMMENT", index + len("VERBATIM"))
            if close < 0 or (0 <= wrong_close < close):
                break
            index = close + len("ENDVERBATIM")
            continue
        if _keyword_at(text, index, "COMMENT"):
            close = text.find("ENDCOMMENT", index + len("COMMENT"))
            wrong_close = text.find("ENDVERBATIM", index + len("COMMENT"))
            if close < 0 or (0 <= wrong_close < close):
                break
            end = close + len("ENDCOMMENT")
            ranges.append((index, end))
            index = end
            continue
        if text[index] == ":" and not _nmodl_identifier_colon(text, index):
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        if text[index] == "?":
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _balanced_property_end(text: str, start: int) -> int | None:
    name_end = start + 1
    while name_end < len(text) and (text[name_end].isalnum() or text[name_end] in "_-."):
        name_end += 1
    index = name_end
    while index < len(text) and text[index] in _ASCII_HORIZONTAL_SPACE:
        index += 1
    if index >= len(text) or text[index] != "(":
        return None

    stack = [")"]
    index += 1
    pairs = {"(": ")", "[": "]", "{": "}"}
    while index < len(text):
        if text[index] in {"'", '"'}:
            index = _quoted_end(text, index, text[index])
            continue
        if text[index] in pairs:
            stack.append(pairs[text[index]])
        elif text[index] == stack[-1]:
            stack.pop()
            if not stack:
                return index + 1
        index += 1
    return len(text)


def _cplusplus_body_end(text: str, start: int) -> int | None:
    if not _keyword_at(text, start, "cplusplus"):
        return None
    index = start + len("cplusplus")
    while index < len(text) and text[index].isspace():
        index += 1
    if not text.startswith("{{", index):
        return None
    close = text.find("}}", index + 2)
    return len(text) if close < 0 else close + 2


def _omnet_comment_ranges(text: str, *, embedded_cpp: bool) -> tuple[tuple[int, int], ...]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] in {"'", '"'}:
            index = _quoted_end(text, index, text[index])
            continue
        if text[index] == "@":
            property_end = _balanced_property_end(text, index)
            if property_end is not None:
                index = property_end
                continue
        if embedded_cpp:
            body_end = _cplusplus_body_end(text, index)
            if body_end is not None:
                index = body_end
                continue
        if text.startswith("//", index):
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def omnet_msg_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return host MSG comments outside property and embedded-C++ states."""

    return _omnet_comment_ranges(text, embedded_cpp=True)


def omnet_ned_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return host NED comments outside quote and property-value states."""

    return _omnet_comment_ranges(text, embedded_cpp=False)


def pip_requirements_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return pip whitespace-boundary comments in exact physical source."""

    ranges: list[tuple[int, int]] = []
    line_start = 0
    while line_start < len(text):
        line_end = _line_end(text, line_start)
        index = line_start
        while index < line_end:
            if text[index] == "#" and (index == line_start or text[index - 1].isspace()):
                ranges.append((index, line_end))
                break
            index += 1
        if line_end == len(text):
            break
        line_start = line_end + (2 if text.startswith("\r\n", line_end) else 1)
    return tuple(ranges)


def _praat_curly_string_end(text: str, start: int) -> int:
    index = start + 1
    while index < len(text):
        if text.startswith("””", index):
            index += 2
            continue
        if text[index] == "”":
            return index + 1
        if text[index] in "\r\n":
            return len(text)
        index += 1
    return len(text)


def praat_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Praat whole-line markers and quote-aware semicolon suffixes."""

    ranges: list[tuple[int, int]] = []
    line_start = 0
    while line_start < len(text):
        line_end = _line_end(text, line_start)
        first = line_start
        while first < line_end and text[first] in _ASCII_HORIZONTAL_SPACE:
            first += 1
        if first < line_end and text[first] in "#;!":
            ranges.append((first, line_end))
        else:
            index = first
            while index < line_end:
                if text[index] == '"':
                    index = _quoted_end(
                        text,
                        index,
                        '"',
                        doubled=True,
                        escaped=False,
                        multiline=False,
                    )
                    if index == len(text):
                        return tuple(ranges)
                    continue
                if text[index] == "“":
                    index = _praat_curly_string_end(text, index)
                    if index == len(text):
                        return tuple(ranges)
                    continue
                if text[index] == ";":
                    ranges.append((index, line_end))
                    break
                index += 1
        if line_end == len(text):
            break
        line_start = line_end + (2 if text.startswith("\r\n", line_end) else 1)
    return tuple(ranges)


def _overpassql_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] in {"'", '"'}:
            index = _quoted_end(text, index, text[index])
            continue
        if text.startswith("//", index):
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            if close < 0:
                break
            end = close + 2
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _semicolon_comment_ranges(text: str, *, protect_strings: bool) -> tuple[tuple[int, int], ...]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if protect_strings and text[index] == '"':
            index = _quoted_end(text, index, '"')
            continue
        if text[index] == ";":
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _polar_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == '"':
            index = _quoted_end(text, index, '"')
            continue
        if text[index] == "#":
            end = _line_end(text, index)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _noir_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        raw_end = _raw_hash_string_end(text, index)
        if raw_end is not None:
            index = raw_end
            continue
        literal_end = _ordinary_literal_end(text, index)
        if literal_end is not None:
            index = literal_end
            continue
        if text.startswith("//", index):
            end = _line_end(text, index, "\n")
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            start = index
            depth = 1
            index += 2
            while index < len(text) and depth:
                if text.startswith("/*", index):
                    depth += 1
                    index += 2
                elif text.startswith("*/", index):
                    depth -= 1
                    index += 2
                else:
                    index += 1
            if depth:
                break
            ranges.append((start, index))
            continue
        index += 1
    return tuple(ranges)


_ALIAS_RANGE_EXTRACTORS: dict[str, Callable[[str], tuple[tuple[int, int], ...]]] = {
    "noir": _noir_comment_ranges,
    "overpassql": _overpassql_comment_ranges,
    "pact": lambda text: _semicolon_comment_ranges(text, protect_strings=True),
    "pddl": lambda text: _semicolon_comment_ranges(text, protect_strings=False),
    "polar": _polar_comment_ranges,
}


def reviewed_batch_06_07_alias_comment_ranges(
    language: str, text: str
) -> tuple[tuple[int, int], ...] | None:
    """Return exact ranges for reviewed aliases, or ``None`` for other keys."""

    normalized = re.sub(r"[^a-z0-9]+", "_", language.strip().lower()).strip("_")
    extractor = _ALIAS_RANGE_EXTRACTORS.get(normalized)
    return None if extractor is None else extractor(text)


STACK_V3_BATCH_06_07_CONTEXTUAL_EXTRACTORS: dict[
    str, Callable[[str], tuple[tuple[int, int], ...]]
] = {
    "mojo_comments": mojo_comment_ranges,
    "moonbit_comments": moonbit_comment_ranges,
    "nmodl_comments": nmodl_comment_ranges,
    "nushell_comments": nushell_comment_ranges,
    "omnet_msg_comments": omnet_msg_comment_ranges,
    "omnet_ned_comments": omnet_ned_comment_ranges,
    "pip_requirements_comments": pip_requirements_comment_ranges,
    "praat_comments": praat_comment_ranges,
}


__all__ = [
    "STACK_V3_BATCH_06_07_CONTEXTUAL_EXTRACTORS",
    "reviewed_batch_06_07_alias_comment_ranges",
    "rust_noir_literal_ranges",
]
