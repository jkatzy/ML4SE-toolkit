"""Language-specific literal rules for the comment-aware source scanner.

Comment extraction protects string-like source regions so comment markers in
them are ignored. By default every ``'``, ``"``, and backtick opens a simple
single-line quoted string. Some languages give those characters other meanings
(primes, Lisp quote, attribute ticks, transpose) or have literals whose
contents look like comment markers (character literals, multi-line strings,
CDATA). A ``LexicalRules`` entry describes those cases for one language.

Rules only protect source ranges; they never create comments.
"""

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from typing import Optional, Tuple

import regex as re

from .registry import LANGUAGE_SYNTAX, get_comment_language_version

DEFAULT_QUOTE_CHARS = frozenset("'\"`")


@dataclass(frozen=True)
class LexicalRules:
    """Literal syntax used to protect non-comment source ranges.

    Attributes:
        quote_chars: Characters that open a simple single-line quoted string
            with backslash escapes.
        literals: Literal scanners tried, in order, at each candidate start
            before simple quote scanning. Each has ``scan(text, start, memo)``
            returning the protected ``(start, end)`` range or ``None``; a
            range may begin after ``start`` (a heredoc body).
        literal_start_chars: Characters at which ``literals`` may start.
        non_string_quote: Optional pattern; when it matches at a quote
            character, that character does not open a string (for example a
            postfix transpose operator).
    """

    quote_chars: frozenset = DEFAULT_QUOTE_CHARS
    literals: Tuple[object, ...] = ()
    literal_start_chars: frozenset = frozenset()
    non_string_quote: Optional["re.Pattern"] = None


def _rules(quote_chars="'\"`", literals=(), starts="", non_string_quote=None):
    return LexicalRules(
        quote_chars=frozenset(quote_chars),
        literals=tuple(_literal(literal) for literal in literals),
        literal_start_chars=frozenset(starts),
        non_string_quote=None if non_string_quote is None else re.compile(non_string_quote),
    )


def _nested_comment_end(text, start, open_delim, close_delim, memo=None):
    """Return the end of the depth-balanced comment opened at ``start``.

    ``memo`` remembers the offset after which no closer exists, and the end
    of every opener met while scanning, so overlapping openers do not each
    rescan the text.
    """

    memo_key = ("nested-unclosed", open_delim, close_delim)
    if memo is not None and start >= memo.get(memo_key, len(text) + 1):
        return None
    ends = None if memo is None else memo.setdefault(("nested-ends", open_delim, close_delim), {})
    if ends is not None and start in ends:
        return ends[start]
    openers = []
    search_from = start
    open_index = close_index = -2
    while True:
        if open_index != -1 and open_index < search_from:
            open_index = text.find(open_delim, search_from)
        if close_index < search_from:
            close_index = text.find(close_delim, search_from)
        if close_index == -1:
            # No closer exists at or after ``search_from``, so no opener
            # starting there can close either.
            if memo is not None:
                memo[memo_key] = min(memo.get(memo_key, len(text) + 1), search_from)
                ends.update(dict.fromkeys(openers))
            return None
        if open_index != -1 and open_index <= close_index:
            openers.append(open_index)
            search_from = open_index + len(open_delim)
            continue
        search_from = close_index + len(close_delim)
        opened = openers.pop()
        if ends is not None:
            ends[opened] = search_from
        if not openers:
            return search_from


class BalancedLiteral:
    """A literal of nesting two-delimiter pairs, matched by depth.

    It replaces a recursive regex such as Lua 5.0's ``[[ ... ]]`` whose
    failed matches rescan to the end from every opener.
    """

    def __init__(self, open_delim, close_delim):
        self.delimiters = (open_delim, close_delim)

    def scan(self, text, start, memo):
        if not text.startswith(self.delimiters[0], start):
            return None
        end = _nested_comment_end(text, start, *self.delimiters, memo)
        return None if end is None else (start, end)


class RegexLiteral:
    """A literal whose whole span is one regex match at the start offset."""

    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def scan(self, text, start, memo):
        match = self.pattern.match(text, start)
        if match is None or match.end() <= start:
            return None
        return start, match.end()


class DelimitedLiteral:
    """A literal opened by a regex and closed by the next closer match.

    Args:
        opener: Pattern matched at the start offset. Its groups may be used
            by ``closer`` through ``str.format`` positional fields.
        closer: Closer regex template, formatted with ``re.escape`` of the
            opener's groups.
        body_on_next_line: Protect only from the next line start (heredocs),
            so code after the opener on the same line is still scanned.

    A failed closer search is remembered per closer, so many unclosed openers
    cost one search instead of one search each.
    """

    def __init__(self, opener, closer, body_on_next_line=False, same_line=False):
        self.opener = re.compile(opener)
        # An opener led by ``(C+)`` that fails at one offset fails at every
        # later offset in the same run of ``C``: its ``C+`` there can only
        # end where the first one already tried.
        run = re.match(r"\((\\?[^\\\w()\[\]|*+?{}.^$])\+\)", opener)
        self.run_char = None if run is None else run.group(1)[-1]
        self.closer = closer
        self.body_on_next_line = body_on_next_line
        # The closer must start before the next CR or LF after the body start.
        self.same_line = same_line

    def scan(self, text, start, memo):
        if self.run_char is not None:
            run_key = (id(self), "run")
            failed_run = memo.get(run_key)
            if failed_run is not None and failed_run[0] < start < failed_run[1]:
                return None
        opened = self.opener.match(text, start)
        if opened is None:
            if self.run_char is not None:
                run_end = start
                while run_end < len(text) and text[run_end] == self.run_char:
                    run_end += 1
                memo[run_key] = (start, run_end)
            return None
        closer_text = self.closer.format(*(re.escape(group or "") for group in opened.groups()))
        body_start = opened.end()
        range_start = start
        if self.body_on_next_line:
            newline = _NEXT_LINE.search(text, body_start)
            if newline is None:
                return None
            body_start = newline.end()
            # Start at the line break so a marker at the body's first column is
            # strictly inside the protected range.
            range_start = newline.start()
        line_end = len(text)
        if self.same_line:
            breaks = memo.get("line-breaks")
            if breaks is None:
                breaks = memo["line-breaks"] = [m.start() for m in _LINE_BREAK.finditer(text)]
            after = bisect_left(breaks, body_start)
            line_end = breaks[after] if after < len(breaks) else len(text)
        failed = memo.get((id(self), closer_text))
        if failed is not None and failed[0] <= body_start < failed[1]:
            return None
        closer = memo.get(("pattern", closer_text))
        if closer is None:
            closer = memo[("pattern", closer_text)] = re.compile(closer_text)
        closed = closer.search(text, body_start, line_end)
        if closed is None:
            memo[(id(self), closer_text)] = (body_start, line_end)
            return None
        return range_start, closed.end()


