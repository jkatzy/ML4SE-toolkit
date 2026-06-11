# Adversarial Findings: impl_g_l

- Worktree: `/home/jovyan/work/tmp/comment_implementation_worktrees/g_l`
- Assigned languages: `gaml`, `gcc_machine_description`, `git_revision_list`, `harbour`, `holyc`, `jasmin`, `javascript_erb`, `jest_snapshot`, `jison`, `jolie`, `kaitai_struct`, `kakounescript`, `kicad_legacy_layout`, `kit`, `krl`, `kvlang`, `lark`, `lex`, `linker_script`, `linux_kernel_module`, `literate_agda`, `literate_coffeescript`, `literate_haskell`, `livescript`, `logos`, `logtalk`, `lookml`, `lsl`
- Fixture generation: `uv run python scripts/build_comment_language_fixtures.py`
- Fixture verification: `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov` -> `803 passed in 0.44s`
- Extraction entry point: `CommentQuery(language)`
- Sanitizer entry point: `CommentSanitizer(language).sanitize(match)`

## Fixture Edits

All assigned fixture files under `tests/fixtures/comment_languages/` were created by the required fixture generator because they were missing in this worktree. I then appended parser-accepted `gl_breaker_*` cases to every assigned fixture and made three fixture-only corrections needed for the generated seeded cases to pass:

- `javascript_erb.code`: moved the seeded `#!/usr/bin/env node fixture_2` hashbang to byte 0 because its registry regex is start-of-file anchored.
- `lex.code`: changed the generated inline duplicate block to `/* scanner rules for identifiers inline duplicate guard */`, preserving the seeded `/* scanner rules for identifiers */` once.
- `linker_script.code`: changed the generated inline duplicate block to `/* place text first inline duplicate guard */`, preserving the seeded `/* place text first */` once.

Changed fixture files:

`gaml.code`, `gcc_machine_description.code`, `git_revision_list.code`, `harbour.code`, `holyc.code`, `jasmin.code`, `javascript_erb.code`, `jest_snapshot.code`, `jison.code`, `jolie.code`, `kaitai_struct.code`, `kakounescript.code`, `kicad_legacy_layout.code`, `kit.code`, `krl.code`, `kvlang.code`, `lark.code`, `lex.code`, `linker_script.code`, `linux_kernel_module.code`, `literate_agda.code`, `literate_coffeescript.code`, `literate_haskell.code`, `livescript.code`, `logos.code`, `logtalk.code`, `lookml.code`, and `lsl.code`.

## Raw Extraction and Sanitizer Observations

These rows are from the appended fixture cases after the passing fixture run. The raw column is the extracted match containing `gl_breaker_*`; the sanitized column is the actual sanitizer output. Expected sanitizer behavior is to remove only the comment syntax scaffolding while preserving meaning-bearing punctuation such as `# Heading`, `--flag`, `C#`, `C++`, URLs, `%hook`, `%orig`, and operators.

