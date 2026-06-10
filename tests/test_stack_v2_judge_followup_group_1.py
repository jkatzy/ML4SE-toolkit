import pytest

from ml4setk import CommentQuery, CommentSanitizer

pytestmark = pytest.mark.unit


def test_apl_cr_only_source_does_not_absorb_code_into_comment():
    source = (
        "    function header\r"
        "[1]   ⍝first comment\r"
        "[2]   executable code\r"
        "[3]   ⍝second comment\r"
        "[4]   more executable code\r"
    )

    matches = CommentQuery("apl").parse(source)

    assert [match.match for match in matches] == [
        "⍝first comment",
        "⍝second comment",
    ]


@pytest.mark.parametrize(
    ("raw_comment", "expected_cleaned"),
    [
        pytest.param(
            (
                "<%--\t--%>\n"
                '<%--    <link rel="stylesheet" '
                "href=\"${resource(dir:'css/dinerotaxi',file:'modal.css')}\" />--%>\n"
                '<%--    <link rel="stylesheet" '
                "href=\"${resource(dir:'css',file:'jquery-ui.tbo.css')}\" />--%>\n"
                "<%--   --%>"
            ),
            (
                '<link rel="stylesheet" '
                "href=\"${resource(dir:'css/dinerotaxi',file:'modal.css')}\" />\n"
                '<link rel="stylesheet" '
                "href=\"${resource(dir:'css',file:'jquery-ui.tbo.css')}\" />"
            ),
            id="grouped-wrapper-lines",
        ),
        pytest.param(
            (
                '<%--<div class="fieldcontain ${hasErrors(bean: categoryInstance, '
                "field: 'code', 'error')} \">--%>"
            ),
            (
                '<div class="fieldcontain ${hasErrors(bean: categoryInstance, '
                "field: 'code', 'error')} \">"
            ),
            id="inline-wrapper",
        ),
        pytest.param(
            (
                "<%--\n"
                "  Created by IntelliJ IDEA.\n"
                "  User: jleo\n"
                "  Date: 12-8-12\n"
                "  Time: 下午1:01\n"
                "  To change this template use File | Settings | File Templates.\n"
                "--%>"
            ),
            (
                "Created by IntelliJ IDEA.\n"
                "User: jleo\n"
                "Date: 12-8-12\n"
                "Time: 下午1:01\n"
                "To change this template use File | Settings | File Templates."
            ),
            id="multiline-intellij-jleo",
        ),
        pytest.param(
            (
                "<%--\n"
                "  Created by IntelliJ IDEA.\n"
                "  User: swestfall\n"
                "  Date: 6/9/11\n"
                "  Time: 5:38 PM\n"
                "  To change this template use File | Settings | File Templates.\n"
                "--%>"
            ),
            (
                "Created by IntelliJ IDEA.\n"
                "User: swestfall\n"
                "Date: 6/9/11\n"
                "Time: 5:38 PM\n"
                "To change this template use File | Settings | File Templates."
            ),
            id="multiline-intellij-swestfall",
        ),
        pytest.param(
            (
                "<%--\n"
                "  Created by IntelliJ IDEA.\n"
                "  User: guo\n"
                "  Date: 13-1-18\n"
                "  Time: PM4:58\n"
                "  To change this template use File | Settings | File Templates.\n"
                "--%>"
            ),
            (
                "Created by IntelliJ IDEA.\n"
                "User: guo\n"
                "Date: 13-1-18\n"
                "Time: PM4:58\n"
                "To change this template use File | Settings | File Templates."
            ),
            id="multiline-intellij-guo",
        ),
        pytest.param(
            (
                "<%--\n"
                "  Created by IntelliJ IDEA.\n"
                "  User: vaibhav\n"
                "  Date: 5/30/19\n"
                "  Time: 2:40 AM\n"
                "--%>"
            ),
            ("Created by IntelliJ IDEA.\nUser: vaibhav\nDate: 5/30/19\nTime: 2:40 AM"),
            id="multiline-intellij-vaibhav",
        ),
        pytest.param(
            (
                "<%--\n"
                "  Created by IntelliJ IDEA.\n"
                "  User: kamesh\n"
                "  Date: 17/3/18\n"
                "  Time: 3:55 PM\n"
                "--%>"
            ),
            ("Created by IntelliJ IDEA.\nUser: kamesh\nDate: 17/3/18\nTime: 3:55 PM"),
            id="multiline-intellij-kamesh",
        ),
        pytest.param(
            (
                "<%--\n"
                "  Created by IntelliJ IDEA.\n"
                "  User: byznr\n"
                "  Date: 18.08.2020\n"
                "  Time: 10:43\n"
                "--%>"
            ),
            ("Created by IntelliJ IDEA.\nUser: byznr\nDate: 18.08.2020\nTime: 10:43"),
            id="multiline-intellij-byznr",
        ),
        pytest.param(
            (
                "<%--\n"
                " Copyright 2010 DTO Labs, Inc. (http://dtolabs.com)\n"
                "\n"
                ' Licensed under the Apache License, Version 2.0 (the "License");\n'
                " you may not use this file except in compliance with the License.\n"
                " You may obtain a copy of the License at\n"
                "\n"
                "      http://www.apache.org/licenses/LICENSE-2.0\n"
                "\n"
                " Unless required by applicable law or agreed to in writing, software\n"
                ' distributed under the License is distributed on an "AS IS" BASIS,\n'
                " WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
                " See the License for the specific language governing permissions and\n"
                " limitations under the License.\n"
                "\n"
                " --%>"
            ),
            (
                "Copyright 2010 DTO Labs, Inc. (http://dtolabs.com)\n"
                "\n"
                'Licensed under the Apache License, Version 2.0 (the "License");\n'
                "you may not use this file except in compliance with the License.\n"
                "You may obtain a copy of the License at\n"
                "\n"
                "     http://www.apache.org/licenses/LICENSE-2.0\n"
                "\n"
                "Unless required by applicable law or agreed to in writing, software\n"
                'distributed under the License is distributed on an "AS IS" BASIS,\n'
                "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
                "See the License for the specific language governing permissions and\n"
                "limitations under the License."
            ),
            id="multiline-license",
        ),
        pytest.param(
            (
                "<%--\n"
                "  Created by IntelliJ IDEA.\n"
                "  User: josh\n"
                "  Date: 7/12/13\n"
                "  Time: 9:33 PM\n"
                "  To change this template use File | Settings | File Templates.\n"
                "--%>"
            ),
            (
                "Created by IntelliJ IDEA.\n"
                "User: josh\n"
                "Date: 7/12/13\n"
                "Time: 9:33 PM\n"
                "To change this template use File | Settings | File Templates."
            ),
            id="multiline-intellij-josh",
        ),
        pytest.param(
            (
                "<%--\r\n"
                "  Created by IntelliJ IDEA.\r\n"
                "  User: spandey\r\n"
                "  Date: 2/3/15\r\n"
                "  Time: 12:01 PM\r\n"
                "  To change this template use File | Settings | File Templates.\r\n"
                "--%>"
            ),
            (
                "Created by IntelliJ IDEA.\n"
                "User: spandey\n"
                "Date: 2/3/15\n"
                "Time: 12:01 PM\n"
                "To change this template use File | Settings | File Templates."
            ),
            id="multiline-intellij-spandey-crlf",
        ),
    ],
)
def test_groovy_server_pages_sanitizer_strips_comment_wrappers(raw_comment, expected_cleaned):
    assert CommentSanitizer("groovy_server_pages").sanitize(raw_comment) == expected_cleaned


def test_genero_delimiter_only_hash_ruler_sanitizes_to_empty():
    raw_comment = "############################################################################"

    assert CommentSanitizer("genero").sanitize(raw_comment) == ""


def test_dm_line_comment_strips_trailing_decorative_slash_padding():
    raw_comment = (
        "/////////////////////////////////////////////////////////////"
        "newer ai/////////////////////////////"
    )

    assert CommentSanitizer("dm").sanitize(raw_comment) == "newer ai"
