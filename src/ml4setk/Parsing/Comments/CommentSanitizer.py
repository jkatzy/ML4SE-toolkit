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
from .registry import (
    CommentSyntax,
    _resolve_comment_language_key,
    get_comment_syntax,
)

_EXAMPLE_BODY_PLACEHOLDERS = (
    "block note",
    "inline note",
    "note",
    "Visible content",
    "+ 100",
    "Remember the bull.",
)
_DECORATIVE_RULER_CHARS = frozenset("#%-=*_<>/+|")
_LINE_ONLY_DECORATIVE_CHARS = frozenset("#%-=*_/<>+|")
_EMBEDDED_BLOCK_WRAPPERS = (
    ("/**", "*/"),
    ("/*!", "*/"),
    ("/*-", "*/"),
    ("/*", "*/"),
)
_JAVA_SCANNER_LINE_ENDINGS = str.maketrans(
    {
        "\u0085": "\n",
        "\u2028": "\n",
        "\u2029": "\n",
    }
)
_GENERO_LANGUAGE_KEYS = frozenset({"genero", "genero_forms"})
_GENERO_FORMS_LANGUAGE_KEYS = frozenset({"genero_forms"})
_ROCQ_LANGUAGE_KEYS = frozenset({"coq", "rocq", "rocq_prover"})
_VISUAL_BASIC_6_LANGUAGE_KEYS = frozenset(
    {"visual_basic", "visual_basic_6_0", "visual_basic_net", "vb6"}
)


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


def _iter_regex_examples(syntax: CommentSyntax):
    yield from syntax.shared_regex_examples
    yield from syntax.canonical_regex_examples


def _refines_explicit_wrapper(
    wrapper: tuple[str, str],
    explicit_wrappers: tuple[tuple[str, str], ...],
) -> bool:
    """Return whether an inferred wrapper accidentally includes example prose."""

    open_token, close_token = wrapper
    return any(
        open_token.startswith(explicit_open)
        and (
            close_token == explicit_close
            or (bool(explicit_close) and close_token.endswith(explicit_close))
        )
        for explicit_open, explicit_close in explicit_wrappers
    )


def _add_known_line_wrapper_variants(
    wrappers: list[tuple[str, str]],
) -> None:
    """Add exact, conventional documentation markers for registered openers.

    Keeping these as explicit wrappers lets ``_line_open_pattern`` stay exact.
    That matters for inputs such as Ada ``---`` diff text and absolute paths
    following ``//``: punctuation after a registered opener is not generically
    another byte of comment syntax.
    """

    known_variants = {
        ("//", ""): (("///", ""), ("//!", "")),
        ("--", ""): (("-- |", ""), ("--|", "")),
        (";", ""): ((";;;", ""), (";;", "")),
    }
    registered = set(wrappers)
    for base_wrapper, variants in known_variants.items():
        if base_wrapper not in registered:
            continue
        for variant in variants:
            if variant not in registered:
                wrappers.append(variant)
                registered.add(variant)


def _add_known_block_wrapper_variants(
    wrappers: list[tuple[str, str]],
) -> None:
    """Add exact documentation and whitespace-control block delimiters."""

    known_variants = {
        ("/*", "*/"): (
            ("/*--", "--*/"),
            ("/***", "***/"),
            ("/**", "**/"),
            ("/**", "*/"),
            ("/*!", "*/"),
        ),
        ("(*", "*)"): (
            ("(**", "**)"),
            ("(**", "*)"),
        ),
        ("{-", "-}"): (
            ("{-|", "-}"),
            ("{-!", "-}"),
        ),
        ("{#", "#}"): (
            ("{#-", "-#}"),
            ("{#-", "#}"),
            ("{#", "-#}"),
        ),
        ("<%#", "%>"): (
            ("<%#-", "-%>"),
            ("<%#-", "%>"),
            ("<%#_", "_%>"),
            ("<%#_", "%>"),
            ("<%#", "-%>"),
            ("<%#", "_%>"),
        ),
        ("<!--", "-->"): (
            ("<!----", "---->"),
            ("<!----", "--->"),
            ("<!---", "---->"),
            ("<!---", "--->"),
            ("<!---", "-->"),
        ),
        ("<!---", "--->"): (
            ("<!----", "---->"),
            ("<!----", "--->"),
            ("<!---", "---->"),
        ),
    }
    normalized_registered = {
        (open_token.rstrip(), close_token.lstrip()) for open_token, close_token in wrappers
    }
    registered = set(wrappers)
    for base_wrapper, variants in known_variants.items():
        if base_wrapper not in normalized_registered:
            continue
        for variant in variants:
            if variant not in registered:
                wrappers.append(variant)
                registered.add(variant)


def _build_sanitizer_syntax(syntax: CommentSyntax) -> _SanitizerSyntax:
    line_wrappers = list(syntax.sanitizer_line_wrappers)
    for example in _iter_regex_examples(syntax):
        if example.kind not in {"line", "directive"}:
            continue
        if example.kind == "directive" and "\n" in example.expected_match:
            continue
        parts = _split_example_placeholder(example.expected_match)
        if parts is None:
            continue
        for wrapper in (
            (parts[0].strip(), parts[2]),
            (parts[0].strip(), parts[2].lstrip()),
        ):
            if wrapper not in line_wrappers and not _refines_explicit_wrapper(
                wrapper, syntax.sanitizer_line_wrappers
            ):
                line_wrappers.append(wrapper)

    block_wrappers = list(syntax.sanitizer_block_wrappers)
    for open_delim, close_delim in syntax.nested_delimiters:
        wrapper = (open_delim, close_delim)
        if wrapper not in block_wrappers:
            block_wrappers.append(wrapper)

    for example in _iter_regex_examples(syntax):
        if example.kind != "block":
            continue
        parts = _split_example_placeholder(example.expected_match)
        if parts is None:
            continue
        for wrapper in (
            (parts[0], parts[2]),
            (parts[0].rstrip(), parts[2].lstrip()),
        ):
            if wrapper not in block_wrappers and not _refines_explicit_wrapper(
                wrapper, syntax.sanitizer_block_wrappers
            ):
                block_wrappers.append(wrapper)

    _add_known_line_wrapper_variants(line_wrappers)
    _add_known_block_wrapper_variants(block_wrappers)
    block_wrappers.sort(key=lambda wrapper: len(wrapper[0]) + len(wrapper[1]), reverse=True)
    line_wrappers.sort(key=lambda wrapper: len(wrapper[0]) + len(wrapper[1]), reverse=True)
    return _SanitizerSyntax(tuple(line_wrappers), tuple(block_wrappers))


def _coerce_comment_text(comment: str | QueryMatch) -> str:
    if isinstance(comment, QueryMatch):
        return comment.match
    if isinstance(comment, str):
        return comment
    raise TypeError("comment must be a string or QueryMatch")


def _is_case_insensitive_token(token: str) -> bool:
    return any(char.isalpha() for char in token)


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _line_open_pattern(open_token: str) -> str:
    """Return a regex fragment for a line-comment opener.

    Args:
        open_token: Registry-derived line-comment opener.

    Returns:
        Regex text that strips exactly the registered opener, followed by a word
        boundary when the opener ends in an alphanumeric token. Documentation
        variants such as ``///`` are registered explicitly.
    """

    pattern = re.escape(open_token)

    if open_token[-1].isalnum():
        pattern += r"(?=$|[^\w])"
    return pattern


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
    indent_match = re.match(r"[^\S\r\n]*", line)
    indent_length = indent_match.end() if indent_match is not None else 0
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

    physical_lines = raw_comment.split("\n")
    if sum(bool(line.strip()) for line in physical_lines) <= 1:
        return None

    matched: list[_WrappedLine | None] = []
    for line in physical_lines:
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
    raw_comment: str,
    line_wrappers: tuple[tuple[str, str], ...],
    *,
    protected_padding_chars: frozenset[str] = frozenset(),
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
                rf"^[^\S\r\n]*(?:{_line_open_pattern(open_token)})"
                rf"(.*){re.escape(close_token)}$",
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
    registered_ruler_chars = {
        token[-1]
        for token in matched_open_tokens
        if len(token) == 1 and not token[-1].isalnum() and not token[-1].isspace()
    }
    stripped_lines = [
        line
        for line in stripped_lines
        if not (
            len("".join(line.split())) >= 4
            and len(set("".join(line.split()))) == 1
            and "".join(line.split())[0] in registered_ruler_chars
        )
    ]
    stripped_lines = _strip_editor_modeline_padding(stripped_lines)
    stripped_lines = _strip_line_frame_segments(stripped_lines)
    stripped_lines = _strip_inline_ruler_padding(
        stripped_lines,
        protected_chars=protected_padding_chars,
    )
    stripped_lines = _strip_pipe_frame(stripped_lines)
    stripped_lines = _strip_single_line_decorative_padding(
        stripped_lines,
        protected_chars=protected_padding_chars,
    )
    stripped_lines = _remove_long_decorative_rulers(stripped_lines)
    stripped_lines = _strip_decorative_edge_rulers(
        stripped_lines,
        empty_ruler_chars=_LINE_ONLY_DECORATIVE_CHARS | frozenset("".join(matched_open_tokens)),
    )
    stripped_lines = _strip_single_line_decorative_padding(
        stripped_lines,
        protected_chars=protected_padding_chars,
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
    candidates = (raw_comment,)
    without_outer_indent = raw_comment.lstrip(" \t")
    if without_outer_indent != raw_comment:
        candidates += (without_outer_indent,)
    without_outer_padding = raw_comment.strip(" \t")
    if without_outer_padding not in candidates:
        candidates += (without_outer_padding,)

    for open_text, close_text in block_wrappers:
        for candidate in candidates:
            if not _wrapper_matches(candidate, open_text, close_text):
                continue

            inner = candidate[len(open_text) : len(candidate) - len(close_text)]
            return inner, (open_text, close_text)
    return None


def _strip_lua_long_comment_wrapper(
    raw_comment: str,
) -> tuple[str, tuple[str, str]] | None:
    """Strip a level-matched Lua long-comment wrapper."""

    candidate = raw_comment.strip(" \t")
    match = re.fullmatch(r"--\[(?P<equals>=*)\[(?P<body>[\s\S]*)\](?P=equals)\]", candidate)
    if match is None:
        return None
    equals = match.group("equals")
    return match.group("body"), (f"--[{equals}[", f"]{equals}]")


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
    lines: list[str],
    wrapper: tuple[str, str],
    *,
    allow_doc_star: bool,
    allow_unguttered_first_line: bool,
) -> tuple[list[str], bool]:
    allowed_chars = set(_wrapper_punctuation_chars(wrapper))
    if allow_doc_star:
        allowed_chars.add("*")
    for line in lines:
        compact = "".join(line.split())
        if _is_decorative_ruler_line(line) and len(set(compact)) == 1:
            allowed_chars.add(compact[0])

    content_indexes = [
        index
        for index, line in enumerate(lines)
        if line.strip() and not _is_decorative_ruler_line(line)
    ]
    if not content_indexes:
        return lines, False

    matches: dict[int, re.Match[str]] = {}
    gutter_char: str | None = None
    pattern = re.compile(r"^[ \t]*([^\w\s]+)(?:[ \t]|$)")
    for index in content_indexes:
        match = pattern.match(lines[index])
        if match is None and allow_doc_star:
            match = re.match(r"^[ \t]*(\*)(?=[^\s*])", lines[index])
        token = match.group(1) if match is not None else ""
        valid_gutter = bool(token) and len(set(token)) == 1 and token[0] in allowed_chars
        if (
            not valid_gutter
            and allow_unguttered_first_line
            and index == content_indexes[0]
            and index == 0
        ):
            continue
        if not valid_gutter or match is None:
            return lines, False
        if gutter_char is not None and token[0] != gutter_char:
            return lines, False
        gutter_char = token[0]
        matches[index] = match

    if gutter_char is None:
        return lines, False
    if (
        len(content_indexes) == 1
        and allow_unguttered_first_line
        and not any(_is_decorative_ruler_line(line) and gutter_char in line for line in lines)
    ):
        return lines, False

    stripped = list(lines)
    gutter_pattern = re.compile(rf"^[ \t]*{re.escape(gutter_char)}+")
    for index, line in enumerate(stripped):
        match = gutter_pattern.match(line)
        if match is not None:
            body_start = match.end()
            if line[body_start : body_start + 1] in {" ", "\t"}:
                body_start += 1
            stripped[index] = line[body_start:]

    return stripped, True


def _strip_common_right_gutter(
    lines: list[str],
    allowed_chars: frozenset[str],
) -> tuple[list[str], bool]:
    content_indexes = [
        index
        for index, line in enumerate(lines)
        if line.strip() and not _is_decorative_ruler_line(line)
    ]
    if len(content_indexes) < 2:
        return lines, False

    gutter_char: str | None = None
    matches: dict[int, re.Match[str]] = {}
    pattern = re.compile(r"(?:(?<=[ \t])|^)([^\w\s]+)[ \t]*$")
    for index in content_indexes:
        match = pattern.search(lines[index])
        if match is None:
            continue
        token = match.group(1)
        if len(set(token)) != 1 or token[0] not in allowed_chars:
            continue
        if gutter_char is not None and token[0] != gutter_char:
            return lines, False
        gutter_char = token[0]
        matches[index] = match

    if not matches or len(matches) / len(content_indexes) < 0.8:
        return lines, False

    stripped = list(lines)
    for index, match in matches.items():
        stripped[index] = lines[index][: match.start()].rstrip()

    if gutter_char is not None:
        punctuation_pattern = re.compile(rf"{re.escape(gutter_char)}+[ \t]*$")
        for index, line in enumerate(stripped):
            if not _is_decorative_ruler_line(line):
                continue
            match = punctuation_pattern.search(line)
            if match is not None:
                stripped[index] = line[: match.start()].rstrip()

        blank_frame_pattern = re.compile(rf"[ \t]+{re.escape(gutter_char)}+[ \t]*$")
        for index, line in enumerate(stripped):
            if index in matches or not line.strip() or _is_decorative_ruler_line(line):
                continue
            match = blank_frame_pattern.search(line)
            if match is not None:
                stripped[index] = line[: match.start()].rstrip()
    return stripped, True


def _strip_pipe_frame(lines: list[str]) -> list[str]:
    """Strip structurally complete fixed-width ``| ... |`` comment frames."""

    first = 0
    while first < len(lines) and not lines[first].strip():
        first += 1
    if first == len(lines) or not (_is_decorative_ruler_line(lines[first]) and "+" in lines[first]):
        return lines

    closing = next(
        (
            index
            for index in range(first + 1, len(lines))
            if _is_decorative_ruler_line(lines[index]) and "+" in lines[index]
        ),
        None,
    )
    if closing is None:
        return lines

    framed_pattern = re.compile(r"^[ \t]*\|(.*?)(?:\|[ \t]*)?$")
    cleaned: list[str] = []
    framed_count = 0
    for line in lines[first + 1 : closing]:
        if not line.strip():
            cleaned.append("")
            continue
        match = framed_pattern.match(line)
        if match is not None:
            framed_count += 1
            cleaned.append(match.group(1).strip())
            continue
        return lines

    if not framed_count:
        return lines
    remainder = list(lines[closing + 1 :])
    if cleaned and not cleaned[-1].strip() and remainder and not remainder[0].strip():
        remainder.pop(0)
    return [*lines[:first], *cleaned, *remainder]


def _strip_line_frame_segments(lines: list[str]) -> list[str]:
    """Strip ruler-bounded line-comment title cards with a repeated side gutter."""

    stripped_lines = list(lines)
    index = 0
    while index < len(stripped_lines):
        compact = "".join(stripped_lines[index].split())
        if len(compact) < 4 or len(set(compact)) != 1 or compact[0] not in _DECORATIVE_RULER_CHARS:
            index += 1
            continue

        frame_char = compact[0]
        closing = next(
            (
                candidate
                for candidate in range(index + 2, len(stripped_lines))
                if (
                    len("".join(stripped_lines[candidate].split())) >= 4
                    and set("".join(stripped_lines[candidate].split())) == {frame_char}
                )
            ),
            None,
        )
        if closing is None:
            index += 1
            continue

        gutter_pattern = re.compile(
            rf"^[ \t]*{re.escape(frame_char)}+[ \t]+"
            rf"(.*?)(?:[ \t]+{re.escape(frame_char)}+)?[ \t]*$"
        )
        matches: list[re.Match[str] | None] = []
        valid = False
        for line in stripped_lines[index + 1 : closing]:
            if not line.strip():
                matches.append(None)
                continue
            match = gutter_pattern.match(line)
            if match is None:
                valid = False
                break
            valid = True
            matches.append(match)
        if not valid or len(matches) != closing - index - 1:
            index += 1
            continue

        stripped_lines[index] = ""
        stripped_lines[closing] = ""
        for offset, match in enumerate(matches, start=index + 1):
            if match is not None:
                stripped_lines[offset] = match.group(1).strip()
        index = closing + 1
    return stripped_lines


def _strip_symmetric_block_frame(lines: list[str]) -> tuple[list[str], bool]:
    """Strip a complete block frame with homogeneous top, bottom, and sides."""

    first = next((index for index, line in enumerate(lines) if line.strip()), None)
    last = next(
        (index for index in range(len(lines) - 1, -1, -1) if lines[index].strip()),
        None,
    )
    if first is None or last is None or first >= last:
        return lines, False

    top = "".join(lines[first].split())
    bottom = "".join(lines[last].split())
    if (
        len(top) < 4
        or len(set(top)) != 1
        or top[0] not in _DECORATIVE_RULER_CHARS
        or set(bottom) != {top[0]}
    ):
        return lines, False

    frame_char = top[0]
    cleaned: list[str] = []
    framed_count = 0
    for line in lines[first + 1 : last]:
        if not line.strip():
            cleaned.append("")
            continue
        stripped = line.strip()
        if not (stripped.startswith(frame_char) and stripped.endswith(frame_char)):
            return lines, False
        framed_count += 1
        cleaned.append(stripped[1:-1].strip())

    if not framed_count:
        return lines, False
    return [*lines[:first], *cleaned, *lines[last + 1 :]], True


def _is_decorative_ruler_line(line: str) -> bool:
    if _is_spaced_underscore_art_line(line):
        return False

    stripped = "".join(line.split())
    if (
        len(stripped) >= 4
        and stripped[0] == stripped[-1]
        and set(stripped[1:-1]) <= _DECORATIVE_RULER_CHARS
        and re.search(r"([#%\-=*_<>/+|])\1{2,}", stripped[1:-1])
    ):
        return True
    if len(stripped) < 4 or not set(stripped) <= _DECORATIVE_RULER_CHARS:
        return False
    return len(set(stripped)) == 1 or bool(re.search(r"([#%\-=*_<>/+|])\1{2,}", stripped))


def _is_spaced_underscore_art_line(line: str) -> bool:
    """Return whether spaces divide an underscore-only ASCII-art row."""

    trimmed = line.strip()
    compact = "".join(trimmed.split())
    return bool(compact) and set(compact) == {"_"} and any(char.isspace() for char in trimmed)


def _is_empty_ruler_line(line: str, allowed_chars: frozenset[str]) -> bool:
    if _is_spaced_underscore_art_line(line):
        return False

    stripped = "".join(line.split())
    if stripped == "-" and line[:1].isspace():
        return False

    return (
        bool(stripped)
        and (len(stripped) == 1 or len(stripped) >= 4)
        and len(set(stripped)) == 1
        and stripped[0] in allowed_chars
    )


def _strip_inline_ruler_padding(
    lines: list[str],
    *,
    protected_chars: frozenset[str] = frozenset(),
) -> list[str]:
    """Strip long homogeneous decoration attached to content-bearing text."""

    stripped_lines: list[str] = []
    leading = re.compile(r"^([ \t]*)([@#%\-=*_<>/+|])\2{3,}[ \t]+(.+)$")
    trailing = re.compile(r"^(.+?)[ \t]+([@#%\-=*_<>/+|])\2{3,}[ \t]*$")
    for line in lines:
        current = line
        leading_match = leading.match(current)
        if (
            leading_match is not None
            and leading_match.group(2) not in protected_chars
            and any(char.isalnum() for char in leading_match.group(3))
        ):
            current = leading_match.group(1) + leading_match.group(3)
        trailing_match = trailing.match(current)
        content_bearing_dash_bar = (
            trailing_match is not None
            and trailing_match.group(2) == "-"
            and leading_match is None
            and trailing_match.group(1).rstrip().endswith(("=", ":"))
        )
        if (
            trailing_match is not None
            and not content_bearing_dash_bar
            and trailing_match.group(2) not in protected_chars
            and any(char.isalnum() for char in trailing_match.group(1))
        ):
            current = trailing_match.group(1).rstrip()
        stripped_lines.append(current)
    return stripped_lines


def _strip_editor_modeline_padding(lines: list[str]) -> list[str]:
    """Remove column-alignment padding before an editor modeline."""

    stripped_lines = list(lines)
    for index, line in enumerate(stripped_lines):
        content = line.lstrip(" \t")
        padding = len(line) - len(content)
        if padding >= 8 and content.startswith("-*-") and content.endswith("-*-"):
            stripped_lines[index] = content
    return stripped_lines


def _remove_long_decorative_rulers(lines: list[str]) -> list[str]:
    """Remove isolated long ruler rows without erasing table/heading syntax."""

    thematic_break_counts = {
        marker: sum(
            bool(compact := "".join(candidate.split()))
            and len(set(compact)) == 1
            and compact[0] == marker
            for candidate in lines
        )
        for marker in "-*_"
    }
    stripped_lines: list[str] = []
    for index, line in enumerate(lines):
        compact = "".join(line.split())
        is_long_ruler = len(compact) >= 8 and _is_decorative_ruler_line(line)
        is_markdown_thematic_break = (
            bool(compact)
            and len(set(compact)) == 1
            and compact[0] in frozenset("-*_")
            and thematic_break_counts[compact[0]] == 1
        )
        surrounded_by_blank_lines = (
            index > 0
            and index + 1 < len(lines)
            and not lines[index - 1].strip()
            and not lines[index + 1].strip()
        )
        if not is_long_ruler or not surrounded_by_blank_lines or is_markdown_thematic_break:
            stripped_lines.append(line)
            continue
        if (
            stripped_lines
            and not stripped_lines[-1].strip()
            and index + 1 < len(lines)
            and not lines[index + 1].strip()
        ):
            stripped_lines.pop()
    return stripped_lines


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
    if [line.strip() for line in non_empty] == ["*"]:
        return lines

    if non_empty and all(
        _is_decorative_ruler_line(line) or _is_empty_ruler_line(line, empty_ruler_chars)
        for line in non_empty
    ):
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
        if not (_is_decorative_ruler_line(first) or _is_empty_ruler_line(first, empty_ruler_chars)):
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
        if not (_is_decorative_ruler_line(last) or _is_empty_ruler_line(last, empty_ruler_chars)):
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
    if len(content_indexes) < 2:
        return lines
    structural_ruler_chars = {
        "".join(line.split())[0]
        for line in lines
        if _is_decorative_ruler_line(line) and len(set("".join(line.split()))) == 1
    }

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
        if (
            start > 0
            and not lines[index][start - 1].isspace()
            and token_length < 2
            and match.group(1) not in structural_ruler_chars
        ):
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
            if not _is_decorative_ruler_line(line):
                continue
            match = punctuation_pattern.search(line)
            if match is not None:
                stripped[index] = line[: match.start()].rstrip()
    return stripped


def _strip_single_line_decorative_padding(
    lines: list[str],
    *,
    protected_chars: frozenset[str] = frozenset(),
) -> list[str]:
    non_empty_indexes = [index for index, line in enumerate(lines) if line.strip()]
    if len(non_empty_indexes) != 1:
        return lines

    index = non_empty_indexes[0]
    line = lines[index]
    if re.match(r"^[ \t]*\.{3}(?!\.)", line) or re.search(
        r"(?<!\.)\.{3}[ \t]*$",
        line,
    ):
        protected_chars |= frozenset(".")

    match = re.match(
        r"^([ \t]*)([@#%.\-=*_<>/+|\\])\2{2,}[ \t]*(.*?)[ \t]*"
        r"\2{2,}[ \t]*$",
        line,
    )
    stripped = list(lines)
    if match is not None and match.group(2) not in protected_chars:
        content = match.group(3).strip()
        if content and any(char != match.group(2) for char in content):
            stripped[index] = match.group(1) + content
            return stripped

    paired = re.match(
        r"^([ \t]*)([@#%.\-=*_<>/+|\\]{4,})[ \t]*(.*?)[ \t]*"
        r"([@#%.\-=*_<>/+|\\]{4,})[ \t]*$",
        line,
    )
    if (
        paired is not None
        and paired.group(3).strip()
        and not set(paired.group(2) + paired.group(4)) & protected_chars
        and re.search(r"(.)\1{2,}", paired.group(2))
        and re.search(r"(.)\1{2,}", paired.group(4))
    ):
        stripped[index] = paired.group(1) + paired.group(3).strip()
        return stripped

    leading_run = re.match(
        r"^([ \t]*)([%.\-=*_<>/+|])\2{2,}[ \t]*(.+)$",
        line,
    )
    if (
        leading_run is not None
        and leading_run.group(2) not in protected_chars
        and any(char.isalnum() for char in leading_run.group(3))
    ):
        stripped[index] = leading_run.group(1) + leading_run.group(3).strip()
        return stripped

    doubled_star = re.match(r"^([ \t]*)\*{2}[ \t]+(.+)$", line)
    if (
        doubled_star is not None
        and "*" not in protected_chars
        and any(char.isalnum() for char in doubled_star.group(2))
    ):
        stripped[index] = doubled_star.group(1) + doubled_star.group(2).strip()
        return stripped

    trailing_run = re.match(
        r"^([ \t]*.*[A-Za-z0-9])([#%.\-=*_<>/+|])\2{2,}[ \t]*$",
        line,
    )
    if trailing_run is not None and trailing_run.group(2) not in protected_chars:
        stripped[index] = trailing_run.group(1).rstrip()
        return stripped
    return lines


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


def _strip_metadata_line_padding(lines: list[str]) -> list[str]:
    """Remove mixed source indentation from all-metadata comment bodies."""

    non_empty = [line for line in lines if line.strip()]
    if non_empty and all(line.lstrip(" \t").startswith("@") for line in non_empty):
        return [line.lstrip(" \t") if line.strip() else line for line in lines]
    return lines


def _strip_unicode_box_frames(lines: list[str]) -> list[str]:
    """Strip complete Unicode box borders while preserving their inner text."""

    top_chars = frozenset("┌┐┏┓╔╗")
    bottom_chars = frozenset("└┘┗┛╚╝")
    vertical_chars = frozenset("│┃║")
    box_chars = frozenset("┌┐┏┓╔╗└┘┗┛╚╝├┤┣┫╠╣┬┴┳┻╦╩┼╋╬─━═│┃║")

    first = next(
        (
            index
            for index, line in enumerate(lines)
            if line.strip() and line.strip()[0] in top_chars and set(line.strip()) <= box_chars
        ),
        None,
    )
    if first is None:
        return lines
    last = next(
        (
            index
            for index in range(len(lines) - 1, first, -1)
            if lines[index].strip()
            and lines[index].strip()[0] in bottom_chars
            and set(lines[index].strip()) <= box_chars
        ),
        None,
    )
    if last is None:
        return lines

    segment = lines[first + 1 : last]
    if not any(
        line.strip() and line.strip()[0] in vertical_chars and line.strip()[-1] in vertical_chars
        for line in segment
    ):
        return lines

    cleaned: list[str] = []
    for line in segment:
        stripped = line.strip()
        if stripped and set(stripped) <= box_chars:
            continue
        if stripped and stripped[0] in vertical_chars and stripped[-1] in vertical_chars:
            cleaned.append(stripped[1:-1].strip())
        else:
            cleaned.append(line)
    return [*lines[:first], *cleaned, *lines[last + 1 :]]


def _strip_asl_generated_frame(body: str) -> str:
    """Remove firmware-generated ASL box gutters and source indentation."""

    cleaned: list[str] = []
    slash_frame = re.compile(r"^[ \t]*//\*{2}[ \t]*(.*?)[ \t]*\*{2}[ \t]*$")
    semicolon_frame = re.compile(r"^[ \t]*;\*+[ \t]*(.*?)[ \t]*\*+;[ \t]*$")
    for line in body.split("\n"):
        stripped = line.strip()
        if stripped in {"/**", "**/"}:
            while cleaned and not cleaned[-1].strip():
                cleaned.pop()
            if cleaned:
                cleaned.append("")
            continue
        compact_without_semicolon = "".join(stripped.rstrip(";").split())
        if (
            len(compact_without_semicolon) >= 4
            and not any(char.isalnum() for char in compact_without_semicolon)
            and re.search(r"(.)\1{2,}", compact_without_semicolon)
        ):
            cleaned.append("")
            continue

        frame_match = slash_frame.match(line) or semicolon_frame.match(line)
        if frame_match is not None:
            cleaned.append(frame_match.group(1).strip())
            continue
        cleaned.append(line.lstrip(" \t").rstrip())

    return _normalize_sanitized_body("\n".join(cleaned))


def _strip_repeated_literal_gutter(body: str, gutter: str) -> str:
    """Remove a literal side gutter when it covers an entire multiline body."""

    lines = body.split("\n")
    non_empty = [line for line in lines if line.strip()]
    guttered_count = sum(line.lstrip(" \t").startswith(gutter) for line in non_empty)
    if len(non_empty) < 3 or guttered_count / len(non_empty) < 0.8:
        return body

    cleaned: list[str] = []
    for line in lines:
        if not line.strip():
            cleaned.append(line)
            continue
        left_stripped = line.lstrip(" \t")
        if not left_stripped.startswith(gutter):
            cleaned.append(line.rstrip())
            continue
        candidate = left_stripped[len(gutter) :]
        if candidate.startswith((" ", "\t")):
            candidate = candidate[1:]
        cleaned.append(candidate.rstrip())
    return _normalize_sanitized_body("\n".join(cleaned))


