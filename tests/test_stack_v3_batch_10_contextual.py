import pytest

from ml4setk.Parsing.Comments.stack_v3_batch_10_contextual import (
    textgrid_comment_ranges,
    toit_comment_ranges,
    tor_config_comment_ranges,
    tree_sitter_query_comment_ranges,
    typespec_comment_ranges,
    typst_comment_ranges,
)

pytestmark = pytest.mark.unit


def _matches(extractor, text):
    ranges = extractor(text)
    assert ranges == tuple(sorted(ranges))
    assert all(ranges[index][1] <= ranges[index + 1][0] for index in range(len(ranges) - 1))
    assert all(0 <= start < end <= len(text) for start, end in ranges)
    return [text[start:end] for start, end in ranges]


def test_textgrid_extracts_explicit_comments_outside_doubled_quote_values():
    source = (
        '"ooTextFile"\r\n'
        '"TextGrid"\r'
        "0 2.3 ! time domain\r"
        '"IntervalTier" "Mary ! literal" ! type and name\n'
        '"say ""hi!""" ! doubled quote note'
    )

    assert _matches(textgrid_comment_ranges, source) == [
        "! time domain",
        "! type and name",
        "! doubled quote note",
    ]


def test_textgrid_malformed_quotes_and_full_format_scaffolding_are_protected():
    source = 'xmin = 0\nitem [1]:\n"unclosed ! literal\n! still literal'

    assert _matches(textgrid_comment_ranges, source) == []


def test_toit_extracts_line_doc_and_escape_aware_nested_blocks():
    source = (
        "main:\n"
        "  /// Toitdoc note\r"
        "  value := 1 // inline note\r\n"
        "  /* outer /* nested */ tail */\n"
        "  /* escaped \\*/ still comment */\n"
        "  /* escaped \\/* does not nest */"
    )

    assert _matches(toit_comment_ranges, source) == [
        "/// Toitdoc note",
        "// inline note",
        "/* outer /* nested */ tail */",
        "/* escaped \\*/ still comment */",
        "/* escaped \\/* does not nest */",
    ]


def test_toit_reenters_code_only_inside_parenthesized_interpolation():
    source = (
        'literal := "https://toit.io/* literal */ '
        '$(1 /* expression note */ + "// nested literal") tail // literal"\n'
        "char := '/'\n"
        "quotient := left / right\n"
        "// final note"
    )

    assert _matches(toit_comment_ranges, source) == [
        "/* expression note */",
        "// final note",
    ]


def test_toit_rejects_unclosed_blocks_and_protects_unclosed_literals():
    assert _matches(toit_comment_ranges, "/* never closed // still block") == []
    assert _matches(toit_comment_ranges, '"unclosed // literal') == []
    assert _matches(toit_comment_ranges, "'x // malformed character") == []
    assert _matches(toit_comment_ranges, "stray */ and left /= right") == []


def test_tor_config_handles_quotes_escape_parity_and_continuations():
    source = (
        'DataDirectory "/srv/tor/#private"\n'
        "Nickname escaped\\#hash\n"
        "ContactInfo double\\\\#public note\r\n"
        "Log notice file /tmp/log \\\n"
        " # continuation note\n"
        "%include /etc/tor/extra\n"
        "Nickname final#eof note"
    )

    assert _matches(tor_config_comment_ranges, source) == [
        "#public note",
        "# continuation note",
        "#eof note",
    ]


def test_tor_config_bare_cr_is_content_but_crlf_is_a_line_ending():
    source = "# before bare CR\rafter\nNext # windows\r\nLast # eof"

    assert _matches(tor_config_comment_ranges, source) == [
        "# before bare CR\rafter",
        "# windows",
        "# eof",
    ]


def test_tor_config_malformed_quotes_protect_the_remainder():
    assert _matches(tor_config_comment_ranges, 'Key "unclosed # literal\n# protected') == []
    assert _matches(tor_config_comment_ranges, "Nickname trailing\\") == []


