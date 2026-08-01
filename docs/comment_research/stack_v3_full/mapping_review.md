# Stack v3 Full Mapping Review

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: `2026-08-01`
- Inventory source and label column: pinned full statistics aggregated from
  `files[].language`
- Registry baseline: `63dc076463472374578d0746a732815c751121fa`
- Review status: `reviewed`

This record covers raw Stack v3 labels whose complete comment contract can be
mapped to an existing registry implementation. Linguist grouping alone was not
accepted as evidence.

## F*

- Proposed registry key: `f*`, aliasing `f_star`
- Classification: language label transport spelling
- Syntax contract: `//` through newline and nested `(* ... *)`
- Evidence: [pinned F* lexer](https://github.com/FStarLang/FStar/blob/42b45f6df687397cbb1b905c4066ff2435d5080f/src/ml/FStarC_Parser_LexFStar.ml#L573-L581)
- Adversarial boundaries: strings, nested depth, unclosed blocks, CRLF
- Decision: `alias`
- Required tests: raw-label lookup, line and nested extraction, unclosed input,
  sanitizer parity with `f_star`

## Genero 4gl

- Proposed registry key: `genero_4gl` (deferred; do not alias yet)
- Classification: renamed language label
- Syntax contract: `#` and `--` line comments plus nonnested `{ ... }`
- Evidence: [official BDL comments](https://4js.com/online_documentation/fjs-fgl-manual-html/fgl-topics/c_fgl_language_features_comment.html),
  [Linguist rename](https://github.com/github-linguist/linguist/commit/a45d988963768e54352ae40792cf5e5350a19f89), and a
  [pinned TextMate grammar](https://github.com/FourjsGenero/GeneroFgl.tmbundle/blob/dedc0c5df4235a3c63969eb15a24c7d10f67b686/Syntaxes/genero-4gl.tmLanguage#L91-L115).
  The highlighter is not the compiler lexer and does not establish malformed
  EOF, exact line endings, or all conditional/SQL modes.
- Adversarial boundaries: `--#` conditional directives, quoted markers, SQL
  blocks, unclosed braces
- Decision: `defer`; remove the current `genero_4gl` alias until a pinned lexer
  or reproducible `fglcomp` probe closes the gaps.
- Required tests after confirmation: exact raw-label lookup, all three forms,
  malformed EOF, line endings, SQL/conditional exclusions, and sanitizer
  preservation.

## Genero per

- Proposed registry key: `genero_per` (deferred; do not alias yet)
- Classification: renamed forms dialect label
- Syntax contract: `#` and `--` line comments plus nonnested `{ ... }`, with
  form-layout regions excluded from brace-comment matching
- Evidence: [Linguist rename](https://github.com/github-linguist/linguist/commit/a45d988963768e54352ae40792cf5e5350a19f89),
  [pinned PER grammar](https://github.com/FourjsGenero/GeneroFgl.tmbundle/blob/dedc0c5df4235a3c63969eb15a24c7d10f67b686/Syntaxes/genero-per.tmLanguage#L95-L119),
  [pinned PER contexts](https://github.com/FourjsGenero/GeneroFgl.tmbundle/blob/dedc0c5df4235a3c63969eb15a24c7d10f67b686/Syntaxes/genero-per.tmLanguage#L11-L90).
  These are highlighter rules, not the `fglform` lexer, and do not establish the
  complete layout/preprocessor grammar or malformed-input behavior.
- Adversarial boundaries: `SCREEN`, `GRID`, `TABLE`, and `TREE` layout bodies;
  `&define` bodies containing `#`; strings; genuine comments around layouts
- Decision: `defer`; remove the current `genero_per` alias until a pinned lexer
  or reproducible `fglform` probe establishes the full contract.
- Required tests after confirmation: raw-label lookup, layout/preprocessor
  exclusions, genuine comments, line endings, malformed input, and sanitizer
  body preservation.

## Go Workspace

- Proposed registry key: `go_workspace`, sharing `go_module`
- Classification: document-format dialect
- Syntax contract: `//` through newline; `/* ... */` is not accepted
- Evidence: [pinned work parser](https://github.com/golang/mod/blob/792ac169a90372d88fb14e712cb793061ba0c104/modfile/work.go#L31-L45),
  [pinned shared lexer](https://github.com/golang/mod/blob/792ac169a90372d88fb14e712cb793061ba0c104/modfile/read.go#L510-L552)
- Adversarial boundaries: block markers, quoted paths, URL-like text, CRLF
- Decision: `alias`
- Required tests: positive line comment and explicit block-comment negative

## Gradle Kotlin DSL

- Proposed registry key: `gradle_kotlin_dsl`, sharing a corrected Kotlin family
- Classification: embedded build-script dialect
- Syntax contract: `//` through newline and nested `/* ... */`; KDoc is a block
  comment subset
- Evidence: [Gradle Kotlin DSL 9.6.1](https://docs.gradle.org/9.6.1/userguide/kotlin_dsl.html),
  [pinned Kotlin lexer](https://github.com/Kotlin/kotlin-spec/blob/2f7aa0524ec27e788dfacd550f144809f2e0254c/grammar/src/main/antlr/KotlinLexer.g4#L15-L22)
- Adversarial boundaries: nested blocks, ordinary strings, triple-quoted strings,
  KDoc, unclosed blocks
- Decision: `separate-family`
- Required tests: move `kotlin` out of the nonnested C-style family, preserve its
  public key, add nested extraction and raw Gradle-label coverage

## Lean 4

- Proposed registry keys: `lean_4` and `lean4`, aliasing `lean`
- Classification: versioned language label
- Syntax contract: `--` through newline and nested `/- ... -/`
- Evidence: [pinned Lean parser](https://github.com/leanprover/lean4/blob/4b7a61dfa4ff3f29f07f0ae8ce428fbe39babd6f/src/Lean/Parser/Basic.lean#L536-L587)
- Adversarial boundaries: nested depth, doc comments, strings, unclosed blocks
- Decision: `alias`
- Required tests: raw-label lookup, line, nested, doc, unclosed, sanitizer parity

## Rocq Prover

- Proposed registry keys: `rocq_prover` and `rocq`, aliasing `coq`
- Classification: renamed language label
- Syntax contract: nested `(* ... *)`
- Evidence: [Linguist rename](https://github.com/github-linguist/linguist/commit/4b9ec2834bd069758bb2ec766997bb2070fe61d2),
  [pinned Rocq lexer](https://github.com/rocq-prover/rocq/blob/d3971a897c7e578afd920eac4c1fcbb666c67ead/parsing/cLexer.ml#L402-L436)
- Adversarial boundaries: strings, nested depth, unclosed blocks, stray closers
- Decision: `alias`
- Required tests: raw-label lookup, nested extraction, string exclusion,
  sanitizer parity with `coq`

## Visual Basic 6.0

- Proposed registry keys: `visual_basic_6_0` and `vb6`, sharing the Visual Basic
  family
- Classification: versioned dialect label
- Syntax contract: apostrophe through newline and case-insensitive `Rem` at a
  statement start; an inline `Rem` statement must follow `:`
- Evidence: [pinned Microsoft REM statement documentation](https://github.com/MicrosoftDocs/VBA-Docs/blob/b2cda886ea91e36c62eb1cb177133ad024ecd345/Language/Reference/User-Interface-Help/rem-statement.md#L15-L34)
- Adversarial boundaries: `Rem` identifiers, quoted apostrophes and `Rem`, inline
  text without `:`, case variants, CRLF
- Decision: `alias` with contextual extraction
- Required tests: raw-label lookup, apostrophe form, line-start and colon-start
  `Rem`, false-positive boundaries, sanitizer body preservation
