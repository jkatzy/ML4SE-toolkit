import json
import re
from pathlib import Path

import pytest

from ml4setk import sanitize_comment, unwrap_comment

pytestmark = pytest.mark.unit

FIXTURES = Path(__file__).resolve().parent / "fixtures"
WRAPPED = (
    "This module defines a generic non-empty data structure, which adds an\n"
    "additional element to any container type, and keeps the original one."
)
JOINED = (
    "This module defines a generic non-empty data structure, which adds an "
    "additional element to any container type, and keeps the original one."
)


def _cleaned_outputs():
    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("expected_cleaned"), str):
                yield node["expected_cleaned"]
            for value in node.values():
                yield from walk(value)
        elif isinstance(node, list):
            for value in node:
                yield from walk(value)

    outputs = set()
    for path in sorted(FIXTURES.glob("comment_cleaning*/*.json")):
        outputs.update(text for text in walk(json.loads(path.read_text())) if "\n" in text)
    return sorted(outputs)


def test_joins_wrapped_prose_and_keeps_paragraph_breaks():
    assert unwrap_comment(WRAPPED + "\n\n" + WRAPPED) == JOINED + "\n\n" + JOINED


def test_works_on_sanitized_comments():
    raw = "/*\n * " + WRAPPED.replace("\n", "\n * ") + "\n */"
    assert unwrap_comment(sanitize_comment("java", raw)) == JOINED


def test_joins_hyphenated_break_without_a_space():
    text = "The query groups the comment lines that it finds into one well-\nknown shape."
    assert unwrap_comment(text) == (
        "The query groups the comment lines that it finds into one well-known shape."
    )


@pytest.mark.parametrize(
    "text",
    [
        "Short header line\nAuthor line\nDate line",
        "Copyright 2015 Example Corporation and the project contributors.\nAll rights reserved.",
        "Make file for the release build of the project on every platform\n"
        "Author : J. Doe (doe@example.com)\nDate : 3 October 2009",
        "The supported options for this command line tool are listed here\n- verbose\n- quiet",
        "Returns the value that is stored under the key in the given map\n@param key the key",
        "Call the function with the argument that you want to convert like\n    convert(value)",
        "Each of these rows lists one header of the table and one value too\n| a | b |",
        "This line ends a sentence in the middle of a long paragraph text.\nThe next one.",
        "Include some common definitions shared by all of the shader files\n----------",
        "Write the configuration file that the server reads when it starts {\n  key = value\n}",
    ],
)
def test_keeps_deliberate_breaks(text):
    assert unwrap_comment(text) == text


def test_joins_list_item_continuations_but_not_the_next_item():
    text = (
        "- change the name of the key in serializedEditor, in encoders.ml\n"
        "  and decoders.ml, otherwise the old setting will be used again.\n"
        "- edit the text and links below"
    )
    assert unwrap_comment(text) == (
        "- change the name of the key in serializedEditor, in encoders.ml "
        "and decoders.ml, otherwise the old setting will be used again.\n"
        "- edit the text and links below"
    )


def test_leaves_fenced_blocks_alone():
    fence = "```\nfirst code line that is long enough to look like wrapped prose\nsecond\n```"
    assert unwrap_comment(WRAPPED + "\n" + fence) == JOINED + "\n" + fence


def test_leaves_narrow_paragraphs_alone():
    text = "Blocks are evaluated in order\nfrom the first expression"
    assert unwrap_comment(text) == text
    joined = "Blocks are evaluated in order from the first expression"
    assert unwrap_comment(text, min_width=20) == joined


def test_only_whitespace_changes_on_the_cleaning_corpus():
    outputs = _cleaned_outputs()
    assert len(outputs) > 500
    changed = 0
    for text in outputs:
        unwrapped = unwrap_comment(text)
        assert re.sub(r"\s", "", unwrapped) == re.sub(r"\s", "", text)
        assert unwrapped.count("\n") <= text.count("\n")
        changed += unwrapped != text
    assert changed > 100