_NEXT_LINE = re.compile(r"\r\n|\r|\n")
_BACKTICK_RUN = re.compile(r"`+")


class LineBoundedLiteral(RegexLiteral):
    """A regex literal that can fail only by reaching the end of its line.

    For such a pattern, a failure at one offset means every later offset on
    that line fails too, so the failure is remembered up to the line end
    instead of each opener rescanning the rest of a long line.
    """

    def scan(self, text, start, memo):
        failed = memo.get(id(self))
        if failed is not None and failed[0] <= start < failed[1]:
            return None
        found = super().scan(text, start, memo)
        if found is None:
            line_break = _LINE_BREAK.search(text, start)
            memo[id(self)] = (start, len(text) if line_break is None else line_break.start())
        return found


class CodeSpanLiteral:
    r"""CommonMark code span, ``(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)``, via a run index.

    The span closes at the next backtick run of exactly the opener's length.
    Indexing every run once keeps long backtick runs and many unmatched
    openers linear instead of rescanning the rest of the text per offset.
    """

    def scan(self, text, start, memo):
        index = memo.get(id(self))
        if index is None:
            runs = [match.span() for match in _BACKTICK_RUN.finditer(text)]
            by_length = {}
            for run_start, run_end in runs:
                by_length.setdefault(run_end - run_start, []).append(run_start)
            index = memo[id(self)] = (runs, by_length)
        runs, by_length = index
        containing = bisect_right(runs, (start, len(text) + 1)) - 1
        if containing < 0 or runs[containing][1] <= start:
            return None
        run_end = runs[containing][1]
        length = run_end - start
        starts = by_length.get(length, ())
        closer = bisect_left(starts, run_end)
        if closer == len(starts):
            return None
        return start, starts[closer] + length


class FencedBlockLiteral:
    r"""CommonMark fenced code block, scanned with a per-text closer index.

        Equivalent to ``(?m)(?<=^[ 	]{0,3})(`{3,}|~{3,})[^
    ]*(?:
    ?
    |
    )``
        ``[\s\S]*?^[ 	]{0,3}[`~]*[ 	]*$``. That regex backtracks the fence
        down to three characters, so the block uses the longest fence some later
        closing line can match, and closes at the first such line. Indexing the
        closing lines once avoids rescanning the text per fence length and per
        unclosed opener.
    """

    def scan(self, text, start, memo):
        if not _FENCE_START.match(text, start):
            return None
        fence_char = text[start]
        fence_end = start + 3
        while fence_end < len(text) and text[fence_end] == fence_char:
            fence_end += 1
        line_break = _LINE_BREAK.search(text, fence_end)
        if line_break is None:
            return None
        body_start = line_break.start() + 1
        lines = memo.get((id(self), fence_char))
        if lines is None:
            lines = memo[(id(self), fence_char)] = _closing_fence_lines(text, fence_char)
        starts, run_lengths, ends, longest_after = lines
        index = bisect_left(starts, body_start)
        if index == len(starts) or longest_after[index] < 3:
            return None
        fence_length = min(fence_end - start, longest_after[index])
        while run_lengths[index] < fence_length:
            index += 1
        return start, ends[index]


_FENCE_START = re.compile(r"(?m)(?<=^[ \t]{0,3})(?:```|~~~)")
_LINE_BREAK = re.compile(r"[\r\n]")


def _closing_fence_lines(text, fence_char):
    """Index lines that close a ``fence_char`` fence: starts, run lengths, ends.

    The last list holds, per line, the longest fence run on it or any later
    closing line, so a lookup can tell at once whether any closer remains.
    """

    closing = re.compile(r"[ \t]{0,3}(" + re.escape(fence_char) + r"+)[`~]*[ \t]*")
    starts, run_lengths, ends = [], [], []
    line_start = 0
    while line_start <= len(text):
        line_end = text.find("\n", line_start)
        if line_end < 0:
            line_end = len(text)
        match = closing.fullmatch(text, line_start, line_end)
        if match is not None:
            starts.append(line_start)
            run_lengths.append(len(match.group(1)))
            ends.append(line_end)
        line_start = line_end + 1
    longest_after = run_lengths[:]
    for index in range(len(longest_after) - 2, -1, -1):
        longest_after[index] = max(longest_after[index], longest_after[index + 1])
    return starts, run_lengths, ends, longest_after


