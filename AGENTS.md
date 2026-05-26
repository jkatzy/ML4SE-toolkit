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
- `make comment-test-prompts`
- `make comment-judge-manifest`
- `make comment-judge-smoke`
- `make comment-judge-test`
- `make comment-judge-generate-tests`
- `make comment-judge-testgen-pipeline`
- `make check-main-branch`

## Repo map

- `src/ml4setk/Parsing`: parsing contracts and query implementations
- `src/ml4setk/Parsing/Comments/registry.py`: seeded language matrix for comment syntax
- `src/ml4setk/Generation`: model-input builders and iterable loaders
- `tests`: unit, regression, integration, and optional-dependency coverage
- `docs/architecture.md`: architecture notes and extension points
- `docs/comment_syntax_matrix.md`: evidence worksheet for comment-language research
- `docs/comment_research`: chunk reports, backlog views, and online-first worker packets
- `docs/comment_testing`: adversarial breaker/fixer and Stack v2 LLM judge testing workflows for implemented languages

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
- Adversarial parser-test expansion for implemented languages should use the
  breaker/fixer workflow in `docs/comment_testing`.
- Real-corpus LLM judge checks for extraction and sanitation should use
  `docs/comment_testing/stack_v2_judge_workflow.md`; keep generated Stack v2
  manifests, sampled source files, and judge failure reports out of commits.
- Judge failure reports are handoff artifacts for test-generation agents. Turn
  them into normal deterministic pytest coverage instead of adding permanent
  LLM-judge assertions for known regressions.
- Stack v2 LLM judge runs must use the central validation ledger in
  `docs/comment_testing/stack_v2_judge_validation_ledger.md` so already-tested
  language/comment-kind buckets are skipped for the same committed code
  fingerprint. Commit relevant comment-code changes before recording ledger
  entries, and use `COMMENT_JUDGE_FORCE=1` only for intentional reruns.


## Coding standard

- Keep production changes small and local to the feature boundary being edited.
- Prefer typed, named helpers over repeating offset arithmetic, tuple indexing,
  or ad hoc string slicing in parser code.
- Public classes, public functions, and non-obvious internal helpers should use
  Python docstrings with JavaDoc-style sections: `Args:`, `Returns:`, and
  `Raises:` when applicable. Keep comments factual and tied to invariants.
- Keep language-specific comment syntax in
  `src/ml4setk/Parsing/Comments/registry.py`. Parser classes may orchestrate
  matching, grouping, sorting, deduplication, and `QueryMatch` construction, but
  must not add new language branches.
- Comment extraction code must preserve source-order output and the exact
  `QueryMatch(prefix, suffix, match)` contract. When range math is needed, use
  shared helpers rather than recalculating offsets inline.
- Compatibility APIs that return legacy tuple shapes must document the tuple
  contract next to the public entry point and stay aligned with the registry
  whenever syntax changes are necessary.
- Add or update focused tests for every parser behavior change. For registry-only
  language additions, seed examples in the registry so generated tests cover the
  syntax.
- Run the narrowest relevant pytest target first, then broader tests or `make
  lint` when the change touches shared parser behavior.

## Git workflow

- Do agent-assisted or research-heavy work on development branches, not on
  `main`.
- `AGENTS.md`, `docs/comment_research/`, `docs/comment_testing/`,
  `docs/comment_syntax_matrix.md`, and `docs/comment_syntax_stack_v2.md` are
  development-only artifacts.
- Scratch directories such as `tmp/` and `scratch/`, plus tracked temporary
  files such as `*.tmp`, `*.bak`, `*.orig`, `*.rej`, and `*.swp`, are allowed
  during development but must not land on `main`.
- Before merging to `main`, run `make check-main-branch`.
- For the permanent workflow document, see `docs/git_workflow.md`.
