import pytest

from ml4setk import CommentQuery, CommentSanitizer

pytestmark = pytest.mark.unit


def _comment_matches(language, sample):
    return [match.match for match in CommentQuery(language).parse(sample)]


def _nl_binary_sample(first_line, payload="\x00# binary payload"):
    return (
        f"{first_line}\n"
        "0 0 0\n"
        "0 0\n"
        "0 0\n"
        "0 0\n"
        "0 0\n"
        "0 0\n"
        "0 0\n"
        "0 0\n"
        "0 0 0 0 0\n"
        f"{payload}"
    )


def test_checksums_only_accepts_column_zero_manifest_comments():
    sample = (
        "# note\n"
        "e3b0c44298fc1c149afbf4c8996fb924  file#part\n"
        " # indented data\n"
        "SHA256 (file#part) = e3b0c442\n"
    )

    assert _comment_matches("checksums", sample) == ["# note"]


def test_ecere_projects_masks_econ_strings_and_skips_quotes_in_comments():
    sample = (
        "{\n"
        '  "url": "https://example.test//path",\n'
        '  "marker": "/* data */",\n'
        '  // note with " quote\n'
        '  "value": 1,\n'
        '  /* block note with " quote */\n'
        '  "next": "https://example.test/next"\n'
        "}\n"
    )

    assert _comment_matches("ecere_projects", sample) == [
        '// note with " quote',
        '/* block note with " quote */',
    ]


def test_ecere_projects_block_comments_are_not_nested():
    sample = "{ /* outer /* inner */ tail */ value: 1 }"

    assert _comment_matches("ecere_projects", sample) == ["/* outer /* inner */"]


def test_visual_studio_solution_comments_must_occupy_the_line():
    sample = (
        "Microsoft Visual Studio Solution File, Format Version 12.00\r\n"
        "\t# note\r\n"
        "Global # inline data\r\n"
        'Project("{GUID}") = "#not-a-comment", "a.csproj", "{GUID}"\r\n'
    )

    assert _comment_matches("microsoft_visual_studio_solution", sample) == ["\t# note"]


def test_visual_studio_solution_uses_trim_whitespace_semantics():
    sample = "Microsoft Visual Studio Solution File\n\u2003# note\nGlobal\n"

    assert _comment_matches("microsoft_visual_studio_solution", sample) == [
        "\u2003# note"
    ]
    match = CommentQuery("microsoft_visual_studio_solution").parse(sample)[0]
    assert CommentSanitizer("microsoft_visual_studio_solution").sanitize(match) == "note"


def test_visual_studio_solution_supports_stream_reader_cr_lines():
    sample = "Microsoft Visual Studio Solution File\r# first\r\t# second\rGlobal\r"

    assert _comment_matches("microsoft_visual_studio_solution", sample) == [
        "# first\r\t# second"
    ]


def test_omgrofl_requires_a_complete_leading_w00t_token():
    sample = (
        "\tW00T note\r\n"
        "lol iz 71\r\n"
        "w00t\r\n"
        "lol iz 72 w00t trailing data\r\n"
        "w00tfoo\r\n"
        "#!/usr/bin/env omgrofl\r\n"
    )

    assert _comment_matches("omgrofl", sample) == ["\tW00T note", "w00t"]


def test_omgrofl_uses_java_whitespace_token_boundaries():
    sample = "\u2003W00T\fnote\nlol iz 71\n"

    matches = CommentQuery("omgrofl").parse(sample)

    assert [match.match for match in matches] == ["\u2003W00T\fnote"]
    assert CommentSanitizer("omgrofl").sanitize(matches[0]) == "note"


@pytest.mark.parametrize("separator", ["\u00a0", "\u2007", "\u202f"])
def test_omgrofl_rejects_non_breaking_token_separators(separator):
    assert _comment_matches("omgrofl", f"w00t{separator}not-a-comment\n") == []


def test_omgrofl_supports_java_scanner_line_separators():
    sample = "lol iz 71\u2028w00t first\u2029W00T second\u0085lol iz 72"

    matches = CommentQuery("omgrofl").parse(sample)

    assert [match.match for match in matches] == ["w00t first\u2029W00T second"]
    assert CommentSanitizer("omgrofl").sanitize(matches[0]) == "first\nsecond"


