import pytest

from ml4setk import CommentQuery, CommentSanitizer, NestedCommentQuery, sanitize_comment
from ml4setk.Parsing.Comments import get_comment_syntax

pytestmark = pytest.mark.unit


def _matches(language: str, text: str) -> list[str]:
    matches = CommentQuery(language).parse(text)
    assert all(match.prefix + match.match + match.suffix == text for match in matches)
    starts = [len(match.prefix) for match in matches]
    assert starts == sorted(starts)
    return [match.match for match in matches]


@pytest.mark.parametrize(
    ("raw_label", "canonical_name", "family_name"),
    (
        ("Pyret", "pyret", "pyret_style"),
        ("Rez", "rez", "rez_style"),
        ("Roc", "roc", "roc_style"),
        ("Rocq Prover", "coq", "nested_star_style"),
        ("RBS", "rbs", "rbs_style"),
        ("RON", "ron", "ron_style"),
        ("Sail", "sail", "sail_style"),
        ("Scenic", "scenic", "scenic_style"),
        (
            "Simple File Verification",
            "simple_file_verification",
            "simple_file_verification_style",
        ),
        ("Slang", "slang", "slang_style"),
        ("Slint", "slint", "slint_style"),
        ("Smithy", "smithy", "smithy_style"),
        ("Snakemake", "snakemake", "snakemake_style"),
        ("Survex data", "survex_data", "survex_data_style"),
        ("Sway", "rust", "rust_style"),
        ("Tact", "java", "c_style"),
        ("templ", "templ", "templ_style"),
        ("Terraform Template", "terraform_template", "terraform_template_style"),
    ),
)
def test_batch_08_09_exact_stack_labels_resolve(
    raw_label: str,
    canonical_name: str,
    family_name: str,
) -> None:
    syntax = get_comment_syntax(raw_label)

    assert syntax.canonical_name == canonical_name
    assert syntax.family_name == family_name


@pytest.mark.parametrize("raw_label", ("QuickBASIC", "Sweave"))
def test_reviewed_deferred_labels_remain_unsupported(raw_label: str) -> None:
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        CommentQuery(raw_label)


@pytest.mark.parametrize(
    "source",
    (
        '// " fake\nfn value() {}\n/* actual */',
        '/* r###" fake */\nfn value() {}\n/* actual */',
    ),
)
def test_sway_comment_prose_does_not_open_literal_ranges(source: str) -> None:
    expected_first = source.split("\n", 1)[0]
    expected_nested = (
        [expected_first, "/* actual */"] if source.startswith("/*") else ["/* actual */"]
    )

    assert _matches("Sway", source) == [expected_first, "/* actual */"]
    assert [match.match for match in NestedCommentQuery("Sway").parse(source)] == expected_nested


def test_pyret_longest_opener_nesting_strings_and_malformed_eof() -> None:
    source = (
        'value = "# literal #| not a block |#" # line note\r\n'
        "value + #| outer #| inner |# tail |# 1\n"
        "#| unclosed\n# hidden"
    )

    assert _matches("Pyret", source) == [
        "# line note",
        "#| outer #| inner |# tail |#",
    ]
    assert sanitize_comment("Pyret", "#| outer #| inner |# tail |#") == ("outer #| inner |# tail")


def test_rez_splices_logical_lines_and_keeps_blocks_non_nested() -> None:
    source = (
        'resource "https://host/a//b"; // first\\\r\ncontinued\r\n'
        "/* outer /* not nested */ source\n"
        "/* unclosed\n// hidden"
    )

    assert _matches("Rez", source) == [
        "// first\\\r\ncontinued",
        "/* outer /* not nested */",
    ]


def test_roc_masks_codepoint_multiline_and_malformed_literals() -> None:
    source = (
        "char = '#'\n"
        'text = "# literal" # line note\n'
        'long = """# first\n# second"""\n'
        "#! /usr/bin/env roc\n"
        'broken = "# hidden'
    )

    assert _matches("Roc", source) == ["# line note", "#! /usr/bin/env roc"]
    assert sanitize_comment("Roc", "## documentation") == "# documentation"


def test_rocq_comment_internal_quotes_shield_delimiters() -> None:
    source = 'Definition x := 1. (* outer "quoted "" *) still quoted" tail *) Check x.'

    assert _matches("Rocq Prover", source) == ['(* outer "quoted "" *) still quoted" tail *)']
    assert _matches("coq", '(* outer "*) text" (* nested *) tail *)') == [
        '(* outer "*) text" (* nested *) tail *)'
    ]


