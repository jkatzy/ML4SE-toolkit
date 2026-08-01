# Stack v3 Full Comment Research: inventory discrepancy 00

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics table, aggregated
  from `files[].language`
- Researcher or agent: `/root/research_inventory_discrepancy`
- Review status: `reviewed`

All five raw labels were checked against `LANGUAGE_SYNTAX` on 2026-08-01.
Neither the exact lowercase label nor its Stack-style normalized candidate
currently resolves. The identity checks below use go-enry's pinned upstream
Linguist revision `537297cdae3ab05f8d5dd1c03627a5bd73707b19` so that a
file extension alone is not treated as language evidence.

## Befunge

### Identity and scope

- Raw dataset label: `Befunge` (16,667 files; 222,859,325 tokens)
- Proposed registry key: `befunge`, reserved only; do not register it from this
  report.
- Existing family or aliases checked: no current family or alias resolves
  `befunge`. `brainfuck` and other esoteric languages do not share Befunge's
  two-dimensional execution semantics.
- Classification: `language`
- Versions or releases checked: Befunge-93 reference distribution commit
  `8fe4065c0415b6f6fa6f699798fa9b64737aadc1` (`rel_2_25`) and the
  Funge-98 final specification release `rel_1_0_2018_0522`, commit
  `a59df464b89cbcb68d01282f384f324d366a4cbc`.
- Dialects checked: Befunge-93 and two-dimensional Befunge-98. Unefunge-98,
  Trefunge-98, implementation extensions, and fingerprints are excluded.
- Intended support scope: unresolved. The Stack label and Linguist metadata
  identify `Befunge` and extensions `.befunge` and `.bf`, but carry no
  Befunge-93 versus Befunge-98 version signal.
- Explicitly excluded scope: `#` as a comment marker, arbitrary unsupported
  characters as comments, pre-directive lines accepted by particular
  interpreters, string-mode data, and cells skipped only because of dynamic
  control flow.

### Syntax contract

- Line comments: unsupported in the common Befunge-93/Befunge-98 contract.
- Block comments: unresolved for the unversioned label. Funge-98 defines `;`
  as the `Jump Over` marker and explicitly says it can insulate comments, but
  Befunge-93 does not define that instruction.
- Nested comments: no. A Funge-98 instruction pointer encountering `;` skips
  until the next `;` along its current direction; this is not recursive
  delimiter nesting.
- Termination at newline, delimiter, or EOF: not line-oriented. In Funge-98,
  termination is the next `;` cell encountered by the moving instruction
  pointer, potentially after a direction-dependent traversal and wrapping.
  The specifications do not establish a safe linear source-to-EOF fallback.
- Inline use: Funge-98 jump-over regions can occur beside executable cells on
  one row, but validity is execution-path dependent rather than line-context
  dependent.
- Adjacent-line grouping: unsupported. Physical adjacency does not imply a
  shared execution path in a two-dimensional playfield.
- Unclosed delimiter behavior: unresolved for static extraction. A missing
  second marker cannot safely consume a row or the remainder of the serialized
  file.
- Lexical or structural context: Befunge source is a two-dimensional playfield.
  The instruction pointer may move east, west, north, or south; Befunge is also
  self-modifying. In string mode, every encountered cell except `"` (and, in
  Funge-98, space) is pushed as data, so `;` inside a string is not `Jump Over`.
- Conflicts with strings, operators, directives, or embedded languages: `#` is
  the Befunge-93 bridge instruction, not a hash comment. `;` is ordinary
  unsupported input in Befunge-93 and data in string mode. The reference
  Befunge-93 interpreter also recognizes some whole-file pre-directives, which
  are implementation controls rather than source comments.
- Sanitizer line wrappers: none established.
- Sanitizer block wrappers: unresolved; do not strip `;` pairs under the raw
  `Befunge` label.
- Content-preservation expectations: until dialect and traversal semantics are
  resolved, return no inferred matches and preserve every source cell exactly.

### Evidence

- Dataset classifier permalink:
  [Linguist Befunge metadata](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L603-L610)
