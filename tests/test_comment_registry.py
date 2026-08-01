import pytest

from ml4setk.Parsing.Comments import (
    SUPPORTED_LANGUAGES,
    CommentSyntax,
    get_comment_syntax,
    get_supported_comment_languages,
    iter_comment_syntaxes,
)

pytestmark = pytest.mark.unit


def test_comment_syntax_preserves_v0_0_2_positional_layout():
    syntax = CommentSyntax(
        "legacy_family",
        "legacy",
        ("legacy_alias",),
        (r"#.*",),
        (("/*", "*/"),),
        (),
        (),
        (),
        (),
        "https://example.test/comments",
        "legacy_parser.py",
        "verified",
        "Legacy positional construction.",
    )

    assert syntax.documentation_source == "https://example.test/comments"
    assert syntax.implementation_source == "legacy_parser.py"
    assert syntax.confidence == "verified"
    assert syntax.notes == "Legacy positional construction."
    assert syntax.contextual_extractor == ""
    assert syntax.sanitizer_line_wrappers == ()
    assert syntax.excluded_comment_prefixes == ()
    assert syntax.sanitizer_mode == "wrapped"


def test_supported_languages_are_sorted_and_resolvable():
    assert SUPPORTED_LANGUAGES == tuple(sorted(SUPPORTED_LANGUAGES))

    for language in SUPPORTED_LANGUAGES:
        syntax = get_comment_syntax(language)
        assert language in syntax.language_names


def test_supported_language_helper_returns_sorted_list_copy():
    languages = get_supported_comment_languages()

    assert isinstance(languages, list)
    assert languages == list(SUPPORTED_LANGUAGES)
    assert languages is not SUPPORTED_LANGUAGES


def test_registry_entries_seed_examples_for_each_implemented_feature():
    for syntax in iter_comment_syntaxes():
        if syntax.regex_patterns:
            assert syntax.shared_regex_examples or syntax.canonical_regex_examples

        if syntax.nested_delimiters:
            assert syntax.shared_nested_examples or syntax.canonical_nested_examples

        if syntax.contextual_extractor:
            assert (
                syntax.shared_contextual_examples
                or syntax.canonical_contextual_examples
            )


def test_registry_examples_use_known_kinds_and_consistent_generation_flags():
    known_kinds = {
        "line",
        "block",
        "nested",
        "ignored",
        "attribute",
        "textile",
        "cue_block",
        "directive",
        "contextual",
    }
    for syntax in iter_comment_syntaxes():
        for example in (
            *syntax.shared_regex_examples,
            *syntax.canonical_regex_examples,
            *syntax.shared_nested_examples,
            *syntax.canonical_nested_examples,
            *syntax.shared_contextual_examples,
            *syntax.canonical_contextual_examples,
        ):
            assert example.kind in known_kinds
            if example.grouped_line_compatible:
                assert example.kind == "line"


def test_registry_aliases_point_to_the_same_comment_syntax_entry():
    for syntax in iter_comment_syntaxes():
        for language in syntax.language_names:
            assert get_comment_syntax(language) is syntax


def test_registry_accepts_raw_stack_style_labels():
    assert get_comment_syntax("Cap'n Proto") is get_comment_syntax("cap_n_proto")
    assert get_comment_syntax("Graphviz (DOT)") is get_comment_syntax("graphviz_dot")
    assert get_comment_syntax("NetLinx+ERB") is get_comment_syntax("netlinx_plus_erb")
    assert get_comment_syntax("Objective-C++") is get_comment_syntax(
        "objective_c_plus_plus"
    )
    assert get_comment_syntax("Ragel in Ruby Host") is get_comment_syntax(
        "ragel_in_ruby_host"
    )
    assert get_comment_syntax("Ren'Py") is get_comment_syntax("ren_py")
    assert get_comment_syntax("Web Ontology Language") is get_comment_syntax(
        "web_ontology_language"
    )
    assert get_comment_syntax("Checksums") is get_comment_syntax("checksums")
    assert get_comment_syntax("Ecere_Projects") is get_comment_syntax(
        "ecere_projects"
    )
    assert get_comment_syntax("FIGlet_Font") is get_comment_syntax("figlet_font")
    assert get_comment_syntax(
        "Microsoft_Visual_Studio_Solution"
    ) is get_comment_syntax("microsoft_visual_studio_solution")
    assert get_comment_syntax("NL") is get_comment_syntax("nl")
    assert get_comment_syntax("Omgrofl") is get_comment_syntax("omgrofl")
    assert get_comment_syntax("PogoScript") is get_comment_syntax("pogoscript")


def test_public_key_aggregate_remains_unsupported():
    with pytest.raises(NotImplementedError):
        get_comment_syntax("Public_Key")
