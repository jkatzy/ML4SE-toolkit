import importlib

import pytest

from ml4setk import CommentQuery, FIMInput


@pytest.mark.integration
def test_public_modules_import():
    for module_name in [
        "ml4setk",
        "ml4setk.Generation",
        "ml4setk.Parsing",
        "ml4setk.Parsing.Code",
        "ml4setk.Parsing.Comments",
    ]:
        importlib.import_module(module_name)


@pytest.mark.integration
def test_comment_query_feeds_fim_input():
    sample = "prefix\n// note\nsuffix"
    match = CommentQuery("java").parse(sample)[0]

    model_input, ground_truth = FIMInput("<pre>", "<suf>", "<mid>").generate(match)

    assert model_input == "<pre>prefix\n<suf>\nsuffix<mid>"
    assert ground_truth == "// note"
