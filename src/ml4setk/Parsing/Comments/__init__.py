"""Comment-oriented query implementations."""

from .CommentQuery import (
    CommentQuery,
    LineCommentQuery,
    NestedCommentQuery,
    OpeningCommentQuery,
)
from .CommentSanitizer import (
    CommentSanitizer,
    sanitize_comment,
    sanitize_comment_text,
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
    "CommentSanitizer",
    "CommentSyntax",
    "LineCommentQuery",
    "NestedCommentQuery",
    "OpeningCommentQuery",
    "get_comment_syntax",
    "get_supported_comment_languages",
    "iter_comment_syntaxes",
    "sanitize_comment",
    "sanitize_comment_text",
]
