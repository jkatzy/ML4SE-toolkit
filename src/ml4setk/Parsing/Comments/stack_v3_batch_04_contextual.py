"""Contextual comment scanners for reviewed Stack v3 full batch 04."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator

_NEWLINES = "\r\n\v\f\u0085\u2028\u2029"
_KICKSTART_RAW_SECTIONS = frozenset(
    {
        "%anaconda",
        "%certificate",
        "%onerror",
        "%post",
        "%pre",
        "%traceback",
    }
)
_KICKSTART_COMMAND_DIRECTIVES = frozenset({"%include", "%ksappend"})
_JTE_LINE_DIRECTIVES = frozenset(
    {
        "contenttype",
        "import",
        "param",
        "template",
    }
)
_JCL_DATA_START = re.compile(
    r"^//[^*\s]\S*[ \t]+DD[ \t]+(?P<mode>\*|DATA)(?=[ \t,]|\Z)",
    re.IGNORECASE,
)
_JCL_DLM = re.compile(
    r"(?:^|,)[ \t]*DLM[ \t]*=[ \t]*(?:'(?P<quoted>[^']{1,2})'|(?P<bare>[^,\s]{1,2}))",
    re.IGNORECASE,
)


def _physical_lines(text: str) -> Iterator[tuple[int, int, int]]:
    """Yield content and next-line offsets without normalizing line endings."""

    start = 0
    while start < len(text):
        end = start
        while end < len(text) and text[end] not in _NEWLINES:
            end += 1
        next_start = end
        if next_start < len(text):
            if text[next_start : next_start + 2] == "\r\n":
                next_start += 2
            else:
                next_start += 1
        yield start, end, next_start
        start = next_start


def _line_end(text: str, start: int) -> int:
    end = start
    while end < len(text) and text[end] not in _NEWLINES:
        end += 1
    return end


def _skip_escaped_quote(text: str, start: int, quote: str) -> int:
    """Return just after a regular quoted literal, or EOF when incomplete."""

    index = start + 1
    while index < len(text):
        if text[index] == "\\":
            index = min(index + 2, len(text))
            continue
        if text[index] == quote:
            return index + 1
        index += 1
    return len(text)


def _nested_block_end(
    text: str, start: int, open_token: str = "/*", close_token: str = "*/"
) -> int | None:
    depth = 1
    index = start + len(open_token)
    while index < len(text):
        if text.startswith(open_token, index):
            depth += 1
            index += len(open_token)
            continue
        if text.startswith(close_token, index):
            depth -= 1
            index += len(close_token)
            if depth == 0:
                return index
            continue
        index += 1
    return None


def _kdl_string_end(text: str, start: int) -> int | None:
    """Return the end of a KDL v1/v2 quoted, multiline, or raw string."""

    if text.startswith('"""', start):
        close = text.find('"""', start + 3)
        return len(text) if close < 0 else close + 3
    if text[start] == '"':
        return _skip_escaped_quote(text, start, '"')

    marker_start = start
    if text[start] == "r":
        marker_start += 1
    if marker_start >= len(text) or text[marker_start] != "#":
        return None
    index = marker_start
    while index < len(text) and text[index] == "#":
        index += 1
    if index >= len(text) or text[index] != '"':
        return None
    hashes = text[marker_start:index]
    close_token = '"' + hashes
    close = text.find(close_token, index + 1)
    return len(text) if close < 0 else close + len(close_token)


def _kdl_balanced_end(text: str, start: int, opener: str, closer: str) -> int | None:
    depth = 1
    index = start + 1
    while index < len(text):
        string_end = _kdl_string_end(text, index)
        if string_end is not None:
            index = string_end
            continue
        if text.startswith("//", index):
            index = _line_end(text, index + 2)
            continue
        if text.startswith("/*", index):
            block_end = _nested_block_end(text, index)
            if block_end is None:
                return None
            index = block_end
            continue
        if text[index] == opener:
            depth += 1
        elif text[index] == closer:
            depth -= 1
            if depth == 0:
                return index + 1
        index += 1
    return None


def _skip_kdl_space(text: str, start: int) -> int | None:
    """Skip KDL whitespace and ordinary comments preceding a slashdash target."""

    index = start
    while index < len(text):
        if text[index].isspace():
            index += 1
            continue
        if text.startswith("//", index):
            index = _line_end(text, index + 2)
            continue
        if text.startswith("/*", index):
            block_end = _nested_block_end(text, index)
            if block_end is None:
                return None
            index = block_end
            continue
        break
    return index


def _kdl_node_position(text: str, slashdash_start: int) -> bool:
    index = slashdash_start - 1
    while index >= 0 and text[index] in " \t":
        index -= 1
    return index < 0 or text[index] in "\r\n\v\f\u0085\u2028\u2029;{}"


