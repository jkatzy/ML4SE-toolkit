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
        ("Circom", "circom", "circom_style"),
        ("Clue", "clue", "clue_style"),
        ("crontab", "crontab", "crontab_style"),
        ("Cylc", "cylc", "cylc_style"),
        ("Cypher", "java", "c_style"),
        ("D2", "d2", "d2_style"),
        ("Daslang", "boogie", "boogie_style"),
        ("Dotenv", "dotenv", "dotenv_style"),
    ),
)
def test_batch_01_supported_raw_labels_resolve(label, canonical, family):
    syntax = get_comment_syntax(label)

    assert syntax.canonical_name == canonical
    assert syntax.family_name == family


@pytest.mark.parametrize("label", ("Cpp-ObjDump", "D-ObjDump"))
def test_batch_01_generated_objdump_labels_remain_explicitly_unsupported(label):
    normalized = label.lower().replace("-", "_")

    assert normalized not in SUPPORTED_LANGUAGES
    for operation in (
        lambda: get_comment_syntax(label),
        lambda: CommentQuery(label),
        lambda: CommentSanitizer(label),
        lambda: sanitize_comment(label, "# // /* generated markers */"),
    ):
        with pytest.raises(NotImplementedError, match="Unsupported language"):
            operation()


def test_circom_preprocessor_recognizes_markers_without_string_state():
    source = (
        'include "https://host/a//preprocessed";\n'
        'include "/* preprocessed block */";\n'
        "signal output out; // line note\n"
        "out <== left / right;\n"
        "/* outer /* inner */ tail */"
    )

    assert _matches("Circom", source) == [
        '//host/a//preprocessed";',
        "/* preprocessed block */",
        "// line note",
        "/* outer /* inner */",
    ]


def test_circom_rejects_incomplete_blocks_and_preserves_eof_lines():
    assert _matches("Circom", "signal x; /* never closed") == []
    assert _matches("Circom", "signal x; // eof note") == ["// eof note"]
    assert _matches("Circom", "left / right") == []

    sanitizer = CommentSanitizer("Circom")
    assert sanitizer.sanitize("// line note") == "line note"
    assert sanitizer.sanitize("/* block note */") == "block note"


def test_clue_masks_all_quotes_and_accepts_first_close_comments():
    source = (
        'local a = "https://host/a//literal"\n'
        "local b = '/* literal */'\n"
        "local c = `// literal`\n"
        'local d = "escaped \\" // literal"\n'
        "local value = 1 // line note\n"
        "/* block note */\n"
        "/* outer /* inner */ tail */"
    )

    assert _matches("Clue", source) == [
        "// line note",
        "/* block note */",
        "/* outer /* inner */",
    ]


def test_clue_accepts_unclosed_blocks_but_not_unclosed_strings():
    assert _matches("Clue", "local value = 1 /* eof block") == ["/* eof block"]
    assert _matches("Clue", 'local value = "unterminated // literal') == []
    assert _matches("Clue", "stray */ value") == []

    sanitizer = CommentSanitizer("Clue")
    assert sanitizer.sanitize("/* eof block") == "eof block"
    assert sanitizer.sanitize("/* block note */") == "block note"


def test_crontab_only_extracts_comment_only_lines_after_ascii_indentation():
    source = (
        "  # first note\n"
        "\t# second note\n"
        "MAILTO=user#team\n"
        "0 0 * * * rotate --tag '#keep' # argument\n"
        "\u00a0# non-ascii indentation\n"
        "# eof note"
    )

    assert _matches("crontab", source) == [
        "  # first note\n\t# second note",
        "# eof note",
    ]
    assert CommentSanitizer("crontab").sanitize("  # note") == "note"


def test_cylc_masks_native_quote_forms_and_excludes_template_directives():
    source = (
        "#!jinja2\n"
        "{# template comment #}\n"
        "[runtime] # heading note\n"
        "    single = '# literal'\n"
        '    double = "# literal"\n'
        "    script = '''\n"
        "        # embedded shell data\n"
        "    '''\n"
        '    other = """# triple data"""\n'
        "    retries = 3 # value note"
    )

    assert _matches("Cylc", source) == ["# heading note", "# value note"]
    assert CommentSanitizer("Cylc").sanitize("# value note") == "value note"


