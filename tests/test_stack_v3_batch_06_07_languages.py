import pytest

from ml4setk import (
    CommentQuery,
    CommentSanitizer,
    LineCommentQuery,
    NestedCommentQuery,
    sanitize_comment,
    sanitize_comment_text,
)
from ml4setk.Comment_util.parse_comment import extract_comments
from ml4setk.Parsing.Comments import (
    get_comment_syntax,
    get_supported_comment_languages,
)

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
        ("Mojo", "mojo", "mojo_style"),
        ("OASv2-yaml", "yaml", "yaml_style"),
        ("NMODL", "nmodl", "nmodl_style"),
        ("Noir", "rust", "rust_style"),
        ("Nushell", "nushell", "nushell_style"),
        ("MoonBit", "moonbit", "moonbit_style"),
        ("OASv3-yaml", "yaml", "yaml_style"),
        ("OMNeT++ MSG", "omnet_plus_plus_msg", "omnet_plus_plus_msg_style"),
        ("OverpassQL", "java", "c_style"),
        ("Pact", "assembly", "semicolon_style"),
        ("OMNeT++ NED", "omnet_plus_plus_ned", "omnet_plus_plus_ned_style"),
        ("PDDL", "assembly", "semicolon_style"),
        ("Pip Requirements", "pip_requirements", "pip_requirements_style"),
        ("Polar", "dockerfile", "hash_line_style"),
        ("Praat", "praat", "praat_style"),
    ),
)
def test_batch_06_07_raw_labels_resolve(label, canonical, family):
    syntax = get_comment_syntax(label)

    assert syntax.canonical_name == canonical
    assert syntax.family_name == family


def test_mojo_masks_strings_docstrings_raw_and_interpolated_literals():
    source = (
        'var ordinary = "# literal"\n'
        'var raw = r"# raw literal"\n'
        'var interpolated = f"# interpolated literal"\n'
        'var docs = """\n# API docstring\n"""\n'
        "var value = 1 # inline note\r\n"
        "# ## Unicode note"
    )

    assert _matches("Mojo", source) == ["# inline note", "# ## Unicode note"]


def test_moonbit_excludes_headers_pragmas_and_literal_lines():
    source = (
        "//!build:wasm\n"
        'let url = "https://host/a//b"\n'
        "#| raw // literal\n"
        "$| interpolated // literal\n"
        "/// @coverage.skip\n"
        "/// @custom remains documentation\n"
        "fn one() -> Int { 1 } // ordinary\u2028"
        "///|"
    )

    assert _matches("MoonBit", source) == [
        "/// @custom remains documentation",
        "// ordinary",
        "///|",
    ]


def test_nushell_uses_item_boundaries_and_path_specific_cr_rules():
    source = (
        "#!/usr/bin/env nu\n"
        "let flake = nixpkgs#hello\n"
        "let raw = r#'path#fragment'#\n"
        'let quoted = "# literal"\n'
        "print $flake # inline\n"
        "[1 # compound\r2]\n"
        "# top-level\rcontinued\n"
        "# eof"
    )

    assert _matches("Nushell", source) == [
        "# inline",
        "# compound",
        "# top-level\rcontinued",
        "# eof",
    ]


def test_nmodl_handles_copy_modes_identifiers_and_all_three_forms():
    source = (
        'TITLE "https://host:443/?x"\n'
        "ONTOLOGY NCIT:C17145\n"
        "COMMENTARY is_an_identifier\n"
        "VERBATIM\n/* foreign */ // foreign : foreign ?\nENDVERBATIM\n"
        "SUFFIX demo : suffix note\n"
        "? own-line note\n"
        "COMMENT\nouter COMMENT text : ?\nENDCOMMENTED\n"
    )

    assert _matches("NMODL", source) == [
        ": suffix note",
        "? own-line note",
        "COMMENT\nouter COMMENT text : ?\nENDCOMMENT",
    ]


