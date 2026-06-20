from dataclasses import dataclass

import pytest

import ml4setk
from ml4setk import (
    CommentQuery,
    CommentSanitizer,
    QueryMatch,
    sanitize_comment,
    sanitize_comment_text,
)
from ml4setk.Parsing.Comments import SUPPORTED_LANGUAGES, iter_comment_syntaxes

pytestmark = pytest.mark.unit

_EXAMPLE_BODY_PLACEHOLDERS = (
    "block note",
    "note",
    "Visible content",
    "+ 100",
    "Remember the bull.",
)


@dataclass(frozen=True)
class SanitizerCase:
    language: str
    sample: str
    expected_match: str
    expected_sanitized: str
    case_id: str


def _split_example_placeholder(example_text):
    for placeholder in _EXAMPLE_BODY_PLACEHOLDERS:
        if placeholder not in example_text:
            continue
        prefix, suffix = example_text.split(placeholder, 1)
        return prefix, suffix
    raise AssertionError(f"Unsupported example placeholder in {example_text!r}")


def _iter_regex_examples_for_language(syntax, language):
    yield from syntax.shared_regex_examples
    if language == syntax.canonical_name:
        yield from syntax.canonical_regex_examples


def _first_line_example(syntax, language):
    for example in _iter_regex_examples_for_language(syntax, language):
        if example.kind == "line":
            return example
    return None


def _first_block_example(syntax, language):
    for example in _iter_regex_examples_for_language(syntax, language):
        if example.kind == "block":
            return example
    return None


def _safe_preserved_symbol(text):
    for char in text:
        if char in "#$%&'*+,-./:;!?<=>@\\|":
            return char
    stripped = text.strip()
    return stripped or "symbol"


def _safe_block_preserved_symbol(text):
    stripped = text.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {'"', "'"}:
        return "*"
    return _safe_preserved_symbol(text)


def _build_line_cases():
    removal_cases = []
    preservation_cases = []

    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            example = _first_line_example(syntax, language)
            if example is None:
                continue

            prefix, suffix = _split_example_placeholder(example.expected_match)
            token = prefix.strip()

            removal_line_one = f"{prefix}adversarial *** ### $$$ %%%{suffix}"
            removal_line_two = f"{prefix}repeated ### *** $$$ %%%{suffix}"
            if example.grouped_line_compatible:
                removal_match = f"{removal_line_one}\n{removal_line_two}"
                removal_expected = "adversarial *** ### $$$ %%%\nrepeated ### *** $$$ %%%"
            else:
                removal_match = removal_line_one
                removal_expected = "adversarial *** ### $$$ %%%"
            removal_cases.append(
                SanitizerCase(
                    language=language,
                    sample=f"before\n{removal_match}\nafter",
                    expected_match=removal_match,
                    expected_sanitized=removal_expected,
                    case_id=f"{language}-line-removal",
                )
            )

            preserved_text = token or _safe_preserved_symbol(example.expected_match)
            keep_line_one = f"{prefix}keep {preserved_text} exactly and *** ### $$$ %%%{suffix}"
            keep_line_two = f"{prefix}second line keeps {preserved_text} again{suffix}"
            if example.grouped_line_compatible:
                keep_match = f"{keep_line_one}\n{keep_line_two}"
                keep_expected = (
                    f"keep {preserved_text} exactly and *** ### $$$ %%%\n"
                    f"second line keeps {preserved_text} again"
                )
            else:
                keep_match = keep_line_one
                keep_expected = f"keep {preserved_text} exactly and *** ### $$$ %%%"
            preservation_cases.append(
                SanitizerCase(
                    language=language,
                    sample=f"before\n{keep_match}\nafter",
                    expected_match=keep_match,
                    expected_sanitized=keep_expected,
                    case_id=f"{language}-line-preservation",
                )
            )

    return removal_cases, preservation_cases


def _build_block_case(language, example, body, case_id):
    prefix, suffix = _split_example_placeholder(example.expected_match)
    expected_match = f"{prefix}{body}{suffix}"
    return SanitizerCase(
        language=language,
        sample=f"before\n{expected_match}\nafter",
        expected_match=expected_match,
        expected_sanitized=body,
        case_id=case_id,
    )