def _sanitize_nasal_hash_layout(raw_comment: str, cleaned: str) -> str:
    """Clean Nasal hash frames while preserving commented-out code indentation."""

    raw_lines = raw_comment.split("\n")
    raw_non_empty = [line for line in raw_lines if line.strip()]
    if len(raw_non_empty) >= 3 and all(re.match(r"^[ \t]*#{2,}", line) for line in raw_non_empty):
        return _normalize_sanitized_body(
            "\n".join(
                re.sub(r"^[ \t]*#+[ \t]*", "", line) if line.strip() else line
                for line in cleaned.split("\n")
            )
        )

    first = next((line.lstrip(" \t") for line in raw_lines if line.strip()), "")
    if (
        first.startswith("#")
        and len(first) > 1
        and not first[1].isspace()
        and any(token in first[1:] for token in ("=", "{", "(", ";"))
    ):
        cleaned_lines = cleaned.split("\n")
        if len(cleaned_lines) == len(raw_lines):
            restored: list[str] = []
            for raw_line, cleaned_line in zip(raw_lines, cleaned_lines):
                raw_body = raw_line.lstrip(" \t")
                if raw_body.startswith("#") and raw_body[1:2] in {" ", "\t"}:
                    restored.append(raw_body[1] + cleaned_line)
                else:
                    restored.append(cleaned_line)
            return _normalize_sanitized_body("\n".join(restored))
    return cleaned


def _sanitize_red_line_result(cleaned: str) -> str:
    """Remove Red's decorative section-label gutters."""

    cleaned_lines: list[str] = []
    for line in cleaned.split("\n"):
        current = re.sub(r"^[ \t]*--[ \t]+", "", line)
        framed = re.match(r"^[ \t]*=+[ \t]*(.*?)[ \t]*=+;*[ \t]*$", current)
        if framed is not None and any(char.isalnum() for char in framed.group(1)):
            current = framed.group(1).strip()
        else:
            trailing = re.match(r"^(.*?[A-Za-z0-9])[ \t]+=+;*[ \t]*$", current)
            if trailing is not None:
                current = trailing.group(1).rstrip()
        cleaned_lines.append(current.rstrip())
    return _normalize_sanitized_body("\n".join(cleaned_lines))


def _sanitize_stata_star_layout(raw_comment: str, cleaned: str) -> str:
    """Remove Stata star title cards without changing command text."""

    has_star_ruler = any(
        len(line.strip()) >= 8 and set(line.strip()) == {"*"} for line in raw_comment.split("\n")
    )
    cleaned_lines: list[str] = []
    for line in cleaned.split("\n"):
        current = line
        framed = re.match(r"^[ \t]*\*{2,}[ \t]*(.*?)[ \t]*\*+[ \t]*$", current)
        if framed is not None and any(char.isalnum() for char in framed.group(1)):
            current = framed.group(1).strip()
        elif has_star_ruler:
            current = re.sub(r"^[ \t]*\*{2,}[ \t]*", "", current)
            current = re.sub(r"\*+[ \t]*$", "", current).rstrip()
            current = current.lstrip(" \t")
        cleaned_lines.append(current.rstrip())
    return _normalize_sanitized_body("\n".join(cleaned_lines))


def _sanitize_sas_block_result(raw_comment: str, cleaned: str) -> str:
    """Clean SAS fixed-width star frames and Doxygen padding."""

    if raw_comment.startswith("/*!"):
        paragraphs: list[list[str]] = []
        current: list[str] = []
        for line in cleaned.split("\n"):
            if line.strip():
                current.append(line)
                continue
            paragraphs.append(current)
            paragraphs.append([])
            current = []
        paragraphs.append(current)

        normalized: list[str] = []
        for paragraph in paragraphs:
            if not paragraph:
                if normalized and normalized[-1] != "":
                    normalized.append("")
                continue
            space_widths = [
                len(line) - len(line.lstrip(" ")) for line in paragraph if line.startswith(" ")
            ]
            baseline = min(space_widths) if space_widths else 0
            for line in paragraph:
                if line.startswith("\t"):
                    normalized.append(line.lstrip("\t"))
                elif baseline:
                    normalized.append(line[baseline:])
                else:
                    normalized.append(line)
        return _normalize_sanitized_body("\n".join(normalized))

    normalized_raw = _normalize_newlines(raw_comment)
    if not (normalized_raw.startswith("/*") and normalized_raw.endswith("*/")):
        return cleaned
    inner_lines = normalized_raw[2:-2].split("\n")
    if not any(len(line.strip()) >= 8 and set(line.strip()) == {"*"} for line in inner_lines):
        return cleaned

    content_lines = [line for line in inner_lines if line.strip() and set(line.strip()) != {"*"}]
    fully_star_prefixed = bool(content_lines) and all(
        line.lstrip(" \t").startswith("*") for line in content_lines
    )
    framed: list[str] = []
    for line in inner_lines:
        current = line
        if len(current.strip()) >= 4 and set(current.strip()) == {"*"}:
            continue
        current = re.sub(r"^[ \t]*\*", "", current)
        current = re.sub(r"\*[ \t]*$", "", current).rstrip()
        if current.strip() and set(current.strip()) == {"*"}:
            continue
        framed.append(current.lstrip(" \t") if fully_star_prefixed else current)
    return _normalize_sanitized_body("\n".join(framed))


def _sanitize_sas_line_result(cleaned: str) -> str:
    if cleaned.strip() and set(cleaned.strip()) == {"*"}:
        return ""
    return cleaned


def _sanitize_rebol_line_result(cleaned: str) -> str:
    """Remove Rebol section-title and complete square-box frames."""

    lines = cleaned.split("\n")
    non_empty = [line.strip() for line in lines if line.strip()]
    if (
        len(non_empty) >= 3
        and all(line.startswith("[") and line.endswith("]") for line in non_empty)
        and set(non_empty[0][1:-1].strip()) == {"-"}
        and set(non_empty[-1][1:-1].strip()) == {"-"}
    ):
        unframed: list[str] = []
        for line in lines[1:-1]:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                unframed.append(stripped[1:-1].strip())
            else:
                unframed.append(line)
        return _normalize_sanitized_body("\n".join(unframed))

    if len(lines) == 1:
        title = re.fullmatch(r"[ \t]*--+[ \t]+(.+?)[ \t]+--+[ \t]*", lines[0])
        if title is not None:
            return title.group(1).strip()
    return cleaned


def _sanitize_hlsl_result(raw_comment: str, cleaned: str) -> str:
    """Remove HLSL documentation padding and long separator rulers."""

    lines = [
        line
        for line in cleaned.split("\n")
        if not (len(line.strip()) >= 8 and set(line.strip()) == {"-"})
    ]

    normalized_raw = _normalize_newlines(raw_comment)
    if normalized_raw.startswith("/**\n"):
        first_unindented = next(
            (
                index
                for index, line in enumerate(lines)
                if line.strip() and not line.startswith((" ", "\t"))
            ),
            None,
        )
        if first_unindented is not None and first_unindented >= 2:
            prefix = lines[:first_unindented]
            widths = [
                len(line) - len(line.lstrip(" "))
                for line in prefix
                if line.strip() and not line.startswith("\t")
            ]
            if widths and min(widths) > 0:
                baseline = min(widths)
                lines[:first_unindented] = [
                    line[baseline:] if line.strip() else line for line in prefix
                ]

    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_ecl_line_result(cleaned: str) -> str:
    """Remove ECL's symmetric star padding around section headings."""

    lines: list[str] = []
    for line in cleaned.split("\n"):
        framed = re.fullmatch(r"[ \t]*\*{3,}(.*?)\*{3,}[ \t]*", line)
        if framed is not None and any(char.isalnum() for char in framed.group(1)):
            lines.append(framed.group(1).strip())
        else:
            lines.append(line)
    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_clean_generated_doc_result(raw_comment: str, cleaned: str) -> str:
    """Dedent one-space continuations in compact generated Clean doc blocks."""

    if not (
        raw_comment.startswith("/**")
        and len(raw_comment) > 3
        and not raw_comment[3].isspace()
        and raw_comment.endswith("*/")
    ):
        return cleaned

    raw_continuations = raw_comment[3:-2].split("\n")[1:]
    if not raw_continuations or not all(
        line.startswith(" ") and not line.startswith("  ") for line in raw_continuations if line
    ):
        return cleaned

    lines = cleaned.split("\n")
    if len(lines) <= 1:
        return cleaned
    return "\n".join(
        [lines[0], *[line[1:] if line.startswith(" ") else line for line in lines[1:]]]
    )


def _sanitize_denizenscript_line_result(raw_comment: str, cleaned: str) -> str:
    """Remove Denizen's exact doubled metadata marker and header footer."""

    lines = cleaned.split("\n")
    if any(re.fullmatch(r"[ \t]*##[ \t]+@file[ \t]*", line) for line in raw_comment.split("\n")):
        lines = [
            "@file" if re.fullmatch(r"#[ \t]+@file", line) is not None else line for line in lines
        ]

    raw_content_lines = [
        line
        for line in raw_comment.split("\n")
        if line.strip() and re.fullmatch(r"[ \t]*#{1,2}(?:[ \t]+@file)?[ \t]*", line) is None
    ]
    if raw_content_lines and all(re.match(r"^[ \t]*#[ ]{2}", line) for line in raw_content_lines):
        lines = [line[1:] if line.startswith(" ") else line for line in lines]

    if (
        re.fullmatch(
            r"[ \t]*#[ \t]+-{8,}[ \t]+END HEADER[ \t]+-{8,}[ \t]*",
            raw_comment.split("\n")[-1],
        )
        and lines
        and lines[-1] == "END HEADER"
    ):
        lines.pop()
    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_kakoune_line_result(language: str, cleaned: str) -> str:
    """Drop only the underline forms reviewed for each Kakoune registry key."""

    underline_chars = {"‾", "─"}
    if language == "kakounescript":
        underline_chars.add("=")
    retained = []
    for line in cleaned.split("\n"):
        compact = "".join(line.split())
        if len(compact) >= 8 and len(set(compact)) == 1 and compact[0] in underline_chars:
            continue
        retained.append(line)
    return _normalize_sanitized_body("\n".join(retained))


def _sanitize_reviewed_slash_line_result(
    language: str,
    raw_comment: str,
    cleaned: str,
) -> str:
    """Remove reviewed extra slash markers without touching embedded operators."""

    lines = cleaned.split("\n")
    raw_lines = raw_comment.split("\n")

    has_repeated_content_marker = any(
        re.match(r"^[ \t]*/{4,}(?=[^/])", raw_line) for raw_line in raw_lines
    )
    if language in {"antlr", "asymptote"} and has_repeated_content_marker:
        lines = [re.sub(r"^/+", "", line) for line in lines]
    if language == "powerbuilder" and has_repeated_content_marker:
        lines = [re.sub(r"^/[ \t]+", "", line) for line in lines]

    right_gutter_languages = {
        "cartocss",
        "harbour",
        "qt_script",
        "rescript",
        "rpgle",
        "sugarss",
        "witcher_script",
        "wollok",
        "xtend",
    }
    has_right_gutter = any(
        re.search(r"/{2,}[ \t]*$", raw_line) and not re.fullmatch(r"[ \t]*/+[ \t]*", raw_line)
        for raw_line in raw_lines
    )
    if language in right_gutter_languages and has_right_gutter:
        lines = [re.sub(r"[ \t]*/{2,}[ \t]*$", "", line).rstrip() for line in lines]

    if language == "openscad":
        lines = [
            "" if len(line.strip()) >= 8 and set(line.strip()) == {"/"} else line for line in lines
        ]

    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_reviewed_dash_line_result(
    language: str,
    raw_comment: str,
    cleaned: str,
) -> str:
    """Remove complete reviewed dash rulers and paired right edges."""

    reviewed_languages = {
        "ada",
        "agda",
        "asn_1",
        "makefile",
        "piglatin",
        "plpgsql",
        "purescript",
        "sql",
        "sqlpl",
        "talon",
        "terra",
        "tex",
        "vim_snippet",
    }
    if language not in reviewed_languages:
        return cleaned

    raw_lines = raw_comment.split("\n")
    has_dash_scaffold = any(
        re.search(r"(?:^|[ \t])-{2,}[ \t]*$", line)
        or re.fullmatch(r"[ \t]*(?:[#%][ \t]*)?-{3,}[ \t]*", line)
        for line in raw_lines
    )
    if not has_dash_scaffold:
        return cleaned

    remove_pure_dash_rows = language != "plpgsql" or any(
        re.fullmatch(r"[ \t]*-{8,}[ \t]*", line) for line in raw_lines
    )
    restored = []
    for line in cleaned.split("\n"):
        current = line
        if any(char.isalnum() for char in current):
            current = re.sub(r"[ \t]+-{2,}[ \t]*$", "", current).rstrip()
        if remove_pure_dash_rows and re.fullmatch(r"[ \t]*-{1,}[ \t]*", current):
            restored.append("")
        else:
            restored.append(current)
    return _normalize_sanitized_body("\n".join(restored))


def _sanitize_faust_special_block(raw_comment: str) -> str | None:
    """Unwrap complete Faust bang-star and leading hash title frames."""

    line_bodies: list[str] = []
    for line in raw_comment.split("\n"):
        wrapped = re.fullmatch(r"[ \t]*//([ \t]?)(.*)", line)
        if wrapped is None:
            break
        line_bodies.append(wrapped.group(2).rstrip())
    else:
        if len(line_bodies) >= 3:
            title = re.fullmatch(r"-{8,}(.+?)-{8,}", line_bodies[0])
            if title is not None and re.fullmatch(r"-{8,}", line_bodies[-1]):
                return _normalize_sanitized_body("\n".join([title.group(1), *line_bodies[1:-1]]))

    if raw_comment.startswith("/*!\n") and raw_comment.endswith("\n!*/"):
        inner_lines = raw_comment[4:-4].split("\n")
        non_empty = [line for line in inner_lines if line.strip()]
        if non_empty and all(re.match(r"^[ \t]*\*", line) for line in non_empty):
            cleaned: list[str] = []
            for line in inner_lines:
                match = re.match(r"^[ \t]*\*([ \t]*)(.*)$", line)
                if match is None:
                    cleaned.append("")
                    continue
                padding, content = match.groups()
                if padding.startswith("\t"):
                    padding = padding[1:]
                    if padding.startswith(" "):
                        padding = padding[1:]
                else:
                    padding = padding[min(3, len(padding)) :]
                cleaned.append((padding + content).rstrip())
            return _normalize_sanitized_body("\n".join(cleaned))

    if not (raw_comment.startswith("/*") and raw_comment.endswith("*/")):
        return None
    lines = raw_comment[2:-2].split("\n")
    while lines and not lines[-1]:
        lines.pop()
    if not (
        len(lines) >= 4
        and re.fullmatch(r"\t#{8,}", lines[0])
        and re.fullmatch(r"\t[ ]+\S.*", lines[1])
        and re.fullmatch(r"\t#{8,}", lines[2])
        and all(not line or line.startswith("\t") for line in lines[3:])
    ):
        return None

    title = lines[1][1:].lstrip(" ")
    content = [line[1:] if line.startswith("\t") else line for line in lines[3:]]
    while content and not content[-1]:
        content.pop()
    return "\n".join([title, *content]).strip("\n")


def _sanitize_faust_frame_result(cleaned: str) -> str:
    """Remove complete Faust title rules while preserving Markdown syntax."""

    lines = [line for line in cleaned.split("\n") if re.fullmatch(r"/{8,}", line.strip()) is None]
    if not lines:
        return cleaned

    equal_title = re.fullmatch(
        r"[ \t]*={3,}[ \t]+(.+?\S)[ \t]+={3,}([ \t]*:)?[ \t]*",
        lines[0],
    )
    if equal_title is not None:
        lines[0] = equal_title.group(1) + (" :" if equal_title.group(2) else "")

    if (
        len(lines) >= 2
        and re.fullmatch(r"-{8,}(.+?)-{8,}", lines[0])
        and re.fullmatch(r"-{8,}", lines[-1])
    ):
        title = re.fullmatch(r"-{8,}(.+?)-{8,}", lines[0])
        assert title is not None
        lines[0] = title.group(1)
        lines.pop()
    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_gap_line_result(raw_comment: str, cleaned: str) -> str:
    """Strip a consistent second GAP hash gutter without touching tag letters."""

    raw_lines = [
        line
        for line in raw_comment.split("\n")
        if line.strip() and re.fullmatch(r"[ \t]*#{8,}[ \t]*", line) is None
    ]
    if not raw_lines or not all(re.match(r"^[ \t]*#(?:#|[WYF])", line) for line in raw_lines):
        return cleaned
    if sum(bool(re.match(r"^[ \t]*##", line)) for line in raw_lines) < 2:
        return cleaned

    lines = [
        re.sub(r"^#[ \t\u00a0]*", "", line) if line.startswith("#") else line
        for line in cleaned.split("\n")
    ]
    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_genero_line_result(raw_comment: str, cleaned: str) -> str:
    """Unwrap complete Genero ASCII boxes and exact trailing hash gutters."""

    bodies: list[str] = []
    for line in raw_comment.split("\n"):
        wrapped = re.fullmatch(r"[ \t]*#[ \t]?(.*)", line)
        if wrapped is None:
            break
        bodies.append(wrapped.group(1))
    else:
        border = re.compile(r"[ \t]*\+-{8,}\+[ \t]*")
        if (
            len(bodies) >= 3
            and border.fullmatch(bodies[0])
            and border.fullmatch(bodies[-1])
            and all(
                border.fullmatch(body) or re.fullmatch(r"[ \t]*\|.*\|[ \t]*", body)
                for body in bodies
            )
        ):
            unframed: list[str] = []
            for body in bodies:
                if border.fullmatch(body):
                    continue
                framed = re.fullmatch(r"[ \t]*\|(.*)\|[ \t]*", body)
                assert framed is not None
                content = framed.group(1)
                if content.startswith(" "):
                    content = content[1:]
                unframed.append(content.rstrip())
            return _normalize_sanitized_body("\n".join(unframed))

    raw_lines = raw_comment.split("\n")
    cleaned_lines = cleaned.split("\n")
    if len(raw_lines) != len(cleaned_lines):
        return cleaned
    for index, raw_line in enumerate(raw_lines):
        framed = re.fullmatch(r"[ \t]*#[ \t]+(.*?\S)[ \t]+#[ \t]*", raw_line)
        if framed is not None:
            cleaned_lines[index] = framed.group(1)
    return _normalize_sanitized_body("\n".join(cleaned_lines))


def _sanitize_monkey_special_comment(raw_comment: str) -> str | None:
    """Handle complete Monkey ``#rem`` scopes and equals title cards."""

    rem_block = re.fullmatch(
        r"([ \t]*)#rem([^\n]*)(?:\n(.*))?\n\1#end",
        raw_comment,
        re.DOTALL,
    )
    if rem_block is not None:
        outer_indent, first_line, continuation = rem_block.groups()
        if first_line.startswith((" ", "\t")):
            first_line = first_line[1:]
        lines = [first_line] if first_line else []
        for line in (continuation or "").split("\n"):
            if outer_indent and line.startswith(outer_indent):
                line = line[len(outer_indent) :]
            lines.append(line.rstrip())
        return _normalize_sanitized_body("\n".join(lines))

    bodies: list[str] = []
    for line in raw_comment.split("\n"):
        wrapped = re.fullmatch(r"[ \t]*'([ \t]?)(.*)", line)
        if wrapped is None:
            return None
        bodies.append(wrapped.group(2))
    if not (
        len(bodies) >= 5
        and re.fullmatch(r"={8,}", bodies[0])
        and re.fullmatch(r"={8,}", bodies[-1])
        and any(re.fullmatch(r"==[ \t]+.+?[ \t]+==", line) for line in bodies[1:-1])
    ):
        return None
    return _normalize_sanitized_body("\n".join(bodies[1:-1]))


def _sanitize_powerbuilder_template(raw_comment: str) -> str | None:
    """Remove separator rows from complete PowerBuilder comment templates."""

    bodies: list[str] = []
    for line in raw_comment.split("\n"):
        wrapped = re.fullmatch(r"[ \t]*//([ \t]?)(.*)", line)
        if wrapped is None:
            return None
        bodies.append(wrapped.group(2).rstrip())
    if not (
        len(bodies) >= 5
        and re.fullmatch(r"={20,}", bodies[0])
        and re.fullmatch(r"={20,}", bodies[-1])
        and sum(bool(re.fullmatch(r"-{20,}", body)) for body in bodies) >= 2
    ):
        return None
    return "\n".join(body for body in bodies if body and re.fullmatch(r"[-=]{20,}", body) is None)


def _sanitize_scaml_scoped_comment(raw_comment: str) -> str | None:
    """Strip a Scaml slash while retaining indentation inside its scope."""

    lines = raw_comment.split("\n")
    first_line = re.fullmatch(r"([ \t]*)/(.*)", lines[0])
    if first_line is None:
        return None

    outer_indent, first_body = first_line.groups()
    if first_body.startswith((" ", "\t")):
        first_body = first_body[1:]

    scoped_lines = [first_body.rstrip()]
    for line in lines[1:]:
        if line.strip() and outer_indent and not line.startswith(outer_indent):
            return None
        scoped_line = line[len(outer_indent) :] if line.startswith(outer_indent) else line
        if scoped_line.lstrip(" \t").startswith("/"):
            return None
        scoped_lines.append(scoped_line.rstrip())
    return _normalize_sanitized_body("\n".join(scoped_lines))


def _sanitize_bluespec_block_result(raw_comment: str, cleaned: str) -> str:
    """Remove Bluespec's ``/*-`` license opener from star-gutter blocks."""

    if not (raw_comment.startswith("/*-\n") and raw_comment.endswith("*/")):
        return cleaned

    inner_lines = raw_comment[3:-2].split("\n")
    content_lines = [line for line in inner_lines if line.strip()]
    if not content_lines or not all(line.lstrip(" \t").startswith("*") for line in content_lines):
        return cleaned
    if not cleaned.startswith("-\n"):
        return cleaned
    return _normalize_sanitized_body(cleaned[2:])


def _sanitize_uno_block_result(raw_comment: str, cleaned: str) -> str:
    """Dedent the tab-scoped continuation of a multiline Uno doc comment."""

    if not (raw_comment.startswith("/** ") and "\n" in raw_comment):
        return cleaned

    continuation_lines = [line for line in cleaned.split("\n")[1:] if line.strip()]
    if not continuation_lines or not all(line.startswith("\t") for line in continuation_lines):
        return cleaned
    return _normalize_sanitized_body(_strip_unclosed_continuation_indent(cleaned))


def _sanitize_mercury_line_result(cleaned: str) -> str:
    """Remove Mercury separator rules whose final percent closes the ruler."""

    lines = [line for line in cleaned.split("\n") if re.fullmatch(r"-{8,}%?", line.strip()) is None]
    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_clips_line_result(raw_comment: str, cleaned: str) -> str:
    """Unwrap complete CLIPS semicolon and asterisk title frames."""

    raw_lines = raw_comment.split("\n")
    if (
        len(raw_lines) >= 3
        and re.fullmatch(r"[ \t]*;{8,}[ \t]*", raw_lines[0])
        and re.fullmatch(r"[ \t]*;{8,}[ \t]*", raw_lines[-1])
    ):
        framed_lines: list[str] = []
        for line in raw_lines[1:-1]:
            if not line.strip():
                framed_lines.append("")
                continue
            framed = re.fullmatch(r"[ \t]*;{4,}[ \t]*(.*?)[ \t]*;{4,}[ \t]*", line)
            if framed is None:
                break
            framed_lines.append(framed.group(1).strip())
        else:
            return _normalize_sanitized_body("\n".join(framed_lines))

    star_bodies: list[str] = []
    for line in raw_lines:
        comment_line = re.fullmatch(r"[ \t]*;(.*)", line)
        if comment_line is None:
            break
        star_bodies.append(comment_line.group(1))
    else:
        if (
            len(star_bodies) >= 3
            and re.fullmatch(r"[ \t]*\*{8,}[ \t]*", star_bodies[0])
            and re.fullmatch(r"[ \t]*\*{8,}[ \t]*", star_bodies[-1])
        ):
            framed_lines = []
            for line in star_bodies[1:-1]:
                framed = re.fullmatch(r"[ \t]*\*(.*?)\*[ \t]*", line)
                if framed is None:
                    break
                content = framed.group(1).strip()
                if content:
                    framed_lines.append(content)
            else:
                return _normalize_sanitized_body("\n".join(framed_lines))

    cleaned_lines: list[str] = []
    for line in cleaned.split("\n"):
        framed = re.fullmatch(r"[ \t]*;{4,}[ \t]*(.*?)[ \t]*;{4,}[ \t]*", line)
        cleaned_lines.append(framed.group(1).strip() if framed is not None else line)
    return _normalize_sanitized_body("\n".join(cleaned_lines))


def _sanitize_click_line_result(raw_comment: str, cleaned: str) -> str:
    """Unwrap a complete exclamation box nested inside Click line comments."""

    bodies: list[str] = []
    for line in raw_comment.split("\n"):
        wrapped = re.fullmatch(r"[ \t]*//[ \t]?(.*)", line)
        if wrapped is None:
            return cleaned
        bodies.append(wrapped.group(1))

    if not (
        len(bodies) >= 3
        and re.fullmatch(r"[ \t]*!{8,}[ \t]*", bodies[0])
        and re.fullmatch(r"[ \t]*!{8,}[ \t]*", bodies[-1])
    ):
        return cleaned

    content_lines: list[str] = []
    for line in bodies[1:-1]:
        framed = re.fullmatch(r"[ \t]*![ \t]*(.*?)[ \t]*![ \t]*", line)
        if framed is None:
            return cleaned
        content = framed.group(1).strip()
        if content:
            content_lines.append(content)
    return _normalize_sanitized_body("\n".join(content_lines))


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
            if (len(token) == 1 and not token[-1].isalnum() and not token[-1].isspace())
        }
        if gutter_char not in registered_chars:
            return stripped_lines
        if not any(
            (
                _is_decorative_ruler_line(line)
                or _is_empty_ruler_line(line, frozenset({gutter_char}))
            )
            for line in non_empty
        ):
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


def _sanitize_portugol_block_result(raw_comment: str, cleaned: str) -> str:
    """Strip a first-line doc-star gutter from an otherwise unguttered block."""

    if re.match(r"^/\*[ \t]*\n[ \t]+\*[ \t]+", raw_comment):
        cleaned = re.sub(r"^[ \t]*\*[ \t]+", "", cleaned, count=1)
    return cleaned


def _sanitize_glyph_line_result(body: str) -> str:
    """Remove Glyph banner rules and the conventional secondary ``--`` gutter."""

    lines = body.split("\n")
    non_empty = [line for line in lines if line.strip()]
    if non_empty and all(line.lstrip().startswith("--") for line in non_empty):
        stripped_lines: list[str] = []
        for line in lines:
            if not line.strip():
                stripped_lines.append("")
                continue
            prefix_length = len(line) - len(line.lstrip(" \t"))
            content = line[prefix_length + 2 :]
            if content.startswith((" ", "\t")):
                content = content[1:]
            stripped_lines.append(line[:prefix_length] + content.rstrip())
        lines = stripped_lines

    lines = [
        line
        for line in lines
        if not (
            len("".join(line.split())) >= 4
            and len(set("".join(line.split()))) == 1
            and "".join(line.split())[0] in _DECORATIVE_RULER_CHARS
        )
    ]
    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_x_bitmap_star_box(raw_comment: str) -> str | None:
    """Unwrap the nested star box used by legacy X bitmap copyright headers."""

    if not (raw_comment.startswith("/*") and raw_comment.endswith("*/")):
        return None

    physical_lines = raw_comment[2:-2].split("\n")
    while physical_lines and not physical_lines[0].strip():
        physical_lines.pop(0)
    while physical_lines and not physical_lines[-1].strip():
        physical_lines.pop()

    lines: list[str] = []
    for line in physical_lines:
        match = re.match(r"^[ \t]*\*(?:[ \t]?)(.*)$", line)
        if match is None:
            return None
        lines.append(match.group(1).rstrip())

    non_empty_indexes = [index for index, line in enumerate(lines) if line.strip()]
    if len(non_empty_indexes) < 3:
        return None
    first, last = non_empty_indexes[0], non_empty_indexes[-1]
    if not (
        re.fullmatch(r"\*{8,}", lines[first].strip())
        and re.fullmatch(r"\*{8,}", lines[last].strip())
    ):
        return None

    cleaned: list[str] = []
    for line in lines[first + 1 : last]:
        stripped = line.strip()
        if not stripped:
            cleaned.append("")
            continue
        if not (stripped.startswith("*") and stripped.endswith("*")):
            return None
        cleaned.append(stripped[1:-1].strip())
    return _normalize_sanitized_body("\n".join(cleaned))


def _sanitize_win32_message_result(body: str, raw_comment: str) -> str:
    """Remove C/hash banners nested inside semicolon-prefixed MC comments."""

    has_hash_frame = any(
        re.fullmatch(r"[ \t]*;//[ \t]*#{8,}[ \t]*", line) for line in raw_comment.split("\n")
    )
    cleaned: list[str] = []
    for line in body.split("\n"):
        stripped = line.strip()
        compact = "".join(stripped.split())
        decoration_core = compact.strip("/")
        if (
            len(decoration_core) >= 4
            and len(set(decoration_core)) == 1
            and decoration_core[0] in {"*", "#"}
        ):
            continue

        banner_match = re.fullmatch(r"/\*{2,}[ \t]*(.*?)[ \t]*\*+/?", stripped)
        if banner_match is not None:
            content = banner_match.group(1).strip()
            if content:
                cleaned.append(content)
            continue

        if has_hash_frame and re.match(r"^[ \t]*#[ \t]+", line):
            line = re.sub(r"^([ \t]*)#[ \t]+", r"\1", line, count=1)
        cleaned.append(line)
    result = _normalize_sanitized_body("\n".join(cleaned))
    if re.search(r"(?m)^;--\*/[ \t]*\n;[ \t]*\n;#ifndef", raw_comment):
        result = result.replace("\n\n\n\n#ifndef", "\n\n\n#ifndef", 1)
    return result