| Language | Raw extracted match -> actual sanitized output | Status |
| --- | --- | --- |
| `gaml` | `/* gl_breaker_gaml_block contains // line marker and C# text */` -> `/* gl_breaker_gaml_block contains // line marker and C# text */`<br>`// gl_breaker_gaml_line keeps http://example.test/path and C++ token` -> same raw text | `confirmed-bug`: sanitizer under-strips both `/* */` and `//`. |
| `gcc_machine_description` | `; gl_breaker_gcc_line keeps --flag and ; literal semicolon` -> `gl_breaker_gcc_line keeps --flag and ; literal semicolon`<br>`/* constraint gl_breaker_gcc_block keeps // marker inside */` -> `gl_breaker_gcc_block keeps // marker inside` | `reviewed-no-issue`: delimiter removal works and preserves `--flag`, literal `;`, and inner `//`. |
| `git_revision_list` | `# gl_breaker_git_inline keeps #123 marker text` -> same raw text<br>`# gl_breaker_git_header keeps #### decorative ruler text` -> same raw text | `confirmed-bug`: sanitizer under-strips `#`. |
| `harbour` | `note gl_breaker_harbour_note lower-case NOTE form keeps --flag` -> same raw text<br>`* gl_breaker_harbour_star full-line keeps ** semantic stars` -> same raw text<br>`&& gl_breaker_harbour_amp keeps && literal marker` -> same raw text | `confirmed-bug`: sanitizer under-strips `NOTE`, `*`, and `&&` forms. |
| `holyc` | `/* gl_breaker_holyc_outer // inner line marker\n   /* gl_breaker_holyc_inner */\n   gl_breaker_holyc_tail */` -> `gl_breaker_holyc_outer // inner line marker\n  /* gl_breaker_holyc_inner */\n  gl_breaker_holyc_tail`<br>`// gl_breaker_holyc_line keeps /* literal text */` -> same raw text | `confirmed-bug`: nested block stripping works; `//` line stripping does not. |
| `jasmin` | `; gl_breaker_jasmin_line keeps --flag and ; literal semicolon` -> same raw text | `confirmed-bug`: sanitizer under-strips `;`. |
| `javascript_erb` | `<%# gl_breaker_javascript_erb_server keeps ERB-only marker %>` -> same raw text<br>`/* client-side gl_breaker_javascript_erb_block with // marker */` -> `gl_breaker_javascript_erb_block with // marker`<br>`// gl_breaker_javascript_erb_line keeps http://example.test/path` -> same raw text | `confirmed-bug`: sanitizer under-strips ERB and `//`; C-style block stripping works only for the registry example scaffold. |
| `jest_snapshot` | `// gl_breaker_jest_metadata keeps https://jestjs.io and // inside prose` -> same raw text | `confirmed-bug`: sanitizer under-strips generated `//` snapshot metadata. |
| `jison` | `/* operator gl_breaker_jison_block contains // lexical marker */` -> `gl_breaker_jison_block contains // lexical marker`<br>`// gl_breaker_jison_line keeps /regex/ and C++ token text` -> same raw text | `confirmed-bug`: block stripping works for the example scaffold; `//` line stripping does not. |
| `jolie` | `/* shared service gl_breaker_jolie_block contains // operation marker */` -> `gl_breaker_jolie_block contains // operation marker`<br>`// gl_breaker_jolie_line keeps http://service.local and C# token` -> same raw text | `confirmed-bug`: block stripping works for the example scaffold; `//` line stripping does not. |
| `kaitai_struct` | `# gl_breaker_kaitai_inline keeps # inside text` -> same raw text<br>`# gl_breaker_kaitai_heading keeps # Heading marker` -> same raw text | `confirmed-bug`: sanitizer under-strips YAML-style `#`. |
| `kakounescript` | `# gl_breaker_kakoune_command keeps %sh{ echo '# not opener' }` -> same raw text | `confirmed-bug`: sanitizer under-strips `#`; preservation target is the quoted `#` inside the command body. |
| `kicad_legacy_layout` | `# gl_breaker_kicad_header keeps #PWR and C++ text` -> same raw text | `confirmed-bug`: sanitizer under-strips `#`. |
| `kit` | `## gl_breaker_kit_doc keeps # Heading marker` -> same raw text<br>`# gl_breaker_kit_line keeps ## documentation marker` -> same raw text | `confirmed-bug`: sanitizer under-strips both `#` and `##`. |
| `krl` | `; gl_breaker_krl_line keeps ; literal command separator text` -> same raw text | `confirmed-bug`: sanitizer under-strips `;`. |
| `kvlang` | `    # gl_breaker_kvlang_indented keeps # Heading after opener` -> `# gl_breaker_kvlang_indented keeps # Heading after opener` | `confirmed-bug`: indentation is removed but the comment opener remains. |
| `lark` | `// gl_breaker_lark_slash_inline keeps # terminal marker` -> same raw text<br>`# gl_breaker_lark_hash_line keeps // literal marker` -> same raw text | `confirmed-bug`: sanitizer under-strips both `//` and `#`. |
| `lex` | `/* gl_breaker_lex_block contains // but remains one block */` -> same raw text | `confirmed-bug`: sanitizer under-strips generic `/* */` blocks. |
| `linker_script` | `/* gl_breaker_linker_block contains # but remains one block */` -> same raw text | `confirmed-bug`: sanitizer under-strips generic `/* */` blocks. |
| `linux_kernel_module` | `/* Module initialization gl_breaker_linux_block keeps // marker. */` -> `gl_breaker_linux_block keeps // marker`<br>`// gl_breaker_linux_line keeps C# and http://kernel.example/path` -> same raw text | `confirmed-bug`: block stripping works only for the example scaffold and drops the example-specific trailing period; `//` line stripping does not. |
| `literate_agda` | `-- gl_breaker_lagda_line keeps --flag and brace literal text` -> same raw text<br>`{- gl_breaker_lagda_outer {- gl_breaker_lagda_inner -} gl_breaker_lagda_tail -}` -> `gl_breaker_lagda_outer {- gl_breaker_lagda_inner -} gl_breaker_lagda_tail` | `confirmed-bug`: nested stripping works; `--` line stripping does not. |
| `literate_coffeescript` | `# gl_breaker_litcoffee_line keeps # Heading marker` -> same raw text<br>`###\ngl_breaker_litcoffee_block keeps # Heading and triple-hash text marker\n###` -> same raw text | `confirmed-bug`: sanitizer under-strips both `#` and `### ... ###`. |
| `literate_haskell` | `-- gl_breaker_lhs_line keeps --flag and brace literal text` -> same raw text<br>`{- gl_breaker_lhs_outer {- gl_breaker_lhs_inner -} gl_breaker_lhs_tail -}` -> `gl_breaker_lhs_outer {- gl_breaker_lhs_inner -} gl_breaker_lhs_tail` | `confirmed-bug`: nested stripping works; `--` line stripping does not. |
| `livescript` | `# gl_breaker_livescript_line keeps # Heading marker` -> same raw text<br>`/* this gl_breaker_livescript_block is preserved\n   in generated JavaScript */` -> `gl_breaker_livescript_block` | `confirmed-bug`: `#` line stripping fails; block sanitizer over-strips example-specific body suffix text. |
| `logos` | `/* hook gl_breaker_logos_block keeps %hook text for this tweak group */` -> `gl_breaker_logos_block keeps %hook text`<br>`// gl_breaker_logos_line keeps %orig and http://tweak.example/path` -> same raw text | `confirmed-bug`: block sanitizer over-strips example-specific suffix; `//` line stripping fails. |
| `logtalk` | `% gl_breaker_logtalk_line keeps :- operator text` -> same raw text<br>`/* example gl_breaker_logtalk_block keeps % nested marker used in tests */` -> `gl_breaker_logtalk_block keeps % nested marker` | `confirmed-bug`: `%` line stripping fails; block sanitizer over-strips example-specific suffix. |
| `lookml` | `# gl_breaker_lookml_inline keeps # in prose` -> same raw text<br>`# gl_breaker_lookml_header keeps ## markdown marker` -> same raw text | `confirmed-bug`: sanitizer under-strips `#`. |
| `lsl` | `/* listen handler gl_breaker_lsl_block keeps // event marker disabled during setup */` -> `gl_breaker_lsl_block keeps // event marker`<br>`// gl_breaker_lsl_line keeps http://lsl.example/path and C++ text` -> same raw text | `confirmed-bug`: block sanitizer over-strips example-specific suffix; `//` line stripping fails. |

