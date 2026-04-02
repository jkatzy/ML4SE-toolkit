import pytest

import ml4setk
from ml4setk import (
    CommentQuery,
    CommentSanitizer,
    FIMInput,
    OpeningCommentQuery,
    QueryMatch,
    get_supported_comment_languages,
    sanitize_comment_text,
)
from ml4setk.Parsing.Code import TreeSitterQuery


def test_root_package_exports_stable_public_symbols():
    assert ml4setk.QueryMatch is QueryMatch
    assert ml4setk.CommentQuery is CommentQuery
    assert ml4setk.CommentSanitizer is CommentSanitizer
    assert ml4setk.OpeningCommentQuery is OpeningCommentQuery
    assert ml4setk.FIMInput is FIMInput
    assert ml4setk.get_supported_comment_languages is get_supported_comment_languages
    assert ml4setk.sanitize_comment_text is sanitize_comment_text


@pytest.mark.unit
def test_tree_sitter_dependency_error_is_deferred_until_instantiation():
    try:
        TreeSitterQuery("python")
    except ModuleNotFoundError as exc:
        assert "uv sync --group dev --extra treesitter" in str(exc)
    else:
        pytest.skip("tree_sitter_languages is installed in this environment.")
