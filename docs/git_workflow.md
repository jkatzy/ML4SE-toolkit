# Git Workflow

The repository has two long-lived branches:

- `main` is always release-ready.
- `dev` is the integration branch for active development, agent instructions,
  research evidence, and operational testing guides.

Short-lived topic branches may be used for review, but they branch from `dev`,
target `dev`, and are deleted after merge. Release pull requests promote tested
code from `dev` to `main`.

## Main branch standard

Keep on `main`:

- package source and public APIs
- deterministic unit, integration, fuzz-invariant, and regression tests
- regression fixtures with provenance notices
- stable user and architecture documentation
- build, release, and reproducible validation tooling

Do not keep on `main`:

- `AGENTS.md`
- comment research workbooks or evidence staging
- adversarial prompt packets, agent reports, or judge ledgers
- operational LLM-judge documentation
- scratch directories or editor backup files

Run the following before every release merge:

```bash
make lint
make test
make test-optional
make check-main-branch
make check-release-version
make build
```

## Dev branch standard

`dev` contains everything on `main`, plus the development-only material under
`docs/comment_research/` and `docs/comment_testing/`, and the root
`AGENTS.md`. Comment extraction or cleaning changes begin on `dev`; confirmed
failures become deterministic tests and fixtures before promotion to `main`.

Generated corpora, downloaded repositories, judge transcripts, and raw failure
reports stay under ignored `tmp/` or `scratch/` paths. Only durable evidence,
reusable instructions, and minimized regressions are committed.

## Enforcement

- `make check-main-branch` rejects development-only paths on `main`.
- CI runs the guard on pushes to `main` and pull requests targeting `main`.
- Branch protection should require CI on both `main` and `dev` and restrict
  direct pushes to `main`.
