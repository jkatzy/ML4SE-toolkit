"""Version-dependent block comments in Lua, OCaml, SuperCollider, and Markdown.

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
            "lua",
            "--[[ a ]] y = 2\n--[==[ b ]==] z = 3\n--[[ a [[ b ]] c ]] x = 1\n"
            "s = [[ -- no ]] -- yes\nt = [=[ -- ]=] -- end\n",
            {
                "4.0": [
                    "--[[ a ]] y = 2",
                    "--[==[ b ]==] z = 3",
                    "--[[ a [[ b ]] c ]] x = 1",
                    "-- yes",
                    "-- ]=] -- end",
                ],
                "5.0": [
                    "--[[ a ]]",
                    "--[==[ b ]==] z = 3",
                    "--[[ a [[ b ]] c ]]",
                    "-- yes",
                    "-- ]=] -- end",
                ],
                "5.1": ["--[[ a ]]", "--[==[ b ]==]", "--[[ a [[ b ]]", "-- yes", "-- end"],
            },
            id="lua-long-comments",
        ),
        pytest.param(
            "ocaml",
            "(* {| *) let x = 1 (* |} *)\n(* {%ext| *) let y = 2 (* |} *)\n"
            "let s = {|(*|} in (* real *)\n",
            {
                "4.01": ["(* {| *)", "(* |} *)", "(* {%ext| *)", "(* |} *)"],
                "4.02": ["(* {| *) let x = 1 (* |} *)", "(* {%ext| *)", "(* |} *)", "(* real *)"],
                "4.11": [
                    "(* {| *) let x = 1 (* |} *)",
                    "(* {%ext| *) let y = 2 (* |} *)",
                    "(* real *)",
                ],
            },
            id="ocaml-quoted-strings-in-comments",
        ),
        pytest.param(
            "supercollider",
            'x = 1; /* a /* b */*/ y = 2; // */\ns = "/* no"; $/ /*/ x */ // c\n',
            {
                "3.8": ["/* a /* b */*/ y = 2; // */", "/*/ x */", "// c"],
                "3.9": ["/* a /* b */*/", "// */", "/*/ x */", "// c"],
            },
            id="supercollider-overlapping-delimiters",
        ),
        pytest.param(
            "markdown",
            "foo <!-- a -- b -->\n<!-- note -- here -->\nbar <!-- ok --> <!---->\n"
            "`<!-- code -->`\n",
            {
                "commonmark-0.30": ["<!-- note -- here -->", "<!-- ok -->", "<!---->"],
                "commonmark-0.31": [
                    "<!-- a -- b -->",
                    "<!-- note -- here -->",
                    "<!-- ok -->",
                    "<!---->",
                ],
            },
            id="markdown-inline-html-comments",
        ),
    ],
)
def test_differential_source_matches_every_version(language, source, expected):
    assert set(expected) == set(get_comment_language_versions(language))
    for version, comments in expected.items():
        assert _matches(language, source, version) == comments, version


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        pytest.param(
            "(* {%%ext id| *) |id} *) x (* b *)",
            ["(* {%%ext id| *) |id} *)", "(* b *)"],
            id="quoted-item-extension",
        ),
        pytest.param("(* {%a.b| *) |} *)", ["(* {%a.b| *) |} *)"], id="dotted-extension"),
        pytest.param('(* "{|" *) x (* |} *)', ['(* "{|" *)', "(* |} *)"], id="brace-in-string"),
        pytest.param("(* {A| *)", ["(* {A| *)"], id="uppercase-is-not-a-delimiter"),
        pytest.param("let r = {x|y} (* c *)", [], id="quoted-string-at-top-level"),
    ],
)
def test_ocaml_default_quoted_literal_forms(source, expected):
    assert _matches("ocaml", source, "4.11") == expected


@pytest.mark.parametrize(
    ("language", "release", "expected"),
    [
        ("lua", "3.2", "4.0"),
        ("lua", "5.0.3", "5.0"),
        ("lua", "5.4.6", "5.1"),
        ("ocaml", "3.12.1", "4.01"),
        ("ocaml", "4.10.2", "4.02"),
        ("ocaml", "5.2", "4.11"),
        ("supercollider", "3.8.0", "3.8"),
        ("supercollider", "3.13", "3.9"),
    ],
)
def test_release_numbers_select_the_containing_version(language, release, expected):
    assert resolve_comment_language_version(language, release) == expected


@pytest.mark.parametrize("label", ["0.30", "gfm", "commonmark-0.30"])
def test_markdown_labels_select_the_older_inline_rule(label):
    assert resolve_comment_language_version("markdown", label) == "commonmark-0.30"


@pytest.mark.parametrize(
    ("language", "version", "comment", "expected"),
    [
        ("ocaml", "4.01", "(* note *)", "note"),
        ("ocaml", "4.02", "(* note *)", "note"),
        ("lua", "5.0", "--[[ note ]]", "note"),
    ],
)
def test_version_comment_forms_are_cleaned(language, version, comment, expected):
    assert sanitize_comment(language, comment, version=version) == expected
