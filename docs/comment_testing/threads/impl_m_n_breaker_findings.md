# Adversarial Findings: impl_m_n

## Scope

- Assigned languages: `m`, `maxscript`, `mcfunction`, `mercury`, `metal`,
  `mirah`, `mirc_script`, `mlir`, `modula_2`, `modula_3`,
  `module_management_system`, `monkey`, `monkey_c`, `moonscript`,
  `motorola_68k_assembly`, `mql4`, `mql5`, `mtml`, `mupad`, `nanorc`,
  `nasal`, `nasl`, `ncl`, `nearley`, `nemerle`, `nesc`, `netlinx`,
  `newlisp`, `nit`, `nwscript`.
- Fixture generator: `uv run python scripts/build_comment_language_fixtures.py`
  completed with no output.
- Fixture verification: `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov`
  passed after edits: `807 passed in 0.44s`.
- Extra parser sweep: all `breaker_` markers in assigned fixture files are
  contained in parsed `CommentQuery(language)` matches.

## Fixture Edits

All fixture edits are parser-accepted and confined to
`tests/fixtures/comment_languages/` files for the assigned languages.

| Language | Fixture file | Added coverage |
| --- | --- | --- |
| `m` | `m.code` | SOF semicolon header, inline semicolon, repeated semicolon run, hash-heading preservation line. |
| `maxscript` | `maxscript.code` | SOF `--`, inline `--`, block containing `--`, C-style doc gutter/bullet pair. |
| `mcfunction` | `mcfunction.code` | SOF `#`, indented line comment, hash ruler, hash-heading preservation line. |
| `mercury` | `mercury.code` | SOF `%`, inline `%`, block containing `%`, C-style doc gutter/bullet pair. |
| `metal` | `metal.code` | SOF `//`, inline preprocessor-line comment, block containing `//`, C-style doc gutter/bullet pair. |
| `mirah` | `mirah.code` | SOF `#`, indented class comment, `=begin` block with hash-heavy body and heading. |
| `mirc_script` | `mirc_script.code` | SOF `;`, standalone alias-body comment, block containing semicolon. |
| `mlir` | `mlir.code` | SOF `//`, inline `//`, line comment whose body contains `#`. |
| `modula_2` | `modula_2.code` | SOF nested block, nested block containing `//`, doc gutter/bullet pair. |
| `modula_3` | `modula_3.code` | SOF nested block, nested block containing `;`, doc gutter/bullet pair. |
| `module_management_system` | `module_management_system.code` | SOF `!`, inline `!`, repeated bang run, hash-heading preservation line. |
| `monkey` | `monkey.code` | SOF apostrophe, indented apostrophe line, `#Rem/#End` block with hash-heavy body and heading. |
| `monkey_c` | `monkey_c.code` | SOF `//`, inline `//`, block containing `//`, C-style doc gutter/bullet pair. |
| `moonscript` | `moonscript.code` | SOF `--`, inline `--`, equals long-bracket block, `--flag` preservation line. |
| `motorola_68k_assembly` | `motorola_68k_assembly.code` | SOF column-zero `*`, inline semicolon, column-zero star hash body, semicolon hash-heading preservation line. |
| `mql4` | `mql4.code` | SOF `//`, inline `//`, block containing `//`, C-style doc gutter/bullet pair. |
| `mql5` | `mql5.code` | SOF `//`, inline `//`, block containing `//`, C-style doc gutter/bullet pair. |
| `mtml` | `mtml.code` | SOF HTML comment, inline HTML comment, `<mt:Ignore>` containing hash and HTML-looking text. |
| `mupad` | `mupad.code` | SOF `//`, inline `//`, block containing `//`, C-style doc gutter/bullet pair. |
| `nanorc` | `nanorc.code` | SOF `#`, indented `#`, hash ruler, hash-heading preservation line. |
| `nasal` | `nasal.code` | SOF `#`, inline `#`, hash ruler, hash-heading preservation line. |
| `nasl` | `nasl.code` | SOF `#`, inline `#`, hash ruler, hash-heading preservation line. |
| `ncl` | `ncl.code` | SOF `;`, inline `;`, `/; ;/` block with semicolon body, hash-heading preservation line. |
| `nearley` | `nearley.code` | SOF `#`, inline `#`, hash ruler, hash-heading preservation line. |
| `nemerle` | `nemerle.code` | SOF `//`, inline `//`, block containing `//`, C-style doc gutter/bullet pair. |
| `nesc` | `nesc.code` | SOF `//`, inline `//`, block containing `//`, C-style doc gutter/bullet pair. |
| `netlinx` | `netlinx.code` | SOF `//`, inline `//`, `(* *)` block containing `//`, doc gutter/bullet pair. |
| `newlisp` | `newlisp.code` | SOF semicolon, inline semicolon, hash comment, semicolon hash-heading preservation line. |
| `nit` | `nit.code` | SOF `#`, inline `#`, hash ruler, hash-heading preservation line. |
| `nwscript` | `nwscript.code` | SOF `//`, inline `//`, block containing `//`, C-style doc gutter/bullet pair. |

