"""Focused extractor regressions from the all-language Stack v2 judge run."""

import pytest

from ml4setk import CommentQuery
from ml4setk.Parsing.Comments import get_comment_syntax

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("case_id", "expected_match", "following_source"),
    [
        pytest.param(
            "maxscript-line-75608d52788844f6",
            "-- align vertices to Grid",
            "\r$.alignToView #Vertex -- align vertices to View\r",
            id="maxscript-line-75608d52788844f6",
        ),
        pytest.param(
            "maxscript-line-fc05250a2d33c7e8",
            "--start animate\t",
            "\r\tsliderTime = 10f\r\tset animate on\r",
            id="maxscript-line-fc05250a2d33c7e8",
        ),
    ],
)
def test_maxscript_cr_only_line_boundaries(
    case_id: str,
    expected_match: str,
    following_source: str,
):
    source = expected_match + following_source

    first_match = CommentQuery("maxscript").parse(source)[0]

    assert case_id.startswith("maxscript-line-")
    assert first_match.prefix == ""
    assert first_match.match == expected_match


def test_solidity_line_085e7902f6597fe9_stops_at_carriage_return():
    expected_match = "// car Info"
    source = (
        expected_match
        + "\r    struct UserDetail{\r"
        + "        string ui_name; // user name\r"
        + "    }\r"
    )

    first_match = CommentQuery("solidity").parse(source)[0]

    assert len(expected_match) == 11
    assert first_match.prefix == ""
    assert first_match.match == expected_match


def test_yacc_line_4fcf0508f0dcbcea_stops_at_first_carriage_return():
    real_world_prefix = "//-/./2149;@A?>>AKQWY[]^^][Zakotz{"
    expected_match = real_world_prefix + ("x" * (16972 - len(real_world_prefix)))
    source = expected_match + "\rgrammar: token // following comment\r"

    first_match = CommentQuery("yacc").parse(source)[0]

    assert len(expected_match) == 16972
    assert first_match.prefix == ""
    assert first_match.match == expected_match


@pytest.mark.parametrize(
    ("language", "source", "expected_match"),
    [
        pytest.param(
            "m",
            "; valid M comment\rSET X=1",
            "; valid M comment",
            id="m-semicolon-syntax-remains-valid",
        ),
        pytest.param(
            "moocode",
            "/* valid MOO block comment */\rverb_code();",
            "/* valid MOO block comment */",
            id="moocode-c-block-syntax-remains-valid",
        ),
    ],
)
def test_m_and_moocode_valid_syntax_is_preserved(
    language: str,
    source: str,
    expected_match: str,
):
    assert CommentQuery(language).parse(source)[0].match == expected_match


def test_portugol_nested_d919ed77adf5953b_extracts_only_block_comment():
    expected_match = (
        "/*\n"
        "        Supondo que a população de um país A seja da ordem de 80000 habitantes \n"
        "        com uma taxa anual de crescimento de 3% \n"
        "        e que a população de B seja 200000 habitantes com uma taxa \n"
        "        de crescimento de 1.5%. \n"
        "        \n"
        "        Faça um programa que calcule e escreva \n"
        "        o número de anos necessários para que a população do país A \n"
        "        ultrapasse ou iguale a população do país B, \n"
        "        mantidas as taxas de crescimento.\n"
        "        \n"
        "        entrada -> nenhuma\n"
        "        saída   -> anos\n"
        "    */"
    )
    source = (
        "{\n    \n    "
        + expected_match
        + "\n    \n\tfuncao inicio() {\n\t    real popA = 80000.0\n\t}\n}"
    )

    matches = CommentQuery("portugol").parse(source)

    assert get_comment_syntax("portugol").family_name == "portugol_style"
    assert [(len(match.prefix), match.match) for match in matches] == [(11, expected_match)]


