import pytest

from ml4setk import CommentSanitizer

pytestmark = pytest.mark.unit


def _sanitize(language: str, raw_comment: str) -> str:
    return CommentSanitizer(language).sanitize(raw_comment)


@pytest.mark.parametrize(
    ("raw_comment", "expected_cleaned"),
    [
        pytest.param(
            (
                "------------------------------------------------------------------------------\n"
                "--                  Copyright (C) 2018, AdaCore                        --\n"
                "------------------------------------------------------------------------------"
            ),
            "Copyright (C) 2018, AdaCore",
            id="ada-line-7c07a474a1543705",
        ),
        pytest.param(
            (
                "------------------------------------------------------------------------------\n"
                "--                            Matreshka Project                             --\n"
                "------------------------------------------------------------------------------"
            ),
            "Matreshka Project",
            id="ada-line-e6fa9d8398441ced",
        ),
        pytest.param(
            (
                "------------------------------------------------------------------------------\n"
                "-- terms of the GNU General Public License as published by the Free Soft- --\n"
                "------------------------------------------------------------------------------"
            ),
            "terms of the GNU General Public License as published by the Free Soft-",
            id="ada-line-e79591e0a5da962a",
        ),
    ],
)
def test_stack_v2_ada_boxed_comments_remove_right_edge_gutters(raw_comment, expected_cleaned):
    assert _sanitize("ada", raw_comment) == expected_cleaned


def test_stack_v2_ant_grouped_comments_remove_each_xml_wrapper():
    raw_comment = (
        "<!-- You may freely edit this file. See commented blocks below for -->\n"
        "<!-- some examples of how to customize the build. -->\n"
        "<!-- (If you delete it and reopen the project it will be recreated.) -->\n"
        "<!-- By default, only the Clean and Build commands use this build script. -->\n"
        "<!-- Commands such as Run, Debug, and Test only use this build script if -->\n"
        "<!-- the Compile on Save feature is turned off for the project. -->\n"
        "<!-- You can turn off the Compile on Save (or Deploy on Save) setting -->\n"
        "<!-- in the project's Project Properties dialog box.-->"
    )
    expected_cleaned = (
        "You may freely edit this file. See commented blocks below for\n"
        "some examples of how to customize the build.\n"
        "(If you delete it and reopen the project it will be recreated.)\n"
        "By default, only the Clean and Build commands use this build script.\n"
        "Commands such as Run, Debug, and Test only use this build script if\n"
        "the Compile on Save feature is turned off for the project.\n"
        "You can turn off the Compile on Save (or Deploy on Save) setting\n"
        "in the project's Project Properties dialog box."
    )

    assert _sanitize("ant_build_system", raw_comment) == expected_cleaned


def test_stack_v2_handlebars_license_removes_comment_tag_delimiters():
    raw_comment = (
        "{{!\n"
        "* Licensed to the Apache Software Foundation (ASF) under one\n"
        "* or more contributor license agreements.  See the NOTICE file\n"
        "* distributed with this work for additional information\n"
        "}}"
    )
    expected_cleaned = (
        "* Licensed to the Apache Software Foundation (ASF) under one\n"
        "* or more contributor license agreements.  See the NOTICE file\n"
        "* distributed with this work for additional information"
    )

    assert _sanitize("handlebars", raw_comment) == expected_cleaned


@pytest.mark.parametrize(
    ("title", "body", "expected_cleaned"),
    [
        pytest.param(
            "ameynert/stage-cram-filter-wgs Nextflow config file",
            None,
            "ameynert/stage-cram-filter-wgs Nextflow config file",
            id="nextflow-block-06cbe92af0516413",
        ),
        pytest.param(
            "nf-core/sarek Nextflow config file",
            "Default config options for all environments.",
            (" nf-core/sarek Nextflow config file\nDefault config options for all environments."),
            id="nextflow-block-0de43860ee5c2ac5",
        ),
        pytest.param(
            "peterk87/nf-iav-ont Nextflow config file",
            (
                "Default config options for all environments.\n"
                "Cluster-specific config options should be saved\n"
                "in the conf folder and imported under a profile\n"
                "name here."
            ),
            (
                " peterk87/nf-iav-ont Nextflow config file\n"
                "Default config options for all environments.\n"
                "Cluster-specific config options should be saved\n"
                "in the conf folder and imported under a profile\n"
                "name here."
            ),
            id="nextflow-block-588b52ab99dc6326",
        ),
        pytest.param(
            "nf-core/proteomicslfq Nextflow config file",
            "Default config options for all environments.",
            (
                " nf-core/proteomicslfq Nextflow config file\n"
                "Default config options for all environments."
            ),
            id="nextflow-block-65f9d49bc979d24d",
        ),
    ],
)
def test_stack_v2_nextflow_config_removes_decorative_rulers(title, body, expected_cleaned):
    body_lines = "" if body is None else "".join(f" * {line}\n" for line in body.splitlines())
    raw_comment = (
        "/*\n"
        " * -------------------------------------------------\n"
        f" *  {title}\n"
        " * -------------------------------------------------\n"
        f"{body_lines}"
        " */"
    )

    assert _sanitize("nextflow", raw_comment) == expected_cleaned


def test_stack_v2_sql_delimiter_only_ruler_sanitizes_to_empty_text():
    raw_comment = (
        "/*-----------------------------------------------------------------------------------*/"
    )

    assert _sanitize("sql", raw_comment) == ""
