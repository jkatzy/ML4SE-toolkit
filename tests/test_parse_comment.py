import sys
from pathlib import Path

import pytest

# Ensure the src layout is importable when running tests without installing the package
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from ml4setk.Comment_util import parse_comment as pc  # noqa: E402

FIXTURES_DIR = ROOT / "tests" / "fixtures" / "comments"


def test_extract_nested_returns_top_level_only():
    content = "code (* outer (* inner *) outer end *) tail"
    matches = pc.extract_nested("(*", "*)", content)

    assert len(matches) == 1
    span, text, kind = matches[0]
    assert text == "(* outer (* inner *) outer end *)"
    assert span[0] == content.index("(*")
    assert span[1] == span[0] + len(text)
    assert kind == "block"


def test_extract_comments_python_line_and_block():
    content = '"""docstring"""\nvalue = 1 # inline comment\n'
    comments = pc.extract_comments_python(content)

    texts = [c[1] for c in comments]
    assert '# inline comment' in texts
    assert '"""docstring"""' in texts


def test_extract_comments_combines_multiple_languages():
    content = "# py comment\n/* sql block */\n"
    comments = pc.extract_comments(content, ["python", "sql"])

    texts = [c[1] for c in comments]
    assert "# py comment" in texts
    assert "/* sql block */" in texts


def test_line_comments_merge_consecutive_lines():
    content = "# first\n# second\ncode()\n"
    comments = pc.extract_comments_python(content)

    assert len(comments) == 1
    span, text, kind = comments[0]
    assert text == "# first\n# second"
    # ensure span covers both lines
    assert span == (0, len("# first\n# second"))
    assert kind == "line"


def test_opening_comment_simple():
    content = (FIXTURES_DIR / "c.c").read_text(encoding="utf-8")
    opening = pc.extract_opening_comment(content, ["c"])

    assert opening is not None
    span, text, kind = opening
    assert text.startswith("/* block comment */")
    assert kind == "block"
    assert span[0] == 0


def test_opening_comment_skips_preprocessor():
    content = "#include <stdio.h>\n# define X 1\n// header comment\nint main() { return 0; }\n"
    opening = pc.extract_opening_comment(content, ["c"])

    assert opening is not None
    _span, text, kind = opening
    assert text.startswith("// header comment")
    assert kind == "line"


# Language fixtures: (filename, language name, expects_block_comment, expects_line_comments)
LANG_FIXTURES = [
    ("java.java", "java", True, True),
    ("c.c", "c", True, True),
    ("cpp.cpp", "c++", True, True),
    ("csharp.cs", "c#", True, True),
    ("javascript.js", "javascript", True, True),
    ("typescript.ts", "typescript", True, True),
    ("objectivec.m", "objective-c", True, True),
    ("go.go", "go", True, True),
    ("kotlin.kt", "kotlin", True, True),
    ("vue.vue", "vue", True, True),
    ("scala.scala", "scala", True, True),
    ("dart.dart", "dart", True, True),
    ("rust.rs", "rust", True, True),
    ("hack.hack", "hack", True, True),
    ("less.less", "less", True, True),
    ("groovy.groovy", "groovy", True, True),
    ("processing.pde", "processing", True, True),
    ("apex.cls", "apex", True, True),
    ("cuda.cu", "cuda", True, True),
    ("scilab.sci", "scilab", True, True),
    ("antlr.g4", "antlr", True, True),
    ("swift.swift", "swift", True, True),
    ("php.php", "php", True, True),
    ("python.py", "python", True, True),
    ("r.r", "r", True, True),
    ("elixir.ex", "elixir", True, True),
    ("nix.nix", "nix", True, True),
    ("starlark.star", "starlark", True, True),
    ("graphql.graphql", "graphql", True, True),
    ("crystal.cr", "crystal", True, True),
    ("agda.agda", "agda", True, True),
    ("elm.elm", "elm", True, True),
    ("cobol.cbl", "cobol", True, False),
    ("coq.v", "coq", True, False),
    ("ocaml.ml", "ocaml", True, False),
    ("d.d", "d", True, True),
    ("forth.frt", "forth", True, True),
    ("lua.lua", "lua", True, True),
    ("mathematica.wl", "mathematica", True, False),
    ("matlab.m", "matlab", True, True),
    ("perl.pl", "perl", True, True),
    ("prolog.pro", "prolog", True, True),
    ("raku.raku", "raku", True, True),
    ("ruby.rb", "ruby", True, True),
    ("sql.sql", "sql", True, True),
    ("webassembly.wat", "webassembly", True, True),
    ("ada.adb", "ada", False, True),
    ("erlang.erl", "erlang", False, True),
    ("fortran.f90", "fortran", False, True),
    ("lisp.lisp", "lisp", False, True),
    ("assembly.asm", "assembly", False, True),
    ("netlogo.nlogo", "netlogo", False, True),
    ("scheme.scm", "scheme", False, True),
]


@pytest.mark.parametrize("fixture,lang,expects_block,has_line_comments", LANG_FIXTURES)
def test_extract_comments_from_fixture(fixture, lang, expects_block, has_line_comments):
    content = (FIXTURES_DIR / fixture).read_text(encoding="utf-8")
    comments = pc.extract_comments(content, [lang])

    assert comments, f"expected comments for {fixture}"

    blocks = [c for c in comments if c[2] == "block"]
    if expects_block:
        assert blocks, f"expected block comment in {fixture}"
    else:
        assert not blocks, f"did not expect block comment in {fixture}"

    if has_line_comments:
        merged_lines = [
            c
            for c in comments
            if c[2] == "line" and "multi line comment part 1" in c[1]
        ]
        assert (
            len(merged_lines) == 1
        ), f"consecutive line comments should merge into one block in {fixture}"
        merged_text = merged_lines[0][1]
        assert "multi line comment part 1\n" in merged_text
        assert "multi line comment part 2" in merged_text

        # The single standalone line comment should still appear separately
        single_lines = [c for c in comments if c[2] == "line" and "single line comment" in c[1]]
        assert single_lines, f"single line comment missing in {fixture}"


C_STYLE_ALIAS_LANGS = [
    "ags script",
    "actionscript",
    "arduino",
    "avro idl",
    "aspectj",
    "bluespec",
    "ceylon",
    "chapel",
    "chuck",
    "cycript",
    "dtrace",
    "ecl",
    "fantom",
    "game maker language",
    "glsl",
    "gosu",
    "gradle",
    "haxe",
    "hlsl",
    "hyphy",
    "idl",
    "json5",
    "jsx",
    "m",
    "metal",
    "modelica",
    "nesc",
    "objective-j",
    "objective-c++",
    "opencl",
    "openscad",
    "pawn",
    "pike",
    "protocol buffer",
    "qml",
    "renderscript",
    "scss",
    "sass",
    "sourcepawn",
    "squirrel",
    "systemverilog",
    "tea",
    "unrealscript",
    "unified parallel c",
    "uno",
    "vala",
    "verilog",
    "webidl",
    "xc",
    "xtend",
    "yacc",
    "yang",
    "linux kernel module",
    "lsl",
    "ec",
    "harbour",
    "io",
    "lasso",
    "logos",
    "max",
    "nemerle",
    "netlinx",
    "ooc",
    "opa",
    "ox",
    "mupad",
    "sqf",
    "stan",
    "stylus",
    "x10",
]

