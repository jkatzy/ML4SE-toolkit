"""Open spec-derived breaker regressions for comment extraction and cleaning.

Every case in this module was written from a language specification or a
language-independent comment contract, reproduced against the current
extractor or sanitizer, and minimized. The cases document confirmed defects
that are not fixed yet, so each one is a strict ``xfail``: the suite stays green
while the defect is open, and fails as soon as a fix makes the case pass. When
that happens, drop the ``xfail`` marker (or remove the language from the pinned
failing set) so the case becomes an ordinary regression.

Expected values come from the cited language contract, never from the current
parser output.
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


@_open_defect("Generic quote scanner treats language-specific apostrophes as strings.")
@pytest.mark.parametrize(
    ("language", "source", "expected", "reference"),
    _LINE_COMMENT_HIDDEN_BY_LEXICAL_APOSTROPHE,
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


@_open_defect("Comment-looking text in non-comment syntax is extracted.")
@pytest.mark.parametrize(
    ("language", "source", "reference"),
    _SPURIOUS_COMMENT_FROM_NON_COMMENT_SYNTAX,
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
        "sql",
        "/* a /* b */ c */ SELECT 1\n",
        ["/* a /* b */ c */"],
        "ISO SQL <bracketed comment> nests; PostgreSQL docs 4.1.5 follow the standard.",
        id="sql-nested-block",
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


@_open_defect("Comment boundary does not follow the language contract.")
@pytest.mark.parametrize(("language", "source", "expected", "reference"), _WRONG_COMMENT_BOUNDARIES)
def test_comment_boundaries_follow_language_contract(language, source, expected, reference):
    assert reference
    assert _matches(language, source) == expected


# ---------------------------------------------------------------------------
# Hand-written sanitizer cases: cleaning must not discard comment content.
# ---------------------------------------------------------------------------


@_open_defect("Sanitizer drops content-bearing characters.")
@pytest.mark.parametrize(
    ("language", "raw_comment", "expected"),
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
    ],
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


# Languages where an apostrophe in one inline block comment pairs with an
# apostrophe in the next comment on the same line, hiding the second comment
# (or exposing a fragment of it).
_APOSTROPHE_PAIR_FAILING_LANGUAGES = frozenset(
    {
        "4d",
        "abap_cds",
        "actionscript",
        "agda",
        "ags_script",
        "aidl",
        "al",
        "alloy",
        "ampl",
        "angelscript",
        "ant_build_system",
        "antlers",
        "antlr",
        "apex",
        "api_blueprint",
        "applescript",
        "arduino",
        "asl",
        "asp",
        "asp_net",
        "aspectj",
        "aspnet",
        "astro",
        "asymptote",
        "ats",
        "autohotkey",
        "avro_idl",
        "ballerina",
        "beef",
        "berry",
        "bicep",
        "bikeshed",
        "bison",
        "blade",
        "bluespec",
        "boo",
        "boogie",
        "c",
        "c#",
        "c++",
        "c2hs_haskell",
        "c_sharp",
        "cadence",
        "cameligo",
        "cap_cds",
        "cartocss",
        "ceylon",
        "chapel",
        "chuck",
        "cil",
        "classic_asp",
        "clean",
        "click",
        "closure_templates",
        "cmake",
        "codeql",
        "coldfusion",
        "coldfusion_cfc",
        "collada",
        "common_lisp",
        "cool",
        "csharp",
        "csound",
        "csound_document",
        "csound_score",
        "css",
        "cuda",
        "curry",
        "cweb",
        "cycript",
        "cypher",
        "d",
        "dafny",
        "dart",
        "daslang",
        "dataweave",
        "dhall",
        "dm",
        "dtrace",
        "dylan",
        "eagle",
        "ec",
        "ecl",
        "edje_data_collection",
        "ejs",
        "elm",
        "eq",
        "euphoria",
        "f#",
        "f_sharp",
        "fantom",
        "faust",
        "filterscript",
        "forth",
        "four_d",
        "freebasic",
        "freemarker",
        "frege",
        "fsharp",
        "g_code",
        "game_maker_language",
        "gaml",
        "gams",
        "genero",
        "genero_forms",
        "genie",
        "genshi",
        "glsl",
        "go",
        "gosu",
        "gradle",
        "grammatical_framework",
        "graphviz_dot",
        "groovy",
        "groovy_server_pages",
        "gsc",
        "hack",
        "handlebars",
        "harbour",
        "haskell",
        "haxe",
        "hcl",
        "hlsl",
        "holyc",
        "html",
        "html_django",
        "html_ecr",
        "html_eex",
        "html_erb",
        "html_php",
        "html_plus_django",
        "html_plus_ecr",
        "html_plus_eex",
        "html_plus_erb",
        "html_plus_php",
        "html_plus_razor",
        "html_plusdjango",
        "html_razor",
        "hyphy",
        "idl",
        "idris",
        "imagej_macro",
        "inform_7",
        "inno_setup",
        "io",
        "java",
        "java_server_pages",
        "javascript",
        "javascript_erb",
        "javascript_plus_erb",
        "jest_snapshot",
        "jetbrains_mps",
        "jflex",
        "jinja",
        "jison",
        "jison_lex",
        "jolie",
        "json5",
        "json_with_comments",
        "jsoniq",
        "jsonnet",
        "jsp",
        "jsx",
        "julia",
        "kit",
        "krl",
        "labview",
        "lasso",
        "latte",
        "leo",
        "less",
        "lex",
        "ligolang",
        "linker_script",
        "literate_agda",
        "literate_haskell",
        "livecode_script",
        "livescript",
        "logos",
        "loomscript",
        "lsl",
        "lua",
        "macaulay2",
        "markdown",
        "marko",
        "mask",
        "mathematica",
        "maven_pom",
        "maxscript",
        "mediawiki",
        "metal",
        "minid",
        "minizinc",
        "minizinc_data",
        "modelica",
        "monkey_c",
        "moocode",
        "moonscript",
        "motoko",
        "move",
        "mql",
        "mql4",
        "mql5",
        "mtml",
        "mupad",
        "nemerle",
        "nesc",
        "netlinx",
        "netlinx_plus_erb",
        "nextflow",
        "nim",
        "nimrod",
        "nsis",
        "nunjucks",
        "nwscript",
        "objective-c",
        "objective_c_plus_plus",
        "objective_cpp",
        "objective_j",
        "objectscript",
        "ocaml",
        "odin",
        "ooc",
        "opa",
        "opencl",
        "openedge_abl",
        "openqasm",
        "openscad",
        "openstep_property_list",
        "ox",
        "oxygene",
        "p4",
        "pascal",
        "pawn",
        "peg_js",
        "pegjs",
        "php",
        "pike",
        "plantuml",
        "pony",
        "portugol",
        "postcss",
        "pov_ray_sdl",
        "powerbuilder",
        "powershell",
        "prisma",
        "processing",
        "prolog",
        "promela",
        "propeller_spin",
        "protocol_buffer",
        "purescript",
        "qml",
        "qt_script",
        "quake",
        "racket",
        "rascal",
        "rdoc",
        "reason",
        "reason_ligo",
        "reasonligo",
        "reasonml",
        "renderscript",
        "rescript",
        "rexx",
        "rhtml",
        "ring",
        "riot",
        "rmarkdown",
        "rpc",
        "rpgle",
        "sas",
        "sass",
        "scala",
        "scilab",
        "scss",
        "shaderlab",
        "shen",
        "sieve",
        "slice",
        "smarty",
        "smpl",
        "solidity",
        "soong",
        "sourcepawn",
        "sqf",
        "sql",
        "squirrel",
        "stan",
        "stata",
        "stringtemplate",
        "stylus",
        "sugarss",
        "supercollider",
        "svelte",
        "svg",
        "swift",
        "swig",
        "systemverilog",
        "tea",
        "terra",
        "textile",
        "thrift",
        "tla",
        "tsx",
        "twig",
        "type_language",
        "typescript",
        "unified_parallel_c",
        "uno",
        "unrealscript",
        "untyped_plutus_core",
        "upc",
        "v",
        "vala",
        "vcl",
        "velocity_template_language",
        "vento",
        "verilog",
        "volt",
        "vue",
        "web_ontology_language",
        "webassembly",
        "webassembly_interface_type",
        "webidl",
        "wgsl",
        "whiley",
        "wikitext",
        "wit",
        "witcher_script",
        "wollok",
        "wren",
        "x10",
        "x_bit_map",
        "x_bitmap",
        "x_pix_map",
        "x_pixmap",
        "xbase",
        "xc",
        "xmake",
        "xml",
        "xml_property_list",
        "xpages",
        "xproc",
        "xquery",
        "xs",
        "xslt",
        "xtend",
        "yacc",
        "yang",
        "yara",
        "yul",
        "zenscript",
        "zephir",
        "zmodel",
    }
)

# Languages whose nested-comment scanner counts an opener inside a line comment,
# so a later, real block comment is never closed at depth zero and is lost.
_NESTED_OPENER_IN_LINE_COMMENT_FAILING_LANGUAGES = frozenset(
    {
        "agda",
        "applescript",
        "ats",
        "beef",
        "boo",
        "boogie",
        "c2hs_haskell",
        "cadence",
        "cameligo",
        "ceylon",
        "chapel",
        "clean",
        "common_lisp",
        "cool",
        "curry",
        "dafny",
        "daslang",
        "dhall",
        "dm",
        "dylan",
        "elm",
        "f#",
        "f_sharp",
        "frege",
        "fsharp",
        "gradle_kotlin_dsl",
        "grammatical_framework",
        "haskell",
        "idris",
        "jflex",
        "julia",
        "koka",
        "kotlin",
        "lean",
        "lean4",
        "lean_4",
        "ligolang",
        "literate_agda",
        "literate_haskell",
        "motoko",
        "nim",
        "nimrod",
        "noir",
        "powerbuilder",
        "purescript",
        "racket",
        "reason",
        "reason_ligo",
        "reasonligo",
        "reasonml",
        "rust",
        "supercollider",
        "sway",
        "tla",
        "untyped_plutus_core",
        "v",
        "webassembly",
        "webassembly_interface_type",
        "wgsl",
        "wit",
        "wren",
    }
)


def _params(cases, failing_languages, reason):
    return [
        pytest.param(
            case,
            id=case.language,
            marks=_open_defect(reason) if case.language in failing_languages else (),
        )
        for case in cases
    ]


@pytest.mark.parametrize(
    "case",
    _params(
        _build_apostrophe_pair_cases(),
        _APOSTROPHE_PAIR_FAILING_LANGUAGES,
        "Quote scanner pairs apostrophes across separate comments.",
    ),
)
def test_apostrophes_in_separate_comments_do_not_form_a_string(case):
    assert tuple(_matches(case.language, case.source)) == case.expected


@pytest.mark.parametrize(
    "case",
    _params(
        _build_nested_opener_in_line_comment_cases(),
        _NESTED_OPENER_IN_LINE_COMMENT_FAILING_LANGUAGES,
        "Nested scanner counts block openers inside line comments.",
    ),
)
def test_block_opener_inside_line_comment_does_not_hide_later_block(case):
    assert tuple(_matches(case.language, case.source)) == case.expected


def test_generated_failing_sets_name_registered_languages():
    apostrophe_languages = {case.language for case in _build_apostrophe_pair_cases()}
    nested_languages = {case.language for case in _build_nested_opener_in_line_comment_cases()}

    assert _APOSTROPHE_PAIR_FAILING_LANGUAGES <= apostrophe_languages
    assert _NESTED_OPENER_IN_LINE_COMMENT_FAILING_LANGUAGES <= nested_languages


@_open_defect("Scenic extraction encodes text as strict UTF-8 and rejects lone surrogates.")
def test_scenic_accepts_lone_surrogate_in_python_string():
    # Minimized from the seeded parser fuzz campaign (seed 0xC0FFEE, scenic case 0).
    assert _matches("scenic", "x = 1  # note \ud800\n") == ["# note \ud800"]
