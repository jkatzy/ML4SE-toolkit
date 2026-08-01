import pytest

from ml4setk import CommentQuery, CommentSanitizer
from ml4setk.Parsing.Comments import get_comment_syntax

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
        ("Dune", "assembly", "semicolon_style"),
        ("Ecmarkup", "html", "markup_style"),
        ("Edge", "edge", "edge_style"),
        ("EdgeQL", "dockerfile", "hash_line_style"),
        ("F*", "f_star", "f_star_style"),
        ("FIRRTL", "assembly", "semicolon_style"),
        ("GDShader", "gdshader", "gdshader_style"),
        ("Glimmer JS", "glimmer_js", "glimmer_js_style"),
        ("Glimmer TS", "glimmer_ts", "glimmer_ts_style"),
        ("Go Workspace", "go_module", "go_directive_file_style"),
        ("Godot Resource", "godot_resource", "godot_resource_style"),
        ("Gradle Kotlin DSL", "kotlin", "kotlin_style"),
        ("Hare", "qsharp", "slash_line_style"),
        ("HIP", "java", "c_style"),
        ("Hosts File", "dockerfile", "hash_line_style"),
        ("Imba", "imba", "imba_style"),
        ("Ink", "ink", "ink_style"),
    ),
)
def test_batch_02_03_raw_labels_resolve(label, canonical, family):
    syntax = get_comment_syntax(label)

    assert syntax.canonical_name == canonical
    assert syntax.family_name == family


def test_dune_masks_quoted_and_end_of_line_strings():
    source = (
        '(name "semi;colon")\n'
        "\\|literal ; data\r"
        "(name demo) ; inline note\n"
        "\\>more ; data\n"
        ";; eof note"
    )

    assert _matches("Dune", source) == ["; inline note", ";; eof note"]


def test_ecmarkup_requires_closed_comments_in_html_data():
    source = (
        '<div data-note="<!-- attribute -->">x</div>\n'
        '<script>const marker = "<!-- script -->";</script>\n'
        "&lt;!-- escaped --&gt;\n"
        "<!-- actual <!-- malformed nesting -->\n"
        "<!-- first -->tail-->",
    )

    assert _matches("Ecmarkup", "".join(source)) == ["<!-- first -->"]
    assert _matches("Ecmarkup", "<!-- unclosed") == []
    assert _matches("Ecmarkup", "<!-- bad --!>") == []


def test_edge_uses_raw_mode_and_brace_depth():
    source = (
        '{{ "{{-- active mustache data --}}" }}\n'
        "{{-- outer { value } {{-- inner --}} tail --}}\n"
        "@if(user) {{-- line-tag rejection --}}\n"
        "{{-- unclosed { --}}"
    )

    assert _matches("Edge", source) == ["{{-- outer { value } {{-- inner --}} tail --}}"]


def test_edgeql_masks_all_string_families_and_keeps_floor_division():
    source = "select 'a#b', r\"c#d\", b'e#f', $$g#h$$; # actual\rselect 7 // 2; # eof"

    assert _matches("EdgeQL", source) == ["# actual", "# eof"]


def test_f_star_handles_terminators_markers_literals_and_eof_blocks():
    source = (
        'let marker = "// string (* data *)"\n'
        "```lang\n// blob\n```\n"
        "// IN F*: let x = 1 // actual\u2028"
        "(* outer (* inner *) tail *)\n"
        "(* accepted EOF"
    )

    assert _matches("F*", source) == [
        "// actual",
        "(* outer (* inner *) tail *)",
        "(* accepted EOF",
    ]


def test_firrtl_masks_lexer_units_before_semicolon_matching():
    source = (
        'wire x : String = "literal;value"\n'
        "node y = x @[file.fir 1:2;3]\n"
        "%[annotation;payload]\n"
        "module Demo: ; actual\rnext"
    )

    assert _matches("FIRRTL", source) == ["; actual"]


def test_gdshader_lf_line_end_and_eof_block_behavior():
    source = (
        'const String marker = "// literal /* data */";\n'
        "// bare cr stays\rcontinued\n"
        "/** doc note */ token /* first /* inner */ tail\n"
        "/* accepted EOF"
    )

    assert _matches("GDShader", source) == [
        "// bare cr stays\rcontinued",
        "/** doc note */",
        "/* first /* inner */",
        "/* accepted EOF",
    ]


@pytest.mark.parametrize("label", ("Glimmer JS", "Glimmer TS"))
def test_glimmer_switches_comment_grammars_at_content_tags(label):
    source = (
        'const fake = "<template>{{! hidden }}</template>";\n'
        "const regex = /<template>\\/\\/ hidden<\\/template>/;\n"
        "// host note\u2029"
        "<template>\n"
        "  // rendered text\n"
        "  {{!-- long }} text --}}\n"
        '  <button {{~! attr note ~}} title="{{! value data }}">ok</button>\n'
        "  <!-- html note -->\n"
        "</template>\n"
        "/* host block */"
    )

    assert _matches(label, source) == [
        "// host note",
        "{{!-- long }} text --}}",
        "{{~! attr note ~}}",
        "<!-- html note -->",
        "/* host block */",
    ]


