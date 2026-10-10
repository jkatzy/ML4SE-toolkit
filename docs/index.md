# ML4SE-toolkit

ML4SE-toolkit provides small, composable primitives for turning source code
into reproducible machine-learning examples for software engineering research.

```bash
pip install ml4setk
```

## Guides

- [Comment extraction and cleaning](comment_extractor.md): find comments in
  source files, strip their syntax, and feed them into model inputs. Start
  here for the quick start and API reference.
- [Comment cleaning policy](comment_cleaning_policy.md): what cleaning removes
  and what it keeps.
- [Input formatting](input_formatting.md): turn matches into
  fill-in-the-middle, autoregressive, masked diffusion, masked LM, or span
  corruption model inputs, with sentinel and mask tokens picked from a model
  name or Hugging Face object.
- [Chunked datasets](chunked_datasets.md): run a function over every row of a
  dataset split into many files, such as The Stack, one file at a time, with
  restartable state on disk and any number of workers.
- [Architecture](architecture.md): the `QueryMatch` contract and extension
  points.
- [Git workflow](git_workflow.md): how `dev` and `main` relate.
