import pytest

from ml4setk import CommentQuery, CommentSanitizer, sanitize_comment
from ml4setk.Comment_util.parse_comment import extract_comments
from ml4setk.Parsing.Comments import SUPPORTED_LANGUAGES, get_comment_syntax

pytestmark = pytest.mark.unit


def _matches(language, text):
    matches = CommentQuery(language).parse(text)
    for match in matches:
        assert match.prefix + match.match + match.suffix == text
    starts = [len(match.prefix) for match in matches]
    assert starts == sorted(starts)
    assert all(
        starts[index] + len(matches[index].match) <= starts[index + 1]
        for index in range(len(matches) - 1)
    )
    return [match.match for match in matches]


@pytest.mark.parametrize(
    ("label", "canonical", "family"),
    (
        ("TextGrid", "textgrid", "textgrid_style"),
        ("Toit", "toit", "toit_style"),
        ("Tor Config", "tor_config", "tor_config_style"),
        ("Tree-sitter Query", "tree_sitter_query", "tree_sitter_query_style"),
        ("TypeSpec", "typespec", "typespec_style"),
        ("Typst", "typst", "typst_style"),
        ("Untyped Plutus Core", "agda", "nested_dash_style"),
    ),
)
def test_batch_10_supported_raw_labels_resolve(label, canonical, family):
    syntax = get_comment_syntax(label)

    assert syntax.canonical_name == canonical
    assert syntax.family_name == family


@pytest.mark.parametrize(
    ("label", "normalized", "candidate"),
    (
        ("TL-Verilog", "tl_verilog", "// unresolved /* syntax */"),
        ("TSPLIB data", "tsplib_data", "COMMENT : data field"),
        ("vCard", "vcard", "NOTE:This is data"),
        ("Befunge", "befunge", ">; dialect-dependent ;1.@"),
        ("C-ObjDump", "c_objdump", "# generated output"),
        ("Darcs Patch", "darcs_patch", "[generated patch data]"),
        ("Gemini", "gemini", "# heading, not a comment"),
        ("Python traceback", "python_traceback", "# displayed source data"),
    ),
)
def test_batch_10_rejected_labels_raise_from_every_public_api(
    label,
    normalized,
    candidate,
):
    assert normalized not in SUPPORTED_LANGUAGES
    for operation in (
        lambda: get_comment_syntax(label),
        lambda: CommentQuery(label),
        lambda: CommentSanitizer(label),
        lambda: sanitize_comment(label, candidate),
    ):
        with pytest.raises(NotImplementedError, match="Unsupported language"):
            operation()


@pytest.mark.parametrize(
    ("label", "source", "expected", "kind"),
    (
        ("TextGrid", "0 2.3 ! time note", "! time note", "line"),
        ("Toit", "value /* block note */", "/* block note */", "block"),
        ("Tor Config", "Nickname value#relay note", "#relay note", "line"),
        ("Tree-sitter Query", "(node) ; query note", "; query note", "line"),
        ("TypeSpec", "/** doc note */", "/** doc note */", "block"),
        ("Typst", "/* accepted through EOF", "/* accepted through EOF", "block"),
        (
            "Untyped Plutus Core",
            "{- outer {- note -} tail -}",
            "{- outer {- note -} tail -}",
            "block",
        ),
    ),
)
def test_batch_10_supported_labels_flow_through_legacy_adapter(
    label,
    source,
    expected,
    kind,
):
    start = source.index(expected)

    assert extract_comments(source, [label]) == [((start, start + len(expected)), expected, kind)]


def test_textgrid_extracts_only_explicit_unquoted_exclamation_comments():
    source = (
        '"ooTextFile"\n'
        '"TextGrid"\n'
        "xmin = 0\n"
        "0 2.3 ! time domain\r"
        '"IntervalTier" "Mary ! literal" ! type and name\n'
        '"say ""hi!""" ! eof note'
    )

    assert _matches("TextGrid", source) == [
        "! time domain",
        "! type and name",
        "! eof note",
    ]
    assert CommentSanitizer("TextGrid").sanitize("!  phonetic ə") == "phonetic ə"


def test_textgrid_unclosed_quote_protects_marker_text():
    assert _matches("TextGrid", '"unclosed ! literal\n! still literal') == []


