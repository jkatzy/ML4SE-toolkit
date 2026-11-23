# Comment parser development

Paths in this guide are relative to the repository root.

Use the narrowest relevant test first. A practical comment-parser target is:

```bash
uv run pytest \
  tests/test_comment_registry.py \
  tests/test_comment_queries.py \
  tests/test_comment_generated_cases.py \
  tests/test_comment_sanitizer.py \
  -q --no-cov
```

## Repository map

- `src/ml4setk/Parsing/Comments/registry.py`: comment syntax, aliases,
  contextual extractor names, sanitizer metadata, evidence, and seeded examples
- `src/ml4setk/Parsing/Comments/CommentQuery.py`: generic matching, range,
  grouping, ordering, and `QueryMatch` construction
- `src/ml4setk/Parsing/Comments/CommentSanitizer.py`: syntax-aware comment
  cleaning
- `tests`: deterministic unit, generated, adversarial, fuzz, and regression
  coverage
- `docs/comment_research/README.md`: evidence-first language intake workflow
- `docs/comment_research/report_template.md`: reusable research record
- `docs/comment_testing/README.md`: adversarial, fuzzing, judge, and regression
  operations

## Parser and registry invariants

- Every extraction API returns `QueryMatch(prefix, suffix, match)` with exact
  source slices. Matches remain ordered by source position and do not overlap.
- Language-specific syntax belongs in `COMMENT_SYNTAXES`. Keep query classes
  generic; add a narrowly scoped lexical or contextual helper only when a
  delimiter cannot express the format's semantics.
- Registry keys and aliases are unique lowercase names. Raw dataset labels may
  normalize during lookup, but the chosen key must be explicit and collision
  checked. Aliases share one `CommentSyntax` only when their syntax and dialect
  scope are genuinely equivalent.
- Every implemented regex, nested delimiter, or contextual extractor has a
  seeded `CommentExample`. Set `kind`, inline compatibility, grouping
  compatibility, wrappers, exclusions, and unclosed behavior deliberately.
- Preserve the public positional field order of `CommentSyntax`; append new
  metadata fields after the compatibility boundary.
- Unsupported or unresolved syntax raises `NotImplementedError`; uncertainty
  is not a reason to add a permissive marker pattern.
- Comment syntax that changed between language versions belongs in the
  family's `language_versions` table. The registry entry implements the
  default version; other versions overlay only what they change and need a
  differential test. See `docs/comment_research/version_dependent_comments.md`.
- Extraction and cleaning are separate contracts. A cleaner may remove verified
  comment scaffolding and normalize line endings, but must not silently discard
  comment content.

## Language implementation workflow

1. Record the new dataset revision and label exactly as received.
2. Follow `docs/comment_research/README.md`; do not infer syntax from a language
   name or a related language.
3. Add or revise one registry family with pinned evidence and representative
   seeded examples. Treat version and dialect differences explicitly.
4. Add adversarial negative cases for strings, directives, operators, embedded
   languages, malformed input, line endings, and delimiter boundaries that are
   relevant to the syntax.
5. Run focused extraction and sanitizer tests, then both deterministic fuzz
   targets.
6. Minimize every failure into ordinary pytest coverage and verify that it fails
   before the fix and passes after it.
7. Run the full verification commands before promotion to `main`.

Do not use an LLM verdict as the permanent oracle. The judge workflow can find
and triage candidates; reviewed source evidence and deterministic tests define
the accepted behavior.