HASH_ALIAS_LANGS = [
    "apacheconf",
    "awk",
    "bitbake",
    "bro",
    "cap'n proto",
    "click",
    "cmake",
    "cucumber",
    "dockerfile",
    "gap",
    "gdscript",
    "gentoo ebuild",
    "gentoo eclass",
    "gettext catalog",
    "gnuplot",
    "golo",
    "graph modeling language",
    "limbo",
    "makefile",
    "monkey",
    "nginx",
    "nit",
    "ninja",
    "puppet",
    "qmake",
    "robotframework",
    "saltstack",
    "shell",
    "slash",
    "sparql",
    "tcl",
    "tcsh",
    "toml",
    "turtle",
    "unity3d asset",
    "yaml",
    "desktop",
    "fish",
    "lookml",
    "raml",
    "ren'py",
    "sage",
    "smali",
    "zimpl",
]

SEMICOLON_ALIAS_LANGS = [
    "arc",
    "blitzbasic",
    "clojure",
    "dns zone",
    "edn",
    "hy",
    "jasmin",
    "krl",
    "lfe",
    "llvm",
    "purebasic",
    "red",
    "redcode",
    "rebol",
    "smt",
]

MARKUP_ALIAS_LANGS = [
    "ant build system",
    "html",
    "markdown",
    "mediawiki",
    "rmarkdown",
    "svg",
    "xml",
    "xproc",
    "xslt",
    "xpages",
]
HASKELL_ALIAS_LANGS = [
    "c2hs haskell",
    "frege",
    "grammatical framework",
    "haskell",
    "idris",
    "literate haskell",
    "purescript",
]
LEAN_ALIAS_LANGS = ["lean"]
JSONNET_ALIAS_LANGS = ["graphviz (dot)", "hcl", "thrift"]
HASH_PIPE_ALIAS_LANGS = ["common lisp", "emacs lisp", "racket"]
NESTED_C_ALIAS_LANGS = ["dm", "dylan", "jflex"]
STAR_NESTED_ALIAS_LANGS = ["augeas", "component pascal", "isabelle", "modula-2", "standard ml"]
EJS_ALIAS_LANGS = ["ejs", "html+eex", "html+erb"]
SQL_ALIAS_LANGS = ["plpgsql", "plsql", "sqlpl"]
DASH_ALIAS_LANGS = ["eiffel", "vhdl"]
BANG_ALIAS_LANGS = ["digital command language", "factor", "clarion"]
SLASH_LINE_ALIAS_LANGS = ["grace", "igor pro"]
PERCENT_ALIAS_LANGS = ["postscript", "tex"]
HASH_BLOCK_ALIAS_LANGS = ["nimrod"]
HASH_CBLOCK_ALIAS_LANGS = ["ampl", "linker script"]
INI_ALIAS_LANGS = ["ini", "nsis"]
BASIC_ALIAS_LANGS = ["inno setup", "visual basic", "realbasic", "xojo", "brightscript"]
APPLE_ALIAS_LANGS = ["applescript"]
APL_ALIAS_LANGS = ["apl"]
ALLOY_ALIAS_LANGS = ["alloy"]
SEMICOLON_CSTYLE_ALIAS_LANGS = ["autohotkey", "clips"]
AUTOIT_ALIAS_LANGS = ["autoit"]
ABAP_ALIAS_LANGS = ["abap"]
BATCH_ALIAS_LANGS = ["batchfile"]
BLITZMAX_ALIAS_LANGS = ["blitzmax"]
COFFEE_ALIAS_LANGS = ["coffeescript", "emberscript"]
CSS_ALIAS_LANGS = ["css", "lex"]
GAMS_ALIAS_LANGS = ["gams"]
GCODE_ALIAS_LANGS = ["g-code"]
LOLCODE_ALIAS_LANGS = ["lolcode"]
M4_ALIAS_LANGS = ["m4", "m4sugar"]
ORG_ALIAS_LANGS = ["org"]
POWERSHELL_ALIAS_LANGS = ["powershell"]
PASCAL_ALIAS_LANGS = ["pascal"]
VIML_ALIAS_LANGS = ["viml"]
PERL6_ALIAS_LANGS = ["perl6"]
ATS_ALIAS_LANGS = ["ats"]
COOL_ALIAS_LANGS = ["cool"]
LILYPOND_ALIAS_LANGS = ["lilypond"]
LIVESCRIPT_ALIAS_LANGS = ["livescript"]
MAXSCRIPT_ALIAS_LANGS = ["maxscript"]
MIRAH_ALIAS_LANGS = ["mirah"]
MOONSCRIPT_ALIAS_LANGS = ["moonscript", "terra"]
PERCENT_CSTYLE_ALIAS_LANGS = ["eclipse", "mercury"]
ANTLERS_ALIAS_LANGS = ["antlers"]
TWIG_ALIAS_LANGS = ["twig"]
NUNJUCKS_ALIAS_LANGS = ["nunjucks"]
SMARTY_ALIAS_LANGS = ["smarty"]
HANDLEBARS_ALIAS_LANGS = ["handlebars"]
DJANGO_ALIAS_LANGS = ["html+django"]
LIQUID_ALIAS_LANGS = ["liquid"]
MAKO_ALIAS_LANGS = ["mako"]
RHTML_ALIAS_LANGS = ["rhtml"]
RDOC_ALIAS_LANGS = ["rdoc"]
COLDFUSION_ALIAS_LANGS = ["coldfusion", "coldfusion cfc"]
XQUERY_ALIAS_LANGS = ["jsoniq", "xquery"]
SMALLTALK_ALIAS_LANGS = ["smalltalk", "self"]
PROLOG_STYLE_ALIAS_LANGS = ["logtalk"]
SAS_ALIAS_LANGS = ["sas"]
STATA_ALIAS_LANGS = ["stata"]
NONE_ALIAS_LANGS = [
    "brainfuck",
    "c-objdump",
    "cpp-objdump",
    "csv",
    "d-objdump",
    "darcs patch",
    "diff",
    "formatted",
    "http",
    "irc log",
    "json",
    "jsonld",
    "jupyter notebook",
    "public key",
    "python traceback",
    "raw token data",
    "rouge",
    "shellsession",
    "text",
    "objdump",
]
SEMICOLON_LINE_ONLY_EXTRA_LANGS = ["ncl"]
JSP_ALIAS_LANGS = ["groovy server pages", "java server pages"]
FREEMARKER_ALIAS_LANGS = ["freemarker"]
ASCIIDOC_ALIAS_LANGS = ["asciidoc"]
INFORM7_ALIAS_LANGS = ["inform 7"]
J_ALIAS_LANGS = ["j"]
NEWLISP_ALIAS_LANGS = ["newlisp"]
OPENEDGE_ABL_ALIAS_LANGS = ["openedge abl"]
RST_ALIAS_LANGS = ["restructuredtext"]
HAML_ALIAS_LANGS = ["haml"]
SLIM_ALIAS_LANGS = ["slim"]


@pytest.mark.parametrize("lang", C_STYLE_ALIAS_LANGS)
def test_c_style_aliases(lang):
    content = "/* block */\n// first\n// second\nvalue = 1;\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "// first\n// second" in texts


