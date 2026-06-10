import pytest

from ml4setk import CommentQuery

pytestmark = pytest.mark.unit


def test_stack_v2_asciidoc_long_matching_delimiters_form_one_block_comment():
    delimiter = "/" * 79
    raw_comment = (
        f"{delimiter}\n"
        "\n"
        "    Copyright (c) 2020 Oracle and/or its affiliates.\n"
        "\n"
        "    Licensed under the Apache License, Version 2.0 (the \"License\");\n"
        "    you may not use this file except in compliance with the License.\n"
        "    You may obtain a copy of the License at\n"
        "\n"
        "        http://www.apache.org/licenses/LICENSE-2.0\n"
        "\n"
        "    Unless required by applicable law or agreed to in writing, software\n"
        "    distributed under the License is distributed on an \"AS IS\" BASIS,\n"
        "    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
        "    See the License for the specific language governing permissions and\n"
        "    limitations under the License.\n"
        "\n"
        f"{delimiter}"
    )
    source = f"{raw_comment}\n= Reactive Engine\n"

    assert [match.match for match in CommentQuery("asciidoc").parse(source)] == [
        raw_comment
    ]