## Confirmed Bugs

### sanitizer_generated_tests_collection

- Status: confirmed-bug
- Fixture edit: findings-only
- Fixture parse check: n/a
- Extraction entry point: n/a
- Sanitizer entry point: `tests/test_comment_sanitizer.py` generated case builder
- Input:
  ```text
  uv run pytest tests/test_comment_sanitizer.py -q --no-cov
  ```
- Actual behavior:
  ```text
  ERROR collecting tests/test_comment_sanitizer.py
  AssertionError: Unsupported example placeholder in '; entry point'
  ```
- Expected behavior: sanitizer tests should collect for every supported
  language, including newly registered languages whose examples do not contain
  the narrow placeholder strings used by the current sanitizer-test generator.
- Source/provenance: local verification after fixture edits.
- Why it matters: the generated sanitizer coverage cannot run at all once the
  `m` registry example is present, so fixer work on sanitizer behavior is
  blocked before assertions execute.

### line_comment_sanitizer_under_strips_assigned_languages

- Status: confirmed-bug
- Fixture edit: parser-accepted paired cases added to the assigned fixture files
  listed above.
- Fixture parse check: `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov`
  passed.
- Extraction entry point: `CommentQuery`
- Sanitizer entry point: `CommentSanitizer`
- Affected assigned languages with line comments:
  `m`, `maxscript`, `mcfunction`, `mercury`, `metal`, `mirah`,
  `mirc_script`, `mlir`, `module_management_system`, `monkey`, `monkey_c`,
  `moonscript`, `motorola_68k_assembly`, `mql4`, `mql5`, `mupad`,
  `nanorc`, `nasal`, `nasl`, `ncl`, `nearley`, `nemerle`, `nesc`,
  `netlinx`, `newlisp`, `nit`, `nwscript`.
- Representative input:
  ```text
  set a=1 ; breaker_m_inline_comment
  ```
- Raw extracted match:
  ```text
  ; breaker_m_inline_comment
  ```
- Sanitized output:
  ```text
  ; breaker_m_inline_comment
  ```
- Expected sanitized output:
  ```text
  breaker_m_inline_comment
  ```
- Additional representative raw/sanitized pairs:
  ```text
  // breaker_metal_sof_header -> // breaker_metal_sof_header
  # breaker_mcfunction_sof_header -> # breaker_mcfunction_sof_header
  -- breaker_moonscript_sof_header -> -- breaker_moonscript_sof_header
  ' breaker_monkey_sof_header -> ' breaker_monkey_sof_header
  * breaker_m68k_sof_header -> * breaker_m68k_sof_header
  ```
- Expected behavior: strip only the registered line-comment opener and one
  padding space, preserving the body.
- Removal contract: opener tokens such as `;`, `--`, `#`, `%`, `//`, `!`,
  apostrophe, and column-zero `*` are comment syntax noise.
- Preservation contract: body punctuation remains content. The fixture files
  include paired preservation samples such as `# Heading`, `--flag`, and
  `* bullet`-style bodies to ensure semantic punctuation survives after the
  opener is stripped.
- Paired preservation testcase:
  ```text
  ; # Heading breaker_m_preserve_hash_heading
  ```
  Expected sanitized body:
  ```text
  # Heading breaker_m_preserve_hash_heading
  ```
- Source/provenance: local synthesized parser-accepted cases derived from the
  registry syntax.
- Why it matters: extracted line comments are currently returned to downstream
  consumers with comment syntax still attached for this whole language chunk.
  The root appears to be that sanitizer wrapper inference depends on seeded
  example body placeholders or body-specific prefixes rather than delimiter
  metadata.

### block_sanitizer_under_strips_language_specific_wrappers

- Status: confirmed-bug
- Fixture edit: parser-accepted cases added to the affected fixture files.
- Fixture parse check: `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov`
  passed.
- Extraction entry point: `CommentQuery`
- Sanitizer entry point: `CommentSanitizer`
- Affected cases:

