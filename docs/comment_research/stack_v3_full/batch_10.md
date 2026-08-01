# Stack v3 Full Comment Research: batch_10

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics aggregated from
  `files[].language`
- Researcher or agent: `/root/research_batch_10`
- Review status: `reviewed`

The exact dataset identities and filename scopes were reconciled against
[Linguist commit `af6f772`](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml).
None of these ten raw labels resolved in the feature-branch registry at the
start of this research.

## TextGrid

### Identity and scope

- Raw dataset label: `TextGrid` (730,414 files; 3,666,252,663 tokens)
- Proposed registry key: `textgrid`
- Existing family or aliases checked: generic exclamation-line and
  format-header families; no existing family implements Praat quoting.
- Classification: `document-format`
- Versions or releases checked: Praat manual and source tree at commit
  `5d452fe3490bdc8d0edd12196a74127795b6a20a`
- Dialects checked: Praat full and short text TextGrid formats; binary TextGrid
  is excluded.
- Intended support scope: explicit `!` comments in textual TextGrid files.
- Explicitly excluded scope: binary files and the full-format labels that
  Praat describes as ignorable explanatory scaffolding. Those labels are
  interleaved with free-standing data and are not safe delimiter-based ranges.

### Syntax contract

- Line comments: `!` through the end of the physical line, outside a quoted
  text value.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF, CRLF, or CR terminates an
  explicit comment; a final comment at EOF is complete.
- Inline use: yes. The official example places `!` after free-standing data.
- Adjacent-line grouping: yes for consecutive explicit comment regions, but
  not across data or implicit full-format labels.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: quoted text is delimited by double quotes and
  represents an embedded data value. A double quote inside the value is
  doubled, so a helper must understand `""` before recognizing `!`.
- Conflicts with strings, operators, directives, or embedded languages: an
  exclamation mark inside a tier name, interval text, or mark is data. The
  first line's `"ooTextFile"` discriminator and the second line's
  `"TextGrid"` are data, not comments.
- Sanitizer line wrappers: `("!", "")` after lexical confirmation.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove only the explicit marker and
  preserve the remainder of the line, including phonetic Unicode. Do not
  discard full-format field labels or quoted annotations.

### Evidence

