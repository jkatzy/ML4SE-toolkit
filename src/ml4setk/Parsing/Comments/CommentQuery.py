"""Registry-backed comment extraction queries.

Language-specific comment syntax belongs in ``registry.py``. The query classes
in this module are responsible only for matching, grouping, deduplicating, and
returning the normalized ``QueryMatch(prefix, suffix, match)`` contract.
"""

import warnings
from bisect import bisect_right
from collections.abc import Iterable
from functools import lru_cache

import regex as re

from ..Query import Query, QueryMatch
from .contextual import contextual_comment_ranges
from .lexical import lexical_rules_for
from .registry import get_comment_syntax
from .stack_v3_batch_02_03_contextual import reviewed_alias_comment_ranges
from .stack_v3_batch_04_contextual import (
    ispc_ignored_ranges,
    kerboscript_literal_ranges,
    koka_literal_ranges,
    lean_ignored_ranges,
)
from .stack_v3_batch_05_contextual import luau_string_ranges, minizinc_string_ranges
from .stack_v3_batch_06_07_contextual import (
    reviewed_batch_06_07_alias_comment_ranges,
    rust_noir_literal_ranges,
)
from .stack_v3_batch_08_09_contextual import (
    coq_comment_ranges,
    fsharp_comment_ranges,
    ocaml_comment_ranges,
    reviewed_batch_08_09_alias_comment_ranges,
)
from .stack_v3_batch_11 import lua_long_bracket_string_ranges
from .stack_v3_contextual import b4x_string_ranges, carbon_string_ranges

_WARNED_LANGUAGE_CAVEATS = set()
_RANGE_END_SENTINEL = float("inf")
_JSON_STRING_AWARE_LANGUAGES = {"jsonc"}
_ECERE_STRING_AWARE_LANGUAGES = {"ecere_projects"}
_POGOSCRIPT_STRING_AWARE_LANGUAGES = {"pogoscript"}
_RDF_IRI_AWARE_LANGUAGES = {"sparql", "turtle"}
_SMALLTALK_STRING_AWARE_LANGUAGES = {"smalltalk"}
_NO_ADJACENT_LINE_GROUPING_LANGUAGES = {"java_template_engine", "jte"}
# Nested-comment scanners for languages that lex literals inside comments.
_NESTED_COMMENT_SCANNERS = {
    "coq": coq_comment_ranges,
    "f": fsharp_comment_ranges,
    "f_sharp": fsharp_comment_ranges,
    "fsharp": fsharp_comment_ranges,
    "ocaml": ocaml_comment_ranges,
    "rocq": coq_comment_ranges,
    "rocq_prover": coq_comment_ranges,
}
_GENERO_FORMS_LAYOUT_OPEN = re.compile(
    r"(?im)^[ \t]*(?:screen|grid|table|tree)\b[^\{\r\n]*"
    r"(?:(?:\r\n|[\r\n\u0085\u2028\u2029])[ \t]*)*"
    r"(?P<open>\{)"
)
_GENERO_DEFINE_DIRECTIVE = re.compile(r"(?im)^[ \t]*&[ \t]*define\b[^\r\n]*")
_NL_RAW_RECORD = re.compile(r"(?m)^h[ \t\v\f\r]*([0-9]+):")
_NL_BINARY_HEADER = re.compile(
    r"^b(?:"
    r"[ \t\v\f\r]*[0-9]+(?=[ \t\v\f\r\n]|\Z)"
    r"|[ \t\v\f\r]*(?=\n|\Z)"
    r")"
)
_NL_HEADER_REQUIRED_UINTS = (3, 2, 2, 2, 2, 2, 2, 2, 5)
_NL_C_WHITESPACE = " \t\v\f\r"
_PHYSICAL_LINE_ENDINGS = "\r\n\u0085\u2028\u2029"


def _warn_language_caveat_once(language):
    """Warn once for intentionally narrow language support.

    Args:
        language: Registry language key requested by the caller.
    """

    normalized = language.lower()
    if normalized != "promela" or normalized in _WARNED_LANGUAGE_CAVEATS:
        return

    warnings.warn(
        "Promela parsing only supports native /* ... */ comments. "
        "// comments are preprocessor-dependent in Spin and are intentionally "
        "not parsed by this registry entry.",
        UserWarning,
        stacklevel=3,
    )
    _WARNED_LANGUAGE_CAVEATS.add(normalized)


def _quoted_string_ranges(text):
    """Return simple single-line quoted string ranges.

    Args:
        text: Source text to scan.

    Returns:
        A list of ``(start, end)`` ranges for single, double, and backtick
        strings. The scanner is deliberately lightweight; it prevents obvious
        false positives for comment markers in strings without attempting to
        parse language-specific lexical rules.
    """

    if "'" not in text and '"' not in text and "`" not in text:
        return []

    ranges = []
    quote = None
    start = None
    escaped = False

    for index, char in enumerate(text):
        if quote is None:
            if char in {"'", '"', "`"}:
                quote = char
                start = index
                escaped = False
            continue

        if char in {"\n", "\r"}:
            quote = None
            start = None
            escaped = False
            continue

        if char == "\\" and not escaped:
            escaped = True
            continue

        if char == quote and not escaped:
            ranges.append((start, index + 1))
            quote = None
            start = None
            escaped = False
            continue

        escaped = False

    return ranges


def _rdf_iri_ranges(text):
    """Return complete SPARQL/Turtle IRIREF ranges."""

    ranges = []
    search_from = 0
    text_length = len(text)
    forbidden = frozenset('<"{}|^`')
    hex_digits = frozenset("0123456789abcdefABCDEF")
    while search_from < text_length:
        start = text.find("<", search_from)
        if start < 0:
            break

        index = start + 1
        while index < text_length:
            char = text[index]
            if char == ">":
                ranges.append((start, index + 1))
                search_from = index + 1
                break
            if char == "\\":
                escape_marker = text[index + 1 : index + 2]
                escape_width = {"u": 4, "U": 8}.get(escape_marker)
                escape_end = index + 2 + (escape_width or 0)
                escaped_digits = text[index + 2 : escape_end]
                if (
                    escape_width is None
                    or len(escaped_digits) != escape_width
                    or any(digit not in hex_digits for digit in escaped_digits)
                ):
                    search_from = start + 1
                    break
                code_point = int(escaped_digits, 16)
                if code_point > 0x10FFFF or 0xD800 <= code_point <= 0xDFFF:
                    search_from = start + 1
                    break
                index = escape_end
                continue
            if char in forbidden or ord(char) <= 0x20:
                search_from = start + 1
                break
            index += 1
        else:
            break

    return ranges


