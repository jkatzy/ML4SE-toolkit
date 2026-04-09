from dataclasses import dataclass

import pytest

from ml4setk import CommentQuery, QueryMatch
from ml4setk.Parsing.Comments import SUPPORTED_LANGUAGES, iter_comment_syntaxes

pytestmark = pytest.mark.unit

INDENTATION_SCOPED_BLOCK_LANGUAGES = {"slim"}


@dataclass(frozen=True)
class GeneratedCommentCase:
    language: str
    sample: str
    expected_match: str
    case_id: str


def _expected_query_match(sample, expected_match):
    start = sample.index(expected_match)
    end = start + len(expected_match)
    return QueryMatch(sample[:start], sample[end:], expected_match)


def _iter_regex_examples_for_language(syntax, language):
    yield from syntax.shared_regex_examples
    if language == syntax.canonical_name:
        yield from syntax.canonical_regex_examples


def _find_regex_example(syntax, language, *, kind, predicate=None):
    for example in _iter_regex_examples_for_language(syntax, language):
        if example.kind != kind:
            continue
        if predicate is not None and not predicate(example):
            continue
        return example
    return None


def _build_single_line_cases():
    cases = []
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            example = _find_regex_example(
                syntax,
                language,
                kind="line",
                predicate=lambda example: example.grouped_line_compatible,
            )
            if example is None:
                continue
            sample = f"{example.expected_match}\nafter"
            cases.append(
                GeneratedCommentCase(
                    language=language,
                    sample=sample,
                    expected_match=example.expected_match,
                    case_id=f"{language}-generated-single-line",
                )
            )
    return cases


def _build_grouped_line_cases():
    cases = []
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            example = _find_regex_example(
                syntax,
                language,
                kind="line",
                predicate=lambda example: example.grouped_line_compatible,
            )
            if example is None:
                continue
            expected_match = f"{example.expected_match}\n{example.expected_match}"
            sample = f"{expected_match}\nafter"
            cases.append(
                GeneratedCommentCase(
                    language=language,
                    sample=sample,
                    expected_match=expected_match,
                    case_id=f"{language}-generated-line-block",
                )
            )
    return cases


def _build_block_cases():
    cases = []
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            example = _find_regex_example(syntax, language, kind="block")
            if example is not None:
                sample = f"{example.expected_match}\nafter"
                cases.append(
                    GeneratedCommentCase(
                        language=language,
                        sample=sample,
                        expected_match=example.expected_match,
                        case_id=f"{language}-generated-block",
                    )
                )
                continue

            if not syntax.nested_delimiters:
                continue

            open_delim, close_delim = syntax.nested_delimiters[0]
            expected_match = f"{open_delim} block note {close_delim}"
            sample = f"{expected_match}\nafter"
            cases.append(
                GeneratedCommentCase(
                    language=language,
                    sample=sample,
                    expected_match=expected_match,
                    case_id=f"{language}-generated-block",
                )
            )
    return cases


def _build_inline_cases():
    cases = []
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            line_example = _find_regex_example(
                syntax,
                language,
                kind="line",
                predicate=lambda example: example.inline_compatible,
            )
            if line_example is not None:
                sample = f"value = 1 {line_example.expected_match}\nreturn value"
                cases.append(
                    GeneratedCommentCase(
                        language=language,
                        sample=sample,
                        expected_match=line_example.expected_match,
                        case_id=f"{language}-generated-inline",
                    )
                )
                continue

            block_example = _find_regex_example(
                syntax,
                language,
                kind="block",
                predicate=lambda example: example.inline_compatible,
            )
            if block_example is not None:
                sample = f"value = 1 {block_example.expected_match} return value"
                cases.append(
                    GeneratedCommentCase(
                        language=language,
                        sample=sample,
                        expected_match=block_example.expected_match,
                        case_id=f"{language}-generated-inline",
                    )
                )
                continue

            if not syntax.nested_delimiters:
                continue

            open_delim, close_delim = syntax.nested_delimiters[0]
            expected_match = f"{open_delim} inline note {close_delim}"
            sample = f"value = 1 {expected_match} return value"
            cases.append(
                GeneratedCommentCase(
                    language=language,
                    sample=sample,
                    expected_match=expected_match,
                    case_id=f"{language}-generated-inline",
                )
            )
    return cases


