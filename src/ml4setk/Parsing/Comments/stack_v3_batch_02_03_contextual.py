"""Reviewed Stack v3 batch 02 and 03 comment scanners.

The contextual extractors in this module own languages whose comment syntax
depends on lexer state.  The alias overrides keep dataset labels attached to
their established registry families while preserving their exact lexical
boundaries.
"""

from __future__ import annotations

import re
from collections.abc import Callable

_ECMASCRIPT_LINE_ENDINGS = "\r\n\u2028\u2029"


def _line_end(text: str, start: int, endings: str) -> int:
    index = start
    while index < len(text) and text[index] not in endings:
        index += 1
    return index


def _quoted_end(
    text: str,
    start: int,
    quote: str,
    *,
    multiline: bool = True,
    doubled: bool = False,
) -> int:
    """Return a quoted token's end, conservatively protecting malformed EOF."""

    index = start + len(quote)
    while index < len(text):
        if doubled and text.startswith(quote + quote, index):
            index += len(quote) * 2
            continue
        if text[index] == "\\":
            index = min(index + 2, len(text))
            continue
        if text.startswith(quote, index):
            return index + len(quote)
        if not multiline and text[index] in _ECMASCRIPT_LINE_ENDINGS:
            return index
        index += 1
    return len(text)


def _balanced_bracket_end(text: str, start: int) -> int:
    """Return the end of a bracketed lexer token, or EOF when malformed."""

    depth = 1
    index = start + 1
    while index < len(text):
        if text[index] in {"'", '"'}:
            index = _quoted_end(text, index, text[index])
            continue
        if text[index] == "[":
            depth += 1
        elif text[index] == "]":
            depth -= 1
            if depth == 0:
                return index + 1
        index += 1
    return len(text)


def dune_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Dune semicolon comments outside quoted and EOL strings."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == '"':
            index = _quoted_end(text, index, '"')
            continue
        if text.startswith(("\\|", "\\>"), index):
            index = _line_end(text, index, "\r\n")
            continue
        if text[index] == ";":
            end = _line_end(text, index, "\r\n")
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _html_tag_end(text: str, start: int) -> int:
    quote = ""
    index = start + 1
    while index < len(text):
        char = text[index]
        if quote:
            if char == quote:
                quote = ""
            index += 1
            continue
        if char in {"'", '"'}:
            quote = char
        elif char == ">":
            return index + 1
        index += 1
    return len(text)


