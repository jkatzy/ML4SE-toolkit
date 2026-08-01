import pytest

from ml4setk import CommentQuery, CommentSanitizer, sanitize_comment
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
        ("ISPC", "java", "c_style"),
        ("JCL", "jcl", "jcl_style"),
        ("Java Template Engine", "java_template_engine", "java_template_engine_style"),
        ("Just", "just", "just_style"),
        ("KDL", "kdl", "kdl_style"),
        ("KerboScript", "qsharp", "slash_line_style"),
        ("Kickstart", "kickstart", "kickstart_style"),
        ("Koka", "dafny", "nested_c_style"),
        ("Lean 4", "lean", "lean_style"),
    ),
)
def test_batch_04_raw_stack_labels_resolve(
    raw_label: str, canonical_name: str, family_name: str
) -> None:
    syntax = get_comment_syntax(raw_label)

    assert syntax.canonical_name == canonical_name
    assert syntax.family_name == family_name


def test_ispc_alias_preserves_c_lexical_boundaries_and_non_nesting() -> None:
    source = (
        'uniform const char *url = "https://host/a//b";\n'
        "uniform int ratio = total / count;\n"
        "uniform int lanes = 4; // line note\r\n"
        "/* outer /* not nested */\n"
        "/* unclosed\n"
        "// still inside the malformed block"
    )

    assert _matches("ISPC", source) == ["// line note", "/* outer /* not nested */"]
    assert sanitize_comment("ISPC", "/* payload * text */") == "payload * text"


def test_kerboscript_alias_masks_doubled_quotes_and_has_no_block_form() -> None:
    source = (
        'print "quoted "" // literal".\n'
        "set ratio to total / count.\n"
        "set throttle to 0.5. // ascent note\n"
        "/* not a KerboScript comment */\n"
        "// eof note"
    )

    assert _matches("KerboScript", source) == ["// ascent note", "// eof note"]
    assert sanitize_comment("KerboScript", "// keep periods.") == "keep periods."


def test_kerboscript_incomplete_string_does_not_leak_a_line_marker() -> None:
    assert _matches("KerboScript", 'print "unterminated // literal') == []


def test_koka_alias_masks_regular_character_and_multiline_raw_literals() -> None:
    source = (
        'val ordinary = "// literal /* data */"\n'
        "val character = '/'\n"
        'val raw = r#"first\n// raw data\n/* raw block */"#\n'
        "#line 20\n"
        "val x = 1 // line note\n"
        "/* outer /* inner */ outer */"
    )

    assert _matches("Koka", source) == [
        "// line note",
        "/* outer /* inner */ outer */",
    ]
    assert sanitize_comment("Koka", "/* outer /* inner */ outer */") == ("outer /* inner */ outer")


@pytest.mark.parametrize(
    "source",
    (
        'val raw = r##"// literal"#\n// still protected',
        "/* outer /* inner */\n// still protected",
    ),
)
def test_koka_malformed_protected_regions_do_not_leak(source: str) -> None:
    assert _matches("Koka", source) == []


def test_lean_4_preserves_doc_forms_and_uses_longest_sanitizer_wrappers() -> None:
    source = (
        'def marker := "/-- literal -/"\n'
        "-- line note\n"
        "/-- Declaration **documentation**. -/\n"
        "/-! Module documentation. -/\n"
        "/- outer /- inner -/ outer -/\n"
        "/- unclosed\n"
        "-- still inside the malformed block"
    )

    assert _matches("Lean 4", source) == [
        "-- line note",
        "/-- Declaration **documentation**. -/",
        "/-! Module documentation. -/",
        "/- outer /- inner -/ outer -/",
    ]
    sanitizer = CommentSanitizer("Lean 4")
    assert sanitizer.sanitize("/-- Declaration docs. -/") == "Declaration docs."
    assert sanitizer.sanitize("/-! Module docs. -/") == "Module docs."
    assert sanitizer.sanitize("/- ordinary -/") == "ordinary"


def test_kdl_extracts_line_nested_and_complete_slashdash_components() -> None:
    source = (
        'server text="// literal /- data" raw=r#"/* data */"# // line note\n'
        "server /* outer /* inner */ outer */ port=8080\n"
        "server /- old=true new=true\n"
        '/- legacy host="old.example" {\n  retry count=9\n}\n'
        'server host="new.example"\n'
    )

    assert _matches("KDL", source) == [
        "// line note",
        "/* outer /* inner */ outer */",
        "/- old=true",
        '/- legacy host="old.example" {\n  retry count=9\n}',
    ]


def test_kdl_excludes_version_marker_and_malformed_or_quoted_markers() -> None:
    source = (
        "/- kdl-version 2\n"
        'node value="/- literal // text"\n'
        "/-\n"
        "/* unclosed\n"
        "// hidden by malformed block"
    )

    assert _matches("KDL", source) == []


def test_kdl_sanitizer_preserves_nested_and_slashdashed_payloads() -> None:
    sanitizer = CommentSanitizer("KDL")

    assert sanitizer.sanitize("/* outer /* inner */ outer */") == ("outer /* inner */ outer")
    assert sanitizer.sanitize('/- old key="value" { child }') == ('old key="value" { child }')