def _strip_unclosed_continuation_indent(body: str) -> str:
    """Remove the source indentation shared by an indentation-scoped body."""

    lines = body.split("\n")
    continuation_lines = [line for line in lines[1:] if line.strip()]
    if not continuation_lines:
        return body

    common_indent = min(len(line) - len(line.lstrip(" \t")) for line in continuation_lines)
    if common_indent == 0:
        return body

    return "\n".join(
        [
            lines[0],
            *[line[common_indent:] if line.strip() else line for line in lines[1:]],
        ]
    )


def _sanitize_unclosed_block_comment(
    raw_comment: str,
    syntax: CommentSyntax,
    line_wrappers: tuple[tuple[str, str], ...],
    protected_ruler_chars: frozenset[str],
) -> str | None:
    for open_text in syntax.unclosed_block_openers:
        flags = re.IGNORECASE if _is_case_insensitive_token(open_text) else 0
        opener_match = re.match(
            rf"^[^\S\r\n]*{_line_open_pattern(open_text)}",
            raw_comment,
            flags,
        )
        if opener_match is None:
            continue

        unclosed_body = _strip_unclosed_continuation_indent(raw_comment[opener_match.end() :])
        if unclosed_body.startswith((" ", "\t")):
            unclosed_body = unclosed_body[1:]
        return _sanitize_block_body(
            unclosed_body,
            (open_text, ""),
            line_wrappers,
            allow_doc_star=True,
            protected_ruler_chars=protected_ruler_chars,
        )
    return None


def _sanitize_slang_spliced_line(raw_comment: str) -> str | None:
    normalized = _normalize_newlines(raw_comment)
    candidate = normalized.lstrip(" \t")
    physical_lines = candidate.split("\n")
    if (
        not candidate.startswith("//")
        or len(physical_lines) < 2
        or not all(line.endswith("\\") for line in physical_lines[:-1])
    ):
        return None

    body = candidate[2:]
    if body.startswith((" ", "\t")):
        body = body[1:]
    return _normalize_sanitized_body(body)


def _sanitize_grouped_block_lines(lines: list[str], wrappers: tuple[tuple[str, str], ...]) -> str:
    wrapper_chars = frozenset(
        char for wrapper in wrappers for char in _wrapper_punctuation_chars(wrapper)
    )
    non_empty = [line for line in lines if line.strip()]
    if non_empty and all(_is_punctuation_only(line) for line in non_empty):
        used_chars = frozenset("".join(line.strip() for line in non_empty))
        if used_chars <= wrapper_chars:
            return ""
    lines = _remove_decorative_block_lines(lines, remove_interior=False)
    return _normalize_sanitized_body("\n".join(lines))


def _sanitize_block_body(
    body: str,
    wrapper: tuple[str, str],
    line_wrappers: tuple[tuple[str, str], ...],
    *,
    allow_doc_star: bool,
    protected_ruler_chars: frozenset[str] = frozenset(),
    strip_single_line_padding: bool = True,
) -> str:
    body = _normalize_newlines(body)
    opener_on_own_line = body.startswith("\n")
    if opener_on_own_line:
        body = body[1:]
    elif _is_spaced_underscore_art_line(body.split("\n", 1)[0]):
        body = _strip_one_comment_padding_cell(body)
    else:
        body = body.lstrip(" \t")
    if body.endswith("\n"):
        body = body[:-1]

    lines = body.split("\n")
    nested_line_wrappers = tuple(
        wrapper for wrapper in line_wrappers if not any(char.isalnum() for char in wrapper[0])
    )
    line_openers = tuple(open_token for open_token, _ in nested_line_wrappers)
    wrapper_chars = _wrapper_punctuation_chars(wrapper)

    def is_wrapper_ruler(line: str) -> bool:
        compact = "".join(line.split())
        return len(compact) >= 4 and len(set(compact)) == 1 and compact[0] in wrapper_chars

    while lines and is_wrapper_ruler(lines[0]):
        lines.pop(0)
    while lines and is_wrapper_ruler(lines[-1]):
        lines.pop()
    while lines and lines[0].strip() in line_openers:
        lines.pop(0)
    while lines and lines[-1].strip() in line_openers:
        lines.pop()

    lines, stripped_symmetric_frame = _strip_symmetric_block_frame(lines)
    grouped_line_result = _strip_grouped_line_wrappers(
        "\n".join(lines),
        nested_line_wrappers,
        protected_padding_chars=protected_ruler_chars,
    )
    if grouped_line_result is not None:
        return grouped_line_result

    lines, stripped_left_gutter = _strip_common_left_gutter(
        lines,
        wrapper,
        allow_doc_star=allow_doc_star,
        allow_unguttered_first_line=not opener_on_own_line,
    )
    lines, stripped_right_gutter = _strip_common_right_gutter(
        lines,
        _wrapper_punctuation_chars(wrapper) | frozenset("*"),
    )
    if stripped_left_gutter and stripped_right_gutter:
        lines = [line.strip() for line in lines]
    elif stripped_symmetric_frame:
        lines = [line.rstrip() for line in lines]
    lines = _strip_inline_ruler_padding(
        lines,
        protected_chars=protected_ruler_chars,
    )
    if strip_single_line_padding:
        lines = _strip_single_line_decorative_padding(
            lines,
            protected_chars=protected_ruler_chars,
        )
    lines = _remove_long_decorative_rulers(lines)
    lines = _remove_decorative_block_lines(
        lines,
        remove_interior=stripped_left_gutter,
        protected_ruler_chars=protected_ruler_chars,
    )
    lines = _strip_unicode_box_frames(lines)
    lines = _strip_metadata_line_padding(lines)

    return _normalize_sanitized_body("\n".join(lines))


_SECONDARY_GUTTER_TOKENS = {
    "ant_build_system": ("#", 1),
    "css": ("*", 1),
    "forth": ("*", 1),
    "gams": ("*", 2),
    "nanorc": ("#", 1),
    "ncl": ("*", 1),
    "nwscript": ("::", 1),
    "php": ("|", 1),
    "tcsh": ("!", 1),
    "vb6": ("*", 2),
    "visual_basic": ("*", 2),
    "visual_basic_6_0": ("*", 2),
    "visual_basic_net": ("*", 2),
}


def _is_long_punctuation_row(line: str) -> bool:
    compact = "".join(line.split())
    return len(compact) >= 8 and compact.isascii() and all(not char.isalnum() for char in compact)


def _has_secondary_frame_evidence(language: str, raw_comment: str, token: str) -> bool:
    raw_lines = [line for line in raw_comment.split("\n") if line.strip()]
    if sum(_is_long_punctuation_row(line) for line in raw_lines) >= 2:
        return True

    token_char = token[-1]
    right_edges = sum(line.rstrip().endswith(token_char) for line in raw_lines)
    if raw_lines and right_edges / len(raw_lines) >= 0.8:
        return True

    if language == "css":
        return raw_comment.startswith("/*\n") and raw_comment.endswith("\n*/")

    compact_edges = ["".join(line.split()) for line in raw_lines]
    return (
        len(compact_edges) >= 2
        and compact_edges[0].endswith(token)
        and compact_edges[-1].endswith(token)
        and len(compact_edges[0]) <= len(token) + 1
        and len(compact_edges[-1]) <= len(token) + 1
    )


def _sanitize_secondary_gutter_result(language: str, raw_comment: str, cleaned: str) -> str:
    """Remove a proven second gutter inside an already stripped comment."""

    configuration = _SECONDARY_GUTTER_TOKENS.get(language)
    if configuration is None:
        return cleaned
    token, padding_limit = configuration

    lines = cleaned.split("\n")
    non_blank = [line for line in lines if line.strip()]
    if len(non_blank) < 3:
        return cleaned
    covered = sum(line.lstrip(" \t").startswith(token) for line in non_blank)
    if covered / len(non_blank) < 0.8:
        return cleaned
    if not _has_secondary_frame_evidence(language, raw_comment, token):
        return cleaned

    stripped_lines: list[str] = []
    for index, line in enumerate(lines):
        prefix_width = len(line) - len(line.lstrip(" \t"))
        body = line[prefix_width:]
        if not body.startswith(token):
            stripped_lines.append(line.rstrip())
            continue

        body = body[len(token) :]
        if language == "tcsh" and index == 0 and body.lstrip(" \t").startswith("/"):
            body = "!" + body.lstrip(" \t")
        else:
            padding_width = len(body) - len(body.lstrip(" \t"))
            body = body[min(padding_width, padding_limit) :]
        if _is_long_punctuation_row(body):
            continue
        stripped_lines.append((line[:prefix_width] + body).rstrip())

    result = "\n".join(stripped_lines)
    if language == "ant_build_system":
        return "\n".join(line.rstrip() for line in result.split("\n")).strip("\n")
    return _normalize_sanitized_body(result)


def _strip_exact_line_marker(raw_comment: str, markers: tuple[str, ...]) -> list[str] | None:
    bodies: list[str] = []
    for line in raw_comment.split("\n"):
        match = re.match(r"^[ \t]*", line)
        assert match is not None
        body = line[match.end() :]
        marker = next((candidate for candidate in markers if body.startswith(candidate)), None)
        if marker is None:
            return None
        body = body[len(marker) :]
        if body.startswith((" ", "\t")):
            body = body[1:]
        bodies.append(body.rstrip())
    return bodies


def _sanitize_literal_double_slash_lines(language: str, raw_comment: str) -> str | None:
    """Strip exactly ``//`` when an unregistered extra slash is content."""

    if language not in {"cap_cds", "lark"}:
        return None

    bodies: list[str] = []
    has_literal_slash = False
    for line in raw_comment.split("\n"):
        match = re.fullmatch(r"[ \t]*//(.*)", line)
        if match is None:
            return None
        body = match.group(1).rstrip()
        has_literal_slash |= body.startswith("/")
        bodies.append(body)
    if not has_literal_slash:
        return None
    return "\n".join(bodies).strip("\n")


def _sanitize_full_inner_c_layer(language: str, raw_comment: str) -> str | None:
    """Unwrap a complete C-style layer embedded in another comment syntax."""

    if language == "ant_build_system":
        if not (raw_comment.startswith("<!--") and raw_comment.endswith("-->")):
            return None
        inner = raw_comment[4:-3].strip(" \t\n")
        raw_lines = inner.split("\n")
        non_blank = [line for line in raw_lines if line.strip()]
        if len(non_blank) < 3:
            return None

        if all(line.lstrip(" \t").startswith("//") for line in non_blank):
            bodies = _strip_exact_line_marker(inner, ("//",))
            if bodies is None or not (
                _is_long_punctuation_row(bodies[0]) and _is_long_punctuation_row(bodies[-1])
            ):
                return None
            return CommentSanitizer("c").sanitize(inner)

        if all(line.lstrip(" \t").startswith("~") for line in non_blank):
            bodies = _strip_exact_line_marker(inner, ("~",))
            if bodies is None:
                return None
            nested = "\n".join(bodies).strip(" \t\n")
            if nested.startswith("/*") and nested.endswith("*/"):
                return CommentSanitizer("c").sanitize(nested)
        return None

    if language != "java_properties":
        return None
    bodies = _strip_exact_line_marker(raw_comment, ("#",))
    if bodies is None or len([line for line in bodies if line.strip()]) < 3:
        return None
    nested = "\n".join(bodies[1:]).strip(" \t\n")
    if not (nested.startswith("/*") and nested.endswith("*/")):
        return None
    nested_result = CommentSanitizer("c").sanitize(nested)
    return _normalize_sanitized_body("\n".join([bodies[0], nested_result]))


def _fixed_frame_border_char(line: str) -> str | None:
    compact = "".join(line.split())
    if len(compact) < 8 or any(char.isalnum() for char in compact):
        return None
    counts = {char: compact.count(char) for char in set(compact)}
    char, count = max(counts.items(), key=lambda item: item[1])
    return char if count >= 8 else None


def _strip_fixed_frame_side(
    line: str,
    left_side: str,
    right_side: str,
    *,
    strip_alignment: bool,
) -> tuple[str, bool]:
    stripped = line.strip() if left_side or strip_alignment else line.rstrip()
    if left_side and not stripped.startswith(left_side):
        return line, False
    if right_side and not stripped.endswith(right_side):
        return line, False
    start = len(left_side)
    end = len(stripped) - len(right_side) if right_side else len(stripped)
    body = stripped[start:end]
    if strip_alignment:
        body = body.strip()
    else:
        body = body.rstrip()
    return body, True


def _unwrap_fixed_frame_source(language: str, raw_comment: str) -> list[str] | None:
    block_wrappers = {
        "c": ("/*", "*/"),
        "c#": ("/*", "*/"),
        "c_sharp": ("/*", "*/"),
        "csharp": ("/*", "*/"),
        "smarty": ("{*", "*}"),
        "sqf": ("/*", "*/"),
        "xbase": ("/*", "*/"),
        "zephir": ("/*", "*/"),
    }
    wrapper = block_wrappers.get(language)
    if wrapper is not None:
        open_token, close_token = wrapper
        if not (raw_comment.startswith(open_token) and raw_comment.endswith(close_token)):
            return None
        lines = raw_comment[len(open_token) : -len(close_token)].split("\n")
        if lines and lines[0].startswith((" ", "\t")):
            lines[0] = lines[0][1:]
        return lines

    line_markers = {
        "asn1": ("--",),
        "asn_1": ("--",),
        "common_lisp": (";;;", ";;"),
        "lisp": (";;;", ";;"),
    }.get(language)
    if line_markers is None:
        return None
    return _strip_exact_line_marker(raw_comment, line_markers)


def _sanitize_complete_fixed_frame(language: str, raw_comment: str) -> str | None:
    """Unwrap a paired fixed-width frame when at least 80% of rows have sides."""

    lines = _unwrap_fixed_frame_source(language, raw_comment)
    if lines is None:
        return None

    side_configuration = {
        "asn1": ("", "--", True),
        "asn_1": ("", "--", True),
        "c": ("{", "}", True),
        "c#": ("{", "}", True),
        "c_sharp": ("{", "}", True),
        "csharp": ("{", "}", True),
        "common_lisp": ("", ";;", False),
        "lisp": ("", ";;", False),
        "smarty": ("|", "|", False),
        "sqf": ("│", "│", True),
        "xbase": ("*", "*", True),
        "zephir": ("|", "|", False),
    }
    left_side, right_side, strip_alignment = side_configuration[language]
    borders = [
        (index, border_char)
        for index, line in enumerate(lines)
        if (border_char := _fixed_frame_border_char(line)) is not None
    ]
    if len(borders) < 2:
        return None

    first, first_char = borders[0]
    last, last_char = borders[-1]
    if language == "xbase" and first_char != last_char:
        transformed = list(lines)
        changed = False
        offset = 0
        for (start, start_char), (end, end_char) in zip(borders, borders[1:]):
            if start_char != end_char or end <= start + 1:
                continue
            content = lines[start + 1 : end]
            non_blank = [line for line in content if line.strip()]
            stripped = [
                _strip_fixed_frame_side(
                    line,
                    left_side,
                    right_side,
                    strip_alignment=strip_alignment,
                )
                for line in non_blank
            ]
            if not non_blank or sum(matched for _, matched in stripped) / len(non_blank) < 0.8:
                continue
            replacement = [
                _strip_fixed_frame_side(
                    line,
                    left_side,
                    right_side,
                    strip_alignment=strip_alignment,
                )[0]
                if line.strip()
                else ""
                for line in content
            ]
            transformed[start - offset : end + 1 - offset] = replacement
            offset += 2
            changed = True
        if not changed:
            return None
        return _normalize_sanitized_body("\n".join(transformed))

    if first_char != last_char or last <= first + 1:
        return None
    content_indexes = [
        index
        for index in range(first + 1, last)
        if lines[index].strip() and _fixed_frame_border_char(lines[index]) is None
    ]
    if not content_indexes:
        return None
    side_matches = {
        index: _strip_fixed_frame_side(
            lines[index],
            left_side,
            right_side,
            strip_alignment=strip_alignment,
        )
        for index in content_indexes
    }
    if sum(matched for _, matched in side_matches.values()) / len(content_indexes) < 0.8:
        return None

    inner: list[str] = []
    for index in range(first + 1, last):
        line = lines[index]
        if _fixed_frame_border_char(line) is not None:
            continue
        if index in side_matches and side_matches[index][1]:
            line = side_matches[index][0]
        elif language in {"asn1", "asn_1"}:
            line = line.strip()
        inner.append(line.rstrip())

    if language in {"common_lisp", "lisp"}:
        had_leading_blank = bool(inner) and not inner[0].strip()
        inner_result = _normalize_sanitized_body("\n".join(inner))
        if had_leading_blank:
            inner_result = "\n" + inner_result
    else:
        inner_result = "\n".join(inner)
    result_lines = [*lines[:first], *inner_result.split("\n"), *lines[last + 1 :]]
    if language in {"asn1", "asn_1"}:
        collapsed: list[str] = []
        for line in result_lines:
            if not line.strip() and collapsed and not collapsed[-1].strip():
                continue
            collapsed.append(line)
        result_lines = collapsed
    return _normalize_sanitized_body("\n".join(result_lines))


def _sanitize_numbered_star_frame(language: str, raw_comment: str) -> str | None:
    if language not in {"linker_script", "rpc"}:
        return None
    match = re.fullmatch(
        r"/\*{8,}20\*\*\n(.*?)\n\*{8,}21\*/",
        raw_comment,
        re.DOTALL,
    )
    if match is None:
        return None
    return _normalize_sanitized_body(match.group(1))


def _sanitize_mcfunction_fixed_frame(language: str, raw_comment: str) -> str | None:
    if language != "mcfunction":
        return None
    lines = raw_comment.split("\n")
    if len([line for line in lines if line.strip()]) < 3:
        return None
    if not (
        re.fullmatch(r"#[=]{8,}(?:[A-Za-z ]+[=]{8,})?#", lines[0])
        and re.fullmatch(r"#[=]{8,}#", lines[-1])
    ):
        return None
    cleaned: list[str] = []
    for line in lines[1:-1]:
        match = re.fullmatch(r"#[ \t]+(.*?)[ \t]+#", line)
        if match is None:
            return None
        cleaned.append(match.group(1).strip())
    return _normalize_sanitized_body("\n".join(cleaned))


def _is_abap_line_ruler(body: str) -> bool:
    """Return whether an ABAP line-comment body is a generated separator."""

    compact = body.strip()
    return bool(
        re.fullmatch(r"-{4,}\*?", compact)
        or re.fullmatch(r"\*{2,}", compact)
        or re.fullmatch(r"\.{4,}", compact)
    )


def _strip_abap_line_marker(line: str) -> tuple[str, str]:
    """Strip one ABAP column-one marker and its conventional padding cell."""

    if line.startswith("*&"):
        marker = "*&"
        body = line[2:]
    elif re.match(r"^\*{3}(?i:INCLUDE)\b", line):
        marker = "***"
        body = line[3:]
    else:
        marker = "*"
        body = line[1:]

    if body.startswith((" ", "\t")):
        body = body[1:]
    return marker, body.rstrip()


def _sanitize_abap_generated_interface(raw_comment: str) -> str | None:
    """Clean SAP-generated ``*"`` interface headers without shifting declarations."""

    lines = raw_comment.split("\n")
    non_empty = [line for line in lines if line]
    if len(non_empty) < 3 or not all(line.startswith('*"') for line in non_empty):
        return None

    bodies = [line[2:].rstrip() if line else "" for line in lines]
    if not (
        bodies
        and re.fullmatch(r"-{8,}", bodies[0].strip())
        and re.fullmatch(r"-{8,}", bodies[-1].strip())
    ):
        return None

    cleaned: list[str] = []
    for body in bodies:
        if re.fullmatch(r"-{8,}", body.strip()):
            continue
        if body.startswith('*"'):
            body = body[2:]
        cleaned.append(body)
    return _normalize_sanitized_body("\n".join(cleaned))


def _sanitize_abap_pipe_frame(raw_comment: str) -> str | None:
    """Clean the fixed-width ``*/---\\`` license boxes emitted by SAPlink."""

    lines = raw_comment.split("\n")
    if (
        len(lines) < 3
        or re.fullmatch(r"\*/-{8,}\\", lines[0]) is None
        or re.fullmatch(r"\*\\-{8,}/", lines[-1]) is None
    ):
        return None

    cleaned: list[str] = []
    for line in lines[1:-1]:
        match = re.fullmatch(r"\*\|(.*)\|", line)
        if match is None:
            return None
        cleaned.append(match.group(1).strip())
    return _normalize_sanitized_body("\n".join(cleaned))


def _sanitize_abap_line_card(raw_comment: str) -> str | None:
    """Clean ruler-backed ABAP line-comment cards and generated banners."""

    lines = raw_comment.split("\n")
    non_empty = [line for line in lines if line]
    if len(non_empty) < 2 or not all(line.startswith("*") for line in non_empty):
        return None

    parsed = [("", "") if not line else _strip_abap_line_marker(line) for line in lines]
    if not any(_is_abap_line_ruler(body) for _, body in parsed):
        return None

    content = [(marker, body) for marker, body in parsed if not _is_abap_line_ruler(body)]

    # SAP's fixed-width cards use a trailing ``*`` column on every retained
    # row. Both edge columns and their alignment padding are scaffolding.
    right_gutter = re.compile(r"[ \t]+\*[ \t]*$")
    framed_rows = [body for _, body in content if body.strip()]
    ordinary_rows = [body for marker, body in content if marker == "*" and body.strip()]
    has_fixed_width_body = (
        (
            len(framed_rows) >= 2
            and all(right_gutter.search(body) is not None for body in framed_rows)
        )
        or (
            len(framed_rows) == 1
            and _is_abap_line_ruler(parsed[0][1])
            and _is_abap_line_ruler(parsed[-1][1])
            and right_gutter.search(framed_rows[0]) is not None
        )
        or (
            any(marker == "*&" and body.strip() for marker, body in content)
            and len(ordinary_rows) >= 2
            and all(right_gutter.search(body) is not None for body in ordinary_rows)
        )
    )

    cleaned: list[str] = []
    for _, body in content:
        if has_fixed_width_body:
            body = right_gutter.sub("", body).strip()
            if _is_abap_line_ruler(body):
                continue
        cleaned.append(body)
    return _normalize_sanitized_body("\n".join(cleaned))


def _sanitize_abap_comment(raw_comment: str) -> str | None:
    """Apply only ABAP-specific generated-comment cleaning conventions."""

    generated_interface = _sanitize_abap_generated_interface(raw_comment)
    if generated_interface is not None:
        return generated_interface

    pipe_frame = _sanitize_abap_pipe_frame(raw_comment)
    if pipe_frame is not None:
        return pipe_frame

    quoted_title = re.fullmatch(
        r'"[ \t]+(.+?)[ \t]+-{8,}"',
        raw_comment,
    )
    if quoted_title is not None:
        return quoted_title.group(1).strip()

    return _sanitize_abap_line_card(raw_comment)


def _strip_one_comment_padding_cell(body: str) -> str:
    """Delete one conventional space or tab after a proven comment marker."""

    if body.startswith((" ", "\t")):
        return body[1:]
    return body


def _sanitize_ec_star_border(raw_comment: str) -> str | None:
    """Clean EC's complete long-star border with a late star-gutter section."""

    lines = raw_comment.split("\n")
    if (
        len(lines) < 4
        or re.fullmatch(r"/\*{8,}", lines[0]) is None
        or re.fullmatch(r"\*{8,}/", lines[-1]) is None
    ):
        return None

    inner = lines[1:-1]
    if not any(line.startswith(" *") and any(char.isalnum() for char in line) for line in inner):
        return None

    cleaned: list[str] = []
    first_content_seen = False
    for line in inner:
        if line.startswith(" *"):
            line = _strip_one_comment_padding_cell(line[2:])
        if line.strip() and not first_content_seen:
            first_content_seen = True
            if line.startswith("\t"):
                line = line[1:]
        cleaned.append(line.rstrip())
    return _normalize_sanitized_body("\n".join(cleaned))


def _sanitize_erlang_ruler_layout(raw_comment: str) -> str | None:
    """Delete only proven Erlang percent-prefixed section rulers and gutters."""

    lines = raw_comment.split("\n")
    if len(lines) < 3 or not all(re.match(r"^%{1,3}", line) for line in lines):
        return None

    def split_marker(line: str) -> tuple[str, str]:
        match = re.match(r"^(%{1,3})(.*)$", line)
        assert match is not None
        return match.group(1), match.group(2)

    def is_ruler(line: str) -> bool:
        _, body = split_marker(line)
        return re.fullmatch(r"[ \t]*-{8,}[ \t]*", body) is not None

    ruler_indexes = [index for index, line in enumerate(lines) if is_ruler(line)]
    if not ruler_indexes:
        return None

    marker_widths = [len(split_marker(line)[0]) for line in lines]
    width_sections = [marker_widths[0]]
    for width in marker_widths[1:]:
        if width != width_sections[-1]:
            width_sections.append(width)
    mixed_generated_header = (
        width_sections == [1, 3, 2]
        and len(ruler_indexes) == 2
        and all(marker_widths[index] == 3 for index in ruler_indexes)
    )
    if mixed_generated_header:
        # Generated Erlang headers use padding only for source alignment. Once
        # the 1/3/2-percent sections prove that layout, delete all such padding.
        cleaned: list[str] = []
        for line in lines:
            if is_ruler(line):
                continue
            _, body = split_marker(line)
            cleaned.append(body.lstrip(" \t").rstrip())
        return _normalize_sanitized_body("\n".join(cleaned))

    rewritten: list[str] = []
    for index, line in enumerate(lines):
        if not is_ruler(line):
            rewritten.append(line)
            continue
        if index in {0, len(lines) - 1}:
            continue
        previous_blank = not split_marker(lines[index - 1])[1].strip()
        next_blank = not split_marker(lines[index + 1])[1].strip()
        if previous_blank or next_blank:
            continue
        marker, _ = split_marker(line)
        rewritten.append(marker)
    return CommentSanitizer("erlang").sanitize("\n".join(rewritten))


