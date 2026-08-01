# Stack v3 Full Comment Research: batch 09

## Dataset provenance

- Dataset/project: HuggingFaceCode/stack-v3-full
- Statistics repository: HuggingFaceCode/stack-v3-train
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics table, aggregated
  from `files[].language`
- Researcher or agent: `/root/research_batch_09`
- Review status: `reviewed`

Identity was checked against
[GitHub Linguist at commit af6f772](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml).
Linguist is used only to bind exact Stack labels to language identities and
extensions, not as comment-syntax evidence.

## Slang

### Identity and scope

- Raw dataset label: `Slang` (80,614 files; 141,591,530 tokens)
- Proposed registry key: `slang`
- Existing family or aliases checked: the non-nested `c_style` family,
  including its existing HLSL alias. Its physical-line regex and shared quote
  heuristic do not model Slang preprocessing or raw strings exactly.
- Classification: `language`
- Versions or releases checked: Slang v2026.14.1, commit
  `7c58a326b1f3812411a204b19cb01e323d8f6010`.
- Dialects checked: ordinary Slang/HLSL source under the documented lexical
  preprocessing phases.
- Intended support scope: source comments accepted by that release.
- Explicitly excluded scope: string, character, and raw-string contents;
  comments introduced by generated or preprocessed output.

### Syntax contract

- Line comments: `//` through the next logical line break or EOF.
- Block comments: `/*` through the first following `*/`.
- Nested comments: unsupported; the next close delimiter always terminates.
- Termination at newline, delimiter, or EOF: CR, LF, and CRLF terminate line
  comments and are excluded. A block requires its closer.
- Inline use: valid for line and block comments.
- Adjacent-line grouping: valid for consecutive full-line `//` regions.
- Unclosed delimiter behavior: an unclosed block is invalid and must not be
  accepted as a verified complete comment; a line comment may end at EOF.
- Lexical or structural context: escaped line breaks are removed before comment
  recognition, so a backslash-newline inside a line comment continues its
  logical line.
- Conflicts with strings, operators, directives, or embedded languages:
  strings and character literals shield marker bytes; a slash operator alone
  is not a comment.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: remove only the outer verified wrapper,
  retain stars, slashes, indentation, Unicode, and text across line splices.

### Evidence

