import pytest

from ml4setk import CommentQuery, CommentSanitizer, sanitize_comment
from ml4setk.Parsing.Comments import get_comment_syntax

pytestmark = pytest.mark.unit


def _matches(language: str, source: str) -> list[str]:
    matches = CommentQuery(language).parse(source)
    for match in matches:
        assert match.prefix + match.match + match.suffix == source
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
        ("Vento", "vento", "vento_style"),
        ("Visual Basic 6.0", "visual_basic_net", "apostrophe_style"),
        (
            "WebAssembly Interface Type",
            "webassembly_interface_type",
            "webassembly_interface_type_style",
        ),
        ("WGSL", "wgsl", "wgsl_style"),
        ("Xmake", "lua", "lua_style"),
        ("Zmodel", "java", "c_style"),
    ),
)
def test_batch_11_exact_labels_resolve(label, canonical, family):
    syntax = get_comment_syntax(label)

    assert syntax.canonical_name == canonical
    assert syntax.family_name == family


def test_vento_uses_first_close_and_rejects_unclosed_tags():
    source = "<h1>{{#- hidden {{# inner #}} suffix -#}}</h1>\r\n{{ value }}\n{{# never closed"

    assert _matches("Vento", source) == ["{{#- hidden {{# inner #}}"]
    assert _matches("Vento", "{{##}}") == ["{{##}}"]
    assert _matches("Vento", "{{ value }} // not template comments /* no */") == []


@pytest.mark.parametrize(
    ("raw_comment", "expected"),
    (
        ("{{# body #}}", "body"),
        ("{{#- body #}}", "body"),
        ("{{# body -#}}", "body"),
        ("{{#- body -#}}", "body"),
        ("{{##}}", ""),
        ("{{#\n  first\n  second\n#}}", "first\nsecond"),
    ),
)
def test_vento_sanitizer_handles_all_trim_wrapper_combinations(raw_comment, expected):
    assert sanitize_comment("Vento", raw_comment) == expected


def test_visual_basic_6_accepts_bare_rem_and_rejects_false_boundaries():
    source = (
        "Rem\r\n"
        "100 Rem numbered\r"
        "value = 1: rEm trailing\n"
        "value = 1 Rem invalid\n"
        "Remember = True\n"
        'text = "Rem and \' stay data"\n'
        "' apostrophe"
    )

    assert _matches("Visual Basic 6.0", source) == [
        "Rem",
        "Rem numbered",
        "rEm trailing",
        "' apostrophe",
    ]
    assert sanitize_comment("Visual Basic 6.0", "Rem") == ""


def test_wit_is_nested_c_style_not_webassembly_text():
    source = (
        'let marker = "// not a comment /* either */";\n'
        "/// API documentation\r\n"
        "/* outer /* inner */ outer */\n"
        ";; not WIT\n"
        "(; not WIT ;)\n"
        "/* unclosed"
    )

    assert _matches("WebAssembly Interface Type", source) == [
        "/// API documentation",
        "/* outer /* inner */ outer */",
    ]
    assert _matches("wit", "run: func(); // eof") == ["// eof"]
    assert sanitize_comment("wit", "/// docs") == "/ docs"
    assert sanitize_comment("wit", "/** docs */") == "* docs"


@pytest.mark.parametrize("line_break", ("\n", "\v", "\f", "\r", "\r\n", "\x85", "\u2028", "\u2029"))
def test_wgsl_line_comment_stops_at_every_normative_line_break(line_break):
    source = f"let value = 1; // note{line_break}let next = 2;"

    assert _matches("WGSL", source) == ["// note"]


def test_wgsl_supports_nested_blocks_and_rejects_unclosed_blocks():
    source = (
        "let ratio = left / right;\n"
        "let update = value /= 2;\n"
        "/* outer /* inner */ outer */\n"
        "/* never closed"
    )

    assert _matches("WGSL", source) == ["/* outer /* inner */ outer */"]
    assert sanitize_comment("WGSL", "/* outer /* inner */ outer */") == ("outer /* inner */ outer")


def test_xmake_masks_quoted_and_long_bracket_strings():
    source = (
        'local quoted = "-- not a comment"\n'
        "local zero = [[-- not a comment]]\n"
        "local level = [=[--[[ still a string ]]]=]\n"
        'target("demo") -- short\r\n'
        "--[=[ long --[[ not nested ]] body ]=]\n"
        "--[==[ unclosed"
    )

    assert _matches("Xmake", source) == [
        "-- short",
        "--[=[ long --[[ not nested ]] body ]=]",
    ]


def test_xmake_malformed_long_openers_fall_back_to_short_comments():
    assert _matches("Xmake", "--[foo") == ["--[foo"]
    assert _matches("Xmake", "--[=") == ["--[="]
    assert _matches("Xmake", "--[=[ never closed") == []


@pytest.mark.parametrize(
    ("raw_comment", "expected"),
    (
        ("-- short", "short"),
        ("--[[ body ]]", "body"),
        ("--[=[ body ]=]", "body"),
        ("--[==[ body ]==]", "body"),
    ),
)
def test_xmake_sanitizer_supports_dynamic_long_comment_levels(raw_comment, expected):
    assert sanitize_comment("Xmake", raw_comment) == expected


def test_zmodel_alias_preserves_documentation_markers_and_masks_strings():
    source = (
        "/// Account docs.\n"
        "/** Persistent record. */\n"
        "model Account {\n"
        '  url String @default("https://host//path")\n'
        '  marker String @default("/* not a comment */")\n'
        "  id String @id // stable key\n"
        "}\n"
        "/* unclosed"
    )

    assert _matches("Zmodel", source) == [
        "/// Account docs.",
        "/** Persistent record. */",
        "// stable key",
    ]
    sanitizer = CommentSanitizer("Zmodel")
    assert sanitizer.sanitize("/// Account docs.") == "/ Account docs."
    assert sanitizer.sanitize("/** Persistent record. */") == "* Persistent record."
