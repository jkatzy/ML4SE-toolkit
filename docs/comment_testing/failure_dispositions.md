# Comment Failure Dispositions

Every case emitted by a fuzz run, judge report, dataset audit, or adversarial
breaker receives exactly one disposition. This is one-to-one accounting, not a
growing model-validation ledger.

Keep the investigation table in the pull request or tracked issue. Keep raw
manifests, reports, transcripts, journals, and model rationales under ignored
`tmp/`. The durable repository evidence is the linked deterministic test,
fixture, harness calibration case, or manifest-builder test.

## Historical baseline, not closure evidence

The stale ledger covered 496 buckets from 2026-06-03 through 2026-06-08 at
commit `b0f7f76` and implementation fingerprint `55e43b0b40e0`: 259 pass and
237 fail. The failures were 83 extraction, 56 sanitation, 2 overall, 78 judge
command, and 18 manifest or sampling buckets. They predate fixes including
`d4e7f7c`, `63b5a46`, `bf13e7f`, `3615113`, and `f9f41f2`.

Only 14 of the 141 product case IDs appear verbatim in current tests, so that
ledger cannot support a one-to-one closure claim. The cleaned release branch
retains comment implementation fingerprint `707f4669fd7b` from baseline commit
`2aeb0f8` and has green deterministic coverage in
`tests/test_comment_extractor_failure_boundaries.py`,
`tests/test_stack_v2_comment_regressions.py`,
`tests/test_comment_sanitizer_regression_edges.py`, and
`tests/test_comment_cleaning_regressions.py`. That is a baseline, not proof that
old judge findings are closed. Closure requires a fresh pinned rerun or a
current deterministic regression for the specific case.

## Required record

Record these fields for every failure:

| Field | Requirement |
| --- | --- |
| Failure ID | Stable case ID; otherwise a SHA-256 of the minimal input |
| Source | Breaker, fuzz command and seed, or manifest hash and judge backend |
| Surface | Registry, extraction, cleaning, dataset, judge, or infrastructure |
| Disposition | Exactly one value from the table below |
| Evidence | Research citation or deterministic reproduction |
| Durable artifact | Test/fixture path and test node, or rerun evidence for infrastructure |
| Resolution | Pull request or commit that closes the item |

Sort records by failure ID and check that the set exactly equals the failure
IDs in the frozen run. Duplicates still receive separate records.

## Allowed dispositions

| Disposition | Meaning | Required closure |
| --- | --- | --- |
| `confirmed_product_defect` | Registry, parser, or sanitizer violates the researched contract | Add a deterministic failing regression before the fix; link the passing test after the fix |
| `confirmed_harness_defect` | Manifest, adapter, prompt construction, importer, or test harness is wrong | Add a deterministic harness regression and fix the harness before rerunning affected cases |
| `judge_false_positive` | Product behavior is correct but the judge reports failure | Add or retain a deterministic product assertion plus a calibration case; do not change product code to satisfy the model |
| `judge_false_negative` | Calibration shows the judge passes known bad behavior | Add a deterministic failing calibration case and reject or revise the judge configuration |
| `dataset_or_label_defect` | Source, language label, offsets, or sampled boundary is invalid | Add a deterministic manifest/filter regression when code can prevent recurrence; record the dataset revision and upstream action |
| `unsupported_or_out_of_scope` | Research proves the case is outside the declared language/dialect contract | Add an executable boundary assertion or explicit registry/manifest exclusion; create a scoped implementation issue if support is desired |
| `duplicate_root_cause` | A distinct case is exercised by an existing root-cause regression | Link the exact test and enumerate the duplicate case ID in its parameterization or compact provenance |
| `infrastructure_rerun` | Timeout, quota, unavailable model, corrupt transfer, or interrupted run produced no trustworthy case verdict | Fix the environment and rerun the same frozen input; never convert it to product pass/fail |

`infrastructure_rerun` is valid only for operational events. Once a run emits a
case verdict, that case needs a case-level disposition.

## Closure rules

- Every confirmed product or harness defect has a deterministic regression.
- Every rejected model finding has a deterministic product assertion and a
  calibration disposition.
- Every dataset exclusion is testable or pinned to a reviewed dataset revision.
- One test can cover several cases, but every case ID remains visible in the
  accounting.
- No item is closed solely because another model says `pass`.
- No item is closed solely because it cannot be reproduced with a different
  seed, manifest, model, or commit.
- Temporary evidence is deleted or retained locally after review; it is never
  promoted wholesale into `docs/`.

For large cleaner runs, the annotation and oracle-exception inputs accepted by
`scripts/import_comment_cleaning_regressions.py` must partition the entire
frozen failure ID set. For repaired runs,
`scripts/import_repaired_comment_failures.py` preserves one compact fixture or
accounting record per classified failure. Use their count and hash checks to
prove there are no omissions.
