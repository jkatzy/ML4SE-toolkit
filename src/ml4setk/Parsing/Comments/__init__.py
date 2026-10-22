"""Comment-oriented query implementations."""

from .CommentQuery import (
    CommentQuery,
    LineCommentQuery,
    NestedCommentQuery,
    OpeningCommentQuery,
    UnclosedCommentError,
    UnclosedCommentWarning,
)
from .CommentSanitizer import (
    CommentSanitizer,
    sanitize_comment,
    sanitize_comment_text,
)
from .registry import (
    SUPPORTED_LANGUAGES,
    VERSIONED_COMMENT_LANGUAGES,
    CommentExample,
    CommentLanguageVersion,
    CommentLanguageVersions,
    CommentLanguageVersionWarning,
    CommentSyntax,
    UnsupportedCommentLanguageVersionError,
    comment_language_requires_version,
    get_comment_language_version,
    get_comment_language_versions,
    get_comment_syntax,
    get_default_comment_language_version,
    get_supported_comment_languages,
    iter_comment_syntaxes,
    resolve_comment_language_version,
)
from .unwrap import unwrap_comment

__all__ = [
    "SUPPORTED_LANGUAGES",
    "VERSIONED_COMMENT_LANGUAGES",
    "CommentExample",
    "CommentLanguageVersion",
    "CommentLanguageVersionWarning",
    "CommentLanguageVersions",
    "CommentQuery",
    "CommentSanitizer",
    "CommentSyntax",
    "LineCommentQuery",
    "NestedCommentQuery",
    "OpeningCommentQuery",
    "UnclosedCommentError",
    "UnclosedCommentWarning",
    "UnsupportedCommentLanguageVersionError",
    "comment_language_requires_version",
    "get_comment_language_version",
    "get_comment_language_versions",
    "get_comment_syntax",
    "get_default_comment_language_version",
    "get_supported_comment_languages",
    "iter_comment_syntaxes",
    "resolve_comment_language_version",
    "sanitize_comment",
    "sanitize_comment_text",
    "unwrap_comment",
]