@pytest.mark.parametrize(
    ("language", "source", "expected"),
    (
        ("Pyret", '#| outer " |# still quoted" tail |#', '#| outer " |#'),
        ("RON", '/* outer " */ still quoted" tail */', '/* outer " */'),
        ("Sail", '/* outer " */ still quoted" tail */', '/* outer " */'),
        ("Rust", '/* outer " */ still quoted" tail */', '/* outer " */'),
    ),
)
def test_rocq_quote_rule_does_not_change_other_nested_families(
    language: str,
    source: str,
    expected: str,
) -> None:
    assert _matches(language, source)[0] == expected


def test_rbs_shields_every_annotation_delimiter_and_quoted_name() -> None:
    source = (
        "%a{route#fragment} %a(item#part) %a[tag#part] "
        "%a|pipe#part| %a<angle#part> # annotation note\n"
        'type label = "name#part"\n'
        "%a{unterminated # hidden"
    )

    assert _matches("RBS", source) == ["# annotation note"]
    assert _matches("RBS", "type x = Integer # eof note") == ["# eof note"]


def test_rbs_lf_contract_retains_cr_and_lone_cr_does_not_terminate() -> None:
    assert _matches("RBS", "# first\r\n# second\n") == ["# first\r\n# second"]
    assert _matches("RBS", "# one\rcontinued") == ["# one\rcontinued"]


def test_ron_requires_lf_for_lines_and_complete_nested_blocks() -> None:
    source = (
        '(url: r#"// literal"#, // line note\r\n'
        " value: /* outer /* inner */ tail */ 1)\n"
        "// invalid eof"
    )

    assert _matches("RON", source) == [
        "// line note\r",
        "/* outer /* inner */ tail */",
    ]
    assert _matches("RON", "// lone cr\r") == []
    assert _matches("RON", "/* unclosed // hidden") == []


def test_sail_strict_lines_nested_docs_attributes_and_pragmas() -> None:
    source = (
        "/// register note\n"
        "/*! outer /* inner */ tail */\n"
        "$[attribute // rejected /* rejected */]\n"
        "$pragma value /* pragma note */   \n"
        'let url = "https://host/a//b"\n'
        "// invalid eof"
    )

    assert _matches("Sail", source) == [
        "/// register note",
        "/*! outer /* inner */ tail */",
        "/* pragma note */",
    ]
    assert sanitize_comment("Sail", "/// documentation") == "documentation"
    assert sanitize_comment("Sail", "/*! documentation */") == "documentation"


def test_sail_malformed_attribute_and_pragma_suppress_rejected_markers() -> None:
    assert _matches("Sail", "$[attribute // rejected") == []
    assert _matches("Sail", "$pragma value /* complete */ trailing // rejected\n") == []


@pytest.mark.parametrize("language", ("Scenic", "Snakemake"))
def test_python_token_languages_shield_all_string_forms(language: str) -> None:
    source = (
        "#!/usr/bin/env python\n"
        'a = "# ordinary"\n'
        "b = r'# raw'\n"
        'c = b"# bytes"\n'
        'd = f"# formatted {1}"\n'
        'e = """# multiline\n# still text"""\n'
        "value = 1 # actual note"
    )

    assert _matches(language, source) == [
        "#!/usr/bin/env python",
        "# actual note",
    ]
    assert _matches(language, 'value = "unterminated # hidden') == []


def test_simple_file_verification_requires_column_zero() -> None:
    source = "; Generated note\r\n file;part.bin DEADBEEF\n\t; not a comment\n;"

    assert _matches("Simple File Verification", source) == [
        "; Generated note",
        ";",
    ]
    assert sanitize_comment("sfv", "; generated metadata") == "generated metadata"


def test_slang_splices_lines_masks_raw_strings_and_is_non_nested() -> None:
    source = (
        "// logical note\\\ncontinued\n"
        'let raw = R"tag(// literal /* text */)tag";\n'
        "/* outer /* not nested */ source\n"
        "/* unclosed // hidden"
    )

    assert _matches("Slang", source) == [
        "// logical note\\\ncontinued",
        "/* outer /* not nested */",
    ]


def test_slint_reenters_code_inside_interpolated_strings() -> None:
    source = (
        'text: "literal // text \\{value // expression note\n} /* text */";\r\n'
        "/* outer /* inner */ tail */"
    )

    assert _matches("Slint", source) == [
        "// expression note",
        "/* outer /* inner */ tail */",
    ]
    assert _matches("Slint", 'text: "unterminated // hidden') == []
    assert _matches("Slint", 'text: "value \\{x // incomplete interpolation') == []


