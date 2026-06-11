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


def test_jest_snapshot_ignores_serialized_template_literal_content():
    sample = "exports[`x 1`] = `\n// rendered text, not metadata\n`;\n"

    assert CommentQuery("jest_snapshot").parse(sample) == []


@pytest.mark.parametrize(
    ("language", "sample", "expected_match"),
    [
        pytest.param(
            "literate_haskell",
            'This prose mentions -- not code.\n\n> main = putStrLn "ok"\n> -- code comment\n',
            "-- code comment",
            id="literate-haskell-bird-track",
        ),
        pytest.param(
            "literate_agda",
            "Prose mentions -- not Agda code.\n\n\\begin{code}\n-- code comment\n\\end{code}\n",
            "-- code comment",
            id="literate-agda-code-block",
        ),
        pytest.param(
            "literate_coffeescript",
            "Markdown heading # not CoffeeScript code\n\n    value = 1\n    # code comment\n",
            "# code comment",
            id="literate-coffeescript-indented-code",
        ),
    ],
)
def test_literate_language_comments_only_match_inside_code_regions(
    language, sample, expected_match
):
    assert CommentQuery(language).parse(sample) == [_expected_query_match(sample, expected_match)]


def test_literate_nested_scanner_ignores_unclosed_delimiter_inside_line_comment():
    sample = (
        "> -- line comment mentions {- but is still a line comment\n"
        "\\begin{code}\n"
        "{- real nested comment -}\n"
        "\\end{code}\n"
    )

    assert CommentQuery("literate_haskell").parse(sample) == [
        _expected_query_match(sample, "-- line comment mentions {- but is still a line comment"),
        _expected_query_match(sample, "{- real nested comment -}"),
    ]


def test_openedge_abl_slash_comment_requires_left_boundary():
    sample = "value//not\nvalue // yes\n// also yes\n"

    assert CommentQuery("openedge_abl").parse(sample) == [
        _expected_query_match(sample, "// yes"),
        _expected_query_match(sample, "// also yes"),
    ]


def test_webvtt_note_cue_text_is_not_comment():
    sample = (
        "WEBVTT\n\n"
        "00:00:00.000 --> 00:00:01.000\n"
        "NOTE spoken cue text, not a comment\n\n"
    )

    assert CommentQuery("webvtt").parse(sample) == []


def test_xbase_note_requires_keyword_boundary():
    sample = 'NOTEBOOK := "field"\n? NOTEBOOK\nNOTE real comment\n'

    assert CommentQuery("xbase").parse(sample) == [
        _expected_query_match(sample, "NOTE real comment")
    ]


def test_xbase_note_line_does_not_group_with_adjacent_block_comment():
    sample = (
        "NOTE breaker_xbase_note keeps NOTE: tag in body\n"
        "/* breaker_xbase_block contains && and NOTE tokens */\n"
        '? "after"\n'
    )

    assert CommentQuery("xbase").parse(sample) == [
        _expected_query_match(sample, "NOTE breaker_xbase_note keeps NOTE: tag in body"),
        _expected_query_match(sample, "/* breaker_xbase_block contains && and NOTE tokens */"),
    ]


def test_stack_v2_csharp_todo_line_comment_extracts_reported_span():
    sample = (
        "using System;\n"
        "using System.Collections;\n"
        "using System.Collections.Generic;\n"
        "using UnityEngine;\n"
        "\n"
        "//TODO this needs a lot of refractoring, a lot of duped code\n"
        "//TODO This belongs somewhere else I think maybe on the Object Base class\n"
        "public enum Interaction {\n"
    )
    expected_match = (
        "//TODO this needs a lot of refractoring, a lot of duped code\n"
        "//TODO This belongs somewhere else I think maybe on the Object Base class"
    )

    matches = CommentQuery("c#").parse(sample)

    assert matches == [_expected_query_match(sample, expected_match)]
    assert len(matches[0].prefix) == 94
    assert len(matches[0].prefix) + len(matches[0].match) == 228
    assert matches[0].prefix.count("\n") + 1 == 6
    assert len(matches[0].prefix) - matches[0].prefix.rfind("\n") == 1


