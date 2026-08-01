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
        ("Aiken", "aiken", "aiken_style"),
        (
            "Answer Set Programming",
            "answer_set_programming",
            "answer_set_programming_style",
        ),
        ("B4X", "b4x", "b4x_style"),
        ("BibTeX Style", "erlang", "percent_style"),
        ("Bluespec BH", "bluespec_bh", "bluespec_bh_style"),
        ("BQN", "bqn", "bqn_style"),
        ("BuildStream", "yaml", "yaml_style"),
        ("Caddyfile", "caddyfile", "caddyfile_style"),
        ("Cairo Zero", "cairo_zero", "cairo_zero_style"),
        ("Carbon", "carbon", "carbon_style"),
    ),
)
def test_batch_00_raw_stack_labels_resolve(label, canonical, family):
    syntax = get_comment_syntax(label)

    assert syntax.canonical_name == canonical
    assert syntax.family_name == family


def test_aiken_extracts_all_line_forms_and_masks_literals_and_division():
    source = (
        '@"https://host/a//b"\n'
        '"bytes//payload"\n'
        "total / count\n"
        "const a = 1 // ordinary\n"
        "const b = 2\n/// documentation\n"
        "const c = 3\n//// module documentation\n"
        "const d = 4\n///// slash payload"
    )

    assert _matches("Aiken", source) == [
        "// ordinary",
        "/// documentation",
        "//// module documentation",
        "///// slash payload",
    ]


@pytest.mark.parametrize(
    ("comment", "expected"),
    (
        ("// ordinary", "ordinary"),
        ("/// **documentation**", "**documentation**"),
        ("//// # module", "# module"),
        ("///// payload slash", "/ payload slash"),
    ),
)
def test_aiken_sanitizer_removes_the_complete_classified_introducer(comment, expected):
    assert CommentSanitizer("Aiken").sanitize(comment) == expected


def test_answer_set_programming_handles_line_nested_and_script_contexts():
    source = (
        'message("100% ready").\n'
        "a. % line note\n"
        "b.\n#! hashbang note\n"
        "%* outer %* inner *% outer *%\n"
        "#script (python)\n"
        "x = 5 % 2\n"
        "#! embedded text\n"
        "#end.\n"
        "c. % after script\n"
    )

    assert _matches("Answer Set Programming", source) == [
        "% line note",
        "#! hashbang note",
        "%* outer %* inner *% outer *%",
        "% after script",
    ]


def test_answer_set_programming_lone_percent_masks_a_same_line_block_close():
    source = "%* outer\n% line masks *%\nstill block *%\na."

    assert _matches("Answer Set Programming", source) == [
        "%* outer\n% line masks *%\nstill block *%"
    ]


@pytest.mark.parametrize(
    "source",
    (
        "%* unclosed",
        "%* outer %* inner *%",
        "#script (python)\nx = 5 % 2\n#! embedded",
    ),
)
def test_answer_set_programming_malformed_protected_regions_do_not_leak(source):
    assert _matches("Answer Set Programming", source) == []


def test_answer_set_programming_sanitizer_preserves_nested_payload():
    sanitizer = CommentSanitizer("Answer Set Programming")

    assert sanitizer.sanitize("% line note") == "line note"
    assert sanitizer.sanitize("#! hashbang note") == "hashbang note"
    assert sanitizer.sanitize("%* outer %* inner *% outer *%") == ("outer %* inner *% outer")


def test_b4x_masks_ordinary_and_smart_strings_without_accepting_rem():
    source = (
        'Dim a = "quoted ""apostrophe \'"" text" \' actual\n'
        'Dim b = $"smart\n\' literal\n"$\n'
        "Rem not a B4X comment\n"
        "#Region Project Attributes\n"
        "Dim c = 3 ' final"
    )

    assert _matches("B4X", source) == ["' actual", "' final"]
    assert CommentSanitizer("B4X").sanitize("' actual") == "actual"


def test_b4x_unclosed_string_conservatively_protects_the_remainder():
    source = "Dim a = \"unterminated\n' not a comment"

    assert _matches("B4X", source) == []


@pytest.mark.parametrize("fake_opener", ('"', '$"'))
def test_b4x_comment_prose_does_not_open_string_ranges(fake_opener):
    source = f"' {fake_opener} fake\nDim value = 1\n' actual"

    assert _matches("B4X", source) == [
        f"' {fake_opener} fake",
        "' actual",
    ]


@pytest.mark.parametrize(
    "source",
    (
        '// " fake\n{}\n// actual',
        '/* " fake */\n{}\n// actual',
    ),
)
def test_jsonc_comment_prose_does_not_open_string_ranges(source):
    expected_first = source.split("\n", 1)[0]

    assert _matches("jsonc", source) == [expected_first, "// actual"]
    assert _matches("jsonc", '{"value": "// literal /* text */"}\n// actual') == ["// actual"]


def test_bibtex_style_is_exact_percent_alias_with_string_masking():
    source = 'title = "100% ready"\nvalue = title % note\nfield = #1'

    assert get_comment_syntax("BibTeX Style") is get_comment_syntax("bibtex")
    assert _matches("BibTeX Style", source) == ["% note"]
    assert CommentSanitizer("BibTeX Style").sanitize("% note") == "note"


