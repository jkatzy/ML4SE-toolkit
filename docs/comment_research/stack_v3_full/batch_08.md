# Stack v3 Full Comment Research: batch 08

## Dataset provenance

- Dataset/project: HuggingFaceCode/stack-v3-full
- Statistics repository: HuggingFaceCode/stack-v3-train
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics table, aggregated
  from `files[].language`
- Researcher or agent: `/root/research_batch_08`
- Review status: `reviewed`

Identity was checked against GitHub Linguist at commit
`af6f772786199696e4d07d618c9c5b625a1a03f0`. Linguist is used only to bind
the Stack labels to language identities and aliases, never as syntax evidence.

## Pyret

### Identity and scope

- Raw dataset label: `Pyret` (22,723 files; 84,197,089 tokens)
- Proposed registry key: `pyret`
- Existing family or aliases checked: generic hash-line and nested-block
  families. Neither combines Pyret's `#` line marker with nested `#| ... |#`.
- Classification: `language`
- Versions or releases checked: current Pyret documentation and
  `brownplt/pyret-lang` commit
  `817b85eba62ef35d345c10fb02c9f7add94f1e54`.
- Dialects checked: ordinary Pyret source accepted by the JavaScript tokenizer.
- Intended support scope: source comments tokenized by current Pyret, including
  nested block comments and comments used inline between expressions.
- Explicitly excluded scope: documentation strings, strings containing marker
  text, and reader/compiler output that is not Pyret source.

### Syntax contract

- Line comments: `#` through the end of the physical line, except when the same
  bytes begin the longer `#|` block opener.
- Block comments: `#|` opens and `|#` closes a block comment.
- Nested comments: supported; each `#|` inside block-comment text increases the
  depth and each `|#` decreases it.
- Termination at newline, delimiter, or EOF: line comments stop before CR, LF,
  or EOF. Blocks stop at the matching depth-zero `|#`; newlines are body text.
- Inline use: valid for both line and block comments.
- Adjacent-line grouping: valid for consecutive full-line `#` comments. Block
  comments are returned as their own exact regions.
- Unclosed delimiter behavior: an unclosed block is invalid and must not be
  silently accepted as a complete comment. A line comment may terminate at EOF.
- Lexical or structural context: strings outside comments protect `#`, `#|`,
  and `|#`. Once a block comment starts, quote-looking text has no shielding
  role; only nested block delimiters affect depth.
- Conflicts with strings, operators, directives, or embedded languages: match
  the longest opener first so `#|` is not consumed as a line comment. Marker
  text inside a Pyret string is not a comment.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: `("#|", "|#")`.
- Content-preservation expectations: remove only verified outer scaffolding,
  retain nested-comment payload and delimiters as content, normalize line
  endings only under the existing cleaner contract, and preserve Unicode.

### Evidence

