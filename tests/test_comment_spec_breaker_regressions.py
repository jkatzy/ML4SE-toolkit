"""Spec-derived breaker regressions for comment extraction and cleaning.

Every case in this module was written from a language specification or a
language-independent comment contract, reproduced against the extractor or
sanitizer, and minimized. Expected values come from the cited language
contract, never from parser output.

Cases whose defect is still open are listed in ``_OPEN_CASES`` and run as
strict ``xfail``: the suite stays green while the defect is open and fails as
soon as a fix makes the case pass, at which point the entry is removed.
"""

import time
from dataclasses import dataclass

import pytest

from ml4setk import CommentQuery, sanitize_comment
from ml4setk.Parsing.Comments import iter_comment_syntaxes

pytestmark = pytest.mark.unit


def _matches(language, source):
    return [match.match for match in CommentQuery(language).parse(source)]


def _open_defect(reason):
    return pytest.mark.xfail(reason=reason, strict=True)


# Shared reasons for the open third-iteration real-code cases.
_APOSTROPHE_NOT_STRING = (
    "The fallback quote scanner pairs apostrophes that this language uses as "
    "primes, transposes, or text."
)
_MULTILINE_STRING = "Protected ranges for this string form stop at the physical line."
_LITERAL_FORM = "This language-specific literal form does not protect comment markers."
_REGEX_LITERAL = "Regular-expression literals do not protect comment markers."
_TEMPLATE_TEXT = "Template, markup, or verbatim text is scanned as code."
_MARKER_POSITION = "The marker starts a comment only at a line, word, token, or command start."
_MISSING_FORM = "This documented comment form is absent from the registry."
_LONE_CR = "A lone CR does not end the line comment."
_NEWER_RULES_NOT_IMPLEMENTED = (
    "The newer version's comment rules read every valid older program the same "
    "way, so no version flag is needed, but the registry still implements the "
    "older or incomplete rules."
)

# Case id -> reason for defects that are confirmed but not fixed yet.
_OPEN_CASES = {
    "lua-cr-terminates-comment": (
        "Lua keeps its legacy published slices; see "
        "test_lua_legacy_crlf_comment_slice_preserves_carriage_return."
    ),
    **dict.fromkeys(
        (
            "standard-ml-primed-binding",
            "isabelle-primed-name",
            "mathematica-derivative",
            "scilab-transpose",
            "yaml-sequence-plain-scalar-apostrophe",
            "yaml-mapping-plain-scalar-apostrophe",
            "jsx-text-apostrophe",
            "tsx-text-apostrophe",
        ),
        _APOSTROPHE_NOT_STRING,
    ),
    **dict.fromkeys(
        (
            "scala-triple-quoted-string",
            "groovy-triple-quoted-string",
            "gdscript-triple-quoted-string",
            "meson-multiline-string",
            "elixir-charlist-heredoc",
            "ruby-multiline-single-quoted-string",
            "r-multiline-string",
            "sql-multiline-string",
            "common-lisp-multiline-string",
        ),
        _MULTILINE_STRING,
    ),
    **dict.fromkeys(
        (
            "perl-q-brace-string",
            "ruby-nested-interpolation",
            "plsql-q-quoted-string",
            "groovy-dollar-slashy-string",
            "rebol-braced-string",
            "red-braced-string",
            "abap-string-template",
            "postscript-parenthesized-string",
            "bibtex-braced-field-value",
            "bibtex-escaped-percent-in-field",
            "m4-quoted-hash",
            "ocaml-quoted-string-literal",
        ),
        _LITERAL_FORM,
    ),
    **dict.fromkeys(
        (
            "ruby-slash-regex-literal",
            "perl-slash-substitution",
            "perl-qr-regex",
            "awk-regex-pattern",
            "awk-match-operator-regex",
            "coffeescript-regex-literal",
        ),
        _REGEX_LITERAL,
    ),
    **dict.fromkeys(
        (
            "html-textarea-rcdata",
            "vue-template-url-text",
            "jsx-text-url",
            "astro-template-url-text",
            "asciidoc-listing-block",
        ),
        _TEMPLATE_TEXT,
    ),
    **dict.fromkeys(
        (
            "nginx-hash-inside-token",
            "ninja-hash-inside-variable-value",
            "apacheconf-hash-inside-directive",
            "desktop-entry-hash-in-value",
            "debian-control-hash-in-field",
            "rpm-spec-source-url-fragment",
            "gherkin-hash-in-step",
            "cucumber-hash-in-step",
            "asciidoc-url-in-paragraph",
            "java-properties-continuation-line",
            "jinja-double-hash-is-text",
            "html-django-double-hash-is-text",
        ),
        _MARKER_POSITION,
    ),
    **dict.fromkeys(
        (
            "sas-star-comment-ends-at-semicolon",
            "sas-star-comment-after-statement",
            "sas-star-comment-spans-lines",
        ),
        "SAS * comment statements may start any statement and end at the semicolon.",
    ),
    **dict.fromkeys(
        (
            "puppet-c-style-block-comment",
            "lfe-block-comment",
            "scheme-nested-block-comment",
            "autoit-long-form-comment-block",
            "html-django-comment-tag",
            "html-erb-html-comment",
            "saltstack-jinja-comment",
        ),
        _MISSING_FORM,
    ),
    "odin-nested-block-comment": (
        "Odin block comments nest, but odin still uses non-nesting c_style blocks."
    ),
    "haskell-dash-arrow-operator": (
        "Only the --> prefix is excluded; ---> is also an operator lexeme."
    ),
    **dict.fromkeys(
        (
            "plpgsql-lone-cr-line-ending",
            "ada-lone-cr-line-ending",
            "nim-lone-cr-line-ending",
        ),
        _LONE_CR,
    ),
    **dict.fromkeys(
        ("python-triple-quoted-assignment", "python-triple-quoted-call-argument"),
        "The hash_style family reports every triple-quoted string, not only docstrings.",
    ),
    **dict.fromkeys(
        (
            "rst-admonition-directive",
            "rst-code-block-directive",
            "rst-hyperlink-target",
            "rst-image-directive",
        ),
        "Directives and hyperlink targets match the .. comment pattern.",
    ),
    "matlab-doubled-quote-string": (
        "Regression: transpose detection reads the doubled quote in 'it''s' as a "
        "transpose, exposing the % inside the character vector."
    ),
    **dict.fromkeys(
        (
            "javascript-es2023-hashbang-comment",
            "typescript-shebang-trivia",
            "python-312-fstring-field-comment",
            "makefile-43-hash-inside-function-call",
            "rpm-415-dnl-comment",
            "handlebars-3-whitespace-control-comment",
            "mini-yaml-escaped-hash",
            "twig-315-inline-expression-comment",
            "openedge-116-line-comment",
            "mirc-61-block-comment",
            "fortran-fixed-form-column-one-comments",
            "factor-bang-inside-word",
        ),
        _NEWER_RULES_NOT_IMPLEMENTED,
    ),
}


def _with_open_marks(params):
    """Apply strict xfail marks to cases listed in ``_OPEN_CASES``."""

    return [
        pytest.param(*param.values, id=param.id, marks=_open_defect(_OPEN_CASES[param.id]))
        if param.id in _OPEN_CASES
        else param
        for param in params
    ]


# ---------------------------------------------------------------------------
# Hand-written extraction cases. Each row is (language, source, expected exact
# comment slices, specification reference).
# ---------------------------------------------------------------------------

