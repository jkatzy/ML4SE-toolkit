"""Reviewed Stack v3 batch 08 and 09 comment scanners.

These scanners implement lexer-state contracts that cannot be represented by
the registry's delimiter metadata alone.  They deliberately return only
complete, verified comment regions and conservatively protect malformed lexer
states from producing nested false positives.
"""

from __future__ import annotations

import io
import re
import tokenize
from collections.abc import Callable
from typing import Optional

_CR_LF = "\r\n"
_CXX_RAW_PREFIX = re.compile(r'(?:u8|u|U|L)?R"([^\s()\\]{0,16})\(')
_RUST_RAW_PREFIX = re.compile(r'(?:br|rb|r)(?P<hashes>#{0,255})"')
_RBS_ANNOTATION_CLOSERS = {"{": "}", "(": ")", "[": "]", "|": "|", "<": ">"}
_SAIL_IDENTIFIER = re.compile(r"[A-Za-z?_][A-Za-z0-9?'#_]*")
_SURVEX_SET = re.compile(r"(?i)^\s*\*set\s+(comment|eol|quote)\b(.*)$", re.DOTALL)


def _line_end(text: str, start: int, endings: str = _CR_LF) -> int:
    index = start
    while index < len(text) and text[index] not in endings:
        index += 1
    return index


def _quoted_end(
    text: str,
    start: int,
    quote: str,
    *,
    multiline: bool = False,
    doubled: bool = False,
) -> tuple[int, bool]:
    """Return a quoted token end and whether a closer was found."""

    index = start + len(quote)
    while index < len(text):
        if doubled and text.startswith(quote + quote, index):
            index += len(quote) * 2
            continue
        if text.startswith(quote, index):
            return index + len(quote), True
        if text[index] == "\\":
            index = min(index + 2, len(text))
            continue
        if not multiline and text[index] in _CR_LF:
            return index, False
        index += 1
    return len(text), False


def _nested_end(
    text: str,
    start: int,
    opener: str,
    closer: str,
) -> int | None:
    depth = 1
    index = start + len(opener)
    while index < len(text):
        if text.startswith(opener, index):
            depth += 1
            index += len(opener)
            continue
        if text.startswith(closer, index):
            depth -= 1
            index += len(closer)
            if depth == 0:
                return index
            continue
        index += 1
    return None


def _rust_raw_end(text: str, start: int) -> int | None:
    match = _RUST_RAW_PREFIX.match(text, start)
    if match is None:
        return None
    if start and (text[start - 1].isalnum() or text[start - 1] == "_"):
        return None
    closer = '"' + match.group("hashes")
    close = text.find(closer, match.end())
    return len(text) if close < 0 else close + len(closer)


def _cxx_raw_end(text: str, start: int) -> int | None:
    match = _CXX_RAW_PREFIX.match(text, start)
    if match is None:
        return None
    if start and (text[start - 1].isalnum() or text[start - 1] == "_"):
        return None
    closer = ")" + match.group(1) + '"'
    close = text.find(closer, match.end())
    return len(text) if close < 0 else close + len(closer)


def _spliced_logical_source(text: str) -> tuple[str, list[int], list[int]]:
    """Remove escaped physical line breaks while retaining source offsets."""

    chars: list[str] = []
    starts: list[int] = []
    ends: list[int] = []
    index = 0
    while index < len(text):
        if text[index] == "\\":
            if text.startswith("\r\n", index + 1):
                index += 3
                continue
            if index + 1 < len(text) and text[index + 1] in _CR_LF:
                index += 2
                continue
        chars.append(text[index])
        starts.append(index)
        ends.append(index + 1)
        index += 1
    return "".join(chars), starts, ends


def _logical_range(
    text: str,
    starts: list[int],
    ends: list[int],
    start: int,
    end: int,
    *,
    through_eof: bool = False,
) -> tuple[int, int]:
    source_start = starts[start]
    source_end = len(text) if through_eof else ends[end - 1]
    return source_start, source_end


