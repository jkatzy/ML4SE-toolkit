# ML4SE-toolkit

ML4SE-toolkit provides small, composable primitives for turning source code into
reproducible machine-learning examples for software engineering research.

## What is in scope

- Comment-oriented parsing utilities that return a normalized
  `QueryMatch(prefix, suffix, match)` contract.
- Input builders for causal and fill-in-the-middle style training examples.
- Optional integrations for Tree-sitter queries and PyTorch-style iterable
  datasets.
- Existing EBNF and grammar-analysis tooling remains available under
  `src/ml4setk/EBNF`.

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

Or via the repo command:

```bash
make build
```

Artifacts are written to `dist/`.

To validate the built distributions before uploading:

```bash
uvx twine check dist/*
```

## Publishing

The repository includes a dedicated GitHub Actions workflow at
`.github/workflows/publish.yml`.

- `workflow_dispatch`: build, validate, and publish the current branch to
  TestPyPI
- `push` of a tag matching `v*`: build, validate, and publish to PyPI

The workflow uses PyPI Trusted Publishing rather than a long-lived API token.
Before the first automated release, configure trusted publishers for this
project in both PyPI and TestPyPI with:

- owner: `jkatzy`
- repository: `ML4SE-toolkit`
- workflow name: `publish.yml`
- environment: `pypi` for PyPI, `testpypi` for TestPyPI

Release flow:

```bash
git switch main
python scripts/check_release_version.py
uv run pytest -m "not optional_dependency"
uv run pytest -m "optional_dependency" --no-cov
uv run ruff check src tests examples
git tag v0.0.2
git push origin main v0.0.2
```

The publish workflow checks that the package version in `pyproject.toml`, the
package `__version__`, and the release tag all agree before uploading.

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
- `make build`: create source and wheel distributions in `dist/`
- `make check-main-branch`: fail if development-only artifacts are still
  tracked and the branch is not ready to merge to `main`
- `make check-release-version`: fail if package version metadata is inconsistent

## Git workflow

`development-base` is the long-lived base branch for agent-assisted
development. Create future development branches from `development-base`, not
directly from `main`. Development branches may contain agent instructions, raw
research outputs, and other temporary working artifacts. `main` may not, and
`development-base` itself should not be merged directly to `main`. The
permanent rules and the enforced main-branch policy are documented in
[docs/git_workflow.md](https://github.com/jkatzy/ML4SE-toolkit/blob/main/docs/git_workflow.md).

## Repository map

- `src/ml4setk/Parsing`: query primitives and optional Tree-sitter support
- `src/ml4setk/Generation`: model-input builders
- `src/ml4setk/EBNF`: grammar-processing and railroad-diagram utilities
- `tests`: regression, unit, integration, and smoke coverage
- `docs/architecture.md`: concise architecture and extension notes
- `docs/comment_extractor.md`: how to use `CommentQuery` and related extractors
- `docs/git_workflow.md`: branch policy, development-only artifacts, and the
  main-branch guard
