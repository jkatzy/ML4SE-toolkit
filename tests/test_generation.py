import pytest

from ml4setk import (
    CausalInput,
    DiffusionCompletionInput,
    DiffusionExpandingInfillInput,
    DiffusionInfillInput,
    FIMInput,
    MaskedLMInput,
    MultiTokenInput,
    QueryMatch,
    SentinelTokens,
    SpanCorruptionInput,
    SpanTokens,
    get_mask_token,
    get_sentinel_tokens,
    get_span_tokens,
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
        ("facebook/incoder-1B", "p<|mask:0|>s<|mask:1|><|mask:0|>"),
        ("Salesforce/codegen25-7b-multi_P", "p<mask_1>s<|endoftext|><sep><mask_1>"),
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


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("microsoft/codebert-base-mlm", "<mask>"),
        ("microsoft/graphcodebert-base", "<mask>"),
        ("microsoft/unixcoder-base", "<mask>"),
        ("FacebookAI/roberta-base", "<mask>"),
        ("answerdotai/ModernBERT-base", "[MASK]"),
        ("google-bert/bert-base-uncased", "[MASK]"),
    ],
)
def test_masked_lm_input_uses_family_mask_and_oracle_length(name, expected):
    match = QueryMatch("p ", " s", "a b")

    assert MaskedLMInput.from_model(name, WordTokenizer()).generate(match) == (
        "p " + expected * 2 + " s",
        "a b",
    )


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Salesforce/codet5-base", "p<extra_id_0>s"),
        ("Salesforce/codet5p-220m", "p<extra_id_0>s"),
        ("google/ul2", "[NLU] p<extra_id_0>s"),
        ("google/flan-ul2", "p<extra_id_0>s"),
        ("microsoft/unixcoder-base", "p<mask0>s"),
    ],
)
def test_span_corruption_input_from_model_name_uses_family_tokens(name, expected):
    assert SpanCorruptionInput.from_model(name).generate(QueryMatch("p", "s", "m")) == (
        expected,
        "m",
    )


def test_span_corruption_input_defaults_and_tokenizer_fallback():
    match = QueryMatch("p", "s", "m")

    assert SpanCorruptionInput().generate(match) == ("p<extra_id_0>s", "m")
    assert SpanCorruptionInput("<s0>", mode="[M] ").generate(match)[0] == "[M] p<s0>s"
    assert get_span_tokens(WordTokenizer(["<mask0>"])) == SpanTokens("<mask0>")


def test_get_span_tokens_rejects_unknown_models():
    with pytest.raises(ValueError, match="explicitly"):
        get_span_tokens("bigcode/starcoder2-3b")


SOURCE = "a = 1  # one\nb = 2  # two\nc = 3  # three\n"


def _comment_matches():
    matches = []
    for comment in ("# one", "# two", "# three"):
        start = SOURCE.index(comment)
        end = start + len(comment)
        matches.append(QueryMatch(SOURCE[:start], SOURCE[end:], comment))
    return matches


def test_generate_many_single_span_format_returns_one_pair_per_match():
    fim = FIMInput("<pre>", "<suf>", "<mid>")
    matches = _comment_matches()

    pairs = fim.generate_many(matches)

    assert pairs == [fim.generate(match) for match in matches]
    assert [truth for _, truth in pairs] == ["# one", "# two", "# three"]


@pytest.mark.parametrize(
    ("select", "expected"),
    [
        ([2, 0, 0], ["# one", "# three"]),
        ([-1], ["# three"]),
        (lambda match: "t" in match.match, ["# two", "# three"]),
        (0, []),
    ],
)
def test_generate_many_selects_indices_or_predicate(select, expected):
    pairs = CausalInput().generate_many(_comment_matches(), select=select)

    assert [truth for _, truth in pairs] == expected


def test_generate_many_samples_count_reproducibly_in_source_order():
    matches = _comment_matches()

    first = CausalInput().generate_many(matches, select=2, seed=7)

    assert first == CausalInput().generate_many(matches, select=2, seed=7)
    assert len(first) == 2
    assert [m.match for m in matches if (m.prefix, m.match) in first] == [t for _, t in first]


def test_generate_many_masks_all_spans_in_one_masked_input():
    masked = DiffusionExpandingInfillInput("<m>", num_masks=2)

    assert masked.generate_many(_comment_matches(), select=[0, 2]) == [
        (
            "a = 1  <m><m>\nb = 2  # two\nc = 3  <m><m>\n",
            ["# one", "# three"],
        )
    ]


def test_generate_many_uses_one_mask_per_token_for_masked_lm():
    class CharTokenizer:
        def encode(self, text, add_special_tokens=True):
            return list(text)

    masked = MaskedLMInput("<m>", CharTokenizer())

    ((model_input, truths),) = masked.generate_many(_comment_matches()[:2])

    assert model_input == "a = 1  " + "<m>" * 5 + "\nb = 2  " + "<m>" * 5 + "\nc = 3  # three\n"
    assert truths == ["# one", "# two"]


def test_generate_many_numbers_span_corruption_sentinels():
    span = SpanCorruptionInput(mode="[NLU] ")

    ((model_input, truths),) = span.generate_many(reversed(_comment_matches()))

    assert model_input == ("[NLU] a = 1  <extra_id_0>\nb = 2  <extra_id_1>\nc = 3  <extra_id_2>\n")
    assert truths == ["# one", "# two", "# three"]
    assert SpanCorruptionInput("<mask0>").generate_many(_comment_matches()[:2])[0][0] == (
        "a = 1  <mask0>\nb = 2  <mask1>" + "\nc = 3  # three\n"
    )


def test_generate_many_completion_masks_each_match_separately():
    completion = DiffusionCompletionInput("<m>", num_masks=1)

    pairs = completion.generate_many(_comment_matches())

    assert pairs[1] == ("a = 1  # one\nb = 2  <m>", "# two")
    assert completion.generate_many([]) == []
    assert SpanCorruptionInput().generate_many(_comment_matches(), select=[]) == []


@pytest.mark.parametrize(
    ("matches", "fmt", "message"),
    [
        (
            [QueryMatch("a ", "", "bc"), QueryMatch("a b", "", "c")],
            DiffusionExpandingInfillInput("<m>"),
            "overlap",
        ),
        (
            [QueryMatch("a", "", "b"), QueryMatch("x", "", "y")],
            DiffusionExpandingInfillInput("<m>"),
            "same source",
        ),
        (
            [QueryMatch("", " b", "a"), QueryMatch("a ", "", "b")],
            SpanCorruptionInput("<mask>"),
            "number",
        ),
    ],
)
def test_generate_many_rejects_spans_it_cannot_mask_together(matches, fmt, message):
    with pytest.raises(ValueError, match=message):
        fmt.generate_many(matches)


def test_generate_many_rejects_out_of_range_selection():
    with pytest.raises(IndexError):
        CausalInput().generate_many(_comment_matches(), select=[3])
    with pytest.raises(ValueError):
        CausalInput().generate_many(_comment_matches(), select=4)
