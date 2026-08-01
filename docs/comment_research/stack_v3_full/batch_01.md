# Stack v3 Full Comment Research: batch_01

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics aggregated from
  `files[].language`
- Researcher or agent: `/root/research_batch_01`
- Review status: `reviewed`

The registry lookup was checked for every raw label at the feature-branch state
used for this research. None of the ten labels currently resolves.

## Circom

### Identity and scope

- Raw dataset label: `Circom` (59,497 files)
- Proposed registry key: `circom`
- Existing family or aliases checked: `java` / `c_style`; its generic literal
  masking conflicts with Circom's preprocessing pass, which recognizes comment
  delimiters even inside marker-looking quoted source.
- Classification: `language`
- Versions or releases checked: Circom 2 documentation and compiler 2.2.3 at
  commit `a100faedb1c62d4d3e1463f8a3f88342d82351cd`
- Intended support scope: Circom 2 source files.
- Explicitly excluded scope: generated C++, WebAssembly, and R1CS output.

### Syntax contract

- Line comments: `//` through the next LF or EOF.
- Block comments: `/*` through the first `*/`.
- Nested comments: no. An inner `/*` has no nesting effect.
- Inline use: yes, for both forms.
- Adjacent-line grouping: yes for consecutive `//` lines.
- Unclosed delimiter behavior: an unclosed block is compiler error `P1005`;
  an EOF-terminated line comment is accepted.
- Lexical or structural context: the compiler's preprocessing pass recognizes
  delimiters before parsing and does not maintain a string state.
- Conflicts: `/` is an operator unless immediately followed by `/` or `*`.
  Marker-looking text in an include/version string is still consumed by the
  current preprocessor and must not be documented as protected string content.
- Sanitizer wrappers: strip `//`, or matching `/*` and `*/`, while preserving
  the body and physical line structure.

### Evidence

