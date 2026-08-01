# Stack v3 Full Comment Research: batch 04

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics table, aggregated
  from `files[].language`
- Researcher or agent: `/root/research_batch_04`
- Review status: `reviewed`

The proposed keys were normalized and collision-checked against the runtime
registry on 2026-08-01. Research artifacts and source checkouts remain under
`tmp/stack_v3_comment_research/`.

## ISPC

### Identity and scope

- Raw dataset label: `ISPC` (399,449 files; 211,663,779 tokens)
- Proposed registry key: `ispc`
- Existing family or aliases checked: `c_style` (`java` canonical); no key
  collision exists, and its two delimiters and non-nesting contract match ISPC.
- Classification: `language`
- Versions or releases checked: ISPC `1.32.0dev`, commit
  `e99a37840cd7d83c84e56e97a03eab6049b59fe7`.
- Dialects checked: compiler-accepted `.ispc` source before and after C
  preprocessing.
- Intended support scope: lexical comments in ISPC source.
- Explicitly excluded scope: comments in host C/C++ files, preprocessor line
  markers, string and character literals, and generated LLVM or object output.

### Syntax contract

- Line comments: `//` through LF or EOF.
- Block comments: `/*` through the first following `*/`.
- Nested comments: unsupported; an inner `/*` has no nesting effect.
- Termination at newline, delimiter, or EOF: a line comment accepts EOF; a block
  requires `*/`, and the compiler reports an unterminated comment at EOF.
- Inline use: valid for both forms.
- Adjacent-line grouping: valid for consecutive `//` lines.
- Unclosed delimiter behavior: invalid; do not extract a verified block through
  EOF.
- Lexical or structural context: comments are lexer tokens outside C-style
  quoted literals. Preprocessor `#` records are not comments.
- Conflicts with strings, operators, directives, or embedded languages: protect
  `"https://host/a//b"`, `'/'`, division, `#pragma`, and preprocessor line
  records. `/** ... */` is only a block-comment subset.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: remove only the outer delimiter and
  ordinary line scaffolding; preserve stars, slashes, Unicode, and newlines in
  the payload.

### Evidence

