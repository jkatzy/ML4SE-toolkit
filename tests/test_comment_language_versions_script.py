"""Version-dependent comments in scripting and configuration languages.

Each case gives the exact comment slices of one source under every supported
version, so a change to any version's rules shows up as a precise diff.
"""

import pytest

from ml4setk import CommentQuery, sanitize_comment
from ml4setk.Parsing.Comments import (
    get_comment_language_versions,
    resolve_comment_language_version,
)

pytestmark = pytest.mark.unit


def _matches(language, source, version):
    return [match.match for match in CommentQuery(language, version=version).parse(source)]


_PHP_SOURCE = (
    "<?php\n$sql = <<<SQL\n  SELECT 1\n  SQL; # end of query\nSQL;\n#[Pure]\nfunction f() {}\n"
)


@pytest.mark.parametrize(
    ("language", "source", "expected"),
    [
        pytest.param(
            "php",
            _PHP_SOURCE,
            {
                "php7.2": ["#[Pure]"],
                "php7.3": ["# end of query", "#[Pure]"],
                "php8.0": ["# end of query"],
            },
            id="php-attributes-and-flexible-heredoc",
        ),
        pytest.param(
            "php",
            "<?php\n$s = <<<'EOT'\n# body\nEOT;\n$t = 1; # code ?>\n",
            {"php7.2": ["# code "], "php7.3": ["# code "], "php8.0": ["# code "]},
            id="php-column-zero-nowdoc-closes-in-every-version",
        ),
        *(
            pytest.param(
                language,
                "<?php\n#[Pure]\nfunction f() {} # tail\n",
                {"php7.4": ["#[Pure]", "# tail"], "php8.0": ["# tail"]},
                id=f"{language}-attributes",
            )
            for language in ("html_php", "html_plus_php")
        ),
        *(
            pytest.param(
                language,
                'vim9script\n# header note\nvar total = 0  # running total\necho "a # b"\n'
                "var path = 'C:\\' # dir\nvar d = {a: 1} #{ not a comment\n",
                {
                    "legacy": [],
                    "vim9": ["# header note", "# running total", "# dir"],
                },
                id=f"{language}-vim9-hash-comments",
            )
            for language in ("vim_script", "viml")
        ),
        pytest.param(
            "editorconfig",
            "[*.py]  ; python files\nindent_style = space ; use spaces\n"
            'name = "a ; b"\nkey=a#b\n# full-line\n',
            {
                "pre-0.15": ["; python files", "; use spaces", '; b"', "# full-line"],
                "0.15": ["# full-line"],
            },
            id="editorconfig-inline-comments",
        ),
        pytest.param(
            "cairo_zero",
            "const SIZE = 3  # cells\n// cells\n%{ x = 1  # hint\n%}\nlet s = 'a#b';\n",
            {"0.9": ["# cells"], "0.10": ["// cells"]},
            id="cairo-zero-comment-marker",
        ),
        pytest.param(
            "macaulay2",
            "{* old block note *}\n-* new block note *-\nx = 1 -- line note\n",
            {
                "1.10": ["{* old block note *}", "-- line note"],
                "1.11": ["{* old block note *}", "-* new block note *-", "-- line note"],
                "1.13": ["-* new block note *-", "-- line note"],
            },
            id="macaulay2-block-delimiters",
        ),
    ],
)
def test_differential_source_matches_every_version(language, source, expected):
    assert set(expected) == set(get_comment_language_versions(language))
    for version, comments in expected.items():
        assert _matches(language, source, version) == comments, version


@pytest.mark.parametrize(
    ("language", "release", "expected"),
    [
        ("php", "5.6", "php7.2"),
        ("php", "7.2.34", "php7.2"),
        ("php", "7.4.33", "php7.3"),
        ("php", "8.3", "php8.0"),
        ("html_php", "7.3", "php7.4"),
        ("html_php", "8.1", "php8.0"),
        ("editorconfig", "0.12.5", "pre-0.15"),
        ("editorconfig", "0.17.2", "0.15"),
        ("cairo_zero", "0.9.1", "0.9"),
        ("cairo_zero", "0.13.1", "0.10"),
        ("macaulay2", "1.9", "1.10"),
        ("macaulay2", "1.12", "1.11"),
        ("macaulay2", "1.24.11", "1.13"),
    ],
)
def test_release_numbers_select_the_containing_version(language, release, expected):
    assert resolve_comment_language_version(language, release) == expected


def test_vim_versions_have_no_release_numbers():
    # Vim 9 still runs legacy scripts, so a Vim release does not pick a version.
    with pytest.raises(NotImplementedError, match="Supported versions"):
        resolve_comment_language_version("vim_script", "9.1")


@pytest.mark.parametrize(
    ("language", "version", "comment", "expected"),
    [
        ("vim_script", "vim9", "# note", "note"),
        ("cairo_zero", "0.9", "# note", "note"),
        ("macaulay2", "1.10", "{* note *}", "note"),
        ("macaulay2", "1.11", "{* note *}", "note"),
        ("editorconfig", "pre-0.15", "; note", "note"),
    ],
)
def test_version_only_comment_forms_are_cleaned(language, version, comment, expected):
    assert sanitize_comment(language, comment, version=version) == expected
