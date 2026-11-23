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

## Adding a published membership-inference method

Work under `src/ml4setk/MIA/`. Use the AST-PAC, PAC, and Loss entries in
[`docs/membership_inference.md`](docs/membership_inference.md) as examples.

1. **Identify the method and its baselines.** Verify the conference or journal
   version with the publisher. Record the title, all authors in publication
   order, venue, year, and DOI or proceedings URL. Give each baseline its own
   module entry and credit both its originators and the study evaluating it.
   Link an existing entry when a later paper uses the same baseline.
2. **Establish provenance.** Follow the authors' artifact link. Pin a version
   DOI or commit and identify the files relevant to the contribution. If the
   authors released no artifact, record the sources checked and what evidence
   will be used for verification.
3. **Decide what may ship.** Record whether the contribution is original code,
   a port, a dependency, or redistributed material. Check the paper, code,
   datasets, and fixtures separately. Compare the applicable terms with both
   the toolkit license file and its distribution metadata. For third-party
   material record the copyright holder, license, compatibility reasoning,
   required notices and their shipping location. When rights are unclear,
   leave that material out and document what evidence would resolve the issue.
4. **Define and test the contribution.** Specify which part of the paper the
   API covers, its inputs, conventions, output, and any deviations. Put the
   method citation in its module docstring and user documentation. Add
   deterministic tests for the conventions most likely to change results.
   Keep large reference artifacts external and optional imports local.
5. **Run every experiment behind every plot.** Inventory the published paper
   and appendices by figure, panel, series, and experimental condition. Include
   experimental tables. Run each configuration with the toolkit, including the
   baselines, sweeps, and repeats used for uncertainty estimates. A single run
   can support multiple panels when they use the same measurements.
   The only exception is a configuration that cannot fit the available hardware.
   Record the configuration, hardware capacity, and measured usage, failure log,
   or defensible resource estimate. Run all configurations that fit. Other
   blockers leave the experiment pending and the paper reproduction incomplete.
6. **Record the reproduction.** Name the exact paper table or artifact result,
   model, cohorts, metric definition, comparison precision, command, and
   observed result. Mirror the path of each paper-backed module under `src/`.
   For `src/<package>/<module>.py`, publish its report at
   `docs/reproduction_reports/<package>/<module>/index.md` and its script at
   `reproductions/<package>/test_<module>.py`. Keep data, figures, and appendices
   with the owning report. Add it to the package index and MkDocs navigation. Put a
   baseline comparison in the report and script for the paper that ran it.
   Pair each reference value with the measured toolkit value in a table or plot.
   Link each result in the inventory to its script command and paired measurements.
   Report outstanding experiments and hardware exceptions explicitly.
   Publish the citation and reuse record beside the example in the MIA guide.
   Run the focused tests, `make lint`, and `make smoke`.

## Setup and verification

Create and sync the development environment:

```bash
uv venv .venv
make setup
```

Use the narrowest relevant test first. A practical comment-parser target is:

```bash
uv run pytest \
  tests/test_comment_registry.py \
  tests/test_comment_queries.py \
  tests/test_comment_generated_cases.py \
  tests/test_comment_sanitizer.py \
  -q --no-cov
```

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

## Repository map

- `src/ml4setk/Parsing/Comments/registry.py`: comment syntax, aliases,
  contextual extractor names, sanitizer metadata, evidence, and seeded examples
- `src/ml4setk/Parsing/Comments/CommentQuery.py`: generic matching, range,
  grouping, ordering, and `QueryMatch` construction
- `src/ml4setk/Parsing/Comments/CommentSanitizer.py`: syntax-aware comment
  cleaning
- `tests`: deterministic unit, generated, adversarial, fuzz, and regression
  coverage
- `docs/comment_research/README.md`: evidence-first language intake workflow
- `docs/comment_research/report_template.md`: reusable research record
- `docs/comment_testing/README.md`: adversarial, fuzzing, judge, and regression
  operations

## Parser and registry invariants

- Every extraction API returns `QueryMatch(prefix, suffix, match)` with exact
  source slices. Matches remain ordered by source position and do not overlap.
- Language-specific syntax belongs in `COMMENT_SYNTAXES`. Keep query classes
  generic; add a narrowly scoped lexical or contextual helper only when a
  delimiter cannot express the format's semantics.
- Registry keys and aliases are unique lowercase names. Raw dataset labels may
  normalize during lookup, but the chosen key must be explicit and collision
  checked. Aliases share one `CommentSyntax` only when their syntax and dialect
  scope are genuinely equivalent.
- Every implemented regex, nested delimiter, or contextual extractor has a
  seeded `CommentExample`. Set `kind`, inline compatibility, grouping
  compatibility, wrappers, exclusions, and unclosed behavior deliberately.
- Preserve the public positional field order of `CommentSyntax`; append new
  metadata fields after the compatibility boundary.
- Unsupported or unresolved syntax raises `NotImplementedError`; uncertainty
  is not a reason to add a permissive marker pattern.
- Comment syntax that changed between language versions belongs in the
  family's `language_versions` table. The registry entry implements the
  default version; other versions overlay only what they change and need a
  differential test. See `docs/comment_research/version_dependent_comments.md`.
- Extraction and cleaning are separate contracts. A cleaner may remove verified
  comment scaffolding and normalize line endings, but must not silently discard
  comment content.
- Optional dependencies must not break core imports. Tests needing an optional
  extra use the `optional_dependency` marker.

## Language implementation workflow

1. Record the new dataset revision and label exactly as received.
2. Follow `docs/comment_research/README.md`; do not infer syntax from a language
   name or a related language.
3. Add or revise one registry family with pinned evidence and representative
   seeded examples. Treat version and dialect differences explicitly.
4. Add adversarial negative cases for strings, directives, operators, embedded
   languages, malformed input, line endings, and delimiter boundaries that are
   relevant to the syntax.
5. Run focused extraction and sanitizer tests, then both deterministic fuzz
   targets.
6. Minimize every failure into ordinary pytest coverage and verify that it fails
   before the fix and passes after it.
7. Run the full verification commands before promotion to `main`.

Do not use an LLM verdict as the permanent oracle. The judge workflow can find
and triage candidates; reviewed source evidence and deterministic tests define
the accepted behavior.
