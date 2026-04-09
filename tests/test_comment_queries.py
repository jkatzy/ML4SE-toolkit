import importlib
import warnings

import pytest

from ml4setk import (
    CommentQuery,
    LineCommentQuery,
    NestedCommentQuery,
    OpeningCommentQuery,
    QueryMatch,
)
from ml4setk.Parsing.Comments import get_comment_syntax, iter_comment_syntaxes

pytestmark = pytest.mark.unit


def _expected_query_match(sample, expected_match):
    start = sample.index(expected_match)
    end = start + len(expected_match)
    return QueryMatch(sample[:start], sample[end:], expected_match)


def _iter_regex_cases():
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            for index, example in enumerate(syntax.shared_regex_examples):
                yield pytest.param(language, example, id=f"{language}-shared-regex-{index}")

        for index, example in enumerate(syntax.canonical_regex_examples):
            yield pytest.param(
                syntax.canonical_name,
                example,
                id=f"{syntax.canonical_name}-canonical-regex-{index}",
            )


def _iter_nested_cases():
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            for index, example in enumerate(syntax.shared_nested_examples):
                yield pytest.param(language, example, id=f"{language}-shared-nested-{index}")

        for index, example in enumerate(syntax.canonical_nested_examples):
            yield pytest.param(
                syntax.canonical_name,
                example,
                id=f"{syntax.canonical_name}-canonical-nested-{index}",
            )


def _iter_nested_only_languages():
    for syntax in iter_comment_syntaxes():
        if syntax.nested_delimiters and not syntax.regex_patterns:
            for language in syntax.language_names:
                yield pytest.param(language, id=f"{language}-nested-only")


def _iter_regex_only_cases():
    for syntax in iter_comment_syntaxes():
        if syntax.regex_patterns and not syntax.nested_delimiters:
            examples = syntax.shared_regex_examples or syntax.canonical_regex_examples
            for language in syntax.language_names:
                yield pytest.param(language, examples[0], id=f"{language}-regex-only")


REGEX_CASES = list(_iter_regex_cases())
NESTED_CASES = list(_iter_nested_cases())
NESTED_ONLY_LANGUAGES = list(_iter_nested_only_languages())
REGEX_ONLY_CASES = list(_iter_regex_only_cases())


@pytest.mark.parametrize(("language", "example"), REGEX_CASES)
def test_line_comment_query_matches_registry_examples(language, example):
    matches = LineCommentQuery(language).parse(example.sample)

    assert matches
    assert matches[0] == _expected_query_match(example.sample, example.expected_match)


@pytest.mark.parametrize(("language", "example"), REGEX_CASES)
def test_line_comment_query_contains_registry_examples(language, example):
    assert LineCommentQuery(language).contains(example.sample) is True


@pytest.mark.parametrize("language", NESTED_ONLY_LANGUAGES)
def test_line_comment_query_returns_no_matches_for_nested_only_languages(language):
    sample = "before (* note *) after"
    query = LineCommentQuery(language)

    assert query.contains(sample) is False
    assert query.parse(sample) == []


@pytest.mark.parametrize(("language", "example"), NESTED_CASES)
def test_nested_comment_query_matches_registry_examples(language, example):
    matches = NestedCommentQuery(language).parse(example.sample)

    assert matches == [_expected_query_match(example.sample, example.expected_match)]
    assert NestedCommentQuery(language).contains(example.sample) is True


@pytest.mark.parametrize(("language", "example"), REGEX_ONLY_CASES)
def test_nested_comment_query_returns_no_matches_for_regex_only_languages(language, example):
    query = NestedCommentQuery(language)

    assert query.contains(example.sample) is False
    assert query.parse(example.sample) == []


def test_comment_query_combines_nested_and_line_matches_in_source_order():
    sample = "before {- block -} middle -- line\nafter"

    matches = CommentQuery("haskell").parse(sample)

    assert matches == [
        QueryMatch("before ", " middle -- line\nafter", "{- block -}"),
        QueryMatch("before {- block -} middle ", "\nafter", "-- line"),
    ]


def test_comment_query_contains_when_either_strategy_matches():
    assert CommentQuery("java").contains("before // line\nafter") is True
    assert CommentQuery("haskell").contains("before {- block -} after") is True


def test_comment_query_contains_returns_false_when_no_comment_is_present():
    assert CommentQuery("java").contains("int x = 1;\nreturn x;") is False


def test_comment_query_accepts_multiple_languages_and_returns_union_of_matches():
    sample = "value = 1 # note\n/* block */\nreturn value\n"

    assert CommentQuery(["python", "java"]).parse(sample) == [
        _expected_query_match(sample, "# note"),
        _expected_query_match(sample, "/* block */"),
    ]