def ecmarkup_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return closed conforming HTML comments in Ecmarkup tokenizer data."""

    ranges: list[tuple[int, int]] = []
    lower = text.lower()
    index = 0
    while index < len(text):
        if text.startswith("<!--", index):
            close = text.find("-->", index + 4)
            if close < 0:
                break
            end = close + 3
            if text.find("<!--", index + 4, close) < 0:
                ranges.append((index, end))
            index = end
            continue
        if text[index] != "<":
            index += 1
            continue

        tag_match = re.match(r"<\s*(script|style)(?=[\s/>])", lower[index:])
        if tag_match:
            tag_name = tag_match.group(1)
            open_end = _html_tag_end(text, index)
            close_start = lower.find(f"</{tag_name}", open_end)
            if close_start < 0:
                break
            index = _html_tag_end(text, close_start)
            continue
        index = _html_tag_end(text, index)
    return tuple(ranges)


_DOLLAR_QUOTE = re.compile(r"\$(?:[A-Za-z_][A-Za-z0-9_]*)?\$")


def _edgeql_string_end(text: str, start: int) -> int | None:
    dollar = _DOLLAR_QUOTE.match(text, start)
    if dollar:
        delimiter = dollar.group(0)
        close = text.find(delimiter, dollar.end())
        return len(text) if close < 0 else close + len(delimiter)

    index = start
    while index < len(text) and text[index].lower() in {"r", "b"}:
        index += 1
        if index - start == 2:
            break
    if index >= len(text) or text[index] not in {"'", '"'}:
        if text[start] not in {"'", '"'}:
            return None
        index = start

    quote = text[index]
    triple = text.startswith(quote * 3, index)
    token = quote * (3 if triple else 1)
    raw = "r" in text[start:index].lower()
    cursor = index + len(token)
    while cursor < len(text):
        if not raw and text[cursor] == "\\":
            cursor = min(cursor + 2, len(text))
            continue
        if text.startswith(token, cursor):
            return cursor + len(token)
        cursor += 1
    return len(text)


def edgeql_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return EdgeQL hash comments outside all documented string forms."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        string_end = _edgeql_string_end(text, index)
        if string_end is not None:
            index = string_end
            continue
        if text[index] == "#":
            end = _line_end(text, index, "\r\n")
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def f_star_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return F* line and recursively nested block comments."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] in {"'", '"'}:
            index = _quoted_end(text, index, text[index])
            continue
        if text.startswith("```", index):
            run_end = index
            while run_end < len(text) and text[run_end] == "`":
                run_end += 1
            delimiter = text[index:run_end]
            close = text.find(delimiter, run_end)
            index = len(text) if close < 0 else close + len(delimiter)
            continue
        if text.startswith("// IN F*:", index):
            index += len("// IN F*:")
            continue
        if text.startswith("//", index):
            end = _line_end(text, index, _ECMASCRIPT_LINE_ENDINGS)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("(*", index):
            start = index
            depth = 1
            index += 2
            while index < len(text) and depth:
                if text.startswith("(*", index):
                    depth += 1
                    index += 2
                elif text.startswith("*)", index):
                    depth -= 1
                    index += 2
                else:
                    index += 1
            ranges.append((start, index))
            continue
        index += 1
    return tuple(ranges)


def firrtl_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return FIRRTL semicolon comments outside atomic lexer tokens."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] in {"'", '"', "`"}:
            index = _quoted_end(text, index, text[index])
            continue
        if text.startswith(("@[", "%["), index):
            index = _balanced_bracket_end(text, index + 1)
            continue
        if text[index] == ";":
            end = _line_end(text, index, "\r\n")
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def gdshader_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Godot shader comments with its LF-only and EOF block rules."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == '"':
            index = _quoted_end(text, index, '"')
            continue
        if text.startswith("//", index):
            end = _line_end(text, index, "\n")
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


def hare_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Hare LF-only line comments outside its literal forms."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] in {"'", '"', "`"}:
            index = _quoted_end(text, index, text[index])
            continue
        if text.startswith("//", index):
            end = _line_end(text, index, "\n")
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _cpp_raw_string_end(text: str, start: int) -> int | None:
    if not text.startswith('R"', start):
        return None
    delimiter_end = text.find("(", start + 2, min(start + 19, len(text)))
    if delimiter_end < 0:
        return None
    delimiter = text[start + 2 : delimiter_end]
    if any(char.isspace() or char in "\\()" for char in delimiter):
        return None
    close_token = ")" + delimiter + '"'
    close = text.find(close_token, delimiter_end + 1)
    return len(text) if close < 0 else close + len(close_token)


def hip_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return HIP-Clang comments, including logical line continuations."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        raw_end = _cpp_raw_string_end(text, index)
        if raw_end is not None:
            index = raw_end
            continue
        if text[index] in {"'", '"'}:
            index = _quoted_end(text, index, text[index], multiline=False)
            continue
        if text.startswith("//", index):
            start = index
            index += 2
            while index < len(text):
                if text.startswith("\\\r\n", index):
                    index += 3
                    continue
                if text.startswith("\\\n", index) or text.startswith("\\\r", index):
                    index += 2
                    continue
                if text[index] in "\r\n":
                    break
                index += 1
            ranges.append((start, index))
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


def hosts_file_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return the first hash suffix on each hosts-file physical line."""

    ranges: list[tuple[int, int]] = []
    line_start = 0
    while line_start < len(text):
        lf = text.find("\n", line_start)
        physical_end = len(text) if lf < 0 else lf
        content_end = (
            physical_end - 1
            if physical_end > line_start and text[physical_end - 1] == "\r"
            else physical_end
        )
        marker = text.find("#", line_start, content_end)
        if marker >= 0:
            ranges.append((marker, content_end))
        if lf < 0:
            break
        line_start = lf + 1
    return tuple(ranges)