_LINE_COMMENT_HIDDEN_BY_LEXICAL_APOSTROPHE = [
    pytest.param(
        "haskell",
        "f' = 1 -- don't\n",
        ["-- don't"],
        "Haskell 2010 Report 2.4: varid characters include the prime (').",
        id="haskell-primed-identifier",
    ),
    pytest.param(
        "elm",
        "f' = 1 -- don't\n",
        ["-- don't"],
        "Elm identifiers do not use quotes, but the generic scanner pairs the prime "
        "in f' with the apostrophe in the comment exactly as for Haskell.",
        id="elm-primed-identifier",
    ),
    pytest.param(
        "purescript",
        "f' = 1 -- don't\n",
        ["-- don't"],
        "PureScript identifiers may contain primes (Haskell-derived lexer).",
        id="purescript-primed-identifier",
    ),
    pytest.param(
        "fsharp",
        "let f' = 1 // it's\n",
        ["// it's"],
        "F# spec 3.4: ident-char includes the apostrophe.",
        id="fsharp-primed-identifier",
    ),
    pytest.param(
        "ocaml",
        "type 'a t (* the element's type *)\n",
        ["(* the element's type *)"],
        "OCaml manual 11.4: type variables are written 'ident.",
        id="ocaml-type-variable",
    ),
    pytest.param(
        "emacs_lisp",
        "(setq x 'foo) ; don't\n",
        ["; don't"],
        "Emacs Lisp manual 10.3: 'object is shorthand for (quote object).",
        id="emacs-lisp-quote",
    ),
    pytest.param(
        "common_lisp",
        "(setq x 'foo) ; it's\n",
        ["; it's"],
        "CLHS 2.4.3: the single-quote reader macro.",
        id="common-lisp-quote",
    ),
    pytest.param(
        "scheme",
        "(define x 'y) ; it's\n",
        ["; it's"],
        "R7RS 4.1.2: 'datum is shorthand for (quote datum).",
        id="scheme-quote",
    ),
    pytest.param(
        "clojure",
        "(def x 'y) ; it's\n",
        ["; it's"],
        "Clojure reader: 'form is (quote form).",
        id="clojure-quote",
    ),
    pytest.param(
        "racket",
        "(define x 'y) ; it's\n",
        ["; it's"],
        "Racket reference 1.3.8: reading quotes.",
        id="racket-quote",
    ),
    pytest.param(
        "verilog",
        "assign x = 4'b1010; // it's\n",
        ["// it's"],
        "IEEE 1364-2005 3.5.1: sized numbers use size'base_format.",
        id="verilog-sized-number",
    ),
    pytest.param(
        "systemverilog",
        "assign x = 4'b1010; // it's\n",
        ["// it's"],
        "IEEE 1800-2017 5.7.1: sized integer literals.",
        id="systemverilog-sized-number",
    ),
    pytest.param(
        "vhdl",
        "x <= a'length; -- it's\n",
        ["-- it's"],
        "IEEE 1076 16: predefined attributes are written prefix'designator.",
        id="vhdl-attribute",
    ),
    pytest.param(
        "ada",
        "X := A'Length; -- it's\n",
        ["-- it's"],
        "Ada RM 4.1.4: attribute_reference ::= prefix'attribute_designator.",
        id="ada-attribute",
    ),
    pytest.param(
        "matlab",
        "y = x'; % it's\n",
        ["% it's"],
        "MATLAB: postfix ' is the complex conjugate transpose operator.",
        id="matlab-transpose",
    ),
    pytest.param(
        "julia",
        "y = x' # it's\n",
        ["# it's"],
        "Julia manual: postfix ' is the adjoint operator.",
        id="julia-adjoint",
    ),
    pytest.param(
        "erlang",
        "X = $', % it's\n",
        ["% it's"],
        "Erlang reference 3.2: $char is a character literal.",
        id="erlang-char-literal-quote",
    ),
    pytest.param(
        "elixir",
        "x = ?' # it's\n",
        ["# it's"],
        "Elixir syntax reference: ?char is a code point literal.",
        id="elixir-codepoint-quote",
    ),
    pytest.param(
        "prolog",
        "X = 0'a, % it's\n",
        ["% it's"],
        "ISO Prolog 6.4.4: 0'char is a character code constant.",
        id="prolog-char-code",
    ),
    pytest.param(
        "dart",
        "var s = r'\\'; // it's\n",
        ["// it's"],
        "Dart spec 17.7: backslash is not an escape inside a raw string r'...'.",
        id="dart-raw-string-backslash",
    ),
    pytest.param(
        "javascript",
        "const re = /'/; // it's\n",
        ["// it's"],
        "ECMA-262 12.9.5: a quote inside a RegularExpressionLiteral is not a string.",
        id="javascript-regex-literal",
    ),
    pytest.param(
        "c",
        "int x; /* don't */ y = 1; // won't\n",
        ["/* don't */", "// won't"],
        "C11 6.4.9: comment contents are not examined for string delimiters.",
        id="c-apostrophes-in-two-comments",
    ),
]


@pytest.mark.parametrize(
    ("language", "source", "expected", "reference"),
    _with_open_marks(_LINE_COMMENT_HIDDEN_BY_LEXICAL_APOSTROPHE),
)
def test_apostrophe_syntax_does_not_hide_following_comment(language, source, expected, reference):
    assert reference
    assert _matches(language, source) == expected


_SPURIOUS_COMMENT_FROM_NON_COMMENT_SYNTAX = [
    pytest.param(
        "shell",
        "echo ${#arr[@]}\n",
        "POSIX XCU 2.3/2.6.2: # starts a comment only at the beginning of a word; "
        "${#parameter} is string length.",
        id="shell-parameter-length",
    ),
    pytest.param(
        "shell",
        "echo $#\n",
        "POSIX XCU 2.5.2: $# is the positional-parameter count.",
        id="shell-special-parameter",
    ),
    pytest.param(
        "shell",
        "x=a#b\n",
        "POSIX XCU 2.3 rule 9: # inside a word is not a comment.",
        id="shell-hash-inside-word",
    ),
    pytest.param(
        "dockerfile",
        "RUN echo a # b\n",
        "Dockerfile reference: a # marker anywhere other than line start is an argument.",
        id="dockerfile-inline-hash",
    ),
    pytest.param(
        "perl",
        "$x =~ s#a#b#;\n",
        "perlop 'Quote and Quote-like Operators': any non-whitespace delimiter, "
        "including #, may delimit s///.",
        id="perl-hash-delimited-substitution",
    ),
    pytest.param(
        "perl",
        "my $n = $#{$r};\n",
        "perldata: $#{expr} is the last index of an array reference.",
        id="perl-last-index-of-array-ref",
    ),
    pytest.param(
        "ruby",
        "c = ?#\n",
        "Ruby syntax/literals: ?# is a one-character string literal.",
        id="ruby-character-literal",
    ),
    pytest.param(
        "ruby",
        "a = %w(# b)\n",
        "Ruby syntax/literals: %w() is a word-array literal.",
        id="ruby-percent-word-array",
    ),
    pytest.param(
        "haskell",
        "a --+ b\n",
        "Haskell 2010 Report 2.3: dashes that form part of a legal lexeme such as "
        "--+ do not begin a comment.",
        id="haskell-dash-operator",
    ),
    pytest.param(
        "haskell",
        "a |-- b\n",
        "Haskell 2010 Report 2.3: '|--' is a legal lexeme, not a comment.",
        id="haskell-pipe-dash-operator",
    ),
    pytest.param(
        "erlang",
        "X = $%,\n",
        "Erlang reference 3.2: $% is a character literal.",
        id="erlang-percent-char-literal",
    ),
    pytest.param(
        "elixir",
        "x = ?#\n",
        "Elixir syntax reference: ?# is a code point literal.",
        id="elixir-hash-codepoint",
    ),
    pytest.param(
        "prolog",
        "X = 0'%,\n",
        "ISO Prolog 6.4.4: 0'% is a character code constant.",
        id="prolog-percent-char-code",
    ),
    pytest.param(
        "tex",
        "50\\% done\n",
        "TeXbook ch. 7: \\% is a control symbol, not a comment character.",
        id="tex-escaped-percent",
    ),
    pytest.param(
        "powershell",
        '$s = "a`"# b"\n',
        "about_Quoting_Rules: backtick escapes a double quote inside a double-quoted string.",
        id="powershell-backtick-escaped-quote",
    ),
    pytest.param(
        "clojure",
        "(str \\;)\n",
        "Clojure reader: \\; is a character literal.",
        id="clojure-semicolon-char",
    ),
    pytest.param(
        "scheme",
        "(display #\\;)\n",
        "R7RS 6.6: #\\; is a character literal.",
        id="scheme-semicolon-char",
    ),
    pytest.param(
        "common_lisp",
        "(print #\\;)\n",
        "CLHS 2.4.8.1: #\\; is a character object.",
        id="common-lisp-semicolon-char",
    ),
    pytest.param(
        "racket",
        "(display #\\;)\n",
        "Racket reference 1.3.14: #\\; is a character literal.",
        id="racket-semicolon-char",
    ),
    pytest.param(
        "emacs_lisp",
        "(insert ?\\;)\n",
        "Emacs Lisp manual 2.4.3.1: ?\\; is a character literal.",
        id="emacs-lisp-semicolon-char",
    ),
    pytest.param(
        "go",
        "s := `\n// not\n`\n",
        "Go spec 'String literals': raw string literals may span lines.",
        id="go-multiline-raw-string",
    ),
    pytest.param(
        "javascript",
        "const s = `\n// not\n`;\n",
        "ECMA-262 12.9.6: template literals may span lines.",
        id="javascript-multiline-template",
    ),
    pytest.param(
        "typescript",
        "const s = `\n// not\n`;\n",
        "TypeScript inherits ECMAScript template literals.",
        id="typescript-multiline-template",
    ),
    pytest.param(
        "java",
        'String s = """\n  // not\n  """;\n',
        "JLS 3.10.6: text blocks span lines.",
        id="java-text-block",
    ),
    pytest.param(
        "swift",
        'let s = """\n// not\n"""\n',
        "Swift reference 'String Literals': multiline string literals.",
        id="swift-multiline-string",
    ),
    pytest.param(
        "csharp",
        'var s = @"\n// not\n";\n',
        "C# spec 6.4.5.6: verbatim string literals may span lines.",
        id="csharp-verbatim-string",
    ),
    pytest.param(
        "toml",
        'a = """\n# not\n"""\n',
        "TOML 1.0 'String': multi-line basic strings.",
        id="toml-multiline-string",
    ),
    pytest.param(
        "xml",
        "<a><![CDATA[ <!-- not --> ]]></a>\n",
        "XML 1.0 2.7: CDATA section content is character data, not markup.",
        id="xml-cdata-section",
    ),
]


@pytest.mark.parametrize(
    ("language", "source", "reference"),
    _with_open_marks(_SPURIOUS_COMMENT_FROM_NON_COMMENT_SYNTAX),
)
def test_comment_marker_inside_non_comment_syntax_is_ignored(language, source, reference):
    assert reference
    assert _matches(language, source) == []