def _smalltalk_literal_ranges(text):
    """Return Smalltalk string and character literal ranges.

    Smalltalk single-quoted strings may cross physical lines and escape an
    apostrophe by doubling it. Paired double quotes are comments, so the
    scanner skips them while looking for literals.
    """

    ranges = []
    index = 0
    text_length = len(text)
    while index < text_length:
        if text[index] == "$" and index + 1 < text_length:
            ranges.append((index, index + 2))
            index += 2
            continue

        if text[index] == '"':
            comment_end = text.find('"', index + 1)
            if comment_end == -1:
                break
            index = comment_end + 1
            continue

        if text[index] != "'":
            index += 1
            continue

        start = index
        index += 1
        while index < text_length:
            if text[index] != "'":
                index += 1
                continue
            if index + 1 < text_length and text[index + 1] == "'":
                index += 2
                continue
            index += 1
            break
        ranges.append((start, index))

    return ranges


def _tcsh_initial_hashbang_range(text):
    """Return a protected range for a tcsh interpreter directive at byte zero."""

    if not text.startswith("#!"):
        return []

    line_ending = re.search(r"\r\n|[\r\n\u0085\u2028\u2029]", text)
    line_end = len(text) if line_ending is None else line_ending.end()
    # The comment delimiter starts at zero. A -1 sentinel keeps it strictly
    # inside the protected range without changing quote-range boundary rules.
    return [(-1, line_end)]


def _genero_forms_layout_ranges(text):
    """Return complete Genero Forms layout bodies introduced by known headers."""

    ranges = []
    for match in _GENERO_FORMS_LAYOUT_OPEN.finditer(text):
        close_match = re.search(
            r"(?m)^[ \t]*\}",
            text,
            pos=match.end("open"),
        )
        range_end = len(text) if close_match is None else close_match.end()
        ranges.append((match.start(), range_end))
    return ranges


def _merge_ignored_ranges(ranges):
    """Return sorted overlapping protected ranges as disjoint spans."""

    merged = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def _json_string_ranges(text):
    """Return JSON double-quoted string ranges, including unterminated values."""

    if '"' not in text:
        return []

    ranges = []
    index = 0
    text_length = len(text)

    while index < text_length:
        if text.startswith("//", index):
            index += 2
            while index < text_length and text[index] not in "\r\n":
                index += 1
            continue

        if text.startswith("/*", index):
            block_end = text.find("*/", index + 2)
            index = text_length if block_end == -1 else block_end + 2
            continue

        if text[index] != '"':
            index += 1
            continue

        start = index
        index += 1
        escaped = False
        while index < text_length:
            char = text[index]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                index += 1
                break
            index += 1

        ranges.append((start, index))

    return ranges


def _c_style_double_quoted_string_ranges(text):
    """Return ECON-style double-quoted ranges while skipping real comments."""

    ranges = []
    index = 0
    text_length = len(text)

    while index < text_length:
        if text.startswith("//", index):
            line_end = index + 2
            while line_end < text_length and text[line_end] not in "\r\n":
                line_end += 1
            index = line_end
            continue

        if text.startswith("/*", index):
            block_end = text.find("*/", index + 2)
            index = text_length if block_end == -1 else block_end + 2
            continue

        if text[index] != '"':
            index += 1
            continue

        start = index
        index += 1
        while index < text_length:
            if text[index] == "\\":
                index = min(index + 2, text_length)
                continue
            if text[index] == '"':
                index += 1
                break
            index += 1
        ranges.append((start, index))

    return ranges


def _pogoscript_string_ranges(text):
    """Return PogoScript string and regexp ranges outside interpolation code."""

    ranges = []
    text_length = len(text)

    def skip_line_comment(index):
        index += 2
        while index < text_length and text[index] not in "\r\n":
            index += 1
        return index

    def skip_block_comment(index):
        block_end = text.find("*/", index + 2)
        return text_length if block_end == -1 else block_end + 2

    def is_identifier_start(char):
        return (
            char.isascii()
            and char.isalpha()
            or "\u3400" <= char <= "\u4dff"
            or "\u4e00" <= char <= "\u9fff"
            or char in {"_", "$"}
        )

    def is_identifier_tail(char):
        return is_identifier_start(char) or "0" <= char <= "9"

    def preceding_token_is_identifier(index):
        token_start = index
        while token_start and is_identifier_tail(text[token_start - 1]):
            token_start -= 1

        token_text = text[token_start:index]
        token_index = 0
        last_kind = None
        while token_index < len(token_text):
            if "0" <= token_text[token_index] <= "9":
                if (
                    token_text.startswith("0x", token_index)
                    and token_index + 2 < len(token_text)
                    and token_text[token_index + 2] in "0123456789abcdefABCDEF"
                ):
                    token_index += 2
                    while (
                        token_index < len(token_text)
                        and token_text[token_index] in "0123456789abcdefABCDEF"
                    ):
                        token_index += 1
                else:
                    while token_index < len(token_text) and "0" <= token_text[token_index] <= "9":
                        token_index += 1
                last_kind = "number"
                continue

            if is_identifier_start(token_text[token_index]):
                token_index += 1
                while token_index < len(token_text) and is_identifier_tail(token_text[token_index]):
                    token_index += 1
                last_kind = "identifier"
                continue

            token_index += 1
            last_kind = None

        return last_kind == "identifier"

    def starts_regexp(index):
        return text.startswith("r/", index) and not preceding_token_is_identifier(index)

    def scan_regexp(index):
        start = index
        index += 2
        while index < text_length:
            if text[index] == "\\":
                index = min(index + 2, text_length)
                continue
            if text[index] == "/":
                index += 1
                while index < text_length and text[index] in {"i", "m", "g"}:
                    index += 1
                ranges.append((start, index))
                return index
            index += 1
        return text_length

    def scan_single_quoted(index):
        start = index
        index += 1
        while index < text_length:
            if text[index] != "'":
                index += 1
                continue
            if index + 1 < text_length and text[index + 1] == "'":
                index += 2
                continue
            index += 1
            ranges.append((start, index))
            return index
        return text_length

    def scan_interpolation(index):
        depth = 1
        while index < text_length:
            if text.startswith("//", index):
                index = skip_line_comment(index)
                continue
            if text.startswith("/*", index):
                index = skip_block_comment(index)
                continue
            if starts_regexp(index):
                index = scan_regexp(index)
                continue
            if text[index] == "'":
                index = scan_single_quoted(index)
                continue
            if text[index] == '"':
                index = scan_double_quoted(index)
                continue
            if text[index] == "(":
                depth += 1
            elif text[index] == ")":
                depth -= 1
                if depth == 0:
                    return index + 1
            index += 1
        return None

    def scan_double_quoted(index):
        checkpoint = len(ranges)
        segment_start = index
        index += 1
        while index < text_length:
            if text[index] == "\\":
                index = min(index + 2, text_length)
                continue
            if text.startswith("#(", index):
                if segment_start < index:
                    ranges.append((segment_start, index))
                interpolation_end = scan_interpolation(index + 2)
                if interpolation_end is None:
                    del ranges[checkpoint:]
                    return text_length
                segment_start = interpolation_end - 1
                index = interpolation_end
                continue
            if text[index] == '"':
                index += 1
                ranges.append((segment_start, index))
                return index
            index += 1

        del ranges[checkpoint:]
        return text_length

    index = 0
    while index < text_length:
        if text.startswith("//", index):
            index = skip_line_comment(index)
            continue
        if text.startswith("/*", index):
            index = skip_block_comment(index)
            continue
        if starts_regexp(index):
            index = scan_regexp(index)
            continue
        if text[index] == "'":
            index = scan_single_quoted(index)
            continue
        if text[index] == '"':
            index = scan_double_quoted(index)
            continue
        index += 1

    return sorted(ranges)


