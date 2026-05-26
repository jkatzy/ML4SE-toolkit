# Stack v2 Judge Workflow

This workflow samples real Stack v2 files and checks comment extraction plus
sanitization with an external LLM-as-a-judge agent. It is an opt-in manual
workflow: it is not part of `make test` or CI because it streams corpus data and
launches one Codex judge process per case.

## Prerequisites

- Run from a development branch, not `main`.
- Sync normal test tooling with `uv sync --group dev`.
- Install or expose a working `codex` CLI for judge execution.
- Use `--fetch-stack-v2-content` or `make comment-judge-manifest` when reading
  the official `bigcode/the-stack-v2` dataset. The official stream contains file
  IDs and metadata, not source text.
- The Stack v2 content fetch uses unsigned requests against the public Software
  Heritage S3 bucket by default. It needs `boto3` and `smart_open`; the Makefile
  target supplies them with transient `uv run --with` dependencies.
- Pass `--s3-sign-requests` only when you intentionally need the local AWS
  credential chain.

## Canonical Make Flow

Generate a manifest with ten distinct files per supported comment kind for each
requested language:

```bash
make comment-judge-manifest \
  COMMENT_JUDGE_LANGUAGES='python,java,coffeescript' \
  COMMENT_JUDGE_PER_KIND=10
```

The target writes:

```text
tmp/stack_v2_comment_judge/manifest.jsonl
tmp/stack_v2_comment_judge/failures.jsonl
tmp/stack_v2_comment_judge/files/
```

`failures.jsonl` is present only when at least one language/comment-kind bucket
could not be sampled. Treat those rows as failure cases, not as skipped judge
cases. For example, if `coffeescript/block` has `0/10` after 1000 scanned
records, review whether the registry syntax is valid for Stack v2, lower the
per-kind target, or explicitly remove/exclude that kind with a research note.

Manifest generation prints flushed progress lines such as
`[stack-v2 manifest] language=python collected ...`, so `nohup.out` should show
activity before the final manifest is written. Tune the scan interval with
`COMMENT_JUDGE_PROGRESS_EVERY=50`, or pass advanced generator flags with
`COMMENT_JUDGE_MANIFEST_ARGS=...`.

Run one Codex-judged case first as a smoke test:

```bash
make comment-judge-smoke
```

Run the full generated judge suite:

```bash
make comment-judge-test
```

Run the judge suite and then hand any failure reports to Codex
test-generation agents:

```bash
make comment-judge-testgen-pipeline
```

That pipeline stops after deterministic tests or fixtures are generated. It
does not ask Codex to implement parser, registry, sanitizer, or manifest
fixes. To process existing reports without rerunning the judge suite, use:

```bash
make comment-judge-generate-tests
```

During the run, each case prints progress lines such as
`[stack-v2 judge 4/90] ... judge-start` and `judge-done elapsed=...`. This is
intentional for large manifests, where each case launches a separate Codex
process. Set `COMMENT_JUDGE_PROGRESS=0` if you need to suppress progress output.
Any judge, judge-command, or manifest-generation failure also writes a per-case
Markdown report under `tmp/stack_v2_comment_judge/reports/` by default. Judge
and judge-command reports include a test-generation-agent task block for adding
deterministic pytest coverage. Manifest-generation reports are missing
language/comment-kind buckets; they include feature-request guidance for syntax
research or registry policy instead of parser-test generation instructions.

Useful Make variables:

- `COMMENT_JUDGE_LANGUAGES`: comma-separated registry languages, default
  `python,java,coffeescript`. Use registry keys such as `c++`, `c#`, and
  `f#`; common underscore aliases such as `c_plus_plus`, `c_sharp`, and
  `f_sharp` are accepted and normalized before sampling.
- `COMMENT_JUDGE_PER_KIND`: target files per comment kind, default `10`
- `COMMENT_JUDGE_OUTPUT_ROOT`: generated manifest/source root, default
  `tmp/stack_v2_comment_judge`
- `COMMENT_JUDGE_MANIFEST`: manifest consumed by pytest, default
  `$(COMMENT_JUDGE_OUTPUT_ROOT)/manifest.jsonl`
- `COMMENT_JUDGE_FAILURES`: generation failures consumed by pytest, default
  `$(COMMENT_JUDGE_OUTPUT_ROOT)/failures.jsonl`
