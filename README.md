# ML4SE-toolkit

ML4SE-toolkit provides small, composable primitives for turning source code into
reproducible machine-learning examples for software engineering research.

## What is in scope

- Comment-oriented parsing utilities that return a normalized
  `QueryMatch(prefix, suffix, match)` contract.
- Input builders for causal and fill-in-the-middle style training examples.
- Optional integrations for Tree-sitter queries and PyTorch-style iterable
  datasets.

## Installation

Install the published package from PyPI:

```bash
pip install ml4setk
```

Install optional extras only when you need them:

```bash
pip install "ml4setk[treesitter]"
pip install "ml4setk[torch]"
```

## Development setup

Use `uv` so package state stays locked to the repository:

```bash
uv venv .venv
uv sync --group dev
```

Install optional extras only when you need them:

```bash
uv sync --group dev --extra treesitter
uv sync --group dev --extra torch
```

## Build

Build source and wheel distributions locally with:

```bash
uv build
```

Artifacts are written to `dist/`.

To validate the built distributions before uploading:

```bash
uvx twine check dist/*
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

The parsing contract is stable across the core query implementations:

- `prefix`: text before the match
- `suffix`: text after the match
- `match`: the extracted region itself

For a fuller extractor guide, including `contains`, grouped line comments,
nested comments, opening file-header extraction, supported-language lookup, and
unsupported-language behavior,
see [docs/comment_extractor.md](https://github.com/jkatzy/ML4SE-toolkit/blob/main/docs/comment_extractor.md).

At the moment the comment extractor covers `326` registry keys, including
template and document syntaxes such as `astro`, `coldfusion`, `jsp`, `marko`,
`plantuml`, `slim`, `smarty`, and `restructuredtext`, plus nested-comment
languages such as `coldfusion`, `dafny`, `frege`, `grammatical_framework`,
`rexx`, `tla`, and `v`.

## Development commands

- `make setup`: create and sync the local development environment with `uv`
- `make test`: run the default unit and integration suite with coverage
- `make test-optional`: run optional-dependency tests without coverage gating
- `make lint`: run `ruff` on the source tree
- `make smoke`: run the minimal end-to-end smoke tests
- `make check-main-branch`: fail if development-only artifacts are still
  tracked and the branch is not ready to merge to `main`

## Git workflow

Development branches may contain agent instructions, raw research outputs, and
other temporary working artifacts. `main` may not. The permanent rules and the
enforced main-branch policy are documented in
[docs/git_workflow.md](https://github.com/jkatzy/ML4SE-toolkit/blob/main/docs/git_workflow.md).

## Repository map

- `src/ml4setk/Parsing`: query primitives and optional Tree-sitter support
- `src/ml4setk/Generation`: model-input builders
- `tests`: regression, unit, integration, and smoke coverage
- `docs/architecture.md`: concise architecture and extension notes
- `docs/comment_extractor.md`: how to use `CommentQuery` and related extractors
- `docs/git_workflow.md`: branch policy, development-only artifacts, and the
  main-branch guard
- `AGENTS.md`: repository guidance for coding agents and contributors
