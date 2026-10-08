"""Version-dependent comments in hash-comment languages.

Each case gives the exact comment slices of one source under every supported
version, so a change to any version's rules shows up as a precise diff.
"""

import pytest

from ml4setk import CommentQuery, sanitize_comment
from ml4setk.Parsing.Comments import (
    get_comment_language_versions,
    get_default_comment_language_version,
    resolve_comment_language_version,
)

pytestmark = pytest.mark.unit


def _matches(language, source, version):
    return [match.match for match in CommentQuery(language, version=version).parse(source)]


@pytest.mark.parametrize(
    ("language", "source", "expected"),
    [
        pytest.param(
            "julia",
            "x = 1 #= note =# + 2\n#= a #= b =# c =#\n",
            {
                "0.2": ["#= note =# + 2", "#= a #= b =# c =#"],
                "0.3": ["#= note =#", "#= a #= b =# c =#"],
            },
            id="julia-block-comments",
        ),
        pytest.param(
            "fluent",
            "// legacy note\n# modern note\nhello = Hello # text\n#tag\n## group\n",
            {"0.4": ["// legacy note"], "1.0": ["# modern note", "## group"]},
            id="fluent-comment-sigil",
        ),
        pytest.param(
            "ssh_config",
            "Host example # office server\n  LocalCommand echo connected # notify\n"
            '  User "a #b" # c\nHost a#b\n# full line\n',
            {
                "8.4": ["# full line"],
                "8.5": ["# office server", "# notify", '#b" # c', "#b", "# full line"],
                "8.7": ["# office server", "# c", "# full line"],
            },
            id="ssh-config-trailing-comments",
        ),
        pytest.param(
            "org",
            "#todo tighten wording\nIssue #42 is fixed.\n  # indented note\n#+TITLE: x\n"
            "  #+ old indented\n#+begin_comment\n# inner\n#+end_comment\n",
            {
                "7.8": [
                    "#todo tighten wording",
                    "#+ old indented",
                    "#+begin_comment\n# inner\n#+end_comment",
                ],
                "8.0": ["# indented note", "#+begin_comment\n# inner\n#+end_comment"],
            },
            id="org-comment-lines",
        ),
        pytest.param(
            "mcfunction",
            "# give the starter kit \\\ngive @s minecraft:bread 4\nsay done\n"
            "execute if block ~ ~ ~ #minecraft:logs run say hi\nsay a \\\n# joined\n",
            {
                "1.20.1": ["# give the starter kit \\", "# joined"],
                "1.20.2": ["# give the starter kit \\\ngive @s minecraft:bread 4"],
            },
            id="mcfunction-line-continuation",
        ),
        pytest.param(
            "picolisp",
            "(setq X 1) #{ note }# (setq Y 2)\n#{ a #{ b }#\n(setq Z 3) # c }#\n",
            {
                "2.3.6": ["#{ note }# (setq Y 2)", "#{ a #{ b }#", "# c }#"],
                "2.3.7": ["#{ note }#", "#{ a #{ b }#", "# c }#"],
                "18.6": ["#{ note }#", "#{ a #{ b }#\n(setq Z 3) # c }#"],
            },
            id="picolisp-block-comments",
        ),
        pytest.param(
            "jq",
            '[\n  1,\n  # skip two \\\n  2,\n  # even \\\\\n  3, "a # b"\n]\n',
            {
                "1.7": ["# skip two \\", "# even \\\\"],
                "1.8": ["# skip two \\\n  2,", "# even \\\\"],
            },
            id="jq-comment-continuation",
        ),
    ],
)
def test_differential_source_matches_every_version(language, source, expected):
    assert set(expected) == set(get_comment_language_versions(language))
    for version, comments in expected.items():
        assert _matches(language, source, version) == comments, version


@pytest.mark.parametrize(
    ("language", "source", "expected"),
    [
        pytest.param("jq", "# a\r\n.foo\n", ["# a\r"], id="jq-1.7-keeps-crlf-cr"),
        pytest.param("ssh_config", "  ProxyCommand=nc %h %p # raw\n", [], id="ssh-command-equals"),
        pytest.param("ssh_config", "  proxycommand nc %h %p # raw\n", [], id="ssh-command-case"),
        pytest.param("org", "#+BEGIN_COMMENT\nnote\n", [], id="org-unclosed-comment-block"),
        pytest.param("fluent", "#note\n# a\r\n", ["# a"], id="fluent-crlf"),
        pytest.param("mcfunction", "  # note\n", ["# note"], id="mcfunction-indented"),
    ],
)
def test_default_version_edge_cases(language, source, expected):
    default = get_default_comment_language_version(language)
    assert _matches(language, source, default) == expected


@pytest.mark.parametrize(
    ("language", "source", "version", "expected"),
    [
        pytest.param("jq", "# a\r\n.foo\n", "1.8", ["# a"], id="jq-1.8-ends-before-crlf"),
        pytest.param("jq", "# a\rb\n.foo\n", "1.8", ["# a\rb"], id="jq-1.8-keeps-bare-cr"),
    ],
)
def test_version_line_ending_rules(language, source, version, expected):
    assert _matches(language, source, version) == expected


@pytest.mark.parametrize(
    ("language", "release", "expected"),
    [
        ("julia", "0.2.1", "0.2"),
        ("julia", "1.10.4", "0.3"),
        ("fluent", "0.4.0", "0.4"),
        ("fluent", "0.9", "1.0"),
        ("ssh_config", "7.4", "8.4"),
        ("ssh_config", "8.6", "8.5"),
        ("ssh_config", "9.9", "8.7"),
        ("org", "7.9.1", "7.8"),
        ("org", "9.6", "8.0"),
        ("mcfunction", "1.20.1", "1.20.1"),
        ("mcfunction", "1.21.4", "1.20.2"),
        ("picolisp", "17.12", "2.3.7"),
        ("picolisp", "24.3", "18.6"),
        ("jq", "1.6", "1.7"),
        ("jq", "1.7.1", "1.7"),
        ("jq", "1.8.1", "1.8"),
    ],
)
def test_release_numbers_select_the_containing_version(language, release, expected):
    assert resolve_comment_language_version(language, release) == expected


def test_releases_before_the_first_supported_range_are_rejected():
    with pytest.raises(NotImplementedError, match="Supported versions"):
        resolve_comment_language_version("fluent", "0.2")


@pytest.mark.parametrize(
    ("language", "version", "comment", "expected"),
    [
        ("fluent", "1.0", "### note", "note"),
        ("fluent", "0.4", "// note", "note"),
        ("org", "8.0", "#+BEGIN_COMMENT\nnote\n#+END_COMMENT", "note"),
        ("picolisp", "2.3.7", "#{ note }#", "note"),
        ("picolisp", "18.6", "#{ note }#", "note"),
    ],
)
def test_version_comment_forms_are_cleaned(language, version, comment, expected):
    assert sanitize_comment(language, comment, version=version) == expected
