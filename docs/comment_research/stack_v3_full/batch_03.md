# Stack v3 Full Comment Research: batch_03

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics aggregated from
  `files[].language`
- Researcher or agent: `/root`
- Review status: `reviewed`

Classifier identities were checked against the pinned
[Linguist language inventory](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml).
Registry lookup was also checked at the working feature-branch state; pre-existing
work already resolves `Go Workspace` and `Gradle Kotlin DSL`, while the other
eight raw labels do not resolve. This record evaluates the syntax independently
of those uncommitted implementation changes.

## Glimmer TS

### Identity and scope

- Raw dataset label: `Glimmer TS` (27,764 files; 301,138,884 tokens)
- Proposed registry key: `glimmer_ts`
- Existing family or aliases checked: TypeScript/C-style, HTML, Handlebars, and
  Glimmer families; none alone represents the language-mode transitions.
- Classification: `template`
- Versions or releases checked: Ember 6.8 template-tag format;
  `ember-template-imports` 4.4.0 commit
  `d48a4841398410404d29e6fe467e125913e1bded`; `content-tag` commit
  `b0426e5dadc1348d57a80ad95229e42e9556207f`; Glimmer grammar commit
  `c67a73679db2945a686ca45d3e5318d86138e72a`; and TypeScript 5.9.3 commit
  `c63de15a992d37f0d6cec03ac7631872838602cb`.
- Intended support scope: `.gts` TypeScript source with Glimmer templates in
  syntactically recognized `<template>...</template>` expressions or class
  members.
- Explicitly excluded scope: standalone `.hbs`, legacy inline-template
  transforms, `.gjs`, and marker-looking text in TypeScript strings, regular
  expressions, or template literals.

### Syntax contract

- Line comments: in TypeScript mode, `//` through the first ECMAScript line
  terminator or EOF. There is no `//` comment in Glimmer template text.
- Block comments: TypeScript `/*...*/`, Glimmer short `{{!...}}`, Glimmer long
  `{{!--...--}}`, and HTML `<!--...-->`; each ends at its first matching closer.
- Nested comments: none of the four block forms nests.
- Termination at newline, delimiter, or EOF: TypeScript line comments accept
  EOF; block/template comments require a closer. CRLF is one line ending, and
  TypeScript also recognizes CR, LF, U+2028, and U+2029 line terminators.
- Inline use: yes, where the active TypeScript or Glimmer grammar admits that
  comment node.
- Adjacent-line grouping: only consecutive TypeScript `//` comments should be
  grouped; do not group across a `<template>` boundary or combine unlike forms.
- Unclosed delimiter behavior: the TypeScript/Glimmer parsers report incomplete
  syntax; do not return an ordinary complete block match.
- Lexical or structural context: parse TypeScript far enough to recognize real
  content tags, then scan their content as Glimmer. The official content-tag
  locator deliberately ignores `<template>` in strings and regular expressions.
- Conflicts: TypeScript strings, regexes, and template literals protect marker
  text; Glimmer text protects `//` and `/*`; `{{...}}` expressions and
  `<template>` transitions are structural, not comments. CSS/JavaScript comment
  rules from unrelated embedded formats must not leak into Glimmer text.
- Sanitizer line wrappers: `("//", "")` in TypeScript mode only.
- Sanitizer block wrappers: `("/*", "*/")`, `("{{!", "}}")`,
  `("{{!--", "--}}")`, and `("<!--", "-->")` in their active modes.
- Content-preservation expectations: preserve comment bodies, newlines, and the
  content-tag delimiters; never remove ordinary template text.

### Evidence

- Identity permalink:
  [Linguist `.gts` entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L2711-L2721)