- Official documentation permalink:
  [pinned TextGrid file-format manual](https://github.com/praat/praat/blob/5d452fe3490bdc8d0edd12196a74127795b6a20a/docs/manual/TextGrid_file_formats.html)
- Documentation version and relevant section: Praat source commit above,
  sections 1, 2, 5, and 7. Section 2 states that everything following `!` on
  the same line is a comment; section 5 specifies doubled double quotes;
  section 7 lists LF, CR, and CRLF in existing files.
- Official rendered documentation:
  [TextGrid file formats](https://praat.org/manual/TextGrid_file_formats.html)
- Dataset identity evidence:
  [Linguist TextGrid entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8073-L8080)
- Evidence conflicts or gaps: Praat calls most human-readable field scaffolding
  "comments" because its reader consumes only free-standing numbers, strings,
  and flags. Extracting that distributed scaffolding would require a complete
  TextGrid parser and has no wrapper-cleaning contract. This recommendation is
  deliberately limited to the separately documented `!` form.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official format examples and reader contract were
  inspected; a Praat executable probe was not run.
- Exact version or commit: `5d452fe3490bdc8d0edd12196a74127795b6a20a`
- Probe method: trace the manual's intermediate-format example and quoted-text
  escaping rule.
- Probe input:

```text
"ooTextFile"
"TextGrid"
0 2.3 ! time domain
"IntervalTier" "Mary ! literal" ! type and name
```

- Observed result: the first `!` starts a comment; the exclamation mark in the
  quoted name is data; the final `!` starts a second comment.
- Conclusion and limits of the probe: the explicit line rule and string
  boundary are established, but implicit full-format scaffolding remains out
  of scope.

### Representative examples

```text
"ooTextFile"
"TextGrid"
0 2.3 ! time domain of TextGrid
"IntervalTier" "Mary" ! type and name of tier 1
```

The two suffixes beginning with `!` are comment ranges.

### Adversarial boundaries

- Negative cases: `text = "surprise!"`, `name = "say ""hi!"""`, first-line
  discriminator text, and full-format labels such as `xmin =` and `item [1]:`.
- Malformed-input cases: unclosed quoted text before `!`, odd quote runs, and a
  binary TextGrid payload misdecoded as text.
- Line-ending and Unicode cases: LF, CRLF, CR, EOF, UTF-8 phonetic content, and
  UTF-16 input rejected or decoded before character-based extraction.
- Version or dialect counterexamples: binary TextGrid and third-party tabular
  exports are not textual Praat TextGrid syntax.
- Cleaner preservation cases: empty `!`, leading whitespace after the marker,
  embedded exclamation marks in the payload, and doubled quotes in nearby data.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `textgrid` with an explicit-exclamation
  contextual extractor, one seeded example, raw sanitizer mode or a verified
  `!` wrapper, and the pinned Praat evidence.
- Deterministic tests to add: exact raw-label lookup; inline/own-line/EOF
  comments; doubled-quote strings; LF/CRLF/CR; implicit-label negatives;
  malformed quotes; and sanitizer body preservation.
- Remaining blocker: implementation must remain scoped to explicit `!`
  comments unless a separately reviewed full TextGrid tokenizer is added.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## TL-Verilog

### Identity and scope

- Raw dataset label: `TL-Verilog` (15,763 files; 11,812,930 tokens)
- Proposed registry key: `tl_verilog`
- Existing family or aliases checked: `verilog`, `systemverilog`, and
  `c_style`; reuse is not established by language ancestry.
- Classification: `language`
- Versions or releases checked: public TL-X/Redwood pages retrieved
  2026-08-01, SandPiper SaaS wrapper commit
  `17e7ca7b443957424e0d7d4447123118213380b7`, and the Linguist grammar identity.
- Dialects checked: current `.tlv` label only; no immutable TL-X language
  revision could be obtained.
- Intended support scope: unresolved pending a versioned lexer or specification.
- Explicitly excluded scope: SystemVerilog sections embedded through TL-X file
  region directives and M4 preprocessing output.

### Syntax contract

- Line comments: unresolved. Public examples use `//`, but examples and a
  highlighter are not a complete lexical contract.
- Block comments: unresolved. Verilog ancestry is not proof that every TLV
  region accepts `/* ... */` with identical termination rules.
- Nested comments: unresolved.
- Termination at newline, delimiter, or EOF: unresolved.
- Inline use: unresolved.
- Adjacent-line grouping: unresolved.
- Unclosed delimiter behavior: unresolved.
- Lexical or structural context: TL-Verilog files can contain region markers
  such as `\TLV`, `\SV`, and `\SV_plus`; comment behavior may depend on the
  active region and preprocessing stage.
- Conflicts with strings, operators, directives, or embedded languages:
  unresolved for TLV-native regions. M4 comments and generated HDL must not be
  inferred as TL-Verilog source comments.
- Sanitizer line wrappers: unresolved.
- Sanitizer block wrappers: unresolved.
- Content-preservation expectations: no cleaner registration until the full
  source contract is pinned.

### Evidence

- Official project page:
  [Redwood EDA TL-Verilog](https://www.redwoodeda.com/tl-verilog)
- Documentation version and relevant section: moving `TL-Verilog
  Specification` page retrieved 2026-08-01; it identifies TL-X specifications
  and file-region constructs but provides no immutable comment grammar.
- Official tool wrapper permalink:
  [SandPiper SaaS at `17e7ca7b`](https://gitlab.com/rweda/sandpiper-saas/-/tree/17e7ca7b443957424e0d7d4447123118213380b7)
- Implementation version, file, and relevant symbol: the pinned public project
  is a client for Redwood's hosted compiler; it does not expose the compiler
  lexer or comment actions.
- Dataset identity evidence:
  [Linguist TL-Verilog entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L7788-L7796)
- Secondary discovery source:
  [Linguist's pinned grammar provenance](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/vendor/README.md#L631)
  points to a VS Code highlighter. It is useful for locating samples but is not
  accepted as language evidence.
- Evidence conflicts or gaps: the official language specification exposed by
  the current website is not immutable, and the public SandPiper repository
  does not contain a lexer. No version-matched compiler token probe was
  available without relying on a moving hosted service.
- Confidence: `unresolved`

### Implementation confirmation

- Implementation tested: none; only the public wrapper and documentation were
  inspected.
- Exact version or commit: wrapper
  `17e7ca7b443957424e0d7d4447123118213380b7`
- Probe method: no acceptable offline lexer probe exists in the pinned public
  artifacts.
- Probe input:

```text
\TLV_version 1d: tl-x.org
\TLV
   // candidate
   /* candidate */
\SV
   // embedded SystemVerilog
```

- Observed result: not run; a highlighter classification would not settle the
  region-specific compiler semantics.
- Conclusion and limits of the probe: no delimiter recommendation is justified
  yet.

### Representative examples

No positive extraction example is accepted while the lexical contract remains
unresolved. The probe above is retained only as the minimal future test.

### Adversarial boundaries

- Negative cases: marker text in strings, `\TLV`/`\SV` transitions, M4 macro
  bodies, URLs, division operators, and generated SystemVerilog.
- Malformed-input cases: missing region terminator, unclosed block candidate,
  unknown TL-X version, and nested-looking blocks.
- Line-ending and Unicode cases: all remain to be established by a compiler
  probe.
- Version or dialect counterexamples: TLV 1a through 1d and future TL-X
  revisions must not be merged without evidence.
- Cleaner preservation cases: blocked until delimiters and region ownership are
  verified.

### Decision

- Recommended action: `defer`
- Registry fields to change: none.
- Deterministic tests to add: after evidence is obtained, region-transition,
  string, operator, line/block termination, and sanitizer tests.
- Remaining blocker: obtain an immutable TL-X specification containing lexical
  comments or a pinned SandPiper lexer/token-dump probe for every source region.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Toit

### Identity and scope

- Raw dataset label: `Toit` (6,065 files; 134,227,803 tokens)
- Proposed registry key: `toit`
- Existing family or aliases checked: `kotlin_style`, `nested_c_style`, and
  `c_style`; none models Toit's escape behavior inside block comments.
- Classification: `language`
- Versions or releases checked: Toit compiler commit
  `0d46acd86c2637c448157f6b1d6c7845252c685e`
- Dialects checked: current `.toit` compiler source, including Toitdoc forms.
- Intended support scope: ordinary and documentation comments recognized by
  the pinned compiler scanner.
- Explicitly excluded scope: comments in YAML handled by the compiler's vendored
  YAML scanner and marker text in string or character literals.

### Syntax contract

- Line comments: `//` through CR, LF, or EOF; `///` is a Toitdoc subset.
- Block comments: `/* ... */`; `/** ... */` is a Toitdoc subset when it is not
  the empty `/**/` form.
- Nested comments: yes, recursively.
- Termination at newline, delimiter, or EOF: a line comment ends before a line
  break; a block requires its balancing `*/`.
- Inline use: yes for line and block forms.
- Adjacent-line grouping: yes for consecutive line comments.
- Unclosed delimiter behavior: the scanner records the range through EOF but
  reports `Unterminated multi-line comment`; extraction must not accept it as a
  valid complete block.
- Lexical or structural context: the scanner dispatches comments outside
  literal string segments and character literals. Parenthesized `$(` string
  interpolations return to ordinary expression scanning, where comments are
  real trivia. Within a block comment, backslash escapes the next source
  character, so an escaped `/*` or `*/` does not change nesting depth.
- Conflicts with strings, operators, directives, or embedded languages: `/`,
  `/=`, URLs, and delimiters in literal portions of interpolated strings are
  not comments. Delimiters inside a parenthesized interpolation expression are
  comments when the ordinary scanner reaches them. Toit's indentation scanner
  treats comments as whitespace but still records their exact ranges.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: preserve Toitdoc body text and escaped
  delimiter characters. Never sanitize an unterminated diagnostic range as a
  complete comment.

### Evidence

- Official documentation permalink:
  [Toit language comments](https://docs.toit.io/language)
- Documentation version and relevant section: current language guide,
  `Comments and indentation`, retrieved 2026-08-01; it defines `//` line
  comments and inline placement.
- Official implementation permalink:
  [scanner comment routines](https://github.com/toitlang/toit/blob/0d46acd86c2637c448157f6b1d6c7845252c685e/src/compiler/scanner.cc#L843-L897)
- Implementation version, file, and relevant symbol:
  `src/compiler/scanner.cc`, `capture_single_line_comment` and
  `capture_multi_line_comment`.
- Interpolation-context evidence:
  [`Parser::parse_string_interpolate`](https://github.com/toitlang/toit/blob/0d46acd86c2637c448157f6b1d6c7845252c685e/src/compiler/parser.cc#L2418-L2499)
  parses `$(` content with the ordinary expression scanner; the adjacent
  recovery comment records that block comments have already been tokenized in
  that context.
- Documentation-comment evidence:
  [Toitdoc guide](https://docs.toit.io/language/sdk/toitdoc/)
- Dataset identity evidence:
  [Linguist Toit entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8112-L8119)
- Evidence conflicts or gaps: prose documentation does not spell out nesting or
  escaped delimiters; the pinned compiler scanner resolves both.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned scanner source was traced; the full Toit
  compiler was not built locally.
- Exact version or commit: `0d46acd86c2637c448157f6b1d6c7845252c685e`
- Probe method: follow `nesting_count` and the backslash branch in
  `capture_multi_line_comment`.
- Probe input:

```toit
main:
  // line
  /* outer /* inner */ tail */
  /* escaped \*/ still comment */
  text := "literal // text $(1 /* expression note */)"
```

- Observed result: the first block closes only after depth returns to zero; the
  backslash causes the first apparent closer in the second block to be skipped.
  The line marker in the final string's literal segment is data, while the
  block inside `$(` is scanned as a comment.
- Conclusion and limits of the probe: source inspection establishes comment
  depth and escapes without executing indentation diagnostics.

### Representative examples

```toit
main:
  // Keep this explanation.
  value := 1  // inline note
  /* outer
     /* nested */
     body */
```

The two line regions and one nested block are comments.

### Adversarial boundaries

- Negative cases: `"https://toit.io/*literal*/"`, division, `/=`, character
  literals, literal portions of interpolated strings, and markers in vendored
  YAML input. Pair each interpolation negative with a positive block comment
  inside a parenthesized interpolation expression.
- Malformed-input cases: unclosed outer/inner block, stray `*/`, escaped closer,
  escaped opener, and a trailing backslash at EOF.
- Line-ending and Unicode cases: LF, CRLF, CR, EOF line comment, non-ASCII body,
  and indentation following comment-only lines.
- Version or dialect counterexamples: Toitdoc is a semantic subset, not a
  separate delimiter family.
- Cleaner preservation cases: nested text, backslashes, empty comments,
  Toitdoc stars, inline spaces, and comment-only indentation.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `toit` with line matching plus a nested block
  scanner that honors backslash escapes; shield character and literal-string
  spans while re-entering ordinary comment scanning for `$(` expressions. Add
  pinned evidence, wrappers, and seeded ordinary/nested examples.
- Deterministic tests to add: raw mapping; line/EOF; nested blocks; escaped
  opener/closer; literal string segments versus `$(` expressions;
  strings/operators; unclosed blocks; indentation; Toitdoc; and sanitizer
  preservation.
- Remaining blocker: none; implementation must not use the existing
  escape-unaware nested delimiter walker unchanged.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Tor Config

### Identity and scope

- Raw dataset label: `Tor Config` (10,926 files; 6,278,588 tokens)
- Proposed registry key: `tor_config`
- Existing family or aliases checked: `hash_line_style`, INI, and shell-style
  families; all are too permissive around quoted and escaped hashes.
- Classification: `document-format`
- Versions or releases checked: Tor commit
  `2fbdc52d625c02a9787c9215cd5d1818dd575e4d`, whose format document describes
  the current parser contract and its July 2015 compatibility baseline.
- Dialects checked: `torrc` and included configuration text read by Tor.
- Intended support scope: physical `#` comments recognized by Tor's
  configuration grammar.
- Explicitly excluded scope: control-protocol `SETCONF` wire syntax and hashes
  protected inside quoted or escaped plain values.

### Syntax contract

- Line comments: `#` through LF or EOF outside a quoted value and outside a
  backslash-escaped character pair.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF terminates in the normative
  grammar and Windows text mode normalizes CRLF. A CRLF pair is therefore one
  physical line ending, but a bare CR is `NonLF` under the pinned grammar and
  must not independently terminate a comment.
- Inline use: yes, with or without whitespace before `#` in a plain value.
- Adjacent-line grouping: yes for consecutive physical comments. A comment line
  inside a continued value does not terminate that logical entry.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: double-quoted values use C-style escapes and
  may contain `#`. In a plain value, backslash followed by a non-newline
  character includes both verbatim, so `\#` is value data. A backslash-newline
  continues an entry; intervening comment lines are valid.
- Conflicts with strings, operators, directives, or embedded languages:
  `%include` is a directive. Hashes in quoted paths or escaped plain values are
  not comments.
- Sanitizer line wrappers: `("#", "")` after torrc lexical confirmation.
- Sanitizer block wrappers: none.
- Content-preservation expectations: strip only a confirmed hash marker and
  preserve the payload. Do not collapse continued configuration lines while
  cleaning extracted comments.

### Evidence

- Official format permalink:
  [Tor `torrc_format.txt`](https://gitlab.torproject.org/tpo/core/tor/-/blob/2fbdc52d625c02a9787c9215cd5d1818dd575e4d/doc/torrc_format.txt)
- Documentation version and relevant section: pinned Tor HEAD, `File Syntax`;
  `Comment`, `PVBody`, `QuotedVal`, `ContinuedVal`, `VC`, and `QC` define the
  contextual boundaries and examples demonstrate comments without preceding
  whitespace.
- Official sample configuration:
  [pinned `torrc.sample.in`](https://gitlab.torproject.org/tpo/core/tor/-/blob/2fbdc52d625c02a9787c9215cd5d1818dd575e4d/src/config/torrc.sample.in)
- Dataset identity evidence:
  [Linguist Tor Config entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8120-L8130)
- Evidence conflicts or gaps: the format document warns that stability is not
  guaranteed. This is a reason to pin the implementation scope, not to replace
  its grammar with generic hash matching.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official ABNF and examples were traced; Tor was not
  built locally.
- Exact version or commit: `2fbdc52d625c02a9787c9215cd5d1818dd575e4d`
- Probe method: classify candidate hashes against `PVBody`, `QuotedVal`, and
  `ContinuedVal`.
- Probe input:

```text
DataDirectory "/srv/tor/#private"
ContactInfo admin@example.test#public note
Nickname escaped\#hash
Log notice file /tmp/log \
 # continuation note
 file /tmp/second
```

- Observed result: the quoted and escaped hashes are value data; the inline
  hash and continuation-line hash begin comments.
- Conclusion and limits of the probe: establishes lexical comment starts but
  does not validate individual option values.

### Representative examples

```text
# Relay identity.
Nickname ExampleRelay # shown in metrics
ContactInfo "operator#1@example.test"
```

The first and second hashes start comments; the quoted hash does not.

### Adversarial boundaries

- Negative cases: quoted hashes, `\#`, `%include`, hashes after escaped
  backslashes, C-style escape sequences, and a hash in control-protocol data.
- Malformed-input cases: unterminated quote, trailing continuation, backslash at
  EOF, and a continued entry interrupted by several comments.
- Line-ending and Unicode cases: LF, CRLF, bare CR retained as comment/value
  content, EOF, tabs around comments, and non-ASCII payload text.
- Version or dialect counterexamples: controller `SETCONF` syntax is not a
  torrc file and must not inherit source comment extraction.
- Cleaner preservation cases: no-space inline comment, empty hash, multiple
  hashes in payload, indentation, and continuation structure.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `tor_config`/`torrc` with a quote-, escape-,
  and continuation-aware hash extractor and verified wrapper metadata.
- Deterministic tests to add: raw/alias mapping; own-line/inline/no-space/EOF;
  quoted and escaped negatives; continued comments; `%include`; line endings;
  malformed quotes; and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Tree-sitter Query

### Identity and scope

- Raw dataset label: `Tree-sitter Query` (139,443 files; 88,753,443 tokens)
- Proposed registry key: `tree_sitter_query`
- Existing family or aliases checked: `semicolon_style`; its delimiter matches,
  but its current generic regex does not prove Tree-sitter string boundaries.
- Classification: `language`
- Versions or releases checked: Tree-sitter commit
  `963b5a5a971021359cf091a63d4f1286bc319643`
- Dialects checked: core `.scm` query language consumed by `ts_query_new`.
- Intended support scope: semicolon line comments outside query string literals.
- Explicitly excluded scope: Scheme files that share `.scm`, comments in the
  source language being queried, and semicolons inside anonymous-node or
  predicate strings.

### Syntax contract

- Line comments: `;` through LF or EOF.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF terminates; EOF is accepted.
- Inline use: yes wherever the query parser next skips whitespace/trivia,
  including within a parenthesized pattern between tokens.
- Adjacent-line grouping: yes for consecutive semicolon comments.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: `stream_skip_whitespace` recognizes `;`; the
  string-literal parser consumes double-quoted strings separately, supports
  backslash escapes, and rejects literal newline or an unclosed quote.
- Conflicts with strings, operators, directives, or embedded languages: a
  literal node name such as `";"` and predicate text such as
  `"a;b"` are not comments. Capture names and predicates beginning with `#`
  have separate meanings.
- Sanitizer line wrappers: `(";", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove one semicolon and preserve all
  query-comment payload, including additional semicolons.

### Evidence

- Official documentation permalink:
  [query syntax manual](https://tree-sitter.github.io/tree-sitter/using-parsers/queries/1-syntax.html)
- Official implementation permalink:
  [`stream_skip_whitespace`](https://github.com/tree-sitter/tree-sitter/blob/963b5a5a971021359cf091a63d4f1286bc319643/lib/src/query.c#L404-L417)
- Implementation version, file, and relevant symbol: commit above,
  `lib/src/query.c`, `stream_skip_whitespace` and
  `ts_query__parse_string_literal`.
- Official conformance test:
  [`test_query_comments`](https://github.com/tree-sitter/tree-sitter/blob/963b5a5a971021359cf091a63d4f1286bc319643/crates/cli/src/tests/query_test.rs#L4580-L4604)
- Dataset identity evidence:
  [Linguist Tree-sitter Query entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8131-L8140)
- Evidence conflicts or gaps: none. The `.scm` extension overlap is an identity
  issue, not a syntax ambiguity once the dataset label is known.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned C parser and Rust CLI test were inspected; the
  repository was not compiled.
- Exact version or commit: `963b5a5a971021359cf091a63d4f1286bc319643`
- Probe method: trace trivia skipping and string-literal control flow.
- Probe input:

```scheme
; file comment
(function_declaration
  ; field comment
  name: (identifier) @name
  "semicolon;literal")
```

- Observed result: the first two semicolon suffixes are skipped as comments;
  the semicolon inside the quoted token is consumed by the string parser.
- Conclusion and limits of the probe: confirms comment and string boundaries;
  the last quoted anonymous node must also be valid in the target grammar to
  make the whole query semantically valid.

### Representative examples

```scheme
; Capture function names.
(function_declaration
  name: (identifier) @function.name) ; trailing note
```

Both semicolon regions are comments.

### Adversarial boundaries

- Negative cases: `";"`, `"a;b"`, escaped quotes, capture names, predicate
  `#match?`, source-language comments in quoted regexes, and ordinary Scheme
  input mislabeled as a query.
- Malformed-input cases: unclosed string before a semicolon, literal newline in
  a string, incomplete escape, and a comment at an incomplete pattern.
- Line-ending and Unicode cases: LF, CRLF, EOF, Unicode payload and identifiers,
  and the pinned scanner's bare-CR edge: `iswspace` can skip CR between tokens,
  but a semicolon comment already in progress continues until LF.
- Version or dialect counterexamples: query dialect extensions may add
  predicates but do not establish additional comment forms.
- Cleaner preservation cases: `;;` payload, inline spaces, consecutive lines,
  empty `;`, and semicolons after the first marker.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `tree_sitter_query` with semicolon line syntax
  and an exact double-quoted-string exclusion, plus pinned evidence and seeds.
- Deterministic tests to add: raw mapping; own-line/inline/EOF; quoted and
  escaped semicolons; predicates/captures; CRLF; malformed strings; grouping;
  and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## TSPLIB data

### Identity and scope

- Raw dataset label: `TSPLIB data` (477,526 files; 12,902,541,295 tokens)
- Proposed registry key: `tsplib_data`
- Existing family or aliases checked: properties/colon-record formats and
  contextual header extractors; none should be used because `COMMENT` is data.
- Classification: `document-format`
- Versions or releases checked: TSPLIB95 format documentation.
- Dialects checked: standard TSP, ATSP, SOP, HCP, CVRP, and TOUR text files.
- Intended support scope: no source-comment extraction from conforming TSPLIB95
  data.
- Explicitly excluded scope: solver-specific parameter files and wrappers that
  may define their own comment syntax.

### Syntax contract

- Line comments: unsupported.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: not applicable.
- Inline use: unsupported.
- Adjacent-line grouping: unsupported.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: the file consists of a specification part and
  a data part. `COMMENT : <string>` is a named specification entry whose value
  is parsed as additional metadata; it is not an ignorable lexical delimiter.
- Conflicts with strings, operators, directives, or embedded languages:
  `COMMENT`, `EOF`, section names, colons, and leading identifiers are all
  structural data.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: none.
- Content-preservation expectations: every conforming byte remains data; no
  comment cleaner should remove `COMMENT` records.

### Evidence

- Official specification permalink:
  [TSPLIB95 documentation](https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf)
- Documentation version and relevant section: TSPLIB95, section 1 and 1.1.3;
  the document defines every specification entry as `<keyword> : <value>` and
  defines `COMMENT` as a keyword carrying a string.
- Dataset identity evidence:
  [Linguist TSPLIB data entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L7808-L7817)
- Cross-checking parser documentation:
  [TSPLIB95 model fields](https://tsplib95.readthedocs.io/en/stable/pages/usage.html)
  exposes `comment` alongside `name`, `type`, and other parsed fields.
- Evidence conflicts or gaps: the English word "comments" describes the
  metadata value, but the grammar makes it a record. Treating it like a source
  comment would silently discard data, contrary to the cleaner contract.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: specification and a conforming parser model were
  inspected; no solver was run.
- Exact version or commit: TSPLIB95 fixed format document.
- Probe method: classify each line against specification keywords.
- Probe input:

```text
NAME : sample
COMMENT : contributed by Example Lab
TYPE : TSP
DIMENSION : 2
EDGE_WEIGHT_TYPE : EXPLICIT
EOF
```

- Observed result: `COMMENT` is a specification field and its value is retained
  in the parsed problem model.
- Conclusion and limits of the probe: establishes absence of lexical comments
  in TSPLIB95; vendor extensions are out of scope.

### Representative examples

There is no source-comment example. In the probe above,
`COMMENT : contributed by Example Lab` is data and must not be extracted.

### Adversarial boundaries

- Negative cases: `COMMENT`, `NAME`, `TYPE`, section headers, `EOF`, colons,
  semicolons in names, and hash characters in metadata strings.
- Malformed-input cases: unknown keywords, duplicate fields, missing section
  data, and missing `EOF`; none creates a comment.
- Line-ending and Unicode cases: parser encoding variation does not introduce
  comment syntax.
- Version or dialect counterexamples: LKH or solver parameter files are not
  covered merely because they accompany a `.tsp` file.
- Cleaner preservation cases: the complete `COMMENT` record and value must be
  preserved unchanged.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none; record the reviewed unsupported disposition
  in coverage tests/ledger.
- Deterministic tests to add: exact raw label remains unsupported and
  `COMMENT : ...`, `#`, `;`, and `//` produce no comment ranges.
- Remaining blocker: none; a future solver-specific label requires separate
  evidence.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## TypeSpec

### Identity and scope

- Raw dataset label: `TypeSpec` (34,586 files; 204,262,204 tokens)
- Proposed registry key: `typespec`
- Existing family or aliases checked: `c_style`; delimiters agree, but generic
  one-line quote masking does not cover TypeSpec triple-quoted strings and
  string templates.
- Classification: `language`
- Versions or releases checked: TypeSpec compiler commit
  `961e5aa200584a4e969e886d92d207c13986e3ef`
- Dialects checked: current `.tsp` source, ordinary comments, and doc comments.
- Intended support scope: compiler comment tokens outside all TypeSpec literal
  forms.
- Explicitly excluded scope: Markdown inside doc comments as a second language,
  JavaScript implementation files, and marker text in string/template spans.

### Syntax contract

- Line comments: `//` through the next TypeSpec line break or EOF.
- Block comments: `/*` through the first `*/`; `/** ... */` is a documentation
  subset.
- Nested comments: no.
- Termination at newline, delimiter, or EOF: line comments accept EOF; complete
  blocks require `*/`.
- Inline use: yes.
- Adjacent-line grouping: yes for consecutive line comments.
- Unclosed delimiter behavior: the scanner emits a multi-line-comment token for
  diagnostics but marks it unterminated; do not accept it as a complete block.
- Lexical or structural context: ordinary and triple-quoted literal string
  spans are scanned before comment dispatch. A string template stops its
  literal token at `${`, scans the interpolation as an ordinary expression,
  and resumes literal scanning after `}`. Comments in the expression are real;
  only the literal template spans protect marker text. Triple-quoted strings
  may cross physical lines, so simple line-local quote masking is insufficient.
- Conflicts with strings, operators, directives, or embedded languages:
  forward slash is an operator when not paired; literal template spans protect
  slash markers but `${value /* note */}` contains a real comment.
  `#suppress`, `#deprecated`, `#{`, and `#[` are directives/value syntax, not
  hash comments.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: keep Markdown/doc tags and ordinary body
  text; do not treat triple-string content as comments.

### Evidence

- Official documentation permalink:
  [TypeSpec comments and doc comments](https://typespec.io/docs/language-basics/documentation/)
- Documentation version and relevant section: current docs retrieved
  2026-08-01, `Comments` and `Doc comments`; defines `//`, `/* ... */`, and
  `/** ... */`.
- Official implementation permalink:
  [scanner comment dispatch](https://github.com/microsoft/typespec/blob/961e5aa200584a4e969e886d92d207c13986e3ef/packages/compiler/src/core/scanner.ts#L728-L742)
  and
  [termination routines](https://github.com/microsoft/typespec/blob/961e5aa200584a4e969e886d92d207c13986e3ef/packages/compiler/src/core/scanner.ts#L1047-L1064).
- Triple-string implementation evidence:
  [string scanner](https://github.com/microsoft/typespec/blob/961e5aa200584a4e969e886d92d207c13986e3ef/packages/compiler/src/core/scanner.ts#L1080-L1147)
- Template-expression evidence:
  [parser string-template spans](https://github.com/microsoft/typespec/blob/961e5aa200584a4e969e886d92d207c13986e3ef/packages/compiler/src/core/parser.ts#L1877-L1987)
  parse an ordinary expression between each literal head/middle/tail token.
- Dataset identity evidence:
  [Linguist TypeSpec entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8196-L8205)
- Evidence conflicts or gaps: none. Documentation omits explicit nesting
  language, but `skipMultiLineComment` stops at the first closer.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: scanner and scanner tests inspected; Node compiler
  probe not run.
- Exact version or commit: `961e5aa200584a4e969e886d92d207c13986e3ef`
- Probe method: trace slash dispatch, `skipMultiLineComment`, and triple-string
  scanning.
- Probe input:

```typespec
// ordinary
model A { value: string; /* block */ }
const sample = """
  // literal
  /* literal */
  """;
const name = "widget";
const templated = "value ${name /* expression comment */}";
```

- Observed result: the first two regions are comments; both marker-looking
  lines in the triple-quoted value belong to a string token. The final block is
  a comment token inside the template expression, not part of either literal
  template span.
- Conclusion and limits of the probe: source establishes boundaries without a
  full compiler execution.

### Representative examples

```typespec
/** A stored widget. */
model Widget {
  // Stable identifier.
  id: string;
}
```

The doc block and line are comments.

### Adversarial boundaries

- Negative cases: ordinary/triple strings and literal template spans, URLs,
  forward-slash operators, `#suppress`, `#deprecated`, `#{}`, `#[]`, and
  doc-code examples. Pair literal-span negatives with positive comments inside
  `${...}` expressions.
- Malformed-input cases: unclosed block, nested-looking block, unclosed ordinary
  or triple string, interpolation boundary, and stray `*/`.
- Line-ending and Unicode cases: all TypeSpec line-break characters used by
  `isLineBreak`, CRLF, EOF, and Unicode body/identifier text.
- Version or dialect counterexamples: Cadl-era naming does not establish a
  separate comment contract without a separately labeled dataset entry.
- Cleaner preservation cases: doc tags, Markdown stars, empty blocks, inline
  text, and marker-looking content inside fenced doc examples.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `typespec` with C-style non-nested delimiters
  and TypeSpec-aware ordinary/triple string exclusions. Template handling must
  shield only literal head/middle/tail spans and scan `${...}` expressions for
  comments. Add evidence and representative seeds.
- Deterministic tests to add: raw mapping; line/block/doc/EOF; first-close
  behavior; triple/ordinary strings; template literal spans and expression
  comments; directives; operators; unclosed blocks; line endings; and
  sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Typst

### Identity and scope

- Raw dataset label: `Typst` (79,173 files; 233,503,171 tokens)
- Proposed registry key: `typst`
- Existing family or aliases checked: `kotlin_style`; it has matching nested
  delimiters but lacks Typst markup, raw-text, URL, and shebang context.
- Classification: `language`
- Versions or releases checked: Typst commit
  `32fd4cc3861e0ab99f4c42ca6bea281482ba9f51`
- Dialects checked: markup, math, and code modes in `.typ` source.
- Intended support scope: lexer comment tokens across all three Typst modes.
- Explicitly excluded scope: raw text delimited by backtick runs, string
  literals, URL/link text, and the byte-zero `#!` shebang token.

### Syntax contract

- Line comments: `//` through the next Typst newline or EOF. Typst newlines are
  LF, VT, FF, CR, NEL, LS, and PS; CRLF is consumed as one line ending.
- Block comments: balanced `/* ... */` and an EOF-terminated `/* ... EOF`
  token accepted by the lexer.
- Nested comments: yes, recursively.
- Termination at newline, delimiter, or EOF: line comments stop before any
  Typst newline and accept EOF. Balanced blocks end when nesting returns to
  zero; otherwise the lexer emits one block-comment token through EOF.
- Inline use: yes in markup, math, and code where the lexer reaches the marker.
- Adjacent-line grouping: yes for consecutive line comments.
- Unclosed delimiter behavior: accepted as a block-comment token through EOF,
  even when nested depth remains nonzero. The official syntax test explicitly
  treats an unterminated opener as okay.
- Lexical or structural context: one shared lexer recognizes comments in every
  mode before mode-specific syntax. Raw text is consumed as a whole token;
  strings are consumed in math/code contexts; markup-mode escapes consume the
  escaped character; markup URLs such as `https://typst.app` are text/link
  syntax rather than comments. A shebang is recognized only from byte zero.
- Conflicts with strings, operators, directives, or embedded languages:
  division, URLs, raw code fences, `#` code expressions, and marker text inside
  strings are not comments.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")` for balanced blocks, plus
  `unclosed_block_openers=("/*",)` for the accepted EOF form.
- Content-preservation expectations: preserve nested bodies and all markup in
  comments; never strip URLs or raw/string content.

### Evidence

- Official documentation permalink:
  [Typst comment syntax](https://www.typst.app/docs/reference/syntax/#comments)
- Documentation version and relevant section: current reference retrieved
  2026-08-01, `Comments`; defines both forms across Typst syntax modes.
- Official implementation permalink:
  [lexer dispatch and comment routines](https://github.com/typst/typst/blob/32fd4cc3861e0ab99f4c42ca6bea281482ba9f51/crates/typst-syntax/src/lexer.rs#L91-L183)
- Implementation version, file, and relevant symbol: commit above,
  `crates/typst-syntax/src/lexer.rs`, `Lexer::next`, `line_comment`, and
  `block_comment`; block depth increments on each inner opener.
- Raw/URL boundary evidence:
  [markup lexer boundaries](https://github.com/typst/typst/blob/32fd4cc3861e0ab99f4c42ca6bea281482ba9f51/crates/typst-syntax/src/lexer.rs#L620-L668)
- Escape boundary evidence:
  [markup backslash handling](https://github.com/typst/typst/blob/32fd4cc3861e0ab99f4c42ca6bea281482ba9f51/crates/typst-syntax/src/lexer.rs#L488-L548)
- Official malformed-edge test:
  [`comment-block-unclosed`](https://github.com/typst/typst/blob/32fd4cc3861e0ab99f4c42ca6bea281482ba9f51/tests/suite/syntax/comment.typ#L72-L79)
  rejects a stray closer but states that an unterminated opener is okay.
- Dataset identity evidence:
  [Linguist Typst entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8206-L8215)
- Evidence conflicts or gaps: rendered docs do not call out nesting, but the
  pinned lexer explicitly tracks depth.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned Rust lexer inspected; Typst binary probe was
  not run. The pinned official syntax test was also inspected.
- Exact version or commit: `32fd4cc3861e0ab99f4c42ca6bea281482ba9f51`
- Probe method: trace shared dispatch, block depth, raw tokenization, and URL
  special handling.
- Probe input:

```typst
// line
Text /* outer /* nested */ tail */
https://typst.app/docs
`// raw /* text */`
#let value = "/* string */"
/* accepted through EOF
```

- Observed result: the first two regions are comments; URL, raw text, and
  quoted marker text are mode-specific non-comment tokens. The final unclosed
  opener is one block-comment token through EOF.
- Conclusion and limits of the probe: establishes the lexical contract without
  checking later semantic evaluation.

### Representative examples

```typst
// Explain the claim.
We show that /* nested /* reviewer note */ retained */ the result holds.
```

The line and balanced nested block are comments.

### Adversarial boundaries

- Negative cases: `https://` and `http://` links, arbitrary-length raw
  backticks, code/math strings, division, escaped markup, byte-zero shebang,
  and comments shown inside raw examples.
- Malformed-input cases: accepted unclosed blocks at several remaining depths,
  stray `*/`, unclosed raw text, unclosed string, and mixed mode delimiters.
- Line-ending and Unicode cases: LF, VT, FF, CR, CRLF, NEL, LS, PS, EOF,
  Unicode markup and comment bodies, and Unicode immediately around delimiters.
- Version or dialect counterexamples: package files are ordinary Typst source;
  embedded raw-language blocks retain their own content syntax.
- Cleaner preservation cases: nested body text, leading stars, markup symbols,
  URLs inside actual comments, empty blocks, and inline spacing.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `typst` with nested slash comments and a
  lexer-aware exclusion helper for raw text, strings, markup escapes and URLs,
  and the initial shebang. Enable the verified EOF block opener and add pinned
  evidence and seeds.
- Deterministic tests to add: raw mapping; line/nested/EOF; all three modes;
  URLs/raw/strings/markup-escape/shebang negatives; accepted unclosed and stray
  blocks; every Typst newline; and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Untyped Plutus Core

### Identity and scope

- Raw dataset label: `Untyped Plutus Core` (10,688 files; 202,826,952 tokens)
- Proposed registry key: `untyped_plutus_core`
- Existing family or aliases checked: `nested_dash_style` and `haskell_style`.
  The unconditional `nested_dash_style` contract matches; Haskell's
  symbol-following restriction is not the correct basis.
- Classification: `language`
- Versions or releases checked: Plutus commit
  `3e257708aea5705074ae5a9687e0d97d66a954f2`
- Dialects checked: textual UPLC programs consumed by the shared PLC/PIR/UPLC
  Megaparsec parser.
- Intended support scope: `--` line comments and nested `{- ... -}` comments in
  textual `.uplc` programs.
- Explicitly excluded scope: Haskell source implementing Plutus, Flat/CBOR
  serialized scripts, and comments in surrounding command or JSON files.

### Syntax contract

- Line comments: unconditional `--` through LF or EOF while consuming parser
  whitespace.
- Block comments: `{-` through balancing `-}`.
- Nested comments: yes; the parser uses Megaparsec's nested block consumer.
- Termination at newline, delimiter, or EOF: line comments accept EOF; blocks
  require balance and report a parse failure when unclosed.
- Inline use: yes wherever whitespace is accepted between textual UPLC tokens.
- Adjacent-line grouping: yes for consecutive line comments.
- Unclosed delimiter behavior: invalid; do not match through EOF.
- Lexical or structural context: comments are part of the shared whitespace
  consumer. Double-quoted text constants, byte strings, and identifiers are
  parsed as tokens before their internal characters can be trivia.
- Conflicts with strings, operators, directives, or embedded languages: unlike
  Haskell source, the UPLC whitespace consumer does not impose a following
  symbol restriction on `--`. Marker-looking content in a text constant is
  data.
- Sanitizer line wrappers: `("--", "")`.
- Sanitizer block wrappers: `("{-", "-}")`.
- Content-preservation expectations: preserve nested content and source order;
  never clean serialized binary script data as text comments.

### Evidence

- Official implementation permalink:
  [shared parser whitespace](https://github.com/IntersectMBO/plutus/blob/3e257708aea5705074ae5a9687e0d97d66a954f2/plutus-core/plutus-core/src/PlutusCore/Parser/ParserCommon.hs#L86-L93)
- Implementation version, file, and relevant symbol: pinned commit,
  `PlutusCore.Parser.ParserCommon.whitespace`, using `skipLineComment "--"`
  and `skipBlockCommentNested "{-" "-}"`.
- UPLC parser scope:
  [textual UPLC parser](https://github.com/IntersectMBO/plutus/blob/3e257708aea5705074ae5a9687e0d97d66a954f2/plutus-core/untyped-plutus-core/src/UntypedPlutusCore/Parser.hs)
- Text-literal boundary evidence:
  [builtin constant parser](https://github.com/IntersectMBO/plutus/blob/3e257708aea5705074ae5a9687e0d97d66a954f2/plutus-core/plutus-core/src/PlutusCore/Parser/Builtin.hs#L67-L90)
- Dataset identity evidence:
  [Linguist UPLC entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8276-L8284)
- Evidence conflicts or gaps: no conflict. The textual language reuses Haskell-
  shaped delimiters, but its implementation's unconditional line consumer is
  the controlling evidence.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned parser source inspected; Cabal test suite was
  not built.
- Exact version or commit: `3e257708aea5705074ae5a9687e0d97d66a954f2`
- Probe method: trace `leadingWhitespace`, `lexeme`, and the shared whitespace
  consumer used by UPLC terms/programs.
- Probe input:

```uplc
-- program note
(program 1.1.0
  {- outer {- nested -} tail -}
  (con string "-- literal {- text -}"))
```

- Observed result: the first two regions are consumed as whitespace comments;
  markers inside the string constant are literal content.
- Conclusion and limits of the probe: establishes comment semantics but does
  not exercise version-specific term validation.

### Representative examples

```uplc
-- Identity program.
(program 1.0.0
  {- the lambda {- nested detail -} follows -}
  (lam x x))
```

The line and nested block are comments.

### Adversarial boundaries

- Negative cases: text constants, byte strings beginning `#`, quoted
  identifiers, Haskell pragma syntax in implementation files, and Flat/CBOR
  bytes decoded as text.
- Malformed-input cases: unclosed outer/inner block, stray `-}`, incomplete
  program, and an unclosed text constant before a marker.
- Line-ending and Unicode cases: LF, CRLF, EOF line comment, tabs, and Unicode
  text/comment bodies accepted by the Text stream.
- Version or dialect counterexamples: Plutus Core and Plutus IR share the
  whitespace consumer but should retain their own raw-label aliases; serialized
  ledger scripts have no textual comment layer.
- Cleaner preservation cases: nested bodies, leading dashes, empty blocks,
  inline whitespace and marker-looking payload.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `untyped_plutus_core` to
  `nested_dash_style`, with a pinned UPLC evidence note and a UPLC-specific
  seeded example.
- Deterministic tests to add: raw mapping; own-line/inline/EOF; nested blocks;
  string and byte-string negatives; unconditional `--` before symbols;
  unclosed blocks; CRLF; and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## vCard

### Identity and scope

- Raw dataset label: `vCard` (83,927 files; 1,135,541,487 tokens)
- Proposed registry key: `vcard`
- Existing family or aliases checked: properties, INI, and iCalendar-like data
  families; none applies because RFC 6350 defines no presentation comments.
- Classification: `document-format`
- Versions or releases checked: vCard 4.0, RFC 6350 (August 2011), including
  updates listed by the RFC Editor.
- Dialects checked: standards-conforming text/vcard 4.0. Earlier vCard versions
  were checked only for identity and are not used to invent comment syntax.
- Intended support scope: no source-comment extraction from conforming vCard.
- Explicitly excluded scope: comments in container MIME headers, generated-code
  templates, and proprietary `X-` properties whose values may contain marker
  characters.

### Syntax contract

- Line comments: unsupported.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: not applicable. CRLF and folding
  delimit content lines, not comments.
- Inline use: unsupported.
- Adjacent-line grouping: unsupported.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: each interior line is a content line with an
  optional group, property name, parameters, colon, and value. Lines beginning
  with space or tab continue a folded content line.
- Conflicts with strings, operators, directives, or embedded languages:
  semicolons delimit parameters, colons delimit values, commas/semicolons may
  be escaped inside text, URLs contain `//`, and hash characters can be value
  data. `NOTE` is a typed property, not a lexical comment.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve every content line and folded
  continuation exactly; removing `NOTE` would discard contact data.

### Evidence

- Official specification permalink:
  [RFC 6350](https://www.rfc-editor.org/rfc/rfc6350.html)
- Documentation version and relevant section: RFC 6350 sections 3.2 and 3.3
  define unfolding and exhaustive `contentline` ABNF; section 6.7.2 defines
  `NOTE` as a text-valued property.
- RFC status and update record:
  [RFC Editor information page](https://www.rfc-editor.org/info/rfc6350/)
- Dataset identity evidence:
  [Linguist vCard entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L9427-L9439)
- Evidence conflicts or gaps: none. Human descriptions sometimes call `NOTE`
  a comment, but the normative grammar makes it preserved application data.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: normative ABNF and property definitions inspected; no
  vCard parser was run.
- Exact version or commit: RFC 6350, August 2011.
- Probe method: classify every physical line after unfolding against
  `contentline`.
- Probe input:

```text
BEGIN:VCARD
VERSION:4.0
FN:Example Person
NOTE:This is retained contact data
URL:https://example.test/a//b#profile
END:VCARD
```

- Observed result: `NOTE` and `URL` are property/value records; no source
  comment is present.
- Conclusion and limits of the probe: establishes absence of comment syntax in
  vCard 4.0; malformed or proprietary files remain data, not inferred comments.

### Representative examples

There is no source-comment example. Every line in the probe above is vCard
structure or property data.

### Adversarial boundaries

- Negative cases: `NOTE`, `URL:https://`, URI fragments, parameter semicolons,
  escaped `\,`/`\;`, folded lines, `#`, `//`, and `BEGIN`/`END` markers.
- Malformed-input cases: missing `END`, bad folding, an unknown property, and a
  line beginning with `#`; none should become a permissive comment match.
- Line-ending and Unicode cases: required CRLF, unfolded WSP continuations,
  UTF-8 property values, and escaped newlines.
- Version or dialect counterexamples: vCard 2.1/3.0 and jCard must be separately
  labeled/researched; neither justifies source comments here.
- Cleaner preservation cases: preserve complete `NOTE`, folded continuation,
  URI, and unknown `X-` property records.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none; record the reviewed unsupported disposition
  in coverage tests/ledger.
- Deterministic tests to add: exact raw label remains unsupported and NOTE,
  URLs, folds, hashes, semicolons, and slash pairs yield no comment ranges.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01