def test_comment_query_multiple_languages_dedupes_identical_matches():
    sample = "before /* note */ after"

    assert CommentQuery(["java", "css"]).parse(sample) == [
        _expected_query_match(sample, "/* note */")
    ]


def test_comment_query_multiple_languages_contains_when_any_language_matches():
    assert CommentQuery(["python", "java"]).contains("value = 1 # note") is True
    assert CommentQuery(["python", "java"]).contains("int x = 1;") is False


def test_comment_query_multiple_languages_validates_input():
    with pytest.raises(ValueError):
        CommentQuery([])

    with pytest.raises(TypeError):
        CommentQuery(["python", 1])


@pytest.mark.parametrize(
    ("language", "sample", "expected_match"),
    [
        pytest.param(
            "java",
            "int x = 1;\n// first line\n// second line\nreturn x;",
            "// first line\n// second line",
            id="java-grouped-line-block",
        ),
        pytest.param(
            "python",
            "value = 1\n# first line\n# second line\nprint(value)",
            "# first line\n# second line",
            id="python-grouped-line-block",
        ),
        pytest.param(
            "haskell",
            "value = 1\n-- first line\n-- second line\nvalue + 1",
            "-- first line\n-- second line",
            id="haskell-grouped-line-block",
        ),
    ],
)
def test_comment_query_groups_adjacent_standalone_line_comments(language, sample, expected_match):
    assert CommentQuery(language).parse(sample) == [_expected_query_match(sample, expected_match)]


@pytest.mark.parametrize(
    ("language", "sample", "expected_match"),
    [
        pytest.param("java", "int x = 1; // note\nreturn x;", "// note", id="java-inline-line"),
        pytest.param(
            "python",
            "value = 1  # note\nprint(value)",
            "# note",
            id="python-inline-line",
        ),
        pytest.param(
            "haskell",
            "value = 1 -- note\nvalue + 1",
            "-- note",
            id="haskell-inline-line",
        ),
        pytest.param("cobol", "MOVE A TO B *> note", "*> note", id="cobol-inline-line"),
        pytest.param("java", "int /* note */ x = 1;", "/* note */", id="java-inline-block"),
        pytest.param("html", "<div><!-- note --></div>", "<!-- note -->", id="html-inline-block"),
    ],
)
def test_comment_query_parses_inline_comments(language, sample, expected_match):
    assert CommentQuery(language).parse(sample) == [_expected_query_match(sample, expected_match)]


@pytest.mark.parametrize(
    ("language", "sample", "expected_match"),
    [
        pytest.param(
            "java",
            "int x = 1; // note\n// follow-up\nreturn x;",
            ["// note", "// follow-up"],
            id="java-inline-then-standalone",
        ),
        pytest.param(
            "python",
            "value = 1  # note\n# follow-up\nprint(value)",
            ["# note", "# follow-up"],
            id="python-inline-then-standalone",
        ),
    ],
)
def test_comment_query_does_not_group_inline_comments_with_following_comment_lines(
    language, sample, expected_match
):
    assert CommentQuery(language).parse(sample) == [
        _expected_query_match(sample, match) for match in expected_match
    ]


@pytest.mark.parametrize(
    ("language", "sample", "expected_match"),
    [
        pytest.param(
            "java",
            "// first line\nint x = 1; // inline\nreturn x;",
            ["// first line", "// inline"],
            id="java-standalone-then-inline",
        ),
        pytest.param(
            "python",
            "# first line\n\n# second line\nprint(value)",
            ["# first line", "# second line"],
            id="python-blank-line-splits-block",
        ),
    ],
)
def test_comment_query_splits_grouped_line_comments_when_continuity_breaks(
    language, sample, expected_match
):
    assert CommentQuery(language).parse(sample) == [
        _expected_query_match(sample, match) for match in expected_match
    ]


@pytest.mark.parametrize(
    ("language", "sample", "expected_match"),
    [
        pytest.param("lua", "x = 1\n--[[ note ]]\ny = 2", "--[[ note ]]", id="lua-block-dedupe"),
        pytest.param("matlab", "x = 1\n%{ note %}\ny = 2", "%{ note %}", id="matlab-block-dedupe"),
    ],
)
def test_line_comment_query_dedupes_overlapping_block_matches(language, sample, expected_match):
    assert LineCommentQuery(language).parse(sample) == [
        _expected_query_match(sample, expected_match)
    ]