Supplemental sanitizer test command:

```text
uv run pytest tests/test_comment_sanitizer.py -q --no-cov
```

Result: collection fails before test execution with `AssertionError: Unsupported example placeholder in '// movement speed'`. This is consistent with the sanitizer observations above: many new registry examples do not contain one of the sanitizer placeholder words, so `_build_sanitizer_syntax` cannot derive generic wrappers from them. This was not fixed here because the breaker role must not edit production code or regular tests.

## Unsupported and Disputed Probes

These probes were not left in fixtures because they are unsupported, disputed, or currently expose incorrect behavior.

| Language | Probe | Actual behavior | Expected/policy outcome |
| --- | --- | --- | --- |
| `gcc_machine_description` | `define_insn "x" // not gcc md comment` | No matches. | `reviewed-no-issue`; registry supports `;` and `/* */`, not `//`. |
| `harbour` | `value := 1 ; command separator, not comment` | No matches. | `reviewed-no-issue`; registry notes semicolon is a command separator. |
| `kvlang` | `Label:\n    text: 'x' # not a legal inline kv comment` | No matches. | `reviewed-no-issue`; current regex only accepts `#` as first non-space. |
| `kvlang` | `#:import os os\n# ordinary comment` | Only `# ordinary comment` was extracted. | `needs-policy-decision`; Kivy docs describe `#:` directives as comments used for declarative commands, but they behave like source directives and the registry intentionally excludes them. Source: https://kivy.org/doc/stable/api-kivy.lang.html |
| `lark` | `%ignore WS /* not lark block */` | No matches. | `reviewed-no-issue`; registry supports `//` and `#`, not block comments. |
| `lex` | `%%\n// not a flex comment` | No matches. | `reviewed-no-issue`; registry supports `/* */` only. |
| `linker_script` | `SECTIONS { # not ld comment\n }` | No matches. | `reviewed-no-issue`; registry supports `/* */` only. |
| `lookml` | `view: users { /* not lookml block */ }` | No matches. | `reviewed-no-issue`; registry supports `#` only. |
| `jest_snapshot` | `exports[\`x 1\`] = \`\n// rendered text, not metadata\n\`;` | Extracted `// rendered text, not metadata`. | `confirmed-bug`; Jest snapshot files store serialized content in template literals, so `//` inside the snapshot body should not be parsed as generated metadata. Source: https://jestjs.io/docs/snapshot-testing |
| `literate_haskell` | `This prose mentions -- not code.\n\n> main = putStrLn "ok"` | Extracted `-- not code.` from prose. | `confirmed-bug` or `needs-policy-decision`; literate Haskell recovers program text from marked code lines, so prose should not be scanned as Haskell code comments. Source: https://www.haskell.org/onlinereport/literate.html |
| `literate_agda` | Prose containing `-- not Agda code.` before an Agda Markdown code fence | Extracted `-- not Agda code.` from prose. | `confirmed-bug` or `needs-policy-decision`; literate Agda ignores text outside code blocks. Source: https://agda.readthedocs.io/en/latest/tools/literate-programming.html |
| `literate_coffeescript` | `This markdown heading # not CoffeeScript code\n\n    value = 1` | Extracted `# not CoffeeScript code` from prose. | `confirmed-bug` or `needs-policy-decision`; literate CoffeeScript treats indented Markdown code blocks as executable code and ignores the rest as prose. Source: https://github.com/jashkenas/coffeescript/blob/main/documentation/sections/literate.md |
| `literate_agda`, `literate_haskell` | Fixture draft line comment containing unclosed `{-` before a later nested block. | The later nested block was not extracted because `NestedCommentQuery` counted the opener inside the line comment. | `confirmed-bug`; nested delimiter scanning should ignore nested openers inside already-extracted line comments, or line-comment ranges should suppress nested scanning. The failing probe was removed from fixtures. |