@dataclass(frozen=True)
class StringForm:
    """One string literal form for ``InterpolatedStrings``.

    Attributes:
        opener: Regex matched at the literal start (prefix and quote).
        quote: Closing quote text.
        escapes: Whether a backslash escapes the next character.
        interpolation: Text that opens an embedded expression, or ``""``.
        interpolation_close: Bracket that closes the embedded expression.
        multiline: Whether the literal may contain line breaks.
        doubled_brace_is_text: Whether ``{{`` and ``}}`` are literal braces
            (Python f-strings).
    """

    opener: "re.Pattern"
    quote: str
    escapes: bool = True
    interpolation: str = ""
    interpolation_close: str = "}"
    multiline: bool = False
    doubled_brace_is_text: bool = False


def _form(opener, quote, **kwargs):
    return StringForm(re.compile(opener), quote, **kwargs)


_BRACKET_PAIRS = {"(": ")", "[": "]", "{": "}"}


class InterpolatedStrings:
    """String literals whose embedded expressions may contain nested strings.

    Forms are tried in order, so longer openers (triple quotes) come first.
    """

    def __init__(self, forms):
        self.forms = tuple(forms)

    def scan(self, text, start, memo):
        state = memo.get(id(self))
        if state is None:
            state = memo[id(self)] = ({}, {}, {})
        end = self._scan_string(text, start, 0, state)
        return None if end is None else (start, end)

    # ``state`` holds three per-text caches. A string scan depends only on its
    # start and nesting depth, so its result is cached; a body scan that finds
    # no closer marks the offsets it passed, since any later body scan of the
    # same form and depth reaching one of them fails the same way; and
    # ``_scan_code`` keeps its own dead offsets. Without them, unclosed nested
    # interpolations rescan exponentially.

    def _scan_string(self, text, start, depth, state):
        if depth > 32:
            return None
        results = state[0]
        key = (start, depth)
        if key in results:
            return results[key]
        end = None
        for form in self.forms:
            opened = form.opener.match(text, start)
            if opened is not None:
                end = self._scan_body(text, opened.end(), form, depth, state)
                break
        results[key] = end
        return end

    def _scan_body(self, text, index, form, depth, state):
        failed = state[1]
        known = failed.get((id(form), depth))
        visited = []
        end = self._walk_body(text, index, form, depth, state, known, visited)
        if end is None:
            if known is None:
                known = failed[(id(form), depth)] = bytearray(len(text) + 1)
            for offset in visited:
                known[offset] = 1
        return end

    def _walk_body(self, text, index, form, depth, state, known, visited):
        length = len(text)
        while index < length:
            if known is not None and known[index]:
                return None
            visited.append(index)
            if form.interpolation and text.startswith(form.interpolation, index):
                if form.doubled_brace_is_text and text.startswith("{{", index):
                    index += 2
                    continue
                index = self._scan_code(
                    text, index + len(form.interpolation), form.interpolation_close, depth, state
                )
                if index is None:
                    return None
                continue
            if form.doubled_brace_is_text and text.startswith("}}", index):
                index += 2
                continue
            if text.startswith(form.quote, index):
                return index + len(form.quote)
            char = text[index]
            if form.escapes and char == "\\":
                index += 2
                continue
            if not form.multiline and char in "\r\n":
                return None
            index += 1
        return None

    def _scan_code(self, text, index, closer, depth, state):
        """Return the end of an embedded expression, or ``None`` if unclosed.

        Which offsets the scan visits does not depend on the bracket stack,
        and a closer that does not match the top is ignored. So when a failed
        scan reached EOF without ever popping below its stack height at an
        offset, a scan with only ``[top]`` on its stack at that offset fails
        too; such offsets are remembered per depth as ``dead``.
        """

        dead = state[2].setdefault(depth, {})
        stack = [closer]
        trail = []
        length = len(text)
        while index < length:
            if len(stack) == 1 and dead.get(index) == stack[0]:
                break
            trail.append((index, len(stack), stack[-1]))
            char = text[index]
            nested = self._scan_string(text, index, depth + 1, state)
            if nested is not None:
                index = nested
                continue
            if char in _BRACKET_PAIRS:
                stack.append(_BRACKET_PAIRS[char])
            elif stack and char == stack[-1]:
                stack.pop()
                if not stack:
                    return index + 1
            index += 1
        lowest = len(stack)
        for offset, height, top in reversed(trail):
            lowest = min(lowest, height)
            if height == lowest:
                dead[offset] = top
        return None


_LAZY_BODIES = (r"[\s\S]*?", r"[\S\s]*?", r"[^\r\n]*?")


def _split_lazy_literal(pattern):
    r"""Split ``OPEN[\s\S]*?CLOSE`` into ``DelimitedLiteral`` arguments.

    The lazy body must appear once at the top level with no top-level
    alternation, so matching the opener and then searching for the first
    closer gives the regex's span. Backreferences in the closer become
    format fields. A ``[^\r\n]*?`` body keeps the closer on the opener's
    line, which needs a closer without anchors or lookaround. Returns
    ``None`` for other shapes.
    """

    depth = 0
    in_class = False
    index = 0
    split_at = None
    while index < len(pattern):
        char = pattern[index]
        if char == "\\":
            index += 2
            continue
        if in_class:
            in_class = char != "]"
        elif depth == 0 and pattern.startswith(_LAZY_BODIES, index):
            if split_at is not None:
                return None
            body = next(body for body in _LAZY_BODIES if pattern.startswith(body, index))
            split_at, split_end = index, index + len(body)
            index = split_end
            continue
        elif char == "[":
            in_class = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "|" and depth == 0:
            return None
        index += 1
    if split_at is None or depth != 0 or split_at == 0:
        return None
    opener, closer = pattern[:split_at], pattern[split_end:]
    same_line = pattern[split_at:split_end] == _LAZY_BODIES[2]
    if not closer or (same_line and re.search(r"\(\?|[$^]|\\[bBAZz]", closer)):
        return None
    template = []
    index = 0
    while index < len(closer):
        char = closer[index]
        if char == "\\" and index + 1 < len(closer):
            escaped = closer[index + 1]
            if escaped in "123456789":
                template.append("{%d}" % (int(escaped) - 1))
            else:
                template.append(char + escaped.replace("{", "{{").replace("}", "}}"))
            index += 2
            continue
        template.append("{{" if char == "{" else "}}" if char == "}" else char)
        index += 1
    return opener, "".join(template), False, same_line