def _kdl_value_end(text: str, start: int) -> int | None:
    index = start
    if text[index] == "(":
        typed_end = _kdl_balanced_end(text, index, "(", ")")
        if typed_end is None:
            return None
        index = typed_end
        while index < len(text) and text[index] in " \t":
            index += 1
        if index == len(text):
            return None

    while index < len(text):
        string_end = _kdl_string_end(text, index)
        if string_end is not None:
            index = string_end
            continue
        if text[index] == "(":
            group_end = _kdl_balanced_end(text, index, "(", ")")
            if group_end is None:
                return None
            index = group_end
            continue
        if text.startswith(("//", "/*", "/-"), index):
            break
        if text[index].isspace() or text[index] in ";{}":
            break
        index += 1
    return index if index > start else None


def _kdl_node_end(text: str, start: int) -> int | None:
    index = start
    last_content = start
    while index < len(text):
        string_end = _kdl_string_end(text, index)
        if string_end is not None:
            index = string_end
            last_content = index
            continue
        if text.startswith("//", index):
            return max(last_content, _line_end(text, index + 2))
        if text.startswith("/*", index):
            block_end = _nested_block_end(text, index)
            if block_end is None:
                return None
            index = block_end
            last_content = index
            continue
        if text.startswith("/-", index):
            nested_end = _kdl_slashdash_end(text, index)
            if nested_end is None:
                return None
            index = nested_end
            last_content = index
            continue
        if text[index] == "{":
            child_end = _kdl_balanced_end(text, index, "{", "}")
            if child_end is None:
                return None
            index = child_end
            last_content = index
            continue
        if text[index] in _NEWLINES + ";" or text[index] == "}":
            break
        if not text[index].isspace():
            last_content = index + 1
        index += 1
    return last_content if last_content > start else None


def _kdl_slashdash_end(text: str, start: int) -> int | None:
    target_start = _skip_kdl_space(text, start + 2)
    if target_start is None or target_start >= len(text):
        return None
    if text.startswith("/-", target_start):
        return None
    if text.startswith("kdl-version", target_start) and (
        target_start + len("kdl-version") == len(text)
        or not text[target_start + len("kdl-version")].isalnum()
    ):
        return None
    if text[target_start] == "{":
        return _kdl_balanced_end(text, target_start, "{", "}")
    if _kdl_node_position(text, start):
        return _kdl_node_end(text, target_start)
    return _kdl_value_end(text, target_start)


