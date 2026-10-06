import pytest

from ml4setk import CommentQuery, CommentSanitizer, sanitize_comment

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


# Seeded registry examples whose prose leaks into an inferred sanitizer wrapper.
# ``_build_sanitizer_syntax`` splits each line example on its body placeholder,
# so words before "note" (``uplc``, ``reader``, ``font alias``) become part of
# the opening delimiter, and a multiline Liquid example turns its second line
# into a closing delimiter. The seeded example then loses content, and other
# comments with the real delimiter are not cleaned at all. Each case lists the
# seeded example and a variant with different prose; extraction is already
# correct, so the expected output is the comment body without its delimiters.
_PROSE_IN_INFERRED_WRAPPER_CASES = [
    pytest.param(
        language,
        source,
        raw_comment,
        expected,
        id=f"{language}-{case}",
    )
    for language in (
        "agda",
        "elm",
        "frege",
        "grammatical_framework",
        "literate_agda",
        "untyped_plutus_core",
    )
    for case, source, raw_comment, expected in (
        (
            "seeded",
            "(program 1.1.0 -- uplc note\n  (lam x x))",
            "-- uplc note",
            "uplc note",
        ),
        (
            "variant",
            "x -- uplc compiler output\ny",
            "-- uplc compiler output",
            "uplc compiler output",
        ),
    )
] + [
    pytest.param(
        "cweb",
        "@q reader note @>\n@c",
        "@q reader note @>",
        "reader note",
        id="cweb-seeded",
    ),
    pytest.param(
        "cweb",
        "@q Copyright 2024 @>\n@c",
        "@q Copyright 2024 @>",
        "Copyright 2024",
        id="cweb-variant",
    ),
    pytest.param(
        "x_font_directory_index",
        "! font alias note\nfixed -misc-fixed-medium-r-normal--13-120-75-75-c-70-iso10646-1",
        "! font alias note",
        "font alias note",
        id="x_font_directory_index-seeded",
    ),
    pytest.param(
        "x_font_directory_index",
        "! Copyright 1999\nfixed -misc-fixed-medium-r-normal--13-120-75-75-c-70-iso10646-1",
        "! Copyright 1999",
        "Copyright 1999",
        id="x_font_directory_index-variant",
    ),
    pytest.param(
        "liquid",
        "prefix\n{%\n  # note\n  # more\n%}\nsuffix",
        "{%\n  # note\n  # more\n%}",
        "note\nmore",
        id="liquid-multiline-seeded",
    ),
    pytest.param(
        "liquid",
        "prefix\n{%\n  # first line\n  # second line\n%}\nsuffix",
        "{%\n  # first line\n  # second line\n%}",
        "first line\nsecond line",
        id="liquid-multiline-variant",
    ),
]


@pytest.mark.xfail(
    strict=True,
    reason="Sanitizer infers wrappers from seeded example prose; remove when fixed.",
)
@pytest.mark.parametrize(
    ("language", "source", "raw_comment", "expected"),
    _PROSE_IN_INFERRED_WRAPPER_CASES,
)
def test_seeded_example_prose_is_not_inferred_as_comment_delimiter(
    language, source, raw_comment, expected
):
    assert [match.match for match in CommentQuery(language).parse(source)] == [raw_comment]
    assert sanitize_comment(language, raw_comment) == expected