def _nl_comment_scan_context(text):
    """Return protected NL ranges and the textual scan limit."""

    scan_limit = len(text)
    binary_scan_limit = _nl_binary_header_scan_limit(text)
    if binary_scan_limit is not None:
        scan_limit = binary_scan_limit

    ranges = []
    search_from = 0
    while search_from < scan_limit:
        match = _NL_RAW_RECORD.search(text, search_from, scan_limit)
        if match is None:
            break

        digits = match.group(1)
        if len(digits) > 9:
            payload_end = scan_limit
        else:
            payload_end = _advance_utf8_bytes(text, match.end(), int(digits), scan_limit)

        record_end = payload_end
        while record_end < scan_limit and text[record_end] not in "\r\n":
            record_end += 1
        if record_end < scan_limit:
            if (
                text[record_end] == "\r"
                and record_end + 1 < scan_limit
                and text[record_end + 1] == "\n"
            ):
                record_end += 2
            else:
                record_end += 1

        ranges.append((match.start(), record_end))
        search_from = max(match.end(), record_end)

    return ranges, scan_limit


def _nl_binary_header_scan_limit(text):
    """Return the text-header boundary for a likely binary NL file."""

    if not text.startswith("b"):
        return None

    strong_prefix = _NL_BINARY_HEADER.match(text) is not None
    line_end = -1
    for _ in range(10):
        line_end = text.find("\n", line_end + 1)
        if line_end == -1:
            return 0 if strong_prefix else None

    scan_limit = line_end + 1
    if strong_prefix:
        return scan_limit

    header_lines = text[:scan_limit].split("\n")[:10]
    if all(
        _nl_line_has_unsigned_prefix(line, required)
        for line, required in zip(header_lines[1:], _NL_HEADER_REQUIRED_UINTS)
    ):
        return scan_limit
    return None


def _nl_line_has_unsigned_prefix(line, required):
    """Return whether an NL header line starts with ``required`` uints."""

    index = 0
    for field_index in range(required):
        while index < len(line) and line[index] in _NL_C_WHITESPACE:
            index += 1
        start = index
        while index < len(line) and "0" <= line[index] <= "9":
            index += 1
        if index == start:
            return False
        if field_index < required - 1 and (
            index >= len(line) or line[index] not in _NL_C_WHITESPACE
        ):
            return False
    return True


def _advance_utf8_bytes(text, start, byte_count, limit):
    """Advance over a byte-counted field represented as decoded UTF-8 text."""

    index = start
    consumed = 0
    while index < limit and consumed < byte_count:
        consumed += len(text[index].encode("utf-8", errors="surrogatepass"))
        index += 1
    return index


def _comment_scan_context(language, text):
    """Return ignored ranges and the maximum source offset to scan.

    String-like ranges are collected in one left-to-right pass that skips
    complete comments, so quote characters inside comment text never pair
    with quotes elsewhere. The interiors of regex comments are returned as
    protected ranges as well, which keeps nested-comment openers written
    inside line comments from opening a block.
    """

    normalized = re.sub(r"[^a-z0-9]+", "_", language.strip().lower()).strip("_")
    if normalized in {"circom", "linear_programming"}:
        return [], len(text)
    if normalized == "nl":
        return _nl_comment_scan_context(text)
    string_ranges = _language_string_ranges(normalized, text)
    return _comment_aware_ignored_ranges(language, text, string_ranges), len(text)


def _language_string_ranges(normalized, text):
    """Return language-specific protected ranges, or ``None`` for the default."""

    if normalized in _JSON_STRING_AWARE_LANGUAGES:
        return _json_string_ranges(text)
    if normalized in _ECERE_STRING_AWARE_LANGUAGES:
        return _c_style_double_quoted_string_ranges(text)
    if normalized in _POGOSCRIPT_STRING_AWARE_LANGUAGES:
        return _pogoscript_string_ranges(text)
    if normalized == "ispc":
        return ispc_ignored_ranges(text)
    if normalized == "kerboscript":
        return kerboscript_literal_ranges(text)
    if normalized == "koka":
        return koka_literal_ranges(text)
    if normalized in {"lean", "lean4", "lean_4"}:
        return lean_ignored_ranges(text)
    if normalized in _SMALLTALK_STRING_AWARE_LANGUAGES:
        return _smalltalk_literal_ranges(text)
    if normalized == "b4x":
        return b4x_string_ranges(text)
    if normalized == "carbon":
        return carbon_string_ranges(text)
    if normalized == "luau":
        return luau_string_ranges(text)
    if normalized in {"lua", "moonscript", "terra", "xmake"}:
        quoted_ranges = _quoted_string_ranges(text)
        return _merge_ignored_ranges(
            quoted_ranges + lua_long_bracket_string_ranges(text, quoted_ranges)
        )
    if normalized in {"minizinc", "minizinc_data"}:
        return minizinc_string_ranges(text)
    if normalized in {"noir", "rust", "sway"}:
        return rust_noir_literal_ranges(text)
    if normalized == "tcsh":
        return _merge_ignored_ranges(
            _quoted_string_ranges(text) + _tcsh_initial_hashbang_range(text)
        )
    if normalized == "genero_forms":
        return _merge_ignored_ranges(
            _quoted_string_ranges(text)
            + _genero_forms_layout_ranges(text)
            + [match.span() for match in _GENERO_DEFINE_DIRECTIVE.finditer(text)]
        )
    if normalized in _RDF_IRI_AWARE_LANGUAGES:
        return _merge_ignored_ranges(_quoted_string_ranges(text) + _rdf_iri_ranges(text))
    return None


