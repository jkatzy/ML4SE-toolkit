# Comment Extraction and Cleaning Test Guide

This directory is the development guide for validating comment extraction and
cleaning. It belongs on `dev`; release-ready code, fixtures, and deterministic
tests belong on `main`.

## Required workflow

1. Research the language and dialect before changing the registry. Follow the
   [comment syntax research workflow](../comment_research/README.md).
2. Establish the deterministic baseline for the affected language.
3. Write adversarial breaker cases and reduce every failure to the smallest
   useful example.
4. Run the parser and sanitizer fuzz campaigns with recorded seeds.
5. Use an LLM judge only as a secondary reviewer over a frozen manifest.
6. Give every reported failure exactly one disposition.
7. Add a deterministic regression before fixing every confirmed defect.
8. Run the focused tests, then the full non-optional suite and lint checks.

The detailed guides are:

- [Adversarial testing](adversarial_testing.md)
- [Deterministic fuzzing](fuzzing.md)
- [LLM judge setup and calibration](llm_judges.md)
- [Regression test policy](regressions.md)
- [Failure dispositions](failure_dispositions.md)

## Baseline

Install the development environment and run the comment-focused deterministic
tests before starting an investigation:

```bash
make setup
uv run pytest \
  tests/test_comment_registry.py \
  tests/test_comment_queries.py \
  tests/test_comment_extractor_failure_boundaries.py \
  tests/test_stack_v2_comment_regressions.py \
  tests/test_comment_sanitizer_regression_edges.py \
  tests/test_comment_cleaning_regressions.py \
  -q --no-cov
```

Tests marked `optional_dependency` require `make setup-optional`.

## Artifact policy

Manifests, source samples, model prompts, transcripts, journals, reports, and
adjudication scratch files are run artifacts. Write them below `tmp/`, which is
ignored by Git, and do not commit them. They may contain dataset text or model
output that is unsuitable for the repository.

The old Markdown judge ledger is stale historical state. Do not copy it into
this branch and do not use it as an oracle. New runs keep their ledger below
the selected `tmp/` output root by default; set `COMMENT_JUDGE_LEDGER=0` only
for a disposable diagnostic. Durable outcomes are limited to:

- parser or sanitizer code;
- minimized deterministic tests and fixtures;
- compact provenance or hashes required by a fixture importer;
- curated workflow updates in this directory.

## Completion gate

A comment change is complete only when:

- every emitted case ID has one documented disposition;
- every confirmed extraction or cleaning defect has a deterministic regression
  that fails without the fix and passes with it;
- rejected judge findings have deterministic calibration evidence;
- the same frozen inputs were used when comparing judge backends or models;
- `make test` and `make lint` pass, plus `make test-optional` when the changed
  path uses optional parsers.

An LLM pass never overrides a deterministic failure, and a larger fuzz budget
never replaces a saved regression.