def test_stack_v2_csharp_inline_russian_todo_line_comment_extracts_reported_span():
    raw_comment = "//todo pn возможна исключительная ситуация"
    sample = (
        "\ufeff/*Написать программу, которая определяет площадь прямоугольника \n"
        "со сторонами a и b.Если пользователь вводит некорректные значения \n"
        "(отрицательные, или 0), должно выдаваться сообщение об ошибке.\n"
        "Возможность ввода пользователем строки вида «абвгд», или нецелых \n"
        "чисел игнорировать.*/\n"
        "\n"
        "namespace Task01\n"
        "{\n"
        "    using System;\n"
        "\n"
        "    internal class Program\n"
        "    {\n"
        "        private static void Main(string[] args)\n"
        "        {\n"
        '            Console.Write("Enter a : ");\n'
        "            double a = double.Parse(Console.ReadLine());"
        "//todo pn возможна исключительная ситуация\n"
        "\t\t\twhile (a <= 0)\n"
        "            {\n"
        '                Console.WriteLine("Error! Try again: ");\n'
        "                a = double.Parse(Console.ReadLine());"
        "//todo pn возможна исключительная ситуация\n"
        "\t\t\t}\n"
        "\n"
        '            Console.Write("Enter b: ");\n'
        "            double b = double.Parse(Console.ReadLine());"
        "//todo pn возможна исключительная ситуация\n"
        "\t\t\twhile (b <= 0)\n"
        "            {\n"
        '                Console.WriteLine("Error! Try again: ");\n'
        "                b = double.Parse(Console.ReadLine());"
        "//todo pn возможна исключительная ситуация\n"
        "\t\t\t}\n"
        "\n"
        "            AreaOfRectangle area = new AreaOfRectangle();\n"
        "            area.FindAreaOfRectangle(a, b);\n"
        "        }\n"
        "    }\n"
        "}\n"
    )
    expected_target = _expected_query_match(sample, raw_comment)

    matches = CommentQuery("c#").parse(sample)

    assert expected_target in matches
    assert len(expected_target.prefix) == 511
    assert len(expected_target.prefix) + len(expected_target.match) == 553
    assert expected_target.prefix.count("\n") + 1 == 16
    assert len(expected_target.prefix) - expected_target.prefix.rfind("\n") == 57


def test_stack_v2_csharp_xml_doc_line_comment_extracts_reported_span():
    raw_comment = (
        "/// <summary>\n"
        "    /// Base class for implementing custom movement for the Retro Controller\n"
        "    /// </summary>"
    )
    sample = (
        "\ufeffusing UnityEngine;\n"
        "\n"
        "namespace vnc\n"
        "{\n"
        f"    {raw_comment}\n"
        "    public abstract class RetroMovement : MonoBehaviour\n"
        "    {\n"
        "    }\n"
        "}\n"
    )

    matches = CommentQuery("c#").parse(sample)

    assert matches == [_expected_query_match(sample, raw_comment)]
    assert len(matches[0].prefix) == 41
    assert len(matches[0].prefix) + len(matches[0].match) == 150
    assert matches[0].prefix.count("\n") + 1 == 5
    assert len(matches[0].prefix) - matches[0].prefix.rfind("\n") == 5


def test_stack_v2_csharp_chinese_xml_doc_line_comment_extracts_reported_span():
    raw_comment = (
        "/// <summary>\n"
        "    /// 单点采集器GPRS通讯对象\n"
        "    /// </summary>"
    )
    sample = (
        "\ufeffusing JYGCloud.JOBMonitor.Common;\n"
        "using JYGCloud.JOBMonitor.ICommunicate;\n"
        "using System;\n"
        "using System.Collections.Generic;\n"
        "using System.Linq;\n"
        "using System.Net;\n"
        "using System.Net.Sockets;\n"
        "using System.Runtime.CompilerServices;\n"
        "using System.Text;\n"
        "using System.Threading;\n"
        "using System.Threading.Tasks;\n"
        "\n"
        "namespace JYGCloud.JOBMonitor.Communicate\n"
        "{\n"
        f"    {raw_comment}\n"
        "    public sealed class SCMGPRSCommunicate : IBaseCommunicate<string>\n"
        "    {\n"
        "    }\n"
        "}\n"
    )

    matches = CommentQuery("c#").parse(sample)

    assert matches[0] == _expected_query_match(sample, raw_comment)
    assert len(matches[0].prefix) == 347
    assert len(matches[0].prefix) + len(matches[0].match) == 401
    assert matches[0].prefix.count("\n") + 1 == 15
    assert len(matches[0].prefix) - matches[0].prefix.rfind("\n") == 5