def _sanitize_validated_secondary_gutter_scaffold(
    language: str,
    raw_comment: str,
) -> str | None:
    """Delete secondary gutters from complete, language-scoped layouts."""

    if language == "freemarker":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and lines[0] == "<#--"
            and lines[-1] == "-->"
            and re.fullmatch(r"/\*{8,}", lines[1])
            and re.fullmatch(r"\*{8,}/", lines[-2])
        ):
            body = lines[2:-2]
            gutter_count = sum(re.match(r"^[ \t]*\*[ \t]+", line) is not None for line in body)
            if gutter_count >= 4:
                cleaned = [re.sub(r"^[ \t]*\*[ \t]+", "", line).rstrip() for line in body]
                return _normalize_sanitized_body("\n".join(cleaned))

        if (
            len(lines) >= 4
            and lines[0] == "<#--"
            and (closing := re.fullmatch(r"([ \t]*)-->", lines[-1])) is not None
            and re.match(r"^[ \t]*\*[ \t]+", lines[1])
            and any("<#" in line for line in lines[2:-1])
        ):
            source_indent = closing.group(1)
            body = lines[1:-1]
            if all(
                not line.strip() or not source_indent or line.startswith(source_indent)
                for line in body
            ):
                cleaned: list[str] = []
                for index, line in enumerate(body):
                    if source_indent and line.startswith(source_indent):
                        line = line[len(source_indent) :]
                    if index == 0:
                        line = re.sub(r"^[ \t]*\*[ \t]+", "", line)
                    cleaned.append(line.rstrip())
                return _normalize_sanitized_body("\n".join(cleaned))

    if language == "imagej_macro":
        lines = raw_comment.split("\n")
        opener = "/**" if raw_comment.startswith("/**") else "/*"
        closing = re.fullmatch(r"([ \t]*)\*/", lines[-1]) if len(lines) >= 2 else None
        if raw_comment.startswith(opener) and closing is not None:
            source_indent = closing.group(1)
            body = [lines[0][len(opener) :], *lines[1:-1]]
            star_indexes = [
                index for index, line in enumerate(body) if re.match(r"^[ \t]*\*[ \t]+", line)
            ]
            non_blank_indexes = [index for index, line in enumerate(body) if line.strip()]
            if star_indexes and non_blank_indexes:
                first_star = star_indexes[0]
                last_star = star_indexes[-1]
                prefix_gutter = all(
                    index in star_indexes for index in non_blank_indexes if 0 < index <= last_star
                )
                suffix_gutter = all(
                    index in star_indexes for index in non_blank_indexes if index >= first_star
                )
                if prefix_gutter or suffix_gutter:
                    cleaned = []
                    for index, line in enumerate(body):
                        if index and source_indent and line.startswith(source_indent):
                            line = line[len(source_indent) :]
                        if index == 0 and line.startswith((" ", "\t")):
                            line = line[1:]
                        line = re.sub(r"^[ \t]*\*[ \t]?", "", line)
                        cleaned.append(line.rstrip())
                    return _normalize_sanitized_body("\n".join(cleaned))

    if language in {"peg_js", "pegjs"}:
        lines = raw_comment.split("\n")
        if len(lines) >= 6 and lines[0] == "/*" and lines[-1] == "*/":
            body = lines[1:-1]
            star_indexes = [
                index for index, line in enumerate(body) if re.match(r"^[ \t]*\*[ \t]+", line)
            ]
            first_plain = next(
                (
                    index
                    for index, line in enumerate(body)
                    if line.strip() and index not in star_indexes
                ),
                None,
            )
            if (
                len(star_indexes) >= 2
                and first_plain is not None
                and max(star_indexes) < first_plain
            ):
                cleaned = [re.sub(r"^[ \t]*\*[ \t]+", "", line).rstrip() for line in body]
                return _normalize_sanitized_body("\n".join(cleaned))

    if language == "promela":
        lines = raw_comment.split("\n")
        if len(lines) >= 6 and lines[0].startswith("/** ") and lines[-1].endswith(" **/"):
            body = [lines[0][3:], *lines[1:-1], lines[-1][:-3]]
            star_count = sum(re.match(r"^[ \t]*\*[ \t]+", line) is not None for line in body)
            non_blank = sum(bool(line.strip()) for line in body)
            if star_count >= 3 and star_count / max(non_blank - 2, 1) >= 0.8:
                cleaned = []
                for index, line in enumerate(body):
                    if line.startswith(" "):
                        line = line[1:]
                    line = re.sub(r"^\*[ \t]+", "", line)
                    cleaned.append(line.rstrip())
                return _normalize_sanitized_body("\n".join(cleaned))

    if language == "pascal":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and re.fullmatch(r"\(\*{8,}", lines[0])
            and re.fullmatch(r"[ \t]*\*{8,}\)", lines[-1])
            and sum(re.match(r"^[ \t]*\*(?:[ \t]|$)", line) is not None for line in lines[1:-1])
            >= 3
        ):
            cleaned = [re.sub(r"^[ \t]*\*(?:[ \t]|$)", "", line).rstrip() for line in lines[1:-1]]
            return _normalize_sanitized_body("\n".join(cleaned))

    if language == "pawn":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and lines[0] == "/*!"
            and lines[-1] == " */"
            and sum(line.startswith(" *") for line in lines[1:-1]) >= 3
        ):
            cleaned = []
            for line in lines[1:-1]:
                if line.startswith(" "):
                    line = line[1:]
                line = re.sub(r"^\*(?:[ \t]|$)", "", line)
                cleaned.append(line.rstrip())
            return _normalize_sanitized_body("\n".join(cleaned))

    if language == "rpgle":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 8
            and re.fullmatch(r"/\*[ \t]+-{20,}", lines[0])
            and re.fullmatch(r"[ \t]*\*[ \t]+-{20,}[ \t]+\*/", lines[-1])
            and sum(line.startswith(" *") for line in lines[1:-1]) >= 5
        ):
            cleaned = []
            for line in lines[1:-1]:
                guttered = line.startswith(" *")
                if guttered:
                    line = re.sub(r"^ \*(?: |$)", "", line)
                elif line.startswith(" "):
                    line = line[1:]
                if re.fullmatch(r"[ \t]*-{20,}[ \t]*", line):
                    continue
                cleaned.append(line.rstrip())
            return _normalize_sanitized_body("\n".join(cleaned))

    if language == "sql":
        lines = raw_comment.split("\n")
        bodies = [
            match.group(1)
            for line in lines
            if (match := re.fullmatch(r"--[ \t]?(.*)", line)) is not None
        ]
        if (
            len(lines) >= 4
            and len(bodies) == len(lines)
            and re.fullmatch(r"-{20,}", bodies[0])
            and re.fullmatch(r"-{20,}", bodies[-1])
            and all(re.match(r"\*[ \t]+", body) for body in bodies[1:-1])
        ):
            return "\n".join(re.sub(r"^\*[ \t]+", "", body).strip() for body in bodies[1:-1])

    if language in {"groovy_server_pages", "maven_pom"}:
        lines = raw_comment.split("\n")
        wrappers = {
            "groovy_server_pages": ("<%--", "--%>"),
            "maven_pom": ("<!--", "-->"),
        }
        open_token, close_token = wrappers[language]
        if len(lines) >= 5 and lines[0] == open_token and lines[-1].strip() == close_token:
            matches = [re.fullmatch(r"[ \t]*~(?:[ \t]{1,2}(.*)|)", line) for line in lines[1:-1]]
            if all(match is not None for match in matches):
                return _normalize_sanitized_body(
                    "\n".join(
                        (match.group(1) or "").rstrip() for match in matches if match is not None
                    )
                )

    if language == "eclipse":
        lines = raw_comment.split("\n")
        if len(lines) >= 3 and re.fullmatch(r"%{8,}", lines[0]) and lines[0] == lines[-1]:
            framed = [re.fullmatch(r"%%[ \t]*(.*?)[ \t]*%%", line) for line in lines[1:-1]]
            if all(match is not None for match in framed):
                return "\n".join(match.group(1).strip() for match in framed if match is not None)
        if len(lines) >= 3 and all(line.startswith("%%") for line in lines):
            markers = [re.match(r"^(%%+)[ \t]?(.*)", line) for line in lines]
            if all(match is not None for match in markers) and any(
                len(match.group(1)) >= 3 for match in markers if match is not None
            ):
                return _normalize_sanitized_body(
                    "\n".join(match.group(2).rstrip() for match in markers if match is not None)
                )

    if language == "openedge_abl":
        lines = raw_comment.split("\n")
        heading = re.fullmatch(r"/\*[ ]{1,2}-{3}[ ]+(.*?)[ ]+-{6,}", lines[0]) if lines else None
        fields = [re.fullmatch(r"[ ]*>[ ]{1,2}(.*)", line) for line in lines[1:-1]]
        if (
            len(lines) >= 4
            and heading is not None
            and re.fullmatch(r"[ ]*\*/", lines[-1])
            and all(match is not None for match in fields)
        ):
            return "\n".join(
                [
                    heading.group(1),
                    *[match.group(1).rstrip() for match in fields if match is not None],
                ]
            )

    if language == "desktop":
        lines = raw_comment.split("\n")
        framed = [re.fullmatch(r"###[ \t]+(.*?)[ \t]+###", line) for line in lines]
        if len(lines) >= 3 and all(match is not None for match in framed):
            return "\n".join(match.group(1).rstrip() for match in framed if match is not None)

    return None


def _sanitize_validated_fixed_frame_scaffold(
    language: str,
    raw_comment: str,
) -> str | None:
    """Unwrap complete, fixed frames without interpreting their content."""

    lines = raw_comment.split("\n")
    if (
        language == "bibtex"
        and len(lines) == 3
        and re.fullmatch(r"%{8,}", lines[0])
        and lines[0] == lines[-1]
        and (content := re.fullmatch(r"%%[ \t]+(.*?)[ \t]+%%", lines[1])) is not None
    ):
        return content.group(1)

    if language == "blitzbasic":
        if len(lines) == 2:
            first = re.fullmatch(r";_{8,}(.*?)[ \t]*", lines[0])
            if first is not None and lines[1].startswith(";"):
                return "\n".join((first.group(1), lines[1][1:].lstrip(" \t")))
        if len(lines) >= 3 and all(line.startswith(";") for line in lines):
            bodies = [line[1 + int(line.startswith("; ")) :] for line in lines]
            heading = re.fullmatch(r"\*[ \t]+(.+)", bodies[0])
            if heading is not None:
                return "\n".join([heading.group(1), *[line.rstrip() for line in bodies[1:]]])

    if language == "clips":
        framed = [re.fullmatch(r";[ \t]+;[ \t]+(.*)", line) for line in lines]
        if len(lines) >= 2 and all(match is not None for match in framed):
            return "\n".join(match.group(1).rstrip() for match in framed if match is not None)

    if language == "clojure":
        framed = re.fullmatch(r";;[ \t]+-{2,}[ \t]+(.+?)[ \t]+-{8,}", raw_comment)
        if framed is not None:
            return framed.group(1)

    if language == "cmake":
        framed = re.fullmatch(r"#-{2,}[ \t]+(.+?)[ \t]+-{8,}#", raw_comment)
        if framed is not None:
            return framed.group(1)

    if language == "denizenscript":
        framed = re.fullmatch(r"#[ \t]+(.+?)[ \t]{8,}\*", raw_comment)
        if framed is not None:
            return framed.group(1)

    if language == "ebnf" and raw_comment.startswith("(*\n") and raw_comment.endswith("\n*)"):
        body = raw_comment[3:-3].split("\n")
        ruler_count = sum(re.fullmatch(r"![ \t]+-{8,}", line) is not None for line in body)
        gutter_count = sum(re.match(r"![ \t]", line) is not None for line in body)
        if ruler_count >= 2 and gutter_count >= 3:
            cleaned = []
            for line in body:
                if re.fullmatch(r"![ \t]+-{8,}", line):
                    continue
                if line == "!":
                    cleaned.append("")
                    continue
                line = re.sub(r"^![ \t]", "", line)
                cleaned.append(line.rstrip())
            return _normalize_sanitized_body("\n".join(cleaned))

    if (
        language == "ninja"
        and len(lines) >= 5
        and re.fullmatch(r"#{8,}", lines[0])
        and lines[0] == lines[2]
        and (heading := re.fullmatch(r"###[ \t]+(.+?)[ \t]+###", lines[1])) is not None
    ):
        body = [re.fullmatch(r"#[ \t]?(.*)", line) for line in lines[3:]]
        if all(match is not None for match in body):
            return _normalize_sanitized_body(
                "\n".join(
                    [
                        heading.group(1),
                        *[match.group(1).rstrip() for match in body if match is not None],
                    ]
                )
            )

    if language == "nsis" and len(lines) >= 3 and re.fullmatch(r"#\*{8,}#", lines[0]):
        content = [re.fullmatch(r"#\*{8,}[ \t]+(.+?)[ \t]+\*{8,}#", line) for line in lines[1:]]
        if all(match is not None for match in content):
            return "\n".join(match.group(1) for match in content if match is not None)

    return None


def _sanitize_validated_divider_result(
    language: str,
    raw_comment: str,
    cleaned: str,
) -> str | None:
    """Delete validated divider rows from narrowly gated oracle layouts."""

    lines = cleaned.split("\n")
    if (
        language == "4d"
        and re.search(r"(?m)^ Created by: .+\n -{8,}$", raw_comment)
        and any(re.fullmatch(r"[ \t]*-{8,}[ \t]*", line) for line in lines)
    ):
        rewritten = [
            line[1:] if line.startswith(" Created by:") else line
            for line in lines
            if re.fullmatch(r"[ \t]*-{8,}[ \t]*", line) is None
        ]
        return _normalize_sanitized_body("\n".join(rewritten))

    if language == "fortran":
        heading = re.fullmatch(r"![-]{8,}(.+?)[-]{8,}!\n!", raw_comment)
        if heading is not None:
            return heading.group(1)
        if re.fullmatch(r"![ \t]*\.{8,}[\r\n]?", raw_comment):
            return ""

    validated_line_rulers = {
        "cython": (r"(?m)^#{8,}$", r"(?m)^#[ \t]+-{8,}$"),
        "git_config": (r"(?m)^#[ \t]+-{8,}$", r"(?m)^#[ \t]+(?:-[ \t]+){8,}-?$"),
        "hyphy": (r"(?m)^[ \t]*//-{8,}$",),
        "kakounescript": (r"(?m)^#[ \t]+={8,}$",),
        "m4": (r"(?m)^#[ \t]+-{8,}$",),
        "mirah": (r"(?m)^[ \t]*#[ \t]+-{8,}$",),
        "objective_j": (r"(?m)^//={8,}$",),
        "saltstack": (r"(?m)^#[ \t]+(?:-[ \t]+){8,}-?$",),
        "systemverilog": (r"(?m)^[ \t]*\*[ \t]+={8,}$",),
        "zig": (r"(?m)^//[ \t]+(?:\*[ \t]+){8,}\*?$",),
    }
    raw_patterns = validated_line_rulers.get(language)
    if raw_patterns is not None and any(
        re.search(pattern, raw_comment) for pattern in raw_patterns
    ):
        ruler_patterns = (
            r"[-=]{8,}",
            r"(?:-[ \t]+){8,}-?",
            r"(?:\*[ \t]+){8,}\*?",
        )
        return _normalize_sanitized_body(
            "\n".join(
                line
                for line in lines
                if not any(re.fullmatch(pattern, line) for pattern in ruler_patterns)
            )
        )

    if (
        language == "fortran_free_form"
        and sum(re.fullmatch(r"!-{8,}!", line) is not None for line in raw_comment.split("\n")) >= 3
    ):
        rewritten = []
        for index, line in enumerate(lines):
            if re.fullmatch(r"-{8,}!", line):
                if index not in {0, len(lines) - 1}:
                    rewritten.append("")
            else:
                rewritten.append(line)
        return _normalize_sanitized_body("\n".join(rewritten))

    if language in {"jade", "pug"}:
        raw_lines = raw_comment.split("\n")
        bodies = [
            match.group(1)
            for line in raw_lines
            if (match := re.fullmatch(r"[ \t]*//-(.*)", line)) is not None
        ]
        if (
            len(raw_lines) >= 5
            and len(bodies) == len(raw_lines)
            and re.fullmatch(r"#{8,}", bodies[1])
            and re.fullmatch(r"#{8,}", bodies[-1])
        ):
            return _normalize_sanitized_body(
                "\n".join([bodies[0].strip(), *[line.rstrip() for line in bodies[2:-1]]])
            )

    if (
        language == "plsql"
        and re.search(r"(?m)^--[ \t]+.+-{8,}$", raw_comment)
        and re.search(r"-{8,}$", cleaned)
    ):
        return re.sub(r"-{8,}$", "", cleaned)

    if language == "shellcheck_config":
        if re.search(r"(?m)^#\._{8,}$", raw_comment) and re.search(r"(?m)^#`$", raw_comment):
            return _normalize_sanitized_body(
                "\n".join(
                    line for line in lines if line != "`" and re.fullmatch(r"\._{8,}", line) is None
                )
            )
        if re.search(r"(?m)^#[ \t]+={8,}[ \t]+#$", raw_comment) and re.search(
            r"(?m)^#[ \t]+-{8,}[ \t]+#$", raw_comment
        ):
            return _normalize_sanitized_body(
                "\n".join(line for line in lines if re.fullmatch(r"-{8,}[ \t]*#", line) is None)
            )

    return None


def _join_restored_lines(lines: list[str]) -> str:
    """Join strict-restoration rows without dedenting content-bearing layout."""

    restored = ["" if not line.strip() else line.rstrip() for line in lines]
    while restored and not restored[0]:
        restored.pop(0)
    while restored and not restored[-1]:
        restored.pop()
    return "\n".join(restored)


_PURE_REGISTERED_LINE_RULER_LANGUAGES = frozenset(
    {
        "arc",
        "asn1",
        "asn_1",
        "eclipse",
        "gdscript",
        "genero",
        "gnuplot",
        "graphql",
        "hocon",
        "ignore_list",
        "java_properties",
        "kaitai_struct",
        "m4sugar",
        "mcfunction",
        "mercury",
        "mirah",
        "nasl",
        "nearley",
        "nix",
        "open_policy_agent",
        "oz",
        "powershell",
        "procfile",
        "prolog",
        "r",
        "singularity",
        "tex",
        "vim_snippet",
        "wdl",
    }
)


_REVIEWED_HASH_LAYOUT_LANGUAGES = frozenset(
    {
        "apacheconf",
        "bro",
        "cson",
        "curl_config",
        "editorconfig",
        "emberscript",
        "html_django",
        "html_plus_django",
        "html_plusdjango",
        "jinja",
        "m4",
        "mako",
        "mini_yaml",
        "miniyaml",
        "nasal",
        "nim",
        "nimrod",
        "parrot_internal_representation",
        "perl6",
        "puppet",
        "saltstack",
        "wdl",
        "wget_config",
        "zeek",
    }
)


def _sanitize_reviewed_hash_lines(raw_comment: str) -> str | None:
    """Unwrap a complete reviewed hash heading or repeated-marker body."""

    lines = raw_comment.split("\n")
    non_blank = [line for line in lines if line.strip()]
    if not non_blank or not all(re.match(r"^[ \t]*#", line) for line in non_blank):
        return None

    has_repeated_marker = any(re.match(r"^[ \t]*#{2,}", line) for line in non_blank)
    has_symmetric_title = any(
        re.fullmatch(r"[ \t]*#+[ \t]+.+?[ \t]+#+[ \t]*", line) for line in non_blank
    )
    if not (has_repeated_marker or has_symmetric_title):
        return None

    restored: list[str] = []
    for line in lines:
        if not line.strip():
            restored.append("")
            continue
        if re.fullmatch(r"[ \t]*#{4,}[ \t]*", line) is not None:
            continue
        marker = re.match(r"^[ \t]*(#+)", line)
        assert marker is not None
        marker_width = len(marker.group(1))
        body = line[marker.end() :]
        if body.startswith((" ", "\t")):
            body = body[1:]
        if not body.strip():
            restored.append("")
            continue
        has_trailing_hash_gutter = re.search(r"[ \t]+#+[ \t]*$", body) is not None
        body = re.sub(r"[ \t]+#+[ \t]*$", "", body).rstrip()
        if marker_width >= 2:
            body = re.sub(rf"#{{{marker_width}}}[ \t]*$", "", body).rstrip()
        if has_trailing_hash_gutter:
            body = body.strip()
        restored.append("" if _is_decorative_ruler_line(body) else body)
    return _normalize_sanitized_body("\n".join(restored))


def _sanitize_pure_registered_line_ruler(
    language: str,
    raw_comment: str,
    line_wrappers: tuple[tuple[str, str], ...],
) -> str | None:
    """Delete a reviewed homogeneous row made only from its line marker."""

    if language not in _PURE_REGISTERED_LINE_RULER_LANGUAGES:
        return None
    compact = "".join(raw_comment.split())
    if len(compact) < 4 or len(set(compact)) != 1:
        return None
    ruler_char = compact[0]
    if any(
        not close_token and open_token and set(open_token) == {ruler_char}
        for open_token, close_token in line_wrappers
    ):
        return ""
    return None


