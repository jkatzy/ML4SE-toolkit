# Parsing

The parsing layer extracts source-code regions and returns them as
`QueryMatch(prefix, suffix, match)` values.

## Modules

- `Comments`: regex- and delimiter-based comment extraction across multiple
  programming languages, including top-of-file opening-comment extraction.
- `Code`: Tree-sitter powered structural queries for language-aware matching.

## Contract

All stable parsing APIs should return matches in source order and use the same
tuple shape:

```python
QueryMatch(prefix, suffix, match)
```

This makes the output directly consumable by the generation utilities in
`ml4setk.Generation`.