class EscapedQuoteLiteral:
    r"""``OPEN Q(?:\\[\s\S]|[^Q\\])*Q`` plus an optional ``[A-Za-z]*``, scanned by hand.

    The body ends only at an unescaped ``Q`` or the end of the text. When a
    body from offset ``b`` runs off the end, a body from any later opener does
    too: its start follows a ``Q`` that ``b``'s scan either stopped at, which
    it did not, or skipped as escaped, which lands on the same offset. So one
    failure is remembered instead of rescanning from every escaped quote.
    """

    def __init__(self, opener, quote, suffix):
        self.opener = re.compile(opener)
        self.stop = re.compile("[\\\\" + re.escape(quote) + "]")
        self.suffix = re.compile(suffix)

    def scan(self, text, start, memo):
        opened = self.opener.match(text, start)
        if opened is None:
            return None
        body = opened.end()
        failed_from = memo.get(id(self))
        if failed_from is not None and body >= failed_from:
            return None
        index = body
        while True:
            stop = self.stop.search(text, index)
            if stop is None or (text[stop.start()] == "\\" and stop.start() + 1 >= len(text)):
                memo[id(self)] = body if failed_from is None else min(failed_from, body)
                return None
            if text[stop.start()] == "\\":
                index = stop.start() + 2
                continue
            return start, self.suffix.match(text, stop.end()).end()


_ESCAPED_QUOTE_SHAPE = re.compile(
    r"(?P<open>.*?(?P<quote>\\[^\w]|[^\\]))"
    r"\(\?:\\\\\[\\s\\S\]\|\[\^(?P<class>\\[^\w]|[^\\])\\\\\]\)\*"
    r"(?P<close>\\[^\w]|[^\\])(?P<suffix>(?:\[A-Za-z\]\*)?)"
)


def _escaped_quote_literal(pattern):
    """Return an ``EscapedQuoteLiteral`` for a pattern of that shape, else ``None``."""

    shape = _ESCAPED_QUOTE_SHAPE.fullmatch(pattern)
    if shape is None:
        return None
    quote, excluded, close = (shape.group(name)[-1] for name in ("quote", "class", "close"))
    if not quote == excluded == close or quote == "\\" or "*" in shape.group("open"):
        # A repeated opener could itself rescan, so keep those as regexes.
        return None
    return EscapedQuoteLiteral(shape.group("open"), quote, shape.group("suffix"))


# Recursive regexes whose match is the depth-balanced run of their delimiters.
_BALANCED_LITERALS = {r"\[\[(?:(?!\[\[|\]\])[\s\S]|(?R))*\]\]": ("[[", "]]")}


def _literal(value):
    if not isinstance(value, str):
        return value
    # A lazy block regex rescans to the end of the text from every unclosed
    # opener; a delimited literal remembers that its closer is missing.
    split = _split_lazy_literal(value)
    if value in _BALANCED_LITERALS:
        literal = BalancedLiteral(*_BALANCED_LITERALS[value])
    else:
        literal = DelimitedLiteral(*split) if split else _escaped_quote_literal(value)
    if literal is None:
        return RegexLiteral(value)
    # The regex it replaces; tests check that both agree.
    literal.pattern = re.compile(value)
    return literal


# A Haskell/ML-style character literal: one character or one escape.
_ML_CHAR_LITERAL = (
    r"'(?:\\(?:[0-9]+|x[0-9a-fA-F]+|o[0-7]+|u\{?[0-9a-fA-F]+\}?|\^.|[A-Z]{2,3}|[^\r\n])"
    r"|[^'\\\r\n])'"
)
_FSHARP_LITERALS = (r'"""[\s\S]*?"""', r'@"(?:""|[^"])*"', _ML_CHAR_LITERAL)
_CSHARP_LITERALS = (r'"""[\s\S]*?"""', r'\$?@\$?"(?:""|[^"])*"')
_TRANSPOSE = r"(?<=[\w)\]}.'])'"
# ECMA-262 12.9.5: a / after an operator, punctuator, or keyword (not after an
# operand) starts a RegularExpressionLiteral.
_REGEX_LITERAL_PATTERN = (
    r"(?<=(?:(?m:^)|[=(,:\[!&|?{};+\-*%<>~^]|\b(?:return|typeof|case|do|else|in|instanceof"
    r"|new|void|delete|throw|yield|await))[ \t]*)"
    r"/(?![/*])(?:\\.|\[(?:\\.|[^\]\\\r\n])*\]|[^/\\\r\n\[])+/[A-Za-z]*"
)


class EcmaRegexLiteral:
    r"""``_REGEX_LITERAL_PATTERN`` with its body scanned by hand.

    The body alternatives (``\\.``, a ``[...]`` class, any other character)
    start with different characters, so the regex never backtracks into them
    and a hand scan gives the same span. Offsets from which a body scan, in or
    out of a class, is known to hit a line break unclosed are remembered, so
    slashes in front of an unclosed class do not each rescan the line.
    """

    _opener = re.compile(_REGEX_LITERAL_PATTERN.split("/(?![/*])")[0] + "/(?![/*])")
    _flags = re.compile(r"[A-Za-z]*")

    def scan(self, text, start, memo):
        opened = self._opener.match(text, start)
        if opened is None:
            return None
        failed = memo.setdefault(id(self), {})
        index = opened.end()
        in_class = False
        visited = []
        while index < len(text):
            known = failed.get(in_class)
            if known is not None and known[index]:
                break
            visited.append((index, in_class))
            char = text[index]
            if char == "\\":
                if index + 1 >= len(text) or text[index + 1] == "\n":
                    break
                index += 2
            elif char in "\r\n":
                break
            elif in_class:
                in_class = char != "]"
                index += 1
            elif char == "/":
                return start, self._flags.match(text, index + 1).end()
            else:
                in_class = char == "["
                index += 1
        for offset, state in visited:
            known = failed.get(state)
            if known is None:
                known = failed[state] = bytearray(len(text) + 1)
            known[offset] = 1
        return None


