"""Inputs for masked diffusion LLMs such as LLaDA, Dream(-Coder), DiffuCoder and DreamOn.

Instead of sentinel tokens, these models see the target as a run of mask
tokens that they denoise in place. The three formats differ only in where the
masks go and how many there are.
"""

from .AbstractInput import AbstractInput, unpack_query_match
from .sentinels import get_mask_token


class _MaskedInput(AbstractInput):
    keep_suffix = True
    multi_span = True

    def __init__(self, mask_token, num_masks):
        if num_masks < 1:
            raise ValueError("num_masks must be at least 1.")
        self.mask_token = mask_token
        self.num_masks = num_masks

    @classmethod
    def from_model(cls, model, **kwargs):
        """Build the input using the mask token of a model name or HF object."""

        return cls(get_mask_token(model), **kwargs)

    def _count(self, middle):
        return self.num_masks

    def generate(self, query_match):
        prefix, suffix, middle = unpack_query_match(query_match)

        masks = self.mask_token * self._count(middle)
        return prefix + masks + (suffix if self.keep_suffix else ""), middle

    def _join_spans(self, segments, middles):
        masks = [self.mask_token * self._count(middle) for middle in middles]
        return "".join(s + m for s, m in zip(segments, masks + [""]))


class DiffusionCompletionInput(_MaskedInput):
    """``prefix + num_masks masks``: the suffix is dropped, as in LLaDA's
    ``generate`` (default ``gen_length=128``) and Dream's ``diffusion_generate``."""

    keep_suffix = False
    multi_span = False

    def __init__(self, mask_token, num_masks=128):
        super().__init__(mask_token, num_masks)


class DiffusionInfillInput(_MaskedInput):
    """``prefix + one mask per ground-truth token + suffix`` (oracle length)."""

    def __init__(self, mask_token, tokenizer):
        self.mask_token = mask_token
        self.tokenizer = tokenizer

    @classmethod
    def from_model(cls, model, tokenizer=None):
        """Build the input from a tokenizer, or from a model name plus ``tokenizer``."""

        return cls(get_mask_token(model), tokenizer or model)

    def _count(self, middle):
        return len(self.tokenizer.encode(middle, add_special_tokens=False))


class DiffusionExpandingInfillInput(_MaskedInput):
    """``prefix + num_masks masks + suffix``: a small starting canvas that a
    variable-length model such as DreamOn grows or shrinks while decoding."""

    def __init__(self, mask_token, num_masks=4):
        super().__init__(mask_token, num_masks)
