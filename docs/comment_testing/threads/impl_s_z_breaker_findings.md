# Adversarial Findings: impl_s_z

## Scope

- Assigned languages: `sage`, `saltstack`, `sed`, `shaderlab`, `singularity`,
  `slice`, `smali`, `smpl`, `smt`, `solidity`, `soong`, `sourcepawn`, `sqf`,
  `sqlpl`, `squirrel`, `ssh_config`, `stan`, `standard_ml`, `star`,
  `stringtemplate`, `stylus`, `sugarss`, `supercollider`, `swig`, `terra`,
  `texinfo`, `type_language`, `unity3d_asset`, `uno`, `urweb`, `vcl`, `volt`,
  `webvtt`, `whiley`, `win32_message_file`, `witcher_script`, `wollok`,
  `world_of_warcraft_addon_data`, `wren`, `xojo`, `xpages`, `yacc`, `yang`,
  `zenscript`, `zephir`
- Status: fixture edits complete; full required fixture verification is blocked
  by a generated `world_of_warcraft_addon_data` seed/registry mismatch described
  below.
- Extraction entry point: `CommentQuery(<language>).parse(...)`
- Sanitizer entry point: `CommentSanitizer(<language>).sanitize(...)`

## Fixture Edits

All assigned fixture files under `tests/fixtures/comment_languages/` were
created by `uv run python scripts/build_comment_language_fixtures.py` when
missing, then appended with parser-accepted breaker cases. Seeded cases were
left intact.

| Languages | Fixture coverage added | Status |
| --- | --- | --- |
| `sage`, `singularity`, `smali`, `ssh_config`, `star`, `unity3d_asset` | Inline hash comments, `#` heading preservation, string false-positive guard. | reviewed-no-issue |
| `shaderlab`, `slice`, `smpl`, `solidity`, `soong`, `sourcepawn`, `sqf`, `squirrel`, `stan`, `stylus`, `sugarss`, `supercollider`, `swig`, `type_language`, `uno`, `whiley`, `witcher_script`, `wollok`, `yang`, `zephir` | `//` line comments, `#` heading preservation inside `//`, star-gutter block comments, bullet/flag preservation, string false-positive guard. | reviewed-no-issue |
| `saltstack` | YAML `#` comments plus Jinja `{# ... #}` wrapper removal and heading preservation. | reviewed-no-issue |
| `sed` | Indented line comments, `#` heading preservation, inline `#` non-comment probe. | reviewed-no-issue |
| `smt` | Semicolon line comments and literal semicolon preservation. | reviewed-no-issue |
| `sqlpl` | `--` comments, `--flag` preservation, nested `/* ... */` with inner line marker. | reviewed-no-issue |
| `standard_ml`, `urweb` | Nested `(* ... *)` comments and star-gutter/bullet preservation. | reviewed-no-issue |
| `stringtemplate` | `<! ... !>` wrapper removal and heading preservation, separated by non-comment lines to avoid accidental grouping. | reviewed-no-issue |
| `terra` | `--` comments, `--flag` preservation, level-1 long comment sanitation. Level-2 long-comment sanitation is findings-only. | confirmed-bug |
| `texinfo` | `@c`, `@comment`, and `@ignore` removal with `#`, `--flag`, and `@code{...}` preservation. | reviewed-no-issue |
| `vcl`, `zenscript` | `//`, `#`, and `/* ... */` mixed-token coverage. | reviewed-no-issue |
| `volt` | `{# ... #}` wrapper removal and heading preservation. | reviewed-no-issue |
| `webvtt` | Blank-line-delimited `NOTE` block with `#` heading and `--flag` preservation. Cue-text overmatch is findings-only. | confirmed-bug |
| `win32_message_file` | Line-start semicolon comments, literal semicolon preservation, inline semicolon non-comment probe. | reviewed-no-issue |
| `world_of_warcraft_addon_data` | Single-`#` comment, `##` metadata and inline `#` non-comment probes, heading preservation. Generated repeated-opener seed is blocked. | confirmed-bug |
| `wren` | `//`, nested `/* ... */`, inner line marker suppression, star-gutter/bullet preservation. | reviewed-no-issue |
| `xojo` | `//` and apostrophe comments plus heading/quote preservation. `Rem` remains unsupported per current docs. | reviewed-no-issue |
| `xpages` | XML comment wrapper removal and heading preservation. | reviewed-no-issue |
| `yacc` | Portable `/* ... */` star-gutter block with flag preservation. GNU/Bison `//` remains a policy question. | needs-policy-decision |

