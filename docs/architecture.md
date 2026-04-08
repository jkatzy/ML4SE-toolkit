# Architecture

## Summary

ML4SE-toolkit is intentionally small. It centers on one stable contract:
query implementations extract a `QueryMatch(prefix, suffix, match)`, and
generation utilities transform that match into model-ready inputs.

## Data flow

1. A parser scans raw source text and returns one or more `QueryMatch` values.
2. A generator such as `FIMInput` or `CausalInput` consumes the match and
   creates the actual prompt plus ground-truth target.
3. `IterableQueryLoader` can wrap a dataset to produce those samples lazily.

## Extension points

- Add a new parser by subclassing `Query` and returning `QueryMatch` values in
  source order.
- Add a new generator by subclassing `AbstractInput` and documenting its input
  shape.
- Keep optional integrations isolated so importing `ml4setk` does not require
  every heavy dependency.

## Optional dependencies

- `treesitter`: enables `TreeSitterQuery`
- `torch`: enables direct interoperability with PyTorch dataset utilities
