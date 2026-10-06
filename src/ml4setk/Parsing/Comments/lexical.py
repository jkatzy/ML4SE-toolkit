"""Language-specific literal rules for the comment-aware source scanner.

Comment extraction protects string-like source regions so comment markers in
them are ignored. By default every ``'``, ``"``, and backtick opens a simple
single-line quoted string. Some languages give those characters other meanings
(primes, Lisp quote, attribute ticks, transpose) or have literals whose
contents look like comment markers (character literals, multi-line strings,
CDATA). A ``LexicalRules`` entry describes those cases for one language.

Rules only protect source ranges; they never create comments.
"""

from dataclasses import dataclass
from typing import Optional, Tuple

import regex as re

from .registry import LANGUAGE_SYNTAX

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

    def __init__(self, opener, closer, body_on_next_line=False):
        self.opener = re.compile(opener)
        self.closer = closer
        self.body_on_next_line = body_on_next_line

    def scan(self, text, start, memo):
        opened = self.opener.match(text, start)
        if opened is None:
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
        failed_from = memo.get((id(self), closer_text))
        if failed_from is not None and body_start >= failed_from:
            return None
        closer = memo.get(("pattern", closer_text))
        if closer is None:
            closer = memo[("pattern", closer_text)] = re.compile(closer_text)
        closed = closer.search(text, body_start)
        if closed is None:
            memo[(id(self), closer_text)] = body_start
            return None
        return range_start, closed.end()


_NEXT_LINE = re.compile(r"\r\n|\r|\n")


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
        end = self._scan_string(text, start, 0)
        return None if end is None else (start, end)

    def _scan_string(self, text, start, depth):
        if depth > 32:
            return None
        for form in self.forms:
            opened = form.opener.match(text, start)
            if opened is not None:
                return self._scan_body(text, opened.end(), form, depth)
        return None

    def _scan_body(self, text, index, form, depth):
        length = len(text)
        while index < length:
            if form.interpolation and text.startswith(form.interpolation, index):
                if form.doubled_brace_is_text and text.startswith("{{", index):
                    index += 2
                    continue
                index = self._scan_code(
                    text, index + len(form.interpolation), form.interpolation_close, depth
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

    def _scan_code(self, text, index, closer, depth):
        stack = [closer]
        length = len(text)
        while index < length:
            char = text[index]
            nested = self._scan_string(text, index, depth + 1)
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
        return None


def _literal(value):
    return RegexLiteral(value) if isinstance(value, str) else value


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
_REGEX_LITERAL = (
    r"(?<=(?:(?m:^)|[=(,:\[!&|?{};+\-*%<>~^]|\b(?:return|typeof|case|do|else|in|instanceof"
    r"|new|void|delete|throw|yield|await))[ \t]*)"
    r"/(?![/*])(?:\\.|\[(?:\\.|[^\]\\\r\n])*\]|[^/\\\r\n\[])+/[A-Za-z]*"
)

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
    "tsql": _rules("'\"", literals=(r"\[(?:\]\]|[^\]\r\n])*\]",), starts="["),
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
            r"(?m)(?<=^[ \t]{0,3})(`{3,}|~{3,})[^\r\n]*(?:\r?\n|\r)"
            r"[\s\S]*?^[ \t]{0,3}\1[`~]*[ \t]*$",
            r"(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)",
        ),
        starts="`~",
    ),
}


def lexical_rules_for(language: str) -> LexicalRules:
    """Return literal rules for a registry language key such as ``c++``."""

    key = language.strip().lower()
    rules = _LEXICAL_RULES.get(key)
    if rules is None:
        rules = _LEXICAL_RULES.get(re.sub(r"[^a-z0-9]+", "_", key).strip("_"))
    if rules is None:
        syntax = LANGUAGE_SYNTAX.get(key)
        rules = _MARKUP if syntax is not None and syntax.family_name == _MARKUP_FAMILY else None
    return _DEFAULT_RULES if rules is None else rules


_DEFAULT_RULES = LexicalRules()
