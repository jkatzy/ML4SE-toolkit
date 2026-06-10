import pytest

from ml4setk import CommentSanitizer

pytestmark = pytest.mark.unit


def test_stack_v2_mustache_facebook_2016_license_removes_tag_delimiters():
    raw_comment = (
        "{{!\n"
        "\n"
        "  Copyright 2016 Facebook, Inc.\n"
        "\n"
        '  Licensed under the Apache License, Version 2.0 (the "License");\n'
        "\n"
        "}}"
    )
    expected_cleaned = (
        "Copyright 2016 Facebook, Inc.\n"
        "\n"
        'Licensed under the Apache License, Version 2.0 (the "License");'
    )

    assert CommentSanitizer("mustache").sanitize(raw_comment) == expected_cleaned


def test_stack_v2_mustache_facebook_affiliates_license_removes_tag_delimiters():
    raw_comment = (
        "{{!\n"
        "\n"
        "  Copyright (c) Facebook, Inc. and its affiliates.\n"
        "\n"
        "  Unless required by applicable law or agreed to in writing, software\n"
        '  distributed under the License is distributed on an "AS IS" BASIS,\n'
        "\n"
        "}}"
    )
    expected_cleaned = (
        "Copyright (c) Facebook, Inc. and its affiliates.\n"
        "\n"
        "Unless required by applicable law or agreed to in writing, software\n"
        'distributed under the License is distributed on an "AS IS" BASIS,'
    )

    assert CommentSanitizer("mustache").sanitize(raw_comment) == expected_cleaned


def test_stack_v2_modelica_clara_header_removes_right_edge_gutters():
    raw_comment = (
        "//___________________________________________________________________________//\n"
        "// Component of the ClaRa library, version: 1.0.0                        //\n"
        "//                                                                           //\n"
        "// Licensed by the DYNCAP research team under Modelica License 2.            //\n"
        "//___________________________________________________________________________//"
    )
    expected_cleaned = (
        "Component of the ClaRa library, version: 1.0.0\n"
        "\n"
        "Licensed by the DYNCAP research team under Modelica License 2."
    )

    assert CommentSanitizer("modelica").sanitize(raw_comment) == expected_cleaned


def test_stack_v2_modelica_transient_header_removes_right_edge_gutters():
    raw_comment = (
        "//________________________________________________________________________________//\n"
        "// Component of the TransiEnt Library, version: 2.0.0                             //\n"
        "//                                                                                //\n"
        "// Licensed by Hamburg University of Technology under the 3-BSD-clause.           //\n"
        "//________________________________________________________________________________//"
    )
    expected_cleaned = (
        "Component of the TransiEnt Library, version: 2.0.0\n"
        "\n"
        "Licensed by Hamburg University of Technology under the 3-BSD-clause."
    )

    assert CommentSanitizer("modelica").sanitize(raw_comment) == expected_cleaned


def test_stack_v2_sas_proc_means_banner_removes_each_block_wrapper():
    raw_comment = (
        "/**********************************************************************************/\r\n"
        "/* MULTIPLE OUTPUT data sets from PROC MEANS using different variables with CLASS */\r\n"
        "/**********************************************************************************/"
    )

    assert CommentSanitizer("sas").sanitize(raw_comment) == (
        "MULTIPLE OUTPUT data sets from PROC MEANS using different variables with CLASS"
    )


def test_stack_v2_sas_wrds_metadata_removes_each_block_wrapper():
    raw_comment = (
        "/* WRDS Macro: ICLINK"
        "                                                                */\r\n"
        "/* Summary   : Create IBES-CRSP Link Table"
        "                                           */\r\n"
        "/* Date      : September 25, 2006                                                    */"
    )
    expected_cleaned = (
        "WRDS Macro: ICLINK\n"
        "Summary   : Create IBES-CRSP Link Table\n"
        "Date      : September 25, 2006"
    )

    assert CommentSanitizer("sas").sanitize(raw_comment) == expected_cleaned


def test_stack_v2_quake_copyright_header_removes_each_block_wrapper():
    raw_comment = (
        "/* Copyright (C)-ip992, Digital Equipment Corporation                         */\n"
        "/* All rights reserved.                                                      */\n"
        "/* See the file COPYRIGHT for a full description.                            */"
    )
    expected_cleaned = (
        "Copyright (C)-ip992, Digital Equipment Corporation\n"
        "All rights reserved.\n"
        "See the file COPYRIGHT for a full description."
    )

    assert CommentSanitizer("quake").sanitize(raw_comment) == expected_cleaned


def test_stack_v2_rust_inner_doc_comment_removes_full_doc_prefix():
    raw_comment = (
        "//! [`super::usefulness`] explains most of what is happening in this file.\n"
        "//! values and patterns are made from constructors applied to fields.\n"
        "//!\n"
        "//! # Constructor splitting"
    )
    expected_cleaned = (
        "[`super::usefulness`] explains most of what is happening in this file.\n"
        "values and patterns are made from constructors applied to fields.\n"
        "\n"
        "# Constructor splitting"
    )

    assert CommentSanitizer("rust").sanitize(raw_comment) == expected_cleaned
