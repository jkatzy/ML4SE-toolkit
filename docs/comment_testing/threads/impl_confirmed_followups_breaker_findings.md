# Confirmed Followups Breaker Findings

Assigned languages:
graph_modeling_language, mask, selinux_policy, srecode_template, txl,
unix_assembly, valve_data_format, x_bit_map, x_pix_map, xbase, zil, zimpl.

## Scope

- Worktree: `/home/jovyan/work/tmp/comment_implementation_worktrees/confirmed_followups`
- Fixture generation: ran `uv run python scripts/build_comment_language_fixtures.py`
  without `--force`.
- Existing dirty files observed before edits: `src/ml4setk/Parsing/Comments/registry.py`
  and `docs/comment_syntax_matrix.md`; not edited by this breaker pass.
- Edited only assigned files under `tests/fixtures/comment_languages/` plus this
  findings file.

## Fixture Additions

Added parser-accepted adversarial cases to:

- `graph_modeling_language.code`: inline `#` after quoted `#` data, plus a line
  comment preserving `# Heading` and `C#` content.
- `mask.code`: `//` URL-like content containing `//`, plus `/* ... */` content
  preserving `# Heading` and `//` as body text.
- `selinux_policy.code`: inline policy `#` comment preserving `#ifdef` and `C#`,
  plus a standalone Markdown-like `# Heading` preservation case.
- `srecode_template.code`: inline `;;` comment preserving `;;` and `--flag`, plus
  a standalone `;;` line preserving semicolon content.
- `txl.code`: trailing `%` comment preserving `%VAR%` and `%%time`, plus a
  standalone percent comment preserving `100%` and `%matplotlib`.
- `unix_assembly.code`: GAS `#` comment preserving `#include` and `C#`, plus a
  `/* ... */` block preserving `#` and `//` markers as body text.
- `valve_data_format.code`: `//` trailing VDF comment preserving URL `//` and
  `C#`, plus a standalone `//` comment preserving `//` as content.
- `x_bit_map.code`: C89 block comment preserving `#define`, `//`, and `C#`.
- `x_pix_map.code`: C-wrapper block comment preserving `#define`, `//`, and `C#`.
- `xbase.code`: `&&`, `NOTE`, and `/* ... */` cases; a non-comment separator was
  inserted between `NOTE` and block comments to avoid the grouping bug recorded
  below.
- `zil.code`: one-line `;"..."` string comment with escaped quotes and an inner
  semicolon.
- `zimpl.code`: inline and standalone `#` comments preserving `#heading`, `#
  Heading`, and `C#`.

## Sanitizer Observations

Entry points used: `CommentQuery(language).parse(source)` followed by
`CommentSanitizer(language).sanitize(match)`.

Accepted fixture additions preserved meaning-bearing marker text after removing
the outer comment syntax:

- `# breaker_gml_inline keeps C# and #heading` -> `breaker_gml_inline keeps C#
  and #heading`
- `// breaker_mask_line_with_url http://example.test/a//b and C#` ->
  `breaker_mask_line_with_url http://example.test/a//b and C#`
- `/* breaker_mask_block_with_hash # Heading and // marker */` ->
  `breaker_mask_block_with_hash # Heading and // marker`
- `# breaker_selinux_inline keeps #ifdef and C#` ->
  `breaker_selinux_inline keeps #ifdef and C#`
- `;; breaker_srecode_inline keeps ;; literal and --flag` ->
  `breaker_srecode_inline keeps ;; literal and --flag`
- `% breaker_txl_percent_body 100% complete and %matplotlib stays content` ->
  `breaker_txl_percent_body 100% complete and %matplotlib stays content`
- `# breaker_unix_hash keeps #include and C#` ->
  `breaker_unix_hash keeps #include and C#`
- `/* breaker_unix_block contains # hash and // slash markers */` ->
  `breaker_unix_block contains # hash and // slash markers`
- `// breaker_vdf_markdown // Heading marker remains content` ->
  `breaker_vdf_markdown // Heading marker remains content`
- `/* breaker_xbm_block contains #define, // marker, and C# */` ->
  `breaker_xbm_block contains #define, // marker, and C#`
- `/* breaker_xpm_block contains #define, // marker, and C# */` ->
  `breaker_xpm_block contains #define, // marker, and C#`
- `&& breaker_xbase_inline keeps && literal and --flag` ->
  `breaker_xbase_inline keeps && literal and --flag`
- `NOTE breaker_xbase_note keeps NOTE: tag in body` ->
  `breaker_xbase_note keeps NOTE: tag in body`
- `/* breaker_xbase_block contains && and NOTE tokens */` ->
  `breaker_xbase_block contains && and NOTE tokens`
- `;"breaker_zil_escaped_quote \"inner\" and semicolon ; stays"` ->
  `breaker_zil_escaped_quote \"inner\" and semicolon ; stays`
