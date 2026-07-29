import pytest

from ml4setk import CommentSanitizer, sanitize_comment

pytestmark = pytest.mark.unit


def test_objective_j_preserves_content_bearing_bang_after_line_delimiter():
    raw_comment = (
        '//! runtextmacro MovementStart("MoveOne","n00O")\n    //! runtextmacro MovementEnd()'
    )

    assert sanitize_comment("objective_j", raw_comment) == (
        '! runtextmacro MovementStart("MoveOne","n00O")\n! runtextmacro MovementEnd()'
    )


def test_two_character_content_is_not_mistaken_for_an_empty_ruler():
    assert sanitize_comment("robots_txt", "#__") == "__"


def test_named_line_marker_is_preserved_as_content_inside_block_comment():
    assert sanitize_comment("harbour", "/* note */") == "note"


def test_forth_star_heading_is_content_without_a_complete_star_frame():
    assert sanitize_comment("forth", r"\ *** important ***") == "*** important ***"


def test_ada_diff_header_does_not_trigger_the_three_line_box_rule():
    assert sanitize_comment("ada", "--- src/file.orig") == "- src/file.orig"


def test_agda_bullet_does_not_trigger_the_multi_ruler_card_rule():
    assert sanitize_comment("agda", "-- - bullet") == "- bullet"


def test_fsharp_ordinary_block_does_not_trigger_the_backslash_capped_box_rule():
    assert sanitize_comment("f#", "(* ordinary * content *)") == "ordinary * content"


def test_gams_inline_stars_are_content_without_matching_triple_star_edges():
    assert sanitize_comment("gams", "* inline *** content") == "inline *** content"


def test_imagej_equals_banner_needs_both_triple_slash_gutters_to_preserve_padding():
    assert sanitize_comment("imagej_macro", "///========MACRO=========") == "MACRO"


@pytest.mark.parametrize(
    "raw_comment",
    [
        "// Intro\n//\n// --------\n//\n// Details",
        "/**\n * Intro\n *\n * --------\n *\n * Details\n */",
    ],
)
def test_isolated_markdown_thematic_break_is_preserved(raw_comment):
    assert sanitize_comment("c", raw_comment) == "Intro\n\n--------\n\nDetails"


def test_case_insensitive_language_lookup_still_applies_alias_specific_repairs():
    raw_comment = "'Limitations:\n'\n'* First\n'    continuation\n'* Second\n'    continuation"
    expected = "Limitations:\n\n* First\n    continuation\n* Second\n    continuation"

    assert sanitize_comment("brightscript", raw_comment) == expected
    assert sanitize_comment("BrightScript", raw_comment) == expected
    assert sanitize_comment("HTML+Django", "{## JR C sn ##}") == "# JR C sn #"


def test_sanitizer_preserves_the_callers_language_string():
    sanitizer = CommentSanitizer("BrightScript")

    assert sanitizer.language == "BrightScript"
