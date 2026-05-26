"""Legacy tuple-based comment extraction helpers.

New parser work should use ``ml4setk.Parsing.Comments.CommentQuery`` and the
registry-backed ``QueryMatch`` contract. This module preserves the older
``((start, end), text, kind)`` API for datasets and callers that still depend on
it. Keep language-specific syntax changes aligned with the registry whenever a
compatibility extractor must be updated here.
"""

import ast
import json
from importlib import resources
from typing import Iterable, List, Tuple

import regex as re

CommentSpan = Tuple[Tuple[int, int], str, str]  # ((start, end), text, kind)


def _regex_matches(
    content: str, patterns: Iterable[str], comment_type: str = "block"
) -> List[CommentSpan]:
    """Return all regex matches for the provided patterns with spans and type.

    Args:
        content: Source text to scan.
        patterns: Regex patterns that identify one comment family.
        comment_type: Output kind label, usually ``line`` or ``block``.

    Returns:
        Comment tuples containing the source span, raw text, and kind label.
    """
    matches: List[CommentSpan] = []
    for pattern in patterns:
        for m in re.finditer(pattern, content, flags=re.MULTILINE):
            matches.append(((m.start(), m.end()), m.group(), comment_type))
    return matches


def _regex_line_matches(content: str, patterns: Iterable[str]) -> List[CommentSpan]:
    """
    Return merged blocks of consecutive single-line comments.

    Two comments are merged when they are separated only by optional whitespace
    and a single newline (i.e., they appear on consecutive lines).
    """
    dedup: dict[Tuple[int, int], CommentSpan] = {}
    for pattern in patterns:
        for m in re.finditer(pattern, content, flags=re.MULTILINE):
            span = (m.start(), m.end())
            dedup.setdefault(span, (span, m.group(), "line"))

    raw: List[CommentSpan] = sorted(dedup.values(), key=lambda c: c[0][0])
    if not raw:
        return []

    merged: List[CommentSpan] = []
    current_start, current_end = raw[0][0]

    for (start, end), _text, _kind in raw[1:]:
        separator = content[current_end:start]
        if re.fullmatch(r"[ \t]*\r?\n[ \t]*", separator):
            # Extend current block to include the next line comment
            current_end = end
        else:
            merged.append(
                ((current_start, current_end), content[current_start:current_end], "line")
            )
            current_start, current_end = start, end

    merged.append(((current_start, current_end), content[current_start:current_end], "line"))
    return merged


def _sorted_spans(*spans_lists: List[CommentSpan]) -> List[CommentSpan]:
    merged: List[CommentSpan] = []
    for spans in spans_lists:
        merged.extend(spans)
    return sorted(merged, key=lambda s: s[0][0])


def _first_code_index(content: str) -> int:
    """
    Return the index of the first non-preprocessor, non-whitespace character.

    Preprocessor lines (starting with '#', ignoring leading whitespace) are
    skipped so that an opening comment following them is still considered.
    """
    offset = 0
    for line in content.splitlines(keepends=True):
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            offset += len(line)
            continue
        return offset + (len(line) - len(stripped))
    return len(content)


def _is_preamble(text: str) -> bool:
    """Return True if the text contains only whitespace or preprocessor lines."""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        return False
    return True


def extract_nested(delim_start: str, delim_end: str, content: str) -> List[CommentSpan]:
    """
    Return top-level nested comment blocks (including delimiters).

    This preserves nesting by only emitting the outermost block when delimiters
    can be nested.
    """
    results: List[CommentSpan] = []
    stack: List[int] = []
    open_len, close_len = len(delim_start), len(delim_end)
    i = 0

    while i < len(content):
        if content.startswith(delim_start, i):
            stack.append(i)
            i += open_len
            continue

        if content.startswith(delim_end, i) and stack:
            start = stack.pop()
            i += close_len
            if not stack:
                results.append(((start, i), content[start:i], "block"))
            continue

        i += 1

    return results