def _scan_quoted_at(text, start):
    """Scan a simple single-line quoted string opened at ``start``.

    Returns:
        ``(end, closed)`` where ``end`` is exclusive for a closed string and
        the line-ending offset (or ``len(text)``) for an unclosed one.
    """

    quote = text[start]
    index = start + 1
    length = len(text)
    while index < length:
        char = text[index]
        if char in "\r\n":
            return index, False
        if char == "\\":
            index += 2
            continue
        if char == quote:
            return index + 1, True
        index += 1
    return length, False


def _nested_comment_end(text, start, open_delim, close_delim, memo=None):
    """Return the end of the depth-balanced comment opened at ``start``.

    ``memo`` remembers the offset after which no closer exists, so many
    unclosed openers do not each rescan to the end of the text.
    """

    memo_key = ("nested-unclosed", open_delim, close_delim)
    if memo is not None and start >= memo.get(memo_key, len(text) + 1):
        return None
    depth = 0
    search_from = start
    while True:
        open_index = text.find(open_delim, search_from)
        close_index = text.find(close_delim, search_from)
        if close_index == -1:
            # No closer exists at or after ``search_from``, so no opener
            # starting there can close either.
            if memo is not None:
                memo[memo_key] = min(memo.get(memo_key, len(text) + 1), search_from)
            return None
        if open_index != -1 and open_index <= close_index:
            depth += 1
            search_from = open_index + len(open_delim)
            continue
        depth -= 1
        search_from = close_index + len(close_delim)
        if depth == 0:
            return search_from


_LAZY_BODIES = (r"[\S\s]*?", r"[\s\S]*?")
_UNESCAPED_BACKREFERENCE = re.compile(r"(?<!\\)\\([1-9])")


def _split_lazy_block_pattern(pattern_text):
    """Split ``OPEN[\\s\\S]*?CLOSE`` into its opener and closer, if possible.

    The split is used only when the lazy body appears once at the top level,
    outside groups and character classes, with no top-level alternation, so
    searching for the opener and then the first closer is equivalent to the
    original regex.
    """

    depth = 0
    in_class = False
    index = 0
    split_at = None
    while index < len(pattern_text):
        char = pattern_text[index]
        if char == "\\":
            index += 2
            continue
        if in_class:
            if char == "]":
                in_class = False
            index += 1
            continue
        if depth == 0:
            body = next((b for b in _LAZY_BODIES if pattern_text.startswith(b, index)), None)
            if body is not None:
                if split_at is not None:
                    return None
                split_at = (index, index + len(body))
                index += len(body)
                continue
            if char == "|":
                return None
        if char == "[":
            in_class = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        index += 1
    if split_at is None or depth != 0:
        return None
    opener, closer = pattern_text[: split_at[0]], pattern_text[split_at[1] :]
    if not opener or not closer or opener.startswith("(?") and not opener.startswith("(?<"):
        return None
    return opener, closer


class _CommentPatternMatcher:
    """Search one registry comment pattern without quadratic rescans."""

    def __init__(self, pattern_text):
        self.pattern = re.compile(pattern_text)
        split = _split_lazy_block_pattern(pattern_text)
        self.opener = None if split is None else re.compile(split[0])
        self.closer_text = None if split is None else split[1]
        self.closer_has_groups = bool(
            split is not None and _UNESCAPED_BACKREFERENCE.search(split[1])
        )
        self._closers = {}

    def _closer_for(self, groups):
        key = tuple(groups)
        closer = self._closers.get(key)
        if closer is None:
            text = _UNESCAPED_BACKREFERENCE.sub(
                lambda match: re.escape(groups[int(match.group(1)) - 1] or ""),
                self.closer_text,
            )
            closer = self._closers[key] = re.compile(text)
        return closer

    def search(self, text, offset, memo):
        """Return the leftmost match span at or after ``offset``, or ``None``."""

        if self.opener is None:
            match = self.pattern.search(text, offset)
            return None if match is None else match.span()
        while True:
            opened = self.opener.search(text, offset)
            if opened is None:
                return None
            groups = opened.groups() if self.closer_has_groups else ()
            memo_key = (id(self), groups)
            if opened.end() >= memo.get(memo_key, len(text) + 1):
                if not self.closer_has_groups:
                    return None
                offset = opened.start() + 1
                continue
            closed = self._closer_for(groups).search(text, opened.end())
            if closed is not None:
                return opened.start(), closed.end()
            memo[memo_key] = min(memo.get(memo_key, len(text) + 1), opened.end())
            if not self.closer_has_groups:
                return None
            offset = opened.start() + 1


@lru_cache(maxsize=None)
def _comment_pattern_matchers(language):
    """Return search helpers for the regex comment patterns of ``language``."""

    patterns = get_comment_syntax(language).regex_patterns_for_language(language)
    return tuple(_CommentPatternMatcher(pattern) for pattern in patterns)


class _PatternCursor:
    """Find the next usable match of one comment regex at or after an offset.

    Searching lazily from the scanner position, instead of collecting every
    overlapped match up front, keeps long comments that contain their own
    opener (for example spliced ``//`` lines) linear.
    """

    def __init__(self, matcher, language, text, excluded, memo):
        self.matcher = matcher
        self.memo = memo
        self.language = language
        self.text = text
        self.excluded = excluded
        self.found = None
        self.exhausted = False

    def peek(self, offset):
        """Return the first ``(start, end)`` match starting at or after ``offset``."""

        if self.found is not None and self.found[0] >= offset:
            return self.found
        self.found = None
        while not self.exhausted:
            span = self.matcher.search(self.text, offset, self.memo)
            if span is None:
                self.exhausted = True
                break
            start, end = _adjust_language_specific_regex_range(
                self.language, self.text, span[0], span[1]
            )
            if end > start and not _starts_with_excluded_comment_prefix(
                self.text, start, self.excluded
            ):
                self.found = (start, end)
                break
            offset = span[0] + 1
        return self.found


