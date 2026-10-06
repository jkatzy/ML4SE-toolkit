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

DEFAULT_QUOTE_CHARS = frozenset("'\"`")


@dataclass(frozen=True)
class LexicalRules:
    """Literal syntax used to protect non-comment source ranges.

    Attributes:
        quote_chars: Characters that open a simple single-line quoted string
            with backslash escapes.
        literals: Compiled patterns tried, in order, at each candidate start
            before simple quote scanning. A match protects its whole span.
        literal_start_chars: Characters at which ``literals`` may start.
        non_string_quote: Optional pattern; when it matches at a quote
            character, that character does not open a string (for example a
            postfix transpose operator).
    """

    quote_chars: frozenset = DEFAULT_QUOTE_CHARS
    literals: Tuple["re.Pattern", ...] = ()
    literal_start_chars: frozenset = frozenset()
    non_string_quote: Optional["re.Pattern"] = None


def _rules(quote_chars="'\"`", literals=(), starts="", non_string_quote=None):
    return LexicalRules(
        quote_chars=frozenset(quote_chars),
        literals=tuple(re.compile(pattern) for pattern in literals),
        literal_start_chars=frozenset(starts),
        non_string_quote=None if non_string_quote is None else re.compile(non_string_quote),
    )


# A Haskell/ML-style character literal: one character or one escape.
_ML_CHAR_LITERAL = (
    r"'(?:\\(?:[0-9]+|x[0-9a-fA-F]+|o[0-7]+|u\{?[0-9a-fA-F]+\}?|\^.|[A-Z]{2,3}|[^\r\n])"
    r"|[^'\\\r\n])'"
)
_TEMPLATE_LITERAL = r"`(?:\\[\s\S]|[^`\\])*`"
_FSHARP_LITERALS = (r'"""[\s\S]*?"""', r'@"(?:""|[^"])*"', _ML_CHAR_LITERAL)
_CSHARP_LITERALS = (r'"""[\s\S]*?"""', r'\$?@\$?"(?:""|[^"])*"')
_DART_LITERALS = (
    r"(?<![\w$])r'{3}[\s\S]*?'{3}",
    r'(?<![\w$])r"{3}[\s\S]*?"{3}',
    r"(?<![\w$])r'[^'\r\n]*'",
    r'(?<![\w$])r"[^"\r\n]*"',
    r"'{3}[\s\S]*?(?<!\\)'{3}",
    r'"{3}[\s\S]*?(?<!\\)"{3}',
)
_TRANSPOSE = r"(?<=[\w)\]}.'])'"
# ECMA-262 12.9.5: a / after an operator, punctuator, or keyword (not after an
# operand) starts a RegularExpressionLiteral.
_REGEX_LITERAL = (
    r"(?<=(?:(?m:^)|[=(,:\[!&|?{};+\-*%<>~^]|\b(?:return|typeof|case|do|else|in|instanceof"
    r"|new|void|delete|throw|yield|await))[ \t]*)"
    r"/(?![/*])(?:\\.|\[(?:\\.|[^\]\\\r\n])*\]|[^/\\\r\n\[])+/[A-Za-z]*"
)

_HASKELL = _rules('"', literals=(_ML_CHAR_LITERAL,), starts="'")
_LISP = _rules('"', literals=(r"#\\(?:[A-Za-z][A-Za-z0-9-]*|[\s\S])",), starts="#")
_FSHARP = _rules('"', literals=_FSHARP_LITERALS, starts="\"@'")
_ECMASCRIPT = _rules("'\"", literals=(_TEMPLATE_LITERAL, _REGEX_LITERAL), starts="`/")
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
    "julia": _rules("'\"", non_string_quote=_TRANSPOSE),
    # Erlang reference 3.2: $c character literals.
    "erlang": _rules(
        "'\"",
        literals=(r"\$(?:\\(?:[0-7]{1,3}|x\{[0-9a-fA-F]+\}|x[0-9a-fA-F]{2}|\^.|[\s\S])|[\s\S])",),
        starts="$",
    ),
    # Elixir: ?c code point literals.
    "elixir": _rules("'\"", literals=(r"(?<![\w?!])\?(?:\\[\s\S]|[^\s\\])",), starts="?"),
    # ISO Prolog 6.4.4: 0'c character code constants.
    "prolog": _rules("'\"`", literals=(r"(?<![\w])0'(?:''|\\[\s\S]|[^\r\n])",), starts="0"),
    # Ruby: ?c character literals and %w/%i/%q percent literals.
    "ruby": _rules(
        "'\"`",
        literals=(
            r"(?<![\w?!)\]}])\?(?:\\[\s\S]|[^\s\\])(?!\w)",
            r"%[wWiIqQ]?\((?:\\[\s\S]|[^()\\])*\)",
            r"%[wWiIqQ]?\[(?:\\[\s\S]|[^\[\]\\])*\]",
            r"%[wWiIqQ]?\{(?:\\[\s\S]|[^{}\\])*\}",
            r"%[wWiIqQ]?<(?:\\[\s\S]|[^<>\\])*>",
        ),
        starts="?%",
    ),
    # perlop "Quote and Quote-like Operators": # may delimit q, qq, qw, qr, qx,
    # m, s, tr, and y when it follows the operator name immediately.
    "perl": _rules(
        "'\"`",
        literals=(
            r"(?<![\w$@%&])(?:s|tr|y)#(?:\\[\s\S]|[^#\\])*#(?:\\[\s\S]|[^#\\])*#[A-Za-z]*",
            r"(?<![\w$@%&])(?:qq|qw|qr|qx|q|m)#(?:\\[\s\S]|[^#\\])*#[A-Za-z]*",
        ),
        starts="stymq",
    ),
    # TeXbook ch. 7: \c is a control symbol, so \% is not a comment.
    "tex": _rules("", literals=(r"\\[\s\S]",), starts="\\"),
    # GNU make manual 3.1: \# is a literal hash.
    "makefile": _rules("'\"`", literals=(r"\\#",), starts="\\"),
    # PowerShell about_Quoting_Rules: backtick escapes, doubled '', here-strings.
    "powershell": _rules(
        "",
        literals=(
            r'@"[^\S\r\n]*\r?\n[\s\S]*?\r?\n"@',
            r"@'[^\S\r\n]*\r?\n[\s\S]*?\r?\n'@",
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
    "swift": _rules("'\"`", literals=(r'#*"{3}[\s\S]*?"{3}#*',), starts='#"'),
    # C# spec 6.4.5.6: verbatim and raw string literals.
    "c#": _CSHARP,
    "c_sharp": _CSHARP,
    "csharp": _CSHARP,
    # Dart spec 17.7: raw strings have no escapes; triple quotes span lines.
    "dart": _rules("'\"`", literals=_DART_LITERALS, starts="r'\""),
    # TOML 1.0: multi-line basic and literal strings.
    "toml": _rules(
        "'\"", literals=(r'"{3}[\s\S]*?"{3}(?!")', r"'{3}[\s\S]*?'{3}(?!')"), starts="\"'"
    ),
    # XML 1.0 2.7: CDATA sections are character data.
    "xml": _rules("'\"`", literals=(r"<!\[CDATA\[[\s\S]*?\]\]>",), starts="<"),
}


def lexical_rules_for(normalized_language: str) -> LexicalRules:
    """Return literal rules for a normalized registry language key."""

    return _LEXICAL_RULES.get(normalized_language, _DEFAULT_RULES)


_DEFAULT_RULES = LexicalRules()