def _build_nested_case(language, open_delim, close_delim, body, case_id):
    expected_match = f"{open_delim} {body} {close_delim}"
    return SanitizerCase(
        language=language,
        sample=f"before {expected_match} after",
        expected_match=expected_match,
        expected_sanitized=body,
        case_id=case_id,
    )


def _build_block_cases():
    removal_cases = []
    preservation_cases = []

    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            if _first_line_example(syntax, language) is not None:
                continue

            example = _first_block_example(syntax, language)
            if example is not None:
                preserved_symbol = _safe_block_preserved_symbol(example.expected_match)
                removal_cases.append(
                    _build_block_case(
                        language,
                        example,
                        "adversarial *** ### $$$ %%%",
                        f"{language}-block-removal",
                    )
                )
                preservation_cases.append(
                    _build_block_case(
                        language,
                        example,
                        f"keep {preserved_symbol} exactly and *** ### $$$ %%%",
                        f"{language}-block-preservation",
                    )
                )
                continue

            if not syntax.nested_delimiters:
                continue

            open_delim, close_delim = syntax.nested_delimiters[0]
            preserved_symbol = _safe_preserved_symbol(open_delim + close_delim)
            removal_cases.append(
                _build_nested_case(
                    language,
                    open_delim,
                    close_delim,
                    "adversarial *** ### $$$ %%%",
                    f"{language}-block-removal",
                )
            )
            preservation_cases.append(
                _build_nested_case(
                    language,
                    open_delim,
                    close_delim,
                    f"keep {preserved_symbol} exactly and *** ### $$$ %%%",
                    f"{language}-block-preservation",
                )
            )

    return removal_cases, preservation_cases


def _build_registry_sample_cases():
    cases = []
    generic_kinds = {"line", "block", "nested"}

    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            for index, example in enumerate(_iter_regex_examples_for_language(syntax, language)):
                if example.kind in generic_kinds:
                    continue
                cases.append(
                    SanitizerCase(
                        language=language,
                        sample=example.sample,
                        expected_match=example.expected_match,
                        expected_sanitized=example.expected_match,
                        case_id=f"{language}-registry-sample-{index}",
                    )
                )

    return cases


def _build_c_style_block_gutter_cases():
    removal_cases = []
    preservation_cases = []

    for syntax in iter_comment_syntaxes():
        wrapper = None
        if ("/*", "*/") in syntax.nested_delimiters:
            wrapper = ("/*", "*/")
        else:
            examples = list(syntax.shared_regex_examples) + list(
                syntax.canonical_regex_examples
            )
            for example in examples:
                if example.kind != "block":
                    continue
                if (
                    example.expected_match.startswith("/**")
                    and example.expected_match.endswith("*/")
                ):
                    wrapper = ("/**", "*/")
                    break
                if (
                    example.expected_match.startswith("/*")
                    and example.expected_match.endswith("*/")
                ):
                    wrapper = ("/*", "*/")
                    break

        if wrapper is None:
            continue

        open_delim, close_delim = wrapper
        for language in syntax.language_names:
            removal_match = (
                f"{open_delim}\n"
                " * adversarial *** ### $$$ %%%\n"
                " * repeated ### *** $$$ %%%\n"
                f" {close_delim}"
            )
            removal_cases.append(
                SanitizerCase(
                    language=language,
                    sample=f"before\n{removal_match}\nafter",
                    expected_match=removal_match,
                    expected_sanitized="adversarial *** ### $$$ %%%\nrepeated ### *** $$$ %%%",
                    case_id=f"{language}-c-block-gutter-removal",
                )
            )

            preservation_match = (
                f"{open_delim}\n"
                " * keep * exactly and *** ### $$$ %%%\n"
                " * second line keeps * again\n"
                f" {close_delim}"
            )
            preservation_cases.append(
                SanitizerCase(
                    language=language,
                    sample=f"before\n{preservation_match}\nafter",
                    expected_match=preservation_match,
                    expected_sanitized=(
                        "keep * exactly and *** ### $$$ %%%\n"
                        "second line keeps * again"
                    ),
                    case_id=f"{language}-c-block-gutter-preservation",
                )
            )

    return removal_cases, preservation_cases