Representative sanitizer observations from the appended fixtures:

```text
Raw:       # # breaker_sage_keep_heading
Sanitized: # breaker_sage_keep_heading

Raw:       /*
            * breaker_shaderlab_remove star gutter
            * * breaker_shaderlab_keep_bullet
            * --flag breaker_shaderlab_keep_flag
           */
Sanitized: breaker_shaderlab_remove star gutter
           * breaker_shaderlab_keep_bullet
           --flag breaker_shaderlab_keep_flag

Raw:       -- --flag breaker_sqlpl_keep_flag
Sanitized: --flag breaker_sqlpl_keep_flag

Raw:       (*
            * breaker_standard_ml_remove star gutter
            * * breaker_standard_ml_keep_bullet
           *)
Sanitized: breaker_standard_ml_remove star gutter
           * breaker_standard_ml_keep_bullet

Raw:       @comment --flag breaker_texinfo_keep_flag
Sanitized: --flag breaker_texinfo_keep_flag

Raw:       NOTE breaker_webvtt_remove note block
           # breaker_webvtt_keep_heading
           --flag breaker_webvtt_keep_flag
Sanitized: breaker_webvtt_remove note block
           # breaker_webvtt_keep_heading
           --flag breaker_webvtt_keep_flag
```

## Confirmed Bugs

### terra

- Family: `terra_style`
- Status: confirmed-bug
- Fixture edit: findings-only for the failing level-2 long-comment sanitizer
  probe. The fixture keeps the parser-accepted level-1 `--[=[ ... ]=]` case,
  which sanitizes correctly.
- Source/provenance: Lua long brackets allow arbitrary equal-sign levels; the
  Lua manual defines matching long brackets by level and states that comments
  use long comments when `--` is followed by an opening long bracket:
  https://www.lua.org/manual/5.4/manual.html
- Input:
  ```text
  local x = 1
  --[==[
   * breaker_terra_level2_remove
   * --flag breaker_terra_level2_keep
  ]==]
  local y = 2
  ```
- Raw extracted match:
  ```text
  --[==[
   * breaker_terra_level2_remove
   * --flag breaker_terra_level2_keep
  ]==]
  ```
- Actual sanitized output:
  ```text
  --[==[
   * breaker_terra_level2_remove
   * --flag breaker_terra_level2_keep
  ]==]
  ```
- Expected sanitized output:
  ```text
  breaker_terra_level2_remove
  --flag breaker_terra_level2_keep
  ```
- Removal contract: remove the matching `--[==[` / `]==]` long-comment wrapper
  and decorative leading `*` gutters.
- Preservation contract: preserve the semantic `--flag` text.
- Why it matters: extraction supports arbitrary equal-depth long comments via
  the registry regex, but sanitizer wrapper inference only strips the seeded
  `--[[ ... ]]` and `--[=[ ... ]=]` forms.

### webvtt

- Family: `webvtt_style`
- Status: confirmed-bug
- Fixture edit: findings-only for cue-text overmatch. The fixture addition was
  kept as a blank-line-delimited `NOTE` block.
- Source/provenance: the WebVTT spec says comments are blocks preceded by a
  blank line, starting with `NOTE`, and ending at the first blank line:
  https://www.w3.org/TR/webvtt1/
- Input:
  ```text
  WEBVTT

  00:00:00.000 --> 00:00:01.000
  NOTE spoken cue text, not a comment

  ```
- Raw extracted match:
  ```text
  NOTE spoken cue text, not a comment
  ```