@pytest.mark.parametrize("label", ("Glimmer JS", "Glimmer TS"))
def test_glimmer_rejects_unclosed_mode_specific_blocks(label):
    assert _matches(label, "<template>{{! unfinished</template>") == []
    assert _matches(label, "<template><!-- unfinished</template>") == []
    assert _matches(label, "/* unfinished") == []


def test_godot_resource_masks_variant_strings_and_preserves_colors():
    source = (
        'path = "res://a;b.tres" ; dependency\nname = &"semi;colon"\ncolor = #ff00ff\n; eof note'
    )

    assert _matches("Godot Resource", source) == ["; dependency", "; eof note"]


def test_go_workspace_and_gradle_kotlin_dsl_existing_fixes_hold():
    go_source = 'use "./module//literal" // actual\n/* rejected */'
    kotlin_source = 'val raw = """/* literal */"""\n// actual\n/* outer /* inner */ tail */'

    assert _matches("Go Workspace", go_source) == ["// actual"]
    assert _matches("Gradle Kotlin DSL", kotlin_source) == [
        "// actual",
        "/* outer /* inner */ tail */",
    ]


def test_hare_masks_literals_and_retains_cr_until_lf():
    source = (
        'let url = "https://example";\n'
        "let rune = '/'; let raw = `// literal`;\n"
        "world// bare cr\rcontinued\n"
        "/* unsupported */\n"
        "//"
    )

    assert _matches("Hare", source) == ["// bare cr\rcontinued", "//"]


def test_hip_handles_raw_strings_splices_and_first_block_close():
    spliced_comment = "// continued \\" + "\n" + "still comment"
    source = (
        'auto raw = R"tag(https://x/* literal */)tag";\n'
        'auto normal = "// literal";\n' + spliced_comment + "\n"
        "__global__ void k() { /* outer /* inner */ tail; }"
    )

    assert _matches("HIP", source) == [
        spliced_comment,
        "/* outer /* inner */",
    ]


def test_hosts_file_has_no_quote_or_escape_shielding():
    source = (
        '127.0.0.1 "quoted#still-comment"\r\n'
        "::1 localhost # ipv6 aliases\n"
        "example.test\\# escaped-looking"
    )

    assert _matches("Hosts File", source) == [
        '#still-comment"',
        "# ipv6 aliases",
        "# escaped-looking",
    ]


def test_imba_common_subset_masks_literals_symbols_and_regexes():
    source = (
        'let text = "# hidden"\n'
        "let state = #ready\n"
        "let pattern = /# hidden/\n"
        "# line note\n"
        "#! bang body\n"
        "### block ###\n"
        "// v2-only\n"
        "/* v2-only */\n"
        "### accepted EOF"
    )

    assert _matches("Imba", source) == [
        "# line note\n#! bang body",
        "### block ###",
        "### accepted EOF",
    ]
    assert _matches("Imba", "###") == []


def test_ink_raw_prepass_ignores_quote_and_url_context():
    source = (
        "Visit https://example.test/path\n"
        'Say "// quoted note"\rNext\n'
        "/* outer /* inner */ tail\n"
        "# story-tag\n"
        "/* accepted EOF"
    )

    assert _matches("Ink", source) == [
        "//example.test/path",
        '// quoted note"',
        "/* outer /* inner */",
        "/* accepted EOF",
    ]
    assert _matches("Ink", "/*") == []


@pytest.mark.parametrize(
    ("label", "raw_comment", "expected"),
    (
        ("Dune", ";; body", "; body"),
        ("Ecmarkup", "<!-- body -->", "body"),
        ("Edge", "{{-- body --}}", "body"),
        ("F*", "(* outer (* inner *) tail *)", "outer (* inner *) tail"),
        ("GDShader", "/** doc body */", "doc body"),
        ("Glimmer JS", "{{~! body ~}}", "body"),
        ("Godot Resource", "; body", "body"),
        ("Hare", "// body", "body"),
        ("Imba", "### body ###", "body"),
        ("Ink", "/* body */", "body"),
    ),
)
def test_batch_02_03_sanitizer_wrappers(label, raw_comment, expected):
    assert CommentSanitizer(label).sanitize(raw_comment) == expected


@pytest.mark.parametrize("label", ("Genero 4gl", "Genero per", "iCalendar"))
def test_reviewed_deferred_and_unsupported_labels_remain_unregistered(label):
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        get_comment_syntax(label)
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        CommentSanitizer(label)