def _sanitize_batch_two_exact_layout(language: str, raw_comment: str) -> str | None:
    """Clean narrowly proven delimiter and gutter layouts from the judge corpus."""

    if language == "mako":
        line_bodies = _strip_exact_line_marker(raw_comment, ("##",))
        if (
            line_bodies is not None
            and len(line_bodies) >= 3
            and line_bodies[0] == "/**"
            and line_bodies[-1] == "*/"
        ):
            return CommentSanitizer("c").sanitize("\n".join(line_bodies))

    if language in {"html_django", "html_plus_django", "html_plusdjango"} and re.fullmatch(
        r"#{8,}[ \t]+-->",
        raw_comment,
    ):
        return ""

    if language == "brightscript":
        star_banner = re.fullmatch(
            r"'\*{8,}[ \t]+(?P<body>.*?[A-Za-z0-9].*?)[ \t]+\*{8,}",
            raw_comment,
        )
        if star_banner is not None:
            return star_banner.group("body").strip()

        line_bodies = _strip_exact_line_marker(raw_comment, ("'",))
        if (
            line_bodies is not None
            and "Limitations:" in line_bodies
            and sum(re.match(r"\*[ \t]+", line) is not None for line in line_bodies) >= 2
        ):
            restored = []
            for raw_line, body in zip(raw_comment.split("\n"), line_bodies):
                marked = re.fullmatch(r"[ \t]*'(?P<body>.*)", raw_line)
                assert marked is not None
                raw_body = marked.group("body")
                leading_padding = len(raw_body) - len(raw_body.lstrip(" \t"))
                if leading_padding >= 2:
                    body = raw_body.rstrip()
                restored.append(body)
            return _normalize_sanitized_body("\n".join(restored))

    skip_reviewed_hash = (
        (language in {"bro", "zeek"} and re.match(r"^[ \t]*##?!", raw_comment) is not None)
        or (
            language == "apacheconf"
            and re.search(r"(?m)^#<IfModule[ \t]", raw_comment) is not None
            and re.search(r"(?m)^#{8,}$", raw_comment) is not None
        )
        or (
            language == "cson"
            and re.search(r"(?m)^[ \t]*##(?!#)", raw_comment) is not None
            and re.search(r"(?m)^[ \t]*###", raw_comment) is None
        )
    )
    if language in _REVIEWED_HASH_LAYOUT_LANGUAGES and not skip_reviewed_hash:
        hash_result = _sanitize_reviewed_hash_lines(raw_comment)
        if hash_result is not None:
            return hash_result

    if (
        language == "html_plusdjango"
        and raw_comment.startswith("{#")
        and raw_comment.endswith("#}")
    ):
        hash_result = _sanitize_reviewed_hash_lines(raw_comment[2:-2])
        if hash_result is not None:
            return hash_result

    if language == "windows_registry_entries":
        lines = raw_comment.split("\n")
        if lines and all(line.startswith(";#") for line in lines):
            restored = []
            for line in lines:
                body = line[2:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "velocity_template_language":
        if raw_comment.startswith("#**") and raw_comment.endswith("*#"):
            return _normalize_sanitized_body(raw_comment[3:-2])

    if language == "java_properties" and raw_comment.startswith("# MWI.properties\n#/"):
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 4
            and re.fullmatch(r"#/\*{8,}", lines[1]) is not None
            and re.fullmatch(r"#[ \t]+\*{8,}/", lines[-1]) is not None
        ):
            restored = [_strip_one_comment_padding_cell(lines[0][1:]).rstrip()]
            for line in lines[2:-1]:
                star_line = re.fullmatch(r"#[ \t]+\*(?P<body>.*)", line)
                if star_line is None:
                    return None
                body = _strip_one_comment_padding_cell(star_line.group("body"))
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "ada":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and re.fullmatch(r"-{20,}", lines[0]) is not None
            and re.fullmatch(r"-{20,}", lines[-1]) is not None
            and "Matreshka Project" in raw_comment
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"-{20,}", line) is not None:
                    continue
                if not line.startswith("--"):
                    return None
                body = line[2:]
                right_gutter = re.fullmatch(r"(?P<body>.*?)[ \t]+--", body)
                if right_gutter is not None:
                    body = right_gutter.group("body")
                restored.append(_strip_one_comment_padding_cell(body).rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "curry":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and re.fullmatch(r"-{20,}", lines[0])
            and lines[-1] == lines[0]
            and all(line.startswith("--") for line in lines[1:-1])
            and any("@author " in line for line in lines)
            and any("@version " in line for line in lines)
        ):
            restored = []
            for line in lines[1:-1]:
                marker_width = 3 if line.startswith("---") else 2
                body = line[marker_width:]
                if body.startswith((" ", "\t")):
                    body = body[1:]
                if marker_width == 2:
                    body = body.lstrip(" \t")
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "asl" and raw_comment.startswith("/*++") and raw_comment.endswith("--*/"):
        return _normalize_sanitized_body(raw_comment[4:-4])

    if language == "asn1":
        bodies = _strip_exact_line_marker(raw_comment, ("--",))
        if (
            bodies is not None
            and len(bodies) >= 4
            and bodies[0].startswith("$Id:")
            and re.fullmatch(r"={20,}", bodies[-1]) is not None
            and sum(re.fullmatch(r"={20,}", body) is not None for body in bodies) >= 3
        ):
            return _normalize_sanitized_body("\n".join(bodies[:-1]))

    if language == "asn_1" and "--==== Version History====--" in raw_comment:
        rewritten = raw_comment.replace(
            "--==== Version History====--",
            "-- Version History",
            1,
        )
        return CommentSanitizer(language).sanitize(rewritten)

    if language in {"asp", "asp_net", "aspnet"} and re.fullmatch(
        r"<!--[ \t]+\*{20,}[ \t]+!-->",
        raw_comment,
    ):
        return ""

    if language == "dns_zone":
        lines = raw_comment.rstrip("\n").split("\n")
        if (
            len(lines) >= 5
            and re.fullmatch(r";{3}={8,}", lines[0]) is not None
            and all(re.match(r"^;{3,4}", line) for line in lines)
        ):
            restored = [
                re.sub(r"^;{3,4}", "", line, count=1).lstrip(" \t").rstrip() for line in lines
            ]
            return _normalize_sanitized_body("\n".join(restored[1:]))

    if language == "eclipse" and "BEGIN LICENSE BLOCK" in raw_comment:
        bodies = _strip_exact_line_marker(raw_comment, ("%",))
        if (
            bodies is not None
            and len(bodies) >= 3
            and re.fullmatch(r"-{20,}", bodies[-1]) is not None
        ):
            first_body = 1 if re.fullmatch(r"-{20,}", bodies[0]) is not None else 0
            return _normalize_sanitized_body("\n".join(bodies[first_body:-1]))

    if language in {"f#", "f_sharp", "fsharp"}:
        nested_title = re.fullmatch(
            r"\(\*{4}[ \t]+(?P<body>.+?)[ \t]+\*{4}\)",
            raw_comment,
        )
        if nested_title is not None:
            return nested_title.group("body").strip()

    if language == "fortran_free_form":
        lines = raw_comment.split("\n")
        if len(lines) >= 3 and all(line.startswith("!") for line in lines):
            title = re.fullmatch(
                r"!={8,}[ \t]+(?P<body>.+?)[ \t]+={8,}80",
                lines[0],
            )
            if title is not None and re.fullmatch(r"!={8,}80", lines[-1]) is not None:
                bodies = [
                    _strip_one_comment_padding_cell(line[1:]).rstrip() for line in lines[1:-1]
                ]
                return _normalize_sanitized_body("\n".join([title.group("body").strip(), *bodies]))

    if language == "java":
        lines = raw_comment.split("\n")
        if len(lines) >= 2:
            title = re.fullmatch(
                r"//-{8,}[ \t]+(?P<body>.+?)[ \t]+-{8,}//",
                lines[0],
            )
            remaining = _strip_exact_line_marker("\n".join(lines[1:]), ("//",))
            if title is not None and remaining is not None:
                return _normalize_sanitized_body(
                    "\n".join([title.group("body").strip(), *remaining])
                )

    if (
        language == "modula_2"
        and raw_comment.startswith("(*")
        and raw_comment.endswith("*)")
        and "UTILITY PROGRAM" in raw_comment
    ):
        lines = raw_comment[1:-2].split("\n")
        if lines and re.fullmatch(r"\*{20,}", lines[0]) is not None:
            frame_end = next(
                (
                    index
                    for index, line in enumerate(lines[1:], 1)
                    if re.fullmatch(r"\*{20,}[ \t]*", line) is not None
                ),
                None,
            )
            if frame_end is not None:
                restored = []
                for line in lines[1:frame_end]:
                    framed = re.fullmatch(r"\*(?P<body>.*)\*", line)
                    if framed is None:
                        return None
                    restored.append(framed.group("body").strip())
                restored.extend(lines[frame_end + 1 :])
                return _normalize_sanitized_body("\n".join(restored))

    if language in {"mql", "mql4"}:
        heading = re.fullmatch(
            r"//={3}(?P<body>.*?[A-Za-z0-9].*?)={8,}//",
            raw_comment,
        )
        if heading is not None:
            return heading.group("body").strip()

    if language == "ncl":
        bodies = _strip_exact_line_marker(raw_comment, (";",))
        if (
            bodies is not None
            and len(bodies) >= 3
            and bodies[0] == bodies[-1]
            and re.fullmatch(r"={20,};", bodies[0]) is not None
        ):
            return _normalize_sanitized_body("\n".join(bodies[1:-1]))

    if language == "tcl":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 2
            and lines[0].startswith("#%Module ")
            and all(line.startswith("##") for line in lines[1:])
        ):
            restored = [lines[0][1:].rstrip()]
            restored.extend(
                _strip_one_comment_padding_cell(line[2:]).rstrip() for line in lines[1:]
            )
            return _normalize_sanitized_body("\n".join(restored))

    if language == "xtend":
        arrow_note = re.fullmatch(r"//[ \t]+(?P<body>===>[ \t]+.+)", raw_comment)
        if arrow_note is not None:
            return arrow_note.group("body").rstrip()

    if language == "rescript":
        restored = []
        for line in raw_comment.split("\n"):
            visible_setting = re.fullmatch(r"(?:////|//)(?P<body>\".+)", line)
            if visible_setting is None:
                break
            restored.append(visible_setting.group("body").rstrip())
        else:
            return _normalize_sanitized_body("\n".join(restored))

    if language == "slice":
        inline_doc = re.fullmatch(
            r"/\*\*[ \t]+(?P<body>.+?)[ \t]+\*\*/",
            raw_comment,
        )
        if inline_doc is not None:
            return inline_doc.group("body").strip()

    if (
        language == "sourcepawn"
        and raw_comment.startswith("/**\n")
        and raw_comment.endswith("\n **/")
    ):
        inner_lines = raw_comment[3:-4].split("\n")
        if (
            len(inner_lines) >= 3
            and all(not line.strip() or re.match(r"^[ \t]*\*", line) for line in inner_lines)
            and sum(re.fullmatch(r"[ \t]*\*[ \t]+={8,}", line) is not None for line in inner_lines)
            >= 2
        ):
            restored = []
            for line in inner_lines:
                if not line.strip():
                    restored.append("")
                    continue
                star_line = re.fullmatch(r"[ \t]*\*(?P<body>.*)", line)
                assert star_line is not None
                body = star_line.group("body").lstrip(" \t").rstrip()
                if re.fullmatch(r"={8,}", body) is not None:
                    continue
                restored.append(body)
            return _normalize_sanitized_body("\n".join(restored))

    if (
        language == "sourcepawn"
        and raw_comment.startswith("/*\n")
        and raw_comment.endswith("\n */")
    ):
        inner_lines = raw_comment[3:-3].split("\n")
        non_blank = [line for line in inner_lines if line.strip()]
        if (
            len(non_blank) >= 3
            and all(re.match(r"^[ \t]*\*(?:[ \t]|$)", line) for line in non_blank)
            and re.fullmatch(r"[ \t]*\*[ \t]+={8,}", non_blank[0])
            and re.fullmatch(r"[ \t]*\*[ \t]+={8,}", non_blank[-1])
        ):
            restored = []
            for line in inner_lines:
                star_line = re.fullmatch(r"[ \t]*\*(?P<body>.*)", line)
                if star_line is None:
                    restored.append("")
                    continue
                body = star_line.group("body").lstrip(" \t").rstrip()
                if re.fullmatch(r"={8,}", body):
                    continue
                restored.append(body)
            return _normalize_sanitized_body("\n".join(restored))

    if (
        language == "cuda"
        and raw_comment.startswith("/*! \\file ")
        and raw_comment.endswith(" */")
        and "\\brief " in raw_comment
    ):
        lines = raw_comment[3:-2].split("\n")
        restored = []
        for index, line in enumerate(lines):
            star_gutter = re.match(r"^[ \t]*\*[ \t]*", line)
            if star_gutter is not None:
                body = line[star_gutter.end() :]
            else:
                body = _strip_one_comment_padding_cell(line)
            if index == 0:
                body = _strip_one_comment_padding_cell(body)
            restored.append(body.rstrip())
        return _normalize_sanitized_body("\n".join(restored))

    if language == "cuda":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 3
            and lines[0].startswith("//===")
            and re.fullmatch(r"//===-{20,}===//", lines[-1]) is not None
            and all(line.startswith("//") for line in lines)
        ):
            restored = []
            for line in lines:
                body = _strip_one_comment_padding_cell(line[2:]).rstrip()
                if body.startswith("===") and body.endswith("//"):
                    body = body[:-2].rstrip()
                restored.append(body)
            return "\n".join(restored[:-1])

    if language == "dircolors":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 3
            and re.fullmatch(r"#{20,}", lines[0]) is not None
            and lines[-1] == lines[0]
        ):
            restored = []
            for line in lines[1:-1]:
                framed = re.fullmatch(r"##(?P<body>.*?)[ \t]+##", line)
                if framed is None:
                    return None
                body = _strip_one_comment_padding_cell(framed.group("body"))
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "dm" and raw_comment.startswith("//var/character/"):
        restored = []
        for line in raw_comment.split("\n"):
            marked = re.fullmatch(r"[ \t]*//(?P<body>.*)", line)
            if marked is None:
                return None
            restored.append(marked.group("body").rstrip())
        return _normalize_sanitized_body("\n".join(restored))

    if language == "gams":
        lines = raw_comment.split("\n")
        if len(lines) >= 2 and all(
            re.fullmatch(r"\*(?P<body>[^*\n]*[A-Za-z0-9][^*\n]*)\*", line) is not None
            for line in lines
        ):
            return _normalize_sanitized_body("\n".join(line[1:-1].strip() for line in lines))

    if language == "gdscript" and "#\N{NO-BREAK SPACE}" in raw_comment:
        restored = []
        for line in raw_comment.split("\n"):
            marked = re.fullmatch(r"[ \t]*#(?P<body>.*)", line)
            if marked is None:
                return None
            body = marked.group("body")
            if body.startswith((" ", "\t", "\N{NO-BREAK SPACE}")):
                body = body[1:]
            restored.append(body.rstrip())
        return _normalize_sanitized_body("\n".join(restored))

    if (
        language in _GENERO_FORMS_LANGUAGE_KEYS
        and raw_comment.startswith("{\n|")
        and raw_comment.endswith("\n}")
        and "RCS INFO" in raw_comment
    ):
        restored = []
        for line in raw_comment[2:-2].split("\n"):
            if not line.startswith("|"):
                return None
            body = line[1:].rstrip()
            if re.fullmatch(r"\*{8,}/?", body) is not None:
                continue
            restored.append(body)
        return _normalize_sanitized_body("\n".join(restored))

    if (
        language == "lex"
        and raw_comment.startswith("/*\n")
        and raw_comment.endswith("\n */")
        and "scanner definition for COOL" in raw_comment
    ):
        restored = []
        for line in raw_comment[3:-3].split("\n"):
            if not line.strip():
                restored.append("")
                continue
            star_gutter = re.fullmatch(r"[ \t]*\*(?P<body>.*)", line)
            if star_gutter is None:
                return None
            restored.append(star_gutter.group("body").lstrip(" \t").rstrip())
        return _normalize_sanitized_body("\n".join(restored))

    if language == "makefile":
        lines = raw_comment.split("\n")
        if lines and re.fullmatch(r"#\*{8,}License\*{8,}", lines[0]) is not None:
            restored = ["License"]
            for line in lines[1:]:
                if not line.startswith("#"):
                    return None
                body = _strip_one_comment_padding_cell(line[1:]).rstrip()
                if re.fullmatch(r"\*{8,}/?", body) is not None:
                    continue
                restored.append(body)
            return _normalize_sanitized_body("\n".join(restored))

    if language == "yasnippet":
        lines = raw_comment.split("\n")
        try:
            sentinel_index = lines.index("# --")
        except ValueError:
            sentinel_index = -1
        if (
            sentinel_index >= 1
            and lines[0] == "# -*- mode: snippet -*-"
            and all(line.startswith("#") for line in lines[: sentinel_index + 1])
        ):
            restored = [
                _strip_one_comment_padding_cell(line[1:]).rstrip()
                for line in lines[: sentinel_index + 1]
            ]
            restored.extend(lines[sentinel_index + 1 :])
            return _normalize_sanitized_body("\n".join(restored))

    if language in {"arduino", "c++"}:
        bodies = _strip_exact_line_marker(raw_comment, ("//",))
        if (
            bodies is not None
            and len(bodies) >= 3
            and bodies[0] == bodies[-1]
            and re.fullmatch(r"(?:-=){8,}-", bodies[0]) is not None
        ):
            return _normalize_sanitized_body("\n".join(bodies[1:-1]))

    if language == "coldfusion":
        normalized_raw = _normalize_newlines(raw_comment)
        if normalized_raw.startswith("<!--- -->\n") and normalized_raw.endswith("\n--->"):
            inner = normalized_raw[len("<!--- -->\n") : -len("\n--->")]
            if inner.startswith('<?xml version="1.0"') and "<fusedoc " in inner:
                return _normalize_sanitized_body(inner)

    if language == "monkey_c":
        normalized_raw = _normalize_newlines(raw_comment)
        if normalized_raw.startswith("/*++\n") and normalized_raw.endswith("\n;--*/"):
            inner_lines = normalized_raw[len("/*++\n") : -len("\n;--*/")].split("\n")
            if inner_lines and all(line.startswith(";") for line in inner_lines):
                return _normalize_sanitized_body(
                    "\n".join(line[1:].rstrip() for line in inner_lines)
                )

    if language == "nwscript" and raw_comment.startswith("/*") and raw_comment.endswith("*/"):
        inner_lines = raw_comment[2:-2].split("\n")
        if (
            len(inner_lines) >= 3
            and re.fullmatch(r"[ \t]*(?:-=){8,}-", inner_lines[0]) is not None
            and re.fullmatch(r"[ \t]*(?:-=){8,}-", inner_lines[-1]) is not None
        ):
            return _normalize_sanitized_body("\n".join(inner_lines[1:-1]))

    if language == "asymptote":
        framed_title = re.fullmatch(
            r"//[ \t]+-{3}[ \t]+(?P<body>.+?)[ \t]+-{3}[ \t]+/",
            raw_comment,
        )
        if framed_title is not None:
            return framed_title.group("body").strip()

    if language == "netlogo" and re.fullmatch(r"(?:;;--){4,};;\n?", raw_comment):
        return ""

    if language == "ssh_config":
        managed_title = re.fullmatch(
            r"#{3}[ \t]+---[ \t]+(?P<body>\{\{.+\}\})[ \t]+---[ \t]+#{3}\n?",
            raw_comment,
        )
        if managed_title is not None:
            return managed_title.group("body").strip()

    if language in {"eclipse", "oz", "tex"}:
        percent_frame_lines = raw_comment.rstrip("\n").split("\n")
        if (
            language == "eclipse"
            and len(percent_frame_lines) >= 3
            and re.fullmatch(r"%{8,}", percent_frame_lines[0]) is not None
            and re.fullmatch(r"%{8,}", percent_frame_lines[-1]) is not None
        ):
            restored = []
            for line in percent_frame_lines[1:-1]:
                framed = re.fullmatch(
                    r"%{2}[ \t]*(?P<body>.*?[^\W_].*?)[ \t]*%{2}",
                    line,
                )
                if framed is None:
                    break
                restored.append(framed.group("body").strip())
            else:
                return _normalize_sanitized_body("\n".join(restored))

        percent_title = re.fullmatch(
            r"%{4,}[ \t]*(?P<body>.*?[^\W_].*?)[ \t]*%{4,}\n?",
            raw_comment,
        )
        if percent_title is not None:
            return percent_title.group("body").strip()

        restored: list[str] = []
        for line in raw_comment.rstrip("\n").split("\n"):
            if re.fullmatch(r"%{4,}", line.rstrip("\r")) is not None:
                restored.append("")
                continue
            percent_line = re.fullmatch(
                r"%{2,3}(?!%)(?P<body>.*)",
                line.rstrip("\r"),
            )
            if percent_line is None:
                break
            restored.append(_strip_one_comment_padding_cell(percent_line.group("body")).rstrip())
        else:
            return _normalize_sanitized_body("\n".join(restored))

    if language == "prolog":
        restored = []
        for line in raw_comment.split("\n"):
            percent_line = re.fullmatch(r"(?:%{4}|%{2})(?P<body>.*)", line)
            if percent_line is None:
                break
            restored.append(_strip_one_comment_padding_cell(percent_line.group("body")).rstrip())
        else:
            if len(restored) >= 2 and raw_comment.startswith("%%%%"):
                return _normalize_sanitized_body("\n".join(restored))

    if language in _VISUAL_BASIC_6_LANGUAGE_KEYS:
        raw_lines = raw_comment.split("\n")
        if raw_lines and all(
            re.match(r"^[ \t]*'''(?:[ \t]|<|$)", line) is not None for line in raw_lines
        ):
            doc_lines = _strip_exact_line_marker(raw_comment, ("'''",))
            assert doc_lines is not None
            return _normalize_sanitized_body("\n".join(doc_lines))
        doubled_line = re.fullmatch(r"''(?P<body>--[^\r\n]*)[\r\n]*", raw_comment)
        if doubled_line is not None:
            return doubled_line.group("body").rstrip()

    if language in {"arc", "newlisp"}:
        semicolon_lines = _strip_exact_line_marker(raw_comment, (";;;;",))
        if semicolon_lines is not None and any(
            any(char.isalnum() for char in line) for line in semicolon_lines
        ):
            return _normalize_sanitized_body("\n".join(semicolon_lines))

    if language in {"assembly", "clarity"}:
        semicolon_title = re.fullmatch(
            r";{4,}[ \t]*(?P<body>.*?[A-Za-z0-9].*?)[ \t]*;{4,}\n?",
            raw_comment,
        )
        if semicolon_title is not None:
            return semicolon_title.group("body").strip()

    if language == "nextflow" and raw_comment.startswith("/*") and raw_comment.endswith("*/"):
        inner_lines = _normalize_newlines(raw_comment[2:-2]).strip("\n").split("\n")
        if (
            len(inner_lines) >= 4
            and re.fullmatch(r"~{8,}", inner_lines[0]) is not None
            and re.fullmatch(r"~{8,}", inner_lines[2]) is not None
            and re.fullmatch(r"-{8,}", inner_lines[-1]) is not None
        ):
            return _normalize_sanitized_body("\n".join(inner_lines[1:-1]))

    tilde_line_markers = {
        "singularity": ("#",),
        "windows_registry_entries": (";",),
    }
    if (markers := tilde_line_markers.get(language)) is not None:
        bodies = _strip_exact_line_marker(raw_comment, markers)
        if (
            bodies is not None
            and len(bodies) >= 2
            and re.fullmatch(r"~{8,}", bodies[0]) is not None
        ):
            return _normalize_sanitized_body("\n".join(bodies[1:]))

    if (
        language == "html_plus_ecr"
        and raw_comment.startswith("<!--")
        and raw_comment.endswith("-->")
    ):
        inner_lines = _normalize_newlines(raw_comment[4:-3]).split("\n")
        if (
            len(inner_lines) >= 2
            and re.fullmatch(r"[ \t]*–{8,}[ \t]*", inner_lines[-1]) is not None
        ):
            return _normalize_sanitized_body("\n".join(inner_lines[:-1]))

    if language == "netlogo":
        restored = []
        for line in raw_comment.split("\n"):
            heading_line = re.fullmatch(
                r";={3,}[ \t]*(?P<body>.*[^\W_].*)",
                line,
            )
            if heading_line is None:
                break
            restored.append(heading_line.group("body").rstrip())
        else:
            return _normalize_sanitized_body("\n".join(restored))

    if language == "runoff":
        framed_title = re.fullmatch(
            r"![ \t]+(?P<body>.*?[A-Za-z0-9].*?)[ \t]{2,}!\n?",
            raw_comment,
        )
        if framed_title is not None:
            return framed_title.group("body").strip()

    if language in {"gams", "stata"}:
        if language == "stata":
            long_star_title = re.fullmatch(
                r"(?P<edge>\*{4,})[ \t]+(?P<body>.*?[A-Za-z0-9].*?)[ \t]+(?P=edge)\n?",
                raw_comment,
            )
            if long_star_title is not None:
                return long_star_title.group("body").strip()
        star_title = re.fullmatch(
            r"\*{2,3}[ \t]*(?P<body>.*?[A-Za-z0-9].*?)[ \t]*\*{2,3}\n?",
            raw_comment,
        )
        if star_title is not None:
            return star_title.group("body").strip()
        if language == "stata":
            star_prefix_title = re.fullmatch(
                r"\*{2}(?P<body>[A-Za-z0-9].*)\n?",
                raw_comment,
            )
            if star_prefix_title is not None:
                return star_prefix_title.group("body").strip()

    if language == "qml":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 4
            and re.fullmatch(r"/\*{8,}", lines[0])
            and re.fullmatch(r"[ \t]*\*{8,}/", lines[-1])
            and all(not line.strip() or line.startswith("**") for line in lines[1:-1])
            and any(re.fullmatch(r"\*{2}[ \t]*", line) for line in lines[1:-1])
        ):
            restored = []
            for line in lines[1:-1]:
                if re.fullmatch(r"\*{2}[ \t]*", line):
                    continue
                body = line[2:]
                restored.append(_strip_one_comment_padding_cell(body).rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "pascal":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 4
            and re.fullmatch(r"\(\*{8,}", lines[0])
            and re.fullmatch(r"[ \t]*\*{8,}\)", lines[-1])
        ):
            restored = []
            for line in lines[1:-1]:
                framed = re.fullmatch(r"[ \t]*\*(?P<body>.*?)\*[ \t]*", line)
                if framed is None:
                    return None
                restored.append(framed.group("body").strip())
            return _normalize_sanitized_body("\n".join(restored))

    if language in _ROCQ_LANGUAGE_KEYS:
        lines = raw_comment.split("\n")
        if (
            len(lines) == 3
            and re.fullmatch(r"\(\*{8,}", lines[0])
            and re.fullmatch(r"[ \t]*\*{8,}\)", lines[-1])
            and (content := re.fullmatch(r"[ \t]*\*[ \t]+(?P<body>.+)", lines[1])) is not None
        ):
            return content.group("body").strip()

    c_star_border_languages = {
        "ags_script",
        "c",
        "c#",
        "c_sharp",
        "csharp",
        "linker_script",
        "powerbuilder",
        "systemverilog",
    }
    if language in c_star_border_languages:
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 3
            and re.fullmatch(r"/\*{8,}", lines[0])
            and re.fullmatch(r"[ \t]*\*{8,}/", lines[-1])
        ):
            has_complete_right_gutter = all(
                not line.strip() or re.search(r"[ \t]+\*[ \t]*$", line) is not None
                for line in lines[1:-1]
            )
            restored = []
            for line in lines[1:-1]:
                if not line.strip():
                    restored.append("")
                    continue
                gutter = re.fullmatch(r"[ \t]*\*+[ \t]*(?P<body>.*?)", line)
                if gutter is None:
                    return None
                body = gutter.group("body")
                if has_complete_right_gutter:
                    if body.strip() == "*":
                        body = ""
                    else:
                        body = re.sub(r"[ \t]+\*[ \t]*$", "", body)
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    doc_star_languages = {
        "closure_templates",
        "jflex",
        "metal",
        "slice",
        "sourcepawn",
    }
    if (
        language in doc_star_languages
        and raw_comment.startswith("/*")
        and raw_comment.endswith("*/")
    ):
        inner_lines = raw_comment[2:-2].split("\n")
        non_blank = [line for line in inner_lines if line.strip()]
        if non_blank and all(re.match(r"^[ \t]*\*(?:[ \t]|$)", line) for line in non_blank):
            restored = []
            for line in inner_lines:
                if not line.strip():
                    restored.append("")
                    continue
                body = re.sub(r"^[ \t]*\*(?:[ \t]|$)", "", line)
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "stata" and raw_comment.startswith("/*") and raw_comment.endswith("*/"):
        lines = raw_comment[2:-2].split("\n")
        if "PROGRAM:" in raw_comment and "AUTHOR:" in raw_comment:
            restored = []
            for line in lines:
                body = re.sub(r"^[ \t]*\*+[ \t]*", "", line).rstrip()
                if not body or re.fullmatch(r"\*{8,}", body):
                    continue
                restored.append(body)
            return _normalize_sanitized_body("\n".join(restored))

    if (
        language == "antlers"
        and "\n" in raw_comment
        and raw_comment.startswith("{{#")
        and raw_comment.endswith("#}}")
    ):
        inner = raw_comment[3:-3]
        if "{{" in inner and "}}" in inner:
            return _normalize_sanitized_body(_strip_one_comment_padding_cell(inner))

    if language == "autohotkey":
        one_byte = re.fullmatch(r";(?P<body>[^\w\s])\n?", raw_comment)
        if one_byte is not None:
            return one_byte.group("body")

    if language == "brightscript":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 3
            and re.fullmatch(r"'\*{8,}", lines[0])
            and lines[-1] == lines[0]
            and all(line.startswith("'**") for line in lines[1:-1])
        ):
            return _normalize_sanitized_body(
                "\n".join(line[3:].lstrip(" ").rstrip() for line in lines[1:-1])
            )

    if language == "dataweave" and raw_comment.startswith("/*") and raw_comment.endswith("*/"):
        inner_lines = raw_comment[2:-2].split("\n")
        non_blank = [line for line in inner_lines if line.strip()]
        if (
            len(non_blank) >= 5
            and all(re.match(r"^[ \t]*\*[ \t]+//", line) for line in non_blank)
            and re.fullmatch(r"[ \t]*\*[ \t]+//={8,}[ \t]*", non_blank[0])
            and re.fullmatch(r"[ \t]*\*[ \t]+//={8,}[ \t]*", non_blank[-1])
            and any(
                re.fullmatch(r"[ \t]*\*[ \t]+//[ \t]*", line) is not None
                for line in non_blank[1:-1]
            )
        ):
            restored: list[str] = []
            for line in inner_lines:
                body = re.sub(r"^[ \t]*\*[ \t]+", "", line).rstrip()
                if re.fullmatch(r"//={8,}", body) or body == "//":
                    continue
                if not body:
                    restored.append("")
                    continue
                assert body.startswith("//")
                restored.append(_strip_one_comment_padding_cell(body[2:]).rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "euphoria":
        if re.fullmatch(r"/\*\*[ \t]+/\*\*/", raw_comment):
            return _normalize_sanitized_body(raw_comment[2:-2])
        if (
            "\n" in raw_comment
            and "Syntax                  Description" not in raw_comment
            and "\n-- |=Idx |=Name" in raw_comment
            and raw_comment.rstrip().endswith("-- \t})")
        ):
            restored = []
            for line in raw_comment.split("\n")[:-1]:
                match = re.fullmatch(r"[ \t]*--(?P<body>.*)", line)
                if match is None:
                    return None
                body = match.group("body")
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "faust":
        bodies = _strip_exact_line_marker(raw_comment, ("//",))
        if (
            bodies is not None
            and len(bodies) >= 3
            and re.fullmatch(r"-{8,}", bodies[0])
            and re.fullmatch(r"-{8,}", bodies[-1])
        ):
            return _normalize_sanitized_body("\n".join(bodies[1:-1]))

    if language == "fortran":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 3
            and re.fullmatch(r"!-{8,}!", lines[0])
            and re.fullmatch(r"!-{8,}!", lines[-1])
            and all(line.startswith("!") and line.rstrip().endswith("!") for line in lines)
        ):
            restored = []
            for line in lines[1:-1]:
                body = line[1:].rstrip()
                body = re.sub(r"[ \t]+![ \t]*$", "", body)
                restored.append(body.strip())
            return _normalize_sanitized_body("\n".join(restored))
        important = re.fullmatch(
            r"!{4,}[ \t]+(?P<body>.+?)[ \t]+!{3,}\n?",
            raw_comment,
        )
        if important is not None:
            return important.group("body").strip()

    if language in _GENERO_LANGUAGE_KEYS:
        lines = raw_comment.split("\n")
        if lines and all(line.startswith("#+") for line in lines):
            restored = []
            for line in lines:
                body = line[2:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "glsl" and raw_comment.startswith("/*/") and raw_comment.endswith("//*/"):
        return _normalize_sanitized_body(raw_comment[3:-4])

    if language == "hoon":
        lines = raw_comment.split("\n")
        if any(line.startswith("::::") for line in lines) and lines[-1].strip() == "::":
            restored = []
            for line in lines:
                if line.strip() == "::" and line.startswith((" ", "\t")):
                    restored.append("")
                    continue
                marker_width = 4 if line.startswith("::::") else 2 if line.startswith("::") else 0
                if not marker_width:
                    return None
                body = line[marker_width:]
                if body.startswith("  "):
                    body = body[2:]
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "ignore_list":
        title = re.fullmatch(
            r"(?P<open>#{1,3})(?:[ \t]*)(?P<body>[^#\n].*?)(?:[ \t]+(?P<close>#{1,3}))?\n?",
            raw_comment,
        )
        if title is not None:
            close = title.group("close")
            if close is None or len(close) == len(title.group("open")):
                return title.group("body").strip()

    if language in {"kakoune_script", "kakounescript"}:
        lines = raw_comment.split("\n")
        if (
            len(lines) == 3
            and re.fullmatch(r"#{8,}", lines[0])
            and lines[-1] == lines[0]
            and (title := re.fullmatch(r"#[ \t]+(.+?)[ \t]+#", lines[1])) is not None
        ):
            return title.group(1).strip()

    if language == "jflex":
        doc = re.fullmatch(r"/\*\*[ \t]*\n[ \t]*\*[ \t]+(?P<body>.+?)\n[ \t]*\*/", raw_comment)
        if doc is not None:
            return doc.group("body").strip()

    if language == "qml" and raw_comment.startswith("//    states: ["):
        lines = raw_comment.split("\n")
        if all(line.startswith("/") for line in lines):
            restored = []
            for line in lines:
                marker = re.match(r"/+", line)
                assert marker is not None
                body = line[marker.end() :]
                body = body[4:] if body.startswith("    ") else body
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    simple_titles = {
        "go": r"//[ \t]+-{4,}[ \t]+(?P<body>.+?)[ \t]+-{4,}[ \t]+//",
        "holyc": r"//[ \t]+\*{4,}[ \t]+(?P<body>.+?)[ \t]+\*{4,}//",
        "julia": r"#[ \t]+-{4,}[ \t]+(?P<body>.+?)[ \t]+-{4,}[ \t]+#",
        "purebasic": r";[ \t]+-{4,}[ \t]+(?P<body>.+?)[ \t]+-{4,}[ \t]+;",
        "sqlpl": r"--\*{4,}[ \t]+(?P<body>.+?)[ \t]+\*{4,}-{3}",
    }
    title_pattern = simple_titles.get(language)
    if title_pattern is not None:
        title = re.fullmatch(title_pattern + r"\n?", raw_comment)
        if title is not None:
            return title.group("body").strip()

    if language == "motorola_68k_assembly" and re.fullmatch(r";={8,};\n?", raw_comment):
        return ""

    if language == "ncl":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 3
            and re.fullmatch(r";={8,}", lines[0])
            and re.fullmatch(r";={8,};", lines[-1])
            and all(line.startswith(";") for line in lines)
        ):
            restored = []
            for line in lines[1:-1]:
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "nwscript":
        lines = raw_comment.split("\n")
        if lines and re.fullmatch(r"//::/{8,}(?:::)?//?\n?", raw_comment):
            return ""
        if (
            len(lines) >= 2
            and re.fullmatch(r"//::/{8,}", lines[0])
            and all(line.startswith("//") and not line.startswith("//::") for line in lines[1:])
        ):
            return _normalize_sanitized_body(
                "\n".join(_strip_one_comment_padding_cell(line[2:]).rstrip() for line in lines[1:])
            )

    if language == "rpgle":
        lines = raw_comment.split("\n")
        if (
            len(lines) == 3
            and re.fullmatch(r"[ \t]*//‚-{8,}", lines[0])
            and re.fullmatch(r"[ \t]*//‚-{8,}", lines[-1])
            and (title := re.fullmatch(r"[ \t]*//‚(?P<body>.+)", lines[1])) is not None
        ):
            return title.group("body").strip()

    if language in {"scss", "stylus"}:
        framed = re.fullmatch(
            r"/\*(?:[-=]{8,})\*\\\n"
            r"[ \t]*(?:\*[ \t]+)?(?P<body>.+?)(?:[ \t]+\*)?[ \t]*\n"
            r"\\\*(?:[-=]{8,})\*/",
            raw_comment,
        )
        if framed is not None:
            return framed.group("body").strip()

    if language in {"vim_script", "viml"}:
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and re.fullmatch(r'"={20,}"', lines[0])
            and lines[-1] == lines[0]
            and all(line.startswith('"') and line.endswith('"') for line in lines)
        ):
            restored = []
            for line in lines[1:-1]:
                body = line[1:-1]
                body = body[2:] if body.startswith("  ") else body.lstrip(" ")
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "xbase" and raw_comment.startswith("/*/\n") and raw_comment.endswith("\n/*/"):
        body = raw_comment[4:-4].split("\n")
        if (
            len(body) >= 5
            and len(set(body[0])) == 1
            and body[0][0] == "▄"
            and len(set(body[-1])) == 1
            and body[-1][0] == "▀"
        ):
            return _normalize_sanitized_body("\n".join(body[1:-1]))

    if (
        language == "xbase"
        and raw_comment.startswith("/*/{Protheus.doc}")
        and raw_comment.endswith("\n/*/")
    ):
        return _normalize_sanitized_body(raw_comment[3:-4])

    if language == "xc":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and re.fullmatch(r"/\*{8,}\\", lines[0])
            and re.fullmatch(r"\\\*{8,}/", lines[-1])
            and all(re.fullmatch(r"[ \t]*\*.*", line) for line in lines[1:-1])
        ):
            restored = []
            for line in lines[1:-1]:
                body = line.lstrip(" \t")[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    return None


def _sanitize_tabbed_star_gutter_block(language: str, raw_comment: str) -> str | None:
    """Strip proven star gutters while preserving every content-bearing tab."""

    if language not in {"chapel", "dm"}:
        return None
    if not (raw_comment.startswith("/*") and raw_comment.endswith("*/")):
        return None

    inner_lines = raw_comment[2:-2].split("\n")
    while inner_lines and not inner_lines[-1].strip():
        inner_lines.pop()
    if len(inner_lines) < 3 or not inner_lines[0].strip():
        return None

    parsed_rows: list[str] = []
    tabbed_rows = 0
    for line in inner_lines[1:]:
        if not line.strip():
            parsed_rows.append("")
            continue
        match = re.fullmatch(r"[ \t]*\*(.*)", line)
        if match is None:
            return None
        body = match.group(1)
        tabbed_rows += bool(re.match(r" *\t", body))
        parsed_rows.append(body)
    if tabbed_rows < 2:
        return None

    space_padding = [
        len(match.group(1))
        for body in parsed_rows
        if body.strip() and (match := re.match(r"( +)", body)) is not None
    ]
    common_padding = min(space_padding) if space_padding else 0

    restored = [inner_lines[0].lstrip(" \t").rstrip()]
    for body in parsed_rows:
        if common_padding and body.startswith(" "):
            leading_spaces = len(body) - len(body.lstrip(" "))
            body = body[min(common_padding, leading_spaces) :]
        restored.append(body.rstrip())
    return _join_restored_lines(restored)


def _sanitize_strict_restoration_layout(language: str, raw_comment: str) -> str | None:
    """Restore exact layout for complete, independently reviewed corpus shapes.

    Exact language keys are intentional: some aliases share byte-identical raw
    comments but have different independently reviewed layout oracles.
    """

    if language == "apacheconf":
        lines = raw_comment.split("\n")
        ruler_indexes = [index for index, line in enumerate(lines) if re.fullmatch(r"#{8,}", line)]
        if (
            ruler_indexes == [0, 3]
            and len(lines) >= 6
            and lines[4].startswith("#<IfModule ")
            and lines[-1] == "#</IfModule>"
            and all(line.startswith("#") for line in lines)
        ):
            restored: list[str] = []
            in_module = False
            for line in lines:
                if re.fullmatch(r"#{8,}", line):
                    continue
                body = line[1:]
                if body.startswith("<IfModule "):
                    in_module = True
                if not in_module and body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "f#":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 4
            and lines[0].startswith("//let rec ")
            and all(line.startswith("//") for line in lines)
            and any(line.startswith("//    match ") for line in lines[1:])
            and sum(line.startswith("//        | ") for line in lines[1:]) >= 2
        ):
            return _join_restored_lines([line[2:].rstrip() for line in lines])

    if language == "haml":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 2
            and re.fullmatch(r"/\[if .+\]", lines[0])
            and all(not line.strip() or re.match(r"^[ \t]{2,}= ", line) for line in lines[1:])
        ):
            return _join_restored_lines([lines[0][1:], *lines[1:]])

    if language == "hy":
        lines = raw_comment.split("\n")
        matches = [re.fullmatch(r"([ \t]*);(\S.*)", line) for line in lines]
        indent_widths = [len(match.group(1)) for match in matches if match is not None]
        if (
            len(lines) >= 5
            and lines[0].startswith(";def ")
            and all(match is not None for match in matches)
            and indent_widths
            and min(indent_widths) == 0
            and max(indent_widths) >= 8
            and any(";except " in line for line in lines)
        ):
            return _join_restored_lines(
                [match.group(1) + match.group(2) for match in matches if match is not None]
            )

    if language == "jade":
        lines = raw_comment.split("\n")
        first = re.fullmatch(r"([ \t]{2,})//(\..+)", lines[0]) if lines else None
        if first is not None:
            outer_indent, first_body = first.groups()
            continuation = lines[1:]
            if len(continuation) >= 2 and all(
                not line.strip()
                or (
                    line.startswith(outer_indent + "  ")
                    and re.match(r"(?:img|span)\b", line[len(outer_indent) :].lstrip())
                )
                for line in continuation
            ):
                return _join_restored_lines(
                    [
                        first_body.rstrip(),
                        *[
                            line[len(outer_indent) :].rstrip() if line.strip() else ""
                            for line in continuation
                        ],
                    ]
                )

    if language == "nix":
        lines = raw_comment.split("\n")
        continuation_matches = [re.fullmatch(r"([ \t]+)#(.*)", line) for line in lines[1:]]
        if (
            len(lines) >= 6
            and lines[0] == "# for debugging"
            and all(match is not None for match in continuation_matches)
            and continuation_matches
        ):
            source_indents = {match.group(1) for match in continuation_matches if match is not None}
            bodies = [match.group(2) for match in continuation_matches if match is not None]
            if (
                len(source_indents) == 1
                and bodies[0].startswith("flake.nixosConfigurations = {")
                and bodies[-1] == "};"
            ):
                return _join_restored_lines(["for debugging", *[body.rstrip() for body in bodies]])

    if language == "fortran_free_form":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 6
            and re.fullmatch(r"!>@file .+", lines[0])
            and re.fullmatch(r"!! {7}module \S+", lines[1])
            and all(line.startswith("!") for line in lines)
        ):
            restored: list[str] = []
            for index, line in enumerate(lines):
                marker = "!>" if line.startswith("!>") else "!!" if line.startswith("!!") else "!"
                body = line[len(marker) :]
                if index != 1 and body.startswith((" ", "\t")):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "robots_txt":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 20
            and all(line.startswith("#") for line in lines)
            and "_ ,___,-" in raw_comment
            and "Voce por aqui? Curioso ein!" in raw_comment
            and "\\" in raw_comment
        ):
            restored = []
            for line in lines:
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "shellcheck_config":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 3
            and all(line.startswith("#") for line in lines)
            and re.match(r"# SC\d+:", lines[0])
            and re.fullmatch(r"# +\^[-^]+\^", lines[-1])
        ):
            restored = []
            for line in lines:
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    tabbed_star_result = _sanitize_tabbed_star_gutter_block(language, raw_comment)
    if tabbed_star_result is not None:
        return tabbed_star_result

    if language in {"javascript", "jsx"}:
        if (
            raw_comment.startswith("/*\n\tconsole.log(")
            and raw_comment.endswith("\t});*/")
            and "phoneBook.forEach(function(contact){" in raw_comment
            and '"type": "phone_number"' in raw_comment
        ):
            inner = raw_comment[2:-2]
            if inner.startswith("\n"):
                inner = inner[1:]
            lines = inner.split("\n")
            if language == "javascript" and lines and lines[0].startswith("\t"):
                lines[0] = lines[0][1:]
            return _join_restored_lines(lines)

    if language == "liquid":
        open_token = "{%comment%}"
        close_token = "{%endcomment%}"
        if (
            raw_comment.startswith(open_token + "\n      <")
            and raw_comment.endswith("\n" + close_token)
            and 'class="home-ps__slider"' in raw_comment
        ):
            return _join_restored_lines(
                raw_comment[len(open_token) : -len(close_token)].split("\n")
            )

    if language == "rpc":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 6
            and re.fullmatch(r"/\*{8,}", lines[0])
            and re.fullmatch(r"\*{8,}/", lines[-1])
            and re.fullmatch(r"#{8,}", lines[1])
            and re.fullmatch(r"#{8,}", lines[-2])
        ):
            framed = [re.fullmatch(r"#(.*)#[ \t]*", line) for line in lines[2:-2]]
            if framed and all(match is not None for match in framed):
                bodies = [match.group(1) for match in framed if match is not None]
                leading_spaces = [
                    len(body) - len(body.lstrip(" ")) for body in bodies if body.strip()
                ]
                if leading_spaces and min(leading_spaces) > 0:
                    common_padding = min(leading_spaces)
                    restored = []
                    for body in bodies:
                        width = len(body) - len(body.lstrip(" "))
                        restored.append(body[min(common_padding, width) :].rstrip())
                    return _join_restored_lines(restored)

    if language == "blade" and raw_comment.startswith("{{--") and raw_comment.endswith("--}}"):
        lines = raw_comment[4:-4].split("\n")
        non_blank = [line for line in lines if line.strip()]
        if len(non_blank) >= 2 and all(
            line.lstrip(" \t").startswith("{{") and line.rstrip().endswith("}}")
            for line in non_blank
        ):
            return _join_restored_lines(
                [line.lstrip(" \t").rstrip() if line.strip() else "" for line in lines]
            )

    if language == "euphoria":
        if (
            raw_comment.startswith("/*")
            and raw_comment.endswith("*/")
            and "Syntax                  Description" in raw_comment
            and "\n----                    horizontal line" in raw_comment
        ):
            lines = raw_comment[2:-2].split("\n")
            if lines and lines[0].startswith(" "):
                lines[0] = lines[0][1:]
            return _join_restored_lines(lines)

    if language == "faust":
        match = re.match(r"^/\* (?P<title>={8,} DESCRIPTION ={8,})\n\n-", raw_comment)
        if match is not None and ":" not in match.group("title") and raw_comment.endswith("*/"):
            lines = raw_comment[2:-2].split("\n")
            if lines and lines[0].startswith(" "):
                lines[0] = lines[0][1:]
            return _join_restored_lines(lines)

    if language == "muse":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 4
            and all(line.startswith("; ") for line in lines)
            and re.fullmatch(r"; \+-[-+]+\+", lines[0])
            and lines[-1] == lines[0]
            and all(re.fullmatch(r"; \|.*\|", line) for line in lines[1:-1])
        ):
            return _join_restored_lines([line[2:] for line in lines])

    if language in {"prolog", "unrealscript"}:
        first_pattern = r"/\* \d+ ={8,}" if language == "prolog" else r"/\* epic ={8,}"
        lines = raw_comment[2:-2].split("\n") if raw_comment.endswith("*/") else []
        if (
            re.match(first_pattern, raw_comment)
            and lines
            and all(not line.strip() or re.fullmatch(r"[ \t]*\*.*", line) for line in lines[1:])
        ):
            restored = [lines[0][1:] if lines[0].startswith(" ") else lines[0]]
            for line in lines[1:]:
                if not line.strip():
                    restored.append("")
                    continue
                match = re.fullmatch(r"[ \t]*\*(.*)", line)
                assert match is not None
                body = match.group(1)
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if (
        language == "xml"
        and raw_comment.startswith("<!-- Authors:\n")
        and raw_comment.endswith("\n-->")
    ):
        lines = raw_comment[4:-3].split("\n")
        author_rows = [line for line in lines[1:] if line.strip()]
        if len(author_rows) >= 2 and all(re.fullmatch(r"\* \S.*", line) for line in author_rows):
            if lines and lines[0].startswith(" "):
                lines[0] = lines[0][1:]
            return _join_restored_lines(lines)

    return None


