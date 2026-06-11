# impl_o_r breaker findings

Worktree: `/home/jovyan/work/tmp/comment_implementation_worktrees/o_r`

Assigned languages:
`object_data_instance_notation`, `ooc`, `opa`, `openedge_abl`,
`openrc_runscript`, `openstep_property_list`, `opentype_feature_file`, `org`,
`ox`, `oz`, `p4`, `pan`, `papyrus`, `parrot_assembly`,
`parrot_internal_representation`, `pawn`, `peg_js`, `pep8`, `pic`,
`picolisp`, `piglatin`, `pod`, `pod_6`, `pogoscript`, `pony`,
`pov_ray_sdl`, `prisma`, `propeller_spin`, `qt_script`, `raml`, `rascal`,
`realbasic`, `reason`, `redcode`, `redirect_rules`, `renderscript`, `renpy`,
`rescript`, `rpc`, `rpm_spec`.

## Commands run

- `uv run python scripts/build_comment_language_fixtures.py`
- `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov`

Final verification result:

- `826 passed, 1 failed`
- Remaining failure:
  `tests/test_comment_language_fixtures.py::test_comment_language_fixture_files_parse_expected_comments[org]`

## Fixture edits

Added parseable adversarial cases to the assigned fixture files:

- `tests/fixtures/comment_languages/object_data_instance_notation.code`
- `tests/fixtures/comment_languages/ooc.code`
- `tests/fixtures/comment_languages/opa.code`
- `tests/fixtures/comment_languages/openedge_abl.code`
- `tests/fixtures/comment_languages/openrc_runscript.code`
- `tests/fixtures/comment_languages/openstep_property_list.code`
- `tests/fixtures/comment_languages/opentype_feature_file.code`
- `tests/fixtures/comment_languages/org.code`
- `tests/fixtures/comment_languages/ox.code`
- `tests/fixtures/comment_languages/oz.code`
- `tests/fixtures/comment_languages/p4.code`
- `tests/fixtures/comment_languages/pan.code`
- `tests/fixtures/comment_languages/papyrus.code`
- `tests/fixtures/comment_languages/parrot_assembly.code`
- `tests/fixtures/comment_languages/parrot_internal_representation.code`
- `tests/fixtures/comment_languages/pawn.code`
- `tests/fixtures/comment_languages/peg_js.code`
- `tests/fixtures/comment_languages/pep8.code`
- `tests/fixtures/comment_languages/pic.code`
- `tests/fixtures/comment_languages/picolisp.code`
- `tests/fixtures/comment_languages/piglatin.code`
- `tests/fixtures/comment_languages/pod.code`
- `tests/fixtures/comment_languages/pod_6.code`
- `tests/fixtures/comment_languages/pogoscript.code`
- `tests/fixtures/comment_languages/pony.code`
- `tests/fixtures/comment_languages/pov_ray_sdl.code`
- `tests/fixtures/comment_languages/prisma.code`
- `tests/fixtures/comment_languages/propeller_spin.code`
- `tests/fixtures/comment_languages/qt_script.code`
- `tests/fixtures/comment_languages/raml.code`
- `tests/fixtures/comment_languages/rascal.code`
- `tests/fixtures/comment_languages/realbasic.code`
- `tests/fixtures/comment_languages/reason.code`
- `tests/fixtures/comment_languages/redcode.code`
- `tests/fixtures/comment_languages/redirect_rules.code`
- `tests/fixtures/comment_languages/renderscript.code`
- `tests/fixtures/comment_languages/renpy.code`
- `tests/fixtures/comment_languages/rescript.code`
- `tests/fixtures/comment_languages/rpc.code`
- `tests/fixtures/comment_languages/rpm_spec.code`

The additions cover:

- meaningful `# Heading` and `--flag` payload preservation inside line comments
- nested block comments containing line-comment markers for languages whose
  registry entries mark slash-star blocks as nested
- non-nested C-style block comments containing line-comment-looking text
- documentation-style slash-star blocks with `*` gutters and semantic `#` /
  `--` payload lines
- Org comment lines and lower-case `#+begin_comment` / `#+end_comment`
- POD and Pod 6 paragraph comments with required blank separators
- Spin single-quote, double-quote, brace, and double-brace comment forms

