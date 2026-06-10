import pytest

from ml4setk import CommentSanitizer

pytestmark = pytest.mark.unit


def test_stack_v2_haml_banner_removes_comment_opener_and_decorative_hashes():
    raw_comment = (
        "/ #####################  JAVASCRIPT FOR THE MAP  "
        "##################################"
    )

    assert CommentSanitizer("haml").sanitize(raw_comment) == "JAVASCRIPT FOR THE MAP"


def test_stack_v2_haml_comment_preserves_meaningful_hashes_and_slashes():
    raw_comment = "/ Keep C# and C++ notes at /api/maps under # Heading"
    expected_cleaned = "Keep C# and C++ notes at /api/maps under # Heading"

    assert CommentSanitizer("haml").sanitize(raw_comment) == expected_cleaned


def test_stack_v2_modelica_delimiter_only_asterisk_ruler_sanitizes_to_empty():
    raw_comment = (
        "/**************************************************************************************/"
    )

    assert CommentSanitizer("modelica").sanitize(raw_comment) == ""


def test_stack_v2_modelica_comment_preserves_meaningful_asterisks():
    raw_comment = "/* Keep *** emphasis *** and pointer *value intact. */"
    expected_cleaned = "Keep *** emphasis *** and pointer *value intact."

    assert CommentSanitizer("modelica").sanitize(raw_comment) == expected_cleaned