@pytest.mark.parametrize(("language", "example"), NESTED_CASES)
def test_comment_query_surfaces_nested_matches(language, example):
    assert CommentQuery(language).parse(example.sample) == [
        _expected_query_match(example.sample, example.expected_match)
    ]


@pytest.mark.parametrize(
    ("language", "sample", "expected_match"),
    [
        pytest.param(
            "java",
            "before /* outer // inner */ after",
            "/* outer // inner */",
            id="java-outer-block-over-line",
        ),
        pytest.param(
            "haskell",
            "before {- outer -- inner -} after",
            "{- outer -- inner -}",
            id="haskell-outer-nested-over-line",
        ),
        pytest.param(
            "nim",
            "before #[ outer # inner ]# after",
            "#[ outer # inner ]#",
            id="nim-outer-nested-over-line",
        ),
        pytest.param(
            "haskell",
            "before {- outer {- inner -} outer -} after",
            "{- outer {- inner -} outer -}",
            id="haskell-outer-nested-over-nested",
        ),
        pytest.param(
            "ocaml",
            "before (* outer (* inner *) outer *) after",
            "(* outer (* inner *) outer *)",
            id="ocaml-outer-nested-over-nested",
        ),
    ],
)
def test_comment_query_prefers_outermost_comment_when_comment_forms_overlap(
    language, sample, expected_match
):
    assert CommentQuery(language).parse(sample) == [_expected_query_match(sample, expected_match)]


def test_nested_comment_query_ignores_unclosed_nested_comments():
    sample = "before {- open only after"

    assert NestedCommentQuery("haskell").contains(sample) is False
    assert NestedCommentQuery("haskell").parse(sample) == []


@pytest.mark.parametrize(
    ("language", "sample"),
    [
        pytest.param("java", "value = 1;\n/* open only\nreturn value;\n", id="java-unclosed-block"),
        pytest.param("html", "<div><!-- open only</div>", id="html-unclosed-block"),
    ],
)
def test_comment_query_ignores_unclosed_non_nested_block_comments(language, sample):
    assert CommentQuery(language).contains(sample) is False
    assert CommentQuery(language).parse(sample) == []


@pytest.mark.parametrize(
    ("language", "sample"),
    [
        pytest.param("java", "before */ after", id="java-stray-close"),
        pytest.param("haskell", "before -} after", id="haskell-stray-close"),
        pytest.param("ocaml", "before *) after", id="ocaml-stray-close"),
        pytest.param("html", "before --> after", id="html-stray-close"),
    ],
)
def test_comment_query_ignores_stray_closing_delimiters(language, sample):
    assert CommentQuery(language).contains(sample) is False
    assert CommentQuery(language).parse(sample) == []


def test_opening_comment_query_extracts_contiguous_start_of_file_comment_block():
    sample = "/* header */\n// detail line\nint value = 1;\n"

    assert OpeningCommentQuery("java").parse(sample) == [
        _expected_query_match(sample, "/* header */\n// detail line")
    ]


def test_opening_comment_query_skips_hashbang_before_opening_comments():
    sample = "#!/usr/bin/env bash\n# header line 1\n# header line 2\n\necho hi\n"

    assert OpeningCommentQuery("shell").parse(sample) == [
        _expected_query_match(sample, "# header line 1\n# header line 2")
    ]


def test_opening_comment_query_respects_default_and_custom_row_limits():
    sample = "\n\n\n# delayed header\nprint('hello')\n"

    assert OpeningCommentQuery("python").parse(sample) == []
    assert OpeningCommentQuery("python", max_start_row=4).parse(sample) == [
        _expected_query_match(sample, "# delayed header")
    ]


def test_opening_comment_query_returns_no_match_when_code_precedes_comment():
    sample = "value = 1\n# not an opening header\nprint(value)\n"

    assert OpeningCommentQuery("python").contains(sample) is False
    assert OpeningCommentQuery("python").parse(sample) == []


def test_opening_comment_query_stops_when_non_comment_content_is_reached():
    sample = "# first header line\nvalue = 1\n# later comment\n"

    assert OpeningCommentQuery("python").parse(sample) == [
        _expected_query_match(sample, "# first header line")
    ]


def test_opening_comment_query_validates_row_limit():
    with pytest.raises(ValueError):
        OpeningCommentQuery("python", max_start_row=0)


def test_supported_aliases_share_the_same_registry_family():
    java_syntax = get_comment_syntax("java")

    assert get_comment_syntax("c") is java_syntax
    assert get_comment_syntax("typescript") is java_syntax