def test_nmodl_mixed_line_markers_group_and_malformed_copy_modes_do_not_leak():
    assert _matches("NMODL", ": first\n? second") == [": first\n? second"]
    assert _matches("NMODL", "COMMENT\n: hidden\n? hidden") == []
    assert _matches("NMODL", "VERBATIM\n: hidden\nENDCOMMENT") == []


def test_noir_and_rust_use_recursive_blocks_while_masking_noir_literals():
    source = (
        'let raw = r#"/* literal */ // literal"#;\n'
        'let ordinary = "// literal";\n'
        "/// outer docs\n"
        "fn main() { /* outer /* inner */ tail */ }\n"
        "// eof\rcontinued"
    )

    assert _matches("Noir", source) == [
        "/// outer docs",
        "/* outer /* inner */ tail */",
        "// eof\rcontinued",
    ]
    assert _matches("rust", "/* outer /* inner */ tail */") == ["/* outer /* inner */ tail */"]
    assert _matches("Noir", "/* unclosed") == []


@pytest.mark.parametrize("language", ("rust", "Noir"))
@pytest.mark.parametrize(
    "source",
    (
        '// " fake\nfn value() {}\n/* actual */',
        '/* r###" fake */\nfn value() {}\n/* actual */',
    ),
)
def test_rust_family_comment_prose_does_not_open_literal_ranges(language, source):
    expected_first = source.split("\n", 1)[0]
    expected_nested = (
        [expected_first, "/* actual */"] if source.startswith("/*") else ["/* actual */"]
    )

    assert _matches(language, source) == [expected_first, "/* actual */"]
    assert [match.match for match in NestedCommentQuery(language).parse(source)] == expected_nested


@pytest.mark.parametrize("language", ("Noir", "rust"))
def test_noir_exact_doc_lookahead_preserves_ordinary_payload_markers(language):
    assert _matches(language, "//// ordinary\n/***/") == [
        "//// ordinary",
        "/***/",
    ]
    assert CommentSanitizer(language).sanitize("//// ordinary") == "// ordinary"
    assert CommentSanitizer(language).sanitize("/***/") == "*"


@pytest.mark.parametrize("label", ("OASv2-yaml", "OASv3-yaml"))
def test_openapi_yaml_reuses_structural_yaml_comment_rules(label):
    source = (
        'openapi: "3.1#literal" # version note\n'
        "host: api.example.test#blue\n"
        "description: |\n"
        "  # scalar data\n"
        "# path note\n"
        "paths: {}"
    )

    assert _matches(label, source) == ["# version note", "# path note"]


@pytest.mark.parametrize("label", ("OMNeT++ MSG", "OMNeT++ NED"))
def test_omnet_modes_protect_quotes_and_property_values(label):
    source = (
        'string endpoint = "http://host/a//b"; // host note\n'
        "char slash = '/';\n"
        "@meta(url=http://host/a//b, nested=(x//y))\n"
        "// eof"
    )

    assert _matches(label, source) == ["// host note", "// eof"]


def test_omnet_msg_protects_embedded_cpp_and_malformed_modes():
    source = "cplusplus {{\n// embedded C++\n/* foreign */\n}}\n// MSG host note"

    assert _matches("OMNeT++ MSG", source) == ["// MSG host note"]
    assert _matches("OMNeT++ MSG", "@meta(url=http://x//y\n// hidden") == []
    assert _matches("OMNeT++ MSG", "cplusplus {{\n// hidden") == []


def test_overpassql_masks_quotes_and_uses_first_block_closer():
    source = (
        'node["url"="https://host/a//b"]; // line note\n'
        "node['text'='/* literal */'];\n"
        "/* outer /* inner */ tail */\n"
        "/* unclosed"
    )

    assert _matches("OverpassQL", source) == [
        "// line note",
        "/* outer /* inner */",
    ]


def test_pact_masks_strings_and_preserves_second_semicolon_payload():
    source = '(defconst note "semi;colon") ; suffix\n;; heading at EOF'

    assert _matches("Pact", source) == ["; suffix", ";; heading at EOF"]
    assert CommentSanitizer("Pact").sanitize(";; heading") == "; heading"


