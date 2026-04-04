# Thread Template

Use this structure for per-chunk adversarial testing threads.

## Breaker findings

```md
# Adversarial Findings: chunk_X

### language_key

- Family: `family_name`
- Status: pending | confirmed-bug | ambiguous-contract | no-high-value-case
- Findings:
  - Case: short label
  - Parser entry point: `CommentQuery` | `OpeningCommentQuery` | `CommentSanitizer`
  - Input:
    ```text
    ...
    ```
  - Actual behavior:
    ```text
    ...
    ```
  - Expected behavior:
    ```text
    ...
    ```
  - Why it matters: ...
```

## Fixer resolution

```md
# Adversarial Resolution: chunk_X

### language_key

- Status: fixed-in-code | fixed-in-tests | documented-limitation | needs-policy-decision
- Resolution: ...
- Tests: ...
```