def test_portugol_nested_e9ed97501301c6ee_extracts_block_and_line_comments():
    expected_block = (
        "/*2. Um dado é lançado 10 vezes e o valor correspondente é anotado. Faça um "
        "programa\n"
        "que gere um vetor com os lançamentos, escreva esse vetor. A seguir determine e\n"
        "imprima a média aritmética dos lançamentos, contabilize e apresente também\n"
        "quantas foram as ocorrências da maior pontuação.\n"
        "*/"
    )
    expected_line = "//--> [0] [1] [2] [3] [4] [5] [6] [7] [8] [9] "
    source = (
        "{\r\n\t\r\n"
        + expected_block
        + "\n\tfuncao inicio()\r{\r\n\n\t\treal dados[10]"
        + expected_line
        + "\n\t\treal maiorPontuacao = 0.0\r\n\t}\r\n}"
    )

    matches = CommentQuery("portugol").parse(source)

    assert [(len(match.prefix), len(match.prefix) + len(match.match)) for match in matches] == [
        (6, 296),
        (334, 380),
    ]
    assert [match.match for match in matches] == [expected_block, expected_line]


PORTUGOL_F34A_LINE_COMMENTS = (
    (617, "// Coordenada X do círculo"),
    (662, "// Coordenada Y do círculo"),
    (706, "// Largura do retângulo"),
    (750, "// Coordenada X do ponto"),
    (793, "// Coordenada Y do ponto"),
    (844, "// Armazena a coordenada X inicial do retângulo"),
    (917, "// Armazena a coordenada Y inicial do retângulo"),
    (991, "// Armazena a coordenada X inicial do ponto"),
    (1060, "// Armazena a coordenada Y inicial do ponto\t"),
    (1866, "// Realiza a movimentação para cima"),
    (1969, "// Desfaz a movimentação para cima"),
    (2133, "// Realiza a movimentação para baixo"),
    (2237, "// Desfaz a movimentação para baixo"),
    (2437, "// Desfaz a movimentação para a esquerda"),
    (2545, "// Realiza a movimentação para a esquerda"),
    (2716, "// Realiza a movimentação para a direita"),
    (2824, "// Desfaz a movimentação para a direita"),
    (3014, "// Realiza a movimentação para cima"),
    (3117, "// Desfaz a movimentação para cima"),
    (3262, "// Realiza a movimentação para baixo"),
    (3366, "// Desfaz a movimentação para baixo"),
    (3543, "// Realiza a movimentação para cima"),
    (3646, "// Desfaz a movimentação para cima"),
    (3791, "// Realiza a movimentação para baixo"),
    (3895, "// Desfaz a movimentação para baixo"),
    (4204, "// Calcula o X do ponto central do retângulo 1"),
    (4281, "// Calcula o Y do ponto central do retângulo 1"),
    (4540, "// Calcula o coeficiente no eixo X"),
    (4634, "// Calcula o coeficiente no eixo Y"),
    (4940, "// Se o número for negativo, torna-o positivo"),
    (
        6155,
        "// Inverte o valor lógico da variável. Se for verdadeiro, se tornará falso. "
        "Se for falso, se tornará verdadeiro",
    ),
    (
        6475,
        "// Inverte o valor lógico da variável. Se for verdadeiro, se tornará falso. "
        "Se for falso, se tornará verdadeiro",
    ),
    (6982, "// Calcula a coordenada X1 da linha vertical"),
    (7049, "// Calcula a coordenada Y1 da linha vertical"),
    (7118, "// Calcula a coordenada X2 da linha vertical"),
    (7197, "// Calcula a coordenada Y2 da linha vertical"),
    (7265, "// Calcula a coordenada X1 da linha horizontal"),
    (7335, "// Calcula a coordenada Y1 da linha horizontal"),
    (7417, "// Calcula a coordenada X2 da linha horizontal"),
    (7487, "// Calcula a coordenada Y2 da linha horizontal"),
)


def _source_with_comments_at_offsets(
    comments: tuple[tuple[int, str], ...],
) -> str:
    parts = []
    cursor = 0
    for start, comment in comments:
        gap_length = start - cursor
        assert gap_length > 0
        if cursor:
            parts.append("\n" + ("x" * (gap_length - 1)))
        else:
            parts.append("x" * gap_length)
        parts.append(comment)
        cursor = start + len(comment)
    return "".join(parts) + "\n}"


def test_portugol_nested_f34a5a575ff0569c_extracts_all_40_line_comments():
    source = _source_with_comments_at_offsets(PORTUGOL_F34A_LINE_COMMENTS)

    matches = CommentQuery("portugol").parse(source)

    assert len(matches) == 40
    assert len(matches[0].prefix) == 617
    assert len(matches[-1].prefix) == 7487
    assert [match.match for match in matches] == [
        comment for _, comment in PORTUGOL_F34A_LINE_COMMENTS
    ]
    assert not matches[0].prefix.startswith("//")


