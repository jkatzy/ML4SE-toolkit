# Adversarial Comment Testing Playbook

This playbook defines the breaker/fixer loop for comment-parser testing.

## Breaker role

The breaker agent tries to expose missing coverage or incorrect behavior
without changing production code.

The breaker should:

- inspect the registry entry and current tests for each assigned language
- create minimal inputs that stress edge cases
- run the current parser locally and capture actual behavior
- when the registry or prior research says a comment scenario does not exist,
  search the internet for real-world examples anyway and use them as crash or
  misparse probes
- keep only cases that fail now, reveal an ambiguous contract, or deserve
  explicit regression coverage
- write findings only to the assigned `threads/*_findings.md` file

The breaker should not:

- patch parser code
- edit test files directly
- rewrite resolution files
- spam low-value variants of the same case

## Fixer role

The fixer agent consumes breaker findings and turns them into stable coverage.

The fixer should:

- validate each reported case before changing code
- add tests first for confirmed bugs or missing contracts
- patch the parser or registry minimally
- document intentional limitations instead of inventing unsupported semantics
- record outcomes in the assigned `threads/*_resolution.md` file

The fixer should not:

- rewrite breaker findings
- revert unrelated work on the branch
- broaden syntax support without evidence or a clear contract

## High-value adversarial themes

- nested block comments containing line-comment markers
- outer comments that should suppress inner comment matches
- unclosed blocks and stray closers
- grouped standalone line comments vs inline comments
- start-of-file headers, leading blank lines, and hashbang handling
- indentation-scoped or column-scoped comments
- version-specific or dialect-specific comment forms
- delimiter-like text inside quote-delimited comments
- sanitizer edge cases after extraction
- unsupported or supposedly absent comment forms found in real code examples
  online

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

## Resolution policy

Every reported case should end in one of these outcomes:

- `fixed-in-code`
- `fixed-in-tests`
- `documented-limitation`
- `needs-policy-decision`

Use the smallest correct outcome. Not every adversarial input should force a
parser change.