For `pod.code` and `pod_6.code`, I also inserted blank non-comment separators
after the seeded `=for comment fixture_2` / `=comment fixture_2` lines. Without
the blank line, the POD paragraph regex consumes the following generator
separator line and the seeded expected match is not returned exactly.

## Sanitizer observations

Entry points used:

- extraction: `CommentQuery(language).parse(source)`
- sanitation: `sanitize_comment(language, QueryMatch)`

Representative paired removal and preservation cases:

- ODIN line comment:
  - raw: `-- breaker odin --flag stays content`
  - sanitized: `breaker odin --flag stays content`
  - removal: leading `--` delimiter
  - preservation: body `--flag`

- P4 documentation block:
  - raw:
    ```text
    /**
     * breaker p4 doc line
     * # Heading preserved
     * --flag preserved
     */
    ```
  - sanitized:
    ```text
    breaker p4 doc line
    # Heading preserved
    --flag preserved
    ```
  - removal: slash-star wrapper and decorative `*` gutters
  - preservation: Markdown-style `# Heading` and CLI-style `--flag`

- ooc nested block:
  - raw:
    ```text
    /* breaker ooc outer // marker
       /* breaker ooc inner */
       breaker ooc tail */
    ```
  - sanitized:
    ```text
    breaker ooc outer // marker
      /* breaker ooc inner */
      breaker ooc tail
    ```
  - removal: outer slash-star wrapper
  - preservation: inner delimiter-looking text and `//` marker as body content

- Org line comment:
  - raw: `# # breaker org heading survives`
  - sanitized: `# breaker org heading survives`
  - removal: leading Org `#` delimiter
  - preservation: body Markdown-style `#`

- POD block:
  - raw:
    ```text
    =begin comment
    breaker pod body keeps # Heading
    --flag remains content
    =end comment
    ```
  - sanitized:
    ```text
    breaker pod body keeps # Heading
    --flag remains content
    ```
  - removal: POD comment directives
  - preservation: `# Heading` and `--flag`

- Propeller Spin double-quote line comment:
  - raw: `'' breaker spin doc # Heading and --flag stay`
  - sanitized: `breaker spin doc # Heading and --flag stay`
  - removal: doubled Spin line-comment delimiter
  - preservation: body `# Heading` and `--flag`

- RPC/XDR block:
  - raw:
    ```text
    /*
     * breaker rpc doc line
     * # Heading preserved
     * --flag preserved
     */
    ```
  - sanitized:
    ```text
    breaker rpc doc line
    # Heading preserved
    --flag preserved
    ```
  - removal: slash-star wrapper and decorative `*` gutters
  - preservation: body `# Heading` and `--flag`

Outcome: sanitizer behavior for the added passing fixture cases is
`reviewed-no-issue`.

## Confirmed findings

### 1. Org generated repeated-opener case does not parse

Outcome: `needs-policy-decision`

Probe:

```python
CommentQuery("org").parse("######## repeated_open_1\n")
```

Actual:

```python
[]
```

The fixture builder expects `######## repeated_open_1` for Org because it
generates repeated symbol opener cases for `#` comments. The current Org line
regex is more restrictive:

```text
(?m)^[ \t]*#(?:[ \t][^\r\n]*|[ \t]*$)
```

That regex intentionally accepts `# note` and blank hash lines, but not
`######## repeated_open_1`. This leaves the canonical fixture test failing even
after the breaker additions:

```text
FAILED tests/test_comment_language_fixtures.py::test_comment_language_fixture_files_parse_expected_comments[org]
```

Fixer options:

- update fixture generation so Org does not receive repeated `#` opener cases,
  if repeated hash leaders are not valid Org comments under the current scope
- or update the Org registry/parser policy if repeated `#` leaders should be
  accepted as comments

The failing generated case was not added by this breaker pass.

### 2. OpenEdge ABL `CommentQuery` extracts adjacent `//not`

Outcome: `needs-policy-decision`

Probe:

```python
CommentQuery("openedge_abl").parse("value//not\nvalue // yes\n")
```

Actual raw matches:

```python
["//not", "// yes"]
```

The existing regular test
`tests/test_parse_comment.py::test_openedge_abl_aliases` asserts that
`value//not` should not be returned by the legacy extraction path. The lower
level `CommentQuery` currently extracts it. This may be an API divergence or a
registry-policy gap around whether OpenEdge `//` must be start-of-line or
whitespace-delimited.