def _logical_c_comment_ranges(
    text: str,
    *,
    raw_strings: bool,
) -> tuple[tuple[int, int], ...]:
    """Return non-nested C comments after escaped-line-break removal."""

    logical, starts, ends = _spliced_logical_source(text)
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(logical):
        if raw_strings:
            raw_end = _cxx_raw_end(logical, index)
            if raw_end is not None:
                index = raw_end
                continue
        if logical[index] in {'"', "'"}:
            index, _ = _quoted_end(logical, index, logical[index])
            continue
        if logical.startswith("//", index):
            end = _line_end(logical, index + 2)
            ranges.append(
                _logical_range(
                    text,
                    starts,
                    ends,
                    index,
                    end,
                    through_eof=end == len(logical),
                )
            )
            index = end
            continue
        if logical.startswith("/*", index):
            close = logical.find("*/", index + 2)
            if close < 0:
                break
            end = close + 2
            ranges.append(_logical_range(text, starts, ends, index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def pyret_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Pyret hash lines and complete nested hash-pipe blocks."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] in {'"', "'", "`"}:
            quote = text[index] * 3 if text.startswith(text[index] * 3, index) else text[index]
            index, _ = _quoted_end(text, index, quote, multiline=len(quote) == 3)
            continue
        if text.startswith("#|", index):
            end = _nested_end(text, index, "#|", "|#")
            if end is None:
                break
            ranges.append((index, end))
            index = end
            continue
        if text[index] == "#":
            end = _line_end(text, index + 1)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def rez_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return contemporary Rez comments after preprocessor line splicing."""

    return _logical_c_comment_ranges(text, raw_strings=False)


def _roc_literal_end(text: str, start: int) -> int:
    if text.startswith('"""', start):
        return _quoted_end(text, start, '"""', multiline=True)[0]
    return _quoted_end(text, start, text[start])[0]


def roc_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Roc hash comments outside string and code-point literals."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] in {'"', "'"}:
            index = _roc_literal_end(text, index)
            continue
        if text[index] == "#":
            end = _line_end(text, index + 1)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def coq_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Coq/Rocq nested blocks with comment-internal quote shielding."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] == '"':
            index, _ = _quoted_end(text, index, '"', multiline=True, doubled=True)
            continue
        if not text.startswith("(*", index):
            index += 1
            continue

        start = index
        depth = 1
        index += 2
        complete = False
        while index < len(text):
            if text[index] == '"':
                index, closed = _quoted_end(
                    text,
                    index,
                    '"',
                    multiline=True,
                    doubled=True,
                )
                if not closed:
                    index = len(text)
                    break
                continue
            if text.startswith("(*", index):
                depth += 1
                index += 2
                continue
            if text.startswith("*)", index):
                depth -= 1
                index += 2
                if depth == 0:
                    ranges.append((start, index))
                    complete = True
                    break
                continue
            index += 1
        if not complete:
            break
    return tuple(ranges)


_OCAML_CHAR_LITERAL = re.compile(r"'(?:\\(?:[0-9]{3}|x[0-9a-fA-F]{2}|o[0-7]{3}|.)|[^'\\\r\n])'")
_FSHARP_CHAR_LITERAL = re.compile(
    r"'(?:\\(?:[0-9]{3}|x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|.)|[^'\\\r\n])'"
)
_FSHARP_TRIPLE_QUOTE = '"' * 3


# OCaml 4.02 lexer.mll: "{" lowercase* "|" opens a quoted string that ends at
# "|" delim "}"; it is lexed inside comments too.
_OCAML_QUOTED_STRING = re.compile(r"\{([a-z_]*)\|")
# OCaml 4.11 lexer.mll adds quoted extensions {%ext|...|} and {%%ext id|...|id}.
_OCAML_QUOTED_EXTENSION = re.compile(
    r"\{(?:%%?[A-Za-z_'0-9]+(?:\.[A-Za-z_'0-9]+)*[ \t]*)?([a-z_]*)\|"
)


def _ocaml_quoted_end(text: str, index: int, opener: re.Pattern[str]) -> Optional[int]:
    opened = opener.match(text, index)
    if opened is None:
        return None
    closer = "|" + opened.group(1) + "}"
    end = text.find(closer, opened.end())
    return len(text) if end == -1 else end + len(closer)


def _ocaml_401_literal_end(text: str, index: int) -> Optional[int]:
    char_literal = _OCAML_CHAR_LITERAL.match(text, index)
    if char_literal is not None:
        return char_literal.end()
    if text[index] == '"':
        return _quoted_end(text, index, '"', multiline=True)[0]
    return None


def _ocaml_402_literal_end(text: str, index: int) -> Optional[int]:
    end = _ocaml_401_literal_end(text, index)
    if end is None and text[index] == "{":
        end = _ocaml_quoted_end(text, index, _OCAML_QUOTED_STRING)
    return end


def _ocaml_literal_end(text: str, index: int) -> Optional[int]:
    end = _ocaml_401_literal_end(text, index)
    if end is None and text[index] == "{":
        end = _ocaml_quoted_end(text, index, _OCAML_QUOTED_EXTENSION)
    return end


def _fsharp_literal_end(text: str, index: int) -> Optional[int]:
    if text.startswith(_FSHARP_TRIPLE_QUOTE, index):
        end = text.find(_FSHARP_TRIPLE_QUOTE, index + 3)
        return len(text) if end == -1 else end + 3
    if text.startswith('@"', index):
        # Verbatim strings have no backslash escapes; "" is a literal quote.
        closer = index + 2
        while True:
            closer = text.find('"', closer)
            if closer == -1:
                return len(text)
            if text.startswith('""', closer):
                closer += 2
                continue
            return closer + 1
    char_literal = _FSHARP_CHAR_LITERAL.match(text, index)
    if char_literal is not None:
        return char_literal.end()
    if text[index] == '"':
        return _quoted_end(text, index, '"', multiline=True)[0]
    return None


def _ml_comment_ranges(
    text: str,
    literal_end: Callable[[str, int], Optional[int]],
    *,
    line_comments: bool = False,
) -> tuple[tuple[int, int], ...]:
    """Return nested ``(* *)`` comments, lexing literals inside comments too."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if line_comments and text.startswith("//", index):
            while index < len(text) and text[index] not in "\r\n":
                index += 1
            continue
        end = literal_end(text, index)
        if end is not None:
            index = end
            continue
        if line_comments and text.startswith("(*)", index):
            index += 3
            continue
        if not text.startswith("(*", index):
            index += 1
            continue

        start = index
        depth = 1
        index += 2
        complete = False
        while index < len(text):
            if text[index] in "\"'{" or text.startswith('@"', index):
                end = literal_end(text, index)
                if end is not None:
                    if end >= len(text) and not text.endswith('"', 0, end):
                        index = len(text)
                        break
                    index = end
                    continue
            if text.startswith("(*", index):
                depth += 1
                index += 2
                continue
            if text.startswith("*)", index):
                depth -= 1
                index += 2
                if depth == 0:
                    ranges.append((start, index))
                    complete = True
                    break
                continue
            index += 1
        if not complete:
            break
    return tuple(ranges)


def ocaml_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return OCaml nested comments, lexing string literals inside comments.

    The OCaml lexer recognizes string and character literals within comments,
    so ``(* "*)" *)`` is one comment. Strings use backslash escapes and may
    span lines. From OCaml 4.11, quoted strings ``{id|...|id}`` and quoted
    extensions ``{%ext|...|}`` are lexed in and outside comments.
    """

    return _ml_comment_ranges(text, _ocaml_literal_end)


def ocaml_402_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return OCaml 4.02-4.10 comments: quoted strings, no quoted extensions."""

    return _ml_comment_ranges(text, _ocaml_402_literal_end)


def ocaml_401_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return OCaml 4.01 comments: only "..." and character literals are lexed."""

    return _ml_comment_ranges(text, _ocaml_401_literal_end)


def fsharp_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return F# block comments, lexing string literals inside comments.

    F# spec 3.2: strings embedded in block comments are tokenized, so
    ``(* "*)" *)`` is one comment. ``//`` line comments and the ``(*)``
    operator token do not open a block comment.
    """

    return _ml_comment_ranges(text, _fsharp_literal_end, line_comments=True)


def rbs_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return standalone RBS hash comments outside annotations and literals."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text[index] in {'"', "'", "`"}:
            end, _ = _quoted_end(text, index, text[index])
            index = end
            continue
        if text.startswith("%a", index) and index + 2 < len(text):
            closer = _RBS_ANNOTATION_CLOSERS.get(text[index + 2])
            if closer is not None:
                annotation_end = _line_end(text, index + 3, "\n")
                cursor = index + 3
                while cursor < annotation_end:
                    if text[cursor] == "\\":
                        cursor = min(cursor + 2, annotation_end)
                        continue
                    if text[cursor] == closer:
                        cursor += 1
                        break
                    cursor += 1
                index = cursor if cursor <= annotation_end else annotation_end
                continue
        if text[index] == "#":
            end = _line_end(text, index + 1, "\n")
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _ron_literal_end(text: str, start: int) -> int | None:
    raw_end = _rust_raw_end(text, start)
    if raw_end is not None:
        return raw_end
    if text[start] in {'"', "'"}:
        return _quoted_end(text, start, text[start])[0]
    if text.startswith(('b"', "b'"), start):
        return _quoted_end(text, start + 1, text[start + 1])[0]
    return None


def ron_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return strict RON comments; line comments require a following LF."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        literal_end = _ron_literal_end(text, index)
        if literal_end is not None:
            index = literal_end
            continue
        if text.startswith("//", index):
            end = text.find("\n", index + 2)
            if end < 0:
                break
            ranges.append((index, end))
            index = end + 1
            continue
        if text.startswith("/*", index):
            end = _nested_end(text, index, "/*", "*/")
            if end is None:
                break
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def _sail_attribute_end(text: str, start: int) -> int:
    depth = 0
    index = start
    while index < len(text):
        if text[index] == "[":
            depth += 1
        elif text[index] == "]":
            depth -= 1
            if depth == 0:
                return index + 1
        index += 1
    return len(text)


def _sail_block_end(text: str, start: int) -> int | None:
    return _nested_end(text, start, "/*", "*/")


def _sail_pragma_ranges(text: str, start: int) -> tuple[int, list[tuple[int, int]], bool]:
    """Scan one simple Sail pragma, requiring its terminating LF."""

    ranges: list[tuple[int, int]] = []
    index = start
    after_block = False
    while index < len(text):
        if text[index] == "\n":
            return index + 1, ranges, True
        if text.startswith("//", index):
            end = text.find("\n", index + 2)
            if end < 0:
                return len(text), [], False
            ranges.append((index, end))
            return end + 1, ranges, True
        if text.startswith("/*", index):
            end = _sail_block_end(text, index)
            if end is None:
                return len(text), [], False
            ranges.append((index, end))
            after_block = True
            index = end
            continue
        if after_block and text[index] not in " \t\r":
            end = text.find("\n", index)
            return (len(text) if end < 0 else end + 1), [], end >= 0
        index += 1
    return len(text), [], False


def sail_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Sail comments in normal and simple-pragma lexer states."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith('"""', index):
            index, _ = _quoted_end(text, index, '"""', multiline=True)
            continue
        if text[index] == '"':
            index, _ = _quoted_end(text, index, '"', multiline=True)
            continue
        if text.startswith("$[", index):
            identifier = _SAIL_IDENTIFIER.match(text, index + 2)
            if identifier is not None:
                index = _sail_attribute_end(text, index + 1)
                continue
        if text[index] == "$":
            identifier = _SAIL_IDENTIFIER.match(text, index + 1)
            if identifier is not None:
                cursor = identifier.end()
                while cursor < len(text) and text[cursor] in " \t":
                    cursor += 1
                if cursor >= len(text) or text[cursor] != "{":
                    end, pragma_ranges, _ = _sail_pragma_ranges(text, identifier.end())
                    ranges.extend(pragma_ranges)
                    index = end
                    continue
        if text.startswith("//", index):
            end = text.find("\n", index + 2)
            if end < 0:
                break
            ranges.append((index, end))
            index = end + 1
            continue
        if text.startswith("/*", index):
            end = _sail_block_end(text, index)
            if end is None:
                break
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


_LONE_SURROGATE = re.compile("[\ud800-\udfff]")
_PYTHON_LINE_ENDING = re.compile(r"\r\n|\r|\n")


def _python_position_offset(line_starts: list[int], position: tuple[int, int]) -> int:
    row, column = position
    if row <= 0:
        return 0
    if row > len(line_starts):
        return line_starts[-1]
    return line_starts[row - 1] + column


def python_hash_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Python ``COMMENT`` token ranges with conservative error recovery."""

    # Python accepts LF, CRLF, and lone CR as physical line terminators. Reading
    # with universal newlines keeps token rows aligned with these line starts
    # and avoids a CPython tokenizer crash on a lone CR before non-ASCII text.
    line_starts = [0]
    line_starts.extend(match.end() for match in _PYTHON_LINE_ENDING.finditer(text))
    ranges: list[tuple[int, int]] = []
    error_offset = len(text) + 1
    # The C tokenizer encodes to UTF-8, so lone surrogates would raise. A
    # one-for-one replacement keeps every token offset unchanged.
    tokenizable = _LONE_SURROGATE.sub("\ufffd", text)
    try:
        tokens = tokenize.generate_tokens(io.StringIO(tokenizable, newline="").readline)
        for token in tokens:
            start = _python_position_offset(line_starts, token.start)
            if token.type == tokenize.ERRORTOKEN and token.string in {'"', "'", "\\"}:
                error_offset = min(error_offset, start)
            if token.type != tokenize.COMMENT:
                continue
            end = _python_position_offset(line_starts, token.end)
            ranges.append((start, end))
    except (IndentationError, SyntaxError, tokenize.TokenError) as exc:
        details = exc.args[1] if len(exc.args) > 1 else None
        if isinstance(details, tuple) and len(details) >= 2:
            error_offset = min(
                error_offset,
                _python_position_offset(line_starts, (details[0], details[1])),
            )
    return tuple(comment_range for comment_range in ranges if comment_range[0] < error_offset)


def scenic_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Python-tokenized comments in Scenic source."""

    return python_hash_comment_ranges(text)


def slang_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Slang comments after escaped physical line breaks are removed."""

    return _logical_c_comment_ranges(text, raw_strings=True)


def _slint_string_segment(
    text: str,
    start: int,
    *,
    continuation: bool,
) -> tuple[int, str]:
    """Scan one Slint string segment and report close/interpolation/error."""

    index = start + 1
    while index < len(text):
        if text[index] == '"':
            return index + 1, "closed"
        if text.startswith("\\{", index):
            return index + 2, "interpolation"
        if text[index] == "\\":
            index = min(index + 2, len(text))
            continue
        index += 1
    return len(text), "error"


def slint_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Slint comments while re-entering code in string interpolation."""

    ranges: list[tuple[int, int]] = []
    interpolation_depths: list[int] = []
    interpolation_checkpoint: int | None = None
    index = 0
    while index < len(text):
        if interpolation_depths and text[index] == "{":
            interpolation_depths[-1] += 1
            index += 1
            continue
        if interpolation_depths and text[index] == "}":
            if interpolation_depths[-1]:
                interpolation_depths[-1] -= 1
                index += 1
                continue
            interpolation_depths.pop()
            index, result = _slint_string_segment(text, index, continuation=True)
            if result == "interpolation":
                interpolation_depths.append(0)
            elif result == "error":
                break
            elif not interpolation_depths:
                interpolation_checkpoint = None
            continue
        if text[index] == '"':
            index, result = _slint_string_segment(text, index, continuation=False)
            if result == "interpolation":
                if not interpolation_depths:
                    interpolation_checkpoint = len(ranges)
                interpolation_depths.append(0)
            elif result == "error":
                break
            continue
        if text.startswith("//", index):
            end = _line_end(text, index + 2)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            end = _nested_end(text, index, "/*", "*/")
            if end is None:
                break
            ranges.append((index, end))
            index = end
            continue
        index += 1
    if interpolation_depths and interpolation_checkpoint is not None:
        del ranges[interpolation_checkpoint:]
    return tuple(ranges)


def smithy_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Smithy slash comments outside strings and text blocks."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith('"""', index):
            index, _ = _quoted_end(text, index, '"""', multiline=True)
            continue
        if text[index] == '"':
            index, _ = _quoted_end(text, index, '"')
            continue
        if text.startswith("//", index):
            end = _line_end(text, index + 2)
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def snakemake_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Python-tokenized comments in Snakemake source."""

    return python_hash_comment_ranges(text)


def _survex_character_values(raw: str) -> set[str] | None:
    values: set[str] = set()
    index = 0
    while index < len(raw):
        if raw[index].isspace():
            index += 1
            continue
        if (
            raw[index : index + 1].lower() == "x"
            and index + 2 < len(raw)
            and re.fullmatch(r"[0-9A-Fa-f]{2}", raw[index + 1 : index + 3])
        ):
            value = chr(int(raw[index + 1 : index + 3], 16))
            index += 3
        else:
            value = raw[index]
            index += 1
        if value.isalnum() or ord(value) > 0x7F:
            return None
        values.add(value)
    return values or None


def _survex_record_end(text: str, start: int, eol_chars: set[str]) -> int:
    index = start
    while index < len(text) and text[index] not in eol_chars:
        index += 1
    return index


def _survex_comment_start(
    record: str,
    comment_chars: set[str],
    quote_chars: set[str],
) -> int | None:
    quote = ""
    for index, char in enumerate(record):
        if quote:
            if char == quote:
                quote = ""
            continue
        if char in quote_chars:
            quote = char
            continue
        if char in comment_chars:
            return index
    return None


def survex_data_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return Survex comments while tracking scoped translation classes."""

    ranges: list[tuple[int, int]] = []
    comment_chars = {";"}
    eol_chars = {"\r", "\n", "\x1a"}
    quote_chars = {'"'}
    scopes: list[tuple[set[str], set[str], set[str]]] = []
    index = 0
    while index < len(text):
        end = _survex_record_end(text, index, eol_chars)
        record = text[index:end]
        marker = _survex_comment_start(record, comment_chars, quote_chars)
        code = record if marker is None else record[:marker]
        if marker is not None:
            ranges.append((index + marker, end))

        stripped = code.strip()
        lowered = stripped.lower()
        if lowered == "*begin" or lowered.startswith("*begin "):
            scopes.append((set(comment_chars), set(eol_chars), set(quote_chars)))
        elif lowered == "*end" or lowered.startswith("*end "):
            if scopes:
                comment_chars, eol_chars, quote_chars = scopes.pop()
        else:
            setting = _SURVEX_SET.match(code)
            if setting is not None:
                values = _survex_character_values(setting.group(2))
                if values is not None:
                    kind = setting.group(1).lower()
                    if kind == "comment":
                        comment_chars = values
                        eol_chars -= values
                        quote_chars -= values
                    elif kind == "eol":
                        eol_chars = values
                        comment_chars -= values
                        quote_chars -= values
                    else:
                        quote_chars = values
                        comment_chars -= values
                        eol_chars -= values

        if end == len(text):
            break
        if text.startswith("\r\n", end) and "\r" in eol_chars and "\n" in eol_chars:
            index = end + 2
        else:
            index = end + 1
    return tuple(ranges)


def _skip_html_tag(text: str, start: int) -> int:
    quote = ""
    index = start + 1
    while index < len(text):
        char = text[index]
        if quote:
            if char == quote:
                quote = ""
            index += 1
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == ">":
            return index + 1
        index += 1
    return len(text)


def _templ_raw_element_end(text: str, start: int, name: str) -> int:
    open_end = _skip_html_tag(text, start)
    close = re.search(rf"(?is)</\s*{name}\s*>", text[open_end:])
    return len(text) if close is None else open_end + close.end()


def _go_code_comment_ranges(
    text: str,
    start: int,
    end: int,
) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    index = start
    while index < end:
        raw_end = _rust_raw_end(text, index) if text.startswith("r", index) else None
        if raw_end is not None:
            index = min(raw_end, end)
            continue
        if text[index] in {'"', "'", "`"}:
            if text[index] == "`":
                close = text.find("`", index + 1, end)
                index = end if close < 0 else close + 1
            else:
                index = min(_quoted_end(text, index, text[index])[0], end)
            continue
        if text.startswith("//", index):
            comment_end = min(_line_end(text, index + 2), end)
            ranges.append((index, comment_end))
            index = comment_end
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2, end)
            if close < 0:
                return ranges
            comment_end = close + 2
            ranges.append((index, comment_end))
            index = comment_end
            continue
        index += 1
    return ranges


def templ_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return templ Go and HTML comment nodes across parser modes."""

    ranges: list[tuple[int, int]] = []
    index = 0
    template_depth = 0
    line_start = 0
    while index < len(text):
        if text[index] in _CR_LF:
            if text.startswith("\r\n", index):
                index += 2
            else:
                index += 1
            line_start = index
            continue

        if template_depth and text[index] == "<":
            raw = re.match(r"(?is)<\s*(script|style)(?=[\s>])", text[index:])
            if raw is not None:
                index = _templ_raw_element_end(text, index, raw.group(1))
                continue
            if text.startswith("<!--", index):
                close = text.find("-->", index + 4)
                if close < 0:
                    break
                if "--" not in text[index + 4 : close]:
                    end = close + 3
                    ranges.append((index, end))
                    index = end
                    continue
            index = _skip_html_tag(text, index)
            continue

        if text[index] in {'"', "'", "`"}:
            if text[index] == "`":
                close = text.find("`", index + 1)
                index = len(text) if close < 0 else close + 1
            else:
                index = _quoted_end(text, index, text[index])[0]
            continue

        if template_depth and text[index] == "{":
            depth = 1
            cursor = index + 1
            while cursor < len(text) and depth:
                if text[cursor] in {'"', "'", "`"}:
                    if text[cursor] == "`":
                        close = text.find("`", cursor + 1)
                        cursor = len(text) if close < 0 else close + 1
                    else:
                        cursor = _quoted_end(text, cursor, text[cursor])[0]
                    continue
                if text.startswith("//", cursor):
                    cursor = _line_end(text, cursor + 2)
                    continue
                if text.startswith("/*", cursor):
                    close = text.find("*/", cursor + 2)
                    if close < 0:
                        cursor = len(text)
                        break
                    cursor = close + 2
                    continue
                if text[cursor] == "{":
                    depth += 1
                elif text[cursor] == "}":
                    depth -= 1
                cursor += 1
            if depth:
                break
            ranges.extend(_go_code_comment_ranges(text, index + 1, cursor - 1))
            index = cursor
            continue

        line_prefix_is_space = text[line_start:index].strip() == ""
        if text.startswith("//", index) and (not template_depth or line_prefix_is_space):
            end = _line_end(text, index + 2)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index) and (not template_depth or line_prefix_is_space):
            close = text.find("*/", index + 2)
            if close < 0:
                break
            end = close + 2
            ranges.append((index, end))
            index = end
            continue

        declaration = re.match(r"\btempl\b[^\r\n{]*\{", text[index:])
        if not template_depth and declaration is not None:
            template_depth = 1
            index += declaration.end()
            continue
        if template_depth and text[index] == "}":
            template_depth -= 1
        index += 1
    return tuple(sorted(ranges))


def _hcl_string_end(text: str, start: int) -> int:
    return _quoted_end(text, start, '"', multiline=True)[0]


def _terraform_expression_ranges(
    text: str,
    start: int,
) -> tuple[int, list[tuple[int, int]], bool]:
    ranges: list[tuple[int, int]] = []
    depth = 1
    index = start
    while index < len(text):
        if text[index] == '"':
            index = _hcl_string_end(text, index)
            continue
        if text.startswith("//", index) or text[index] == "#":
            end = _line_end(text, index + (2 if text.startswith("//", index) else 1))
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            if close < 0:
                return len(text), [], False
            end = close + 2
            ranges.append((index, end))
            index = end
            continue
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index + 1, ranges, True
        index += 1
    return len(text), [], False


def terraform_template_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return HCL comments only inside standalone-template code modes."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith(("$${", "%%{"), index):
            index += 3
            continue
        if text.startswith(("${", "%{"), index):
            end, expression_ranges, complete = _terraform_expression_ranges(text, index + 2)
            if complete:
                ranges.extend(expression_ranges)
            index = end
            continue
        index += 1
    return tuple(ranges)


def _plain_slash_alias_ranges(
    text: str,
    *,
    nested: bool,
    line_endings: str,
    line_requires_lf: bool = False,
    trim_cr_before_lf: bool = False,
) -> tuple[tuple[int, int], ...]:
    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        raw_end = _rust_raw_end(text, index)
        if raw_end is not None:
            index = raw_end
            continue
        if text[index] in {'"', "'"}:
            index = _quoted_end(text, index, text[index])[0]
            continue
        if text.startswith("//", index):
            if line_requires_lf:
                lf = text.find("\n", index + 2)
                if lf < 0:
                    end = len(text)
                else:
                    end = (
                        lf - 1 if trim_cr_before_lf and lf > index and text[lf - 1] == "\r" else lf
                    )
            else:
                end = _line_end(text, index + 2, line_endings)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            if nested:
                end = _nested_end(text, index, "/*", "*/")
            else:
                close = text.find("*/", index + 2)
                end = None if close < 0 else close + 2
            if end is None:
                break
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return tuple(ranges)


def reviewed_batch_08_09_alias_comment_ranges(
    language: str,
    text: str,
) -> tuple[tuple[int, int], ...] | None:
    """Return exact lexical ranges for reviewed aliases, if applicable."""

    normalized = re.sub(r"[^a-z0-9]+", "_", language.strip().lower()).strip("_")
    if normalized == "sway":
        return _plain_slash_alias_ranges(
            text,
            nested=True,
            line_endings="\n",
            line_requires_lf=True,
            trim_cr_before_lf=True,
        )
    if normalized == "tact":
        return _plain_slash_alias_ranges(text, nested=False, line_endings=_CR_LF)
    return None


STACK_V3_BATCH_08_09_CONTEXTUAL_EXTRACTORS: dict[
    str,
    Callable[[str], tuple[tuple[int, int], ...]],
] = {
    "ocaml_401_comments": ocaml_401_comment_ranges,
    "ocaml_402_comments": ocaml_402_comment_ranges,
    "pyret_comments": pyret_comment_ranges,
    "rbs_comments": rbs_comment_ranges,
    "rez_comments": rez_comment_ranges,
    "roc_comments": roc_comment_ranges,
    "ron_comments": ron_comment_ranges,
    "sail_comments": sail_comment_ranges,
    "scenic_comments": scenic_comment_ranges,
    "slang_comments": slang_comment_ranges,
    "slint_comments": slint_comment_ranges,
    "smithy_comments": smithy_comment_ranges,
    "snakemake_comments": snakemake_comment_ranges,
    "survex_data_comments": survex_data_comment_ranges,
    "templ_comments": templ_comment_ranges,
    "terraform_template_comments": terraform_template_comment_ranges,
}

__all__ = [
    "STACK_V3_BATCH_08_09_CONTEXTUAL_EXTRACTORS",
    "coq_comment_ranges",
    "fsharp_comment_ranges",
    "ocaml_401_comment_ranges",
    "ocaml_402_comment_ranges",
    "ocaml_comment_ranges",
    "pyret_comment_ranges",
    "rbs_comment_ranges",
    "reviewed_batch_08_09_alias_comment_ranges",
    "rez_comment_ranges",
    "roc_comment_ranges",
    "ron_comment_ranges",
    "sail_comment_ranges",
    "scenic_comment_ranges",
    "slang_comment_ranges",
    "slint_comment_ranges",
    "smithy_comment_ranges",
    "snakemake_comment_ranges",
    "survex_data_comment_ranges",
    "templ_comment_ranges",
    "terraform_template_comment_ranges",
]