def _comment_aware_ignored_ranges(language, text, string_ranges=None):
    """Return string and comment ranges found by one source-order pass.

    Args:
        language: Registry language key.
        text: Source text to scan.
        string_ranges: Precomputed language-specific protected ranges, or
            ``None`` to scan simple single-line quoted strings in place.

    Returns:
        Sorted, disjoint ranges. A string that starts inside a complete
        comment is not a string, and a comment marker that starts inside a
        string is not a comment.
    """

    syntax = get_comment_syntax(language)
    excluded = syntax.excluded_comment_prefixes_for_language(language)
    comment_ends = {}
    memo = {}

    def add_comment(start, end):
        if end > start and not _starts_with_excluded_comment_prefix(text, start, excluded):
            comment_ends[start] = max(comment_ends.get(start, start), end)

    cursors = []
    reviewed_ranges = _reviewed_alias_ranges(language, text)
    if reviewed_ranges is not None:
        for start, end in reviewed_ranges:
            add_comment(start, end)
    else:
        cursors = [
            _PatternCursor(matcher, language, text, excluded, memo)
            for matcher in _comment_pattern_matchers(language)
        ]
        if syntax.contextual_extractor:
            for start, end in contextual_comment_ranges(syntax.contextual_extractor, text):
                add_comment(start, end)

    nested_starts = {}
    normalized = re.sub(r"[^a-z0-9]+", "_", language.strip().lower()).strip("_")
    nested_scanner = _NESTED_COMMENT_SCANNERS.get(normalized)
    if nested_scanner is not None:
        for start, end in nested_scanner(text):
            comment_ends[start] = max(comment_ends.get(start, start), end)
    for open_delim, close_delim in () if nested_scanner else syntax.nested_delimiters:
        index = text.find(open_delim)
        while index != -1:
            nested_starts.setdefault(index, []).append((open_delim, close_delim))
            index = text.find(open_delim, index + 1)

    rules = lexical_rules_for(language)
    if string_ranges is None:
        string_starts = None
        candidate_chars = rules.quote_chars | rules.literal_start_chars
        quote_positions = [index for index, char in enumerate(text) if char in candidate_chars]
    else:
        string_starts = {}
        for start, end in string_ranges:
            string_starts[start] = max(string_starts.get(start, start), end)
        quote_positions = list(string_starts)

    events = sorted(set(comment_ends) | set(nested_starts) | set(quote_positions))
    event_index = 0
    result = []
    # A heredoc body is protected from the line after its opener; the rest of
    # the opener's line is still scanned before the body is skipped.
    pending = None
    # Some protected ranges deliberately start at -1 to cover offset zero.
    position = float("-inf")
    scan_from = float("-inf")
    while True:
        offset = max(position, scan_from)
        while event_index < len(events) and events[event_index] < offset:
            event_index += 1
        candidates = [events[event_index]] if event_index < len(events) else []
        regex_offset = max(0, int(offset)) if offset != float("-inf") else 0
        for cursor in cursors:
            found = cursor.peek(regex_offset)
            if found is not None:
                candidates.append(found[0])
        if not candidates:
            break
        start = min(candidates)
        scan_from = start + 1
        if pending is not None and start >= pending[0]:
            if position <= pending[0]:
                result.append(pending)
                position = pending[1]
            pending = None
            if start < position:
                continue
        end = comment_ends.get(start)
        for cursor in cursors:
            found = cursor.found
            if found is not None and found[0] == start and (end is None or found[1] > end):
                end = found[1]
        for open_delim, close_delim in nested_starts.get(start, ()):
            if _starts_with_excluded_comment_prefix(text, start, excluded):
                continue
            nested_end = _nested_comment_end(text, start, open_delim, close_delim, memo)
            if nested_end is not None and (end is None or nested_end > end):
                end = nested_end
        if end is not None:
            result.append((start, end))
            position = end
            continue
        if string_starts is not None:
            if start in string_starts:
                result.append((start, string_starts[start]))
                position = string_starts[start]
            continue
        char = text[start]
        if char in rules.literal_start_chars:
            literal_range = next(
                (
                    found
                    for found in (literal.scan(text, start, memo) for literal in rules.literals)
                    if found is not None
                ),
                None,
            )
            if literal_range is not None:
                range_start, range_end = literal_range
                if range_start > start:
                    if pending is None:
                        pending = literal_range
                    continue
                result.append(literal_range)
                position = range_end
                continue
        if char not in rules.quote_chars:
            continue
        if rules.non_string_quote is not None and rules.non_string_quote.match(text, start):
            continue
        end, closed = _scan_quoted_at(text, start)
        if closed:
            result.append((start, end))
        position = end
    if pending is not None and position <= pending[0]:
        result.append(pending)
    return result


def _comment_start_ignored_ranges(language, text):
    """Return source ranges where comment delimiters should be ignored."""

    ignored_ranges, _ = _comment_scan_context(language, text)
    return ignored_ranges


def _starts_inside_ignored_range(start, ignored_ranges):
    """Return ``True`` when ``start`` is inside a protected source range."""

    if not ignored_ranges:
        return False

    index = bisect_right(ignored_ranges, (start, _RANGE_END_SENTINEL)) - 1
    if index < 0:
        return False

    range_start, range_end = ignored_ranges[index]
    return range_start < start < range_end


def _starts_with_excluded_comment_prefix(text, start, prefixes):
    """Return whether a comment-like range begins with excluded source syntax."""

    return any(text.startswith(prefix, start) for prefix in prefixes)


def _query_match_from_range(text, start, end):
    """Build a ``QueryMatch`` for a half-open source range.

    Args:
        text: The source text that produced the match.
        start: Inclusive match offset.
        end: Exclusive match offset.

    Returns:
        A normalized ``QueryMatch(prefix, suffix, match)`` value.
    """

    return QueryMatch(text[:start], text[end:], text[start:end])


def _match_range(text, match):
    """Return the half-open source range represented by ``match``.

    Args:
        text: The source text that produced the match.
        match: Query match from ``text``.

    Returns:
        ``(start, end)`` offsets for ``match.match``.
    """

    start = len(match.prefix)
    end = len(text) - len(match.suffix)
    return start, end


def _match_sort_key(text, match):
    """Return a stable source-order sort key for a ``QueryMatch``."""

    start, end = _match_range(text, match)
    return start, end


def _query_matches_from_ranges(text, ranges):
    """Build ``QueryMatch`` values from half-open source ranges."""

    return [_query_match_from_range(text, start, end) for start, end in ranges]


def _reviewed_alias_ranges(language, text):
    """Return ranges from a reviewed alias scanner, when one owns ``language``."""

    for extractor in (
        reviewed_alias_comment_ranges,
        reviewed_batch_06_07_alias_comment_ranges,
        reviewed_batch_08_09_alias_comment_ranges,
    ):
        ranges = extractor(language, text)
        if ranges is not None:
            return ranges
    return None


def _starts_with_nested_delimiter(syntax, text, start, end):
    """Return whether a classified range uses this syntax's nested opener."""

    candidate = text[start:end].lstrip()
    return any(candidate.startswith(opener) for opener, _closer in syntax.nested_delimiters)


# Languages whose lexers end a line comment at a lone CR, keyed to the line
# comment openers that the trim applies to. Python: reference 2.1.2 physical
# lines; Haskell 2010 Report 2.2 ``newline``. Lua and Terra keep their legacy
# published slices; only the newer Lua aliases end at a lone CR.
_LONE_CR_LINE_COMMENT_OPENERS = {
    "haskell": ("--",),
    "literate_haskell": ("--",),
    "luau": ("--",),
    "numpy": ("#",),
    "python": ("#",),
    "xmake": ("--",),
}