## Detailed Findings

### Generated Fixture Problems

- Status: `confirmed-bug`
- Fixture edit: kept as fixture-only corrections in `javascript_erb.code`, `lex.code`, and `linker_script.code`
- Actual behavior before correction:
  - `javascript_erb.code` placed `#!/usr/bin/env node fixture_2` after `value_1 = 1`, but the registry pattern is `\A#![^\r\n]*`, so `CommentQuery("javascript_erb")` did not return the seeded hashbang.
  - `lex.code` and `linker_script.code` generated the exact same block comment as both the standalone seeded case and the inline block case. The fixture test requires each seeded expected match to appear exactly once.
- Expected behavior:
  - Start-anchored hashbang examples should be emitted at byte 0 in generated fixtures, or the generator should know how to suppress the leading separator.
  - Inline block generation should force a unique body even when the registry example lacks a placeholder such as `note`.
- Fixture parse check: `uv run pytest tests/test_comment_language_fixtures.py -q --no-cov` -> pass after fixture-only corrections.

### Sanitizer Wrapper Derivation

- Status: `confirmed-bug`
- Fixture edit: parser-accepted sanitizer samples kept in assigned fixtures
- Removal contract: strip only line/block delimiters and decorative syntax scaffolding.
- Preservation contract: keep `# Heading`, `#123`, `--flag`, `;` in prose, `C#`, `C++`, URLs, `%hook`, `%orig`, `:-`, regex slashes, and inner delimiter-like text that belongs to the comment body.
- Actual behavior:
  - Many line forms are returned unchanged, including `//`, `#`, `;`, `--`, `%`, `&&`, `NOTE`, and `*`.
  - Generic `/* ... */` examples for `gaml`, `lex`, and `linker_script` are returned unchanged.
  - Several C-style block comments sanitize only when the raw comment happens to match the registry example's prose scaffold. For example, `/* hook gl_breaker_logos_block keeps %hook text for this tweak group */` sanitizes to `gl_breaker_logos_block keeps %hook text`, dropping the content phrase `for this tweak group`.
