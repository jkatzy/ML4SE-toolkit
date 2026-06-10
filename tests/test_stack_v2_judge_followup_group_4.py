import pytest

from ml4setk import CommentQuery, CommentSanitizer

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("source", "expected_comments"),
    [
        pytest.param(
            (
                "$Ontext\n"
                "First documentation block.\n"
                "$Offtext\n"
                "variable x;\n"
                "$ONTEXT second documentation block\n"
                "more documentation\n"
                "$OFFTEXT\n"
                "solve x;\n"
            ),
            [
                "$Ontext\nFirst documentation block.\n$Offtext",
                "$ONTEXT second documentation block\nmore documentation\n$OFFTEXT",
            ],
            id="gams-block-8017ad5594504b18",
        ),
        pytest.param(
            (
                "$ontext\n"
                "write solution2.txt file for\n"
                "contingency solution values\n"
                "$offtext\n"
                "\n"
                "file solution2 /solution2.txt/;\n"
                "put solution2;\n"
            ),
            [("$ontext\nwrite solution2.txt file for\ncontingency solution values\n$offtext")],
            id="gams-block-824cf71dfe39b523",
        ),
    ],
)
def test_stack_v2_extraction_stops_gams_ontext_at_matching_offtext(source, expected_comments):
    assert [match.match for match in CommentQuery("gams").parse(source)] == expected_comments


