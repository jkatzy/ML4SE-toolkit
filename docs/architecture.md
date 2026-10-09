# Architecture

## Summary

ML4SE-toolkit is intentionally small. It centers on one stable contract:
query implementations extract a `QueryMatch(prefix, suffix, match)`, and
generation utilities transform that match into model-ready inputs.

## Data flow

1. A parser scans raw source text and returns one or more `QueryMatch` values.
2. An input formatter such as `FIMInput`, `CausalInput`, `MaskedLMInput`,
   `SpanCorruptionInput`, or a diffusion input consumes the match and returns
   `(model_input, ground_truth)`; `generate_many` formats several matches at
   once (see [Input formatting](input_formatting.md)).
3. `ml4setk.Generation.IterableQueryLoader` can wrap a dataset to produce those
   samples lazily; subclasses implement `process(file, query)`.

Comment queries and `CommentSanitizer` read one per-language registry in
`ml4setk.Parsing.Comments.registry`. Input formatters that support
`from_model` read the model token registries in `ml4setk.Generation.sentinels`.

## Extension points

- Add a new parser by subclassing `Query` and returning `QueryMatch` values in
  source order.
- Add a new generator by subclassing `AbstractInput` and documenting its input
  shape.
- Add a comment language by adding registry data, and a model family by adding
  an entry to `MODEL_SENTINELS`, `MODEL_MASK_TOKENS`, or `MODEL_SPAN_TOKENS`.
- Keep optional integrations isolated so importing `ml4setk` does not require
  every heavy dependency.

## Optional dependencies

- `treesitter`: enables `ml4setk.Parsing.Code.TreeSitterQuery`, whose
  `parse(text, rule)` also takes a Tree-sitter query string
- `torch`: enables direct interoperability with PyTorch dataset utilities
