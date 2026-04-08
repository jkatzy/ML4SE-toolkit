import pytest

from ml4setk.Parsing.Query import QueryMatch

pytestmark = [pytest.mark.integration, pytest.mark.optional_dependency]


def test_tree_sitter_query_finds_python_comments():
    pytest.importorskip("tree_sitter_languages")

    from ml4setk.Parsing.Code import TreeSitterQuery

    query = TreeSitterQuery("python")
    sample = "x = 1\n# note\n"

    matches = query.parse(sample, "(comment) @comment")

    assert query.contains(sample, "(comment) @comment") is True
    assert matches == [QueryMatch("x = 1\n", "\n", "# note")]