- Actual sanitized output:
  ```text
  spoken cue text, not a comment
  ```
- Expected behavior:
  ```text
  []
  ```
- Removal contract: strip `NOTE` only when it starts a WebVTT comment block.
- Preservation contract: preserve cue text that happens to begin with `NOTE`.
- Why it matters: the regex currently treats any line-start `NOTE` as a comment,
  including cue text after a timing line.

### world_of_warcraft_addon_data

- Family: `world_of_warcraft_addon_data_style`
- Status: confirmed-bug
- Fixture edit: appended parser-accepted single-`#` and metadata/inline
  negative probes; seeded generated `######## repeated_open_1` was left intact.
- Source/provenance: WoW TOC files distinguish single-`#` comments from
  double-`##` metadata tags:
  https://addonstudio.org/wiki/WoW%3ATOC_format
- Current generated fixture seed:
  ```text
  ######## repeated_open_1
  ```
- Actual behavior:
  ```text
  CommentQuery("world_of_warcraft_addon_data").parse(...) does not return
  ######## repeated_open_1
  ```
- Expected behavior:
  ```text
  The fixture generator should not create repeated-opener `########` as an
  expected comment for this language, because the registry pattern is
  (?m)^#(?!#)[^\r\n]*.
  ```
- Required verification failure:
  ```text
  uv run pytest tests/test_comment_language_fixtures.py -q --no-cov
  1 failed, 836 passed
  ```
- Follow-up surface: `scripts/build_comment_language_fixtures.py` should skip
  repeated-opener generation for line-comment examples whose opener has a
  negative lookahead or equivalent metadata exclusion, or the registry policy
  should explicitly decide how repeated single-`#` comments should work here.

## Policy / No-Change Probes

### sed

- Status: reviewed-no-issue
- Source/provenance: GNU sed documents that first-line `#n` forces `-n`
  behavior rather than being an ordinary comment:
  https://www.gnu.org/software/sed/manual/sed.html
- Probe:
  ```text
  #n breaker_sed_special_not_comment
  p
  ```
- Actual output: no matches.
- Outcome: current registry exclusion for first-line `#n` is correct.

### yacc

- Status: needs-policy-decision
- Source/provenance: GNU Bison is a yacc replacement with dialect extensions:
  https://www.gnu.org/software/bison/manual/bison.html
- Probe:
  ```text
  %token A
  // breaker_yacc_bison_line
  %%
  ```
- Actual output: no matches.
- Outcome: no parser bug under the current portable `yacc` policy, but add a
  separate `bison` registry key or alias if GNU/Bison `//` comments are in
  scope.

### xojo

- Status: reviewed-no-issue
- Source/provenance: current Xojo documentation lists `//` and apostrophe
  comments:
  https://documentation.xojo.com/api/language/commenting.html
- Probe:
  ```text
  Rem breaker_xojo_rem_candidate
  Dim x As Integer
  ```
- Actual output: no matches.
- Outcome: no change needed for the current docs-backed Xojo policy.

### world_of_warcraft_addon_data

- Status: reviewed-no-issue for metadata and inline non-comment handling
- Probe:
  ```text
  ## Interface: 100207
  Lib.lua # breaker_wow_inline_not_comment
  # breaker_wow_real_comment
  ```
- Actual output:
  ```text
  # breaker_wow_real_comment
  ```
- Sanitized output:
  ```text
  breaker_wow_real_comment
  ```
- Outcome: `##` metadata and inline file-path `#` text are preserved as
  non-comments; single-`#` line comments parse as expected.

## Verification

- `uv run python scripts/build_comment_language_fixtures.py`: completed with no
  terminal output.
- Custom parser/sanitizer sentinel check across all 45 assigned languages:
  `sanity-ok 45`.
- Required command:
  `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov`
  failed with the `world_of_warcraft_addon_data` generated repeated-opener
  mismatch above.
- Isolation check:
  `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov -k 'not world_of_warcraft_addon_data'`
  passed with `835 passed, 2 deselected`.
