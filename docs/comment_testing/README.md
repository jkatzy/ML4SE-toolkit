# Comment Testing Workflow

This directory holds a development-only adversarial testing workflow for the
comment parser and downstream comment sanitization.

The workflow is intentionally agent-oriented:

- a breaker agent adds parseable adversarial cases to per-language fixture
  files and records candidates that still expose parser or sanitizer gaps
- a fixer agent validates those findings, adds regression tests, and patches
  the parser, registry, or sanitizer logic when needed

## Canonical command

Generate the current prompt packets and chunk assignments with:

```bash
make comment-test-prompts
```

That command rebuilds:

- `docs/comment_testing/agent_chunk_assignments.json`
- `docs/comment_testing/prompt_packets/`

It also creates missing breaker/fixer thread files under
`docs/comment_testing/threads/` without overwriting existing findings.

## Stack v2 LLM Judge Tests

Use the Stack v2 judge workflow when you want real-corpus coverage for both
comment extraction and sanitizer behavior. This is a manual, opt-in testing
path because it streams Stack v2/S3 data and launches Codex judge processes.

Canonical local flow:

```bash
make comment-judge-manifest \
  COMMENT_JUDGE_LANGUAGES='python,java,coffeescript' \
  COMMENT_JUDGE_PER_KIND=10
make comment-judge-smoke
make comment-judge-test
make comment-judge-testgen-pipeline
```

The judge test prints live per-case progress by default so large manifests do
not look hung. Disable that with `COMMENT_JUDGE_PROGRESS=0` when needed.

Before launching Codex for a case, the judge test checks
`stack_v2_judge_validation_ledger.md` for the current committed comment parser,
sanitizer, registry, and judge-contract fingerprint. Buckets that already passed
for that version are skipped, and buckets with recorded failures fail fast with
the previous report link. Relevant comment-code files must be clean and
committed before the ledger can validate or record a run. Use
`COMMENT_JUDGE_FORCE=1` only when you intentionally want to rerun a cached
bucket.

`make comment-judge-manifest` writes
`tmp/stack_v2_comment_judge/manifest.jsonl`, optional incomplete-bucket failures
in `tmp/stack_v2_comment_judge/failures.jsonl`, and sampled source files under
`tmp/stack_v2_comment_judge/files/`. Failure rows are deliberate pytest
failures, not generation failures: if a kind such as `coffeescript/block` cannot
be found in the scanned corpus, `make comment-judge-test` reports it explicitly.
Treat that as a feature request for syntax research or registry policy, not as
an extraction/sanitation regression. Review the syntax or document/exclude that
kind rather than silently skipping it.
When judge tests fail, they write Markdown reports under
`tmp/stack_v2_comment_judge/reports/` by default. If Codex reports a usage,
quota, or rate limit, the run aborts immediately with
`COMMENT_JUDGE_USAGE_LIMIT_EXIT_CODE` (default `88`) instead of continuing to
launch judge cases. Use `make comment-judge-generate-tests` to hand existing
parser/sanitizer reports to Codex test-generation agents, or `make
comment-judge-testgen-pipeline` to run the judge suite and then process
reports. Manifest-generation reports are skipped by test generation and should
be converted into feature requests. Those agents should add normal
deterministic pytest coverage for the
expected behavior and must not add another LLM-judge assertion or implement the
production fix. Extraction and sanitation failures should become separate
assertions or separate tests. Generated corpus files and reports must not be
committed. The central validation ledger is committed because it records only
language/kind status, code fingerprints, and report links.

The manifest target uses `--fetch-stack-v2-content` and unsigned public
Software Heritage S3 requests by default. No AWS credentials are needed unless
you explicitly pass `--s3-sign-requests`. It prints flushed manifest progress to
stderr, so `nohup.out` should show language, scanned-record, and collected-case
updates while it is running. For local Stack v2 JSONL exports that already
contain source text, run
`scripts/build_stack_v2_comment_judge_cases.py --input-jsonl ...` directly.

Inspect cached coverage for a manifest with:

```bash
uv run python scripts/comment_judge_validation_ledger.py status \
  --manifest tmp/stack_v2_comment_judge/manifest.jsonl
```

Full details, direct commands, environment variables, and troubleshooting are in
`stack_v2_judge_workflow.md`.

