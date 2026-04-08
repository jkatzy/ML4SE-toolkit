# Comment Parsing

The comment parsing module provides four query implementations:

- `LineCommentQuery`: detects single-line and non-nested block comments based
  on language-specific regexes.
- `NestedCommentQuery`: extracts top-level nested comment regions using
  delimiter pairs for languages that support them.
- `CommentQuery`: combines both strategies, returns matches in source order,
  coalesces adjacent standalone single-line comments into one logical block,
  and can union comment matches across multiple candidate languages when you
  pass a list of language keys.
- `OpeningCommentQuery`: extracts one logical opening comment block from the
  top of a file, optionally skipping a hashbang and enforcing a configurable
  row limit for where the header starts.
- `registry.py`: the language registry that agents should update when extending
  support, including aliases, syntax patterns, seeded examples, and evidence
  placeholders.

All returned matches follow the same `QueryMatch(prefix, suffix, match)`
contract so they can feed directly into generation utilities such as
`FIMInput` and `CausalInput`.

For concrete usage, examples, supported-language lookup, and current
limitations, see
[`docs/comment_extractor.md`](../../../../docs/comment_extractor.md).

The registry currently covers `333` language keys, including programming,
template, markup, config, and record-oriented syntaxes such as `astro`,
`coldfusion`, `genero`, `marko`, `openqasm`, `plantuml`, `q`,
`restructuredtext`, `rexx`, `slim`, `smarty`, and `tla`.

## Expansion workflow

When adding a language or revising syntax support:

1. Update `registry.py` instead of editing branching logic in the parser.
2. Record the evidence in `docs/comment_syntax_matrix.md`.
3. Add or adjust seeded examples in the registry so the pytest suite exercises
   the new behavior automatically.
