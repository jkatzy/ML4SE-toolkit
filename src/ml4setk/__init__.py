"""Public package surface for the ML4SE toolkit."""

from .Datasets.ChunkedIterator import ChunkedIterator, ChunkResult
from .Generation.CausalInput import CausalInput
from .Generation.DenoisingInput import MaskedLMInput, SpanCorruptionInput
from .Generation.DiffusionInput import (
    DiffusionCompletionInput,
    DiffusionExpandingInfillInput,
    DiffusionInfillInput,
)
from .Generation.FIMInput import FIMInput
from .Generation.MultiTokenInput import MultiTokenInput
from .Generation.sentinels import (
    SentinelTokens,
    SpanTokens,
    get_mask_token,
    get_sentinel_tokens,
    get_span_tokens,
)
from .Parsing.Comments.CommentQuery import (
    CommentQuery,
    LineCommentQuery,
    NestedCommentQuery,
    OpeningCommentQuery,
    UnclosedCommentError,
    UnclosedCommentWarning,
)
from .Parsing.Comments.CommentSanitizer import (
    CommentSanitizer,
    sanitize_comment,
    sanitize_comment_text,
)
from .Parsing.Comments.registry import (
    CommentLanguageVersionWarning,
    UnsupportedCommentLanguageVersionError,
    comment_language_requires_version,
    get_comment_language_versions,
    get_default_comment_language_version,
    get_supported_comment_languages,
)
from .Parsing.Comments.unwrap import unwrap_comment
from .Parsing.Query import Query, QueryMatch

__all__ = [
    "CausalInput",
    "ChunkResult",
    "ChunkedIterator",
    "CommentLanguageVersionWarning",
    "CommentQuery",
    "CommentSanitizer",
    "DiffusionCompletionInput",
    "DiffusionExpandingInfillInput",
    "DiffusionInfillInput",
    "FIMInput",
    "LineCommentQuery",
    "MaskedLMInput",
    "MultiTokenInput",
    "NestedCommentQuery",
    "OpeningCommentQuery",
    "Query",
    "QueryMatch",
    "SentinelTokens",
    "SpanCorruptionInput",
    "SpanTokens",
    "UnclosedCommentError",
    "UnclosedCommentWarning",
    "UnsupportedCommentLanguageVersionError",
    "comment_language_requires_version",
    "get_comment_language_versions",
    "get_default_comment_language_version",
    "get_mask_token",
    "get_sentinel_tokens",
    "get_span_tokens",
    "get_supported_comment_languages",
    "sanitize_comment",
    "sanitize_comment_text",
    "unwrap_comment",
]

__version__ = "0.1.0"