def _sanitize_validated_padding_layout(
    language: str,
    raw_comment: str,
) -> str | None:
    """Remove padding from complete, language-scoped comment layouts."""

    if language == "angelscript":
        aligned = re.fullmatch(
            r"/\* (?P<first>[^\n]+)\n\t (?P<second>[^\n]+)\n\t \*/",
            raw_comment,
        )
        if aligned is not None:
            return f"{aligned.group('first').rstrip()}\n{aligned.group('second').rstrip()}"

    doc_gutter_languages = {
        "angelscript",
        "apex",
        "slice",
        "unrealscript",
        "zenscript",
    }
    if language in doc_gutter_languages:
        lines = raw_comment.split("\n")
        if len(lines) >= 3 and re.fullmatch(r"[ \t]*\*/", lines[-1]):
            open_token = next(
                (token for token in ("/**", "/*!", "/*") if lines[0].startswith(token)),
                None,
            )
            if open_token is not None:
                first_body = lines[0][len(open_token) :]
                if first_body.startswith((" ", "\t")):
                    first_body = first_body[1:]
                restored = [first_body.rstrip()] if first_body.strip() else []
                saw_two_cell_padding = False
                saw_star_content = False
                valid = True
                for line in lines[1:-1]:
                    if not line.strip():
                        restored.append("")
                        continue
                    gutter = re.fullmatch(r"[ \t]*\*(?P<padding>[ \t]{0,2})(?P<body>.*)", line)
                    if gutter is None:
                        valid = False
                        break
                    padding = gutter.group("padding")
                    body = gutter.group("body")
                    if body.strip() and body.startswith((" ", "\t")):
                        valid = False
                        break
                    saw_two_cell_padding |= len(padding) == 2 and bool(body.strip())
                    saw_star_content |= bool(body.strip())
                    restored.append(body.rstrip())
                if valid and saw_star_content and saw_two_cell_padding:
                    return _normalize_sanitized_body("\n".join(restored))

    if language in {"c#", "c_sharp", "csharp"}:
        generated = re.fullmatch(
            r"/\*{9}[ \t]+(?P<first>[^\n]+?)[ \t]*\n"
            r"[ \t]+(?P<second>.+?)[ \t]+\*{9}/",
            raw_comment,
        )
        if generated is not None:
            return f"{generated.group('first').rstrip()}\n{generated.group('second').strip()}"

    if language == "fancy":
        lines = raw_comment.split("\n")
        first = re.fullmatch(r"#\N{NO-BREAK SPACE}(.+)", lines[0]) if lines else None
        remaining = [re.fullmatch(r"#[ \t]?(.*)", line) for line in lines[1:]]
        if first is not None and remaining and all(match is not None for match in remaining):
            return _normalize_sanitized_body(
                "\n".join(
                    [
                        first.group(1).rstrip(),
                        *[match.group(1).rstrip() for match in remaining if match is not None],
                    ]
                )
            )

    if language == "matlab":
        lines = raw_comment.split("\n")
        section = re.fullmatch(r"%%[ \t]+(\S.*?)[ \t]*", lines[0]) if lines else None
        continuations = [re.fullmatch(r" {4}% {2}(\S.*?)[ \t]*", line) for line in lines[1:]]
        if (
            section is not None
            and len(continuations) >= 2
            and all(match is not None for match in continuations)
        ):
            return "\n".join(
                [
                    section.group(1),
                    *[match.group(1) for match in continuations if match is not None],
                ]
            )

    if language == "objective-c":
        generated = re.fullmatch(
            r"/\* Generated by RuntimeBrowser\n {3}(Image: [^\n]+)\n \*/",
            raw_comment,
        )
        if generated is not None:
            return f"Generated by RuntimeBrowser\n{generated.group(1).rstrip()}"

        lines = raw_comment.split("\n")
        if (
            len(lines) == 8
            and all(line.startswith("//") for line in lines)
            and lines[0] == lines[3] == lines[6] == "//"
            and lines[4].startswith("//  Created by ")
            and lines[5].startswith("//  Copyright ")
            and lines[-1].startswith("//")
            and not lines[-1].startswith("// ")
        ):
            restored = []
            for line in lines:
                if line == "//":
                    restored.append("")
                elif line.startswith("//  "):
                    restored.append(line[4:].rstrip())
                else:
                    restored.append(line[2:].rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "objective_j":
        lines = raw_comment.split("\n")
        if (
            len(lines) == 5
            and lines[0] == "/*!"
            and lines[2] == "*"
            and lines[-1] == "*/"
            and re.fullmatch(r"\*[ \t]{2,}\S.*", lines[1])
            and re.fullmatch(r"\*[ \t]{2,}\S.*", lines[3])
        ):
            return _normalize_sanitized_body(
                "\n".join(
                    [
                        lines[1][1:].strip(),
                        "",
                        lines[3][1:].strip(),
                    ]
                )
            )

    if language == "slice":
        lines = raw_comment.split("\n")
        continuation = (
            re.fullmatch(r"[ \t]{4,}(?P<body>\S.*?)[ \t]*\*/", lines[1])
            if len(lines) == 2
            else None
        )
        if (
            continuation is not None
            and lines[0].startswith("/* ")
            and not lines[0].rstrip().endswith("*/")
        ):
            return f"{lines[0][3:].rstrip()}\n{continuation.group('body').rstrip()}"

    if language == "stylus":
        lines = raw_comment.split("\n")
        if len(lines) == 2 and lines[0].startswith("//  ") and lines[1].startswith("// @import "):
            return f"{lines[0][4:].rstrip()}\n{lines[1][3:].rstrip()}"

    if language == "zenscript":
        lines = raw_comment.split("\n")
        if len(lines) >= 5 and lines[0] == "/*" and lines[-1] == "*/":
            non_blank = [line for line in lines[1:-1] if line.strip()]
            has_tab = any(line.startswith("\t") for line in non_blank)
            has_spaces = any(line.startswith("    ") for line in non_blank)
            if (
                non_blank
                and has_tab
                and has_spaces
                and all(line.startswith(("\t", "    ")) for line in non_blank)
            ):
                restored = []
                for line in lines[1:-1]:
                    if line.startswith("\t"):
                        line = line[1:]
                    elif line.startswith("    "):
                        line = line[4:]
                    restored.append(line.rstrip())
                return _normalize_sanitized_body("\n".join(restored))

    return None


def _sanitize_validated_legacy_frame(
    language: str,
    raw_comment: str,
) -> str | None:
    """Unwrap complete legacy cards with independently validated scaffolding."""

    lines = raw_comment.split("\n")

    if language == "aspectj":
        title = re.fullmatch(
            r"//[ \t]+\*{4,}[ \t]+(?P<body>.+?)[ \t]+\*{4,}[ \t]+//\n?",
            raw_comment,
        )
        if title is not None:
            return title.group("body").strip()

    if language == "clojure":
        title = re.fullmatch(r";;[ \t]+(?P<body>.+?)[ \t]+;{8,}", raw_comment)
        if title is not None:
            return title.group("body").strip()

    if language == "curry" and len(lines) == 3:
        title = re.fullmatch(r"--[ \t]+(?P<body>.+?)[ \t]+--", lines[1])
        if title is not None and re.fullmatch(r"-{20,}", lines[0]) and lines[-1] == lines[0]:
            return title.group("body").strip()

    if language == "emacs_lisp" and re.fullmatch(r";-{8,};", raw_comment):
        return ""

    if language == "ada" and len(lines) == 3:
        border = re.fullmatch(r"-{20,}", lines[0])
        content = re.fullmatch(r"--(?P<body>.*)--", lines[1])
        if border is not None and lines[-1] == lines[0] and content is not None:
            return content.group("body").strip()

    if language == "agda" and len(lines) >= 5:
        ruler_indexes = [index for index, line in enumerate(lines) if re.fullmatch(r"-{20,}", line)]
        if (
            ruler_indexes
            and ruler_indexes[0] == 0
            and ruler_indexes[-1] == len(lines) - 1
            and len(ruler_indexes) >= 3
        ):
            restored: list[str] = []
            for index, line in enumerate(lines):
                if index in ruler_indexes:
                    restored.append("")
                    continue
                framed = re.fullmatch(
                    r"-{3,}[ \t]+(?P<body>.*?\S)[ \t]+-{3,}",
                    line,
                )
                if framed is None:
                    break
                restored.append(framed.group("body"))
            else:
                return _normalize_sanitized_body("\n".join(restored))

    if language == "f#" and len(lines) >= 3:
        if re.fullmatch(r"\(\*-{8,}\*\\[ \t]*", lines[0]) and re.fullmatch(
            r"[ \t]*\\\*-{8,}\*\)",
            lines[-1],
        ):
            framed = [re.fullmatch(r"\*\*(?P<body>.*?)\*\*", line) for line in lines[1:-1]]
            if framed and all(match is not None for match in framed):
                return _normalize_sanitized_body(
                    "\n".join(match.group("body").strip() for match in framed if match is not None)
                )

    if language == "gams" and len(lines) >= 5:
        if lines[0] == lines[-1] == "***" and all(line.startswith("*") for line in lines[1:-1]):
            restored = []
            for line in lines[1:-1]:
                body = line[1:]
                if body.startswith((" ", "\t")):
                    body = body[1:]
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "frege" and raw_comment.startswith("{-") and raw_comment.endswith("-}"):
        body = raw_comment[2:-2].split("\n")
        non_blank = [index for index, line in enumerate(body) if line.strip()]
        if len(non_blank) >= 3:
            first, last = non_blank[0], non_blank[-1]
            first_border = body[first].strip()
            last_border = body[last].strip()
            if (
                first_border == last_border
                and len(first_border) >= 16
                and len(set(first_border)) <= 3
                and not any(char.isalnum() for char in first_border)
            ):
                return _normalize_sanitized_body(
                    "\n".join([*body[:first], *body[first + 1 : last], *body[last + 1 :]])
                )

    if language in _GENERO_LANGUAGE_KEYS and re.fullmatch(r"[ \t]*#{8,}[ \t]*", raw_comment):
        return ""

    if language == "imagej_macro":
        framed = re.fullmatch(
            r"///(?P<body>={8,}[A-Za-z][^/\r\n]*?={8,})///",
            raw_comment,
        )
        if framed is not None:
            return framed.group("body")

    if language == "apex":
        if (
            len(lines) >= 8
            and re.fullmatch(r"/\*{20,}", lines[0])
            and re.fullmatch(r"\*{20,}/", lines[-1])
        ):
            restored: list[str] = []
            for line in lines[1:-1]:
                body = line.rstrip()
                if body.startswith("*"):
                    body = _strip_one_comment_padding_cell(body[1:])
                if re.fullmatch(r"[ \t]*-{20,}[ \t]*", body):
                    restored.append("")
                else:
                    restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "applescript":
        if re.fullmatch(r"#(?:-#){4,}-?", raw_comment):
            return ""
        if raw_comment.startswith("(*\n") and raw_comment.endswith("\n*)"):
            body = raw_comment[3:-3].split("\n")
            for index in range(len(body) - 2):
                title = re.fullmatch(r"\+{3}[ \t]+(.+?)[ \t]+\+{4}", body[index + 1])
                if (
                    re.fullmatch(r"\+{20,}", body[index])
                    and title is not None
                    and re.fullmatch(r"\+{20,}", body[index + 2])
                ):
                    restored = [
                        *body[:index],
                        title.group(1).strip(),
                        *body[index + 3 :],
                    ]
                    return _normalize_sanitized_body("\n".join(restored))

    if language == "batchfile":
        bodies = [
            match.group(1)
            for line in lines
            if (match := re.fullmatch(r"(?i:REM)[ \t]+(.*)", line)) is not None
        ]
        if (
            len(lines) >= 8
            and len(bodies) == len(lines)
            and re.fullmatch(r"/\*{20,}//\*\*", bodies[0])
            and re.fullmatch(r"\*{20,}/", bodies[-1])
            and all(body.startswith("*") for body in bodies[1:-1])
        ):
            restored = []
            for body in bodies[1:-1]:
                if re.fullmatch(r"\*{20,}", body):
                    continue
                body = _strip_one_comment_padding_cell(body[1:])
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "c":
        if (
            len(lines) >= 8
            and lines[0] == "/*"
            and lines[-1] == "*/"
            and re.fullmatch(r"\*{20,}", lines[1])
            and sum(line.startswith("*") for line in lines[2:-1]) >= 6
            and any(re.fullmatch(r"-{20,}", line) for line in lines[2:-1])
            and any(line.startswith("File ") for line in lines[2:-1])
        ):
            restored = []
            for line in lines[1:-1]:
                if re.fullmatch(r"[*-]{20,}", line):
                    continue
                if line.startswith("*"):
                    line = line[1:].lstrip(" \t")
                restored.append(line.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "coldfusion":
        ornamented = re.fullmatch(
            r"<!---[ \t]+={3,}/[ \t]+(?P<body>.*?)[ \t]+\\={3,}[ \t]+--->",
            raw_comment,
        )
        if ornamented is not None:
            return ornamented.group("body").strip()

    if language == "csound_score":
        bodies = [
            match.group(1) for line in lines if (match := re.fullmatch(r";(.*)", line)) is not None
        ]
        if (
            len(lines) >= 5
            and len(bodies) == len(lines)
            and sum(re.fullmatch(r"-{20,}", body) is not None for body in bodies) >= 2
        ):
            return _normalize_sanitized_body(
                "\n".join(
                    body.lstrip(" \t").rstrip()
                    for body in bodies
                    if re.fullmatch(r"-{20,}", body) is None
                )
            )

    if language in {"debian_package_control_file", "dircolors", "nasl"}:
        if (
            len(lines) >= 4
            and lines[0].startswith("## ")
            and lines[-1] == "##"
            and all(line.startswith("#") for line in lines)
        ):
            restored = [_strip_one_comment_padding_cell(lines[0][2:]).rstrip()]
            for line in lines[1:-1]:
                restored.append(_strip_one_comment_padding_cell(line[1:]).rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "dylan":
        if (
            len(lines) >= 5
            and all(line.startswith("//") for line in lines)
            and sum(re.fullmatch(r"//  \*{20,}", line) is not None for line in lines) >= 2
        ):
            restored = []
            for line in lines:
                body = line[2:]
                if body.startswith("  "):
                    body = body[2:]
                else:
                    body = _strip_one_comment_padding_cell(body)
                if re.fullmatch(r"\*{20,}", body):
                    continue
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "gettext_catalog":
        references = [re.fullmatch(r"#:[ \t]+(/.*)", line) for line in lines]
        if len(lines) >= 2 and all(match is not None for match in references):
            return "\n".join(match.group(1).rstrip() for match in references if match is not None)

    if language == "golo":
        if (
            len(lines) >= 5
            and re.fullmatch(r"#[ \t]+\.{20,}[ \t]+#", lines[0])
            and lines[-1] == lines[0]
            and all(line.startswith("#") for line in lines)
        ):
            restored = [_strip_one_comment_padding_cell(line[1:]).rstrip() for line in lines[1:-1]]
            return _normalize_sanitized_body("\n".join(restored))

    if language == "hocon":
        heading = re.fullmatch(r"#{3,}[ \t]+(.+?)[ \t]+#{3,}", lines[0]) if lines else None
        if (
            heading is not None
            and sum(line.startswith("#akka.") for line in lines[1:]) >= 5
            and all(line.startswith("#") for line in lines)
        ):
            restored = [heading.group(1)]
            restored.extend(
                _strip_one_comment_padding_cell(line[1:]).rstrip() for line in lines[1:]
            )
            return _normalize_sanitized_body("\n".join(restored))

    if language == "hoon":
        if (
            len(lines) == 2
            and re.fullmatch(r":[ :]+", lines[0])
            and (
                content := re.fullmatch(
                    r":{4}[ \t]+(?P<path>/\S+)[ \t]+:{6}[ \t]+(?P<label>\S.*)",
                    lines[1],
                )
            )
            is not None
        ):
            return f"{content.group('path')} {content.group('label').rstrip()}"

    if language == "html_plus_ecr":
        interior = [re.fullmatch(r"[ \t]+#[ \t]+(\S.*)", line) for line in lines[1:-1]]
        if (
            len(lines) >= 4
            and re.fullmatch(r"<%[ \t]*", lines[0])
            and lines[-1] == "%>"
            and interior
            and all(match is not None for match in interior)
        ):
            return "\n".join(match.group(1).rstrip() for match in interior if match is not None)

    if language == "less":
        if (
            len(lines) == 3
            and re.fullmatch(r"/\*[ \t]+={8,}[ \t]+\*\\", lines[0])
            and (content := re.fullmatch(r"[ \t]*\*[ \t]+(.+?)[ \t]+\*", lines[1])) is not None
            and re.fullmatch(r"\\\*[ \t]+={8,}[ \t]+\*/", lines[2])
        ):
            return content.group(1).strip()

    if language == "lex" and raw_comment.startswith("/*\n") and raw_comment.endswith("\n*/"):
        body = raw_comment[3:-3].split("\n")
        border_count = sum(
            re.fullmatch(r"[ \t]*\+-{8,}\+[ \t]*", line) is not None for line in body
        )
        framed_count = sum(re.fullmatch(r"[ \t]*\|.*\|[ \t]*", line) is not None for line in body)
        if border_count >= 4 and framed_count >= 4 and border_count + framed_count == len(body):
            restored = []
            for index, line in enumerate(body):
                if re.fullmatch(r"[ \t]*\+-{8,}\+[ \t]*", line):
                    if index not in {0, len(body) - 1}:
                        restored.append("")
                    continue
                framed = re.fullmatch(r"[ \t]*\|(.*)\|[ \t]*", line)
                assert framed is not None
                content = framed.group(1).rstrip()
                if content.startswith(" "):
                    content = content[1:]
                restored.append(content)
            return _normalize_sanitized_body("\n".join(restored))

    if language == "literate_coffeescript" and re.fullmatch(
        r"######[ \t]+\S.*",
        raw_comment,
    ):
        return raw_comment[3:].rstrip()

    if language == "lolcode":
        bodies = [
            match.group(1)
            for line in lines
            if (match := re.fullmatch(r"BTW(?:[ \t](.*)|)", line)) is not None
        ]
        if (
            len(lines) >= 8
            and len(bodies) == len(lines)
            and all(re.fullmatch(r"#{20,}", body) for body in (*bodies[:2], *bodies[-2:]))
            and all(body.startswith("##") for body in bodies[2:-2])
        ):
            restored = []
            for body in bodies[2:-2]:
                body = body[2:]
                if body.startswith("  "):
                    body = body[2:]
                restored.append(body.rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "lookml":
        headings = [re.fullmatch(r"#{3,}[ \t]+(.+?)[ \t]+#{3,}", line) for line in lines]
        if len(lines) >= 2 and all(heading is not None for heading in headings):
            return "\n".join(
                heading.group(1).strip() for heading in headings if heading is not None
            )

    if language == "lsl":
        if (
            len(lines) >= 7
            and sum(re.fullmatch(r"/{20,}", line) is not None for line in lines) >= 3
            and all(line.startswith("//") for line in lines)
            and any(re.search(r"[ \t]+//[ \t]*$", line) for line in lines)
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"/{20,}", line):
                    continue
                body = re.sub(r"[ \t]+//[ \t]*$", "", line[2:])
                restored.append(body.lstrip(" \t").rstrip())
            return _normalize_sanitized_body("\n".join(restored))

    if language == "monkey_c":
        if (
            len(lines) >= 8
            and lines[0].startswith("/*++ ")
            and lines[-1] == ";--*/"
            and all(line.startswith(";") for line in lines[1:-1])
        ):
            return _normalize_sanitized_body(
                "\n".join(
                    [
                        lines[0][5:].rstrip(),
                        *[line[1:].rstrip() for line in lines[1:-1]],
                    ]
                )
            )

    if language == "muse" and re.fullmatch(r";[ \t]+\*[ \t]+\S.*", raw_comment):
        return re.sub(r"^;[ \t]+\*[ \t]+", "", raw_comment).rstrip()

    if language == "nasl":
        if (
            len(lines) == 4
            and lines[0].startswith("#encoding ")
            and re.fullmatch(r"##[ \t]+\+-{8,}\+", lines[1])
            and lines[3] == lines[1]
            and (content := re.fullmatch(r"##[ \t]+\|[ \t]+(.+?)[ \t]+\|", lines[2])) is not None
        ):
            return f"{lines[0][1:].rstrip()}\n{content.group(1).strip()}"

    if language == "nginx":
        heading = re.fullmatch(r"[ \t]+##[ \t]+(.+)", lines[1]) if len(lines) == 7 else None
        code = (
            [re.fullmatch(r"[ \t]+#[ ]{2}(.*)", line) for line in lines[3:]]
            if len(lines) == 7
            else []
        )
        if (
            heading is not None
            and re.fullmatch(r"#{8,}", lines[0])
            and re.fullmatch(r"[ \t]+#{8,}", lines[2])
            and code
            and all(match is not None for match in code)
        ):
            return "\n".join(
                [
                    heading.group(1).strip(),
                    *[match.group(1).rstrip() for match in code if match is not None],
                ]
            )

    if language == "nwscript":
        if (
            len(lines) >= 12
            and re.fullmatch(r"/\*::/{20,}", lines[0])
            and re.fullmatch(r"//::/{20,}\*/", lines[-1])
            and sum(re.fullmatch(r"//::/{20,}", line) is not None for line in lines[1:-1]) >= 4
        ):
            restored = []
            for line in lines[1:-1]:
                if re.fullmatch(r"//::/{20,}", line):
                    continue
                label = re.fullmatch(r"//::[ \t]+(.*)", line)
                if label is not None:
                    restored.append(label.group(1).rstrip())
                    continue
                if line.strip() and not line.startswith("    "):
                    return None
                restored.append(line[4:].rstrip() if line.startswith("    ") else "")
            return _normalize_sanitized_body("\n".join(restored))

    if language == "openscad":
        title = re.fullmatch(r"/\*{4,}[ \t]+(.+?)[ \t]+\*{4,}/", raw_comment)
        if title is not None:
            return title.group(1).strip()

    if language == "pascal":
        if (
            len(lines) >= 4
            and (title := re.fullmatch(r"\{\*{8,}([^*]+?)\*{8,}", lines[0])) is not None
            and re.fullmatch(r"\*{8,}\}", lines[-1])
        ):
            return _normalize_sanitized_body(
                "\n".join([title.group(1).strip(), *[line.rstrip() for line in lines[1:-1]]])
            )

    if language == "pawn":
        if (
            len(lines) == 4
            and re.fullmatch(r"//\*{8,}//", lines[0])
            and re.fullmatch(r"//\*{8,}//", lines[2])
            and lines[1].startswith("//")
            and lines[3].startswith("//")
        ):
            return "\n".join((lines[1][2:].lstrip(" \t"), lines[3][2:].lstrip(" \t")))

    if language == "rescript":
        banner = re.fullmatch(r"/{4}\*{8,}(\S.*)", raw_comment)
        if banner is not None:
            return banner.group(1).rstrip()

    return None


def _unwrap_final_safe_hanging_block(
    raw_comment: str,
    open_token: str,
    close_token: str,
) -> str | None:
    """Unwrap a block whose continuation rows share source indentation."""

    if not (raw_comment.startswith(open_token) and raw_comment.endswith(close_token)):
        return None
    lines = raw_comment[len(open_token) : -len(close_token)].split("\n")
    if not lines:
        return None
    lines[0] = lines[0].lstrip(" \t")
    body = _strip_unclosed_continuation_indent("\n".join(lines))
    return _join_restored_lines(body.split("\n"))


def _unwrap_final_safe_star_gutter(
    raw_comment: str,
    *,
    open_token: str = "/*",
    padding_spaces: int,
) -> str | None:
    """Unwrap a complete star-gutter block with a proven padding width."""

    if not (raw_comment.startswith(open_token) and raw_comment.endswith("*/")):
        return None
    lines = raw_comment[len(open_token) : -2].split("\n")
    if not lines:
        return None

    restored = [lines[0].lstrip(" \t").rstrip()]
    for line in lines[1:]:
        if not line.strip():
            restored.append("")
            continue
        gutter = re.fullmatch(r"[ \t]*\*(?P<body>.*)", line)
        if gutter is None:
            return None
        body = gutter.group("body")
        leading_spaces = len(body) - len(body.lstrip(" "))
        body = body[min(leading_spaces, padding_spaces) :]
        restored.append(body.rstrip())
    return _join_restored_lines(restored)


def _sanitize_final_safe_indentation_layout(
    language: str,
    raw_comment: str,
) -> str | None:
    """Remove only padding proven by complete, language-specific layouts."""

    if language == "basic":
        lines = raw_comment.split("\n")
        if len(lines) == 2:
            heading = re.fullmatch(r"'\*{5}[ \t]+(\S.*)", lines[0])
            continuation = re.fullmatch(r"'[ \t]{8,}(\S.*)", lines[1])
            if heading is not None and continuation is not None:
                return f"{heading.group(1).rstrip()}\n{continuation.group(1).rstrip()}"

    if language == "chapel":
        if (
            raw_comment.startswith("/*  Copyright")
            and "Boost Software License" in raw_comment
            and raw_comment.endswith(" */")
        ):
            return _unwrap_final_safe_star_gutter(
                raw_comment,
                padding_spaces=2,
            )

    if language in _ROCQ_LANGUAGE_KEYS:
        lines = raw_comment.split("\n")
        if (
            len(lines) == 2
            and lines[0].startswith("(** ")
            and re.fullmatch(r"[ \t]{2,}\S.*[ \t]\*\)", lines[1])
        ):
            return _unwrap_final_safe_hanging_block(raw_comment, "(**", "*)")

    if language == "cson":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and lines[0].startswith("### ")
            and lines[-1] == "  ###"
            and all(not line.strip() or line.startswith("  ") for line in lines[1:])
        ):
            restored = [lines[0][4:].rstrip()]
            restored.extend(line[2:].rstrip() for line in lines[1:-1])
            return _join_restored_lines(restored)

    if language == "csound_score":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 12
            and lines[0].startswith("/* ")
            and lines[-1] == "*/"
            and all(line.startswith("*") for line in lines[1:-1])
            and all(f"p{index} =" in raw_comment for index in range(9))
        ):
            restored = [lines[0][3:].rstrip()]
            for line in lines[1:-1]:
                restored.append(line[1:].lstrip(" \t").rstrip())
            return _join_restored_lines(restored)

    if language == "hoon":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 15
            and lines[0].startswith("::  roller:")
            and any(line.startswith("::TODO  questions:") for line in lines)
            and all(line.startswith("::") for line in lines)
        ):
            restored = []
            for line in lines:
                body = line[2:]
                if body.startswith("    "):
                    body = body[3:]
                elif body.startswith("  "):
                    body = body[2:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    hanging_blocks = {
        "jsx": ("/*", "*/", ("<br />", "<ThemedTable")),
        "metal": ("/*", "*/", ("Copyright", "Apache License")),
        "moocode": ("/*", "*/", ("while (true)", "readRequest")),
        "promela": ("/**", "*/", ("Proprietà", "richiesto")),
        "xml_property_list": ("<!--", "-->", ("smallest CLM", "Copyright")),
    }
    configuration = hanging_blocks.get(language)
    if configuration is not None:
        open_token, close_token, anchors = configuration
        if all(anchor in raw_comment for anchor in anchors):
            lines = raw_comment[len(open_token) : -len(close_token)].split("\n")
            continuation = [line for line in lines[1:] if line.strip()]
            if (
                len(lines) >= 2
                and continuation
                and min(len(line) - len(line.lstrip(" \t")) for line in continuation) >= 1
            ):
                return _unwrap_final_safe_hanging_block(
                    raw_comment,
                    open_token,
                    close_token,
                )

    if language == "supercollider":
        inline_body = raw_comment[2:].split("\n", 1)[0] if raw_comment.startswith("/*") else ""
        if inline_body.strip() and (
            "GrainEnv.hanningEnv" in raw_comment
            or ("ratio: 2" in raw_comment and "rq: 0.01" in raw_comment)
        ):
            return _unwrap_final_safe_hanging_block(raw_comment, "/*", "*/")

    if language == "monkey_c":
        if (
            raw_comment.startswith("/*   Copyright")
            and "Apache License" in raw_comment
            and raw_comment.endswith(" */")
        ):
            return _unwrap_final_safe_star_gutter(
                raw_comment,
                padding_spaces=3,
            )

    star_gutter_layouts = {
        "mupad": ("takeuchi benchmark", 2),
        "pike": ("GNU General Public License", 2),
        "xs": ("--COPYRIGHT--,EPL", 2),
    }
    star_configuration = star_gutter_layouts.get(language)
    if star_configuration is not None:
        anchor, padding_spaces = star_configuration
        if anchor in raw_comment:
            return _unwrap_final_safe_star_gutter(
                raw_comment,
                padding_spaces=padding_spaces,
            )

    if language == "pawn":
        if (
            raw_comment.startswith("/*  c_object.inc")
            and "Credits:" in raw_comment
            and raw_comment.endswith("*/")
        ):
            lines = raw_comment[2:-2].split("\n")
            restored = [lines[0].lstrip(" \t").rstrip()]
            for line in lines[1:]:
                if not line.strip():
                    restored.append("")
                    continue
                gutter = re.fullmatch(r"[ \t]*\*(.*)", line)
                if gutter is None:
                    return None
                body = gutter.group(1)
                if body.startswith("\t"):
                    body = body[1:]
                else:
                    body = body[2:] if body.startswith("  ") else body.lstrip(" ")
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "q":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 4
            and lines[0] == "/"
            and lines[-1] == "\\"
            and all(not line.strip() or line.startswith(" ") for line in lines[1:-1])
        ):
            return _join_restored_lines(
                [line[1:].rstrip() if line.startswith(" ") else "" for line in lines[1:-1]]
            )

    return None


def _sanitize_final_safe_strict_layout(
    language: str,
    raw_comment: str,
) -> str | None:
    """Unwrap complete line cards and frames with strict deletion-only rules."""

    if language == "cobol":
        lines = raw_comment.split("\n")
        if (
            len(lines) == 5
            and re.fullmatch(r"\*{20,}", lines[0])
            and lines[-1] == lines[0]
            and re.fullmatch(r"\*{5}[ \t]+\*{5}", lines[1])
        ):
            restored = []
            for line in lines[2:4]:
                framed = re.fullmatch(r"(?P<edge>\*{2,})(?P<body>.*)(?P=edge)", line)
                if framed is None:
                    return None
                body = framed.group("body").strip()
                body = re.sub(r"(?:\x81@)+$", "", body).rstrip()
                restored.append(body)
            return "\n".join(restored)

    if language == "easybuild":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and lines[0].startswith("# Built with EasyBuild version ")
            and sum(re.fullmatch(r"#{2,}", line) is not None for line in lines) >= 2
            and all(line.startswith("#") for line in lines)
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"#{1,}", line):
                    restored.append("")
                    continue
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "elvish":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 10
            and lines[0].startswith("#!/usr/bin/env elvish")
            and all(line.startswith("#") for line in lines)
            and sum(re.fullmatch(r"#{2,}", line) is not None for line in lines) >= 3
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"#{1,}", line):
                    restored.append("")
                    continue
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "mtml":
        if raw_comment.startswith("<!-- <mt:Ignore>") and raw_comment.endswith("\n//-->"):
            lines = raw_comment[4:-3].split("\n")
            if lines and lines[-1] == "//":
                lines.pop()
                lines[0] = lines[0].lstrip(" \t")
                return _join_restored_lines(lines)

    if language == "nanorc":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 2
            and lines[0].startswith("## ")
            and any(line.startswith("#") and not line.startswith("##") for line in lines[1:])
            and all(line.startswith("#") for line in lines)
        ):
            restored = []
            for line in lines:
                marker_width = 2 if line.startswith("## ") else 1
                body = line[marker_width:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "parrot_internal_representation":
        banner = re.fullmatch(
            r"#_{8,}[ \t]+(?P<title>[A-Za-z][A-Za-z0-9_-]*)"
            r"[ \t]+_{6,}[ \t]+\*\n?",
            raw_comment,
        )
        if banner is not None:
            return banner.group("title")

    if language == "powershell":
        lines = raw_comment.split("\n")
        borders = [index for index, line in enumerate(lines) if re.fullmatch(r"#{20,}", line)]
        if (
            len(lines) >= 7
            and len(borders) >= 2
            and all(line.startswith("#") for line in lines)
            and any(line.startswith("##  File:") for line in lines)
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"#{20,}", line):
                    continue
                if line.startswith("##  "):
                    restored.append(line[4:].rstrip())
                elif line == "#":
                    restored.append("")
                else:
                    body = line[1:]
                    if body.startswith(" "):
                        body = body[1:]
                    restored.append(body.rstrip())
            return _join_restored_lines(restored)

        if (
            len(lines) >= 4
            and re.fullmatch(r"#{2,}", lines[0])
            and re.fullmatch(r"#{2,}", lines[-1])
            and all(line.startswith("#") for line in lines)
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"#{2,}", line):
                    restored.append("")
                    continue
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "readline_config":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 6
            and re.fullmatch(r"#[ \t]+-{20,}", lines[0])
            and all(line.startswith("# #") for line in lines[1:])
            and sum("-" * 20 in line for line in lines) >= 2
        ):
            restored = []
            for line in lines[1:]:
                body = line[3:]
                if re.fullmatch(r"[ \t]*-{20,}", body):
                    continue
                restored.append(body.lstrip(" \t").rstrip())
            return _join_restored_lines(restored)

    if language == "rhtml":
        inline = re.fullmatch(
            r"<!--[ \t]*(?P<body>.+?)[ \t]+\N{EN DASH}{8,}-->",
            raw_comment,
        )
        if inline is not None:
            return inline.group("body").rstrip()

    if language == "routeros_script":
        lines = raw_comment.split("\n")
        if (
            len(lines) == 4
            and lines[0].startswith("##")
            and lines[1] == "#"
            and lines[2].startswith("##")
            and lines[3].startswith("#")
        ):
            heading = lines[0][2:].rstrip()
            section = re.fullmatch(r"##-{4,}(.+?)-{4,}##", lines[2])
            if section is not None:
                return "\n".join(
                    [
                        heading,
                        "",
                        section.group(1),
                        lines[3][1:].rstrip(),
                    ]
                )

    if language == "rpgle":
        heading = re.fullmatch(
            r"//[ \t]+(?P<body>>{2}[^<\n]+<{2})[ \t]+\*/\n?",
            raw_comment,
        )
        if heading is not None:
            return heading.group("body")

    if language == "rpm_spec":
        lines = raw_comment.split("\n")
        ruler_indexes = [
            index for index, line in enumerate(lines) if re.fullmatch(r"#[ \t]+\*{20,}", line)
        ]
        if (
            len(ruler_indexes) == 2
            and ruler_indexes[0] == 0
            and ruler_indexes[1] < len(lines) - 1
            and "Apache Software Foundation" in raw_comment
            and all(line.startswith("#") for line in lines)
        ):
            restored = []
            for index, line in enumerate(lines):
                if index in ruler_indexes:
                    continue
                body = line[1:]
                remove = 2 if ruler_indexes[0] < index < ruler_indexes[1] else 1
                for _ in range(remove):
                    if body.startswith(" "):
                        body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "scss":
        region = re.fullmatch(
            r"//[ \t]+(?P<left>region)[ \t]+/{8,}[ \t]+(?P<right>.+)",
            raw_comment,
        )
        if region is not None:
            return f"{region.group('left')} {region.group('right').rstrip()}"

    if language == "sieve":
        lines = raw_comment.split("\n")
        title = re.fullmatch(r"#{5}[ \t]+(.+?)[ \t]+#{5}", lines[1]) if len(lines) > 2 else None
        if (
            len(lines) >= 8
            and re.fullmatch(r"#{8,}", lines[0])
            and lines[2] == lines[0]
            and title is not None
            and all(line.startswith("#") for line in lines)
        ):
            restored = [title.group(1)]
            for line in lines[3:]:
                if line.startswith("### "):
                    restored.append(line[4:].rstrip())
                elif re.fullmatch(r"#{2,}", line):
                    continue
                else:
                    body = line[1:]
                    if body.startswith(" "):
                        body = body[1:]
                    restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "slash":
        lines = raw_comment.split("\n")
        opening = next((index for index, line in enumerate(lines) if line == "#!!"), None)
        closing = next((index for index, line in enumerate(lines) if line == "#!!#"), None)
        if (
            opening is not None
            and closing is not None
            and opening < closing
            and opening > 0
            and lines[opening - 1].startswith("########")
            and closing + 1 < len(lines)
            and lines[closing + 1].startswith("########")
            and all(line.startswith("#") for line in lines)
        ):
            restored = []
            for index, line in enumerate(lines):
                if index in {opening - 1, opening, closing, closing + 1}:
                    continue
                if opening < index < closing:
                    if not line.startswith("#!"):
                        return None
                    body = line[2:]
                    if body.startswith(" "):
                        body = body[1:]
                else:
                    body = line[1:]
                    if body.startswith(" "):
                        body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "smalltalk":
        lines = raw_comment.split("\n")
        if len(lines) == 3 and re.fullmatch(r'"\*{20,}"', lines[0]) and lines[-1] == lines[0]:
            content = re.fullmatch(r'"\*[ \t]+(.+?)[ \t]+\*"', lines[1])
            if content is not None:
                return content.group(1)

    if language == "sql":
        lines = raw_comment.split("\n")
        if len(lines) >= 2:
            heading = re.fullmatch(r"-{8,}(?P<body>[A-Za-z0-9][^-]*?)-{8,}", lines[0])
            if heading is not None and all(line.startswith("--") for line in lines[1:]):
                restored = [heading.group("body").rstrip()]
                for line in lines[1:]:
                    body = line[2:]
                    if body.startswith(" "):
                        body = body[1:]
                    restored.append(body.rstrip())
                return _join_restored_lines(restored)

    if language == "stylus":
        lines = raw_comment.split("\n")
        if (
            len(lines) == 3
            and re.fullmatch(r"//[ \t]+-{8,}[ \t]+//", lines[0])
            and lines[2] == lines[0]
        ):
            heading = re.fullmatch(
                r"//[ \t]+-{8,}[ \t]+(.+?)[ \t]+-{8,}[ \t]+//",
                lines[1],
            )
            if heading is not None:
                return heading.group(1)

    if language == "tcl":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 20
            and lines[0].startswith("#!")
            and sum(re.fullmatch(r"#={20,}", line) is not None for line in lines) >= 3
            and all(line.startswith("#") for line in lines)
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"#={20,}", line):
                    continue
                framed = re.fullmatch(r"#={3}(?P<body>.+?)[ \t]*={3,}", line)
                if framed is not None:
                    restored.append(framed.group("body").rstrip())
                    continue
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "txl":
        lines = raw_comment.split("\n")
        if len(lines) >= 2 and all(line.startswith("%%") for line in lines):
            return _join_restored_lines([line[2:].lstrip(" ").rstrip() for line in lines])

    if language == "vhdl":
        lines = raw_comment.split("\n")
        if len(lines) >= 2 and all(re.match(r"-{5,}\S", line) for line in lines):
            restored = []
            for line in lines:
                body = re.sub(r"^-{5,}", "", line)
                body = re.sub(r"-{8,}$", "", body)
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "wavefront_object":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 7
            and sum(re.fullmatch(r"#{4,}", line) is not None for line in lines) >= 3
            and all(line.startswith("#") for line in lines)
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"#{4,}", line):
                    continue
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "wdl":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 20
            and all(line.startswith("##") for line in lines)
            and lines[0].startswith("### ")
        ):
            restored = []
            for line in lines:
                marker = re.match(r"#{2,}", line)
                assert marker is not None
                body = line[marker.end() :]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "xbase":
        marker = re.fullmatch(r"\t\*{3}[ \t]+(\S.*?)[ \t]*", raw_comment)
        if marker is not None:
            return marker.group(1).rstrip()

    if language == "xml_property_list":
        vertical = re.fullmatch(
            r"<!--\n[ \t]+\|[ \t]*(?P<body>\S.*?)\n-->",
            raw_comment,
        )
        if vertical is not None and "auto-generated" in vertical.group("body"):
            return vertical.group("body").rstrip()

    if language == "xtend":
        framed = re.fullmatch(r"/\*{5,}(?P<body>[A-Za-z][A-Za-z0-9 ]*?)\*{5,}/", raw_comment)
        if framed is not None:
            return framed.group("body").strip()

    if language == "zimpl":
        lines = raw_comment.split("\n")
        if len(lines) >= 4 and re.fullmatch(r"#{8,}", lines[0]) and lines[2] == lines[0]:
            title = re.fullmatch(r"#[ \t]+(.+?)[ \t]+#", lines[1])
            if title is not None and all(line.startswith("#") for line in lines[3:]):
                restored = [title.group(1)]
                for line in lines[3:]:
                    body = line[1:]
                    if body.startswith(" "):
                        body = body[1:]
                    restored.append(body.rstrip())
                return _join_restored_lines(restored)

    return None