_WRONG_COMMENT_BOUNDARIES = [
    pytest.param(
        "perl",
        "my $n = $#arr; # it's\n",
        ["# it's"],
        "perldata: $#array is the last index; only the second # is a comment.",
        id="perl-last-index-before-comment",
    ),
    pytest.param(
        "tex",
        "x\\% y % it's\n",
        ["% it's"],
        "TeXbook ch. 7: \\% is a control symbol; the comment starts at the bare %.",
        id="tex-escaped-percent-before-comment",
    ),
    pytest.param(
        "makefile",
        "x = a\\#b # real\n",
        ["# real"],
        "GNU make manual 3.1: a backslash-escaped # does not start a comment.",
        id="makefile-escaped-hash",
    ),
    pytest.param(
        "c",
        "// a \\\nint hidden;\nint x;\n",
        ["// a \\\nint hidden;"],
        "C11 5.1.1.2: line splicing (phase 2) precedes comment removal (phase 3).",
        id="c-line-splice-continues-comment",
    ),
    pytest.param(
        "php",
        "<?php // note ?> <b>html</b>\n",
        ["// note "],
        "PHP manual 'Comments': one-line comments end at the line or at ?>, whichever comes first.",
        id="php-close-tag-ends-line-comment",
    ),
    pytest.param(
        "php",
        "<?php\n$x = 1; # note\n",
        ["# note"],
        "PHP manual 'Comments': # is a shell-style one-line comment.",
        id="php-hash-comment",
    ),
    pytest.param(
        "ocaml",
        '(* "*)" *)\nlet x = 1\n',
        ['(* "*)" *)'],
        "OCaml lexer: string literals are lexed inside comments, so a quoted *) "
        "does not close the comment.",
        id="ocaml-string-inside-comment",
    ),
    pytest.param(
        "scala",
        "/* a /* b */ c */ x\n",
        ["/* a /* b */ c */"],
        "Scala spec 1.4: multi-line comments may be nested.",
        id="scala-nested-block",
    ),
    pytest.param(
        "swift",
        "/* a /* b */ c */ x\n",
        ["/* a /* b */ c */"],
        "Swift reference 'Lexical Structure': multiline comments can be nested.",
        id="swift-nested-block",
    ),
    pytest.param(
        "dart",
        "/* a /* b */ c */ x\n",
        ["/* a /* b */ c */"],
        "Dart spec 21.1.2: multi-line comments may nest.",
        id="dart-nested-block",
    ),
    pytest.param(
        "plpgsql",
        "/* a /* b */ c */ SELECT 1\n",
        ["/* a /* b */ c */"],
        "PostgreSQL docs 4.1.5: C-style block comments can be nested.",
        id="plpgsql-nested-block",
    ),
    pytest.param(
        "d",
        "int x; // note\n",
        ["// note"],
        "D spec 'Lexical': // line comments.",
        id="d-line-comment",
    ),
    pytest.param(
        "d",
        "/* a */ x\n",
        ["/* a */"],
        "D spec 'Lexical': /* */ block comments.",
        id="d-block-comment",
    ),
    pytest.param(
        "d",
        "/+ a /+ b +/ c +/ x\n",
        ["/+ a /+ b +/ c +/"],
        "D spec 'Lexical': /+ +/ comments nest.",
        id="d-nesting-comment",
    ),
    pytest.param(
        "python",
        "x = 1 # a\rprint(x)\r",
        ["# a"],
        "Python reference 2.1.2: CR alone is a line terminator.",
        id="python-cr-terminates-comment",
    ),
    pytest.param(
        "haskell",
        "x = 1 -- a\ry = 2\r",
        ["-- a"],
        "Haskell 2010 Report 2.2: newline -> return linefeed | return | linefeed.",
        id="haskell-cr-terminates-comment",
    ),
    pytest.param(
        "lua",
        "x = 1 -- a\ry = 2\r",
        ["-- a"],
        "Lua llex.c currIsNewline: CR terminates a short comment.",
        id="lua-cr-terminates-comment",
    ),
    pytest.param(
        "python",
        "x = 1 # a\r\nprint(x)\r\n",
        ["# a"],
        "Python reference 2.1.2: CRLF is one terminator, so CR is not comment text.",
        id="python-crlf-excludes-cr",
    ),
    pytest.param(
        "ruby",
        "x = 1 # a\r\ny\r\n",
        ["# a"],
        "Ruby lexer treats CRLF as a newline; CR is not comment text.",
        id="ruby-crlf-excludes-cr",
    ),
    pytest.param(
        "sql",
        "SELECT 1 -- a\r\nFROM t\r\n",
        ["-- a"],
        "ISO SQL <simple comment> ends at <newline>; CRLF is one newline.",
        id="sql-crlf-excludes-cr",
    ),
]


@pytest.mark.parametrize(
    ("language", "source", "expected", "reference"), _with_open_marks(_WRONG_COMMENT_BOUNDARIES)
)
def test_comment_boundaries_follow_language_contract(language, source, expected, reference):
    assert reference
    assert _matches(language, source) == expected


# ---------------------------------------------------------------------------
# Hand-written sanitizer cases: cleaning must not discard comment content.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("language", "raw_comment", "expected"),
    _with_open_marks(
        [
            pytest.param(
                "classic_asp",
                "<!-- 'quoted' -->",
                "'quoted'",
                id="classic-asp-html-comment-keeps-leading-quote",
            ),
            pytest.param(
                "glyph",
                "# --verbose enables logging",
                "--verbose enables logging",
                id="glyph-keeps-command-line-flag",
            ),
            pytest.param("sql", "-- | a | b |", "| a | b |", id="sql-keeps-table-pipe"),
            pytest.param("ada", "-- | a | b |", "| a | b |", id="ada-keeps-table-pipe"),
            pytest.param("lua", "-- | a | b |", "| a | b |", id="lua-keeps-table-pipe"),
            pytest.param("vhdl", "-- | a | b |", "| a | b |", id="vhdl-keeps-table-pipe"),
            pytest.param("haskell", "-- | Haddock doc", "Haddock doc", id="haskell-haddock-marker"),
            pytest.param("glyph", "# -- note", "note", id="glyph-secondary-gutter"),
            pytest.param("php", "# note", "note", id="php-hash-wrapper"),
        ]
    ),
)
def test_sanitizer_preserves_content_edges(language, raw_comment, expected):
    assert sanitize_comment(language, raw_comment) == expected


# ---------------------------------------------------------------------------
# Generated cross-language cases. Comment bodies are arbitrary text in every
# registered language, so these oracles need no per-language syntax research.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _GeneratedCase:
    language: str
    source: str
    expected: tuple[str, ...]


def _registry_examples(syntax, language):
    yield from syntax.shared_regex_examples
    yield from syntax.shared_nested_examples
    if language == syntax.canonical_name:
        yield from syntax.canonical_regex_examples
        yield from syntax.canonical_nested_examples


def _single_line(example):
    return "\n" not in example.expected_match and "\r" not in example.expected_match


