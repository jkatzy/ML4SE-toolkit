import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("raw_comment", "expected"),
    [
        (
            "# =============================================================================\n"
            "# SELECTION SCRIPT - SELECT ENTITIES BY SIZE\n"
            "# =============================================================================\n"
            "# Written by Travis Carrigan\n"
            "# \n"
            "# v1: Dec. 12, 2012\n"
            "# v2: Jan. 04, 2013\n"
            "# v3: Jan. 07, 2013\n"
            "#",
            "SELECTION SCRIPT - SELECT ENTITIES BY SIZE\n"
            "Written by Travis Carrigan\n"
            "\n"
            "v1: Dec. 12, 2012\n"
            "v2: Jan. 04, 2013\n"
            "v3: Jan. 07, 2013",
        ),
        (
            "# --------------------------------------------------------\n"
            "# -- INITIALIZATION\n"
            "# --\n"
            "# -- Load Glyph package, initialize Pointwise, and\n"
            "# -- define the working directory.\n"
            "# --\n"
            "# --------------------------------------------------------",
            "INITIALIZATION\n"
            "\n"
            "Load Glyph package, initialize Pointwise, and\n"
            "define the working directory.",
        ),
    ],
)
def test_glyph_banners_and_secondary_gutters_are_removed(raw_comment, expected):
    assert sanitize_comment("glyph", raw_comment) == expected


@pytest.mark.parametrize(
    "raw_comment",
    [
        "COMMENT +",
        "COMMENT ======================================================================",
    ],
)
def test_bdf_delimiter_only_comment_records_clean_to_empty(raw_comment):
    assert sanitize_comment("glyph_bitmap_distribution_format", raw_comment) == ""


def test_win32_nested_c_banner_is_removed():
    raw_comment = (
        ";/************************************************************************************************\n"
        ";Copyright (c) 2001 Microsoft Corporation;\n"
        ";\n"
        ";Module Name:    DSREvents.mc\n"
        ";Abstract:       Message definitions for the DSRestore log messages.\n"
        ";************************************************************************************************/\n"
        ";\n"
        ";#pragma once"
    )

    assert sanitize_comment("win32_message_file", raw_comment) == (
        "Copyright (c) 2001 Microsoft Corporation;\n"
        "\n"
        "Module Name:    DSREvents.mc\n"
        "Abstract:       Message definitions for the DSRestore log messages.\n"
        "\n"
        "#pragma once"
    )


def test_win32_nested_hash_title_card_is_removed():
    raw_comment = (
        ";//\n"
        ";// ####################################################################################\n"
        ";// #\n"
        ";// #  Message File\n"
        ";// #\n"
        ";// ####################################################################################\n"
        ";//"
    )

    assert sanitize_comment("win32_message_file", raw_comment) == "Message File"


@pytest.mark.parametrize("language", ["x_bit_map", "x_bitmap"])
def test_x_bitmap_continuation_gutters_preserve_header_punctuation(language):
    raw_comment = (
        "/* --- Copyright University of Sussex 1991. All rights reserved. ----------\n"
        " * File:            C.x/x/ved/bitmaps/src_48.xbm\n"
        " * Purpose:         Ved icon\n"
        " */"
    )

    assert sanitize_comment(language, raw_comment) == (
        "--- Copyright University of Sussex 1991. All rights reserved. ----------\n"
        "File:            C.x/x/ved/bitmaps/src_48.xbm\n"
        "Purpose:         Ved icon"
    )


@pytest.mark.parametrize("language", ["x_bit_map", "x_bitmap"])
def test_x_bitmap_nested_star_box_is_unwrapped(language):
    raw_comment = (
        "/*\n"
        " * ****************************************\n"
        " * *                                      *\n"
        " * *    Copyright Example Corp.           *\n"
        " * *                                      *\n"
        " * *   All Rights Reserved.               *\n"
        " * *                                      *\n"
        " * ****************************************\n"
        " */"
    )

    assert sanitize_comment(language, raw_comment) == (
        "Copyright Example Corp.\n\nAll Rights Reserved."
    )
