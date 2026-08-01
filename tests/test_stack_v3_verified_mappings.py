import pytest

from ml4setk import CommentQuery, sanitize_comment
from ml4setk.Parsing.Comments import get_comment_syntax

pytestmark = pytest.mark.unit


def _matches(language: str, source: str) -> list[str]:
    return [match.match for match in CommentQuery(language).parse(source)]


@pytest.mark.parametrize(
    ("raw_label", "canonical_name", "family_name"),
    (
        ("F*", "f_star", "f_star_style"),
        ("Go Workspace", "go_module", "go_directive_file_style"),
        ("Gradle Kotlin DSL", "kotlin", "kotlin_style"),
        ("Lean 4", "lean", "lean_style"),
        ("Rocq Prover", "coq", "nested_star_style"),
        ("Visual Basic 6.0", "visual_basic_net", "apostrophe_style"),
    ),
)
def test_stack_v3_verified_raw_labels_resolve(
    raw_label: str,
    canonical_name: str,
    family_name: str,
):
    syntax = get_comment_syntax(raw_label)

    assert syntax.canonical_name == canonical_name
    assert syntax.family_name == family_name


def test_f_star_raw_label_preserves_nested_comment_contract():
    source = (
        'let marker = "(* not a comment"\n'
        "let x = 1 // line note\r\n"
        "(* outer (* inner *) outer *)\n"
        "(* unclosed"
    )

    assert _matches("F*", source) == [
        "// line note",
        "(* outer (* inner *) outer *)",
        "(* unclosed",
    ]
    assert sanitize_comment("F*", "(* body *)") == sanitize_comment("f_star", "(* body *)")


@pytest.mark.parametrize("raw_label", ("Genero 4gl", "Genero per", "iCalendar"))
def test_reviewed_deferred_or_unsupported_labels_raise(raw_label):
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        CommentQuery(raw_label)
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        sanitize_comment(raw_label, "# source data")


def test_go_workspace_only_accepts_slash_line_comments():
    source = 'use "./module//path"\r\n// workspace note\r\n/* rejected */\n'

    assert _matches("Go Workspace", source) == ["// workspace note"]
    assert sanitize_comment("Go Workspace", "// body") == sanitize_comment("go_module", "// body")


def test_gradle_kotlin_dsl_uses_nested_kotlin_blocks_and_masks_strings():
    source = (
        'val ordinary = "/* not a comment */"\n'
        'val raw = """\n/* still not a comment */\n"""\n'
        "// line note\n"
        "/** KDoc note */\n"
        "/* outer /* inner */ outer */\n"
        "/* unclosed"
    )

    assert _matches("Gradle Kotlin DSL", source) == [
        "// line note",
        "/** KDoc note */",
        "/* outer /* inner */ outer */",
    ]
    assert sanitize_comment("Gradle Kotlin DSL", "/* body */") == sanitize_comment(
        "kotlin", "/* body */"
    )


def test_lean_4_raw_label_preserves_nested_and_doc_comments():
    source = (
        'def marker := "/- not a comment"\n'
        "-- line note\n"
        "/-- doc note -/\n"
        "/- outer /- inner -/ outer -/\n"
        "/- unclosed"
    )

    assert _matches("Lean 4", source) == [
        "-- line note",
        "/-- doc note -/",
        "/- outer /- inner -/ outer -/",
    ]
    assert sanitize_comment("Lean 4", "/- body -/") == sanitize_comment("lean", "/- body -/")


def test_rocq_prover_raw_label_preserves_nested_comment_contract():
    source = (
        'Definition marker := "(* not a comment".\n'
        "*) stray closer\n"
        "(* outer (* inner *) outer *)\n"
        "(* unclosed"
    )

    assert _matches("Rocq Prover", source) == ["(* outer (* inner *) outer *)"]
    assert sanitize_comment("Rocq Prover", "(* body *)") == sanitize_comment("coq", "(* body *)")


def test_visual_basic_6_rem_requires_a_statement_boundary():
    source = (
        "Rem line note\r\n"
        "100 Rem numbered note\r\n"
        "value = 1: rEm colon note\r\n"
        "value = Rem + 1\r\n"
        "Remember = True\r\n"
        'text = "value: Rem string note \' note"\r\n'
        "' apostrophe note\r\n"
    )

    assert _matches("Visual Basic 6.0", source) == [
        "Rem line note",
        "Rem numbered note",
        "rEm colon note",
        "' apostrophe note",
    ]
    assert sanitize_comment("Visual Basic 6.0", "rEm body") == "body"
    assert sanitize_comment("Visual Basic 6.0", "' body") == "body"
