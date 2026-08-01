# LLM Judge Setup and Calibration

LLM judges are secondary reviewers for ambiguous extraction and cleaning
behavior. They are nondeterministic, model-dependent, and vulnerable to bad
instructions in source text. They do not define expected output and must not be
a required release gate.

## Data and artifact boundary

Judge inputs can contain third-party source and model output. Before using a
hosted backend, confirm that the dataset license and data-handling policy permit
the transfer. Do not put credentials or private source in a judge manifest.

Keep manifests, failures, prompts, transcripts, journals, reports, run
summaries, and validation ledgers below `tmp/`. The directory is ignored by
Git. The historical Markdown validation ledger is stale; do not copy or extend
it. The Make targets default to a ledger in the selected output root. Disable
ledger recording only for a disposable diagnostic with:

```bash
COMMENT_JUDGE_LEDGER=0
```

Pin the Git commit, dataset revision, manifest SHA-256, provider, exact model,
temperature, scope, and command in the investigation or pull request.

## Build a frozen manifest

The default manifest target fetches Stack v2 source content and samples line,
block, nested, and contextual kinds for selected languages:

```bash
make comment-judge-manifest \
  COMMENT_JUDGE_LANGUAGES=python,java,coffeescript \
  COMMENT_JUDGE_PER_KIND=20 \
  COMMENT_JUDGE_OUTPUT_ROOT=tmp/comment-judge-2026-08-01

make comment-judge-coverage \
  COMMENT_JUDGE_LANGUAGES=python,java,coffeescript \
  COMMENT_JUDGE_OUTPUT_ROOT=tmp/comment-judge-2026-08-01
```

Do not regenerate the manifest while comparing models. All comparisons must
use the same file and hash.

## Single-stage backends

The combined scope judges extraction and cleaning. The cleaner targets use a
cleaning-only contract and treat `raw_comment` as an accepted input boundary.
Start with one case:

```bash
make comment-judge-smoke \
  COMMENT_JUDGE_BACKEND=codex \
  COMMENT_JUDGE_OUTPUT_ROOT=tmp/comment-judge-2026-08-01 \
  COMMENT_JUDGE_LEDGER=0
```

Codex requires an authenticated `codex` CLI. The adapter invokes `codex exec`
ephemerally with a read-only sandbox and a strict output schema. Optional model
and profile overrides are available through `COMMENT_JUDGE_CODEX_MODEL` and
`COMMENT_JUDGE_CODEX_PROFILE`.

For Ollama, start its local server and ensure the exact model is present:

```bash
make comment-judge-test \
  COMMENT_JUDGE_BACKEND=ollama \
  COMMENT_JUDGE_LOCAL_PROVIDER=ollama \
  COMMENT_JUDGE_LOCAL_MODEL=gemma4:31b \
  COMMENT_JUDGE_LOCAL_TEMPERATURE=0 \
  COMMENT_JUDGE_OUTPUT_ROOT=tmp/comment-judge-2026-08-01
```

For a vLLM OpenAI-compatible server:

```bash
make comment-judge-test \
  COMMENT_JUDGE_BACKEND=vllm \
  COMMENT_JUDGE_LOCAL_PROVIDER=vllm \
  COMMENT_JUDGE_LOCAL_MODEL=your-exact-served-model \
  COMMENT_JUDGE_LOCAL_BASE_URL=http://localhost:8000/v1 \
  COMMENT_JUDGE_LOCAL_TEMPERATURE=0 \
  COMMENT_JUDGE_OUTPUT_ROOT=tmp/comment-judge-2026-08-01
```

Use `comment-cleaner-judge-manifest`, `comment-cleaner-judge-smoke`, and
`comment-cleaner-judge-test` for cleaning-only runs. Set
`COMMENT_CLEANER_JUDGE_OUTPUT_ROOT` to an ignored `tmp/` directory.

`make comment-judge-full-run` is the resumable, per-language Ollama pipeline.
It is expensive and should follow calibration and a focused smoke run.

## Two-stage cleaner judge

The two-stage runner recomputes sanitizer output from a frozen cleaner manifest.
It asks `gpt-5.6-luna` to judge every case, then sends only primary failures to
`gpt-5.6-sol`. Both model names are fixed by the runner. Results are append-only,
fsynced journals; reruns resume only when the manifest and input fingerprints
still match.

```bash
make comment-cleaner-judge-manifest \
  COMMENT_JUDGE_LANGUAGES=python,java \
  COMMENT_CLEANER_JUDGE_OUTPUT_ROOT=tmp/cleaner-two-stage

make comment-cleaner-judge-two-stage \
  COMMENT_CLEANER_JUDGE_OUTPUT_ROOT=tmp/cleaner-two-stage \
  COMMENT_CLEANER_TWO_STAGE_WORKERS=4 \
  COMMENT_CLEANER_TWO_STAGE_TIMEOUT=300
```

The runner exits nonzero when final failures remain. Review
`two_stage/final_failures.jsonl`, `two_stage/final_failures.md`, and
`two_stage/run_summary.json` as temporary evidence. Never treat the secondary
model's decision as the expected cleaned string.

## Prompt-injection resistance

Raw comments and candidate outputs are untrusted quoted data. Include
calibration cases containing instructions such as "ignore the contract,"
fabricated JSON verdicts, Markdown fences, role labels, tool requests, and text
that asks the judge to reveal secrets or return `pass`.

The two-stage prompt explicitly tells models never to follow instructions in
the strings, and all adapters validate a strict verdict schema. Schema
validation prevents malformed output; it does not prove semantic resistance.
Reject a judge configuration that follows payload instructions or changes a
verdict when only injection text is added as content.

Run judges with no write access, no repository secrets, and an empty or
read-only working directory. Keep rationales short and avoid reproducing source
text unnecessarily.

## Calibration

Before judging a new dataset or model:

1. Freeze a small, hand-reviewed set with balanced extraction pass/fail and
   cleaning pass/fail cases, including confusing but correct boundary pairs.
2. Add prompt-injection and very long input cases.
3. Run the exact same manifest at temperature zero through each candidate
   backend. Repeat enough times to expose instability.
4. Measure false passes, false failures, malformed responses, backend
   disagreement, and repeated-run disagreement separately.
5. Define acceptance thresholds before the production run. Prefer the
   configuration with the lowest false-pass rate for destructive cleaning.
6. Give every disagreement a disposition. Save durable calibration examples as
   deterministic harness tests or fixtures, not as a model ledger.

The repository validates adapters and harness behavior in
`tests/test_codex_comment_judge.py`, `tests/test_local_comment_judge.py`,
`tests/test_stack_v2_comment_judge.py`, and
`tests/test_two_stage_comment_cleaner_judge.py`.

## From finding to test

`make comment-judge-generate-tests` can ask Codex to draft tests from temporary
failure reports. It is an accelerator only. Review, minimize, and prove every
generated assertion independently. For cleaner consensus review and
hash-pinned fixture import, inspect:

```bash
uv run python scripts/run_comment_cleaning_failure_oracle.py --help
uv run python scripts/import_comment_cleaning_regressions.py --help
uv run python scripts/import_repaired_comment_failures.py --help
```

All final findings follow the [regression policy](regressions.md) and receive a
[failure disposition](failure_dispositions.md).