No failing fixture was added for this probe.

### 3. POD and Pod 6 fixture generator needs paragraph-aware separators

Outcome: `fixed-in-fixture`, generator follow-up recommended

Probe on generated fixture shape:

```text
=for comment fixture_2
value_2 = 2
```

Actual raw match before fixture adjustment:

```text
=for comment fixture_2
value_2 = 2
...
```

POD `=for comment` and Pod 6 `=comment` comments consume a full nonblank
paragraph. The fixture builder currently inserts a nonblank code separator
immediately after these one-line seeded comments. In this worktree I fixed the
assigned fixture files by adding a blank line after the seeded one-liners, but
`scripts/build_comment_language_fixtures.py --force` would recreate the failing
shape unless the generator learns to insert blank separators after paragraph
comment forms.

## Reviewed probes with no code change requested

- `redirect_rules` and `rpm_spec` line-anchored hash comments:
  - probe: inline `#` after a route/spec line plus a standalone `#` comment
  - actual: only the standalone line comment parsed
  - outcome: `no-change-needed`

- Org keywords:
  - probe: `#+TITLE: not a comment` followed by `# visible comment`
  - actual: only `# visible comment` parsed
  - outcome: `no-change-needed`

- PicoLisp block opener precedence:
  - probe: `#{ outer #{ inner }# tail }#` followed by `# line`
  - actual: nested block and line comment parsed separately
  - outcome: `no-change-needed`

- Propeller Spin2 continuation comments:
  - probe: `... continuation comment?` followed by a normal `'` line comment
  - actual: only the normal quote comment parsed
  - outcome: `documented-limitation`
  - note: registry notes explicitly exclude Spin2 `...` continuation comments
    as version-specific

- Non-nested slash-star block behavior:
  - languages probed: `openstep_property_list`, `p4`, `pawn`, `peg_js`,
    `piglatin`, `pogoscript`, `prisma`, `qt_script`, `rascal`, `reason`,
    `renderscript`, `rescript`, `rpc`
  - probe: `/* outer /* inner */ outer */`
  - actual: each parsed only `/* outer /* inner */`
  - outcome: `no-change-needed`
  - note: this matches the registry/matrix scope for non-nested block comments

## Per-language coverage summary

- `object_data_instance_notation`: added double-hyphen line comments with
  semantic `# Heading` and `--flag` body text.
- `ooc`, `opa`, `openedge_abl`, `ox`, `pony`, `pov_ray_sdl`: added nested
  slash-star comments containing line-comment markers plus line comments with
  semantic punctuation.
- `oz`: added percent line comment with semantic punctuation plus nested
  slash-star comment containing a percent marker.
- `picolisp`: added hash line comment and nested `#{ }#` block that confirms
  block opener precedence over the hash line opener.
- `openstep_property_list`, `pawn`, `peg_js`, `pogoscript`, `qt_script`,
  `rascal`, `reason`, `renderscript`, `rescript`: added slash line comments
  and non-nested slash-star blocks containing delimiter-looking body text.
- `p4`, `prisma`, `rpc`: added documentation-style slash-star blocks with
  removable `*` gutters and preserved semantic `#` / `--` payload lines.
- `piglatin`: added SQL-style double-hyphen line comment and non-nested
  slash-star block containing delimiter-looking body text.
- `openrc_runscript`, `opentype_feature_file`, `pan`, `pic`, `raml`, `renpy`:
  added hash line comments with semantic `# Heading` and `--flag` body text.
- `redirect_rules`, `rpm_spec`: added line-anchored hash comments with semantic
  body punctuation, and separately probed that inline hash text is ignored.
- `papyrus`: added semicolon line comment and `;/ /;` block containing body
  lines that look like hash and semicolon comments.
- `parrot_assembly`, `parrot_internal_representation`: added hash line
  comments and POD regions with semantic body punctuation.
- `pep8`, `redcode`: added semicolon line comments with semantic `# Heading`
  and `--flag` body text.
- `pod`, `pod_6`: added paragraph-aware `=for comment` / `=comment` and
  `=begin comment` / `=end comment` cases with blank separation.
- `propeller_spin`: added single-quote line, double-quote line, brace block,
  and double-brace block comments with semantic punctuation.
- `realbasic`: added both apostrophe and slash line-comment forms.