| Language | Raw extracted match | Sanitized output | Expected sanitized output |
| --- | --- | --- | --- |
| `mirc_script` | `/* breaker_mirc_block_with_semicolon ; still block */` | `/* breaker_mirc_block_with_semicolon ; still block */` | `breaker_mirc_block_with_semicolon ; still block` |
| `monkey` | `#Rem\n#### breaker_monkey_decorative_hashes\n# Heading breaker_monkey_preserve_heading\n#End` | unchanged | `#### breaker_monkey_decorative_hashes\n# Heading breaker_monkey_preserve_heading` |
| `moonscript` | `--[=[\nbreaker_moonscript_equals_long_bracket\n]=]` | unchanged | `breaker_moonscript_equals_long_bracket` |
| `mtml` | `<!-- breaker_mtml_inline_html_comment -->` | unchanged | `breaker_mtml_inline_html_comment` |
| `mtml` | `<mt:Ignore>\n# breaker_mtml_hash_inside_ignore\n<!-- breaker_mtml_html_inside_ignore -->\n</mt:Ignore>` | unchanged | `# breaker_mtml_hash_inside_ignore\n<!-- breaker_mtml_html_inside_ignore -->` |
| `ncl` | `/;\n; breaker_ncl_semicolon_inside_block\n;/` | unchanged | `; breaker_ncl_semicolon_inside_block` |

- Removal contract: remove only the outer block delimiters or language block
  wrappers (`/* */`, `#Rem/#End`, MoonScript long brackets, HTML comments,
  `<mt:Ignore>`, `/; ;/`).
- Preservation contract: punctuation inside the body remains meaningful unless
  a later rule can prove it is decorative gutter text. For example, the MTML
  body deliberately contains `#` and `<!-- ... -->` text that should remain as
  body content once the outer `<mt:Ignore>` wrapper is removed.
- Paired preservation testcase: each affected fixture keeps a body line with
  content-bearing punctuation, such as `# Heading`, `--flag`, semicolon text,
  or HTML-looking text inside another wrapper.
- Source/provenance: local synthesized parser-accepted cases derived from the
  registry syntax.
- Why it matters: these comments extract correctly, but downstream sanitized
  text still includes the entire comment wrapper for ordinary valid block
  shapes. MoonScript is especially notable because the parser regex already
  supports equals-delimited long brackets, but the sanitizer does not strip
  that captured delimiter variant.

## Reviewed No-Issue / Findings-Only Probes

### mcfunction_trailing_hash

- Status: reviewed-no-issue
- Fixture edit: findings-only
- Extraction entry point: `CommentQuery("mcfunction")`
- Input:
  ```text
  execute if entity @s run say not # trailing not comment
  ```
- Actual behavior: no match for the trailing `#`.
- Expected behavior: no match. The registry intentionally requires `#` as the
  first non-whitespace character.
- Source/provenance: registry notes and public mcfunction guidance that comments
  start a line with `#`: https://wiki.bedrock.dev/commands/mcfunctions

### nanorc_trailing_hash

- Status: reviewed-no-issue
- Fixture edit: findings-only
- Extraction entry point: `CommentQuery("nanorc")`
- Input:
  ```text
  set linenumbers # trailing not comment
  ```
- Actual behavior: no match for the trailing `#`.
- Expected behavior: no match under the current registry contract. Indented
  leading `#` comments were kept in the fixture; trailing command comments were
  not.
- Source/provenance: registry notes and nano `nanorc` manual context:
  https://www.nano-editor.org/dist/latest/nanorc.5.html

### motorola_68k_indented_star

- Status: reviewed-no-issue
- Fixture edit: findings-only
- Extraction entry point: `CommentQuery("motorola_68k_assembly")`
- Input:
  ```text
          * breaker_m68k_indented_star_probe
  ```
- Actual behavior: no match.
- Expected behavior: no match. The registry `*` form is column-sensitive via
  `(?m)^\*...`; semicolon inline comments and column-zero `*` comments were
  kept in the fixture.
- Source/provenance: registry-derived local probe.

### mql4_mql5_nested_block_probe

- Status: documented-limitation
- Fixture edit: findings-only
- Extraction entry point: `CommentQuery("mql4")`, `CommentQuery("mql5")`
- Input:
  ```text
  /* outer /* inner terminates? */ after */
  ```
- Actual behavior:
  ```text
  /* outer /* inner terminates? */
  ```
- Expected behavior: current non-nested extraction is consistent with official
  MQL4 and MQL5 documentation. Do not add this as a nested fixture.
- Source/provenance:
  - https://docs.mql4.com/basis/syntax/commentaries
  - https://www.mql5.com/en/docs/basis/syntax/commentaries

### modula_2_modula_3_nested_blocks

- Status: reviewed-no-issue
- Fixture edit: parser-accepted cases added to `modula_2.code` and
  `modula_3.code`
- Extraction entry point: `CommentQuery`
- Input:
  ```text
  (* breaker_modula2_outer (* breaker_modula2_inner // not line *) breaker_modula2_tail *)
  ```
- Actual behavior: one top-level nested block match that includes the inner
  delimiter and suppresses the `//` text as ordinary body content.
- Expected behavior: same.
- Source/provenance: registry-derived local probe.