LINE_REMOVAL_CASES, LINE_PRESERVATION_CASES = _build_line_cases()
BLOCK_REMOVAL_CASES, BLOCK_PRESERVATION_CASES = _build_block_cases()
REGISTRY_SAMPLE_CASES = _build_registry_sample_cases()
(
    C_BLOCK_GUTTER_REMOVAL_CASES,
    C_BLOCK_GUTTER_PRESERVATION_CASES,
) = _build_c_style_block_gutter_cases()

SANITIZER_REMOVAL_CASES = LINE_REMOVAL_CASES + BLOCK_REMOVAL_CASES
SANITIZER_PRESERVATION_CASES = LINE_PRESERVATION_CASES + BLOCK_PRESERVATION_CASES


def _expected_query_match(sample, expected_match):
    start = sample.index(expected_match)
    end = start + len(expected_match)
    return QueryMatch(sample[:start], sample[end:], expected_match)


def _case_languages(cases):
    return {case.language for case in cases}


@pytest.mark.parametrize("case", SANITIZER_REMOVAL_CASES, ids=lambda case: case.case_id)
def test_comment_sanitizer_removes_only_comment_scaffolding(case):
    match = CommentQuery(case.language).parse(case.sample)

    assert match == [_expected_query_match(case.sample, case.expected_match)]
    assert CommentSanitizer(case.language).sanitize(match[0]) == case.expected_sanitized
    assert sanitize_comment(case.language, case.expected_match) == case.expected_sanitized
    assert sanitize_comment_text(case.language, case.expected_match) == case.expected_sanitized


@pytest.mark.parametrize("case", SANITIZER_PRESERVATION_CASES, ids=lambda case: case.case_id)
def test_comment_sanitizer_preserves_meaningful_symbols(case):
    match = CommentQuery(case.language).parse(case.sample)

    assert match == [_expected_query_match(case.sample, case.expected_match)]
    assert CommentSanitizer(case.language).sanitize(match[0]) == case.expected_sanitized


@pytest.mark.parametrize("case", REGISTRY_SAMPLE_CASES, ids=lambda case: case.case_id)
def test_comment_sanitizer_preserves_custom_registry_samples(case):
    match = CommentQuery(case.language).parse(case.sample)

    assert match == [_expected_query_match(case.sample, case.expected_match)]
    assert CommentSanitizer(case.language).sanitize(match[0]) == case.expected_sanitized


@pytest.mark.parametrize(
    "case",
    C_BLOCK_GUTTER_REMOVAL_CASES,
    ids=lambda case: case.case_id,
)
def test_comment_sanitizer_removes_c_style_block_gutters(case):
    match = CommentQuery(case.language).parse(case.sample)

    assert match == [_expected_query_match(case.sample, case.expected_match)]
    assert CommentSanitizer(case.language).sanitize(match[0]) == case.expected_sanitized


@pytest.mark.parametrize(
    "case",
    C_BLOCK_GUTTER_PRESERVATION_CASES,
    ids=lambda case: case.case_id,
)
def test_comment_sanitizer_preserves_semantic_symbols_inside_c_style_blocks(case):
    match = CommentQuery(case.language).parse(case.sample)

    assert match == [_expected_query_match(case.sample, case.expected_match)]
    assert CommentSanitizer(case.language).sanitize(match[0]) == case.expected_sanitized


def test_sanitizer_generated_cases_cover_every_supported_language():
    covered = _case_languages(SANITIZER_REMOVAL_CASES) | _case_languages(
        SANITIZER_PRESERVATION_CASES
    ) | _case_languages(REGISTRY_SAMPLE_CASES)

    assert covered == set(SUPPORTED_LANGUAGES)


