# Stack v3 Full Comment Research: batch 00

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics table, aggregated
  from `files[].language`
- Researcher or agent: `/root/research_batch_00`
- Review status: `reviewed`

The registry lookup candidates and proposed keys below were collision-checked
against `LANGUAGE_SYNTAX` on 2026-08-01. None of the ten normalized Stack
labels currently resolves.

## Aiken

### Identity and scope

- Raw dataset label: `Aiken` (13,263 files; 52,715,749 tokens)
- Proposed registry key: `aiken`
- Existing family or aliases checked: `slash_line_style`, whose canonical key
  is `qsharp`; extraction delimiters match, but its shared cleaner cannot remove
  Aiken's full three- and four-slash documentation introducers without changing
  the payload contract for the other aliases. No `aiken` collision exists.
- Classification: `language`
- Versions or releases checked: Aiken compiler `1.1.23`, commit
  `6aa51055f6d54b57f508d8ddcb2c33612c96dee4`; documentation commit
  `20b105bcdf4842f31f24e36a2b9b8013670765ff`.
- Dialects checked: ordinary Aiken modules, documentation comments, and module
  comments. Untyped Plutus Core is a separate dataset language and is excluded.
- Intended support scope: lexical comments in `.ak` source accepted by the
  Aiken 1.1 lexer.
- Explicitly excluded scope: comments in `aiken.toml`, generated documentation,
  UPLC, string and byte-array literal contents, and Markdown interpreted inside
  documentation-comment payloads.

### Syntax contract

- Line comments: `//`, `///` (documentation), and `////` (module
  documentation) all consume through the end of the physical line. The
  longest prefix is classified first by the compiler, but all three have the
  same extraction and cleaning contract.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF, CRLF, or EOF. The compiler has
  a specific regression test for comments at EOF without a final newline.
- Inline use: valid; ordinary `//` can follow an expression.
- Adjacent-line grouping: valid for consecutive comment lines. Preserve each
  line's payload; do not reinterpret `///` or `////` as a block wrapper.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: comment recognition precedes operator parsing,
  but only after a literal has failed to start at that position. Aiken has `/`
  and `%` operators and both `@"..."` strings and `"..."` byte arrays.
- Conflicts with strings, operators, directives, or embedded languages:
  `@"https://example.invalid/a//b"`, `"a//b"`, and `x / y` are not comments.
  No block-comment delimiter exists.
- Sanitizer line wrappers: longest-first `("////", "")`, `("///", "")`, and
  `("//", "")`; all slashes in the compiler-classified introducer are
  scaffolding, while the text after them is payload.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve the payload byte-for-byte apart
  from the established line-ending normalization. Do not strip Markdown
  punctuation from documentation comments or leave an introducer slash in the
  cleaned payload.

### Evidence

