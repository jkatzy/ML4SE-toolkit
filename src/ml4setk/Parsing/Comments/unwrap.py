"""Join hard-wrapped comment prose back into one line per paragraph."""

from __future__ import annotations

import re

_LIST_ITEM = re.compile(r"[ \t]*(?:[-*+•]|\d+[.)]|[A-Za-z][.)])[ \t]+")
# Lines whose break carries meaning: tags (@param, :param, \brief), doctest
# and shell prompts, headings, tables, fences, markup, directives, URLs,
# key: value rows, and tab-separated columns.
_STRUCTURE = re.compile(
    r"[ \t]*(?:[@\\][A-Za-z]|:[A-Za-z]+[: ]|>>>|\$ |[#|<=/]|```|~~~|[A-Za-z][\w+.-]*://|www\."
    r"|[^\s:]{1,30}(?:[ \t][^\s:]+){0,3}[ \t]*(?:\.{2,}[ \t]*)?:(?:[ \t]|$)"
    r"|\S[^\t]*\t)"
)
_CODE_EDGE = re.compile(r"[;{}][ \t]*$|^[ \t]*[{}]")
# An indented call or assignment under a prose line is an example, not a
# continuation aligned under the opener.
_CODE_EXAMPLE = re.compile(r"[ \t]*(?:[\w.$]+\(.*\)\W*$|\S+[ \t]+[-+*/:!<>]?=[ \t])")
_SENTENCE_END = re.compile(r"[.!?:][\"')]?$")
_WORD = re.compile(r"\w")
_HYPHENATED = re.compile(r"\w-$")
_FENCES = ("```", "~~~")
_NARROW_WIDTH = 60


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _keeps_break(line: str) -> bool:
    return (
        _STRUCTURE.match(line) is not None
        or _CODE_EDGE.search(line) is not None
        or _WORD.search(line) is None
    )


def _unwrap_paragraph(lines: list[str], min_width: int) -> list[str]:
    # The longest line approximates the wrap column. A line ended early (below
    # 80% of it) is taken as a deliberate break rather than a wrap.
    width = max(len(line.rstrip()) for line in lines)
    if width < min_width:
        return lines
    # Short lines are as often a list of short entries as narrow prose, so a
    # narrow paragraph only joins a line that continues a sentence.
    narrow = width < _NARROW_WIDTH
    # Each output line is a list of pieces, so a long paragraph is joined once.
    out: list[list[str]] = []
    # Indents a continuation of the current line may have. A list item allows
    # both its text column and its own indent.
    hang: tuple[int, ...] = ()
    # The paragraph's first line may continue at a deeper indent, as text
    # aligned under a block opener does (``/* text`` then ``   more``).
    aligned = False
    last = ""
    for line in lines:
        text = line.strip()
        if out:
            tail = out[-1][-1].rstrip()[-2:]
            deeper = _indent(line) - _indent(last)
            continues = _indent(line) in hang or (
                aligned
                and 0 < deeper <= 16
                and tail[-1:] != ":"
                and _CODE_EXAMPLE.match(line) is None
            )
            if (
                continues
                and len(last.rstrip()) + 1 + len(text.split()[0]) > width * 0.8
                and not (narrow and not text[:1].islower())
                and not (_SENTENCE_END.search(tail) and text[:1].isupper())
                and _LIST_ITEM.match(line) is None
                and not _keeps_break(line)
            ):
                out[-1][-1] = out[-1][-1].rstrip()
                out[-1].append(text if _HYPHENATED.search(tail) else " " + text)
                if aligned and deeper > 0:
                    hang = (_indent(line),)
                aligned = False
                last = line
                continue
        aligned = not out and _LIST_ITEM.match(line) is None and not _keeps_break(line)
        out.append([line])
        last = line
        item = _LIST_ITEM.match(line)
        if item is not None:
            hang = (item.end(), _indent(line))
        elif _keeps_break(line):
            hang = ()
        else:
            hang = (_indent(line),)
    return ["".join(pieces) for pieces in out]


def unwrap_comment(text: str, min_width: int = 40) -> str:
    """Join hard-wrapped lines of cleaned comment text into paragraphs.

    Blank lines, list items, tags such as ``@param``, ``key: value`` rows,
    headings, tables, markup, code-like lines, fenced blocks, and changes in
    indentation keep their line breaks. The one indentation change that is
    joined is text aligned under a block opener: a paragraph's first line
    followed by lines up to 16 columns deeper. A line is joined to the one
    before it only when that line reaches close to the paragraph's wrap
    column, so lists of short lines stay as they are. In a paragraph narrower
    than 60 columns, only a line that starts in lowercase is joined.

    Args:
        text: Cleaned comment text, such as ``sanitize_comment`` returns.
        min_width: Paragraphs whose longest line is shorter than this are
            left alone, since they give no reliable wrap column.

    Returns:
        ``text`` with soft line breaks replaced by a space. A break after a
        hyphenated word is removed without adding a space. Only the
        whitespace around a joined break changes.
    """

    out: list[str] = []
    paragraph: list[str] = []
    fenced = False
    for line in text.split("\n"):
        fence = line.lstrip().startswith(_FENCES)
        if fence or fenced or not line.strip():
            if paragraph:
                out.extend(_unwrap_paragraph(paragraph, min_width))
                paragraph = []
            fenced ^= fence
            out.append(line)
        else:
            paragraph.append(line)
    if paragraph:
        out.extend(_unwrap_paragraph(paragraph, min_width))
    return "\n".join(out)


__all__ = ["unwrap_comment"]