@pytest.mark.parametrize(
    ("sample", "expected"),
    [
        ("g3 0 1 0 # note\n", ["# note"]),
        ("b\t#5 bounds (on variables)\n", ["#5 bounds (on variables)"]),
        ("b # bounds\nn1 # note\n", ["# bounds", "# note"]),
        ("# standalone\n", []),
        ("h3:a#b\nn1 # note\n", ["# note"]),
        ("h3:#ab\n", []),
        ("h0:# trailing invalid raw-record data\n", []),
        ("h6:ab\n#cd\nn1 # note\n", ["# note"]),
        ("h10:ééééé\nn1 # note\n", ["# note"]),
        ("h\v3:a#b\nn1 # note\n", ["# note"]),
        ("h\f3:a#b\nn1 # note\n", ["# note"]),
        ("h999:a#b\nn1 # hidden by truncated payload\n", []),
    ],
)
def test_nl_text_records_respect_counted_raw_payloads(sample, expected):
    assert _comment_matches("nl", sample) == expected


def test_nl_binary_input_scans_only_the_ten_line_text_header():
    sample = _nl_binary_sample("b3 0 1 0 # note")

    assert _comment_matches("nl", sample) == ["# note"]


def test_nl_binary_header_may_omit_the_optional_option_count():
    sample = _nl_binary_sample("b")

    assert _comment_matches("nl", sample) == []


@pytest.mark.parametrize("separator", ["\v", "\f"])
def test_nl_binary_header_uses_c_whitespace(separator):
    sample = _nl_binary_sample(f"b{separator}0")

    assert _comment_matches("nl", sample) == []


def test_nl_annotated_binary_header_requires_the_complete_header_shape():
    complete = _nl_binary_sample("b # header annotation")
    fragment = "b # bounds\nn1 # note\n"

    assert _comment_matches("nl", complete) == ["# header annotation"]
    assert _comment_matches("nl", fragment) == ["# bounds", "# note"]


def test_nl_incomplete_binary_header_is_not_scanned():
    sample = "b3 0 1 0 # header-looking data\n0 0\n\x00# payload"

    assert _comment_matches("nl", sample) == []


def test_pogoscript_multiline_strings_hide_comment_markers():
    sample = (
        "single = 'first\n"
        "// string data\n"
        "/* string data */\n"
        "last'\n"
        'double = "first\n'
        "// string data\n"
        "/* string data */\n"
        'last"\n'
        "value = 1 // actual\n"
        "next = 2 /* actual block */\n"
    )

    assert _comment_matches("pogoscript", sample) == [
        "// actual",
        "/* actual block */",
    ]


def test_pogoscript_interpolation_keeps_real_comments_visible():
    sample = 'message = "before #(value // interpolation note\n) after"\n'

    assert _comment_matches("pogoscript", sample) == ["// interpolation note"]


def test_pogoscript_nested_interpolation_masks_only_literal_segments():
    sample = (
        'message = "before #((value + (1))) after // string data"\n'
        "value = 1 // actual\n"
    )

    assert _comment_matches("pogoscript", sample) == ["// actual"]


def test_pogoscript_crlf_interpolation_keeps_block_comments_visible():
    sample = (
        'message = "before\r\n'
        "#(value /* block ) note */\r\n"
        ') after"\r\n'
    )

    assert _comment_matches("pogoscript", sample) == ["/* block ) note */"]


@pytest.mark.parametrize(
    "sample",
    [
        "value = 'unterminated\n// malformed-source marker",
        'value = "unterminated\n// malformed-source marker',
    ],
)
def test_pogoscript_unterminated_strings_do_not_hide_later_markers(sample):
    assert _comment_matches("pogoscript", sample) == [
        "// malformed-source marker"
    ]


def test_pogoscript_malformed_interpolation_does_not_hide_the_rest_of_the_file():
    sample = 'message = "before #(value\n// malformed-source marker'

    assert _comment_matches("pogoscript", sample) == [
        "// malformed-source marker"
    ]


def test_pogoscript_unterminated_regexp_has_no_comment_match():
    assert _comment_matches("pogoscript", 'pattern = r/"unterminated') == []


@pytest.mark.parametrize("numeric_token", ["1", "0x1"])
def test_pogoscript_regexp_can_immediately_follow_a_numeric_token(numeric_token):
    sample = (
        f"x = {numeric_token}r/a\\/*b/\n"
        "next = 1 // actual\n"
    )

    assert _comment_matches("pogoscript", sample) == ["// actual"]


