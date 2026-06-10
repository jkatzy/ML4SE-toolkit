import pytest

from ml4setk import CommentSanitizer, QueryMatch

pytestmark = pytest.mark.unit


def _sanitize(language: str, raw_comment: str) -> str:
    return CommentSanitizer(language).sanitize(QueryMatch("", "", raw_comment))


def test_csharp_boxed_block_removes_decorative_borders_and_gutters():
    raw_comment = (
        "/**************************************************************************\n"
        " *                                                                        *\n"
        " *  Website:     https://github.com/florinleon/ActressMas                 *\n"
        " *  Description: Mechanism design using the ActressMas framework          *\n"
        " *  Copyright:   (c) 2018, Florin Leon                                    *\n"
        " *                                                                        *\n"
        " *  This program is free software; you can redistribute it and/or modify  *\n"
        " *  it under the terms of the GNU General Public License as published by  *\n"
        " *  the Free Software Foundation. This program is distributed in the      *\n"
        " *  hope that it will be useful, but WITHOUT ANY WARRANTY; without even   *\n"
        " *  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR   *\n"
        " *  PURPOSE. See the GNU General Public License for more details.         *\n"
        " *                                                                        *\n"
        " **************************************************************************/"
    )
    expected = (
        "Website:     https://github.com/florinleon/ActressMas\n"
        "Description: Mechanism design using the ActressMas framework\n"
        "Copyright:   (c) 2018, Florin Leon\n"
        "\n"
        "This program is free software; you can redistribute it and/or modify\n"
        "it under the terms of the GNU General Public License as published by\n"
        "the Free Software Foundation. This program is distributed in the\n"
        "hope that it will be useful, but WITHOUT ANY WARRANTY; without even\n"
        "the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR\n"
        "PURPOSE. See the GNU General Public License for more details."
    )

    assert _sanitize("c#", raw_comment) == expected


def test_hocon_license_block_strips_each_hash_prefix():
    raw_comment = (
        "# Copyright 2022 HM Revenue & Customs\n"
        "#\n"
        '# Licensed under the Apache License, Version 2.0 (the "License");\n'
        "# you may not use this file except in compliance with the License.\n"
        "# You may obtain a copy of the License at\n"
        "#\n"
        "#     http://www.apache.org/licenses/LICENSE-2.0\n"
        "#\n"
        "# Unless required by applicable law or agreed to in writing, software\n"
        '# distributed under the License is distributed on an "AS IS" BASIS,\n'
        "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
        "# See the License for the specific language governing permissions and\n"
        "# limitations under the License."
    )
    expected = (
        "Copyright 2022 HM Revenue & Customs\n"
        "\n"
        'Licensed under the Apache License, Version 2.0 (the "License");\n'
        "you may not use this file except in compliance with the License.\n"
        "You may obtain a copy of the License at\n"
        "\n"
        "    http://www.apache.org/licenses/LICENSE-2.0\n"
        "\n"
        "Unless required by applicable law or agreed to in writing, software\n"
        'distributed under the License is distributed on an "AS IS" BASIS,\n'
        "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
        "See the License for the specific language governing permissions and\n"
        "limitations under the License."
    )

    assert _sanitize("hocon", raw_comment) == expected


def test_hocon_grouped_lines_strip_each_hash_prefix():
    raw_comment = (
        "# ------------- resume or retrain options ------------------------------\n"
        "# dcp_0.5_our_sq_finetune_checkpoint17"
    )
    expected = (
        "------------- resume or retrain options ------------------------------\n"
        "dcp_0.5_our_sq_finetune_checkpoint17"
    )

    assert _sanitize("hocon", raw_comment) == expected


def test_hyphy_delimiter_only_separator_sanitizes_to_empty_text():
    raw_comment = "/*--------------------------------------------------------------------------*/"

    assert _sanitize("hyphy", raw_comment) == ""


def test_imagej_macro_line_strips_trailing_slash_gutter():
    raw_comment = "///======================MACRO=========================///"

    assert _sanitize("imagej_macro", raw_comment) == (
        "======================MACRO========================="
    )


def test_javascript_adjacent_block_comments_strip_each_wrapper():
    raw_comment = (
        "/* eslint-disable react/no-render-return-value */\n"
        "/* eslint-disable react/no-find-dom-node */"
    )
    expected = "eslint-disable react/no-render-return-value\neslint-disable react/no-find-dom-node"

    assert _sanitize("javascript", raw_comment) == expected


def test_php_adjacent_block_comments_strip_each_wrapper():
    raw_comment = "/* @var $this KategorieController */\n/* @var $model Category */"
    expected = "@var $this KategorieController\n@var $model Category"

    assert _sanitize("php", raw_comment) == expected


def test_restructuredtext_grouped_targets_strip_each_directive_prefix():
    raw_comment = (
        ".. _GH3164: https://github.com/pydata/pandas/issues/3164\n"
        ".. _GH2786: https://github.com/pydata/pandas/issues/2786"
    )
    expected = (
        "_GH3164: https://github.com/pydata/pandas/issues/3164\n"
        "_GH2786: https://github.com/pydata/pandas/issues/2786"
    )

    assert _sanitize("restructuredtext", raw_comment) == expected