def test_pddl_alias_is_raw_semicolon_syntax():
    source = "(:requirements :strips) ; baseline\n;; temporal notes"

    assert _matches("PDDL", source) == ["; baseline", ";; temporal notes"]
    assert CommentSanitizer("PDDL").sanitize(";; temporal") == "; temporal"


def test_pip_requirements_uses_whitespace_not_quote_context():
    source = (
        "https://host/pkg.tgz#egg=pkg\n"
        'name==1 --config="value # still comment"\n'
        "other-package \\\n"
        "    # comment after continuation\n"
        "pkg==1 # pinned\n"
        "name#fragment"
    )

    assert _matches("Pip Requirements", source) == [
        '# still comment"',
        "# comment after continuation",
        "# pinned",
    ]


def test_polar_masks_escaped_strings_but_needs_no_space_before_hash():
    source = 'allow(user, "read\\"#literal", resource);# inline\r# ## heading'

    assert _matches("Polar", source) == ["# inline", "# ## heading"]


def test_praat_distinguishes_whole_line_markers_and_inline_semicolons():
    source = (
        "  # heading\n"
        "\t! implementation note\n"
        "; own-line semicolon\n"
        "values# = { 1, 2 }\n"
        'label$ = "semi; hash# bang! and ""quote"""\n'
        "curly$ = “semi; hash# bang!”\n"
        "ok = values# [1] != 0 ; verified\n"
        "x = ! value # inline data"
    )

    assert _matches("Praat", source) == [
        "# heading\n\t! implementation note\n; own-line semicolon",
        "; verified",
    ]


def test_praat_backslash_does_not_escape_a_straight_quote():
    assert _matches("Praat", 'label$ = "value\\" ; outside string') == ["; outside string"]


def test_nmodl_legacy_adapter_preserves_line_and_block_kinds():
    comments = extract_comments(": line note\nCOMMENT\nblock note\nENDCOMMENT", ["NMODL"])

    assert [(comment, kind) for _, comment, kind in comments] == [
        (": line note", "line"),
        ("COMMENT\nblock note\nENDCOMMENT", "block"),
    ]


@pytest.mark.parametrize(
    ("label", "raw_comment", "expected"),
    (
        ("Mojo", "# ## heading", "## heading"),
        ("MoonBit", "/// documentation", "documentation"),
        ("MoonBit", "///|", ""),
        ("Nushell", "# body # payload", "body # payload"),
        ("NMODL", ": body ? payload", "body ? payload"),
        ("NMODL", "COMMENT\nblock note\nENDCOMMENT", "block note"),
        ("Noir", "/* outer /* inner */ tail */", "outer /* inner */ tail"),
        ("OMNeT++ MSG", "// body", "body"),
        ("OMNeT++ NED", "// body", "body"),
        ("OverpassQL", "/* block note */", "block note"),
        ("Pip Requirements", "# body", "body"),
        ("Polar", "# ## heading", "## heading"),
        ("Praat", "! body", "body"),
    ),
)
def test_batch_06_07_sanitizer_contracts(label, raw_comment, expected):
    assert CommentSanitizer(label).sanitize(raw_comment) == expected


UNSUPPORTED_LABELS = (
    "Nu",
    "OASv2-json",
    "OASv3-json",
    "Oberon",
    "Option List",
    "Pkl",
)


@pytest.mark.parametrize("label", UNSUPPORTED_LABELS)
def test_deferred_and_unsupported_labels_raise_across_public_apis(label):
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        get_comment_syntax(label)
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        CommentQuery(label)
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        LineCommentQuery(label)
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        NestedCommentQuery(label)
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        CommentSanitizer(label)
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        sanitize_comment(label, "# source data")
    with pytest.raises(NotImplementedError, match="Unsupported language"):
        sanitize_comment_text(label, "# source data")

    assert label.lower().replace(" ", "_").replace("-", "_") not in (
        get_supported_comment_languages()
    )
    assert extract_comments("# source data", [label]) == []
