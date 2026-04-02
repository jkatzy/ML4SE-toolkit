import regex as re

from ..Query import Query, QueryMatch
from .registry import get_comment_syntax


class LineCommentQuery(Query):
    def __init__(self, language):
        self.language = language
        self.syntax = get_comment_syntax(language)
        self.regexes = self.syntax.regex_patterns

    def contains(self, string):
        for pattern in self.regexes:
            if re.search(pattern, string):
                return True
        return False

    def parse(self, text):
        matches = []
        for start, end in self._dedupe_match_ranges(self._iter_match_ranges(text)):
            matches.append(
                QueryMatch(
                    text[:start],
                    text[end:],
                    text[start:end],
                )
            )
        return matches

    def _iter_match_ranges(self, text):
        for pattern in self.regexes:
            for match in re.finditer(pattern, text):
                yield match.start(), match.end()

    @staticmethod
    def _dedupe_match_ranges(ranges):
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
    def __init__(self, language):
        self.language = language
        self.syntax = get_comment_syntax(language)
        self.delimeters = self.syntax.nested_delimiters

    def contains(self, string):
        for open_delim, close_delim in self.delimeters:
            pattern = re.escape(open_delim) + r"[\s\S]*?" + re.escape(close_delim)
            if re.search(pattern, string):
                return True
        return False

    def parse(self, text):
        matches = []
        for open_delim, close_delim in self.delimeters:
            matches.extend(self.parse_nested(open_delim, close_delim, text))
        return sorted(matches, key=lambda match: len(match.prefix))

    @staticmethod
    def parse_nested(open_delim, close_delim, text):
        """Extract top-level delimited text, including the delimiters."""

        result = []
        stack = []
        top_level_ranges = []
        open_len = len(open_delim)
        close_len = len(close_delim)
        i = 0

        while i < len(text):
            if text.startswith(open_delim, i):
                if not stack:
                    top_level_ranges.append([i, None])
                stack.append(i)
                i += open_len
                continue

            if text.startswith(close_delim, i) and stack:
                stack.pop()
                if not stack:
                    top_level_ranges[-1][1] = i + close_len
                i += close_len
                continue

            i += 1

        for start, end in top_level_ranges:
            if end is None:
                continue

            result.append(
                QueryMatch(
                    text[:start],
                    text[end:],
                    text[start:end],
                )
            )

        return result


class CommentQuery(Query):
    def __init__(self, language):
        self.language = language
        self.line_comments = LineCommentQuery(language)
        self.nested_comments = NestedCommentQuery(language)

    def contains(self, text):
        if self.nested_comments.contains(text):
            return True
        if self.line_comments.contains(text):
            return True
        return False

    def parse(self, text):
        comments = []
        comments.extend(self.nested_comments.parse(text))
        comments.extend(self._group_line_comment_blocks(text, self.line_comments.parse(text)))
        return self._dedupe_comment_matches(text, comments)

    @staticmethod
    def _group_line_comment_blocks(text, matches):
        if not matches:
            return []

        grouped = []
        group_start = None
        group_end = None

        for match in matches:
            start = len(match.prefix)
            end = len(text) - len(match.suffix)
            if not CommentQuery._is_standalone_single_line(text, start, end):
                if group_start is not None:
                    grouped.append(
                        QueryMatch(
                            text[:group_start],
                            text[group_end:],
                            text[group_start:group_end],
                        )
                    )
                    group_start = None
                    group_end = None
                grouped.append(match)
                continue

            if group_start is None:
                group_start = start
                group_end = end
                continue

            separator = text[group_end:start]
            if CommentQuery._is_consecutive_line_separator(separator):
                group_end = end
                continue

            grouped.append(
                QueryMatch(text[:group_start], text[group_end:], text[group_start:group_end])
            )
            group_start = start
            group_end = end

        if group_start is not None:
            grouped.append(
                QueryMatch(
                    text[:group_start],
                    text[group_end:],
                    text[group_start:group_end],
                )
            )

        return grouped

    @staticmethod
    def _dedupe_comment_matches(text, matches):
        ranges = []
        for match in matches:
            start = len(match.prefix)
            end = len(text) - len(match.suffix)
            ranges.append((start, end))

        deduped_matches = []
        for start, end in LineCommentQuery._dedupe_match_ranges(ranges):
            deduped_matches.append(
                QueryMatch(
                    text[:start],
                    text[end:],
                    text[start:end],
                )
            )
        return deduped_matches

    @staticmethod
    def _is_standalone_single_line(text, start, end):
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
        separator = separator.replace("\r", "")
        return separator.count("\n") == 1 and separator.replace("\n", "").strip() == ""


class OpeningCommentQuery(Query):
    def __init__(self, language, max_start_row=3, skip_hashbang=True):
        if max_start_row < 1:
            raise ValueError("max_start_row must be at least 1")

        self.language = language
        self.max_start_row = max_start_row
        self.skip_hashbang = skip_hashbang
        self.line_comments = LineCommentQuery(language)
        self.nested_comments = NestedCommentQuery(language)

    def contains(self, text):
        return bool(self.parse(text))

    def parse(self, text):
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

        return [QueryMatch(text[:block_start], text[block_end:], text[block_start:block_end])]

    def _opening_comment_ranges(self, text, start_anchor):
        ranges = []
        for match in self.line_comments.parse(text):
            ranges.append(self._match_range(text, match))
        for match in self.nested_comments.parse(text):
            ranges.append(self._match_range(text, match))

        filtered = [
            (start, end)
            for start, end in LineCommentQuery._dedupe_match_ranges(ranges)
            if end > start_anchor
        ]
        return sorted(filtered)

    @staticmethod
    def _match_range(text, match):
        start = len(match.prefix)
        end = len(text) - len(match.suffix)
        return start, end

    @staticmethod
    def _hashbang_end(text):
        if not text.startswith("#!"):
            return 0
        line_end = text.find("\n")
        if line_end == -1:
            return len(text)
        return line_end + 1

    @staticmethod
    def _row_number(text, offset):
        return text.count("\n", 0, offset) + 1
