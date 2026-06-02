import pytest

from ml4setk import CommentSanitizer, QueryMatch, sanitize_comment

pytestmark = pytest.mark.unit


def _assert_sanitized(language, raw_comment, expected_cleaned):
    target = QueryMatch("", "", raw_comment)

    assert CommentSanitizer(language).sanitize(target) == expected_cleaned
    assert sanitize_comment(language, raw_comment) == expected_cleaned


def test_stack_v2_autoit_block_removes_decorative_ruler_line():
    raw_comment = (
        "#cs ----------------------------------------------------------------------------\n"
        "\n"
        " AutoIt Version: 3.2.8.1\n"
        " Author:         myName\n"
        "\n"
        " Script Function:\n"
        "\tTemplate AutoIt script.\n"
        "\n"
        "#ce"
    )
    expected_cleaned = (
        "AutoIt Version: 3.2.8.1\n"
        "Author:         myName\n"
        "\n"
        "Script Function:\n"
        "\tTemplate AutoIt script."
    )

    _assert_sanitized("autoit", raw_comment, expected_cleaned)


def test_stack_v2_cmake_line_removes_hash_ruler():
    raw_comment = ("#" * 67) + "\n# Find mongocxx"

    _assert_sanitized("cmake", raw_comment, "Find mongocxx")


def test_stack_v2_julia_nested_ruler_strips_nested_delimiters():
    raw_comment = "#" + ("=" * 90) + "#"
    expected_cleaned = "=" * 88

    _assert_sanitized("julia", raw_comment, expected_cleaned)


def test_stack_v2_pascal_block_preserves_directive_and_slash_star_banner():
    raw_comment = (
        "{$IFDEF LIVE_SERVER_AT_DESIGN_TIME}\n"
        "// *********************************************************************//\n"
        "// OLE Server Properties Proxy Class\n"
        "// Server Object    : TWordDocument\n"
        "// (This object is used by the IDE's Property Inspector to allow editing\n"
        "//  of the properties of this server)\n"
        "// *********************************************************************//"
    )

    _assert_sanitized("pascal", raw_comment, raw_comment)


def test_stack_v2_pascal_line_preserves_framed_hash_title_card():
    raw_comment = (
        "// ##################################\r\n"
        "// ######     IT PAT 2018     #######\r\n"
        "// ######      GrowCery       #######\r\n"
        "// ######  Tiaan van der Riel #######\r\n"
        "// ##################################\r"
    )
    expected_cleaned = (
        "##################################\n"
        "######     IT PAT 2018     #######\n"
        "######      GrowCery       #######\n"
        "######  Tiaan van der Riel #######\n"
        "##################################"
    )

    _assert_sanitized("pascal", raw_comment, expected_cleaned)


def test_stack_v2_powershell_block_preserves_inline_dash_ornament():
    raw_comment = "<#-------------Create Deployment Start------------------#>"
    expected_cleaned = "-------------Create Deployment Start------------------"

    _assert_sanitized("powershell", raw_comment, expected_cleaned)


def test_stack_v2_python_line_removes_hash_ruler_and_residual_hash_gutter():
    raw_comment = (
        "################################################################\r\n"
        "##\r\n"
        "##  As a demonstration of a function which applies defensive\r\n"
        "##  programming in different ways, consider a predicate\r\n"
        "##  which is intended to return True if a given natural\r\n"
        "##  number (i.e., a non-negative integer) is a square of\r\n"
        "##  another natural number.\r\n"
        "##\r\n"
        "##  From this description the function could be \"misused\" in\r\n"
        "##  three ways:\r\n"
        "##\r\n"
        "##  1) It could be given a negative number.\r\n"
        "##  2) It could be given a floating point number.\r\n"
        "##  3) It could be given a value which is not a number at\r\n"
        "##     all.\r\n"
        "##\r\n"
        "##  By adding some \"defensive\" code we can make a naive\r\n"
        "##  implementation more robust by responding appropriately\r\n"
        "##  to each of these cases:\r\n"
        "##\r\n"
        "##  1) A negative number can never be a square of another\r\n"
        "##     number, so we can always return False in this case.\r\n"
        "##     Here we choose to do so \"silently\", not drawing\r\n"
        "##     attention to the unexpected value at all, since the\r\n"
        "##     answer returned is still \"correct\" mathematically.\r\n"
        "##  2) A positive floating point number could be a square of\r\n"
        "##     a natural number so, even though we're not required\r\n"
        "##     to handle floating point numbers we can still do so,\r\n"
        "##     but choose to generate a \"warning\" message in this\r\n"
        "##     case.\r\n"
        "##  3) If the function is given a non-numerical value it\r\n"
        "##     is reasonable to assume that something is seriously\r\n"
        "##     wrong with the calling code, so in this case we\r\n"
        "##     generate an \"error\" message and return the special\r\n"
        "##     value None.\r"
    )
    expected_cleaned = (
        "As a demonstration of a function which applies defensive\n"
        "programming in different ways, consider a predicate\n"
        "which is intended to return True if a given natural\n"
        "number (i.e., a non-negative integer) is a square of\n"
        "another natural number.\n"
        "\n"
        "From this description the function could be \"misused\" in\n"
        "three ways:\n"
        "\n"
        "1) It could be given a negative number.\n"
        "2) It could be given a floating point number.\n"
        "3) It could be given a value which is not a number at\n"
        "   all.\n"
        "\n"
        "By adding some \"defensive\" code we can make a naive\n"
        "implementation more robust by responding appropriately\n"
        "to each of these cases:\n"
        "\n"
        "1) A negative number can never be a square of another\n"
        "   number, so we can always return False in this case.\n"
        "   Here we choose to do so \"silently\", not drawing\n"
        "   attention to the unexpected value at all, since the\n"
        "   answer returned is still \"correct\" mathematically.\n"
        "2) A positive floating point number could be a square of\n"
        "   a natural number so, even though we're not required\n"
        "   to handle floating point numbers we can still do so,\n"
        "   but choose to generate a \"warning\" message in this\n"
        "   case.\n"
        "3) If the function is given a non-numerical value it\n"
        "   is reasonable to assume that something is seriously\n"
        "   wrong with the calling code, so in this case we\n"
        "   generate an \"error\" message and return the special\n"
        "   value None."
    )

    _assert_sanitized("python", raw_comment, expected_cleaned)


def test_stack_v2_sql_line_removes_dash_rulers():
    raw_comment = (
        "-- ----------------------------\n"
        "-- Table structure for tb_article\n"
        "-- ----------------------------"
    )

    _assert_sanitized("sql", raw_comment, "Table structure for tb_article")


def test_stack_v2_python_line_preserves_markdown_heading_and_csharp_token():
    raw_comment = "# # Heading\n# Use C# and F# here"
    expected_cleaned = "# Heading\nUse C# and F# here"

    _assert_sanitized("python", raw_comment, expected_cleaned)


def test_stack_v2_sql_line_preserves_meaningful_dash_flag():
    raw_comment = "-- --force keeps the flag visible\n-- plain explanation"
    expected_cleaned = "--force keeps the flag visible\nplain explanation"

    _assert_sanitized("sql", raw_comment, expected_cleaned)