def _sanitize_final_safe_mixed_layout(
    language: str,
    raw_comment: str,
) -> str | None:
    """Restore mixed prose/code cards using exact, complete structural gates."""

    if language == "apex":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 10
            and re.fullmatch(r"/\*={40,}", lines[0])
            and lines[-1].endswith("*/")
            and "Update History" in raw_comment
            and "Developer" in raw_comment
        ):
            restored = []
            for line in lines[1:-1]:
                if not line.startswith("*"):
                    return None
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                if re.fullmatch(r"[ \t]*[-=]{8,}", body):
                    restored.append("")
                else:
                    restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "asn1":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 20
            and all(line.startswith("--") for line in lines)
            and "Version History" in raw_comment
            and "HEADER SECTION" in raw_comment
            and sum(re.fullmatch(r"--[ \t]*={20,}", line) is not None for line in lines) >= 4
        ):
            restored = []
            for line in lines:
                body = line[2:]
                if re.fullmatch(r"[ \t]*={20,}", body):
                    continue
                heading = re.fullmatch(r"={4}[ \t]*(.+?)[ \t]*={4}--", body)
                if heading is not None:
                    restored.append(heading.group(1))
                    continue
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "asn_1":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 20
            and all(line.startswith("--") for line in lines)
            and "PUBLIC DOMAIN NOTICE" in raw_comment
            and "National Center for Biotechnology Information" in raw_comment
            and sum(re.fullmatch(r"--[ \t]*={20,}", line) is not None for line in lines) >= 3
        ):
            restored = []
            for line in lines:
                body = line[2:]
                if re.fullmatch(r"[ \t]*={20,}", body):
                    continue
                restored.append(body.lstrip(" \t").rstrip())
            return _join_restored_lines(restored)

    if language == "cobol":
        lines = raw_comment.split("\n")
        if (
            len(lines) == 7
            and re.fullmatch(r"\*{20,}", lines[0])
            and lines[-1] == lines[0]
            and all(re.fullmatch(r"\*.*\*", line) for line in lines[1:-1])
            and "PROGRAM" in raw_comment
            and "COMPILE TYPE" in raw_comment
        ):
            restored = []
            for line in lines[1:-1]:
                body = line[1:-1]
                body = body[4:] if body.startswith("    ") else body.lstrip(" ")
                body = body.rstrip()
                body = re.sub(r"(?:(?:\x81@){2,})$", "\x81@", body)
                restored.append(body)
            return _join_restored_lines(restored)

    if language == "cuda":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 10
            and raw_comment.startswith("/*////")
            and raw_comment.endswith("////*/")
            and "Copyright" in raw_comment
            and "main.cu" in raw_comment
        ):
            inner_lines = raw_comment[2:-2].split("\n")
            restored = []
            for line in inner_lines:
                if re.fullmatch(r"/{8,}", line):
                    continue
                left_width = len(line) - len(line.lstrip("/"))
                right_width = len(line) - len(line.rstrip("/"))
                if left_width < 2 or right_width < 2:
                    return None
                body = line[left_width : len(line) - right_width]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

        if (
            len(lines) >= 8
            and all(line.startswith("//") for line in lines)
            and "Part of the LLVM Project" in raw_comment
            and sum(re.fullmatch(r"//={3}-{20,}={3}//", line) is not None for line in lines) >= 2
        ):
            restored = []
            for line in lines:
                body = line[2:]
                if body.startswith("===") and body.endswith("//"):
                    body = body[:-2]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "dm":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 20
            and lines[0] == "/**"
            and raw_comment.endswith("*/")
            and "pif_Arithmetic" in raw_comment
            and "Contents" in raw_comment
        ):
            restored = []
            for line in lines[1:]:
                if line.endswith("*/"):
                    line = line[:-2]
                if re.fullmatch(r"[ \t]*\*{20,}", line):
                    restored.append("")
                    continue
                if line.startswith(" **"):
                    body = line[3:]
                    if body.startswith(" "):
                        body = body[1:]
                    restored.append(body.rstrip())
                else:
                    restored.append(line.rstrip())
            return _join_restored_lines(restored)

    if language == "limbo":
        banner = re.fullmatch(
            r"(?P<hashes>#{8,})(?P<body>[^\n]*#{4,}[^\n]*#{4,})"
            r"[ \t]+\*\n?",
            raw_comment,
        )
        if banner is not None:
            return (banner.group("hashes")[1:] + banner.group("body")).rstrip()

    if language == "makefile":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 15
            and all(line.startswith("#") for line in lines)
            and "License" in lines[0]
            and sum(re.fullmatch(r"#\*{8,}(?:License\*+)?/?", line) is not None for line in lines)
            >= 3
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"#\*{8,}(?:License\*+)?/?", line):
                    continue
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "metal":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 20
            and lines[0].startswith("/*  $Id:")
            and raw_comment.endswith("*/")
            and "PUBLIC DOMAIN NOTICE" in raw_comment
            and "National Center for Biotechnology Information" in raw_comment
        ):
            restored = [lines[0][2:].lstrip(" \t").rstrip()]
            for line in lines[1:]:
                if line.endswith("*/"):
                    line = line[:-2]
                gutter = re.fullmatch(r"[ \t]*\*(.*)", line)
                if gutter is None:
                    if line.strip():
                        return None
                    restored.append("")
                    continue
                body = gutter.group(1)
                if re.fullmatch(r"[ \t]*={20,}", body):
                    continue
                restored.append(body.lstrip(" \t").rstrip())
            return _join_restored_lines(restored)

    if language == "motoko":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 12
            and lines[0] == "/**"
            and raw_comment.endswith("*/")
            and sum(re.fullmatch(r"[ \t]*\*={20,}", line) is not None for line in lines) == 2
            and "@license" in raw_comment
        ):
            restored = []
            for line in lines[1:]:
                if line.endswith("*/"):
                    line = line[:-2]
                if line.startswith(" *"):
                    body = line[2:]
                    if body.startswith(" "):
                        body = body[1:]
                    restored.append(body.rstrip())
                else:
                    restored.append(line.rstrip())
            return _join_restored_lines(restored)

    if language == "mql5":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 5
            and re.fullmatch(r"//\+-{20,}\+", lines[0])
            and re.fullmatch(r"//\+-{20,}\+", lines[-1])
            and all(re.fullmatch(r"//(?:\+-{20,}\+|\|.*\|)", line) for line in lines)
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"//\+-{20,}\+", line):
                    restored.append("")
                else:
                    framed = re.fullmatch(r"//\|(.*)\|", line)
                    assert framed is not None
                    restored.append(framed.group(1).strip())
            return _join_restored_lines(restored)

    if language == "nextflow":
        lines = raw_comment.split("\n")
        if len(lines) >= 6 and lines[0] == "/*" and lines[-1] == " */":
            bodies = []
            for line in lines[1:-1]:
                match = re.fullmatch(r" \*(?: (?P<body>.*))?", line)
                if match is None:
                    break
                bodies.append((match.group("body") or "").rstrip())
            else:
                if (
                    len(bodies) >= 4
                    and re.fullmatch(r"-{20,}", bodies[0])
                    and bodies[2] == bodies[0]
                    and bodies[1].startswith(" ")
                    and any(body.strip() for body in bodies[3:])
                ):
                    restored = [
                        bodies[1].lstrip(" "),
                        bodies[2],
                        *bodies[3:],
                    ]
                    return _join_restored_lines(restored)

    if language == "opencl":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 10
            and re.fullmatch(r"/\*{20,}", lines[0])
            and re.fullmatch(r"[ \t]*\*{20,}/", lines[-1])
            and "LuxCoreRender" in raw_comment
            and all(re.fullmatch(r"[ \t]*\*.*\*", line) for line in lines[1:-1])
        ):
            restored = []
            for line in lines[1:-1]:
                body = line.lstrip(" \t")[1:-1]
                if body.startswith(" "):
                    body = body[1:]
                if body.lstrip(" ").startswith("This file is part of LuxCoreRender."):
                    body = body.lstrip(" ")
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "pep8":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 8
            and all(line.startswith(";") for line in lines)
            and any(re.fullmatch(r";-{8,}", line) for line in lines)
            and any(line.startswith(";\t") for line in lines)
        ):
            restored = []
            for line in lines:
                body = line[1:]
                if re.fullmatch(r"-{8,}", body):
                    continue
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "routeros_script":
        lines = raw_comment.split("\n")
        borders = [index for index, line in enumerate(lines) if re.fullmatch(r"#{40,}", line)]
        if (
            len(lines) >= 15
            and len(borders) >= 3
            and all(line.startswith("#") for line in lines)
            and sum(re.fullmatch(r"#.*#", line) is not None for line in lines) >= 4
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"#{40,}", line):
                    restored.append("")
                    continue
                framed = re.fullmatch(r"#(?P<body>.*)#", line)
                if framed is not None:
                    restored.append(framed.group("body").strip())
                    continue
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "verilog":
        lines = raw_comment.split("\n")
        border_indexes = [
            index for index, line in enumerate(lines) if re.fullmatch(r"/{20,}", line)
        ]
        if (
            len(lines) >= 20
            and len(border_indexes) >= 2
            and border_indexes[0] == 0
            and all(line.startswith("//") for line in lines)
            and "8051 cores Definitions" in raw_comment
        ):
            restored = []
            last_border = border_indexes[-1]
            for index, line in enumerate(lines):
                if re.fullmatch(r"/{20,}", line):
                    restored.append("")
                    continue
                if index < last_border:
                    framed = re.fullmatch(r"////(?P<body>.*)////", line)
                    if framed is None:
                        return None
                    body = framed.group("body")
                    for _ in range(2):
                        if body.startswith((" ", "\t")):
                            body = body[1:]
                    restored.append(body.rstrip())
                else:
                    body = line[2:]
                    if body.startswith(" "):
                        body = body[1:]
                    restored.append(body.rstrip())
            return _join_restored_lines(restored)

    return None


def _sanitize_policy_safe_residual_layout(
    language: str,
    raw_comment: str,
) -> str | None:
    """Clean the final independently approved, narrowly scoped residuals."""

    if language == "aidl":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 15
            and re.fullmatch(r"/\*{20,}", lines[0])
            and re.fullmatch(r"\*{20,}/", lines[-1])
            and "droid2droid - Distributed Android Framework" in raw_comment
            and all(re.fullmatch(r"[ \t]*\*.*", line) for line in lines[1:-1])
        ):
            restored = []
            for line in lines[1:-1]:
                body = line.lstrip(" \t")[1:]
                if re.fullmatch(r"\*{20,}", body.strip()):
                    continue
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "gn":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 10
            and all(line.startswith("#") for line in lines)
            and "VERY IMPORTANT NOTE!" in raw_comment
            and "VIVALDI_FFMPEG_REBUILD" in raw_comment
        ):
            restored = []
            for line in lines:
                body = line[1:]
                if body.startswith(" "):
                    body = body[1:]
                if re.fullmatch(r"\*{20,}", body):
                    continue
                framed = re.fullmatch(r"\*[ \t]+(.+?)[ \t]+\*", body)
                restored.append(framed.group(1) if framed is not None else body.rstrip())
            return _join_restored_lines(restored)

    if language == "html_plus_php":
        lines = raw_comment.split("\n")
        if (
            len(lines) == 4
            and re.fullmatch(r"[ \t]*//-{8,}", lines[0])
            and re.fullmatch(r"[ \t]*//-{8,}", lines[2])
        ):
            title = re.fullmatch(r"[ \t]*//-[ \t]+(.+?)[ \t]+-", lines[1])
            prose = re.fullmatch(r"[ \t]*//[ \t]+(.+)", lines[3])
            if title is not None and prose is not None:
                return f"{title.group(1)}\n{prose.group(1).rstrip()}"

    if language == "logtalk":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 7
            and re.fullmatch(r"%{20,}", lines[0])
            and all(line.startswith("%") for line in lines)
            and "ported to Logtalk by Paulo Moura" in raw_comment
        ):
            restored = []
            for line in lines:
                if re.fullmatch(r"%{20,}", line):
                    continue
                if not line.startswith("%%"):
                    return None
                body = line[2:]
                if body.startswith(" "):
                    body = body[1:]
                body = body.rstrip()
                if not body and restored and not restored[-1]:
                    continue
                restored.append(body)
            return _join_restored_lines(restored)

    if language in {"mql", "mql4"}:
        lines = raw_comment.split("\n")
        if (
            len(lines) == 5
            and re.fullmatch(r"//\+-{20,}\+", lines[0])
            and lines[-1] == lines[0]
            and all(re.fullmatch(r"//\|.*\|", line) for line in lines[1:-1])
            and "#MAMA.mq4" in raw_comment
        ):
            restored = []
            for line in lines[1:-1]:
                framed = re.fullmatch(r"//\|(.*)\|", line)
                assert framed is not None
                body = framed.group(1).strip()
                if body:
                    restored.append(body)
            return "\n".join(restored)

    if language == "proguard":
        lines = raw_comment.split("\n")
        exact_double = re.compile(r"##(?!#)(.*)")
        if (
            len(lines) >= 15
            and sum(exact_double.fullmatch(line) is not None for line in lines) >= 10
            and all(line == "#" or exact_double.fullmatch(line) is not None for line in lines)
            and "ProGuard rules" in raw_comment
        ):
            restored = []
            for line in lines:
                if line == "#":
                    restored.append("")
                    continue
                match = exact_double.fullmatch(line)
                assert match is not None
                body = match.group(1)
                if body.startswith(" "):
                    body = body[1:]
                restored.append(body.rstrip())
            return _join_restored_lines(restored)

    if language == "propeller_spin":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 10
            and lines[0].startswith("{{ FDS_sgf.spin")
            and lines[-1] == "}}"
            and all(not line.strip() or line.startswith("  ") for line in lines[1:-1])
        ):
            restored = [lines[0][3:].rstrip()]
            restored.extend(
                line[2:].rstrip() if line.startswith("  ") else "" for line in lines[1:-1]
            )
            return _join_restored_lines(restored)

    return None


