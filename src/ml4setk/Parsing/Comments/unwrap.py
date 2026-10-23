"""Join hard-wrapped comment prose back into one line per paragraph."""

from __future__ import annotations

import re

_LIST_ITEM = re.compile(r"[ \t]*(?:[-*+•]|\d+(?:[.)]| -)|[A-Za-z][.)]|\(\w{1,3}\))[ \t]+")
# Inline tags, which sit inside a line of prose rather than starting a block.
_INLINE_TAGS = "tt|code|c|b|i|em|strong|a|span|var|kbd"
# Lines that start a new entry but may wrap onto the lines after them: tags
# (@param, \brief), field lists (:param x:), key: value rows, and an
# opening tag followed by its text (<p>, <summary>, <param name="x">) other
# than <pre> and inline tags. A key that starts with a lowercase letter, even
# inside an inline tag, is more often the end of a sentence with a colon.
_LEADER = re.compile(
    r"[ \t]*(?:[@\\][A-Za-z]|:[A-Za-z]+[: ]|<(?i:p|li|dd|dt)>"
    rf"|<(?!(?i:{_INLINE_TAGS}|pre)\b|https?:)[A-Za-z][^<>]*>(?=\S)"
    r"|(?!(?:<\w+>)?[a-z])[^\s:]{1,30}(?:[ \t][^\s:]+){0,3}[ \t]*(?:\.{2,}[ \t]*)?:(?:[ \t]|$))"
)
# Lines whose break carries meaning on both sides: doctest, REPL (iex>), and
# shell prompts, numpydoc fields (name : type), quotes, headings, tables,
# fences, lines of nothing but block tags (a lone <code> counts), other markup
# except inline tags, autolinks, and the entry tags above, directives, paths
# (but not /emphasis/), URLs, link definitions ([name]: target),
# tab-separated columns, and Dartdoc directives ({@template x}, {@macro x}).
_STRUCTURE = re.compile(
    r"[ \t]*(?:>>>|\$ |\w+(?:\(\d+\))?> |[\w*]+(?:, [\w*]+)* : |[#|>=]|/(?![^/\s]+/[ \t])"
    r"|\{@(?:template|endtemplate|macro|tool|end-tool)\b"
    r"|(?:<(?!/?(?i:tt|c|b|i|em|strong|a|span|var|kbd)\b|https?:)[^<>]+>[ \t]*)+$"
    rf"|<(?!(?i:{_INLINE_TAGS}|p|li|dd|dt)\b|https?:|(?!/|(?i:pre)\b)[A-Za-z][^<>]*>(?=\S))"
    r"|```|~~~|[A-Za-z][\w+.-]*://|www\.|\[[^\]]+\]:|\S[^\t]*\t)"
)
# A doctest or REPL prompt; the lines after it are its output.
_PROMPT = re.compile(r"[ \t]*(?:>>>|\w+(?:\(\d+\))?>)[ \t]")
# A line that opens or closes a block, ends in an assignment, or opens a call.
# A Javadoc inline tag ({@code x} text) starts prose, but a lone {@code opens
# a block. A line that ends by closing an inline tag ({@link X}) is prose too.
_CODE_EDGE = re.compile(
    r"(?:\{|(?<![<>!=])=|\w[(\[])[ \t]*$|^(?!.*\{@[^{}]*\}[ \t]*$).*\}[ \t]*$"
    r"|^[ \t]*(?:\{(?!@\w+[ \t]+\S)|\})"
)
# A statement ends in a semicolon, perhaps before a // comment. Prose may end
# in a semicolon too, so a line of four or more words needs a bracket, an
# assignment, or a leading keyword as well.
_STATEMENT = re.compile(
    r"[ \t]*(?:(?:return|break|continue)\b.*|.*[(){}\[\]=].*|\S+(?:[ \t]+\S+){0,2});"
    r"[ \t]*(?://.*)?$"
)
# A call whose parentheses balance, nested up to three deep.
_CALL = r"[\w.$]+\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)"
# An indented call or assignment under a prose line is an example, not a
# continuation aligned under the opener. Calls joined by operators must span
# the line, so prose that starts and ends with a call stays prose. A Verilog
# `MACRO(...) counts, but not `code` quoted inline.
_CODE_EXAMPLE = re.compile(
    rf"[ \t]*(?:(?:`(?![^`]*`))?{_CALL}(?:[^\w(]+{_CALL})*\W*$"
    r"|(?:(?:var|let|const|val|my|local|type)[ \t]+)?\S+[ \t]+[-+*/:!<>]?=[ \t])"
)
# Other lines of example code: type signatures (name :: Type), match arms,
# block openers and ends (do |x|, end), calls with a symbol argument
# (belongs_to :author, ...), trailing comments (# => value, or a comment set
# off by two spaces), results (f(x) = y, or f(x) => y, outside inline code),
# and table rows or diagrams laid out in columns.
_CODE_LINE = re.compile(
    r"[ \t]*(?:[\w']+(?:[ \t]*,[ \t]*[\w']+)*[ \t]+::[ \t]|case[ \t].*=>|end[ \t]*$"
    r"|[a-z_]\w*[ \t]+:\w+,[ \t])"
    r"|.*\bdo[ \t]*\|[^|]*\|[ \t]*$"
    r"|.*(?:[ \t](?:#|//|--)[ \t]*=>|\S[ \t]{2,}(?:#|//)[ \t])"
    r"|[^`]*\)[ \t]+(?:==?|=>)[ \t]"
    r"|(?:.*\S {3,}){2}\S"
    r"|(?:.*[ \t]\|[ \t]){3}"
)
_SENTENCE_END = re.compile(r"[.!?:][\"')]?$")
_WORD = re.compile(r"\w")
_HYPHENATED = re.compile(r"\w-$")
_FENCES = ("```", "~~~")
_UNDERLINE = re.compile(r"[ \t]*~+[ \t]*$")
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
    # A line holding a URL may run past the wrap column. When at least three
    # other lines are wide enough to show the column, they set it instead.
    plain = [len(line.rstrip()) for line in lines if "://" not in line]
    if len(plain) >= 3 and max(plain) >= _NARROW_WIDTH:
        width = max(plain)
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
    blocks (a line of tildes under a title is a heading underline, not a
    fence), lines of nothing but block tags, indented example paragraphs, and
    changes in indentation keep their line breaks. Lines that begin an entry
    (list items, tags, ``Key: value`` rows, ``<p>``, XML doc tags such as
    ``<summary>``) keep the break before them but may continue onto the
    lines after them, at any hanging indent under their text. Text aligned
    under a block opener (an unindented first line followed by lines up to
    16 columns deeper) is joined too. A line is joined to the one before it
    only when that line reaches close to the paragraph's wrap column
    (ignoring lines with a URL when three others show it), so lists of short
    lines stay as they are. In a paragraph narrower than 60 columns, only a
    line that starts in lowercase is joined.

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

    prev = ""
    for line in lines:
        # A line of tildes under a title at least as long is a reStructuredText
        # heading underline, not a fence.
        underline = (
            not fenced
            and prev.strip() != ""
            and _UNDERLINE.match(line) is not None
            and len(line.strip()) >= len(prev.strip())
        )
        fence = line.lstrip().startswith(_FENCES) and not underline
        prev = line
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
