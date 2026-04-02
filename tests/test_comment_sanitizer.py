import pytest

import ml4setk
from ml4setk import CommentQuery, CommentSanitizer, QueryMatch, sanitize_comment_text

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("language", "comment", "expected"),
    [
        pytest.param("java", "// note", "note", id="java-line"),
        pytest.param("batchfile", "REM note", "note", id="batchfile-rem"),
        pytest.param("adobe_font_metrics", "Comment note", "note", id="afm-comment-record"),
        pytest.param("gerber_image", "G04 note *", "note", id="gerber-line-terminator"),
        pytest.param("mustache", "{{! note }}", "note", id="mustache-line-wrapper"),
        pytest.param("objectscript", "##; + 100", "+ 100", id="objectscript-line-prefix"),
        pytest.param("java", "/* note */", "note", id="java-block"),
        pytest.param("html", "<!-- note -->", "note", id="html-block"),
        pytest.param("python", '"""note"""', "note", id="python-triple-quote"),
        pytest.param(
            "liquid",
            "{% comment %}\nblock note\n{% endcomment %}",
            "block note",
            id="liquid-multiline-block",
        ),
        pytest.param("perl", "=pod\nnote\n=cut", "note", id="perl-pod-block"),
        pytest.param(
            "inform_7",
            "[Remember the bull.]",
            "Remember the bull.",
            id="inform7-bracket-block",
        ),
    ],
)
def test_sanitize_comment_text_strips_comment_syntax(language, comment, expected):
    assert sanitize_comment_text(language, comment) == expected


def test_comment_sanitizer_accepts_query_match_objects():
    sample = "prefix\n// keep the fallback branch\nsuffix"
    match = CommentQuery("java").parse(sample)[0]

    assert CommentSanitizer("java").sanitize(match) == "keep the fallback branch"


def test_comment_sanitizer_strips_grouped_line_comment_blocks():
    sample = "// first line\n// second line\nint value = 1;"
    match = CommentQuery("java").parse(sample)[0]

    assert sanitize_comment_text("java", match) == "first line\nsecond line"


def test_comment_sanitizer_strips_doc_block_leaders():
    comment = "/**\n * first line\n * second line\n */"

    assert sanitize_comment_text("java", comment) == "first line\nsecond line"


def test_comment_sanitizer_strips_only_the_outer_nested_comment_syntax():
    sample = "before {- outer {- inner -} outer -} after"
    match = CommentQuery("haskell").parse(sample)[0]

    assert sanitize_comment_text("haskell", match) == "outer {- inner -} outer"


def test_comment_sanitizer_rejects_non_comment_input_types():
    with pytest.raises(TypeError):
        sanitize_comment_text("java", 123)  # type: ignore[arg-type]


def test_root_package_exports_comment_sanitizer_helpers():
    assert ml4setk.CommentSanitizer is CommentSanitizer
    assert ml4setk.sanitize_comment_text is sanitize_comment_text
    assert isinstance(QueryMatch("", "", "// note"), QueryMatch)
