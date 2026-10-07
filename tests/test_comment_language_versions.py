"""Version-dependent comment syntax: registry tables, resolution, and queries.

A language whose comment syntax changed between versions carries a
``CommentLanguageVersions`` table. Its registry entry implements the default
version; every other version overlays the fields it changes. Queries accept a
``version`` keyword, warn once when a versioned language is used without one,
and raise ``UnsupportedCommentLanguageVersionError`` listing the supported
versions when the requested version is unknown.
"""

import importlib
import warnings

import pytest

from ml4setk import (
    CommentQuery,
    CommentSanitizer,
    LineCommentQuery,
    NestedCommentQuery,
    OpeningCommentQuery,
    sanitize_comment,
)
from ml4setk.Parsing.Comments import (
    VERSIONED_COMMENT_LANGUAGES,
    CommentLanguageVersionWarning,
    UnsupportedCommentLanguageVersionError,
    comment_language_requires_version,
    get_comment_language_versions,
    get_comment_syntax,
    get_default_comment_language_version,
    iter_comment_syntaxes,
    resolve_comment_language_version,
)

pytestmark = pytest.mark.unit

registry_module = importlib.import_module("ml4setk.Parsing.Comments.registry")


@pytest.fixture(autouse=True)
def _reset_default_version_warnings():
    registry_module._WARNED_DEFAULT_VERSIONS.clear()
    yield
    registry_module._WARNED_DEFAULT_VERSIONS.clear()


def _tables():
    for syntax in iter_comment_syntaxes():
        for table in syntax.language_versions:
            yield syntax, table


def _version_cases():
    for syntax, table in _tables():
        for language in table.languages:
            for version in table.versions:
                yield pytest.param(
                    syntax, table, language, version, id=f"{language}@{version.name}"
                )


def _matches(language, source, version):
    return [match.match for match in CommentQuery(language, version=version).parse(source)]


def test_versioned_languages_are_flagged_and_listed():
    assert VERSIONED_COMMENT_LANGUAGES
    assert list(VERSIONED_COMMENT_LANGUAGES) == sorted(VERSIONED_COMMENT_LANGUAGES)
    for language in VERSIONED_COMMENT_LANGUAGES:
        assert comment_language_requires_version(language)
        assert get_comment_syntax(language).requires_version(language)
        versions = get_comment_language_versions(language)
        assert len(versions) >= 2
        assert get_default_comment_language_version(language) in versions


def test_unversioned_language_reports_no_versions():
    assert not comment_language_requires_version("java")
    assert get_comment_language_versions("java") == ()
    assert get_default_comment_language_version("java") is None
    assert resolve_comment_language_version("java", None) is None


@pytest.mark.parametrize(("syntax", "table", "language", "version"), list(_version_cases()))
def test_every_version_label_resolves_to_its_version(syntax, table, language, version):
    for label in version.labels:
        assert resolve_comment_language_version(language, label) == version.name
        assert resolve_comment_language_version(language, label.upper()) == version.name
    if version.release:
        assert resolve_comment_language_version(language, version.release) == version.name


@pytest.mark.parametrize(("syntax", "table", "language", "version"), list(_version_cases()))
def test_version_examples_are_comments_under_their_version(syntax, table, language, version):
    for example in version.examples:
        assert example.expected_match in _matches(language, example.sample, version.name)


@pytest.mark.parametrize(("syntax", "table", "language", "version"), list(_version_cases()))
def test_non_default_versions_change_extraction(syntax, table, language, version):
    if version.name == table.default:
        assert get_comment_syntax(language, version.name) is syntax
        return
    assert get_comment_syntax(language, version.name) is not syntax
    assert any(
        _matches(language, example.sample, version.name)
        != _matches(language, example.sample, table.default)
        for example in version.examples
    )


def test_default_version_is_the_registry_entry_and_warns_once():
    language = VERSIONED_COMMENT_LANGUAGES[0]
    default = get_default_comment_language_version(language)

    with pytest.warns(CommentLanguageVersionWarning, match=r"assuming '.+'") as recorded:
        query = CommentQuery(language)
    assert query.version == default
    assert str(default) in str(recorded[0].message)
    for name in get_comment_language_versions(language):
        assert name in str(recorded[0].message)

    with warnings.catch_warnings(record=True) as again:
        warnings.simplefilter("always")
        CommentQuery(language)
        LineCommentQuery(language)
        sanitize_comment(language, "x")
    assert not [w for w in again if issubclass(w.category, CommentLanguageVersionWarning)]


def test_explicit_version_does_not_warn():
    language = VERSIONED_COMMENT_LANGUAGES[0]
    default = get_default_comment_language_version(language)
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        CommentQuery(language, version=default)
        NestedCommentQuery(language, version=default)
        OpeningCommentQuery(language, version=default)
        CommentSanitizer(language, version=default)
    assert not [w for w in recorded if issubclass(w.category, CommentLanguageVersionWarning)]


def test_unversioned_language_never_warns():
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        CommentQuery("java")
    assert not [w for w in recorded if issubclass(w.category, CommentLanguageVersionWarning)]


@pytest.mark.parametrize(
    "factory",
    [
        lambda language, version: CommentQuery(language, version=version),
        lambda language, version: LineCommentQuery(language, version=version),
        lambda language, version: NestedCommentQuery(language, version=version),
        lambda language, version: OpeningCommentQuery(language, version=version),
        lambda language, version: CommentSanitizer(language, version=version),
        lambda language, version: sanitize_comment(language, "x", version=version),
        lambda language, version: get_comment_syntax(language, version),
    ],
    ids=["comment", "line", "nested", "opening", "sanitizer", "sanitize", "syntax"],
)
def test_unknown_version_lists_supported_versions(factory):
    language = VERSIONED_COMMENT_LANGUAGES[0]
    with pytest.raises(UnsupportedCommentLanguageVersionError) as caught:
        factory(language, "no-such-version")

    error = caught.value
    assert isinstance(error, NotImplementedError)
    assert isinstance(error, ValueError)
    assert error.language == language
    assert error.version == "no-such-version"
    assert error.supported_versions == get_comment_language_versions(language)
    message = str(error)
    assert "Supported versions:" in message
    for name in error.supported_versions:
        assert name in message
    assert "default" in message


def test_version_for_unversioned_language_is_rejected():
    with pytest.raises(UnsupportedCommentLanguageVersionError) as caught:
        CommentQuery("java", version="17")
    assert caught.value.supported_versions == ()
    assert "no version-dependent comment syntax" in str(caught.value)


def test_unknown_language_still_raises_not_implemented():
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        CommentQuery("befunge", version="93")


def test_version_must_be_a_string():
    with pytest.raises(TypeError):
        CommentQuery(VERSIONED_COMMENT_LANGUAGES[0], version=3)


def test_multi_language_query_takes_a_version_mapping():
    language = VERSIONED_COMMENT_LANGUAGES[0]
    default = get_default_comment_language_version(language)
    query = CommentQuery([language, "java"], version={language: default})
    assert query.version == {language: default, "java": None}

    with pytest.raises(TypeError):
        CommentQuery([language, "java"], version=default)
    with pytest.raises(ValueError, match="not queried"):
        CommentQuery([language, "java"], version={"python": "3"})
    with pytest.raises(UnsupportedCommentLanguageVersionError):
        CommentQuery([language, "java"], version={"java": "17"})
