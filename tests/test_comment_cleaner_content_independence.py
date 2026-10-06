"""Comment cleaning must depend on comment layout, not on the words inside it.

Every reviewed cleaning fixture is re-run with its content words replaced by
same-length, same-case ROT13 words. A layout-driven cleaner produces the same
output with the same substitution applied. Cases that currently clean
correctly only because of specific prose (for example a rule keyed to
"Apache License") are frozen in ``comment_cleaning_content_dependent_cases.json``
so the list can only shrink: new content-keyed behavior fails here, and a case
that becomes content-independent must be removed from the list.
"""

from __future__ import annotations

import codecs
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit

FIXTURES = Path(__file__).parent / "fixtures"
KNOWN_CONTENT_DEPENDENT_PATH = FIXTURES / "comment_cleaning_content_dependent_cases.json"
_WORD = re.compile(r"[A-Za-z]{3,}")


def _iter_reviewed_cases():
    paths = sorted(
        [
            *FIXTURES.glob("comment_cleaning_regressions/*.json"),
            *FIXTURES.glob("comment_cleaning_repaired_failures/*.json"),
            *FIXTURES.glob("comment_cleaning_*.json"),
        ]
    )
    for path in paths:
        if path == KNOWN_CONTENT_DEPENDENT_PATH:
            continue
        yield from _walk(json.loads(path.read_text(encoding="utf-8")))


def _walk(node):
    if isinstance(node, dict):
        raw = node.get("raw_comment")
        expected = node.get("expected_cleaned")
        if isinstance(raw, str) and isinstance(expected, str) and node.get("language"):
            yield node.get("case_id") or node.get("id"), node["language"], raw, expected
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk(value)


def _substitute_content_words(raw: str, expected: str) -> tuple[str, str] | None:
    """ROT13 the words that occur only as content, in both raw and expected text.

    A word is rotated only when it occurs equally often in the raw comment and
    the cleaned output, so alphabetic delimiters such as ``REM`` or ``=begin``
    are never changed.
    """

    raw_words = Counter(_WORD.findall(raw))
    expected_words = Counter(_WORD.findall(expected))
    content_words = {word for word in expected_words if raw_words[word] == expected_words[word]}
    if not content_words:
        return None
    pattern = re.compile(
        r"(?<![A-Za-z])("
        + "|".join(sorted(map(re.escape, content_words), key=len, reverse=True))
        + r")(?![A-Za-z])"
    )

    def rotate(match):
        return codecs.encode(match.group(0), "rot13")

    return pattern.sub(rotate, raw), pattern.sub(rotate, expected)


def _case_key(case_id: str, raw: str) -> str:
    return f"{case_id}:{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]}"


def _content_dependent_case_keys() -> set[str]:
    dependent = set()
    for case_id, language, raw, expected in _iter_reviewed_cases():
        substituted = _substitute_content_words(raw, expected)
        if substituted is None:
            continue
        substituted_raw, substituted_expected = substituted
        if sanitize_comment(language, substituted_raw) != substituted_expected:
            dependent.add(_case_key(case_id, raw))
    return dependent


def _known_content_dependent_case_keys() -> set[str]:
    data = json.loads(KNOWN_CONTENT_DEPENDENT_PATH.read_text(encoding="utf-8"))
    return {entry["key"] for entry in data["cases"]}


@pytest.fixture(scope="module")
def content_dependent_case_keys():
    return _content_dependent_case_keys()


def test_reviewed_fixture_set_is_large_enough_to_be_meaningful():
    assert sum(1 for _ in _iter_reviewed_cases()) > 1000


def test_no_new_content_dependent_cleaning(content_dependent_case_keys):
    new_cases = sorted(content_dependent_case_keys - _known_content_dependent_case_keys())

    assert new_cases == [], (
        "These reviewed cases clean correctly only with their original words. "
        "Make the rule layout-driven instead of keyed to prose."
    )


def test_content_dependent_list_only_shrinks(content_dependent_case_keys):
    resolved_cases = sorted(_known_content_dependent_case_keys() - content_dependent_case_keys)

    assert resolved_cases == [], (
        "These cases are now content-independent; remove them from "
        f"{KNOWN_CONTENT_DEPENDENT_PATH.name}."
    )


def test_substitution_keeps_alphabetic_delimiters():
    assert _substitute_content_words("REM note", "note") == ("REM abgr", "abgr")
    assert _substitute_content_words("=begin\nhello\n=end", "hello") == (
        "=begin\nuryyb\n=end",
        "uryyb",
    )
