# Feature Request: Review Emacs Lisp Nested Comment Stack v2 Sampling

## Summary

The Stack v2 judge-case manifest generator found enough Emacs Lisp line-comment
cases but found only 8 nested-comment cases while scanning 10000 Emacs Lisp
records for a 20-per-kind run. Treat this as a corpus coverage and sampling
policy review, not as a parser or sanitizer regression.

## Evidence

- Language: `emacs_lisp`
- Comment kind: `nested`
- Expected sample target: 20 source files containing nested-delimiter comments
- Actual sample result: 8 nested-comment files after 10000 scanned records
- Observed related coverage: 20 line-comment files were collected
- Current registry example under review:

  ```emacs-lisp
  #| outer #| inner |# outer |#
  ```

- Generated report:
  `tmp/stack_v2_emacs_lisp_20_ollama/languages/emacs_lisp/reports/manifest-emacs_lisp-nested-manifest_generation-ff208651.md`
- Follow-up validation:
  `tests/test_stack_v2_comment_judge.py::test_stack_v2_comment_extraction_and_cleaning_with_llm_judge`
  passed for all 28 collected Emacs Lisp cases with the Ollama `gemma4:31b`
  judge and ledger disabled.

## Requested Work

Review Emacs Lisp nested comment sampling policy for Stack v2. Confirm whether
the `#| ... |#` nested-delimiter syntax should remain a required 20-case bucket
for this corpus. If the syntax is valid but rare, prefer raising
`--max-records-per-language`, lowering the per-kind target for this bucket, or
adding an explicit rare-bucket policy instead of changing parser behavior. If
the collected samples show the manifest generator is accepting non-comment
matches, add deterministic parser coverage before changing extraction logic.

## Acceptance Criteria

- The Emacs Lisp registry entry and Stack v2 judge workflow document the
  reviewed nested-comment sampling decision.
- `make comment-judge-manifest COMMENT_JUDGE_LANGUAGES=emacs_lisp` either
  collects the expected nested-comment cases or records an intentional
  rare-bucket policy rather than a generic missing-bucket failure.
- Follow-up deterministic tests are added only if review confirms a parser,
  sanitizer, or sampler bug.
