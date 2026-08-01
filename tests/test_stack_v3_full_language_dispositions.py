import pytest

from ml4setk import CommentQuery, CommentSanitizer, sanitize_comment
from ml4setk.Parsing.Comments import get_comment_syntax

pytestmark = pytest.mark.unit

DATASET_ID = "HuggingFaceCode/stack-v3-full"
DATASET_REVISION = "716a043a6c2adc34a2032b159364908a09ffe4ec"
FULL_STATS_SHA256 = "804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45"

ALIAS_LABELS = (
    "BibTeX Style",
    "Cypher",
    "Daslang",
    "Dune",
    "Ecmarkup",
    "EdgeQL",
    "F*",
    "FIRRTL",
    "Go Workspace",
    "Hare",
    "HIP",
    "Hosts File",
    "ISPC",
    "KerboScript",
    "Koka",
    "Lean 4",
    "Luau",
    "MiniZinc Data",
    "Noir",
    "OASv2-yaml",
    "OASv3-yaml",
    "OverpassQL",
    "Pact",
    "PDDL",
    "Polar",
    "Rocq Prover",
    "Sway",
    "Tact",
    "Untyped Plutus Core",
    "Visual Basic 6.0",
    "Xmake",
    "Zmodel",
)

CONTEXTUAL_LABELS = (
    "Answer Set Programming",
    "BQN",
    "BuildStream",
    "Caddyfile",
    "Cairo Zero",
    "Clue",
    "Cylc",
    "D2",
    "Dotenv",
    "Edge",
    "Glimmer JS",
    "Glimmer TS",
    "Godot Resource",
    "Imba",
    "Java Template Engine",
    "JCL",
    "Just",
    "KDL",
    "Kickstart",
    "MDX",
    "Mermaid",
    "Mojo",
    "MoonBit",
    "Nushell",
    "OMNeT++ MSG",
    "OMNeT++ NED",
    "Pip Requirements",
    "Praat",
    "RBS",
    "Rez",
    "Roc",
    "Sail",
    "Scenic",
    "Slang",
    "Slint",
    "Smithy",
    "Snakemake",
    "Survex data",
    "Terraform Template",
    "TextGrid",
    "Toit",
    "Tor Config",
    "Tree-sitter Query",
    "TypeSpec",
    "Typst",
    "mdsvex",
    "templ",
)

SEPARATE_FAMILY_LABELS = (
    "Aiken",
    "B4X",
    "Bluespec BH",
    "Carbon",
    "Circom",
    "GDShader",
    "Gradle Kotlin DSL",
    "Ink",
    "Leo",
    "Linear Programming",
    "LiveCode Script",
    "MiniZinc",
    "Pyret",
    "RON",
    "Vento",
    "WebAssembly Interface Type",
    "WGSL",
    "crontab",
)

IMPLEMENT_LABELS = (
    "NMODL",
    "Simple File Verification",
)

DEFERRED_LABELS = (
    "Befunge",
    "Genero 4gl",
    "Genero per",
    "Jai",
    "M3U",
    "Oberon",
    "Option List",
    "Pkl",
    "QuickBASIC",
    "Sweave",
    "TL-Verilog",
)

UNSUPPORTED_LABELS = (
    "C-ObjDump",
    "Cpp-ObjDump",
    "D-ObjDump",
    "Darcs Patch",
    "Gemini",
    "OASv2-json",
    "OASv3-json",
    "Python traceback",
    "TSPLIB data",
    "iCalendar",
    "vCard",
)

SUPPORTED_REVIEWED_LABELS = (
    *ALIAS_LABELS,
    *CONTEXTUAL_LABELS,
    *SEPARATE_FAMILY_LABELS,
    *IMPLEMENT_LABELS,
)
REJECTED_REVIEWED_LABELS = (*DEFERRED_LABELS, *UNSUPPORTED_LABELS)
ALL_REVIEWED_LABELS = (*SUPPORTED_REVIEWED_LABELS, *REJECTED_REVIEWED_LABELS)


def test_stack_v3_full_review_disposition_is_complete_and_collision_free():
    assert DATASET_ID == "HuggingFaceCode/stack-v3-full"
    assert len(DATASET_REVISION) == 40
    assert len(FULL_STATS_SHA256) == 64
    assert len(ALIAS_LABELS) == 32
    assert len(CONTEXTUAL_LABELS) == 47
    assert len(SEPARATE_FAMILY_LABELS) == 18
    assert len(IMPLEMENT_LABELS) == 2
    assert len(DEFERRED_LABELS) == 11
    assert len(UNSUPPORTED_LABELS) == 11
    assert len(ALL_REVIEWED_LABELS) == 121
    assert len(set(ALL_REVIEWED_LABELS)) == len(ALL_REVIEWED_LABELS)


@pytest.mark.parametrize("label", SUPPORTED_REVIEWED_LABELS)
def test_stack_v3_full_accepted_label_resolves_across_public_apis(label):
    syntax = get_comment_syntax(label)
    query = CommentQuery(label)

    assert syntax.language_names
    assert query.parse("") == []
    assert query.contains("") is False
    assert CommentSanitizer(label).syntax is syntax
    assert sanitize_comment(label, "candidate payload") == "candidate payload"


@pytest.mark.parametrize("label", REJECTED_REVIEWED_LABELS)
def test_stack_v3_full_rejected_label_stays_explicitly_unsupported(label):
    for operation in (
        lambda: get_comment_syntax(label),
        lambda: CommentQuery(label),
        lambda: CommentSanitizer(label),
        lambda: sanitize_comment(label, "# // /* candidate */"),
    ):
        with pytest.raises(NotImplementedError, match="Unsupported language"):
            operation()