- `COMMENT_JUDGE_REPORT_DIR`: per-case failure report directory, default
  `$(COMMENT_JUDGE_OUTPUT_ROOT)/reports`
- `COMMENT_JUDGE_LEDGER`: Markdown validation ledger, default
  `docs/comment_testing/stack_v2_judge_validation_ledger.md`; set to `0` to
  disable ledger checks for local diagnostics
- `COMMENT_JUDGE_FORCE`: set to `1` to rerun a cached pass/fail bucket for the
  current code fingerprint
- `COMMENT_JUDGE_TIMEOUT`: outer pytest timeout per case, default `240`
- `COMMENT_JUDGE_CODEX_TIMEOUT`: Codex subprocess timeout per case, default
  `180`
- `COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE`: special non-zero exit code used when
  Codex reports a usage, quota, or rate limit, default `88`
- `COMMENT_JUDGE_PROGRESS_EVERY`: manifest-generation scanned-record progress
  interval, default `10`
- `COMMENT_JUDGE_MANIFEST_ARGS`: extra flags appended to
  `scripts/build_stack_v2_comment_judge_cases.py`, for example
  `--no-progress` or `--fail-on-incomplete`
- `COMMENT_TESTGEN_CODEX_TIMEOUT`: timeout per test-generation Codex agent,
  default `600`
- `COMMENT_TESTGEN_CODEX_SANDBOX`: Codex sandbox for test-generation agents,
  default `workspace-write`; use `danger-full-access` only when the local
  bubblewrap sandbox fails before file access
- `COMMENT_TESTGEN_REPORT_LIMIT`: optional maximum number of reports to
  process during test generation
- `COMMENT_TESTGEN_REPORTS`: optional explicit report paths to process

If failures are written, `make comment-judge-manifest` still exits
successfully by default. The failure is reported by `make comment-judge-test` as
one pytest failure per missing language/comment kind. Use
`COMMENT_JUDGE_MANIFEST_ARGS=--fail-on-incomplete` only when you want generation
itself to return non-zero.

Do not commit generated Stack v2 source files or judge failure reports. Commit
`docs/comment_testing/stack_v2_judge_validation_ledger.md` when it changes; it
is the central cache of which language/comment-kind buckets passed or failed for
a committed code fingerprint.

## Validation Ledger

The judge harness consults `COMMENT_JUDGE_LEDGER` before launching Codex. The
default ledger path is
`docs/comment_testing/stack_v2_judge_validation_ledger.md`. Each entry records
the language, comment kind, pass/fail status, case count, judge model, report
link, git commit, and a SHA-256 fingerprint over the committed comment parser,
sanitizer, registry, Stack v2 sampler, and judge-contract files.

Relevant comment-code files must be clean and committed before a ledger-aware
judge run starts. This prevents recording expensive LLM validation against a
working-tree state that cannot be recovered later. If a bucket already passed
for the current fingerprint, pytest skips it before starting Codex. If a bucket
has a recorded failure for the current fingerprint, pytest fails fast and prints
the prior report path. Set `COMMENT_JUDGE_FORCE=1` only when you intentionally
want to rerun a cached bucket. Partial runs with `COMMENT_JUDGE_CASE_LIMIT` do
not record passed coverage.

Inspect current manifest coverage without launching judges:

```bash
uv run python scripts/comment_judge_validation_ledger.py status \
  --manifest tmp/stack_v2_comment_judge/manifest.jsonl
```

When pytest prints `Failure report: ...`, use the failure-report regression
loop below.

## Failure Report Regression Loop

Judge failures are discovery signals. They should be turned into ordinary
deterministic tests before the parser, registry, or sanitizer is changed. The
LLM judge should not become the permanent assertion for a known regression.

1. Run the judge suite and note every `Failure report: ...` path printed by
   pytest. Reports are written under `$(COMMENT_JUDGE_REPORT_DIR)`, defaulting
   to `tmp/stack_v2_comment_judge/reports/`.
2. Pass extraction, sanitation, overall, or judge-command reports to a
   test-generation agent. The automated path is
   `make comment-judge-generate-tests`; manifest-generation reports are skipped
   by that runner and should become feature requests instead. The manual
   equivalent for parser/sanitizer reports uses a prompt like:

   ```text
   Read tmp/stack_v2_comment_judge/reports/<report>.md. Add deterministic
   pytest coverage for the expected behavior in that report. Use the actual
   behavior only to understand the current failure. Do not add an LLM judge
   assertion. Put the test in the closest extraction, sanitizer, or registry
   test module, then run the narrowest relevant pytest target.
   ```

