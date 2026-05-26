# Adversarial Comment Testing Playbook

This playbook defines the breaker/fixer loop for comment-parser and sanitizer
testing.

## Breaker role

The breaker agent tries to expose missing coverage or incorrect behavior
without changing production code. Breakers now also update the assigned
per-language fixture files with cases that are expected to parse correctly
with the current implementation.

The breaker should:

- inspect the registry entry and current tests for each assigned language
- inspect the assigned fixture file under `tests/fixtures/comment_languages/`
- systematically cover every relevant scenario family for each assigned language
- create minimal inputs that stress edge cases
- add representative cases directly to the assigned fixture file when the
  current parser should accept them
- keep seeded fixture comments intact and use non-comment separator code lines
  when needed to avoid accidental grouping of adjacent line comments
- run the current parser locally and capture actual behavior
- run `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov`
  after fixture edits
- when sanitizer behavior is in scope, record both the raw extracted match and
  the sanitized output
- when sanitizer behavior removes a symbol, add a paired case where the same
  symbol is preserved because it is semantically meaningful
- when the registry or prior research says a comment scenario does not exist,
  search the internet for real-world examples anyway and use them as crash or
  misparse probes
- record an outcome for each reviewed scenario family, even when the result is
  that the current behavior is already correct
- write findings only to the assigned `threads/*_findings.md` file

The breaker should not:

- patch parser code
- edit regular test modules or non-assigned fixture files
- leave a fixture-file addition in place when it does not parse correctly with
  current behavior; record that case as a finding for the fixer instead
- rewrite resolution files
- spam redundant variants of the same case family

## Fixer role

The fixer agent consumes breaker findings and turns them into stable coverage.

The fixer should:

- validate each reported case before changing code
- validate breaker fixture-file additions and keep them only when they parse
  correctly
- process all recorded languages and scenario families, not only the failing
  ones
- add tests first for confirmed bugs or missing contracts
- add a fixed parser case to the relevant fixture file once it is stable and
  should parse correctly
- for sanitizer changes, pair every new removal testcase with a preservation
  testcase for the same symbol when that symbol can carry meaning
- patch the parser, registry, or sanitizer minimally
- record `no-change-needed` when the reviewed behavior is already correct
- document intentional limitations instead of inventing unsupported semantics
- run `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov`
  whenever fixture files change
- record outcomes in the assigned `threads/*_resolution.md` file

The fixer should not:

- rewrite breaker findings
- revert unrelated work on the branch
- broaden syntax support without evidence or a clear contract

## Coverage themes

Systematically review these as applicable to each assigned language:

- seeded registry fixture cases for every supported comment syntax
- repeated symbol line-comment openers such as `////////`, `########`,
  `;;;;;;;;`, or equivalent language-specific symbol runs
- odd repeated openers for homogeneous even-length openers, such as `///` for
  `//`, `---` for `--`, and `;;;` for `;;`
- inline block or nested comments with code before and after the comment
- star-prefixed multiline documentation comments, including C-style
  `/** ... */` blocks with `* @param`, `* @return`, and `* @throws` lines
- comment delimiters inside simple quoted strings that should not parse as
  comments
- nested block comments containing line-comment markers
- outer comments that should suppress inner comment matches
- unclosed blocks and stray closers
- grouped standalone line comments vs inline comments
- start-of-file headers, leading blank lines, and hashbang handling
- indentation-scoped or column-scoped comments
- version-specific or dialect-specific comment forms
- delimiter-like text inside quote-delimited comments
- sanitizer edge cases after extraction
- sanitizer under-stripping of delimiter clutter or decorative gutters
- sanitizer over-stripping of semantically important punctuation and markers
- unsupported or supposedly absent comment forms found in real code examples
  online
- fixture-file regressions where an added adversarial case changes, merges, or
  hides one of the seeded comments

For sanitizer-specific expectations and examples, see
`docs/comment_testing/sanitizer_playbook.md`.

## Unsupported-scenario probing

If earlier research concluded that one of these scenarios does not exist for a
language, the breaker should still try to falsify that conclusion safely:

- search for real examples on the public web, including docs, blog posts,
  tutorials, GitHub, SourceForge, Stack Overflow, issue trackers, mailing
  lists, and code-search results
- prefer exact language names plus terms such as `comment`, `block comment`,
  `nested comment`, `header comment`, or the candidate delimiter itself
- feed those examples to the parser and check whether it crashes, throws, hangs,
  or returns clearly wrong matches
- record the source URL or provenance for any kept case

The goal is not to force unsupported syntax into the registry. The goal is to
ensure that unsupported or disputed forms do not break the parser.

If a probe demonstrates current incorrect behavior, do not leave it in the
fixture file as a failing sample. Record it in the findings thread with the
source and expected behavior so the fixer can add a regression test or code
change first. Once fixed, the case can be moved into the fixture file as a
stable parseable sample.

## Resolution policy

Every reported case should end in one of these outcomes:

- `fixed-in-code`
- `fixed-in-tests`
- `documented-limitation`
- `needs-policy-decision`
- `no-change-needed`

Use the smallest correct outcome. Not every adversarial input should force a
parser change, but every relevant reviewed theme should have an explicit
recorded outcome.
