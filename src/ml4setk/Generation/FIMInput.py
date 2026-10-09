from .AbstractInput import AbstractInput, unpack_query_match
from .sentinels import get_sentinel_tokens


class FIMInput(AbstractInput):
    def __init__(self, FIM_PREFIX, FIM_SUFFIX, FIM_MIDDLE, order="psm"):
        if order not in ("psm", "spm"):
            raise ValueError("order must be 'psm' or 'spm'.")

        self.FIM_PREFIX = FIM_PREFIX
        self.FIM_SUFFIX = FIM_SUFFIX
        self.FIM_MIDDLE = FIM_MIDDLE
        self.order = order

    @classmethod
    def from_model(cls, model):
        """Build a FIMInput using the sentinel tokens of a model name or HF object."""

        tokens = get_sentinel_tokens(model)
        return cls(tokens.prefix, tokens.suffix, tokens.middle, order=tokens.order)

    def generate(self, query_tuple):
        prefix, suffix, middle = unpack_query_match(query_tuple)

        prefix_part = self.FIM_PREFIX + prefix
        suffix_part = self.FIM_SUFFIX + suffix
        if self.order == "spm":
            text = suffix_part + prefix_part + self.FIM_MIDDLE
        else:
            text = prefix_part + suffix_part + self.FIM_MIDDLE
        return text, middle