@pytest.mark.parametrize("lang", HASH_ALIAS_LANGS)
def test_hash_line_aliases(lang):
    content = '# first\n# second\n"""not a comment"""\nvalue = 1\n'
    comments = pc.extract_comments(content, [lang])

    blocks = [comment for comment in comments if comment[2] == "block"]
    assert not blocks
    assert [comment[1] for comment in comments] == ["# first\n# second"]


def test_cython_alias_keeps_python_block_behavior():
    content = '"""doc"""\n# first\n# second\nvalue = 1\n'
    comments = pc.extract_comments(content, ["cython"])

    texts = [comment[1] for comment in comments]
    assert '"""doc"""' in texts
    assert "# first\n# second" in texts


@pytest.mark.parametrize("lang", SEMICOLON_ALIAS_LANGS)
def test_semicolon_aliases(lang):
    content = "; first\n; second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["; first\n; second"]


@pytest.mark.parametrize("lang", MARKUP_ALIAS_LANGS)
def test_markup_aliases(lang):
    content = "<!-- block -->\n<tag />\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["<!-- block -->"]


@pytest.mark.parametrize("lang", HASKELL_ALIAS_LANGS)
def test_haskell_style_aliases(lang):
    content = "{- outer {- inner -} outer -}\n-- first\n-- second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "{- outer {- inner -} outer -}" in texts
    assert "-- first\n-- second" in texts


@pytest.mark.parametrize("lang", LEAN_ALIAS_LANGS)
def test_lean_aliases(lang):
    content = "/- outer /- inner -/ outer -/\n-- first\n-- second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/- outer /- inner -/ outer -/" in texts
    assert "-- first\n-- second" in texts


@pytest.mark.parametrize("lang", JSONNET_ALIAS_LANGS)
def test_jsonnet_style_aliases(lang):
    content = "# hash\n// slash\n/* block */\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "# hash\n// slash" in texts
    assert "/* block */" in texts


@pytest.mark.parametrize("lang", HASH_PIPE_ALIAS_LANGS)
def test_hash_pipe_aliases(lang):
    content = "#| outer #| inner |# outer |#\n; first\n; second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "#| outer #| inner |# outer |#" in texts
    assert "; first\n; second" in texts


@pytest.mark.parametrize("lang", NESTED_C_ALIAS_LANGS)
def test_nested_c_aliases(lang):
    content = "/* outer /* inner */ outer */\n// first\n// second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* outer /* inner */ outer */" in texts
    assert "// first\n// second" in texts


@pytest.mark.parametrize("lang", STAR_NESTED_ALIAS_LANGS)
def test_star_nested_aliases(lang):
    content = "(* outer (* inner *) outer *)\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["(* outer (* inner *) outer *)"]


@pytest.mark.parametrize("lang", EJS_ALIAS_LANGS)
def test_ejs_aliases(lang):
    content = "<%# block %>\n<%= value %>\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["<%# block %>"]


@pytest.mark.parametrize("lang", SQL_ALIAS_LANGS)
def test_sql_aliases(lang):
    content = "/* block */\n-- first\n-- second\nselect 1;\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "-- first\n-- second" in texts


@pytest.mark.parametrize("lang", DASH_ALIAS_LANGS)
def test_dash_aliases(lang):
    content = "-- first\n-- second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["-- first\n-- second"]


@pytest.mark.parametrize("lang", BANG_ALIAS_LANGS)
def test_bang_aliases(lang):
    content = "! first\n! second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["! first\n! second"]


@pytest.mark.parametrize("lang", SLASH_LINE_ALIAS_LANGS)
def test_slash_line_aliases(lang):
    content = "// first\n// second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["// first\n// second"]


@pytest.mark.parametrize("lang", PERCENT_ALIAS_LANGS)
def test_percent_aliases(lang):
    content = "% first\n% second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["% first\n% second"]


@pytest.mark.parametrize("lang", HASH_BLOCK_ALIAS_LANGS)
def test_hash_block_aliases(lang):
    content = "#[block]#\n# first\n# second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "#[block]#" in texts
    assert "# first\n# second" in texts


@pytest.mark.parametrize("lang", INI_ALIAS_LANGS)
def test_ini_aliases(lang):
    content = "; first\n# second\nvalue=1\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["; first\n# second"]


@pytest.mark.parametrize("lang", BASIC_ALIAS_LANGS)
def test_basic_aliases(lang):
    content = "' first\n' second\nREM third\nvalue = 1\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["' first\n' second\nREM third"]


@pytest.mark.parametrize("lang", APPLE_ALIAS_LANGS)
def test_applescript_aliases(lang):
    content = "(* block *)\n-- first\n-- second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "(* block *)" in texts
    assert "-- first\n-- second" in texts


@pytest.mark.parametrize("lang", AUTOIT_ALIAS_LANGS)
def test_autoit_aliases(lang):
    content = "#cs\nblock\n#ce\n; first\n; second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "#cs\nblock\n#ce" in texts
    assert "; first\n; second" in texts


@pytest.mark.parametrize("lang", ABAP_ALIAS_LANGS)
def test_abap_aliases(lang):
    content = '* first\n* second\nWRITE foo. " inline\n'
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "* first\n* second" in texts
    assert '" inline' in texts


@pytest.mark.parametrize("lang", BATCH_ALIAS_LANGS)
def test_batch_aliases(lang):
    content = ":: first\n:: second\nREM third\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == [":: first\n:: second\nREM third"]


@pytest.mark.parametrize("lang", COFFEE_ALIAS_LANGS)
def test_coffee_aliases(lang):
    content = "### block ###\n# first\n# second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "### block ###" in texts
    assert "# first\n# second" in texts


@pytest.mark.parametrize("lang", CSS_ALIAS_LANGS)
def test_css_aliases(lang):
    content = "/* block */\nselector {}\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["/* block */"]


@pytest.mark.parametrize("lang", POWERSHELL_ALIAS_LANGS)
def test_powershell_aliases(lang):
    content = "<# block #>\n# first\n# second\n$value = 1\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "<# block #>" in texts
    assert "# first\n# second" in texts


@pytest.mark.parametrize("lang", PASCAL_ALIAS_LANGS)
def test_pascal_aliases(lang):
    content = "{ block }\n(* alt block *)\n// first\n// second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "{ block }" in texts
    assert "(* alt block *)" in texts
    assert "// first\n// second" in texts


@pytest.mark.parametrize("lang", MAXSCRIPT_ALIAS_LANGS)
def test_maxscript_aliases(lang):
    content = "/* block */\n-- first\n-- second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "-- first\n-- second" in texts


@pytest.mark.parametrize("lang", VIML_ALIAS_LANGS)
def test_viml_aliases(lang):
    content = '  " first\n  " second\nlet g:x = 1\n'
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ['  " first\n  " second']


@pytest.mark.parametrize("lang", PERL6_ALIAS_LANGS)
def test_perl6_aliases(lang):
    content = "#'(block)\n# first\n# second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "#'(block)" in texts
    assert "# first\n# second" in texts


