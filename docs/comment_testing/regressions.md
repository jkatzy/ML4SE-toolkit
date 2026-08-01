# Comment Regression Test Policy

Every confirmed extraction or cleaning failure must become a deterministic
regression before the production fix is written. LLM reports, fuzz logs, and
dataset samples are discovery inputs, not permanent tests by themselves.

## Required sequence

1. Freeze the failing run under `tmp/` and record its command, Git commit,
   dataset revision, seed or manifest hash, and case ID.
2. Classify the failure using [failure dispositions](failure_dispositions.md).
3. Reduce the input without changing the failing behavior.
4. Write an exact deterministic assertion against a public API or a narrow
   internal contract.
5. Demonstrate that the new test fails on the pre-fix code for the intended
   reason.
6. Implement the fix and demonstrate that the same test passes.
7. Run neighboring syntax-family tests, the original fuzz seed or frozen judge
   cases, then the full suite.

Never derive an expected cleaner output from the sanitizer version being
tested. Establish exact output from the language contract and human review.

## Placement

Use the narrowest existing home:

- registry keys, aliases, and syntax metadata:
  `tests/test_comment_registry.py`, `tests/test_missing_comment_languages.py`;
- query behavior and ordinary extraction examples:
  `tests/test_comment_queries.py`, `tests/test_parse_comment.py`, and
  `tests/fixtures/comments/`;
- exact language fixture coverage:
  `tests/test_comment_language_fixtures.py` and
  `tests/fixtures/comment_languages/`;
- extraction boundary defects:
  `tests/test_comment_extractor_failure_boundaries.py` and
  `tests/test_stack_v2_comment_regressions.py`;
- sanitizer edge behavior:
  `tests/test_comment_sanitizer_regression_edges.py` and the existing
  `tests/test_comment_sanitizer_*.py` family suites;
- reviewed cleaning cases:
  `tests/test_comment_cleaning_regressions.py` and
  `tests/fixtures/comment_cleaning_regressions/`;
- repaired-run accounting and executable fixtures:
  `tests/test_repaired_comment_failure_fixtures.py` and
  `tests/fixtures/comment_cleaning_repaired_failures/`;
- fuzz harness contracts: `tests/test_comment_fuzzing.py`;
- judge adapters and prompt/harness behavior:
  `tests/test_codex_comment_judge.py`, `tests/test_local_comment_judge.py`,
  `tests/test_stack_v2_comment_judge.py`, and
  `tests/test_two_stage_comment_cleaner_judge.py`.

Extend an existing parameterized table or fixture family when it expresses the
case cleanly. Create a new test module only for a distinct contract.

## Assertion quality

A regression must include:

- the language registry key and relevant dialect or alias;
- the smallest raw source or accepted raw comment boundary;
- exact extracted raw text and/or exact cleaned output;
- enough surrounding code to prove boundaries for extraction defects;
- a compact case ID, source hash, or run hash when provenance may be retained;
- a name that states the previously broken contract.

Do not commit full source files, judge rationales, transcripts, repository
paths, or unrelated context merely for provenance. Hashes and compact metadata
are preferred.

One parameterized regression may close several equivalent failures only when
all affected case IDs or hashes are enumerated and the assertion executes each
distinct raw input. A duplicate disposition may point to the same root-cause
test, but no failure can disappear from accounting.

## Importing reviewed cleaner failures

The import tools enforce stronger provenance for large reviewed runs:

- `scripts/run_comment_cleaning_failure_oracle.py` produces temporary exact
  output proposals and independent reviews;
- `scripts/import_comment_cleaning_regressions.py` requires reviewed annotations,
  explicit oracle exceptions, counts, and pinned hashes, then writes
  family-sharded deterministic fixtures;
- `scripts/import_repaired_comment_failures.py` preserves one compact record per
  classified failure and only keeps literal input/output for executable
  sanitizer regressions;
- `scripts/import_final_comment_validation_failures.py` freezes a narrowly
  audited final validation set with pinned output hashes.

Read each tool's `--help`, review every oracle, use `--check` before `--force`
where available, and inspect the resulting diff. Importers do not replace human
classification.

## Verification

Run the narrow test node during reduction, then finish with:

```bash
make comment-fuzz COMMENT_FUZZ_SEED=0xC0FFEE
make comment-cleaner-fuzz COMMENT_FUZZ_SEED=0xC0FFEE
make test
make lint
```

Run `make test-optional` when optional tree-sitter paths or fixtures changed.
Judge reruns are supporting evidence and are not a substitute for these gates.