def test_c_style_block_gutter_cases_cover_every_language_with_slash_star_blocks():
    expected = set()
    for syntax in iter_comment_syntaxes():
        supports_c_block = ("/*", "*/") in syntax.nested_delimiters
        if not supports_c_block:
            supports_c_block = any(
                example.kind == "block"
                and example.expected_match.startswith("/*")
                and example.expected_match.endswith("*/")
                for example in (
                    list(syntax.shared_regex_examples) + list(syntax.canonical_regex_examples)
                )
            )
        if supports_c_block:
            expected.update(syntax.language_names)

    assert _case_languages(C_BLOCK_GUTTER_REMOVAL_CASES) == expected
    assert _case_languages(C_BLOCK_GUTTER_PRESERVATION_CASES) == expected


def test_comment_sanitizer_rejects_non_comment_input_types():
    with pytest.raises(TypeError):
        sanitize_comment_text("java", 123)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        sanitize_comment("java", 123)  # type: ignore[arg-type]


def test_root_package_exports_comment_sanitizer_helpers():
    assert ml4setk.CommentSanitizer is CommentSanitizer
    assert ml4setk.sanitize_comment is sanitize_comment
    assert ml4setk.sanitize_comment_text is sanitize_comment_text


def test_stack_v2_csharp_crlf_perlin_block_sanitizes_reference_text():
    raw_comment = (
        "/* Perlin noise class.  ( by Tom Nuydens (tom@delphi3d.net) )\r\n"
        "* Converted to C# by Mattias Fagerlund, Mattias.Fagerlund@cortego.se\r\n"
        "\r\n"
        "******************************************************************************\r\n"
        "\r\n"
        "I used the following references for my implementation:\r\n"
        " http://students.vassar.edu/mazucker/code/perlin-noise-math-faq.html\r\n"
        ' Darwin Peachey\'s chapter in "Texturing & Modeling: A Procedural Approach"\r\n'
        "Another good resource is\r\n"
        " http://freespace.virgin.net/hugo.elias/models/m_perlin.htm\r\n"
        "\r\n"
        "******************************************************************************\r\n"
        "\r\n"
        "This class generates 3D Perlin noise. The demo that comes with this is 2D, but\r\n"
        "uses the 3rd dimension to create animated noise. The noise does not tile,\r\n"
        "although it could be made to do so with a few small modifications to the\r\n"
        "algorithm.\r\n"
        "\r\n"
        "Perlin noise can be used as a starting point for all kinds of things,\r\n"
        "including terrain generation, cloud rendering, procedural textures, and more.\r\n"
        'Most of these techniques involve rendering multiple "octaves" of noise. This\r\n'
        "means you generate multiple noise values for every pixel (each with different\r\n"
        "X, Y and/or Z coordinates), and then sum them. There's an example of this in\r\n"
        "the accompanying demo.\r\n"
        "*/"
    )
    expected_cleaned = (
        " Perlin noise class.  ( by Tom Nuydens (tom@delphi3d.net) )\n"
        "* Converted to C# by Mattias Fagerlund, Mattias.Fagerlund@cortego.se\n"
        "\n"
        "******************************************************************************\n"
        "\n"
        "I used the following references for my implementation:\n"
        " http://students.vassar.edu/mazucker/code/perlin-noise-math-faq.html\n"
        ' Darwin Peachey\'s chapter in "Texturing & Modeling: A Procedural Approach"\n'
        "Another good resource is\n"
        " http://freespace.virgin.net/hugo.elias/models/m_perlin.htm\n"
        "\n"
        "******************************************************************************\n"
        "\n"
        "This class generates 3D Perlin noise. The demo that comes with this is 2D, but\n"
        "uses the 3rd dimension to create animated noise. The noise does not tile,\n"
        "although it could be made to do so with a few small modifications to the\n"
        "algorithm.\n"
        "\n"
        "Perlin noise can be used as a starting point for all kinds of things,\n"
        "including terrain generation, cloud rendering, procedural textures, and more.\n"
        'Most of these techniques involve rendering multiple "octaves" of noise. This\n'
        "means you generate multiple noise values for every pixel (each with different\n"
        "X, Y and/or Z coordinates), and then sum them. There's an example of this in\n"
        "the accompanying demo."
    )
    target = QueryMatch("", "", raw_comment)

    assert CommentSanitizer("c#").sanitize(target) == expected_cleaned
    assert sanitize_comment("c#", raw_comment) == expected_cleaned