def test_cylc_unclosed_triple_quote_protects_the_remainder():
    source = 'script = """\n# embedded\n[runtime] # still embedded'

    assert _matches("Cylc", source) == []


def test_cypher_exact_alias_masks_literals_and_uses_first_close_blocks():
    source = (
        "MATCH (n) // line note\n"
        "WHERE n.url = 'https://host/a//literal'\n"
        'AND n.marker = "/* literal */"\n'
        "RETURN n.`// identifier`\n"
        "/* outer /* inner */ tail */"
    )

    assert get_comment_syntax("Cypher") is get_comment_syntax("java")
    assert _matches("Cypher", source) == ["// line note", "/* outer /* inner */"]
    assert CommentSanitizer("Cypher").sanitize("/* block note */") == "block note"


def test_cypher_unclosed_blocks_and_operators_are_not_comments():
    assert _matches("Cypher", "RETURN left / right") == []
    assert _matches("Cypher", "MATCH (a)-->(b)") == []
    assert _matches("Cypher", "MATCH (n) /* unclosed") == []


def test_d2_extracts_structural_comments_and_masks_all_scalar_forms():
    source = (
        "# diagram note\n"
        "client -> server # path note\n"
        'quoted: "# literal and \\" data"\n'
        "single: '# literal'\n"
        "body: |md\n"
        "# block string data\n"
        '""" block string data\n'
        "|\n"
        '""" block note\nwith # payload\n"""\n'
        "# eof note"
    )

    assert _matches("D2", source) == [
        "# diagram note",
        "# path note",
        '""" block note\nwith # payload\n"""',
        "# eof note",
    ]


def test_d2_rejects_nonstructural_and_unclosed_triple_quotes():
    assert _matches("D2", 'node: """ not a map-node comment """') == []
    assert _matches("D2", '""" unclosed block') == []
    assert _matches("D2", '"" one or two quotes') == []

    sanitizer = CommentSanitizer("D2")
    assert sanitizer.sanitize("# line note") == "line note"
    assert sanitizer.sanitize('""" block note """') == "block note"


def test_daslang_exact_alias_preserves_nested_comment_contract():
    source = (
        'let marker = "/* literal */ // literal"\n'
        '#row,12,4,"// file marker"#\n'
        "var value = 1 // line note\n"
        "/* outer /* inner */ outer */\n"
        "left / right"
    )

    assert get_comment_syntax("Daslang") is get_comment_syntax("boogie")
    assert _matches("Daslang", source) == [
        "// line note",
        "/* outer /* inner */ outer */",
    ]
    assert CommentSanitizer("Daslang").sanitize("/* outer /* inner */ outer */") == (
        "outer /* inner */ outer"
    )


def test_daslang_rejects_stray_and_unclosed_block_delimiters():
    assert _matches("Daslang", "stray */ close") == []
    assert _matches("Daslang", "/* outer /* inner */") == []


def test_dotenv_extracts_only_parser_classified_hashes():
    source = (
        "\ufeff  # deployment note\n"
        "TOKEN=abc# token note\n"
        'HASH="abc#data" # double note\n'
        "SINGLE='abc#data'# single note\n"
        "BACK=`abc#data` # backtick note\n"
        "MULTI='line one\n"
        "# multiline data\n"
        "line three' # multiline note\n"
        "EMPTY=# empty note\n"
        "export EXPORTED=value# export note\n"
        "URL=https://host/a# fragment note\n"
        "invalid assignment # ignored"
    )

    assert _matches("Dotenv", source) == [
        "# deployment note",
        "# token note",
        "# double note",
        "# single note",
        "# backtick note",
        "# multiline note",
        "# empty note",
        "# export note",
        "# fragment note",
    ]


def test_dotenv_handles_escaped_quotes_unclosed_fallback_and_line_endings():
    source = (
        'DOUBLE="escaped \\" # data" # actual\r\n'
        "SINGLE='escaped \\' # data' # second\r"
        'BROKEN="value# fallback'
    )

    assert _matches("Dotenv", source) == ["# actual", "# second", "# fallback"]
    assert CommentSanitizer("Dotenv").sanitize("# actual") == "actual"