3. The test-generation agent reads these report sections:

   - `Expected Behavior`: the assertion target for the new deterministic test
   - `Actual Behavior`: the current failing parser or sanitizer output
   - `Judge Context`: source excerpt, verdict, rationale, or generation context
   - `Machine Payload`: JSON form for agents that prefer structured input

4. For extraction failures, add or update a test that calls `CommentQuery` and
   asserts the full raw comment match. Keep span-sensitive assertions in
   deterministic tests only when the report or bug explicitly requires them;
   the LLM judge itself does not validate character spans.
5. For sanitation failures, add or update a test that calls `CommentSanitizer`
   on the extracted match and asserts the cleaned text. Keep extraction and
   sanitation assertions separate when the report separates them.
6. For manifest-generation failures, create or update a feature request for
   syntax research and registry policy. These failures mean the corpus sampler
   could not find a language/comment-kind bucket; they do not prove that
   extraction or sanitation is wrong. Add deterministic tests only after the
   valid syntax contract is confirmed.
7. After the deterministic test exists, fix the parser, registry, or sanitizer,
   rerun the focused pytest target, and rerun the judge case or manifest bucket
   only when the deterministic failure is resolved.

The acceptance criteria for a completed report are: a normal pytest regression
exists, it would have failed before the fix, the implementation passes it, and
the generated report file remains uncommitted.

## Direct Manifest Commands

The Makefile path is preferred for official Stack v2 because it supplies the S3
fetch dependencies. The equivalent direct command is:

```bash
uv run --with boto3 --with 'smart_open[s3]' \
  python scripts/build_stack_v2_comment_judge_cases.py \
  --languages python,java,coffeescript \
  --per-kind 10 \
  --progress-every 10 \
  --fetch-stack-v2-content \
  --output-root tmp/stack_v2_comment_judge
```

The generator resolves Stack v2 config names such as `CoffeeScript`, `ABAP`,
`ASN.1`, `C-Sharp`, and `F-Sharp` from registry language keys.

If your local Stack v2 export is JSONL with source content already included,
use it instead of S3 fetching:

```bash
uv run python scripts/build_stack_v2_comment_judge_cases.py \
  --input-jsonl /path/to/stack-v2-sample.jsonl \
  --language-field language \
  --content-field content \
  --languages python,java \
  --per-kind 10 \
  --output-root tmp/stack_v2_comment_judge
```

## Direct Judge Command

The pytest harness is opt-in because it needs both sampled data and an agent
command. The command must read the judge prompt from stdin and print JSON to
stdout.

```bash
STACK_V2_COMMENT_JUDGE_MANIFEST=tmp/stack_v2_comment_judge/manifest.jsonl \
STACK_V2_COMMENT_JUDGE_REPORT_DIR=tmp/stack_v2_comment_judge/reports \
COMMENT_JUDGE_USE_CODEX=1 \
uv run pytest tests/test_stack_v2_comment_judge.py -q --no-cov
```

This launches one non-interactive Codex agent per pytest case through
`scripts/run_codex_comment_judge.py`. The adapter runs `codex exec` with
`--sandbox read-only`, `--ask-for-approval never`, and a JSON schema for the
final verdict.

You can still use another judge command by setting `COMMENT_JUDGE_AGENT_CMD`;
that command must read the prompt from stdin and print JSON to stdout.

Useful environment variables:

- `STACK_V2_COMMENT_JUDGE_FAILURES`: optional JSONL failure file. When rows
  exist, pytest reports one explicit failure per missing language/comment kind.
- `STACK_V2_COMMENT_JUDGE_REPORT_DIR`: optional directory for per-case failure
  reports. Defaults to `reports/` next to the manifest when unset.
- `COMMENT_JUDGE_LEDGER`: optional Markdown ledger path. Defaults to
  `docs/comment_testing/stack_v2_judge_validation_ledger.md`; use `0` to
  disable ledger checks for diagnostics.
- `COMMENT_JUDGE_FORCE`: set to `1` to ignore cached pass/fail entries and
  launch judges for the requested cases.
- `COMMENT_JUDGE_CASE_LIMIT`: run only the first N manifest cases
- `COMMENT_JUDGE_PROGRESS`: set to `0`, `false`, `no`, or `off` to suppress
  live per-case progress lines