- `# breaker_zimpl_inline keeps #heading and C#` ->
  `breaker_zimpl_inline keeps #heading and C#`

These cover paired removal/preservation behavior: the language delimiter is
removed as scaffolding, while the same or related symbols remain when they are
inside the content-bearing body.

## Findings-Only Bugs

### ZIL Generated Multiline Fixture Is Not Parseable

Status: confirmed existing failure.

Baseline command before fixture edits:

```bash
uv run pytest tests/test_comment_language_fixtures.py -q --no-cov
```

Result: `zil` failed before breaker fixture additions. The generated expected
match is:

```text
;"
 * star_doc_1 Description of what the method does.
 *
 * @param input Description of parameter.
 * @return Description of return value.
 * @throws Exception Description of exception.
"
```

Current parsed matches for the generated ZIL fixture only include:

```text
;"fixture_1"
;"inline_block_1"
```

The registry pattern for ZIL is the single-line `;"..."`
string-comment form, so the fixture generator's C-style star-doc expansion is
not parseable for this language. This looks like a fixture-generator or
registry-metadata contract bug, not a breaker-added fixture issue.

### xBase `NOTE` Overmatches Identifiers

Status: confirmed parser/sanitizer bug or dialect-policy issue.

Probe input:

```text
NOTEBOOK := "field"
? NOTEBOOK
```

Actual parser output:

```text
NOTEBOOK := "field"
```

Actual sanitizer output:

```text
BOOK := "field"
```

Expected behavior: `NOTEBOOK` should remain ordinary code unless the xBase
policy intentionally treats any line beginning with `note` as a comment. The
Harbour/Clipper-style `NOTE` comment form should likely require a keyword
boundary after `NOTE` or `NOTE*`.

### xBase Adjacent `NOTE` Line And Block Comment Are Grouped

Status: confirmed parser grouping bug with sanitizer fallout.

Probe input:

```text
NOTE breaker_xbase_note keeps NOTE: tag in body
/* breaker_xbase_block contains && and NOTE tokens */
? "after"
```

Actual parser output is one combined match:

```text
NOTE breaker_xbase_note keeps NOTE: tag in body
/* breaker_xbase_block contains && and NOTE tokens */
```

Actual sanitizer output leaves both syntaxes in place:

```text
NOTE breaker_xbase_note keeps NOTE: tag in body
/* breaker_xbase_block contains && and NOTE tokens */
```

Expected behavior: the `NOTE` line and the `/* ... */` block should be separate
comments. A non-comment separator was used in the fixture addition so the
accepted fixture cases do not depend on this broken grouping behavior.

## Unsupported Or Disputed Probes

These probes were not added to fixtures. Outcomes are based on the current
registry policy and local parser behavior.

- `graph_modeling_language`: `/* block? */` produced no matches. Outcome:
  no-change-needed for current hash-only policy.
- `selinux_policy`: `/* block? */` produced no matches. Outcome:
  no-change-needed for current hash-only policy.
- `srecode_template`: single-semicolon `;` produced no matches. Outcome:
  no-change-needed for current `;;` policy.
- `txl`: `/* block? */` produced no matches. Outcome: no-change-needed for
  current percent-line policy.
- `valve_data_format`: `/* block as data? */` produced no matches. Outcome:
  no-change-needed for current `//`-only VDF policy.
- `x_bit_map`: `// modern C comment?` produced no matches. Outcome:
  no-change-needed under the current portable C89 XBM policy; policy review is
  needed before adding C99-style `//`.
- `x_pix_map`: `// modern C comment?` produced no matches. Outcome:
  no-change-needed under the current XPM3/C-wrapper block-only policy; policy
  review is needed before adding carrier-dialect `//`.
- `zil`: general semicolon expression comment produced no matches. Outcome:
  no-change-needed for current conservative `;"..."` string-comment policy.
- `zimpl`: `/* block? */` produced no matches. Outcome: no-change-needed for
  current hash-only policy.
- `mask`: nested-looking `/* outer /* inner */ tail */` parsed only through the
  first close delimiter as `/* outer /* inner */`. Outcome: documented
  limitation/no-change-needed under the current non-nested MaskJS block policy.
- `unix_assembly`: nested-looking `/* outer /* inner */ tail */` parsed only
  through the first close delimiter as `/* outer /* inner */`. Outcome:
  documented limitation/no-change-needed under the current non-nested GNU as
  block policy.

## Verification

- Pre-edit baseline: `uv run pytest tests/test_comment_language_fixtures.py -q
  --no-cov` failed only on the existing ZIL generated multiline fixture issue.
- Post-edit parser probe: every added `breaker_` fixture case appears in
  `CommentQuery(...).parse(...)` output and sanitizes as recorded above.
- Final fixture pytest result is expected to remain blocked by the same ZIL
  generated multiline fixture failure until the fixer updates generator,
  registry metadata, or parser policy.
