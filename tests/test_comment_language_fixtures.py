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
