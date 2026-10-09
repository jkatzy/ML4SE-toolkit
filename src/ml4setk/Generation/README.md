# Generation

The generation layer turns parsed examples into model-ready inputs.

## Core classes

- `FIMInput`: builds fill-in-the-middle prompts from a parsed match.
  `FIMInput.from_model(model)` picks a model's sentinel tokens; see
  `docs/input_formatting.md`.
- `CausalInput`: builds prefix-to-target training pairs.
- `DiffusionCompletionInput`, `DiffusionInfillInput`,
  `DiffusionExpandingInfillInput`: build mask-token inputs for masked
  diffusion LLMs; `from_model(model)` picks the mask token.
- `MultiTokenInput`: expands a target sequence into per-token contexts for
  next-token style training.
- `IterableQueryLoader`: reusable iterator wrapper for turning source datasets
  into query-driven sample streams.

The recommended flow is:

1. Parse a source string into a `QueryMatch`.
2. Feed that match into an input builder such as `FIMInput` or `CausalInput`.
3. Use `IterableQueryLoader` when you want to generate those samples lazily from
   a larger corpus.
