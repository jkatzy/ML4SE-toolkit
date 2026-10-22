"""Wrapped prose through every language's comment wrappers.

Each language key gets the line and block wrappers its generated cleaning
fixture already proves (a one-line case that cleans to its bare payload). The
test wraps a prose paragraph in those wrappers in many layouts, varying how
much scaffolding there is to strip: the number of lines (each with its own
marker), padding after the marker, shared indentation, gutters, rulers, blank
comment lines, and text aligned under a block opener. Cleaning must return
exactly the wrapped lines, and ``unwrap_comment`` must turn them back into the
paragraph.

Layouts the sanitizer does not clean yet are frozen in
``tests/fixtures/comment_cleaning_wrapped_prose_known_gaps.json``. That list
may only shrink: an entry that starts passing fails the test until removed.
"""

import json
import textwrap
import warnings
from pathlib import Path

import pytest

from ml4setk import CommentSanitizer, unwrap_comment

pytestmark = pytest.mark.unit

FIXTURES = Path(__file__).resolve().parent / "fixtures"
KNOWN_GAPS_PATH = FIXTURES / "comment_cleaning_wrapped_prose_known_gaps.json"
WORDS = (
    "tokens are stripped from every wrapped line of this comment so the cleaned "
    "text reads as one paragraph again, and the payload keeps its words, commas "
    "and order while the scaffolding around it goes away for good"
).split()
LINE_KINDS = frozenset({"line", "sanitizer_line_wrapper"})
BLOCK_KINDS = frozenset({"block", "sanitizer_block_wrapper", "nested"})


def _proven_wrapper(case):
    raw, marker = case["raw_comment"], case["payload_marker"]
    if case["expected_cleaned"] != marker or raw.count(marker) != 1 or "\n" in raw:
        return None
    if case["kind"] in LINE_KINDS:
        kind = "line"
    elif case["kind"] in BLOCK_KINDS:
        kind = "block"
    else:
        return None
    before, after = raw.split(marker)
    return kind, before.rstrip(" \t"), after.lstrip(" \t")


def _wrappers_by_language():
    wrappers = {}
    for path in sorted((FIXTURES / "comment_cleaning").glob("*.json")):
        family = json.loads(path.read_text())
        if family["sanitizer_mode"] != "wrapped":
            continue
        proven = sorted({w for w in map(_proven_wrapper, family["cases"]) if w is not None})
        for language in family["language_keys"]:
            wrappers[language] = proven
    return wrappers


WRAPPERS = _wrappers_by_language()
KNOWN_GAPS = {
    (gap["language"], gap["wrapper"], gap["layout"]): gap["reason"]
    for gap in json.loads(KNOWN_GAPS_PATH.read_text())["gaps"]
}


def _paragraph(width, line_count):
    words = (WORDS * 4)[: max(4, line_count * width // 6)]
    return textwrap.wrap(" ".join(words), width)


def _line_layouts(opener, closer):
    tail = f" {closer}" if closer else ""
    min_pad = " " if opener[-1:].isalnum() else ""
    for width in (60, 80):
        for line_count in (1, 3, 6):
            lines = _paragraph(width, line_count)
            for pad in sorted({min_pad, " ", "  "}):
                for indent in ("", "    "):
                    raw = "\n".join(f"{indent}{opener}{pad}{line}{tail}" for line in lines)
                    yield "line", raw, lines, lines
    lines = _paragraph(72, 3)
    body = [f"{opener} {line}{tail}" for line in lines]
    for char in "=-*#":
        for length in (8, 40):
            ruler = f"{opener} {char * length}{tail}"
            yield "line-ruler", "\n".join([ruler, *body, ruler]), lines, lines
    blank = f"{opener}{tail}"
    two = [*lines, "", *lines]
    yield "line-two-paragraphs", "\n".join([*body, blank, *body]), two, two


def _block_layouts(opener, closer):
    open_pad = " " if opener[-1:].isalnum() else ""
    close_pad = " " if closer[:1].isalnum() else ""
    for width in (60, 80):
        for line_count in (1, 3, 6):
            lines = _paragraph(width, line_count)
            if len(lines) == 1:
                raw = f"{opener}{open_pad or ' '}{lines[0]}{close_pad or ' '}{closer}"
                yield "block-inline", raw, lines, lines
            for indent in ("", "  ", "    "):
                body = "\n".join(f"{indent}{line}" for line in lines)
                yield "block-own-lines", f"{opener}\n{body}\n{closer}", lines, lines
            if opener.endswith("*"):
                body = "\n".join(f" * {line}" for line in lines)
                yield "block-gutter", f"{opener}\n{body}\n {closer}", lines, lines
    lines = _paragraph(72, 3)
    two = [*lines, "", *lines]
    yield "block-two-paragraphs", "\n".join([opener, *two, closer]), two, two
    # Cleaning keeps continuation alignment under the opener text; unwrapping
    # joins it.
    align = " " * (len(opener) + 1)
    aligned = [lines[0], *(align + line for line in lines[1:])]
    raw = f"{opener} " + "\n".join(aligned) + f" {closer}"
    yield "block-aligned", raw, aligned, lines


def _layouts(kind, opener, closer):
    if kind == "line":
        return _line_layouts(opener, closer)
    return _block_layouts(opener, closer)


def _unwrapped(lines):
    return "\n\n".join(" ".join(p.split("\n")) for p in "\n".join(lines).split("\n\n"))


@pytest.mark.parametrize("language", sorted(WRAPPERS))
def test_wrapped_prose_cleans_and_unwraps(language):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sanitizer = CommentSanitizer(language)
    failures = []
    gap_hits = set()
    for kind, opener, closer in WRAPPERS[language]:
        for layout, raw, cleaned_lines, unwrapped_lines in _layouts(kind, opener, closer):
            cleaned = sanitizer.sanitize(raw)
            gap = (language, opener, layout)
            if cleaned != "\n".join(cleaned_lines):
                if gap in KNOWN_GAPS:
                    gap_hits.add(gap)
                else:
                    failures.append(f"clean {layout} {opener!r}: {raw!r} -> {cleaned!r}")
                continue
            unwrapped = unwrap_comment(cleaned)
            if unwrapped != _unwrapped(unwrapped_lines):
                failures.append(f"unwrap {layout} {opener!r}: {cleaned!r} -> {unwrapped!r}")
    fixed = {gap for gap in KNOWN_GAPS if gap[0] == language} - gap_hits
    failures += [f"known gap now passes, remove it from the list: {gap}" for gap in sorted(fixed)]
    assert not failures, "\n".join(failures[:20])


def test_known_gaps_name_tested_layouts():
    for language, opener, _layout in KNOWN_GAPS:
        assert opener in {wrapper[1] for wrapper in WRAPPERS[language]}