_REGEX_LITERAL = EcmaRegexLiteral()


_TRIPLE_DOUBLE = '"' * 3
_TRIPLE_SINGLE = "'" * 3


def _plain_forms(prefix=""):
    """Escaped single-line ' and " strings, as nested inside interpolation."""

    return (
        _form(prefix + '"', '"'),
        _form(prefix + "'", "'"),
    )


# ECMA-262 13.2.8: template substitutions are expressions that may contain
# strings and templates.
_ECMASCRIPT_STRINGS = InterpolatedStrings(
    (_form("`", "`", interpolation="${", multiline=True),) + _plain_forms()
)
# Dart spec 17.7: raw strings have no escapes or interpolation; ${} may nest
# strings in every other form.
_DART_STRINGS = InterpolatedStrings(
    (
        _form(r"(?<![\w$])r" + _TRIPLE_SINGLE, _TRIPLE_SINGLE, escapes=False, multiline=True),
        _form(r"(?<![\w$])r" + _TRIPLE_DOUBLE, _TRIPLE_DOUBLE, escapes=False, multiline=True),
        _form(r"(?<![\w$])r'", "'", escapes=False),
        _form(r'(?<![\w$])r"', '"', escapes=False),
        _form(_TRIPLE_SINGLE, _TRIPLE_SINGLE, interpolation="${", multiline=True),
        _form(_TRIPLE_DOUBLE, _TRIPLE_DOUBLE, interpolation="${", multiline=True),
        _form("'", "'", interpolation="${"),
        _form('"', '"', interpolation="${"),
    )
)
# Kotlin grammar: "..." and raw triple-quoted strings both support ${} templates.
_KOTLIN_STRINGS = InterpolatedStrings(
    (
        _form(
            _TRIPLE_DOUBLE,
            _TRIPLE_DOUBLE,
            escapes=False,
            interpolation="${",
            multiline=True,
        ),
        _form('"', '"', interpolation="${"),
        _form("'", "'"),
    )
)
# Swift reference "String Literals": \( ) interpolation; raw #"..."# strings.
_SWIFT_STRINGS = InterpolatedStrings(
    (
        _form(
            _TRIPLE_DOUBLE,
            _TRIPLE_DOUBLE,
            interpolation="\\(",
            interpolation_close=")",
            multiline=True,
        ),
        _form('"', '"', interpolation="\\(", interpolation_close=")"),
    )
)
_SWIFT_RAW = (
    r"(#+)" + _TRIPLE_DOUBLE + r"[\s\S]*?" + _TRIPLE_DOUBLE + r"\1",
    r'(#+)"[^\r\n]*?"\1',
)


def _python_forms():
    forms = []
    for quote, multiline in (
        (_TRIPLE_DOUBLE, True),
        (_TRIPLE_SINGLE, True),
        ('"', False),
        ("'", False),
    ):
        forms.append(
            _form(
                r"(?<![\w])(?i:rf|fr|f)" + quote,
                quote,
                interpolation="{",
                multiline=multiline,
                doubled_brace_is_text=True,
            )
        )
        forms.append(_form(r"(?<![\w])(?i:rb|br|r|b|u)?" + quote, quote, multiline=multiline))
    return tuple(forms)


# PEP 701 (Python 3.12): replacement fields may contain any expression,
# including strings that reuse the enclosing quote.
_PYTHON_STRINGS = InterpolatedStrings(_python_forms())

# C++ [lex.string]: R"delim( ... )delim" raw strings may span lines.
_CPP_RAW_STRING = DelimitedLiteral(r'(?<![\w])(?:u8|[uUL])?R"([^()\\\s]{0,16})\(', r'\){0}"')
# C++14 [lex.ppnumber] and C23: ' is a digit separator inside a pp-number.
_PP_NUMBER = r"(?<![\w.])\.?[0-9](?:'[0-9A-Za-z_]|[eEpP][+-]|[0-9A-Za-z_.])*"
_C_FAMILY = _rules("'\"`", literals=(_PP_NUMBER,), starts="0123456789.")
_CPP_FAMILY = _rules("'\"`", literals=(_CPP_RAW_STRING, _PP_NUMBER), starts="uULR0123456789.")

# POSIX XCU 2.2: backslash quotes one character; single quotes have no
# escapes; 2.7.4: here-document bodies are data.
_SHELL = _rules(
    "",
    literals=(
        DelimitedLiteral(
            r"<<-?[ \t]*(['\"]?)([A-Za-z_][\w.-]*)\1",
            r"(?m)^\t*{1}\r?$",
            body_on_next_line=True,
        ),
        r"\\[\s\S]",
        r"\$'(?:\\[\s\S]|[^'\\])*'",
        r"'[^']*'",
        r'"(?:\\[\s\S]|[^"\\])*"',
        r"`(?:\\[\s\S]|[^`\\])*`",
    ),
    starts="<\\$'\"`",
)

_LISP_LITERALS = (r"#\\(?:[A-Za-z][A-Za-z0-9-]*|[\s\S])", r"\|(?:\\[\s\S]|[^|\\])*\|")