def edge_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return raw-mode Edge comments using the lexer's brace-depth close rule."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("{{--", index):
            line_start = max(text.rfind("\n", 0, index), text.rfind("\r", 0, index)) + 1
            if text[line_start:index].lstrip().startswith("@"):
                index += 4
                continue
            start = index
            depth = 0
            index += 4
            while index < len(text):
                if depth == 0 and text.startswith("--}}", index):
                    index += 4
                    ranges.append((start, index))
                    break
                if text[index] == "{":
                    depth += 1
                elif text[index] == "}":
                    if depth == 0:
                        index = len(text)
                        break
                    depth -= 1
                index += 1
            continue
        if text.startswith("{{", index):
            close = text.find("}}", index + 2)
            if close < 0:
                break
            index = close + 2
            continue
        index += 1
    return tuple(ranges)


def _regex_literal_end(text: str, start: int) -> int | None:
    """Return a conservative JavaScript/Imba regex literal end."""

    previous = start - 1
    while previous >= 0 and text[previous].isspace():
        previous -= 1
    if previous >= 0 and (text[previous].isalnum() or text[previous] in "_)]}"):
        return None

    index = start + 1
    in_class = False
    while index < len(text):
        char = text[index]
        if char == "\\":
            index = min(index + 2, len(text))
            continue
        if char in _ECMASCRIPT_LINE_ENDINGS:
            return None
        if char == "[":
            in_class = True
        elif char == "]":
            in_class = False
        elif char == "/" and not in_class:
            index += 1
            while index < len(text) and (text[index].isalnum() or text[index] == "_"):
                index += 1
            return index
        index += 1
    return None


def _glimmer_comment_end(text: str, start: int) -> int | None:
    if text.startswith(("{{!--", "{{~!--"), start):
        candidates = [
            close for token in ("--}}", "--~}}") if (close := text.find(token, start + 6)) >= 0
        ]
        if not candidates:
            return None
        close = min(candidates)
        return close + (5 if text.startswith("--~}}", close) else 4)
    if text.startswith(("{{!", "{{~!"), start):
        candidates = [
            close for token in ("}}", "~}}") if (close := text.find(token, start + 3)) >= 0
        ]
        if not candidates:
            return None
        close = min(candidates)
        return close + (3 if text.startswith("~}}", close) else 2)
    return None


def _scan_glimmer_template(text: str, start: int) -> tuple[list[tuple[int, int]], int | None]:
    ranges: list[tuple[int, int]] = []
    index = start
    in_tag = False
    quote = ""
    while index < len(text):
        if quote:
            if text[index] == quote:
                quote = ""
            index += 1
            continue
        if in_tag and text[index] in {"'", '"'}:
            quote = text[index]
            index += 1
            continue
        if not in_tag and text.startswith("</template>", index):
            return ranges, index + len("</template>")

        boundary = not in_tag or index == 0 or text[index - 1].isspace()
        if boundary and text.startswith(("{{!--", "{{~!--", "{{!", "{{~!"), index):
            end = _glimmer_comment_end(text, index)
            if end is None:
                return ranges, None
            ranges.append((index, end))
            index = end
            continue
        if not in_tag and text.startswith("<!--", index):
            close = text.find("-->", index + 4)
            if close < 0:
                return ranges, None
            end = close + 3
            ranges.append((index, end))
            index = end
            continue
        if text[index] == "<":
            in_tag = True
        elif in_tag and text[index] == ">":
            in_tag = False
        index += 1
    return ranges, None


