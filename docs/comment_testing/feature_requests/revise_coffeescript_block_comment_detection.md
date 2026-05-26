# Feature Request: Revise CoffeeScript Block Comment Detection

## Summary

The Stack v2 judge-case manifest generator found CoffeeScript line comments but
found no CoffeeScript block comments while scanning 1000 CoffeeScript records.
Treat this as a syntax-support/research feature request, not as an extraction or
sanitizer regression.

## Evidence

- Language: `coffeescript`
- Comment kind: `block`
- Expected sample target: 10 source files containing block comments
- Actual sample result: 0 block-comment files after 1000 scanned records
- Observed related coverage: 10 line-comment files were collected
- Current registry example under review:

  ```coffeescript
  ###
  note
  ###
  ```
- Generated report:
  `tmp/stack_v2_comment_judge_coffeescript_until_fail/reports/manifest-coffeescript-block-manifest_generation-28a6634b.md`

## Requested Work

Revise CoffeeScript block comment detection and support policy. Confirm whether
triple-hash block comments are valid for the CoffeeScript version and file types
represented in Stack v2. If valid, update the registry or manifest sampling
logic so block comments can be found and covered deterministically. If not valid
for this corpus, remove or exclude CoffeeScript block comments from the Stack v2
judge manifest expectation and document the reason in the syntax research notes.

## Acceptance Criteria

- The CoffeeScript registry entry and documentation reflect the reviewed block
  comment support decision.
- `make comment-judge-manifest COMMENT_JUDGE_LANGUAGES=coffeescript` either
  collects the expected block-comment cases or records an intentional exclusion
  rather than a generic missing-bucket failure.
- Follow-up deterministic tests are added only after the valid CoffeeScript
  block-comment contract is confirmed.
