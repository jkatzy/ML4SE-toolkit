"""Comment-oriented query implementations."""

from .CommentQuery import (
    CommentQuery,
    LineCommentQuery,
    NestedCommentQuery,
    OpeningCommentQuery,
)
from .registry import (
    SUPPORTED_LANGUAGES,
    CommentExample,
    CommentSyntax,
    get_comment_syntax,
    get_supported_comment_languages,
    iter_comment_syntaxes,
)

__all__ = [
    "SUPPORTED_LANGUAGES",
    "CommentExample",
    "CommentQuery",
    "CommentSyntax",
    "LineCommentQuery",
    "NestedCommentQuery",
    "OpeningCommentQuery",
    "get_comment_syntax",
    "get_supported_comment_languages",
    "iter_comment_syntaxes",
]
