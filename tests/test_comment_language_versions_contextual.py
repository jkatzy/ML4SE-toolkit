"""Version-dependent comments in languages with contextual extractors.

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


@pytest.mark.parametrize(
    ("language", "source", "expected"),
    [
        pytest.param(
            "nushell",
            "http get https://example.com/docs#intro # fetch docs\necho r#'a #b'#\n"
            'let x = "a#b" # q\n',
            {
                "0.76": ["#intro # fetch docs", "#'a #b'#", "# q"],
                "0.77": ["# fetch docs", "#b'#", "# q"],
                "0.94": ["# fetch docs", "# q"],
            },
            id="nushell-hash-and-raw-strings",
        ),
        pytest.param(
            "caddyfile",
            "example.com {\n\t# docs redirect\n\tredir /help https://example.com/docs#install\n"
            '\trespond "a # b" `c # d`\n}\n',
            {
                "2.0": ["# docs redirect", "#install", "# d`"],
                "2.1": ["# docs redirect"],
            },
            id="caddyfile-hash-inside-token",
        ),
        pytest.param(
            "dotenv",
            "API_URL=https://example.com/#top\nSECRET=abc # rotate monthly\n# full-line note\n"
            'TOKEN=`x#y`\nKEY="a\n# b\nc"\n',
            {
                "13": ["# full-line note", "# b"],
                "14.0": ["#top", "# rotate monthly", "# full-line note", "#y`", "# b"],
                "14.3.2": ["# rotate monthly", "# full-line note", "# b"],
                "15": ["#top", "# rotate monthly", "# full-line note", "#y`"],
                "16": ["#top", "# rotate monthly", "# full-line note"],
            },
            id="dotenv-inline-comments",
        ),
        pytest.param(
            "templ",
            "package main\n\n// hello renders a greeting.\ntempl hello(name string) {\n"
            "\t// greeting markup\n\t<p>Hello, { name }</p>\n}\n",
            {
                "0.2.364": ["// hello renders a greeting."],
                "0.2.408": ["// hello renders a greeting.", "// greeting markup"],
            },
            id="templ-body-go-comments",
        ),
        pytest.param(
            "mermaid",
            'flowchart LR\n  A["one\n  %% two\n  three"] --> B %% trailing\n  %% own line\n'
            "  %%{init: {}}%%\n  B --> C\n",
            {"10.0": ["%% trailing", "%% own line"], "10.1": ["%% two", "%% own line"]},
            id="mermaid-trailing-comments",
        ),
        pytest.param(
            "imba",
            "# hash note\nlet x = 1 // slash note\n/* js block */\nlet r = /// a ///\n",
            {
                "imba1": ["# hash note"],
                "imba2": ["# hash note", "// slash note", "/* js block */"],
            },
            id="imba-slash-comments",
        ),
        pytest.param(
            "mdx",
            "# Title\n\n<!-- draft note -->\n\n{/* reviewer note */}\n\n`<!-- code -->`\n",
            {"mdx1": ["<!-- draft note -->"], "mdx2": ["/* reviewer note */"]},
            id="mdx-comment-forms",
        ),
    ],
)
def test_differential_source_matches_every_version(language, source, expected):
    assert set(expected) == set(get_comment_language_versions(language))
    for version, comments in expected.items():
        assert _matches(language, source, version) == comments, version


@pytest.mark.parametrize(
    ("language", "source", "version", "expected"),
    [
        pytest.param("nushell", "ls foo#'a # c\n", "0.94", ["# c"], id="nushell-mid-word-hash"),
        pytest.param("dotenv", 'KEY="a"b #c\n', "14.3.2", ["#c"], id="dotenv-14.3.2-backtrack"),
        pytest.param("dotenv", "export KEY=a # c\n", "14.0", [], id="dotenv-14-no-export"),
        pytest.param("caddyfile", '"a""b # c"\n', "2.0", [], id="caddy-2.0-adjacent-quotes"),
        pytest.param(
            "mdx",
            "<Note title={/* hint */ 'x'} />\n\n{text}\n",
            "mdx1",
            ["/* hint */"],
            id="mdx1-jsx-attribute-expression",
        ),
    ],
)
def test_version_edge_cases(language, source, version, expected):
    assert _matches(language, source, version) == expected


@pytest.mark.parametrize(
    ("language", "release", "expected"),
    [
        ("nushell", "0.60", "0.76"),
        ("nushell", "0.93.0", "0.77"),
        ("nushell", "0.100", "0.94"),
        ("caddyfile", "1.0.5", "2.0"),
        ("caddyfile", "2.10", "2.1"),
        ("dotenv", "8.2.0", "13"),
        ("dotenv", "14.2.0", "14.0"),
        ("dotenv", "14.3.2", "14.3.2"),
        ("dotenv", "15.0.1", "15"),
        ("dotenv", "17.4.2", "16"),
        ("templ", "0.2.316", "0.2.364"),
        ("templ", "0.3.906", "0.2.408"),
        ("mermaid", "9.4.3", "10.0"),
        ("mermaid", "11.4.1", "10.1"),
        ("mdx", "1.6.22", "mdx1"),
        ("mdx", "3.1", "mdx2"),
    ],
)
def test_release_numbers_select_the_containing_version(language, release, expected):
    assert resolve_comment_language_version(language, release) == expected


@pytest.mark.parametrize(("label", "expected"), [("1", "imba1"), ("2", "imba2")])
def test_imba_major_labels(label, expected):
    assert resolve_comment_language_version("imba", label) == expected


@pytest.mark.parametrize(
    ("language", "version", "comment", "expected"),
    [
        ("imba", "imba2", "// note", "note"),
        ("imba", "imba2", "/* note */", "note"),
        ("mdx", "mdx1", "<!-- note -->", "note"),
        ("dotenv", "13", "# note", "note"),
    ],
)
def test_version_comment_forms_are_cleaned(language, version, comment, expected):
    assert sanitize_comment(language, comment, version=version) == expected
