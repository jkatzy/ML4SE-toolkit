"""Helpers for removing comment syntax from extracted comment text."""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from functools import lru_cache

from ..Query import QueryMatch
from .registry import get_comment_syntax

_PLACEHOLDER_SEGMENTS = (
    "Remember the bull.",
    "block note",
    "inline note",
    "+ 100",
    "note",
)


@dataclass(frozen=True)
class _InlineRule:
    open_token: str
    close_token: str = ""


@dataclass(frozen=True)
class _BlockRule:
    open_token: str
    close_token: str
    full_line_wrapper: bool = False


@dataclass(frozen=True)
class _SanitizerRules:
    line_rules: tuple[_InlineRule, ...]
    block_rules: tuple[_BlockRule, ...]


class CommentSanitizer:
    """Strip the outer comment syntax from extracted comment text."""

    def __init__(self, language: str):
        self.language = language
        self.syntax = get_comment_syntax(language)
        self.rules = _build_sanitizer_rules(self.syntax.canonical_name)

    def sanitize(self, comment: str | QueryMatch) -> str:
        text = self._coerce_comment_text(comment)
        text = self._strip_outer_block_wrapper(text)
        text = self._strip_grouped_line_syntax(text)
        text = self._strip_doc_block_leaders(text)
        return self._normalize(text)

    @staticmethod
    def _coerce_comment_text(comment: str | QueryMatch) -> str:
        if isinstance(comment, QueryMatch):
            return comment.match
        if isinstance(comment, str):
            return comment
        raise TypeError("comment must be a string or QueryMatch")

    def _strip_outer_block_wrapper(self, text: str) -> str:
        for rule in self.rules.block_rules:
            stripped = self._apply_block_rule(text, rule)
            if stripped is not None:
                return stripped
        return text

    @staticmethod
    def _apply_block_rule(text: str, rule: _BlockRule) -> str | None:
        if rule.full_line_wrapper:
            lines = text.splitlines()
            if len(lines) < 2:
                return None
            if lines[0].strip() != rule.open_token or lines[-1].strip() != rule.close_token:
                return None
            return "\n".join(lines[1:-1])

        if not text.startswith(rule.open_token):
            return None
        if rule.close_token and not text.endswith(rule.close_token):
            return None

        end = len(text) - len(rule.close_token) if rule.close_token else len(text)
        return text[len(rule.open_token) : end]

    def _strip_grouped_line_syntax(self, text: str) -> str:
        lines = text.splitlines()
        if not lines:
            return text

        non_empty_indices = [index for index, line in enumerate(lines) if line.strip()]
        if not non_empty_indices:
            return ""

        if len(non_empty_indices) == 1:
            index = non_empty_indices[0]
            stripped = self._strip_line(lines[index])
            if stripped is None:
                return text
            lines[index] = stripped
            return "\n".join(lines)

        stripped_lines = list(lines)
        for index in non_empty_indices:
            stripped = self._strip_line(lines[index])
            if stripped is None:
                return text
            stripped_lines[index] = stripped

        return "\n".join(stripped_lines)

    def _strip_line(self, line: str) -> str | None:
        candidate = line.lstrip()
        for rule in self.rules.line_rules:
            if not candidate.startswith(rule.open_token):
                continue

            if rule.close_token:
                if not candidate.endswith(rule.close_token):
                    continue
                body = candidate[len(rule.open_token) : len(candidate) - len(rule.close_token)]
                return body.strip()

            body = candidate[len(rule.open_token) :]
            if body.startswith(" "):
                body = body[1:]
            return body.rstrip()

        return None

    @staticmethod
    def _strip_doc_block_leaders(text: str) -> str:
        lines = text.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        if not non_empty_lines:
            return text

        for leader in ("*", "!"):
            if all(
                CommentSanitizer._has_decorative_leader(line, leader)
                for line in non_empty_lines
            ):
                return "\n".join(
                    CommentSanitizer._remove_decorative_leader(line, leader)
                    if line.strip()
                    else ""
                    for line in lines
                )

        return text

    @staticmethod
    def _has_decorative_leader(line: str, leader: str) -> bool:
        stripped = line.lstrip()
        return stripped == leader or stripped.startswith(f"{leader} ")

    @staticmethod
    def _remove_decorative_leader(line: str, leader: str) -> str:
        stripped = line.lstrip()
        remainder = stripped[len(leader) :]
        if remainder.startswith(" "):
            remainder = remainder[1:]
        return remainder.rstrip()

    @staticmethod
    def _normalize(text: str) -> str:
        text = textwrap.dedent(text)
        lines = [line.rstrip() for line in text.splitlines()]

        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()

        return "\n".join(lines).strip()


