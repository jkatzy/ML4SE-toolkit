import pytest

from ml4setk import CommentQuery, sanitize_comment

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("language", "raw_comment", "expected"),
    [
        ("texinfo", "@c @subsection Hooks", "@subsection Hooks"),
        ("texinfo", "@comment  node-name", "node-name"),
        ("muse", "; TODO: keep #tag\n; second", "TODO: keep #tag\nsecond"),
        (
            "world_of_warcraft_addon_data",
            "#@no-lib-strip@",
            "@no-lib-strip@",
        ),
        ("dogescript", "shh much wow", "much wow"),
        (
            "dogescript",
            "quiet\n  this is a block\n  much wow\nloud",
            "this is a block\nmuch wow",
        ),
        ("runoff", ".! To produce help", "To produce help"),
        ("runoff", ".;COPYRIGHT", "COPYRIGHT"),
        ("batchfile", "::Enable feature", "Enable feature"),
        ("two_dimensional_array", "//recurve bow", "recurve bow"),
        ("two_dimensional_array", "#table note", "table note"),
        ("netlinx", "/* note */", "note"),
        ("xquery", "(:: pragma bea:test ::)", "pragma bea:test"),
        ("xquery", "(:~\n : docs\n :)", "docs"),
        ("nsis", "# note", "note"),
        ("smalltalk", '"instance creation"', "instance creation"),
    ],
)
def test_explicit_registry_wrappers_remove_language_scaffolding(
    language,
    raw_comment,
    expected,
):
    assert sanitize_comment(language, raw_comment) == expected


def test_word_comment_openers_require_a_token_boundary():
    assert sanitize_comment("dogescript", "shhh content") == "shhh content"
    assert sanitize_comment("batchfile", "REMOTE content") == "REMOTE content"


def test_wow_metadata_directive_is_not_extracted_as_a_comment():
    source = "## Interface: 100000\n# actual comment\nAddon.lua"

    matches = CommentQuery("world_of_warcraft_addon_data").parse(source)

    assert [match.match for match in matches] == ["# actual comment"]


@pytest.mark.parametrize("language", ["pug", "jade"])
def test_pug_family_uses_longest_opener_and_cleans_indentation_blocks(language):
    assert sanitize_comment(language, "//-#landing") == "#landing"
    assert sanitize_comment(language, "//- first\n//- second") == "first\nsecond"
    assert sanitize_comment(language, "  //- note\n    continued") == "note\ncontinued"
    assert sanitize_comment(language, "  //-\n    pagejs") == "pagejs"


def test_win32_mixed_comment_prefixes_are_removed_per_physical_line():
    raw_comment = ";/*++\n;\n;Module Name:\n;\n;    file.mc\n;\n;--*/\n;#pragma once"

    cleaned = sanitize_comment("win32_message_file", raw_comment)

    assert "Module Name:" in cleaned
    assert "file.mc" in cleaned
    assert "#pragma once" in cleaned
    assert ";/*" not in cleaned
    assert ";--*/" not in cleaned
    assert not any(line.startswith(";") for line in cleaned.splitlines())


def test_smalltalk_extraction_is_paired_and_cr_safe():
    source = '"first"\rObject new.\r"second"'

    matches = CommentQuery("smalltalk").parse(source)

    assert [match.match for match in matches] == ['"first"', '"second"']
    assert [sanitize_comment("smalltalk", match) for match in matches] == [
        "first",
        "second",
    ]


def test_adjacent_smalltalk_comments_clean_as_independent_paired_lines():
    matches = CommentQuery("smalltalk").parse('"first"\r"second"')

    assert len(matches) == 1
    assert sanitize_comment("smalltalk", matches[0]) == "first\nsecond"


def test_multiline_smalltalk_comment_does_not_consume_following_source():
    source = '"multi\rline"\rObject new.'

    matches = CommentQuery("smalltalk").parse(source)

    assert [match.match for match in matches] == ['"multi\rline"']
    assert sanitize_comment("smalltalk", matches[0]) == "multi\nline"


@pytest.mark.parametrize(
    ("language", "raw_comment", "expected"),
    [
        ("applescript", "# User-defined Attributes", "User-defined Attributes"),
        ("editorconfig", "; .editorconfig", ".editorconfig"),
        ("classic_asp", "<%'NPC召唤术", "NPC召唤术"),
        ("classic_asp", "<%'추가파일 %>", "추가파일"),
        (
            "r",
            "#' @title Score the measure\n#'\n#' @export",
            "@title Score the measure\n\n@export",
        ),
        (
            "fortran_free_form",
            "!> \\brief API docs\n!!@author Ada\n!$OMP PARALLEL",
            "\\brief API docs\n@author Ada\n$OMP PARALLEL",
        ),
        (
            "gleam",
            "//// # Module docs\n////\n//// ```\n//// ...\n//// ```",
            "# Module docs\n\n```\n...\n```",
        ),
        ("bro", "#! Logs socket activity.", "Logs socket activity."),
        ("bro", "##! Package documentation.", "Package documentation."),
        ("zeek", "#! Logs socket activity.", "Logs socket activity."),
        ("zeek", "##! Package documentation.", "Package documentation."),
        (
            "matlab",
            "%% Update NetworkGraph Interface\n% Output:",
            "Update NetworkGraph Interface\nOutput:",
        ),
        (
            "erlang",
            "%%% Module documentation\n%% @private",
            "Module documentation\n@private",
        ),
        ("sas", "*;", ""),
        (
            "sas",
            "*****Usual Descriptive Work*****;",
            "Usual Descriptive Work",
        ),
        ("handlebars", "{{!-- note --}}", "note"),
        ("mustache", "{{!-- Må velge én --}}", "Må velge én"),
        ("mustache", "{{!---- Nested value ----}}", "Nested value"),
        (
            "abap",
            '*"*"Global interface:\n*"  IMPORTING',
            "Global interface:\n IMPORTING",
        ),
        ("abap", "***INCLUDE ZXMPKZZZ .", "INCLUDE ZXMPKZZZ ."),
    ],
)
def test_language_specific_documentation_markers_are_removed(
    language,
    raw_comment,
    expected,
):
    assert sanitize_comment(language, raw_comment) == expected


def test_applescript_line_comment_extraction_stops_at_carriage_returns():
    source = "-- note\rproperty enabled : true\r# second\rproperty count : 2"

    matches = CommentQuery("applescript").parse(source)

    assert [match.match for match in matches] == ["-- note", "# second"]
    assert [sanitize_comment("applescript", match) for match in matches] == [
        "note",
        "second",
    ]


def test_classic_asp_comment_tags_clean_with_or_without_a_closing_tag():
    source = "<%'first\rResponse.Write Now()\r<%'second %>"

    matches = CommentQuery("classic_asp").parse(source)

    assert [match.match for match in matches] == ["<%'first", "<%'second %>"]
    assert [sanitize_comment("classic_asp", match) for match in matches] == [
        "first",
        "second",
    ]