def _build_nested_cases():
    cases = []
    for syntax in iter_comment_syntaxes():
        if not syntax.nested_delimiters:
            continue
        open_delim, close_delim = syntax.nested_delimiters[0]
        expected_match = (
            f"{open_delim} outer {open_delim} inner {close_delim} outer {close_delim}"
        )
        sample = f"before {expected_match} after"
        for language in syntax.language_names:
            cases.append(
                GeneratedCommentCase(
                    language=language,
                    sample=sample,
                    expected_match=expected_match,
                    case_id=f"{language}-generated-nested",
                )
            )
    return cases


def _build_block_with_inner_line_cases():
    cases = []
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            if language in INDENTATION_SCOPED_BLOCK_LANGUAGES:
                continue
            line_example = _find_regex_example(syntax, language, kind="line")
            block_example = _find_regex_example(syntax, language, kind="block")
            if line_example is None or block_example is None:
                continue

            expected_match = _build_block_with_inner_line_comment(
                block_example.expected_match,
                line_example.expected_match,
            )
            if block_example.inline_compatible:
                sample = f"before {expected_match} after"
            else:
                sample = f"before\n{expected_match}\nafter"
            cases.append(
                GeneratedCommentCase(
                    language=language,
                    sample=sample,
                    expected_match=expected_match,
                    case_id=f"{language}-generated-block-contains-line",
                )
            )
    return cases


def _build_outer_block_wins_cases():
    cases = []
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            if language in INDENTATION_SCOPED_BLOCK_LANGUAGES:
                continue
            line_example = _find_regex_example(
                syntax,
                language,
                kind="line",
            )
            if line_example is None:
                continue

            block_example = _find_regex_example(syntax, language, kind="block")
            if block_example is not None:
                expected_match = _build_block_with_inner_line_comment(
                    block_example.expected_match,
                    line_example.expected_match,
                )
                sample = (
                    f"before {expected_match} after"
                    if block_example.inline_compatible
                    else f"before\n{expected_match}\nafter"
                )
            elif syntax.nested_delimiters:
                open_delim, close_delim = syntax.nested_delimiters[0]
                expected_match = (
                    f"{open_delim}\nouter\n{line_example.expected_match}\ninner\n{close_delim}"
                )
                sample = f"before {expected_match} after"
            else:
                continue

            cases.append(
                GeneratedCommentCase(
                    language=language,
                    sample=sample,
                    expected_match=expected_match,
                    case_id=f"{language}-generated-outer-block-wins",
                )
            )
    return cases


def _build_block_with_inner_line_comment(block_match, line_match):
    replacement = f"outer\n{line_match}\ninner"
    for marker in ("block note", "note"):
        if marker in block_match:
            return block_match.replace(marker, replacement, 1)

    raise ValueError(f"Cannot synthesize block overlap case from {block_match!r}")


SINGLE_LINE_CASES = _build_single_line_cases()
GROUPED_LINE_CASES = _build_grouped_line_cases()
BLOCK_CASES = _build_block_cases()
INLINE_CASES = _build_inline_cases()
NESTED_CASES = _build_nested_cases()
BLOCK_WITH_INNER_LINE_CASES = _build_block_with_inner_line_cases()
OUTER_BLOCK_WINS_CASES = _build_outer_block_wins_cases()


def _case_languages(cases):
    return {case.language for case in cases}


@pytest.mark.parametrize("case", SINGLE_LINE_CASES, ids=lambda case: case.case_id)
def test_generated_single_line_cases(case):
    query = CommentQuery(case.language)

    assert query.contains(case.sample) is True
    assert query.parse(case.sample) == [_expected_query_match(case.sample, case.expected_match)]


@pytest.mark.parametrize("case", GROUPED_LINE_CASES, ids=lambda case: case.case_id)
def test_generated_grouped_line_block_cases(case):
    query = CommentQuery(case.language)

    assert query.contains(case.sample) is True
    assert query.parse(case.sample) == [_expected_query_match(case.sample, case.expected_match)]


@pytest.mark.parametrize("case", BLOCK_CASES, ids=lambda case: case.case_id)
def test_generated_block_cases(case):
    query = CommentQuery(case.language)

    assert query.contains(case.sample) is True
    assert query.parse(case.sample) == [_expected_query_match(case.sample, case.expected_match)]