def _insert_apostrophe(comment):
    """Insert ``'s`` after a word near the middle of a comment body."""

    length = len(comment)
    for index in range(length // 3, 2 * length // 3 + 1):
        if index + 1 < length and comment[index].isalpha() and comment[index + 1] in " \t":
            return comment[: index + 1] + "'s" + comment[index + 1 :]
    return None


def _build_apostrophe_pair_cases():
    cases = []
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            example = next(
                (
                    example
                    for example in _registry_examples(syntax, language)
                    if example.kind in {"block", "nested"}
                    and example.inline_compatible
                    and not example.consumes_eof
                    and _single_line(example)
                ),
                None,
            )
            if example is None:
                continue
            comment = _insert_apostrophe(example.expected_match)
            if comment is None:
                continue
            cases.append(_GeneratedCase(language, f"x {comment} x {comment}\n", (comment, comment)))
    return cases


def _build_nested_opener_in_line_comment_cases():
    cases = []
    for syntax in iter_comment_syntaxes():
        if not syntax.nested_delimiters:
            continue
        opener, closer = syntax.nested_delimiters[0]
        for language in syntax.language_names:
            example = next(
                (
                    example
                    for example in _registry_examples(syntax, language)
                    if example.kind == "line"
                    and example.standalone_compatible
                    and _single_line(example)
                ),
                None,
            )
            if example is None:
                continue
            line_comment = f"{example.expected_match} see {opener} here"
            block_comment = f"{opener} real {closer}"
            cases.append(
                _GeneratedCase(
                    language,
                    f"{line_comment}\nx\n{block_comment}\n",
                    (line_comment, block_comment),
                )
            )
    return cases


@pytest.mark.parametrize("case", _build_apostrophe_pair_cases(), ids=lambda case: case.language)
def test_apostrophes_in_separate_comments_do_not_form_a_string(case):
    assert tuple(_matches(case.language, case.source)) == case.expected


@pytest.mark.parametrize(
    "case", _build_nested_opener_in_line_comment_cases(), ids=lambda case: case.language
)
def test_block_opener_inside_line_comment_does_not_hide_later_block(case):
    assert tuple(_matches(case.language, case.source)) == case.expected


def test_scenic_accepts_lone_surrogate_in_python_string():
    # Minimized from the seeded parser fuzz campaign (seed 0xC0FFEE, scenic case 0).
    assert _matches("scenic", "x = 1  # note \ud800\n") == ["# note \ud800"]


@pytest.mark.parametrize("language", ["scenic", "snakemake"])
def test_python_tokenized_comments_accept_lone_cr_before_non_ascii(language):
    # CPython's tokenizer raised UnicodeDecodeError on a lone CR followed by
    # non-ASCII text; Python reference 2.1.2 treats the CR as a line ending.
    source = "x = 1 # a\rж = 2 # b\n"

    assert _matches(language, source) == ["# a", "# b"]


@pytest.mark.parametrize(
    ("language", "source", "expected"),
    [
        pytest.param("matlab", "s = 'a % b'; % real\n", ["% real"], id="matlab-char-array"),
        pytest.param("julia", 's = "a # b" # real\n', ["# real"], id="julia-string"),
        pytest.param("haskell", 's = "a -- b" -- real\n', ["-- real"], id="haskell-string"),
        pytest.param("haskell", "c = '\"' -- real\n", ["-- real"], id="haskell-quote-char"),
        pytest.param("scheme", '(display "a ; b") ; real\n', ["; real"], id="scheme-string"),
        pytest.param("erlang", 'X = "a % b", % real\n', ["% real"], id="erlang-string"),
        pytest.param("tex", "a \\\\% real\n", ["% real"], id="tex-escaped-backslash"),
        pytest.param("go", "s := `a // b` // real\n", ["// real"], id="go-raw-string"),
        pytest.param("shell", "echo a; # real\n", ["# real"], id="shell-after-operator"),
        pytest.param("dockerfile", "  # real\nRUN x\n", ["# real"], id="dockerfile-indented"),
        pytest.param("javascript", "x = a / b / c; // real\n", ["// real"], id="js-division"),
        pytest.param("perl", "print $s # real\n", ["# real"], id="perl-variable-then-comment"),
        pytest.param("php", "<?php\n#[Attr]\n// real\n", ["// real"], id="php-attribute"),
        pytest.param("c", "// a \\ b\nint x;\n", ["// a \\ b"], id="c-backslash-not-at-eol"),
        pytest.param("ocaml", "let c = '\"' (* real *)\n", ["(* real *)"], id="ocaml-quote-char"),
        pytest.param("d", "/++ doc /+ in +/ +/ x\n", ["/++ doc /+ in +/ +/"], id="d-nested-doc"),
        pytest.param(
            "tsql", "/* a /* b */ c */ SELECT 1\n", ["/* a /* b */ c */"], id="tsql-nested"
        ),
    ],
)
def test_lexical_rules_keep_ordinary_literals_and_comments(language, source, expected):
    assert _matches(language, source) == expected


# ---------------------------------------------------------------------------
# Second breaker iteration: spec-derived cases (now fixed).
# ---------------------------------------------------------------------------

_ITERATION_2_CASES = [
    pytest.param(
        "javascript",
        "x = 1; // a\u2028y = 2; // b\n",
        ["// a", "// b"],
        "ECMA-262 12.3: U+2028 LINE SEPARATOR is a LineTerminator.",
        id="javascript-line-separator-ends-comment",
    ),
    pytest.param(
        "typescript",
        "x = 1; // a\u2029y = 2;\n",
        ["// a"],
        "TypeScript inherits ECMAScript LineTerminator, including U+2029.",
        id="typescript-paragraph-separator-ends-comment",
    ),
    pytest.param(
        "csharp",
        "x = 1; // a\u2028y = 2;\n",
        ["// a"],
        "C# spec 6.3.2: new_line includes U+2028.",
        id="csharp-line-separator-ends-comment",
    ),
    pytest.param(
        "csharp",
        "x = 1; // a\x85y = 2;\n",
        ["// a"],
        "C# spec 6.3.2: new_line includes U+0085.",
        id="csharp-next-line-ends-comment",
    ),
    pytest.param(
        "java",
        "int x; // a \\u000a int y; // b\n",
        ["// a ", "// b"],
        "JLS 3.3/3.4: Unicode escapes are translated before line terminators and comments.",
        id="java-unicode-escape-newline-ends-comment",
    ),
    pytest.param(
        "c++",
        "int n = 1'000; // it's\n",
        ["// it's"],
        "C++14 [lex.icon]: ' is a digit separator.",
        id="cpp-single-digit-separator",
    ),
    pytest.param(
        "c++",
        'auto s = R"x(a)" // b)x"; // real\n',
        ["// real"],
        'C++ [lex.string]: R"d( ... )d" ends only at )d".',
        id="cpp-raw-string-delimiter",
    ),
    pytest.param(
        "c++",
        'auto s = R"(\n// not\n)";\n',
        [],
        "C++ [lex.string]: raw strings may span lines.",
        id="cpp-multiline-raw-string",
    ),
    pytest.param(
        "javascript",
        'const s = `a ${"`"} // b`; // real\n',
        ["// real"],
        "ECMA-262 13.2.8: substitutions inside templates are expressions.",
        id="javascript-nested-template-backtick",
    ),
    pytest.param(
        "php",
        "<?php\n$s = <<<EOT\n# not\nEOT;\n",
        [],
        "PHP manual 'Heredoc': body text is string data.",
        id="php-heredoc",
    ),
    pytest.param(
        "php",
        "<?php\n$s = <<<'EOT'\n// not\nEOT;\n",
        [],
        "PHP manual 'Nowdoc': body text is string data.",
        id="php-nowdoc",
    ),
    pytest.param(
        "ruby",
        "s = <<~EOS\n  # not\nEOS\n",
        [],
        "Ruby syntax/literals 'Here Documents'.",
        id="ruby-squiggly-heredoc",
    ),
    pytest.param(
        "ruby",
        "__END__\n# data\n",
        [],
        "Ruby: __END__ at line start ends the program; the rest is DATA.",
        id="ruby-end-marker",
    ),
    pytest.param(
        "ruby",
        "r = %r{#}\n",
        [],
        "Ruby syntax/literals: %r{} regexp literal.",
        id="ruby-percent-regexp",
    ),
    pytest.param(
        "perl",
        'print <<"EOT";\n# not\nEOT\n',
        [],
        "perlop '<<EOF': here-document body is string data.",
        id="perl-heredoc",
    ),
    pytest.param(
        "perl",
        "=head1 NAME\n\nfoo\n\n=cut\n",
        ["=head1 NAME\n\nfoo\n\n=cut"],
        "perlpod: any =command paragraph at line start begins Pod, not only =pod.",
        id="perl-pod-head-command",
    ),
    pytest.param(
        "perl",
        "__END__\n# data\n",
        [],
        "perldata: __END__ ends the program text.",
        id="perl-end-marker",
    ),
    pytest.param(
        "shell",
        "echo don\\'t # it's\n",
        ["# it's"],
        "POSIX XCU 2.2.1: backslash quotes the next character outside quotes.",
        id="shell-escaped-apostrophe",
    ),
    pytest.param(
        "shell",
        "echo 'a\\' # c'\n",
        ["# c'"],
        "POSIX XCU 2.2.2: a backslash inside single quotes is literal.",
        id="shell-single-quote-has-no-escape",
    ),
    pytest.param(
        "shell",
        "cat <<EOF\n# not\nEOF\n",
        [],
        "POSIX XCU 2.7.4: here-document lines are data.",
        id="shell-heredoc",
    ),
    pytest.param(
        "plpgsql",
        "SELECT $$ -- not $$;\n",
        [],
        "PostgreSQL 4.1.2.4: dollar-quoted string constants.",
        id="plpgsql-dollar-quote",
    ),
    pytest.param(
        "plpgsql",
        "SELECT $fn$ /* not */ $fn$;\n",
        [],
        "PostgreSQL 4.1.2.4: tagged dollar quotes.",
        id="plpgsql-tagged-dollar-quote",
    ),
    pytest.param(
        "tsql",
        "SELECT [a--b] FROM t\n",
        [],
        "T-SQL 'Database identifiers': [ ] delimited identifiers.",
        id="tsql-bracket-identifier",
    ),
    pytest.param(
        "r",
        'x <- r"(a"#b)"\n',
        [],
        'R ?Quotes (R >= 4.0): raw strings r"(...)".',
        id="r-raw-string",
    ),
    pytest.param(
        "scss",
        "a { background: url(http://x.com/a.png); }\n",
        [],
        "Sass 'Special Functions': unquoted url() is parsed specially.",
        id="scss-unquoted-url",
    ),
    pytest.param(
        "less",
        "a { background: url(http://x.com/a.png); }\n",
        [],
        "Less parses url() arguments as URLs.",
        id="less-unquoted-url",
    ),
    pytest.param(
        "html",
        "<!--> a <!-- b -->\n",
        ["<!-->", "<!-- b -->"],
        "WHATWG HTML 13.2.5.43: '<!-->' emits an empty comment.",
        id="html-abrupt-empty-comment",
    ),
    pytest.param(
        "html",
        "<!-- a --!> b -->\n",
        ["<!-- a --!>"],
        "WHATWG HTML 13.2.5.52: '--!>' closes a comment.",
        id="html-bang-comment-close",
    ),
    pytest.param(
        "markdown",
        "```\n<!-- not -->\n```\n",
        [],
        "CommonMark 4.5: fenced code block content is literal text.",
        id="markdown-fenced-code",
    ),
    pytest.param(
        "vhdl",
        "/* a */ x <= 1;\n",
        ["/* a */"],
        "IEEE 1076-2008 15.9: delimited comments.",
        id="vhdl-2008-delimited-comment",
    ),
    pytest.param(
        "dart",
        "var s = '${'//'}'; // real\n",
        ["// real"],
        "Dart spec 17.7: interpolated expressions may contain strings.",
        id="dart-nested-interpolation-quote",
    ),
    pytest.param(
        "swift",
        'let s = "\\("//")" // real\n',
        ["// real"],
        "Swift reference: interpolated expressions may contain strings.",
        id="swift-nested-interpolation-quote",
    ),
    pytest.param(
        "swift",
        'let s = #"a "// b"# // real\n',
        ["// real"],
        'Swift reference: #"..."# raw strings end at "#.',
        id="swift-raw-string",
    ),
    pytest.param(
        "python",
        'f"{"#"}" # real\n',
        ["# real"],
        "PEP 701 (Python 3.12): f-string replacement fields may reuse the quote.",
        id="python-312-fstring-same-quote",
    ),
    pytest.param(
        "kotlin",
        'val s = "${"//"}" // real\n',
        ["// real"],
        "Kotlin grammar: ${} templates contain expressions, including strings.",
        id="kotlin-nested-template-string",
    ),
    pytest.param(
        "zig",
        "const s =\n    \\\\ // not a comment\n;\n",
        [],
        "Zig reference 'Multiline String Literals': \\\\ lines are string data.",
        id="zig-multiline-string",
    ),
    pytest.param(
        "fsharp",
        '(* "*)" *)\nlet x = 1\n',
        ['(* "*)" *)'],
        "F# spec 3.2: strings inside block comments are tokenized.",
        id="fsharp-string-inside-comment",
    ),
    pytest.param(
        "nix",
        "x = ''\n  # not\n'';\n",
        [],
        "Nix manual: ''...'' indented strings.",
        id="nix-indented-string",
    ),
    pytest.param(
        "hcl",
        "x = <<EOF\n# not\nEOF\n",
        [],
        "HCL native syntax spec: heredoc templates.",
        id="hcl-heredoc",
    ),
    pytest.param(
        "jsonnet",
        "x: |||\n  # not\n|||,\n",
        [],
        "Jsonnet spec: ||| text blocks.",
        id="jsonnet-text-block",
    ),
    pytest.param(
        "julia",
        's = """\n# not\n"""\n',
        [],
        "Julia manual: triple-quoted string literals.",
        id="julia-triple-quoted-string",
    ),
    pytest.param(
        "nim",
        's = """\n# not\n"""\n',
        [],
        "Nim manual: triple-quoted string literals.",
        id="nim-triple-quoted-string",
    ),
    pytest.param(
        "elixir",
        "x = ~r/#/\n",
        [],
        "Elixir sigils: ~r/.../.",
        id="elixir-regex-sigil",
    ),
    pytest.param(
        "elixir",
        "x = ~s(# not)\n",
        [],
        "Elixir sigils: ~s(...).",
        id="elixir-string-sigil",
    ),
    pytest.param(
        "common_lisp",
        "(print '|a;b|)\n",
        [],
        "CLHS 2.1.4.2: |...| multiple escape in symbols.",
        id="common-lisp-multiple-escape",
    ),
    pytest.param(
        "racket",
        "(display '|a;b|)\n",
        [],
        "Racket reference 1.3.2: |...| in symbols.",
        id="racket-bar-symbol",
    ),
    pytest.param(
        "scheme",
        "#;(foo bar) baz\n",
        ["#;(foo bar)"],
        "R7RS 2.2: #; comments out the next datum.",
        id="scheme-datum-comment",
    ),
    pytest.param(
        "racket",
        "#;(foo bar) baz\n",
        ["#;(foo bar)"],
        "Racket reference 1.3.9: #; datum comments.",
        id="racket-datum-comment",
    ),
    pytest.param(
        "matlab",
        "%{\n%{\ninner\n%}\nouter\n%}\nx = 1;\n",
        ["%{\n%{\ninner\n%}\nouter\n%}"],
        "MATLAB 'Comments': block comments can be nested.",
        id="matlab-nested-block-comment",
    ),
    pytest.param(
        "matlab",
        "x = 1; %{ not a block\ny = 2;\n",
        ["%{ not a block"],
        "MATLAB 'Comments': %{ opens a block only alone on its line.",
        id="matlab-inline-percent-brace-is-line-comment",
    ),
    pytest.param(
        "tcl",
        "set x #y\n",
        [],
        "Tcl(n) rule [10]: # starts a comment only where a command is expected.",
        id="tcl-hash-in-argument",
    ),
    pytest.param(
        "cmake",
        "set(x [=[ # not ]=])\n",
        [],
        "cmake-language(7): bracket arguments.",
        id="cmake-bracket-argument",
    ),
    pytest.param(
        "vim_script",
        'echo "hello"\n',
        [],
        'Vim :help :comment: " in a command argument is a string.',
        id="vim-echo-string",
    ),
    pytest.param(
        "tex",
        "\\verb|50%| done % real\n",
        ["% real"],
        "LaTeX manual \\verb: the argument is verbatim.",
        id="latex-verb",
    ),
    pytest.param(
        "tex",
        "\\begin{verbatim}\n% not\n\\end{verbatim}\n",
        [],
        "LaTeX manual: verbatim environment content is literal.",
        id="latex-verbatim-environment",
    ),
    pytest.param(
        "batchfile",
        "echo a & rem b\n",
        ["rem b"],
        "cmd /?: & separates commands; REM is a command.",
        id="batchfile-rem-after-ampersand",
    ),
    pytest.param(
        "ignore_list",
        "\ufeff# note\n*.log\n",
        ["# note"],
        "git dir.c add_patterns_from_buffer: skip_utf8_bom.",
        id="gitignore-utf8-bom",
    ),
]


@pytest.mark.parametrize(("language", "source", "expected", "reference"), _ITERATION_2_CASES)
def test_iteration_2_extraction_follows_language_contract(language, source, expected, reference):
    assert reference
    assert _matches(language, source) == expected


# Performance: each input is far smaller than real source files. These cases
# used to rescan to EOF from every opener; a linear scan finishes them in a few
# hundredths of a second, far under the budget.
_PARSE_BUDGET_SECONDS = 0.5


@pytest.mark.parametrize(
    ("language", "unit", "repeat"),
    [
        pytest.param(
            "leo",
            "/* ",
            2500,
            id="leo-many-unclosed-blocks",
        ),
        pytest.param(
            "c++",
            "// a \\\n",
            2500,
            id="cpp-long-line-splice-chain",
        ),
        pytest.param(
            "powershell",
            '@"\n ',
            8000,
            id="powershell-many-unclosed-here-strings",
        ),
        pytest.param(
            "lua",
            "--[[ ",
            12000,
            id="lua-many-unclosed-long-comments",
        ),
        pytest.param("c", "/* ", 7000, id="c-many-unclosed-blocks"),
        pytest.param("javascript", "` ", 20000, id="javascript-many-backticks"),
    ],
)
def test_adversarial_repetition_parses_within_budget(language, unit, repeat):
    source = unit * repeat
    query = CommentQuery(language)

    started = time.perf_counter()
    query.parse(source)
    elapsed = time.perf_counter() - started

    assert elapsed < _PARSE_BUDGET_SECONDS


# Guards for the iteration-2 lexical rules: each literal form stays narrow
# enough that ordinary comments around it are still extracted.
@pytest.mark.parametrize(
    ("language", "source", "expected"),
    [
        pytest.param("f#", "let f' = 1 // it's\n", ["// it's"], id="fsharp-alias-key"),
        pytest.param("c#", 'var p = @"C:\\"; // real\n', ["// real"], id="csharp-alias-key"),
        pytest.param("shell", 'echo "a # b" # real\n', ["# real"], id="shell-double-quotes"),
        pytest.param(
            "shell",
            "cat <<EOF # real\nbody # not\nEOF\necho hi # after\n",
            ["# real", "# after"],
            id="shell-heredoc-opener-line",
        ),
        pytest.param("shell", "x=$((1 << 2)) # real\n", ["# real"], id="shell-shift"),
        pytest.param(
            "ruby",
            "s = <<~EOS # real\n  # not\nEOS\nx = 1 # after\n",
            ["# real", "# after"],
            id="ruby-heredoc-opener-line",
        ),
        pytest.param("perl", "print 1 << 2; # real\n", ["# real"], id="perl-shift"),
        pytest.param("python", 'x = f"{v!r:>{w}}" # real\n', ["# real"], id="python-format-spec"),
        pytest.param("python", 's = f"{{#}}" # real\n', ["# real"], id="python-doubled-brace"),
        pytest.param("markdown", "It's <!-- c --> isn't\n", ["<!-- c -->"], id="markdown-prose"),
        pytest.param(
            "html", "<p>It's</p><!-- c --><p>isn't</p>\n", ["<!-- c -->"], id="html-prose"
        ),
        pytest.param(
            "html",
            '<p title="<!-- no -->">x</p><!-- real -->\n',
            ["<!-- real -->"],
            id="html-attribute-value",
        ),
        pytest.param("xml", "<a>It's</a><!-- c --><b>isn't</b>\n", ["<!-- c -->"], id="xml-prose"),
        pytest.param(
            "kotlin", 'val s = """a "quoted" b""" // real\n', ["// real"], id="kotlin-raw"
        ),
        pytest.param("plpgsql", "SELECT $1 -- real\n", ["-- real"], id="plpgsql-parameter"),
        pytest.param("tsql", "SELECT a[1] -- real\n", ["-- real"], id="tsql-subscript"),
        pytest.param("cmake", "set(x [y]) # real\n", ["# real"], id="cmake-plain-bracket"),
        pytest.param("matlab", "x = [1 2]'; % real\n", ["% real"], id="matlab-transpose"),
        pytest.param("vim_script", 'let x = "a" " real\n', ['" real'], id="vim-after-string"),
        pytest.param("tcl", "proc f {} { # real\n}\n", ["# real"], id="tcl-in-body"),
        pytest.param("batchfile", "echo (a) & rem real\n", ["rem real"], id="batch-after-paren"),
        pytest.param("racket", "(f #;x y) ; real\n", ["#;x", "; real"], id="racket-atom-datum"),
        pytest.param(
            "fsharp", "let m = (*) 2 3 // c\n(* b *)", ["// c", "(* b *)"], id="fsharp-op"
        ),
        pytest.param(
            "lua",
            "--[==[ a ]] b ]==] x --[[ c ]]\n",
            ["--[==[ a ]] b ]==]", "--[[ c ]]"],
            id="lua-levels",
        ),
    ],
)
def test_iteration_2_literal_rules_keep_surrounding_comments(language, source, expected):
    assert _matches(language, source) == expected


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        pytest.param('(* """*)""" *)\nlet x = 1\n', ['(* """*)""" *)'], id="triple-quoted"),
        pytest.param('(* @"*)" *)\nlet x = 1\n', ['(* @"*)" *)'], id="verbatim"),
        pytest.param(
            '(* @"a""*)" *)\nlet x = 1\n', ['(* @"a""*)" *)'], id="verbatim-doubled-quote"
        ),
        pytest.param(
            '(* @"C:\\" *) x (* y *)\n', ['(* @"C:\\" *)', "(* y *)"], id="verbatim-backslash"
        ),
        pytest.param("(* '\"' *) x\n", ["(* '\"' *)"], id="char-literal-quote"),
        pytest.param('let s = """(* not *)""" (* real *)\n', ["(* real *)"], id="code-triple"),
        pytest.param('(* "unclosed *)\n', [], id="unclosed-string-in-comment"),
    ],
)
def test_fsharp_strings_inside_block_comments_are_tokenized(source, expected):
    # F# spec 3.2: strings embedded within block comments are tokenized by the
    # string literal rules, so a closer inside them does not end the comment.
    assert _matches("fsharp", source) == expected