def test_stack_v2_cpp_doxygen_line_header_extracts_reported_span():
    raw_comment = (
        "/// @file    Noise.ino\n"
        "/// @brief   Demonstrates how to use noise generation on a 2D LED matrix\n"
        "/// @example Noise.ino"
    )
    sample = (
        raw_comment
        + "\n\n#include <FastLED.h>\n\n"
        + "//\n"
        + "// Mark's xy coordinate mapping code.  See the XYMatrix for more information on it.\n"
        + "//\n"
        + "\n"
        + "// Params for width and height\n"
        + "const uint8_t kMatrixWidth = 16;\n"
    )

    matches = CommentQuery("c++").parse(sample)

    assert matches[0] == _expected_query_match(sample, raw_comment)
    assert len(matches[0].prefix) == 0
    assert len(matches[0].prefix) + len(matches[0].match) == 118
    assert matches[0].prefix.count("\n") + 1 == 1
    assert len(matches[0].prefix) - matches[0].prefix.rfind("\n") == 1


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


def test_comment_query_parses_inline_block_comment_with_code_before_and_after():
    sample = "int value = 1 /* inline block */ + 2;"

    assert CommentQuery("java").parse(sample) == [
        _expected_query_match(sample, "/* inline block */")
    ]


def test_comment_query_parses_star_prefixed_javadoc_block_comment():
    sample = (
        "/**\n"
        " * Description of what the method does.\n"
        " *\n"
        " * @param input Description of parameter.\n"
        " * @return Description of return value.\n"
        " * @throws Exception Description of exception.\n"
        " */\n"
        "public String example(String input) { return input; }"
    )
    expected_match = (
        "/**\n"
        " * Description of what the method does.\n"
        " *\n"
        " * @param input Description of parameter.\n"
        " * @return Description of return value.\n"
        " * @throws Exception Description of exception.\n"
        " */"
    )

    assert CommentQuery("java").parse(sample) == [_expected_query_match(sample, expected_match)]


@pytest.mark.parametrize(
    ("language", "sample"),
    [
        pytest.param(
            "java",
            'String url = "https://example.test/path";\nint x = 1;',
            id="java-line-marker-in-string",
        ),
        pytest.param(
            "java",
            'String text = "not /* a block */";\nint x = 1;',
            id="java-block-marker-in-string",
        ),
        pytest.param(
            "python",
            'value = "# not a comment"\nprint(value)',
            id="python-hash-marker-in-string",
        ),
        pytest.param(
            "sql",
            "SELECT '-- not a comment';\nSELECT 1;",
            id="sql-dash-marker-in-string",
        ),
        pytest.param(
            "haskell",
            'value = "{- not a block -}"\nvalue',
            id="haskell-nested-marker-in-string",
        ),
    ],
)
def test_comment_query_ignores_comment_markers_inside_simple_strings(language, sample):
    assert CommentQuery(language).parse(sample) == []


def test_comment_query_parses_comment_after_string_literal():
    sample = 'String url = "https://example.test/path"; // actual comment\nint x = 1;'

    assert CommentQuery("java").parse(sample) == [
        _expected_query_match(sample, "// actual comment")
    ]


def test_comment_query_groups_triple_slash_doc_line_comments():
    sample = "/// first doc line\n/// second doc line\nint value = 1;"
    expected_match = "/// first doc line\n/// second doc line"

    assert CommentQuery("java").parse(sample) == [_expected_query_match(sample, expected_match)]


@pytest.mark.parametrize(
    ("language", "sample", "expected_match"),
    [
        pytest.param(
            "java",
            "//////// repeated opener\nint value = 1;",
            "//////// repeated opener",
            id="java-repeated-slash-opener",
        ),
        pytest.param(
            "java",
            "/// odd repeated opener\nint value = 1;",
            "/// odd repeated opener",
            id="java-odd-repeated-slash-opener",
        ),
        pytest.param(
            "python",
            "######## repeated opener\nvalue = 1",
            "######## repeated opener",
            id="python-repeated-hash-opener",
        ),
    ],
)
def test_comment_query_parses_repeated_line_comment_openers(
    language, sample, expected_match
):
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