def test_ignore_list_fc4e75a23a6d4074_preserves_escaped_hash_pattern():
    source = "*~\nauto-save-list/\n\\#*\n# actual comment\n.svn/\n"

    matches = CommentQuery("ignore_list").parse(source)

    assert [match.match for match in matches] == ["# actual comment"]
    assert matches[0].prefix.endswith("\\#*\n")


@pytest.mark.parametrize(
    ("source", "expected_matches"),
    [
        pytest.param("# comment\n*.log\n", ["# comment"], id="column-zero-comment"),
        pytest.param("*.log\n# second line\n", ["# second line"], id="later-line-comment"),
        pytest.param("\\#literal\n", [], id="escaped-column-zero-hash"),
        pytest.param(" #pattern-with-leading-space\n", [], id="indented-hash-pattern"),
        pytest.param("cache/#fragment\n", [], id="hash-later-in-pattern"),
    ],
)
def test_ignore_list_hash_boundary_exact_and_near_misses(
    source: str,
    expected_matches: list[str],
):
    assert [match.match for match in CommentQuery("ignore_list").parse(source)] == (
        expected_matches
    )


def test_applescript_shebang_is_not_a_hash_comment():
    source = (
        "#!/usr/bin/osascript\n"
        "-- actual dash comment\n"
        "# actual hash comment\n"
        "#! later hash comment\n"
    )

    assert [match.match for match in CommentQuery("applescript").parse(source)] == [
        "-- actual dash comment",
        "# actual hash comment\n#! later hash comment",
    ]


def test_tcsh_line_c04cf242730c0844_excludes_only_the_initial_shebang():
    source = (
        "#!/bin/csh -f\n"
        "#+\n"
        "# KCWI library of scripts\n"
        "#\n"
        "# NAME\n"
        "#\tkcwiArrangeGuis - Arrange guis\n"
        "#-\n"
        "echo ready\n"
        "#! later hash comment\n"
    )

    assert [match.match for match in CommentQuery("tcsh").parse(source)] == [
        "#+\n# KCWI library of scripts\n#\n# NAME\n#\tkcwiArrangeGuis - Arrange guis",
        "#-",
        "#! later hash comment",
    ]


def test_tcsh_hashbang_near_miss_away_from_byte_zero_remains_a_comment():
    source = "\n#!/usr/bin/env tcsh\n# next comment\n"

    assert [match.match for match in CommentQuery("tcsh").parse(source)] == [
        "#!/usr/bin/env tcsh\n# next comment"
    ]


def test_haskell_8d107f4c38793fe3_arrow_operator_is_not_a_comment():
    source = "(-->) value = transform value\n-- actual comment\n"

    assert [match.match for match in CommentQuery("haskell").parse(source)] == ["-- actual comment"]


def test_sql_executable_directive_is_not_a_block_comment():
    source = (
        "/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n"
        "/* ordinary block comment */\n"
        "-- actual line comment\n"
    )

    assert [match.match for match in CommentQuery("sql").parse(source)] == [
        "/* ordinary block comment */",
        "-- actual line comment",
    ]


@pytest.mark.parametrize("language", ["c", "reason", "reasonml"])
def test_re2c_generator_block_is_not_a_source_comment(language: str):
    source = '/*!re2c\n\t<a> "a" {}\n*/\n/* ordinary block comment */\n'

    assert [match.match for match in CommentQuery(language).parse(source)] == [
        "/* ordinary block comment */"
    ]


@pytest.mark.parametrize(
    "language",
    [
        "java",
        "dart",
        "javascript",
        "c++",
        "supercollider",
        "cameligo",
        "reason_ligo",
        "wren",
    ],
)
def test_re2c_like_block_remains_a_comment_in_other_family_dialects(
    language: str,
):
    source = '/*!re2c\n\t<a> "a" {}\n*/\n'

    assert [match.match for match in CommentQuery(language).parse(source)] == [source.rstrip("\n")]


