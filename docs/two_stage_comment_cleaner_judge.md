# Two-stage comment cleaner judge

`scripts/run_two_stage_comment_cleaner_judge.py` is the resumable,
cleaning-only judge for large real-corpus manifests. It ignores the manifest's
`cleaned_comment` snapshot and recomputes every candidate from `raw_comment`
with the current `CommentSanitizer`.

The fixed model policy is:

1. Judge every case with `gpt-5.6-luna`.
2. Send only Luna failures to `gpt-5.6-sol`.
3. Use Sol's result as the final decision for escalated cases.

Both Codex subprocesses use `--ask-for-approval never`, `--sandbox read-only`,
and `--ephemeral`. Each model runs in a fresh empty temporary working
directory with user configuration and repository rules ignored, so its verdict
is independent of the checkout and local Codex instructions. The runner
validates exactly one structured verdict for every requested `case_id`.

## Running

First create a Stack v2 manifest. For the explicit all-registry-language,
50-distinct-files scope, use the resumable per-language shard orchestrator:

```bash
uv run --with boto3 --with datasets --with 'smart_open[s3]' \
  python scripts/run_stack_v2_comment_manifest_pipeline.py \
  --all-languages \
  --files-per-language 50 \
  --dataset bigcode/the-stack-v2-dedup \
  --language-workers 4 \
  --output-root tmp/stack_v2_comment_cleaner_all_languages_50
```

Every completed language shard is fingerprinted and reused on restart,
including explicit corpus shortfalls. The command requires `--all-languages`
or an exact `--languages` list so an accidental invocation cannot start a
large transfer. Dataset access and source retrieval are separate from the
judge and remain subject to the dataset's current access terms.

Then run:

```bash
make comment-cleaner-judge-two-stage \
  COMMENT_CLEANER_TWO_STAGE_MANIFEST=tmp/stack_v2_comment_cleaner_all_languages_50/manifest.jsonl \
  COMMENT_CLEANER_TWO_STAGE_OUTPUT_ROOT=tmp/stack_v2_comment_cleaner_all_languages_50/two_stage
```

The default input is
`tmp/stack_v2_comment_cleaner_judge/manifest.jsonl`; output is written beneath
`tmp/stack_v2_comment_cleaner_judge/two_stage`. Common scale controls are:

```bash
make comment-cleaner-judge-two-stage \
  COMMENT_CLEANER_TWO_STAGE_BATCH_SIZE=50 \
  COMMENT_CLEANER_TWO_STAGE_MAX_PROMPT_CHARS=80000 \
  COMMENT_CLEANER_TWO_STAGE_WORKERS=4 \
  COMMENT_CLEANER_TWO_STAGE_TIMEOUT=300
```

Cases are greedily packed into same-language batches, with both a 50-case hard
maximum and a prompt-character target. `raw_comment` and
`candidate_cleaned_comment` are never truncated or summarized. If either
string exceeds `--max-text-chars` (12,000 by default), the complete case is
sent alone even when its prompt exceeds `--max-prompt-chars`; a model/context
failure aborts the run and cannot be recorded as a pass. `run_summary.json`
reports `full_judgment_input_strings`, `oversized_case_policy`, and the number
of `full_fidelity_singleton_cases`.

If a response has missing, duplicate, or unknown case IDs, the runner
recursively splits that batch. A malformed single-case response is retried
once. Command failures, timeouts, and usage limits abort instead of being
treated as cleaning failures.

## Resume and output files

`run_metadata.json` fingerprints the exact manifest, freshly computed
sanitizer candidates, model policy, prompt settings, full-fidelity oversized
case policy, and isolated model environment. Reusing an output directory with
different inputs, settings, or judge protocol fails clearly; use a new output
directory for a different run.

Validated results are fsynced to append-only journals after every batch:

- `primary_results.jsonl`
- `secondary_results.jsonl`

On restart, completed cases are skipped. A truncated last journal line is
discarded safely; corruption in any completed line aborts the resume. Final
derived files are written atomically:

- `final_results.jsonl`: one merged primary/secondary result per case
- `final_failures.jsonl`: machine-readable final failures with raw and cleaned text
- `final_failures.md`: human-readable failures with embedded machine payloads
- `run_summary.json`: counts and input fingerprints

The command exits `0` when every final decision passes, `1` when final cleaning
failures remain, `2` for operational or validation errors, and the configured
comment-judge usage-limit exit code (normally `88`) for quota exhaustion.
Generated corpus samples and reports may contain sensitive public-source text;
keep the output directory out of commits.

## Local verification without model calls

The focused synthetic suite mocks Codex and exercises batching, escalation,
resume, reports, structured-output validation, and usage-limit handling:

```bash
uv run pytest tests/test_two_stage_comment_cleaner_judge.py -q --no-cov
```
