# Adversarial Comment Testing

Adversarial testing targets plausible inputs that sit just outside ordinary
examples. Test extraction and cleaning separately because a correct extracted
span can still be cleaned destructively, while a good cleaner cannot repair an
incorrect span.

## Contracts

Extraction must return exact, ordered, non-overlapping source slices for the
selected language. It must not absorb surrounding code, lose delimiter text,
or reinterpret comment-like text inside strings and other protected regions.

Cleaning may remove only comment syntax scaffolding, decorative gutters,
delimiter-only edges, and padding. It must preserve content-bearing text,
punctuation, examples, TODO tags, Markdown, code-like text, Unicode, and
meaningful blank-line structure.

## Breaker and fixer loop

Use separate breaker and fixer passes, even when one developer performs both.

1. The breaker starts from researched syntax and writes the smallest input that
   could contradict a contract. The breaker does not change production code.
2. Confirm which layer failed: registry selection, extraction, cleaning, judge,
   manifest construction, or dataset labeling.
3. Reduce the input while preserving the failure. Keep the original case ID or
   source hash in test provenance when policy permits.
4. The fixer first turns the reduced input into a deterministic failing test.
5. Make the narrowest implementation or registry change that satisfies the
   researched dialect.
6. Rerun the breaker test, adjacent language-family tests, fuzzing, and the full
   comment suite.

Do not let a fixer weaken an assertion, broaden a delimiter, or add a sanitizer
exception without evidence about the language and neighboring cases.

## Extraction attacks

Cover at least these boundaries for every new syntax family:

- delimiter-looking text inside single, double, raw, template, heredoc, regex,
  and escaped strings supported by the language;
- a comment immediately before or after code, another comment, EOF, or a line
  ending;
- empty, delimiter-only, and one-character comments;
- nested blocks, mixed block types, excess closers, and unclosed blocks;
- doc comments, directives, pragmas, shebangs, and preprocessor regions;
- contextual comments whose meaning depends on column, line start, or parser
  state;
- LF, CRLF, and CR boundaries;
- aliases and dialects that share a registry entry but differ in syntax;
- Unicode whitespace, combining marks, bidi controls, NULs, and malformed
  decoded text where the public API accepts Python strings;
- very long comments and many adjacent matches.

Assert exact raw spans and surrounding source reconstruction. Do not assert
only that "a comment was found."

## Cleaning attacks

Exercise the same wrapper in both ordinary and content-bearing forms:

- opener or closer tokens repeated as real prose or code examples;
- decorative stars, dashes, hashes, quotes, boxes, and indentation beside real
  punctuation;
- Markdown headings, lists, fences, links, tables, emphasis, and block quotes;
- TODO/FIXME tags, issue IDs, URLs, paths, command lines, and snippets;
- nested delimiters shown as examples inside an outer comment;
- blank first or last lines versus meaningful internal blank lines;
- mixed newline styles and trailing whitespace;
- all Unicode payload classes used by `scripts/fuzz_comment_parsers.py`;
- text that resembles instructions to a model or serialized judge output.

Test public API parity where applicable: `CommentSanitizer.sanitize` with a
string and `QueryMatch`, `sanitize_comment`, and `sanitize_comment_text` must
agree.

## Focused execution

```bash
uv run pytest \
  tests/test_comment_extractor_failure_boundaries.py \
  tests/test_stack_v2_comment_regressions.py \
  tests/test_comment_sanitizer_regression_edges.py \
  tests/test_comment_cleaning_regressions.py \
  -q --no-cov

make comment-fuzz COMMENT_FUZZ_SEED=0xC0FFEE
make comment-cleaner-fuzz COMMENT_FUZZ_SEED=0xC0FFEE
```

Record and close every breaker finding according to
[failure dispositions](failure_dispositions.md). A judge report or generated
test is a lead; it is not a reviewed adversarial regression.