def test_kdl_does_not_group_adjacent_slashdashed_nodes() -> None:
    source = "/- old value=1\n/- older value=2\n"

    assert _matches("KDL", source) == ["/- old value=1", "/- older value=2"]


def test_kickstart_tracks_host_ordinary_and_raw_section_states() -> None:
    source = (
        "#platform=x86,AMD64\n"
        "  # host note\n"
        'url --url="https://host/tree#fragment" # inline host note\n'
        "%packages\n"
        "# package-section note\n"
        "%end\n"
        "%pre\n"
        "#!/bin/sh\n"
        "echo value # shell data\n"
        "%end\n"
        "%certificate\n"
        "# certificate data\n"
        "%end\n"
        "%include /tmp/common.ks\n"
        "network --hostname=node # after include\n"
        "# final note"
    )

    assert _matches("Kickstart", source) == [
        "# host note",
        "# inline host note",
        "# package-section note",
        "# after include",
        "# final note",
    ]
    assert sanitize_comment("Kickstart", "# preserve # payload") == "preserve # payload"


def test_kickstart_unclosed_host_quote_does_not_leak_a_hash() -> None:
    assert _matches("Kickstart", 'url --url="unterminated # data') == []


def test_java_template_engine_only_extracts_native_text_mode_comments() -> None:
    source = (
        "Hello <%-- hidden native comment --%> world\n"
        "@raw <%-- rendered literally --%> @endraw\n"
        '${"<%-- Java string --%>"}\n'
        '@if("<%-- condition literal --%>".isEmpty()) text\n'
        "<!-- output HTML comment -->\n"
        "<%-- first <%-- nested-looking --%> tail --%>"
    )

    assert _matches("Java Template Engine", source) == [
        "<%-- hidden native comment --%>",
        "<%-- first <%-- nested-looking --%>",
    ]
    assert sanitize_comment("jte", "<%-- <b>payload</b> --%>") == "<b>payload</b>"


@pytest.mark.parametrize(
    "source",
    (
        "<%-- unclosed",
        "@raw\n<%-- literal without raw close --%>",
        '${"<%-- literal without expression close --%>"',
    ),
)
def test_java_template_engine_incomplete_modes_do_not_leak(source: str) -> None:
    assert _matches("Java Template Engine", source) == []


def test_java_template_engine_does_not_group_adjacent_native_blocks() -> None:
    source = "<%-- first --%>\n<%-- second --%>"

    assert _matches("Java Template Engine", source) == [
        "<%-- first --%>",
        "<%-- second --%>",
    ]


def test_jcl_tracks_fixed_comment_fields_and_instream_data_modes() -> None:
    source = (
        "//JOB1 JOB CLASS=A\n"
        "//* full statement note\n"
        " // * indented data, not a comment\n"
        "//STEP1 EXEC PGM=IEFBR14  compatibility no-op\n"
        "//SYSIN DD *\n"
        "//* DD star ends at this JCL statement\n"
        "//INPUT DD DATA\n"
        "//* data inside DD DATA\n"
        "/*\n"
        "//* after DATA\n"
        "//CUSTOM DD DATA,DLM='@@'\n"
        "//* custom-delimited data\n"
        "@@\n"
        "//* after custom delimiter"
    )

    assert _matches("JCL", source) == [
        "//* full statement note",
        "compatibility no-op",
        "//* DD star ends at this JCL statement",
        "//* after DATA",
        "//* after custom delimiter",
    ]
    assert sanitize_comment("JCL", "//* Preserve * alignment") == ("Preserve * alignment")


def test_jcl_trailing_field_respects_quotes_parentheses_and_sequence_columns() -> None:
    sequence = "12345678"
    source = "//A EXEC PARM=('A B',(C,D))  quoted parameter note".ljust(72) + sequence + "\r\n"

    assert _matches("JCL", source) == ["quoted parameter note"]


def test_just_excludes_recipe_bodies_but_keeps_native_header_comments() -> None:
    source = (
        'value := "# string data"\n'
        "# native documentation\n"
        "build: # native header note\n"
        "  echo value # recipe text\n"
        "  #!/usr/bin/env bash\n"
        "  # shell text\n"
        "# native after recipe\n"
        "set ignore-comments := true\n"
        "archive: dist.tar # native trailing"
    )

    assert _matches("Just", source) == [
        "# native documentation",
        "# native header note",
        "# native after recipe",
        "# native trailing",
    ]
    assert sanitize_comment("Just", "# preserve # payload") == "preserve # payload"


def test_just_unclosed_top_level_string_does_not_leak_hash() -> None:
    assert _matches("Just", 'value := "unterminated # data') == []


def test_jai_remains_explicitly_deferred() -> None:
    with pytest.raises(NotImplementedError, match="Jai"):
        get_comment_syntax("Jai")
    with pytest.raises(NotImplementedError, match="Jai"):
        CommentQuery("Jai")
