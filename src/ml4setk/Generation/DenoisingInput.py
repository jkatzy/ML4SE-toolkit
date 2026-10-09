"""Inputs for denoising pretrained models: BERT-style masked LMs and
T5-style span corruption."""

from .AbstractInput import AbstractInput, unpack_query_match
from .DiffusionInput import DiffusionInfillInput
from .sentinels import get_span_tokens


class MaskedLMInput(DiffusionInfillInput):
    """``prefix + one mask per ground-truth token + suffix`` for encoder MLMs
    such as CodeBERT, GraphCodeBERT, UniXcoder and ModernBERT.

    Each mask predicts exactly one token, so the layout is the oracle-length
    infill of :class:`DiffusionInfillInput`; the tokenizer adds ``[CLS]`` and
    ``[SEP]`` (or ``<s>`` and ``</s>``) itself.
    """


class SpanCorruptionInput(AbstractInput):
    """``mode + prefix + sentinel + suffix`` for encoder-decoder models trained
    with span corruption, such as T5, CodeT5, CodeT5+ and UL2.

    The decoder answers with ``sentinel + span`` (and, for T5, a closing
    ``<extra_id_1>``), so one sentinel stands for the whole target.
    """

    def __init__(self, sentinel="<extra_id_0>", mode=""):
        self.sentinel = sentinel
        self.mode = mode

    @classmethod
    def from_model(cls, model):
        """Build the input using the span tokens of a model name or HF object."""

        tokens = get_span_tokens(model)
        return cls(tokens.sentinel, mode=tokens.mode)

    def generate(self, query_match):
        prefix, suffix, middle = unpack_query_match(query_match)

        return self.mode + prefix + self.sentinel + suffix, middle
