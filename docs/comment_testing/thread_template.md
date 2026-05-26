# Thread Template

Use this structure for per-chunk adversarial testing threads.

## Breaker findings

```md
# Adversarial Findings: chunk_X

### language_key

- Family: `family_name`
- Fixture file: `tests/fixtures/comment_languages/language_key.code`
- Status: pending | confirmed-bug | ambiguous-contract | reviewed-no-issue
- Findings:
  - Case: short label
  - Fixture edit: path and unique sentinel added, or `findings-only`
  - Fixture parse check: command and pass/fail result
  - Extraction entry point: `CommentQuery` | `OpeningCommentQuery`
  - Sanitizer entry point: `CommentSanitizer` | exact helper name | n/a
  - Input:
    ```text
    ...
    ```
  - Raw extracted match:
    ```text
    ...
    ```
  - Actual behavior:
    ```text
    ...
    ```
  - Sanitized output:
    ```text
    ...
    ```
  - Expected behavior:
    ```text
    ...
    ```
  - Expected sanitized output:
    ```text
    ...
    ```
  - Removal contract: which characters are syntax noise and should be removed
  - Preservation contract: which characters are semantically important and must remain
  - Paired preservation testcase: the companion case that keeps the same symbol
    because it is meaningful
  - Source/provenance: URL, local synthesis note, or registry-derived
  - Why it matters: ...
```

## Fixer resolution

```md
# Adversarial Resolution: chunk_X

### language_key

- Status: fixed-in-code | fixed-in-tests | documented-limitation | needs-policy-decision | no-change-needed | ambiguous-contract
- Resolution: ...
- Fixture updates: fixture paths changed, cases kept/removed, and parser
  verification result
- Sanitizer notes: what was removed, what must now be preserved, or why the
  limitation is intentional
- Paired-case coverage: where the matching keep-vs-remove tests live
- Tests: ...
```