@pytest.mark.parametrize("language", ["sparql", "turtle"])
def test_rdf_iri_fragment_terminator_is_not_a_hash_comment(language: str):
    source = (
        "PREFIX ex: <http://example.test/ns#>\n"
        "<http://example.test/subject#item> ex:value 1 . # actual comment\n"
    )

    assert [match.match for match in CommentQuery(language).parse(source)] == ["# actual comment"]


@pytest.mark.parametrize("language", ["sparql", "turtle"])
def test_rdf_hash_comment_near_iri_boundary_remains_valid(language: str):
    source = "#> standalone comment\n<http://example.test/ns#item> # second comment\n"

    assert [match.match for match in CommentQuery(language).parse(source)] == [
        "#> standalone comment",
        "# second comment",
    ]


@pytest.mark.parametrize("language", ["sparql", "turtle"])
def test_rdf_iri_unicode_escapes_protect_fragments(language: str):
    source = (
        r"<http://example.test/\u0061#short> <http://example.test/\U0001F600#long> ."
        "\n# actual comment\n"
    )

    assert [match.match for match in CommentQuery(language).parse(source)] == ["# actual comment"]


@pytest.mark.parametrize(
    ("language", "illegal_escape"),
    [
        ("sparql", r"\q"),
        ("turtle", r"\u12xz"),
        ("sparql", r"\U00110000"),
        ("turtle", r"\uD800"),
    ],
)
def test_rdf_iri_illegal_backslash_escape_does_not_protect_fragment(
    language: str,
    illegal_escape: str,
):
    source = f"<http://example.test/{illegal_escape}#invalid-fragment>\n# actual comment\n"

    assert [match.match for match in CommentQuery(language).parse(source)] == [
        "#invalid-fragment>",
        "# actual comment",
    ]


def test_smalltalk_multiline_comment_requires_its_closing_quote():
    expected = (
        '"This will pack a pointer to a certain arity. \n'
        "The explanation continues on the next physical line.\n"
        '"'
    )
    source = expected + "\n| rolledPointer |\n"

    assert [match.match for match in CommentQuery("smalltalk").parse(source)] == [expected]


def test_smalltalk_line_748e879082b2cb10_xml_quotes_inside_string_are_not_comments():
    source = (
        "icons-import\n"
        "iconCircle\n"
        "\t^ self fromCache: #iconCircle ifAbsentPut: "
        '[\'<?xml version="1.0" encoding="utf-8"?>\n'
        '<svg width="1792" viewBox="0 0 1792 1792" '
        'xmlns="http://www.w3.org/2000/svg"><path fill="#fff"/></svg>\']\n'
    )

    assert CommentQuery("smalltalk").parse(source) == []


def test_smalltalk_literals_preserve_real_comments_and_doubled_apostrophes():
    source = (
        '"real comment with an apostrophe: don\'t"\n'
        "label := 'it''s a multiline string\n"
        'whose XML attribute is "not-a-comment"\'.\n'
        'quote := $".\n'
        '"second real comment"\n'
    )

    assert [match.match for match in CommentQuery("smalltalk").parse(source)] == [
        '"real comment with an apostrophe: don\'t"',
        '"second real comment"',
    ]


def test_genero_forms_block_c2731952d8a3345f_screen_body_is_not_a_comment():
    source = (
        "screen  \n"
        "{\n"
        "                                                                              \n"
        "\n"
        " *** PROCESO REQUIERE CLAVE DE ACCESO ****\n"
        "\n"
        "       DIGITE SU CLAVE: [c001      ]\n"
        "\n"
        "}\n"
        "end\n"
        "attributes\n"
        "c001 = formonly.clave, INVISIBLE, REVERSE, COLOR=CYAN;\n"
    )

    assert CommentQuery("genero_forms").parse(source) == []


def test_genero_forms_screen_context_preserves_genuine_brace_comments():
    source = (
        "{ genuine form header comment }\n"
        "screen\n"
        "{\n"
        "  Item: [c001]\n"
        "}\n"
        "display screen\n"
        "{ genuine comment after a different statement }\n"
        "-- actual line comment\n"
    )

    assert [match.match for match in CommentQuery("genero_forms").parse(source)] == [
        "{ genuine form header comment }",
        "{ genuine comment after a different statement }",
        "-- actual line comment",
    ]