def _adjust_language_specific_regex_range(language, text, start, end):
    """End line comments at a lone CR for languages whose lexers do so."""

    normalized = re.sub(r"[^a-z0-9]+", "_", language.strip().lower()).strip("_")
    openers = _LONE_CR_LINE_COMMENT_OPENERS.get(normalized)
    if openers is None:
        return start, end

    candidate = text[start:end]
    if not candidate.startswith(openers) or re.match(r"--\[[=]*\[", candidate):
        return start, end

    carriage_return = text.find("\r", start, end)
    return (start, carriage_return) if carriage_return >= 0 else (start, end)


class LineCommentQuery(Query):
    """Extract registry regex comments for one language.

    Args:
        language: Registry language key or alias understood by
            ``get_comment_syntax``.
    """

    def __init__(self, language):
        _warn_language_caveat_once(language)
        self.language = language
        self.syntax = get_comment_syntax(language)
        self.regex_patterns = self.syntax.regex_patterns_for_language(language)
        self.regexes = tuple(re.compile(pattern) for pattern in self.regex_patterns)
        self.contextual_extractor = self.syntax.contextual_extractor
        self.excluded_comment_prefixes = self.syntax.excluded_comment_prefixes_for_language(
            language
        )

    def contains(self, string):
        """Return ``True`` when extraction finds a comment."""

        return bool(self.parse_ranges(string))

    def parse(self, text):
        """Return non-nested comment matches in source order.

        Args:
            text: Source text to scan.

        Returns:
            A list of ``QueryMatch`` values for single-line comments,
            non-nested block comments, and contextual comment regions.
            Matches starting inside protected source ranges are ignored.
        """

        return _query_matches_from_ranges(text, self.parse_ranges(text))

    def parse_ranges(self, text, quoted_ranges=None, scan_limit=None):
        """Return regex and contextual comment ranges in source order."""

        reviewed_ranges = _reviewed_alias_ranges(self.language, text)
        if reviewed_ranges is not None:
            return self._dedupe_match_ranges(
                (start, end)
                for start, end in reviewed_ranges
                if not _starts_with_nested_delimiter(self.syntax, text, start, end)
            )

        if not self.regexes and not self.contextual_extractor:
            return []

        if quoted_ranges is None or scan_limit is None:
            default_ranges, default_limit = _comment_scan_context(self.language, text)
            if quoted_ranges is None:
                quoted_ranges = default_ranges
            if scan_limit is None:
                scan_limit = default_limit

        def accept(start, end):
            return (
                end <= scan_limit
                and not _starts_inside_ignored_range(start, quoted_ranges)
                and not _starts_with_excluded_comment_prefix(
                    text,
                    start,
                    self.excluded_comment_prefixes,
                )
            )

        match_ranges = [
            _adjust_language_specific_regex_range(self.language, text, start, end)
            for start, end in self._iter_match_ranges(text, accept)
        ]
        if self.contextual_extractor:
            match_ranges.extend(contextual_comment_ranges(self.contextual_extractor, text))
        return self._dedupe_match_ranges(match_ranges)

    def _iter_match_ranges(self, text, accept=None):
        """Yield regex match ranges for all configured patterns, lazily.

        After an accepted match the search resumes at its end; after a
        rejected one it resumes one character later, so overlapping
        candidates are still found without rescanning long comments.
        """

        memo = {}
        for matcher in _comment_pattern_matchers(self.language):
            offset = 0
            while True:
                span = matcher.search(text, offset, memo)
                if span is None:
                    break
                start, end = span
                if accept is None or accept(start, end):
                    yield start, end
                    adjusted_end = _adjust_language_specific_regex_range(
                        self.language, text, start, end
                    )[1]
                    offset = max(adjusted_end, start + 1)
                else:
                    offset = start + 1

    @staticmethod
    def _dedupe_match_ranges(ranges):
        """Return non-overlapping ranges, keeping the longest match per start.

        Args:
            ranges: Iterable of half-open ``(start, end)`` offsets.

        Returns:
            Source-ordered ranges with overlaps removed. When multiple patterns
            start at the same offset, the longest match wins so outer block
            comments can contain line-comment-looking text.
        """

        deduped = {}
        for start, end in ranges:
            current_end = deduped.get(start, -1)
            if end > current_end:
                deduped[start] = end

        result = []
        current_end = -1
        for start, end in sorted(deduped.items()):
            if start < current_end:
                continue
            result.append((start, end))
            current_end = end
        return result


class NestedCommentQuery(Query):
    """Extract top-level nested comment regions for one language.

    Args:
        language: Registry language key with nested delimiter metadata.
    """

    def __init__(self, language):
        _warn_language_caveat_once(language)
        self.language = language
        self.syntax = get_comment_syntax(language)
        self.delimiters = self.syntax.nested_delimiters
        self.delimeters = self.delimiters  # Preserve the older misspelled attribute.
        self.excluded_comment_prefixes = self.syntax.excluded_comment_prefixes_for_language(
            language
        )

    def contains(self, string):
        """Return ``True`` when nested-delimiter extraction finds a comment."""

        if not self.delimiters:
            return False

        return bool(self.parse(string))

    def parse(self, text):
        """Return nested comment matches in source order.

        Args:
            text: Source text to scan.

        Returns:
            Top-level nested comment regions as ``QueryMatch`` values. Inner
            nested regions are included inside the outer match, not emitted as
            separate matches.
        """

        return _query_matches_from_ranges(text, self.parse_ranges(text))

    def parse_ranges(self, text, quoted_ranges=None):
        """Return nested comment ranges in source order."""

        if not self.delimiters:
            return []

        normalized = re.sub(r"[^a-z0-9]+", "_", self.language.strip().lower()).strip("_")
        scanner = _NESTED_COMMENT_SCANNERS.get(normalized)
        if scanner is not None:
            return list(scanner(text))

        if quoted_ranges is None:
            quoted_ranges = _comment_start_ignored_ranges(self.language, text)
        ranges = []
        for open_delim, close_delim in self.delimiters:
            ranges.extend(
                (start, end)
                for start, end in self.parse_nested_ranges(
                    open_delim,
                    close_delim,
                    text,
                    quoted_ranges,
                )
                if not _starts_inside_ignored_range(start, quoted_ranges)
                and not _starts_with_excluded_comment_prefix(
                    text,
                    start,
                    self.excluded_comment_prefixes,
                )
            )
        return sorted(ranges)

    @staticmethod
    def parse_nested(open_delim, close_delim, text):
        """Extract top-level delimited text, including the delimiters.

        Args:
            open_delim: Opening nested comment delimiter.
            close_delim: Closing nested comment delimiter.
            text: Source text to scan.

        Returns:
            ``QueryMatch`` values for complete top-level nested blocks. Unclosed
            blocks are ignored.
        """

        return _query_matches_from_ranges(
            text, NestedCommentQuery.parse_nested_ranges(open_delim, close_delim, text)
        )

    @staticmethod
    def parse_nested_ranges(open_delim, close_delim, text, ignored_ranges=()):
        """Extract top-level delimited text ranges, including the delimiters."""

        result = []
        stack_depth = 0
        block_start = None
        open_len = len(open_delim)
        close_len = len(close_delim)
        search_from = 0

        while True:
            open_index = text.find(open_delim, search_from)
            close_index = text.find(close_delim, search_from)
            if open_index == -1 and close_index == -1:
                break

            if open_index != -1 and (close_index == -1 or open_index <= close_index):
                if stack_depth == 0 and _starts_inside_ignored_range(open_index, ignored_ranges):
                    search_from = open_index + open_len
                    continue
                if stack_depth == 0:
                    block_start = open_index
                stack_depth += 1
                search_from = open_index + open_len
                continue

            if stack_depth == 0 and _starts_inside_ignored_range(close_index, ignored_ranges):
                search_from = close_index + close_len
                continue
            if stack_depth:
                stack_depth -= 1
                if stack_depth == 0 and block_start is not None:
                    result.append((block_start, close_index + close_len))
                    block_start = None
            search_from = close_index + close_len

        return result