- `COMMENT_JUDGE_TIMEOUT`: per-case outer pytest timeout in seconds, default
  `120` in the pytest harness
- `COMMENT_JUDGE_CODEX_TIMEOUT`: per-case Codex process timeout in seconds,
  default `180`
- `COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE`: exit code used to abort the pytest
  session when the judge output indicates an LLM usage, quota, or rate limit;
  default `88`
- `COMMENT_JUDGE_CODEX_MODEL`: optional model override for `codex exec`
- `COMMENT_JUDGE_CODEX_PROFILE`: optional Codex config profile
- `CODEX_BIN`: Codex executable name or path, default `codex`

## Judge Contract

The test does not directly assert exact raw or cleaned strings. It sends
sampled target raw/cleaned content, nearby current extracted comment content,
and current sanitized content to the judge agent. It does not send character
offsets, line/column numbers, span-overlap metadata, or marked source excerpts;
the LLM judge evaluates only returned content. The sampled target came from a
previous parser run, so deterministic follow-up tests should confirm any
ambiguous case before production behavior is changed. The agent must return
JSON:

```json
{
  "verdict": "pass",
  "extraction_correct": true,
  "cleaning_correct": true,
  "rationale": "short explanation"
}
```

The pytest test fails when the judge command fails or when the JSON shape is
invalid. Missing required fields are reported explicitly, including whether the
judge omitted `extraction_correct` or `cleaning_correct`. Extraction and
sanitation are asserted separately: a false `extraction_correct` produces an
extraction-specific pytest failure, a false `cleaning_correct` produces a
sanitation-specific pytest failure, and a non-`pass` `verdict` is reported as a
separate overall-judge disagreement. Judge failures include an `Expected vs
actual` JSON block with the sampled raw/cleaned comment and the parser/sanitizer
outputs the judge evaluated. Manifest-generation failures include expected and
actual counts plus the syntax examples that were being searched for. The same
payload is written as a Markdown failure report so a follow-up test-generation
agent can add a normal deterministic regression test without consulting the
LLM judge again.

## Troubleshooting

- `failures.jsonl` contains a row such as `coffeescript/block`: treat it as
  a real failure case for the sampled corpus. Review the registry syntax and
  Stack v2 examples before expecting judge coverage for that kind.
- `nohup.out` shows only the Make command and `Error 137`: the manifest
  generation process was killed before it wrote `manifest.jsonl`. Rerun with
  current progress output and watch for the last `[stack-v2 manifest]` line.
- `Unable to locate credentials`: update to the current generator and rerun
  without `--s3-sign-requests`; unsigned public S3 is the default.
- `The official bigcode/the-stack-v2 stream contains file IDs`: add
  `--fetch-stack-v2-content`, use `make comment-judge-manifest`, or provide a
  local JSONL export with a source-content field.
- `Stack v2 judge already passed`: the validation ledger has a passing entry
  for this language/comment kind and code fingerprint. Nothing was sent to
  Codex. Use `COMMENT_JUDGE_FORCE=1` only when you need to rerun it.
- `Stack v2 judge previously failed`: the validation ledger has a failure entry
  for this language/comment kind and code fingerprint. Inspect the linked
  report, add deterministic coverage or a feature request as appropriate, then
  rerun with `COMMENT_JUDGE_FORCE=1` if you need a fresh judge result.
- `validation requires relevant comment-code files to be committed`: commit or
  stash relevant parser, sanitizer, registry, sampler, and judge-contract
  changes before running the expensive ledger-aware judge suite.
- `LLM judge usage limit was reached`: pytest intentionally exits the whole
  judge run with `COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE` instead of continuing to
  launch doomed judge cases. Resume after the account limit resets, or lower
  `COMMENT_JUDGE_CASE_LIMIT` for a smaller run.
- `judge command failed`: inspect the pytest failure block; it includes the
  judge process stderr and stdout, plus a failure report path when reports are
  enabled.
- `bwrap: loopback: Failed RTM_NEWADDR`: rerun only the test-generation
  stage with `COMMENT_TESTGEN_CODEX_SANDBOX=danger-full-access`; keep the
  agent prompt constrained to tests only and inspect the resulting diff.
- `judge verdict missing required field`: the judge command did not return the
  required JSON shape.
