import pytest

from ml4setk import CommentQuery, CommentSanitizer, sanitize_comment
from ml4setk.Parsing.Comments import SUPPORTED_LANGUAGES, get_comment_syntax

pytestmark = pytest.mark.unit


def _matches(language, text):
    matches = CommentQuery(language).parse(text)
    for match in matches:
        assert match.prefix + match.match + match.suffix == text
    starts = [len(match.prefix) for match in matches]
    assert starts == sorted(starts)
    assert all(
        starts[index] + len(matches[index].match) <= starts[index + 1]
        for index in range(len(matches) - 1)
    )
    return [match.match for match in matches]


@pytest.mark.parametrize(
    ("label", "canonical", "family"),
    (
        ("Leo", "leo", "leo_style"),
        ("Linear Programming", "linear_programming", "linear_programming_style"),
        ("LiveCode Script", "livecode_script", "livecode_script_style"),
        ("Luau", "lua", "lua_style"),
        ("mdsvex", "mdsvex", "mdsvex_style"),
        ("MDX", "mdx", "mdx_style"),
        ("Mermaid", "mermaid", "mermaid_style"),
        ("MiniZinc", "minizinc", "minizinc_style"),
        ("MiniZinc Data", "minizinc", "minizinc_style"),
    ),
)
def test_batch_05_supported_raw_labels_resolve(label, canonical, family):
    syntax = get_comment_syntax(label)

    assert syntax.canonical_name == canonical
    assert syntax.family_name == family


def test_m3u_aggregate_remains_explicitly_deferred():
    assert "m3u" not in SUPPORTED_LANGUAGES
    for operation in (
        lambda: get_comment_syntax("M3U"),
        lambda: CommentQuery("M3U"),
        lambda: CommentSanitizer("M3U"),
        lambda: sanitize_comment("M3U", "# vendor-dependent line"),
    ):
        with pytest.raises(NotImplementedError, match="Unsupported language"):
            operation()


def test_leo_extracts_string_aware_first_close_comments():
    source = (
        'let url = "https://host/a//literal";\n'
        'let marker = "/* literal */";\n'
        "let value = left / right; // line note\r\n"
        "/* outer /* inner */ tail */"
    )

    assert _matches("Leo", source) == ["// line note", "/* outer /* inner */"]


@pytest.mark.parametrize(
    "boundary",
    tuple(chr(codepoint) for codepoint in (*range(0x202A, 0x202F), *range(0x2066, 0x206A))),
)
def test_leo_bidi_controls_end_line_comment_tokens(boundary):
    source = f"// visible {boundary}hidden"

    assert _matches("Leo", source) == ["// visible "]


def test_leo_rejects_bidi_and_unclosed_block_comments():
    assert _matches("Leo", "/* visible \u202ehidden */") == []
    assert _matches("Leo", "/* never closed") == []
    assert _matches("Leo", "stray */ and / operators") == []

    sanitizer = CommentSanitizer("Leo")
    assert sanitizer.sanitize("// line note") == "line note"
    assert sanitizer.sanitize("/* block note */") == "block note"
    assert sanitizer.sanitize("/* never closed") == "/* never closed"


def test_linear_programming_backslash_is_unconditional_and_cr_is_excluded():
    source = (
        "\\ model note\r\n"
        "Minimize\n"
        " cost: 4 x + 2 y \\ objective note\r\n"
        ' name: "C:\\copied path"\n'
        "End"
    )

    assert _matches("Linear Programming", source) == [
        "\\ model note",
        "\\ objective note",
        '\\copied path"',
    ]


def test_linear_programming_rejects_other_format_markers_and_cleans_one_wrapper():
    source = "* MPS line\n# MathProg line\n// slash line\nleft / right"

    assert _matches("Linear Programming", source) == []
    assert CommentSanitizer("Linear Programming").sanitize("\\  keep spacing") == ("  keep spacing")


def test_livecode_script_extracts_all_four_forms_outside_strings():
    source = (
        'put "# -- // /* https://host/a//b */" into marker\n'
        "# hash note\n"
        "put 1 into value -- dash note\r\n"
        "add 1 to value // slash note\r"
        "/* block note */\n"
        "put value"
    )

    assert _matches("LiveCode Script", source) == [
        "# hash note",
        "-- dash note",
        "// slash note",
        "/* block note */",
    ]