def kdl_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return KDL v1/v2 line, nested-block, and slashdash comment ranges."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        string_end = _kdl_string_end(text, index)
        if string_end is not None:
            index = string_end
            continue
        if text.startswith("//", index):
            end = _line_end(text, index + 2)
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/*", index):
            end = _nested_block_end(text, index)
            if end is None:
                break
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("/-", index):
            end = _kdl_slashdash_end(text, index)
            if end is not None:
                ranges.append((index, end))
                index = end
                continue
            index += 2
            continue
        index += 1
    return tuple(ranges)


def _unquoted_hash(line: str, start: int = 0) -> int | None:
    quote: str | None = None
    escaped = False
    index = start
    while index < len(line):
        char = line[index]
        if quote is None:
            if char == "#":
                return index
            if char in {"'", '"', "`"}:
                quote = char
            index += 1
            continue
        if escaped:
            escaped = False
        elif char == "\\" and quote != "'":
            escaped = True
        elif char == quote:
            if index + 1 < len(line) and line[index + 1] == quote:
                index += 2
                continue
            quote = None
        index += 1
    return None if quote is None else -1


def ispc_ignored_ranges(text: str) -> list[tuple[int, int]]:
    """Return ISPC literals and block spans that can contain slash markers."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("//", index):
            index = _line_end(text, index + 2)
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            end = len(text) if close < 0 else close + 2
            ranges.append((index, end))
            index = end
            continue
        if text[index] not in {"'", '"'}:
            index += 1
            continue

        start = index
        quote = text[index]
        index += 1
        while index < len(text) and text[index] not in _NEWLINES:
            if text[index] == "\\":
                index = min(index + 2, len(text))
                continue
            if text[index] == quote:
                index += 1
                break
            index += 1
        ranges.append((start, index))
    return ranges


def kerboscript_literal_ranges(text: str) -> list[tuple[int, int]]:
    """Return KerboScript strings, including incomplete scanner tokens."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("//", index):
            index = _line_end(text, index + 2)
            continue
        if text[index] != '"':
            index += 1
            continue

        start = index
        index += 1
        while index < len(text) and text[index] not in _NEWLINES:
            if text[index] != '"':
                index += 1
                continue
            if index + 1 < len(text) and text[index + 1] == '"':
                index += 2
                continue
            index += 1
            break
        ranges.append((start, index))
    return ranges


def lean_ignored_ranges(text: str) -> list[tuple[int, int]]:
    """Return Lean literals and complete or incomplete nested comment spans."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("--", index):
            index = _line_end(text, index + 2)
            continue
        if text.startswith("/-", index):
            block_end = _nested_block_end(text, index, "/-", "-/")
            end = len(text) if block_end is None else block_end
            ranges.append((index, end))
            index = end
            continue
        if text[index] in {"'", '"'}:
            end = _skip_escaped_quote(text, index, text[index])
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return ranges


def kickstart_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return pykickstart 3.76 host comments outside all-lines sections."""

    ranges: list[tuple[int, int]] = []
    section = "command"
    for line_start, line_end, _ in _physical_lines(text):
        line = text[line_start:line_end]
        stripped = line.lstrip(" \t")
        control = stripped.split(None, 1)[0].lower() if stripped.startswith("%") else ""

        if section == "raw":
            if control == "%end":
                section = "command"
            continue
        if control:
            if control in _KICKSTART_RAW_SECTIONS:
                section = "raw"
            elif control in _KICKSTART_COMMAND_DIRECTIVES:
                section = "command"
            elif control == "%end":
                section = "command"
            else:
                section = "ordinary"
            continue
        if not stripped or stripped.lower().startswith("#platform="):
            continue
        if stripped.startswith("#"):
            marker = line_start + len(line) - len(stripped)
            ranges.append((marker, line_end))
            continue
        if section == "command":
            marker = _unquoted_hash(line)
            if marker is not None and marker >= 0:
                ranges.append((line_start + marker, line_end))
    return tuple(ranges)


def _java_balanced_end(text: str, start: int, opener: str, closer: str) -> int:
    depth = 1
    index = start + 1
    while index < len(text):
        if text[index] in {"'", '"'}:
            index = _skip_escaped_quote(text, index, text[index])
            continue
        if text.startswith("//", index):
            index = _line_end(text, index + 2)
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            index = len(text) if close < 0 else close + 2
            continue
        if text[index] == opener:
            depth += 1
        elif text[index] == closer:
            depth -= 1
            if depth == 0:
                return index + 1
        index += 1
    return len(text)


def java_template_engine_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return native JTE comments recognized in template text mode."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("<%--", index):
            close = text.find("--%>", index + 4)
            if close < 0:
                break
            end = close + 4
            ranges.append((index, end))
            index = end
            continue
        if text.startswith("${", index):
            index = _java_balanced_end(text, index + 1, "{", "}")
            continue
        raw_match = re.match(r"@raw\b", text[index:], re.IGNORECASE)
        if raw_match is not None:
            raw_end = re.search(r"@endraw\b", text[index + raw_match.end() :], re.IGNORECASE)
            if raw_end is None:
                break
            index += raw_match.end() + raw_end.end()
            continue
        directive = re.match(r"@([A-Za-z_][A-Za-z0-9_]*)", text[index:])
        if directive is not None:
            name = directive.group(1).lower()
            directive_end = index + directive.end()
            argument = directive_end
            while argument < len(text) and text[argument] in " \t":
                argument += 1
            if argument < len(text) and text[argument] == "(":
                index = _java_balanced_end(text, argument, "(", ")")
                continue
            if argument < len(text) and text[argument] == "{":
                index = _java_balanced_end(text, argument, "{", "}")
                continue
            if name in _JTE_LINE_DIRECTIVES:
                index = _line_end(text, directive_end)
                continue
        index += 1
    return tuple(ranges)


def _jcl_trailing_comment(line: str) -> tuple[int, int] | None:
    """Return a conservative base-JCL trailing comment field range."""

    statement = line[:71]
    if not statement.startswith("//") or statement.startswith("//*", 0):
        return None
    index = 2
    if index >= len(statement) or statement[index].isspace():
        return None
    while index < len(statement) and not statement[index].isspace():
        index += 1
    while index < len(statement) and statement[index] in " \t":
        index += 1
    while index < len(statement) and not statement[index].isspace():
        index += 1
    while index < len(statement) and statement[index] in " \t":
        index += 1
    parameter_start = index
    if parameter_start >= len(statement):
        return None

    quote = False
    depth = 0
    while index < len(statement):
        char = statement[index]
        if quote:
            if char == "'":
                if index + 1 < len(statement) and statement[index + 1] == "'":
                    index += 2
                    continue
                quote = False
            index += 1
            continue
        if char == "'":
            quote = True
            index += 1
            continue
        if char == "(":
            depth += 1
        elif char == ")" and depth:
            depth -= 1
        elif char in " \t" and depth == 0:
            separator = index
            while index < len(statement) and statement[index] in " \t":
                index += 1
            if index < len(statement):
                parameter = statement[parameter_start:separator]
                if "=" in parameter or parameter.upper() in {"*", "DATA"}:
                    return index, len(statement.rstrip())
            return None
        index += 1
    return None


def jcl_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return base z/OS JCL comment statements and trailing comment fields."""

    ranges: list[tuple[int, int]] = []
    data_mode: str | None = None
    data_delimiter: str | None = None
    for line_start, line_end, _ in _physical_lines(text):
        line = text[line_start:line_end]
        if data_mode is not None:
            if data_delimiter is not None:
                if line.startswith(data_delimiter):
                    data_mode = None
                    data_delimiter = None
                continue
            if line.startswith("/*"):
                data_mode = None
                continue
            if data_mode == "star" and line.startswith("//"):
                data_mode = None
            else:
                continue

        if line.startswith("//*"):
            ranges.append((line_start, line_end))
            continue
        trailing = _jcl_trailing_comment(line)
        if trailing is not None:
            ranges.append((line_start + trailing[0], line_start + trailing[1]))

        data_start = _JCL_DATA_START.match(line[:71])
        if data_start is None:
            continue
        data_mode = "star" if data_start.group("mode") == "*" else "data"
        delimiter_match = _JCL_DLM.search(line[data_start.end() : 71])
        if delimiter_match is not None:
            data_delimiter = delimiter_match.group("quoted") or delimiter_match.group("bare")
    return tuple(ranges)


def _just_recipe_header(code: str) -> bool:
    if not code or code[0].isspace():
        return False
    lowered = code.lstrip().lower()
    if lowered.startswith(("alias ", "export ", "set ")):
        return False

    quote: str | None = None
    escaped = False
    for index, char in enumerate(code):
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\" and quote != "'":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"', "`"}:
            quote = char
            continue
        if char == ":" and code[index + 1 : index + 2] != "=":
            return True
    return False


def just_comment_ranges(text: str) -> tuple[tuple[int, int], ...]:
    """Return native Just comments while preserving recipe-body text."""

    ranges: list[tuple[int, int]] = []
    in_recipe_body = False
    for line_start, line_end, _ in _physical_lines(text):
        line = text[line_start:line_end]
        if in_recipe_body:
            if not line or line[0].isspace():
                continue
            in_recipe_body = False

        marker = _unquoted_hash(line)
        if marker == -1:
            continue
        code = line if marker is None else line[:marker]
        if marker is not None:
            ranges.append((line_start + marker, line_end))
        if _just_recipe_header(code.rstrip()):
            in_recipe_body = True
    return tuple(ranges)


def koka_literal_ranges(text: str) -> list[tuple[int, int]]:
    """Return Koka ordinary, character, and hash-delimited raw literals."""

    ranges: list[tuple[int, int]] = []
    index = 0
    while index < len(text):
        if text.startswith("//", index):
            index = _line_end(text, index + 2)
            continue
        if text.startswith("/*", index):
            block_end = _nested_block_end(text, index)
            if block_end is None:
                ranges.append((index, len(text)))
                break
            index = block_end
            continue
        if text[index] == "r":
            hashes_end = index + 1
            while hashes_end < len(text) and text[hashes_end] == "#":
                hashes_end += 1
            if hashes_end > index + 1 and hashes_end < len(text) and text[hashes_end] == '"':
                hashes = text[index + 1 : hashes_end]
                close_token = '"' + hashes
                close = text.find(close_token, hashes_end + 1)
                end = len(text) if close < 0 else close + len(close_token)
                ranges.append((index, end))
                index = end
                continue
        if text[index] in {"'", '"'}:
            end = _skip_escaped_quote(text, index, text[index])
            ranges.append((index, end))
            index = end
            continue
        index += 1
    return ranges


STACK_V3_BATCH_04_CONTEXTUAL_EXTRACTORS: dict[str, Callable[[str], tuple[tuple[int, int], ...]]] = {
    "java_template_engine_comments": java_template_engine_comment_ranges,
    "jcl_comments": jcl_comment_ranges,
    "just_comments": just_comment_ranges,
    "kdl_comments": kdl_comment_ranges,
    "kickstart_comments": kickstart_comment_ranges,
}

__all__ = [
    "STACK_V3_BATCH_04_CONTEXTUAL_EXTRACTORS",
    "java_template_engine_comment_ranges",
    "jcl_comment_ranges",
    "just_comment_ranges",
    "kdl_comment_ranges",
    "kerboscript_literal_ranges",
    "kickstart_comment_ranges",
    "koka_literal_ranges",
    "ispc_ignored_ranges",
    "lean_ignored_ranges",
]
