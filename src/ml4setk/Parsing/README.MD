# Parsing

The parsing layer extracts source-code regions and returns them as
`QueryMatch(prefix, suffix, match)` values.

## Modules

- `Comments`: registry-driven regex, delimiter, lexical, and contextual
  structural comment extraction, including top-of-file opening comments.
- `Code`: Tree-sitter powered structural queries for language-aware matching.

## Contract

All stable parsing APIs should return matches in source order and use the same
tuple shape:

```python
QueryMatch(prefix, suffix, match)
```

This makes the output directly consumable by the generation utilities in
`ml4setk.Generation`.