- Official Befunge-93 documentation permalink:
  [Befunge-93 reference documentation](https://github.com/catseye/Befunge-93/blob/8fe4065c0415b6f6fa6f699798fa9b64737aadc1/doc/Befunge-93.markdown#appendix-a-command-summary)
- Documentation version and relevant section: `rel_2_25`, Appendix A's
  exhaustive command summary. It defines `#` as bridge and contains no `;`
  comment or jump-over instruction.
- Official Befunge-93 implementation permalink:
  [reference interpreter dispatch](https://github.com/catseye/Befunge-93/blob/8fe4065c0415b6f6fa6f699798fa9b64737aadc1/src/bef.c#L469-L821)
- Implementation version, file, and relevant symbol: `rel_2_25`, `src/bef.c`,
  the string-mode branch and instruction `switch`; unsupported characters reach
  `default`, while `#` has its own bridge case.
- Official Funge-98 specification permalink:
  [Funge-98 flow control and Jump Over](https://github.com/catseye/Funge-98/blob/a59df464b89cbcb68d01282f384f324d366a4cbc/doc/funge98.markdown#flow-control)
- Conformance detail:
  [Funge-98 string mode](https://github.com/catseye/Funge-98/blob/a59df464b89cbcb68d01282f384f324d366a4cbc/doc/funge98.markdown#strings)
  establishes that marker-looking cells in a string are data.
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the official specifications agree about each
  version, but the dataset label does not say which version a file uses. Even
  after choosing Funge-98, a generic left-to-right delimiter matcher would not
  model instruction-pointer direction, string mode, or self-modification.
- Confidence: `unresolved`

### Implementation confirmation

- Implementation tested: pinned source inspection only; no executable
  interpreter probe was required to establish the version conflict.
- Exact version or commit: Befunge-93
  `8fe4065c0415b6f6fa6f699798fa9b64737aadc1`; Funge-98
  `a59df464b89cbcb68d01282f384f324d366a4cbc`.
- Probe method: compared the complete Befunge-93 command table and reference
  interpreter dispatch with Funge-98 `Jump Over` and string-mode clauses.
- Probe input:

```text
>;skipped in Befunge-98;1.@
>"a;b",@
>12#3..@
```

- Observed result: by specification, only the first snippet has a Funge-98
  jump-over region. The semicolon in the second snippet is string data, and
  `#` in the third is a one-cell bridge rather than a comment.
- Conclusion and limits of the probe: the evidence distinguishes the dialects
  and contexts but does not define a safe static contract for the raw dataset
  label.

### Representative examples

#### Funge-98 jump-over region

```text
>; satellite cells ;1.@
```

The cells from the first through second `;` are skipped only when an
instruction pointer reaches the first marker while moving east outside string
mode. This is not yet an accepted extraction example for `befunge`.

#### Befunge-93 bridge, not a comment

```text
>12#3..@
```

`#` skips one cell; neither it nor the skipped cell is comment scaffolding.

### Adversarial boundaries

- Negative cases: `;` inside string mode, `#` bridge, unsupported characters,
  semicolons stored or modified through `p`, and a semicolon reached while
  travelling west, north, or south.
- Malformed-input cases: one semicolon, multiple candidate closing semicolons,
  playfield wrapping, and a closing marker modified before traversal.
- Line-ending and Unicode cases: LF and CRLF serialization must not determine
  execution adjacency; non-ASCII bytes require an explicit implementation
  encoding policy before they can be classified.
- Version or dialect counterexamples: every Funge-98 semicolon example must be
  paired with Befunge-93, where `;` has no specified jump-over meaning.
- Cleaner preservation cases: until resolution, preserve `;`, `#`, strings,
  whitespace cells, row boundaries, and all skipped-looking content byte for
  byte.

### Decision

- Recommended action: `defer`
- Registry fields to change: none.
- Deterministic tests to add: keep raw and normalized `Befunge` lookup
  unsupported; retain explicit negatives for Befunge-93 `#` and Funge-98
  string-mode semicolons when a future implementation is proposed.
- Remaining blocker: establish the dialect/version represented by the dataset
  label and design a contiguous source-slice contract that is sound for
  direction-dependent Funge-98 `Jump Over` regions.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## C-ObjDump

### Identity and scope

- Raw dataset label: `C-ObjDump` (18 files; 9,660 tokens)
- Proposed registry key: `c_objdump` only for inventory accounting; do not
  register an extraction family.
- Existing family or aliases checked: `C`, `ObjDump`, `Cpp-ObjDump`,
  `D-ObjDump`, assembly families, and legacy no-op handling. C source syntax is
  not a valid alias for generated disassembly.
- Classification: `generated-format`
- Versions or releases checked: go-enry commit
  `71719e4bdde528496011d030354a97b7f3ed4ff6`, generated from Linguist
  `537297cdae3ab05f8d5dd1c03627a5bd73707b19`; GNU binutils 2.41.
- Dialects checked: GNU `objdump` disassembly output and optional `-S` source
  intermixing. Architecture-specific assembly syntaxes are excluded.
- Intended support scope: none; this label identifies generated textual data.
- Explicitly excluded scope: C comments in optionally interleaved source,
  target-assembler comment conventions, and an invocation-selected
  `--source-comment` prefix.

### Syntax contract

- Line comments: `unsupported`.
- Block comments: `unsupported`.
- Nested comments: `unsupported`.
- Termination at newline, delimiter, or EOF: not applicable.
- Inline use: unsupported.
- Adjacent-line grouping: unsupported.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: Linguist classifies `.c-objdump` as `data`
  with TextMate scope `objdump.x86asm`. GNU `objdump -S` may intermix source
  with disassembly, but the raw label does not encode producer options, target
  architecture, or whether a line is source or disassembly.
- Conflicts with strings, operators, directives, or embedded languages: GNU
  `--source-comment[=txt]` prefixes displayed source with arbitrary caller text
  and defaults to `# `. Assembly operands and annotations may also contain
  `#`, `;`, `/`, or `*` according to target and disassembler mode. None is a
  portable `C-ObjDump` source-comment wrapper.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: none.
- Content-preservation expectations: produce no matches and preserve the dump,
  diagnostics, addresses, instruction text, and any interleaved source exactly.

### Evidence

- Dataset classifier permalink:
  [Linguist C-ObjDump metadata](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L874-L880)
- Official producer documentation permalink:
  [GNU objdump 2.41](https://sourceware.org/binutils/docs-2.41/binutils/objdump.html)
- Documentation version and relevant sections: binutils 2.41, `-d` /
  `--disassemble`, `-S` / `--source`, and `--source-comment[=txt]`.
- Official implementation or grammar permalink: the producer manual is the
  authoritative output contract; there is no separate source-language grammar
  for `.c-objdump` data.
- Conformance test or official example permalink: the same manual specifies
  that `txt` is caller-selected and the default is `# `.
- Secondary source, if needed: none.
- Evidence conflicts or gaps: no fixed invocation is represented by the raw
  label, so marker-like lines cannot be assigned one stable meaning.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: metadata and producer-contract inspection only.
- Exact version or commit: GNU binutils 2.41; classifier revision
  `537297cdae3ab05f8d5dd1c03627a5bd73707b19`.
- Probe method: compared the data classification with the documented output
  switches and caller-controlled source prefix.
- Probe input:

```text
objdump -S --source-comment='arbitrary-prefix ' object-file
```

- Observed result: the official option contract permits the displayed source
  prefix to be changed and permits source to be absent entirely.
- Conclusion and limits of the probe: no delimiter can be derived from the
  label; target-specific output remains outside comment extraction.

### Representative examples

```text
0000000000000000 <main>:
   0:  55                    push   %rbp
# int main(void) { /* source note */ return 0; }
```

Even the final line may be invocation-decorated embedded source. Neither `#`
nor the C-looking block is a stable wrapper for the generated format.

### Adversarial boundaries

- Negative cases: `#` from the default source prefix, an arbitrary custom
  prefix, semicolons in target assembly, C `//` and `/*...*/` in interleaved
  source, URLs, symbol names, relocation annotations, and instruction bytes.
- Malformed-input cases: truncated dumps, mixed stderr diagnostics, and a
  partial interleaved source line remain data.
- Line-ending and Unicode cases: LF, CRLF, EOF without newline, demangled
  Unicode symbols, and non-UTF-8 bytes must all remain untouched.
- Version or dialect counterexamples: different target architectures and
  disassembler options must not select C or assembler comment families.
- Cleaner preservation cases: byte-preserving no-op for all marker-looking
  lines and embedded source text.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none; retain an explicit inventory disposition.
- Deterministic tests to add: lookup remains `NotImplementedError`; add a
  no-extraction disposition fixture containing `#`, `;`, `//`, `/*...*/`, and
  a custom source prefix.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Darcs Patch

### Identity and scope

- Raw dataset label: `Darcs Patch` (962 files; 2,828,741 tokens)
- Proposed registry key: `darcs_patch` only for inventory accounting; do not
  register an extraction family.
- Existing family or aliases checked: unified diff, patch metadata, email
  bundles, Haskell, and legacy no-op handling. None provides a source-comment
  contract for Darcs patch data.
- Classification: `generated-format`
- Versions or releases checked: Darcs 2.18.5 source distribution, published
  2025-01-09, tarball SHA-256
  `e310692989e313191824f532a26c5eae712217444214266503d5eb5867f951ab`;
  pinned Linguist revision
  `537297cdae3ab05f8d5dd1c03627a5bd73707b19`.
- Dialects checked: Darcs named patches and V1 primitive textual patch forms.
  Darcs 1 versus Darcs 2 patch semantics do not create a comment wrapper.
- Intended support scope: none; `.darcspatch` and `.dpatch` are classified as
  `data`.
- Explicitly excluded scope: the named patch's free-form description (called a
  long comment by Darcs UI documentation), `Ignore-this:` identity salt,
  email prose around a bundle, Debian `dpatch` scripts, and source comments
  carried as added or removed hunk payload.

### Syntax contract

- Line comments: `unsupported`.
- Block comments: `unsupported`.
- Nested comments: `unsupported`.
- Termination at newline, delimiter, or EOF: not applicable to comments.
- Inline use: unsupported.
- Adjacent-line grouping: unsupported.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: the official primitive parser consumes
  commands such as `hunk`, `replace`, `binary`, `addfile`, `rmfile`, `adddir`,
  `rmdir`, `move`, and `changepref`. Within a hunk, lines beginning with a
  space, `-`, or `+` are context or payload. Those prefixes are structural data,
  not removable comments.
- Conflicts with strings, operators, directives, or embedded languages: hunk
  payload can contain arbitrary source text and therefore every comment marker
  supported by this package. Patch descriptions and email text are metadata,
  not lexically wrapped source comments. `Ignore-this:` is parsed identity
  material despite its name.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: none.
- Content-preservation expectations: produce no matches. Preserve patch
  metadata and every hunk/context/payload byte because deleting a marker-looking
  region changes the patch being represented.

### Evidence

- Dataset classifier permalink:
  [Linguist Darcs Patch metadata](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L1652-L1662)
- Official documentation permalink:
  [Darcs repository patch example](https://darcs.net/Internals/Repository)
- Documentation version and relevant section: repository internals, "After
  recording a patch"; it separates patch metadata from a list of primitive
  patches and shows `addfile` and `hunk` data.
- Official implementation or grammar permalink:
  [Darcs 2.18.5 V1 primitive parser](https://hackage.haskell.org/package/darcs-2.18.5/src/src/Darcs/Patch/Prim/V1/Read.hs)
- Implementation version, file, and relevant symbol: Darcs 2.18.5,
  `Darcs.Patch.Prim.V1.Read`, `readPrim`, `readHunk`, and the readers for every
  primitive command. `readHunk` assigns space, minus, and plus lines to patch
  data and defines no ignorable comment branch.
- Conformance detail:
  [Darcs 2.18.5 PatchInfo source](https://hackage.haskell.org/package/darcs-2.18.5/src/src/Darcs/Patch/Info.hs)
  defines patch log metadata and the `Ignore-this:` uniqueness line.
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the `.dpatch` extension can be used outside
  Darcs, but the exact dataset label is specifically `Darcs Patch`; mixed or
  misclassified files still do not justify a permissive comment pattern.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: static inspection of the immutable Darcs 2.18.5
  source distribution.
- Exact version or commit: Darcs 2.18.5 tarball SHA-256
  `e310692989e313191824f532a26c5eae712217444214266503d5eb5867f951ab`.
- Probe method: enumerated every `readPrim` alternative and inspected hunk and
  patch-info parsing for an ignorable comment production.
- Probe input:

```text
[example
Alice <alice@example.test>**20250801000000
 Ignore-this: 0123456789abcdef
] hunk ./main.c 1
-/* old source comment */
+// new source comment
```

- Observed result: marker-looking text is patch metadata or hunk payload; the
  official parser defines no comment token that can be discarded.
- Conclusion and limits of the probe: source comments inside payload belong to
  the patched file's language, not to the Darcs Patch container.

### Representative examples

```text
hunk ./notes.txt 1
-# old heading
+# new heading
```

Both hash-prefixed lines are patch payload. Extraction or cleaning would corrupt
the represented change.

### Adversarial boundaries

- Negative cases: `Ignore-this:`, free-form patch descriptions, email lines,
  `+//`, `-/*...*/`, hash-prefixed payload, `--` metadata-looking text, and a
  literal `hunk` word inside added content.
- Malformed-input cases: truncated named-patch brackets, incomplete hunks,
  missing binary data, and partial email bundles remain opaque data.
- Line-ending and Unicode cases: LF/CRLF, EOF without a newline, Unicode patch
  names/authors, and binary patch text must be preserved.
- Version or dialect counterexamples: Darcs 1, Darcs 2, and external Debian
  `.dpatch` files must not be aliased to diff, Haskell, shell, or any
  delimiter-based family based only on extension.
- Cleaner preservation cases: byte-preserving no-op across metadata, context,
  removed lines, and added lines.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none; retain an explicit inventory disposition.
- Deterministic tests to add: unsupported lookup and a no-extraction fixture
  covering patch metadata plus source-comment-looking hunk payload.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Gemini

### Identity and scope

- Raw dataset label: `Gemini` (24,820 files; 36,342,778 tokens)
- Proposed registry key: `gemini` only for inventory accounting; `gemtext` is
  the classifier alias, not a comment-syntax alias to register.
- Existing family or aliases checked: Markdown, AsciiDoc, plain text,
  configuration formats, and legacy no-op handling. Gemtext's heading, quote,
  list, link, and preformat controls are document structure, not comments.
- Classification: `document-format`
- Versions or releases checked: official Gemtext specification 0.24.1,
  retrieved over Gemini on 2026-08-01. The complete protocol response has
  SHA-256 `ad9d90143eaa542101d37eb874c074d960489ab3dde5c76bc2843e5dff20682a`.
- Dialects checked: canonical `text/gemini` Gemtext. Markdown, Gopher menus,
  arbitrary plain-text Gemini responses, and source code inside preformatted
  regions are excluded.
- Intended support scope: none; Linguist classifies `.gmi` as `prose` and names
  `gemtext` as an alias.
- Explicitly excluded scope: headings beginning `#`, quotes beginning `>`, list
  items beginning `* `, links beginning `=>`, preformat toggle lines beginning
  three backticks, alt text after a toggle, and comments belonging to source
  code embedded inside a preformatted region.

### Syntax contract

- Line comments: `unsupported`. The formal grammar has no comment line type;
  an otherwise unrecognized line is a visible text line.
- Block comments: `unsupported`.
- Nested comments: `unsupported`.
- Termination at newline, delimiter, or EOF: Gemtext is line-oriented, but none
  of its line types terminates or wraps a comment.
- Inline use: unsupported.
- Adjacent-line grouping: unsupported.
- Unclosed delimiter behavior: a final unmatched preformat toggle leaves the
  parser in preformatted mode at EOF; the specification says final parser state
  has no consequence. It is not an unclosed comment.
- Lexical or structural context: in normal mode there are exactly six line
  types: text, link, heading, list item, quote, and preformat toggle. In
  preformatted mode all lines except a leading-three-backticks toggle are text.
- Conflicts with strings, operators, directives, or embedded languages: `#`
  is a heading prefix, `>` is a quote prefix, `* ` is a list marker, and a line
  beginning `//` is ordinary visible text. Toggle alt text may be ignored by a
  client for rendering, but it is accessibility/indexing metadata and must not
  be treated as removable comment content.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: none.
- Content-preservation expectations: produce no matches and preserve every
  line. Rendering behavior is not a license to delete document structure or
  preformatted source.

### Evidence

- Dataset classifier permalink:
  [Linguist Gemini metadata](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L2501-L2511)
- Official documentation permalink:
  [Gemtext specification 0.24.1](https://geminiprotocol.net/docs/gemtext-specification.gmi)
- Documentation version and relevant sections: 0.24.1, "Line oriented
  design", "Parser state", "Recognising and handling gemtext lines", and
  "Formal grammar". The source was content-pinned by the response SHA-256 above
  because the provider exposes a version number but no immutable revision URL.
- Official implementation or grammar permalink: the normative ABNF in the same
  specification exhaustively lists all six line productions and has no comment
  production.
- Conformance test or official example permalink: the normative normal-mode and
  preformatted-mode examples in the same specification distinguish structural
  marker lines from text.
- Secondary source, if needed: none.
- Evidence conflicts or gaps: no comment syntax exists in the normative format.
  Client-specific hidden extensions are intentionally outside the dataset label.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: fetched the official specification directly over the
  Gemini protocol and inspected its normative ABNF.
- Exact version or commit: Gemtext 0.24.1; full response SHA-256
  `ad9d90143eaa542101d37eb874c074d960489ab3dde5c76bc2843e5dff20682a`.
- Probe method: enumerated the six normative normal-mode line types and the two
  preformatted-mode cases, then checked for a comment production.
- Probe input:

````text
# Heading, not a comment
// Visible text
```source
/* embedded source remains document content */
```
````

- Observed result: the first line is a heading, the second is a text line, and
  the source-looking line is preformatted text. No line is a Gemtext comment.
- Conclusion and limits of the probe: renderer-specific behavior and embedded
  source languages are outside the canonical Gemtext comment contract.

### Representative examples

```text
# Release notes
=> /next Continue
> // quoted prose
* /* literal list text */
```

Every line is user-visible document content or structure; expected extraction
is empty.

### Adversarial boundaries

- Negative cases: one to four leading `#`, `//` text, `/*...*/` text, quote and
  list markers, link labels containing markers, preformat alt text, and source
  comments inside a preformatted block.
- Malformed-input cases: unmatched preformat toggle, malformed link line,
  heading with more than three hashes, and invalid UTF-8 remain document data;
  none creates a comment region.
- Line-ending and Unicode cases: canonical CRLF, protocol-permitted LF, EOF,
  UTF-8 headings/links, and combining characters must be preserved.
- Version or dialect counterexamples: Markdown comments, HTML comments, and
  client extensions must not be inherited by canonical Gemtext.
- Cleaner preservation cases: no-op for all structural prefixes, toggle lines,
  alt text, and preformatted payload.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none; retain an explicit inventory disposition.
- Deterministic tests to add: unsupported lookup and no-extraction fixtures for
  every Gemtext line type plus marker-looking preformatted content.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Python traceback

### Identity and scope

- Raw dataset label: `Python traceback` (827 files; 227,342 tokens)
- Proposed registry key: `python_traceback` only for inventory accounting; do
  not alias it to Python source.
- Existing family or aliases checked: Python source, Python console, shell
  session, plain text, generated diagnostics, and legacy no-op handling. A
  traceback is output data, not a Python compilation unit.
- Classification: `generated-format`
- Versions or releases checked: CPython 3.14.6, commit
  `c63aec69bd59c55314c06c23f4c22c03de76fe45`, and pinned Linguist
  revision `537297cdae3ab05f8d5dd1c03627a5bd73707b19`.
- Dialects checked: standard CPython stack traceback and exception-group
  formatting. Third-party test runners, logging prefixes, alternate Python
  implementations, and notebook rich output are excluded.
- Intended support scope: none; Linguist classifies `.pytb` as `data` grouped
  under Python, with TextMate scope `text.python.traceback`.
- Explicitly excluded scope: Python comments in an optionally reproduced source
  line, marker-looking exception messages, chained-exception separator prose,
  exception-group layout, ANSI color sequences, and logging prefixes.

### Syntax contract

- Line comments: `unsupported` for traceback data.
- Block comments: `unsupported`.
- Nested comments: `unsupported`.
- Termination at newline, delimiter, or EOF: not applicable to comments.
- Inline use: unsupported.
- Adjacent-line grouping: unsupported.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: CPython formats a header, frame summaries,
  optional reproduced source text and caret annotations, then exception type
  and message. Chained exceptions and exception groups add more generated
  separators and nested layouts.
- Conflicts with strings, operators, directives, or embedded languages: a frame
  source line is copied from a source file and can contain Python `#` comments.
  Exception messages, filenames, function names, and logging prefixes are
  arbitrary text and can contain any delimiter. CPython 3.13 and later may also
  colorize output.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: none.
- Content-preservation expectations: produce no matches and preserve all
  diagnostic information. Do not silently parse reproduced frame lines as a
  complete Python source file or remove text from exception messages.

### Evidence

- Dataset classifier permalink:
  [Linguist Python traceback metadata](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L6185-L6193)
- Official documentation permalink:
  [CPython 3.14.6 traceback documentation](https://github.com/python/cpython/blob/c63aec69bd59c55314c06c23f4c22c03de76fe45/Doc/library/traceback.rst#traceback-print-or-retrieve-a-stack-traceback)
- Documentation version and relevant section: Python 3.14.6, module overview
  and `print_exception`; it defines traceback output as formatted diagnostic
  data and documents the header, stack entries, and exception value.
- Official implementation permalink:
  [CPython traceback formatter](https://github.com/python/cpython/blob/c63aec69bd59c55314c06c23f4c22c03de76fe45/Lib/traceback.py#L527-L646)
- Implementation version, file, and relevant symbols: CPython 3.14.6,
  `StackSummary.format_frame_summary` reproduces filename, location, and source
  text; `TracebackException.format` emits headers, formatted stacks, chained
  exception text, groups, and exception messages.
- Conformance detail:
  [unhandled exception behavior](https://github.com/python/cpython/blob/c63aec69bd59c55314c06c23f4c22c03de76fe45/Doc/reference/executionmodel.rst#exceptions)
  states that an unhandled exception prints a stack traceback and warns that
  exception-message content may change between Python versions.
- Secondary source, if needed: none.
- Evidence conflicts or gaps: third-party producers can wrap or modify standard
  output, reinforcing that no marker-based source-comment contract is portable.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned CPython documentation and formatter-source
  inspection.
- Exact version or commit: CPython 3.14.6,
  `c63aec69bd59c55314c06c23f4c22c03de76fe45`.
- Probe method: traced frame and exception formatting to identify which fields
  may carry arbitrary or embedded source text.
- Probe input:

```text
Traceback (most recent call last):
  File "/tmp/example.py", line 1, in <module>
    raise RuntimeError("// message")  # reproduced source note
RuntimeError: // message
```

- Observed result: `#` belongs to an embedded source line and `//` belongs to a
  string and exception message; neither is traceback comment scaffolding.
- Conclusion and limits of the probe: extracting the embedded Python comment
  would require a separately scoped embedded-language contract, which the raw
  traceback label does not provide.

### Representative examples

```text
Traceback (most recent call last):
  File "service.py", line 42, in run
    connect("https://example.test/a#fragment")  # retry path
RuntimeError: /* upstream returned // */
```

Expected extraction is empty; every marker-looking substring is diagnostic,
embedded source, a literal, or an exception message.

### Adversarial boundaries

- Negative cases: Python `#` in reproduced source, URL fragments, `//` and
  `/*...*/` in messages, filenames containing punctuation, chained-exception
  prose, exception-group gutters, caret lines, and ANSI escapes.
- Malformed-input cases: truncated frames, missing exception tail, pasted
  logging prefixes, mixed standard/error output, and partially colorized text
  remain opaque diagnostic data.
- Line-ending and Unicode cases: LF, CRLF, EOF without newline, Unicode paths,
  function names and messages, combining characters, and terminal color codes
  must remain intact.
- Version or dialect counterexamples: CPython versions, PyPy, test-runner rich
  tracebacks, notebook output, and logging wrappers must not alias the label to
  Python source comments.
- Cleaner preservation cases: byte-preserving no-op across headers, frames,
  source excerpts, carets, messages, and exception-group structure.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none; retain an explicit inventory disposition.
- Deterministic tests to add: lookup remains `NotImplementedError`; add a
  no-extraction fixture with an inline Python comment, URL, arbitrary exception
  message, chained separator, and exception-group layout.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01
