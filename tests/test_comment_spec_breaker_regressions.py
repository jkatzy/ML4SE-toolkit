"""Spec-derived breaker regressions for comment extraction and cleaning.

Every case in this module was written from a language specification or a
language-independent comment contract, reproduced against the extractor or
sanitizer, and minimized. Expected values come from the cited language
contract, never from parser output.

Cases whose defect is still open are listed in ``_OPEN_CASES`` and run as
strict ``xfail``: the suite stays green while the defect is open and fails as
soon as a fix makes the case pass, at which point the entry is removed.
"""

from dataclasses import dataclass

import pytest

from ml4setk import CommentQuery, sanitize_comment
from ml4setk.Parsing.Comments import iter_comment_syntaxes

pytestmark = pytest.mark.unit


def _matches(language, source):
    return [match.match for match in CommentQuery(language).parse(source)]


def _open_defect(reason):
    return pytest.mark.xfail(reason=reason, strict=True)


# Case id -> reason for defects that are confirmed but not fixed yet.
_OPEN_CASES = {
    "lua-cr-terminates-comment": (
        "Lua keeps its legacy published slices; see "
        "test_lua_legacy_crlf_comment_slice_preserves_carriage_return."
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