class CommentQuery(Query):
    """Extract comments by combining line/block regex and nested matching.

    Args:
        language: One registry language key, or an iterable of keys when the
            source language is ambiguous.

    Raises:
        TypeError: If ``language`` is not a string or iterable of strings.
        ValueError: If an iterable of languages is empty.
        NotImplementedError: If any language key is unknown to the registry.
    """

    def __init__(self, language):
        self.languages = self._normalize_languages(language)
        self.language = self.languages[0] if len(self.languages) == 1 else self.languages
        self._query_pairs = [
            (LineCommentQuery(entry), NestedCommentQuery(entry)) for entry in self.languages
        ]

    def contains(self, text):
        """Return ``True`` when any configured language finds a comment."""

        for line_comments, nested_comments in self._query_pairs:
            if line_comments.contains(text):
                return True
            if nested_comments.contains(text):
                return True
        return False

    def parse(self, text):
        """Return unique comment matches in source order.

        Args:
            text: Source text to scan.

        Returns:
            A list of ``QueryMatch`` values. Adjacent standalone single-line
            comments are grouped into one logical match.
        """

        return _query_matches_from_ranges(text, self.parse_ranges(text))

    def parse_ranges(self, text):
        """Return unique comment ranges in source order."""

        if len(self._query_pairs) == 1:
            line_comments, nested_comments = self._query_pairs[0]
            return self._parse_single_language_ranges(text, line_comments, nested_comments)

        ranges = []
        for line_comments, nested_comments in self._query_pairs:
            ranges.extend(self._parse_single_language_ranges(text, line_comments, nested_comments))
        return self._union_comment_ranges(ranges)

    def iter_ranges(self, text):
        """Yield unique comment ranges in source order."""

        yield from self.parse_ranges(text)

    @staticmethod
    def _normalize_languages(language):
        """Normalize constructor input into a non-empty tuple of language keys."""

        if isinstance(language, str):
            return (language,)

        if not isinstance(language, Iterable):
            raise TypeError("language must be a string or an iterable of language strings")

        languages = tuple(language)
        if not languages:
            raise ValueError("language list must contain at least one language")
        if any(not isinstance(entry, str) for entry in languages):
            raise TypeError("every language entry must be a string")
        return languages

    @staticmethod
    def _parse_single_language(text, line_comments, nested_comments):
        """Return grouped and deduplicated matches for one language."""

        return _query_matches_from_ranges(
            text,
            CommentQuery._parse_single_language_ranges(text, line_comments, nested_comments),
        )

    @staticmethod
    def _parse_single_language_ranges(text, line_comments, nested_comments):
        """Return grouped and deduplicated match ranges for one language."""

        quoted_ranges, scan_limit = _comment_scan_context(line_comments.language, text)
        ranges = []
        ranges.extend(nested_comments.parse_ranges(text, quoted_ranges))
        line_ranges = line_comments.parse_ranges(text, quoted_ranges, scan_limit=scan_limit)
        normalized = re.sub(r"[^a-z0-9]+", "_", line_comments.language.strip().lower()).strip("_")
        if normalized in _NO_ADJACENT_LINE_GROUPING_LANGUAGES:
            ranges.extend(line_ranges)
        else:
            ranges.extend(
                CommentQuery._group_line_comment_block_ranges(
                    text,
                    line_ranges,
                    language=line_comments.language,
                )
            )
        return LineCommentQuery._dedupe_match_ranges(ranges)

    @staticmethod
    def _group_line_comment_blocks(text, matches):
        """Group adjacent standalone line comments into logical blocks.

        Inline comments are intentionally not grouped with neighboring lines;
        grouping only applies when the comment occupies the whole source line.
        """

        ranges = [_match_range(text, match) for match in matches]
        grouped_ranges = CommentQuery._group_line_comment_block_ranges(text, ranges)
        return _query_matches_from_ranges(text, grouped_ranges)

    @staticmethod
    def _group_line_comment_block_ranges(text, ranges, language=""):
        """Group adjacent standalone line comment ranges into logical blocks."""

        if not ranges:
            return []

        grouped = []
        group_start = None
        group_end = None

        for start, end in ranges:
            if not CommentQuery._is_standalone_single_line(text, start, end):
                if group_start is not None:
                    grouped.append((group_start, group_end))
                    group_start = None
                    group_end = None
                grouped.append((start, end))
                continue

            if group_start is None:
                group_start = start
                group_end = end
                continue

            separator = text[group_end:start]
            group_key = CommentQuery._line_comment_group_key(text[group_start:group_end], language)
            next_key = CommentQuery._line_comment_group_key(text[start:end], language)
            if (
                CommentQuery._is_consecutive_line_separator(separator)
                and group_key is not None
                and group_key == next_key
            ):
                group_end = end
                continue

            grouped.append((group_start, group_end))
            group_start = start
            group_end = end

        if group_start is not None:
            grouped.append((group_start, group_end))

        return grouped

    @staticmethod
    def _dedupe_comment_matches(text, matches):
        """Deduplicate combined regex and nested matches by source range."""

        ranges = [_match_range(text, match) for match in matches]
        return _query_matches_from_ranges(text, LineCommentQuery._dedupe_match_ranges(ranges))

    @staticmethod
    def _union_comment_matches(text, matches):
        """Return unique matches across candidate languages."""

        return _query_matches_from_ranges(
            text,
            CommentQuery._union_comment_ranges(_match_range(text, match) for match in matches),
        )

    @staticmethod
    def _union_comment_ranges(ranges):
        """Return unique ranges across candidate languages in source order."""

        unique_ranges = set()
        result = []
        for start, end in ranges:
            comment_range = (start, end)
            if comment_range in unique_ranges:
                continue
            unique_ranges.add(comment_range)
            result.append(comment_range)
        return sorted(result)

    @staticmethod
    def _is_standalone_single_line(text, start, end):
        """Return ``True`` when a match is the only non-space content on a line."""

        match_text = text[start:end]
        if match_text.endswith("\r") and text[end : end + 1] == "\n":
            match_text = match_text[:-1]
        if any(ending in match_text for ending in _PHYSICAL_LINE_ENDINGS):
            return False

        previous_endings = (text.rfind(ending, 0, start) for ending in _PHYSICAL_LINE_ENDINGS)
        line_start = max(previous_endings) + 1
        next_endings = (
            index for ending in _PHYSICAL_LINE_ENDINGS if (index := text.find(ending, end)) != -1
        )
        line_end = min(next_endings, default=len(text))

        before = text[line_start:start]
        after = text[end:line_end]
        return before.strip() == "" and after.strip() == ""

    @staticmethod
    def _is_consecutive_line_separator(separator):
        """Return ``True`` for whitespace plus exactly one newline."""

        return (
            re.fullmatch(
                r"[^\S\r\n\u0085\u2028\u2029]*"
                r"(?:\r\n|[\r\n\u0085\u2028\u2029])"
                r"[^\S\r\n\u0085\u2028\u2029]*",
                separator,
            )
            is not None
        )

    @staticmethod
    def _line_comment_group_key(comment, language=""):
        """Return the delimiter family used for adjacent line grouping.

        Args:
            comment: Raw matched comment text.

        Returns:
            A normalized delimiter key for line comments, or ``None`` for
            block-like comments that should not merge into line-comment groups.
        """

        stripped = comment.lstrip()
        normalized_language = re.sub(r"[^a-z0-9]+", "_", language.strip().lower()).strip("_")
        if normalized_language == "nmodl" and stripped.startswith((":", "?")):
            return "nmodl-line"
        if normalized_language == "praat" and stripped.startswith(("#", ";", "!")):
            return "praat-line"
        if normalized_language in {"perl6", "raku"} and stripped.startswith(("#|", "#=")):
            paired_openers = ("#|(", "#|{", "#|[", "#|<", "#=(", "#={", "#=[", "#=<")
            return None if stripped.startswith(paired_openers) else "#"
        if normalized_language == "imba" and stripped.startswith("###"):
            return None
        if normalized_language in {
            "lua",
            "luau",
            "moonscript",
            "terra",
            "xmake",
        } and re.match(r"--\[[=]*\[", stripped):
            return None
        if normalized_language in {"glimmer_js", "glimmer_ts"} and stripped.startswith(
            ("{{!", "{{~!")
        ):
            return None
        block_prefixes = (
            "/*",
            "/-",
            "/+",
            "(*",
            "{-",
            "{#",
            "<!--",
            "<%#",
            "<% #",
            "#-",
            "#|",
            "#[[",
            "#[=",
        )
        if not stripped or stripped.startswith(block_prefixes):
            return None
        if stripped.lower().startswith("w00t"):
            return "w00t"

        line_prefixes = (
            "Comment",
            "G04",
            "<%--",
            "{{!",
            "{% #",
            "///",
            "//",
            "--",
            "-#",
            "::",
            "*>",
            "NB.",
            "BTW",
            "dnl",
            "REM",
            "\\",
            ";;",
            ";",
            "%%%",
            "%%",
            "%",
            "!",
            "⍝",
            "/",
            "#",
            "*",
            "'",
            '"',
        )
        for prefix in line_prefixes:
            if stripped.startswith(prefix):
                if prefix in {"///", "//"}:
                    return "//"
                if prefix in {"%%%", "%%", "%"}:
                    return "%"
                return prefix

        return None