def glimmer_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return JS/TS comments outside content tags and Glimmer comments inside."""

    ranges: list[tuple[int, int]] = []
    index = 0
    if text.startswith("#!"):
        index = _line_end(text, 0, _ECMASCRIPT_LINE_ENDINGS)
    while index < len(text):
        if text[index] in {"'", '"', "`"}:
            index = _quoted_end(text, index, text[index])
            continue
        if text.startswith("//", index):
            end = _line_end(text, index, _ECMASCRIPT_LINE_ENDINGS)
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
        if text[index] == "/":
            regex_end = _regex_literal_end(text, index)
            if regex_end is not None:
                index = regex_end
                continue
        if text.startswith("<template>", index):
            template_ranges, end = _scan_glimmer_template(text, index + len("<template>"))
            if end is None:
                break
            ranges.extend(template_ranges)
            index = end
            continue
        index += 1
    return tuple(ranges)


def godot_resource_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Godot resource semicolon comments outside Variant strings."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == '"':
            index = _quoted_end(text, index, '"')
            continue
        if text[index] == ";":
            end = _line_end(text, index, "\n")
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def imba_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return the hash-comment subset shared by Imba 1 and Imba 2."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        triple = text[index : index + 3]
        if triple in {"'''", '"""'}:
            index = _quoted_end(text, index, triple)
            continue
        if text[index] in {"'", '"', "`"}:
            index = _quoted_end(text, index, text[index])
            continue
        if text[index] == "/":
            regex_end = _regex_literal_end(text, index)
            if regex_end is not None:
                index = regex_end
                continue
        if text.startswith("###", index):
            body_start = index + 3
            if body_start < len(text) and text[body_start] != "#":
                close = text.find("###", body_start + 1)
                end = len(text) if close < 0 else close + 3
                ranges.append((index, end))
                index = end
                continue
            index += 3
            continue
        if text[index] == "#":
            following = text[index + 1 : index + 2]
            if not following or following in " \t!\r\n":
                end = _line_end(text, index, "\n")
                ranges.append((index, end))
                index = end
                continue
        index += 1
    return tuple(ranges)


def ink_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Ink comments from its raw preprocessing pass."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("//", index):
            end = _line_end(text, index, "\r\n")
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            if close >= 0:
                end = close + 2
                ranges.append((index, end))
                index = end
                continue
            if index + 2 < len(text):
                ranges.append((index, len(text)))
            break
        index += 1
    return tuple(ranges)


_ALIAS_RANGE_EXTRACTORS: dict[str, Callable[[str], tuple[tuple[int, int], ...]]] = {
    "dune": dune_comment_ranges,
    "ecmarkup": ecmarkup_comment_ranges,
    "edgeql": edgeql_comment_ranges,
    "firrtl": firrtl_comment_ranges,
    "hare": hare_comment_ranges,
    "hip": hip_comment_ranges,
    "hosts_file": hosts_file_comment_ranges,
}


def reviewed_alias_comment_ranges(language: str, text: str) -> tuple[tuple[int, int], ...] | None:
    """Return exact ranges for a reviewed alias, or ``None`` for other keys."""

    normalized = re.sub(r"[^a-z0-9]+", "_", language.strip().lower()).strip("_")
    extractor = _ALIAS_RANGE_EXTRACTORS.get(normalized)
    return None if extractor is None else extractor(text)


STACK_V3_BATCH_02_03_CONTEXTUAL_EXTRACTORS: dict[
    str, Callable[[str], tuple[tuple[int, int], ...]]
] = {
    "edge_comments": edge_comment_ranges,
    "f_star_comments": f_star_comment_ranges,
    "gdshader_comments": gdshader_comment_ranges,
    "glimmer_comments": glimmer_comment_ranges,
    "godot_resource_comments": godot_resource_comment_ranges,
    "imba_comments": imba_comment_ranges,
    "ink_comments": ink_comment_ranges,
}


__all__ = [
    "STACK_V3_BATCH_02_03_CONTEXTUAL_EXTRACTORS",
    "reviewed_alias_comment_ranges",
]