def test_bluespec_bh_respects_operators_pragmas_literals_and_nested_blocks():
    source = (
        "a --+ b\n"
        "c --> d\n"
        's = "-- not a comment"\n'
        "{-# OPTIONS -Wall #-}\n"
        "--- line note\n"
        "value\n"
        "--@ annotation note\n"
        "before {- outer {- inner -} outer -} after"
    )

    assert _matches("Bluespec BH", source) == [
        "--- line note",
        "--@ annotation note",
        "{- outer {- inner -} outer -}",
    ]


def test_bluespec_bh_requires_a_physical_lf_for_line_comments():
    assert _matches("Bluespec BH", "-- no final newline") == []
    assert _matches("Bluespec BH", "-- crlf note\r\nnext") == ["-- crlf note"]


def test_bluespec_bh_sanitizer_removes_the_maximal_dash_run():
    sanitizer = CommentSanitizer("Bluespec BH")

    assert sanitizer.sanitize("----- note") == "note"
    assert sanitizer.sanitize("{- outer {- inner -} outer -}") == ("outer {- inner -} outer")


def test_bqn_masks_multiline_strings_doubled_quotes_and_character_literals():
    source = (
        '"first line\n# string data"\n'
        '"escaped "" # still data"\n'
        "'#'\n"
        "value # line note\n"
        "next # eof note"
    )

    assert _matches("BQN", source) == ["# line note", "# eof note"]
    assert CommentSanitizer("BQN").sanitize("# line note") == "line note"


def test_bqn_unclosed_string_protects_the_remainder():
    assert _matches("BQN", '"unterminated\n# literal') == []


def test_buildstream_yaml_obeys_boundaries_quotes_and_block_scalars():
    source = (
        "url: https://example.invalid/a#fragment\n"
        "plain: abc#def\n"
        'quoted: "# literal"\n'
        "script: | # header note\n"
        "  # literal block data\n"
        "  echo ok # also data\n"
        "# after block\n"
        "kind: manual # final note"
    )

    expected = ["# header note", "# after block", "# final note"]
    assert _matches("BuildStream", source) == expected
    assert _matches("yaml", source) == expected


def test_yaml_multiline_quotes_and_explicit_block_indentation_are_protected():
    source = 'quoted: "first\n# still quoted"\nscript: |2\n  # scalar data\n# actual'

    assert _matches("BuildStream", source) == ["# actual"]
    assert CommentSanitizer("BuildStream").sanitize("# actual") == "actual"


def test_caddyfile_requires_token_start_and_masks_all_quoted_forms():
    source = (
        "redir / /some/#/path\n"
        'respond "# double quoted"\n'
        "respond `# backtick quoted`\n"
        "respond <<HTML\n"
        "  # heredoc data\n"
        "HTML\n"
        "reverse_proxy localhost:9000 # inline note\n"
    )

    assert _matches("Caddyfile", source) == ["# inline note"]
    assert _matches("Caddyfile", "\ufeff# bom note") == ["# bom note"]
    assert CommentSanitizer("Caddyfile").sanitize("# inline note") == "inline note"


def test_caddyfile_escaped_newline_keeps_the_continued_token_open():
    source = "token\\\n#continued\n# actual\n"

    assert _matches("Caddyfile", source) == ["# actual"]


@pytest.mark.parametrize(
    "source",
    (
        'respond "unterminated\n# literal',
        "respond `unterminated\n# literal",
        "respond <<HTML\n# literal without terminator",
    ),
)
def test_caddyfile_malformed_tokens_protect_the_remainder(source):
    assert _matches("Caddyfile", source) == []


def test_cairo_zero_masks_hints_and_literals_before_slash_comments():
    source = (
        '%{ python_value = "// hint data" %}\n'
        'let a = "// string data";\n'
        "let b = '// character data';\n"
        "let c = 1; // line note\n"
        "ret; // eof note"
    )

    assert _matches("Cairo Zero", source) == ["// line note", "// eof note"]
    assert CommentSanitizer("Cairo Zero").sanitize("// line note") == "line note"


@pytest.mark.parametrize(
    "source",
    (
        "%{ unclosed hint\n// literal",
        'let value = "unclosed\n// literal',
    ),
)
def test_cairo_zero_malformed_protected_regions_do_not_leak(source):
    assert _matches("Cairo Zero", source) == []


def test_carbon_requires_the_pinned_ascii_post_introducer_set():
    source = "//identifier\n//\u00a0not-space\n//\r\n// text\r\nvalue;\n//\tTabbed\nvalue;\n//"

    assert _matches("Carbon", source) == ["// text", "//\tTabbed", "//"]


def test_carbon_masks_simple_raw_and_block_literals_but_keeps_header_comment():
    source = (
        'var simple = "// string";\n'
        'var raw = #"// raw"#;\n'
        "var block = ''' Core // header note\n"
        "// block data\n"
        "''' ;\n"
        "var raw_block = #'''\n"
        "// raw block data\n"
        "'''#;\n"
        "// final note"
    )

    assert _matches("Carbon", source) == ["// header note", "// final note"]
    assert CommentSanitizer("Carbon").sanitize("// final note") == "final note"


def test_carbon_unclosed_literals_protect_the_remainder():
    assert _matches("Carbon", 'var s = "unterminated\n// literal') == []
    assert _matches("Carbon", "var s = '''\n// literal") == []