def test_pogoscript_skips_quotes_and_comment_markers_inside_other_tokens():
    sample = (
        '// " quote in an actual comment\n'
        "value = 'one '' // string data\n"
        "two'\n"
        'pattern = r/"\\/*"/g\n'
        "next = 1 /* actual block */\n"
    )

    assert _comment_matches("pogoscript", sample) == [
        '// " quote in an actual comment',
        "/* actual block */",
    ]


@pytest.mark.parametrize(
    ("sample", "expected"),
    [
        ("a // eof note", ["// eof note"]),
        ("a /* EOF note", ["/* EOF note"]),
        ("a /* outer /* inner */ tail */", ["/* outer /* inner */"]),
        ("#!/usr/bin/env pogo\na", []),
    ],
)
def test_pogoscript_comment_edges(sample, expected):
    assert _comment_matches("pogoscript", sample) == expected


def test_pogoscript_unterminated_block_sanitizes_through_eof():
    raw_comment = "/* EOF note\n second line"

    assert CommentSanitizer("pogoscript").sanitize(raw_comment) == ("EOF note\nsecond line")


@pytest.mark.parametrize("line_ending", ["\n", "\r\n", "\r"])
def test_figlet_font_extracts_the_counted_header_region(line_ending):
    sample = line_ending.join(
        (
            "flf2a$ 1 1 1 0 2",
            "first note",
            "  second note",
            "@ glyph sentinel",
            "",
        )
    )
    expected = f"first note{line_ending}  second note"

    assert _comment_matches("figlet_font", sample) == [expected]


def test_figlet_font_accepts_future_numeric_header_parameters():
    sample = "flf2a$ 1 1 1 0 1 0 0 0 42 43\nnote\n@ glyph sentinel\n"

    assert _comment_matches("figlet_font", sample) == ["note"]


def test_figlet_font_does_not_apply_quote_masking_to_the_hardblank():
    sample = 'flf2a" 1 1 1 0 1\nnote\n@ glyph sentinel\n'

    assert _comment_matches("figlet_font", sample) == ["note"]


def test_figlet_font_preserves_unicode_comment_payloads():
    sample = "flf2a$ 1 1 1 0 1\n注釈 Примечание ملاحظة 🧪\n@ glyph\n"

    assert _comment_matches("figlet_font", sample) == [
        "注釈 Примечание ملاحظة 🧪"
    ]


def test_figlet_font_preserves_a_declared_blank_comment_line():
    sample = "flf2a$ 1 1 1 0 1\n\n@ glyph sentinel\n"
    matches = CommentQuery("figlet_font").parse(sample)

    assert len(matches) == 1
    assert matches[0].prefix == "flf2a$ 1 1 1 0 1\n"
    assert matches[0].match == ""
    assert matches[0].suffix == "\n@ glyph sentinel\n"


def test_figlet_font_accepts_an_eof_terminated_final_comment_line():
    sample = "flf2a$ 1 1 1 0 2\nfirst note\nsecond note"

    assert _comment_matches("figlet_font", sample) == [
        "first note\nsecond note"
    ]


@pytest.mark.parametrize(
    "sample",
    [
        "flf2a$ 1 1 1 0 0\n@ glyph\n",
        "\ufeffflf2a$ 1 1 1 0 1\nnote\n",
        " flf2a$ 1 1 1 0 1\nnote\n",
        "flf2a$ 1 1 1 0 -1\nnote\n",
        "flf2a$ 1 1 1 0 nope\nnote\n",
        "flf2a  1 1 1 0 1\nnote\n",
        "flf2aé 1 1 1 0 1\nnote\n",
        "flf2a😀 1 1 1 0 1\nnote\n",
        "flf2a$\u00a01 1 1 0 1\nnote\n",
        "flf2a$ 1 1 1 0 3\nonly one terminated line\nsecond line",
    ],
)
def test_figlet_font_rejects_empty_or_malformed_comment_regions(sample):
    assert _comment_matches("figlet_font", sample) == []


def test_figlet_font_does_not_parse_markers_after_the_counted_region():
    sample = (
        "flf2a$ 1 1 1 0 1\n"
        "font note\n"
        "# glyph data\n"
        "// glyph data\n"
        "/* glyph data */\n"
        "flf2a$ 1 1 1 0 1\n"
        "not another comment\n"
    )

    assert _comment_matches("figlet_font", sample) == ["font note"]


def test_figlet_font_sanitizer_preserves_indentation_and_normalizes_newlines():
    raw_comment = "first\r\n  preserved indentation"

    assert CommentSanitizer("figlet_font").sanitize(raw_comment) == (
        "first\n  preserved indentation"
    )