- Official documentation permalink:
  [Aiken language-tour source](https://github.com/aiken-lang/site/blob/20b105bcdf4842f31f24e36a2b9b8013670765ff/src/pages/language-tour/functions.mdx)
- Documentation version and relevant section: language tour, Functions,
  "Documentation" and "Section headings"; it distinguishes `///` documentation
  comments and `//` section-heading comments.
- Official implementation or grammar permalink:
  [Aiken lexer](https://github.com/aiken-lang/aiken/blob/6aa51055f6d54b57f508d8ddcb2c33612c96dee4/crates/aiken-lang/src/parser/lexer.rs#L270-L353)
- Implementation version, file, and relevant symbol: Aiken `1.1.23`,
  `parser/lexer.rs`, `comment_line` and `comment_parser`; token choices for
  module, doc, and ordinary comments are ordered before normal tokens.
- Conformance test or official example permalink:
  [EOF comment parser test](https://github.com/aiken-lang/aiken/blob/6aa51055f6d54b57f508d8ddcb2c33612c96dee4/crates/aiken-lang/src/parser.rs#L102-L116)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: no conflict. The documentation does not provide a
  separate general comments page, but the official lexer is definitive.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: source-level lexer and official regression-test
  inspection; the compiler was not built locally.
- Exact version or commit: `6aa51055f6d54b57f508d8ddcb2c33612c96dee4`
- Probe method: traced `Token::ModuleComment`, `Token::DocComment`, and
  `Token::Comment` through `comment_parser`, and inspected the checked-in EOF
  test.
- Probe input:

```text
const n = 1 // ordinary
/// documentation
//// module documentation at EOF
```

- Observed result: each introducer is consumed to newline or EOF and recorded
  in the corresponding `ModuleExtra` span.
- Conclusion and limits of the probe: confirms all three line forms and EOF
  termination; it does not independently execute the compiler.

### Representative examples

#### Line comment

```text
const timeout = 60 // seconds
```

#### Block comment

Unsupported.

#### Nested or contextual comment

```text
/// Timeout in seconds.
const timeout = 60
```

### Adversarial boundaries

- Negative cases: `@"https://host/a//b"`, `"a//b"`, `total / count`, and a
  lone `/`.
- Malformed-input cases: empty `//`, `///`, and `////` at EOF; five or more
  slashes still begin a module-comment token via the four-slash prefix.
- Line-ending and Unicode cases: LF, CRLF, no final newline, non-ASCII Markdown
  in a `///` payload, and a Unicode scalar immediately before `//`.
- Version or dialect counterexamples: UPLC syntax and `#` comments in TOML are
  not Aiken source comments.
- Cleaner preservation cases: keep Markdown headings, backticks, URLs, leading
  indentation, and the extra slash that distinguishes documentation payloads.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: create canonical `aiken` with the shared `//`
  extraction shape but Aiken-specific longest-first `////`, `///`, and `//`
  sanitizer wrappers and pinned evidence. Do not add it to `slash_line_style`,
  because aliases must share one extraction and cleaning contract.
- Deterministic tests to add: raw-label lookup; `//`, `///`, and `////`; inline
  and EOF cases; strings containing `//`; division; LF and CRLF sanitizer
  preservation.
- Remaining blocker: none for the lookup and delimiter contract. String-literal
  negatives must pass before promotion.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Answer Set Programming

### Identity and scope

- Raw dataset label: `Answer Set Programming` (642,494 files;
  10,367,253,423 tokens)
- Proposed registry key: `answer_set_programming`
- Existing family or aliases checked: `percent_style` has only `%` line
  comments; `asp` is already an alias for ASP.NET and must not be reused. No
  `answer_set_programming` collision exists.
- Classification: `language`
- Versions or releases checked: clingo `5.8.0`, commit
  `920d06bcda7dd420814ce50953feff260a60fd8b`; Potassco guide commit
  `26fba894654e88aa511c2a547e69afe1ae0f23fa`.
- Dialects checked: Potassco clingo/gringo input language. The dataset label's
  upstream language metadata names `clingo` as its interpreter. Pure
  ASP-Core-2 and other solver extensions were not assumed to support clingo's
  full lexical extensions.
- Intended support scope: host-language comments accepted by clingo 5.8 in
  ordinary, theory, definition, and script-header lexer modes.
- Explicitly excluded scope: Python or Lua source between `#script (...)` and
  `#end`, solver output, ASPIF, and comments of other ASP implementations that
  do not accept clingo syntax.

### Syntax contract

- Line comments: `%` through end of line. clingo also treats `#!` through end
  of line as a comment in host-language modes.
- Block comments: `%*` opens and `*%` closes a block comment.
- Nested comments: supported to arbitrary lexer-counter depth; another `%*`
  increments the depth and each `*%` decrements it.
- A lone `%` encountered while already in a block enters the line-comment state
  until newline. Consequently, a `*%` later on that same physical line does not
  close the block; scanning resumes in block state on the next line.
- Termination at newline, delimiter, or EOF: line comments end at LF, CRLF, or
  EOF. Block comments require a matching `*%`; EOF while nested is a lexer
  error.
- Inline use: valid for `%` line comments and `%* ... *%` blocks.
- Adjacent-line grouping: valid for consecutive `%` or `#!` line comments;
  do not merge a following block automatically.
- Unclosed delimiter behavior: invalid. Do not manufacture a verified block
  match from `%*` through EOF.
- Lexical or structural context: quoted strings are tokens before comment
  markers. Within `#script` bodies the host comment rules are suspended until
  `#end`.
- Conflicts with strings, operators, directives, or embedded languages: `%` in
  a quoted string is data; `#show`, `#const`, and other `#` directives are not
  comments; Python remainder and floor-division operators inside a script body
  are embedded code, not ASP comments.
- Sanitizer line wrappers: `("%", "")` and `("#!", "")`.
- Sanitizer block wrappers: `("%*", "*%")`.
- Content-preservation expectations: preserve block payload and its internal
  newlines, including nested delimiters as content after removing only the
  outer wrapper.

### Evidence

- Official documentation permalink:
  [Potassco guide comment section](https://github.com/potassco/guide/blob/26fba894654e88aa511c2a547e69afe1ae0f23fa/language.tex#L1692-L1709)
- Documentation version and relevant section: Potassco guide, gringo
  meta-statements, "Comments"; documents `%` and `%* ... *%`.
- Official implementation or grammar permalink:
  [clingo nonground lexer](https://github.com/potassco/clingo/blob/920d06bcda7dd420814ce50953feff260a60fd8b/libgringo/src/input/nongroundlexer.xch#L149-L217)
- Implementation version, file, and relevant symbol: clingo `5.8.0`,
  `nongroundlexer.xch`; the `blockcomment` state maintains `bc`, the `comment`
  state handles line termination, and mode lists delimit where these rules
  apply.
- Conformance test or official example permalink:
  [nonground lexer test](https://github.com/potassco/clingo/blob/920d06bcda7dd420814ce50953feff260a60fd8b/libgringo/tests/input/nongroundlexer.cc#L38-L101)
- Secondary source, if needed:
  [upstream label identity](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L328-L337)
- Evidence conflicts or gaps: the guide documents blocks but does not state
  nesting; the current official lexer explicitly implements nesting. `#!` is
  implementation-defined and is not mentioned in the guide. These are scoped
  to clingo, not asserted as portable ASP-Core-2 syntax.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: official lexer source and checked-in lexer test; no
  local clingo binary execution.
- Exact version or commit: clingo `5.8.0`,
  `920d06bcda7dd420814ce50953feff260a60fd8b`
- Probe method: followed the mode transitions and `bc` counter in the generated
  lexer source.
- Probe input:

```text
a. % line
%* outer %* inner *% outer *% b.
#script (python)
x = 5 % 2
#end.
```

- Observed result: host `%` is a line comment, nested blocks balance through
  depth two, and the Python remainder operator is consumed in `script_body`
  rather than by the host comment rule.
- Conclusion and limits of the probe: source proves the disputed nesting and
  embedded-mode behavior; runtime diagnostics for every malformed EOF shape
  were not executed.

### Representative examples

#### Line comment

```text
chosen(X) :- candidate(X). % retain selected candidates
```

#### Block comment

```text
%* temporarily disabled rule *%
selected(X) :- chosen(X).
```

#### Nested or contextual comment

```text
%* outer
   %* inner *%
   outer
*%
```

### Adversarial boundaries

- Negative cases: `message("100% ready").`, `#show selected/1.`, `#const n=1.`,
  and `%` or `//` operators inside `#script` bodies.
- Malformed-input cases: `%*` at EOF, one missing `*%` in a nested block,
  unmatched `*%`, empty `%` at EOF, and `#!` at EOF.
- Line-ending and Unicode cases: LF, CRLF, CR-only probe, no final newline, and
  Unicode in line and nested-block payloads.
- Version or dialect counterexamples: ASP-Core-2 portability must not be claimed
  for nested blocks or `#!`; DLV and other solver dialects need their own
  evidence if added separately.
- Cleaner preservation cases: remove only the outer `%* ... *%`; retain nested
  markers and literal `%` text inside the payload; do not clean embedded script
  operators as comments.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add a distinct `answer_set_programming` family
  carrying `%`, `#!`, and nested `%* ... *%` metadata, and bind it to a helper
  that excludes quoted strings and `#script ... #end` bodies.
- Deterministic tests to add: all three comment forms, nested depth, inline
  blocks, unclosed blocks, directives, quoted percent signs, embedded Python
  and Lua bodies, raw-label normalization, and sanitizer preservation.
- Remaining blocker: none. For a malformed script body with no terminating
  `#end`, conservatively protect the remainder of the file from ASP comment
  extraction. Tests must also cover a lone `%` inside a block masking a later
  same-line `*%`.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## B4X

### Identity and scope

- Raw dataset label: `B4X` (10,536 files; 36,693,512 tokens)
- Proposed registry key: `b4x`
- Existing family or aliases checked: `apostrophe_style` covers several Visual
  Basic dialects but also accepts `REM`; the B4X founder explicitly identifies
  apostrophe as the B4X comment character. No `b4x` collision exists.
- Classification: `dialect`
- Versions or releases checked: B4X Language booklet edition 2.5
  (2024-01-05), B4X IDE booklet current in 2025, and the founder's 2014 syntax
  statement.
- Dialects checked: shared B4A, B4i, B4J, and B4R language syntax. The older
  Basic4ppc guide was used only as historical corroboration.
- Intended support scope: apostrophe comments in B4X source modules.
- Explicitly excluded scope: `#Region`, module attributes and other `#`
  directives, Java/Objective-C/C++ code embedded by platform-specific tooling,
  SQL strings, and comments in generated target-language source.

### Syntax contract

- Line comments: apostrophe (`'`) through end of line.
- Block comments: unsupported. The IDE's "Block Comment" command prefixes
  selected physical lines with apostrophes; it does not create a language-level
  block delimiter.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: newline or EOF.
- Inline use: valid; official getting-started examples place apostrophe comments
  after assignments.
- Adjacent-line grouping: valid for consecutive apostrophe-comment lines.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: ordinary strings use double quotes and smart
  strings use `$" ... "$`; apostrophes inside either are content. A doubled
  double quote is a string concern, not a comment escape.
- Conflicts with strings, operators, directives, or embedded languages:
  apostrophes in SQL/text strings are not comments; `#Region` and module
  attributes are directives, not hash comments. `REM` is deliberately excluded
  absent primary evidence that the B4X compiler accepts it as syntax.
- Sanitizer line wrappers: `("'", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove one leading apostrophe and
  conventional following space only according to the normal line-cleaning
  policy; preserve additional apostrophes and documentation text.

### Evidence

- Official documentation permalink:
  [B4X Getting Started guide](https://www.b4x.com/guides/B4XGettingStarted.html)
- Documentation version and relevant section: current guide, "My first
  program"; explicitly states that text after the quote is a comment and shows
  inline examples.
- Official implementation or grammar permalink: unavailable; B4X's compiler
  implementation is not published.
- Implementation version, file, and relevant symbol: unavailable.
- Conformance test or official example permalink:
  [B4X founder syntax statement](https://www.b4x.com/android/forum/threads/coments-as.37729/#post-222534)
- Secondary source, if needed:
  [B4X IDE commenting guide](https://www.b4x.com/guides/B4XIDE.html)
- Evidence conflicts or gaps: no public lexer or versioned grammar is
  available. Community posts sometimes use "rem out" colloquially, but the
  founder's direct answer says apostrophe is the language comment character and
  rejects additional markers. Therefore `REM` is not accepted into this
  contract without an executable compiler probe.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: not executable in this environment; official examples
  and the language designer's statement were cross-checked.
- Exact version or commit: B4X booklet edition 2.5; proprietary compiler version
  not available.
- Probe method: documentation/example inspection only.
- Probe input:

```text
Dim n As Int = 1 ' inline note
' full-line note
```

- Observed result: both forms are documented B4X comments.
- Conclusion and limits of the probe: sufficient for apostrophe syntax; no
  primary executable evidence supports `REM`, so it remains excluded.

### Representative examples

#### Line comment

```text
Dim retries As Int = 3 ' maximum attempts
```

#### Block comment

Unsupported; IDE block commenting emits one `'` per selected line.

#### Nested or contextual comment

```text
'Draws a cross at the given coordinates.
Sub DrawCross(x As Int, y As Int)
```

### Adversarial boundaries

- Negative cases: `Dim s As String = "Joe's"`, a smart string containing an
  apostrophe, `#Region Project Attributes`, and `REM` followed by prose.
- Malformed-input cases: empty apostrophe at EOF and an unterminated string that
  contains an apostrophe; favor string state until recovery proves otherwise.
- Line-ending and Unicode cases: LF, CRLF, no final newline, and non-ASCII text
  following the apostrophe.
- Version or dialect counterexamples: Visual Basic and VBA `REM` syntax must not
  leak into B4X; generated Java `//` comments are outside B4X source scope.
- Cleaner preservation cases: SQL examples containing apostrophes, doubled
  apostrophes in prose, and two consecutively comment-prefixed lines.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: create canonical `b4x` with apostrophe line syntax
  only; do not add it to `apostrophe_style` while that family includes `REM`.
- Deterministic tests to add: full-line and inline apostrophe comments, strings
  and smart strings, `#Region`, negative `REM`, EOF, CRLF, grouping, and
  sanitizer payload preservation.
- Remaining blocker: a proprietary-compiler probe would be needed before ever
  adding `REM`; it is not a blocker for apostrophe-only support.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## BibTeX Style

### Identity and scope

- Raw dataset label: `BibTeX Style` (112,305 files; 1,085,929,971 tokens)
- Proposed registry key: `bibtex_style`
- Existing family or aliases checked: `percent_style` already contains
  `bibtex`; no `bibtex_style` collision exists.
- Classification: `language`
- Versions or releases checked: original BibTeX style language 0.99d and TeX
  Live source commit `1a25c04b49317750330b4cf95994ea0d08f9d5ec`.
- Dialects checked: BibTeX `.bst` stack language. BibTeX database `.bib` files
  are a different dataset label and structural format.
- Intended support scope: `%` comments in `.bst` style programs.
- Explicitly excluded scope: arbitrary text and `@COMMENT` constructs in
  `.bib` databases, TeX comments inside output string contents, `.bbx` or
  `.cbx` BibLaTeX styles, and Biber configuration.

### Syntax contract

- Line comments: `%` through end of the physical input line, outside a quoted
  string. The comment may occupy the full line or follow a style-language
  token.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: newline or EOF.
- Inline use: valid; the official style guide shows `%` after executable style
  code.
- Adjacent-line grouping: valid for consecutive percent-comment lines.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: a quoted style string is delimited by `"` and
  must remain on one line. The style guide permits any printing character
  inside it, so `%` there is data. Number sign `#` introduces integer literals
  or concatenation-related syntax and is not a comment marker.
- Conflicts with strings, operators, directives, or embedded languages:
  `"100%"` is a string, `#1` is an integer literal, and TeX emitted from a
  string must not be recursively parsed as `.bst` source.
- Sanitizer line wrappers: `("%", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve TeX control sequences and `%`
  characters in the comment payload after removing only the leading comment
  marker.

### Evidence

- Official documentation permalink:
  [Designing BibTeX Styles](https://tug.org/texmf-docs/bibtex/btxhak.pdf)
- Documentation version and relevant section: Oren Patashnik, 1988,
  "Bibliography-style hacking"; states that BibTeX treats text following `%`
  as a style-file comment and shows inline examples.
- Official implementation or grammar permalink:
  [BibTeX WEB source](https://github.com/TeX-Live/texlive-source/blob/1a25c04b49317750330b4cf95994ea0d08f9d5ec/texk/web2c/bibtex.web#L789-L804)
- Implementation version, file, and relevant symbol: BibTeX 0.99d,
  `bibtex.web`; `comment = "%"`, `eat_bst_white_space`, and
  `bst_identifier_scan` implement end-of-line comments in style input.
- Conformance test or official example permalink:
  [scanner implementation](https://github.com/TeX-Live/texlive-source/blob/1a25c04b49317750330b4cf95994ea0d08f9d5ec/texk/web2c/bibtex.web#L3487-L3511)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the existing registry key `bibtex` does not
  distinguish `.bib` from `.bst`; this recommendation aliases only the exact
  Stack `BibTeX Style` label to the established percent-line extraction
  contract and does not validate the separate `.bib` mapping.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official WEB scanner and manual inspection; BibTeX
  was not invoked locally.
- Exact version or commit: BibTeX 0.99d at TeX Live commit
  `1a25c04b49317750330b4cf95994ea0d08f9d5ec`
- Probe method: traced the `%` constant through whitespace and identifier
  scanning, and compared the manual's executable example.
- Probe input:

```text
label "a" * 'label := % append a suffix
"100% literal" write$
```

- Observed result: the first `%` begins an inline comment; the percent sign
  inside the quoted style string is part of the string token.
- Conclusion and limits of the probe: confirms lexical context from source;
  does not reassess the separate `BibTeX` database label.

### Representative examples

#### Line comment

```text
label "a" * 'label := % append a suffix
```

#### Block comment

Unsupported.

#### Nested or contextual comment

```text
% Function names are stack-language identifiers.
FUNCTION {format.title} { title "t" change.case$ }
```

### Adversarial boundaries

- Negative cases: `"100%"`, `#1`, a TeX sequence stored inside a string, and
  `@COMMENT{...}` from a `.bib` file.
- Malformed-input cases: `%` at EOF and an unterminated quoted string containing
  `%`; the latter must not be confidently reclassified as a comment.
- Line-ending and Unicode cases: LF, CRLF, no final newline, and 8-bit/Unicode
  payload preservation without claiming broader BibTeX character support.
- Version or dialect counterexamples: BibLaTeX `.bbx`/`.cbx` use TeX syntax;
  `.bib` structural comments are out of scope.
- Cleaner preservation cases: TeX commands, braces, backslashes, doubled
  percent signs in prose, and inline comment spacing.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `bibtex_style` to `percent_style.aliases` and
  record that this alias is specifically the `.bst` language.
- Deterministic tests to add: normalized raw-label lookup, full-line and inline
  `%`, quoted-string negative, `#1`, EOF, CRLF, grouping, and sanitizer
  preservation.
- Remaining blocker: none for `.bst`; do not use this work as evidence that the
  separate `bibtex`/`.bib` mapping is structurally complete.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Bluespec BH

### Identity and scope

- Raw dataset label: `Bluespec BH` (75,938 files; 41,412,966 tokens)
- Proposed registry key: `bluespec_bh`
- Existing family or aliases checked: `bluespec_style` implements BSV `//` and
  non-nested `/* ... */`; `haskell_style` is closer but its current broad `--`
  pattern and pragma handling do not encode the BH lexical boundary. No key
  collision exists.
- Classification: `dialect`
- Versions or releases checked: BH Language Reference revision 2024-02-17 and
  BSC commit `941eecfe1bf583ce717a10965a0bcb6f6b3b8773`.
- Dialects checked: Bluespec Haskell / Bluespec Classic (`.bs`). Bluespec
  SystemVerilog (`.bsv`) remains the existing `bluespec` family.
- Intended support scope: BH source as accepted by the BSC Classic lexer.
- Explicitly excluded scope: BSV C-style comments, generated Verilog, and BH
  pragmas delimited by `{-#` and `#-}`.

### Syntax contract

- Line comments: a lexical token of two or more consecutive `-` characters
  followed by a non-symbol starts a comment through and including newline. The
  lexer also treats `@` after the dash run as comment-starting. A dash run
  followed by another symbol remains an operator.
- Block comments: `{-` through matching `-}`.
- Nested comments: supported to arbitrary depth.
- Termination at newline, delimiter, or EOF: ordinary-comment payload ends
  immediately before a required physical newline; the lexer consumes that
  newline while advancing. The current lexer reports `LexMissingNL` if such a
  comment reaches EOF without one. Nested comments require a matching `-}` and
  report `LexUntermComm` at EOF.
- Inline use: valid when the dash-run boundary rule is satisfied.
- Adjacent-line grouping: valid for consecutive ordinary-comment lines.
- Unclosed delimiter behavior: invalid; do not report an unterminated nested
  block as a verified match. A final line comment without newline can be
  retained only under an explicitly tested malformed-input recovery policy.
- Lexical or structural context: `{-# ... #-}` is tokenized as a pragma before
  the generic `{-` rule and is executable/compiler-directive syntax, not a
  comment. Strings and character literals take their own lexer paths.
- Conflicts with strings, operators, directives, or embedded languages:
  `--->`, `--+`, `--:`, and other symbol-followed dash runs are operators, not
  comments. `{-# properties ... #-}` is a pragma. `"-- text"` and `'-'` are
  literals.
- Sanitizer line wrappers: the complete leading dash run of at least two
  characters is syntactic scaffolding and must be removed; retaining extra
  introducer dashes as payload would disagree with the lexer boundary.
- Sanitizer block wrappers: `("{-", "-}")`.
- Content-preservation expectations: preserve nested delimiters inside the
  outer block payload and never strip pragma bodies as prose.

### Evidence

- Official documentation permalink:
  [BH language reference](https://github.com/B-Lang-org/bsc/blob/941eecfe1bf583ce717a10965a0bcb6f6b3b8773/doc/BH_ref_guide/BH_lang.tex#L510-L534)
- Documentation version and relevant section: revision 2024-02-17, "Comments in
  BH programs"; defines the dash boundary, `--->` counterexample, nested
  comments, and unlimited nesting.
- Official implementation or grammar permalink:
  [BSC Classic lexer](https://github.com/B-Lang-org/bsc/blob/941eecfe1bf583ce717a10965a0bcb6f6b3b8773/src/comp/Lex.hs#L198-L231)
- Implementation version, file, and relevant symbol: BSC at the pinned commit,
  `Lex.lx`, `isComm`, `skipComm`, and `skipToEOL`.
- Conformance test or official example permalink:
  [BH pragma example](https://github.com/B-Lang-org/bsc/blob/941eecfe1bf583ce717a10965a0bcb6f6b3b8773/doc/BH_ref_guide/BH_lang.tex#L3443-L3460)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the reference describes the ordinary comment as
  including end of line; the current lexer emits `LexMissingNL` at EOF. The
  report follows the implementation for malformed EOF behavior. The existing
  generic Haskell family is not precise enough to alias safely without shared
  hardening and BH-specific `@` review.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official source and reference comparison; BSC was not
  built locally.
- Exact version or commit: `941eecfe1bf583ce717a10965a0bcb6f6b3b8773`
- Probe method: traced the `isComm` guard and nested-depth counter.
- Probe input:

```text
x = y -- ordinary
op = (--->)
{- outer {- inner -} outer -}
{-# properties useSRAM = { verilog } #-}
```

- Observed result: the first line comments, `--->` remains an operator, the
  nested block balances, and the pragma receives dedicated tokens.
- Conclusion and limits of the probe: establishes all disputed boundaries from
  primary source; compiler execution remains for implementation-stage testing.

### Representative examples

#### Line comment

```text
value = next -- update the register
```

#### Block comment

```text
{- temporarily disabled definition -}
```

#### Nested or contextual comment

```text
{- outer {- inner -} outer -}
```

### Adversarial boundaries

- Negative cases: `(--->)`, `(--+)`, `(--:)`, `{-# noinline f #-}`,
  `"-- text"`, and a character literal containing `-`.
- Malformed-input cases: nested `{-` without `-}`, one unclosed inner level,
  unmatched `-}`, and a final `-- comment` without physical newline.
- Line-ending and Unicode cases: LF and CRLF, noting that the lexer treats CR
  separately; Unicode symbol characters after a dash run must follow `isSym`
  rather than ASCII-only assumptions.
- Version or dialect counterexamples: BSV `//` and `/* ... */` are not BH
  comments; Haskell behavior must not be assumed for BH's special `@` branch.
- Cleaner preservation cases: nested delimiters, extra dash prefixes, pragmas,
  and operator-heavy prose.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: create `bluespec_bh` with guarded ordinary line
  recognition, nested `{- ... -}`, and a `{-# ... #-}` pragma exclusion. Do not
  add it to `bluespec_style`.
- Deterministic tests to add: dash boundary table over every documented symbol,
  `--->`, `--@`, nesting, pragmas, strings/chars, malformed EOF, CRLF, Unicode
  symbols, grouping, ordering, and sanitizer preservation.
- Remaining blocker: none. A final ordinary dash comment without a physical
  newline is a conservative non-match because the pinned BSC lexer reports
  `LexMissingNL`; an unterminated nested block is likewise not a match.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## BQN

### Identity and scope

- Raw dataset label: `BQN` (8,562 files; 2,900,336 tokens)
- Proposed registry key: `bqn`
- Existing family or aliases checked: `hash_line_style` has a raw `#.*`
  pattern, but BQN permits multiline string literals and gives strings/comments
  explicit precedence; no `bqn` collision exists.
- Classification: `language`
- Versions or releases checked: BQN specification commit
  `1d43de0a8d66010c55f26fafb967c648d2fefade`; CBQN implementation commit
  `2d2337d3b31e8ba1c6625b2c0fb414bc6960154e` was checked for current project
  alignment.
- Dialects checked: canonical BQN source. REPL display/output is excluded.
- Intended support scope: lexical `#` comments in BQN source according to the
  normative token-formation specification.
- Explicitly excluded scope: character and string literal content, Markdown in
  BQN documentation, and shell comments surrounding launcher scripts.

### Syntax contract

- Line comments: `#` plus all following text up to, but not including, the next
  newline.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: either LF or CR is a newline in the
  specification; EOF also ends the final comment.
- Inline use: valid with or without whitespace before/after `#`, provided the
  marker is not already inside a literal.
- Adjacent-line grouping: valid for consecutive `#` comment lines.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: character/string literals and comments obey
  first-started precedence. A string may contain newline characters and escapes
  a double quote by doubling it. A character literal contains exactly one BQN
  character and needs no escape.
- Conflicts with strings, operators, directives, or embedded languages:
  `"# data"`, `'#'`, and a multiline string line beginning `#` are literal
  content. Once a comment begins, quotes inside it do not open literals.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve BQN Unicode glyphs and all text
  after the marker; operate on Unicode scalar boundaries, not UTF-16 code
  units.

### Evidence

- Official documentation permalink:
  [BQN token specification](https://github.com/mlochbaum/BQN/blob/1d43de0a8d66010c55f26fafb967c648d2fefade/spec/token.md#L3-L23)
- Documentation version and relevant section: normative "BQN token formation";
  defines newline characters, literal/comment precedence, exact `#` extent,
  and Unicode code-point processing.
- Official implementation or grammar permalink:
  [BQN reference token documentation](https://github.com/mlochbaum/BQN/blob/1d43de0a8d66010c55f26fafb967c648d2fefade/doc/token.md#L7-L25)
- Implementation version, file, and relevant symbol: canonical spec at pinned
  commit; token formation is itself the normative executable contract.
- Conformance test or official example permalink:
  [BQN comment help](https://github.com/mlochbaum/BQN/blob/1d43de0a8d66010c55f26fafb967c648d2fefade/help/comment.md)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: no conflict. The repository has no numbered
  language release attached to this commit, so support is commit-scoped.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: normative token examples and source rules inspected;
  CBQN was not built locally.
- Exact version or commit: BQN
  `1d43de0a8d66010c55f26fafb967c648d2fefade`
- Probe method: applied first-started literal/comment precedence to the
  specification examples.
- Probe input:

```text
1 + 2 # + 3
"# literal"
'#'
```

- Observed result: only the first line's `# + 3` is a comment.
- Conclusion and limits of the probe: normative evidence is complete; an
  implementation-stage differential probe against CBQN remains useful for
  malformed multiline literals.

### Representative examples

#### Line comment

```text
total ← +´ values # Sum the values
```

#### Block comment

Unsupported.

#### Nested or contextual comment

```text
"# literal" # actual comment
```

### Adversarial boundaries

- Negative cases: `"#"`, `'#'`, `"first
# still literal
last"`, and `""""` near a hash marker.
- Malformed-input cases: unterminated multiline string before `#`; remain in
  literal recovery rather than claiming a verified comment without a parser
  decision.
- Line-ending and Unicode cases: LF, CR, CRLF (avoid double termination), EOF,
  supplementary-plane BQN glyphs, combining characters, and invalid Unicode
  input handled without offset corruption.
- Version or dialect counterexamples: APL glyph behavior and notebook/REPL
  output are not BQN source-comment evidence.
- Cleaner preservation cases: BQN glyphs, hashes in prose, no whitespace after
  `#`, and adjacent Unicode comment lines.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: create `bqn` with `#` line-wrapper metadata and a
  small lexical helper that honors BQN character/string/comment precedence,
  including multiline strings and doubled double quotes.
- Deterministic tests to add: inline/no-space comments, string and character
  negatives, multiline strings, quote-in-comment, LF/CR/CRLF/EOF, Unicode
  offsets, malformed literals, grouping, and sanitizer preservation.
- Remaining blocker: none. If a BQN string starts before a hash and never
  closes, first-started precedence protects the remainder; do not recover by
  reclassifying a later hash as a verified comment.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## BuildStream

### Identity and scope

- Raw dataset label: `BuildStream` (21,695 files; 156,238,846 tokens)
- Proposed registry key: `buildstream`
- Existing family or aliases checked: `yaml` in `hash_line_style`; no
  `buildstream` collision exists.
- Classification: `document-format`
- Versions or releases checked: Apache BuildStream commit
  `ad6b437d760df8b3a8cdb151bd3da93ca3a77006`, pinned with
  `ruamel.yaml==0.19.1`; YAML 1.2.2 at spec commit
  `1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a`.
- Dialects checked: BuildStream 2 project configuration, `.bst` elements,
  plugin default YAML, `project.conf`, and `project.refs` parsed by the same
  loader.
- Intended support scope: the YAML presentation-layer comments in BuildStream
  configuration documents.
- Explicitly excluded scope: shell/Python comments inside scalar values,
  BuildStream conditional-expression syntax inside keys, and comments in
  plugin implementation `.py` files.

### Syntax contract

- Line comments: YAML `#` through end of line, only outside scalar content and
  separated from another token by whitespace. A comment-only line may have any
  indentation outside block scalar content.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: line break or EOF; YAML processors
  must accept an omitted final comment line break.
- Inline use: valid when whitespace separates the comment from preceding YAML
  content. In an unquoted plain scalar, a non-whitespace-preceded `#` remains
  scalar content.
- Adjacent-line grouping: valid for consecutive YAML comment lines, subject to
  block-scalar indentation boundaries.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: quoted scalars and literal/folded block scalars
  own their contents. `#` inside them is data. BuildStream's `(?)` and
  `(>)`-style directives are YAML keys/structures and add no comment marker.
- Conflicts with strings, operators, directives, or embedded languages:
  `url: https://host/a#fragment`, `value: "# data"`, and lines inside `|`/`>`
  scalar bodies are not comments. Shell fragments can contain their own `#`,
  but remain YAML scalar content.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve configuration prose only; never
  remove scalar text or reinterpret embedded commands.

### Evidence

- Official documentation permalink:
  [BuildStream project format](https://github.com/apache/buildstream/blob/ad6b437d760df8b3a8cdb151bd3da93ca3a77006/doc/source/core_format.rst)
- Documentation version and relevant section: current BuildStream 2 source;
  explicitly calls the format YAML and identifies `.bst` files and project
  configuration as the data model.
- Official implementation or grammar permalink:
  [BuildStream YAML loader](https://github.com/apache/buildstream/blob/ad6b437d760df8b3a8cdb151bd3da93ca3a77006/src/buildstream/_yaml.pyx#L244-L325)
- Implementation version, file, and relevant symbol: pinned BuildStream commit,
  `_yaml.load_data`; uses `ruamel.yaml.CParser` and explicitly permits a file
  containing only comments.
- Conformance test or official example permalink:
  [builtin project configuration](https://github.com/apache/buildstream/blob/ad6b437d760df8b3a8cdb151bd3da93ca3a77006/src/buildstream/data/projectconfig.yaml)
- Secondary source, if needed:
  [YAML 1.2.2 comments](https://github.com/yaml/yaml-spec/blob/1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a/spec/1.2.2/spec.md#L2791-L2868)
- Evidence conflicts or gaps: BuildStream constrains YAML nodes and forbids
  anchors/non-core tags, but it does not redefine YAML comment syntax.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official loader/source inspection and pinned YAML
  grammar comparison; no BuildStream build was run.
- Exact version or commit: BuildStream
  `ad6b437d760df8b3a8cdb151bd3da93ca3a77006`, ruamel.yaml `0.19.1`
- Probe method: traced `load_data` to `yaml.CParser` and inspected the explicit
  only-comments special case.
- Probe input:

```text
kind: manual # element kind
config:
  commands: |
    echo '# scalar data'
```

- Observed result: the first hash begins a YAML comment; the second is block
  scalar content.
- Conclusion and limits of the probe: establishes exact YAML inheritance;
  implementation-stage tests should execute the project's installed parser.

### Representative examples

#### Line comment

```text
kind: manual # build commands are configured below
```

#### Block comment

Unsupported.

#### Nested or contextual comment

```text
config:
  commands: |
    echo '# this is shell text inside a YAML scalar'
```

### Adversarial boundaries

- Negative cases: quoted `#`, URI fragments, unquoted `abc#def`, literal and
  folded scalar bodies, conditional keys, and shell snippets.
- Malformed-input cases: bad block-scalar indentation, an unterminated quoted
  scalar before `#`, and a comment-only file at EOF.
- Line-ending and Unicode cases: LF, CRLF, EOF without line break, Unicode keys
  and prose, and block-scalar chomping indicators.
- Version or dialect counterexamples: Python plugin files and shell scripts are
  separate languages; BuildStream directives do not create a second comment
  syntax.
- Cleaner preservation cases: `#` in commands, URLs, quoted variables,
  `%{variable}` substitutions, and comments adjacent to mappings/sequences.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: move `yaml` out of the generic hash-line family
  into a dedicated `yaml_style` family, add `buildstream` as its alias, and bind
  that family to a YAML-aware helper for token separation, quoted scalars, and
  block scalars. Adding `buildstream` directly to the current unconstrained
  `#.*` family would knowingly violate the researched contract.
- Deterministic tests to add: raw-label lookup, inline/full-line comments,
  whitespace boundary, quoted/plain scalars, URI fragments, block scalars,
  comments-only EOF, CRLF, grouping, and sanitizer preservation.
- Remaining blocker: none at the research layer. Implementation must land the
  dedicated YAML helper and pass scalar and whitespace-boundary negatives
  before the `buildstream` lookup is enabled.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Caddyfile

### Identity and scope

- Raw dataset label: `Caddyfile` (42,700 files; 12,551,557 tokens)
- Proposed registry key: `caddyfile`
- Existing family or aliases checked: `hash_line_style`; its unguarded `#.*`
  does not satisfy the Caddyfile token-start, quote, and heredoc rules. No key
  collision exists.
- Classification: `document-format`
- Versions or releases checked: Caddy 2 source commit
  `e096ca9503188f057c69a049f709fdade6077631` and its current Caddyfile lexer.
- Dialects checked: Caddy 2 Caddyfile adapter syntax, including double-quoted
  tokens, backtick-quoted tokens, heredocs, escaped newlines, and imports.
- Intended support scope: comments recognized by `caddyconfig/caddyfile` before
  directive parsing.
- Explicitly excluded scope: Caddy JSON configuration, template-language
  comments in served content, comments in imported files classified under
  another language, and hash characters in tokens/heredocs.

### Syntax contract

- Line comments: `#` through end of line only when `#` starts a token, meaning
  it is at file/line start or preceded by whitespace.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF or EOF. CR is ignored by the
  lexer and CRLF behaves as a single line ending.
- Inline use: valid when separated from the preceding token by whitespace.
- Adjacent-line grouping: valid for consecutive comment lines.
- Unclosed delimiter behavior: not applicable for comments; unterminated quote
  or heredoc state must prevent hashes within that state from becoming
  comments.
- Lexical or structural context: hashes are literal inside a token, a
  double-quoted token, a backtick-quoted token, or a heredoc. Double quotes may
  be escaped with backslash. Quoted/backtick tokens and heredocs may span lines.
  Escaped newlines continue an argument.
- Conflicts with strings, operators, directives, or embedded languages:
  `/some/#/path`, `"# value"`, `` `# value` ``, and heredoc body hashes are not
  comments. A `#` after whitespace is a comment even after another directive
  argument.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve the complete comment payload;
  never strip URI fragments or heredoc/quoted-token content.

### Evidence

- Official documentation permalink:
  [Caddyfile concepts, Comments](https://caddyserver.com/docs/caddyfile/concepts#comments)
- Documentation version and relevant section: Caddy 2 current documentation;
  states the exact token-start requirement and why hashes in URIs are allowed.
- Official implementation or grammar permalink:
  [Caddyfile lexer](https://github.com/caddyserver/caddy/blob/e096ca9503188f057c69a049f709fdade6077631/caddyconfig/caddyfile/lexer.go#L71-L238)
- Implementation version, file, and relevant symbol: pinned Caddy commit,
  `lexer.next`; `len(val) == 0` is the token-start guard and quote/backtick/
  heredoc states precede it.
- Conformance test or official example permalink:
  [Caddyfile lexer tests](https://github.com/caddyserver/caddy/blob/e096ca9503188f057c69a049f709fdade6077631/caddyconfig/caddyfile/lexer_test.go#L63-L96)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: no conflict. The moving documentation page is
  corroborated by a pinned implementation and pinned tests.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official source and conformance-test inspection; the
  Go tests were not run locally.
- Exact version or commit: `e096ca9503188f057c69a049f709fdade6077631`
- Probe method: followed `val`, `comment`, `quoted`, `btQuoted`, and `inHeredoc`
  state transitions and checked official expected token arrays.
- Probe input:

```text
redir / /some/#/path
respond "# literal"
file_server # actual comment
```

- Observed result: only the third hash starts a comment.
- Conclusion and limits of the probe: establishes the context boundary; malformed
  heredoc recovery still needs local deterministic coverage.

### Representative examples

#### Line comment

```text
reverse_proxy localhost:9000 # application upstream
```

#### Block comment

Unsupported.

#### Nested or contextual comment

```text
respond <<HTML
  # literal response text
HTML
# actual Caddyfile comment
```

### Adversarial boundaries

- Negative cases: `/some/#/path`, `abc#def`, quoted and backtick-quoted hashes,
  heredoc hashes, escaped quotes, and a hash after a continued token without
  whitespace.
- Malformed-input cases: unclosed double quote, backtick token, and heredoc;
  missing/invalid heredoc markers; trailing backslash before newline.
- Line-ending and Unicode cases: LF, CRLF, BOM at file start, EOF, Unicode token
  values, and Unicode whitespace as classified by Go `unicode.IsSpace`.
- Version or dialect counterexamples: Caddy JSON has JSON's no-comment
  contract; Caddy v1 syntax is not included without separate evidence.
- Cleaner preservation cases: URI fragments, hashes in response bodies,
  backticks, heredocs, and an inline comment after multiple arguments.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: create `caddyfile` with hash line-wrapper metadata
  and a lexer-like helper implementing token-start, quote, backtick, heredoc,
  escape, BOM, and line-continuation states.
- Deterministic tests to add: official lexer cases plus URI tokens, all quoted
  forms, heredocs, malformed states, Unicode whitespace, BOM, LF/CRLF/EOF,
  ordering, grouping, and sanitizer preservation.
- Remaining blocker: none. On an unterminated quote, backtick token, or heredoc,
  conservatively protect the remainder from hash-comment extraction; do not
  fall back to the unquoted token-start rule.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Cairo Zero

### Identity and scope

- Raw dataset label: `Cairo Zero` (26,506 files; 71,929,951 tokens)
- Proposed registry key: `cairo_zero`
- Existing family or aliases checked: `cairo` is currently an alias in
  `slash_line_style`; no `cairo_zero` collision exists.
- Classification: `dialect`
- Versions or releases checked: Cairo Zero compiler `0.14.3`, commit
  `cf9bf972bede402a125e8638bb258e77563ae933`.
- Dialects checked: legacy Cairo Zero only. Modern Cairo is a separate dataset
  label and remains under `cairo`.
- Intended support scope: Cairo Zero host-language `//` comments.
- Explicitly excluded scope: Python code inside `%{ ... %}` hint blocks,
  modern Cairo documentation semantics, generated CASM, and strings/short
  strings.

### Syntax contract

- Line comments: `//` through end of line; grammar permits an optional comment
  after each code element and comments as notes inside parentheses.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: the parser normalizes a missing
  final newline by appending one, so extraction may treat EOF as termination.
- Inline use: valid after a code or struct element.
- Adjacent-line grouping: valid for consecutive `//` lines.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: `"..."` and `'...'` are Cairo tokens. `%{`
  through `%}` is one `HINT` token with embedded Python; `//` inside that body
  is not a Cairo Zero comment and Python `//` is floor division.
- Conflicts with strings, operators, directives, or embedded languages:
  URLs or `//` in strings, Python floor division in hints, and the Cairo `/`
  operator are not comments.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve comment payload and do not strip
  Python hint code or literal contents.

### Evidence

- Official documentation permalink:
  [Cairo Zero tutorial example](https://docs.cairo-lang.org/cairozero/hello_cairo/puzzle.html)
- Documentation version and relevant section: archived Cairo Zero tutorial;
  repeatedly shows full-line and inline `//` comments.
- Official implementation or grammar permalink:
  [Cairo Zero grammar](https://github.com/starkware-libs/cairo-lang/blob/cf9bf972bede402a125e8638bb258e77563ae933/src/starkware/cairo/lang/compiler/cairo.ebnf#L1-L10)
- Implementation version, file, and relevant symbol: Cairo Zero `0.14.3`,
  `cairo.ebnf`; `HINT`, `STRING`, `SHORT_STRING`, `COMMENT`, `code_block`, and
  `notes` define the relevant lexer modes and placement.
- Conformance test or official example permalink:
  [comment grammar rules](https://github.com/starkware-libs/cairo-lang/blob/cf9bf972bede402a125e8638bb258e77563ae933/src/starkware/cairo/lang/compiler/cairo.ebnf#L141-L183)
- Secondary source, if needed:
  [official Cairo/Cairo Zero distinction](https://www.cairo-lang.org/about-cairo/)
- Evidence conflicts or gaps: no syntax conflict. The existing registry's
  `cairo` alias has no Cairo Zero hint exclusion, so a bare alias would expose a
  known false-positive boundary.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official Lark grammar and parser source inspection;
  no local Cairo Zero environment was installed.
- Exact version or commit: Cairo Zero `0.14.3`,
  `cf9bf972bede402a125e8638bb258e77563ae933`
- Probe method: compared longest `HINT`/literal tokens with `COMMENT` placement
  and inspected `parse_file` EOF-newline normalization.
- Probe input:

```text
tempvar x = 1; // Cairo comment
%{
y = 8 // 2
%}
```

- Observed result: the first `//` is a `COMMENT`; the second is contained by the
  single `HINT` token.
- Conclusion and limits of the probe: proves the embedded-hint boundary from
  grammar; malformed hints require explicit implementation recovery tests.

### Representative examples

#### Line comment

```text
tempvar row = loc.row; // cache the row
```

#### Block comment

Unsupported.

#### Nested or contextual comment

```text
%{
value = ids // 2
%}
// Cairo comment after the hint
```

### Adversarial boundaries

- Negative cases: `"https://host/a//b"`, `'a//b'`, division `/`, and Python
  floor division or URLs inside `%{ ... %}`.
- Malformed-input cases: unclosed `%{` hint, unterminated string before `//`,
  empty comment at EOF, and `%}` without an opener.
- Line-ending and Unicode cases: LF, CRLF, EOF without newline, Unicode payload,
  and accurate byte offsets around non-ASCII literal content.
- Version or dialect counterexamples: modern Cairo uses separate compiler
  semantics; Python comments inside hints are embedded-language content and not
  Cairo Zero comments.
- Cleaner preservation cases: hint bodies, URL strings, `//` in short strings,
  adjacent comments, and inline comment indentation.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add a distinct `cairo_zero` entry with the same
  line wrapper as `cairo`, but bind it to a helper that skips strings, short
  strings, and `%{ ... %}` hints. Do not use an unguarded alias.
- Deterministic tests to add: raw-label lookup, inline/full-line comments,
  strings, short strings, hints with floor division, malformed hints/literals,
  EOF normalization, CRLF, grouping, and sanitizer preservation.
- Remaining blocker: none. An unclosed `%{` hint conservatively protects the
  remainder from Cairo comment extraction; an unterminated string or short
  string follows the same no-fallback rule.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Carbon

### Identity and scope

- Raw dataset label: `Carbon` (21,257 files; 117,050,687 tokens)
- Proposed registry key: `carbon`
- Existing family or aliases checked: `slash_line_style` accepts every `//`
  sequence, while Carbon requires whitespace or EOF after the introducer. C-like
  families incorrectly add block comments. No `carbon` collision exists.
- Classification: `language`
- Versions or releases checked: Carbon language and toolchain commit
  `46b5482bb4723a51b9f6870f4644d7de6af29f07`; proposal 7441 trailing-comment
  behavior included.
- Dialects checked: current experimental Carbon. Earlier proposal 198 behavior
  that prohibited trailing comments has been superseded.
- Intended support scope: valid current Carbon line comments.
- Explicitly excluded scope: C/C++ source in interop files, proposal Markdown,
  `/* ... */`, and reserved/diagnosed no-whitespace comment introducers.

### Syntax contract

- Line comments: `//` through end of physical line, but the next character must
  be ASCII space, tab, LF, or EOF in the pinned lexer. Current Carbon permits
  both full-line and trailing comments.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: newline or EOF. A trailing
  backslash does not continue the comment.
- Inline use: valid after other source content, with or without whitespace
  before `//`, provided the character after `//` satisfies the whitespace/EOF
  rule.
- Adjacent-line grouping: valid for consecutive valid line comments.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: ordinary, raw, and multiline string/character
  literals own their contents. The toolchain diagnoses `//abc` as missing
  whitespace and consumes it for recovery, but it is not valid source-comment
  syntax.
- Conflicts with strings, operators, directives, or embedded languages:
  `/` is division; `/* ... */` is not a Carbon comment; `//identifier` is a
  diagnosed reserved introducer; `//` inside literals is data.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve payload and do not join the next
  physical line when a comment ends in backslash.

### Evidence

- Official documentation permalink:
  [Carbon comments design](https://github.com/carbon-language/carbon-lang/blob/46b5482bb4723a51b9f6870f4644d7de6af29f07/docs/design/lexical_conventions/comments.md)
- Documentation version and relevant section: current design, "Overview" and
  "Details"; defines whitespace after `//`, trailing comments, no physical line
  continuation, and no block comments.
- Official implementation or grammar permalink:
  [Carbon lexer](https://github.com/carbon-language/carbon-lang/blob/46b5482bb4723a51b9f6870f4644d7de6af29f07/toolchain/lex/lex.cpp)
- Implementation version, file, and relevant symbol: pinned toolchain,
  `Lexer::LexCommentOrSlash` and `Lexer::LexComment`.
- Whitespace implementation permalink:
  [Carbon lexical character sets](https://github.com/carbon-language/carbon-lang/blob/46b5482bb4723a51b9f6870f4644d7de6af29f07/toolchain/lex/character_set.h#L34-L53)
- Conformance test or official example permalink:
  [trailing-comment tests](https://github.com/carbon-language/carbon-lang/blob/46b5482bb4723a51b9f6870f4644d7de6af29f07/toolchain/lex/testdata/trailing_comments.carbon)
- Secondary source, if needed:
  [bad introducer tests](https://github.com/carbon-language/carbon-lang/blob/46b5482bb4723a51b9f6870f4644d7de6af29f07/toolchain/lex/testdata/fail_bad_comment_introducers.carbon)
- Evidence conflicts or gaps: proposal 198 originally prohibited trailing
  comments, but accepted proposal 7441, the current design page, lexer, and
  tests all permit them. Invalid `//abc` is consumed as recovery after a
  diagnostic; this report treats it as malformed, not accepted comment syntax.
  The design calls newline whitespace, but the pinned `IsSpace` accepts only
  space, tab, and LF, so a bare `//` immediately before CRLF is conservatively
  excluded while ordinary `// text\r\n` remains supported.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned lexer and conformance-test inspection; the
  Carbon toolchain was not built locally.
- Exact version or commit: `46b5482bb4723a51b9f6870f4644d7de6af29f07`
- Probe method: compared valid trailing-comment tests with diagnostic fixtures
  for missing post-introducer whitespace.
- Probe input:

```text
var x: i32 = 1;// valid trailing comment
// valid
//invalid
```

- Observed result: the first two are comments; the third is consumed only with
  `NoWhitespaceAfterCommentIntroducer` diagnostic.
- Conclusion and limits of the probe: current accepted syntax is unambiguous;
  runtime testing is still needed for raw/multiline literal negatives.

### Representative examples

#### Line comment

```text
var count: i32 = 1; // number of entries
```

#### Block comment

Unsupported.

#### Nested or contextual comment

```text
// This line ends here. \
var still_code: i32 = 2;
```

### Adversarial boundaries

- Negative cases: `//invalid`, `/* not a comment */`, division, ordinary/raw/
  multiline literals containing `//`, and a C++ interop file.
- Malformed-input cases: `//invalid` at EOF, unterminated string before `//`,
  isolated `/`, and a backslash as the last payload character.
- Line-ending and Unicode cases: LF, `// text` with CRLF, EOF immediately after
  `//`, a bare `//` before CRLF as a negative case, non-ASCII whitespace after
  `//` as a negative case, and Unicode payloads after a proven ASCII separator.
- Version or dialect counterexamples: pre-7441 Carbon rejected trailing
  comments; current support is commit-scoped and should not add C++ block
  syntax.
- Cleaner preservation cases: trailing backslash, reserved `//identifier`,
  URLs/literals, adjacent comments, and exact whitespace after the wrapper.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: create canonical `carbon` with a line pattern that
  requires whitespace/newline/EOF immediately after `//`, no block delimiter,
  and current trailing-comment compatibility.
- Deterministic tests to add: full-line/trailing comments, no-space before the
  introducer, required space after it, empty `//` at newline/EOF, invalid
  `//identifier`, strings/raw strings, division, block-comment negative,
  backslash termination, CRLF, grouping, and sanitizer preservation.
- Remaining blocker: none. The pinned `character_set.h` proves that the accepted
  post-introducer set is ASCII space, tab, LF, or EOF; do not expand it to
  Unicode whitespace.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01
