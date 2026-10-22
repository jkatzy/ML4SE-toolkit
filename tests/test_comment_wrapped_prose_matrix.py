"""Wrapped prose through every language's comment wrappers.

Each language key gets the line and block wrappers its generated cleaning
fixture already proves (a one-line case that cleans to its bare payload). The
test wraps a prose paragraph in those wrappers in many layouts, varying how
much scaffolding there is to strip: the number of lines (each with its own
marker), padding after the marker, shared indentation, gutters, rulers, blank
comment lines, and text aligned under a block opener. Cleaning must return
exactly the wrapped lines, and ``unwrap_comment`` must turn them back into the
paragraph.

``tests/fixtures/comment_cleaning_wrapped_prose_known_gaps.json`` lists
reviewed language conventions that clean a layout differently on purpose, and
layouts the sanitizer does not clean yet. The gap list may only shrink: an
entry that starts passing fails the test until removed.
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
_EXCEPTIONS = json.loads(KNOWN_GAPS_PATH.read_text())
KNOWN_GAPS = {
    (gap["language"], gap["wrapper"], gap["layout"]): gap["reason"] for gap in _EXCEPTIONS["gaps"]
}
# Conventions whose reviewed output flushes continuation lines left instead of
# keeping their alignment under the opener.
FLUSH_LEFT = {
    (entry["language"], entry["wrapper"], entry["closer"], entry["layout"])
    for entry in _EXCEPTIONS["flush_left_conventions"]
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
            if (language, opener, closer, layout) in FLUSH_LEFT:
                cleaned_lines = [line.lstrip(" ") for line in cleaned_lines]
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
    for language, opener, *_ in [*KNOWN_GAPS, *FLUSH_LEFT]:
        assert opener in {wrapper[1] for wrapper in WRAPPERS[language]}
    assert {language for language, _ in HEADER_GAPS} <= set(WRAPPERS)


@pytest.mark.parametrize(
    ("language", "raw", "expected"),
    [
        ("dune", "; ========\n; first line\n; second line\n; ========", "first line\nsecond line"),
        ("mermaid", "%% --------\n%% first line\n%% --------", "first line"),
        ("survex_data", "! ********\n! first line\n! second line", "first line\nsecond line"),
        ("linear_programming", "\\ ====\n\\ first line\n\\ ====", "first line"),
        ("abap", "*** first line\n***\n*** second line", "first line\n\nsecond line"),
        (
            "classic_asp",
            "<% Rem first line\n<% Rem\n<% Rem second line",
            "first line\n\nsecond line",
        ),
    ],
)
def test_layouts_the_matrix_found(language, raw, expected):
    assert CommentSanitizer(language).sanitize(raw) == expected


BOXED_TITLE = (
    "/********************************\n"
    " *     CACHE INITIALIZATION     *\n"
    " ********************************\n"
    " * Initializes the application cache by loading\n"
    " * frequently accessed data into memory.\n"
    " *\n"
    " * Existing cache entries are preserved unless\n"
    " * they have expired or become invalid.\n"
    " */"
)


@pytest.mark.parametrize(
    "raw",
    [
        BOXED_TITLE,
        BOXED_TITLE.replace(
            " *     CACHE INITIALIZATION     *\n",
            " *     CACHE                    *\n *     INITIALIZATION           *\n",
        ),
    ],
)
def test_boxed_title_rows_lose_their_frame(raw):
    title = "CACHE INITIALIZATION" if raw == BOXED_TITLE else "CACHE\nINITIALIZATION"
    body = (
        "Initializes the application cache by loading\n"
        "frequently accessed data into memory.\n\n"
        "Existing cache entries are preserved unless\n"
        "they have expired or become invalid."
    )
    assert CommentSanitizer("java").sanitize(raw) == f"{title}\n{body}"


# Decorative headers around the same comment: a title set off by rulers, boxed
# in a frame, or drawn with the line marker itself. Cleaning keeps the title
# rows and the body and drops every ruler and frame.
HEADER_TITLE = "CACHE INITIALIZATION"
HEADER_BODY = (
    "Initializes the application cache by loading",
    "frequently accessed data into memory.",
    "",
    "Existing cache entries are preserved unless",
    "they have expired or become invalid.",
)
HEADER_WIDTH = 52
HEADER_GAPS = {
    (gap["language"], shape) for gap in _EXCEPTIONS["header_gaps"] for shape in gap["shapes"]
}


def _boxed(char, text, lead=""):
    return f"{lead}{char}{text.center(HEADER_WIDTH - 2)}{char}"


def _block_headers(opener, closer):
    width, title, body = HEADER_WIDTH, HEADER_TITLE, HEADER_BODY
    for char in sorted(set("*=-#") - {opener[-1]}):
        rule = char * width
        rows = [_boxed(char, " " + line.ljust(width - 3)) for line in body]
        yield f"inline-title {char}", [opener, f"{char * 6} {title} {char * 6}", *body, closer]
        yield f"title-between-rulers {char}", [opener, rule, title, rule, *body, closer]
        yield f"full-box {char}", [opener + rule, _boxed(char, title), *rows, rule + closer]
    if opener.endswith("*"):
        rule = " " + "*" * width
        gutter = [f" * {line}".rstrip() for line in body]
        for name, titles in (("title-box", [title]), ("title-box-two-rows", title.split())):
            framed = [_boxed("*", row, " ") for row in titles]
            yield name, [opener + rule[1:], *framed, rule, *gutter, " " + closer]


def _line_headers(opener, closer):
    width, title, body = HEADER_WIDTH, HEADER_TITLE, HEADER_BODY
    tail = f" {closer}" if closer else ""

    def line(text):
        return f"{opener} {text}{tail}" if text else f"{opener}{tail}"

    marker = opener[-1]
    for char in sorted(set("*=-#") | ({marker} & set("/;%!"))):
        rule = line(char * width)
        boxed = line(_boxed(char, title))
        rows = [line(f"{char} {text.ljust(width - 4)} {char}") for text in body]
        inline = line(f"{char * 6} {title} {char * 6}")
        yield f"line-inline-title {char}", [inline, *map(line, body)]
        yield f"line-title-between-rulers {char}", [rule, line(title), rule, *map(line, body)]
        yield f"line-title-box {char}", [rule, boxed, rule, *map(line, body)]
        yield f"line-full-box {char}", [rule, boxed, rule, *rows, rule]
    if closer or marker not in "*=-#/;%!":
        return
    # The marker draws the box's left edge: ``#####`` / ``#  TITLE  #``.
    rule = opener + marker * width
    banner = f"{opener}{title.center(width)}{marker}"
    rows = [f"{opener} {text.ljust(width - 1)}{marker}" for text in body]
    yield "line-banner", [rule, banner, rule, *map(line, body)]
    yield "line-banner-box", [rule, banner, rule, *rows, rule]


@pytest.mark.parametrize("language", sorted(WRAPPERS))
def test_decorative_headers_clean_to_title_and_body(language):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sanitizer = CommentSanitizer(language)
    body = [line for line in HEADER_BODY if line]
    joined = " ".join(HEADER_BODY[:2])
    failures = []
    gap_hits = set()
    for kind, opener, closer in WRAPPERS[language]:
        if kind == "line" and len(closer) > 3:
            continue
        shapes = _line_headers if kind == "line" else _block_headers
        for shape, rows in shapes(opener, closer):
            cleaned = sanitizer.sanitize("\n".join(rows))
            filled = [line for line in cleaned.split("\n") if line.strip()]
            titles = HEADER_TITLE.split() if "two-rows" in shape else [HEADER_TITLE]
            unwrapped = unwrap_comment(cleaned).split("\n")
            if filled == [*titles, *body] and titles[-1] in unwrapped and joined in unwrapped:
                continue
            if (language, shape) in HEADER_GAPS:
                gap_hits.add((language, shape))
            else:
                failures.append(f"{shape} {opener!r}: {cleaned!r}")
    fixed = {gap for gap in HEADER_GAPS if gap[0] == language} - gap_hits
    failures += [f"header gap now passes, remove it from the list: {gap}" for gap in sorted(fixed)]
    assert not failures, "\n".join(failures[:20])