def test_smithy_shields_text_blocks_and_preserves_doc_slashes() -> None:
    source = (
        "string Name // ordinary note\r\n"
        'string Value = "// literal"\n'
        'metadata example = """// text block\n/// still text"""\n'
        "/// documentation note"
    )

    assert _matches("Smithy", source) == [
        "// ordinary note",
        "/// documentation note",
    ]
    assert sanitize_comment("Smithy", "/// documentation") == "/ documentation"
    assert _matches("Smithy", "/* not supported */") == []


def test_survex_tracks_marker_replacement_hex_eol_and_scope_restore() -> None:
    source = (
        "A B 1 2 3 ; default note\n"
        "*begin\n"
        "*set comment x25!\n"
        "A B 1 2 3 % percent note\n"
        "A B 1 2 3 ! bang note\n"
        "*set eol ^\n"
        "A B 1 2 3 % spans\nphysical line^"
        "*end^"
        "C D 1 2 3 ; restored note"
    )

    assert _matches("Survex data", source) == [
        "; default note",
        "% percent note",
        "! bang note",
        "% spans\nphysical line",
        "; restored note",
    ]
    assert CommentSanitizer("Survex data").sanitize("% dynamic note") == "dynamic note"


def test_survex_quote_role_and_invalid_set_preserve_current_map() -> None:
    source = (
        'A "station;name" B ; real note\n'
        "*set comment alphanumeric\n"
        "A B ; still active\n"
        '*set comment "\n'
        'A "quoted marker starts here'
    )

    assert _matches("Survex data", source) == [
        "; real note",
        "; still active",
        '"quoted marker starts here',
    ]


def test_sway_alias_is_recursive_and_honors_lf_line_contract() -> None:
    source = (
        'let url = r#"https://host/a//b"#;\n'
        "/* outer /* inner */ tail */\n"
        "// lone cr\rcontinues\n"
        "// eof note"
    )

    assert _matches("Sway", source) == [
        "/* outer /* inner */ tail */",
        "// lone cr\rcontinues",
        "// eof note",
    ]


def test_tact_alias_is_non_nested_and_masks_malformed_blocks() -> None:
    source = (
        'let url = "https://host/a//b";\n/* outer /* not nested */ return;\n/* unclosed\n// hidden'
    )

    assert _matches("Tact", source) == ["/* outer /* not nested */"]


def test_templ_respects_template_go_html_and_raw_element_modes() -> None:
    source = (
        "// top-level Go note\n"
        "templ render() {\n"
        "  <p>https://host/a//b</p>\n"
        "  // template Go note\n"
        "  <!-- rendered note -->\n"
        "  <script>/* client text */ // client text</script>\n"
        "  <style>/* css text */</style>\n"
        "}\n"
    )

    assert _matches("templ", source) == [
        "// top-level Go note",
        "// template Go note",
        "<!-- rendered note -->",
    ]
    assert sanitize_comment("templ", "<!-- rendered note -->") == "rendered note"


def test_templ_rejects_malformed_html_and_go_blocks() -> None:
    assert _matches("templ", "templ x() { <!-- bad -- inner --> }") == []
    assert _matches("templ", "templ x() { /* unclosed // hidden") == []
    assert _matches("templ", "templ x() { { value // incomplete expression") == []


def test_terraform_template_limits_comments_to_complete_code_modes() -> None:
    source = (
        "# literal heading\n"
        "https://host/a//b\n"
        "$${ // escaped literal }\n"
        "%%{ # escaped directive }\n"
        "${var.name /* block note */}\n"
        "${\n  # expression note\n  var.name\n}\n"
        "%{ if var.enabled // directive note\n}\n"
    )

    assert _matches("Terraform Template", source) == [
        "/* block note */",
        "# expression note",
        "// directive note",
    ]
    assert sanitize_comment("Terraform Template", "# expression note") == "expression note"


@pytest.mark.parametrize(
    "source",
    (
        "${var.name /* unclosed // hidden",
        "${var.name // close swallowed }",
        '${"# literal // literal"}',
        "%{ if var.enabled # no closing directive",
    ),
)
def test_terraform_template_malformed_or_string_modes_do_not_leak(source: str) -> None:
    assert _matches("Terraform Template", source) == []
