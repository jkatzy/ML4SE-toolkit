"""Registry validation rejects malformed ``CommentSyntax`` entries.

Each case swaps the registry for one deliberately invalid entry and checks
that ``_build_language_lookup`` refuses it with the rule's error message.
"""

from dataclasses import replace

import pytest

from ml4setk.Parsing.Comments import registry
from ml4setk.Parsing.Comments.registry import CommentExample, CommentSyntax

pytestmark = pytest.mark.unit

_LINE = CommentExample("prefix\n# note\nsuffix", "# note", kind="line")
_NESTED = CommentExample("a (* note *) b", "(* note *)", kind="nested")
_CONTEXTUAL = CommentExample("% note\n", "% note", kind="line")
_EXTRACTOR = "answer_set_programming_comments"
_VALID = CommentSyntax(
    "validation_style",
    "validation_lang",
    aliases=("validation_alias",),
    regex_patterns=(r"#.*",),
    shared_regex_examples=(_LINE,),
)


def _build(monkeypatch, *syntaxes):
    monkeypatch.setattr(registry, "COMMENT_SYNTAXES", syntaxes)
    return registry._build_language_lookup()


def test_valid_entry_builds_lookup_for_every_key(monkeypatch):
    lookup = _build(monkeypatch, _VALID)

    assert set(lookup) == {"validation_lang", "validation_alias"}


@pytest.mark.parametrize(
    ("syntax", "message"),
    [
        pytest.param(
            replace(_VALID, shared_regex_examples=()),
            "must provide seeded regex examples",
            id="regex-without-examples",
        ),
        pytest.param(
            replace(_VALID, nested_delimiters=(("(*", "*)"),)),
            "must provide seeded nested examples",
            id="nested-without-examples",
        ),
        pytest.param(
            replace(_VALID, contextual_extractor=_EXTRACTOR),
            "must provide seeded contextual examples",
            id="contextual-without-examples",
        ),
        pytest.param(
            replace(_VALID, shared_contextual_examples=(_CONTEXTUAL,)),
            "Contextual examples require a contextual extractor",
            id="contextual-examples-without-extractor",
        ),
        pytest.param(
            replace(
                _VALID,
                contextual_extractor="no_such_extractor",
                shared_contextual_examples=(_CONTEXTUAL,),
            ),
            "Unknown contextual extractor",
            id="unknown-extractor",
        ),
        pytest.param(
            replace(_VALID, sanitizer_mode="stripped"),
            "Unknown sanitizer mode",
            id="unknown-sanitizer-mode",
        ),
        pytest.param(
            replace(_VALID, sanitizer_line_wrappers=(("", ""),)),
            "wrapper openers must not be empty",
            id="empty-wrapper-opener",
        ),
        pytest.param(
            replace(_VALID, sanitizer_block_wrappers=(("/*", ""),)),
            "block closers must not be empty",
            id="empty-block-closer",
        ),
        pytest.param(
            replace(_VALID, sanitizer_mode="raw", sanitizer_line_wrappers=(("#", ""),)),
            "Raw sanitizers cannot declare explicit wrappers",
            id="raw-with-wrappers",
        ),
        pytest.param(
            replace(_VALID, unclosed_block_openers=("",)),
            "Unclosed block openers must not be empty",
            id="empty-unclosed-opener",
        ),
        pytest.param(
            replace(_VALID, sanitizer_mode="raw", unclosed_block_openers=("/*",)),
            "Raw sanitizers cannot declare unclosed block openers",
            id="raw-with-unclosed-opener",
        ),
        pytest.param(
            replace(
                _VALID, regex_patterns=(), shared_regex_examples=(), unclosed_block_openers=("/*",)
            ),
            "Unclosed block openers require extractable syntax",
            id="unclosed-opener-without-syntax",
        ),
        pytest.param(
            replace(_VALID, excluded_comment_prefixes=("",)),
            "Excluded comment prefixes must not be empty",
            id="empty-excluded-prefix",
        ),
        pytest.param(
            replace(
                _VALID,
                regex_patterns=(),
                shared_regex_examples=(),
                excluded_comment_prefixes=("#!",),
            ),
            "Excluded comment prefixes require extractable syntax",
            id="excluded-prefix-without-syntax",
        ),
        pytest.param(
            replace(
                _VALID,
                language_excluded_comment_prefixes=(
                    ("validation_lang", ("#!",)),
                    ("validation_lang", ("#?",)),
                ),
            ),
            "excluded comment prefixes must use unique languages",
            id="duplicate-dialect-exclusion",
        ),
        pytest.param(
            replace(_VALID, language_excluded_comment_prefixes=(("other", ("#!",)),)),
            "excluded comment prefixes require a family language",
            id="dialect-exclusion-outside-family",
        ),
        pytest.param(
            replace(_VALID, language_excluded_comment_prefixes=(("validation_lang", ()),)),
            "excluded comment prefixes must not be empty",
            id="empty-dialect-exclusion",
        ),
        pytest.param(
            replace(
                _VALID,
                regex_patterns=(),
                shared_regex_examples=(),
                language_excluded_comment_prefixes=(("validation_lang", ("#!",)),),
            ),
            "excluded comment prefixes require extractable syntax",
            id="dialect-exclusion-without-syntax",
        ),
        pytest.param(
            replace(
                _VALID,
                language_regex_patterns=(
                    ("validation_lang", (r"#.*",)),
                    ("validation_lang", (r";.*",)),
                ),
            ),
            "regex patterns must use unique languages",
            id="duplicate-dialect-regex",
        ),
        pytest.param(
            replace(_VALID, language_regex_patterns=(("other", (r"#.*",)),)),
            "regex patterns require a family language",
            id="dialect-regex-outside-family",
        ),
        pytest.param(
            replace(_VALID, language_regex_patterns=(("validation_lang", ()),)),
            "regex patterns must not be empty",
            id="empty-dialect-regex",
        ),
        pytest.param(
            replace(
                _VALID,
                regex_patterns=(),
                shared_regex_examples=(),
                nested_delimiters=(("(*", "*)"),),
                shared_nested_examples=(_NESTED,),
                language_regex_patterns=(("validation_lang", (r"#.*",)),),
            ),
            "regex patterns require family regex patterns",
            id="dialect-regex-without-family-regex",
        ),
        pytest.param(
            replace(_VALID, canonical_name="Validation_Lang"),
            "Language names must be lowercase",
            id="mixed-case-key",
        ),
    ],
)
def test_malformed_entry_is_rejected(monkeypatch, syntax, message):
    with pytest.raises(ValueError, match=message):
        _build(monkeypatch, syntax)


def test_duplicate_key_across_families_is_rejected(monkeypatch):
    duplicate = replace(_VALID, family_name="other_style", aliases=())

    with pytest.raises(ValueError, match="Duplicate comment syntax entry"):
        _build(monkeypatch, _VALID, duplicate)
