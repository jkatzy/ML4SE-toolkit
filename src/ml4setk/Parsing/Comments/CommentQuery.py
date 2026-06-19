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
from .registry import get_comment_syntax

_WARNED_LANGUAGE_CAVEATS = set()
_RANGE_END_SENTINEL = float("inf")
_JSON_STRING_AWARE_LANGUAGES = {"jsonc"}


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


def _comment_start_ignored_ranges(language, text):
    """Return source ranges where comment delimiters should be ignored."""

    if language.lower() in _JSON_STRING_AWARE_LANGUAGES:
        return _json_string_ranges(text)
    return _quoted_string_ranges(text)


def _starts_inside_quoted_string(start, quoted_ranges):
    """Return ``True`` when ``start`` is inside any quoted string range."""

    if not quoted_ranges:
        return False

    index = bisect_right(quoted_ranges, (start, _RANGE_END_SENTINEL)) - 1
    if index < 0:
        return False

    quote_start, quote_end = quoted_ranges[index]
    return quote_start < start < quote_end


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

    def contains(self, string):
        """Return ``True`` when regex-based extraction finds a comment."""

        if not self.regexes:
            return False

        quoted_ranges = _comment_start_ignored_ranges(self.language, string)
        return any(
            not _starts_inside_quoted_string(start, quoted_ranges)
            for start, _ in self._iter_match_ranges(string)
        )

    def parse(self, text):
        """Return regex-based comment matches in source order.

        Args:
            text: Source text to scan.

        Returns:
            A list of ``QueryMatch`` values for single-line comments and
            non-nested block comments. Matches starting inside simple quoted
            strings are ignored.
        """

        return _query_matches_from_ranges(text, self.parse_ranges(text))

    def parse_ranges(self, text, quoted_ranges=None):
        """Return regex-based comment ranges in source order."""

        if not self.regexes:
            return []

        if quoted_ranges is None:
            quoted_ranges = _comment_start_ignored_ranges(self.language, text)
        match_ranges = (
            (start, end)
            for start, end in self._iter_match_ranges(text)
            if not _starts_inside_quoted_string(start, quoted_ranges)
        )
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
                if not _starts_inside_quoted_string(start, quoted_ranges)
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
            ranges.extend(
                self._parse_single_language_ranges(text, line_comments, nested_comments)
            )
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
            CommentQuery._parse_single_language_ranges(
                text, line_comments, nested_comments
            ),
        )

    @staticmethod
    def _parse_single_language_ranges(text, line_comments, nested_comments):
        """Return grouped and deduplicated match ranges for one language."""

        quoted_ranges = _comment_start_ignored_ranges(line_comments.language, text)
        ranges = []
        ranges.extend(nested_comments.parse_ranges(text, quoted_ranges))
        ranges.extend(
            CommentQuery._group_line_comment_block_ranges(
                text, line_comments.parse_ranges(text, quoted_ranges)
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
        if "\n" in match_text:
            return False

        line_start = text.rfind("\n", 0, start) + 1
        line_end = text.find("\n", end)
        if line_end == -1:
            line_end = len(text)

        before = text[line_start:start]
        after = text[end:line_end]
        return before.strip() == "" and after.strip() == ""

    @staticmethod
    def _is_consecutive_line_separator(separator):
        """Return ``True`` for whitespace plus exactly one newline."""

        separator = separator.replace("\r", "")
        return separator.count("\n") == 1 and separator.replace("\n", "").strip() == ""

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