def test_java_properties_comments_only_match_at_line_start():
    query = CommentQuery("java_properties")

    assert query.parse("x=1!2") == []
    assert query.parse("x=1 # not comment?") == []
    assert query.parse("# top=1") == [_expected_query_match("# top=1", "# top=1")]
    assert query.parse("  ! top=1") == [
        _expected_query_match("  ! top=1", "  ! top=1")
    ]


def test_forth_parenthesized_comment_accepts_token_adjacent_closer():
    sample = "before ( a b c--d e) after"

    assert CommentQuery("forth").parse(sample) == [
        _expected_query_match(sample, "( a b c--d e)")
    ]


def test_lua_long_bracket_comment_handles_equal_sign_variants():
    sample = "x=1 --[=[ note ]=] y=2"

    assert CommentQuery("lua").parse(sample) == [
        _expected_query_match(sample, "--[=[ note ]=]")
    ]


def test_julia_block_comment_wins_over_line_comment_prefix():
    sample = "x = 1 #= note =# y = 2"

    assert CommentQuery("julia").parse(sample) == [
        _expected_query_match(sample, "#= note =#")
    ]


def test_julia_nested_block_comment_consumes_full_nested_region():
    sample = "code #= outer #= inner =# after =# tail"

    assert CommentQuery("julia").parse(sample) == [
        _expected_query_match(sample, "#= outer #= inner =# after =#")
    ]


def test_perl_pod_block_requires_line_start():
    sample = "x = 1 # note\n=cut\n"

    assert CommentQuery("perl").parse(sample) == [
        _expected_query_match(sample, "# note")
    ]


def test_perl_pod_block_does_not_start_midline():
    sample = "code =pod\ninner\n=cut\n"

    assert CommentQuery("perl").parse(sample) == []


def test_raku_embedded_comment_uses_backtick_syntax():
    sample = (
        'if #`( why would I ever write an inline comment here? ) True { say "something stupid"; }'
    )

    assert CommentQuery("raku").parse(sample) == [
        _expected_query_match(sample, "#`( why would I ever write an inline comment here? )")
    ]


def test_rdoc_block_comment_requires_line_start():
    sample = "code = 1\n=begin\nline\n=end\nmore"

    assert CommentQuery("rdoc").parse(sample) == [
        _expected_query_match(sample, "=begin\nline\n=end")
    ]


@pytest.mark.parametrize("language", ["ruby", "rdoc"])
def test_begin_end_block_comments_do_not_start_midline(language):
    sample = "code =begin\nline\n=end\n"

    assert CommentQuery(language).parse(sample) == []


def test_webassembly_nested_block_comment_consumes_full_nested_region():
    sample = "code (; outer (; inner ;) after ;) tail"

    assert CommentQuery("webassembly").parse(sample) == [
        _expected_query_match(sample, "(; outer (; inner ;) after ;)")
    ]


@pytest.mark.parametrize(
    ("language", "sample", "expected_match"),
    [
        pytest.param("pascal", "before { note } after", "{ note }", id="pascal-brace-block"),
        pytest.param(
            "pascal",
            "before (* note *) after",
            "(* note *)",
            id="pascal-paren-star-block",
        ),
        pytest.param(
            "powerbuilder",
            "before /* outer /* inner */ outer */ after",
            "/* outer /* inner */ outer */",
            id="powerbuilder-nested-block",
        ),
        pytest.param("self", 'before "note" after', '"note"', id="self-double-quote-block"),
    ],
)
def test_comment_query_supports_new_version_aware_language_forms(language, sample, expected_match):
    assert CommentQuery(language).parse(sample) == [_expected_query_match(sample, expected_match)]


def test_promela_parser_warns_once_and_supports_only_native_comments():
    comment_query_module = importlib.import_module("ml4setk.Parsing.Comments.CommentQuery")
    comment_query_module._WARNED_LANGUAGE_CAVEATS.clear()

    with pytest.warns(
        UserWarning,
        match=r"Promela parsing only supports native /\* \.\.\. \*/ comments",
    ):
        query = CommentQuery("promela")

    sample = "active proctype main() { /* native note */ skip }"
    assert query.parse(sample) == [_expected_query_match(sample, "/* native note */")]
    assert query.contains("active proctype main() { // preprocessed note\nskip }") is False

    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        OpeningCommentQuery("promela")

    assert recorded == []


def test_unsupported_languages_raise_clear_errors():
    with pytest.raises(NotImplementedError):
        LineCommentQuery("brainfuck")

    with pytest.raises(NotImplementedError):
        NestedCommentQuery("brainfuck")