def test_livecode_script_uses_first_close_and_rejects_malformed_blocks():
    source = "/* outer /* inner */ tail */"

    assert _matches("LiveCode Script", source) == ["/* outer /* inner */"]
    assert _matches("LiveCode Script", "/* never closed") == []
    assert _matches("LiveCode Script", "left / right - value") == []

    sanitizer = CommentSanitizer("LiveCode Script")
    assert sanitizer.sanitize("# hash") == "hash"
    assert sanitizer.sanitize("-- dash") == "dash"
    assert sanitizer.sanitize("// slash") == "slash"
    assert sanitizer.sanitize("/* block */") == "block"


def test_luau_alias_excludes_hot_comments_and_masks_all_string_forms():
    source = (
        "--!strict\n"
        "--!arbitrary-directive\n"
        "local quotient = 8 // 2\n"
        'local a = "-- literal"\n'
        "local b = '-- literal'\n"
        "local c = `-- interpolated-looking literal`\n"
        "local d = [=[-- long string literal]=]\n"
        "local value = 1 -- ordinary line\n"
        "-- ! spaced ordinary line\n"
        "--[==[ long comment --[[ does not nest ]==]"
    )

    assert get_comment_syntax("Luau") is get_comment_syntax("Lua")
    assert _matches("Luau", source) == [
        "-- ordinary line",
        "-- ! spaced ordinary line",
        "--[==[ long comment --[[ does not nest ]==]",
    ]


def test_luau_malformed_long_forms_and_sanitizer_preserve_directives():
    assert _matches("Luau", "--[=[ broken ]] and no matching close") == []
    assert _matches("Luau", "--[=x malformed opener") == ["--[=x malformed opener"]
    assert _matches("Luau", "--!native") == []

    sanitizer = CommentSanitizer("Luau")
    assert sanitizer.sanitize("--!strict") == "--!strict"
    assert sanitizer.sanitize("-- ordinary") == "ordinary"
    assert sanitizer.sanitize("--[==[ long body ]==]") == "long body"


@pytest.mark.parametrize("fake_opener", ('[=[ "', "[==["))
def test_luau_comment_prose_does_not_open_literal_ranges(fake_opener):
    source = f"-- {fake_opener} fake\nlocal value = 1\n-- actual"

    assert _matches("Luau", source) == [
        f"-- {fake_opener} fake",
        "-- actual",
    ]

    long_comment = '--[=[ " [==[ fake ]=]\nlocal value = 1\n-- actual'
    assert _matches("Luau", long_comment) == [
        '--[=[ " [==[ fake ]=]',
        "-- actual",
    ]


def test_mdsvex_extracts_only_ordinary_host_html_comment_nodes():
    source = (
        "---\n"
        'title: "<!-- metadata -->"\n'
        "---\n"
        "<!-- host note -->\n"
        "`<!-- inline code -->`\n"
        "    <!-- indented code -->\n"
        "<script><!-- script data --></script>\n"
        "<style>/* <!-- style data --> */</style>\n"
        "<pre><!-- pre data --></pre>\n"
        '<p title="<!-- attribute data -->">value <!-- inline host --> value</p>\n'
        "{`<!-- expression data -->`}\n"
        "<!-- svelte-ignore a11y_missing_attribute -->\n"
        "```html\n"
        "<!-- fenced code -->\n"
        "```\n"
    )

    assert _matches("mdsvex", source) == ["<!-- host note -->", "<!-- inline host -->"]


def test_mdsvex_first_close_malformed_and_sanitizer_semantics():
    source = "é <!-- outer <!-- inner --> tail -->"

    assert _matches("mdsvex", source) == ["<!-- outer <!-- inner -->"]
    assert _matches("mdsvex", "<!-- never closed") == []
    assert _matches("mdsvex", "<!-- svelte-ignore warning -->") == []

    sanitizer = CommentSanitizer("mdsvex")
    assert sanitizer.sanitize("<!-- host\r\nnote -->") == "host\nnote"
    directive = "<!-- svelte-ignore warning -->"
    assert sanitizer.sanitize(directive) == directive


def test_mdx_extracts_acorn_style_ranges_only_inside_javascript_regions():
    source = (
        "export const value = 1 // ESM note\n"
        "\n"
        "Before {/* content note */} after\n"
        "{// line note\n"
        "}\n"
        "<Widget value={value /* attribute note */} />\n"
        "<Widget {...props /* spread note */} />\n"
        '{"https://host/a//literal" + `/* template */` '
        "+ /a\\/\\/*b/.source /* expression note */}\n"
        "`{/* inline code */}`\n"
        "```jsx\n"
        "{/* fenced code */}\n"
        "```\n"
        "<!-- HTML syntax is not an MDX comment -->"
    )

    assert _matches("MDX", source) == [
        "// ESM note",
        "/* content note */",
        "// line note",
        "/* attribute note */",
        "/* spread note */",
        "/* expression note */",
    ]