def extract_comments_java(content):
    blocks = _regex_matches(content, [r"\/\*[\S\s]*?\*\/"])
    lines = _regex_line_matches(content, [r"/{2}.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_python(content):
    blocks = _regex_matches(content, [r"\"{3}([\S\s]*?)\"{3}"])
    lines = _regex_line_matches(content, [r"#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_hash(content):
    return _regex_line_matches(content, [r"#.*"])


def extract_comments_hash_cblock(content):
    blocks = _regex_matches(content, [r"\/\*[\S\s]*?\*\/"])
    lines = _regex_line_matches(content, [r"#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_hash_block(content):
    blocks = _regex_matches(content, [r"#\[[\s\S]*?\]#"])
    lines = _regex_line_matches(content, [r"^(?!\s*#\[)\s*#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_erlang(content):
    return _regex_line_matches(content, [r"%.*"])


def extract_comments_julia(content):
    blocks = _regex_matches(content, [r"#=([\S\s]*?)=#"])
    lines = _regex_line_matches(content, [r"#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_lisp(content):
    return _regex_line_matches(content, [r";.*"])


def extract_comments_fortran(content):
    return _regex_line_matches(content, [r"!.*"])


def extract_comments_cobol(content):
    blocks = _regex_matches(content, [r"(^|\n).{6}(\*|/).*"])
    lines = _regex_line_matches(content, [r"\*>.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_html(content):
    return _regex_matches(content, [r"<!--([\S\s]*?)-->"])


def extract_comments_coldfusion(content):
    return extract_nested("<!---", "--->", content)


def extract_comments_antlers(content):
    return _regex_matches(content, [r"\{\{#[\S\s]*?#\}\}"])


def extract_comments_asciidoc(content):
    blocks = _regex_matches(content, [r"^\s*////[\s\S]*?^\s*////"])
    lines = _regex_line_matches(content, [r"^(?!\s*////)\s*//.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_alloy(content):
    blocks = _regex_matches(content, [r"\/\*[\S\s]*?\*\/"])
    lines = _regex_line_matches(content, [r"//.*", r"--.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_apl(content):
    return _regex_line_matches(content, ["\u235D.*"])


def extract_comments_matlab(content):
    blocks = _regex_matches(content, [r"%{([\S\s]*?)%}"])
    lines = _regex_line_matches(content, [r"^(?!\s*%\{)(?!\s*%\})\s*%.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_webassembly(content):
    blocks = _regex_matches(content, [r"\(;([\S\s]*?);\)"])
    lines = _regex_line_matches(content, [r";;.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_assembly(content):
    return _regex_line_matches(content, [r";.*"])


def extract_comments_semicolon(content):
    return _regex_line_matches(content, [r";.*"])


def extract_comments_semicolon_cstyle(content):
    blocks = _regex_matches(content, [r"\/\*[\S\s]*?\*\/"])
    lines = _regex_line_matches(content, [r";.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_ini(content):
    return _regex_line_matches(content, [r"^\s*[#;].*"])


def extract_comments_twig(content):
    return _regex_matches(content, [r"\{#[\s\S]*?#\}"])


def extract_comments_freemarker(content):
    return _regex_matches(content, [r"<#--[\s\S]*?-->"])


def extract_comments_handlebars(content):
    blocks = _regex_matches(content, [r"\{\{!--[\s\S]*?--\}\}", r"\{\{![\s\S]*?\}\}"])
    return _sorted_spans(blocks)


def extract_comments_smarty(content):
    return _regex_matches(content, [r"\{\*[\s\S]*?\*\}"])


def extract_comments_blitzmax(content):
    blocks = _regex_matches(content, [r"(?ims)^[ \t]*Rem\b[\S\s]*?^[ \t]*End[ \t]*Rem\b"])
    lines = _regex_line_matches(content, [r"'.*", r"(?i)^[ \t]*rem\b.+"],)
    return _sorted_spans(blocks, lines)


def extract_comments_jsp(content):
    return _regex_matches(content, [r"<%--[\s\S]*?--%>"])


def extract_comments_liquid(content):
    return _regex_matches(content, [r"\{%\s*comment\s*%\}[\s\S]*?\{%\s*endcomment\s*%\}"])


def extract_comments_django(content):
    blocks = _regex_matches(
        content,
        [r"\{#[\s\S]*?#\}", r"\{%\s*comment\s*%\}[\s\S]*?\{%\s*endcomment\s*%\}"],
    )
    return _sorted_spans(blocks)


def extract_comments_haml(content):
    blocks = _regex_matches(content, [r"(?m)^([ \t]*)/[^\n]*(?:\n\1[ \t]+.*)*"])
    lines = _regex_line_matches(content, [r"(?m)^[ \t]*-#.*$"])
    return _sorted_spans(blocks, lines)


def extract_comments_mako(content):
    blocks = _regex_matches(content, [r"<%doc>[\s\S]*?</%doc>"])
    lines = _regex_line_matches(content, [r"##.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_rhtml(content):
    return _sorted_spans(extract_comments_ejs(content), extract_comments_html(content))


def extract_comments_ruby(content):
    blocks = _regex_matches(content, [r"=begin([\S\s]*?)=end"])
    lines = _regex_line_matches(content, [r"#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_abap(content):
    return _regex_line_matches(content, [r'^\*.*', r'".*'])


def extract_comments_mathematica(content):
    return extract_nested("(*", "*)", content)


def extract_comments_ada(content):
    return _regex_line_matches(content, [r"--.*"])


def extract_comments_applescript(content):
    blocks = extract_nested("(*", "*)", content)
    lines = _regex_line_matches(content, [r"--.*", r"#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_agda(content):
    blocks = extract_nested("{-", "-}", content)
    lines = _regex_line_matches(content, [r"--.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_coq(content):
    return extract_nested("(*", "*)", content)


def extract_comments_fsharp(content):
    blocks = extract_nested("(*", "*)", content)
    lines = _regex_line_matches(content, [r"\/\/.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_lean(content):
    blocks = extract_nested("/-", "-/", content)
    lines = _regex_line_matches(content, [r"--.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_star_nested(content):
    return extract_nested("(*", "*)", content)


def extract_comments_d(content):
    blocks = _regex_matches(content, [r"\/\*\*[\S\s]*?\*\/", r"\/\+\+[\S\s]*?\+\/"])
    lines = _regex_line_matches(content, [r"\/\/\/.*", r"//.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_c_nested(content):
    blocks = extract_nested("/*", "*/", content)
    lines = _regex_line_matches(content, [r"//.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_css(content):
    return _regex_matches(content, [r"\/\*[\S\s]*?\*\/"])


def extract_comments_forth(content):
    blocks = _regex_matches(content, [r"\(\s[\s\S]*?\s\)"])
    lines = _regex_line_matches(content, [r"\\\s.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_lua(content):
    blocks = _regex_matches(content, [r"--\[(=*)\[[\s\S]*?\]\1\]"])
    lines = _regex_line_matches(content, [r"--(?!\[).*"])
    return _sorted_spans(blocks, lines)


def extract_comments_basic(content):
    lines = _regex_line_matches(content, [r"'.*", r"(?i)^\s*rem\b.*"])
    return _sorted_spans(lines)


def extract_comments_gams(content):
    blocks = _sorted_spans(
        _regex_matches(content, [r"\/\*[\S\s]*?\*\/"]),
        _regex_matches(content, [r"(?im)^\$ontext\b[\S\s]*?^\$offtext\b[^\n]*"]),
    )
    lines = _regex_line_matches(content, [r"(?m)^\*.*$", r"!!.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_gcode(content):
    blocks = _regex_matches(content, [r"\([\S\s]*?\)"])
    lines = _regex_line_matches(content, [r";.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_percent_cstyle(content):
    blocks = _regex_matches(content, [r"\/\*[\s\S]*?\*\/"])
    lines = _regex_line_matches(content, [r"%.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_none(content):
    return []


def extract_comments_batchfile(content):
    lines = _regex_line_matches(content, [r"::.*", r"(?i)^\s*rem\b.*"])
    return _sorted_spans(lines)


def extract_comments_smalltalk(content):
    return _regex_matches(content, [r'"[\s\S]*?"'])


def extract_comments_newlisp(content):
    return _regex_line_matches(content, [r";.*", r"#.*"])


def extract_comments_lolcode(content):
    blocks = _regex_matches(content, [r"(?im)^[ \t]*OBTW\b[\S\s]*?^[ \t]*TLDR\b[^\n]*"])
    lines = _regex_line_matches(content, [r"(?m)^[ \t]*BTW\b.*$"])
    return _sorted_spans(blocks, lines)


def extract_comments_inform7(content):
    return _regex_matches(content, [r"\[[\s\S]*?\]"])


def extract_comments_j(content):
    return _regex_line_matches(content, [r"(?m)(?<!\S)NB\..*$"])


def extract_comments_autoit(content):
    blocks = _regex_matches(
        content,
        [r"(?i)#(?:comments-start|cs)\b[\s\S]*?^\s*#(?:comments-end|ce)\b.*"],
    )
    lines = _regex_line_matches(content, [r";.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_perl(content):
    blocks = _regex_matches(content, [r"=[\s\S]*?=cut"])
    lines = _regex_line_matches(content, [r"#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_powershell(content):
    blocks = _regex_matches(content, [r"<#[\s\S]*?#>"])
    lines = _regex_line_matches(content, [r"^(?!\s*<#)\s*#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_coffeescript(content):
    blocks = _regex_matches(content, [r"#{3}[\s\S]*?#{3}"])
    lines = _regex_line_matches(content, [r"^(?!\s*###)\s*#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_openedge_abl(content):
    blocks = extract_nested("/*", "*/", content)
    lines = _regex_line_matches(content, [r"(?m)(?<!\S)//.*$"])
    return _sorted_spans(blocks, lines)


def extract_comments_livescript(content):
    blocks = _sorted_spans(
        _regex_matches(content, [r"\/\*[\S\s]*?\*\/"]),
        _regex_matches(content, [r"#{3}[\s\S]*?#{3}"]),
    )
    lines = _regex_line_matches(content, [r"//.*", r"^(?!\s*###)\s*#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_prolog(content):
    blocks = _regex_matches(content, [r"\/\*[\s\S]*?\*\/"])
    lines = _regex_line_matches(content, [r"%.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_rdoc(content):
    blocks = _sorted_spans(
        _regex_matches(content, [r"=begin\b[\s\S]*?=end\b"]),
        _regex_matches(content, [r"\/\*[\S\s]*?\*\/"]),
    )
    lines = _regex_line_matches(content, [r"#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_sas(content):
    blocks = _regex_matches(content, [r"\/\*[\s\S]*?\*\/"])
    lines = _regex_line_matches(content, [r"^\s*\*[^;]*;"])
    return _sorted_spans(blocks, lines)


def extract_comments_stata(content):
    blocks = _regex_matches(content, [r"\/\*[\s\S]*?\*\/"])
    lines = _regex_line_matches(content, [r"^\*.*", r"//.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_raku(content):
    blocks = _regex_matches(
        content,
        [r"#'\([\s\S]*?\)", r"#'\{[\s\S]*?\}", r"#'\[[\s\S]*?\]", r"#'\<[\s\S]*?\>"],
    )
    lines = _regex_line_matches(content, [r"^(?!\s*#')\s*#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_sql(content):
    blocks = _regex_matches(content, [r"\/\*[\S\s]*?\*\/"])
    lines = _regex_line_matches(content, [r"--.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_haskell(content):
    blocks = extract_nested("{-", "-}", content)
    lines = _regex_line_matches(content, [r"--.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_jsonnet(content):
    blocks = _regex_matches(content, [r"\/\*[\S\s]*?\*\/"])
    lines = _regex_line_matches(content, [r"//.*", r"#.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_dash(content):
    return _regex_line_matches(content, [r"--.*"])


def extract_comments_dash_cstyle(content):
    blocks = _regex_matches(content, [r"\/\*[\S\s]*?\*\/"])
    lines = _regex_line_matches(content, [r"--.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_bang(content):
    return _regex_line_matches(content, [r"!.*"])


def extract_comments_slash_line(content):
    return _regex_line_matches(content, [r"//.*"])


def extract_comments_percent(content):
    return _regex_line_matches(content, [r"%.*"])


def extract_comments_hash_pipe(content):
    blocks = extract_nested("#|", "|#", content)
    lines = _regex_line_matches(content, [r";.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_dash_star_nested(content):
    blocks = extract_nested("(*", "*)", content)
    lines = _regex_line_matches(content, [r"--.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_ejs(content):
    return _regex_matches(content, [r"<%#[\S\s]*?%>"])


def extract_comments_pascal(content):
    blocks = _sorted_spans(
        _regex_matches(content, [r"\{[\S\s]*?\}"]),
        _regex_matches(content, [r"\(\*[\S\s]*?\*\)"]),
    )
    lines = _regex_line_matches(content, [r"//.*"])
    return _sorted_spans(blocks, lines)


def extract_comments_viml(content):
    return _regex_line_matches(content, [r'^\s*".*'])


def extract_comments_m4(content):
    return _regex_line_matches(content, [r"(?i)^[ \t]*dnl\b.*"])


def extract_comments_org(content):
    blocks = _regex_matches(
        content, [r"(?ims)^[ \t]*#\+BEGIN_COMMENT\b[\S\s]*?^[ \t]*#\+END_COMMENT\b"]
    )
    lines = _regex_line_matches(content, [r"(?m)^[ \t]*#(?!\+).*$"])
    return _sorted_spans(blocks, lines)


def extract_comments_restructuredtext(content):
    return _regex_matches(content, [r"(?m)^\.\.\s.*(?:\n[ \t]+.*)*"])


def extract_comments_slim(content):
    return _regex_matches(content, [r"(?m)^([ \t]*)/!?[^\n]*(?:\n\1[ \t]+.*)*"])


def extract_comments_xquery(content):
    return extract_nested("(:", ":)", content)


def ending_to_langs(ending):
    """Return language names associated with one file extension.

    Args:
        ending: File extension with or without a leading dot.

    Returns:
        Language names from ``langs_extension.json`` that declare the extension.
    """

    ending = "." + ending.lower().lstrip(".")
    langs = []
    try:
        data_path = resources.files(__package__).joinpath("langs_extension.json")
        with data_path.open("rb") as infile:
            ending_map = json.load(infile)
    except FileNotFoundError:
        # Fallback for running from repo root without installation
        with open("./langs_extension.json", "rb") as infile:
            ending_map = json.load(infile)
    for row in ending_map:
        if "extensions" in row.keys() and ending in row["extensions"]:
            langs.append(row["name"])
    return langs


def get_langs(entry):
    """Infer candidate language names from a dataset row.

    Args:
        entry: Dataset record from The Stack, GitHubCode, RedPajama,
            CodeClippy, or a compatible source that exposes a file path field.

    Returns:
        Candidate language names inferred from the file extension.
    """
    # The Stack V2, GithubCode, codeparrot
    if "path" in entry.keys():
        path = entry["path"]
    # The Stack v1
    elif "max_stars_repo_path" in entry.keys():
        path = entry["max_stars_repo_path"]
    # Red pajama
    elif "meta" in entry.keys():
        meta_data = entry["meta"]
        meta_data = ast.literal_eval(meta_data)
        path = meta_data["path"]
    # CodeClippy
    elif "file_name" in entry.keys():
        path = entry["file_name"]
    elif "file_path" in entry.keys():
        path = entry["file_path"]
    file_ending = path.split(".")[-1]
    langs = ending_to_langs(file_ending)
    return langs


_LANG_EXTRACTORS = {
    # C-style block + line
    "java": extract_comments_java,
    "ags script": extract_comments_java,
    "actionscript": extract_comments_java,
    "arduino": extract_comments_java,
    "aspectj": extract_comments_java,
    "avro idl": extract_comments_java,
    "bluespec": extract_comments_java,
    "c": extract_comments_java,
    "ceylon": extract_comments_java,
    "chapel": extract_comments_java,
    "chuck": extract_comments_java,
    "cpp": extract_comments_java,
    "c++": extract_comments_java,
    "csharp": extract_comments_java,
    "c#": extract_comments_java,
    "cycript": extract_comments_java,
    "dtrace": extract_comments_java,
    "ecl": extract_comments_java,
    "fantom": extract_comments_java,
    "game maker language": extract_comments_java,
    "glsl": extract_comments_java,
    "gosu": extract_comments_java,
    "gradle": extract_comments_java,
    "haxe": extract_comments_java,
    "hlsl": extract_comments_java,
    "hyphy": extract_comments_java,
    "idl": extract_comments_java,
    "linux kernel module": extract_comments_java,
    "javascript": extract_comments_java,
    "json5": extract_comments_java,
    "jsx": extract_comments_java,
    "modelica": extract_comments_java,
    "m": extract_comments_java,
    "metal": extract_comments_java,
    "nesc": extract_comments_java,
    "objective-j": extract_comments_java,
    "objective-c++": extract_comments_java,
    "typescript": extract_comments_java,
    "objective-c": extract_comments_java,
    "objectivec": extract_comments_java,
    "go": extract_comments_java,
    "kotlin": extract_comments_java,
    "opencl": extract_comments_java,
    "openscad": extract_comments_java,
    "pawn": extract_comments_java,
    "pike": extract_comments_java,
    "protocol buffer": extract_comments_java,
    "qml": extract_comments_java,
    "renderscript": extract_comments_java,
    "scss": extract_comments_java,
    "sass": extract_comments_java,
    "sourcepawn": extract_comments_java,
    "squirrel": extract_comments_java,
    "vue": extract_comments_java,
    "scala": extract_comments_java,
    "dart": extract_comments_java,
    "rust": extract_comments_java,
    "hack": extract_comments_java,
    "less": extract_comments_java,
    "lsl": extract_comments_java,
    "groovy": extract_comments_java,
    "processing": extract_comments_java,
    "apex": extract_comments_java,
    "cuda": extract_comments_java,
    "scilab": extract_comments_java,
    "antlr": extract_comments_java,
    "swift": extract_comments_java,
    "php": extract_comments_java,
    "systemverilog": extract_comments_java,
    "tea": extract_comments_java,
    "unrealscript": extract_comments_java,
    "unified parallel c": extract_comments_java,
    "uno": extract_comments_java,
    "vala": extract_comments_java,
    "verilog": extract_comments_java,
    "webidl": extract_comments_java,
    "xc": extract_comments_java,
    "xtend": extract_comments_java,
    "yacc": extract_comments_java,
    "yang": extract_comments_java,
    # Python-style
    "python": extract_comments_python,
    "cython": extract_comments_python,
    "r": extract_comments_python,
    "elixir": extract_comments_python,
    "nix": extract_comments_python,
    "starlark": extract_comments_python,
    "graphql": extract_comments_python,
    "crystal": extract_comments_python,
    # Hash line-only
    "apacheconf": extract_comments_hash,
    "awk": extract_comments_hash,
    "bitbake": extract_comments_hash,
    "bro": extract_comments_hash,
    "cap'n proto": extract_comments_hash,
    "click": extract_comments_hash,
    "cmake": extract_comments_hash,
    "cucumber": extract_comments_hash,
    "dockerfile": extract_comments_hash,
    "gap": extract_comments_hash,
    "gdscript": extract_comments_hash,
    "gentoo ebuild": extract_comments_hash,
    "gentoo eclass": extract_comments_hash,
    "gettext catalog": extract_comments_hash,
    "gnuplot": extract_comments_hash,
    "golo": extract_comments_hash,
    "graph modeling language": extract_comments_hash,
    "limbo": extract_comments_hash,
    "makefile": extract_comments_hash,
    "monkey": extract_comments_hash,
    "nginx": extract_comments_hash,
    "nit": extract_comments_hash,
    "ninja": extract_comments_hash,
    "puppet": extract_comments_hash,
    "qmake": extract_comments_hash,
    "robotframework": extract_comments_hash,
    "raml": extract_comments_hash,
    "saltstack": extract_comments_hash,
    "shell": extract_comments_hash,
    "slash": extract_comments_hash,
    "sparql": extract_comments_hash,
    "tcl": extract_comments_hash,
    "tcsh": extract_comments_hash,
    "toml": extract_comments_hash,
    "turtle": extract_comments_hash,
    "unity3d asset": extract_comments_hash,
    "yaml": extract_comments_hash,
    "desktop": extract_comments_hash,
    "fish": extract_comments_hash,
    "lookml": extract_comments_hash,
    "ren'py": extract_comments_hash,
    "sage": extract_comments_hash,
    "smali": extract_comments_hash,
    "zimpl": extract_comments_hash,
    # Hash line + block
    "ampl": extract_comments_hash_cblock,
    "nimrod": extract_comments_hash_block,
    # INI-style
    "ini": extract_comments_ini,
    "nsis": extract_comments_ini,
    # Markup-style blocks
    "ant build system": extract_comments_html,
    "antlers": extract_comments_antlers,
    "coldfusion": extract_comments_coldfusion,
    "coldfusion cfc": extract_comments_coldfusion,
    "freemarker": extract_comments_freemarker,
    "genshi": extract_comments_html,
    "groovy server pages": extract_comments_jsp,
    "haml": extract_comments_haml,
    "html+django": extract_comments_django,
    "html": extract_comments_html,
    "http": extract_comments_none,
    "jupyter notebook": extract_comments_none,
    "java server pages": extract_comments_jsp,
    "json": extract_comments_none,
    "jsonld": extract_comments_none,
    "latte": extract_comments_smarty,
    "liquid": extract_comments_liquid,
    "markdown": extract_comments_html,
    "mediawiki": extract_comments_html,
    "mako": extract_comments_mako,
    "nunjucks": extract_comments_twig,
    "rmarkdown": extract_comments_html,
    "rhtml": extract_comments_rhtml,
    "smarty": extract_comments_smarty,
    "svg": extract_comments_html,
    "twig": extract_comments_twig,
    "xml": extract_comments_html,
    "xproc": extract_comments_html,
    "xslt": extract_comments_html,
    # Semicolon-style
    "clojure": extract_comments_semicolon,
    "arc": extract_comments_semicolon,
    "dns zone": extract_comments_semicolon,
    "edn": extract_comments_semicolon,
    "hy": extract_comments_semicolon,
    "jasmin": extract_comments_semicolon,
    "krl": extract_comments_semicolon,
    "lfe": extract_comments_semicolon,
    "llvm": extract_comments_semicolon,
    "purebasic": extract_comments_semicolon,
    "red": extract_comments_semicolon,
    "redcode": extract_comments_semicolon,
    "rebol": extract_comments_semicolon,
    "smt": extract_comments_semicolon,
    # Haskell-style nested blocks
    "c2hs haskell": extract_comments_haskell,
    "frege": extract_comments_haskell,
    "grammatical framework": extract_comments_haskell,
    "haskell": extract_comments_haskell,
    "idris": extract_comments_haskell,
    "lean": extract_comments_lean,
    "literate haskell": extract_comments_haskell,
    "purescript": extract_comments_haskell,
    # Mixed slash/hash styles
    "graphviz (dot)": extract_comments_jsonnet,
    "hcl": extract_comments_jsonnet,
    "thrift": extract_comments_jsonnet,
    # Dash, bang, slash, percent, and template-specific helpers
    "abap": extract_comments_abap,
    "apl": extract_comments_apl,
    "applescript": extract_comments_applescript,
    "asciidoc": extract_comments_asciidoc,
    "clarion": extract_comments_bang,
    "autohotkey": extract_comments_semicolon_cstyle,
    "autoit": extract_comments_autoit,
    "batchfile": extract_comments_batchfile,
    "brightscript": extract_comments_basic,
    "coffeescript": extract_comments_coffeescript,
    "emberscript": extract_comments_coffeescript,
    "css": extract_comments_css,
    "digital command language": extract_comments_bang,
    "eiffel": extract_comments_dash,
    "ejs": extract_comments_ejs,
    "factor": extract_comments_bang,
    "grace": extract_comments_slash_line,
    "html+eex": extract_comments_ejs,
    "html+erb": extract_comments_ejs,
    "igor pro": extract_comments_slash_line,
    "inno setup": extract_comments_basic,
    "inform 7": extract_comments_inform7,
    "plpgsql": extract_comments_sql,
    "plsql": extract_comments_sql,
    "powershell": extract_comments_powershell,
    "postscript": extract_comments_percent,
    "maxscript": extract_comments_dash_cstyle,
    "pascal": extract_comments_pascal,
    "tex": extract_comments_percent,
    "vhdl": extract_comments_dash,
    "viml": extract_comments_viml,
    "visual basic": extract_comments_basic,
    "realbasic": extract_comments_basic,
    "xojo": extract_comments_basic,
    # Others
    "ada": extract_comments_ada,
    "agda": extract_comments_agda,
    "alloy": extract_comments_alloy,
    "elm": extract_comments_agda,
    "assembly": extract_comments_assembly,
    "ats": extract_comments_fsharp,
    "augeas": extract_comments_star_nested,
    "common lisp": extract_comments_hash_pipe,
    "brainfuck": extract_comments_none,
    "netlogo": extract_comments_assembly,
    "scheme": extract_comments_assembly,
    "clips": extract_comments_semicolon_cstyle,
    "cobol": extract_comments_cobol,
    "coq": extract_comments_coq,
    "cool": extract_comments_dash_star_nested,
    "ocaml": extract_comments_coq,
    "d": extract_comments_d,
    "dm": extract_comments_c_nested,
    "dylan": extract_comments_c_nested,
    "emacs lisp": extract_comments_hash_pipe,
    "ec": extract_comments_java,
    "eclipse": extract_comments_percent_cstyle,
    "erlang": extract_comments_erlang,
    "f#": extract_comments_fsharp,
    "forth": extract_comments_forth,
    "fortran": extract_comments_fortran,
    "g-code": extract_comments_gcode,
    "gams": extract_comments_gams,
    "isabelle": extract_comments_star_nested,
    "jflex": extract_comments_c_nested,
    "j": extract_comments_j,
    "julia": extract_comments_julia,
    "harbour": extract_comments_java,
    "io": extract_comments_java,
    "lasso": extract_comments_java,
    "lex": extract_comments_css,
    "lilypond": extract_comments_matlab,
    "lisp": extract_comments_lisp,
    "livescript": extract_comments_livescript,
    "lolcode": extract_comments_lolcode,
    "logtalk": extract_comments_prolog,
    "linker script": extract_comments_hash_cblock,
    "logos": extract_comments_java,
    "max": extract_comments_java,
    "mercury": extract_comments_percent_cstyle,
    "mirah": extract_comments_ruby,
    "standard ml": extract_comments_star_nested,
    "component pascal": extract_comments_star_nested,
    "modula-2": extract_comments_star_nested,
    "moonscript": extract_comments_lua,
    "mupad": extract_comments_java,
    "netlinx": extract_comments_java,
    "nemerle": extract_comments_java,
    "lua": extract_comments_lua,
    "m4": extract_comments_m4,
    "m4sugar": extract_comments_m4,
    "mathematica": extract_comments_mathematica,
    "matlab": extract_comments_matlab,
    "newlisp": extract_comments_newlisp,
    "ooc": extract_comments_java,
    "openedge abl": extract_comments_openedge_abl,
    "opa": extract_comments_java,
    "ox": extract_comments_java,
    "perl": extract_comments_perl,
    "perl6": extract_comments_raku,
    "prolog": extract_comments_prolog,
    "raw token data": extract_comments_none,
    "raku": extract_comments_raku,
    "racket": extract_comments_hash_pipe,
    "rouge": extract_comments_none,
    "ruby": extract_comments_ruby,
    "rdoc": extract_comments_rdoc,
    "restructuredtext": extract_comments_restructuredtext,
    "sas": extract_comments_sas,
    "self": extract_comments_smalltalk,
    "smalltalk": extract_comments_smalltalk,
    "slim": extract_comments_slim,
    "sql": extract_comments_sql,
    "sqlpl": extract_comments_sql,
    "stata": extract_comments_stata,
    "sqf": extract_comments_java,
    "stan": extract_comments_java,
    "stylus": extract_comments_java,
    "supercollider": extract_comments_java,
    "terra": extract_comments_lua,
    "webassembly": extract_comments_webassembly,
    "xquery": extract_comments_xquery,
    "jsoniq": extract_comments_xquery,
    "x10": extract_comments_java,
    "xpages": extract_comments_html,
    "org": extract_comments_org,
    "handlebars": extract_comments_handlebars,
    "ncl": extract_comments_semicolon,
    "literate coffeescript": extract_comments_coffeescript,
    "blitzbasic": extract_comments_semicolon,
    "blitzmax": extract_comments_blitzmax,
    "zephir": extract_comments_java,
    "c-objdump": extract_comments_none,
    "cpp-objdump": extract_comments_none,
    "csv": extract_comments_none,
    "d-objdump": extract_comments_none,
    "darcs patch": extract_comments_none,
    "diff": extract_comments_none,
    "formatted": extract_comments_none,
    "irc log": extract_comments_none,
    "objdump": extract_comments_none,
    "public key": extract_comments_none,
    "python traceback": extract_comments_none,
    "shellsession": extract_comments_none,
    "text": extract_comments_none,
}


def extract_comments(content, langs):
    """Return all detected comments for the provided languages.

    Args:
        content: Source text to scan.
        langs: Candidate language names. Unknown names are ignored so callers
            can pass every extension-derived candidate without pre-filtering.

    Returns:
        Comment tuples in extractor order. Multiple languages can share an
        extension; collecting every applicable language avoids false negatives
        but can introduce duplicates. Each tuple is ``((start, end), text, kind)``
        where ``kind`` is ``line`` or ``block``.
    """
    comments: List[CommentSpan] = []
    langs = [lang.lower() for lang in langs]
    for lang in langs:
        extractor = _LANG_EXTRACTORS.get(lang)
        if extractor is None:
            # Unknown language: skip to avoid raising for multi-extension files
            continue
        comments.extend(extractor(content))
    return comments


# Backwards-compatible entry point: still named remove_comments but now returns
# structured comment tuples ((start, end), text, kind).
def remove_comments(content, langs):
    """Return extracted comments using the historical function name.

    Args:
        content: Source text to scan.
        langs: Candidate language names.

    Returns:
        The same structured tuples as ``extract_comments``.
    """

    return extract_comments(content, langs)


def extract_opening_comment(content: str, langs) -> CommentSpan | None:
    """Return the first file-opening comment, if present.

    Args:
        content: Source text to scan.
        langs: Candidate language names.

    Returns:
        The opening ``((start, end), text, kind)`` tuple when the comment appears
        before the first non-preprocessor, non-whitespace code token; otherwise
        ``None``.
    """
    comments = sorted(extract_comments(content, langs), key=lambda c: c[0][0])
    for span, text, kind in comments:
        prefix = content[: span[0]]
        if _is_preamble(prefix):
            return (span, text, kind)
    return None
