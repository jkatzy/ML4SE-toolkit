"""Comment sanitization helpers built on the comment registry.

The sanitizer accepts raw extracted comments or ``QueryMatch`` values and removes
comment delimiters while preserving the content-bearing text. It derives wrapper
syntax from the registry so parser and sanitizer maintenance stay coupled.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass

from ..Query import QueryMatch
from .registry import CommentSyntax, get_comment_syntax

_EXAMPLE_BODY_PLACEHOLDERS = (
    "block note",
    "note",
    "Visible content",
    "+ 100",
    "Remember the bull.",
)
_DECORATIVE_RULER_CHARS = frozenset("#-=*_<>/")
_LINE_ONLY_DECORATIVE_CHARS = frozenset("#-*_/<>")


@dataclass(frozen=True)
class _SanitizerSyntax:
    """Resolved delimiter wrappers used to normalize extracted comments.

    Attributes:
        line_wrappers: Ordered ``(open, close)`` pairs for line comments.
        block_wrappers: Ordered ``(open, close)`` pairs for block comments.
    """

    line_wrappers: tuple[tuple[str, str], ...]
    block_wrappers: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class _WrappedLine:
    """One physical line with a registry-derived wrapper removed.

    Attributes:
        outer_indent: Whitespace before the opening delimiter.
        inner: Text between the opening and closing delimiters.
        wrapper: Delimiter pair matched on this line.
        opener_adjacent: Whether content started immediately after the opener.
    """

    outer_indent: str
    inner: str
    wrapper: tuple[str, str]
    opener_adjacent: bool


def _split_example_placeholder(example_text: str) -> tuple[str, str, str] | None:
    for placeholder in _EXAMPLE_BODY_PLACEHOLDERS:
        if placeholder not in example_text:
            continue
        prefix, suffix = example_text.split(placeholder, 1)
        return prefix, placeholder, suffix
    return None


def _line_wrapper_from_example(example_text: str) -> tuple[str, str] | None:
    parts = _split_example_placeholder(example_text)
    if parts is not None:
        return parts[0].strip(), parts[2]

    if _known_block_wrappers(example_text):
        return None

    if "\n" in example_text or "\r" in example_text:
        return None

    stripped = example_text.lstrip(" \t")
    if not stripped:
        return None

    token_candidates = (
        "NOTE*",
        "NOTE",
        "REM",
        "BTW",
        "dnl",
        "NB.",
        "@comment",
        "@c",
    )
    for token in token_candidates:
        if stripped[: len(token)].lower() != token.lower():
            continue
        if len(stripped) == len(token) or stripped[len(token)].isspace():
            return token, ""

    token_match = re.match(r"[^\w\s]+", stripped)
    if token_match is None:
        token_match = re.match(r"[^\s]+", stripped)
    if token_match is None:
        return None
    return token_match.group(0), ""


def _known_block_wrappers(example_text: str) -> tuple[tuple[str, str], ...]:
    stripped = example_text.strip()
    fixed_wrappers = (
        ("<%--", "--%>"),
        ("<%#", "%>"),
        ("<!--", "-->"),
        ("<mt:Ignore>", "</mt:Ignore>"),
        ("<comment>", "</comment>"),
        ("<#--", "-->"),
        ("{#", "#}"),
        ("{{!", "}}"),
        ("<!", "!>"),
        ("#Rem", "#End"),
        ("#rem", "#end"),
        ("#-", "-#"),
        ("#|", "|#"),
        ("#=", "=#"),
        ("%{", "%}"),
        ("###", "###"),
        ("--[[", "]]"),
        ("/*", "*/"),
        ("/**", "*/"),
        ("/+", "+/"),
        ("/;", ";/"),
        ("(*", "*)"),
        ("{-", "-}"),
        ("#{", "}#"),
        ("@q", "@>"),
        (';"', '"'),
    )

    wrappers = []
    for wrapper in fixed_wrappers:
        if _wrapper_matches(stripped, wrapper[0], wrapper[1]):
            wrappers.append(wrapper)

    lua_long = re.match(r"--\[(=*)\[[\s\S]*\]\1\]$", stripped)
    if lua_long is not None:
        equals = lua_long.group(1)
        wrappers.append((f"--[{equals}[", f"]{equals}]"))

    if re.match(r"(?is)^=begin[ \t]+comment\b", stripped) and re.search(
        r"(?im)^=end[ \t]+comment\b[^\r\n]*$",
        stripped,
    ):
        wrappers.append(("=begin comment", "=end comment"))
    elif re.match(r"(?i)^=for[ \t]+comment\b", stripped):
        wrappers.append(("=for comment", ""))
    elif re.match(r"(?i)^=comment\b", stripped):
        wrappers.append(("=comment", ""))
    elif re.match(r"(?i)^NOTE(?:[ \t]|\n|$)", stripped):
        wrappers.append(("NOTE", ""))

    return tuple(dict.fromkeys(wrappers))


def _iter_regex_examples(syntax: CommentSyntax):
    yield from syntax.shared_regex_examples
    yield from syntax.canonical_regex_examples


def _build_sanitizer_syntax(syntax: CommentSyntax) -> _SanitizerSyntax:
    line_wrappers = []
    for example in _iter_regex_examples(syntax):
        if example.kind != "line":
            continue
        wrapper = _line_wrapper_from_example(example.expected_match)
        if wrapper is None:
            continue
        for candidate in (
            wrapper,
            (wrapper[0], wrapper[1].lstrip()),
        ):
            if candidate not in line_wrappers:
                line_wrappers.append(candidate)

    block_wrappers = []
    for open_delim, close_delim in syntax.nested_delimiters:
        wrapper = (open_delim, close_delim)
        if wrapper not in block_wrappers:
            block_wrappers.append(wrapper)

    for example in _iter_regex_examples(syntax):
        if example.kind != "block":
            continue
        parts = _split_example_placeholder(example.expected_match)
        candidates: tuple[tuple[str, str], ...] = ()
        if parts is not None:
            candidates = (
                (parts[0], parts[2]),
                (parts[0].rstrip(), parts[2].lstrip()),
            )
        candidates = (*candidates, *_known_block_wrappers(example.expected_match))
        for wrapper in candidates:
            if wrapper not in block_wrappers:
                block_wrappers.append(wrapper)

    block_wrappers.sort(key=lambda wrapper: len(wrapper[0]) + len(wrapper[1]), reverse=True)
    line_wrappers.sort(key=lambda wrapper: len(wrapper[0]) + len(wrapper[1]), reverse=True)
    return _SanitizerSyntax(tuple(line_wrappers), tuple(block_wrappers))


def _is_case_insensitive_token(token: str) -> bool:
    return any(char.isalpha() for char in token)


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _line_open_pattern(open_token: str) -> str:
    """Return a regex fragment for a line-comment opener.

    Args:
        open_token: Registry-derived line-comment opener.

    Returns:
        Regex text that strips the opener. Multi-character homogeneous openers
        such as ``//`` also strip documentation/ruler variants like ``///`` or
        ``////``. Single-character openers stay exact so Markdown headings inside
        ``#`` comments remain content.
    """

    if len(open_token) > 1 and len(set(open_token)) == 1:
        return rf"{re.escape(open_token[0])}{{{len(open_token)},}}"
    return re.escape(open_token)


def _token_startswith(text: str, token: str) -> bool:
    if not _is_case_insensitive_token(token):
        return text.startswith(token)
    return text[: len(token)].lower() == token.lower()


def _token_endswith(text: str, token: str) -> bool:
    if not token:
        return True
    if not _is_case_insensitive_token(token):
        return text.endswith(token)
    return text[-len(token) :].lower() == token.lower()


def _strip_wrapped_line(line: str, wrappers: tuple[tuple[str, str], ...]) -> _WrappedLine | None:
    indent_length = len(line) - len(line.lstrip(" \t"))
    outer_indent = line[:indent_length]
    candidate = line[indent_length:]

    for open_token, close_token in wrappers:
        if not open_token or not _token_startswith(candidate, open_token):
            continue
        if not _token_endswith(candidate, close_token):
            continue
        if close_token and len(candidate) < len(open_token) + len(close_token):
            continue

        inner_end = len(candidate) - len(close_token) if close_token else len(candidate)
        inner = candidate[len(open_token) : inner_end]
        opener_adjacent = not open_token.endswith((" ", "\t")) and not inner.startswith((" ", "\t"))
        if not open_token.endswith((" ", "\t")) and inner.startswith((" ", "\t")):
            inner = inner[1:]
        return _WrappedLine(
            outer_indent=outer_indent,
            inner=inner,
            wrapper=(open_token, close_token),
            opener_adjacent=opener_adjacent,
        )
    return None


def _strip_grouped_wrapped_lines(
    raw_comment: str, wrappers: tuple[tuple[str, str], ...]
) -> tuple[list[str], tuple[tuple[str, str], ...]] | None:
    """Strip a registry wrapper independently from every non-empty line.

    Args:
        raw_comment: Newline-normalized extracted comment text.
        wrappers: Registry-derived opening and closing delimiter pairs.

    Returns:
        Sanitized physical lines and the wrappers they matched, or ``None`` when
        any non-empty line is not independently wrapped.
    """

    if not wrappers:
        return None

    matched: list[_WrappedLine | None] = []
    for line in raw_comment.split("\n"):
        if not line.strip():
            matched.append(None)
            continue
        wrapped = _strip_wrapped_line(line, wrappers)
        if wrapped is None:
            return None
        matched.append(wrapped)

    content_lines = [
        wrapped.inner for wrapped in matched if wrapped is not None and wrapped.inner.strip()
    ]
    use_inner_indent = bool(content_lines) and all(
        not wrapped.opener_adjacent
        for wrapped in matched
        if wrapped is not None and wrapped.inner.strip()
    )

    stripped_lines: list[str] = []
    for wrapped in matched:
        if wrapped is None:
            stripped_lines.append("")
            continue
        prefix = "" if use_inner_indent else wrapped.outer_indent
        stripped_lines.append(prefix + wrapped.inner.rstrip())

    if use_inner_indent:
        indent_widths = [
            len(line) - len(line.lstrip(" \t")) for line in stripped_lines if line.strip()
        ]
        if indent_widths and max(indent_widths) - min(indent_widths) <= 2:
            stripped_lines = [line.lstrip(" \t") for line in stripped_lines]
    else:
        positive_outer_indents = [
            len(wrapped.outer_indent)
            for wrapped in matched
            if wrapped is not None and wrapped.outer_indent
        ]
        if positive_outer_indents and any(
            wrapped is not None and not wrapped.outer_indent for wrapped in matched
        ):
            trim_width = min(positive_outer_indents)
            stripped_lines = [
                line[trim_width:] if line.startswith((" ", "\t")) else line
                for line in stripped_lines
            ]

    return stripped_lines, tuple(wrapped.wrapper for wrapped in matched if wrapped is not None)


def _strip_grouped_line_wrappers(
    raw_comment: str, line_wrappers: tuple[tuple[str, str], ...]
) -> str | None:
    if not line_wrappers:
        return None

    stripped_lines: list[str] = []
    matched_open_tokens: list[str] = []
    opener_adjacent: list[bool] = []
    repeated_registered_openers: list[bool] = []
    for line in raw_comment.split("\n"):
        if line == "":
            stripped_lines.append("")
            continue

        wrapper = None
        stripped = None
        for open_token, close_token in line_wrappers:
            flags = re.IGNORECASE if _is_case_insensitive_token(open_token + close_token) else 0
            pattern = re.compile(
                rf"^[ \t]*(?:{_line_open_pattern(open_token)})(.*){re.escape(close_token)}$",
                flags,
            )
            match = pattern.match(line)
            if match is not None:
                wrapper = (open_token, close_token)
                matched_open_tokens.append(open_token)
                stripped = match.group(1)
                opener_adjacent.append(not stripped.startswith((" ", "\t")))
                repeated_registered_openers.append(
                    bool(open_token) and len(open_token) == 1 and stripped.startswith(open_token)
                )
                if stripped.startswith((" ", "\t")):
                    stripped = stripped[1:]
                break

        if wrapper is None or stripped is None:
            return None

        stripped_lines.append(stripped.rstrip())

    stripped_lines = _strip_residual_line_gutters(
        stripped_lines,
        tuple(matched_open_tokens),
        tuple(opener_adjacent),
    )
    stripped_lines = _strip_registered_right_gutters(
        stripped_lines,
        tuple(matched_open_tokens),
        allow_repeated_single_char=bool(repeated_registered_openers)
        and all(repeated_registered_openers),
    )
    stripped_lines = _strip_single_line_decorative_padding(stripped_lines)
    stripped_lines = _strip_decorative_edge_rulers(
        stripped_lines,
        empty_ruler_chars=_LINE_ONLY_DECORATIVE_CHARS | frozenset("".join(matched_open_tokens)),
    )
    return _normalize_sanitized_body("\n".join(stripped_lines))


def _wrapper_matches(raw_comment: str, open_text: str, close_text: str) -> bool:
    if raw_comment.startswith(open_text) and raw_comment.endswith(close_text):
        return True

    if not (_is_case_insensitive_token(open_text) or _is_case_insensitive_token(close_text)):
        return False

    return (
        raw_comment[: len(open_text)].lower() == open_text.lower()
        and raw_comment[len(raw_comment) - len(close_text) :].lower() == close_text.lower()
    )


def _strip_block_wrapper(
    raw_comment: str, block_wrappers: tuple[tuple[str, str], ...]
) -> tuple[str, tuple[str, str]] | None:
    for open_text, close_text in block_wrappers:
        if not _wrapper_matches(raw_comment, open_text, close_text):
            continue

        inner = raw_comment[len(open_text) : len(raw_comment) - len(close_text)]
        return inner, (open_text, close_text)
    return None


def _is_punctuation_only(line: str) -> bool:
    stripped = line.strip()
    return len(stripped) >= 2 and all(
        not char.isalnum() and not char.isspace() for char in stripped
    )


def _wrapper_punctuation_chars(wrapper: tuple[str, str]) -> frozenset[str]:
    return frozenset(
        char for token in wrapper for char in token if not char.isalnum() and not char.isspace()
    )


def _strip_common_left_gutter(
    lines: list[str], wrapper: tuple[str, str], *, allow_doc_star: bool
) -> tuple[list[str], bool]:
    allowed_chars = set(_wrapper_punctuation_chars(wrapper))
    if allow_doc_star:
        allowed_chars.add("*")

    content_indexes = [
        index for index, line in enumerate(lines) if line.strip() and not _is_punctuation_only(line)
    ]
    if not content_indexes:
        return lines, False

    matches: dict[int, re.Match[str]] = {}
    gutter_char: str | None = None
    pattern = re.compile(r"^[ \t]*([^\w\s]+)(?:[ \t]|$)")
    for index in content_indexes:
        match = pattern.match(lines[index])
        if match is None:
            return lines, False
        token = match.group(1)
        if len(set(token)) != 1 or token[0] not in allowed_chars:
            return lines, False
        if gutter_char is not None and token[0] != gutter_char:
            return lines, False
        gutter_char = token[0]
        matches[index] = match

    stripped = list(lines)
    for index, match in matches.items():
        stripped[index] = lines[index][match.end() :]

    if gutter_char is not None:
        blank_frame_pattern = re.compile(rf"^[ \t]*{re.escape(gutter_char)}+[ \t]+")
        for index, line in enumerate(stripped):
            if index in matches or not line.strip() or _is_punctuation_only(line):
                continue
            match = blank_frame_pattern.match(line)
            if match is not None:
                stripped[index] = line[match.end() :]

    return stripped, True


def _strip_common_right_gutter(lines: list[str], allowed_chars: frozenset[str]) -> list[str]:
    content_indexes = [
        index for index, line in enumerate(lines) if line.strip() and not _is_punctuation_only(line)
    ]
    if not content_indexes:
        return lines

    gutter_char: str | None = None
    matches: dict[int, re.Match[str]] = {}
    pattern = re.compile(r"(?:(?<=[ \t])|^)([^\w\s]+)[ \t]*$")
    for index in content_indexes:
        match = pattern.search(lines[index])
        if match is None:
            return lines
        token = match.group(1)
        if len(set(token)) != 1 or token[0] not in allowed_chars:
            return lines
        if gutter_char is not None and token[0] != gutter_char:
            return lines
        gutter_char = token[0]
        matches[index] = match

    stripped = list(lines)
    for index, match in matches.items():
        stripped[index] = lines[index][: match.start()].rstrip()

    if gutter_char is not None:
        punctuation_pattern = re.compile(rf"{re.escape(gutter_char)}+[ \t]*$")
        for index, line in enumerate(stripped):
            if not _is_punctuation_only(line):
                continue
            match = punctuation_pattern.search(line)
            if match is not None:
                stripped[index] = line[: match.start()].rstrip()

        blank_frame_pattern = re.compile(rf"[ \t]+{re.escape(gutter_char)}+[ \t]*$")
        for index, line in enumerate(stripped):
            if index in matches or not line.strip() or _is_punctuation_only(line):
                continue
            match = blank_frame_pattern.search(line)
            if match is not None:
                stripped[index] = line[: match.start()].rstrip()
    return stripped


def _is_decorative_ruler_line(line: str) -> bool:
    stripped = line.strip()
    return len(stripped) >= 2 and (
        (len(set(stripped)) == 1 and stripped[0] in _DECORATIVE_RULER_CHARS)
        or _is_punctuation_only(stripped)
    )


def _has_framed_content_line(lines: list[str], frame_char: str) -> bool:
    """Return whether a ruler character frames content in the remaining body.

    Args:
        lines: Sanitized body lines after delimiter removal.
        frame_char: Candidate decorative ruler character.

    Returns:
        True when a non-ruler line starts and ends with the same character,
        indicating an ASCII title card whose frame should be preserved.
    """

    for line in lines:
        stripped = line.strip()
        if not stripped or _is_decorative_ruler_line(stripped):
            continue
        if (
            stripped.startswith(frame_char)
            and stripped.endswith(frame_char)
            and any(char != frame_char for char in stripped)
        ):
            return True
    return False


def _strip_decorative_edge_rulers(
    lines: list[str],
    *,
    empty_ruler_chars: frozenset[str] = frozenset(),
    protected_ruler_chars: frozenset[str] = frozenset(),
) -> list[str]:
    """Remove delimiter-created ruler-only edge lines while preserving banners.

    Args:
        lines: Comment body lines after language delimiter stripping.

    Returns:
        Lines with leading and trailing ruler-only scaffolding removed unless
        the same ruler character frames an interior title-card line.
    """

    non_empty = [line for line in lines if line.strip()]
    if non_empty and all(_is_decorative_ruler_line(line) for line in non_empty):
        used_chars = frozenset("".join(line.strip() for line in non_empty))
        if used_chars & empty_ruler_chars:
            return []
        return lines

    stripped = list(lines)
    while stripped and not stripped[0].strip():
        stripped.pop(0)
    while stripped and not stripped[-1].strip():
        stripped.pop()

    while stripped:
        first = stripped[0]
        first_text = first.strip()
        if not _is_decorative_ruler_line(first):
            break
        if len(set(first_text)) == 1 and first_text[0] in protected_ruler_chars:
            break
        if _has_framed_content_line(stripped[1:], first_text[0]):
            break
        stripped.pop(0)
        while stripped and not stripped[0].strip():
            stripped.pop(0)

    while stripped:
        last = stripped[-1]
        last_text = last.strip()
        if not _is_decorative_ruler_line(last):
            break
        if len(set(last_text)) == 1 and last_text[0] in protected_ruler_chars:
            break
        if _has_framed_content_line(stripped[:-1], last_text[0]):
            break
        stripped.pop()
        while stripped and not stripped[-1].strip():
            stripped.pop()

    return stripped


def _remove_decorative_block_lines(
    lines: list[str],
    *,
    remove_interior: bool,
    protected_ruler_chars: frozenset[str] = frozenset(),
) -> list[str]:
    non_empty = [line for line in lines if line.strip()]
    if non_empty and all(_is_decorative_ruler_line(line) for line in non_empty):
        return []
    if remove_interior:
        ruler_counts: dict[str, int] = {}
        for line in lines:
            stripped = line.strip()
            if not _is_decorative_ruler_line(stripped):
                continue
            if len(set(stripped)) == 1:
                ruler_counts[stripped[0]] = ruler_counts.get(stripped[0], 0) + 1

        stripped_lines = [
            line
            for line in lines
            if not (
                _is_decorative_ruler_line(line)
                and len(set(line.strip())) == 1
                and line.strip()[0] not in protected_ruler_chars
                and ruler_counts.get(line.strip()[0], 0) >= 2
            )
        ]
        return _strip_decorative_edge_rulers(
            stripped_lines, protected_ruler_chars=protected_ruler_chars
        )
    return _strip_decorative_edge_rulers(lines)


def _strip_registered_right_gutters(
    lines: list[str],
    open_tokens: tuple[str, ...],
    *,
    allow_repeated_single_char: bool = False,
) -> list[str]:
    opener_lengths: dict[str, set[int]] = {}
    for token in open_tokens:
        if not token or token[-1].isalnum() or token[-1].isspace():
            continue
        opener_lengths.setdefault(token[-1], set()).add(len(token))
    if not opener_lengths:
        return lines

    content_indexes = [
        index
        for index, line in enumerate(lines)
        if line.strip() and not _is_decorative_ruler_line(line)
    ]
    if not content_indexes:
        return lines

    matches: dict[int, re.Match[str]] = {}
    gutter_char: str | None = None
    pattern = re.compile(r"([^\w\s])\1*[ \t]*$")
    for index in content_indexes:
        match = pattern.search(lines[index])
        if match is None or match.group(1) not in opener_lengths:
            return lines
        start = match.start()
        token_length = len(lines[index][start:].rstrip())
        registered_lengths = opener_lengths[match.group(1)]
        if max(registered_lengths) == 1 and token_length != 1 and not allow_repeated_single_char:
            return lines
        if start > 0 and not lines[index][start - 1].isspace() and token_length < 2:
            return lines
        if gutter_char is not None and match.group(1) != gutter_char:
            return lines
        gutter_char = match.group(1)
        matches[index] = match

    stripped = list(lines)
    for index, match in matches.items():
        stripped[index] = lines[index][: match.start()].rstrip()

    if gutter_char is not None:
        punctuation_pattern = re.compile(rf"{re.escape(gutter_char)}+[ \t]*$")
        for index, line in enumerate(stripped):
            if not _is_punctuation_only(line):
                continue
            match = punctuation_pattern.search(line)
            if match is not None:
                stripped[index] = line[: match.start()].rstrip()
    return stripped


def _strip_single_line_decorative_padding(lines: list[str]) -> list[str]:
    non_empty_indexes = [index for index, line in enumerate(lines) if line.strip()]
    if len(non_empty_indexes) != 1:
        return lines

    index = non_empty_indexes[0]
    line = lines[index]
    match = re.match(r"^([ \t]*)([^\w\s])\2{2,}[ \t]*(.*?)[ \t]*\2{2,}$", line)
    if match is None or match.group(2) == "=" or not any(char.isalnum() for char in match.group(3)):
        return lines

    stripped = list(lines)
    stripped[index] = match.group(1) + match.group(3).strip()
    return stripped


def _strip_space_padding_before_tabs(lines: list[str]) -> list[str]:
    """Strip space padding from aligned text when tab-indented lines coexist.

    Args:
        lines: Comment body lines before final normalization.

    Returns:
        Lines with common leading spaces removed from space-indented lines when
        every non-empty line is indented by spaces or tabs.
    """

    non_empty = [line for line in lines if line.strip()]
    if not non_empty or not all(line.startswith((" ", "\t")) for line in non_empty):
        return lines

    space_indented = [line for line in non_empty if line.startswith(" ")]
    if not space_indented or not any(line.startswith("\t") for line in non_empty):
        return lines

    common_spaces = min(len(line) - len(line.lstrip(" ")) for line in space_indented)
    if common_spaces == 0:
        return lines

    stripped = []
    for line in lines:
        if line.startswith(" "):
            stripped.append(line[common_spaces:])
        else:
            stripped.append(line)
    return stripped


def _strip_residual_line_gutters(
    lines: list[str],
    matched_open_tokens: tuple[str, ...],
    opener_adjacent: tuple[bool, ...],
) -> list[str]:
    """Strip punctuation directly repeated after a registered line opener.

    Args:
        lines: Lines after one registered line-comment opener has been removed.
        matched_open_tokens: Openers matched while removing each non-empty line.
        opener_adjacent: Whether each non-empty line had no opener padding.

    Returns:
        Lines with common directly-adjacent punctuation gutters removed.
    """

    if not matched_open_tokens or not all(opener_adjacent):
        return lines

    stripped_lines = list(lines)
    while True:
        non_empty = [line for line in stripped_lines if line.strip()]
        if not non_empty:
            return stripped_lines

        first_chars = {line.lstrip()[0] for line in non_empty}
        if len(first_chars) != 1:
            return stripped_lines
        (gutter_char,) = first_chars
        if gutter_char.isalnum() or gutter_char.isspace():
            return stripped_lines
        registered_chars = {
            token[-1]
            for token in matched_open_tokens
            if token and not token[-1].isalnum() and not token[-1].isspace()
        }
        if len(non_empty) == 1 and gutter_char not in registered_chars:
            return stripped_lines
        if len(non_empty) > 1 and _has_framed_content_line(stripped_lines, gutter_char):
            return stripped_lines

        next_lines: list[str] = []
        for line in stripped_lines:
            prefix_length = len(line) - len(line.lstrip())
            stripped = line[prefix_length:]
            if stripped.startswith(gutter_char):
                stripped = stripped[1:]
            next_lines.append(line[:prefix_length] + stripped)
        stripped_lines = next_lines


def _normalize_sanitized_body(body: str, *, preserve_single_line_padding: bool = False) -> str:
    body = _normalize_newlines(body)
    body = body.strip("\n")

    if "\n" not in body:
        return body.rstrip() if preserve_single_line_padding else body.strip()

    normalized = textwrap.dedent("\n".join(_strip_space_padding_before_tabs(body.split("\n"))))
    normalized_lines = [line.rstrip() for line in normalized.split("\n")]
    return "\n".join(normalized_lines).strip("\n")


def _sanitize_grouped_block_lines(lines: list[str], wrappers: tuple[tuple[str, str], ...]) -> str:
    wrapper_chars = frozenset(
        char for wrapper in wrappers for char in _wrapper_punctuation_chars(wrapper)
    )
    non_empty = [line for line in lines if line.strip()]
    if non_empty and all(_is_decorative_ruler_line(line) for line in non_empty):
        used_chars = frozenset("".join(line.strip() for line in non_empty))
        if used_chars <= wrapper_chars:
            if all(
                wrapper[0].startswith("/*") and wrapper[1].endswith("*/")
                for wrapper in wrappers
            ):
                return ""
            return _normalize_sanitized_body("\n".join(lines))
    lines = _remove_decorative_block_lines(lines, remove_interior=False)
    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_block_body(
    body: str,
    wrapper: tuple[str, str],
    line_wrappers: tuple[tuple[str, str], ...],
    *,
    allow_doc_star: bool,
    protected_ruler_chars: frozenset[str] = frozenset(),
) -> str:
    body = _normalize_newlines(body)
    if body.startswith("\n"):
        body = body[1:]
    if body.endswith("\n"):
        body = body[:-1]

    lines = body.split("\n")
    line_openers = tuple(open_token for open_token, _ in line_wrappers)
    wrapper_chars = _wrapper_punctuation_chars(wrapper)
    while lines and lines[0].strip() and set(lines[0].strip()) <= wrapper_chars:
        lines.pop(0)
    while lines and lines[-1].strip() and set(lines[-1].strip()) <= wrapper_chars:
        lines.pop()
    while lines and lines[0].strip() in line_openers:
        lines.pop(0)
    while lines and lines[-1].strip() in line_openers:
        lines.pop()

    lines, stripped_left_gutter = _strip_common_left_gutter(
        lines, wrapper, allow_doc_star=allow_doc_star
    )
    lines = _strip_common_right_gutter(lines, _wrapper_punctuation_chars(wrapper) | frozenset("*"))
    lines = _remove_decorative_block_lines(
        lines,
        remove_interior=stripped_left_gutter,
        protected_ruler_chars=protected_ruler_chars,
    )

    return _normalize_sanitized_body("\n".join(lines))


class CommentSanitizer:
    """Normalize extracted comments for one language.

    Args:
        language: Registry language key used to resolve comment delimiters.

    Raises:
        NotImplementedError: If the language is not present in the registry.
    """

    def __init__(self, language: str):
        self.language = language
        self.syntax = get_comment_syntax(language)
        self._sanitizer_syntax = _build_sanitizer_syntax(self.syntax)

    def sanitize(self, comment: str | QueryMatch) -> str:
        """Return the content-bearing body for one extracted comment.

        Args:
            comment: Raw comment text or a ``QueryMatch`` returned by a comment
                query.

        Returns:
            The comment body with language delimiters, repeated line prefixes,
            and common block gutters removed.
        """

        raw_comment = comment.match if isinstance(comment, QueryMatch) else comment
        raw_comment = _normalize_newlines(raw_comment)

        grouped_block_result = _strip_grouped_wrapped_lines(
            raw_comment, self._sanitizer_syntax.block_wrappers
        )
        if grouped_block_result is not None:
            lines, wrappers = grouped_block_result
            return _sanitize_grouped_block_lines(lines, wrappers)

        closed_line_wrappers = tuple(
            wrapper for wrapper in self._sanitizer_syntax.line_wrappers if wrapper[1]
        )
        grouped_closed_line_result = _strip_grouped_wrapped_lines(raw_comment, closed_line_wrappers)
        if grouped_closed_line_result is not None:
            lines, wrappers = grouped_closed_line_result
            return _sanitize_grouped_block_lines(lines, wrappers)

        block_result = _strip_block_wrapper(raw_comment, self._sanitizer_syntax.block_wrappers)
        if block_result is not None:
            inner, wrapper = block_result
            protected_ruler_chars = (
                frozenset("=")
                if raw_comment.startswith(wrapper[0] + wrapper[0][-1] + "\n")
                else frozenset()
            )
            return _sanitize_block_body(
                inner,
                wrapper,
                self._sanitizer_syntax.line_wrappers,
                allow_doc_star=True,
                protected_ruler_chars=protected_ruler_chars,
            )

        line_block_result = _strip_block_wrapper(raw_comment, closed_line_wrappers)
        if line_block_result is not None:
            inner, wrapper = line_block_result
            return _sanitize_block_body(
                inner,
                wrapper,
                self._sanitizer_syntax.line_wrappers,
                allow_doc_star=False,
            )

        line_result = _strip_grouped_line_wrappers(
            raw_comment, self._sanitizer_syntax.line_wrappers
        )
        if line_result is not None:
            return line_result

        return _normalize_sanitized_body(raw_comment)


def sanitize_comment(language: str, comment: str | QueryMatch) -> str:
    """Return sanitized comment text for ``language``."""

    return CommentSanitizer(language).sanitize(comment)


__all__ = ["CommentSanitizer", "sanitize_comment"]