- Official documentation permalink:
  [Slang lexical structure](https://github.com/shader-slang/slang/blob/7c58a326b1f3812411a204b19cb01e323d8f6010/docs/language-reference/lexical-structure.md#comments)
- Documentation version and relevant section: v2026.14.1, "Comments" and
  "Phases"; lines 41-59 define EOF, non-nesting, errors, and splice order.
- Official implementation or grammar permalink:
  [Slang lexer comment loops](https://github.com/shader-slang/slang/blob/7c58a326b1f3812411a204b19cb01e323d8f6010/source/compiler-core/slang-lexer.cpp#L405-L455)
- Implementation version, file, and relevant symbol: commit above,
  `_lexLineComment`, `_lexBlockComment`, and `_advance`.
- Conformance test or official example permalink:
  [lexical comment conformance cases](https://github.com/shader-slang/slang/tree/7c58a326b1f3812411a204b19cb01e323d8f6010/docs/generated/tests/conformance/lexical-structure)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the block loop has a TODO for an EOF diagnostic,
  while the specification and conformance case require rejection. Extraction
  follows the documented valid-source contract.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned lexer source trace.
- Exact version or commit: 7c58a326b1f3812411a204b19cb01e323d8f6010.
- Probe method: followed splice handling and both comment loops.
- Probe input: a spliced line comment, protected string, and closed block.
- Observed result: the logical line continues; the block closes first-match.
- Conclusion and limits of the probe: exact physical slices need regression tests.

### Representative examples

#### Line comment

~~~text
float gain = 1.0; // preserve calibration
~~~

Expected region: `// preserve calibration`.

#### Block comment

~~~text
/* shared shader parameters */
cbuffer Params { float gain; }
~~~

Expected region: `/* shared shader parameters */`.

#### Nested or contextual comment

~~~text
/* outer /* not nested */ float enabled;
~~~

Expected region: `/* outer /* not nested */`; the trailing source is not
part of the comment.

### Adversarial boundaries

- Negative cases: markers in normal and raw strings, character literals, slash
  operators, URLs in strings, and marker-looking macro payload.
- Malformed-input cases: unclosed block, stray `*/`, splice at EOF, and
  unterminated string before a marker.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF line comment, Unicode
  payload, and every escaped-line-break form.
- Version or dialect counterexamples: do not infer recursive block comments
  from Rust-like languages or accept HLSL comments in rendered shader output.
- Cleaner preservation cases: empty wrappers, star-decorated blocks, logical
  line continuations, indentation, and exact Unicode source slices.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `slang` with C-style delimiters and a pinned
  Slang lexer helper for escaped-line-break preprocessing, ordinary/character
  strings, and raw strings; seed a line-splice example.
- Deterministic tests to add: raw-label lookup, both forms, first-close
  non-nesting, strings/raw strings, unclosed blocks, EOF, CR/LF/CRLF, escaped
  line breaks, exact `QueryMatch` slices, and sanitizer parity.
- Remaining blocker: none; keep the behavior language-specific because other
  aliases in the shared C-style family do not all splice physical lines before
  recognizing comments.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Slint

### Identity and scope

- Raw dataset label: `Slint` (11,098 files; 13,812,306 tokens)
- Proposed registry key: `slint`
- Existing family or aliases checked: `rust_style`; its recursive slash-block
  delimiters match, but Slint also terminates line comments on lone CR and
  re-enters code mode inside interpolated strings. Those semantics are not an
  exact Rust-family alias.
- Classification: `language`
- Versions or releases checked: Slint v1.17.1, commit
  `cf62c975c311e7036d599ed8ed0b7e6a8386a934`.
- Dialects checked: declarative `.slint` source and interpolated
  expression mode.
- Intended support scope: comments tokenized by the Slint compiler.
- Explicitly excluded scope: Rust host files, rendered text, and marker text
  inside Slint strings.

### Syntax contract

- Line comments: `//` through CR, LF, or EOF.
- Block comments: `/*` through its depth-matching `*/`.
- Nested comments: recursively supported.
- Termination at newline, delimiter, or EOF: line terminators are excluded;
  blocks may cross lines and require all nesting levels to close.
- Inline use: valid for both forms.
- Adjacent-line grouping: valid for consecutive full-line comments.
- Unclosed delimiter behavior: `lex_comment` returns zero for an unclosed
  block, so it must not be extracted as complete.
- Lexical or structural context: the lexer consumes strings separately;
  comments in expression portions of interpolated strings are code comments,
  while marker text in string portions is protected.
- Conflicts with strings, operators, directives, or embedded languages: URL and
  color-like text inside strings is not a comment.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: strip only the outer pair and preserve
  inner delimiter text, indentation, line endings, and Unicode.

### Evidence

- Official documentation permalink:
  [Slint comments guide](https://docs.slint.dev/latest/docs/slint/guide/language/coding/file/#comments)
- Documentation version and relevant section: latest guide checked against
  v1.17.1; the prose confirms line and block forms.
- Official implementation or grammar permalink:
  [Slint recursive comment lexer](https://github.com/slint-ui/slint/blob/cf62c975c311e7036d599ed8ed0b7e6a8386a934/internal/compiler/lexer.rs#L51-L85)
- Implementation version, file, and relevant symbol: commit above,
  `internal/compiler/lexer.rs::lex_comment`.
- Conformance test or official example permalink:
  [official nested-comment fixture](https://github.com/slint-ui/slint/blob/cf62c975c311e7036d599ed8ed0b7e6a8386a934/internal/compiler/tests/syntax/basic/comments.slint#L1-L28)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the guide's wording about block termination is
  imprecise; pinned lexer code and fixture establish delimiter closure and
  recursion.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned lexer and fixture trace.
- Exact version or commit: cf62c975c311e7036d599ed8ed0b7e6a8386a934.
- Probe method: followed nested-depth increments, decrements, and zero returns.
- Probe input: a nested block beside a URL string.
- Observed result: one nested comment; the string stays protected.
- Conclusion and limits of the probe: interpolation mode needs integration tests.

### Representative examples

#### Line comment

~~~text
width: 100px; // fixed design width
~~~

Expected region: `// fixed design width`.

#### Block comment

~~~text
background: /* fallback */ blue;
~~~

Expected region: `/* fallback */`.

#### Nested or contextual comment

~~~text
/* outer /* inner */ outer */
~~~

Expected region: the complete outer region.

### Adversarial boundaries

- Negative cases: markers in strings, URLs, slash operators in embedded
  expressions, and braces that change interpolation state.
- Malformed-input cases: unclosed outer/inner blocks, stray closers, and
  unclosed strings adjacent to an opener.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF line comment, Unicode
  payload, and byte offsets around multibyte text.
- Version or dialect counterexamples: do not use the non-nested current
  `rust_style` regex unchanged; correct that mapping to recursive blocks.
- Cleaner preservation cases: nested delimiters remain payload when only the
  outer wrapper is removed; preserve indentation and blank lines.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `slint` with recursive slash blocks and a
  Slint lexer helper for CR/LF line termination and interpolated-string mode;
  do not add it as a plain `rust_style` alias.
- Deterministic tests to add: raw lookup, line/inline/nested forms, EOF,
  unclosed blocks, strings and interpolation, exact slices, and cleaner parity.
- Remaining blocker: none; preserve Slint's lone-CR and interpolation behavior
  independently of Rust and Sway.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Smithy

### Identity and scope

- Raw dataset label: `Smithy` (11,821 files; 9,886,352 tokens)
- Proposed registry key: `smithy`
- Existing family or aliases checked: line-only slash `cue_style`; its
  delimiter matches, but its shared single-line quote heuristic does not cover
  Smithy triple-quoted text blocks.
- Classification: `language`
- Versions or releases checked: Smithy 2.0 and smithy-java 1.72.1, commit
  `bc9f0babd071d4ab818d5c4ea582f0e6f71f251e`.
- Dialects checked: Smithy IDL 2.0 ordinary and documentation comments.
- Intended support scope: every `COMMENT` or `DOC_COMMENT` token
  produced by the official tokenizer.
- Explicitly excluded scope: JSON AST/model files, string and text-block
  contents, and semantic documentation attachment.

### Syntax contract

- Line comments: `//`; `///`, `////`, and longer runs are
  documentation-comment lexical subsets but share the same outer marker.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: official 1.72.1 tokenizer accepts
  LF, CRLF, lone CR, and EOF, and includes a present newline in its token.
  Extraction excludes the terminator.
- Inline use: ordinary comments are allowed wherever whitespace is allowed;
  misplaced documentation comments remain comment tokens even when attachment
  later produces a validation event.
- Adjacent-line grouping: valid for consecutive ordinary or documentation
  lines; semantic documentation concatenation is outside extraction.
- Unclosed delimiter behavior: not applicable; line comments may end at EOF.
- Lexical or structural context: quoted strings and triple-quoted text blocks
  are consumed before interior markers can become comments.
- Conflicts with strings, operators, directives, or embedded languages: a lone
  slash is a tokenizer error; `#` is a shape-ID token, not a comment.
- Sanitizer line wrappers: `("//", "")`; preserve one or more extra
  leading slashes as content for doc comments.
- Sanitizer block wrappers: none.
- Content-preservation expectations: retain doc-comment slash payload,
  CommonMark content, whitespace, and Unicode.

### Evidence

- Official documentation permalink:
  [Smithy 2.0 comments specification](https://smithy.io/2.0/spec/idl.html#comments)
- Documentation version and relevant section: Smithy 2.0 IDL grammar,
  `Comment`, `DocumentationComment`, `LineComment`, and
  `NL`.
- Official implementation or grammar permalink:
  [DefaultTokenizer.parseComment](https://github.com/smithy-lang/smithy/blob/bc9f0babd071d4ab818d5c4ea582f0e6f71f251e/smithy-model/src/main/java/software/amazon/smithy/model/loader/DefaultTokenizer.java#L299-L329)
- Implementation version, file, and relevant symbol: smithy-java 1.72.1,
  `DefaultTokenizer.parseComment`.
- Conformance test or official example permalink:
  [official documentation-comment model](https://github.com/smithy-lang/smithy/blob/bc9f0babd071d4ab818d5c4ea582f0e6f71f251e/smithy-model/src/test/resources/software/amazon/smithy/model/loader/valid/doc-comments/doc-comments.smithy)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the ABNF requires LF or CRLF, while the release
  tokenizer explicitly accepts lone CR and EOF. The implementation scope is
  recorded and both differences require tests.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: tokenizer and official fixtures traced.
- Exact version or commit: bc9f0babd071d4ab818d5c4ea582f0e6f71f251e.
- Probe method: followed slash branches and CR/LF/EOF termination.
- Probe input: ordinary and documentation comments ending at newline and EOF.
- Observed result: both are comments; strings remain protected.
- Conclusion and limits of the probe: documentation attachment is excluded.

### Representative examples

#### Line comment

~~~text
string Name // public name
~~~

Expected region: `// public name`.

#### Block comment

Smithy has no block-comment region; `/* text */` is a negative case.

#### Nested or contextual comment

~~~text
/// Shape documentation
string Name
~~~

Expected region: `/// Shape documentation`, cleaned through the shared
two-slash wrapper with one slash retained.

### Adversarial boundaries

- Negative cases: `//` in strings and text blocks, `#` shape IDs,
  lone slash, and block-looking text.
- Malformed-input cases: lone CR versus the grammar, EOF comments, misplaced
  doc comments, and unterminated strings before a marker.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF, tabs, CommonMark
  Unicode, and exact offsets when tokenizer tokens include newline bytes.
- Version or dialect counterexamples: keep Smithy 1.0 JSON AST and semantic
  documentation traits outside this key.
- Cleaner preservation cases: `///`, `////`, empty comments,
  leading content spaces, and adjacent doc lines.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `smithy` with the line-only slash delimiter
  and Smithy-aware shielding for quoted strings and triple-quoted text blocks;
  attach pinned evidence and a documentation-line seed without block syntax.
- Deterministic tests to add: raw lookup, ordinary/doc slash runs, string and
  text-block shielding, CR/LF/CRLF/EOF, lone slash, exact slices, and cleaning.
- Remaining blocker: none; document the spec/implementation terminator
  difference and do not rely on the shared single-line quote heuristic.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Snakemake

### Identity and scope

- Raw dataset label: `Snakemake` (81,115 files; 145,124,898 tokens)
- Proposed registry key: `snakemake`
- Existing family or aliases checked: pure `hash_line_style`; its delimiter
  matches, but its shared single-line quote heuristic cannot reproduce Python
  multiline-string and f-string lexical modes.
- Classification: `language`
- Versions or releases checked: Snakemake 9.24.0, commit
  `e7f10a512bfe8c25ecfaa1062f60f282f427edd0`, with Python 3 tokenization.
- Dialects checked: Snakefiles and `.smk` modules parsed by the bundled
  parser.
- Intended support scope: Python `COMMENT` tokens in Snakemake source.
- Explicitly excluded scope: docstrings/triple strings, shell-language comments
  inside quoted shell directives, and comments in external scripts.

### Syntax contract

- Line comments: `#` through CR/LF or EOF as produced by Python
  `tokenize`.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: the physical newline is excluded;
  EOF closes the comment.
- Inline use: valid, including after rule fields and Python expressions.
- Adjacent-line grouping: valid for consecutive full-line comment tokens.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: Snakemake constructs its token stream with
  `tokenize.generate_tokens(self.file.readline)`; Python strings,
  triple-quoted strings, f-strings, and escapes shield hash bytes.
- Conflicts with strings, operators, directives, or embedded languages:
  shebang and encoding-cookie lines are lexically comments; `#` inside
  `shell:` strings belongs to the string, not the Snakefile layer.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: retain shebang/cookie payload, extra
  leading hashes, indentation, and Unicode.

### Evidence

- Official documentation permalink:
  [Snakemake 9.24 rule documentation](https://snakemake.readthedocs.io/en/v9.24.0/snakefiles/rules.html)
- Documentation version and relevant section: v9.24.0 Snakefile syntax,
  identified as a Python-based workflow language.
- Official implementation or grammar permalink:
  [Snakefile Python-tokenizer construction](https://github.com/snakemake/snakemake/blob/e7f10a512bfe8c25ecfaa1062f60f282f427edd0/src/snakemake/parser.py#L1351-L1361)
- Implementation version, file, and relevant symbol: v9.24.0,
  `parser.py::Snakefile`; comment handling is also explicit at lines
  241-255 and 858-866.
- Conformance test or official example permalink:
  [terminal comment regression fixture](https://github.com/snakemake/snakemake/tree/e7f10a512bfe8c25ecfaa1062f60f282f427edd0/tests/test_parsing_terminal_comment_following_statement)
- Secondary source, if needed:
  [Python tokenize documentation](https://docs.python.org/3/library/tokenize.html)
- Evidence conflicts or gaps: Python-version-specific f-string token details
  vary, but hashes inside valid strings remain non-comments across supported
  versions.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: Python 3.13.9 generate_tokens.
- Exact version or commit: Snakemake e7f10a512bfe8c25ecfaa1062f60f282f427edd0.
- Probe method: printed only STRING and COMMENT tokens.
- Probe input: quoted/triple-quoted hashes plus inline and EOF hashes.
- Observed result: only the latter two were comments.
- Conclusion and limits of the probe: add supported-version f-string tests.

### Representative examples

#### Line comment

~~~text
output: "result.txt"  # generated artifact
~~~

Expected region: `# generated artifact`.

#### Block comment

There is no block syntax; a triple-quoted rule docstring is a string.

#### Nested or contextual comment

~~~text
shell: "printf '# shell data\n' > {output}"
~~~

Expected region: none at the Snakefile layer.

### Adversarial boundaries

- Negative cases: single/double/triple/raw/f-strings, hashes in shell strings,
  dictionary keys, and hashes in external script paths.
- Malformed-input cases: unclosed strings, invalid f-strings, backslash at EOF,
  and comments adjacent to rule-state transitions.
- Line-ending and Unicode cases: LF, CRLF, EOF comment, encoding cookies,
  shebangs, and Unicode identifiers/body text.
- Version or dialect counterexamples: do not inherit Python docstring
  pseudo-comment extraction or comments from Bash/R scripts referenced by a
  Snakefile.
- Cleaner preservation cases: shebangs, coding cookies, multiple hashes,
  indentation, and an EOF line without newline.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `snakemake` with the hash-line delimiter and
  Python-tokenizer-compatible shielding for multiline strings, bytes/raw
  strings, and supported-version f-string modes; retain the pinned parser
  evidence and no triple-string pseudo-comments.
- Deterministic tests to add: raw lookup, inline/full-line/EOF hashes, all
  Python string forms, shell directives, shebang/cookie, f-strings, exact
  slices, and cleaner parity.
- Remaining blocker: none; use the pinned Python-token stream contract rather
  than the shared single-line quote heuristic.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Survex data

### Identity and scope

- Raw dataset label: `Survex data` (5,378 files; 12,953,595 tokens)
- Proposed registry key: `survex_data`
- Existing family or aliases checked: `semicolon_style`; rejected because
  both comment and end-of-line character classes are mutable and scoped.
- Classification: `document-format`
- Versions or releases checked: Survex 1.4.22 source and manual.
- Dialects checked: native `.svx` data read by Cavern.
- Intended support scope: default settings plus in-file `*set`,
  `*begin`, and `*end` changes that can be derived from one file.
- Explicitly excluded scope: caller-inherited settings from an including parent,
  Walls/Compass import formats, and cross-file state not present in the source.

### Syntax contract

- Line comments: any active one-byte `COMMENT` class member starts a
  comment; the default is semicolon.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: comment text continues until an
  active `EOL` character. Defaults are CR, LF, Ctrl-Z, and EOF, but
  `*set eol` can make a comment span physical newlines.
- Inline use: valid after data or commands when the scanner reaches an active
  comment character.
- Adjacent-line grouping: valid only after resolving the active comment/EOL
  maps per logical line.
- Unclosed delimiter behavior: not applicable; EOF is always an EOL sentinel.
- Lexical or structural context: `*set comment` replaces all
  nonalphanumeric comment characters and accepts literal bytes or `xHH`;
  settings are inherited into and restored after nested survey scopes.
- Conflicts with strings, operators, directives, or embedded languages: a
  character assigned a special meaning loses its double-quote role; a static
  semicolon regex becomes wrong immediately after a set command.
- Sanitizer line wrappers: dynamic one-character wrappers from the active map.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove exactly the active marker and keep
  all payload, including physical newlines before a custom logical EOL.

### Evidence

- Official documentation permalink:
  [Survex data-file manual](https://survex.com/docs/manual/datafile.htm)
- Documentation version and relevant section: Survex 1.4.22, `*SET`
  character classes and semicolon comment examples.
- Official implementation or grammar permalink:
  [Survex 1.4.22 source archive](https://deb.debian.org/debian/pool/main/s/survex/survex_1.4.22.orig.tar.gz)
- Implementation version, file, and relevant symbol: archive SHA-256
  `a26962d888621cfd2043a7cc6a227fc905130dfbd14c450dc1c4c02fbfdd9dbc`;
  `src/commands.c::init_default_translate_map` and `cmd_set`,
  `src/datain.c::process_eol`.
- Conformance test or official example permalink:
  [upstream source repository](https://repo.or.cz/survex.git)
  file `tests/cmd_set.svx`, lines 11-15 and 44-51 in release 1.4.22.
- Secondary source, if needed: Debian only hosts the byte-identical official
  release archive used for the pinned checksum.
- Evidence conflicts or gaps: extraction of an included file cannot recover
  nondefault settings inherited from its parent; that case is explicitly out
  of standalone scope.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: release source and cmd_set.svx traced.
- Exact version or commit: Survex 1.4.22 archive checksum above.
- Probe method: followed map replacement, scope copying, and active-EOL skipping.
- Probe input: two custom comment bytes and caret as EOL.
- Observed result: both bytes start comments; comments cross LF until caret.
- Conclusion and limits of the probe: inherited include state is excluded.

### Representative examples

#### Line comment

~~~text
A B 10 90 0 ; surveyed twice
~~~

Expected default region: `; surveyed twice`.

#### Block comment

Survex has no block-comment delimiter.

#### Nested or contextual comment

~~~text
*begin
*set comment %
A B 10 90 0 % local note
*end
C D 10 90 0 ; default restored
~~~

Expected regions use percent inside the scope and semicolon after restoration.

### Adversarial boundaries

- Negative cases: old markers after replacement, alphanumeric `*set`
  values, station-name punctuation, quoted values before and after quote is
  reassigned, and keyword characters.
- Malformed-input cases: invalid `xHH`, empty maps, unterminated scopes,
  unknown character classes, and a set command whose active EOL changes.
- Line-ending and Unicode cases: default CR/LF/Ctrl-Z/EOF, CRLF as two active
  EOL bytes, custom ASCII EOL, physical newline inside a logical comment, and
  non-ASCII payload.
- Version or dialect counterexamples: do not apply Survex settings to Walls
  data or infer an include parent's active translation table.
- Cleaner preservation cases: dynamic markers, multiple active markers,
  physical newlines in one logical comment, blank payload, and scope changes.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `survex_data` with a scanner helper that
  tracks translation maps and scopes; default semicolon metadata alone is not
  sufficient.
- Deterministic tests to add: raw lookup, defaults, multiple/replaced markers,
  `xHH`, custom EOL spanning LF, nested scope restoration, quote-role
  changes, exact slices, and dynamic cleaning.
- Remaining blocker: none for standalone files; inherited include state remains
  an explicit exclusion.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Sway

### Identity and scope

- Raw dataset label: `Sway` (28,043 files; 52,169,663 tokens)
- Proposed registry key: `sway`
- Existing family or aliases checked: corrected recursive
  `rust_style`; delimiter, nesting, and cleaning semantics match.
- Classification: `language`
- Versions or releases checked: Sway v0.72.0, commit
  `91be236f71fbb541ee6639ef0d955b2b8cf0a658`.
- Dialects checked: ordinary Sway source and inner/outer documentation comments.
- Intended support scope: comment nodes produced by `sway-parse`.
- Explicitly excluded scope: strings, ABI JSON, generated Rust, and formatter
  metadata outside source regions.

### Syntax contract

- Line comments: `//` through LF or EOF. `///` and `//!` are
  doc subsets; `////` is ordinary.
- Block comments: `/*` through its depth-matching `*/`.
- Nested comments: recursively supported.
- Termination at newline, delimiter, or EOF: implementation searches for LF;
  CRLF therefore leaves CR immediately before the terminator in the raw span,
  and lone CR does not terminate. Extraction should exclude CR from a CRLF
  terminator while preserving exact source positions.
- Inline use: valid for both forms.
- Adjacent-line grouping: valid for ordinary and doc line comments.
- Unclosed delimiter behavior: emits `UnclosedMultilineComment` and no
  completed comment node.
- Lexical or structural context: strings are consumed by `lex_string`
  and protect slash markers.
- Conflicts with strings, operators, directives, or embedded languages: slash
  operators and markers in strings are not comments; doc classification does
  not change extraction wrappers.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: preserve nested delimiter text as payload,
  doc sigils, whitespace, and Unicode.

### Evidence

- Official documentation permalink:
  [Sway comments guide](https://github.com/FuelLabs/sway/blob/91be236f71fbb541ee6639ef0d955b2b8cf0a658/docs/book/src/basics/comments_and_logging.md#L1-L37)
- Documentation version and relevant section: v0.72.0, comments and inline/block
  examples.
- Official implementation or grammar permalink:
  [Sway line and block lexers](https://github.com/FuelLabs/sway/blob/91be236f71fbb541ee6639ef0d955b2b8cf0a658/sway-parse/src/token.rs#L398-L489)
- Implementation version, file, and relevant symbol: commit above,
  `lex_line_comment` and `lex_block_comment`.
- Conformance test or official example permalink:
  [unclosed multiline comment fixture](https://github.com/FuelLabs/sway/tree/91be236f71fbb541ee6639ef0d955b2b8cf0a658/test/src/e2e_vm_tests/test_programs/should_fail/unclosed_multiline_comment)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the introductory guide does not describe nesting;
  the pinned lexer stack and official failure fixtures establish it.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned lexer and fixture trace.
- Exact version or commit: 91be236f71fbb541ee6639ef0d955b2b8cf0a658.
- Probe method: followed nesting-stack pushes/pops and LF search.
- Probe input: nested block, URL string, and trailing line comment.
- Observed result: one nested block and one line comment; URL protected.
- Conclusion and limits of the probe: retain a CR-only regression case.

### Representative examples

#### Line comment

~~~text
let fuel = 8; // initial amount
~~~

Expected region: `// initial amount`.

#### Block comment

~~~text
/* initialization path */
fn main() {}
~~~

Expected region: `/* initialization path */`.

#### Nested or contextual comment

~~~text
/* outer /* inner */ outer */
~~~

Expected region: the entire outer region.

### Adversarial boundaries

- Negative cases: URLs and markers in strings, slash operators, raw
  identifiers, doc sigils, and `////` classification.
- Malformed-input cases: unclosed outer/inner blocks, stray closer, unclosed
  string, and opener at EOF.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF line comment, Unicode
  identifiers/body, and exact byte spans.
- Version or dialect counterexamples: do not map to non-nested C style.
- Cleaner preservation cases: inner delimiters, `//!`/`///`
  payload, empty comments, and indentation.

### Decision

- Recommended action: `alias`
- Registry fields to change: correct `rust_style` to recursive blocks and
  add `sway` as an alias with pinned evidence.
- Deterministic tests to add: raw lookup, line/doc/nested forms, strings,
  unclosed blocks, LF/CRLF/lone CR/EOF, exact slices, and cleaning.
- Remaining blocker: none.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Sweave

### Identity and scope

- Raw dataset label: `Sweave` (72,384 files; 567,932,112 tokens)
- Proposed registry key: `sweave`
- Existing family or aliases checked: R hash and TeX percent families; neither
  can be applied globally to the mixed document.
- Classification: `template`
- Versions or releases checked: R 4.4.3 runtime and R-devel source commit
  `81ef5aab518eb98f7d8102ba689e855bd118e933`.
- Dialects checked: default Noweb `.Rnw`/`.Snw` syntax selected by
  `SweaveSyntaxNoweb`.
- Intended support scope: standard LaTeX comments in documentation chunks and
  R comments in code chunks and inline `\Sexpr{...}` expressions.
- Explicitly excluded scope: `.Rtex` `SweaveSyntaxLatex`,
  user-defined Sweave syntax objects, arbitrary TeX catcode redefinitions, and
  comments in generated TeX/R output.

### Syntax contract

- Line comments: percent in standard LaTeX documentation context; hash in R
  code context. Escaped TeX percent does not start a comment.
- Block comments: unsupported in both layers.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: both line forms end before the
  physical line ending or at EOF.
- Inline use: valid in each active layer.
- Adjacent-line grouping: valid only within the same layer; a Noweb transition
  splits groups.
- Unclosed delimiter behavior: not applicable to comments; malformed chunk or
  inline-expression boundaries must not leak one layer's marker globally.
- Lexical or structural context: mode starts as documentation;
  `^<<(.*)>>=.*` starts R code and `^@` returns to documentation.
  Transition lines are control lines. Inline `\Sexpr` temporarily uses R.
- Conflicts with strings, operators, directives, or embedded languages:
  `#` is literal/macro syntax in TeX, percent operators such as
  `%%` and `%in%` are R code, and both marker types are protected
  by their layer's strings/verbatim contexts.
- Sanitizer line wrappers: context-selected `("%", "")` or
  `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve marker-adjacent content,
  operational vignette metadata, chunk boundaries, indentation, and Unicode.

### Evidence

- Official documentation permalink:
  [R Sweave manual](https://stat.ethz.ch/R-manual/R-devel/library/utils/html/Sweave.html)
- Documentation version and relevant section: R-devel `utils::Sweave`,
  Noweb documentation/code chunks and syntax selection.
- Official implementation or grammar permalink:
  [Sweave mode loop and syntax definitions](https://github.com/wch/r-source/blob/81ef5aab518eb98f7d8102ba689e855bd118e933/src/library/utils/R/Sweave.R#L90-L172)
- Implementation version, file, and relevant symbol: commit above,
  `Sweave`, `SweaveSyntaxNoweb` at lines 295-315, and
  `SweaveSyntaxLatex` at lines 317-327.
- Conformance test or official example permalink:
  [official Sweave test document](https://github.com/wch/r-source/blob/81ef5aab518eb98f7d8102ba689e855bd118e933/src/library/utils/inst/Sweave/Sweave-test-1.Rnw)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: TeX permits arbitrary catcode changes; the key
  deliberately promises standard LaTeX/Sweave behavior, not a full TeX engine.
- Confidence: `provisional`

### Implementation confirmation

- Implementation tested: R 4.4.3 utils::Stangle.
- Exact version or commit: R 4.4.3; source 81ef5aab518eb98f7d8102ba689e855bd118e933.
- Probe method: tangled a mixed .Rnw file.
- Probe input: TeX percent/hash, R hash/string, and percent operator.
- Observed result: only the code chunk reached R and retained its tokens.
- Conclusion and limits of the probe: TeX catcode changes remain excluded.

### Representative examples

#### Line comment

~~~text
<<fit>>=
# Fit the model
model <- lm(y ~ x)
@
~~~

Expected region: `# Fit the model`.

#### Block comment

Neither R nor standard LaTeX supplies a Sweave block-comment wrapper.

#### Nested or contextual comment

~~~text
% TeX-side note
<<calc>>=
remainder <- 5 %% 2 # R-side note
@
~~~

Expected regions: the percent line in documentation and the trailing hash in
R code; `%%` is not a comment.

### Adversarial boundaries

- Negative cases: TeX `#1`, escaped percent, `\verb`/verbatim
  content, R percent operators, all R strings, chunk-marker-looking text away
  from column zero, and hash text in documentation.
- Malformed-input cases: missing `@`, malformed chunk header, marker line
  inside an invalid R construct, and unbalanced `\Sexpr`.
- Line-ending and Unicode cases: LF, CRLF, EOF in either mode, Unicode TeX/R
  payload, and exact offsets across transition lines.
- Version or dialect counterexamples: `.Rtex`, custom
  `\SweaveSyntax`, knitr-only chunk syntax, and arbitrary TeX catcodes are
  excluded.
- Cleaner preservation cases: vignette metadata lines, escaped percent,
  multiple hashes, chunk labels, transition lines, and R/TeX indentation.

### Decision

- Recommended action: `defer`
- Registry fields to change: none until the embedded-layer lexical evidence is
  complete. The eventual `sweave` helper needs a Noweb mode scanner, standard
  TeX percent recognition, R hash tokenization, and inline `\Sexpr` handling.
- Deterministic tests to add: raw lookup, transitions, both markers, cross-layer
  negatives, R strings/operators, TeX escapes/verbatim, inline expressions,
  line endings, exact slices, and contextual cleaning.
- Remaining blocker: pin versioned TeX and R lexer evidence for escaped percent,
  verbatim contexts, strings, and comments, then probe nested/escaped braces
  and comment boundaries inside `\Sexpr`. The Sweave mode loop alone does not
  establish those embedded-language lexical contracts.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Tact

### Identity and scope

- Raw dataset label: `Tact` (15,897 files; 88,130,483 tokens)
- Proposed registry key: `tact`
- Existing family or aliases checked: non-nested `c_style`; exact match.
- Classification: `language`
- Versions or releases checked: Tact v1.6.13, commit
  `2f488e4c339d6e2dbcdff8ab8ad8a410060d9cc6`.
- Dialects checked: ordinary Tact and assembly sequences parsed by the PEG.
- Intended support scope: grammar `Comment` regions.
- Explicitly excluded scope: strings, FunC source, generated BoC/cell data, and
  documentation produced by tooling.

### Syntax contract

- Line comments: `//` through CR, LF, or EOF.
- Block comments: `/*` through the first `*/`.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: line endings are excluded; block
  closer is required.
- Inline use: valid where grammar space or assembly items are accepted.
- Adjacent-line grouping: valid for consecutive full-line comments.
- Unclosed delimiter behavior: PEG block production fails without `*/`;
  do not extract it as complete.
- Lexical or structural context: quoted strings are separate productions and
  shield comment markers.
- Conflicts with strings, operators, directives, or embedded languages:
  assembly explicitly parses comments and quoted text before its fallback.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: strip only wrappers and preserve
  indentation, stars, slashes, and Unicode.

### Evidence

- Official documentation permalink:
  [Tact language repository](https://github.com/tact-lang/tact/tree/2f488e4c339d6e2dbcdff8ab8ad8a410060d9cc6)
- Documentation version and relevant section: v1.6.13 source grammar is the
  normative checked artifact.
- Official implementation or grammar permalink:
  [Tact comment PEG productions](https://github.com/tact-lang/tact/blob/2f488e4c339d6e2dbcdff8ab8ad8a410060d9cc6/src/grammar/grammar.peggy#L355-L358)
- Implementation version, file, and relevant symbol: commit above,
  `space`, `Comment`, `multiLineComment`, and
  `singleLineComment`; assembly comments appear at lines 165-171.
- Conformance test or official example permalink:
  [official string-as-comment test](https://github.com/tact-lang/tact/blob/2f488e4c339d6e2dbcdff8ab8ad8a410060d9cc6/src/test/e2e-emulated/strings/as-comment.tact)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: none affecting extraction.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned PEG and fixture traced.
- Exact version or commit: 2f488e4c339d6e2dbcdff8ab8ad8a410060d9cc6.
- Probe method: followed ordered alternatives and first-close repetition.
- Probe input: protected string marker followed by a closed block.
- Observed result: only the block is a comment and closes first-match.
- Conclusion and limits of the probe: malformed recovery needs tests.

### Representative examples

#### Line comment

~~~text
return total; // nanotons
~~~

Expected region: `// nanotons`.

#### Block comment

~~~text
/* validate sender */
require(sender() == owner);
~~~

Expected region: `/* validate sender */`.

#### Nested or contextual comment

~~~text
/* outer /* not nested */ return;
~~~

Expected region ends at the first `*/`.

### Adversarial boundaries

- Negative cases: markers in strings and assembly quoted items, slash
  operators, a lone slash, and FunC syntax.
- Malformed-input cases: unclosed block, stray close, unclosed string, and an
  opener at EOF.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF line comment, Unicode
  payload, and exact offsets.
- Version or dialect counterexamples: do not infer nested blocks from Sway or
  Rust and do not import comments from embedded/generated languages.
- Cleaner preservation cases: empty comments, decorated blocks, extra slashes,
  indentation, and first-close payload.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `tact` to `c_style` with pinned
  grammar evidence and line/block seeds.
- Deterministic tests to add: raw lookup, both forms, non-nesting, strings and
  assembly quotes, unclosed blocks, line endings/EOF, exact slices, and cleaner.
- Remaining blocker: none.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## templ

### Identity and scope

- Raw dataset label: `templ` (60,892 files; 89,375,457 tokens)
- Proposed registry key: `templ`
- Existing family or aliases checked: Go C-style and HTML-comment families;
  neither is safe globally across templ parser modes.
- Classification: `template`
- Versions or releases checked: templ v0.3.1020, commit
  `09d6b02946f54492f3d3dcb9729f5b792f220b40`.
- Dialects checked: `.templ` files parsed by parser/v2.
- Intended support scope: parser `GoComment` and `HTMLComment` nodes
  in their accepted template/source contexts.
- Explicitly excluded scope: JavaScript/CSS comments in raw
  `<script>`/`<style>` bodies, rendered output comments from other
  languages, and marker-looking plain text.

### Syntax contract

- Line comments: Go `//` through newline or EOF in Go/comment parser
  contexts.
- Block comments: Go non-nested `/* ... */`; HTML
  `<!-- ... -->` within template nodes.
- Nested comments: unsupported for both block forms.
- Termination at newline, delimiter, or EOF: line comments allow EOF; both
  block forms require a closer. HTML closes only at `-->`; an internal
  `--` not followed by `>` is invalid.
- Inline use: Go comments are accepted at top level and in the template-node
  parser; HTML comments are template nodes.
- Adjacent-line grouping: valid for consecutive Go line comments in the same
  parser mode; HTML regions remain individually delimited.
- Unclosed delimiter behavior: parser returns an explicit missing-closer error;
  do not accept incomplete block regions.
- Lexical or structural context: Go strings/raw strings and templ expression
  parsers shield markers; raw script/style elements consume their contents
  without applying templ comment parsers.
- Conflicts with strings, operators, directives, or embedded languages: URLs
  and `//` in literal HTML text are not automatically Go comments;
  `{! call !}` is a template call, not a comment.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: context-selected `("/*", "*/")` and
  `("<!--", "-->")`.
- Content-preservation expectations: preserve HTML comment content even though
  it renders, suppress only wrappers in cleaned text, and retain Go/HTML bytes.

### Evidence

- Official documentation permalink:
  [templ comments documentation](https://github.com/a-h/templ/blob/09d6b02946f54492f3d3dcb9729f5b792f220b40/docs/docs/03-syntax-and-usage/14-comments.md)
- Documentation version and relevant section: v0.3.1020, HTML comments inside
  templ statements and Go comments outside.
- Official implementation or grammar permalink:
  [template-node parser ordering](https://github.com/a-h/templ/blob/09d6b02946f54492f3d3dcb9729f5b792f220b40/parser/v2/templateparser.go#L61-L84)
- Implementation version, file, and relevant symbol: commit above,
  `templateNodeParsers`, plus
  [Go comment parser](https://github.com/a-h/templ/blob/09d6b02946f54492f3d3dcb9729f5b792f220b40/parser/v2/gocommentparser.go#L7-L66)
  and
  [HTML comment parser](https://github.com/a-h/templ/blob/09d6b02946f54492f3d3dcb9729f5b792f220b40/parser/v2/htmlcommentparser.go#L7-L40).
- Conformance test or official example permalink:
  [Go comments inside a template fixture](https://github.com/a-h/templ/blob/09d6b02946f54492f3d3dcb9729f5b792f220b40/generator/test-go-comments/template.templ)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: documentation says Go comments outside templ
  statements, while the pinned parser and official generator fixture accept
  them inside template bodies. Scope follows the release implementation.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: parser order, comment parsers, and fixtures traced.
- Exact version or commit: 09d6b02946f54492f3d3dcb9729f5b792f220b40.
- Probe method: followed template alternatives and both closers.
- Probe input: Go/HTML comments, URL text, and raw script content.
- Observed result: only Go/HTML comment nodes matched.
- Conclusion and limits of the probe: malformed mode recovery needs fixtures.

### Representative examples

#### Line comment

~~~text
templ render() {
    // Not rendered.
    <p>Ready</p>
}
~~~

Expected region: `// Not rendered.`.

#### Block comment

~~~text
templ render() {
    <!-- rendered note -->
}
~~~

Expected region: `<!-- rendered note -->`.

#### Nested or contextual comment

~~~text
templ render() {
    <style>.x { background: url("https://host/a//b"); }</style>
    /* Go comment node */
}
~~~

Expected region: only `/* Go comment node */`.

### Adversarial boundaries

- Negative cases: URLs/plain text, Go quoted/raw strings, `{! ... !}`,
  HTML-like text in Go strings, and JS/CSS comments in raw elements.
- Malformed-input cases: unclosed Go/HTML blocks, internal invalid `--`,
  unclosed raw elements, unbalanced Go expressions, and stray closers.
- Line-ending and Unicode cases: LF, CRLF, EOF Go line, Unicode HTML/Go payload,
  and exact byte slices around mode transitions.
- Version or dialect counterexamples: generated `_templ.go` and comments
  in embedded client languages are outside the source key.
- Cleaner preservation cases: rendered HTML-comment bodies, Go comments inside
  templates, empty wrappers, indentation, and markers in raw elements.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `templ` with parser-mode recognition for
  Go line/block and HTML block nodes; do not combine global regex families.
- Deterministic tests to add: raw lookup, top-level/template Go comments, HTML
  comments, strings/URLs/raw script/style exclusions, invalid closers,
  line endings/EOF, exact slices, and all sanitizer wrappers.
- Remaining blocker: none.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01

## Terraform Template

### Identity and scope

- Raw dataset label: `Terraform Template` (9,229 files; 11,901,854 tokens)
- Proposed registry key: `terraform_template`
- Existing family or aliases checked: global `jsonnet_style`/`hcl`;
  rejected because standalone template literal regions do not recognize HCL
  comments.
- Classification: `template`
- Versions or releases checked: HashiCorp HCL v2.24.0, commit
  `6b5068090eef06b1f127f61529db5ba0be7ed343`.
- Dialects checked: standalone HCL templates parsed by
  `hclsyntax.ParseTemplate`/`LexTemplate`, corresponding to
  `.tftpl`.
- Intended support scope: HCL `TokenComment` regions inside template
  interpolation and directive expression modes.
- Explicitly excluded scope: literal template text, Terraform `.tf`
  configuration files, comments in rendered output, and comments in languages
  emitted by the template.

### Syntax contract

- Line comments: `#` and `//` inside active `${...}`
  interpolation or `%{...}` directive expression context only.
- Block comments: non-nested `/* ... */` in those expression contexts.
- Nested comments: unsupported; the first `*/` closes.
- Termination at newline, delimiter, or EOF: line comments accept an optional
  LF/CRLF terminator and stop at EOF; block comments require a closer.
- Inline use: valid inside HCL expression/directive mode. A same-line line
  comment can consume the expected closing brace and make the template invalid.
- Adjacent-line grouping: valid only while expression mode remains active and
  the surrounding template is structurally valid.
- Unclosed delimiter behavior: unclosed block or interpolation yields invalid
  tokens/diagnostics and must not be accepted as a complete comment.
- Lexical or structural context: `LexTemplate` starts
  `scanTemplate`; bare text becomes `TokenStringLit`. Only
  interpolation/control actions call the normal HCL scanner.
- Conflicts with strings, operators, directives, or embedded languages:
  `#`, URLs, and block-looking text in bare template output are literal;
  quoted strings inside HCL expressions shield markers; escaped
  `$${` and `%%{` do not open code mode.
- Sanitizer line wrappers: context-selected `("#", "")` or
  `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: remove only verified expression-mode
  wrappers and preserve bare output text, trim markers, Unicode, and layout.

### Evidence

- Official documentation permalink:
  [HCL native syntax comments specification](https://github.com/hashicorp/hcl/blob/6b5068090eef06b1f127f61529db5ba0be7ed343/hclsyntax/spec.md#comments-and-whitespace)
- Documentation version and relevant section: v2.24.0, lines 66-88; comments
  cannot begin in template literals except inside interpolation/directive.
- Official implementation or grammar permalink:
  [HCL scanner template modes](https://github.com/hashicorp/hcl/blob/6b5068090eef06b1f127f61529db5ba0be7ed343/hclsyntax/scan_tokens.rl#L249-L291)
- Implementation version, file, and relevant symbol: commit above,
  `bareTemplate`, `beginTemplateInterp`,
  `beginTemplateControl`, and `Comment` at lines 68-82.
- Conformance test or official example permalink:
  [HCL template parser tests](https://github.com/hashicorp/hcl/blob/6b5068090eef06b1f127f61529db5ba0be7ed343/hclsyntax/expression_template_test.go)
- Secondary source, if needed:
  [LexTemplate public API](https://github.com/hashicorp/hcl/blob/6b5068090eef06b1f127f61529db5ba0be7ed343/hclsyntax/public.go#L180-L190)
- Evidence conflicts or gaps: Terraform's `.tftpl` label carries no
  embedded output-language metadata; those rendered-language comments remain
  literal by design.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned Ragel scanner and public API traced.
- Exact version or commit: 6b5068090eef06b1f127f61529db5ba0be7ed343.
- Probe method: followed template entry and transitions to normal mode.
- Probe input: bare hash/URL plus comments in interpolation/directive spans.
- Observed result: bare markers are literals; expression markers are comments.
- Conclusion and limits of the probe: add a runtime token-offset test.

### Representative examples

#### Line comment

~~~text
${
  # choose the display name
  var.name
}
~~~

Expected region: `# choose the display name`.

#### Block comment

~~~text
${var.name /* normalized upstream */}
~~~

Expected region: `/* normalized upstream */`.

#### Nested or contextual comment

~~~text
# literal heading
${var.name // expression note
}
~~~

Expected region: only `// expression note`; the first hash is output text.

### Adversarial boundaries

- Negative cases: bare hash/slash/block text, URLs, `$${` and
  `%%{` escapes, markers in expression strings, and comments belonging to
  the rendered target language.
- Malformed-input cases: unclosed interpolation/directive/block/string,
  line comment swallowing a close brace, mismatched directives, and stray
  braces.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF comments, Unicode
  literal/expression content, and exact offsets across scanner-mode changes.
- Version or dialect counterexamples: do not alias `terraform_template`
  to global HCL or apply this contextual restriction to ordinary `.tf`.
- Cleaner preservation cases: literal marker text, trim modifiers, both line
  wrappers, block wrappers, nested braces, indentation, and Unicode.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add `terraform_template` with a template-mode
  scanner that delegates recognized interpolation/directive spans to HCL
  comment extraction.
- Deterministic tests to add: raw lookup, literal negatives, interpolation and
  control comments, all three forms, escapes, nested braces/strings, malformed
  boundaries, line endings/EOF, exact slices, and contextual cleaning.
- Remaining blocker: none.
- Reviewer: `/root/review_batches_08_09`
- Review date: 2026-08-01
