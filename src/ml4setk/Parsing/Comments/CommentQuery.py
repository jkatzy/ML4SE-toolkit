"""Registry-backed comment extraction queries.

Language-specific comment syntax belongs in ``registry.py``. The query classes
in this module are responsible only for matching, grouping, deduplicating, and
returning the normalized ``QueryMatch(prefix, suffix, match)`` contract.
"""

import warnings
from bisect import bisect_right
from collections.abc import Iterable

import regex as re

from ..Query import Query, QueryMatch
from .contextual import contextual_comment_ranges
from .registry import get_comment_syntax

_WARNED_LANGUAGE_CAVEATS = set()
_RANGE_END_SENTINEL = float("inf")
_JSON_STRING_AWARE_LANGUAGES = {"jsonc"}
_ECERE_STRING_AWARE_LANGUAGES = {"ecere_projects"}
_POGOSCRIPT_STRING_AWARE_LANGUAGES = {"pogoscript"}
_RDF_IRI_AWARE_LANGUAGES = {"sparql", "turtle"}
_SMALLTALK_STRING_AWARE_LANGUAGES = {"smalltalk"}
_GENERO_FORMS_SCREEN_OPEN = re.compile(
    r"(?im)^[ \t]*screen[ \t]*"
    r"(?:(?:\r\n|[\r\n\u0085\u2028\u2029])[ \t]*)*"
    r"(?P<open>\{)"
)
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


def _genero_forms_screen_header_ranges(text):
    """Return headers whose opening brace starts a Genero Forms screen body."""

    return [match.span() for match in _GENERO_FORMS_SCREEN_OPEN.finditer(text)]


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
    """Return ignored ranges and the maximum source offset to scan."""

    normalized = re.sub(r"[^a-z0-9]+", "_", language.strip().lower()).strip("_")
    if normalized == "nl":
        return _nl_comment_scan_context(text)
    if normalized in _JSON_STRING_AWARE_LANGUAGES:
        return _json_string_ranges(text), len(text)
    if normalized in _ECERE_STRING_AWARE_LANGUAGES:
        return _c_style_double_quoted_string_ranges(text), len(text)
    if normalized in _POGOSCRIPT_STRING_AWARE_LANGUAGES:
        return _pogoscript_string_ranges(text), len(text)
    if normalized in _SMALLTALK_STRING_AWARE_LANGUAGES:
        return _smalltalk_literal_ranges(text), len(text)
    if normalized == "tcsh":
        return (
            _merge_ignored_ranges(_quoted_string_ranges(text) + _tcsh_initial_hashbang_range(text)),
            len(text),
        )
    if normalized == "genero_forms":
        return (
            _merge_ignored_ranges(
                _quoted_string_ranges(text) + _genero_forms_screen_header_ranges(text)
            ),
            len(text),
        )
    if normalized in _RDF_IRI_AWARE_LANGUAGES:
        return (
            _merge_ignored_ranges(_quoted_string_ranges(text) + _rdf_iri_ranges(text)),
            len(text),
        )
    return _quoted_string_ranges(text), len(text)


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
        self.regex_patterns = self.syntax.regex_patterns
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

        if not self.regexes and not self.contextual_extractor:
            return []

        if quoted_ranges is None or scan_limit is None:
            default_ranges, default_limit = _comment_scan_context(self.language, text)
            if quoted_ranges is None:
                quoted_ranges = default_ranges
            if scan_limit is None:
                scan_limit = default_limit

        match_ranges = [
            (start, end)
            for start, end in self._iter_match_ranges(text)
            if end <= scan_limit
            and not _starts_inside_ignored_range(start, quoted_ranges)
            and not _starts_with_excluded_comment_prefix(
                text,
                start,
                self.excluded_comment_prefixes,
            )
        ]
        if self.contextual_extractor:
            match_ranges.extend(contextual_comment_ranges(self.contextual_extractor, text))
        return self._dedupe_match_ranges(match_ranges)

    def _iter_match_ranges(self, text):
        """Yield raw regex match ranges for all configured patterns."""

        for pattern in self.regexes:
            seen_starts = set()
            for match in pattern.finditer(text, overlapped=True):
                if match.start() in seen_starts:
                    continue
                seen_starts.add(match.start())
                yield match.start(), match.end()

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

        if quoted_ranges is None:
            quoted_ranges = _comment_start_ignored_ranges(self.language, text)
        ranges = []
        for open_delim, close_delim in self.delimiters:
            ranges.extend(
                (start, end)
                for start, end in self.parse_nested_ranges(open_delim, close_delim, text)
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
    def parse_nested_ranges(open_delim, close_delim, text):
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
                if stack_depth == 0:
                    block_start = open_index
                stack_depth += 1
                search_from = open_index + open_len
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
        ranges.extend(
            CommentQuery._group_line_comment_block_ranges(
                text,
                line_comments.parse_ranges(text, quoted_ranges, scan_limit=scan_limit),
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
    def _group_line_comment_block_ranges(text, ranges):
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
            group_key = CommentQuery._line_comment_group_key(text[group_start:group_end])
            next_key = CommentQuery._line_comment_group_key(text[start:end])
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
    def _line_comment_group_key(comment):
        """Return the delimiter family used for adjacent line grouping.

        Args:
            comment: Raw matched comment text.

        Returns:
            A normalized delimiter key for line comments, or ``None`` for
            block-like comments that should not merge into line-comment groups.
        """

        stripped = comment.lstrip()
        block_prefixes = (
            "/*",
            "/+",
            "(*",
            "{-",
            "{#",
            "<!--",
            "<%#",
            "<% #",
            "#-",
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