@pytest.mark.parametrize("terminator", ("\n", "\r", "\r\n", "\u2028", "\u2029"))
def test_mdx_line_comments_honor_all_ecmascript_line_terminators(terminator):
    source = f"{{// note{terminator}}}"

    assert _matches("MDX", source) == ["// note"]


def test_mdx_rejects_invalid_attribute_and_malformed_expression_comments():
    assert _matches("MDX", "<div {/* invalid attribute slot */} />") == []
    assert _matches("MDX", "{/* never closed") == []
    assert _matches("MDX", "{// close is swallowed }") == []
    assert _matches("MDX", 'text "// prose" https://host/a//b') == []
    assert _matches("MDX", "export const x = 1 // eof") == ["// eof"]


def test_mdx_sanitizer_preserves_surrounding_braces_and_content():
    source = "Before {/* retained body */} after"
    match = CommentQuery("MDX").parse(source)[0]

    assert match.prefix == "Before {"
    assert match.suffix == "} after"
    assert CommentSanitizer("MDX").sanitize(match) == "retained body"


def test_mermaid_extracts_only_portable_own_line_comments():
    source = (
        "---\n"
        'title: "%% metadata"\n'
        "---\n"
        "sequenceDiagram\n"
        "  %% indented note\r\n"
        "Client->>Server: request %% inline dialect form\r"
        "\t%% tabbed note\n"
        "%%{init: {'theme': 'forest'}}%%\n"
        'A["%% quoted label"]\n'
        "%%\n"
        "%% "
    )

    assert _matches("Mermaid", source) == ["%% indented note", "%% tabbed note", "%% "]


def test_mermaid_directives_are_preserved_by_extraction_and_cleaning():
    assert _matches("Mermaid", "%%{ incomplete") == []
    assert _matches("Mermaid", "A --> B %% inline") == []

    sanitizer = CommentSanitizer("Mermaid")
    assert sanitizer.sanitize("  %% note") == "note"
    directive = "%%{init: {}}%%"
    assert sanitizer.sanitize(directive) == directive


@pytest.mark.parametrize("label", ("MiniZinc", "MiniZinc Data"))
def test_minizinc_family_extracts_doc_blocks_and_protects_literals(label):
    source = (
        'string: literal = "% and /* text */";\n'
        "int: `% quoted identifier` = 1;\n"
        "/*** file documentation */\n"
        "/** declaration documentation */\n"
        "constraint 8 / 2 > 0; /* ordinary block */\n"
        "int: x = 1; % line note\r\n"
        "/* outer /* inner */ tail */"
    )

    assert _matches(label, source) == [
        "/*** file documentation */",
        "/** declaration documentation */",
        "/* ordinary block */",
        "% line note\r",
        "/* outer /* inner */",
    ]


@pytest.mark.parametrize("label", ("MiniZinc", "MiniZinc Data"))
@pytest.mark.parametrize("opener", ("/*", "/**", "/***"))
def test_minizinc_family_accepts_all_unclosed_block_forms(label, opener):
    source = f"{opener} accepted through EOF"

    assert _matches(label, source) == [source]
    assert CommentSanitizer(label).sanitize(source) == "accepted through EOF"


def test_minizinc_percent_comments_end_only_at_lf_or_eof():
    assert _matches("MiniZinc", "% before CR\rstill comment") == ["% before CR\rstill comment"]
    assert _matches("MiniZinc", "% before CRLF\r\nconstraint true;") == ["% before CRLF\r"]
    assert _matches("MiniZinc", "% eof") == ["% eof"]


def test_minizinc_alias_identity_and_longest_sanitizer_wrappers():
    assert get_comment_syntax("MiniZinc Data") is get_comment_syntax("MiniZinc")

    sanitizer = CommentSanitizer("MiniZinc Data")
    assert sanitizer.sanitize("/*** file body */") == "file body"
    assert sanitizer.sanitize("/** doc body */") == "doc body"
    assert sanitizer.sanitize("/* ordinary body */") == "ordinary body"
    assert sanitizer.sanitize("% line body") == "line body"


@pytest.mark.parametrize("label", ("MiniZinc", "MiniZinc Data"))
@pytest.mark.parametrize(
    "source",
    (
        '% " fake\nint: value = 1;\n% actual',
        "% ` fake\nint: value = 1;\n% actual",
        '/* " fake */\nint: value = 1;\n% actual',
        "/* ` fake */\nint: value = 1;\n% actual",
    ),
)
def test_minizinc_comment_prose_does_not_open_literal_ranges(label, source):
    expected_first = source.split("\n", 1)[0]

    assert _matches(label, source) == [expected_first, "% actual"]
