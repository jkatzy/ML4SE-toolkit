# Stack v3 Full Comment Research: batch_02

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics aggregated from
  `files[].language`
- Researcher or agent: `/root/research_batch_02`
- Review status: `reviewed`

Registry lookup was checked for every exact raw label at the feature-branch
state used for this research. `F*` resolves to `f_star_style`; the other nine
raw labels do not resolve. Existing families named below were comparison
targets, not evidence for a language contract.

## Dune

### Identity and scope

- Raw dataset label: `Dune` (124,385 files; 5,055,519 tokens)
- Proposed registry key: `dune`
- Existing family or aliases checked: `assembly` / `semicolon_style`
- Classification: `document-format`
- Versions or releases checked: Dune main at commit
  `863b7d02241fe4f3b8ac15f8fcb22230db0ce195`
- Intended support scope: Dune S-expression files such as `dune`,
  `dune-project`, and `dune-workspace` parsed by `dune_sexp`.
- Explicitly excluded scope: OCaml comments in `.ml` files and generated
  opam/shell content embedded in Dune atoms or strings.

### Syntax contract

- Line comments: `;` through the next CR, LF, CRLF, or EOF. The opener may
  occur at the start of a line or after an S-expression.
- Block comments: unsupported. Nested comments: unsupported.
- Inline use: yes. Adjacent-line grouping: consecutive semicolon-comment lines
  are compatible with grouping; indentation is allowed and a blank line ends a
  group.
- Unclosed delimiter behavior: not applicable; an EOF-terminated line comment
  is complete.
- Lexical context: the lexer recognizes quoted strings and Dune's end-of-line
  string forms before normal tokenization. A semicolon in such a string is
  data; a semicolon cannot occur in an unquoted atom.
- Conflicts: do not treat semicolons in `"a;b"` or after the `"\|` and
  `"\>` end-of-line-string prefixes as comments. Repeated `;;` has no distinct
  comment kind.
- Sanitizer wrappers: strip one leading `;`. There are no block wrappers.
- Content preservation: retain every payload character, including additional
  semicolons, indentation, non-ASCII text, and the original line ending.

### Evidence