def test_stack_v2_csharp_todo_line_comment_sanitizes_no_space_delimiters():
    raw_comment = (
        "//TODO this needs a lot of refractoring, a lot of duped code\n"
        "//TODO This belongs somewhere else I think maybe on the Object Base class"
    )
    expected_cleaned = (
        "TODO this needs a lot of refractoring, a lot of duped code\n"
        "TODO This belongs somewhere else I think maybe on the Object Base class"
    )
    target = QueryMatch("", "", raw_comment)

    assert CommentSanitizer("c#").sanitize(target) == expected_cleaned
    assert sanitize_comment("c#", raw_comment) == expected_cleaned


def test_stack_v2_csharp_inline_russian_todo_line_comment_sanitizes_delimiter():
    raw_comment = "//todo pn возможна исключительная ситуация"
    expected_cleaned = "todo pn возможна исключительная ситуация"
    target = QueryMatch("", "", raw_comment)

    assert CommentSanitizer("c#").sanitize(target) == expected_cleaned
    assert sanitize_comment("c#", raw_comment) == expected_cleaned


def test_stack_v2_csharp_xml_doc_line_comment_sanitizes_delimiters():
    raw_comment = (
        "/// <summary>\n"
        "    /// Base class for implementing custom movement for the Retro Controller\n"
        "    /// </summary>"
    )
    expected_cleaned = (
        "<summary>\n"
        "Base class for implementing custom movement for the Retro Controller\n"
        "</summary>"
    )
    target = QueryMatch("", "", raw_comment)

    assert CommentSanitizer("c#").sanitize(target) == expected_cleaned
    assert sanitize_comment("c#", raw_comment) == expected_cleaned


def test_stack_v2_csharp_chinese_xml_doc_line_comment_sanitizes_delimiters():
    raw_comment = (
        "/// <summary>\n"
        "    /// 单点采集器GPRS通讯对象\n"
        "    /// </summary>"
    )
    expected_cleaned = (
        "<summary>\n"
        "单点采集器GPRS通讯对象\n"
        "</summary>"
    )
    target = QueryMatch("", "", raw_comment)

    assert CommentSanitizer("c#").sanitize(target) == expected_cleaned
    assert sanitize_comment("c#", raw_comment) == expected_cleaned


def test_stack_v2_cpp_doxygen_line_header_sanitizes_delimiters():
    raw_comment = (
        "/// @file    Noise.ino\n"
        "/// @brief   Demonstrates how to use noise generation on a 2D LED matrix\n"
        "/// @example Noise.ino"
    )
    expected_cleaned = (
        "@file    Noise.ino\n"
        "@brief   Demonstrates how to use noise generation on a 2D LED matrix\n"
        "@example Noise.ino"
    )
    target = QueryMatch("", "", raw_comment)

    assert CommentSanitizer("c++").sanitize(target) == expected_cleaned
    assert sanitize_comment("c++", raw_comment) == expected_cleaned


def test_stack_v2_cpp_qpid_decoder_doxygen_line_comment_sanitizes_delimiters():
    raw_comment = (
        "/// **Experimental** - Stream-like decoder from AMQP bytes to C++\n"
        "/// values.\n"
        "///\n"
        "/// For internal use only.\n"
        "///\n"
        "/// @see @ref types_page for the recommended ways to manage AMQP data"
    )
    expected_cleaned = (
        "**Experimental** - Stream-like decoder from AMQP bytes to C++\n"
        "values.\n"
        "\n"
        "For internal use only.\n"
        "\n"
        "@see @ref types_page for the recommended ways to manage AMQP data"
    )
    target = QueryMatch("", "", raw_comment)

    assert CommentSanitizer("c++").sanitize(target) == expected_cleaned
    assert sanitize_comment("c++", raw_comment) == expected_cleaned
