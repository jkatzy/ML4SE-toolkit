import importlib.util
import sys
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from pathlib import Path

import pytest

from ml4setk import CommentQuery, QueryMatch
from ml4setk.Parsing.Comments import SUPPORTED_LANGUAGES

pytestmark = [
    pytest.mark.unit,
    pytest.mark.filterwarnings("ignore:Promela parsing only supports native"),
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_BUILDER_PATH = PROJECT_ROOT / "scripts" / "build_comment_language_fixtures.py"


def _load_fixture_builder():
    spec = importlib.util.spec_from_file_location(
        "comment_language_fixture_builder", FIXTURE_BUILDER_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load fixture builder from {FIXTURE_BUILDER_PATH}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


FIXTURE_BUILDER = _load_fixture_builder()
FIXTURE_DIR = PROJECT_ROOT / FIXTURE_BUILDER.FIXTURE_DIR
LANGUAGE_FIXTURES = FIXTURE_BUILDER.build_language_fixtures()


def _expected_query_match(sample, expected_match):
    start = sample.index(expected_match)
    end = start + len(expected_match)
    return QueryMatch(sample[:start], sample[end:], expected_match)


def _fixture_comment_detection_result(fixture):
    content = (FIXTURE_DIR / fixture.filename).read_text(encoding="utf-8")
    matches = CommentQuery(fixture.language).parse(content)
    return fixture.language, len(matches)


def _parallel_fixture_results(fixtures):
    workers = min(len(fixtures), cpu_count() or 1)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_fixture_comment_detection_result, fixtures))


def test_comment_language_fixture_folder_has_one_file_per_language():
    assert FIXTURE_DIR.is_dir()

    expected_filenames = {fixture.filename for fixture in LANGUAGE_FIXTURES}
    actual_filenames = {
        path.name
        for path in FIXTURE_DIR.iterdir()
        if path.is_file() and path.name.endswith(FIXTURE_BUILDER.FIXTURE_SUFFIX)
    }

    assert len(LANGUAGE_FIXTURES) == len(SUPPORTED_LANGUAGES)
    assert {fixture.language for fixture in LANGUAGE_FIXTURES} == set(SUPPORTED_LANGUAGES)
    assert actual_filenames == expected_filenames


@pytest.mark.parametrize(
    "language",
    ("circom", "ecmarkup", "hosts_file", "linear_programming", "pddl"),
)
def test_raw_syntaxes_do_not_receive_string_negative_probes(language):
    probes = [
        case
        for case in FIXTURE_BUILDER.build_fixture_cases(language)
        if (case.forbidden_sentinel or "").startswith("string_probe_")
    ]

    assert probes == []


def test_coq_string_probes_use_only_its_documented_double_quote_form():
    probes = [
        case
        for case in FIXTURE_BUILDER.build_fixture_cases("coq")
        if (case.forbidden_sentinel or "").startswith("string_probe_")
    ]

    assert probes
    assert all(' = "not ' in case.content for case in probes)


def test_minizinc_eof_seed_is_unique_and_last():
    cases = FIXTURE_BUILDER.build_fixture_cases("minizinc")
    eof_cases = [case for case in cases if case.consumes_eof]

    assert len(eof_cases) == 1
    assert cases[-1] == eof_cases[0]
    assert cases[-1].expected_match == "/* accepted through EOF"
    content = FIXTURE_BUILDER.build_fixture_content("minizinc")
    assert content.endswith(cases[-1].expected_match)
    assert content.count(cases[-1].expected_match) == 1


def test_nested_dash_doc_synthesis_uses_the_registered_outer_closer():
    doc_cases = [
        case.expected_match
        for case in FIXTURE_BUILDER.build_fixture_cases("agda")
        if case.expected_match and "star_doc_" in case.expected_match
    ]

    assert doc_cases
    assert all(comment.startswith("{-\n") for comment in doc_cases)
    assert all(comment.endswith("\n-}") for comment in doc_cases)


def test_contextual_and_xmake_fixtures_keep_all_reviewed_seed_forms():
    slang_matches = FIXTURE_BUILDER.expected_matches_for_language("slang")
    xmake_matches = FIXTURE_BUILDER.expected_matches_for_language("xmake")

    assert len(slang_matches) == 3
    assert any(match.startswith("/*") for match in slang_matches)
    assert any("\\\ncontinued" in match for match in slang_matches)
    assert "--[=[ long fixture_2 ]=]" in xmake_matches


@pytest.mark.parametrize(
    "language",
    (
        "basic",
        "realbasic",
        "vba",
        "vb6",
        "vbscript",
        "visual_basic",
        "visual_basic_6_0",
        "visual_basic_net",
        "xojo",
    ),
)
def test_mixed_visual_basic_fixtures_keep_contextual_and_regex_seeds_once(language):
    expected_matches = FIXTURE_BUILDER.expected_matches_for_language(language)
    fixture_content = (FIXTURE_DIR / FIXTURE_BUILDER.language_fixture_filename(language)).read_text(
        encoding="utf-8"
    )
    required_seeds = (
        "Rem contextual_fixture_1",
        "Rem contextual_fixture_2",
        "' fixture_1",
    )

    for seed in required_seeds:
        assert expected_matches.count(seed) == 1
        assert fixture_content.count(seed) == 1

    assert fixture_content == FIXTURE_BUILDER.build_fixture_content(language)


@pytest.mark.parametrize("fixture", LANGUAGE_FIXTURES, ids=lambda fixture: fixture.language)
def test_comment_language_fixture_files_keep_expected_comments(fixture):
    content = (FIXTURE_DIR / fixture.filename).read_text(encoding="utf-8")

    for expected_match in fixture.expected_matches:
        assert content.count(expected_match) == 1

    for forbidden_sentinel in fixture.forbidden_sentinels:
        assert forbidden_sentinel in content


@pytest.mark.parametrize("fixture", LANGUAGE_FIXTURES, ids=lambda fixture: fixture.language)
def test_comment_language_fixture_files_parse_expected_comments(fixture):
    content = (FIXTURE_DIR / fixture.filename).read_text(encoding="utf-8")

    expected_matches = list(fixture.expected_matches)
    matches = CommentQuery(fixture.language).parse(content)
    parsed_matches = [match.match for match in matches]

    assert matches
    for expected_match in expected_matches:
        assert parsed_matches.count(expected_match) == 1
        assert _expected_query_match(content, expected_match) in matches

    for forbidden_sentinel in fixture.forbidden_sentinels:
        assert all(forbidden_sentinel not in match.match for match in matches)


def test_stack_v2_language_fixtures_detect_at_least_one_comment_for_every_language():
    results = _parallel_fixture_results(LANGUAGE_FIXTURES)

    missing_languages = [language for language, match_count in results if match_count == 0]

    assert not missing_languages, "No comments found for: " + ", ".join(missing_languages)