- Official documentation permalink:
  [Circom comment lines](https://github.com/iden3/circom/blob/a100faedb1c62d4d3e1463f8a3f88342d82351cd/mkdocs/docs/circom-language/comment-lines.md)
- Official implementation permalink:
  [parser preprocessing state machine](https://github.com/iden3/circom/blob/a100faedb1c62d4d3e1463f8a3f88342d82351cd/parser/src/parser_logic.rs#L9-L85)
- Relevant implementation symbols: `preprocess`, states 0 (normal), 1 (line),
  and 2 (block).
- Evidence conflicts or gaps: documentation describes C/C++-like comments but
  does not mention that preprocessing is not string-aware; the implementation
  is authoritative for that boundary.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: source state machine and official error path inspected;
  no local Circom binary was built.
- Probe conclusion: source inspection proves first-close, non-nested behavior,
  LF/EOF line termination, and rejection of unclosed blocks.

### Representative examples

```text
template Example() {
    signal input in; // public input
    /* constrain the output */
    out <== in;
}
```

### Adversarial boundaries

- Negative cases: division, `a / *b`, and a slash at EOF.
- Malformed cases: `/* outer /* inner */ tail */` closes at the inner `*/`;
  `/* never closed` is an error and should not become a normal complete match.
- Line endings: test LF and CRLF source slices and a line comment at EOF.
- Cleaner preservation: retain comment text and blank lines; never consume the
  following Circom statement.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: create canonical `circom` with the same non-nested
  delimiters as C style but an explicit no-literal-protection scan policy that
  mirrors `preprocess`. Do not add it to `c_style`, because that family masks
  quoted ranges and would miss source the Circom preprocessor consumes.
- Deterministic tests to add: line, inline, block, first-close, EOF line,
  unclosed block, slash operator, and raw-string-marker behavior.
- Remaining blocker: none.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Clue

### Identity and scope

- Raw dataset label: `Clue` (16,665 files)
- Proposed registry key: `clue`
- Existing family or aliases checked: `java` / `c_style`; rejected because
  current Clue accepts an unclosed block through EOF and protects quoted text.
- Classification: `language`
- Versions or releases checked: Clue 3.4.7 at commit
  `78ce10c1d7a985b294ce7d08ef03565cc956e3c1`
- Intended support scope: `.clue` source handled by the 3.4.7 preprocessor.
- Explicitly excluded scope: emitted Lua and preprocessor debug output.

### Syntax contract

- Line comments: `//` through LF or EOF.
- Block comments: `/*` through the first `*/`.
- Nested comments: no.
- Inline use: yes.
- Adjacent-line grouping: yes for consecutive `//` lines.
- Unclosed delimiter behavior: the preprocessor has no EOF error for its
  `Multi` state, so an unclosed `/*` consumes through EOF in 3.4.7.
- Lexical context: single-quoted, double-quoted, and backtick strings are
  protected, including escaped matching quote characters.
- Conflicts: division and multiplication operators are not comments; `//` and
  `/*` inside any supported quote form are string data.
- Sanitizer wrappers: strip `//` or `/*`/`*/`; for the accepted EOF block strip
  only the opening wrapper and preserve all body text.

### Evidence

- Official documentation permalink:
  [Clue README syntax summary](https://github.com/ClueLang/Clue/blob/78ce10c1d7a985b294ce7d08ef03565cc956e3c1/README.md#general-syntax-differences)
- Official implementation permalink:
  [comment and string states](https://github.com/ClueLang/Clue/blob/78ce10c1d7a985b294ce7d08ef03565cc956e3c1/core/src/preprocessor.rs#L97-L231)
- String implementation permalink:
  [`read_string`](https://github.com/ClueLang/Clue/blob/78ce10c1d7a985b294ce7d08ef03565cc956e3c1/core/src/preprocessor.rs#L314-L343)
- Evidence conflicts or gaps: the README does not define malformed EOF
  behavior. The state machine has an unterminated-string error but no
  unterminated-comment check.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned source inspection; a runtime probe could not be
  run because `cargo` is unavailable in this environment.
- Probe conclusion: the absence of an EOF check after the main preprocessing
  loop is the basis for the EOF-block contract and should receive a regression
  test before implementation.

### Representative examples

```text
local url = "https://example.test/a/*literal*/"
// compile this branch
/* block note */
print(url)
```

### Adversarial boundaries

- Negative cases: all three quote forms containing `//` and `/*...*/`, escaped
  quotes, `/` division, `*` multiplication, and `//` in a quoted URL.
- Malformed cases: unclosed block to EOF, stray `*/`, and unclosed strings.
- Line endings: LF, CRLF, EOF line comment, and EOF block comment.
- Cleaner preservation: preserve every byte after an unclosed `/*`; do not
  discard the final source line merely because no closing wrapper exists.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `clue` with a quote-aware scanner
  for `//`, non-nested `/*...*/`, and the accepted EOF block.
- Deterministic tests to add: all quote forms, escaped quotes, nested-looking
  block, unclosed block, EOF line, operators, sanitizer EOF preservation.
- Remaining blocker: none. The pinned state machine has no final `Multi` check
  and blanks every remaining byte, so the commit-scoped contract treats an
  unclosed block as consuming through EOF; retain a deterministic regression
  test in case the compiler later changes this behavior.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Cpp-ObjDump

### Identity and scope

- Raw dataset label: `Cpp-ObjDump` (15 files)
- Proposed registry key: `cpp_objdump` only for inventory accounting, not as an
  extraction family.
- Existing family or aliases checked: `ObjDump`, `C-ObjDump`, C++, and assembly.
- Classification: `generated-format`
- Versions or releases checked: go-enry commit
  `71719e4bdde528496011d030354a97b7f3ed4ff6`, generated from Linguist commit
  `537297cdae3ab05f8d5dd1c03627a5bd73707b19`; GNU binutils 2.41 manual.
- Intended support scope: none; this label is generated textual disassembly.
- Explicitly excluded scope: comments from interleaved C++ source and
  target-specific assembly comment conventions.

### Syntax contract

- Line comments, block comments, nesting, wrappers, and grouping: `unsupported`.
  Registry lookup, extraction, and cleaning must raise `NotImplementedError`;
  this disposition does not install a silent no-comment family.
- Lexical context: go-enry classifies the extensions `.cppobjdump`,
  `.c++-objdump`, `.c++objdump`, `.cpp-objdump`, and `.cxx-objdump` as `data`
  with TextMate scope `objdump.x86asm`.
- Conflicts: GNU `objdump -S` can intermix source; `--source-comment[=txt]`
  accepts an arbitrary prefix and defaults to `# `. That output decoration is
  invocation-specific, not a comment syntax for this generated format.
- Content preservation: no cleaning operation is defined. Callers must receive
  `NotImplementedError` rather than a result that could imply the format was
  safely analyzed.

### Evidence

- Classifier permalink:
  [go-enry Cpp-ObjDump metadata](https://github.com/go-enry/go-enry/blob/71719e4bdde528496011d030354a97b7f3ed4ff6/data/languageInfo.go#L2785-L2809)
- Official tool documentation:
  [GNU objdump 2.41](https://sourceware.org/binutils/docs-2.41/binutils/objdump.html)
- Relevant sections: `--disassemble`, `--source`, and `--source-comment`.
- Evidence conflicts or gaps: no fixed producer command is encoded in the
  dataset label, so no stable prefix can be inferred.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: metadata and producer documentation inspection only.
- Conclusion: the label identifies output data, and marker-like text is not a
  portable source-comment contract.

### Representative examples

```text
0000000000000000 <main>:
   0:  55                    push   %rbp
```

### Adversarial boundaries

- Negative cases: `#` generated by `--source-comment`, semicolons in assembly,
  C++ `//` in `-S` source, URLs/file paths, symbol names, and relocation text.
- Malformed-input cases: truncated dumps and mixed diagnostics remain data.
- Cleaner preservation: output must be byte-preserving because there are no
  accepted wrappers.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none; record the explicit inventory disposition.
- Deterministic tests to add: lookup, extraction, and sanitizer construction all
  remain `NotImplementedError` for marker-bearing disassembly fixtures.
- Remaining blocker: none.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## crontab

### Identity and scope

- Raw dataset label: `crontab` (28,029 files)
- Proposed registry key: `crontab`
- Existing family or aliases checked: `microsoft_visual_studio_solution` /
  `visual_studio_solution_style`; rejected because its regex accepts all
  non-newline Unicode whitespace, while Cronie's pinned parser skips only ASCII
  space and tab before checking `#`.
- Classification: `document-format`
- Versions or releases checked: Cronie at commit
  `5f9f16b5663becefdd0dd70df31c0ef5ac36f943`
- Intended support scope: user and system crontab files parsed by Cronie.
- Explicitly excluded scope: shell comments inside the command field and
  anacrontab syntax.

### Syntax contract

- Line comments: a line whose first non-space/tab character is `#`.
- Block and nested comments: unsupported.
- Termination: LF or EOF.
- Inline use: no. `#` after a cron command or environment assignment is data in
  that active line.
- Adjacent-line grouping: yes for consecutive comment-only lines.
- Unclosed behavior: not applicable.
- Conflicts: leading spaces/tabs are allowed; a shell fragment such as
  `* * * * * echo value # argument` is one command, not an inline crontab comment.
- Sanitizer wrapper: remove the leading indentation plus `#` wrapper while
  preserving content; do not touch active lines.

### Evidence

- Official implementation manual:
  [Cronie `crontab(5)`](https://github.com/cronie-crond/cronie/blob/5f9f16b5663becefdd0dd70df31c0ef5ac36f943/man/crontab.5#L25-L43)
- Official implementation:
  [`skip_comments`](https://github.com/cronie-crond/cronie/blob/5f9f16b5663becefdd0dd70df31c0ef5ac36f943/src/misc.c#L416-L455)
- Documentation and code both require `#` as the first nonblank character and
  reject the concept of an inline comment.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned parser loop inspected; no local Cronie build.
- Conclusion: whitespace-aware full-line matching is sufficient and must be
  anchored to the physical line.

### Representative examples

```text
  # rotate every night
0 0 * * * rotate --tag '#keep'
```

### Adversarial boundaries

- Negative cases: `MAILTO=user#team`, command arguments containing `#`, quoted
  shell hashes, and a hash after the schedule fields.
- Malformed cases: whitespace-only final line and comment at EOF.
- Line endings: LF and CRLF.
- Cleaner preservation: never strip command text after `#` on an active line.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: create canonical `crontab` with a physical-line
  pattern anchored after ASCII space/tab only. Do not alias the broader Visual
  Studio solution family.
- Deterministic tests to add: indented/full-line comments, inline negative cases,
  command strings, CRLF, EOF, and grouped lines.
- Remaining blocker: none.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Cylc

### Identity and scope

- Raw dataset label: `Cylc` (1,099 files)
- Proposed registry key: `cylc`
- Existing family or aliases checked: `ini`; rejected because Cylc supports
  trailing comments plus single, double, and triple-quoted protected values.
- Classification: `document-format`
- Versions or releases checked: Cylc 8.6 documentation and `cylc-flow` commit
  `4ae32d5218fdfa87f26f200ca3659e1e1ade4276`
- Intended support scope: the native `.cylc` / `flow.cylc` configuration layer.
- Explicitly excluded scope: Jinja2 `{#...#}` comments, the `#!jinja2` selector,
  and shell/Python comments inside string-valued settings.

### Syntax contract

- Line comments: `#` after leading whitespace on a comment-only line.
- Inline comments: `#` after a section heading or outside a setting's quoted
  value; for an unquoted typed value the first `#` begins the trailing comment.
- Block and nested comments: unsupported in native Cylc syntax.
- Termination: physical line or EOF.
- Adjacent-line grouping: yes for consecutive native `#` comment lines.
- Lexical context: single, double, triple-single, and triple-double quoted values
  protect internal hashes, including whole lines of embedded shell script.
- Conflicts: `#!jinja2` is a preprocessing directive, not a comment; `%include`
  is a directive; Jinja and embedded script syntax are separate layers.
- Sanitizer wrapper: remove the recognized `#`, preserve comment text, and do
  not alter protected multiline values.

### Evidence

- Official documentation:
  [Cylc 8.6 file format](https://cylc.github.io/cylc-doc/stable/html/reference/config/file-format.html)
- Official implementation design:
  [Parsec README](https://github.com/cylc/cylc-flow/blob/4ae32d5218fdfa87f26f200ca3659e1e1ade4276/cylc/flow/parsec/README.md#design--implementation)
- Parser permalink:
  [line, heading, and quote expressions](https://github.com/cylc/cylc-flow/blob/4ae32d5218fdfa87f26f200ca3659e1e1ade4276/cylc/flow/parsec/fileparse.py#L69-L121)
- Validation permalink:
  [quoted-value comment handling](https://github.com/cylc/cylc-flow/blob/4ae32d5218fdfa87f26f200ca3659e1e1ade4276/cylc/flow/parsec/validate.py#L54-L73)
- Evidence conflicts or gaps: the high-level docs say comments follow `#`; the
  parser and validator define the necessary quote and section context.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: official parser tests and expressions inspected; no
  separate runtime probe.
- Conclusion: a raw `#.*` regex would corrupt embedded scripts and quoted values.

### Representative examples

```text
# native comment
[runtime]
    [[job]]  # native trailing comment
        script = """
            echo '# embedded shell data'
        """
```

### Adversarial boundaries

- Negative cases: `#!jinja2`, `{# template comment #}`, hashes inside every
  quote form, triple-quoted shell comments, and URL fragments.
- Malformed cases: unclosed triple quote and a dangling continuation.
- Line endings: LF/CRLF and EOF comment.
- Cleaner preservation: retain embedded script lines exactly; strip only the
  native wrapper selected outside quotes.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: canonical `cylc`, a quote-aware native-layer
  extractor, `#` sanitizer wrapper, and documented exclusions.
- Deterministic tests to add: all quote forms, headings, unquoted values,
  `#!jinja2`, Jinja comments, embedded shell, CRLF, and malformed triple quotes.
- Remaining blocker: none.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Cypher

### Identity and scope

- Raw dataset label: `Cypher` (30,610 files)
- Proposed registry key: `cypher`
- Existing family or aliases checked: `java` / `c_style`
- Classification: `language`
- Versions or releases checked: openCypher 9, Neo4j Cypher 25 documentation,
  and Neo4j language-support commit
  `4949084d0916a756d41c6c5644abc0a42624c3f7`
- Intended support scope: openCypher and Neo4j Cypher query text.
- Explicitly excluded scope: shell commands, TCK/Gherkin `#` comments, and
  comments in a host-language string containing a Cypher query.

### Syntax contract

- Line comments: `//` through CR, LF, or EOF.
- Block comments: non-nested `/*` through the first `*/`.
- Inline use: yes.
- Adjacent-line grouping: yes for consecutive `//` lines.
- Unclosed block behavior: lexer error; it is not a complete comment token.
- Lexical context: single- and double-quoted string literals and backtick-quoted
  identifiers protect delimiter-looking text.
- Conflicts: `/` is division; relationship punctuation such as `--` is not a
  comment; `//` inside a URL/string is data.
- Sanitizer wrappers: standard `//` and `/*...*/`, preserving body text.

### Evidence

- Official documentation:
  [Neo4j Cypher comments](https://neo4j.com/docs/cypher-manual/current/syntax/comments/)
- Official implementation:
  [Cypher 25 lexer](https://github.com/neo4j/cypher-language-support/blob/4949084d0916a756d41c6c5644abc0a42624c3f7/packages/language-support/src/antlr-grammar/Cypher25Lexer.g4#L17-L58)
- Conformance/example evidence:
  [openCypher adopted CIPs](https://github.com/opencypher/openCypher/tree/677cbafabb8c3c5eed458fd3b1ec0daec8d67d23/cip/1.adopted)
- The lexer uses a non-greedy block rule and distinct string tokens; the manual
  explicitly demonstrates that `//` inside a string is not a comment.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned ANTLR lexer inspected; no Neo4j server probe.
- Conclusion: syntax and malformed behavior match the non-nested C-style family.

### Representative examples

```text
MATCH (n) // select all nodes
WHERE n.url = 'https://example.test/a/*literal*/'
/* retain only active nodes */
RETURN n
```

### Adversarial boundaries

- Negative cases: both string quote forms, escaped quotes, backtick identifiers,
  division, relationship punctuation, URLs, and Gherkin `#` lines.
- Malformed cases: nested-looking blocks close at the first `*/`; unclosed block.
- Line endings: CR, LF, CRLF, and EOF line comments.
- Cleaner preservation: do not consume a following clause or string content.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `cypher` to the non-nested `c_style` family.
- Deterministic tests to add: official examples, string/backtick negatives,
  first-close behavior, operators, EOF line, and unclosed block.
- Remaining blocker: none.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## D-ObjDump

### Identity and scope

- Raw dataset label: `D-ObjDump` (7 files)
- Proposed registry key: `d_objdump` only for inventory accounting.
- Existing family or aliases checked: `ObjDump`, `C-ObjDump`, D, and assembly.
- Classification: `generated-format`
- Versions or releases checked: the same pinned go-enry/Linguist metadata and
  GNU binutils 2.41 used for `Cpp-ObjDump`.
- Intended support scope: none.
- Explicitly excluded scope: D source comments interleaved by `objdump -S` and
  target-assembly comment conventions.

### Syntax contract

- Line comments, block comments, nesting, grouping, and wrappers: `unsupported`.
  Registry lookup, extraction, and cleaning must raise `NotImplementedError`;
  this disposition does not install a silent no-comment family.
- Lexical context: go-enry classifies `.d-objdump` as `data` with TextMate scope
  `objdump.x86asm`; it is not D source.
- Conflicts: disassembly can contain target-specific punctuation and optional,
  arbitrarily prefixed interleaved source text.
- Content preservation: no cleaning operation is defined. Callers must receive
  `NotImplementedError` rather than a result that could imply the generated
  format was safely analyzed.

### Evidence

- Classifier permalink:
  [go-enry D-ObjDump metadata](https://github.com/go-enry/go-enry/blob/71719e4bdde528496011d030354a97b7f3ed4ff6/data/languageInfo.go#L3077-L3095)
- Official producer documentation:
  [GNU objdump 2.41](https://sourceware.org/binutils/docs-2.41/binutils/objdump.html)
- Evidence conflicts or gaps: no fixed invocation, architecture, or source
  prefix is represented by the dataset label.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: metadata and producer documentation inspection only.
- Conclusion: D syntax must not be inherited by a generated dump label.

### Representative examples

```text
Disassembly of section .text:
00000000 <_Dmain>:
```

### Adversarial boundaries

- Negative cases: D `//` or `/+...+/` in interleaved source, assembler `#` or
  `;`, symbol names, paths, and arbitrary `--source-comment` prefixes.
- Malformed cases: truncated output and diagnostics remain data.
- Cleaner preservation: byte-preserving no-op.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none; record the explicit inventory disposition.
- Deterministic tests to add: lookup, extraction, and sanitizer construction all
  remain `NotImplementedError` for marker-bearing disassembly fixtures.
- Remaining blocker: none.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## D2

### Identity and scope

- Raw dataset label: `D2` (10,574 files)
- Proposed registry key: `d2`
- Existing family or aliases checked: hash-line families and triple-quote string
  formats; none has D2's structural block-comment contract.
- Classification: `language`
- Versions or releases checked: D2 documentation and commit
  `2446e247b6d7d5b9395a1ae8ad1e9c2641231035`
- Intended support scope: D2 diagram source parsed by the official Go parser.
- Explicitly excluded scope: imported files' contents, Markdown/code embedded in
  D2 values, and rendered SVG comments.

### Syntax contract

- Line comments: `#` through LF or EOF, including inline comments after a node.
- Block comments: `"""` through the next `"""`, but only where the parser is
  beginning a map node.
- Nested comments: no.
- Inline use: line comments yes; block comments can occupy a map-node position
  and may occur on one line.
- Adjacent-line grouping: the official parser combines `#` lines separated by
  exactly one newline, allowing indentation, and stops across a blank line.
- Unclosed delimiter behavior: an unclosed triple-quote block is a parse error.
- Lexical context: hashes and triple quotes inside quoted strings or block-string
  values are data, not native comments.
- Sanitizer wrappers: strip one leading `#` per physical line, or matching
  triple-quote wrappers; preserve indentation and comment body.

### Evidence

- Official documentation:
  [D2 comments](https://d2lang.com/tour/comments/)
- Official implementation:
  [`parseComment` and `parseBlockComment`](https://github.com/terrastruct/d2/blob/2446e247b6d7d5b9395a1ae8ad1e9c2641231035/d2parser/parse.go#L517-L633)
- Structural dispatch:
  [`parseMapNode`](https://github.com/terrastruct/d2/blob/2446e247b6d7d5b9395a1ae8ad1e9c2641231035/d2parser/parse.go#L466-L515)
- Official parser examples:
  [`TestParse`](https://github.com/terrastruct/d2/blob/2446e247b6d7d5b9395a1ae8ad1e9c2641231035/d2parser/parse_test.go#L26-L95)
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: parser dispatch, grouping loop, and EOF error paths
  inspected; no separate D2 binary probe.
- Conclusion: triple quotes cannot be registered as an unconditional delimiter.

### Representative examples

```text
# diagram note
client -> server # request path
"""
Block note for maintainers.
"""
```

### Adversarial boundaries

- Negative cases: quoted labels containing `#`, block-string content, hashes in
  imported paths, and `"""` outside a map-node position.
- Malformed cases: one/two quotes, unclosed triple quote, and four or more quotes.
- Line endings: LF/CRLF, Unicode indentation/content, and EOF line comments.
- Cleaner preservation: preserve interior hashes/quotes and blank lines; do not
  merge groups separated by a blank line.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: canonical `d2`, structural scanner for map-node
  `"""..."""`, quote-aware `#`, and both sanitizer wrappers.
- Deterministic tests to add: parser examples, inline/grouping behavior, blank
  separation, quoted negatives, malformed quote counts, CRLF, and unclosed block.
- Remaining blocker: none.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Daslang

### Identity and scope

- Raw dataset label: `Daslang` (24,728 files)
- Proposed registry key: `daslang`
- Existing family or aliases checked: `boogie` / `boogie_style`, which has the
  same `//` plus nested `/*...*/` contract; `c_style` is not sufficient.
- Classification: `language`
- Versions or releases checked: current Daslang reference and compiler commit
  `540e3b51280685ae1bc395d4173f962ebbc792bb`
- Intended support scope: Daslang (formerly daScript) source in both indentation
  and brace/parser modes.
- Explicitly excluded scope: generated C++ and reader-macro payload semantics.

### Syntax contract

- Line comments: `//` through LF or EOF.
- Block comments: `/*...*/` with recursive nesting.
- Inline use: yes.
- Adjacent-line grouping: yes for consecutive `//` lines.
- Unclosed delimiter behavior: an EOF inside a block is compiler error
  `comment_contains_eof`; EOF line comment is accepted.
- Lexical context: comment rules apply in normal/indent lexer states, not string
  states. A stray `*/` in normal source is an explicit lexer error.
- Conflicts: `/` and `*` operators, strings, reader constants, and the special
  `#row,column,"file"#` line directive are not comments.
- Sanitizer wrappers: strip `//` or the outermost `/*...*/`; preserve nested
  delimiters as comment content.

### Evidence

- Official reference:
  [Daslang lexical structure](https://github.com/GaijinEntertainment/daScript/blob/540e3b51280685ae1bc395d4173f962ebbc792bb/doc/source/reference/language/lexical_structure.rst#L278-L303)
- Official compiler lexer:
  [brace-mode comment states](https://github.com/GaijinEntertainment/daScript/blob/540e3b51280685ae1bc395d4173f962ebbc792bb/src/parser/ds2_lexer.lpp#L102-L161)
- Alternate official lexer:
  [indent-mode comment states](https://github.com/GaijinEntertainment/daScript/blob/540e3b51280685ae1bc395d4173f962ebbc792bb/src/parser/ds_lexer.lpp#L100-L183)
- Both lexers increment depth on inner `/*`, decrement on `*/`, reject stray
  close delimiters, and error at EOF with positive depth.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: both Flex lexer sources and official reference example
  inspected; no local compiler build.
- Conclusion: the nested contract is explicit and consistent across both modes.

### Representative examples

```text
var x = 42 // line note
/* outer
   /* nested note */
   outer tail
*/
```

### Adversarial boundaries

- Negative cases: quoted delimiter text, division/multiplication, the line
  directive, and reader-macro bodies.
- Malformed cases: stray `*/`, unclosed outer block, and nested unclosed block.
- Line endings: LF/CRLF, EOF line comment, and Unicode body text.
- Cleaner preservation: remove only the outer nested wrapper and retain nested
  wrapper text/body in source order.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `daslang` to `boogie_style`, whose nested
  delimiter and slash-line metadata match.
- Deterministic tests to add: nested depth, strings/operators/directive negatives,
  stray close, unclosed block, EOF line, both layout modes, and sanitizer nesting.
- Remaining blocker: none.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01

## Dotenv

### Identity and scope

- Raw dataset label: `Dotenv` (9,562,902 files)
- Proposed registry key: `dotenv`
- Existing family or aliases checked: `shell`, `ini`, and generic hash-line
  families; rejected because inline hashes depend on quote state and may occur
  without preceding whitespace.
- Classification: `document-format`
- Versions or releases checked: Node dotenv 17.4.2 at commit
  `c0e32b8267b69a438bc0cc31345f73b5e2f037db`
- Intended support scope: `.env` grammar implemented by Node dotenv >=15,
  including `export`, quoted multiline values, and inline comments.
- Explicitly excluded scope: shell command files, dotenv interpolation extensions,
  and other ecosystem parsers whose grammar conflicts with Node dotenv.

### Syntax contract

- Line comments: after optional spaces/tabs, `#` through the physical line end.
- Inline comments: the first `#` in an unquoted value, with no whitespace
  requirement, or `#` after a closed quoted value.
- Block and nested comments: unsupported.
- Termination: CR, LF, CRLF, or EOF; the implementation normalizes CR variants.
- Adjacent-line grouping: yes for consecutive comment-only lines.
- Unclosed delimiter behavior: no comment delimiter is unclosed. An unclosed
  quote falls back to unquoted parsing, so a subsequent `#` starts a comment.
- Lexical context: single, double, and backtick quoted values protect internal
  hashes; matching quotes may be backslash-escaped. Quoted values may span lines.
- Conflicts: a hash inside any closed quoted value is data. An unquoted URL
  fragment or secret containing `#` is a comment boundary under >=15 behavior.
- Sanitizer wrapper: remove `#` only after quote-aware classification and
  preserve all comment body text and original line endings.

### Evidence

- Official documentation:
  [dotenv comments](https://github.com/motdotla/dotenv/blob/c0e32b8267b69a438bc0cc31345f73b5e2f037db/README.md#comments)
- Official implementation:
  [classic and fast parsers](https://github.com/motdotla/dotenv/blob/c0e32b8267b69a438bc0cc31345f73b5e2f037db/lib/main.js#L12-L215)
- Official conformance tests:
  [comment and quote cases](https://github.com/motdotla/dotenv/blob/c0e32b8267b69a438bc0cc31345f73b5e2f037db/tests/test-parse.js#L56-L66)
- Documentation explicitly calls inline comments a breaking change from v15;
  the two current parsers are tested for parity.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned implementation and its parity/conformance tests
  inspected; Node runtime probe was unnecessary for documented cases.
- Conclusion: delimiter-only regex extraction would falsely match hashes inside
  three quote modes and multiline secrets.

### Representative examples

```text
# deployment secret
TOKEN=abc#this-is-a-comment
HASH="abc#this-is-data" # trailing comment
MULTI='line one
# still quoted data
line three'
```

### Adversarial boundaries

- Negative cases: `#` inside single/double/backtick values, escaped closing
  quotes, multiline quoted hashes, and an empty quoted value.
- Positive edge cases: no space before inline `#`, comment-only indentation,
  comment after each quote form, empty unquoted value followed by `#`, and EOF.
- Malformed cases: unclosed quotes with a later hash and invalid assignment lines.
- Line endings: lone CR, LF, CRLF, Unicode values/comment bodies, and BOM input.
- Cleaner preservation: never remove a hash-bearing secret inside quotes; retain
  comment body after removing only the selected wrapper.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: canonical `dotenv`, quote-aware line scanner,
  `#` sanitizer wrapper, and scope note for >=15 behavior.
- Deterministic tests to add: official cases, three quote modes, multiline values,
  escaped quotes, no-space inline marker, all line endings, BOM, malformed quotes,
  and sanitizer content preservation.
- Remaining blocker: none for the documented >=15 scope; older parser behavior
  is intentionally excluded.
- Reviewer: /root/review_batches_00_01
- Review date: 2026-08-01