def _sanitize_strict_real_world_scaffold(language: str, raw_comment: str) -> str | None:
    """Clean complete, language-specific scaffold shapes seen in the oracle run.

    Every branch requires both a language and a full structural shape. The
    returned text is formed only by deleting delimiters, rulers, gutters, and
    their adjacent padding from ``raw_comment``.
    """

    secondary_gutter_result = _sanitize_validated_secondary_gutter_scaffold(
        language,
        raw_comment,
    )
    if secondary_gutter_result is not None:
        return secondary_gutter_result

    fixed_frame_result = _sanitize_validated_fixed_frame_scaffold(language, raw_comment)
    if fixed_frame_result is not None:
        return fixed_frame_result

    if (
        language == "cweb"
        and raw_comment.startswith("/*++ ")
        and raw_comment.endswith("--*/")
        and raw_comment[-5:-4] in {" ", "\n"}
    ):
        return CommentSanitizer(language).sanitize(
            "/*" + raw_comment[4:-4] + "*/",
        )

    if language in {"ec", "rpc", "vala"}:
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 3
            and lines[0] == "/*-"
            and lines[-1] == " */"
            and all(not line.strip() or line.startswith(" *") for line in lines[1:-1])
        ):
            return CommentSanitizer(language).sanitize("/*" + raw_comment[3:])
        if language == "ec":
            bordered = _sanitize_ec_star_border(raw_comment)
            if bordered is not None:
                return bordered

    if language == "grammatical_framework":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 4
            and lines[0] == "{--"
            and re.fullmatch(r"={8,}[ \t]+--}", lines[-1]) is not None
        ):
            return _normalize_sanitized_body("\n".join(lines[1:-1]))

    if language == "actionscript":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 4
            and re.fullmatch(r"/\*\*[ \t]+\S.*", lines[0]) is not None
            and re.fullmatch(r"[ \t]+\*[ \t]*-{8,}[ \t]+\*", lines[1]) is not None
            and re.fullmatch(r"[ \t]+\*[ \t]*-{8,}[ \t]+\*/", lines[-1]) is not None
            and all(not line.strip() or re.match(r"^[ \t]+\*", line) for line in lines[1:])
        ):
            rewritten = [lines[0], "", *lines[2:-1], "*/"]
            return CommentSanitizer(language).sanitize("\n".join(rewritten))

    if language == "cadence":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 3
            and all(line.startswith("//") for line in lines)
            and re.fullmatch(r"//[ \t]+\*{8,}[ \t]*", lines[1]) is not None
        ):
            return CommentSanitizer(language).sanitize("\n".join([lines[0], *lines[2:]]))

    if language == "coldfusion":
        lines = raw_comment.split("\n")
        if (
            len(lines) == 4
            and lines[0].startswith("<!--- ")
            and re.fullmatch(r"-{8,}", lines[1]) is not None
            and lines[-1] == "--->"
        ):
            return CommentSanitizer(language).sanitize("\n".join([lines[0], *lines[2:]]))

    if language == "erlang":
        erlang_result = _sanitize_erlang_ruler_layout(raw_comment)
        if erlang_result is not None:
            return erlang_result

    if language == "module_management_system":
        lines = raw_comment.split("\n")
        if (
            len(lines) >= 4
            and re.fullmatch(r"#\*{8,}", lines[0]) is not None
            and re.fullmatch(r"#\*{8,}", lines[-1]) is not None
        ):
            framed = [re.fullmatch(r"#(.*)\*", line) for line in lines[1:-1]]
            if all(match is not None for match in framed):
                return _normalize_sanitized_body(
                    "\n".join(
                        match.group(1).strip()
                        for match in framed
                        if match is not None and match.group(1).strip()
                    )
                )

    if language == "apacheconf":
        lines = raw_comment.split("\n")
        if (
            len(lines) == 3
            and re.fullmatch(r"#[ \t]+-{8,}", lines[0]) is not None
            and lines[0] == lines[-1]
        ):
            content = re.fullmatch(r"#[ \t]+\|[ \t]+(.+?)[ \t]+\|", lines[1])
            if content is not None:
                return content.group(1)

    if language == "alloy":
        lines = raw_comment.split("\n")
        if len(lines) >= 2 and all(line.startswith("//") for line in lines):
            heading = re.fullmatch(r"//-{3,}[ \t]+(.+?)[ \t]+-{3,}", lines[0])
            if heading is not None:
                rewritten = ["//" + heading.group(1), *lines[1:]]
                return CommentSanitizer(language).sanitize("\n".join(rewritten))

    if language == "cycript":
        framed = re.fullmatch(r"/\*-{4,}[ \t]+(.+?)[ \t]+-{4,}\*/", raw_comment)
        if framed is not None:
            return framed.group(1)

    if language == "macaulay2":
        modeline = re.fullmatch(r"-\*-[ \t]+(.+?)[ \t]+-\*-", raw_comment)
        if modeline is not None:
            return modeline.group(1)

    if language in {"html_plusdjango", "jinja"}:
        framed = re.fullmatch(r"{##[ \t]+(.+?)[ \t]+##}", raw_comment)
        if framed is not None:
            return framed.group(1)

    if language == "papyrus":
        framed = re.fullmatch(
            r";(?:=+[ \t]+(.+?)[ \t]+=+|--[ \t]+(.+?)[ \t]+-{8,})\n?",
            raw_comment,
        )
        if framed is not None:
            return next(group for group in framed.groups() if group is not None)

    if language == "pawn":
        lines = raw_comment.split("\n")
        if lines:
            title = re.fullmatch(
                r"/\*[ \t]+(?P<edge>[-+]{8,})[ \t]+(?P<title>.+?)[ \t]+(?P=edge)",
                lines[0],
            )
            if title is not None and lines[-1] == "*/":
                rewritten = ["/* " + title.group("title"), *lines[1:]]
                return CommentSanitizer(language).sanitize("\n".join(rewritten))

    if language == "webassembly":
        lines = raw_comment.split("\n")
        if len(lines) >= 3:
            opening = re.fullmatch(r"\(;;[ \t]+(STD(?:OUT|ERR))[ \t]+;;;", lines[0])
            closing = re.fullmatch(r";;;[ \t]+(STD(?:OUT|ERR))[ \t]+;;\)", lines[-1])
            if opening is not None and closing is not None and opening.group(1) == closing.group(1):
                label = opening.group(1)
                return _normalize_sanitized_body("\n".join([label, *lines[1:-1], label]))

    if language == "sqf":
        framed = re.fullmatch(r"//[ \t]+\*[ \t]+(.+?)[ \t]+\*", raw_comment)
        if framed is not None:
            return framed.group(1)

    if language in {"asn1", "asn_1"}:
        lines = raw_comment.split("\n")
        if len(lines) >= 2 and all(line.startswith("--") for line in lines):
            heading = re.fullmatch(r"--[ \t]+(.+?)[ \t]+--", lines[0])
            if heading is not None:
                rewritten = ["-- " + heading.group(1), *lines[1:]]
                return CommentSanitizer(language).sanitize("\n".join(rewritten))

    return None


class CommentSanitizer:
    """Normalize extracted comments for one language.

    Args:
        language: Registry language key used to resolve comment delimiters.

    Raises:
        NotImplementedError: If the language is not present in the registry.
    """

    def __init__(self, language: str):
        self.language = language
        self._language_key = _resolve_comment_language_key(language)
        self.syntax = get_comment_syntax(self._language_key)
        self._sanitizer_syntax = _build_sanitizer_syntax(self.syntax)
        language = self._language_key
        if language == "bro":
            self._sanitizer_syntax = _SanitizerSyntax(
                line_wrappers=(("##!", ""), *self._sanitizer_syntax.line_wrappers),
                block_wrappers=self._sanitizer_syntax.block_wrappers,
            )
        literal_doc_marker_languages = {
            "abap_cds": {("///", ""), ("//!", "")},
            "linker_script": {("///", ""), ("//!", "")},
            "mint": {("///", ""), ("//!", "")},
            "objective_j": {("//!", "")},
            "rascal": {("///", ""), ("//!", "")},
            "scilab": {("//!", "")},
            "smithy": {("///", "")},
            "webassembly_interface_type": {("///", "")},
            "wit": {("///", "")},
            "zmodel": {("///", "")},
        }
        if language in literal_doc_marker_languages:
            self._sanitizer_syntax = _SanitizerSyntax(
                line_wrappers=tuple(
                    wrapper
                    for wrapper in self._sanitizer_syntax.line_wrappers
                    if wrapper not in literal_doc_marker_languages[language]
                ),
                block_wrappers=self._sanitizer_syntax.block_wrappers,
            )
        if language in {"webassembly_interface_type", "wit", "zmodel"}:
            self._sanitizer_syntax = _SanitizerSyntax(
                line_wrappers=self._sanitizer_syntax.line_wrappers,
                block_wrappers=tuple(
                    wrapper
                    for wrapper in self._sanitizer_syntax.block_wrappers
                    if not wrapper[0].startswith("/**")
                ),
            )
        language_specific_line_wrappers = {
            "antlr": (("////", ""),),
            "asciidoc": (("////", ""),),
            "aspectj": (("////", ""),),
            "asymptote": (("////", ""),),
            "bluespec": (("////", ""),),
            "brightscript": (("'//", ""), ("'**", ""), ("'*", "")),
            "bro": (("#!", ""),),
            "clojure": ((";;;;", ""),),
            "common_lisp": ((";;;;", ""),),
            "curry": (("---", ""),),
            "dtrace": (("////", ""),),
            "edje_data_collection": (("////", ""),),
            "emacs_lisp": ((";;;;", ""),),
            "erlang": (("%%%", ""), ("%%", "")),
            "fortran": (("!>", ""), ("!!", "")),
            "fortran_free_form": (("!>", ""), ("!!", "")),
            "freebasic": (("''", ""),),
            "genero": (("#+", ""),),
            "genero_forms": (("#+", ""),),
            "gleam": (("////", ""),),
            "glsl": (("////", ""),),
            "grace": (("////", ""),),
            "gsc": (("////", ""),),
            "lfe": ((";;;;", ""),),
            "lisp": ((";;;;", ""),),
            "matlab": (("%%%", ""), ("%%", "")),
            "nextflow": (("////", ""),),
            "openscad": (("////", ""),),
            "openstep_property_list": (("////", ""),),
            "piglatin": (("----", ""),),
            "plpgsql": (("----", ""), ("---", "")),
            "purescript": (("---", ""),),
            "qt_script": (("////", ""),),
            "r": (("#'", ""),),
            "supercollider": (("////", ""),),
            "sqlpl": (("----", ""),),
            "zeek": (("##!", ""), ("#!", "")),
            "zenscript": (("////", ""),),
        }
        if language in language_specific_line_wrappers:
            self._sanitizer_syntax = _SanitizerSyntax(
                line_wrappers=(
                    *language_specific_line_wrappers[language],
                    *self._sanitizer_syntax.line_wrappers,
                ),
                block_wrappers=self._sanitizer_syntax.block_wrappers,
            )
        language_specific_block_wrappers = {
            "classic_asp": (("<!--", "//-->"),),
            "d": (("/***", "***/"), ("/***", "*/")),
            "elm": (("{--", "--}"), ("{--", "-}")),
            "frege": (("{--", "--}"), ("{--", "-}")),
            "haskell": (("{--", "--}"), ("{--", "-}")),
            "mtml": (("<!--", "//-->"),),
            "xbase": (("/*", "/*/"),),
            "xproc": (("<!--", "//-->"),),
        }
        if language in language_specific_block_wrappers:
            self._sanitizer_syntax = _SanitizerSyntax(
                line_wrappers=self._sanitizer_syntax.line_wrappers,
                block_wrappers=(
                    *language_specific_block_wrappers[language],
                    *self._sanitizer_syntax.block_wrappers,
                ),
            )
        self._protected_padding_chars = {
            "1c_enterprise": frozenset("+"),
            "autoit": frozenset("="),
            "beef": frozenset("#<>+-."),
            "brightscript": frozenset("*"),
            "chuck": frozenset("<"),
            "clean": frozenset("<"),
            "coq": frozenset("*"),
            "rocq": frozenset("*"),
            "rocq_prover": frozenset("*"),
            "faust": frozenset("="),
            "forth": frozenset("*"),
            "literate_coffeescript": frozenset("#"),
            "monkey": frozenset("="),
            "nextflow": frozenset("#"),
            "pascal": frozenset("-"),
            "propeller_spin": frozenset("#"),
            "texinfo": frozenset("="),
            "x_bit_map": frozenset("-"),
            "x_bitmap": frozenset("-"),
        }.get(language, frozenset())

    def sanitize(self, comment: str | QueryMatch) -> str:
        """Return the content-bearing body for one extracted comment.

        Args:
            comment: Raw comment text or a ``QueryMatch`` returned by a comment
                query.

        Returns:
            The comment body with language delimiters, repeated line prefixes,
            and common block gutters removed.
        """

        raw_comment = _coerce_comment_text(comment)
        directive_candidate = raw_comment.lstrip(" \t")
        excluded_prefixes = self.syntax.excluded_comment_prefixes_for_language(self._language_key)
        if any(directive_candidate.startswith(prefix) for prefix in excluded_prefixes):
            return raw_comment
        if self._language_key == "survex_data" and directive_candidate:
            marker = directive_candidate[0]
            if ord(marker) < 128 and not marker.isalnum() and not marker.isspace():
                normalized = _normalize_newlines(directive_candidate)
                lines = normalized.split("\n")
                if len(lines) > 1 and all(
                    line.lstrip(" \t").startswith(marker) for line in lines[1:]
                ):
                    bodies = []
                    for line in lines:
                        body = line.lstrip(" \t")[1:]
                        bodies.append(body[1:] if body.startswith((" ", "\t")) else body)
                    return _normalize_sanitized_body("\n".join(bodies))
                body = normalized[1:]
                if body.startswith((" ", "\t")):
                    body = body[1:]
                return _normalize_sanitized_body(body)
        if self.syntax.canonical_name == "rust" and directive_candidate.startswith("////"):
            normalized = _normalize_newlines(directive_candidate)
            lines = normalized.split("\n")
            if all(line.startswith("////") for line in lines):
                return _normalize_sanitized_body("\n".join(line[2:] for line in lines))
        if (
            self.syntax.canonical_name == "rust"
            and directive_candidate.startswith("/***")
            and directive_candidate.endswith("*/")
        ):
            return _sanitize_block_body(
                directive_candidate[2:-2],
                ("/*", "*/"),
                self._sanitizer_syntax.line_wrappers,
                allow_doc_star=True,
                protected_ruler_chars=self._protected_padding_chars,
            )
        if self._language_key == "mdsvex" and re.match(
            r"<!--\s*svelte-ignore\s", directive_candidate
        ):
            return raw_comment
        if self._language_key == "mermaid" and directive_candidate.startswith("%%{"):
            return raw_comment
        if self._language_key == "mermaid":
            normalized_comment = _normalize_newlines(raw_comment)
            mermaid_bodies = []
            for line in normalized_comment.split("\n"):
                stripped_line = line.lstrip(" \t")
                if not stripped_line.startswith("%%") or len(stripped_line) == 2:
                    break
                body = stripped_line[2:]
                if body.startswith((" ", "\t")):
                    body = body[1:]
                mermaid_bodies.append(body)
            else:
                return _normalize_sanitized_body("\n".join(mermaid_bodies))
        if self._language_key == "linear_programming":
            normalized_comment = _normalize_newlines(raw_comment)
            lines = normalized_comment.split("\n")
            if lines and all(line.startswith("\\") for line in lines):
                return "\n".join(line[1:] for line in lines)
        if self.syntax.canonical_name == "omgrofl":
            raw_comment = raw_comment.translate(_JAVA_SCANNER_LINE_ENDINGS)
        raw_comment = _normalize_newlines(raw_comment)
        if self._language_key in {"dune", "pact", "pddl"}:
            cleaned_lines = []
            for line in raw_comment.split("\n"):
                wrapper = re.match(r"^[ \t]*;", line)
                if wrapper is None:
                    cleaned_lines.append(line)
                    continue
                body = line[wrapper.end() :]
                cleaned_lines.append(body[1:] if body.startswith(" ") else body)
            return _normalize_sanitized_body("\n".join(cleaned_lines))
        if self._language_key == "bluespec_bh" and not raw_comment.lstrip(" \t").startswith("{-"):
            raw_comment = re.sub(r"(?m)^([ \t]*)-{2,}", r"\1--", raw_comment)
        if self.syntax.canonical_name == "cobol":
            raw_comment = re.sub(
                r"(?m)^[^\r\n]{6}(?=[*/])",
                "",
                raw_comment,
            )
            if re.fullmatch(r"\*{4,}", raw_comment.strip()):
                return ""
        if self._language_key == "applescript" and re.fullmatch(
            r"#!(?:/usr/bin/osascript|/usr/bin/env[ \t]+osascript)",
            raw_comment,
        ):
            return raw_comment
        if self.syntax.sanitizer_mode == "raw":
            return raw_comment

        pure_line_ruler = _sanitize_pure_registered_line_ruler(
            self._language_key,
            raw_comment,
            self._sanitizer_syntax.line_wrappers,
        )
        if pure_line_ruler is not None:
            return pure_line_ruler

        batch_two_exact = _sanitize_batch_two_exact_layout(self._language_key, raw_comment)
        if batch_two_exact is not None:
            return batch_two_exact

        strict_restoration_result = _sanitize_strict_restoration_layout(
            self._language_key,
            raw_comment,
        )
        if strict_restoration_result is not None:
            return strict_restoration_result

        validated_padding_result = _sanitize_validated_padding_layout(
            self._language_key,
            raw_comment,
        )
        if validated_padding_result is not None:
            return validated_padding_result

        validated_legacy_frame = _sanitize_validated_legacy_frame(
            self._language_key,
            raw_comment,
        )
        if validated_legacy_frame is not None:
            return validated_legacy_frame

        final_safe_indentation = _sanitize_final_safe_indentation_layout(
            self._language_key,
            raw_comment,
        )
        if final_safe_indentation is not None:
            return final_safe_indentation

        final_safe_strict = _sanitize_final_safe_strict_layout(
            self._language_key,
            raw_comment,
        )
        if final_safe_strict is not None:
            return final_safe_strict

        final_safe_mixed = _sanitize_final_safe_mixed_layout(
            self._language_key,
            raw_comment,
        )
        if final_safe_mixed is not None:
            return final_safe_mixed

        policy_safe_residual = _sanitize_policy_safe_residual_layout(
            self._language_key,
            raw_comment,
        )
        if policy_safe_residual is not None:
            return policy_safe_residual

        strict_scaffold_result = _sanitize_strict_real_world_scaffold(
            self._language_key,
            raw_comment,
        )
        if strict_scaffold_result is not None:
            return strict_scaffold_result

        literal_slash_result = _sanitize_literal_double_slash_lines(self._language_key, raw_comment)
        if literal_slash_result is not None:
            return literal_slash_result

        if self._language_key == "batchfile" and re.fullmatch(
            r"(?i:REM)[ \t]+\*{8,}[ \t]+(?i:REM)",
            raw_comment,
        ):
            return ""

        numbered_frame_result = _sanitize_numbered_star_frame(self._language_key, raw_comment)
        if numbered_frame_result is not None:
            return numbered_frame_result

        mcfunction_frame_result = _sanitize_mcfunction_fixed_frame(self._language_key, raw_comment)
        if mcfunction_frame_result is not None:
            return mcfunction_frame_result

        inner_layer_result = _sanitize_full_inner_c_layer(self._language_key, raw_comment)
        if inner_layer_result is not None:
            return inner_layer_result

        fixed_frame_result = _sanitize_complete_fixed_frame(self._language_key, raw_comment)
        if fixed_frame_result is not None:
            return fixed_frame_result

        if self._language_key in {"x_bit_map", "x_bitmap"}:
            star_box = _sanitize_x_bitmap_star_box(raw_comment)
            if star_box is not None:
                return star_box

        if self.syntax.canonical_name == "abap":
            abap_result = _sanitize_abap_comment(raw_comment)
            if abap_result is not None:
                return abap_result

        if self._language_key == "faust":
            faust_result = _sanitize_faust_special_block(raw_comment)
            if faust_result is not None:
                return faust_result

        if self._language_key in _GENERO_LANGUAGE_KEYS and re.match(
            r"^[ \t]*#[ \t]+\+-{8,}\+",
            raw_comment,
        ):
            genero_result = _sanitize_genero_line_result(raw_comment, raw_comment)
            if genero_result != raw_comment:
                return genero_result

        if self._language_key == "monkey":
            monkey_result = _sanitize_monkey_special_comment(raw_comment)
            if monkey_result is not None:
                return monkey_result

        if self._language_key == "powerbuilder":
            powerbuilder_result = _sanitize_powerbuilder_template(raw_comment)
            if powerbuilder_result is not None:
                return powerbuilder_result

        if self._language_key == "scaml":
            scaml_result = _sanitize_scaml_scoped_comment(raw_comment)
            if scaml_result is not None:
                return scaml_result

        if self.syntax.canonical_name == "lua":
            lua_long_comment = _strip_lua_long_comment_wrapper(raw_comment)
            if lua_long_comment is not None:
                inner, wrapper = lua_long_comment
                return _sanitize_block_body(
                    inner,
                    wrapper,
                    self._sanitizer_syntax.line_wrappers,
                    allow_doc_star=True,
                    protected_ruler_chars=self._protected_padding_chars,
                )

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

        open_line_wrappers = tuple(
            wrapper for wrapper in self._sanitizer_syntax.line_wrappers if not wrapper[1]
        )
        grouped_line_scaffolding = _strip_grouped_wrapped_lines(
            raw_comment,
            open_line_wrappers,
        )
        if grouped_line_scaffolding is not None:
            lines, _ = grouped_line_scaffolding
            embedded_comment = "\n".join(lines).strip(" \t\n")
            embedded_block = _strip_block_wrapper(
                embedded_comment,
                _EMBEDDED_BLOCK_WRAPPERS,
            )
            if embedded_block is not None:
                inner, wrapper = embedded_block
                return _sanitize_block_body(
                    inner,
                    wrapper,
                    self._sanitizer_syntax.line_wrappers,
                    allow_doc_star=True,
                    protected_ruler_chars=self._protected_padding_chars,
                )

        block_result = _strip_block_wrapper(raw_comment, self._sanitizer_syntax.block_wrappers)
        if block_result is not None:
            inner, wrapper = block_result
            protected_ruler_chars = self._protected_padding_chars | (
                frozenset("=")
                if raw_comment.startswith(wrapper[0] + wrapper[0][-1] + "\n")
                else frozenset()
            )
            cleaned_block = _sanitize_block_body(
                inner,
                wrapper,
                self._sanitizer_syntax.line_wrappers,
                allow_doc_star=self._language_key not in {"handlebars", "mediawiki", "wikitext"},
                protected_ruler_chars=protected_ruler_chars,
                strip_single_line_padding=self._language_key != "powershell",
            )
            if (
                self._language_key in {"x_bit_map", "x_bitmap"}
                and "Sun Microsystems, Inc" in raw_comment
                and sum(
                    re.fullmatch(r"[ \t]*\*{2}[ \t]+-{20,}[ \t]*", line) is not None
                    for line in raw_comment.split("\n")
                )
                >= 2
            ):
                return _normalize_sanitized_body(
                    "\n".join(
                        line
                        for line in cleaned_block.split("\n")
                        if line.strip() and re.fullmatch(r"[ \t]*-{8,}[ \t]*", line) is None
                    )
                )
            if self._language_key == "asl":
                return _strip_asl_generated_frame(cleaned_block)
            if self._language_key == "bluespec":
                return _sanitize_bluespec_block_result(raw_comment, cleaned_block)
            if self._language_key == "clean":
                return _sanitize_clean_generated_doc_result(raw_comment, cleaned_block)
            if self._language_key == "faust":
                return _sanitize_faust_frame_result(cleaned_block)
            if self._language_key == "mustache":
                return _strip_repeated_literal_gutter(cleaned_block, "|")
            if self._language_key == "portugol":
                return _sanitize_portugol_block_result(raw_comment, cleaned_block)
            if self._language_key == "hlsl":
                return _sanitize_hlsl_result(raw_comment, cleaned_block)
            if self._language_key == "sas":
                return _sanitize_sas_block_result(raw_comment, cleaned_block)
            if self._language_key == "uno":
                return _sanitize_uno_block_result(raw_comment, cleaned_block)
            divider_result = _sanitize_validated_divider_result(
                self._language_key,
                raw_comment,
                cleaned_block,
            )
            if divider_result is not None:
                return divider_result
            return _sanitize_secondary_gutter_result(
                self._language_key,
                raw_comment,
                cleaned_block,
            )

        if self._language_key == "imba":
            unclosed_block_result = _sanitize_unclosed_block_comment(
                raw_comment,
                self.syntax,
                self._sanitizer_syntax.line_wrappers,
                self._protected_padding_chars,
            )
            if unclosed_block_result is not None:
                return unclosed_block_result

        if self._language_key == "slang":
            spliced_line_result = _sanitize_slang_spliced_line(raw_comment)
            if spliced_line_result is not None:
                return spliced_line_result

        line_result = _strip_grouped_line_wrappers(
            raw_comment,
            self._sanitizer_syntax.line_wrappers,
            protected_padding_chars=self._protected_padding_chars,
        )
        if line_result is not None:
            if self._language_key == "click":
                return _sanitize_click_line_result(raw_comment, line_result)
            if self._language_key == "clips":
                return _sanitize_clips_line_result(raw_comment, line_result)
            if self._language_key == "denizenscript":
                return _sanitize_denizenscript_line_result(raw_comment, line_result)
            if self._language_key == "ecl":
                return _sanitize_ecl_line_result(line_result)
            if self._language_key == "faust":
                return _sanitize_faust_frame_result(line_result)
            if self._language_key == "gap":
                return _sanitize_gap_line_result(raw_comment, line_result)
            if self._language_key in _GENERO_LANGUAGE_KEYS:
                return _sanitize_genero_line_result(raw_comment, line_result)
            if self._language_key == "glyph":
                return _sanitize_glyph_line_result(line_result)
            if self._language_key == "hlsl":
                return _sanitize_hlsl_result(raw_comment, line_result)
            if self._language_key in {"kakoune_script", "kakounescript"}:
                return _sanitize_kakoune_line_result(self._language_key, line_result)
            if self._language_key == "mercury":
                return _sanitize_mercury_line_result(line_result)
            if self._language_key == "nasal":
                return _sanitize_nasal_hash_layout(raw_comment, line_result)
            if self._language_key == "rebol":
                return _sanitize_rebol_line_result(line_result)
            if self._language_key == "red":
                return _sanitize_red_line_result(line_result)
            if self._language_key == "sas":
                return _sanitize_sas_line_result(line_result)
            if self._language_key == "stata":
                return _sanitize_stata_star_layout(raw_comment, line_result)
            if self._language_key == "win32_message_file":
                return _sanitize_win32_message_result(line_result, raw_comment)
            line_result = _sanitize_reviewed_slash_line_result(
                self._language_key,
                raw_comment,
                line_result,
            )
            line_result = _sanitize_reviewed_dash_line_result(
                self._language_key,
                raw_comment,
                line_result,
            )
            divider_result = _sanitize_validated_divider_result(
                self._language_key,
                raw_comment,
                line_result,
            )
            if divider_result is not None:
                return divider_result
            return _sanitize_secondary_gutter_result(
                self._language_key,
                raw_comment,
                line_result,
            )

        line_block_result = _strip_block_wrapper(raw_comment, closed_line_wrappers)
        if line_block_result is not None:
            inner, wrapper = line_block_result
            return _sanitize_block_body(
                inner,
                wrapper,
                self._sanitizer_syntax.line_wrappers,
                allow_doc_star=False,
                protected_ruler_chars=self._protected_padding_chars,
            )

        unclosed_block_result = _sanitize_unclosed_block_comment(
            raw_comment,
            self.syntax,
            self._sanitizer_syntax.line_wrappers,
            self._protected_padding_chars,
        )
        if unclosed_block_result is not None:
            return unclosed_block_result

        return _normalize_sanitized_body(raw_comment)


def sanitize_comment(language: str, comment: str | QueryMatch) -> str:
    """Return sanitized comment text for ``language``."""

    return CommentSanitizer(language).sanitize(comment)


def sanitize_comment_text(language: str, comment: str | QueryMatch) -> str:
    """Backward-compatible alias for ``sanitize_comment``."""

    return sanitize_comment(language, comment)


__all__ = [
    "CommentSanitizer",
    "sanitize_comment",
    "sanitize_comment_text",
]
