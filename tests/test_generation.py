import pytest

from ml4setk import CausalInput, FIMInput, MultiTokenInput, QueryMatch
from ml4setk.Generation.AbstractInput import unpack_query_match

pytestmark = pytest.mark.unit


def test_unpack_query_match_accepts_named_tuple_and_plain_tuple():
    match = QueryMatch("prefix", "suffix", "match")

    assert unpack_query_match(match) == ("prefix", "suffix", "match")
    assert unpack_query_match(("prefix", "suffix", "match")) == (
        "prefix",
        "suffix",
        "match",
    )


def test_unpack_query_match_rejects_invalid_input():
    with pytest.raises(TypeError):
        unpack_query_match(("prefix", "suffix"))


def test_fim_input_uses_normalized_query_contract():
    match = QueryMatch("prefix", "suffix", "comment")

    model_input, ground_truth = FIMInput("<pre>", "<suf>", "<mid>").generate(match)

    assert model_input == "<pre>prefix<suf>suffix<mid>"
    assert ground_truth == "comment"


def test_causal_input_uses_normalized_query_contract():
    match = QueryMatch("prefix", "suffix", "comment")

    assert CausalInput().generate(match) == ("prefix", "comment")


def test_multi_token_input_returns_independent_context_snapshots():
    class ToyTokenizer:
        def encode(self, text):
            return [ord(character) for character in text]

    result = MultiTokenInput(ToyTokenizer()).generate("ab", "cd")

    assert result == [
        ([97, 98], 99),
        ([97, 98, 99], 100),
    ]
