"""Join hard-wrapped comment prose back into one line per paragraph."""

from __future__ import annotations

import re

_LIST_ITEM = re.compile(r"[ \t]*(?:[-*+•]|\d+[.)]|[A-Za-z][.)]|\(\w{1,3}\))[ \t]+")
# Lines that start a new entry but may wrap onto the lines after them: tags
# (@param, \brief), field lists (:param x:), key: value rows, and paragraph
# or list markup. A key that starts with a lowercase letter, even inside an
# inline tag, is more often the end of a sentence that contains a colon.
_LEADER = re.compile(
    r"[ \t]*(?:[@\\][A-Za-z]|:[A-Za-z]+[: ]|<(?i:p|li|dd|dt)>"
    r"|(?!(?:<\w+>)?[a-z])[^\s:]{1,30}(?:[ \t][^\s:]+){0,3}[ \t]*(?:\.{2,}[ \t]*)?:(?:[ \t]|$))"
)
# Lines whose break carries meaning on both sides: doctest, REPL (iex>), and
# shell prompts, numpydoc fields (name : type), quotes, headings, tables,
# fences, markup other than inline tags (<tt>), autolinks, and the entry tags
# above, directives, paths (but not /emphasis/), URLs, link definitions
# ([name]: target), and tab-separated columns.
_STRUCTURE = re.compile(
    r"[ \t]*(?:>>>|\$ |\w+(?:\(\d+\))?> |[\w*]+(?:, [\w*]+)* : |[#|>=]|/(?![^/\s]+/[ \t])"
    r"|<(?!(?i:tt|code|b|i|em|strong|a|span|var|kbd|p|li|dd|dt)\b|https?:)"
    r"|```|~~~|[A-Za-z][\w+.-]*://|www\.|\[[^\]]+\]:|\S[^\t]*\t)"
)
# A doctest or REPL prompt; the lines after it are its output.
_PROMPT = re.compile(r"[ \t]*(?:>>>|\w+(?:\(\d+\))?>)[ \t]")
_CODE_EDGE = re.compile(r"(?:[{}]|(?<![<>!=])=|\w[(\[])[ \t]*$|^[ \t]*[{}]")
# A statement ends in a semicolon. Prose may too, so a line of four or more
# words needs a bracket, an assignment, or a leading keyword as well.
_STATEMENT = re.compile(
    r"[ \t]*(?:(?:return|break|continue)\b.*|.*[(){}\[\]=].*|\S+(?:[ \t]+\S+){0,2});[ \t]*$"
)
# An indented call or assignment under a prose line is an example, not a
# continuation aligned under the opener.
_CODE_EXAMPLE = re.compile(
    r"[ \t]*(?:[\w.$]+\(.*\)\W*$"
    r"|(?:(?:var|let|const|val|my|local)[ \t]+)?\S+[ \t]+[-+*/:!<>]?=[ \t])"
)
# Other lines of example code: type signatures (name :: Type), match arms,
# block openers and ends (do |x|, end), trailing comments (# => value, or a
# comment set off by two spaces), results (f(x) = y), and table rows or diagrams laid out in
# columns.
_CODE_LINE = re.compile(
    r"[ \t]*(?:[\w']+(?:[ \t]*,[ \t]*[\w']+)*[ \t]+::[ \t]|case[ \t].*=>|end[ \t]*$)"
    r"|.*\bdo[ \t]*\|[^|]*\|[ \t]*$"
    r"|.*(?:[ \t](?:#|//|--)[ \t]*=>|\S[ \t]{2,}(?:#|//)[ \t]|\)[ \t]+==?[ \t])"
    r"|(?:.*\S {3,}){2}\S"
    r"|(?:.*[ \t]\|[ \t]){3}"
)
_SENTENCE_END = re.compile(r"[.!?:][\"')]?$")
_WORD = re.compile(r"\w")
_HYPHENATED = re.compile(r"\w-$")
_FENCES = ("```", "~~~")
_NARROW_WIDTH = 60


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _is_code(line: str) -> bool:
    return (
        _CODE_EDGE.search(line) is not None
        or _STATEMENT.match(line) is not None
        or _CODE_EXAMPLE.match(line) is not None
        or _CODE_LINE.match(line) is not None
    )


def _keeps_break(line: str) -> bool:
    return (
        _STRUCTURE.match(line) is not None
        or _LEADER.match(line) is not None
        or _is_code(line)
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
    # How much deeper a continuation of the current line may be indented: up
    # to 16 columns for text aligned under a block opener (``/* text`` then
    # ``   more``), and anywhere under the text of a list item or tag.
    reach = 0
    last = ""
    for line in lines:
        text = line.strip()
        if out:
            tail = out[-1][-1].rstrip()[-2:]
            deeper = _indent(line) - _indent(last)
            continues = _indent(line) in hang or (
                0 < deeper <= reach and tail[-1:] != ":" and _CODE_EXAMPLE.match(line) is None
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
                if reach and deeper > 0:
                    hang = (_indent(line),)
                reach = 0
                last = line
                continue
        item = _LIST_ITEM.match(line)
        leader = item is not None or _LEADER.match(line) is not None
        if _STRUCTURE.match(line) or _is_code(line) or _WORD.search(line) is None:
            hang = ()
            reach = 0
        else:
            hang = (item.end(), _indent(line)) if item is not None else (_indent(line),)
            if leader:
                reach = len(text)
            else:
                reach = 16 if not out and _indent(line) == 0 else 0
        out.append([line])
        last = line
    return ["".join(pieces) for pieces in out]


def unwrap_comment(text: str, min_width: int = 40) -> str:
    """Join hard-wrapped lines of cleaned comment text into paragraphs.

    Blank lines, headings, quotes, tables, markup, prompts and the output
    that follows them, numpydoc ``name : type`` rows, code-like lines, fenced
    blocks, indented example paragraphs, and changes in indentation keep
    their line breaks. Lines that begin an entry (list items, tags,
    ``Key: value`` rows, ``<p>``) keep the break before them but may continue
    onto the lines after them, at any hanging indent under their text. Text
    aligned under a block opener (an unindented first line followed by lines
    up to 16 columns deeper) is joined too. A line is joined to the one
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

    lines = text.split("\n")
    # Prose sits at the shallowest indent after the first line (a docstring's
    # summary line has none). A paragraph that sits deeper and has a line of
    # code or a prompt is an indented example and is kept as it is, as is any
    # paragraph with a prompt, whose output follows it.
    base = min((_indent(line) for line in lines[1:] if line.strip()), default=0)
    out: list[str] = []
    paragraph: list[str] = []
    fenced = False

    def flush() -> None:
        if any(_PROMPT.match(line) for line in paragraph) or (
            all(_indent(line) > base for line in paragraph)
            and _LIST_ITEM.match(paragraph[0]) is None
            and any(_is_code(line) or _STRUCTURE.match(line) for line in paragraph)
        ):
            out.extend(paragraph)
        else:
            out.extend(_unwrap_paragraph(paragraph, min_width))
        paragraph.clear()

    for line in lines:
        fence = line.lstrip().startswith(_FENCES)
        if fence or fenced or not line.strip():
            if paragraph:
                flush()
            fenced ^= fence
            out.append(line)
        else:
            paragraph.append(line)
    if paragraph:
        flush()
    return "\n".join(out)


__all__ = ["unwrap_comment"]
