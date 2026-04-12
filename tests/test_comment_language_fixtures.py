import importlib.util
import sys
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


def test_comment_language_fixture_folder_has_one_file_per_language():
    assert FIXTURE_DIR.is_dir()

    expected_filenames = {fixture.filename for fixture in LANGUAGE_FIXTURES}
    actual_filenames = {path.name for path in FIXTURE_DIR.iterdir() if path.is_file()}

    assert len(LANGUAGE_FIXTURES) == len(SUPPORTED_LANGUAGES)
    assert {fixture.language for fixture in LANGUAGE_FIXTURES} == set(SUPPORTED_LANGUAGES)
    assert actual_filenames == expected_filenames


@pytest.mark.parametrize("fixture", LANGUAGE_FIXTURES, ids=lambda fixture: fixture.language)
def test_comment_language_fixture_files_match_registry(fixture):
    content = (FIXTURE_DIR / fixture.filename).read_text(encoding="utf-8")

    assert content == fixture.content
    for expected_match in fixture.expected_matches:
        assert content.count(expected_match) == 1


@pytest.mark.parametrize("fixture", LANGUAGE_FIXTURES, ids=lambda fixture: fixture.language)
def test_comment_language_fixture_files_parse_to_expected_comments(fixture):
    content = (FIXTURE_DIR / fixture.filename).read_text(encoding="utf-8")

    expected_matches = list(fixture.expected_matches)
    matches = CommentQuery(fixture.language).parse(content)

    assert [match.match for match in matches] == expected_matches
    assert matches == [_expected_query_match(content, match) for match in expected_matches]