# ---------------------------------------------------------------------------
# Third breaker iteration: real-code audit. Each source is a small fragment of
# ordinary code in the target language; open cases are listed in _OPEN_CASES.
# ---------------------------------------------------------------------------

_ITERATION_3_CASES = [
    # Apostrophes that are primes, ticks, transposes, or text.
    pytest.param(
        "ocaml",
        "let x' = 1 (* it's *)\n",
        ["(* it's *)"],
        "OCaml manual 11.1: identifiers may contain '.",
        id="ocaml-primed-binding",
    ),
    pytest.param(
        "standard_ml",
        "val x' = 1 (* it's *)\n",
        ["(* it's *)"],
        "SML Definition 2.4: alphanumeric identifiers may contain '.",
        id="standard-ml-primed-binding",
    ),
    pytest.param(
        "isabelle",
        "lemma x': \"P\" (* it's *)\n",
        ["(* it's *)"],
        "Isabelle outer syntax: ' is a quasi-letter in identifiers.",
        id="isabelle-primed-name",
    ),
    pytest.param(
        "mathematica",
        "f'[x] (* it's *)\n",
        ["(* it's *)"],
        "Wolfram Language: f' is Derivative[1][f].",
        id="mathematica-derivative",
    ),
    pytest.param(
        "systemverilog",
        "assign x = 'b0; // it's\n",
        ["// it's"],
        "IEEE 1800 5.7.1: 'b0 is an unsized based number.",
        id="systemverilog-unsized-literal",
    ),
    pytest.param(
        "vhdl",
        "if clk'event and clk = '1' then -- it's\n",
        ["-- it's"],
        "IEEE 1076 16.2: clk'event is an attribute name; '1' is a character literal.",
        id="vhdl-attribute-then-char-literal",
    ),
    pytest.param(
        "ada",
        "X := T'(A => 1); -- it's\n",
        ["-- it's"],
        "Ada RM 4.7: T'(...) is a qualified expression.",
        id="ada-qualified-expression",
    ),
    pytest.param(
        "scilab",
        "x = a'; // it's\n",
        ["// it's"],
        "Scilab: postfix ' is the transpose operator.",
        id="scilab-transpose",
    ),
    pytest.param(
        "tex",
        "Don't do it. % it's\n",
        ["% it's"],
        "TeXbook ch. 7: only % (catcode 14) starts a comment; ' is text.",
        id="tex-prose-apostrophes",
    ),
    pytest.param(
        "yaml",
        "- don't # note\n- it's\n",
        ["# note"],
        "YAML 1.2 7.3.3: ' inside a plain scalar is content.",
        id="yaml-sequence-plain-scalar-apostrophe",
    ),
    pytest.param(
        "yaml",
        "msg: It's here # note\n",
        ["# note"],
        "YAML 1.2 7.3.3: ' inside a plain scalar is content.",
        id="yaml-mapping-plain-scalar-apostrophe",
    ),
    pytest.param(
        "jsx",
        "const el = <p>Don't panic</p>; // it's\n",
        ["// it's"],
        "JSX spec: JSXText is not a string literal.",
        id="jsx-text-apostrophe",
    ),
    pytest.param(
        "tsx",
        "const el = <p>Don't panic</p>; // it's\n",
        ["// it's"],
        "TSX follows JSX: JSXText is not a string literal.",
        id="tsx-text-apostrophe",
    ),
    pytest.param(
        "matlab",
        "s = 'it''s %not'; % note\n",
        ["% note"],
        "MATLAB: '' inside a character vector is an escaped quote.",
        id="matlab-doubled-quote-string",
    ),
    # Multi-line, raw, and continued strings.
    pytest.param(
        "c#",
        'var s = """\n// not\n"""; // note\n',
        ["// note"],
        "C# 11: raw string literals span lines.",
        id="csharp-raw-string",
    ),
    pytest.param(
        "scala",
        'val s = """\n// not\n""" // note\n',
        ["// note"],
        "Scala spec 1.3.5: multi-line string literals.",
        id="scala-triple-quoted-string",
    ),
    pytest.param(
        "dart",
        "var s = '''\n// not\n'''; // note\n",
        ["// note"],
        "Dart spec 17.7: multi-line strings.",
        id="dart-triple-single-quoted-string",
    ),
    pytest.param(
        "groovy",
        "def s = '''\n// not\n''' // note\n",
        ["// note"],
        "Groovy syntax 4.3: triple-single-quoted strings span lines.",
        id="groovy-triple-quoted-string",
    ),
    pytest.param(
        "python",
        "s = '''\n# not a comment\n'''\n",
        [],
        "Python reference 2.4.1: triple-quoted strings span lines.",
        id="python-triple-single-quoted-string",
    ),
    pytest.param(
        "python",
        "s = 'a\\\n# not'\n",
        [],
        "Python reference 2.4.1: backslash-newline continues a string.",
        id="python-string-line-continuation",
    ),
    pytest.param(
        "toml",
        "a = '''\n# not\n'''\n",
        [],
        "TOML 1.0, Multi-line literal strings.",
        id="toml-multiline-literal-string",
    ),
    pytest.param(
        "gdscript",
        'var s = """\n# not\n"""\n',
        [],
        "GDScript reference: triple-quoted strings span lines.",
        id="gdscript-triple-quoted-string",
    ),
    pytest.param(
        "meson",
        "x = '''\n# not\n'''\n",
        [],
        "Meson syntax: triple-quoted multiline strings.",
        id="meson-multiline-string",
    ),
    pytest.param(
        "elixir",
        "s = '''\n# not\n'''\n",
        [],
        "Elixir syntax reference: ''' delimits a charlist heredoc.",
        id="elixir-charlist-heredoc",
    ),
    pytest.param(
        "ruby",
        "s = 'a\n# not\nb' # note\n",
        ["# note"],
        "Ruby syntax: string literals may contain newlines.",
        id="ruby-multiline-single-quoted-string",
    ),
    pytest.param(
        "shell",
        'echo "a\n# not\nb" # note\n',
        ["# note"],
        "POSIX 2.2.3: double quotes preserve newlines.",
        id="shell-multiline-double-quoted-string",
    ),
    pytest.param(
        "r",
        "x <- 'a\n# not\nb' # note\n",
        ["# note"],
        "R language definition 10.3.1: strings may span lines.",
        id="r-multiline-string",
    ),
    pytest.param(
        "sql",
        "SELECT 'a\n-- not\nb' FROM t; -- note\n",
        ["-- note"],
        "SQL character string literals may contain newlines.",
        id="sql-multiline-string",
    ),
    pytest.param(
        "common_lisp",
        '(f "multi\nline ; not comment") ; note\n',
        ["; note"],
        'CLHS 2.4.5: " strings may contain newlines.',
        id="common-lisp-multiline-string",
    ),
    pytest.param(
        "c",
        'char *s = "a\\\nb // not"; // note\n',
        ["// note"],
        "C11 5.1.1.2 phase 2 splices lines before tokenization.",
        id="c-string-line-splice",
    ),
    pytest.param(
        "haskell",
        'x = "a\\\n  \\b -- not"\n',
        [],
        "Haskell 2010 2.6: string gaps span lines.",
        id="haskell-string-gap",
    ),
    pytest.param(
        "powershell",
        '$s = @"\n# not\n"@ # note\n',
        ["# note"],
        "about_Quoting_Rules: here-strings span lines.",
        id="powershell-here-string-body",
    ),
    # Language-specific literal forms.
    pytest.param(
        "perl",
        "my $s = q{# not}; # note\n",
        ["# note"],
        "perlop, Quote and Quote-like Operators.",
        id="perl-q-brace-string",
    ),
    pytest.param(
        "ruby",
        "s = %q(# not) # note\n",
        ["# note"],
        "Ruby syntax, Percent Strings.",
        id="ruby-percent-q-string",
    ),
    pytest.param(
        "ruby",
        's = "#{"#"} # not" # note\n',
        ["# note"],
        "Ruby syntax: #{...} interpolation may contain strings.",
        id="ruby-nested-interpolation",
    ),
    pytest.param(
        "plsql",
        "SELECT q'[it's -- not]' FROM dual; -- note\n",
        ["-- note"],
        "Oracle SQL Reference, Text Literals: q'[...]'.",
        id="plsql-q-quoted-string",
    ),
    pytest.param(
        "groovy",
        "def s = $/a//b/$ // note\n",
        ["// note"],
        "Groovy syntax 4.7: dollar slashy strings.",
        id="groovy-dollar-slashy-string",
    ),
    pytest.param(
        "rebol",
        "print {a;b} ; note\n",
        ["; note"],
        "REBOL/Core: {...} is a multi-line string.",
        id="rebol-braced-string",
    ),
    pytest.param(
        "red",
        "print {a;b} ; note\n",
        ["; note"],
        "Red follows REBOL: {...} is a string.",
        id="red-braced-string",
    ),
    pytest.param(
        "abap",
        'DATA(s) = |a"b|. " note\n',
        ['" note'],
        "ABAP keyword docs: |...| is a string template.",
        id="abap-string-template",
    ),
    pytest.param(
        "postscript",
        "(50%) show % note\n",
        ["% note"],
        "PLRM 3.2.2: (...) is a string; % in a string is text.",
        id="postscript-parenthesized-string",
    ),
    pytest.param(
        "bibtex",
        "@misc{a, url = {http://x/a%20b}}\n",
        [],
        "BibTeX: braced field values are literal text.",
        id="bibtex-braced-field-value",
    ),
    pytest.param(
        "bibtex",
        "@misc{a, title = {50\\% off}}\n",
        [],
        "BibTeX field text: \\% is an escaped percent sign.",
        id="bibtex-escaped-percent-in-field",
    ),
    pytest.param(
        "m4",
        "define(`x', `#not')\n",
        [],
        "GNU m4 manual 3.3: quoted # does not start a comment.",
        id="m4-quoted-hash",
    ),
    pytest.param(
        "ocaml",
        "let s = {|(* not *)|} (* note *)\n",
        ["(* note *)"],
        "OCaml manual 11.1: {|...|} quoted strings.",
        id="ocaml-quoted-string-literal",
    ),
    # Regular-expression literals.
    pytest.param(
        "javascript",
        "const re = /[/*]/; x = 1; /* note */\n",
        ["/* note */"],
        "ECMA-262 12.9.5: a class may contain an unescaped /.",
        id="javascript-regex-class-with-slash",
    ),
    pytest.param(
        "ruby",
        "r = /#[a-z]/ # note\n",
        ["# note"],
        "Ruby syntax: /.../ is a regexp literal.",
        id="ruby-slash-regex-literal",
    ),
    pytest.param(
        "perl",
        "s/#//g; # note\n",
        ["# note"],
        "perlop: s/// is a quote-like substitution.",
        id="perl-slash-substitution",
    ),
    pytest.param(
        "perl",
        "my $re = qr/a#b/; # note\n",
        ["# note"],
        "perlop: qr// is a quote-like regex.",
        id="perl-qr-regex",
    ),
    pytest.param(
        "awk",
        "/^#/ { next }\n{ print } # note\n",
        ["# note"],
        "POSIX awk: /ERE/ is a regular expression token.",
        id="awk-regex-pattern",
    ),
    pytest.param(
        "awk",
        "$0 ~ /#/ { n++ } # note\n",
        ["# note"],
        "POSIX awk: /ERE/ is a regular expression token.",
        id="awk-match-operator-regex",
    ),
    pytest.param(
        "coffeescript",
        "x = /#/.test(s) # note\n",
        ["# note"],
        "CoffeeScript lexer: /.../ is a regex literal.",
        id="coffeescript-regex-literal",
    ),
    # Template, markup, and verbatim text.
    pytest.param(
        "html",
        "<textarea><!-- not --></textarea>\n",
        [],
        "HTML 13.1.2: textarea is an escapable raw text element.",
        id="html-textarea-rcdata",
    ),
    pytest.param(
        "vue",
        "<template>\n  <p>see http://example.com</p>\n</template>\n",
        [],
        "Vue SFC: template text is HTML text, not script.",
        id="vue-template-url-text",
    ),
    pytest.param(
        "jsx",
        'const a = <a href="x">http://example.com</a>; // note\n',
        ["// note"],
        "JSX spec: JSXText is literal text.",
        id="jsx-text-url",
    ),
    pytest.param(
        "astro",
        "---\nconst x = 1; // note\n---\n<p>see http://example.com</p>\n",
        ["// note"],
        "Astro: content after frontmatter is HTML template text.",
        id="astro-template-url-text",
    ),
    pytest.param(
        "asciidoc",
        "----\n// not a comment in listing\n----\n",
        [],
        "AsciiDoc: listing block content is verbatim.",
        id="asciidoc-listing-block",
    ),
    # Markers that start a comment only at a specific position.
    pytest.param(
        "tcl",
        "set x a#b\n",
        [],
        "Tcl(n) rule 10: # is a comment only where a command starts.",
        id="tcl-hash-inside-word",
    ),
    pytest.param(
        "nginx",
        "return 302 /app/#/login; # note\n",
        ["# note"],
        "ngx_conf_read_token: # is a comment only at token start.",
        id="nginx-hash-inside-token",
    ),
    pytest.param(
        "ninja",
        "rule cc\n  command = gcc -c $in # not\n",
        [],
        "Ninja lexer: comments are skipped only between statements.",
        id="ninja-hash-inside-variable-value",
    ),
    pytest.param(
        "apacheconf",
        "RewriteRule ^/old$ /new#section [NE,R]\n# note\n",
        ["# note"],
        "httpd docs: comments may not share a line with a directive.",
        id="apacheconf-hash-inside-directive",
    ),
    pytest.param(
        "desktop",
        "[Desktop Entry]\nName=C# Editor\n# note\n",
        ["# note"],
        "Desktop Entry spec: only lines beginning with # are comments.",
        id="desktop-entry-hash-in-value",
    ),
    pytest.param(
        "debian_package_control_file",
        "Homepage: https://example.com/#readme\n# note\n",
        ["# note"],
        "Debian Policy 5.1: comments are lines starting with #.",
        id="debian-control-hash-in-field",
    ),
    pytest.param(
        "rpm_spec",
        "Source0: https://example.com/foo.tar.gz#/foo-1.0.tar.gz\n# note\n",
        ["# note"],
        "RPM spec: comments are lines starting with #.",
        id="rpm-spec-source-url-fragment",
    ),
    pytest.param(
        "mcfunction",
        "execute if block ~ ~ ~ #minecraft:logs run say hi\n",
        [],
        "Minecraft functions: # is a comment only at line start.",
        id="mcfunction-block-tag",
    ),
    pytest.param(
        "mcfunction",
        "function #minecraft:tick\n",
        [],
        "Minecraft functions: #namespace:tag is a tag reference.",
        id="mcfunction-function-tag",
    ),
    pytest.param(
        "gherkin",
        "Then I see issue #42\n# note\n",
        ["# note"],
        "Gherkin token matcher: comments are lines starting with #.",
        id="gherkin-hash-in-step",
    ),
    pytest.param(
        "cucumber",
        "Then I see issue #42\n# note\n",
        ["# note"],
        "Gherkin token matcher: comments are lines starting with #.",
        id="cucumber-hash-in-step",
    ),
    pytest.param(
        "org",
        "Issue #42 is fixed.\n# note\n",
        ["# note"],
        "Org manual: comment lines start with # and whitespace.",
        id="org-hash-in-paragraph",
    ),
    pytest.param(
        "asciidoc",
        "See http://example.com\n",
        [],
        "Asciidoctor CommentLineRx: ^//(?=[^/]|$).",
        id="asciidoc-url-in-paragraph",
    ),
    pytest.param(
        "java_properties",
        "a=b\\\n  # not a comment\n",
        [],
        "java.util.Properties.load: continuation lines are values.",
        id="java-properties-continuation-line",
    ),
    pytest.param(
        "jinja",
        "## {{ title }}\n",
        [],
        "Jinja defaults: LINE_COMMENT_PREFIX is None.",
        id="jinja-double-hash-is-text",
    ),
    pytest.param(
        "html_django",
        "## Heading {{ x }}\n",
        [],
        "Django templates have no ## line comments.",
        id="html-django-double-hash-is-text",
    ),
    pytest.param(
        "sas",
        "* note; data x; set y; run;\n",
        ["* note;"],
        "SAS comment statement: *message; ends at the semicolon.",
        id="sas-star-comment-ends-at-semicolon",
    ),
    pytest.param(
        "sas",
        "data x; * note; set y; run;\n",
        ["* note;"],
        "SAS comment statement may start any statement.",
        id="sas-star-comment-after-statement",
    ),
    pytest.param(
        "sas",
        "* multi\n  line note;\ndata x; run;\n",
        ["* multi\n  line note;"],
        "SAS comment statement continues to the semicolon.",
        id="sas-star-comment-spans-lines",
    ),
    # Missing comment forms and nesting.
    pytest.param(
        "puppet",
        "/* note */\nclass a {}\n",
        ["/* note */"],
        "Puppet lexer2: PATTERN_MLCOMMENT = /\\*(.*?)\\*/.",
        id="puppet-c-style-block-comment",
    ),
    pytest.param(
        "lfe",
        "#| note |# (f)\n",
        ["#| note |#"],
        "lfe_scan.erl: scan_block_comment handles #| ... |#.",
        id="lfe-block-comment",
    ),
    pytest.param(
        "scheme",
        "#| outer #| inner |# still |# (f)\n",
        ["#| outer #| inner |# still |#"],
        "R7RS 2.2: #| ... |# comments nest.",
        id="scheme-nested-block-comment",
    ),
    pytest.param(
        "autoit",
        "#comments-start\nnote\n#comments-end\n$x = 1\n",
        ["#comments-start\nnote\n#comments-end"],
        "AutoIt docs: #comments-start/#comments-end (#cs/#ce).",
        id="autoit-long-form-comment-block",
    ),
    pytest.param(
        "html_django",
        "{% comment %}note{% endcomment %}\n<p>x</p>\n",
        ["{% comment %}note{% endcomment %}"],
        "Django built-in tags: {% comment %} ... {% endcomment %}.",
        id="html-django-comment-tag",
    ),
    pytest.param(
        "html_erb",
        "<!-- note -->\n<%= x %>\n",
        ["<!-- note -->"],
        "HTML+ERB documents carry HTML comments.",
        id="html-erb-html-comment",
    ),
    pytest.param(
        "saltstack",
        "{# note #}\npkg.installed: []\n",
        ["{# note #}"],
        "Salt SLS files render with jinja|yaml by default.",
        id="saltstack-jinja-comment",
    ),
    pytest.param(
        "odin",
        "/* outer /* inner */ still */ x := 1\n",
        ["/* outer /* inner */ still */"],
        "Odin tokenizer scan_comment tracks nest depth.",
        id="odin-nested-block-comment",
    ),
    pytest.param(
        "haskell",
        "x = a ---> b\n",
        [],
        "Haskell 2010 2.3: dashes in a legal lexeme do not comment.",
        id="haskell-dash-arrow-operator",
    ),
    # Line endings.
    pytest.param(
        "plpgsql",
        "-- a\rSELECT 1;\r",
        ["-- a"],
        "PostgreSQL scan.l: newline is [\\n\\r].",
        id="plpgsql-lone-cr-line-ending",
    ),
    pytest.param(
        "ada",
        "-- a\rX := 1;\r",
        ["-- a"],
        "Ada RM 2.2: a format effector other than HT ends a line.",
        id="ada-lone-cr-line-ending",
    ),
    pytest.param(
        "nim",
        "# a\rlet x = 1\r",
        ["# a"],
        "Nim lexer: CR, LF, and CRLF end a line.",
        id="nim-lone-cr-line-ending",
    ),
    pytest.param(
        "d",
        "/// a\rint x;\r",
        ["/// a"],
        "D spec, EndOfLine includes \\u000D.",
        id="d-lone-cr-line-ending",
    ),
    # Docstring policy, explicit markup, and string-versus-comment markers.
    pytest.param(
        "python",
        'QUERY = """\nSELECT 1\n"""\n',
        [],
        "Python reference 7.2: an assigned string is data.",
        id="python-triple-quoted-assignment",
    ),
    pytest.param(
        "python",
        'cursor.execute("""SELECT 1""")  # note\n',
        ["# note"],
        "Python reference 6.3.4: a call argument is data.",
        id="python-triple-quoted-call-argument",
    ),
    pytest.param(
        "python",
        'def f():\n    """Docstring."""\n',
        ['"""Docstring."""'],
        "Registry policy: docstring statements are comment blocks.",
        id="python-docstring-remains-comment",
    ),
    pytest.param(
        "restructuredtext",
        ".. note:: Important text\n",
        [],
        "Docutils spec, Comments: directives are not comments.",
        id="rst-admonition-directive",
    ),
    pytest.param(
        "restructuredtext",
        ".. code-block:: python\n\n   x = 1\n",
        [],
        "Docutils spec, Comments: directives are not comments.",
        id="rst-code-block-directive",
    ),
    pytest.param(
        "restructuredtext",
        ".. _label:\n\nTitle\n",
        [],
        "Docutils spec, Comments: hyperlink targets are not comments.",
        id="rst-hyperlink-target",
    ),
    pytest.param(
        "restructuredtext",
        ".. image:: a.png\n",
        [],
        "Docutils spec, Comments: directives are not comments.",
        id="rst-image-directive",
    ),
    pytest.param(
        "restructuredtext",
        ".. this is a comment\n",
        [".. this is a comment"],
        "Docutils spec, Comments: other explicit markup is a comment.",
        id="rst-plain-comment",
    ),
    pytest.param(
        "vim_script",
        '" note\nlet x = 1\n',
        ['" note'],
        'Vim cmdline.txt: a line starting with " is a comment.',
        id="vim-standalone-comment",
    ),
    # String-protection guards that a lexical fix must preserve.
    pytest.param(
        "verilog",
        '$display("//not"); // note\n',
        ["// note"],
        "IEEE 1364 3.6: // inside a string is text.",
        id="verilog-string-protects-slashes",
    ),
    pytest.param(
        "shell",
        "echo '#' # note\n",
        ["# note"],
        "POSIX 2.2.2: single quotes preserve #.",
        id="shell-single-quoted-hash",
    ),
]