class OpeningCommentQuery(Query):
    """Extract a file-opening logical comment block.

    Args:
        language: Registry language key.
        max_start_row: Last one-based row where the first real comment may
            begin.
        skip_hashbang: Whether to ignore an initial ``#!`` line before applying
            the opening-comment rule.

    Raises:
        ValueError: If ``max_start_row`` is less than one.
    """

    def __init__(self, language, max_start_row=3, skip_hashbang=True):
        if max_start_row < 1:
            raise ValueError("max_start_row must be at least 1")

        _warn_language_caveat_once(language)
        self.language = language
        self.max_start_row = max_start_row
        self.skip_hashbang = skip_hashbang
        self.line_comments = LineCommentQuery(language)
        self.nested_comments = NestedCommentQuery(language)

    def contains(self, text):
        """Return ``True`` when an opening comment block is found."""

        return bool(self.parse(text))

    def parse(self, text):
        """Return the first contiguous opening comment block, if any.

        Args:
            text: Source text to scan.

        Returns:
            A one-item list containing the opening ``QueryMatch`` or an empty
            list when the file does not begin with a supported comment block.
        """

        start_anchor = self._hashbang_end(text) if self.skip_hashbang else 0
        ranges = self._opening_comment_ranges(text, start_anchor)
        if not ranges:
            return []

        block_start, block_end = ranges[0]
        if self._row_number(text, block_start) > self.max_start_row:
            return []
        if text[start_anchor:block_start].strip():
            return []

        for next_start, next_end in ranges[1:]:
            if text[block_end:next_start].strip():
                break
            block_end = next_end

        return [_query_match_from_range(text, block_start, block_end)]

    def _opening_comment_ranges(self, text, start_anchor):
        """Return candidate comment ranges that start after the hashbang anchor."""

        ranges = []
        quoted_ranges = _comment_start_ignored_ranges(self.language, text)
        ranges.extend(self.line_comments.parse_ranges(text, quoted_ranges))
        ranges.extend(self.nested_comments.parse_ranges(text, quoted_ranges))

        filtered = [
            (start, end)
            for start, end in LineCommentQuery._dedupe_match_ranges(ranges)
            if end > start_anchor
        ]
        return sorted(filtered)

    @staticmethod
    def _match_range(text, match):
        """Return the half-open source range represented by ``match``."""

        return _match_range(text, match)

    @staticmethod
    def _hashbang_end(text):
        """Return the offset immediately after an initial hashbang line."""

        if not text.startswith("#!"):
            return 0
        line_end = text.find("\n")
        if line_end == -1:
            return len(text)
        return line_end + 1

    @staticmethod
    def _row_number(text, offset):
        """Return the one-based source row containing ``offset``."""

        return text.count("\n", 0, offset) + 1
