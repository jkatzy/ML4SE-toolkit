# Agent Guide

This repository is optimized for small, explicit changes with fast local
verification.

## Setup

- Create the local environment with `uv venv .venv`.
- Sync core development tooling with `uv sync --group dev`.
- Install optional Tree-sitter support with `uv sync --group dev --extra treesitter`.

## Canonical commands

- `make setup`
- `make test`
- `make test-optional`
- `make lint`
- `make smoke`
- `make research-prompts`
- `make check-main-branch`

## Repo map

- `src/ml4setk/Parsing`: parsing contracts and query implementations
- `src/ml4setk/Parsing/Comments/registry.py`: seeded language matrix for comment syntax
- `src/ml4setk/Generation`: model-input builders and iterable loaders
- `tests`: unit, regression, integration, and optional-dependency coverage
- `docs/architecture.md`: architecture notes and extension points
- `docs/comment_syntax_matrix.md`: evidence worksheet for comment-language research
- `docs/comment_research`: chunk reports, backlog views, and online-first worker packets

## Invariants

- Core parsing APIs return `QueryMatch(prefix, suffix, match)`.
- `FIMInput` and `CausalInput` consume that normalized match contract.
- Optional dependencies must not break import-time behavior; failure should be
  deferred until the optional feature is instantiated.
- Tests that require optional extras must be marked `optional_dependency`.
- Comment-language expansion work must go through the registry and matrix doc,
  not through new `if/elif` branches in the parser.
- Stronger comment-language research should use the online-first playbook and
  packet generator in `docs/comment_research`.

## Git workflow

- The long-lived `development-base` branch is the base for agent-assisted
  development work and carries the shared agent instructions.
- Create all future development branches from `development-base`, not from
  `main`.
- Do agent-assisted or research-heavy work on development branches, not on
  `main`.
- Do not merge `development-base` directly to `main`.
- `AGENTS.md`, `docs/comment_research/`, `docs/comment_syntax_matrix.md`, and
  `docs/comment_syntax_stack_v2.md` are development-only artifacts.
- Scratch directories such as `tmp/` and `scratch/`, plus tracked temporary
  files such as `*.tmp`, `*.bak`, `*.orig`, `*.rej`, and `*.swp`, are allowed
  during development but must not land on `main`.
- Before merging to `main`, run `make check-main-branch`.
- For the permanent workflow document, see `docs/git_workflow.md`.