- Official documentation permalink:
  [Dune lexical conventions](https://github.com/ocaml/dune/blob/863b7d02241fe4f3b8ac15f8fcb22230db0ce195/doc/reference/lexical-conventions.rst)
- Official implementation permalink:
  [`dune_sexp` lexer](https://github.com/ocaml/dune/blob/863b7d02241fe4f3b8ac15f8fcb22230db0ce195/src/dune_sexp/lexer.mll)
- Relevant implementation symbols: `comment`, `comment_body`, `token`, and
  `comment_trail`.
- Evidence conflicts or gaps: none for comment recognition. Comment grouping is
  a lexer/API facility rather than a second lexical form.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned lexer and comment-trail rules inspected; no
  local Dune binary was invoked.
- Probe conclusion: the rules distinguish semicolons in quoted/EOL strings,
  terminate on either CR or LF, and accept a final comment without a newline.

### Representative examples

```text
(lang dune 3.20)
; project-wide note
(name demo) ; inline note
```

### Adversarial boundaries

- Negative cases: `"semi;colon"`, both EOL-string syntaxes containing `;`, and
  a bare atom immediately before a semicolon.
- Malformed cases: a missing quote is a string error, not permission to extract
  an interior semicolon independently of the lexer state.
- Line endings: test LF, CRLF, bare CR, EOF, and a non-ASCII payload.
- Cleaner preservation: keep repeated semicolons in the body and never consume
  the following list or its closing parenthesis.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `dune` to `semicolon_style`, with Dune string
  ignored ranges and the Dune line-grouping boundary.
- Deterministic tests to add: start/inline comments, quoted and EOL strings,
  consecutive/blank-separated lines, all line endings, EOF, and sanitizer
  payload preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Ecmarkup

### Identity and scope

- Raw dataset label: `Ecmarkup` (86,353 files; 2,048,027,056 tokens)
- Proposed registry key: `ecmarkup`
- Existing family or aliases checked: `html` / `markup_style`
- Classification: `document-format`
- Versions or releases checked: Ecmarkup 25.0.0 source at commit
  `2de548d53a6d7ffa04791111647ae0132e131c47`; WHATWG HTML source at commit
  `24c5e48bf66ea61bc199ec6338c81258275ba9c6`
- Intended support scope: the HTML layer of Ecmarkup specification sources.
- Explicitly excluded scope: comment-looking text inside JavaScript/CSS raw-text
  elements, attribute values, escaped markup, and Ecmarkdown prose constructs.

### Syntax contract

- Line comments: unsupported.
- Block comments: conforming HTML comments open with `<!--` and close with
  `-->`; they may span lines.
- Nested comments: no. An interior `<!--` is a parse error and does not create a
  nested node; the outer tokenizer state continues to its end sequence.
- Termination and malformed input: conforming comments use `-->`. The HTML
  tokenizer also recovers `--!>` as a close and emits a comment at EOF, and has
  separate abrupt/bogus-comment states; those parse-error forms are outside the
  recommended source-comment scope.
- Inline use: yes, in HTML data between nodes. Adjacent-line grouping: no
  language-level grouping; keep distinct HTML comment nodes distinct.
- Lexical context: Ecmarkup parses its input through JSDOM's HTML tokenizer.
  Comment recognition therefore depends on HTML tokenizer state, not a global
  delimiter search.
- Conflicts: `<!--` in an attribute, escaped as `&lt;!--`, or in `script` or
  `style` raw text is data. `<!DOCTYPE ...>`, CDATA-like input, and `<?...>` are
  not conforming HTML source comments.
- Sanitizer wrappers: strip `<!--` and the matching `-->`; preserve the body
  byte-for-byte and preserve line structure. Do not silently normalize malformed
  parser-recovery forms into conforming comments.

### Evidence

- Official Ecmarkup documentation: [current Ecmarkup specification](https://tc39.es/ecmarkup/)
- Official Ecmarkup implementation permalinks:
  [`Spec` HTML ingestion](https://github.com/tc39/ecmarkup/blob/2de548d53a6d7ffa04791111647ae0132e131c47/src/ecmarkup.ts#L56-L66) and
  [`htmlToDom`](https://github.com/tc39/ecmarkup/blob/2de548d53a6d7ffa04791111647ae0132e131c47/src/utils.ts#L77-L83)
- Normative implementation grammar:
  [WHATWG HTML tokenizer source](https://github.com/whatwg/html/blob/24c5e48bf66ea61bc199ec6338c81258275ba9c6/source)
- Relevant states: comment start, comment, comment end, bogus comment, and EOF in
  comment.
- Evidence conflicts or gaps: the HTML parser deliberately creates comment
  nodes for some invalid recovery inputs. This recommendation covers conforming
  source syntax only and records the recovery cases as malformed boundaries.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: Ecmarkup's pinned JSDOM call path and the pinned HTML
  tokenizer algorithm were inspected; no DOM runtime probe was needed.
- Probe conclusion: ordinary `<!--...-->` is the stable shared contract;
  tokenizer-state recovery must not be approximated by broad `<!...>` matching.

### Representative examples

```html
<emu-clause id="sec-example">
  <!-- editorial note -->
  <h1>Example</h1>
</emu-clause>
```

### Adversarial boundaries

- Negative cases: `<script>const x = "<!--";</script>`,
  `<div data-x="<!--">`, `&lt;!--`, doctype, CDATA-like text, and processing
  instructions.
- Malformed cases: nested-looking opener, `<!-->`, `<!--->`, `--!>`, and EOF
  before `-->`; valid-syntax extraction must not expand to all bogus-comment
  tokens.
- Line endings: preserve LF/CRLF/CR and Unicode payload exactly.
- Cleaner preservation: remove only the conventional wrappers and never consume
  adjacent element markup.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `ecmarkup` to `markup_style` for conventional
  closed HTML comments; retain HTML raw-text and quoted-attribute exclusions.
- Deterministic tests to add: ordinary/inline/multiline comments, first close,
  tokenizer-context negatives, malformed recovery forms, EOF, and cleaner
  boundaries.
- Remaining blocker: none for the stated conforming-source scope.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Edge

### Identity and scope

- Raw dataset label: `Edge` (94,927 files; 714,462,207 tokens)
- Proposed registry key: `edge`
- Existing family or aliases checked: no exact family; generic paired/nested
  delimiters are insufficient because the official scanner balances braces.
- Classification: `template`
- Versions or releases checked: Edge 6.5.1 source at commit
  `0eccdced8d0ab1b017249c1810b54c356224cd88`; `edge-lexer` 6.0.5 source at
  commit `730f916e350498c2eb93817e490eb4bfd52edef4`
- Intended support scope: `.edge` templates tokenized by Edge 6.x.
- Explicitly excluded scope: comments belonging only to an embedded output
  language such as HTML, CSS, JavaScript, Markdown, or JSON.

### Syntax contract

- Line comments: unsupported.
- Block comments: `{{--` through an eligible `--}}`, on one or many lines.
- Nested comments: effectively yes for balanced nested full delimiters. The
  scanner counts every `{` and `}` in the body and recognizes `--}}` only at
  brace depth zero; this is broader than simply counting full openers.
- Inline use: yes in raw template text and next to interpolation. An Edge tag
  that requires the rest of its physical line cannot have a trailing comment.
- Adjacent-line grouping: no language-level grouping; keep comment tokens
  separate.
- Unclosed delimiter behavior: tokenizer error `unclosedCurlyBrace`; do not
  accept an EOF-terminated comment.
- Lexical or structural context: detection begins at a `{{` in raw template
  text; once a mustache/comment scan starts, brace balance controls closure.
- Conflicts: `{{--` inside an already active mustache is not a second top-level
  comment. HTML `<!-- -->`, JavaScript `//`/`/* */`, CSS comments, and strings in
  embedded output are outside the Edge-comment contract. Unbalanced ordinary
  braces in the body affect whether a nominal `--}}` can close.
- Sanitizer wrappers: strip `{{--` and the closing `--}}`; preserve all body
  whitespace, braces, and newlines.

### Evidence

- Official documentation: [Edge comments](https://edgejs.dev/docs/syntax_specification#comments)
- Official package permalink:
  [Edge 6.5.1 dependency metadata](https://github.com/edge-js/edge/blob/0eccdced8d0ab1b017249c1810b54c356224cd88/package.json)
- Official lexer permalinks:
  [`getMustache`](https://github.com/edge-js/lexer/blob/730f916e350498c2eb93817e490eb4bfd52edef4/src/detector.ts#L75-L119),
  [comment scanning](https://github.com/edge-js/lexer/blob/730f916e350498c2eb93817e490eb4bfd52edef4/src/tokenizer.ts#L299-L420), and
  [brace-tolerant `Scanner`](https://github.com/edge-js/lexer/blob/730f916e350498c2eb93817e490eb4bfd52edef4/src/scanner.ts#L90-L157)
- Official tests:
  [comment tokenizer cases](https://github.com/edge-js/lexer/blob/730f916e350498c2eb93817e490eb4bfd52edef4/tests/tokenizer_comment.spec.ts)
- Evidence conflicts or gaps: documentation presents a paired delimiter; the
  implementation adds brace-depth and tag-line constraints.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: source-level trace of `getMustache`, `Scanner.scan`,
  `#feedCharsToCurrentMustache`, and `#checkForErrors`, plus official tests.
- Probe conclusion: a regex or ordinary first-close block matcher would be
  observably wrong for nested or unbalanced braces and malformed EOF.

### Representative examples

```edge
<p>{{-- not rendered --}} Hello {{ user.username }}</p>
{{-- outer {{-- inner --}} outer tail --}}
```

### Adversarial boundaries

- Negative cases: HTML/JS/CSS markers, `{{ "{{--" }}` within a mustache, and a
  comment placed after a line-oriented `@if(...)` tag.
- Malformed cases: unclosed comment, unmatched `{` before `--}}`, unmatched `}`,
  and a stray `--}}`.
- Line endings: the tokenizer splits LF, CRLF, and CR; preserve the original
  source slices and test all three plus EOF.
- Cleaner preservation: retain nested markers and braces as content; never
  consume the following raw node or interpolation.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `edge` with a brace-depth-aware
  `{{--` scanner and exact `--}}` wrapper metadata.
- Deterministic tests to add: official inline/multiline cases, nested comments,
  brace imbalance, tag-line rejection, embedded-language negatives, all line
  endings, unclosed EOF, and sanitizer slices.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## EdgeQL

### Identity and scope

- Raw dataset label: `EdgeQL` (11,753 files; 35,716,765 tokens)
- Proposed registry key: `edgeql`
- Existing family or aliases checked: `dockerfile` / `hash_line_style`
- Classification: `language`
- Versions or releases checked: current Gel/EdgeQL documentation and Gel source
  at commit `85191063b4db8b87caf26499de40f8a9d90c8146`
- Dialects checked: EdgeQL queries and ESDL schema files use the same tokenizer.
- Intended support scope: `.edgeql` and `.esdl` text accepted by the pinned
  EdgeQL tokenizer.
- Explicitly excluded scope: SDL/EdgeQL embedded inside host-language strings
  and PostgreSQL emitted by the compiler.

### Syntax contract

- Line comments: `#` through CR, LF, or EOF.
- Block comments and nested comments: unsupported.
- Inline use: yes wherever whitespace may separate tokens.
- Adjacent-line grouping: yes for consecutive hash-comment lines; a blank or
  non-comment line breaks a group.
- Unclosed delimiter behavior: not applicable; EOF completes a line comment.
- Lexical context: comments are skipped between tokens. Single/double-quoted,
  raw, bytes, and dollar-quoted strings are tokenized as strings, so interior
  hashes are data.
- Conflicts: `//` is the floor-division operator, not a comment; `#` in a string
  or host-language embedding is not an EdgeQL comment. Prohibited Unicode format
  controls remain tokenizer errors even when encountered while skipping text.
- Sanitizer wrappers: strip one `#`; there are no block wrappers. Preserve the
  body, original line ending, and all additional hashes.

### Evidence

- Official documentation: [EdgeQL lexical structure](https://docs.geldata.com/reference/reference/edgeql/lexical)
- Official implementation permalink:
  [`skip_whitespace` and comment scan](https://github.com/geldata/gel/blob/85191063b4db8b87caf26499de40f8a9d90c8146/edb/edgeql-parser/src/tokenizer.rs#L914-L955)
- Official conformance tests:
  [tokenizer whitespace/comments](https://github.com/geldata/gel/blob/85191063b4db8b87caf26499de40f8a9d90c8146/edb/edgeql-parser/tests/tokenizer.rs#L46-L55) and
  [`//` operator cases](https://github.com/geldata/gel/blob/85191063b4db8b87caf26499de40f8a9d90c8146/edb/edgeql-parser/tests/tokenizer.rs#L205-L212)
- Evidence conflicts or gaps: product naming changed from EdgeDB to Gel, but the
  language and tokenizer retain the EdgeQL name and syntax.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned Rust tokenizer and official tokenizer tests
  inspected; no local Gel server was started.
- Probe conclusion: `#` is a conventional EOF-capable line comment, while
  string tokenization and the `//` operator are mandatory negative boundaries.

### Representative examples

```edgeql
select User { name }; # response shape note
# a complete comment line
```

### Adversarial boundaries

- Negative cases: `select 'a#b';`, raw/dollar-quoted strings containing `#`,
  `select 7 // 2;`, and EdgeQL embedded in a host string.
- Malformed cases: prohibited format-control characters and unclosed strings
  preceding a hash.
- Line endings: test LF, CRLF, bare CR, EOF, and U+2028/U+2029 explicitly rather
  than assuming they are physical line terminators.
- Cleaner preservation: retain leading spaces and additional `#` characters in
  the payload and never consume the next query token.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `edgeql` (and explicit `esdl` if desired by the
  inventory policy) to `hash_line_style`, with EdgeQL string ignored ranges.
- Deterministic tests to add: inline/full-line/EOF, every string form, `//`
  operator, CR/LF variants, Unicode-control rejection, grouping, and sanitizer.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## F*

### Identity and scope

- Raw dataset label: `F*` (295,002 files; 521,913,433 tokens)
- Proposed registry key: existing `f_star` with exact alias `f*`
- Existing family or aliases checked: `f_star_style`; the raw label already
  resolves to this family.
- Classification: `language`
- Versions or releases checked: F* tutorial and compiler source at commit
  `42b45f6df687397cbb1b905c4066ff2435d5080f`
- Intended support scope: `.fst` and `.fsti` source parsed by the pinned F*
  lexer.
- Explicitly excluded scope: extraction inside uninterpreted ````` `` blobs,
  `#lang-...` payloads, and generated OCaml/F#/SMT.

### Syntax contract

- Line comments: `//` through CR, LF, U+2028, U+2029, or EOF.
- Block comments: `(*` through its balanced `*)`.
- Nested comments: yes; the lexer recursively tracks nested `(* ... *)`.
- Inline use: yes for both forms. Adjacent-line grouping: yes for consecutive
  `//` lines.
- Unclosed delimiter behavior: the pinned lexer accepts EOF in a block-comment
  state and records a synthetic closing `*)` internally. Extraction must return
  only the exact source slice through EOF and must not invent bytes.
- Lexical context: quoted strings/characters and uninterpreted language blobs
  have their own lexer states and protect marker-looking text.
- Conflicts: the exact compatibility prefix `// IN F*:` is consumed as a marker
  and lexing resumes on the remainder of that physical line; treating the whole
  line as a comment would discard active F* code. `/` remains an operator.
- Sanitizer wrappers: strip `//`, or matching `(*` and `*)`; for an accepted EOF
  block strip only `(*`. Preserve nested wrappers as payload and preserve all
  physical line structure.

### Evidence

- Official documentation: [F* comments](https://fstar-lang.org/tutorial/book/part1/part1_getting_off_the_ground.html#comments)
- Official implementation permalink:
  [`LexFStar` comment rules and states](https://github.com/FStarLang/FStar/blob/42b45f6df687397cbb1b905c4066ff2435d5080f/src/ml/FStarC_Parser_LexFStar.ml#L573-L678)
- Relevant implementation symbols: ordinary `//`, special `// IN F*:`,
  recursive `comment`, `terminate_comment`, and uninterpreted-blob states.
- Evidence conflicts or gaps: the tutorial documents normal closed forms but
  not the accepted EOF block or compatibility marker; the lexer is decisive.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned lexer actions were traced; no local F* compiler
  build was run.
- Probe conclusion: nesting, four line terminators, synthetic EOF closure, and
  `// IN F*:` all require tests beyond the two documented delimiters.

### Representative examples

```fstar
let x = 1 // line note
(* outer (* inner *) outer tail *)
let y = x + 1
```

### Adversarial boundaries

- Negative cases: comment markers in strings/chars and uninterpreted blobs,
  `/` division, and `// IN F*: let active = true`.
- Malformed cases: unclosed nested block through EOF, stray `*)`, and a partial
  opener.
- Line endings: LF, CRLF, CR, U+2028, U+2029, and EOF line comments.
- Cleaner preservation: never materialize the lexer's synthetic `*)`; retain
  inner delimiters and the final source bytes of an EOF block.

### Decision

- Recommended action: `alias`
- Registry fields to change: retain `f*` as an alias of `f_star_style`; harden
  that family for the compatibility marker, Unicode line terminators, protected
  blobs, and accepted unclosed blocks.
- Deterministic tests to add: nested blocks, every line terminator, EOF block,
  strings/chars/blobs, `// IN F*:`, exact slices, and sanitizer behavior.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## FIRRTL

### Identity and scope

- Raw dataset label: `FIRRTL` (178,762 files; 2,164,102,421 tokens)
- Proposed registry key: `firrtl`
- Existing family or aliases checked: `assembly` / `semicolon_style`
- Classification: `language`
- Versions or releases checked: FIRRTL specification 6.0.0 at commit
  `5ab37a032d822c8e3975fb9f7f36e52a019c34ec`; CIRCT importer at commit
  `02046f45e22ee214a63f3635fb57318e05145ba8`
- Intended support scope: textual `.fir` input accepted by CIRCT's FIRRTL
  importer.
- Explicitly excluded scope: MLIR syntax around FIRRTL dialect operations,
  Verilog output, and annotation JSON parsed outside the FIRRTL lexer.

### Syntax contract

- Line comments: `;` through CR, LF, or EOF.
- Block comments and nested comments: unsupported.
- Inline use: yes. Adjacent-line grouping: yes for consecutive semicolon lines.
- Unclosed delimiter behavior: not applicable; EOF completes a line comment.
- Lexical context: strings, literal/verbatim forms, info locators `@[...]`, and
  inline-annotation tokens are lexed as units; semicolons inside those units are
  data rather than comment openers.
- Conflicts: `;;` has no special directive meaning; it is one comment whose body
  begins with `;`. Do not import Verilog `//` or `/* */` syntax.
- Sanitizer wrappers: strip one `;`; there are no block wrappers. Preserve the
  remaining semicolons, indentation, Unicode payload, and original line ending.

### Evidence

- Official specification permalink:
  [FIRRTL 6.0.0 comments](https://github.com/chipsalliance/firrtl-spec/blob/5ab37a032d822c8e3975fb9f7f36e52a019c34ec/spec.md#comments)
- Official implementation permalink:
  [CIRCT `lexComment`](https://github.com/llvm/circt/blob/02046f45e22ee214a63f3635fb57318e05145ba8/lib/Dialect/FIRRTL/Import/FIRLexer.cpp#L450-L470)
- Implementation context:
  [FIRRTL lexer dispatch](https://github.com/llvm/circt/blob/02046f45e22ee214a63f3635fb57318e05145ba8/lib/Dialect/FIRRTL/Import/FIRLexer.cpp)
- Evidence conflicts or gaps: none for comment syntax; the implementation gives
  the explicit CR/LF/EOF boundary.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned specification and CIRCT lexer inspected; no
  local `firtool` binary was invoked.
- Probe conclusion: the language is semicolon-line compatible, provided lexical
  units that can contain semicolons are excluded before comment matching.

### Representative examples

```firrtl
circuit Demo:
  module Demo: ; module note
    input clock: Clock
```

### Adversarial boundaries

- Negative cases: semicolons in quoted/verbatim values, info locators, and
  inline annotations; `//` and `/*...*/`; a lone non-comment token before `;`.
- Malformed cases: unclosed protected lexical units preceding a semicolon and a
  stray Verilog closer.
- Line endings: LF, CRLF, bare CR, EOF, and non-ASCII comment payload.
- Cleaner preservation: strip exactly one semicolon and never remove the next
  declaration or indentation needed by FIRRTL.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `firrtl` to `semicolon_style`, with FIRRTL
  string/info/annotation ignored ranges.
- Deterministic tests to add: full-line/inline/EOF comments, lexical-unit
  negatives, repeated semicolons, all line endings, grouping, and sanitizer.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## GDShader

### Identity and scope

- Raw dataset label: `GDShader` (96,369 files; 69,931,161 tokens)
- Proposed registry key: `gdshader`
- Existing family or aliases checked: `java` / `c_style`; rejected as an exact
  family because the Godot lexer accepts an unclosed block through EOF and does
  not end `//` at a bare CR.
- Classification: `language`
- Versions or releases checked: Godot documentation at commit
  `cc147ca70ba721db8b5dcf5864f211d9687f8f85`; Godot engine source at commit
  `eda2a482e9ce82e4056cfffae0ea98c1954605a1`
- Intended support scope: `.gdshader` and `.gdshaderinc` source tokenized by
  Godot's `ShaderLanguage` lexer.
- Explicitly excluded scope: GDScript, GLSL imported through another toolchain,
  and shader source embedded in `.tscn`/`.tres` strings.

### Syntax contract

- Line comments: `//` through LF or EOF. In the pinned lexer a bare CR is
  skipped as whitespace only outside the comment loop, so it does not terminate
  an active line comment; CRLF terminates at its LF.
- Block comments: `/*` through the first `*/`.
- Nested comments: no; an inner `/*` has no balancing effect.
- Inline use: yes for line and block forms. Adjacent-line grouping: yes for
  consecutive `//` lines.
- Unclosed delimiter behavior: EOF in the block-comment loop returns `TK_EOF`
  without a lexical error, so an unclosed block consumes through EOF.
- Lexical context: double-quoted strings are scanned separately and protect
  comment markers. Documentation comments `/** ... */` are lexically ordinary
  block comments; immediately preceding a uniform gives them Inspector meaning.
- Conflicts: `/` and `/=` are operators; `//`/`/*` in strings are data. `/**`
  must use longest-wrapper sanitizer metadata if documentation payload is to
  lose all three opening characters.
- Sanitizer wrappers: strip `//`, `/*`/`*/`, or `/**`/`*/`; for an accepted EOF
  block strip only its opener. Preserve body whitespace, leading `*`, BBCode,
  and line structure.

### Evidence

- Official documentation permalink:
  [Godot shading-language comments](https://github.com/godotengine/godot-docs/blob/cc147ca70ba721db8b5dcf5864f211d9687f8f85/tutorials/shaders/shader_reference/shading_language.rst#comments)
- Official implementation permalink:
  [`ShaderLanguage::_get_token`](https://github.com/godotengine/godot/blob/eda2a482e9ce82e4056cfffae0ea98c1954605a1/servers/rendering/shader_language.cpp#L418-L480)
- Relevant implementation paths: `/` dispatch, block loop, line loop, string
  tokenization, `TK_OP_DIV`, and `TK_OP_ASSIGN_DIV`.
- Evidence conflicts or gaps: documentation presents C-style forms but does not
  document the accepted EOF block or bare-CR line behavior; source is decisive.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned engine lexer control flow inspected; no local
  Godot editor was launched.
- Probe conclusion: the EOF and CR behavior differs from the current generic
  C-style contract and warrants a distinct family.

### Representative examples

```glsl
shader_type spatial;
/** [b]Tint[/b] shown in the Inspector. */
uniform vec4 tint; // material control
```

### Adversarial boundaries

- Negative cases: `a / b`, `/=`, marker-looking strings, GLSL preprocessor text,
  and comments embedded in resource-file strings.
- Malformed cases: nested-looking blocks close at the inner `*/`; an unclosed
  block is accepted through EOF; stray `*/` is not an opener.
- Line endings: distinguish LF, CRLF, bare CR, and EOF; include Unicode payload
  but do not infer Unicode line separators.
- Cleaner preservation: preserve doc-comment BBCode and all bytes after an
  unclosed opener; never consume a following token after a closed block.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: add canonical `gdshader` with `//`, non-nested
  `/*...*/`, documentation-wrapper metadata, LF-only line termination, and
  EOF-accepted block behavior.
- Deterministic tests to add: strings/operators, inline/doc comments, first
  close, EOF block, LF/CRLF/bare CR, grouping, exact slices, and sanitizer.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Genero 4gl

### Identity and scope

- Raw dataset label: `Genero 4gl` (32,114 files; 353,783,819 tokens)
- Proposed registry key: `genero_4gl`
- Existing family or aliases checked: `genero` / `genero_style`; the feature
  branch now resolves the raw label through `genero_4gl`, but that alias was
  added from `mapping_review.md` after the original research and is not a
  substitute for a verified compiler grammar.
- Classification: `language`
- Versions or releases checked: Four Js Genero Business Development Language
  6.00 online manual current on 2026-08-01.
- Intended support scope: `.4gl` source accepted by current `fglcomp`.
- Explicitly excluded scope: `.per` forms, SQL/server-side comment rules,
  generated C, and Informix-compatibility preprocessing not active as BDL code.

### Syntax contract

- Verified line comments: `--` and `#` through end of line. The official manual
  permits comments at the beginning of a line and after a statement.
- Verified block comments: `{` through `}`, including across lines.
- Nested comments: no. The manual explicitly prohibits nesting curly-brace
  comments.
- Termination: line endings and ordinary `}` closure are documented; exact bare
  CR, Unicode-separator, EOF, and malformed unclosed-brace behavior are
  unresolved without a lexer grammar or compiler probe.
- Inline use: documented for ordinary comments. Adjacent-line grouping is
  extraction-compatible for consecutive line comments but has no documented
  language-level grouping semantics.
- Lexical context: the manual explicitly protects comment indicators inside
  quoted strings and prohibits comments in form-layout grids. Escape details
  and malformed-input interactions remain unresolved from the available
  primary sources.
- Conflicts: `--#` is explicitly not a BDL comment. `--#{` and `--#}` delimit
  Informix-compatibility conditional regions, and `# fgl-format off/on` remains
  a comment with formatter semantics. `#` is not a comment inside an SQL
  statement block or prepared-statement text. These forms prohibit a
  context-free `--.*`/`#.*` implementation.
- Sanitizer behavior: if implemented after confirmation, strip `--`, `#`, or
  matching `{`/`}` while preserving content and line structure. Wrapper handling
  for unclosed braces is unresolved and must not be guessed.

### Evidence

- Official documentation: [BDL comments](https://4js.com/online_documentation/fjs-fgl-manual-html/fgl-topics/c_fgl_language_features_comment.html)
- Official example: [Genero tutorial `.4gl` comments](https://4js.com/online_documentation/fjs-genero-manual-tutorial-html/genero-tutorial-topics/c_fgl_TutChap02_002.html)
- Documentation version and section: Genero BDL 6.00, language features,
  comments and Informix compatibility.
- Official implementation or grammar permalink: none publicly available was
  found for the 6.00 compiler lexer.
- Mapping-review evidence assessed: the pinned Four Js TextMate grammar lists
  `#`, `--`, and `{...}`, but syntax highlighting is not the `fglcomp` lexer and
  does not define malformed EOF, compiler modes, or exact source slices.
- Evidence conflicts or gaps: valid delimiters, non-nesting, quoted strings,
  layout grids, and SQL/compatibility exceptions are documented, but malformed
  EOF, exact line terminators, and escape-error recovery are not.
- Confidence: `unresolved`

### Implementation confirmation

- Implementation tested: documentation-only review; `fglcomp` 6.00 was not
  available in this environment and no official public lexer was found.
- Required probe: compile ordinary inline forms, escaped strings containing all
  three markers, nested/unclosed braces, LF/CRLF/CR, SQL blocks, `--#`,
  `--#{`/`--#}`, and EOF line comments under both BDL and compatibility modes.
- Conclusion: the verified positive forms are insufficient to specify safe
  exact source slices for malformed and conditional cases.

### Representative examples

```genero
MAIN
    LET answer = 42 -- ordinary BDL comment
    { a documented multiline
      comment }
END MAIN
```

### Adversarial boundaries

- Negative/context cases: strings containing `--`, `#`, or braces; `--# active
  compatibility text`; `--#{`/`--#}` regions; SQL embedded in BDL.
- Malformed cases: nested `{...{...}...}`, unclosed `{`, stray `}`, and a comment
  opener following an unclosed string.
- Line endings: LF, CRLF, bare CR, EOF, U+2028/U+2029, and Unicode payload all
  require compiler confirmation where noted.
- Cleaner preservation: formatter controls remain meaningful payload; never
  delete code after `--#` or invent a missing brace closer.

### Decision

- Recommended action: `defer`
- Registry fields to change: remove the current `genero_4gl` alias from
  `genero_style`; retain the pre-existing `genero` key while this raw Stack
  label remains deferred.
- Deterministic tests to add after confirmation: every documented delimiter,
  strings, nesting/unclosed behavior, conditional markers, line endings, exact
  slices, grouping, and sanitizer preservation.
- Remaining blocker: a pinned official lexer grammar or reproducible `fglcomp`
  6.00 probe covering the unresolved boundaries.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Genero per

### Identity and scope

- Raw dataset label: `Genero per` (27,778 files; 235,388,353 tokens)
- Proposed registry key: `genero_per`
- Existing family or aliases checked: `genero_forms` / `genero_style`; the
  feature branch now resolves the raw label through `genero_per`, but that alias
  was added from `mapping_review.md` after the original research and inheriting
  the `.4gl` contract is not yet justified.
- Classification: `document-format`
- Versions or releases checked: Four Js Genero 6.00 form-specification manuals;
  official `FourjsGenero/tool_fglped` examples at commit
  `d798b8dcff0cbe038ca3c2c7b1e4f1334578bf8c`
- Intended support scope: textual `.per` form specifications compiled by
  `fglform`.
- Explicitly excluded scope: `.4gl` BDL source and screen records/layout text
  that merely resembles a BDL comment delimiter.

### Syntax contract

- Verified line comments: official maintained `.per` examples use `--` for
  disabled/comment lines. Exact inline eligibility and the complete set of line
  terminators remain unresolved.
- Other line comments: `#` is unresolved and must not be inherited from `.4gl`;
  hashes occur as visible form-layout data.
- Block comments: no `.per` block-comment form was verified. Braces are
  structural delimiters for `SCREEN`, `GRID`, and related layout sections and
  must not be treated globally as comments.
- Nested comments and unclosed-comment behavior: unresolved because no public
  official `.per` lexer grammar or complete comment specification was found.
- Adjacent-line grouping: consecutive verified `--` lines may eventually be
  grouping-compatible, but this needs a compiler-backed lexical contract.
- Lexical/structural context: screen-layout bodies, quoted attributes,
  preprocessor directives, and section boundaries require `.per`-specific
  state. A delimiter-only matcher would erase form definitions.
- Sanitizer behavior: unresolved. If `--` is confirmed as the sole applicable
  form, strip only that wrapper and preserve disabled form text; do not strip
  braces or hashes on current evidence.

### Evidence

- Official documentation: [form specification files](https://4js.com/online_documentation/fjs-fgl-manual-html/fgl-topics/c_fgl_FormSpecFiles.html)
- Official tutorial: [text-based `.per` form](https://4js.com/online_documentation/fjs-genero-manual-tutorial-html/genero-tutorial-topics/c_fgl_TutChap03_007.html)
- Official maintained examples:
  [`fglped.per`](https://github.com/FourjsGenero/tool_fglped/blob/d798b8dcff0cbe038ca3c2c7b1e4f1334578bf8c/fglped.per)
- Official implementation or grammar permalink: none publicly available was
  found for the current `fglform` lexer.
- Mapping-review evidence assessed: the pinned Four Js TextMate grammar marks
  `#`, `--`, and `{...}` as comments and gives screen layout rules priority.
  It is useful corroboration, but it is not the `fglform` lexer and does not
  establish all layout, preprocessing, termination, or malformed-input states.
- Evidence conflicts or gaps: examples establish practical `--` use and prove
  braces are structural; the highlighter and corpus examples show candidate
  hash/brace comments but do not define a complete compiler contract, inline
  use, termination, or malformed recovery.
- Confidence: `unresolved`

### Implementation confirmation

- Implementation tested: primary manuals and pinned official examples inspected;
  no `fglform` compiler was available.
- Required probe: compile `--` at line start and inline, `#` in layout/text,
  screen braces, quoted attributes, preprocessor regions, every line ending,
  and EOF under Genero 6.00.
- Conclusion: importing the BDL contract would produce confirmed false positives
  on structural braces and potentially on visible hashes.

### Representative examples

```text
LAYOUT
SCREEN
{
  [customer_id  ]  Store #: [store_no ]
}
-- disabled form item retained as comment content
```

### Adversarial boundaries

- Negative cases: `SCREEN { ... }`, grid/layout braces, visible `#` labels,
  hashes in attributes, quoted `COMMENT` attributes, and BDL code in another
  file.
- Malformed cases: unmatched layout braces, `--` near a section boundary, and
  preprocessor constructs that remove or introduce layout regions.
- Line endings: LF, CRLF, bare CR, EOF, and Unicode payload need a compiler
  matrix.
- Cleaner preservation: never delete screen bodies or visible `#` text; preserve
  disabled field declarations after a verified `--` wrapper.

### Decision

- Recommended action: `defer`
- Registry fields to change: remove the current `genero_per` alias from
  `genero_style`; do not change the pre-existing `genero_forms` key in this
  Stack-label review.
- Deterministic tests to add after confirmation: `--` placement/termination,
  screen braces, visible hashes, attributes, preprocessing, line endings, exact
  slices, and sanitizer preservation.
- Remaining blocker: a pinned official `.per` lexer/grammar or reproducible
  `fglform` 6.00 probes that establish the complete contract.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Glimmer JS

### Identity and scope

- Raw dataset label: `Glimmer JS` (8,170 files; 13,734,192 tokens)
- Proposed registry key: `glimmer_js`
- Existing family or aliases checked: JavaScript `c_style` and HTML
  `markup_style`; neither alone models `.gjs` mode switches.
- Classification: `template`
- Versions or releases checked: First-Class Component Templates RFC at commit
  `227ec9b21ed0bdecc01713d3637e79d509e7d553`; `content-tag` 4.2.0 at commit
  `b0426e5dadc1348d57a80ad95229e42e9556207f`; Glimmer VM source at commit
  `3c206686cea0c2dafad98eb4c3a8dc65cc572318`; ECMAScript 2026 source at commit
  `0248456c758431e4bb8e5d26333ff1865123c9cd`
- Intended support scope: `.gjs` files with JavaScript outside `<template>` and
  Glimmer template syntax inside content tags.
- Explicitly excluded scope: TypeScript `.gts`, preprocessed output, and comment
  syntax of arbitrary languages embedded as rendered template text.

### Syntax contract

- JavaScript mode: `//` through CR, LF, U+2028, U+2029, or EOF; non-nested
  `/*...*/` through the first `*/`; an unclosed block is a syntax error.
- Glimmer mode: short Handlebars comments `{{! ... }}` and whitespace-control
  variants such as `{{~! ... ~}}`; long comments `{{!-- ... --}}` and their
  whitespace-control variants; HTML comments `<!-- ... -->` in template data.
- Nesting: none of the JavaScript, Handlebars, or HTML forms is a nested-comment
  construct. Long Handlebars comments may contain ordinary `}}` text because
  their close is `--}}`.
- Inline use: JavaScript forms are allowed between JS tokens. Glimmer comments
  are allowed in template content; long/Handlebars comments are also valid
  between attributes, but comments inside an attribute name or quoted value are
  invalid/data according to that parser state.
- Adjacent-line grouping: compatible only within the same mode and line-comment
  form; never group across a `<template>` boundary.
- Unclosed behavior: an unclosed JavaScript block, Handlebars comment, or
  `<template>` content tag is rejected. The current Glimmer HTML tokenizer does
  not finish a comment node at EOF and its parser has incomplete final-state
  validation, so an unclosed `<!--` may produce no comment node without a
  dedicated diagnostic; do not accept it as a complete match.
- Lexical context: `content-tag` uses a JavaScript parser to locate real
  `<template>` ranges, protecting comparisons, JSX-like text in strings,
  regular expressions, comments, and template literals. Inside those ranges,
  Glimmer tokenizer states decide which comment forms are active.
- Conflicts: JS markers inside strings/templates/regex are data; Glimmer markers
  outside `<template>` are JS operators/text, not template comments; JS
  `//`/`/* */` inside plain Glimmer text are rendered data. A JavaScript hashbang
  is a host directive, not an extractable source comment. Glimmer's pinned HTML
  tokenizer accepts abrupt empty `<!-->` and `<!--->` comment tokens but does
  not implement WHATWG's `--!>` recovery close; treat all three as malformed
  implementation boundaries, not ordinary conforming comments.
- Sanitizer wrappers: strip the mode-appropriate `//`, `/*`/`*/`, `{{!`/`}}`,
  `{{!--`/`--}}`, or `<!--`/`-->`, including wrapper-owned `~` controls while
  preserving payload whitespace and newlines. Never remove a content-tag
  boundary or merge bodies across modes.

### Evidence

- Official language-design permalink:
  [First-Class Component Templates RFC](https://github.com/emberjs/rfcs/blob/227ec9b21ed0bdecc01713d3637e79d509e7d553/text/0779-first-class-component-templates.md)
- Official content-tag implementation:
  [`locate` mode ranges](https://github.com/embroider-build/content-tag/blob/b0426e5dadc1348d57a80ad95229e42e9556207f/src/locate.rs#L33-L88) and
  [unclosed-tag test](https://github.com/embroider-build/content-tag/blob/b0426e5dadc1348d57a80ad95229e42e9556207f/test/node/parse.test.js#L245-L259)
- Official Glimmer conformance tests:
  [comment printing](https://github.com/glimmerjs/glimmer-vm/blob/3c206686cea0c2dafad98eb4c3a8dc65cc572318/packages/%40glimmer/syntax/test/generation/print-test.ts#L67-L122) and
  [parser contexts and whitespace variants](https://github.com/glimmerjs/glimmer-vm/blob/3c206686cea0c2dafad98eb4c3a8dc65cc572318/packages/%40glimmer/syntax/test/parser-node-test.ts#L772-L873)
- Official Glimmer parser integration:
  [HTML tokenizer event handlers](https://github.com/glimmerjs/glimmer-vm/blob/3c206686cea0c2dafad98eb4c3a8dc65cc572318/packages/%40glimmer/syntax/lib/parser/tokenizer-event-handlers.ts#L46-L60) and
  [parser final-state limitation](https://github.com/glimmerjs/glimmer-vm/blob/3c206686cea0c2dafad98eb4c3a8dc65cc572318/packages/%40glimmer/syntax/lib/parser/handlebars-node-visitors.ts#L40-L56)
- JavaScript specification: [ECMAScript 2026 comments](https://tc39.es/ecma262/2026/multipage/ecmascript-language-lexical-grammar.html#sec-comments) and
  [pinned specification source](https://github.com/tc39/ecma262/blob/0248456c758431e4bb8e5d26333ff1865123c9cd/spec.html)
- Evidence conflicts or gaps: the RFC defines the mode boundary while separate
  JavaScript and Glimmer implementations define comments inside each mode; no
  single flat delimiter grammar is authoritative.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: pinned range locator, its parse-error test, Glimmer
  parser/print tests and HTML-tokenizer integration, and ECMAScript lexical
  grammar inspected; no local Ember build was run.
- Probe conclusion: exact extraction requires a JavaScript-aware content-tag
  locator followed by a Glimmer-aware scanner, then ordinary JavaScript comment
  handling outside the located ranges.

### Representative examples

```gjs
// JavaScript-mode note
const label = "{{! data, not a comment here }}";

<template>
  {{!-- template-only note --}}
  <button {{! valid between attributes }} type="button">{{label}}</button>
</template>
```

### Adversarial boundaries

- Negative cases: `<template>` in JS strings, regexes, template literals, or
  comments; JS markers in Glimmer text; Handlebars markers outside content tags;
  markers inside attribute values; JavaScript hashbang.
- Malformed cases: unclosed content tag, every unclosed comment form, abrupt
  `<!-->`/`<!--->`, unsupported `--!>` recovery, nested-looking openers, `}}`
  inside long comments, and invalid comments inside attribute names/values.
- Line endings: JavaScript's four line terminators plus LF/CRLF/CR within
  templates; preserve Unicode and whitespace-control source slices.
- Cleaner preservation: retain `~` only when it is payload rather than wrapper
  control, preserve template indentation, and never consume adjacent JS or HTML
  nodes.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `glimmer_js` with JavaScript comment
  metadata plus a `content-tag`-equivalent range locator and Glimmer-mode
  Handlebars/HTML comment scanner.
- Deterministic tests to add: all comment forms and whitespace variants, mode
  boundaries hidden in every JS literal kind, attribute contexts, nested-looking
  forms, unclosed errors, line terminators, exact ordering, and sanitizer slices.
- Remaining blocker: none for `.gjs`; `.gts` needs separate TypeScript research.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01