def test_tree_sitter_query_extracts_semicolons_outside_strings():
    source = (
        "; file note\n"
        '(node name: ";literal") @capture ; inline note\n'
        '(#match? @capture "a\\";b")\n'
        "; eof note"
    )

    assert _matches(tree_sitter_query_comment_ranges, source) == [
        "; file note",
        "; inline note",
        "; eof note",
    ]


def test_tree_sitter_query_bare_cr_and_crlf_follow_lf_termination():
    source = "; bare\rcontent\n; windows\r\n"

    assert _matches(tree_sitter_query_comment_ranges, source) == [
        "; bare\rcontent",
        "; windows\r",
    ]


def test_tree_sitter_query_malformed_string_recovers_only_at_lf():
    source = '"unclosed ; literal\rstill literal\n; recovered'

    assert _matches(tree_sitter_query_comment_ranges, source) == ["; recovered"]
    assert _matches(tree_sitter_query_comment_ranges, '"incomplete escape \\; literal') == []


@pytest.mark.parametrize("terminator", ("\r", "\n", "\u2028", "\u2029"))
def test_typespec_line_comments_honor_compiler_line_breaks(terminator):
    source = f"// note{terminator}model Next {{}}"

    assert _matches(typespec_comment_ranges, source) == ["// note"]


def test_typespec_shields_literal_spans_but_scans_template_expressions():
    source = (
        'const ordinary = "https://host/a//literal";\n'
        'const triple = """\n// triple literal\n/* triple literal */\n""";\n'
        'const template = "literal // ${ {'
        ' value: "/* nested literal */"} /* expression note */ } tail /* literal */";\n'
        "// final note"
    )

    assert _matches(typespec_comment_ranges, source) == [
        "/* expression note */",
        "// final note",
    ]


def test_typespec_blocks_are_non_nested_and_must_close():
    source = "/** doc note */\n/* outer /* inner */ tail */"

    assert _matches(typespec_comment_ranges, source) == [
        "/** doc note */",
        "/* outer /* inner */",
    ]
    assert _matches(typespec_comment_ranges, "/* never closed") == []
    assert _matches(typespec_comment_ranges, '"unclosed // literal') == []
    assert _matches(typespec_comment_ranges, "#suppress #deprecated #{ #[ left / right") == []


@pytest.mark.parametrize(
    "terminator",
    ("\n", "\v", "\f", "\r", "\r\n", "\u0085", "\u2028", "\u2029"),
)
def test_typst_line_comments_honor_every_lexer_newline(terminator):
    source = f"// note{terminator}Text"

    assert _matches(typst_comment_ranges, source) == ["// note"]


def test_typst_extracts_nested_and_eof_terminated_blocks():
    source = "Text /* outer /* inner */ tail */ more\n/* accepted through EOF"

    assert _matches(typst_comment_ranges, source) == [
        "/* outer /* inner */ tail */",
        "/* accepted through EOF",
    ]
    assert _matches(typst_comment_ranges, "stray */ and division / value") == []


def test_typst_shields_raw_strings_urls_escapes_and_initial_shebang():
    source = (
        "#!/usr/bin/env typst // shebang data\n"
        "https://typst.app/*link-data*/\n"
        "http://example.test/path // actual note\n"
        "`// raw /* text */`\n"
        "```typ\n// raw block\n```\n"
        '#let value = "/* string */ // literal"\n'
        "\\// escaped markup\n"
        "// final note"
    )

    assert _matches(typst_comment_ranges, source) == [
        "// actual note",
        "// final note",
    ]


def test_typst_empty_double_backticks_do_not_hide_following_comments():
    source = "``// follows empty raw token"

    assert _matches(typst_comment_ranges, source) == ["// follows empty raw token"]


def test_typst_unclosed_string_and_raw_text_protect_the_remainder():
    assert _matches(typst_comment_ranges, '#let value = "unclosed // literal') == []
    assert _matches(typst_comment_ranges, "```unclosed // raw") == []