@pytest.mark.parametrize(
    ("language", "raw_comment", "expected_cleaned"),
    [
        pytest.param(
            "agda",
            (
                "------------------------------------------------------\n"
                "------------------- MPhil project --------------------\n"
                "------------------------------------------------------\n"
                "--- Computational effects, algebraic theories and ----\n"
                "------------ normalization by evaluation -------------\n"
                "------------------------------------------------------\n"
                "--------------------- Renamings ----------------------\n"
                "------------------------------------------------------\n"
                "-------------------- Danel Ahman ---------------------\n"
                "------------------------------------------------------"
            ),
            (
                "MPhil project\n"
                "\n"
                "Computational effects, algebraic theories and\n"
                "normalization by evaluation\n"
                "\n"
                "Renamings\n"
                "\n"
                "Danel Ahman"
            ),
            id="agda-line-f2395c264862a8d3",
        ),
        pytest.param(
            "antlr",
            (
                "/*\n"
                " * =================================\n"
                " * Query\n"
                " * =================================\n"
                " */"
            ),
            "Query",
            id="antlr-block-118af6a931fc1f92",
        ),
        pytest.param(
            "antlr",
            (
                "/**\n"
                "    Copy from the protostuff-compiler project\n"
                "\n"
                "    https://github.com/protostuff/protostuff-compiler\n"
                "*/"
            ),
            (
                "Copy from the protostuff-compiler project\n"
                "\n"
                "https://github.com/protostuff/protostuff-compiler"
            ),
            id="antlr-block-3b504e864b5e064e",
        ),
        pytest.param(
            "antlr",
            (
                "/*------------------------------------------------------------------\n"
                " * PARSER RULES\n"
                " *------------------------------------------------------------------*/"
            ),
            "PARSER RULES",
            id="antlr-block-ae6278470b643597",
        ),
        pytest.param(
            "c",
            (
                "/* ************************************************************************** */\n"
                "/*                                                                            */\n"
                "/*   ft_isalnum.c                                       :+:      :+:    :+:   */\n"
                "/*                                                                            */\n"
                "/* ************************************************************************** */"
            ),
            "ft_isalnum.c                                       :+:      :+:    :+:",
            id="c-block-37dd961ce98f282e",
        ),
        pytest.param(
            "c",
            (
                "/* ************************************************************************** */\n"
                "/*                                                                            */\n"
                "/*   ft_putchar_fd.c                                    :+:      :+:    :+:   */\n"
                "/*                                                                            */\n"
                "/* ************************************************************************** */"
            ),
            "ft_putchar_fd.c                                    :+:      :+:    :+:",
            id="c-block-c022e2b652b31c5a",
        ),
        pytest.param(
            "coldfusion_cfc",
            (
                "<!---\n"
                " * CKFinder\n"
                " * ========\n"
                " * http://cksource.com/ckfinder\n"
                " * Copyright (C) 2007-2015, CKSource.\n"
                "--->"
            ),
            (
                "CKFinder\n"
                "========\n"
                "http://cksource.com/ckfinder\n"
                "Copyright (C) 2007-2015, CKSource."
            ),
            id="coldfusion_cfc-nested-82e99df86e7ada22",
        ),
        pytest.param(
            "f#",
            (
                "(*--------------------------------------------------------------------------*\\\n"
                "**  FsCheck                                                                 **\n"
                "**  Copyright (c) 2008-2013 Kurt Schelfthout. All rights reserved.          **\n"
                "**  https://github.com/kurtschelfthout/FsCheck                              **\n"
                "\\*--------------------------------------------------------------------------*)"
            ),
            (
                "FsCheck\n"
                "Copyright (c) 2008-2013 Kurt Schelfthout. All rights reserved.\n"
                "https://github.com/kurtschelfthout/FsCheck"
            ),
            id="f-nested-5865aafb28cb96e3",
        ),
        pytest.param(
            "gams",
            "*-------------------------------------------------------------------------------",
            "",
            id="gams-line-2c7c1bf46477606a",
        ),
        pytest.param(
            "gams",
            (
                "***\n"
                "* Standard output reports\n"
                "* =======================\n"
                "*\n"
                "* This part contains standard output reports.\n"
                "***"
            ),
            (
                "Standard output reports\n"
                "=======================\n"
                "\n"
                "This part contains standard output reports."
            ),
            id="gams-line-388ed5f553921640",
        ),
        pytest.param(
            "gams",
            "*-------------------------------------------------------------------------------",
            "",
            id="gams-line-e261f910f9482f86",
        ),
        pytest.param(
            "nunjucks",
            (
                "{# *-landing-page classes are a holdover from devsite. #}\n"
                "{# It would be great to remove them as part of the v1 migration. #}"
            ),
            (
                "*-landing-page classes are a holdover from devsite.\n"
                "It would be great to remove them as part of the v1 migration."
            ),
            id="nunjucks-block-824066b0ee3dcb54",
        ),
        pytest.param(
            "opencl",
            (
                "/***************************************************************************\n"
                " * Copyright 1998-2018 by authors (see AUTHORS.txt)                        *\n"
                " *                                                                         *\n"
                " * This file is part of LuxCoreRender.                                     *\n"
                " ***************************************************************************/"
            ),
            (
                "Copyright 1998-2018 by authors (see AUTHORS.txt)\n"
                "\n"
                "This file is part of LuxCoreRender."
            ),
            id="opencl-block-90216fbed4b77390",
        ),
        pytest.param(
            "pike",
            (
                "/* ========================================================================== */\n"
                "/*                                                                            */\n"
                "/*   ftpd.pike"
                "                                                                 */\n"
                "/*   (c) 2010 Ralph Ritoch                                                    */\n"
                "/*                                                                            */\n"
                "/*   Description                                                              */\n"
                "/*   ftpd service controller                                                 */\n"
                "/* ========================================================================== */"
            ),
            ("ftpd.pike\n(c) 2010 Ralph Ritoch\n\nDescription\nftpd service controller"),
            id="pike-block-8332a226e7aeb7e0",
        ),
        pytest.param(
            "pike",
            (
                "/*******************************************************************************\n"
                " *                                                                             *\n"
                " * NOTE! Uncomment the following variables if the language supports macros.    *\n"
                " * Otherwise the default values will apply.                                  *\n"
                " *                                                                             *\n"
                " ******************************************************************************/"
            ),
            (
                "NOTE! Uncomment the following variables if the language supports macros.\n"
                "Otherwise the default values will apply."
            ),
            id="pike-block-a54638bc3007273a",
        ),
        pytest.param(
            "readline_config",
            (
                "#----------------------------------------------------------------#\n"
                "# Name : .inputrc                                                #\n"
                "# Author : Ankit Jain <ajatkj@yahoo.co.in>                       #\n"
                "# Desc : readline configuration                                  #\n"
                "#----------------------------------------------------------------#"
            ),
            (
                "Name : .inputrc\n"
                "Author : Ankit Jain <ajatkj@yahoo.co.in>\n"
                "Desc : readline configuration"
            ),
            id="readline_config-line-800eae0a6c8222c6",
        ),
        pytest.param(
            "scilab",
            "//************************** Generic Digital ***************************",
            "Generic Digital",
            id="scilab-line-899206c68dca5de4",
        ),
        pytest.param(
            "xml_property_list",
            (
                "<!-- Generated by: TmTheme-Editor                 -->\n"
                "<!-- ============================================ -->\n"
                "<!-- app:  http://tmtheme-editor.herokuapp.com    -->\n"
                "<!-- code: https://github.com/aziz/tmTheme-Editor -->"
            ),
            (
                "Generated by: TmTheme-Editor\n"
                "============================================\n"
                "app:  http://tmtheme-editor.herokuapp.com\n"
                "code: https://github.com/aziz/tmTheme-Editor"
            ),
            id="xml_property_list-block-5229aa80b98f0452",
        ),
        pytest.param(
            "xml_property_list",
            (
                "<!-- Generated by: TmTheme-Editor                 -->\n"
                "<!-- ============================================ -->\n"
                "<!-- app:  http://tmtheme-editor.herokuapp.com    -->\n"
                "<!-- code: https://github.com/aziz/tmTheme-Editor -->"
            ),
            (
                "Generated by: TmTheme-Editor\n"
                "============================================\n"
                "app:  http://tmtheme-editor.herokuapp.com\n"
                "code: https://github.com/aziz/tmTheme-Editor"
            ),
            id="xml_property_list-block-ba5e725be2a6d0de",
        ),
    ],
)
def test_stack_v2_sanitation_removes_scaffolding_without_losing_content(
    language, raw_comment, expected_cleaned
):
    assert CommentSanitizer(language).sanitize(raw_comment) == expected_cleaned
