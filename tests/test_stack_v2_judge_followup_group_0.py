import pytest

from ml4setk import CommentSanitizer, QueryMatch

pytestmark = pytest.mark.unit


def _assert_sanitized(language, raw_comment, expected_cleaned):
    target = QueryMatch("", "", raw_comment)

    assert CommentSanitizer(language).sanitize(target) == expected_cleaned


@pytest.mark.parametrize(
    ("raw_comment", "expected_cleaned"),
    [
        pytest.param(
            "[ JayMarkRelationship                                       ]\n"
            "[   0: not met yet                                          ]\n"
            "[   1: met the two of them                                  ]\n"
            "[   2: met the two of them, player knows their names        ]",
            "JayMarkRelationship\n"
            "0: not met yet\n"
            "1: met the two of them\n"
            "2: met the two of them, player knows their names",
            id="b59d9d357b80685d",
        ),
        pytest.param(
            "[ BridgetPowellEventVar                                ]\n"
            "[  0: never met                                        ]\n"
            "[  1: watched Bridget fuck Powell                      ]\n"
            "[ 98: didn't help in the fight against the lizards     ]\n"
            "[ 99: didn't stay to see what Bridget does with Powell ]",
            "BridgetPowellEventVar\n"
            "0: never met\n"
            "1: watched Bridget fuck Powell\n"
            "98: didn't help in the fight against the lizards\n"
            "99: didn't stay to see what Bridget does with Powell",
            id="c2b2a90c506ce593",
        ),
        pytest.param(
            "[ JayMarkRelationship                                       ]\n"
            "[   0: net met yet                                          ]\n"
            "[   1: met the two of them                                  ]\n"
            "[   2: met the two of them, player knows their names        ]\n"
            "[   3: fucked around with, player knows the names           ]",
            "JayMarkRelationship\n"
            "0: net met yet\n"
            "1: met the two of them\n"
            "2: met the two of them, player knows their names\n"
            "3: fucked around with, player knows the names",
            id="d34e6dde3304294b",
        ),
        pytest.param(
            "[ HP states of Ares                                                               ]\n"
            "[   0: hasn't met the player yet                                                  ]\n"
            "[   1: option for walking him brought up                                          ]\n"
            "[   2: no sex during a walk with him                                              ]\n"
            "[   3: mounted the player when out for a walk                                     ]\n"
            "[   4: mounted Helen/Xerxes when out for a walk                                   ]\n"
            "[   5: mounted both the player and Helen/Xerxes when out for a walk               ]",
            "HP states of Ares\n"
            "0: hasn't met the player yet\n"
            "1: option for walking him brought up\n"
            "2: no sex during a walk with him\n"
            "3: mounted the player when out for a walk\n"
            "4: mounted Helen/Xerxes when out for a walk\n"
            "5: mounted both the player and Helen/Xerxes when out for a walk",
            id="da06b266fbf89410",
        ),
    ],
)
def test_stack_v2_inform_7_grouped_blocks_strip_each_bracket_pair(raw_comment, expected_cleaned):
    _assert_sanitized("inform_7", raw_comment, expected_cleaned)


def test_stack_v2_lfe_line_strips_repeated_semicolons_and_ruler_edges():
    raw_comment = (
        ";;;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
        ";;; Public API\n"
        ";;;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    )

    _assert_sanitized("lfe", raw_comment, "Public API")


def test_stack_v2_rexx_nested_strips_box_gutters():
    raw_comment = (
        "/** REXX **************************************************************\n"
        "**                                                                   **\n"
        "** Copyright 2016-2020 IBM Corp.                                     **\n"
        "**********************************************************************/"
    )
    expected_cleaned = "REXX\n\nCopyright 2016-2020 IBM Corp."

    _assert_sanitized("rexx", raw_comment, expected_cleaned)


def test_stack_v2_xml_grouped_blocks_strip_each_delimiter_pair():
    raw_comment = (
        "<!-- 파싱해서 사용하는 데이터이니 직접 수정하지 마세요 -->\n"
        "<!--From : itemProperty_Skin_newGacha-->"
    )
    expected_cleaned = (
        "파싱해서 사용하는 데이터이니 직접 수정하지 마세요\nFrom : itemProperty_Skin_newGacha"
    )

    _assert_sanitized("xml", raw_comment, expected_cleaned)
