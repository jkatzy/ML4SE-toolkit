import pytest

from ml4setk import (
    CausalInput,
    DiffusionCompletionInput,
    DiffusionExpandingInfillInput,
    DiffusionInfillInput,
    FIMInput,
    MultiTokenInput,
    QueryMatch,
    SentinelTokens,
    get_mask_token,
    get_sentinel_tokens,
)
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


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("bigcode/starcoder2-3b", "<fim_prefix>p<fim_suffix>s<fim_middle>"),
        ("bigcode/santacoder", "<fim-prefix>p<fim-suffix>s<fim-middle>"),
        ("codellama/CodeLlama-7b-hf", "<PRE> p <SUF>s <MID>"),
        (
            "deepseek-ai/deepseek-coder-1.3b-base",
            "<｜fim▁begin｜>p<｜fim▁hole｜>s<｜fim▁end｜>",
        ),
        ("Qwen/Qwen2.5-Coder-7B", "<|fim_prefix|>p<|fim_suffix|>s<|fim_middle|>"),
        ("google/codegemma-2b", "<|fim_prefix|>p<|fim_suffix|>s<|fim_middle|>"),
        ("mistralai/Codestral-22B-v0.1", "[SUFFIX]s[PREFIX]p"),
    ],
)
def test_fim_input_from_model_name_uses_family_sentinels(name, expected):
    model_input, ground_truth = FIMInput.from_model(name).generate(QueryMatch("p", "s", "m"))

    assert model_input == expected
    assert ground_truth == "m"


def test_get_sentinel_tokens_reads_hf_model_name_and_model_type():
    class Config:
        def __init__(self, name, model_type):
            self._name_or_path = name
            self.model_type = model_type

    class Model:
        def __init__(self, name, model_type):
            self.name_or_path = name
            self.config = Config(name, model_type)

    assert get_sentinel_tokens(Model("Qwen/Qwen2.5-Coder-1.5B", "qwen2")).prefix == (
        "<|fim_prefix|>"
    )
    # A local fine-tune path is unknown, but its architecture is not.
    assert get_sentinel_tokens(Model("/ckpt/run-7", "starcoder2")).prefix == ("<fim_prefix>")


def test_get_sentinel_tokens_falls_back_to_tokenizer_vocab():
    class Tokenizer:
        name_or_path = "/ckpt/unknown"

        def __init__(self, vocab):
            self.vocab = vocab

        def get_vocab(self):
            return dict.fromkeys(self.vocab, 0)

    class Pipeline:
        tokenizer = Tokenizer(["<|fim_prefix|>", "<|fim_suffix|>", "<|fim_middle|>"])

    assert get_sentinel_tokens(Pipeline()) == SentinelTokens(
        "<|fim_prefix|>", "<|fim_suffix|>", "<|fim_middle|>"
    )
    # SentencePiece vocabularies store the CodeLlama markers with a "▁" prefix.
    assert get_sentinel_tokens(Tokenizer(["▁<PRE>", "▁<SUF>", "▁<MID>"])).prefix == ("<PRE> ")


def test_get_sentinel_tokens_rejects_unknown_models():
    with pytest.raises(ValueError, match="explicitly"):
        get_sentinel_tokens("gpt2")


def test_fim_input_rejects_unknown_order():
    with pytest.raises(ValueError):
        FIMInput("<pre>", "<suf>", "<mid>", order="mps")


class WordTokenizer:
    name_or_path = "/ckpt/unknown"

    def __init__(self, vocab=()):
        self.vocab = vocab

    def get_vocab(self):
        return dict.fromkeys(self.vocab, 0)

    def encode(self, text, add_special_tokens=True):
        assert not add_special_tokens
        return text.split()


def test_diffusion_inputs_place_masks_per_setting():
    match = QueryMatch("p ", " s", "a b c")

    assert DiffusionCompletionInput("<m>", num_masks=2).generate(match) == (
        "p <m><m>",
        "a b c",
    )
    assert DiffusionInfillInput("<m>", WordTokenizer()).generate(match) == (
        "p <m><m><m> s",
        "a b c",
    )
    assert DiffusionExpandingInfillInput("<m>", num_masks=1).generate(match) == (
        "p <m> s",
        "a b c",
    )


def test_diffusion_inputs_default_mask_counts():
    match = QueryMatch("", "", "m")

    assert DiffusionCompletionInput("<m>").generate(match)[0] == "<m>" * 128
    assert DiffusionExpandingInfillInput("<m>").generate(match)[0] == "<m>" * 4


@pytest.mark.parametrize("cls", [DiffusionCompletionInput, DiffusionExpandingInfillInput])
def test_diffusion_inputs_reject_empty_canvas(cls):
    with pytest.raises(ValueError):
        cls("<m>", num_masks=0)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("GSAI-ML/LLaDA-8B-Base", "<|mdm_mask|>"),
        ("Dream-org/Dream-Coder-v0-Instruct-7B", "<|mask|>"),
        ("Dream-org/DreamOn-v0-7B", "<|mask|>"),
        ("apple/DiffuCoder-7B-cpGRPO", "<|mask|>"),
    ],
)
def test_diffusion_input_from_model_name_uses_family_mask(name, expected):
    match = QueryMatch("p", "s", "m")

    assert DiffusionCompletionInput.from_model(name, num_masks=1).generate(match)[0] == (
        "p" + expected
    )
    assert DiffusionExpandingInfillInput.from_model(name, num_masks=1).generate(match)[0] == (
        "p" + expected + "s"
    )


def test_diffusion_infill_input_from_model_uses_tokenizer_for_length():
    match = QueryMatch("p", "s", "x y")
    tokenizer = WordTokenizer(["<|mdm_mask|>"])

    # A bare tokenizer supplies both the mask token (via its vocab) and the length.
    assert DiffusionInfillInput.from_model(tokenizer).generate(match)[0] == (
        "p<|mdm_mask|><|mdm_mask|>s"
    )
    assert (
        DiffusionInfillInput.from_model("Dream-org/Dream-v0-Base-7B", tokenizer).generate(match)[0]
        == "p<|mask|><|mask|>s"
    )


def test_get_mask_token_rejects_unknown_models():
    with pytest.raises(ValueError, match="explicitly"):
        get_mask_token("Qwen/Qwen2.5-Coder-7B")