- Official documentation permalink:
  [Pyret comments documentation](https://pyret.org/docs/latest/s_comments.html)
- Documentation version and relevant section: current language reference,
  "Comments"; it specifies `#`, `#| ... |#`, inline use, and nesting.
- Official implementation or grammar permalink:
  [Pyret tokenizer comment actions](https://github.com/brownplt/pyret-lang/blob/817b85eba62ef35d345c10fb02c9f7add94f1e54/src/js/base/pyret-tokenizer.js#L524-L563)
- Implementation version, file, and relevant symbol: commit above,
  `src/js/base/pyret-tokenizer.js`; `#|` depth loop and `#` line loop.
- Conformance test or official example permalink:
  [official parser examples containing comments](https://github.com/brownplt/pyret-lang/tree/817b85eba62ef35d345c10fb02c9f7add94f1e54/tests/parse)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the moving documentation page is corroborated by
  the pinned official tokenizer. No syntax conflict was found.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned tokenizer source was traced; the full compiler
  was not built.
- Exact version or commit: `817b85eba62ef35d345c10fb02c9f7add94f1e54`
- Probe method: followed the line loop's CR/LF/EOF exits and the block loop's
  depth transitions and unterminated-token branch.
- Probe input:

~~~text
fun f(x):
  # ordinary
  x + #| outer #| inner |# tail |# 1
end
~~~

- Observed result: the line region ends before LF; the block region is one
  token extending through the second `|#`.
- Conclusion and limits of the probe: source establishes delimiter precedence,
  nesting, and EOF behavior. Runtime position accounting still needs tests.

### Representative examples

#### Line comment

~~~text
fun area(w, h):
  # dimensions are positive
  rectangle(w, h)
end
~~~

Expected region: `# dimensions are positive`.

#### Block comment

~~~text
rectangle(width #| measured in pixels |#, height)
~~~

Expected region: `#| measured in pixels |#`.

#### Nested or contextual comment

~~~text
#| outside
   #| nested |#
   outside again
|#
~~~

Expected region: the entire outer comment, including the nested delimiters.

### Adversarial boundaries

- Negative cases: markers in single- and double-quoted strings, a bare `|#`,
  `#` immediately followed by `|`, and comment-looking text after a protected
  string escape.
- Malformed-input cases: unclosed outer block, unclosed nested block, opener at
  EOF, and a close delimiter missing its final `#`.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF line comment, Unicode
  payload, and exact source offsets around multibyte text.
- Version or dialect counterexamples: do not import Python triple-quoted-string
  behavior or another hash language's block syntax.
- Cleaner preservation cases: empty comments, nested delimiters, leading `|` or
  trailing `#` in payload, indentation, and multiple consecutive hash marks.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: add canonical `pyret`, `#` line syntax, nested
  `#|`/`|#` metadata, both sanitizer wrappers, pinned evidence, and seeds for
  line, inline block, and nested block forms.
- Deterministic tests to add: raw-label lookup, longest-opener precedence,
  inline and grouped line comments, nested blocks, string shielding, all EOF
  and line-ending cases, exact `QueryMatch` slices, and sanitizer parity.
- Remaining blocker: none for implementation; the Pyret nested matcher must
  treat quote-looking bytes inside comment bodies as ordinary text.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Rez

### Identity and scope

- Raw dataset label: `Rez` (39,483 files; 543,266,215 tokens)
- Proposed registry key: `rez`
- Existing family or aliases checked: the non-nested C-style family. Its
  delimiters match contemporary Apple Rez source, but its physical-line regex
  does not model the preprocessor's logical-line splicing.
- Classification: `language`
- Versions or releases checked: Apple Macintosh Programmer's Workshop 2.0
  reference (1987), Apple A/UX 3.0 Toolbox/ROM Interface (1992), and Retro68
  commit `f99ecb5aeb6fbb004c647518ea760daba2b1f6bb`.
- Dialects checked: Apple's resource compiler language and the source-compatible
  Retro68 implementation.
- Intended support scope: contemporary Apple Rez resource-description source,
  including preprocessor input.
- Explicitly excluded scope: the unrelated Rez interactive-fiction language,
  generated resource data, and Lisa Workshop RMAKER source.

### Syntax contract

- Line comments: `//` through physical line end or EOF in the contemporary
  language and implementations.
- Block comments: `/*` through the first following `*/`.
- Nested comments: unsupported; an inner `/*` does not add depth.
- Termination at newline, delimiter, or EOF: line comments stop before CR/LF or
  EOF. Block comments require `*/`; newlines are part of their body.
- Inline use: valid for both forms.
- Adjacent-line grouping: valid for consecutive full-line `//` comments. Block
  regions remain individually delimited.
- Unclosed delimiter behavior: an unclosed block is malformed and must not be
  reported as a verified complete block. A line comment may end at EOF.
- Lexical or structural context: quoted strings and character-like constants
  shield comment markers. Rez is preprocessed; backslash-newline splicing and
  directive lines must be exercised against the chosen preprocessor semantics.
- Conflicts with strings, operators, directives, or embedded languages: slash
  operators and path-like string text are not comments. Resource payload bytes
  and preprocessor macro text must retain exact offsets.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: strip only verified wrappers, retain stars
  in formatted blocks and all payload, and never reinterpret resource literals.

### Evidence

- Official documentation permalink:
  [Apple MPW 2.0 Reference PDF](https://ftpmirror.your.org/pub/misc/bitsavers/pdf/apple/mac/developer/MPW_2.0_Reference_1987.pdf)
- Documentation version and relevant section: MPW 2.0 Rez reference, lexical
  conventions and C-like preprocessing; the downloaded PDF SHA-256 was
  `b0120854732427e61edd526cbea11dd0f2502e1beb08f1a928e4d0bad5be34c9`.
- Official implementation or grammar permalink:
  [Retro68 Rez lexer and preprocessor setup](https://github.com/autc04/Retro68/blob/f99ecb5aeb6fbb004c647518ea760daba2b1f6bb/Rez/RezLexer.cc#L71-L89)
- Implementation version, file, and relevant symbol: Retro68 commit above,
  `Rez/RezLexer.cc`; Boost Wave C/C++ preprocessing token stream.
- Conformance test or official example permalink:
  [Retro68 Rez source using both comment forms](https://github.com/autc04/Retro68/blob/f99ecb5aeb6fbb004c647518ea760daba2b1f6bb/libretro/Retro68.r#L1-L10)
- Secondary source, if needed:
  [Apple A/UX 3.0 Toolbox Macintosh ROM Interface](https://bitsavers.computerhistory.org/pdf/apple/mac/a_ux/aux_3.0/AUX_3.0_AUX_Toolbox_Macintosh_ROM_Interface_1992.pdf)
- Evidence conflicts or gaps: the oldest MPW manual emphasizes C block comments;
  the A/UX reference and current source-compatible implementation establish
  C++-style line comments for the intended contemporary scope. Historic
  pre-A/UX source is not promised by this key.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: Retro68 source and examples were inspected; Apple's
  proprietary Rez executable was not run.
- Exact version or commit: `f99ecb5aeb6fbb004c647518ea760daba2b1f6bb`
- Probe method: traced the Rez lexer through the Boost Wave preprocessor and
  inspected repository `.r` inputs containing trailing and block comments.
- Probe input:

~~~text
#define ID 128 // resource identifier
resource 'STR ' (ID) { "http://example.invalid" }; /* label */
~~~

- Observed result: the implementation uses C/C++ preprocessing comment tokens;
  the URL remains inside a string while both exterior regions are comments.
- Conclusion and limits of the probe: confirms the contemporary forms and
  string boundary. Backslash-newline cases require explicit regression tests.

### Representative examples

#### Line comment

~~~text
resource 'STR ' (128) { "Ready" }; // status text
~~~

Expected region: `// status text`.

#### Block comment

~~~text
/* Shared resource IDs */
#define kStatusString 128
~~~

Expected region: `/* Shared resource IDs */`.

#### Nested or contextual comment

~~~text
resource 'STR ' (128) { "https://host/path//name" }; // real comment
~~~

Expected region: only `// real comment`.

### Adversarial boundaries

- Negative cases: URLs and `/*` text inside strings, slash operators, a lone
  slash, character constants, macro replacement text, and the unrelated Rez
  language's `%%` marker.
- Malformed-input cases: unclosed string, unclosed block, stray `*/`, directive
  ending in backslash, and a block opener split around a line splice.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF line comment, Unicode
  payload, and classic Mac source conversion as an explicit compatibility test.
- Version or dialect counterexamples: MPW-era documentation and RMAKER syntax
  must not be silently broadened; scope aliases only to Apple Rez.
- Cleaner preservation cases: star-decorated blocks, preprocessor text, empty
  comments, resource type literals, and exact whitespace around wrappers.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `rez` with the C-style `//` and non-nested
  `/* ... */` delimiters plus Rez/Boost-Wave-aware string, character, and
  escaped-line-break handling; do not attach unrelated language aliases.
- Deterministic tests to add: raw-label lookup, both forms, strings and resource
  literals, non-nesting, unclosed blocks, EOF lines, preprocessor directives and
  splices, all line endings, exact slices, and sanitizer parity.
- Remaining blocker: none for the contemporary scope; do not broaden the
  shared C-style family because several of its other aliases do not splice
  physical lines before comment recognition.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Roc

### Identity and scope

- Raw dataset label: `Roc` (18,556 files; 56,996,741 tokens)
- Proposed registry key: `roc`
- Existing family or aliases checked: the pure hash-line family and Python-like
  hash family. Roc matches the pure line delimiter but needs Roc-tokenizer
  shielding for multiline strings and interpolation; it must not inherit
  triple-quoted pseudo-comments.
- Classification: `language`
- Versions or releases checked: current language reference and `roc-lang/roc`
  commit `a892c9f42c528ba13c1ac9e61cc4c3226f1be918`.
- Dialects checked: ordinary Roc modules, application headers, shebangs, and Roc
  documentation comments.
- Intended support scope: all line comments recognized by the current Roc
  tokenizer, including doc comments as a semantic subset.
- Explicitly excluded scope: Markdown generated from docs, string literals, and
  any inferred multiline comment form.

### Syntax contract

- Line comments: `#` through CR, LF, or EOF.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: the tokenizer stops before CR/LF;
  EOF closes the line comment.
- Inline use: valid.
- Adjacent-line grouping: valid for consecutive full-line comments. Consecutive
  beginning-of-line `## ` comments may also form one documentation unit.
- Unclosed delimiter behavior: not applicable; line comments may end at EOF.
- Lexical or structural context: Roc strings and character literals shield
  marker bytes. `#!` at file start is treated as an ordinary comment, not a
  separate extraction syntax.
- Conflicts with strings, operators, directives, or embedded languages: `## `
  at the beginning of consecutive lines has documentation semantics only when
  followed by an assignment; it remains a hash comment lexically. Do not treat
  triple-quoted text as a comment.
- Sanitizer line wrappers: `("#", "")`; documentation lines are the same form.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve one additional leading hash in
  doc-comment content, shebang payload, indentation, and Unicode.

### Evidence

- Official documentation permalink:
  [Roc comments and documentation comments](https://github.com/roc-lang/roc/blob/a892c9f42c528ba13c1ac9e61cc4c3226f1be918/docs/langref/comments-and-docs.md#L1-L41)
- Documentation version and relevant section: commit above, complete comments
  chapter; it states that all comments start with `#`, no multiline form exists,
  inline use is valid, and `#!` is an ordinary comment.
- Official implementation or grammar permalink:
  [Roc tokenizer hash-comment loop](https://github.com/roc-lang/roc/blob/a892c9f42c528ba13c1ac9e61cc4c3226f1be918/src/parse/tokenize.zig#L757-L785)
- Implementation version, file, and relevant symbol: commit above,
  `src/parse/tokenize.zig`; comment trivia scanning through CR/LF/EOF.
- Conformance test or official example permalink:
  [official language-reference examples](https://github.com/roc-lang/roc/tree/a892c9f42c528ba13c1ac9e61cc4c3226f1be918/examples)
- Secondary source, if needed: none.
- Additional official lexical evidence:
  [Roc string forms](https://github.com/roc-lang/roc/blob/a892c9f42c528ba13c1ac9e61cc4c3226f1be918/docs/langref/strings.md).
- Evidence conflicts or gaps: none affecting extraction. Documentation-comment
  attachment is semantic and does not require a distinct delimiter contract.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned tokenizer source trace; the Roc compiler was
  not built.
- Exact version or commit: `a892c9f42c528ba13c1ac9e61cc4c3226f1be918`
- Probe method: followed the tokenizer's hash branch through CR, LF, and EOF and
  compared it with the official shebang and doc-comment statements.
- Probe input:

~~~text
#! /usr/bin/env roc
# module note
answer = "# not a comment" # inline
~~~

- Observed result: the first, second, and final hash regions are trivia; the
  hash inside the string is not.
- Conclusion and limits of the probe: confirms the pure hash-line contract;
  documentation attachment itself is outside extraction.

### Representative examples

#### Line comment

~~~text
answer = 42 # chosen value
~~~

Expected region: `# chosen value`.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
#! /usr/bin/env roc
message = "# literal"
# actual comment
~~~

Expected regions: the shebang line and final comment, not the string content.

### Adversarial boundaries

- Negative cases: hash in strings and character literals, repeated hashes in
  ordinary code, Python triple-quoted text, and a Unicode number sign.
- Malformed-input cases: unterminated string before a hash, escape at line end,
  bare hash, shebang without final newline, and hash at EOF.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF, Unicode payload and
  identifiers, and exact offsets after multibyte strings.
- Version or dialect counterexamples: no block form should be imported from
  Pyret or another hash language; `##` remains a line-comment subset.
- Cleaner preservation cases: shebang payload, second hash in documentation
  content, empty `#`, indentation, and adjacent documentation lines.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `roc` with the pure hash-line delimiter and a
  Roc-tokenizer-compatible masker for quoted, multiline, character, and
  interpolated string regions; explicitly avoid pseudo-comment extraction from
  any string form.
- Deterministic tests to add: raw-label lookup, inline/full-line/doc/shebang
  forms, strings, EOF and every line ending, grouping, Unicode offsets, absence
  of block syntax, and sanitizer preservation.
- Remaining blocker: none; the helper must follow the pinned Roc tokenizer
  rather than the shared single-line quote heuristic.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Rocq Prover

### Identity and scope

- Raw dataset label: `Rocq Prover` (587,060 files; 13,038,001,596 tokens)
- Proposed registry key: `rocq_prover`, aliasing canonical `coq`; also accept
  the official short name `rocq`.
- Existing family or aliases checked: the Coq/Rocq nested `(* ... *)` family.
  The mapping exists in the development registry, but its matcher must be
  checked for quoted spans inside comment bodies.
- Classification: `language`
- Versions or releases checked: Rocq official repository commit
  `d3971a897c7e578afd920eac4c1fcbb666c67ead` and Linguist's Coq-to-Rocq rename.
- Dialects checked: Rocq/Coq vernacular source handled by the official lexer.
- Intended support scope: the shared current and historic Coq/Rocq comment
  contract under one canonical family.
- Explicitly excluded scope: OCaml host/build files, generated documentation,
  and strings outside comments.

### Syntax contract

- Line comments: unsupported.
- Block comments: `(*` opens and `*)` closes.
- Nested comments: supported recursively.
- Termination at newline, delimiter, or EOF: comments may span lines and end at
  the matching depth-zero `*)`; EOF before that is a lexer error.
- Inline use: valid between vernacular tokens.
- Adjacent-line grouping: not a line-comment concept; each outer block is an
  exact independently delimited region.
- Unclosed delimiter behavior: invalid and not a complete verified comment.
- Lexical or structural context: strings outside comments protect delimiters.
  Inside a comment, the Rocq lexer recognizes double-quoted spans specially, so
  `(*` or `*)` occurring within such a quoted span does not alter comment depth.
- Conflicts with strings, operators, directives, or embedded languages: a
  generic nested-delimiter counter that ignores quote handling will close too
  early on `"*)"` in comment text. Apostrophes in identifiers are not quotes.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: `("(*", "*)")`.
- Content-preservation expectations: remove only the outer wrapper, preserve
  nested delimiters and quoted comment payload exactly, and retain doc-comment
  decoration as content.

### Evidence

- Official documentation permalink:
  [Rocq reference manual lexical conventions](https://rocq-prover.org/doc/V8.20.0/refman/language/core/basic.html#lexical-conventions)
- Documentation version and relevant section: Rocq/Coq 8.20 reference, lexical
  conventions; comments are nested `(* ... *)` regions.
- Official implementation or grammar permalink:
  [Rocq lexer comment rule](https://github.com/rocq-prover/rocq/blob/d3971a897c7e578afd920eac4c1fcbb666c67ead/parsing/cLexer.ml#L402-L436)
  and
  [quoted-span scanner](https://github.com/rocq-prover/rocq/blob/d3971a897c7e578afd920eac4c1fcbb666c67ead/parsing/cLexer.ml#L312-L365).
- Implementation version, file, and relevant symbol: commit above,
  `parsing/cLexer.ml`; recursive `comment`, `string` with
  `comm_level = Some 0`, doubled-double-quote escaping, multiline quoted spans,
  and EOF errors.
- Conformance test or official example permalink:
  [Rocq test-suite sources](https://github.com/rocq-prover/rocq/tree/d3971a897c7e578afd920eac4c1fcbb666c67ead/test-suite)
- Secondary source, if needed:
  [Linguist Rocq rename commit](https://github.com/github-linguist/linguist/commit/4b9ec2834bd069758bb2ec766997bb2070fe61d2)
- Evidence conflicts or gaps: no delimiter conflict was found. The current
  registry's nominal alias does not by itself prove quoted-delimiter handling.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned official lexer source trace; Rocq was not
  compiled locally.
- Exact version or commit: `d3971a897c7e578afd920eac4c1fcbb666c67ead`
- Probe method: followed recursive entry/exit branches and the distinct quoted
  span branch inside the comment scanner.
- Probe input:

~~~text
Definition x := 1. (* outer "*)" still outer (* nested *) done *)
~~~

- Observed result: the close-looking bytes in quotes do not end the comment;
  the nested pair changes depth, and the final close ends the outer region.
- Conclusion and limits of the probe: proves the behavior a plain depth counter
  would miss. Exact escaped/doubled-quote handling needs regression fixtures.

### Representative examples

#### Line comment

Unsupported.

#### Block comment

~~~text
Definition zero := 0. (* a natural number *)
~~~

Expected region: `(* a natural number *)`.

#### Nested or contextual comment

~~~text
(* outer "*) is text" (* nested *) tail *)
~~~

Expected region: the complete outer block through the final `*)`.

The doubled-quote boundary must also remain inside the same outer comment:

~~~text
(* outer "quoted "" *) still quoted" tail *)
~~~

Expected region: the complete source through the final `*)`; the earlier
close-looking bytes occur inside the quoted span.

### Adversarial boundaries

- Negative cases: delimiters in Rocq strings outside comments, apostrophes in
  identifiers, a bare `*)`, parenthesized multiplication-like tokens, and OCaml
  source routed under a different label.
- Malformed-input cases: unclosed outer and nested blocks, unclosed quoted span
  inside a comment, stray close, and opener at EOF.
- Line-ending and Unicode cases: LF, CRLF, lone CR within blocks, Unicode proof
  text, and exact offsets after multibyte identifiers.
- Version or dialect counterexamples: old `Coq`, new `Rocq Prover`, and `Rocq`
  labels share the same contract; the rename must not create a new syntax.
- Cleaner preservation cases: nested delimiters, quoted close-looking text,
  documentation decoration, blank blocks, leading stars, and indentation.

### Decision

- Recommended action: `alias`
- Registry fields to change: ensure raw `rocq_prover` and `rocq` resolve to the
  canonical Coq/Rocq nested-star family; give that family alone a focused
  matcher so doubled-quote-aware quoted spans inside comments follow `cLexer`.
  Do not apply this shielding to Pyret, RON, Sail, Rust, or other nested
  families where quote-looking bytes are ordinary comment payload.
- Deterministic tests to add: all three label mappings, ordinary/inline/nested
  blocks, quoted open and close text inside comments, doubled quotes,
  multiline quoted spans, strings outside, unclosed forms, Unicode and line
  endings, exact slices, and sanitizer parity; run the same quote-looking
  payload against Pyret/RON/Sail/Rust to prove their nesting is unchanged.
- Remaining blocker: the mapping is ready, but promotion requires the quoted
  delimiter regression to pass against the Coq/Rocq family without changing
  any other nested family.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## QuickBASIC

### Identity and scope

- Raw dataset label: `QuickBASIC` (64,803 files; 401,614,697 tokens)
- Proposed registry key: `quickbasic`
- Existing family or aliases checked: the Visual Basic apostrophe/`Rem` family
  and normalized aliases `qb`, `qbasic`, `qb64`, and `classic_qbasic`. The
  delimiter family alone cannot enforce QuickBASIC's `DATA` rule.
- Classification: `language`
- Versions or releases checked: Microsoft QuickBASIC 4.5 Language Reference
  and current QB64 documentation for the shared modern-compatible subset.
- Dialects checked: Microsoft QuickBASIC/QBasic and QB64, which Linguist groups
  under this label.
- Intended support scope: the documented common comment forms, with classic
  `DATA` statement handling and case-insensitive `REM` statement recognition.
- Explicitly excluded scope: GW-BASIC-only behavior, Visual Basic block/XML
  documentation forms, and arbitrary apostrophes inside `DATA` payloads.

### Syntax contract

- Line comments: an apostrophe `'` outside a string starts a comment through
  the line end, except that an apostrophe within the payload of a `DATA`
  statement is data. A case-insensitive `REM` statement also comments through
  the line end.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: both forms extend through the
  current program line and may terminate at EOF. Newline bytes are excluded.
- Inline use: apostrophe comments may immediately follow a statement. `REM`
  must occur where a statement may begin; after another colon-separated
  statement it is preceded by `:`.
- Adjacent-line grouping: consecutive comment-only apostrophe and `REM` lines
  may be grouped while retaining their individual source regions.
- Unclosed delimiter behavior: not applicable; both forms are line comments.
- Lexical or structural context: double-quoted BASIC strings shield apostrophes
  and `REM`. Optional line numbers precede a statement. A `DATA` statement
  protects apostrophes until its statement-ending colon; after that colon a new
  apostrophe or `REM` can start a comment.
- Conflicts with strings, operators, directives, or embedded languages:
  identifiers such as `Reminder` are not `REM`; token boundaries and statement
  position are mandatory. Compiler metacommands such as apostrophe-`$INCLUDE`
  use comment scaffolding but carry directive content.
- Sanitizer line wrappers: `("'", "")` and case-insensitive `("REM", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve all remark text, especially a
  leading `$` metacommand payload. Never remove an apostrophe from a `DATA`
  field or a quoted string.

### Evidence

- Official documentation permalink:
  [Microsoft QuickBASIC 4.5 Language Reference transcript](https://www.pcjs.org/documents/books/mspl13/basic/qblang/)
- Documentation version and relevant section: Microsoft QuickBASIC 4.5,
  "Comments" and `REM` statement entries; apostrophe and `REM` run to line end,
  and `REM` following another statement requires a colon.
- Official implementation or grammar permalink: no redistributable Microsoft
  lexer source was found; the primary Microsoft language reference is the
  normative source for the classic dialect.
- Implementation version, file, and relevant symbol: QuickBASIC 4.5 reference,
  `REM Statement` and `DATA Statement` lexical notes.
- Conformance test or official example permalink:
  [QB64 apostrophe documentation and examples](https://qb64.com/wiki/Apostrophe.html)
- Secondary source, if needed:
  [QB64 REM documentation](https://qb64.com/wiki/REM.html)
- Evidence conflicts or gaps: QB64 documents the shared forms but its current
  parser is not the authority for every historic QuickBASIC edge. The report
  establishes the cross-checked delimiters and classic `DATA` exception, but
  does not yet establish every grammar position where `REM` begins a statement.
- Confidence: `provisional`

### Implementation confirmation

- Implementation tested: documentation-level confirmation; no proprietary
  QuickBASIC executable was used.
- Exact version or commit: Microsoft QuickBASIC 4.5 reference; current QB64
  documentation retrieved 2026-08-01.
- Probe method: compared Microsoft statement rules with QB64 examples and
  isolated the `DATA`/apostrophe distinction that a generic VB matcher misses.
- Probe input:

~~~text
10 DATA O'BRIEN,42: ' comment after DATA
20 PRINT "REM isn't a comment": REM actual comment
~~~

- Observed result: the first apostrophe is data, the apostrophe after `:` is a
  comment, the quoted text is protected, and the final `REM` is a statement.
- Conclusion and limits of the probe: establishes the required contextual
  cases. Additional dialect-specific statement positions need adversarial
  compiler fixtures before aliases beyond the checked label set are added.

### Representative examples

#### Line comment

~~~text
10 PRINT "READY" ' display a prompt
20 REM Wait for input
~~~

Expected regions: `' display a prompt` and `REM Wait for input`.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
10 DATA O'BRIEN,42: PRINT "loaded" ' trailing remark
20 PRINT "REM and ' are text": REM actual remark
~~~

Expected regions: only `' trailing remark` and `REM actual remark`.

### Adversarial boundaries

- Negative cases: apostrophe in `DATA`, both markers in strings, `Reminder` and
  `REMARK` identifiers, `XREM`, an apostrophe-like Unicode character, and `REM`
  after an expression where no statement can begin.
- Malformed-input cases: unterminated string, incomplete `DATA`, repeated
  colons, line number without a statement, and a `REM` token at EOF.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF comments, mixed-case
  `rEm`, Unicode payload, and source offsets after non-ASCII string text.
- Version or dialect counterexamples: Visual Basic .NET XML documentation and
  GW-BASIC extensions are outside this key. Verify any `THEN REM`/`ELSE REM`
  dialect behavior before teaching the helper extra statement boundaries.
- Cleaner preservation cases: `$INCLUDE` and other metacommand payloads, bare
  apostrophe, bare `REM`, indentation, line numbers, and colons before comments.

### Decision

- Recommended action: `defer`
- Registry fields to change: none until all valid `REM` statement positions
  are pinned; the eventual `quickbasic` helper needs apostrophe and `REM`
  wrappers plus a BASIC statement scanner that shields strings and `DATA`
  fields.
- Deterministic tests to add: raw-label/alias lookup, case-insensitive `REM`,
  line numbers, colon-separated statements, all `DATA` cases, strings,
  metacommands, grouping, line endings, malformed input, and cleaner parity.
- Remaining blocker: pin an executable QuickBASIC-compatible compiler or
  official grammar fixture for statement positions such as single-line
  `IF ... THEN REM` and `ELSE REM`. Implementing only line-start and
  colon-separated `REM` would leave a partial language contract.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## RBS

### Identity and scope

- Raw dataset label: `RBS` (140,495 files; 504,642,637 tokens)
- Proposed registry key: `rbs`
- Existing family or aliases checked: Ruby, generic hash-line, and inline-RBS
  helpers. RBS signature files have a hash line marker, but `%a` annotations can
  legally contain hash bytes and require language-specific shielding.
- Classification: `language`
- Versions or releases checked: `ruby/rbs` commit
  `7534c7e8a5f6c83bc28cc057cc4f84d881125c33`, version `4.1.2.dev.1`.
- Dialects checked: standalone `.rbs` signature files and, only as a negative
  boundary, RBS declarations embedded in Ruby source.
- Intended support scope: comments in standalone RBS signature source.
- Explicitly excluded scope: Ruby's `=begin`/`=end`, Ruby comments surrounding
  embedded signatures, and `--` tokens used by the separate inline-RBS lexer.

### Syntax contract

- Line comments: `#` through LF or EOF. The pinned lexer consumes CR as comment
  payload, including the CR of CRLF; it distinguishes a comment that is the
  first token on an LF-defined line from a trailing comment.
- Block comments: unsupported in standalone RBS.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: LF or EOF terminates the token.
  Lone CR does not terminate it, and CR immediately before LF is included in
  the token's raw range.
- Inline use: lexically and parser-valid after a declaration even though the
  syntax guide recommends comments on their own lines.
- Adjacent-line grouping: valid for consecutive full-line `#` comments; do not
  group a trailing declaration comment across source code.
- Unclosed delimiter behavior: not applicable; line comments may end at EOF.
- Lexical or structural context: single-, double-, and backtick-quoted tokens
  protect hash bytes. RBS annotation literals `%a{...}`, `%a(...)`, `%a[...]`,
  `%a|...|`, and `%a<...>` are lexed as whole annotations before the `#` rule,
  so a hash inside one is not a comment.
- Conflicts with strings, operators, directives, or embedded languages: `--`
  is produced by the shared lexer as `tINLINECOMMENT`, but only inline-RBS
  parser entry points consume it as descriptive text. It is not a standalone
  `.rbs` source-comment form. Do not inherit Ruby block comments.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove only a verified hash prefix and
  preserve payload. Annotation contents, quoted names, and inline-RBS markers
  must remain untouched.

### Evidence

- Official documentation permalink:
  [RBS syntax guide comment section](https://github.com/ruby/rbs/blob/7534c7e8a5f6c83bc28cc057cc4f84d881125c33/docs/syntax.md#L912-L924)
- Documentation version and relevant section: RBS `4.1.2.dev.1`, "Comments";
  it documents single-line hash comments and the own-line convention.
- Official implementation or grammar permalink:
  [RBS lexer rules](https://github.com/ruby/rbs/blob/7534c7e8a5f6c83bc28cc057cc4f84d881125c33/src/lexer.re#L19-L66)
- Implementation version, file, and relevant symbol: commit above,
  `src/lexer.re`; annotation, string, `tLINECOMMENT`, and `tCOMMENT` rules.
- Conformance test or official example permalink:
  [RBS parser comment tests](https://github.com/ruby/rbs/blob/7534c7e8a5f6c83bc28cc057cc4f84d881125c33/test/rbs/parser_test.rb#L1002-L1031)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: documentation presents own-line style while the
  lexer/parser tests prove trailing comments are also tokenized and skipped.
  This is a style-versus-validity distinction, not a syntax conflict.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned lexer and parser source trace; native extension
  was not rebuilt.
- Exact version or commit: `7534c7e8a5f6c83bc28cc057cc4f84d881125c33`
- Probe method: checked rule ordering and parser handling for full-line versus
  trailing tokens, then enumerated every `%a` delimiter accepted before `#`.
- Probe input:

~~~text
# API type
type path = %a{route#fragment} # trailing description
type label = "name#part"
~~~

- Observed result: the first and trailing hashes produce comment tokens; the
  hashes inside the annotation and string do not.
- Conclusion and limits of the probe: establishes the contextual exclusion.
  Escape and malformed-annotation recovery still require deterministic tests.

### Representative examples

#### Line comment

~~~text
# Public interface
class User
  def name: () -> String # display name
end
~~~

Expected regions: `# Public interface` and `# display name`.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
type Route = %a{path#fragment} # annotation metadata is protected
~~~

Expected region: only `# annotation metadata is protected`.

### Adversarial boundaries

- Negative cases: hash in all five `%a` annotation delimiters, quoted type or
  member names, backticks, standalone `--`, Ruby `=begin`, and a hash-like
  Unicode character.
- Malformed-input cases: unterminated annotation, escaped annotation closer,
  unterminated string, bare `%a`, comment at EOF, and hash immediately after an
  annotation closer.
- Line-ending and Unicode cases: LF, CRLF with CR retained in the raw token,
  lone CR continuing to EOF, EOF, Unicode identifiers and payload, and exact
  offsets after multibyte annotation text.
- Version or dialect counterexamples: inline RBS embedded in Ruby has separate
  `--` handling and host-language boundaries; it must not share this key.
- Cleaner preservation cases: multiple leading hashes, annotation payload,
  trailing comments after complex types, blank comment bodies, and indentation.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `rbs`, hash wrapper metadata, pinned
  evidence, seeds for full-line/trailing comments, and a helper that shields RBS
  strings and complete `%a` annotation tokens.
- Deterministic tests to add: raw-label lookup, first-token/trailing distinction,
  every annotation delimiter with hash payload, quoted names, `--` and Ruby
  negatives, malformed annotations, line endings, grouping, exact slices, and
  sanitizer preservation.
- Remaining blocker: none for valid source. On malformed input, conservatively
  shield from an unterminated `%a` annotation opener through LF or EOF so a
  hash in its incomplete payload is not promoted to a verified comment.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## RON

### Identity and scope

- Raw dataset label: `RON` (70,845 files; 246,501,007 tokens)
- Proposed registry key: `ron`
- Existing family or aliases checked: Rust-like slash families. RON shares the
  delimiters and nesting shape but has a documented LF requirement for a
  complete line comment and should not inherit a permissive EOF contract.
- Classification: `language`
- Versions or releases checked: `ron-rs/ron` 0.12.2 at commit
  `31529b8b8d8c44ebf6ef91975da6cb14ae76a505`.
- Dialects checked: standard RON deserialization grammar and raw-value parser.
- Intended support scope: comments that form valid RON whitespace under the
  official 0.12 grammar.
- Explicitly excluded scope: Rust source syntax, serde host-language strings,
  and a `//` run reaching EOF without LF.

### Syntax contract

- Line comments: `//` followed by zero or more non-LF characters and then LF.
- Block comments: `/*` through the depth-matching `*/`.
- Nested comments: supported recursively.
- Termination at newline, delimiter, or EOF: the grammar requires LF to close a
  line comment; EOF instead records an unclosed line comment. Blocks require a
  matching close before EOF.
- Inline use: valid wherever RON whitespace is permitted.
- Adjacent-line grouping: valid for consecutive complete `//` lines.
- Unclosed delimiter behavior: both an EOF line comment and an unclosed block
  are invalid under the strict grammar; neither is a verified complete comment.
- Lexical or structural context: comments are consumed while skipping
  whitespace between values. Quoted strings, character forms, raw strings, and
  byte strings are parsed as values and shield marker text.
- Conflicts with strings, operators, directives, or embedded languages: inside
  a block comment, quote-looking text has no shielding role and nested slash-star
  delimiters still change depth. A single slash followed by another character
  is an error, not a comment.
- Sanitizer line wrappers: `("//", "")`, only for LF-terminated matches.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: retain nested delimiter text as payload,
  preserve CR immediately before LF consistently with source slices, and never
  clean markers inside a serialized string.

### Evidence

- Official documentation permalink:
  [RON grammar comment productions](https://github.com/ron-rs/ron/blob/31529b8b8d8c44ebf6ef91975da6cb14ae76a505/docs/grammar.md#L16-L23)
- Documentation version and relevant section: RON 0.12.2 grammar, whitespace;
  it defines `// no_newline \n` and recursively nested block comments.
- Official implementation or grammar permalink:
  [RON parser comment scanner](https://github.com/ron-rs/ron/blob/31529b8b8d8c44ebf6ef91975da6cb14ae76a505/src/parse.rs#L1396-L1438)
- Implementation version, file, and relevant symbol: commit above,
  `src/parse.rs`; `skip_comment`, `Comment::UnclosedLine`, and depth loop.
- Conformance test or official example permalink:
  [RON nested and unclosed comment tests](https://github.com/ron-rs/ron/blob/31529b8b8d8c44ebf6ef91975da6cb14ae76a505/tests/comments.rs#L3-L65)
- Secondary source, if needed:
  [raw-value EOF line-comment tests](https://github.com/ron-rs/ron/blob/31529b8b8d8c44ebf6ef91975da6cb14ae76a505/tests/407_raw_value.rs#L328-L383)
- Evidence conflicts or gaps: some callers internally skip an EOF line while
  parsing, but deserialization completion and raw values report
  `UnclosedLineComment`; grammar plus official tests define the strict contract.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official test source and parser trace; the Rust test
  suite was not rebuilt.
- Exact version or commit: `31529b8b8d8c44ebf6ef91975da6cb14ae76a505`
- Probe method: followed `skip_comment` into `skip_ws` and deserializer
  completion, then checked raw-value assertions for EOF versus LF.
- Probe input:

~~~text
(value: 42, // complete
 note: /* outer /* nested */ tail */ "ok")
~~~

- Observed result: LF closes the line comment and the outer block closes only
  after nested depth returns to zero; replacing the LF with EOF is unclosed.
- Conclusion and limits of the probe: confirms the strict complete-comment
  contract. Error recovery after malformed serialized values remains separate.

### Representative examples

#### Line comment

~~~text
(name: "Ada", // display name
 active: true)
~~~

Expected region: `// display name`, excluding LF.

#### Block comment

~~~text
(value: /* generated default */ 42)
~~~

Expected region: `/* generated default */`.

#### Nested or contextual comment

~~~text
/* outer /* nested */ tail */
"// string value"
~~~

Expected region: only the complete outer block.

### Adversarial boundaries

- Negative cases: markers in normal/raw/byte strings, a lone slash, division-like
  malformed text, and `//` at EOF without LF.
- Malformed-input cases: unclosed nested block, stray `*/`, opener at EOF,
  unterminated string, and EOF immediately after a line-comment marker.
- Line-ending and Unicode cases: LF, CRLF with CR in the scanned body, lone CR
  without LF as unclosed, Unicode payload, and exact multibyte offsets.
- Version or dialect counterexamples: Rust accepts a line comment at EOF and has
  additional doc semantics; do not alias RON to a family with that promise.
- Cleaner preservation cases: nested delimiters, stars and slashes in payload,
  empty blocks, empty LF-terminated line comments, and CRLF normalization.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: add canonical `ron`, LF-terminated `//`, nested
  `/* ... */`, strict unclosed metadata, both wrappers, evidence, and examples.
- Deterministic tests to add: raw-label lookup, LF versus EOF line behavior,
  CRLF/lone-CR behavior, inline/nested blocks, strings and raw strings, stray
  slashes, unclosed input, exact slices, grouping, and sanitizer parity.
- Remaining blocker: none; implementation must not reuse a line regex that
  automatically accepts EOF.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Sail

### Identity and scope

- Raw dataset label: `Sail` (12,556 files; 59,704,571 tokens)
- Proposed registry key: `sail`
- Existing family or aliases checked: C/Rust slash families. Sail combines
  nested blocks with strict LF-terminated line comments, documentation forms,
  and lexer states that forbid comments inside attributes.
- Classification: `language`
- Versions or releases checked: `rems-project/sail` commit
  `19f73e47ef094732749828d578cfa3a9e3e43fa9`.
- Dialects checked: ordinary Sail source, documentation comments, pragmas, and
  `$[...]` attributes.
- Intended support scope: comments accepted by the official Sail lexer.
- Explicitly excluded scope: C generated by Sail, marker text in strings, and
  slash markers inside attribute bodies where the lexer rejects comments.

### Syntax contract

- Line comments: ordinary `//` and documentation `///`; each requires LF.
- Block comments: ordinary `/* ... */` and documentation `/*! ... */`.
- Nested comments: both ordinary and documentation block scanners nest.
- Termination at newline, delimiter, or EOF: line comments close only on LF and
  error at EOF. Blocks require depth-zero `*/` and error at EOF.
- Inline use: ordinary line and block comments are valid in normal lexer state.
  Documentation forms have attachment semantics but are still comments.
- Adjacent-line grouping: ordinary consecutive line comments may group. The
  lexer specifically combines consecutive documentation `///` lines.
- Unclosed delimiter behavior: EOF line comments and unclosed blocks are lexer
  errors and are not verified complete regions.
- Lexical or structural context: strings shield marker text. Inside `$[...]`
  attributes, encountering `//` or `/*` is an error, not a comment token. A
  block comment in a pragma must terminate the pragma before further same-line
  content.
- Conflicts with strings, operators, directives, or embedded languages: match
  `///` and `/*!` before their ordinary prefixes. A stray `*/` is an error.
  Attribute and pragma modes cannot be represented by delimiter regexes alone.
- Sanitizer line wrappers: longest-first `("///", "")`, then `("//", "")`.
- Sanitizer block wrappers: longest-first `("/*!", "*/")`, then
  `("/*", "*/")`.
- Content-preservation expectations: preserve documentation payload and inner
  nested delimiters. Never strip rejected markers from attributes or consume
  pragma content following an invalid block-comment placement.

### Evidence

- Official documentation permalink:
  [Sail module syntax documentation](https://github.com/rems-project/sail/blob/19f73e47ef094732749828d578cfa3a9e3e43fa9/doc/asciidoc/modules.adoc#L80-L92)
- Documentation version and relevant section: commit above, source modules;
  examples and text identify line and block comments.
- Official implementation or grammar permalink:
  [Sail lexer comment rules](https://github.com/rems-project/sail/blob/19f73e47ef094732749828d578cfa3a9e3e43fa9/src/lib/lexer.mll#L315-L360)
- Implementation version, file, and relevant symbol: commit above,
  `src/lib/lexer.mll`; ordinary/doc line rules, recursive block scanners, EOF
  errors, attribute rejection, and pragma restrictions.
- Conformance test or official example permalink:
  [Sail lexer token declarations and comment entry rules](https://github.com/rems-project/sail/blob/19f73e47ef094732749828d578cfa3a9e3e43fa9/src/lib/lexer.mll#L232-L247)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: prose is less detailed than the lexer; the pinned
  official lexer resolves documentation, EOF, attribute, and pragma behavior.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned OCamllex source trace; Sail was not built.
- Exact version or commit: `19f73e47ef094732749828d578cfa3a9e3e43fa9`
- Probe method: traced entry rules into ordinary/doc comment states and checked
  the `$[...]`, pragma, string, stray-close, and EOF branches.
- Probe input:

~~~text
/// register helper
function f(x) = x /* outer /* nested */ tail */
$[note // rejected here]
~~~

- Observed result: the first two regions are comments; the slash marker inside
  the attribute follows the lexer's error branch rather than a comment action.
- Conclusion and limits of the probe: proves a contextual helper is required.
  Malformed-mode recovery needs deterministic tests.

### Representative examples

#### Line comment

~~~text
function increment(x) = x + 1 // one step
~~~

Expected region: `// one step`, provided LF follows it.

#### Block comment

~~~text
/*! Public register helper */
function read_reg(r) = /* implementation note */ read(r)
~~~

Expected regions: both complete block comments.

#### Nested or contextual comment

~~~text
/* outer /* nested */ tail */
$[note // not a valid comment in this mode]
~~~

Expected region: only the outer nested block.

### Adversarial boundaries

- Negative cases: slash markers in strings, both markers inside `$[...]`, a
  slash operator, stray `*/`, and prefixes `///`/`/*!` consumed as ordinary
  forms because of wrong precedence.
- Malformed-input cases: line comment at EOF, unclosed ordinary/doc block,
  unterminated attribute or string, and content after a pragma block comment.
- Line-ending and Unicode cases: LF, CRLF with CR in body, lone CR without LF,
  Unicode documentation payload, and exact offsets around nested comments.
- Version or dialect counterexamples: generated C uses C rules and is outside
  the Sail label; do not generalize Sail's EOF rule from C or Rust.
- Cleaner preservation cases: documentation marker content, nested delimiters,
  stars at line starts, blank comments, and all attribute/pragma text.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `sail`, strict LF line forms,
  nested ordinary/doc blocks, longest-first wrapper metadata, pinned evidence,
  and a Sail helper for strings, attributes, pragmas, and lexer errors.
- Deterministic tests to add: raw-label lookup, ordinary/doc comments, nesting,
  EOF rejection, string shielding, attribute negatives, pragma termination,
  stray closes, all line endings, exact slices, grouping, and sanitizer parity.
- Remaining blocker: none for valid source. On malformed input, conservatively
  suppress markers from an unclosed attribute or pragma through EOF rather
  than reclassifying rejected bytes as verified comments.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Scenic

### Identity and scope

- Raw dataset label: `Scenic` (5,968 files; 4,715,246 tokens)
- Proposed registry key: `scenic`
- Existing family or aliases checked: Python-like and pure hash-line families.
  Scenic delegates tokenization to Python, but Python strings and docstrings are
  not source comments, so only the pure hash-line contract is appropriate.
- Classification: `language`
- Versions or releases checked: Scenic 3.2.0b1 at commit
  `2fc163437ef1d3a47f109419c89b33295e26186d` and its supported Python 3.8+
  baseline.
- Dialects checked: standalone Scenic programs and embedded Python expressions
  tokenized by Scenic's front end.
- Intended support scope: Python-tokenizer `COMMENT` tokens in Scenic source.
- Explicitly excluded scope: Python/Scenic strings and docstrings, simulator
  configuration files, generated Python, and comments in other embedded files.

### Syntax contract

- Line comments: `#` through logical line end or EOF.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: comment token text excludes the
  newline and may end at EOF; Python universal-newline handling covers standard
  LF, CRLF, and CR source forms.
- Inline use: valid.
- Adjacent-line grouping: valid for consecutive full-line hash comments.
- Unclosed delimiter behavior: not applicable; line comments may end at EOF.
- Lexical or structural context: Python lexical tokens shield hash bytes inside
  single-, double-, triple-quoted, raw, bytes, and formatted strings according
  to the supported Python version.
- Conflicts with strings, operators, directives, or embedded languages:
  shebang and encoding-cookie lines are lexically comments even though tools
  assign metadata meaning. Triple-quoted strings/docstrings are never comments.
  Python-version-specific f-string parsing must not expose string hashes.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve shebang/cookie payload and all
  comment text. Never remove triple-quote scaffolding or hash text from strings.

### Evidence

- Official documentation permalink:
  [Scenic syntax guide](https://github.com/BerkeleyLearnVerify/Scenic/blob/2fc163437ef1d3a47f109419c89b33295e26186d/docs/syntax_guide.rst#L1-L10)
- Documentation version and relevant section: Scenic 3.2.0b1 syntax guide; basic
  syntax is defined as Python-compatible unless overridden.
- Official implementation or grammar permalink:
  [Scenic parser tokenization hook](https://github.com/BerkeleyLearnVerify/Scenic/blob/2fc163437ef1d3a47f109419c89b33295e26186d/src/scenic/syntax/scenic.gram#L59-L89)
- Implementation version, file, and relevant symbol: commit above,
  `src/scenic/syntax/scenic.gram`; token stream generated by Python `tokenize`.
- Conformance test or official example permalink:
  [Scenic's official Pygments comment rule](https://github.com/BerkeleyLearnVerify/Scenic/blob/2fc163437ef1d3a47f109419c89b33295e26186d/src/scenic/syntax/pygment.py#L109-L116)
- Secondary source, if needed:
  [Python lexical comments specification](https://docs.python.org/3/reference/lexical_analysis.html#comments)
- Evidence conflicts or gaps: the highlighter alone would be insufficient, but
  the grammar's direct use of Python tokenization and Python's lexical spec
  establish the contract. F-string details vary by Python release.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned Scenic grammar and tokenizer integration were
  traced; Scenic was not installed into the project environment.
- Exact version or commit: `2fc163437ef1d3a47f109419c89b33295e26186d`
- Probe method: confirmed that Scenic feeds source through Python tokenization
  and compared the official hash highlighter rule with string token boundaries.
- Probe input:

~~~text
ego = new Object with description "# literal" # Scenic comment
note = """not a comment"""
~~~

- Observed result: only the final hash region is a comment token; both quoted
  regions are strings.
- Conclusion and limits of the probe: confirms the pure hash-line mapping.
  Cross-version f-string corner cases need fixed-version tests.

### Representative examples

#### Line comment

~~~text
ego = new Object at 0@0 # initial position
~~~

Expected region: `# initial position`.

#### Block comment

Unsupported; triple-quoted strings are not comments.

#### Nested or contextual comment

~~~text
param label = "# not a comment"
# actual Scenic comment
~~~

Expected region: only `# actual Scenic comment`.

### Adversarial boundaries

- Negative cases: hash in every Python string prefix/quote form, triple-quoted
  docstrings, f-strings, bytes/raw strings, a Unicode number sign, and hashes in
  simulator data not classified as Scenic.
- Malformed-input cases: unterminated string and f-string, escape before newline,
  bare hash, and comment at EOF.
- Line-ending and Unicode cases: LF, CRLF, CR, EOF, Unicode identifiers and
  payload, and exact source offsets after multibyte string text.
- Version or dialect counterexamples: Python 3.12 permits additional f-string
  constructs, including comments in multiline replacement fields; implement
  only behavior defensible across Scenic's declared Python baseline unless the
  runtime version is known.
- Cleaner preservation cases: shebang, encoding cookie, repeated hashes,
  indentation, blank comments, and all triple-quoted content.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `scenic` with the pure hash-line delimiter and
  Python-tokenizer-compatible shielding for multiline strings, bytes/raw
  strings, and version-scoped f-string modes; do not treat triple-quoted
  strings as comments.
- Deterministic tests to add: raw-label lookup, inline/full-line/EOF comments,
  all quote and string-prefix forms, shebang/cookie handling, line endings,
  grouping, Unicode offsets, absence of blocks, and sanitizer preservation.
- Remaining blocker: none for the common Python 3.8+ lexical contract; pin the
  CI interpreter for f-string regression cases and do not rely on the shared
  single-line quote heuristic.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Simple File Verification

### Identity and scope

- Raw dataset label: `Simple File Verification` (11,809 files; 113,716,102
  tokens)
- Proposed registry key: `simple_file_verification`, alias `sfv`.
- Existing family or aliases checked: generic semicolon-line source families and
  GNU checksum formats. SFV is a data format with its own column-zero rule; no
  GNU checksum implementation was used to infer this syntax.
- Classification: `generated-format`
- Versions or releases checked: cksfv 1.3.15 source at commit
  `25fc8bd369887fc6f1feccdf035db64f50d5f1a4` and cfv at commit
  `adae0459a933b36105b0b2da9400516111e2d8a5`.
- Dialects checked: conventional `.sfv` CRC32 manifests produced and consumed
  independently by cksfv and cfv.
- Intended support scope: semicolon-prefixed metadata/comment records in SFV.
- Explicitly excluded scope: GNU md5sum/sha*sum syntax, inline semicolons in SFV
  filenames or checksum records, and whitespace-indented semicolon lines.

### Syntax contract

- Line comments: `;` is a comment marker only when it is byte zero of a logical
  record. The rest of that record is comment payload.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: the comment runs to LF/CRLF or EOF;
  line-ending bytes are excluded. Implementations use text-line readers, so a
  lone-CR compatibility case must be tested explicitly and conservatively.
- Inline use: unsupported. A semicolon after any filename/data byte is data.
- Adjacent-line grouping: valid for consecutive column-zero semicolon records.
- Unclosed delimiter behavior: not applicable; a final comment may end at EOF.
- Lexical or structural context: column position is the complete context. There
  is no SFV string-literal or escaping layer that turns an indented semicolon
  into a comment.
- Conflicts with strings, operators, directives, or embedded languages: SFV
  filenames may contain spaces and semicolons. Only `line[0] == ';'` is ignored
  by both parsers; leading spaces make the record non-comment data or invalid.
- Sanitizer line wrappers: `(";", "")` on column-zero matches only.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove one verified leading semicolon and
  preserve generated metadata, filenames mentioned in comments, timestamps,
  Unicode, subsequent semicolons, and whitespace.

### Evidence

- Official documentation permalink:
  [cksfv project page](https://zakalwe.fi/~shd/foss/cksfv/)
- Documentation version and relevant section: cksfv 1.3.15 project/source;
  cksfv is a dedicated SFV creator and verifier, independently of GNU checksum
  utilities.
- Official implementation or grammar permalink:
  [cksfv SFV record parser](https://gitlab.com/heikkiorsila/cksfv/-/blob/25fc8bd369887fc6f1feccdf035db64f50d5f1a4/src/readsfv.c#L90-L100)
- Implementation version, file, and relevant symbol: commit above,
  `src/readsfv.c`; `fgets` followed by the exact `buf[0] == ';'` rejection.
- Conformance test or official example permalink:
  [cksfv generated comment records](https://gitlab.com/heikkiorsila/cksfv/-/blob/25fc8bd369887fc6f1feccdf035db64f50d5f1a4/src/print.c#L35-L83)
- Secondary source, if needed:
  [independent cfv SFV parser/generator](https://github.com/cfv-project/cfv/blob/adae0459a933b36105b0b2da9400516111e2d8a5/lib/cfv/common.py#L1386-L1421)
- Evidence conflicts or gaps: no formal standards document was found. Two
  independent mature SFV implementations agree on exact column-zero semicolon
  recognition and generation, which is sufficient for this narrow contract.
  Neither GNU checksums nor Linguist grouping was used as syntax evidence.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: cksfv was built successfully from the pinned source;
  both parsers and generators were inspected independently.
- Exact version or commit: cksfv
  `25fc8bd369887fc6f1feccdf035db64f50d5f1a4`; cfv
  `adae0459a933b36105b0b2da9400516111e2d8a5`.
- Probe method: compared cksfv's `buf[0]` parser check and generated header with
  cfv's independent `line[0]` check and generator output.
- Probe input:

~~~text
; Generated manifest
 file;name.bin DEADBEEF
;second metadata line
~~~

- Observed result: first and third records are ignored comments; the indented
  middle record is not, and its inline semicolon belongs to the filename.
- Conclusion and limits of the probe: independently verifies the exact marker
  and anchoring. Lone-CR-only files remain a compatibility test, not a basis for
  broadening the format.

### Representative examples

#### Line comment

~~~text
; Generated by checksum tool
archive.bin DEADBEEF
~~~

Expected region: `; Generated by checksum tool`.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
;metadata
 file;part.bin DEADBEEF
; more metadata
~~~

Expected regions: only the first and third records; the indented record and its
inline semicolon are not comments.

### Adversarial boundaries

- Negative cases: leading space/tab before semicolon, semicolon inside a
  filename, a checksum record beginning with another byte, GNU checksum comment
  conventions, and a Unicode semicolon lookalike.
- Malformed-input cases: bare semicolon, missing checksum, empty file, very long
  metadata line, and final comment without newline. Bare semicolon is still a
  valid comment record even if neighboring data is invalid.
- Line-ending and Unicode cases: LF, CRLF, EOF, lone CR as an explicit
  compatibility fixture, Unicode payload, and byte-zero anchoring independent
  of character display width.
- Version or dialect counterexamples: `.md5`, `.sha1`, BSD checksum output, and
  GNU coreutils manifests are separate formats and must not inherit this rule.
- Cleaner preservation cases: second and later semicolons, generated timestamp
  text, one leading payload space, blank `;`, Unicode filenames mentioned in
  metadata, and non-comment records byte-for-byte.

### Decision

- Recommended action: `implement`
- Registry fields to change: add canonical `simple_file_verification`, alias
  `sfv`, anchored line pattern `(?m)^;[^\r\n]*`, semicolon wrapper metadata,
  pinned cksfv/cfv evidence, and column-zero examples.
- Deterministic tests to add: raw and alias lookup, column-zero positive cases,
  leading-whitespace and inline-semicolon negatives, generated headers, bare
  semicolon, all line endings and EOF, grouping, Unicode, exact slices, and
  sanitizer preservation.
- Remaining blocker: none. Keep the lone-CR expectation explicit rather than
  silently deriving it from GNU or platform-specific checksum behavior.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01
