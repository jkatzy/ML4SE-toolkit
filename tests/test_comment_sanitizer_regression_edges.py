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


@pytest.mark.parametrize(
    ("language", "source", "raw_comment", "expected"),
    _PROSE_IN_INFERRED_WRAPPER_CASES,
)
def test_seeded_example_prose_is_not_inferred_as_comment_delimiter(
    language, source, raw_comment, expected
):
    _assert_extracts_and_cleans(language, source, raw_comment, expected)


def _assert_extracts_and_cleans(language, source, raw_comment, expected):
    assert [match.match for match in CommentQuery(language).parse(source)] == [raw_comment]
    assert sanitize_comment(language, raw_comment) == expected


_CASE_FIELDS = ("language", "source", "raw_comment", "expected")


def _inline_cases(language_cases):
    """Build params whose source places each raw comment between code lines."""

    return [
        pytest.param(language, f"x;\n{raw}\ny;", raw, expected, id=case_id)
        for case_id, language, raw, expected in language_cases
    ]


# A leading run of punctuation that only looks like a ruler is dropped while the
# matching trailing run, or the rest of the prose, survives. Doctest prompts,
# merge-conflict markers, and Markdown emphasis are content.
@pytest.mark.parametrize(
    _CASE_FIELDS,
    _inline_cases(
        (
            ("c-block-chevrons", "c", "/* <<< merge >>> */", "<<< merge >>>"),
            ("c-line-chevrons", "c", "// <<< merge >>>", "<<< merge >>>"),
            ("c-block-doctest", "c", "/* >>> prompt */", ">>> prompt"),
            ("java-block-doctest", "java", "/* >>> prompt */", ">>> prompt"),
            ("c-line-doctest", "c", "// >>> f()", ">>> f()"),
            ("c-line-conflict-marker", "c", "// <<<<<<< HEAD", "<<<<<<< HEAD"),
            ("c-block-conflict-marker", "c", "/* <<<<<<< HEAD */", "<<<<<<< HEAD"),
            ("c-block-bold", "c", "/* ** bold ** */", "** bold **"),
            ("c-line-bold", "c", "// ** bold **", "** bold **"),
        )
    ),
)
def test_leading_punctuation_run_is_content_not_a_ruler(language, source, raw_comment, expected):
    _assert_extracts_and_cleans(language, source, raw_comment, expected)


# GNU and OCaml styles align continuation lines with the text after the opener.
# Reviewed cleaning oracles (for example the Apache license and Benchmarks Game
# headers in ``tests/fixtures/comment_cleaning_regressions``) keep that
# alignment verbatim, so the cleaner must not dedent it.
@pytest.mark.parametrize(
    _CASE_FIELDS,
    _inline_cases(
        (
            ("c-two-lines", "c", "/* a\n   b */", "a\n   b"),
            (
                "c-three-lines",
                "c",
                "/* First line\n   second line\n   third */",
                "First line\n   second line\n   third",
            ),
            (
                "c-relative-indent",
                "c",
                "/* a\n     b indented more\n   c */",
                "a\n     b indented more\n   c",
            ),
            ("c-doc-opener", "c", "/** a\n    b */", "a\n    b"),
            ("java", "java", "/* a\n   b */", "a\n   b"),
            ("javascript", "javascript", "/* a\n   b */", "a\n   b"),
            ("rust", "rust", "/* a\n   b */", "a\n   b"),
            ("go", "go", "/* a\n   b */", "a\n   b"),
            ("ocaml", "ocaml", "(* a\n   b *)", "a\n   b"),
            ("ocaml-doc", "ocaml", "(** a\n    b *)", "a\n    b"),
        )
    ),
)
def test_block_continuation_aligned_with_opener_text_keeps_reviewed_indentation(
    language, source, raw_comment, expected
):
    _assert_extracts_and_cleans(language, source, raw_comment, expected)


# Documentation openers are already removed in their compact or line forms
# (``{-|``, ``-- |``, ``///``, ``/**``), but not in these equivalent spellings.
@pytest.mark.parametrize(
    _CASE_FIELDS,
    _inline_cases(
        (
            ("haskell-spaced-haddock", "haskell", "{- | doc -}", "doc"),
            ("purescript-spaced-haddock", "purescript", "{- | doc -}", "doc"),
            ("elm-spaced-doc", "elm", "{- | doc -}", "doc"),
            ("idris-spaced-doc", "idris", "{- | doc -}", "doc"),
            ("d-single-line-ddoc-plus", "d", "/++ doc +/", "doc"),
            ("lua-ldoc", "lua", "--- Doc comment", "Doc comment"),
            ("lua-luals-annotation", "lua", "---@param x number", "@param x number"),
            ("lua-ldoc-grouped", "lua", "--- a\n--- b", "a\nb"),
            ("luau-ldoc", "luau", "--- Doc comment", "Doc comment"),
            ("terra-ldoc", "terra", "--- Doc comment", "Doc comment"),
            ("moonscript-ldoc", "moonscript", "--- Doc comment", "Doc comment"),
        )
    ),
)
def test_documentation_opener_variants_are_removed(language, source, raw_comment, expected):
    _assert_extracts_and_cleans(language, source, raw_comment, expected)


# Inside a one-line block comment ``//`` cannot be a delimiter; it is
# commented-out code and must be kept.
@pytest.mark.parametrize(
    _CASE_FIELDS,
    _inline_cases(
        (
            ("c", "c", "/* // disabled code */", "// disabled code"),
            ("java", "java", "/* // x = 1; */", "// x = 1;"),
        )
    ),
)
def test_line_marker_inside_single_line_block_comment_is_content(
    language, source, raw_comment, expected
):
    _assert_extracts_and_cleans(language, source, raw_comment, expected)
