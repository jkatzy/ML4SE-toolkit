import pytest

from ml4setk import CommentSanitizer

pytestmark = pytest.mark.unit


def test_abap_generated_report_header_removes_decorative_frame():
    raw_comment = (
        "*&---------------------------------------------------------------------*\n"
        "*& Report z_ccm_vbtyp_06\n"
        "*&---------------------------------------------------------------------*\n"
        "*&\n"
        "*&---------------------------------------------------------------------*"
    )

    assert CommentSanitizer("abap").sanitize(raw_comment) == "Report z_ccm_vbtyp_06"


def test_lua_long_comment_removes_symmetric_closing_decoration():
    raw_comment = (
        "--[[\n"
        "    by LYQ(Virose / MOUZU)\n"
        "    https://github.com/MOUZU/BigWigs\n"
        "    \n"
        "    This is a small plugin which is inspried by ThaddiusArrows and how "
        "Sulfuras of Mesmerize (Warsong/Feenix) used it.\n"
        "    I wanted to convert his idea in a more dynamic, flexible and easy "
        "to use plugin.\n"
        "\n"
        "    At the current state it is built to only display one Icon at a time, "
        "at the moment I can not think of\n"
        "    a situation where it would be needed to display more than one.\n"
        "--]]"
    )
    expected = (
        "by LYQ(Virose / MOUZU)\n"
        "https://github.com/MOUZU/BigWigs\n"
        "\n"
        "This is a small plugin which is inspried by ThaddiusArrows and how "
        "Sulfuras of Mesmerize (Warsong/Feenix) used it.\n"
        "I wanted to convert his idea in a more dynamic, flexible and easy "
        "to use plugin.\n"
        "\n"
        "At the current state it is built to only display one Icon at a time, "
        "at the moment I can not think of\n"
        "a situation where it would be needed to display more than one."
    )

    assert CommentSanitizer("lua").sanitize(raw_comment) == expected


def test_lua_long_comment_removes_closing_decoration_before_dedent():
    raw_comment = (
        "--[[\n"
        "\t© CloudSixteen.com do not share, re-distribute or modify\n"
        "\twithout permission of its author (kurozael@gmail.com).\n"
        "--]]"
    )
    expected = (
        "© CloudSixteen.com do not share, re-distribute or modify\n"
        "without permission of its author (kurozael@gmail.com)."
    )

    assert CommentSanitizer("lua").sanitize(raw_comment) == expected


def test_motoko_framed_line_comments_remove_trailing_gutters():
    raw_comment = (
        "//___________________________________________________________________________//\r\n"
        "  // Component of the ClaRa library, version: 1.0.0                        //\r\n"
        "  //                                                                           //\r\n"
        "  // Licensed by the DYNCAP research team under Modelica License 2.            //\r\n"
        "  // Copyright © 2013-2015, DYNCAP research team.                                   //\r\n"
        "  //___________________________________________________________________________//\r\n"
        "  // DYNCAP is a research project supported by the German Federal Ministry of  //\r\n"
        "  // Economics and Technology (FKZ 03ET2009).                                  //\r\n"
        "  // The DYNCAP research team consists of the following project partners:      //\r\n"
        "  // Institute of Energy Systems (Hamburg University of Technology),           //\r\n"
        "  // Institute of Thermo-Fluid Dynamics (Hamburg University of Technology),    //\r\n"
        "  // TLK-Thermo GmbH (Braunschweig, Germany),                                  //\r\n"
        "  // XRG Simulation GmbH (Hamburg, Germany).                                   //\r\n"
        "  //___________________________________________________________________________//\r"
    )
    expected = (
        "Component of the ClaRa library, version: 1.0.0\n"
        "\n"
        "Licensed by the DYNCAP research team under Modelica License 2.\n"
        "Copyright © 2013-2015, DYNCAP research team.\n"
        "___________________________________________________________________________\n"
        "DYNCAP is a research project supported by the German Federal Ministry of\n"
        "Economics and Technology (FKZ 03ET2009).\n"
        "The DYNCAP research team consists of the following project partners:\n"
        "Institute of Energy Systems (Hamburg University of Technology),\n"
        "Institute of Thermo-Fluid Dynamics (Hamburg University of Technology),\n"
        "TLK-Thermo GmbH (Braunschweig, Germany),\n"
        "XRG Simulation GmbH (Hamburg, Germany)."
    )

    assert CommentSanitizer("motoko").sanitize(raw_comment) == expected


def test_ring_hash_comment_removes_registered_opener():
    raw_comment = "#======================================================\r"

    assert CommentSanitizer("ring").sanitize(raw_comment) == "=" * 54
