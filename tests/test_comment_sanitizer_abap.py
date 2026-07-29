import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit


def test_abap_generated_interface_preserves_declaration_indentation():
    raw_comment = (
        '*"----------------------------------------------------------------------\n'
        '*"*"Global interface:\n'
        '*"  IMPORTING\n'
        '*"     VALUE(I_DATUM) LIKE  SY-DATUM\n'
        '*"  TABLES\n'
        '*"      T_WORKTIME STRUCTURE  ZS_WORKTIME OPTIONAL\n'
        '*"----------------------------------------------------------------------'
    )
    expected = (
        "Global interface:\n"
        "  IMPORTING\n"
        "     VALUE(I_DATUM) LIKE  SY-DATUM\n"
        "  TABLES\n"
        "      T_WORKTIME STRUCTURE  ZS_WORKTIME OPTIONAL"
    )

    assert sanitize_comment("abap", raw_comment) == expected


def test_abap_generated_module_box_removes_both_side_gutters():
    raw_comment = (
        "*&---------------------------------------------------------------------*\n"
        "*&      Module  RM03E-ZEANS  OUTPUT\n"
        "*&---------------------------------------------------------------------*\n"
        "*   Setzen Kennzeichen 'referentielle EANs vorhanden' auf dem Popup    *\n"
        "*   'Europäische Artikelnummer'                                        *\n"
        "*----------------------------------------------------------------------*"
    )
    expected = (
        "Module  RM03E-ZEANS  OUTPUT\n"
        "Setzen Kennzeichen 'referentielle EANs vorhanden' auf dem Popup\n"
        "'Europäische Artikelnummer'"
    )

    assert sanitize_comment("abap", raw_comment) == expected


@pytest.mark.parametrize(
    ("raw_comment", "expected"),
    [
        (
            "*&---------------------------------------------------------------------*\n"
            "*& Report  ZMMR_IF008                                                  *\n"
            "*&                                                                     *\n"
            "*&---------------------------------------------------------------------*\n"
            "*&                                                                     *\n"
            "*&                                                                     *\n"
            "*&---------------------------------------------------------------------*",
            "Report  ZMMR_IF008",
        ),
        (
            "*---------------------------------------------------------------------*\n"
            "*       FORM LISTE_ABBRECHEN                                          *\n"
            "*---------------------------------------------------------------------*\n"
            "*       ........                                                      *\n"
            "*---------------------------------------------------------------------*",
            "FORM LISTE_ABBRECHEN",
        ),
    ],
)
def test_abap_fixed_width_cards_remove_blank_and_placeholder_rows(
    raw_comment,
    expected,
):
    assert sanitize_comment("abap", raw_comment) == expected


def test_abap_ruler_card_removes_internal_separators_and_common_padding():
    raw_comment = (
        "*&---------------------------------------------------------------------*\n"
        "*&  Include           Z_TH0701_ALV_2_GRIDALV_I01\n"
        "*&---------------------------------------------------------------------*\n"
        "*&---------------------------------------------------------------------*\n"
        "*&      Module  USER_COMMAND_0100  INPUT\n"
        "*&---------------------------------------------------------------------*\n"
        "*       text\n"
        "*----------------------------------------------------------------------*"
    )
    expected = (
        "Include           Z_TH0701_ALV_2_GRIDALV_I01\n"
        "    Module  USER_COMMAND_0100  INPUT\n"
        "     text"
    )

    assert sanitize_comment("abap", raw_comment) == expected


def test_abap_star_banner_preserves_ascii_art_indentation_and_blank_lines():
    raw_comment = (
        "************************************************************************\n"
        "****\n"
        "*            _\n"
        "*   __ _  __| | ___  ___\n"
        "*  / _` |/ _` |/ _ \\\n"
        "* | (_| | (_| |  __/\n"
        "*  \\__,_|\\__,_|\\___|\n"
        "************************************************************************\n"
        "*******\n"
        "*\n"
        "*\n"
        "*&         $USER  $DATE\n"
        "************************************************************************\n"
        "*******"
    )
    expected = (
        "           _\n"
        "  __ _  __| | ___  ___\n"
        " / _` |/ _` |/ _ \\\n"
        "| (_| | (_| |  __/\n"
        " \\__,_|\\__,_|\\___|\n"
        "\n"
        "\n"
        "        $USER  $DATE"
    )

    assert sanitize_comment("abap", raw_comment) == expected


def test_abap_quoted_title_removes_generated_hyphen_padding():
    raw_comment = '" INIT ' + "-" * 74 + '"'

    assert sanitize_comment("abap", raw_comment) == "INIT"


def test_abap_saplink_pipe_frame_preserves_license_punctuation_and_paragraphs():
    raw_comment = (
        "*/---------------------------------------------------------------------\\\n"
        "*|   This file is part of SAPlink.                                     |\n"
        "*|                                                                     |\n"
        "*|   Free software; redistribute it and/or modify it.                  |\n"
        "*|   Copyright (c) Example, Inc.                                      |\n"
        "*\\---------------------------------------------------------------------/"
    )
    expected = (
        "This file is part of SAPlink.\n"
        "\n"
        "Free software; redistribute it and/or modify it.\n"
        "Copyright (c) Example, Inc."
    )

    assert sanitize_comment("abap", raw_comment) == expected


def test_abap_ruler_card_preserves_content_bearing_stars_and_pipes():
    raw_comment = (
        "*----------------------------------------------------------------------*\n"
        "* **bold** | coefficient * scale\n"
        "*----------------------------------------------------------------------*"
    )

    assert sanitize_comment("abap", raw_comment) == "**bold** | coefficient * scale"


@pytest.mark.parametrize(
    ("raw_comment", "expected"),
    [
        ("///EY1/SAV_I_PR_G2S_YB_LCGC\r", "/EY1/SAV_I_PR_G2S_YB_LCGC"),
        ("///EY1/SAV_I_ETR_RG_SUM_ExpTaxEB\r", "/EY1/SAV_I_ETR_RG_SUM_ExpTaxEB"),
    ],
)
def test_abap_cds_namespace_slash_is_content_not_documentation_syntax(
    raw_comment,
    expected,
):
    assert sanitize_comment("abap_cds", raw_comment) == expected
