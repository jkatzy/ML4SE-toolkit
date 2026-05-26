# Comment Sanitizer Testing Playbook

This playbook defines the sanitizer-specific pass within the adversarial
comment-testing workflow.

## Goal

Sanitizer tests are two-sided:

- remove syntax-only clutter that should not survive extraction
- preserve characters that still carry meaning in the comment body

The sanitizer should not merely "strip punctuation." It should remove comment
notation and decorative scaffolding while leaving meaningful text intact.

## Paired-case rule

Every removal-oriented sanitizer testcase must have a preservation-oriented
counterpart when the same symbol can also carry meaning.

If one testcase proves that a symbol should be removed, add at least one
companion testcase showing that the symbol must be kept when it is part of the
comment body. Do not land one-sided symbol-removal coverage.

Typical pairs:

- remove decorative leading `#`, keep `# Heading`
- remove decorative leading `*`, keep `* bullet`
- remove decorative leading `--`, keep `--flag`
- remove decorative leading `%`, keep `%matplotlib` or `%VAR%`
- remove decorative repeated punctuation, keep deliberate punctuation inside
  prose, examples, regexes, or emphasis

## Starting point

Start from a real extracted comment match whenever possible. Use
`CommentQuery` or `OpeningCommentQuery` to obtain the raw match, then run the
sanitizer entry point under test.

If the sanitizer case is also a parser-accepted adversarial sample, add it to
the assigned file under `tests/fixtures/comment_languages/` and verify that the
fixture still parses. If the raw extraction currently fails, record the case in
the findings thread instead of leaving a failing fixture edit behind.

If the sanitizer is invoked indirectly through another API, record the exact
caller or helper used in the finding. The important artifact is the transition
from raw extracted match to sanitized output.

## Removal contract

Treat these as removable only when they are acting as comment scaffolding:

- outer delimiters and delimiter-only edge lines such as `/* */`, `<!-- -->`,
  `(* *)`, `"""`, or language-specific block wrappers
- decorative per-line gutters such as repeated leading `*`, `#`, `--`, `;`,
  `%`, or `'` characters that exist only for aligned block-comment formatting
- padding-only indentation introduced by aligned comment blocks
- empty leading or trailing lines created solely by delimiter placement

Prefer adversarial inputs that mix removable scaffolding with one line that is
not scaffolding, so the sanitizer must distinguish between the two.

## Preservation contract

Do not strip characters when they are part of the actual comment text. High-
value preservation targets include:

- Markdown headings, lists, and emphasis such as `# Heading`, `##`, `- item`,
  `* item`, or `***important***`
- tags and annotations such as `TODO:`, `FIXME:`, `NOTE:`, `@param`,
  `@return`, or `@see`
- shell and CLI text such as `#!/bin/sh`, `--flag`, `$HOME`, or `%VAR%`
- code and language tokens such as `C#`, `F#`, `C++`, `#include`, `::`,
  `**kwargs`, `%%time`, or `%matplotlib`
- deliberate repeated punctuation or formatting inside prose, regexes, math,
  examples, or ASCII diagrams

Semantically important characters are contextual. A leading `#` might be
comment clutter in one case and a Markdown heading in another. A leading `*`
might be a decorative block gutter or a real list bullet. The finding must say
which interpretation is correct.

## Breaker focus

The breaker should:

- systematically cover all relevant removable and preservable symbol families
  for the assigned languages
- keep cases minimal and concrete
- add parser-accepted sanitizer samples to the assigned fixture file when they
  still parse correctly
- record the raw extracted match before sanitization
- record the actual sanitized output
- explain which pieces are expected to be removed
- explain which pieces must remain because they carry meaning
- pair every symbol-removal case with a symbol-preservation case when the same
  symbol can appear as meaningful content
- record `reviewed-no-issue` when a checked symbol family already behaves
  correctly or when the current surface is only raw extraction with no
  sanitizer entry point available

Coverage themes:

- delimiter-only opening and closing lines around meaningful inner text
- mixed decorative and semantic leading punctuation in the same block comment
- aligned `*`/`#`/`;` gutters where one line is actually a bullet or heading
- repeated punctuation that should survive because it is content, not syntax
- sanitizer outputs that over-strip text into a less informative comment body
- sanitizer outputs that under-strip obvious comment notation and alignment
  noise

## Fixer focus

The fixer should:

- validate the raw extracted match before touching sanitizer expectations
- process every reviewed symbol family, not only the failing ones
- add tests that assert the sanitized output directly
- ensure every new symbol-removal testcase is paired with a testcase where the
  same symbol is preserved when semantically meaningful
- make the smallest rule change that fixes the confirmed contract
- avoid broad punctuation stripping that would erase valid content
- record `no-change-needed` when the reviewed sanitizer behavior is already
  correct
- document intentional limitations if the sanitizer cannot distinguish a case
  safely

## Case format

For sanitizer-focused cases, record:

- the original source input when relevant
- the fixture file updated, or `findings-only` for a currently failing parser
  probe
- the extraction entry point used
- the sanitizer entry point used
- the raw extracted match
- the actual sanitized output
- the expected sanitized output
- the removal contract
- the preservation contract
- the paired preservation testcase when a symbol-removal case is reported
- the fixture verification command and result when a fixture file changed
- why the case matters