- Expected behavior:
  - Sanitizer syntax should derive delimiters from registry syntax, not from incidental example prose around placeholder words.
  - The paired preservation strings in the fixture comments should remain after delimiter removal.

### Literate Source Scope

- Status: `confirmed-bug` or `needs-policy-decision`
- Fixture edit: findings-only; overmatching probes were not left in fixtures
- Source/provenance:
  - Haskell literate comments: https://www.haskell.org/onlinereport/literate.html
  - Agda literate programming: https://agda.readthedocs.io/en/latest/tools/literate-programming.html
  - Literate CoffeeScript: https://github.com/jashkenas/coffeescript/blob/main/documentation/sections/literate.md
- Actual behavior:
  - `CommentQuery("literate_haskell")` extracts `-- not code.` from prose.
  - `CommentQuery("literate_agda")` extracts `-- not Agda code.` from prose.
  - `CommentQuery("literate_coffeescript")` extracts `# not CoffeeScript code` from prose.
- Expected behavior:
  - For literate language keys, either parse comments only inside recognized code regions or document that the current registry key is a lexical approximation over the whole file. If the latter is intentional, the finding should become `documented-limitation`.

### Jest Snapshot Multiline Template Strings

- Status: `confirmed-bug`
- Fixture edit: findings-only; the failing snapshot body was not left in `jest_snapshot.code`
- Source/provenance: Jest docs show `.snap` artifacts as `exports[...] = \`...\`;` template-string snapshots: https://jestjs.io/docs/snapshot-testing
- Input:

```text
exports[`x 1`] = `
// rendered text, not metadata
`;
```

- Raw extracted match:

```text
// rendered text, not metadata
```

- Actual sanitized output:

```text
// rendered text, not metadata
```

- Expected behavior:
  - Do not parse `//` inside serialized snapshot template-string content as generated snapshot metadata.
  - For real generated metadata, remove the leading `//` while preserving meaningful URLs or literal `//` inside the body.

### kvlang Directives

- Status: `needs-policy-decision`
- Fixture edit: only ordinary first-non-space `#` comments were added to `kvlang.code`
- Source/provenance: Kivy docs describe `#:` directives as comments used to add declarative commands: https://kivy.org/doc/stable/api-kivy.lang.html
- Probe:

```text
#:import os os
# ordinary comment
```

- Actual behavior:

```text
# ordinary comment
```

- Expected behavior:
  - If `#:` directives are treated as executable/source directives, keep excluding them and document the policy.
  - If the parser contract is "all comments recognized by the host parser", add a separate directive/comment policy test before changing the registry.
