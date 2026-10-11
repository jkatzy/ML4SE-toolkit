# ML4SE-toolkit

ML4SE-toolkit provides small, composable primitives for turning source code into
reproducible machine-learning examples for software engineering research.

Documentation: https://jkatzy.github.io/ML4SE-toolkit/

## Installation

```bash
pip install ML4SE-ToolKit
```

The import name is `ml4setk`, for example `from ml4setk import CommentQuery`.
Optional extras:

- `treesitter`: Tree-sitter queries through `ml4setk.Parsing.Code.TreeSitterQuery`
- `datasets`: Parquet and Hugging Face Hub chunks for `ml4setk.Datasets.ChunkedIterator`
- `torch`: PyTorch dataset interoperability

```bash
pip install "ML4SE-ToolKit[treesitter,datasets,torch]"
```

## Minimal example

```python
from ml4setk import CommentQuery, FIMInput

sample = "prefix\n// explain this branch\nsuffix"
match = CommentQuery("java").parse(sample)[0]

model_input, ground_truth = FIMInput(
    "<fim_prefix>",
    "<fim_suffix>",
    "<fim_middle>",
).generate(match)

print(model_input)
print(ground_truth)
```

Queries return `QueryMatch(prefix, suffix, match)` values, and input
formatters turn a match into `(model_input, ground_truth)`. Use
`FIMInput.from_model("bigcode/starcoder2-3b")` to pick a model's own sentinel
tokens instead of passing them by hand.

## Guides

- [Comment extraction and cleaning](https://jkatzy.github.io/ML4SE-toolkit/comment_extractor/):
  find comments in source files across 776 language keys, strip their syntax,
  and feed them into model inputs. Start here for the quick start and API
  reference.
- [Comment cleaning policy](https://jkatzy.github.io/ML4SE-toolkit/comment_cleaning_policy/):
  what cleaning removes and what it keeps.
- [Input formatting](https://jkatzy.github.io/ML4SE-toolkit/input_formatting/):
  fill-in-the-middle, autoregressive, masked diffusion, masked LM, and span
  corruption inputs, with sentinel and mask tokens picked from a model name or
  Hugging Face object.
- [Chunked datasets](https://jkatzy.github.io/ML4SE-toolkit/chunked_datasets/):
  run a function over every row of a dataset split into many files, such as
  The Stack, with restartable state on disk and any number of workers.
- [Architecture](https://jkatzy.github.io/ML4SE-toolkit/architecture/): the
  `QueryMatch` contract and extension points.
- [Git workflow](https://jkatzy.github.io/ML4SE-toolkit/git_workflow/): how
  `dev` and `main` relate, and how releases work.

## Development

Use `uv` so package state stays locked to the repository:

```bash
make setup            # uv sync --group dev
make setup-optional   # adds the treesitter and datasets extras
```

- `make test`: unit and integration suite with coverage
- `make test-optional`: optional-dependency tests without coverage gating
- `make lint`: `ruff` on maintained source, tests, and examples
- `make smoke`: minimal end-to-end smoke tests
- `make comment-fuzz`: deterministic Unicode-heavy parser and sanitizer
  invariants across every registered language (`make comment-cleaner-fuzz`
  runs only the sanitizer campaign)
- `make comment-cleaner-fixtures`: regenerate the comment cleaning oracles
- `make docs`: build the documentation site into `site/` and fail on broken
  links; `make docs-serve` previews it at http://127.0.0.1:8000
- `make build`: source and wheel distributions in `dist/`
- `make check-main-branch`: fail if development-only files are tracked
- `make check-release-version`: fail if package version metadata disagrees

## Branches and releases

`main` is the release branch and `dev` is the integration branch. Topic
branches start from `dev` and target `dev`; release pull requests promote
tested code from `dev` to `main`. Every merge to `main` republishes the
documentation site. See the
[git workflow](https://jkatzy.github.io/ML4SE-toolkit/git_workflow/) for the
release checks and the main-branch policy.

The `Publish` workflow (`.github/workflows/publish.yml`) uses PyPI Trusted
Publishing. A tag matching `v*` on `main` builds, validates, and publishes to
PyPI; a manual run publishes the current branch to TestPyPI. The workflow
checks that the tag, `pyproject.toml`, and the package `__version__` agree.

## Repository map

- `src/ml4setk/Parsing`: query primitives, the comment registry, the
  sanitizer, and optional Tree-sitter support
- `src/ml4setk/Generation`: input formatters and the model token registries
- `src/ml4setk/Datasets`: the chunked, restartable dataset iterator
- `src/ml4setk/Comment_util`: the legacy tuple-based comment API
- `src/ml4setk/EBNF`: grammar-processing and railroad-diagram utilities, kept
  in the repository but not shipped in the PyPI package
- `tests`: regression, unit, integration, and smoke coverage
- `docs`: the source of the documentation site
