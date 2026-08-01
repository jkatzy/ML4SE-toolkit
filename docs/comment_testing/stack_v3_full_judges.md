# Stack v3 Full Judge Manifests

The Stack v3 full adapter builds frozen comment-judge manifests from a local
flat JSONL export. It never contacts Hugging Face, downloads source, or falls
back to `HuggingFaceCode/stack-v3-train`.

## Export boundary

Accept the gated dataset terms and use an authorized Hugging Face credential,
normally `HF_TOKEN`, in a separate approved export process. Export exactly:

- dataset: `HuggingFaceCode/stack-v3-full`;
- revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`;
- table or configuration: `contents`;
- format: JSONL with one source file per top-level object.

The manifest builder does not read or record `HF_TOKEN`. Its required input is
the resulting local JSONL path. Each row needs a string `language` and string
`content` field. `lang` or `programming_language`, and `text` or `code`, are
also recognized. Use `--language-field` and `--content-field` through
`STACK_V3_FULL_JUDGE_MANIFEST_ARGS` when an approved export uses other names.
Keep stable identity fields such as `blob_id`, `repo_name` or `repo`, and
`path` when they are available.

A row containing nested `files: [...]` is a repository-level Stack v3 train
shape and is rejected. If a row includes `dataset`, `dataset_name`,
`dataset_revision`, or `dataset_table`, those values must match the pinned full
dataset identity above. The builder records the exact input SHA-256, but the
operator remains responsible for exporting the asserted revision.

For a large corpus export, filter it to the exact requested dataset language
labels before building, or set `COMMENT_JUDGE_MAX_RECORDS_PER_LANGUAGE` high
enough to reach each requested language. A JSON language map can translate
registry keys to exact export labels:

```bash
STACK_V3_FULL_JUDGE_MANIFEST_ARGS="--language-map tmp/stack-v3-language-map.json"
```

## Build and run

Build and validate a frozen manifest under an ignored `tmp/` directory:

```bash
make stack-v3-full-comment-judge-coverage \
  STACK_V3_FULL_JUDGE_INPUT=/path/to/stack-v3-full-contents.jsonl \
  COMMENT_JUDGE_LANGUAGES=java,python \
  COMMENT_JUDGE_PER_KIND=20 \
  STACK_V3_FULL_JUDGE_OUTPUT_ROOT=tmp/stack-v3-full-judge-2026-08-01
```

After reviewing `manifest.jsonl`, `failures.jsonl` when present, and
`provenance.json`, run one case before the full judge:

```bash
make stack-v3-full-comment-judge-smoke \
  STACK_V3_FULL_JUDGE_OUTPUT_ROOT=tmp/stack-v3-full-judge-2026-08-01 \
  COMMENT_JUDGE_BACKEND=codex \
  STACK_V3_FULL_JUDGE_LEDGER=0

make stack-v3-full-comment-judge-test \
  STACK_V3_FULL_JUDGE_OUTPUT_ROOT=tmp/stack-v3-full-judge-2026-08-01 \
  COMMENT_JUDGE_BACKEND=codex
```

The adapter reuses the existing manifest and judge harness. Generated source
files, manifests, failure records, provenance, reports, and validation ledgers
must remain below `tmp/` and untracked. Freeze the manifest and its recorded
hash before comparing models.
