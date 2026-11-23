# Agent Guide

This file is development-only. It belongs on `dev` with the research and test
operations guides; it must not be promoted to `main`.

## Branch policy

- `main` is the release branch. It contains releasable code, deterministic
  regression tests, and stable user documentation.
- `dev` is the single long-lived integration branch. It contains everything on
  `main` plus agent instructions, research notes, and testing operations docs.
- Promote reviewed, fully tested changes from `dev` to `main`. Run
  `make check-main-branch` on the promotion candidate; it intentionally fails on
  `dev` while development-only files are present.
- Use a short-lived topic branch only when review requires one, then delete it
  after merge. Do not create another permanent branch.
- Keep generated manifests, sampled datasets, model responses, judge reports,
  and scratch downloads untracked. A confirmed failure becomes a minimized
  deterministic regression test before its fix is promoted.

See `docs/git_workflow.md` for the permanent repository policy.

## Choose a workflow

Role files under `agents/` mirror the package paths below `src/`. Place each
role at the highest package where its task applies throughout the subtree.
Select the role by task and use the owning source module for context, including
when work starts from a test, reproduction script, or documentation page.

| Task | Scope | Instructions |
| --- | --- | --- |
| Run or audit a paper reproduction | Any paper-backed module in `ml4setk` | [Reproduction agent](agents/ml4setk/reproduction.md) |
| Implement a published method | Any paper-backed module in `ml4setk` | [Implementation workflow](agents/ml4setk/implementation.md) |
| Add a comment syntax or investigate a parser failure | `ml4setk.Parsing.Comments` | [Comment parser workflow](agents/ml4setk/Parsing/Comments/workflow.md) |
| Promote or release a change | Whole repository | [Git workflow](docs/git_workflow.md) |

## Setup and verification

Create and sync the development environment:

```bash
uv venv .venv
make setup
```

Use the narrowest relevant test first.

Before promotion, run:

```bash
make test
make lint
make comment-fuzz
make comment-cleaner-fuzz
```

Run `make test-optional` when optional Tree-sitter behavior changes. Use
`make smoke` for a quick package-level check, and run `make build` plus
`uvx twine check dist/*` for a release candidate.

Optional dependencies must not break core imports. Tests needing an optional
extra use the `optional_dependency` marker.