- Official documentation:
  [Ember 6.8 template-tag format](https://guides.emberjs.com/v6.8.0/components/template-tag-format/)
  and the pinned
  [Glimmer TS definition](https://github.com/ember-cli/ember-template-imports/blob/d48a4841398410404d29e6fe467e125913e1bded/README.md#L141-L146)
- Official implementation/grammar:
  [TypeScript comment scanner](https://github.com/microsoft/TypeScript/blob/c63de15a992d37f0d6cec03ac7631872838602cb/src/compiler/scanner.ts#L2047-L2122),
  [content-tag AST locator](https://github.com/embroider-build/content-tag/blob/b0426e5dadc1348d57a80ad95229e42e9556207f/src/locate.rs), and the pinned
  [Glimmer comment scanner](https://github.com/ember-tooling/tree-sitter-glimmer/blob/c67a73679db2945a686ca45d3e5318d86138e72a/src/scanner.c).
- Secondary combined grammar:
  [tree-sitter-glimmer-typescript](https://github.com/NullVoxPopuli/tree-sitter-glimmer-typescript/blob/12d98944c1d5077b957cbdb90d663a7c4d50118c/grammar.js).
- Official tests:
  [content-tag parser boundaries](https://github.com/embroider-build/content-tag/blob/b0426e5dadc1348d57a80ad95229e42e9556207f/test/node/parse.test.js)
  and
  [Glimmer comment corpus](https://github.com/ember-tooling/tree-sitter-glimmer/blob/c67a73679db2945a686ca45d3e5318d86138e72a/test/corpus/comments.txt).
- Evidence conflicts or gaps: Ember documents the source format but delegates
  exact comment tokens to the TypeScript and Glimmer parsers. The independent
  combined grammar is corroboration only; the pinned official scanners and
  content-tag locator support the stated boundaries.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: pinned parser, external scanner, and official parser
  tests inspected; no local Ember toolchain was executed.
- Probe method: trace whether a content-tag range is produced before applying
  the Glimmer scanner.
- Probe input: `const s = '<template>{{! no }}</template>'; <template>{{! yes }}</template>`
- Observed result: the quoted tag is TypeScript string data; the second range is
  Glimmer and contains one comment.
- Conclusion and limits: mode boundaries are verified in source; exact
  TypeScript lexical behavior should reuse its established scanner.

### Representative examples

```gts
// TypeScript comment
const marker = "{{! string data }}";
<template>
  {{! Glimmer comment }}
  <!-- HTML comment -->
  <p>// template text</p>
</template>
```

### Adversarial boundaries

- Negative cases: all markers in TypeScript strings/regex/template literals;
  fake `<template>` text; `//` and `/*...*/` in Glimmer text; ordinary `{{name}}`.
- Malformed-input cases: each unclosed block form and a missing content-tag
  closer; an inner opener must not create nesting.
- Line-ending and Unicode cases: CRLF, lone CR/LF, U+2028/U+2029 for TypeScript
  line comments, and non-ASCII template comment bodies.
- Version or dialect counterexamples: `.gjs` is JavaScript rather than
  TypeScript; standalone `.hbs` has no outer TypeScript mode.
- Cleaner preservation cases: retain the `<template>` tags and all comment body
  text; preserve line count around multiline comments.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `glimmer_ts` with TypeScript scanning
  outside parser-confirmed content-tag ranges and Glimmer comment scanning inside.
- Deterministic tests to add: every comment form, false content tags, strings,
  regex/template literals, template text, unclosed forms, and all line endings.
- Remaining blocker: none for the scoped `.gts` format.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Go Workspace

### Identity and scope

- Raw dataset label: `Go Workspace` (22,259 files; 1,325,017 tokens)
- Proposed registry key: `go_workspace`
- Existing family or aliases checked: `go_module` / slash-line family; the
  working feature branch already carries this alias.
- Classification: `document-format`
- Versions or releases checked: Go workspace syntax from Go 1.18 through the
  current Go 1.26.5 source; `golang.org/x/mod` commit
  `792ac169a90372d88fb14e712cb793061ba0c104`.
- Intended support scope: files named `go.work` parsed by the Go workspace-file
  grammar.
- Explicitly excluded scope: Go source, `go.mod`, `go.sum`, vendor metadata, and
  arbitrary files containing Go-like directives.

### Syntax contract

- Line comments: `//` outside a quoted token through LF or EOF.
- Block comments: unsupported; the official lexer diagnoses `/*`.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF or EOF; a CR immediately before
  LF belongs to the physical line ending and is not comment content returned to
  callers.
- Inline use: yes, with or without preceding whitespace.
- Adjacent-line grouping: yes for consecutive `//` comment lines.
- Unclosed delimiter behavior: not applicable; a line comment at EOF is valid.
- Lexical or structural context: workspace files reuse the line-oriented
  `go.mod` lexical elements. Interpreted double-quoted and raw backtick strings
  are scanned before comment recognition.
- Conflicts: `//` inside either string form is data; `/*` is an explicit syntax
  error rather than a comment; parentheses group directive blocks.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve comment body and directives such
  as `go`, `toolchain`, `use`, and `replace` exactly.

### Evidence

- Identity permalink:
  [Linguist `go.work` entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L2819-L2829)
- Official specification:
  [Go work-file syntax and lexical elements](https://go.dev/ref/mod#go-work-file-syntax)
- Official implementation:
  [pinned work-file parser](https://github.com/golang/mod/blob/792ac169a90372d88fb14e712cb793061ba0c104/modfile/work.go#L31-L45)
  and
  [shared lexer](https://github.com/golang/mod/blob/792ac169a90372d88fb14e712cb793061ba0c104/modfile/read.go#L510-L617).
- Release cross-check:
  [Go 1.26.5 vendored lexer](https://github.com/golang/go/blob/c19862e5f8415b4f24b189d065ed739517c548ba/src/cmd/vendor/golang.org/x/mod/modfile/read.go#L510-L617)
- Evidence conflicts or gaps: none; documentation and both pinned lexer copies
  agree.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: source inspection of `readToken`; no Go binary probe
  was needed.
- Probe input: `use "./module//literal" // actual\n/* rejected */`
- Observed result: the quoted marker is data, the suffix is a comment, and the
  block opener enters the lexer's error path.
- Conclusion and limits: the result covers the shared lexer used by `go.work`.

### Representative examples

```go.mod
go 1.26.0
use (
    ./app // main workspace module
    "./path//kept"
)
```

### Adversarial boundaries

- Negative cases: quoted and raw-string `//`, rejected `/*...*/`, and a slash
  that is not followed by slash.
- Malformed-input cases: unterminated quoted strings and an unexpected block
  opener must remain parser errors, not recovered comments.
- Line-ending and Unicode cases: LF, CRLF, final line without LF, and Unicode in
  comment bodies and quoted paths.
- Version or dialect counterexamples: `go.mod` shares the lexer but is a
  different label; Go source additionally accepts block comments.
- Cleaner preservation cases: keep quoted paths and the next directive; retain
  body text from full-line and suffix comments.

### Decision

- Recommended action: `alias`
- Registry fields to change: keep/add `go_workspace` as an alias of the existing
  `go_module` slash-line-only family.
- Deterministic tests to add: raw-label lookup, quoted/raw paths, suffix and EOF
  comments, CRLF, and explicit block-comment rejection.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Godot Resource

### Identity and scope

- Raw dataset label: `Godot Resource` (3,507,061 files; 65,768,596,978 tokens)
- Proposed registry key: `godot_resource`
- Existing family or aliases checked: generic semicolon-line and INI families;
  an unguarded regular expression would match semicolons in Variant strings.
- Classification: `document-format`
- Versions or releases checked: Godot 4.6 documentation and 4.6.3-stable commit
  `35e80b3a8822a9df9be390814b62f44c0a9c69e8`; legacy Godot 3.5/3.6 text
  resource and `ConfigFile` documentation.
- Dialects checked: `.tscn`, `.tres`, `project.godot`, and legacy `.gdns` text
  resources and `.gdnlib` ConfigFile resources represented by the classifier.
- Intended support scope: textual Godot resource, scene, and ConfigFile syntax
  using Variant tokens.
- Explicitly excluded scope: binary `.scn`/`.res`, GDScript source, C# source,
  imported payloads, and non-Godot INI dialects.

### Syntax contract

- Line comments: `;` outside a Variant string through LF or EOF.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF or EOF; CRLF is one physical
  line ending.
- Inline use: yes. The 4.6 TSCN documentation includes comments after node
  declarations, and the tokenizer recognizes `;` whenever it is the next token.
- Adjacent-line grouping: yes for consecutive semicolon comment lines.
- Unclosed delimiter behavior: not applicable; EOF terminates a comment.
- Lexical or structural context: quoted Variant strings, escaped quotes, and
  `&"..."` StringNames protect semicolons. Tokenization occurs inside section
  headers, values, arrays, and dictionaries.
- Conflicts: `#` begins a Color token, not a comment; `#` is a GDScript comment
  only in separate `.gd` source. Semicolons inside resource paths or strings are
  data. Section brackets and constructor parentheses are structure.
- Sanitizer line wrappers: `(";", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve bodies and line structure even
  though Godot discards comments when resaving these formats.

### Evidence

- Identity permalink:
  [Linguist Godot Resource entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L2830-L2842)
- Official current documentation:
  [Godot 4.6 TSCN/TRES comments](https://docs.godotengine.org/en/4.6/engine_details/file_formats/tscn.html)
- Official legacy documentation:
  [Godot 3.5 TSCN/TRES format](https://docs.godotengine.org/en/3.5/development/file_formats/tscn.html),
  [Godot 3.6 ConfigFile comments](https://docs.godotengine.org/en/3.6/classes/class_configfile.html),
  and the
  [`.gdnlib` ConfigFile identity](https://docs.godotengine.org/en/3.5/classes/class_gdnativelibrary.html).
- Official implementation:
  [Godot 4.6.3 Variant tokenizer](https://github.com/godotengine/godot/blob/35e80b3a8822a9df9be390814b62f44c0a9c69e8/core/variant/variant_parser.cpp#L162-L415),
  especially the `';'`, `'#'`, and string token branches.
- Evidence conflicts or gaps: the ConfigFile prose describes comment *lines*,
  while the shared tokenizer accepts inline semicolons too; the implementation
  and current TSCN examples establish inline behavior. Legacy `.gdns` is a text
  resource rather than a separate comment dialect.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: pinned tokenizer source inspection; no engine build.
- Probe input: `path = "res://a;b.tres" ; note\ncolor = #ff00ff`
- Observed result: the quoted semicolon is string data, `; note` is discarded to
  LF, and `#ff00ff` becomes `TK_COLOR`.
- Conclusion and limits: this proves lexical boundaries shared by current text
  resources; versioned documentation supplies the legacy scope.

### Representative examples

```ini
[ext_resource type="Resource" path="res://a;b.tres" id="1"] ; dependency
color = #ff00ff
; full-line note
```

### Adversarial boundaries

- Negative cases: semicolons in quoted values and escaped strings, `#` colors,
  GDScript-looking `# text`, and section/array/dictionary punctuation.
- Malformed-input cases: unterminated strings stay errors; a comment at EOF is
  valid; no block marker is recognized.
- Line-ending and Unicode cases: LF, CRLF, EOF, Unicode comment bodies, and
  Unicode strings containing semicolons.
- Version or dialect counterexamples: Godot binary resources and arbitrary INI
  files are excluded; editor resaving removes comments but does not change the
  input grammar.
- Cleaner preservation cases: keep string semicolons, Color values, and all
  comment text; do not imitate the editor's destructive resave behavior.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `godot_resource` with a Variant
  string-aware semicolon scanner and `(";", "")` sanitizer metadata.
- Deterministic tests to add: inline/full/EOF comments, strings and escapes,
  StringNames, Colors, arrays/dictionaries, legacy examples, CRLF, and cleaner
  preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Gradle Kotlin DSL

### Identity and scope

- Raw dataset label: `Gradle Kotlin DSL` (4,208,271 files; 934,377,286 tokens)
- Proposed registry key: `gradle_kotlin_dsl`
- Existing family or aliases checked: Kotlin and non-nested C-style. The working
  feature branch already contains a corrected nested `kotlin_style` family.
- Classification: `dialect`
- Versions or releases checked: Gradle 9.6.1 and the Kotlin language grammar at
  commit `2f7aa0524ec27e788dfacd550f144809f2e0254c`.
- Intended support scope: `.gradle.kts` settings, initialization, and build
  scripts parsed as Kotlin DSL source.
- Explicitly excluded scope: Groovy `.gradle` scripts, generated accessors,
  Gradle properties, and shell/batch wrappers.

### Syntax contract

- Line comments: `//` through CR, LF, or EOF.
- Block comments: `/*...*/`; KDoc `/**...*/` is the same nested token family.
- Nested comments: yes, recursively, including ordinary block comments inside
  KDoc and vice versa.
- Termination at newline, delimiter, or EOF: line comments end before the line
  terminator; blocks end only when nesting depth returns to zero.
- Inline use: yes for line and block comments.
- Adjacent-line grouping: yes for consecutive `//` lines; block/KDoc forms
  remain individual matches.
- Unclosed delimiter behavior: an unterminated block is invalid Kotlin and must
  not be returned as an ordinary complete match.
- Lexical or structural context: ordinary strings, characters, and triple-quoted
  strings protect markers. Within `${...}`, Kotlin code resumes and comments are
  real comments.
- Conflicts: `/`, `/=`, and `*` operators; `//` in strings/URLs; markers in raw
  strings; and the initial `#!` shebang token are not comments.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/**", "*/")` before `("/*", "*/")` if wrapper
  identity is retained; both share nested extraction.
- Content-preservation expectations: preserve bodies and physical lines at all
  nesting depths; do not delete `${...}` source surrounding a comment.

### Evidence

- Identity permalink:
  [Linguist Gradle Kotlin DSL entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L2878-L2886)
- Official documentation:
  [Gradle 9.6.1 Kotlin DSL](https://docs.gradle.org/9.6.1/userguide/kotlin_dsl.html),
  which defines `.gradle.kts` scripts as Kotlin code.
- Official specification:
  [Kotlin lexical grammar](https://kotlinlang.org/spec/syntax-and-grammar.html#lexical-grammar)
- Official pinned grammar:
  [`DelimitedComment`, `LineComment`, and `ShebangLine`](https://github.com/Kotlin/kotlin-spec/blob/2f7aa0524ec27e788dfacd550f144809f2e0254c/grammar/src/main/antlr/KotlinLexer.g4#L11-L32)
- Evidence conflicts or gaps: none. The recursive lexer rule is explicit and
  differs from the existing generic non-nested C-style contract.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned ANTLR lexer inspected; no Gradle daemon run.
- Probe input: `/* outer /* inner */ outer */ val s = "// kept" // comment`
- Observed result: the recursive rule consumes the entire nested block, the
  string is protected, and the suffix is a line comment.
- Conclusion and limits: Gradle adds DSL APIs, not a different Kotlin lexer.

### Representative examples

```kotlin
plugins {
    /* outer /* nested */ still outer */
    kotlin("jvm") version "2.2.0" // plugin version
}
```

### Adversarial boundaries

- Negative cases: markers in ordinary/triple strings and chars, `/` and `/=`,
  URLs, and a shebang; positive comments inside `${...}` expressions.
- Malformed-input cases: unclosed outer/inner blocks and stray `*/`.
- Line-ending and Unicode cases: LF, CRLF, EOF line comment, U+2028 inside raw
  strings, and Unicode KDoc bodies.
- Version or dialect counterexamples: Groovy Gradle uses non-nested C-style
  comments; it must not share this nested family.
- Cleaner preservation cases: preserve KDoc stars, nested bodies, and the code
  immediately following the outer closer.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: keep/create canonical `kotlin` with nested
  `/*...*/` and alias `gradle_kotlin_dsl`; do not place either in the non-nested
  C-style family.
- Deterministic tests to add: nested/KDoc combinations, all string forms,
  interpolation, shebang, operators, unclosed blocks, CRLF, and raw-label lookup.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Hare

### Identity and scope

- Raw dataset label: `Hare` (4,947 files; 39,161,174 tokens)
- Proposed registry key: `hare`
- Existing family or aliases checked: slash-line-only family; its delimiter set
  matches Hare.
- Classification: `language`
- Versions or releases checked: Hare specification draft commit
  `e4e56ee128583835f3f4d0f3ddcb200756eccd11` and compiler release 0.26.0
  commit `015c7de19152c7ddb72780d19451e6dad078dccd`.
- Intended support scope: Hare `.ha` source accepted by the 0.26.0 lexer.
- Explicitly excluded scope: generated assembly, C headers, documentation prose,
  and shell scripts used by Hare projects.

### Syntax contract

- Line comments: `//` through U+000A or EOF. U+000D is an ordinary comment
  character, not a terminator.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF or EOF. In CRLF input, the CR is
  lexically part of the comment and only LF terminates it; a bare CR does not
  end the comment.
- Inline use: yes, with no whitespace requirement; the compiler tests
  `world// baz`.
- Adjacent-line grouping: yes for consecutive line comments.
- Unclosed delimiter behavior: not applicable; EOF is accepted, including an
  empty `//` in the implementation.
- Lexical or structural context: quoted strings, rune literals, and raw
  backtick strings are lexed as tokens before a comment can begin.
- Conflicts: `/` and `/=` operators, quoted URLs, and `#[...]` attributes are not
  comments. `/*...*/` is unsupported.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: retain bodies, Unicode, and any CR before
  LF; do not treat an attribute's `#` as scaffolding.

### Evidence

- Identity permalink:
  [Linguist Hare entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L3189-L3196)
- Official specification:
  [Hare language specification](https://harelang.org/specification.pdf), section
  6.2, defining `//` and excluding U+000A from comment characters.
- Pinned specification source:
  [lexical-analysis chapter](https://git.sr.ht/~sircmpwn/hare-specification/tree/e4e56ee128583835f3f4d0f3ddcb200756eccd11/item/language/analysis.tex)
- Official implementation:
  [Hare 0.26.0 lexer](https://git.sr.ht/~sircmpwn/hare/tree/015c7de19152c7ddb72780d19451e6dad078dccd/item/hare/lex/lex.ha)
  and its
  [lexer tests](https://git.sr.ht/~sircmpwn/hare/tree/015c7de19152c7ddb72780d19451e6dad078dccd/item/hare/lex/+test.ha).
- Evidence conflicts or gaps: the draft grammar's production visually requires
  a comment character, while the compiler accepts bare `//` at LF/EOF. The
  implementation behavior is adopted for empty comments.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: `lex2` and `lex_comment` source plus official lexer
  tests inspected; no compiler binary built.
- Probe input: `let s = "https://example"; // note\nlet n = 6 / 2; //`
- Observed result: quoted slash pairs and division are tokens; both suffix forms
  are comments, including the empty final form.
- Conclusion and limits: exact token behavior is verified for 0.26.0.

### Representative examples

```hare
let endpoint = "https://example.test"; // string is protected
let half = total / 2;
// explain the next operation
```

### Adversarial boundaries

- Negative cases: strings/runes/raw strings containing `//`, `/`, `/=`,
  `#[test]`, and `/*...*/`.
- Malformed-input cases: unterminated strings stay lexical errors; bare `//` and
  EOF comments are valid.
- Line-ending and Unicode cases: LF, CRLF, bare CR, EOF, empty comments, and
  Unicode body text; assert that CR is retained and does not terminate.
- Version or dialect counterexamples: none found in the checked specification
  and 0.26.0 implementation.
- Cleaner preservation cases: retain empty and nonempty bodies and never consume
  the following token or attribute.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `hare` to the LF-only slash-line family with
  `("//", "")` sanitizer metadata; its matcher must retain CR.
- Deterministic tests to add: inline, empty, EOF, CRLF and bare-CR continuation,
  strings/runes/raw strings, division, attributes, unsupported blocks, and
  Unicode.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## HIP

### Identity and scope

- Raw dataset label: `HIP` (128,584 files; 617,797,947 tokens)
- Proposed registry key: `hip`
- Existing family or aliases checked: C++ / non-nested C-style; HIP-Clang uses
  the same preprocessing-token lexer.
- Classification: `dialect`
- Versions or releases checked: ROCm HIP 7.2.3 commit
  `bc9af25177f96c0fea93198b89cf4c3cf08f3ea3` and current Clang lexer commit
  `36b6f48f88914b83acbadcb0c310d292c7304fc3`.
- Intended support scope: `.hip` single-source HIP C++ compiled by HIP-Clang.
- Explicitly excluded scope: generated host/device output, HIP build logs,
  CMake, Fortran HIP bindings, and embedded assembly's own comment syntax.

### Syntax contract

- Line comments: C++ `//` through the next logical newline or EOF. A
  backslash-newline splice continues the logical comment onto the next physical
  line.
- Block comments: `/*` through the first `*/`; documentation forms are subsets.
- Nested comments: no; Clang may warn about an inner opener, but it does not
  increase depth.
- Termination at newline, delimiter, or EOF: logical newline/EOF for line
  comments, first closer for blocks; CRLF and escaped newlines follow C++
  translation phases.
- Inline use: yes for both forms.
- Adjacent-line grouping: yes for consecutive logical `//` comments.
- Unclosed delimiter behavior: an unterminated block is a compiler diagnostic
  and is not an ordinary complete match; EOF line comments are valid.
- Lexical or structural context: normal/raw strings, character literals, and
  preprocessing tokens protect marker-like text. Comments are replaced with
  whitespace before later parsing.
- Conflicts: division, `/=`, multiplication, string/URL content, preprocessor
  directives, and device attributes such as `__global__` are not comments.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: preserve bodies and physical newlines,
  including continued line-comment text; do not remove adjacent kernel code.

### Evidence

- Identity permalink:
  [Linguist HIP entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L3002-L3011)
- Official HIP documentation:
  [What is HIP](https://rocm.docs.amd.com/projects/HIP/en/latest/what_is_hip.html)
  and the pinned
  [ROCm HIP 7.2.3 README](https://github.com/ROCm/HIP/blob/bc9af25177f96c0fea93198b89cf4c3cf08f3ea3/README.md),
  identifying HIP as C++ single-source kernel code.
- Official compiler documentation:
  [Clang HIP support](https://clang.llvm.org/docs/HIPSupport.html)
- Official implementation:
  [Clang `SkipLineComment` and `SkipBlockComment`](https://github.com/llvm/llvm-project/blob/36b6f48f88914b83acbadcb0c310d292c7304fc3/clang/lib/Lex/Lexer.cpp#L2684-L3165).
- Evidence conflicts or gaps: none for HIP-Clang. Platform/API differences do
  not change the C++ lexical comment contract.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned Clang lexer source inspected; no ROCm compiler
  was installed.
- Probe input: `auto u = R"(https://x/*kept*/)"; // continued \\\n+still comment\n__global__ void k() { /* note */ }`
- Observed result: raw-string markers are data, the escaped newline extends the
  line comment, and the block closes at the first `*/`.
- Conclusion and limits: confirmation is source-level and applies to HIP-Clang.

### Representative examples

```cpp
// launch configuration
hipLaunchKernelGGL(kernel, grid, block, 0, 0, data); /* device call */
const char *url = R"(https://example.test/a/*literal*/)";
```

### Adversarial boundaries

- Negative cases: raw/ordinary strings and chars, `/`, `/=`, preprocessor `#`,
  HIP attributes, and URLs.
- Malformed-input cases: nested-looking blocks close at the first closer;
  unterminated block errors; trailing backslash line continuation.
- Line-ending and Unicode cases: LF/CRLF, EOF line comment, spliced lines, and
  Unicode comment bodies.
- Version or dialect counterexamples: generated assembly or build-language files
  inside HIP projects retain their own syntax.
- Cleaner preservation cases: preserve comment text across a spliced physical
  line and leave raw strings and kernel launch syntax untouched.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `hip` to the C++/non-nested C-style family;
  retain the shared C++ lexical exclusions and logical-line behavior.
- Deterministic tests to add: raw and ordinary strings, both comment forms,
  first-close nesting, unclosed blocks, line splicing, HIP kernel syntax, and
  raw-label lookup.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Hosts File

### Identity and scope

- Raw dataset label: `Hosts File` (50,607 files; 539,817,641 tokens)
- Proposed registry key: `hosts_file`
- Existing family or aliases checked: hash-line family; the hosts grammar has no
  quoting or escaping exception to its `#` delimiter.
- Classification: `document-format`
- Versions or releases checked: current Linux man-pages commit
  `ae6b221882ce71ba82fcdbe02419a225111502f0` and glibc commit
  `04e750e75b73957cf1c791535a3f4319534a52fc`.
- Intended support scope: conventional `hosts`, `HOSTS`, and `hosts.txt` files
  containing IP-address-to-hostname mappings.
- Explicitly excluded scope: SSH `known_hosts`, dnsmasq configuration, zone
  files, adblock rule syntax, and shell scripts.

### Syntax contract

- Line comments: `#` from its first occurrence through LF or EOF.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF or EOF; the physical CRLF is not
  part of the returned comment slice.
- Inline use: yes, after an address/name mapping or at column zero.
- Adjacent-line grouping: yes for consecutive hash-comment lines.
- Unclosed delimiter behavior: not applicable; EOF is a valid terminator.
- Lexical or structural context: fields are separated by spaces/tabs; there are
  no quoted or escaped fields in the documented format. The implementation
  truncates the line at its first `#` before tokenizing fields.
- Conflicts: IPv6 uses colons, not `#`; valid hostnames do not require `#`;
  apparent shell quoting does not protect the marker in a hosts file.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve body, aliases, addresses, line
  endings, and the next mapping.

### Evidence

- Identity permalink:
  [Linguist Hosts File entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L3243-L3254)
- Official documentation:
  [`hosts(5)` format](https://man7.org/linux/man-pages/man5/hosts.5.html), stating
  that text from `#` to end of line is ignored.
- Pinned documentation source:
  [Linux man-pages `hosts.5`](https://github.com/mkerrisk/man-pages/blob/ae6b221882ce71ba82fcdbe02419a225111502f0/man5/hosts.5)
- Official implementation:
  [glibc hosts line parser](https://github.com/bminor/glibc/blob/04e750e75b73957cf1c791535a3f4319534a52fc/nss/nss_files/files-hosts.c#L48-L100)
  and its shared
  [first-`#` truncation](https://github.com/bminor/glibc/blob/04e750e75b73957cf1c791535a3f4319534a52fc/nss/nss_files/files-parse.c#L94-L109).
- Evidence conflicts or gaps: none for the conventional hosts format. The raw
  label does not license syntaxes from similarly named DNS or SSH files.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: glibc parser macro expansion inspected; no resolver
  configuration was changed.
- Probe input: `::1 localhost ip6-localhost # IPv6 aliases`
- Observed result: tokenization sees the address and aliases before the first
  `#`; the suffix is discarded.
- Conclusion and limits: this confirms glibc's conventional hosts-file parser.

### Representative examples

```text
127.0.0.1 localhost # loopback
::1 localhost ip6-localhost
# managed entries below
```

### Adversarial boundaries

- Negative cases: IPv4/IPv6 addresses, hyphenated and internationalized names,
  aliases, and similarly named non-hosts formats.
- Malformed-input cases: a line containing only `#`, EOF after `#`, and invalid
  mappings before a valid suffix comment.
- Line-ending and Unicode cases: LF, CRLF, EOF, tabs, Unicode body text, and
  ASCII/Punycode host fields.
- Version or dialect counterexamples: SSH/DNS/adblock formats may give `#`
  different context and are explicitly excluded.
- Cleaner preservation cases: keep every address and alias before `#`; retain
  comment body even when the native parser would discard it.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `hosts_file` to the existing hash-line family
  with `("#", "")` sanitizer metadata.
- Deterministic tests to add: full-line/inline/empty/EOF comments, IPv4/IPv6,
  aliases, tabs, CRLF, Unicode, and raw-label lookup.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## iCalendar

### Identity and scope

- Raw dataset label: `iCalendar` (991,625 files; 2,100,133,324 tokens)
- Proposed registry key: `icalendar` for unsupported-label accounting only.
- Existing family or aliases checked: INI/semicolon/hash and mail-style formats;
  none applies.
- Classification: `document-format`
- Versions or releases checked: RFC 5545 and libical 4.0.5 commit
  `325985fcc305bbff47f16f7a4eb62267c34f6107`.
- Intended support scope: `.ics` and `.ical` iCalendar content lines governed by
  RFC 5545.
- Explicitly excluded scope: vCalendar 1.0 extensions, MIME envelope comments,
  editor annotations outside the calendar object, and implementation source code.

### Syntax contract

- Line comments: unsupported.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: not applicable. Content lines end
  in CRLF and may be folded by CRLF followed by one space or tab.
- Inline use: unsupported.
- Adjacent-line grouping: unsupported.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: a content line is `name *(";" param) ":" value
  CRLF`. Semicolons introduce parameters; colon separates name/parameters from
  value; folding continues one logical property.
- Conflicts: `COMMENT` is a standard property carrying `TEXT`, not ignored
  source syntax. `#` in a URI/value, `//` in a URI, semicolon parameters, and
  RFC ABNF prose annotations are all data or specification notation.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: none.
- Content-preservation expectations: return no matches and preserve every byte,
  including `COMMENT` properties and folded lines.

### Evidence

- Identity permalink:
  [Linguist iCalendar entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L9268-L9280)
- Official specification:
  [RFC 5545 section 3.1, Content Lines](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.1)
  and
  [section 3.8.1.4, COMMENT](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.8.1.4).
- Official implementation:
  [libical content-line parser](https://github.com/libical/libical/blob/325985fcc305bbff47f16f7a4eb62267c34f6107/src/libical/icalparser.c#L134-L211),
  which treats semicolon and colon structurally and has no comment token.
- Evidence conflicts or gaps: none. Parenthesized comments appearing in RFC
  ABNF are grammar-description syntax, not characters accepted as calendar
  source comments.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: RFC ABNF and pinned libical parser inspected; no
  calendar file was rewritten.
- Probe input: `COMMENT:Bring #2; use https://example.test/a//b\r\n`
- Observed result: the entire value is `TEXT`; none of `#`, `;`, or `//` starts
  an ignored region.
- Conclusion and limits: no source-comment contract exists in RFC 5545.

### Representative examples

```icalendar
BEGIN:VEVENT
COMMENT:This whole property is calendar data
URL:https://example.test/a#fragment
END:VEVENT
```

### Adversarial boundaries

- Negative cases: `COMMENT:`, URI `#`/`//`, parameter semicolons, escaped text,
  and folded continuation lines must all produce zero matches.
- Malformed-input cases: bare `#`, missing colon, or bad folding may be invalid
  data but does not become a comment.
- Line-ending and Unicode cases: required CRLF, folded UTF-8 content, escaped
  newline text, and final malformed lines.
- Version or dialect counterexamples: MIME comments and producer-specific
  annotations are outside RFC 5545 calendar content.
- Cleaner preservation cases: byte-for-byte preservation; never remove a
  `COMMENT` property or URI fragment.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: record `icalendar` as a known unsupported label if
  the registry exposes that facility; add no extraction or sanitizer wrappers.
- Deterministic tests to add: raw-label unsupported lookup plus zero-match tests
  for `COMMENT`, URI markers, parameters, folding, CRLF, and malformed markers.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Imba

### Identity and scope

- Raw dataset label: `Imba` (7,639 files; 12,638,293 tokens)
- Proposed registry key: `imba`
- Existing family or aliases checked: generic hash-line, slash-line, and
  C-style families; each overmatches a different valid Imba lexical context.
- Classification: `language`
- Versions or releases checked: current Imba 2 compiler repository commit
  `9eaa35332461a3dde4342e67cd1f1e40fb16400e` (package
  `2.0.0-alpha.252`) and Imba 1.5.2 commit
  `ee743778e205e8b50aa6a6cd1238ee904c33854d`.
- Intended support scope: the version-common Imba source comment forms accepted
  by both checked compiler generations.
- Explicitly excluded scope: generated JavaScript/CSS and Imba-2-only
  JavaScript-style `//` and `/*...*/` until a file-version discriminator exists.

### Syntax contract

- Line comments: a `#` token followed by space/tab or `!`, or a bare `#` before
  newline/EOF, through the physical line. `#word` and `##word` are not comments.
- Block comments: `###` through the first later `###`; the opener must be
  followed by a non-`#` body character in both checked lexers.
- Nested comments: no.
- Termination at newline, delimiter, or EOF: line forms end at LF/EOF. A
  nonempty `###` block may consume through EOF without a closer under the pinned
  lexer rule.
- Inline use: yes for recognized hash-line forms and triple-hash blocks.
- Adjacent-line grouping: yes for consecutive hash-line comments; keep triple
  blocks separate.
- Unclosed delimiter behavior: a nonempty unclosed triple-hash block is an
  accepted lexer match through EOF. A bare `###` opener has no verified comment
  match and must remain untouched.
- Lexical or structural context: the Imba lexer must distinguish strings,
  heredocs, regexes, symbol identifiers, tag syntax, and CSS/style regions
  before classifying `#`.
- Conflicts: `#name`/`##name` symbols and tag/style selectors are data. Imba 2's
  lexer additionally accepts `//` except `///`, and `/*...*/`; Imba 1.5.2 does
  not expose those rules, so their union is unsafe for an unversioned label.
- Sanitizer line wrappers: `("#", "")`, retaining any semantic leading `!` as
  content rather than treating it as part of the wrapper.
- Sanitizer block wrappers: `("###", "###")`; an accepted EOF block has only an
  opening wrapper.
- Content-preservation expectations: preserve bodies and indentation; never
  strip symbol/selectors or marker text in protected literals.

### Evidence

- Identity permalink:
  [Linguist Imba entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L3434-L3441)
- Official documentation:
  [Imba basic syntax comments](https://github.com/imba/imba/blob/9eaa35332461a3dde4342e67cd1f1e40fb16400e/apps/imba.io/content/docs/basic-syntax.md#L650-L668)
- Official current implementation:
  [Imba 2 comment token rules](https://github.com/imba/imba/blob/9eaa35332461a3dde4342e67cd1f1e40fb16400e/packages/imba/src/compiler/lexer.mjs#L204-L240)
  and
  [`commentToken`](https://github.com/imba/imba/blob/9eaa35332461a3dde4342e67cd1f1e40fb16400e/packages/imba/src/compiler/lexer.mjs#L1685-L1760).
- Version comparison:
  [Imba 1.5.2 lexer rules](https://github.com/imba/imba/blob/ee743778e205e8b50aa6a6cd1238ee904c33854d/lib/compiler/lexer.js#L118-L120)
- Evidence conflicts or gaps: current prose says a space is required after `#`,
  while both compilers also accept tab, `!`, and bare end-of-line forms. The
  implementation defines those edges. The unversioned dataset label prevents
  safely enabling Imba-2-only slash forms.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: pinned v1/v2 lexer regular expressions and token
  dispatch inspected; no compiler runtime was built.
- Probe input: `# note\n#symbol\n### block ###\n// v2 only`
- Observed result: the first and third are common comments, `#symbol` is not,
  and the final form differs between the two checked generations.
- Conclusion and limits: the common subset is implementable; version-specific
  slash comments require future version detection rather than a guessed union.

### Representative examples

```imba
# explain the component
tag App
    let state = #ready
    ### rendered only on the client ###
```

### Adversarial boundaries

- Negative cases: `#symbol`, `##symbol`, tag IDs, CSS color/selectors, all
  string/heredoc/regex forms, `///`, and v1 input containing v2-only slash forms.
- Malformed-input cases: bare `###`, nonempty unclosed triple block, extra
  closers, and an unterminated protected literal.
- Line-ending and Unicode cases: LF, CRLF, EOF, bare `#`, `#` plus tab, and
  Unicode bodies/identifiers.
- Version or dialect counterexamples: Imba 2 accepts `//` and `/*...*/`; Imba
  1.5.2 lacks those lexer rules. Do not silently combine them.
- Cleaner preservation cases: keep `#ready`, selectors/colors, indentation, and
  every byte after an accepted unclosed block opener.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `imba` with a lexer-aware scanner for
  the v1/v2-common hash and triple-hash forms plus accepted EOF-block metadata.
- Deterministic tests to add: whitespace-sensitive hashes, symbols/selectors,
  protected literals, closed/unclosed triple blocks, v1/v2 slash counterexamples,
  CRLF, Unicode, and sanitizer preservation.
- Remaining blocker: version-specific slash forms remain excluded until a
  deterministic source-version discriminator is established.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Ink

### Identity and scope

- Raw dataset label: `Ink` (39,829 files; 47,287,620 tokens)
- Proposed registry key: `ink`
- Existing family or aliases checked: non-nested C-style; rejected as the final
  family because Ink preprocesses comments before parsing and accepts a
  nonempty unclosed block through EOF.
- Classification: `language`
- Versions or releases checked: ink 1.2.1 commit
  `35c63e52f1d36060930dc7ed3cfba38ea224b528`.
- Intended support scope: `.ink` narrative source passed through the official
  `CommentEliminator`.
- Explicitly excluded scope: compiled JSON, Unity/C# integration source, Inky
  project metadata, and the unrelated React terminal package named Ink.

### Syntax contract

- Line comments: `//` anywhere in raw source through CR, LF, or EOF.
- Block comments: `/*` through the first `*/`.
- Nested comments: no; a nested-looking opener has no depth effect.
- Termination at newline, delimiter, or EOF: line comments accept EOF. A
  nonempty unclosed block is consumed through EOF by `ParseUntil`; a closed
  block ends at its first closer.
- Inline use: yes for both forms, including within ordinary narrative text.
- Adjacent-line grouping: yes for consecutive `//` lines; keep blocks separate.
- Unclosed delimiter behavior: accept a nonempty `/*...EOF` match with only an
  opening wrapper. A bare `/*` has no nonempty `ParseUntil` result and must not
  be promoted to a verified comment.
- Lexical or structural context: comment elimination is a raw preprocessing pass
  before the Ink parser. It has no string, quote, divert, or story-text state.
- Conflicts: `//` in prose such as `https://...` really starts a comment under
  the implementation. `#` begins Ink tag syntax, and `TODO:` produces a compiler
  warning; neither is an ignored comment delimiter.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`; the accepted EOF form has no closer.
- Content-preservation expectations: unlike the compiler, the cleaner must keep
  body text. Preserve physical line count; line-ending normalization is allowed
  only under the sanitizer's documented contract.

### Evidence

- Identity permalink:
  [Linguist Ink entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L3454-L3461)
- Official documentation:
  [Ink writing guide, comments](https://github.com/inkle/ink/blob/35c63e52f1d36060930dc7ed3cfba38ea224b528/Documentation/WritingWithInk.md#L77-L96)
- Official implementation:
  [`CommentEliminator`](https://github.com/inkle/ink/blob/35c63e52f1d36060930dc7ed3cfba38ea224b528/compiler/InkParser/CommentEliminator.cs)
  and
  [`StringParser.ParseUntil`](https://github.com/inkle/ink/blob/35c63e52f1d36060930dc7ed3cfba38ea224b528/compiler/StringParser/StringParser.cs#L551-L615).
- Evidence conflicts or gaps: the guide says block comments may span unlimited
  lines but does not specify malformed EOF. `ParseUntil` supplies the nonempty
  EOF behavior and the bare-opener edge.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned preprocessor and parser-combinator source
  inspected; no .NET build was run.
- Probe input: `Visit https://example.test/path\n/* unfinished note`
- Observed result: raw preprocessing treats `//example...` as a line comment and
  returns the nonempty unfinished block body through EOF.
- Conclusion and limits: source inspection establishes behavior before any Ink
  narrative syntax can protect the markers.

### Representative examples

```ink
=== start ===
Hello. // author note
/* multiline
   author note */
# scene-tag
```

### Adversarial boundaries

- Negative cases: `#` tags, `TODO:` warnings, `/` in ordinary text, and a bare
  opener `/*`; quoted or narrative-looking text does not protect `//` or `/*`.
- Malformed-input cases: nested-looking blocks close at the first `*/`; nonempty
  unclosed block reaches EOF; stray closer is data.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF line/block comments, and
  Unicode narrative/comment bodies.
- Version or dialect counterexamples: none found for the checked 1.2.1 compiler;
  generated JSON and host C# are excluded.
- Cleaner preservation cases: retain comment body and physical blank lines,
  preserve tags/TODO text, and never discard the rest of an accepted EOF block.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: add canonical `ink` with raw-prepass `//`,
  non-nested `/*...*/`, and nonempty EOF-block behavior; do not alias the stricter
  generic C-style family.
- Deterministic tests to add: global markers in prose/quotes/URLs, both normal
  forms, first-close nesting, unclosed nonempty and bare opener edges, tags,
  TODO, all line endings, Unicode, and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01
