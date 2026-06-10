import pytest

from ml4setk import CommentQuery, CommentSanitizer

pytestmark = pytest.mark.unit


def _sanitize_extracted_autoit_block(source: str) -> str:
    match, = CommentQuery("autoit").parse(source)
    return CommentSanitizer("autoit").sanitize(match)


def test_autoit_block_removes_source_indentation_from_single_content_line():
    source = (
        "\t#cs ==============================\n"
        "\tEXAMPLE SECTION ==================\n"
        "\t#ce =============================="
    )

    assert _sanitize_extracted_autoit_block(source) == "EXAMPLE SECTION =================="


def test_autoit_block_preserves_relative_content_indentation():
    source = "#cs\n\tExample:\n\t\tchild\n\t#ce"

    assert _sanitize_extracted_autoit_block(source) == "Example:\n\tchild"