def sanitize_comment_text(language: str, comment: str | QueryMatch) -> str:
    """Return the textual content of an extracted comment."""

    return CommentSanitizer(language).sanitize(comment)


@lru_cache(maxsize=None)
def _build_sanitizer_rules(language: str) -> _SanitizerRules:
    syntax = get_comment_syntax(language)

    line_rules: list[_InlineRule] = []
    block_rules: list[_BlockRule] = [
        _BlockRule(open_delim, close_delim)
        for open_delim, close_delim in syntax.nested_delimiters
    ]

    examples = (
        *syntax.shared_regex_examples,
        *syntax.canonical_regex_examples,
        *syntax.shared_nested_examples,
        *syntax.canonical_nested_examples,
    )
    for example in examples:
        inline_rule = _derive_inline_rule(example.expected_match)
        if example.kind == "line":
            if inline_rule is not None:
                line_rules.append(inline_rule)
            continue

        block_rule = _derive_block_rule(example.expected_match)
        if block_rule is not None:
            block_rules.append(block_rule)
        elif inline_rule is not None:
            line_rules.append(inline_rule)

    return _SanitizerRules(
        line_rules=_dedupe_inline_rules(line_rules),
        block_rules=_dedupe_block_rules(block_rules),
    )


def _derive_block_rule(comment: str) -> _BlockRule | None:
    if "\n" in comment:
        lines = comment.splitlines()
        if len(lines) >= 2:
            open_token = lines[0].strip()
            close_token = lines[-1].strip()
            if open_token and close_token:
                return _BlockRule(open_token, close_token, full_line_wrapper=True)

    inline_rule = _derive_inline_rule(comment)
    if inline_rule is None or not inline_rule.close_token:
        return None
    return _BlockRule(inline_rule.open_token, inline_rule.close_token)


def _derive_inline_rule(comment: str) -> _InlineRule | None:
    for placeholder in _PLACEHOLDER_SEGMENTS:
        if placeholder not in comment:
            continue

        before, after = comment.split(placeholder, 1)
        return _InlineRule(before.strip(), after.strip())

    candidate = comment.lstrip()
    if not candidate:
        return None

    parts = candidate.split(None, 1)
    return _InlineRule(parts[0])


def _dedupe_inline_rules(rules: list[_InlineRule]) -> tuple[_InlineRule, ...]:
    deduped = {
        (rule.open_token, rule.close_token): rule
        for rule in sorted(
            rules,
            key=lambda rule: (len(rule.open_token) + len(rule.close_token), len(rule.close_token)),
            reverse=True,
        )
        if rule.open_token
    }
    return tuple(deduped.values())


def _dedupe_block_rules(rules: list[_BlockRule]) -> tuple[_BlockRule, ...]:
    deduped = {
        (rule.open_token, rule.close_token, rule.full_line_wrapper): rule
        for rule in sorted(
            rules,
            key=lambda rule: (
                rule.full_line_wrapper,
                len(rule.open_token) + len(rule.close_token),
            ),
            reverse=True,
        )
        if rule.open_token and rule.close_token
    }
    return tuple(deduped.values())