@pytest.mark.parametrize("case", INLINE_CASES, ids=lambda case: case.case_id)
def test_generated_inline_cases(case):
    query = CommentQuery(case.language)

    assert query.contains(case.sample) is True
    assert query.parse(case.sample) == [_expected_query_match(case.sample, case.expected_match)]


@pytest.mark.parametrize("case", NESTED_CASES, ids=lambda case: case.case_id)
def test_generated_nested_cases(case):
    query = CommentQuery(case.language)

    assert query.contains(case.sample) is True
    assert query.parse(case.sample) == [_expected_query_match(case.sample, case.expected_match)]


@pytest.mark.parametrize("case", BLOCK_WITH_INNER_LINE_CASES, ids=lambda case: case.case_id)
def test_generated_block_cases_treat_inner_line_markers_as_part_of_the_outer_block(case):
    query = CommentQuery(case.language)

    assert query.contains(case.sample) is True
    assert query.parse(case.sample) == [_expected_query_match(case.sample, case.expected_match)]


@pytest.mark.parametrize("case", OUTER_BLOCK_WINS_CASES, ids=lambda case: case.case_id)
def test_generated_outer_block_wins_over_inner_line_comment_cases(case):
    query = CommentQuery(case.language)

    assert query.contains(case.sample) is True
    assert query.parse(case.sample) == [_expected_query_match(case.sample, case.expected_match)]


def test_generated_cases_cover_every_supported_language():
    covered = (
        _case_languages(SINGLE_LINE_CASES)
        | _case_languages(BLOCK_CASES)
        | _case_languages(INLINE_CASES)
        | _case_languages(NESTED_CASES)
    )

    assert covered == set(SUPPORTED_LANGUAGES)


def test_generated_grouped_line_cases_cover_all_supported_line_languages():
    expected = set()
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            example = _find_regex_example(
                syntax,
                language,
                kind="line",
                predicate=lambda example: example.grouped_line_compatible,
            )
            if example is not None:
                expected.add(language)

    assert _case_languages(GROUPED_LINE_CASES) == expected


def test_generated_block_cases_cover_all_supported_block_languages():
    expected = set()
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            if _find_regex_example(syntax, language, kind="block") is not None:
                expected.add(language)
                continue
            if syntax.nested_delimiters:
                expected.add(language)

    assert _case_languages(BLOCK_CASES) == expected


def test_generated_inline_cases_cover_all_inline_capable_languages():
    expected = set()
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            line_example = _find_regex_example(
                syntax,
                language,
                kind="line",
                predicate=lambda example: example.inline_compatible,
            )
            block_example = _find_regex_example(
                syntax,
                language,
                kind="block",
                predicate=lambda example: example.inline_compatible,
            )
            if line_example is not None or block_example is not None or syntax.nested_delimiters:
                expected.add(language)

    assert _case_languages(INLINE_CASES) == expected


def test_generated_nested_cases_cover_all_nested_comment_languages():
    expected = {
        language
        for syntax in iter_comment_syntaxes()
        if syntax.nested_delimiters
        for language in syntax.language_names
    }

    assert _case_languages(NESTED_CASES) == expected


def test_generated_block_with_inner_line_cases_cover_all_block_and_line_languages():
    expected = set()
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            if language in INDENTATION_SCOPED_BLOCK_LANGUAGES:
                continue
            line_example = _find_regex_example(syntax, language, kind="line")
            block_example = _find_regex_example(syntax, language, kind="block")
            if line_example is not None and block_example is not None:
                expected.add(language)

    assert _case_languages(BLOCK_WITH_INNER_LINE_CASES) == expected


def test_generated_outer_block_wins_cases_cover_all_block_and_line_languages():
    expected = set()
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            if language in INDENTATION_SCOPED_BLOCK_LANGUAGES:
                continue
            line_example = _find_regex_example(syntax, language, kind="line")
            block_example = _find_regex_example(syntax, language, kind="block")
            if line_example is None:
                continue
            if block_example is not None or syntax.nested_delimiters:
                expected.add(language)

    assert _case_languages(OUTER_BLOCK_WINS_CASES) == expected
