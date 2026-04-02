# Git Workflow

`main` is the release-ready branch. Development branches may carry extra
working material while research, agent-assisted exploration, and cleanup are
still in progress, but `main` must stay publishable.

## Branch rules

- `development-base` is the long-lived base branch for shared development
  workflow files and agent instructions.
- Create all future development branches from `development-base`, not directly
  from `main`.
- Do feature and research work on named development branches.
- Do not merge `development-base` directly to `main`.
- Merge to `main` only when the branch is safe to publish and maintain.
- Before merging to `main`, run `make check-main-branch`.

## Allowed on development branches only

These are useful during active work, but they must not land on `main`:

- `AGENTS.md`
- `docs/comment_research/`
- `docs/comment_syntax_matrix.md`
- `docs/comment_syntax_stack_v2.md`
- scratch directories such as `tmp/` and `scratch/`
- tracked temporary files such as `*.tmp`, `*.bak`, `*.orig`, `*.rej`, and `*.swp`

## Main branch standard

`main` must not contain:

- agent instructions or agent-only workflow files
- raw agent outputs, prompt packets, or chunk reports
- temporary research staging artifacts
- scratch files or editor backup files

If development-only work produces something valuable, promote the stable result
into permanent code, tests, or user-facing documentation and remove the raw
artifact before merging.

## Enforcement

- `make check-main-branch` runs the repository guard locally.
- CI runs the same guard on pushes to `main` and pull requests targeting
  `main`.
