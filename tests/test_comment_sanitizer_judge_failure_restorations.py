"""Focused regressions and near misses from the two-stage judge repair."""

from __future__ import annotations

import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("language", "raw_comment", "expected"),
    [
        ("arc", ";;;; ui.arc - pages", "ui.arc - pages"),
        ("eclipse", "%%% Fibonacci", "Fibonacci"),
        ("eclipse", "%%%%%%%%MODEL%%%%%%%%", "MODEL"),
        ("oz", "%% Section\n%%%%%%%%%%%%%%%%%%%%", "Section"),
        (
            "visual_basic",
            "''' <summary>\n''' Saves a file.\n''' </summary>",
            "<summary>\nSaves a file.\n</summary>",
        ),
        ("netlogo", ";=== First heading\n;=== Second heading", "First heading\nSecond heading"),
        ("runoff", "! Text Segment\t\t   !", "Text Segment"),
        ("xtend", "// ===> Attribute name", "===> Attribute name"),
        ("mql4", "//===Settings====================//", "Settings"),
        (
            "tcl",
            "#%Module -*- tcl -*-\n##\n## module description\n##",
            "%Module -*- tcl -*-\n\nmodule description",
        ),
        ("f#", "(****    SERIALIZE TO THIS FILE    ****)", "SERIALIZE TO THIS FILE"),
        (
            "gams",
            "*Author: Example*\n*Affiliation: Example Org*",
            "Author: Example\nAffiliation: Example Org",
        ),
        (
            "gdscript",
            "# UI.gd - View\n#\N{NO-BREAK SPACE}information about the UI",
            "UI.gd - View\ninformation about the UI",
        ),
        (
            "dns_zone",
            ";;;==============\n;;;  JazzScheme\n;;;==============\n;;;\n;;;; Zone\n;;;",
            "JazzScheme\n==============\n\nZone",
        ),
        ("aspnet", "<!-- ************************ !-->", ""),
        (
            "fortran_free_form",
            "!============ limiter ============80\n!\n! Takes gradients\n!============80",
            "limiter\n\nTakes gradients",
        ),
        (
            "java",
            "//----------  Solution 1 ----------//\n// brute force",
            "Solution 1\nbrute force",
        ),
        (
            "asl",
            "/*++\n\n  Copyright Example\n\n  Module Name:\n\n    Demo.ASL\n\n--*/",
            "Copyright Example\n\nModule Name:\n\n  Demo.ASL",
        ),
        (
            "ncl",
            (
                ";====================;\n"
                ";  title.ncl\n"
                ";====================;\n"
                "; body\n"
                ";====================;"
            ),
            " title.ncl\n====================;\nbody",
        ),
        (
            "yasnippet",
            "# -*- mode: snippet -*-\n# name: main\n# --\n#include <iostream>",
            "-*- mode: snippet -*-\nname: main\n--\n#include <iostream>",
        ),
        (
            "dm",
            '//var/character/char = mob\n\t//if(char)\n\t//\treturn "busy"',
            'var/character/char = mob\nif(char)\n\treturn "busy"',
        ),
        (
            "makefile",
            "#********License********\n#\n# Copyright Example\n#***************",
            "License\n\nCopyright Example",
        ),
    ],
)
def test_reviewed_judge_layouts_restore_only_scaffolding(
    language: str,
    raw_comment: str,
    expected: str,
) -> None:
    assert sanitize_comment(language, raw_comment) == expected


def test_cuda_line_footer_is_deleted_without_losing_the_preceding_blank_comment() -> None:
    raw_comment = (
        "//===------------ header ------------===//\n"
        "//\n"
        "// body\n"
        "//\n"
        "//===------------------------------===//"
    )

    assert sanitize_comment("cuda", raw_comment) == (
        "===------------ header ------------===\n\nbody\n"
    )


def test_cuda_doc_star_gutter_does_not_shift_an_unguttered_continuation() -> None:
    raw_comment = "/*! \\file demo.cu\n *  \\brief Kernel definitions.\n           Continuation. */"

    assert sanitize_comment("cuda", raw_comment) == (
        "\\file demo.cu\n\\brief Kernel definitions.\n          Continuation."
    )


def test_repeated_arc_marker_without_content_remains_an_empty_ruler() -> None:
    assert sanitize_comment("arc", ";" * 46) == ""


def test_long_percent_rulers_are_not_partially_consumed_as_two_percent_docs() -> None:
    assert sanitize_comment("eclipse", "%" * 46) == ""


def test_four_apostrophes_do_not_trigger_the_exact_triple_apostrophe_doc_rule() -> None:
    assert sanitize_comment("visual_basic", "'''' heading") == "''' heading"


def test_netlogo_consumes_the_complete_equals_prefix_only_when_it_has_content() -> None:
    assert sanitize_comment("netlogo", ";====== Heading") == "Heading"


def test_runoff_content_bang_is_not_treated_as_a_fixed_width_gutter() -> None:
    assert sanitize_comment("runoff", "! Wow !") == "Wow !"


def test_lasso_preserves_internal_section_rulers_after_removing_box_gutters() -> None:
    raw_comment = (
        "/*####################\n"
        "# Application: dCore #\n"
        "######################\n"
        "# License LGPL       #\n"
        "######################\n"
        "# SOURCE BELOW       #\n"
        "####################*/"
    )

    cleaned = sanitize_comment("lasso", raw_comment)

    assert "####################" in cleaned
    assert "License LGPL" in cleaned