# HTML/XML: quotes delimit strings only in attribute values inside a tag;
# quotes in text content are prose.
_MARKUP_TAG = r"<[A-Za-z/?!](?:\"[^\"]*\"|'[^']*'|[^<>\"'])*>"
_CDATA = r"<!\[CDATA\[[\s\S]*?\]\]>"
_MARKUP = _rules("", literals=(_CDATA, _MARKUP_TAG), starts="<")
_MARKUP_FAMILY = "markup_style"

_HASKELL = _rules('"', literals=(_ML_CHAR_LITERAL,), starts="'")
_LISP = _rules('"', literals=_LISP_LITERALS, starts="#|")
_FSHARP = _rules('"', literals=_FSHARP_LITERALS, starts="\"@'")
_ECMASCRIPT = _rules("'\"", literals=(_ECMASCRIPT_STRINGS, _REGEX_LITERAL), starts="`/'\"")
_CSHARP = _rules("'\"`", literals=_CSHARP_LITERALS, starts='"$@')

_LEXICAL_RULES = {
    # Haskell 2010 2.4/2.6 and descendants: primes in identifiers, 'c' literals.
    "haskell": _HASKELL,
    "literate_haskell": _HASKELL,
    "c2hs_haskell": _HASKELL,
    "purescript": _HASKELL,
    "idris": _HASKELL,
    "curry": _HASKELL,
    "elm": _HASKELL,
    "frege": _HASKELL,
    "agda": _HASKELL,
    # OCaml manual 11.1: 'a type variables, 'c' literals, {id|...|id} strings.
    "ocaml": _rules('"', literals=(r"\{([a-z_]*)\|[\s\S]*?\|\1\}", _ML_CHAR_LITERAL), starts="{'"),
    # F# spec 3.4/3.5: primes, 'c' literals, verbatim and triple-quoted strings.
    "fsharp": _FSHARP,
    "f#": _FSHARP,
    "f_sharp": _FSHARP,
    # Lisps: ' is quote, only " delimits strings, #\c is a character.
    "common_lisp": _LISP,
    "scheme": _LISP,
    "racket": _LISP,
    "clojure": _rules(
        '"',
        literals=(
            r"\\(?:newline|space|tab|formfeed|backspace|return|u[0-9a-fA-F]{4}|o[0-7]{1,3}"
            r"|[\s\S])",
        ),
        starts="\\",
    ),
    "emacs_lisp": _rules('"', literals=(r"\?(?:\\[\s\S]|[^\s\\])",), starts="?"),
    # IEEE 1364/1800: ' introduces sized numbers and casts; " strings only.
    "verilog": _rules('"'),
    "systemverilog": _rules('"'),
    # VHDL/Ada: ' is the attribute tick; 'c' is a character literal.
    "vhdl": _rules('"', literals=(r"'[^\r\n]'",), starts="'"),
    "ada": _rules('"', literals=(r"'[^\r\n]'",), starts="'"),
    # MATLAB/Julia: a postfix ' is the (conjugate) transpose or adjoint.
    "matlab": _rules("'\"", non_string_quote=_TRANSPOSE),
    "julia": _rules(
        "'\"",
        literals=(DelimitedLiteral(_TRIPLE_DOUBLE, _TRIPLE_DOUBLE),),
        starts='"',
        non_string_quote=_TRANSPOSE,
    ),
    # Erlang reference 3.2: $c character literals.
    "erlang": _rules(
        "'\"",
        literals=(r"\$(?:\\(?:[0-7]{1,3}|x\{[0-9a-fA-F]+\}|x[0-9a-fA-F]{2}|\^.|[\s\S])|[\s\S])",),
        starts="$",
    ),
    # Elixir: ?c code point literals.
    # Elixir: ?c code point literals and ~x sigils with any sigil delimiter.
    "elixir": _rules(
        "'\"",
        literals=(
            r"(?<![\w?!])\?(?:\\[\s\S]|[^\s\\])",
            r"~(?:[a-z]|[A-Z][A-Z0-9]*)(?:"
            + _TRIPLE_DOUBLE
            + r"[\s\S]*?"
            + _TRIPLE_DOUBLE
            + r"|"
            + _TRIPLE_SINGLE
            + r"[\s\S]*?"
            + _TRIPLE_SINGLE
            + r'|"(?:\\[\s\S]|[^"\\])*"'
            + r"|'(?:\\[\s\S]|[^'\\])*'"
            + r"|/(?:\\[\s\S]|[^/\\])*/"
            + r"|\|(?:\\[\s\S]|[^|\\])*\|"
            + r"|\((?:\\[\s\S]|[^)\\])*\)"
            + r"|\[(?:\\[\s\S]|[^\]\\])*\]"
            + r"|\{(?:\\[\s\S]|[^}\\])*\}"
            + r"|<(?:\\[\s\S]|[^>\\])*>)",
        ),
        starts="?~",
    ),
    # ISO Prolog 6.4.4: 0'c character code constants.
    "prolog": _rules("'\"`", literals=(r"(?<![\w])0'(?:''|\\[\s\S]|[^\r\n])",), starts="0"),
    # Ruby: ?c character literals and %w/%i/%q percent literals.
    "ruby": _rules(
        "'\"`",
        literals=(
            DelimitedLiteral(
                r"<<[~-]?(['\"`]?)([A-Za-z_]\w*)\1",
                r"(?m)^[ \t]*{1}[ \t]*\r?$",
                body_on_next_line=True,
            ),
            r"(?m)^__END__\r?$[\s\S]*",
            r"(?<![\w?!)\]}])\?(?:\\[\s\S]|[^\s\\])(?!\w)",
            r"%[wWiIqQrsx]?\((?:\\[\s\S]|[^()\\])*\)",
            r"%[wWiIqQrsx]?\[(?:\\[\s\S]|[^\[\]\\])*\]",
            r"%[wWiIqQrsx]?\{(?:\\[\s\S]|[^{}\\])*\}",
            r"%[wWiIqQrsx]?<(?:\\[\s\S]|[^<>\\])*>",
        ),
        starts="?%<_",
    ),
    # perlop "Quote and Quote-like Operators": # may delimit q, qq, qw, qr, qx,
    # m, s, tr, and y when it follows the operator name immediately.
    "perl": _rules(
        "'\"`",
        literals=(
            DelimitedLiteral(
                r"<<~?(['\"]?)([A-Za-z_]\w*)\1",
                r"(?m)^[ \t]*{1}\r?$",
                body_on_next_line=True,
            ),
            r"(?m)^__(?:END|DATA)__\b[\s\S]*",
            r"(?<![\w$@%&])(?:s|tr|y)#(?:\\[\s\S]|[^#\\])*#(?:\\[\s\S]|[^#\\])*#[A-Za-z]*",
            r"(?<![\w$@%&])(?:qq|qw|qr|qx|q|m)#(?:\\[\s\S]|[^#\\])*#[A-Za-z]*",
        ),
        starts="stymq<_",
    ),
    # TeXbook ch. 7: \c is a control symbol, so \% is not a comment.
    # LaTeX manual: \verb arguments and verbatim/lstlisting bodies are literal.
    "tex": _rules(
        "",
        literals=(
            r"\\verb\*?([^A-Za-z\s*])[^\r\n]*?\1",
            r"\\begin\{(verbatim\*?|lstlisting)\}[\s\S]*?\\end\{\1\}",
            r"\\[\s\S]",
        ),
        starts="\\",
    ),
    # GNU make manual 3.1: \# is a literal hash.
    "makefile": _rules("'\"`", literals=(r"\\#",), starts="\\"),
    # PowerShell about_Quoting_Rules: backtick escapes, doubled '', here-strings.
    "powershell": _rules(
        "",
        literals=(
            DelimitedLiteral(r'@"[^\S\r\n]*\r?\n', r'(?m)^"@'),
            DelimitedLiteral(r"@'[^\S\r\n]*\r?\n", r"(?m)^'@"),
            r'"(?:`[\s\S]|""|[^"`])*"',
            r"'(?:''|[^'])*'",
        ),
        starts="@\"'",
    ),
    # Go spec: raw string literals may span lines.
    "go": _rules("'\"", literals=(r"`[^`]*`",), starts="`"),
    # ECMA-262 12.9.6: template literals may span lines.
    "javascript": _ECMASCRIPT,
    "jsx": _ECMASCRIPT,
    "typescript": _ECMASCRIPT,
    "tsx": _ECMASCRIPT,
    # JLS 3.10.6: text blocks.
    "java": _rules("'\"`", literals=(r'"{3}[\s\S]*?(?<!\\)"{3}',), starts='"'),
    # Swift reference: multiline and raw string literals.
    "swift": _rules("'\"`", literals=_SWIFT_RAW + (_SWIFT_STRINGS,), starts='#"'),
    # C# spec 6.4.5.6: verbatim and raw string literals.
    "c#": _CSHARP,
    "c_sharp": _CSHARP,
    "csharp": _CSHARP,
    # Dart spec 17.7: raw strings have no escapes; triple quotes span lines.
    "dart": _rules("'\"`", literals=(_DART_STRINGS,), starts="r'\""),
    # TOML 1.0: multi-line basic and literal strings.
    "toml": _rules(
        "'\"", literals=(r'"{3}[\s\S]*?"{3}(?!")', r"'{3}[\s\S]*?'{3}(?!')"), starts="\"'"
    ),
    # XML 1.0 2.7: CDATA sections are character data.
    "xml": _rules("", literals=(_CDATA, _MARKUP_TAG), starts="<"),
    # C23 and C++14: digit separators; C++ raw strings.
    "c": _C_FAMILY,
    "c++": _CPP_FAMILY,
    "cuda": _CPP_FAMILY,
    "objective-c": _C_FAMILY,
    "objective_cpp": _CPP_FAMILY,
    "objective_c_plus_plus": _CPP_FAMILY,
    # PEP 701 f-strings with nested strings in replacement fields.
    "python": _rules("'\"", literals=(_PYTHON_STRINGS,), starts="fFrRbBuU'\""),
    "numpy": _rules("'\"", literals=(_PYTHON_STRINGS,), starts="fFrRbBuU'\""),
    # Kotlin templates may contain nested strings.
    "kotlin": _rules("'\"", literals=(_KOTLIN_STRINGS,), starts="'\""),
    "gradle_kotlin_dsl": _rules("'\"", literals=(_KOTLIN_STRINGS,), starts="'\""),
    # PHP manual: heredoc and nowdoc bodies are string data.
    "php": _rules(
        "'\"`",
        literals=(
            DelimitedLiteral(
                r"<<<[ \t]*(['\"]?)([A-Za-z_]\w*)\1\r?\n",
                r"(?m)^[ \t]*{1}\b",
            ),
        ),
        starts="<",
    ),
    "shell": _SHELL,
    # PostgreSQL 4.1.2.4: dollar-quoted string constants.
    "plpgsql": _rules(
        "'\"",
        literals=(DelimitedLiteral(r"(?<![\w$])\$([A-Za-z_]\w*)?\$", r"\${0}\$"),),
        starts="$",
    ),
    # T-SQL: [ ] delimited identifiers, with ]] as an escaped bracket.
    # A bracket identifier fails only when no ] follows on its line.
    "tsql": _rules("'\"", literals=(LineBoundedLiteral(r"\[(?:\]\]|[^\]\r\n])*\]"),), starts="["),
    # R ?Quotes (R >= 4.0): r"(...)", r"[...]", r"{...}" with optional dashes.
    "r": _rules(
        "'\"`",
        literals=(
            DelimitedLiteral(r"(?<![\w.])[rR](['\"])(-*)\(", r"\){1}{0}"),
            DelimitedLiteral(r"(?<![\w.])[rR](['\"])(-*)\[", r"\]{1}{0}"),
            DelimitedLiteral(r"(?<![\w.])[rR](['\"])(-*)\{", r"\}{1}{0}"),
        ),
        starts="rR",
    ),
    # Sass "Special Functions" and Less: unquoted url() arguments are URLs.
    "scss": _rules("'\"`", literals=(r"(?i)url\(\s*(?![\"'])[^)\s]*\s*\)",), starts="uU"),
    "less": _rules("'\"`", literals=(r"(?i)url\(\s*(?![\"'])[^)\s]*\s*\)",), starts="uU"),
    # Zig reference: \\ starts a multiline string literal line.
    "zig": _rules("'\"", literals=(r"\\\\[^\r\n]*",), starts="\\"),
    # Nix manual: ''...'' indented strings; ' also appears in identifiers.
    "nix": _rules(
        '"',
        literals=(r"''(?:'''|''[$\\][\s\S]|[^']|'(?!'))*''",),
        starts="'",
    ),
    # HCL native syntax: heredoc templates.
    "hcl": _rules(
        "'\"`",
        literals=(DelimitedLiteral(r"<<-?([A-Za-z_]\w*)\r?\n", r"(?m)^[ \t]*{0}\r?$"),),
        starts="<",
    ),
    # Jsonnet spec: ||| text blocks.
    "jsonnet": _rules(
        "'\"`",
        literals=(DelimitedLiteral(r"\|\|\|-?[ \t]*\r?\n", r"(?m)^[ \t]*\|\|\|"),),
        starts="|",
    ),
    # Nim manual: triple-quoted and raw triple-quoted strings.
    "nim": _rules(
        "'\"`",
        literals=(DelimitedLiteral(r"(?<![\w])[rR]?" + _TRIPLE_DOUBLE, _TRIPLE_DOUBLE + '(?!")'),),
        starts='"rR',
    ),
    # cmake-language(7): bracket arguments.
    "cmake": _rules(
        "'\"",
        literals=(DelimitedLiteral(r"\[(=*)\[", r"\]{0}\]"),),
        starts="[",
    ),
    # CommonMark 4.5/6.1: fenced code blocks and code spans are literal text;
    # quotes in prose do not delimit strings.
    "markdown": _rules(
        "",
        literals=(
            FencedBlockLiteral(),
            CodeSpanLiteral(),
        ),
        starts="`~",
    ),
}


