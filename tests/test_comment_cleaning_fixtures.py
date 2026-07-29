import importlib.util
import json
import sys
from pathlib import Path

import pytest

from ml4setk import (
    CommentSanitizer,
    QueryMatch,
    sanitize_comment,
    sanitize_comment_text,
)
from ml4setk.Parsing.Comments import (
    SUPPORTED_LANGUAGES,
    get_comment_syntax,
    iter_comment_syntaxes,
)

pytestmark = pytest.mark.unit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_BUILDER_PATH = PROJECT_ROOT / "scripts" / "build_comment_cleaning_fixtures.py"


def _load_fixture_builder():
    spec = importlib.util.spec_from_file_location(
        "comment_cleaning_fixture_builder",
        FIXTURE_BUILDER_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load fixture builder from {FIXTURE_BUILDER_PATH}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


FIXTURE_BUILDER = _load_fixture_builder()
FIXTURE_DIR = PROJECT_ROOT / FIXTURE_BUILDER.FIXTURE_DIR
CLEANING_FIXTURES = FIXTURE_BUILDER.build_cleaning_fixtures()
CLEANING_CASES = tuple(
    (fixture, language, case)
    for fixture in CLEANING_FIXTURES
    for language in fixture.language_keys
    for case in fixture.cases
)


def _case_sources(fixture, prefix):
    return [case.source for case in fixture.cases if case.source.startswith(prefix)]


def test_comment_cleaning_fixture_folder_has_exact_family_file_set():
    syntaxes = tuple(iter_comment_syntaxes())
    expected_filenames = {fixture.filename for fixture in CLEANING_FIXTURES}
    actual_filenames = {
        path.name
        for path in FIXTURE_DIR.iterdir()
        if path.is_file() and path.suffix == FIXTURE_BUILDER.FIXTURE_SUFFIX
    }

    assert len(CLEANING_FIXTURES) == len(syntaxes)
    assert {fixture.family_name for fixture in CLEANING_FIXTURES} == {
        syntax.family_name for syntax in syntaxes
    }
    assert actual_filenames == expected_filenames


@pytest.mark.parametrize(
    "fixture",
    CLEANING_FIXTURES,
    ids=lambda fixture: fixture.family_name,
)
def test_comment_cleaning_fixture_file_has_exact_generated_content(fixture):
    fixture_path = FIXTURE_DIR / fixture.filename
    content = fixture_path.read_text(encoding="utf-8")

    assert content == FIXTURE_BUILDER.render_cleaning_fixture(fixture)
    assert json.loads(content) == fixture.as_dict()


def test_comment_cleaning_fixtures_cover_every_supported_key_once():
    fixture_languages = [
        language for fixture in CLEANING_FIXTURES for language in fixture.language_keys
    ]

    assert len(fixture_languages) == len(set(fixture_languages))
    assert set(fixture_languages) == set(SUPPORTED_LANGUAGES)


@pytest.mark.parametrize(
    "fixture",
    CLEANING_FIXTURES,
    ids=lambda fixture: fixture.family_name,
)
def test_comment_cleaning_fixture_metadata_matches_registry(fixture):
    syntax = get_comment_syntax(fixture.canonical_language)

    assert fixture.family_name == syntax.family_name
    assert fixture.canonical_language == syntax.canonical_name
    assert fixture.language_keys == syntax.language_names
    assert fixture.sanitizer_mode == syntax.sanitizer_mode
    assert all(get_comment_syntax(language) is syntax for language in fixture.language_keys)


@pytest.mark.parametrize(
    "fixture",
    CLEANING_FIXTURES,
    ids=lambda fixture: fixture.family_name,
)
def test_comment_cleaning_fixture_covers_every_registry_form(fixture):
    syntax = get_comment_syntax(fixture.canonical_language)

    for attribute_name in (
        "shared_regex_examples",
        "canonical_regex_examples",
        "shared_contextual_examples",
        "canonical_contextual_examples",
    ):
        examples = getattr(syntax, attribute_name)
        source_cases = {
            case.source: case
            for case in fixture.cases
            if case.source.startswith(f"registry:{attribute_name}[")
        }
        expected_sources = {f"registry:{attribute_name}[{index}]" for index in range(len(examples))}
        assert set(source_cases) == expected_sources
        for index, example in enumerate(examples):
            case = source_cases[f"registry:{attribute_name}[{index}]"]
            placeholder = FIXTURE_BUILDER._split_payload_placeholder(example.expected_match)
            assert (case.payload_marker is not None) == (placeholder is not None)

    nested_cases = {
        case.source: case
        for case in fixture.cases
        if case.source.startswith("registry:nested_delimiters[")
    }
    assert len(nested_cases) == len(syntax.nested_delimiters)
    for index, (open_delimiter, close_delimiter) in enumerate(syntax.nested_delimiters):
        case = nested_cases[f"registry:nested_delimiters[{index}]"]
        assert case.raw_comment.startswith(open_delimiter)
        assert case.raw_comment.endswith(close_delimiter)
        assert f"{open_delimiter} {case.payload_marker}_inner {close_delimiter}" in case.raw_comment
        assert open_delimiter in case.expected_cleaned
        assert close_delimiter in case.expected_cleaned

    for wrapper_kind, wrappers in (
        ("line", syntax.sanitizer_line_wrappers),
        ("block", syntax.sanitizer_block_wrappers),
    ):
        wrapper_cases = {
            case.source: case
            for case in fixture.cases
            if case.source.startswith(f"registry:sanitizer_{wrapper_kind}_wrappers[")
        }
        assert len(wrapper_cases) == len(wrappers)
        for index, (open_delimiter, close_delimiter) in enumerate(wrappers):
            case = wrapper_cases[f"registry:sanitizer_{wrapper_kind}_wrappers[{index}]"]
            assert case.raw_comment.startswith(open_delimiter)
            assert case.raw_comment.endswith(close_delimiter)
            assert case.expected_cleaned == case.payload_marker

    assert len(_case_sources(fixture, "registry:unclosed_block_openers[")) == len(
        syntax.unclosed_block_openers
    )

    expected_grouped_sources = set()
    for attribute_name in (
        "shared_regex_examples",
        "canonical_regex_examples",
    ):
        for index, example in enumerate(getattr(syntax, attribute_name)):
            if (
                example.kind == "line"
                and example.grouped_line_compatible
                and FIXTURE_BUILDER._split_payload_placeholder(example.expected_match) is not None
            ):
                expected_grouped_sources.add(f"generated-group:registry:{attribute_name}[{index}]")
    assert set(_case_sources(fixture, "generated-group:")) == (expected_grouped_sources)

    raw_mode_sources = _case_sources(fixture, "generated:sanitizer_mode=raw")
    assert len(raw_mode_sources) == (1 if syntax.sanitizer_mode == "raw" else 0)


@pytest.mark.parametrize(
    "fixture",
    CLEANING_FIXTURES,
    ids=lambda fixture: fixture.family_name,
)
def test_comment_cleaning_fixture_case_ids_and_payload_markers_are_stable(fixture):
    case_ids = [case.case_id for case in fixture.cases]

    assert len(case_ids) == len(set(case_ids))
    for case in fixture.cases:
        assert "\r" not in case.expected_cleaned
        if case.payload_marker is not None:
            assert case.payload_marker in case.raw_comment
            assert case.payload_marker in case.expected_cleaned


@pytest.mark.parametrize(
    "fixture,language,case",
    CLEANING_CASES,
    ids=[
        f"{fixture.family_name}:{language}:{case.case_id}"
        for fixture, language, case in CLEANING_CASES
    ],
)
def test_comment_cleaning_fixture_matches_all_public_sanitizer_apis(
    fixture,
    language,
    case,
):
    del fixture
    raw_match = QueryMatch("", "", case.raw_comment)
    sanitizer = CommentSanitizer(language)

    assert sanitizer.sanitize(case.raw_comment) == case.expected_cleaned
    assert sanitizer.sanitize(raw_match) == case.expected_cleaned
    assert sanitize_comment(language, case.raw_comment) == case.expected_cleaned
    assert sanitize_comment_text(language, raw_match) == case.expected_cleaned
