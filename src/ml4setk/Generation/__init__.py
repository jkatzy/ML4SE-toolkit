"""Input builders that turn parsed examples into model-ready samples."""

from .CausalInput import CausalInput
from .DenoisingInput import MaskedLMInput, SpanCorruptionInput
from .DiffusionInput import (
    DiffusionCompletionInput,
    DiffusionExpandingInfillInput,
    DiffusionInfillInput,
)
from .FIMInput import FIMInput
from .IterableQueryLoader import IterableQueryLoader
from .MultiTokenInput import MultiTokenInput
from .sentinels import (
    SentinelTokens,
    SpanTokens,
    get_mask_token,
    get_sentinel_tokens,
    get_span_tokens,
)

__all__ = [
    "CausalInput",
    "DiffusionCompletionInput",
    "DiffusionExpandingInfillInput",
    "DiffusionInfillInput",
    "FIMInput",
    "IterableQueryLoader",
    "MaskedLMInput",
    "MultiTokenInput",
    "SentinelTokens",
    "SpanCorruptionInput",
    "SpanTokens",
    "get_mask_token",
    "get_sentinel_tokens",
    "get_span_tokens",
]