# Version profiles named by ``CommentLanguageVersion.lexical_profile``. A
# profile replaces a language's literal rules for that version only.
LEXICAL_VERSION_PROFILES = {
    # C before C23 and C++ before C++14: ' never separates digits.
    "c-without-digit-separators": _rules("'\"`"),
    # C++11: raw string literals, but no digit separators yet.
    "cpp-raw-strings-without-digit-separators": _rules(
        "'\"`", literals=(_CPP_RAW_STRING,), starts="uULR"
    ),
    # CMake before 3.0 has no [[...]] bracket arguments.
    "cmake-2.8": _rules("'\""),
    # OpenSSH 8.5 and 8.6 cut every line at its first #, even inside quotes.
    "ssh-config-8.5": _rules(""),
    # PHP before 7.3: a heredoc closes only at its label in column 0, followed
    # by an optional ; and the line break.
    "php-7.2": _rules(
        "'\"`",
        literals=(
            DelimitedLiteral(
                r"<<<[ \t]*(['\"]?)([A-Za-z_]\w*)\1\r?\n",
                r"(?m)^{1};?(?=[\r\n]|\Z)",
            ),
        ),
        starts="<",
    ),
    # Vim9 script: "..." strings take backslash escapes; '...' strings double
    # a quote to escape it and treat a backslash literally.
    "vim9": _rules('"', literals=(r"'(?:[^'\r\n]|'')*'",), starts="'"),
    # EditorConfig cores before spec 0.15 (ini.c) have no quoted values.
    "editorconfig-pre-0.15": _rules(""),
    # Lua 4.0 and 5.0: [[ ]] long strings nest; there are no leveled brackets.
    "lua-5.0": _rules("'\"", literals=(r"\[\[(?:(?!\[\[|\]\])[\s\S]|(?R))*\]\]",), starts="["),
}


def lexical_rules_for(language: str, version: Optional[str] = None) -> LexicalRules:
    """Return literal rules for a registry language key such as ``c++``.

    Args:
        language: Registry language key.
        version: Resolved version name. A version whose registry entry names a
            ``lexical_profile`` uses that profile instead of the language rules.
    """

    key = language.strip().lower()
    if version is not None:
        profile = _version_lexical_profile(key, version)
        if profile:
            return LEXICAL_VERSION_PROFILES[profile]
    rules = _LEXICAL_RULES.get(key)
    if rules is None:
        rules = _LEXICAL_RULES.get(re.sub(r"[^a-z0-9]+", "_", key).strip("_"))
    if rules is None:
        syntax = LANGUAGE_SYNTAX.get(key)
        rules = _MARKUP if syntax is not None and syntax.family_name == _MARKUP_FAMILY else None
    return _DEFAULT_RULES if rules is None else rules


_DEFAULT_RULES = LexicalRules()


def _version_lexical_profile(language: str, version: str) -> str:
    """Return the lexical profile named by ``language``'s ``version``, if any."""

    metadata = get_comment_language_version(language, version)
    return "" if metadata is None else metadata.lexical_profile