@pytest.mark.parametrize(
    ("language", "source", "expected", "reference"), _with_open_marks(_ITERATION_3_CASES)
)
def test_iteration_3_real_code_extraction_follows_language_contract(
    language, source, expected, reference
):
    assert reference
    assert _matches(language, source) == expected


# ---------------------------------------------------------------------------
# Fourth breaker iteration: version research. In each language below a newer
# version changed comment syntax in a way that never alters the comments of a
# valid program written for an older version, so the language needs no version
# table; the registry should simply implement the newer rules.
# ---------------------------------------------------------------------------

_ITERATION_4_CASES = [
    pytest.param(
        "javascript",
        "#!/usr/bin/env node\nconst n = 1; // note\n",
        ["#!/usr/bin/env node", "// note"],
        "ECMA-262 2023 sec-hashbang: HashbangComment at the start of the source.",
        id="javascript-es2023-hashbang-comment",
    ),
    pytest.param(
        "typescript",
        "#!/usr/bin/env node\nconst n: number = 1; // note\n",
        ["#!/usr/bin/env node", "// note"],
        "TypeScript 1.6 scanner.ts: shebang trivia at position 0.",
        id="typescript-shebang-trivia",
    ),
    pytest.param(
        "python",
        'total = f"""{\n    price * qty  # line total\n}"""\nprint(total)  # show\n',
        ["# line total", "# show"],
        "PEP 701 (Python 3.12): replacement fields may span lines and hold comments.",
        id="python-312-fstring-field-comment",
    ),
    pytest.param(
        "makefile",
        "# build flags\n\nfoo := $(subst /,#,a/b)\n",
        ["# build flags"],
        "GNU make 4.3 NEWS: # inside a function invocation does not start a comment.",
        id="makefile-43-hash-inside-function-call",
    ),
    pytest.param(
        "rpm_spec",
        "Name: demo\n%dnl packaging note\nVersion: 1.0\n# legacy note\nRelease: 1\n",
        ["%dnl packaging note", "# legacy note"],
        "RPM 4.15 macros: %dnl discards to the end of the line.",
        id="rpm-415-dnl-comment",
    ),
    pytest.param(
        "handlebars",
        "<ul>\n{{~! trim before list ~}}\n{{! plain note }}\n</ul>\n",
        ["{{~! trim before list ~}}", "{{! plain note }}"],
        "Handlebars 3.0: comments accept whitespace control.",
        id="handlebars-3-whitespace-control-comment",
    ),
    pytest.param(
        "mini_yaml",
        "Tooltip:\n\tName: C\\# Tank # prototype unit\n",
        ["# prototype unit"],
        "OpenRA release-20180923 MiniYaml: \\# is an escaped hash.",
        id="mini-yaml-escaped-hash",
    ),
    pytest.param(
        "twig",
        '{{\n    "Hello World"|upper # shout it\n}}\n{# page footer #}\n',
        ["# shout it", "{# page footer #}"],
        "Twig 3.15: # starts an inline comment inside expressions.",
        id="twig-315-inline-expression-comment",
    ),
    pytest.param(
        "openedge_abl",
        "DEFINE VARIABLE i AS INTEGER NO-UNDO. /* counter */\n"
        "i = 10. // initial value\nDISPLAY i.\n",
        ["/* counter */", "// initial value"],
        "OpenEdge 11.6 ABL: // single-line comments.",
        id="openedge-116-line-comment",
    ),
    pytest.param(
        "mirc_script",
        "/*\necho -a disabled\n*/\n; greet\nalias hi { echo -a hi }\n",
        ["/*\necho -a disabled\n*/", "; greet"],
        "mIRC 6.1: /* and */ on their own lines delimit a block comment.",
        id="mirc-61-block-comment",
    ),
    pytest.param(
        "fortran",
        "C     old style\n*     star style\n      X = 1.0 ! inline\n",
        ["C     old style", "*     star style", "! inline"],
        "Fortran 90 fixed form: C, c, or * in column 1, and ! outside column 6.",
        id="fortran-fixed-form-column-one-comments",
    ),
    pytest.param(
        "factor",
        'USING: io ;\n: hello! ( -- ) "hi" print ;\n',
        [],
        "Factor lexer: only a token exactly equal to ! starts a comment.",
        id="factor-bang-inside-word",
    ),
]


@pytest.mark.parametrize(
    ("language", "source", "expected", "reference"), _with_open_marks(_ITERATION_4_CASES)
)
def test_iteration_4_newer_comment_rules_need_no_version(language, source, expected, reference):
    assert reference
    assert _matches(language, source) == expected