- Official documentation permalink:
  [ISPC lexical structure](https://github.com/ispc/ispc/blob/e99a37840cd7d83c84e56e97a03eab6049b59fe7/docs/ispc.rst#L2801-L2814)
- Documentation version and relevant section: ISPC `1.32.0dev`, "Lexical
  Structure"; it specifies both forms and explicitly forbids nesting.
- Official implementation or grammar permalink:
  [ISPC lexer rules and handlers](https://github.com/ispc/ispc/blob/e99a37840cd7d83c84e56e97a03eab6049b59fe7/src/lex.ll#L308-L310)
- Implementation version, file, and relevant symbol: same commit, `src/lex.ll`,
  `lCComment` at lines 718-736 and `lCppComment` at lines 919-931.
- Conformance test or official example permalink: the specification examples
  and the official source corpus use both forms; no dedicated conformance test
  was needed to resolve the contract.
- Secondary source, if needed: none.
- Evidence conflicts or gaps: none.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: source-level lexer inspection; compiler not built.
- Exact version or commit: `e99a37840cd7d83c84e56e97a03eab6049b59fe7`
- Probe method: traced the two lexer actions and their EOF paths.
- Probe input:

```text
uniform int n = 4; // lanes
/* outer /* not nested */ uniform int m = 2;
```

- Observed result: line input is consumed through LF/EOF; the first `*/` closes
  a block, and EOF before it emits `unterminated comment`.
- Conclusion and limits of the probe: the source and specification agree; the
  probe was not executed against a local binary.

### Representative examples

#### Line comment

```text
uniform int count = 4; // number of elements
```

#### Block comment

```text
/* Keep this uniform across all program instances. */
uniform int count = 4;
```

#### Nested or contextual comment

Unsupported: ISPC block comments do not nest.

### Adversarial boundaries

- Negative cases: quoted URLs, escaped quotes followed by `//`, character
  literals, division, `#pragma`, and `# line` records.
- Malformed-input cases: empty comments, `//` at EOF, lone `/*`, and an apparent
  nested block whose first closer ends the comment.
- Line-ending and Unicode cases: LF, CRLF, no final newline, and Unicode payload.
- Version or dialect counterexamples: C++ raw strings and comments in host C++
  are outside the ISPC lexer contract.
- Cleaner preservation cases: payload lines beginning with `*`, delimiter-like
  text before the real closer, and inline spacing.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `ispc` to `c_style.aliases` and attach the
  pinned evidence in alias-specific metadata if supported.
- Deterministic tests to add: exact-label lookup; line, EOF, block, non-nesting,
  unclosed block, strings, division, CRLF, and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01

## KDL

### Identity and scope

- Raw dataset label: `KDL` (28,735 files; 45,279,043 tokens)
- Proposed registry key: `kdl`
- Existing family or aliases checked: `nested_c_style` covers two lexical
  delimiters but cannot represent slashdash component scope or KDL strings.
- Classification: `document-format`
- Versions or releases checked: KDL 2.0.0 and legacy KDL 1.0.0 at commit
  `b8570137b6d3486a6b0cd64706f749c624ffd0ad`.
- Dialects checked: version-marked and unmarked KDL v1/v2 documents.
- Intended support scope: lexical comments plus parser-delimited slashdash
  comments in valid KDL v1 or v2 documents.
- Explicitly excluded scope: KDL Query/Schema languages, comments inside quoted
  or raw strings, and the optional `/- kdl-version 1|2` version marker itself.

### Syntax contract

- Line comments: `//` through the next KDL newline or EOF.
- Block comments: `/* ... */` comments may span lines.
- Nested comments: block comments nest recursively.
- Termination at newline, delimiter, or EOF: KDL newlines include CRLF, CR, LF,
  NEL, VT, FF, LS, and PS. A block requires a balancing `*/`.
- Inline use: line and block comments are valid where their corresponding KDL
  whitespace class is valid.
- Adjacent-line grouping: valid for consecutive `//` comments separated only by
  recognized KDL newlines/indentation.
- Unclosed delimiter behavior: an unclosed block or syntactically incomplete
  slashdashed component is invalid and must not become a verified match.
- Lexical or structural context: `/-` plus optional non-slashdash whitespace
  comments out one complete node, argument, property, or child block. The match
  must span that grammar component, even across lines; ranges nested inside that
  outer span must not be emitted separately.
- Conflicts with strings, operators, directives, or embedded languages: all
  marker text in quoted, multiline, or hash-delimited raw strings is data. The
  version marker is a directive. V1 and v2 permit slashdash at slightly
  different grammar positions, so a version-aware parser/fallback is required.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`; slashdash uses `("/-", "")`
  only after the helper has established the exact component span.
- Content-preservation expectations: preserve nested delimiters within block
  payloads and preserve the entire slashdashed component after removing only
  the outer slashdash marker and its scaffolding whitespace.

### Evidence

- Official documentation permalink:
  [KDL 2.0 comment sections](https://github.com/kdl-org/kdl/blob/b8570137b6d3486a6b0cd64706f749c624ffd0ad/draft-marchan-kdl2.md#L870-L901)
- Documentation version and relevant section: KDL 2.0.0, "Single-line",
  "Multi-line", and "Slashdash comments"; legacy behavior is in
  [`SPEC_v1.md`](https://github.com/kdl-org/kdl/blob/b8570137b6d3486a6b0cd64706f749c624ffd0ad/SPEC_v1.md#L105-L107).
- Official implementation or grammar permalink:
  [KDL 2.0 full grammar](https://github.com/kdl-org/kdl/blob/b8570137b6d3486a6b0cd64706f749c624ffd0ad/draft-marchan-kdl2.md#L1008-L1065)
- Implementation version, file, and relevant symbol: KDL 2.0 grammar,
  `single-line-comment`, `multi-line-comment`, `commented-block`, and
  `slashdash`.
- Conformance test or official example permalink:
  [nested block test](https://github.com/kdl-org/kdl/blob/b8570137b6d3486a6b0cd64706f749c624ffd0ad/tests/test_cases/input/nested_block_comment.kdl),
  [slashdashed node test](https://github.com/kdl-org/kdl/blob/b8570137b6d3486a6b0cd64706f749c624ffd0ad/tests/test_cases/input/commented_node.kdl).
- Secondary source, if needed: none.
- Evidence conflicts or gaps: v1 and v2 change legal slashdash positions but
  retain line and nested-block syntax. Dataset rows carry no version metadata.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official grammar and conformance cases inspected; no
  standalone KDL parser executed.
- Exact version or commit: `b8570137b6d3486a6b0cd64706f749c624ffd0ad`
- Probe method: traced nested `commented-block` recursion and slashdash targets.
- Probe input:

```text
node /* outer /* inner */ outer */ arg
/- removed key="value" { child }
kept /- old=true new=true
```

- Observed result: the block balances at depth two; slashdash removes one full
  node or property rather than merely the next physical line.
- Conclusion and limits of the probe: grammar proves scope; implementation must
  still validate v2 then v1 for unmarked legacy documents.

### Representative examples

#### Line comment

```text
server host="localhost" // development default
```

#### Block comment

```text
server /* outer /* migration note */ retained */ port=8080
```

#### Nested or contextual comment

```text
/- legacy-server host="old.example" {
  retry count=9
}
server host="new.example"
```

### Adversarial boundaries

- Negative cases: all string forms containing `//`, `/*`, or `/-`; `/`; `-`;
  the version marker; and KQL/KSL input.
- Malformed-input cases: unclosed/nested blocks, slashdash at an illegal
  position, slashdash followed only by EOF, and directly repeated slashdash.
- Line-ending and Unicode cases: every specified newline, CRLF as one newline,
  Unicode whitespace, BOM placement, and disallowed control characters.
- Version or dialect counterexamples: v1 versus v2 slashdash positions and
  explicit `kdl-version` selection.
- Cleaner preservation cases: nested blocks, multiline nodes, type annotations,
  properties, child blocks, strings and comments inside a slashdashed span.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `kdl` with line/nested wrappers and a
  version-aware grammar helper for slashdash ranges and literal protection.
- Deterministic tests to add: raw lookup; all three forms; v1/v2 version marker;
  node/property/argument/child scopes; nested blocks; strings; all newline
  classes; malformed EOF; non-overlap; and sanitizer preservation.
- Remaining blocker: none; the helper must use the pinned grammar rather than a
  line-oriented slashdash approximation.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01

## KerboScript

### Identity and scope

- Raw dataset label: `KerboScript` (42,109 files; 59,072,796 tokens)
- Proposed registry key: `kerboscript`
- Existing family or aliases checked: `slash_line_style` (`qsharp` canonical)
  has the same single delimiter and cleaning contract.
- Classification: `language`
- Versions or releases checked: official kOS development commit
  `8f281a459b6ea0ba917c91bbbc117e68bb948199`.
- Dialects checked: KerboScript parsed by the kOS TinyPG grammar; kRISC and C#
  implementation source are excluded.
- Intended support scope: comments in KerboScript source.
- Explicitly excluded scope: comments in generated C#, kRISC, documentation,
  configuration files, and string literal content.

### Syntax contract

- Line comments: `//` through LF or EOF.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: the official scanner pattern
  accepts an optional final newline, so EOF is valid; CR before LF is part of
  the physical line boundary.
- Inline use: valid.
- Adjacent-line grouping: valid for consecutive `//` lines.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: the scanner recognizes quoted strings as a
  longer token and skips `COMMENTLINE`; `//` outside a string always starts a
  comment.
- Conflicts with strings, operators, directives, or embedded languages:
  protect `"https://host/path"`, doubled-quote string escapes, division `/`,
  multiplication `*`, and array-index `#`. No `/* */` form exists.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove only `//`; preserve periods,
  braces, URLs, Unicode text and inline spacing in the payload.

### Evidence

- Official documentation permalink:
  [KerboScript syntax comments](https://github.com/KSP-KOS/KOS/blob/8f281a459b6ea0ba917c91bbbc117e68bb948199/doc/source/language/syntax.rst#L69-L99)
- Documentation version and relevant section: current kOS language syntax,
  "Other Symbols" and "Comments".
- Official implementation or grammar permalink:
  [TinyPG KerboScript grammar](https://github.com/KSP-KOS/KOS/blob/8f281a459b6ea0ba917c91bbbc117e68bb948199/src/kOS.Safe/Compilation/KS/kRISC.tpg#L74-L108)
- Implementation version, file, and relevant symbol: same commit,
  `COMMENTLINE`; generated `Scanner.cs` lines 371-377 adds it to the skip list.
- Conformance test or official example permalink:
  [parser comment test](https://github.com/KSP-KOS/KOS/blob/8f281a459b6ea0ba917c91bbbc117e68bb948199/src/kOS.Safe.Test/KS/ParserTest.cs#L24-L29)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: none.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official grammar, generated scanner, and parser test
  inspected; kOS was not built.
- Exact version or commit: `8f281a459b6ea0ba917c91bbbc117e68bb948199`
- Probe method: compared STRING and COMMENTLINE token patterns and skip order.
- Probe input:

```text
set x to 1. // inline
print "https://example.invalid/a//b".
// eof
```

- Observed result: only the first and third markers are skipped comments; the
  quoted URL is a STRING token.
- Conclusion and limits of the probe: source establishes the delimiter and
  string boundary; no runtime compiler invocation was needed.

### Representative examples

#### Line comment

```text
set throttle to 0.5. // hold during ascent
```

#### Block comment

Unsupported.

#### Nested or contextual comment

Unsupported.

### Adversarial boundaries

- Negative cases: quoted URLs, doubled quotes, division, lone slash, `/* */`,
  `#` array syntax, and C# source.
- Malformed-input cases: empty `//`, `//` at EOF, and lone `/` at EOF.
- Line-ending and Unicode cases: LF, CRLF, no final newline and Unicode payload.
- Version or dialect counterexamples: kRISC/C# comments are not KerboScript.
- Cleaner preservation cases: periods that terminate nearby statements,
  leading slash payload, URLs and indentation.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `kerboscript` to `slash_line_style.aliases`
  with pinned evidence metadata where supported.
- Deterministic tests to add: exact-label lookup; inline, adjacent and EOF
  lines; quoted URL/doubled quote; division; block negative; CRLF and sanitizer.
- Remaining blocker: none.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01

## Kickstart

### Identity and scope

- Raw dataset label: `Kickstart` (48,731 files; 139,251,963 tokens)
- Proposed registry key: `kickstart`
- Existing family or aliases checked: `hash_line_style` is too permissive and
  `ignore_list_style` lacks leading-whitespace, inline, and section semantics.
- Classification: `document-format`
- Versions or releases checked: pykickstart `3.76`, tag/commit
  `15c401010c5bb8984deca9a4d132f99f938bffc3`.
- Dialects checked: Fedora/RHEL command and package sections, script sections,
  certificate/raw sections, includes, and current special comment handling.
- Intended support scope: comments consumed by the pykickstart host parser,
  excluding raw section bodies and semantic pseudo-comments.
- Explicitly excluded scope: `%pre`, `%post`, `%onerror`, `%traceback`, and other
  `allLines` bodies; embedded interpreter syntax; certificate/raw data; and the
  semantic `#platform=` record.

### Syntax contract

- Line comments: a line whose first non-whitespace character is `#` is ignored
  in host command state and ordinary non-`allLines` sections. In command state,
  `shlex.split(..., comments=True)` also starts a comment at an unquoted `#` on
  a nonblank command line.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: physical line or EOF.
- Inline use: accepted only where host command lines are split with Python
  `shlex`; quotes protect `#`. Do not extend this rule into raw section bodies.
- Adjacent-line grouping: valid for consecutive host whole-line comments; do
  not group across section boundaries or with inline tails.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: the parser tracks command versus section
  states. `ScriptSection`, `NullSection`, and `CertificateSection` request every
  raw line and therefore retain comment-looking text for another interpreter or
  data consumer.
- Conflicts with strings, operators, directives, or embedded languages:
  `#platform=` is read as metadata; quoted URL fragments/passwords are data;
  shebangs and shell hashes in script sections are embedded syntax. `%include`
  changes source context but not the delimiter.
- Sanitizer line wrappers: `("#", "")` for helper-verified host comments.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve the payload and indentation;
  never clean or remove raw section content or semantic `#platform=` metadata.

### Evidence

- Official documentation permalink:
  [pykickstart file rules](https://github.com/rhinstaller/pykickstart/blob/15c401010c5bb8984deca9a4d132f99f938bffc3/docs/kickstart-docs.rst#L52-L97)
- Documentation version and relevant section: pykickstart 3.76, "Creating the
  Kickstart File"; lines beginning with `#` are ignored.
- Official implementation or grammar permalink:
  [pykickstart parser state machine](https://github.com/rhinstaller/pykickstart/blob/15c401010c5bb8984deca9a4d132f99f938bffc3/pykickstart/parser.py#L649-L719)
- Implementation version, file, and relevant symbol: same commit,
  `_isBlankOrComment` and `_stateMachine` at lines 741-784; `Section.allLines`
  and `ScriptSection` in `sections.py` lines 43-58 and 148-150.
- Conformance test or official example permalink:
  [official Kickstart examples](https://github.com/rhinstaller/pykickstart/blob/15c401010c5bb8984deca9a4d132f99f938bffc3/docs/kickstart-examples.rst#L10-L27)
- Secondary source, if needed: Python `shlex` behavior is used only because the
  pinned official parser invokes it directly.
- Evidence conflicts or gaps: user documentation promises whole-line comments;
  the current command-state implementation additionally strips unquoted inline
  hashes. That inline behavior is scoped to pykickstart 3.76, not generalized to
  every historical Kickstart reader.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: source-level state-machine trace; no Anaconda install
  or local pykickstart execution.
- Exact version or commit: `15c401010c5bb8984deca9a4d132f99f938bffc3`
- Probe method: followed `_isBlankOrComment`, `shlex.split`, and `allLines`.
- Probe input:

```text
  # host comment
url --url="https://host/tree#fragment" # inline host comment
%pre
# shell comment retained in script body
%end
```

- Observed result: the first and final unquoted tail are host comments; the URL
  hash is quoted data; the script hash is delivered unchanged to the section.
- Conclusion and limits of the probe: current parser semantics are clear; other
  consumer versions are outside the selected scope.

### Representative examples

#### Line comment

```text
# Reboot after package installation.
reboot
```

#### Block comment

Unsupported.

#### Nested or contextual comment

```text
%post
# interpreted by the post-install shell, not by Kickstart
%end
```

### Adversarial boundaries

- Negative cases: quoted hashes, `#platform=`, `%pre/%post` shebang/comments,
  certificate data, package names and URL fragments.
- Malformed-input cases: whitespace-only records, `#` at EOF, unterminated
  quotes before `#`, unterminated sections, and nested includes.
- Line-ending and Unicode cases: LF, CRLF, EOF and Unicode payload/paths.
- Version or dialect counterexamples: old versions without `%end`, downstream
  vendor sections, and non-pykickstart consumers.
- Cleaner preservation cases: leading indentation, hashes in payload, quoted
  fragments, and byte-for-byte raw section bodies.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `kickstart` with a parser-state helper, a hash
  wrapper, and explicit exclusion for `#platform=` and `allLines` bodies.
- Deterministic tests to add: raw lookup; indented/inline/EOF host comments;
  quoted hashes; command/package/script/certificate sections; `#platform=`;
  include transitions; CRLF; grouping; and sanitizer preservation.
- Remaining blocker: none for the pykickstart 3.76 scope.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01

## Koka

### Identity and scope

- Raw dataset label: `Koka` (8,556 files; 29,699,670 tokens)
- Proposed registry key: `koka`
- Existing family or aliases checked: `nested_c_style` (`dafny` canonical) has
  identical comment delimiters/nesting, but Koka needs raw-string masking.
- Classification: `language`
- Versions or releases checked: Koka `3.2.7`, commit
  `569c6d5586dc68dea65d3eba075ae9d0ccb86188`.
- Dialects checked: Koka v3 lexical specification and current compiler lexer.
- Intended support scope: Koka source comments, including documentation uses of
  the same delimiters.
- Explicitly excluded scope: `#` line directives, regular/raw strings,
  character literals, generated C/JavaScript, and editor grammar extensions.

### Syntax contract

- Line comments: `//` through the inserted/physical linefeed; EOF is treated as
  a line end by the specified lexer input normalization.
- Block comments: `/* ... */`.
- Nested comments: supported recursively.
- Termination at newline, delimiter, or EOF: line comments accept LF/CRLF/EOF;
  block comments require a balanced `*/`.
- Inline use: valid for both forms.
- Adjacent-line grouping: valid for consecutive `//` lines.
- Unclosed delimiter behavior: invalid block comment; do not match through EOF.
- Lexical or structural context: comments are whitespace tokens. Ordinary
  strings, character literals, and `r#*"..."#*` raw strings are scanned before
  comment recognition in their own lexer states.
- Conflicts with strings, operators, directives, or embedded languages: protect
  multiline raw strings containing delimiters, escaped ordinary strings,
  character literals, `/` operators, and column-start `#` line directives. A
  line directive is ignored by the compiler but is not a source comment.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: strip one outer wrapper; retain nested
  delimiter text, Unicode and line structure. Never strip a `#` directive.

### Evidence

- Official documentation permalink:
  [Koka lexical whitespace grammar](https://github.com/koka-lang/koka/blob/569c6d5586dc68dea65d3eba075ae9d0ccb86188/doc/spec/spec.kk.md#L208-L220)
- Documentation version and relevant section: Koka v3.2.7 draft specification,
  "White space"; raw strings are specified at lines 182-192.
- Official implementation or grammar permalink:
  [Koka lexer comment states](https://github.com/koka-lang/koka/blob/569c6d5586dc68dea65d3eba075ae9d0ccb86188/src/Syntax/Lexer.x#L117-L126)
- Implementation version, file, and relevant symbol: same commit,
  `<comment>` and `<linecom>` rules at lines 205-230; block openers push lexer
  state and closers pop it.
- Conformance test or official example permalink:
  [current Koka language specification](https://koka-lang.github.io/koka/doc/book.html#sec-language-specification)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: none. The specification explicitly says the Flex
  implementation is authoritative, while the current Haskell lexer agrees.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official specification and lexer source inspected;
  compiler not built.
- Exact version or commit: `569c6d5586dc68dea65d3eba075ae9d0ccb86188`
- Probe method: traced lexer-state push/pop and raw-string delimiter handling.
- Probe input:

```text
val x = 1 // line
/* outer /* inner */ outer */
val text = r#"// not comment /* neither */"#
```

- Observed result: the first two regions become `LexComment`; raw-string content
  remains in the `stringraw` state.
- Conclusion and limits of the probe: delimiter behavior is conclusive; the
  registry needs Koka-aware raw-string protection for a safe alias.

### Representative examples

#### Line comment

```text
val attempts = 3 // retry budget
```

#### Block comment

```text
/* outer rationale /* historical note */ retained text */
```

#### Nested or contextual comment

```text
val text = r#"// literal, not a comment"#
```

### Adversarial boundaries

- Negative cases: ordinary, raw and character literals; `/` operators; line
  directives; generated backends; delimiter text after escaped quotes.
- Malformed-input cases: unclosed nested block, stray closer, line at EOF, and
  raw-string delimiter-count mismatch.
- Line-ending and Unicode cases: LF, CRLF, EOF, valid Unicode payload and
  prohibited control/bidirectional characters.
- Version or dialect counterexamples: v1 syntax and generated JavaScript/C are
  not asserted by the v3 key.
- Cleaner preservation cases: nested delimiters, doc markup, Unicode, and
  marker-looking raw-string content.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `koka` to `nested_c_style.aliases` and add a
  narrow Koka literal-range scanner for ordinary, character and hash-delimited
  multiline raw strings before generic matching.
- Deterministic tests to add: raw lookup; line/EOF, nested depth, unclosed block,
  ordinary/raw/character strings, `/` operator, `#` directive, CRLF, Unicode,
  overlap ordering, and sanitizer preservation.
- Remaining blocker: none, provided raw-string masking lands with the alias.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01

## Lean 4

### Identity and scope

- Raw dataset label: `Lean 4` (316,684 files; 1,057,859,249 tokens)
- Proposed registry keys: `lean_4` and compact alias `lean4`, both sharing
  existing canonical key `lean`.
- Existing family or aliases checked: `lean_style`; exact delimiters, nesting,
  cleaning, and dialect scope match Lean 4.
- Classification: `dialect`
- Versions or releases checked: current Lean 4 commit
  `4b7a61dfa4ff3f29f07f0ae8ce428fbe39babd6f`.
- Dialects checked: ordinary Lean 4, declaration docstrings `/--`, and module
  docstrings `/-!`. Lean 3 was checked only for family compatibility.
- Intended support scope: all Lean 4 lexical and documentation comments.
- Explicitly excluded scope: strings containing markers, generated C, Lake TOML,
  and comments in tactic payload languages with their own lexer.

### Syntax contract

- Line comments: `--` through LF or EOF.
- Block comments: `/- ... -/`; `/-- ... -/` declaration docs and
  `/-! ... -/` module docs are specialized block-comment tokens.
- Nested comments: all block forms use nested `/-`/`-/` balancing.
- Termination at newline, delimiter, or EOF: line comments accept EOF. Block and
  documentation comments require a balancing `-/`; EOF is an unterminated
  comment error.
- Inline use: ordinary line/block comments are valid inline. Documentation
  variants additionally have parser placement rules, but remain extractable
  comment regions.
- Adjacent-line grouping: valid for consecutive `--` comments; do not merge
  documentation blocks automatically.
- Unclosed delimiter behavior: invalid; no verified block through EOF.
- Lexical or structural context: whitespace consumes ordinary comments, while
  `/--` and `/-!` are actual parser tokens. Quoted strings are lexed separately.
- Conflicts with strings, operators, directives, or embedded languages: protect
  `"--"`, `"/-"`, minus/subtraction, `/`, malformed doc placement, and quoted
  syntax. Tabs and isolated carriage returns also have Lean-specific errors.
- Sanitizer line wrappers: `("--", "")`.
- Sanitizer block wrappers: `("/-", "-/")`, with longest-first doc variants
  `("/--", "-/")` and `("/-!", "-/")` so the doc marker is scaffolding.
- Content-preservation expectations: preserve nested delimiter text and doc
  markup after removing only the outermost, longest matching wrapper.

### Evidence

- Official documentation permalink:
  [Lean parser comment implementation](https://github.com/leanprover/lean4/blob/4b7a61dfa4ff3f29f07f0ae8ce428fbe39babd6f/src/Lean/Parser/Basic.lean#L536-L587)
- Documentation version and relevant section: parser implementation documents
  whitespace/comment consumption and distinguishes doc tokens.
- Official implementation or grammar permalink: same pinned parser; nesting is
  the `finishCommentBlock` counter at lines 537-560.
- Implementation version, file, and relevant symbol: same commit,
  `finishCommentBlock` and `whitespace`.
- Conformance test or official example permalink:
  [Lean command doc-comment grammar](https://github.com/leanprover/lean4/blob/4b7a61dfa4ff3f29f07f0ae8ce428fbe39babd6f/src/Lean/Parser/Command.lean#L54-L62)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: none.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: source-level parser trace; Lean binary not invoked.
- Exact version or commit: `4b7a61dfa4ff3f29f07f0ae8ce428fbe39babd6f`
- Probe method: traced line `takeUntilFn`, nested depth increment/decrement, and
  the doc-token exclusions from ordinary whitespace.
- Probe input:

```text
def n := 1 -- line
/- outer /- inner -/ outer -/
/-- Declaration documentation. -/
```

- Observed result: line ends at LF/EOF, the block balances at depth two, and the
  doc form is parsed as a comment token rather than ordinary whitespace.
- Conclusion and limits of the probe: all extraction forms match the existing
  `lean_style` family; runtime diagnostics were not separately executed.

### Representative examples

#### Line comment

```text
def retries : Nat := 3 -- bounded attempts
```

#### Block comment

```text
/- outer explanation /- historical detail -/ retained -/
```

#### Nested or contextual comment

```text
/-- Returns the configured retry count. -/
def retries : Nat := 3
```

### Adversarial boundaries

- Negative cases: marker text in strings, subtraction/minus, division, quoted
  syntax, and generated C.
- Malformed-input cases: unclosed nested/doc blocks, stray `-/`, and doc forms
  in invalid parser positions.
- Line-ending and Unicode cases: LF, CRLF transport, isolated CR, EOF line,
  tabs around comments, and Unicode doc payload.
- Version or dialect counterexamples: Lean 3 compatibility must not justify new
  Lean 4 forms; Lake TOML is separate.
- Cleaner preservation cases: longest-first doc wrappers, nested delimiters,
  Markdown/code spans and leading punctuation.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `lean_4` and `lean4` to `lean_style.aliases`;
  retain canonical `lean` and its nested delimiter, and register longest-first
  sanitizer wrappers for `/--` and `/-!` documentation comments.
- Deterministic tests to add: exact raw and compact lookup; line/EOF, nested,
  doc/module-doc, unclosed, strings/operators, CRLF, grouping, and sanitizer
  longest-wrapper behavior.
- Remaining blocker: none.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01

## Jai

### Identity and scope

- Raw dataset label: `Jai` (9,920 files; 78,257,304 tokens)
- Proposed registry key: `jai`
- Existing family or aliases checked: `c_style` and `nested_c_style`; neither
  can be selected without verified current nesting and literal rules.
- Classification: `language`
- Versions or releases checked: go-enry commit
  `71719e4bdde528496011d030354a97b7f3ed4ff6`; public community primer commit
  `dd6581a2ffb9edf344463aa4020c118cd404df29`.
- Dialects checked: public `.jai` samples only. The closed-beta compiler version
  represented by each dataset file is not recorded.
- Intended support scope: unresolved pending a versioned official lexer or
  compiler probe.
- Explicitly excluded scope: unrelated projects named JAI, clean-room
  implementations, editor grammars, and syntax inferred from C/C++ ancestry.

### Syntax contract

- Line comments: unresolved. Public samples consistently show `//`, but no
  pinned official grammar establishes the dataset-wide contract.
- Block comments: unresolved. Community material shows `/* ... */`.
- Nested comments: unresolved. The community primer claims nested blocks, but
  explicitly states that none of its information is official.
- Termination at newline, delimiter, or EOF: unresolved.
- Inline use: provisionally observed for `//`, not accepted as registry proof.
- Adjacent-line grouping: unresolved.
- Unclosed delimiter behavior: unresolved.
- Lexical or structural context: unresolved for ordinary, raw, multiline, and
  compile-time string forms and for compiler directives.
- Conflicts with strings, operators, directives, or embedded languages: must
  test quoted URLs, division, directive syntax beginning `#`, nested blocks,
  and generated code once an official implementation is available.
- Sanitizer line wrappers: unresolved.
- Sanitizer block wrappers: unresolved.
- Content-preservation expectations: no cleaner contract may be registered
  before delimiters and nesting are verified.

### Evidence

- Official documentation permalink: unavailable publicly as of 2026-08-01.
- Documentation version and relevant section: unavailable; the compiler and
  bundled documentation remain in a closed beta.
- Official implementation or grammar permalink: unavailable publicly.
- Implementation version, file, and relevant symbol: unavailable.
- Conformance test or official example permalink: unavailable.
- Secondary source, if needed:
  [Jai Primer disclaimer and samples](https://github.com/BSVino/JaiPrimer/blob/dd6581a2ffb9edf344463aa4020c118cd404df29/JaiPrimer.md#L1-L9),
  [community nesting claim](https://github.com/BSVino/JaiPrimer/blob/dd6581a2ffb9edf344463aa4020c118cd404df29/JaiPrimer.md#L640-L670), and
  [go-enry label identity](https://github.com/go-enry/go-enry/blob/71719e4bdde528496011d030354a97b7f3ed4ff6/data/languageInfo.go#L6844-L6861).
- Evidence conflicts or gaps: the only detailed public source located disclaims
  official status and may lag a rapidly changing beta. It cannot establish
  nesting, EOF, or literal boundaries.
- Confidence: `unresolved`

### Implementation confirmation

- Implementation tested: none; no authorized official compiler was available.
- Exact version or commit: unresolved.
- Probe method: not run.
- Probe input:

```text
// candidate line form
/* candidate /* disputed nesting */ block */
```

- Observed result: no admissible result.
- Conclusion and limits of the probe: public examples locate questions but do
  not provide an oracle.

### Representative examples

#### Line comment

Unresolved; do not create a seed from community examples.

#### Block comment

Unresolved; do not create a seed from community examples.

#### Nested or contextual comment

Unresolved; nesting is the primary disputed behavior.

### Adversarial boundaries

- Negative cases: every string form, `/` operators, URLs, directives, and code
  generated or consumed at compile time.
- Malformed-input cases: comment opener at EOF, unmatched closers, and nested
  opener sequences.
- Line-ending and Unicode cases: LF, CRLF, EOF, and non-ASCII payloads.
- Version or dialect counterexamples: record the exact beta compiler version;
  do not combine older video syntax with current beta behavior.
- Cleaner preservation cases: blocked until wrappers are verified.

### Decision

- Recommended action: `defer`
- Registry fields to change: none.
- Deterministic tests to add: none until an official oracle is available; then
  add all disputed boundaries before the key.
- Remaining blocker: obtain a versioned official Jai reference/lexer or an
  authorized compiler probe with version output and minimized inputs.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01

## Java Template Engine

### Identity and scope

- Raw dataset label: `Java Template Engine` (17,076 files; 11,362,189 tokens)
- Proposed registry key: `java_template_engine`; optional short alias `jte`.
- Existing family or aliases checked: `java`, `jsp`, and markup/template
  families. None matches JTE's native delimiter and mode restrictions.
- Classification: `template`
- Versions or releases checked: jte `3.2.5-SNAPSHOT`, commit
  `5b2f6983f6eb3d804ddb3cf4a5dea4876dc1e60d`.
- Dialects checked: `.jte` Java templates with Plain and Html content types.
  Kotlin `.kte` is a distinct upstream extension and dataset concern.
- Intended support scope: native JTE comments in template text mode.
- Explicitly excluded scope: Java comments inside expressions, HTML comments,
  CSS/JavaScript comments, `@raw` bodies, and configuration-dependent removal
  of output-language comments.

### Syntax contract

- Line comments: unsupported as native JTE comments.
- Block comments: `<%--` opens and the first `--%>` closes a native JTE comment.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: comments span lines and require
  `--%>`; EOF in comment mode produces an unexpected-end parser error.
- Inline use: valid wherever the parser is in template `Text` mode.
- Adjacent-line grouping: not applicable to this block-only form.
- Unclosed delimiter behavior: invalid; do not accept through EOF.
- Lexical or structural context: the native opener is recognized only in
  `Text`, not inside `@raw`, Java code/string modes, or another comment.
- Conflicts with strings, operators, directives, or embedded languages:
  `<%--` inside `@raw ... @endraw` or `${"<%--"}` is literal/code content.
  `<!-- -->`, CSS `/* */`, and JavaScript comments have output-mode and option
  dependent behavior and are excluded from this native contract.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: `("<%--", "--%>")`.
- Content-preservation expectations: remove only the native outer wrapper;
  preserve HTML-like text, Java snippets, whitespace, and line endings inside.

### Evidence

- Official documentation permalink:
  [jte syntax, Comments](https://github.com/casid/jte/blob/5b2f6983f6eb3d804ddb3cf4a5dea4876dc1e60d/docs/syntax.md#L184-L194)
- Documentation version and relevant section: jte 3.2.5 development manual,
  "Comments"; native comments are omitted from rendered output.
- Official implementation or grammar permalink:
  [TemplateParser mode dispatch](https://github.com/casid/jte/blob/5b2f6983f6eb3d804ddb3cf4a5dea4876dc1e60d/jte/src/main/java/gg/jte/compiler/TemplateParser.java#L121-L170)
- Implementation version, file, and relevant symbol: same commit,
  `TemplateParser.doParse`, `isCommentAllowed` at lines 418-420, and
  `handleUnclosedKeywords` at lines 396-408.
- Conformance test or official example permalink: the official syntax example
  at documentation lines 188-190 is the canonical native form.
- Secondary source, if needed:
  [go-enry label identity](https://github.com/go-enry/go-enry/blob/71719e4bdde528496011d030354a97b7f3ed4ff6/data/languageInfo.go#L6965-L6985).
- Evidence conflicts or gaps: output-language comments may be stripped by the
  Html parser depending on `htmlCommentsPreserved`; they are intentionally not
  promoted to stable source-comment syntax.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official parser source inspection; jte was not built.
- Exact version or commit: `5b2f6983f6eb3d804ddb3cf4a5dea4876dc1e60d`
- Probe method: traced `Mode.Text -> Mode.Comment -> Mode.Text` and EOF handling.
- Probe input:

```text
Hello <%-- hidden --%> world
@raw <%-- literal --%> @endraw
```

- Observed result: the first region enters comment mode and is omitted; the raw
  region never enters comment mode.
- Conclusion and limits of the probe: mode and termination behavior are clear
  in source; no runtime rendering probe was executed.

### Representative examples

#### Line comment

Unsupported as a native JTE form.

#### Block comment

```text
<h1>Orders</h1><%-- Keep heading stable for clients. --%>
```

#### Nested or contextual comment

```text
@raw
<%-- rendered literally, not a JTE comment --%>
@endraw
```

### Adversarial boundaries

- Negative cases: native markers in `@raw`, Java strings/code, ordinary HTML
  comments, script/style blocks, and a lone `<%`.
- Malformed-input cases: opener at EOF, missing `--%>`, extra closer, and an
  apparent nested opener closed by the first closer.
- Line-ending and Unicode cases: LF, CRLF, multiline and Unicode payload.
- Version or dialect counterexamples: `.kte` and jte 1.x migration syntax are
  excluded from this exact `.jte` label contract.
- Cleaner preservation cases: HTML tags, `@` directives, nested-looking text,
  and leading/trailing spaces inside the wrapper.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add a `java_template_engine` family/key with the
  native wrapper and route it to a mode-aware helper; add `jte` only as an
  exact-syntax alias.
- Deterministic tests to add: raw-label and `jte` lookup; text-mode comment;
  multiline, unclosed, nonnested, raw/code/string negatives, CRLF, and cleaner.
- Remaining blocker: none for native comments; output-language comments remain
  deliberately excluded.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01

## JCL

### Identity and scope

- Raw dataset label: `JCL` (15,743 files; 58,603,531 tokens)
- Proposed registry key: `jcl`
- Existing family or aliases checked: no registry family models fixed-column
  JCL records, trailing comment fields, or embedded in-stream data.
- Classification: `language`
- Versions or releases checked: IBM z/OS 3.2 JCL reference.
- Dialects checked: base z/OS JCL statements. JES2, JES3, SMP/E JCLIN control
  comments, and utility control languages were examined only as exclusions.
- Intended support scope: base JCL comment statements and structurally
  identified comment fields outside in-stream data.
- Explicitly excluded scope: JES control statements, `DD *`/`DD DATA` payloads,
  custom `DLM` payloads, cataloged utility languages, and listing prefixes.

### Syntax contract

- Line comments: a JCL comment statement has `//*` exactly in columns 1-3;
  its comment text occupies the remainder of that record. Most JCL statements
  may also have a trailing comment field after the parameter field, separated
  by at least one blank.
- Block comments: unsupported. `/*` in columns 1-2 is a delimiter/JES statement,
  not a block-comment opener.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: comments are record-scoped. A
  comment statement may use through column 80; ordinary statement fields do not
  extend beyond column 71, with later columns reserved for control/sequence use.
- Inline use: only the grammar-defined trailing comment field, not a marker
  detectable by substring alone.
- Adjacent-line grouping: valid for adjacent `//*` comment statements; do not
  merge trailing fields or data records automatically.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: locating a trailing comment requires parsing
  the statement type, parameter field, quotes, parentheses, and continuation.
  The scanner must track `DD *`, `DD DATA`, and `DLM` regions.
- Conflicts with strings, operators, directives, or embedded languages: `//`
  identifies ordinary JCL, and `/*` may terminate in-stream data. In a plain
  `DD *` region, a record beginning `//` terminates the data and is interpreted
  as JCL; in a `DD DATA` region, the same bytes remain data until `/*`, a custom
  `DLM`, or EOF. JES2/JES3 assign meanings to some `/*` and `//*` records, so
  the base helper must not silently claim those dialects.
- Sanitizer line wrappers: `("//*", "")` for a full comment statement.
- Sanitizer block wrappers: none. A trailing comment field has no literal
  wrapper; a helper must return its payload span without deleting data.
- Content-preservation expectations: preserve comment text and column spacing;
  exclude sequence/control columns rather than folding them into payload.

### Evidence

- Official documentation permalink:
  [IBM z/OS 3.2 JCL statement fields](https://www.ibm.com/docs/en/zos/3.2.0?topic=statements-jcl-statement-fields)
- Documentation version and relevant section: z/OS 3.2, identifier and comment
  fields; it defines `//*` in columns 1-3 and the trailing comment field.
- Official implementation or grammar permalink: IBM publishes the normative
  product reference rather than an open lexer; no official source permalink is
  available.
- Implementation version, file, and relevant symbol: not applicable.
- Conformance test or official example permalink:
  [IBM in-stream `*` parameter rules](https://www.ibm.com/docs/en/zos/3.2.0?topic=statement-parameter)
- Additional conformance permalink:
  [IBM in-stream `DATA` parameter rules](https://www.ibm.com/docs/en/zos/3.2.0?topic=statement-data-parameter)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: JES2/JES3 use superficially overlapping record
  prefixes. The exact dataset label has no subsystem/version metadata, so those
  forms are excluded instead of generalized.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: no local z/OS implementation; normative reference
  rules were cross-checked across statement-field and in-stream-data pages.
- Exact version or commit: IBM z/OS 3.2 documentation.
- Probe method: documentation trace only.
- Probe input:

```text
//JOB1 JOB CLASS=A
//* Explain why this step is retained.
//STEP1 EXEC PGM=IEFBR14  no-op compatibility step
//SYSIN DD *
//* this ends DD * and is a JCL comment statement
//INPUT DD DATA
//* this is data until the delimiter
/*
```

- Observed result: the second record is a JCL comment statement and the EXEC
  tail is a comment field. The `//*` after `DD *` terminates that data and is
  processed as JCL, while the identical prefix after `DD DATA` remains data
  until the delimiter.
- Conclusion and limits of the probe: the structural contract is normative,
  but subsystem-specific JES forms need separate future research.

### Representative examples

#### Line comment

```text
//* Retain this step for catalog compatibility.
```

#### Block comment

Unsupported; `/*` is not a JCL block comment.

#### Nested or contextual comment

```text
//STEP1 EXEC PGM=IEFBR14  compatibility no-op
```

### Adversarial boundaries

- Negative cases: ordinary `//` statements, `/*` delimiters, apparent `//*`
  records inside `DD DATA` or custom-`DLM` payloads, quoted blanks,
  parentheses, continuation records, and columns 73-80 sequence data. A
  `//*` record after plain `DD *` is deliberately not a negative case because
  its leading `//` terminates the data.
- Malformed-input cases: indented `//*`, short records, missing data delimiter,
  invalid continuation, and a trailing blank with no legal parameter field.
- Line-ending and Unicode cases: fixed 80-byte records, LF/CRLF transport,
  EBCDIC-transcoded text, and payload outside ASCII after decoding.
- Version or dialect counterexamples: JES2 `/*...`, JES3 `//*...`, and SMP/E
  conditional JCLIN records need explicit dialect handling.
- Cleaner preservation cases: column alignment, asterisks in payload, blank
  comments, and trailing sequence numbers.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `jcl` with a fixed-record helper and only the
  verified full-line sanitizer wrapper.
- Deterministic tests to add: column-1 `//*`; indented negative; trailing-field
  parse; quoted/continued parameters; `DD *`, `DD DATA`, custom `DLM`; `/*`;
  sequence columns; CRLF; and cleaner preservation.
- Remaining blocker: none for scoped base JCL; JES dialect support is excluded.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01

## Just

### Identity and scope

- Raw dataset label: `Just` (64,698 files; 58,974,653 tokens)
- Proposed registry key: `just`
- Existing family or aliases checked: generic `hash_line_style` has the same
  marker but cannot distinguish just syntax from recipe-body text.
- Classification: `language`
- Versions or releases checked: just `1.57.0`, commit
  `13bf03f642f4cec7799c19f1f8f039e1cb3b095d`.
- Dialects checked: ordinary, shell, shebang/script, and `default-script`
  recipes; `set ignore-comments` behavior was also checked.
- Intended support scope: comments lexed by just outside recipe bodies.
- Explicitly excluded scope: shell/interpreter comments in recipe bodies and
  hashes in recipe text, even when runtime settings cause a line to be ignored.

### Syntax contract

- Line comments: `#` through CR, LF, CRLF, or EOF outside a recipe body.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: the lexer stops before the line
  ending and accepts EOF.
- Inline use: valid, including after a recipe header or expression.
- Adjacent-line grouping: valid for consecutive native comments outside recipe
  bodies; comments immediately before recipes may serve as documentation.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: `#` is a comment token in `lex_normal`; after
  recipe indentation begins, `lex_body` emits the full line as `Text` and only
  recognizes interpolation/newline boundaries.
- Conflicts with strings, operators, directives, or embedded languages: hashes
  in quoted strings are data. A recipe line such as `echo x # shell text` is
  not a native Just comment. `set ignore-comments` changes command execution,
  not lexical classification, and does not apply to script recipes.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove one native `#`; preserve recipe
  text entirely and preserve documentation-comment payload.

### Evidence

- Official documentation permalink:
  [Just documentation comments](https://github.com/casey/just/blob/13bf03f642f4cec7799c19f1f8f039e1cb3b095d/README.md#L1516-L1556)
- Documentation version and relevant section: just 1.57.0 manual,
  "Documentation Comments" and the `ignore-comments` setting at line 4837.
- Official implementation or grammar permalink:
  [Just lexer modes](https://github.com/casey/just/blob/13bf03f642f4cec7799c19f1f8f039e1cb3b095d/src/lexer.rs#L474-L604)
- Implementation version, file, and relevant symbol: same commit,
  `lex_normal`, `lex_body`, and `lex_comment` at lines 806-817.
- Conformance test or official example permalink:
  [lexer recipe-boundary tests](https://github.com/casey/just/blob/13bf03f642f4cec7799c19f1f8f039e1cb3b095d/src/lexer.rs#L1860-L1897)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the compact `GRAMMAR.md` production is less
  precise than the current lexer around modes; current lexer and tests govern.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official lexer and checked-in tests inspected; no
  local Rust build.
- Exact version or commit: `13bf03f642f4cec7799c19f1f8f039e1cb3b095d`
- Probe method: traced identical `#` text through `lex_normal` and `lex_body`.
- Probe input:

```text
# native
build: # native trailing
  echo value # recipe text
```

- Observed result: the first two hashes become `Comment`; the recipe-body line
  is one `Text` token.
- Conclusion and limits of the probe: source and tests prove the context split;
  execution under every possible recipe interpreter was intentionally excluded.

### Representative examples

#### Line comment

```text
# Build the release archive.
archive: dist.tar
```

#### Block comment

Unsupported.

#### Nested or contextual comment

```text
build:
  echo value # recipe text, not a native Just comment
```

### Adversarial boundaries

- Negative cases: `"# value"`, single/backtick strings, recipe hashes, shebang
  recipe bodies, and interpolation boundaries.
- Malformed-input cases: bare `#`, `#` at EOF, recipe header with no body, and
  inconsistent indentation around a comment-looking line.
- Line-ending and Unicode cases: LF, CRLF, EOF, Unicode payload and recipe text.
- Version or dialect counterexamples: `set ignore-comments`, script recipes,
  and `default-script` must not reclassify embedded lines as native comments.
- Cleaner preservation cases: documentation text, leading hashes in payload,
  and all recipe body bytes.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `just` and route hash matching through a lexer
  state/indentation helper; use the standard hash sanitizer only for returned
  native ranges.
- Deterministic tests to add: raw-label lookup; top-level, trailing and EOF
  comments; all string forms; recipe body, shebang/default-script and
  `ignore-comments` negatives; indentation, CRLF, grouping, and cleaner.
- Remaining blocker: none.
- Reviewer: `/root/review_batches_04_05`
- Review date: 2026-08-01
