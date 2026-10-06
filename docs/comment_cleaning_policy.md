# Comment Cleaning Policy

`CommentSanitizer` turns one extracted comment into its content. This page is
the contract for what cleaning removes and what it keeps. Extraction (which
source range is a comment) is a separate contract; see
[comment_extractor.md](comment_extractor.md).

## Principle

Cleaning removes comment *scaffolding* and keeps comment *content*. Scaffolding
is syntax or layout that exists only because the text is a comment. Content is
everything a reader of the comment would need, including symbols and code.

Cleaning decisions depend on the comment's layout and the language's registry
syntax, never on the specific words in the comment. Two comments with the same
layout and different prose clean the same way.

## Removed

| Scaffolding | Example | Cleaned |
| --- | --- | --- |
| Delimiters and registered doc markers | `/// outer doc` (Rust) | `outer doc` |
| Repeated line markers of grouped line comments | `// a` + `// b` | `a` + `b` |
| A uniform block gutter such as ` * ` | `/**\n * Summary.\n *\n * @param x the x\n */` | `Summary.\n\n@param x the x` |
| Documentation opener variants | `{- \| doc -}` (Haskell) | `doc` |
| Decorative rulers and frames made of one repeated character | `// ============ Section ============` | `Section` |
| Box frames whose edges all match | `/***********\n * Title *\n ***********/` | `Title` |
| One padding space after an opener and before a closer | `REM note` (Batch) | `note` |
| Line-ending differences | `// a\r\n// b` | `a\nb` |

## Kept

| Content | Example | Cleaned |
| --- | --- | --- |
| Punctuation that is not a uniform ruler | `/* <<< merge >>> */` | `<<< merge >>>` |
| Prompts and merge-conflict markers | `// >>> f()` | `>>> f()` |
| Markdown emphasis | `/* ** bold ** */` | `** bold **` |
| Commented-out code, including line markers inside a one-line block | `/* // disabled code */` | `// disabled code` |
| Indentation relative to the comment body | `/*\n *   if (x) {\n *     y();\n *   }\n */` | `if (x) {\n  y();\n}` |
| Continuation alignment under the opener text | `/* a\n   b */` | `a\n   b` |
| Nested comments inside a comment | `{- a {- b -} c -}` | `a {- b -} c` |
| Text on block marker lines | `=begin\nnote\n=end trailing` (Ruby) | `note\ntrailing` |
| Line splices that continue a comment | `# a \\\n  b` (Makefile) | `a \\\n  b` |

Some markers are deliberately literal in specific languages. For example,
Smithy and WIT keep the third slash of `///` (`/// documentation` cleans to
`/ documentation`), and Ada keeps the third dash of `---` because a diff header
such as `--- src/file.orig` is content. These exceptions are listed in the
sanitizer and covered by tests.

Uncertainty is resolved toward keeping text. A cleaner may leave a little
scaffolding behind; it must not silently discard content.

## Enforcement

- Generated per-family fixtures in `tests/fixtures/comment_cleaning` derive the
  expected output from registry syntax, not from the sanitizer under test.
- Reviewed fixtures under `tests/fixtures/comment_cleaning_*` record
  human-reviewed raw-to-cleaned pairs from real repositories.
- `tests/test_comment_cleaner_content_independence.py` re-runs every reviewed
  fixture with its content words replaced by same-shape ROT13 words and
  requires the same cleaning. Cases that still depend on specific prose are
  frozen in `tests/fixtures/comment_cleaning_content_dependent_cases.json`.
  That list may only shrink: a new prose-keyed rule fails the test, and a case
  that becomes layout-driven must be removed from the list.
- `make comment-cleaner-fuzz` checks that cleaning is total and stable on
  randomized and structured input for every language key.

## Working down the content-dependent list

Each entry in the frozen list records the sanitizer pass that currently decides
the case (`decided_by`). Most come from the exact-layout passes
(`_sanitize_batch_two_exact_layout`, `_sanitize_final_safe_*`,
`_sanitize_strict_restoration_layout`) that match specific reviewed text. To
retire an entry:

1. Identify the layout feature the reviewed output actually relies on, such as
   a gutter width, a frame shape, or a metadata tag form.
2. Replace the text match with a rule on that feature, scoped by registry
   syntax rather than by prose.
3. Run the reviewed fixture tests, the content-independence test, and both fuzz
   targets, then remove the resolved entries from the list.