@pytest.mark.parametrize("lang", TWIG_ALIAS_LANGS)
def test_twig_aliases(lang):
    content = "{# block #}\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["{# block #}"]


@pytest.mark.parametrize("lang", SMARTY_ALIAS_LANGS)
def test_smarty_aliases(lang):
    content = "{* block *}\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["{* block *}"]


@pytest.mark.parametrize("lang", HANDLEBARS_ALIAS_LANGS)
def test_handlebars_aliases(lang):
    content = "{{! line }}\n{{!-- block --}}\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "{{! line }}" in texts
    assert "{{!-- block --}}" in texts


@pytest.mark.parametrize("lang", DJANGO_ALIAS_LANGS)
def test_django_aliases(lang):
    content = "{# line #}\n{% comment %}block{% endcomment %}\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "{# line #}" in texts
    assert "{% comment %}block{% endcomment %}" in texts


@pytest.mark.parametrize("lang", LIQUID_ALIAS_LANGS)
def test_liquid_aliases(lang):
    content = "{% comment %}block{% endcomment %}\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["{% comment %}block{% endcomment %}"]


@pytest.mark.parametrize("lang", MAKO_ALIAS_LANGS)
def test_mako_aliases(lang):
    content = "<%doc>block</%doc>\n## first\n## second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "<%doc>block</%doc>" in texts
    assert "## first\n## second" in texts


@pytest.mark.parametrize("lang", RHTML_ALIAS_LANGS)
def test_rhtml_aliases(lang):
    content = "<%# block %>\n<!-- html -->\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "<%# block %>" in texts
    assert "<!-- html -->" in texts


@pytest.mark.parametrize("lang", RDOC_ALIAS_LANGS)
def test_rdoc_aliases(lang):
    content = "# first\n=begin\nblock note\n=end\n/* c block */\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "# first" in texts
    assert "=begin\nblock note\n=end" in texts
    assert "/* c block */" in texts


@pytest.mark.parametrize("lang", COLDFUSION_ALIAS_LANGS)
def test_coldfusion_aliases(lang):
    content = "<!--- outer <!--- inner ---> outer --->\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["<!--- outer <!--- inner ---> outer --->"]


@pytest.mark.parametrize("lang", XQUERY_ALIAS_LANGS)
def test_xquery_aliases(lang):
    content = "(: outer (: inner :) outer :)\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["(: outer (: inner :) outer :)"]


@pytest.mark.parametrize("lang", SMALLTALK_ALIAS_LANGS)
def test_smalltalk_aliases(lang):
    content = '"block"\nvalue\n'
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ['"block"']


@pytest.mark.parametrize("lang", PROLOG_STYLE_ALIAS_LANGS)
def test_prolog_style_aliases(lang):
    content = "/* block */\n% first\n% second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "% first\n% second" in texts


@pytest.mark.parametrize("lang", SAS_ALIAS_LANGS)
def test_sas_aliases(lang):
    content = "/* block */\n* first;\nvalue;\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "* first;" in texts


@pytest.mark.parametrize("lang", STATA_ALIAS_LANGS)
def test_stata_aliases(lang):
    content = "/* block */\n* first\n// second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "* first\n// second" in texts


@pytest.mark.parametrize("lang", NONE_ALIAS_LANGS)
def test_none_aliases(lang):
    content = '{\"cells\": [], \"metadata\": {}}\n'
    comments = pc.extract_comments(content, [lang])

    assert comments == []


@pytest.mark.parametrize("lang", SEMICOLON_LINE_ONLY_EXTRA_LANGS)
def test_extra_semicolon_aliases(lang):
    content = "; first\n; second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["; first\n; second"]


@pytest.mark.parametrize("lang", JSP_ALIAS_LANGS)
def test_jsp_aliases(lang):
    content = "<%-- block --%>\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["<%-- block --%>"]


@pytest.mark.parametrize("lang", FREEMARKER_ALIAS_LANGS)
def test_freemarker_aliases(lang):
    content = "<#-- block -->\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["<#-- block -->"]


@pytest.mark.parametrize("lang", ASCIIDOC_ALIAS_LANGS)
def test_asciidoc_aliases(lang):
    content = "////\nblock\n////\n// first\n// second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "////\nblock\n////" in texts
    assert "// first\n// second" in texts


@pytest.mark.parametrize("lang", INFORM7_ALIAS_LANGS)
def test_inform7_aliases(lang):
    content = "[ block ]\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["[ block ]"]


@pytest.mark.parametrize("lang", HASH_CBLOCK_ALIAS_LANGS)
def test_hash_cblock_aliases(lang):
    content = "/* block */\n# first\n# second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "# first\n# second" in texts


@pytest.mark.parametrize("lang", APL_ALIAS_LANGS)
def test_apl_aliases(lang):
    content = "value <- 1 \u235D note\nvalue <- value + 1\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["\u235D note"]


@pytest.mark.parametrize("lang", ALLOY_ALIAS_LANGS)
def test_alloy_aliases(lang):
    content = "/* block */\n// first\ncode\n-- second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "// first" in texts
    assert "-- second" in texts


@pytest.mark.parametrize("lang", SEMICOLON_CSTYLE_ALIAS_LANGS)
def test_semicolon_cstyle_aliases(lang):
    content = "/* block */\n; first\n; second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "; first\n; second" in texts


@pytest.mark.parametrize("lang", BLITZMAX_ALIAS_LANGS)
def test_blitzmax_aliases(lang):
    content = "' first\ncode\nRem\nblock note\nEndRem\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "' first" in texts
    assert "Rem\nblock note\nEndRem" in texts


@pytest.mark.parametrize("lang", GAMS_ALIAS_LANGS)
def test_gams_aliases(lang):
    content = "* first\nvalue\n/* block */\nvalue = 1 !! inline\n$ontext\nblock two\n$offtext\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "* first" in texts
    assert "/* block */" in texts
    assert "!! inline" in texts
    assert "$ontext\nblock two\n$offtext" in texts


@pytest.mark.parametrize("lang", GCODE_ALIAS_LANGS)
def test_gcode_aliases(lang):
    content = "( block )\nG1 X1 ; first\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "( block )" in texts
    assert "; first" in texts


@pytest.mark.parametrize("lang", LOLCODE_ALIAS_LANGS)
def test_lolcode_aliases(lang):
    content = "BTW line\nHAI 1.2\nOBTW\nblock note\nTLDR\nKTHXBYE\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "BTW line" in texts
    assert "OBTW\nblock note\nTLDR" in texts


@pytest.mark.parametrize("lang", M4_ALIAS_LANGS)
def test_m4_aliases(lang):
    content = "dnl first\ndefine([name], [value])\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["dnl first"]


@pytest.mark.parametrize("lang", ORG_ALIAS_LANGS)
def test_org_aliases(lang):
    content = "# note\n#+BEGIN_COMMENT\nblock note\n#+END_COMMENT\nafter\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "# note" in texts
    assert "#+BEGIN_COMMENT\nblock note\n#+END_COMMENT" in texts


@pytest.mark.parametrize("lang", ANTLERS_ALIAS_LANGS)
def test_antlers_aliases(lang):
    content = "{{# block #}}\n{{ title }}\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["{{# block #}}"]


@pytest.mark.parametrize("lang", NUNJUCKS_ALIAS_LANGS)
def test_nunjucks_aliases(lang):
    content = "{# block #}\n{% if user %}ok{% endif %}\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["{# block #}"]


@pytest.mark.parametrize("lang", NEWLISP_ALIAS_LANGS)
def test_newlisp_aliases(lang):
    content = "; first\n# second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["; first\n# second"]


@pytest.mark.parametrize("lang", OPENEDGE_ABL_ALIAS_LANGS)
def test_openedge_abl_aliases(lang):
    content = "value // first\n/* outer /* inner */ outer */\nvalue//not\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "// first" in texts
    assert "/* outer /* inner */ outer */" in texts
    assert all("//not" not in text for text in texts)


@pytest.mark.parametrize("lang", RST_ALIAS_LANGS)
def test_restructuredtext_aliases(lang):
    content = "Heading\n\n.. keep hidden\n   still hidden\n\nText\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == [".. keep hidden\n   still hidden"]


@pytest.mark.parametrize("lang", J_ALIAS_LANGS)
def test_j_aliases(lang):
    content = "value =: 1 NB. inline note\nvalue =: 2\nNB. second\nvalue =: 3\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "NB. inline note" in texts
    assert "NB. second" in texts


@pytest.mark.parametrize("lang", HAML_ALIAS_LANGS)
def test_haml_aliases(lang):
    content = "prefix\n-# note\nbody\n  / note\n    hidden line\n  p visible\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "-# note" in texts
    assert "  / note\n    hidden line" in texts


@pytest.mark.parametrize("lang", SLIM_ALIAS_LANGS)
def test_slim_aliases(lang):
    content = "body\n  /! note\n    hidden line\n  p visible\n"
    comments = pc.extract_comments(content, [lang])

    assert [comment[1] for comment in comments] == ["  /! note\n    hidden line"]


NOISE_TOKENS = ("***", "###", "$$$", "%%%")


def _merged(*lines):
    return "\n".join(lines)


def _comment_line(prefix, text="adversarial *** ### $$$ %%%"):
    separator = "" if prefix.endswith(" ") else " "
    return f"{prefix}{separator}{text}"


def _block_body(*exclude):
    return _merged(
        *(
            f"{token} repeats at the start of a block-comment line"
            for token in NOISE_TOKENS
            if token not in exclude
        )
    )


def _delimited_block(opening, closing, *exclude):
    return _merged(opening, _block_body(*exclude), closing)


def _nested_block(opening, closing, *exclude):
    return _merged(
        f"{opening} outer comment begins",
        _block_body(*exclude),
        f"{opening} inner adversarial *** $$$ %%% {closing}",
        "outer comment resumes after the nested block",
        closing,
    )


def _case(*segments, trailer="value = 1"):
    content_parts = []
    expected = []
    for kind, text in segments:
        content_parts.append(text)
        expected.append((text, kind))
    content_parts.append(trailer)
    return {"content": "\n".join(content_parts) + "\n", "expected": expected}


def _none_case():
    return {
        "content": "value *** ### $$$ %%%\n### still not a comment\n$$$ still not a comment\n",
        "expected": [],
        "exact": True,
    }


CASE_C_STYLE = _case(
    ("block", _delimited_block("/*", "*/")),
    ("line", _merged(_comment_line("//"), _comment_line("//", "repeated ### *** $$$ %%%"))),
)
CASE_PYTHON_STYLE = _case(
    ("block", _delimited_block('"""', '"""', "###")),
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
)
CASE_HASH = _case(
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
)
CASE_HASH_CBLOCK = _case(
    ("block", _delimited_block("/*", "*/", "###")),
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
)
CASE_HASH_BLOCK = _case(
    ("block", _delimited_block("#[", "]#", "###")),
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
)
CASE_ERLANG = _case(
    ("line", _merged(_comment_line("%"), _comment_line("%", "repeated ### *** $$$ %%%"))),
)
CASE_JULIA = {
    "content": (
        _delimited_block("#=", "=#", "###")
        + "\nvalue = 1\n"
        + _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))
        + "\nvalue = 2\n"
    ),
    "expected": [
        (_delimited_block("#=", "=#", "###"), "block"),
        (_merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%")), "line"),
    ],
}
CASE_LISP = _case(
    ("line", _merged(_comment_line(";"), _comment_line(";", "repeated ### *** $$$ %%%"))),
    trailer="(print 1)",
)
CASE_FORTRAN = _case(
    ("line", _merged(_comment_line("!"), _comment_line("!", "repeated ### *** $$$ %%%"))),
    trailer="print *, 1",
)
CASE_COBOL = _case(
    ("block", "000100* adversarial *** ### $$$ %%%"),
    ("line", _merged(_comment_line("*>"), _comment_line("*>", "repeated ### *** $$$ %%%"))),
    trailer="       IDENTIFICATION DIVISION.",
)
CASE_HTML = _case(
    ("block", _delimited_block("<!--", "-->")),
    trailer="<tag />",
)
CASE_COLDFUSION = _case(
    ("block", _nested_block("<!---", "--->")),
    trailer="<cfset x = 1>",
)
CASE_ANTLERS = _case(
    ("block", _delimited_block("{{#", "#}}")),
    trailer="{{ title }}",
)
CASE_ASCIIDOC = _case(
    ("block", _delimited_block("////", "////")),
    ("line", _merged(_comment_line("//"), _comment_line("//", "repeated ### *** $$$ %%%"))),
    trailer="= Heading",
)
CASE_ALLOY = _case(
    ("block", _delimited_block("/*", "*/")),
    ("line", _merged(_comment_line("//"), _comment_line("--", "repeated ### *** $$$ %%%"))),
)
CASE_APL = _case(
    ("line", _merged(_comment_line("⍝"), _comment_line("⍝", "repeated ### *** $$$ %%%"))),
    trailer="A←1",
)
CASE_MATLAB = _case(
    ("block", _delimited_block("%{", "%}", "%%%")),
    ("line", _merged(_comment_line("%"), _comment_line("%", "repeated ### *** $$$ %%%"))),
)
CASE_WEBASSEMBLY = _case(
    ("block", _delimited_block("(;", ";)")),
    ("line", _merged(_comment_line(";;"), _comment_line(";;", "repeated ### *** $$$ %%%"))),
    trailer="(module)",
)
CASE_SEMICOLON_CSTYLE = _case(
    ("block", _delimited_block("/*", "*/")),
    ("line", _merged(_comment_line(";"), _comment_line(";", "repeated ### *** $$$ %%%"))),
)
CASE_INI = _case(
    ("line", _merged(_comment_line(";"), _comment_line("#", "repeated ### *** $$$ %%%"))),
    trailer="value=1",
)
CASE_TWIG = _case(
    ("block", _delimited_block("{#", "#}")),
    trailer="{{ value }}",
)
CASE_FREEMARKER = _case(
    ("block", _delimited_block("<#--", "-->")),
    trailer="${value}",
)
CASE_HANDLEBARS = _case(
    ("block", "{{! adversarial *** ### $$$ %%% }}"),
    ("block", _delimited_block("{{!--", "--}}")),
    trailer="{{ value }}",
)
CASE_SMARTY = _case(
    ("block", _delimited_block("{*", "*}")),
    trailer="{$value}",
)
CASE_BLITZMAX = _case(
    ("block", _merged("Rem", _block_body(), "EndRem")),
    ("line", _merged(_comment_line("'"), _comment_line("REM", "repeated ### *** $$$ %%%"))),
    trailer="Print 1",
)
CASE_JSP = _case(
    ("block", _delimited_block("<%--", "--%>")),
    trailer="<%= value %>",
)
CASE_LIQUID = _case(
    ("block", _merged("{% comment %}", _block_body(), "{% endcomment %}")),
    trailer="{{ value }}",
)
CASE_DJANGO = _case(
    ("block", _delimited_block("{#", "#}")),
    ("block", _merged("{% comment %}", _block_body(), "{% endcomment %}")),
    trailer="{{ value }}",
)
CASE_HAML = _case(
    ("line", _comment_line("-#")),
    (
        "block",
        _merged(
            "  / adversarial *** ### $$$ %%%",
            "    ### repeats inside the Haml block comment",
            "    *** repeats inside the Haml block comment",
            "    $$$ repeats inside the Haml block comment",
            "    %%% repeats inside the Haml block comment",
        ),
    ),
    trailer="%p visible",
)
CASE_MAKO = _case(
    ("block", _merged("<%doc>", _block_body(), "</%doc>")),
    ("line", _merged(_comment_line("##"), _comment_line("##", "repeated ### *** $$$ %%%"))),
    trailer="${value}",
)
CASE_RHTML = _case(
    ("block", _delimited_block("<%#", "%>")),
    ("block", _delimited_block("<!--", "-->")),
    trailer="<%= value %>",
)
CASE_RUBY = _case(
    ("block", _merged("=begin", _block_body("###"), "=end")),
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_ABAP = {
    "content": (
        "* adversarial *** ### $$$ %%%\n"
        "* repeated ### *** $$$ %%%\n"
        'WRITE value. " inline adversarial *** ### $$$ %%%\n'
    ),
    "expected": [
        ("* adversarial *** ### $$$ %%%\n* repeated ### *** $$$ %%%", "line"),
        ('" inline adversarial *** ### $$$ %%%', "line"),
    ],
}
CASE_MATHEMATICA = _case(
    ("block", _nested_block("(*", "*)")),
    trailer="x = 1",
)
CASE_DASH = _case(
    ("line", _merged(_comment_line("--"), _comment_line("--", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_APPLESCRIPT = {
    "content": (
        _delimited_block("(*", "*)", "###")
        + "\n-- adversarial *** $$$ %%%\n"
        + "# repeated ### *** $$$ %%%\n"
        + "set value to 1\n"
    ),
    "expected": [
        (_delimited_block("(*", "*)", "###"), "block"),
        ("-- adversarial *** $$$ %%%\n# repeated ### *** $$$ %%%", "line"),
    ],
}
CASE_AGDA = _case(
    ("block", _nested_block("{-", "-}")),
    ("line", _merged(_comment_line("--"), _comment_line("--", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_COQ = _case(
    ("block", _nested_block("(*", "*)")),
    trailer="Definition value := 1.",
)
CASE_FSHARP = _case(
    ("block", _nested_block("(*", "*)")),
    ("line", _merged(_comment_line("//"), _comment_line("//", "repeated ### *** $$$ %%%"))),
    trailer="let value = 1",
)
CASE_LEAN = _case(
    ("block", _nested_block("/-", "-/")),
    ("line", _merged(_comment_line("--"), _comment_line("--", "repeated ### *** $$$ %%%"))),
    trailer="def value := 1",
)
CASE_STAR_NESTED = _case(
    ("block", _nested_block("(*", "*)")),
    trailer="value = 1",
)
CASE_D = _case(
    ("block", _delimited_block("/**", "*/")),
    ("block", _delimited_block("/++", "+/")),
    ("line", _merged(_comment_line("///"), _comment_line("//", "repeated ### *** $$$ %%%"))),
    trailer="int value = 1;",
)
CASE_C_NESTED = _case(
    ("block", _nested_block("/*", "*/")),
    ("line", _merged(_comment_line("//"), _comment_line("//", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_CSS = _case(
    ("block", _delimited_block("/*", "*/")),
    trailer="selector {}",
)
CASE_FORTH = _case(
    ("block", _merged("(", _block_body(), ")")),
    ("line", _merged(_comment_line("\\ "), _comment_line("\\ ", "repeated ### *** $$$ %%%"))),
    trailer="1 2 +",
)
CASE_LUA = _case(
    ("block", _merged("--[[", _block_body(), "]]")),
    ("line", _merged(_comment_line("--"), _comment_line("--", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_BASIC = _case(
    ("line", _merged(_comment_line("'"), _comment_line("REM", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_GAMS = _case(
    ("block", _delimited_block("/*", "*/", "***")),
    ("block", _merged("$ontext", _block_body("***"), "$offtext")),
    ("line", _merged(_comment_line("*"), _comment_line("!!", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_GCODE = _case(
    ("block", "( adversarial *** ### $$$ %%% )"),
    ("line", _merged(_comment_line(";"), _comment_line(";", "repeated ### *** $$$ %%%"))),
    trailer="G1 X1",
)
CASE_PERCENT_CSTYLE = _case(
    ("block", _delimited_block("/*", "*/", "%%%")),
    ("line", _merged(_comment_line("%"), _comment_line("%", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_NONE = _none_case()
CASE_BATCHFILE = _case(
    ("line", _merged(_comment_line("::"), _comment_line("REM", "repeated ### *** $$$ %%%"))),
    trailer="echo value",
)
CASE_SMALLTALK = _case(
    ('block', _merged('"adversarial *** ### $$$ %%%', _block_body(), '"')),
    trailer="Transcript show: 'ok'.",
)
CASE_NEWLISP = {
    "content": "; adversarial *** $$$ %%%\n# repeated ### *** $$$ %%%\n(println 1)\n",
    "expected": [("; adversarial *** $$$ %%%\n# repeated ### *** $$$ %%%", "line")],
}
CASE_LOLCODE = _case(
    ("block", _merged("OBTW", _block_body(), "TLDR")),
    ("line", _comment_line("BTW")),
    trailer="KTHXBYE",
)
CASE_INFORM7 = _case(
    ("block", _merged("[ adversarial *** ### $$$ %%%", _block_body(), "]")),
    trailer="The Lab is a room.",
)
CASE_J = {
    "content": (
        "value =: 1 NB. adversarial *** ### $$$ %%%\n"
        "value =: 2\n"
        "NB. repeated ### *** $$$ %%%\n"
        "value =: 3\n"
    ),
    "expected": [
        ("NB. adversarial *** ### $$$ %%%", "line"),
        ("NB. repeated ### *** $$$ %%%", "line"),
    ],
}
CASE_AUTOIT = _case(
    ("block", _merged("#comments-start", _block_body(), "#comments-end")),
    ("line", _merged(_comment_line(";"), _comment_line(";", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_PERL = _case(
    ("block", _merged("=begin", _block_body("###"), "=cut")),
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
    trailer="my $value = 1;",
)
CASE_POWERSHELL = {
    "content": (
        _merged("<#", _block_body("###"), "#>")
        + "\n$value = 1\n"
        + _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))
        + "\n$value = 2\n"
    ),
    "expected": [
        (_merged("<#", _block_body("###"), "#>"), "block"),
        (_merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%")), "line"),
    ],
}
CASE_COFFEESCRIPT = _case(
    ("block", _merged("###", _block_body("###"), "###")),
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_LIVESCRIPT = {
    "content": (
        _delimited_block("/*", "*/", "###")
        + "\n"
        + _merged("###", _block_body("###"), "###")
        + "\nvalue = 1\n"
        + _merged(_comment_line("#"), _comment_line("//", "repeated ### *** $$$ %%%"))
        + "\nvalue = 2\n"
    ),
    "expected": [
        (_delimited_block("/*", "*/", "###"), "block"),
        (_merged("###", _block_body("###"), "###"), "block"),
        (_merged(_comment_line("#"), _comment_line("//", "repeated ### *** $$$ %%%")), "line"),
    ],
}
CASE_OPENEDGE_ABL = {
    "content": (
        "value // adversarial *** ### $$$ %%%\n"
        "/* outer comment begins\n"
        "### repeats at the start of a block-comment line\n"
        "/* inner adversarial *** $$$ %%% */\n"
        "outer comment resumes after the nested block\n"
        "*/\n"
        "next // repeated ### *** $$$ %%%\n"
        "value = 1\n"
    ),
    "expected": [
        ("// adversarial *** ### $$$ %%%", "line"),
        (
            "/* outer comment begins\n"
            "### repeats at the start of a block-comment line\n"
            "/* inner adversarial *** $$$ %%% */\n"
            "outer comment resumes after the nested block\n"
            "*/",
            "block",
        ),
        ("// repeated ### *** $$$ %%%", "line"),
    ],
}
CASE_PROLOG = _case(
    ("block", _delimited_block("/*", "*/", "%%%")),
    ("line", _merged(_comment_line("%"), _comment_line("%", "repeated ### *** $$$ %%%"))),
    trailer="goal :- ok.",
)
CASE_RDOC = _case(
    ("block", _merged("=begin", _block_body("###"), "=end")),
    ("block", _delimited_block("/*", "*/", "###")),
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_SAS = _case(
    ("line", _merged("* adversarial *** ### $$$ %%%;", "* repeated ### *** $$$ %%%;")),
    ("block", _delimited_block("/*", "*/", "***")),
    trailer="value = 1;",
)
CASE_STATA = _case(
    ("line", _merged(_comment_line("*"), _comment_line("//", "repeated ### *** $$$ %%%"))),
    ("block", _delimited_block("/*", "*/", "***")),
    trailer="value = 1",
)
CASE_RAKU = _case(
    ("block", _merged("#'(", _block_body("###"), ")")),
    ("block", "#'{ adversarial *** ### $$$ %%% }"),
    ("block", "#'[ adversarial *** ### $$$ %%% ]"),
    ("block", "#'< adversarial *** ### $$$ %%% >"),
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_SQL = _case(
    ("block", _delimited_block("/*", "*/")),
    ("line", _merged(_comment_line("--"), _comment_line("--", "repeated ### *** $$$ %%%"))),
    trailer="select 1;",
)
CASE_HASKELL = _case(
    ("block", _nested_block("{-", "-}")),
    ("line", _merged(_comment_line("--"), _comment_line("--", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_JSONNET = _case(
    ("block", _delimited_block("/*", "*/", "###")),
    ("line", _merged(_comment_line("#"), _comment_line("//", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_DASH_CSTYLE = _case(
    ("block", _delimited_block("/*", "*/")),
    ("line", _merged(_comment_line("--"), _comment_line("--", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_DASH_STAR_NESTED = _case(
    ("block", _nested_block("(*", "*)")),
    ("line", _merged(_comment_line("--"), _comment_line("--", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_BANG = _case(
    ("line", _merged(_comment_line("!"), _comment_line("!", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_SLASH_LINE = _case(
    ("line", _merged(_comment_line("//"), _comment_line("//", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_PERCENT = _case(
    ("line", _merged(_comment_line("%"), _comment_line("%", "repeated ### *** $$$ %%%"))),
    trailer="value = 1",
)
CASE_HASH_PIPE = _case(
    ("block", _nested_block("#|", "|#")),
    ("line", _merged(_comment_line(";"), _comment_line(";", "repeated ### *** $$$ %%%"))),
    trailer="(display 1)",
)
CASE_EJS = _case(
    ("block", _delimited_block("<%#", "%>")),
    trailer="<%= value %>",
)
CASE_PASCAL = _case(
    ("block", "{ adversarial *** ### $$$ %%% }"),
    ("block", _delimited_block("(*", "*)")),
    ("line", _merged(_comment_line("//"), _comment_line("//", "repeated ### *** $$$ %%%"))),
    trailer="value := 1;",
)
CASE_VIML = _case(
    ("line", _merged(_comment_line('  "'), _comment_line('  "', "repeated ### *** $$$ %%%"))),
    trailer="let g:value = 1",
)
CASE_M4 = _case(
    ("line", _merged(_comment_line("dnl"), _comment_line("dnl", "repeated ### *** $$$ %%%"))),
    trailer="define([value], [1])",
)
CASE_ORG = _case(
    ("block", _merged("#+BEGIN_COMMENT", _block_body("###"), "#+END_COMMENT")),
    ("line", _merged(_comment_line("#"), _comment_line("#", "repeated ### *** $$$ %%%"))),
    trailer="* Heading",
)
CASE_RST = _case(
    (
        "block",
        _merged(
            ".. adversarial *** ### $$$ %%%",
            "   ### stays in the reStructuredText comment",
            "   *** stays in the reStructuredText comment",
            "   $$$ stays in the reStructuredText comment",
            "   %%% stays in the reStructuredText comment",
        ),
    ),
    trailer="Title",
)
CASE_SLIM = _case(
    (
        "block",
        _merged(
            "  /! adversarial *** ### $$$ %%%",
            "    ### repeats inside the Slim block comment",
            "    *** repeats inside the Slim block comment",
            "    $$$ repeats inside the Slim block comment",
            "    %%% repeats inside the Slim block comment",
        ),
    ),
    trailer="  p visible",
)
CASE_XQUERY = _case(
    ("block", _nested_block("(:", ":)")),
    trailer="let $value := 1",
)


EXTRACTOR_ADVERSARIAL_CASES = {}


def _register(case, *extractors):
    for extractor in extractors:
        EXTRACTOR_ADVERSARIAL_CASES[extractor] = case


_register(CASE_C_STYLE, "extract_comments_java")
_register(CASE_PYTHON_STYLE, "extract_comments_python")
_register(CASE_HASH, "extract_comments_hash")
_register(CASE_HASH_CBLOCK, "extract_comments_hash_cblock")
_register(CASE_HASH_BLOCK, "extract_comments_hash_block")
_register(CASE_ERLANG, "extract_comments_erlang")
_register(CASE_JULIA, "extract_comments_julia")
_register(
    CASE_LISP,
    "extract_comments_lisp",
    "extract_comments_semicolon",
    "extract_comments_assembly",
)
_register(CASE_FORTRAN, "extract_comments_fortran")
_register(CASE_COBOL, "extract_comments_cobol")
_register(CASE_HTML, "extract_comments_html")
_register(CASE_COLDFUSION, "extract_comments_coldfusion")
_register(CASE_ANTLERS, "extract_comments_antlers")
_register(CASE_ASCIIDOC, "extract_comments_asciidoc")
_register(CASE_ALLOY, "extract_comments_alloy")
_register(CASE_APL, "extract_comments_apl")
_register(CASE_MATLAB, "extract_comments_matlab")
_register(CASE_WEBASSEMBLY, "extract_comments_webassembly")
_register(CASE_SEMICOLON_CSTYLE, "extract_comments_semicolon_cstyle")
_register(CASE_INI, "extract_comments_ini")
_register(CASE_TWIG, "extract_comments_twig")
_register(CASE_FREEMARKER, "extract_comments_freemarker")
_register(CASE_HANDLEBARS, "extract_comments_handlebars")
_register(CASE_SMARTY, "extract_comments_smarty")
_register(CASE_BLITZMAX, "extract_comments_blitzmax")
_register(CASE_JSP, "extract_comments_jsp")
_register(CASE_LIQUID, "extract_comments_liquid")
_register(CASE_DJANGO, "extract_comments_django")
_register(CASE_HAML, "extract_comments_haml")
_register(CASE_MAKO, "extract_comments_mako")
_register(CASE_RHTML, "extract_comments_rhtml")
_register(CASE_RUBY, "extract_comments_ruby")
_register(CASE_ABAP, "extract_comments_abap")
_register(CASE_MATHEMATICA, "extract_comments_mathematica")
_register(CASE_DASH, "extract_comments_ada", "extract_comments_dash")
_register(CASE_APPLESCRIPT, "extract_comments_applescript")
_register(CASE_AGDA, "extract_comments_agda")
_register(CASE_COQ, "extract_comments_coq")
_register(CASE_FSHARP, "extract_comments_fsharp")
_register(CASE_LEAN, "extract_comments_lean")
_register(CASE_STAR_NESTED, "extract_comments_star_nested")
_register(CASE_D, "extract_comments_d")
_register(CASE_C_NESTED, "extract_comments_c_nested")
_register(CASE_CSS, "extract_comments_css")
_register(CASE_FORTH, "extract_comments_forth")
_register(CASE_LUA, "extract_comments_lua")
_register(CASE_BASIC, "extract_comments_basic")
_register(CASE_GAMS, "extract_comments_gams")
_register(CASE_GCODE, "extract_comments_gcode")
_register(CASE_PERCENT_CSTYLE, "extract_comments_percent_cstyle")
_register(CASE_NONE, "extract_comments_none")
_register(CASE_BATCHFILE, "extract_comments_batchfile")
_register(CASE_SMALLTALK, "extract_comments_smalltalk")
_register(CASE_NEWLISP, "extract_comments_newlisp")
_register(CASE_LOLCODE, "extract_comments_lolcode")
_register(CASE_INFORM7, "extract_comments_inform7")
_register(CASE_J, "extract_comments_j")
_register(CASE_AUTOIT, "extract_comments_autoit")
_register(CASE_PERL, "extract_comments_perl")
_register(CASE_POWERSHELL, "extract_comments_powershell")
_register(CASE_COFFEESCRIPT, "extract_comments_coffeescript")
_register(CASE_LIVESCRIPT, "extract_comments_livescript")
_register(CASE_OPENEDGE_ABL, "extract_comments_openedge_abl")
_register(CASE_PROLOG, "extract_comments_prolog")
_register(CASE_RDOC, "extract_comments_rdoc")
_register(CASE_SAS, "extract_comments_sas")
_register(CASE_STATA, "extract_comments_stata")
_register(CASE_RAKU, "extract_comments_raku")
_register(CASE_SQL, "extract_comments_sql")
_register(CASE_HASKELL, "extract_comments_haskell")
_register(CASE_JSONNET, "extract_comments_jsonnet")
_register(CASE_DASH_CSTYLE, "extract_comments_dash_cstyle")
_register(CASE_DASH_STAR_NESTED, "extract_comments_dash_star_nested")
_register(CASE_BANG, "extract_comments_bang")
_register(CASE_SLASH_LINE, "extract_comments_slash_line")
_register(CASE_PERCENT, "extract_comments_percent")
_register(CASE_HASH_PIPE, "extract_comments_hash_pipe")
_register(CASE_EJS, "extract_comments_ejs")
_register(CASE_PASCAL, "extract_comments_pascal")
_register(CASE_VIML, "extract_comments_viml")
_register(CASE_M4, "extract_comments_m4")
_register(CASE_ORG, "extract_comments_org")
_register(CASE_RST, "extract_comments_restructuredtext")
_register(CASE_SLIM, "extract_comments_slim")
_register(CASE_XQUERY, "extract_comments_xquery")


IMPLEMENTED_LANGUAGE_CASES = sorted((lang, fn.__name__) for lang, fn in pc._LANG_EXTRACTORS.items())
IMPLEMENTED_EXTRACTORS = {extractor_name for _lang, extractor_name in IMPLEMENTED_LANGUAGE_CASES}
MISSING_ADVERSARIAL_CASES = sorted(IMPLEMENTED_EXTRACTORS - set(EXTRACTOR_ADVERSARIAL_CASES))


def test_adversarial_matrix_covers_all_implemented_extractors():
    assert MISSING_ADVERSARIAL_CASES == []


@pytest.mark.parametrize(
    "lang,extractor_name",
    IMPLEMENTED_LANGUAGE_CASES,
    ids=[f"{lang}:{extractor_name}" for lang, extractor_name in IMPLEMENTED_LANGUAGE_CASES],
)
def test_all_implemented_languages_handle_adversarial_comment_samples(lang, extractor_name):
    case = EXTRACTOR_ADVERSARIAL_CASES[extractor_name]
    comments = pc.extract_comments(case["content"], [lang])
    actual_pairs = [(comment[1], comment[2]) for comment in comments]

    if case.get("exact"):
        assert actual_pairs == case["expected"]
        return

    assert comments, f"expected adversarial comments for {lang}"
    for expected_pair in case["expected"]:
        assert expected_pair in actual_pairs, f"missing {expected_pair!r} for {lang}"


@pytest.mark.parametrize("lang", ATS_ALIAS_LANGS)
def test_ats_aliases(lang):
    content = "(* outer (* inner *) outer *)\n// first\n// second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "(* outer (* inner *) outer *)" in texts
    assert "// first\n// second" in texts


@pytest.mark.parametrize("lang", COOL_ALIAS_LANGS)
def test_cool_aliases(lang):
    content = "(* outer (* inner *) outer *)\n-- first\n-- second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "(* outer (* inner *) outer *)" in texts
    assert "-- first\n-- second" in texts


@pytest.mark.parametrize("lang", LILYPOND_ALIAS_LANGS)
def test_lilypond_aliases(lang):
    content = "%{\nblock note\n%}\n% first\n% second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "%{\nblock note\n%}" in texts
    assert "% first\n% second" in texts


@pytest.mark.parametrize("lang", LIVESCRIPT_ALIAS_LANGS)
def test_livescript_aliases(lang):
    content = "/* block */\n### alt block ###\n# first\n// second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "### alt block ###" in texts
    assert "# first\n// second" in texts


@pytest.mark.parametrize("lang", MIRAH_ALIAS_LANGS)
def test_mirah_aliases(lang):
    content = "# first\n# second\n=begin\nblock note\n=end\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "# first\n# second" in texts
    assert "=begin\nblock note\n=end" in texts


@pytest.mark.parametrize("lang", MOONSCRIPT_ALIAS_LANGS)
def test_moonscript_aliases(lang):
    content = "--[[\nblock note\n]]\n-- first\n-- second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "--[[\nblock note\n]]" in texts
    assert "-- first\n-- second" in texts


@pytest.mark.parametrize("lang", PERCENT_CSTYLE_ALIAS_LANGS)
def test_percent_cstyle_aliases(lang):
    content = "/* block */\n% first\n% second\nvalue\n"
    comments = pc.extract_comments(content, [lang])

    texts = [comment[1] for comment in comments]
    assert "/* block */" in texts
    assert "% first\n% second" in texts