## Layout

- `adversarial_playbook.md`: how the breaker and fixer roles should work
- `sanitizer_playbook.md`: sanitizer-specific removal vs preservation guidance
- `thread_template.md`: reference structure for per-chunk findings and
  resolutions
- `../../tests/fixtures/comment_languages/`: one editable code fixture file
  per supported language; breakers add cases here when the current parser
  should still parse them correctly
- `agent_chunk_assignments.json`: current chunk-to-language map
- `prompt_packets/`: generated breaker and fixer prompts per chunk
- `threads/`: breaker findings and fixer resolution logs

## Generated Fixture Coverage

The per-language fixture generator currently emits these parser cases for
implemented languages when the registry marks the relevant syntax as
applicable:

- seeded registry examples for each supported line, block, and nested comment
  form
- repeated symbol line-comment openers such as `////////` for `//` and
  `########` for `#`
- odd repeated openers for homogeneous even-length openers, such as `///` for
  `//`, `---` for `--`, and `;;;` for `;;`
- inline block or nested comments with runnable-looking code before and after
  the comment
- star-prefixed multiline documentation blocks, including C-style
  `/** ... */` comments with `* @param`, `* @return`, and `* @throws` lines
- grouped adjacent standalone line comments that should parse as a single
  comment block
- string-probe cases where comment-looking delimiters appear inside simple
  quoted strings and must not be returned as parsed comments

Fixture tests assert that expected comments appear once, parse once, and that
string-probe sentinels never appear in parsed comment matches. The fixture
folder check only considers files ending in `.code`, so development scratch
files such as editor swap files do not invalidate the fixture set.

## Intended loop

1. Generate prompt packets.
2. Spawn one breaker and one fixer per chunk.
3. The breaker updates the assigned
   `tests/fixtures/comment_languages/*.code` files with representative
   adversarial cases that should parse correctly with current behavior. The
   breaker must preserve the seeded fixture comments, separate added comments
   with non-comment code lines when needed, and verify fixture edits with
   `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov`.
4. The breaker records coverage for every assigned language and each relevant
   scenario family, including fixture edits, confirmed bugs that could not be
   left in the fixture file, ambiguous contracts, reviewed no-issue outcomes,
   and internet-sourced probes for scenarios that research previously marked
   as unsupported or absent. For sanitizer cases, the breaker records both the
   raw extracted match and the sanitized output, with an explicit note about
   which characters should be removed as syntax noise and which must be
   preserved as meaning-bearing text. Those sources are not limited to Stack
   Overflow; GitHub, SourceForge, project docs, issue trackers, blogs,
   tutorials, and similar sources are all in scope.
5. The fixer validates breaker fixture edits, turns confirmed gaps into
   regression tests and minimal code changes, and records `no-change-needed`
   outcomes for reviewed cases that are already correct, preserving the
   contract that only superfluous syntax clutter is stripped while
   semantically important characters survive. Once a parser gap is fixed, the
   fixer may add the now-stable case to the relevant fixture file.
6. Regenerate packets as the supported-language set changes.

## Scope

This workflow exists to improve tests for already-implemented languages. It is
not the same as the comment-research workflow under `docs/comment_research`,
which is for discovering and validating new language syntaxes.

The goal is systematic coverage, not triage to only the highest-priority
findings. Each assigned language should end a pass with either concrete
findings or an explicit reviewed-no-issue outcome for the relevant scenario
families.

Fixture files are editable test inputs, not immutable generator output. The
generator seeds missing files from registry examples, while
`tests/test_comment_language_fixtures.py` ensures the seeded comments still
appear once and remain parseable after breaker-added cases are appended.

Sanitizer-oriented work is still grounded in real extracted comments. The
sanitizer playbook defines the two-sided contract:

- remove comment-syntax scaffolding, decorative gutters, delimiter-only lines,
  and padding-only indentation when they are not part of the actual comment
  text
- preserve semantically important punctuation and markers such as Markdown
  headings, list bullets, TODO tags, code examples, CLI flags, language names
  like `C#` or `C++`, and deliberate repeated punctuation inside the comment
  body
- whenever a sanitizer rule removes a symbol in one testcase, add a paired
  testcase where the same symbol is preserved because it is semantically part
  of the comment content