def test_toit_preserves_nested_escape_and_interpolation_boundaries():
    source = (
        'text := "literal // $(1 /* expression note */) tail //"\n'
        "/// Toitdoc note\r\n"
        "/* outer /* nested */ tail */\n"
        "/* escaped \\*/ still comment */"
    )

    assert _matches("Toit", source) == [
        "/* expression note */",
        "/// Toitdoc note",
        "/* outer /* nested */ tail */",
        "/* escaped \\*/ still comment */",
    ]
    assert _matches("Toit", "/* unclosed") == []

    sanitizer = CommentSanitizer("Toit")
    assert sanitizer.sanitize("/// Toitdoc note") == "Toitdoc note"
    assert sanitizer.sanitize("/* outer /* nested */ tail */") == ("outer /* nested */ tail")


def test_tor_config_honors_quote_escape_and_lf_boundaries():
    source = (
        'DataDirectory "/srv/tor/#private"\n'
        "Nickname escaped\\#hash\n"
        "ContactInfo double\\\\#public\r\n"
        "# bare CR\rcontinued\n"
        "Nickname final#eof"
    )

    assert get_comment_syntax("Tor Config") is get_comment_syntax("torrc")
    assert _matches("Tor Config", source) == [
        "#public",
        "# bare CR\rcontinued",
        "#eof",
    ]
    assert CommentSanitizer("torrc").sanitize("#  keep spacing") == "keep spacing"


def test_tree_sitter_query_uses_lf_termination_and_groups_comment_lines():
    source = (
        "; first\r\n"
        "; second\n"
        '(node name: ";literal") @capture ; inline ;; payload\n'
        '(#match? @capture "a;b")'
    )

    assert _matches("Tree-sitter Query", source) == [
        "; first\r\n; second",
        "; inline ;; payload",
    ]
    assert CommentSanitizer("Tree-sitter Query").sanitize("; ; payload") == "; payload"


def test_tree_sitter_query_unclosed_strings_protect_until_lf():
    source = '"unclosed ; literal\rstill literal\n; recovered'

    assert _matches("Tree-sitter Query", source) == ["; recovered"]


def test_typespec_scans_template_expressions_but_shields_literal_spans():
    source = (
        "/** A stored widget. */\n"
        'const triple = """// literal\n/* literal */""";\n'
        'const template = "literal // ${value /* expression note */} tail /* literal */";\n'
        "model Widget { id: string; // identifier note\u2028}"
    )

    assert _matches("TypeSpec", source) == [
        "/** A stored widget. */",
        "/* expression note */",
        "// identifier note",
    ]
    assert _matches("TypeSpec", "/* unclosed") == []

    sanitizer = CommentSanitizer("TypeSpec")
    assert sanitizer.sanitize("/** @doc body */") == "@doc body"
    assert sanitizer.sanitize("// line body") == "line body"


def test_typst_shields_lexer_literals_and_accepts_unclosed_blocks():
    source = (
        "#!/usr/bin/env typst // shebang data\n"
        "https://typst.app/docs\n"
        "`// raw` and \\// escaped\n"
        '#let value = "/* string */ // literal"\n'
        "Text // line note\u0085"
        "/* outer /* nested */ tail */\n"
        "/* accepted through EOF"
    )

    assert _matches("Typst", source) == [
        "// line note",
        "/* outer /* nested */ tail */",
        "/* accepted through EOF",
    ]
    assert _matches("Typst", '#let value = "unclosed // literal') == []

    sanitizer = CommentSanitizer("Typst")
    assert sanitizer.sanitize("/* outer /* nested */ tail */") == ("outer /* nested */ tail")
    assert sanitizer.sanitize("/* accepted through EOF") == "accepted through EOF"


def test_untyped_plutus_core_reuses_unconditional_nested_dash_contract():
    source = (
        "-- program note\r\n"
        "(program 1.1.0\n"
        '  (con string "-- literal {- text -}")\n'
        "  {- outer {- nested -} tail -}\n"
        "  --+ unconditional symbol note\n"
        "  (lam x x))"
    )

    assert get_comment_syntax("Untyped Plutus Core") is get_comment_syntax("Agda")
    assert _matches("Untyped Plutus Core", source) == [
        "-- program note\r",
        "{- outer {- nested -} tail -}",
        "--+ unconditional symbol note",
    ]
    assert _matches("Untyped Plutus Core", "{- unclosed") == []

    sanitizer = CommentSanitizer("Untyped Plutus Core")
    assert sanitizer.sanitize("-- program note") == "program note"
    assert sanitizer.sanitize("{- outer {- nested -} tail -}") == ("outer {- nested -} tail")
