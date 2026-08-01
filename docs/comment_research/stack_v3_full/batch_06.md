# Stack v3 Full Comment Research: batch_06

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics aggregated from
  `files[].language`
- Researcher or agent: `/root/research_batch_06`
- Review status: `reviewed`

All ten raw labels failed registry lookup at the feature-branch baseline used
for this research. Label identity was checked against
[Linguist 9.5.0](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml),
the classifier inventory from which these exact spellings originate.

## Mojo

### Identity and scope

- Raw dataset label: `Mojo` (17,097 files; 49,585,879 tokens)
- Proposed registry key: `mojo`
- Existing family or aliases checked: `python` / `hash_style` is wrong because
  its registry contract includes triple-quoted blocks; `dockerfile` /
  `hash_line_style` has the right marker but not Mojo's literal context.
- Classification: `language`
- Versions or releases checked: Modular documentation commit
  `83bacbc5121ef488bbc44f412703a70c97739a99` and Mojo compiler 0.26.2.0
  (`d627decc`).
- Dialects checked: `.mojo` source across the documented 0.x and 1.0 beta
  syntax; the comment form is common to both.
- Intended support scope: lexical source comments in ordinary Mojo files.
- Explicitly excluded scope: API docstrings, generated MLIR, notebooks, and
  comments belonging to foreign code stored in strings.

### Syntax contract

- Line comments: `#` through the physical line ending or EOF.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: a final line comment without a
  newline is valid; there is no block delimiter.
- Inline use: yes, including after an expression or statement.
- Adjacent-line grouping: yes for consecutive hash-comment lines.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: `#` is recognized only outside Mojo's quoted,
  triple-quoted, raw, and interpolated string literals.
- Conflicts with strings, operators, directives, or embedded languages:
  `"# literal"`, raw strings, and hashes inside API docstrings are data.
  Triple-quoted API documentation is explicitly a string literal, not a
  comment. `/* ... */` is invalid source, not a second comment form.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove one verified hash and at most its
  conventional following space; preserve payload hashes, indentation, Unicode,
  and physical line order. Never turn a docstring into comment text.

### Evidence

- Official documentation permalink:
  [code comments and docstrings](https://github.com/modular/modular/blob/83bacbc5121ef488bbc44f412703a70c97739a99/mojo/docs/manual/basics.mdx#L140-L175)
- Documentation version and relevant section: Modular repository state for
  Mojo 1.0.0 beta development, `Code comments`; it defines one-line `#`, shows
  inline use, and says docstrings are multiline string literals.
- Official implementation or grammar permalink: the compiler is distributed
  as a binary; the executable probe below is the implementation evidence.
- Conformance test or official example permalink:
  [multiline string forms](https://github.com/modular/modular/blob/83bacbc5121ef488bbc44f412703a70c97739a99/mojo/docs/manual/types.mdx#L670-L704)
- Dataset identity evidence:
  [Linguist Mojo entry](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L4811-L4820)
- Evidence conflicts or gaps: Modular does not publish the compiler lexer in
  this repository. Documentation and the installed compiler agree on both
  positive and negative forms.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: yes, with the official `mojo-compiler` executable.
- Exact version or commit: `Mojo 0.26.2.0 (d627decc)`.
- Probe method: `mojo build` on one valid source and one block-marker source.
- Probe input:

```mojo
fn main():
    var literal = "# not a comment"
    var value = 1 # inline comment
    print(literal, value) # comment at EOF
```

The valid file built with exit 0. Replacing the comment with
`/* not a Mojo comment */` failed at `/` with `unexpected token in expression`.
The probe confirms ordinary strings, inline/EOF hashes, and absence of the
C-style block form; the documentation supplies the wider literal inventory.

### Representative examples

```mojo
fn clamp(value: Int) -> Int:
    # Keep generated indices in range.
    return max(0, value) # lower bound
```

The two hash regions are comments. `comptime text = "# retained"` and a
triple-quoted API docstring are not.

### Adversarial boundaries

- Negative cases: every quoted/raw/triple-quoted string form, escaped quotes,
  interpolation containing a literal hash, API docstrings, and `/* ... */`.
- Malformed-input cases: unterminated strings next to `#` and a lone block
  opener must not expand a comment range.
- Line-ending and Unicode cases: LF, CRLF, EOF without newline, UTF-8 payload,
  and a payload containing additional hashes.
- Version or dialect counterexamples: Python triple-quoted strings and Python
  registry behavior must not be inherited merely because editor modes match.
- Cleaner preservation cases: inline spacing, consecutive comments, hashes in
  payload, blank comment lines, and docstrings left untouched.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `mojo`, wrapper `#`, a Mojo literal-
  aware contextual extractor, and a seeded inline example. Do not alias Mojo to
  the current Python or broad hash families.
- Deterministic tests to add: raw lookup; own-line/inline/EOF comments; all
  documented literal forms; docstring negative; invalid block form; CRLF; and
  sanitizer payload preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## OASv2-json

### Identity and scope

- Raw dataset label: `OASv2-json` (889,694 files; 16,898,942,639 tokens)
- Proposed registry key: `oasv2_json` for explicit unsupported lookup/accounting,
  not as an extraction family.
- Existing family or aliases checked: JSON, JSON with Comments, JSON5, and
  JavaScript. Extension formats are not valid aliases.
- Classification: `document-format`
- Versions or releases checked: OpenAPI/Swagger Specification 2.0 at OAI
  commit `5423da4b0c16a563a7226663018fcd9294be279d`; RFC 8259 JSON.
- Dialects checked: conforming JSON serialization only.
- Intended support scope: no comment extraction from conforming OAS 2 JSON.
- Explicitly excluded scope: JSONC, JSON5, JavaScript object literals, vendor
  parser extensions, and comments in source files that generate an OAS file.

### Syntax contract

- Line comments: `unsupported`.
- Block comments: `unsupported`.
- Nested comments: `unsupported`.
- Termination at newline, delimiter, or EOF: not applicable.
- Inline use: `unsupported`.
- Adjacent-line grouping: `unsupported`.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: RFC 8259 defines a JSON text solely from
  structural tokens, strings, numbers, three literals, and four whitespace
  characters. It defines no comment token.
- Conflicts with strings, operators, directives, or embedded languages:
  `//`, `/*`, `*/`, and `#` may occur as ordinary characters inside a JSON
  string. Outside a string they make the document nonconforming rather than
  beginning a source comment.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: none.
- Content-preservation expectations: byte-preserving no-op; do not delete
  marker-looking string data or attempt to repair nonconforming JSON.

### Evidence

- Official documentation permalink:
  [Swagger 2.0 Format](https://github.com/OAI/OpenAPI-Specification/blob/5423da4b0c16a563a7226663018fcd9294be279d/versions/2.0.md#L49-L64)
- Documentation version and relevant section: OAS 2.0; descriptions are JSON
  objects conforming to JSON standards, with YAML as another representation.
- Official grammar permalink:
  [RFC 8259 section 2](https://www.rfc-editor.org/rfc/rfc8259.html#section-2)
- Implementation version, file, and relevant symbol: immutable RFC grammar,
  `JSON-text = ws value ws`; its exhaustive token and whitespace productions
  contain no comment rule.
- Conformance test or official example permalink: the OAS format section above
  provides conforming JSON; RFC 8259 section 9 says parsers may accept non-JSON
  extensions, which does not make those extensions JSON syntax.
- Dataset identity evidence:
  [Linguist OASv2-json entry](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L5203-L5213)
- Evidence conflicts or gaps: some editors and OAS tools accept comments as an
  extension. The standard explicitly scopes this label to JSON, so extension
  acceptance is not portable evidence.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: normative OAS and JSON grammars inspected; no
  implementation-specific parser was treated as the oracle.
- Exact version or commit: OAI `5423da4b0c16a563a7226663018fcd9294be279d`;
  RFC 8259.
- Probe method: derive accepted tokens from the exhaustive JSON ABNF.
- Probe input:

```json
{
  "openapiMarker": "// data, /* data */, # data",
  "swagger": "2.0"
}
```

- Observed result: all marker text is string content. Moving any marker outside
  the string produces text outside the RFC grammar.
- Conclusion and limits of the probe: the format has no native comment syntax;
  vendor extensions are intentionally not generalized.

### Representative examples

```json
{
  "swagger": "2.0",
  "info": {"description": "Use https://host/#fragment"},
  "paths": {}
}
```

There are no comments. The URL fragment is string data.

### Adversarial boundaries

- Negative cases: marker-looking strings, escaped quotes, URI fragments,
  CommonMark text in `description`, regex strings, and `$ref` URI values.
- Malformed-input cases: `//`, `#`, or `/* ... */` outside strings remains
  invalid JSON and must not be accepted as a cleanable comment.
- Line-ending and Unicode cases: every RFC whitespace character, UTF-8 strings,
  escaped newlines, and EOF must remain byte-preserving.
- Version or dialect counterexamples: JSONC, JSON5, YAML, and tool-specific
  relaxed modes require their own labels/contracts.
- Cleaner preservation cases: input containing every marker in keys and values
  must be unchanged.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none for extraction; retain an explicit inventory
  disposition so `oasv2_json` cannot accidentally fall through to JavaScript.
- Deterministic tests to add: exact raw-label lookup raises
  `NotImplementedError`; a no-op fixture preserves marker strings; invalid
  outside-string markers never become matches.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## OASv2-yaml

### Identity and scope

- Raw dataset label: `OASv2-yaml` (312,891 files; 3,202,251,272 tokens)
- Proposed registry key: `oasv2_yaml`
- Existing family or aliases checked: `yaml` is the correct syntax owner, but
  its current placement in broad `hash_line_style` overmatches scalar data and
  must be corrected before aliasing this label.
- Classification: `document-format`
- Versions or releases checked: OpenAPI/Swagger 2.0 at OAI commit
  `5423da4b0c16a563a7226663018fcd9294be279d`; YAML 1.2.2 specification commit
  `1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a`.
- Dialects checked: conforming YAML representation of OAS 2 JSON objects.
- Intended support scope: YAML presentation comments in OAS 2 documents.
- Explicitly excluded scope: comments in JSON serialization, marker text in
  any scalar, embedded examples treated as scalar content, and templating
  preprocessors layered over an OAS file.

### Syntax contract

- Line comments: `#` plus non-break characters, only outside scalar content and
  separated from preceding tokens by YAML separation whitespace; an own-line
  comment may appear at any indentation level.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: a YAML line break or EOF ends the
  comment; EOF without a final line break must be accepted.
- Inline use: yes when separated from the preceding token. A hash joined to a
  plain scalar, as in `foo#bar`, remains scalar content.
- Adjacent-line grouping: yes only for actual consecutive YAML comment nodes.
  Do not group or recognize hash-looking lines that belong to a block scalar.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: single/double-quoted, plain, literal `|`, and
  folded `>` scalars protect their content according to YAML grammar. Parser
  indentation and scalar state, not a global hash regex, determine validity.
- Conflicts with strings, operators, directives, or embedded languages: URI
  fragments without separation are plain-scalar data; hashes in quoted and
  block scalars are data. `%YAML`/`%TAG` lines and document markers are
  directives/structure, not comments. OAS `example` and `description` values do
  not recursively introduce source comments inside their scalar content.
- Sanitizer line wrappers: `("#", "")` after retaining the source indentation
  used to establish YAML structure.
- Sanitizer block wrappers: none.
- Content-preservation expectations: strip only a verified comment indicator
  and conventional following space. Preserve payload hashes and never modify
  scalar bytes, indentation, chomping indicators, or document structure.

### Evidence

- Official documentation permalink:
  [Swagger 2.0 Format](https://github.com/OAI/OpenAPI-Specification/blob/5423da4b0c16a563a7226663018fcd9294be279d/versions/2.0.md#L49-L64)
- Documentation version and relevant section: OAS 2.0 permits YAML to represent
  the same Swagger JSON object.
- Official grammar permalink:
  [YAML 1.2.2 comments](https://github.com/yaml/yaml-spec/blob/1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a/spec/1.2.2/spec.md#L2791-L2853)
- Implementation version, file, and relevant symbols: YAML 1.2.2 productions
  `c-nb-comment-text`, `b-comment`, and `l-comment`.
- Conformance example permalink:
  [plain-scalar hash boundary](https://github.com/yaml/yaml-spec/blob/1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a/spec/1.2.2/spec.md#L4074-L4184)
- Dataset identity evidence:
  [Linguist OASv2-yaml entry](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L5214-L5225)
- Evidence conflicts or gaps: OAS 2.0 says YAML is a JSON superset without
  spelling out comment behavior. YAML's own normative grammar supplies that
  presentation-layer contract.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: normative OAS and YAML grammars inspected; no one
  YAML library was used to broaden the standard.
- Exact version or commit: OAI `5423da4b0c16a563a7226663018fcd9294be279d`;
  YAML spec `1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a`.
- Probe method: traced YAML separation, plain-scalar, quoted-scalar, and block-
  scalar productions.
- Probe input:

```yaml
swagger: "2.0" # format version
host: api.example.test#blue
description: |
  # This hash is API description content.
# This is a presentation comment.
paths: {}
```

- Observed result: only the separated inline hash and final own-line hash are
  comments; the joined and block-scalar hashes are content.
- Conclusion and limits of the probe: a contextual YAML scanner is required;
  a delimiter-only regex cannot implement the normative boundary.

### Representative examples

```yaml
swagger: "2.0" # required version
# Public operations
paths:
  /pets: {}
```

The two separated hash regions are comments.

### Adversarial boundaries

- Negative cases: all scalar styles, URI fragments, `foo#bar`, quoted examples,
  block-scalar hashes, directives, anchors/tags, and JSON input.
- Malformed-input cases: invalid indentation, an unterminated quote, malformed
  flow collections, and a hash after a token without separation.
- Line-ending and Unicode cases: YAML's recognized line breaks, EOF comment,
  Unicode payload/scalars, BOM, and Unicode separation boundaries.
- Version or dialect counterexamples: YAML 1.1 resolution differences do not
  change the common hash boundary; templated OAS dialects are excluded.
- Cleaner preservation cases: indentation, payload hashes, empty comments,
  scalar/chomping indicators, and marker-looking block content.

### Decision

- Recommended action: `alias`
- Registry fields to change: move `yaml` out of broad `hash_line_style` into a
  YAML structural/contextual family, then add `oasv2_yaml` as an exact alias.
  Do not add OAS-specific delimiters.
- Deterministic tests to add: raw lookup; own-line/separated inline/EOF;
  plain/quoted/block scalar negatives; URI fragments; directives; flow and
  indentation contexts; all line endings; and sanitizer preservation.
- Remaining blocker: none after the shared YAML correction.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## NMODL

### Identity and scope

- Raw dataset label: `NMODL` (157,178 files; 263,616,987 tokens)
- Proposed registry key: `nmodl`
- Existing family or aliases checked: none combines NMODL's two punctuation
  line forms with its keyword-delimited block.
- Classification: `language`
- Versions or releases checked: BlueBrain NMODL transpiler commit
  `06132d23125bf6d65b0cc7b7136754ed378969d9`.
- Dialects checked: modern NEURON NMODL accepted by the BlueBrain lexer.
- Intended support scope: lexical comments in `.mod` mechanism source.
- Explicitly excluded scope: C/C++ text inside `VERBATIM ... ENDVERBATIM`,
  legacy parser extensions not accepted by the pinned lexer, and simulator
  output.

### Syntax contract

- Line comments: `:` or `?` through CR, LF, CRLF, or EOF. Either marker may be
  used own-line or inline outside a string or copy-mode block.
- Block comments: exact uppercase `COMMENT` through exact uppercase
  `ENDCOMMENT`.
- Nested comments: no. A second `COMMENT` is body text and the first
  `ENDCOMMENT` closes; the official construct corpus classifies nesting as
  invalid.
- Termination at newline, delimiter, or EOF: line forms accept EOF. A block
  requires `ENDCOMMENT`; EOF in copy mode reports an unexpected EOF and does
  not produce a complete block-comment token.
- Inline use: yes. Punctuation forms begin wherever their marker is lexically
  reached. A block keyword is recognized as its own token, not as a prefix of a
  longer identifier such as `COMMENTARY`.
- Adjacent-line grouping: yes for consecutive `:` and/or `?` comment lines.
- Unclosed delimiter behavior: invalid; do not match `COMMENT` through EOF.
- Lexical or structural context: double-quoted strings are recognized before
  punctuation comments. Flex longest-match rules protect ontology identifiers
  such as `NCIT:C17145` and longer identifiers containing `COMMENT`.
- Conflicts with strings, operators, directives, or embedded languages:
  colons and question marks inside strings are data. `VERBATIM` opens embedded
  C/C++ copied as one foreign-language block; C comments inside it are not
  NMODL comments. The implementation shares one copy mode for `COMMENT` and
  `VERBATIM`, so mismatched `ENDVERBATIM`/`ENDCOMMENT` is malformed input and
  must not be normalized into a valid comment.
- Sanitizer line wrappers: `("?", "")` and `(":", "")`, after source
  indentation is separated from the marker.
- Sanitizer block wrappers: `("COMMENT", "ENDCOMMENT")`.
- Content-preservation expectations: preserve punctuation and keywords inside
  the payload, all block newlines, and embedded-looking text. Remove only the
  verified outer wrapper.

### Evidence

- Official documentation permalink:
  [supported NMODL constructs](https://github.com/BlueBrain/nmodl/blob/06132d23125bf6d65b0cc7b7136754ed378969d9/docs/language.rst#L89-L149)
- Documentation version and relevant section: pinned transpiler support table;
  `COMMENT` is supported. The project tutorial also names `?`, `:`, and
  `COMMENT` as comments.
- Official implementation or grammar permalink:
  [NMODL Flex lexer](https://github.com/BlueBrain/nmodl/blob/06132d23125bf6d65b0cc7b7136754ed378969d9/src/lexer/nmodl.ll#L137-L151)
- Implementation version, file, and relevant symbols: same commit,
  `src/lexer/nmodl.ll`; punctuation rules are at
  [lines 413-419](https://github.com/BlueBrain/nmodl/blob/06132d23125bf6d65b0cc7b7136754ed378969d9/src/lexer/nmodl.ll#L413-L419)
  and copy-mode close/EOF behavior at
  [lines 425-467](https://github.com/BlueBrain/nmodl/blob/06132d23125bf6d65b0cc7b7136754ed378969d9/src/lexer/nmodl.ll#L425-L467).
- Conformance test or official example permalink:
  [nested COMMENT is invalid](https://github.com/BlueBrain/nmodl/blob/06132d23125bf6d65b0cc7b7136754ed378969d9/test/unit/utils/nmodl_constructs.cpp#L119-L131)
- Dataset identity evidence:
  [Linguist NMODL entry](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L4956-L4963)
- Evidence conflicts or gaps: line comments are currently discarded rather
  than returned as AST nodes, but their lexer actions unambiguously define the
  source ranges. No dedicated test covers every malformed cross-closer.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: source-level lexer and official invalid-construct
  corpus inspected; no local C++ build was run.
- Exact version or commit: `06132d23125bf6d65b0cc7b7136754ed378969d9`.
- Probe method: traced Flex longest-match selection and `COPY_MODE` actions.
- Probe input:

```nmodl
SUFFIX example : suffix note
? own-line note
COMMENT
outer COMMENT text
ENDCOMMENT
VERBATIM
/* foreign C, not NMODL */
ENDVERBATIM
```

- Observed result: both punctuation tails are discarded, the block returns one
  `BLOCK_COMMENT`, and the `VERBATIM` region returns a foreign-code token.
- Conclusion and limits of the probe: the implementation source establishes
  exact matching and malformed EOF; a compiled smoke probe remains useful but
  is not a blocker.

### Representative examples

```nmodl
NEURON {
    SUFFIX example : mechanism suffix
}
? Parameter notes follow
COMMENT
This mechanism is used for regression coverage.
ENDCOMMENT
```

The `:`, `?`, and `COMMENT ... ENDCOMMENT` regions are three comments.

### Adversarial boundaries

- Negative cases: quoted `"https://host:443/?x"`, `NCIT:C17145`,
  `COMMENTARY`, an outside-block `ENDCOMMENTED` identifier, and all marker text
  in `VERBATIM`. Inside a block, the `ENDCOMMENT` prefix in `ENDCOMMENTED`
  closes the block and must receive an exact-boundary regression.
- Malformed-input cases: unclosed block, nested block, stray `ENDCOMMENT`, and
  each mismatched copy-mode closer.
- Line-ending and Unicode cases: LF, CRLF, CR, EOF line comments, multiline
  Unicode block payload, and no CR leakage into a line match.
- Version or dialect counterexamples: embedded C comment conventions and
  older translator-specific extensions remain outside this key.
- Cleaner preservation cases: payload colons/question marks, the word
  `COMMENT`, leading indentation, empty block lines, and keyword-like prose.

### Decision

- Recommended action: `implement`
- Registry fields to change: add canonical `nmodl`, two line patterns, one
  non-nested keyword block contract, explicit wrappers, and representative
  seeds for all three forms. Protect strings/ontology IDs and exclude verbatim
  spans before matching.
- Deterministic tests to add: raw lookup; own-line/inline/EOF line forms;
  keyword block; non-nesting; unclosed and cross-closer malformed cases;
  strings, ontology IDs, identifiers, `VERBATIM`, all line endings, and
  sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Noir

### Identity and scope

- Raw dataset label: `Noir` (22,554 files; 101,989,819 tokens)
- Proposed registry key: `noir`
- Existing family or aliases checked: `rust` / `rust_style`; its intended
  contract matches, but the current registry incorrectly models Rust blocks as
  non-nested and must be corrected before adding Noir.
- Classification: `language`
- Versions or releases checked: Noir `nightly-2026-08-01`, commit
  `d89d99a9442295afa676633d9433291377f7d3b2`.
- Dialects checked: `.nr` source accepted by `noirc_frontend`.
- Intended support scope: all lexer comment tokens, including documentation
  variants, in Noir source.
- Explicitly excluded scope: generated ACIR/Brillig, Rust host code, and
  delimiter text inside Noir literals.

### Syntax contract

- Line comments: `//` through LF or EOF. `//!` is inner documentation and
  exactly `///` is outer documentation; four or more leading slashes are an
  ordinary line comment after the initial `//`.
- Block comments: `/* ... */`; `/*!` and eligible `/**` are documentation
  variants.
- Nested comments: yes, recursively for every `/*` encountered before the
  balancing `*/`, including doc-looking nested openers.
- Termination at newline, delimiter, or EOF: the line scanner stops only at LF;
  in CRLF input the CR is part of the lexer span before LF, and lone CR does not
  terminate. Blocks require balanced closure.
- Inline use: yes for line and block forms.
- Adjacent-line grouping: yes for consecutive line comments, including mixed
  ordinary and documentation wrappers.
- Unclosed delimiter behavior: an unclosed block raises
  `UnterminatedBlockComment`; do not accept it through EOF.
- Lexical or structural context: ordinary, raw, byte, and format strings are
  tokenized as literals; marker text wholly inside them is data. Comments may
  appear in genuine expression portions where the lexer has re-entered code.
- Conflicts with strings, operators, directives, or embedded languages: `/`
  remains division unless followed by `/` or `*`. `/**/` and `/***/` are
  ordinary blocks rather than outer docs under the lexer's lookahead rule.
  Compiler attributes beginning `#[` are not hash comments.
- Sanitizer line wrappers: longest semantic forms first, `("//!", "")`,
  `("///", "")`, then `("//", "")`, while `////` retains two payload slashes.
- Sanitizer block wrappers: `("/*!", "*/")`, eligible `("/**", "*/")`, and
  `("/*", "*/")`; strip only the outer pair and preserve nested delimiters.
- Content-preservation expectations: retain nested delimiter text, doc payload,
  Unicode, and line structure. Invalid blocks remain unchanged.

### Evidence

- Official documentation permalink:
  [Noir comments](https://github.com/noir-lang/noir/blob/d89d99a9442295afa676633d9433291377f7d3b2/docs/docs/language/comments.md#L1-L30)
- Documentation version and relevant section: pinned nightly documentation;
  it defines `//` and `/* ... */`.
- Official implementation or grammar permalink:
  [line and nested block scanners](https://github.com/noir-lang/noir/blob/d89d99a9442295afa676633d9433291377f7d3b2/compiler/noirc_frontend/src/lexer/lexer.rs#L888-L990)
- Implementation version, file, and relevant symbols: nightly commit,
  `parse_comment` and `parse_block_comment`; slash dispatch is at
  [lines 290-301](https://github.com/noir-lang/noir/blob/d89d99a9442295afa676633d9433291377f7d3b2/compiler/noirc_frontend/src/lexer/lexer.rs#L290-L301).
- Conformance test or official example permalink:
  [ordinary/doc and nested tests](https://github.com/noir-lang/noir/blob/d89d99a9442295afa676633d9433291377f7d3b2/compiler/noirc_frontend/src/lexer/lexer.rs#L1255-L1301)
- Dataset identity evidence:
  [Linguist Noir entry](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L5137-L5148)
- Evidence conflicts or gaps: the prose page still says native doc comments
  are unsupported, while the same pinned compiler and its tests explicitly
  classify `///`, `//!`, `/**`, and `/*!`. Compiler behavior is authoritative
  for extraction at this nightly.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official lexer unit tests and implementation source
  inspected; no local Rust build was run.
- Exact version or commit: `nightly-2026-08-01`,
  `d89d99a9442295afa676633d9433291377f7d3b2`.
- Probe method: traced depth increments/decrements and documentation lookahead.
- Probe input:

```rust
/// Outer documentation.
fn main(x: Field) {
    /* outer /* inner */ outer */
    assert(x != 0); // line at EOF
}
```

- Observed result: the first and final forms are line-comment tokens; the block
  balances at depth two. The official unclosed path returns a lexer error.
- Conclusion and limits of the probe: source and tests establish the full
  nesting contract; line-ending edge cases still require project regressions.

### Representative examples

```rust
//! Module note.
fn constrain(x: Field) {
    /* outer /* audit note */ outer */
    assert(x != 0); // reject zero
}
```

All three indicated regions are comments; the block is one nested match.

### Adversarial boundaries

- Negative cases: all string forms containing markers, division, `/ *`,
  attributes, and slash pairs in non-code literal portions.
- Malformed-input cases: unclosed outer/inner block, stray `*/`, `/* */ */`,
  and doc-looking edge forms `////`, `/**/`, and `/***/`.
- Line-ending and Unicode cases: LF, CRLF including exact CR span behavior,
  lone CR, EOF line comment, UTF-8 payload, and rejected bidi/lookalike spaces.
- Version or dialect counterexamples: older documentation does not define doc
  semantics; extraction scope follows the pinned lexer, not Rust tooling.
- Cleaner preservation cases: mixed doc wrappers, nested delimiter payload,
  four-slash lines, star gutters, and invalid unclosed input.

### Decision

- Recommended action: `alias`
- Registry fields to change: first correct `rust_style` to use nested
  `("/*", "*/")` delimiters instead of a non-nested block regex, then add
  `noir` as an alias with pinned evidence and doc seeds.
- Deterministic tests to add: raw lookup; ordinary/doc line and block variants;
  recursive nesting; doc lookahead edge forms; strings/division/attributes;
  unclosed blocks; CRLF/lone-CR/EOF; and nested sanitizer preservation. Existing
  Rust tests must prove the family correction does not regress Rust.
- Remaining blocker: none after the shared Rust correction.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Nushell

### Identity and scope

- Raw dataset label: `Nushell` (93,004 files; 123,099,582 tokens)
- Proposed registry key: `nushell`
- Existing family or aliases checked: the current `nu` alias is a mapping
  collision, not a synonym. Linguist defines `Nu` (Scheme-like, interpreter
  `nush`) and `Nushell` (shell, interpreter `nu`) as separate languages that
  happen to share `.nu`; the current hash-line mapping cannot be retained for
  the unrelated `Nu` key without independent evidence.
- Classification: `language`
- Versions or releases checked: Nushell commit
  `4c6dcc59d6ea3f42ce434cfd0da3d422deb776c9` and Book commit
  `bef55b50ba8cdf93a576dd142971294253cb4d98`.
- Dialects checked: `.nu` scripts and modules parsed by current Nushell.
- Intended support scope: Nushell line comments outside literal/bare-word data.
- Explicitly excluded scope: byte-zero shebang, the unrelated Nu language,
  HJSON/NUON data syntax, and foreign-shell code handled by another parser.

### Syntax contract

- Line comments: `#` only when it begins a lexer item or is preceded inside
  that item by whitespace. A top-level comment token runs through the next LF
  or EOF and retains a preceding CR; inside a compound item, either CR or LF
  leaves comment mode. `test#testing` and `nixpkgs#hello` are bare-word data.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: CR or LF ends an in-item comment;
  the top-level comment token ends before LF and accepts EOF. A bare CR does
  not terminate a top-level comment, and CR in CRLF belongs to that token's
  source span.
- Inline use: yes when separated by whitespace; own-line comments are valid.
- Adjacent-line grouping: yes for consecutive comment lines. Comments can also
  participate in Nushell's pipeline continuation parsing, but extraction ranges
  remain individual physical lines before grouping.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: single-, double-, backtick-, and raw-string
  forms protect hashes. Paired `[]`, `{}`, and `()` items are tracked so a
  comment within a compound token ends at its physical newline without
  swallowing the remaining delimiters.
- Conflicts with strings, operators, directives, or embedded languages: a
  byte-zero `#!` line is an executable shebang and must be excluded. Hashes in
  bare words, paths, URLs, cell/path-like values, or quoted/raw strings are
  data unless the lexer boundary rule is satisfied.
- Sanitizer line wrappers: `("#", "")`; never sanitize the excluded shebang.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve body hashes such as
  `# celebrates an event # for a person`, indentation, help Markdown, and
  exact content used for command/parameter descriptions. Preserve the pinned
  lexer's distinct top-level and compound-item CR behavior in source ranges.

### Evidence

- Official documentation permalinks:
  [comment documentation and required inline space](https://github.com/nushell/nushell.github.io/blob/bef55b50ba8cdf93a576dd142971294253cb4d98/book/custom_commands.md#L856-L936)
  and [shebang syntax](https://github.com/nushell/nushell.github.io/blob/bef55b50ba8cdf93a576dd142971294253cb4d98/book/scripts.md#L159-L180)
- Documentation version and relevant sections: current Nushell Book,
  `Documenting Your Command` and `Shebangs`.
- Official implementation or grammar permalink:
  [Nushell lexer boundary and literal states](https://github.com/nushell/nushell/blob/4c6dcc59d6ea3f42ce434cfd0da3d422deb776c9/crates/nu-parser/src/lex.rs#L87-L260)
- Implementation version, file, and relevant symbols: pinned main commit,
  `lex_item` and top-level comment tokenization at
  [lines 637-675](https://github.com/nushell/nushell/blob/4c6dcc59d6ea3f42ce434cfd0da3d422deb776c9/crates/nu-parser/src/lex.rs#L637-L675).
- Conformance test or official example permalink:
  [hash-boundary lexer tests](https://github.com/nushell/nushell/blob/4c6dcc59d6ea3f42ce434cfd0da3d422deb776c9/crates/nu-parser/tests/test_lex.rs#L147-L197)
  and [bare-word negative cases](https://github.com/nushell/nushell/blob/4c6dcc59d6ea3f42ce434cfd0da3d422deb776c9/crates/nu-parser/tests/test_lex.rs#L229-L278)
- Mapping evidence:
  [distinct Nu and Nushell entries](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L5149-L5202)
- Mapping counterexample:
  [pinned Nu sample using semicolon comments](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/samples/Nu/RandomApp.nu)
- Evidence conflicts or gaps: the lexer tokenizes a shebang as a comment-shaped
  token, while module parsing and official docs give it directive semantics.
  The extraction contract deliberately follows the semantic distinction.
  Top-level and compound-item comment paths also differ at CR. This review
  does not establish a complete contract for the separate Nu language.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned lexer and official tests inspected; no local
  `nu` binary was required.
- Exact version or commit: `4c6dcc59d6ea3f42ce434cfd0da3d422deb776c9`.
- Probe method: traced top-level `#`, in-item whitespace detection, quote
  states, the two distinct CR/LF paths, and module shebang suppression.
- Probe input:

```nu
#!/usr/bin/env nu
let flake = nixpkgs#hello
let url = 'https://example.test/#fragment'
print $flake # actual comment
```

- Observed result: the shebang is semantically ignored as module description,
  the two embedded hashes remain item data, and only the whitespace-separated
  final hash begins an ordinary comment.
- Conclusion and limits of the probe: source and official tests establish the
  boundary and the asymmetric CR behavior. Exact non-ASCII whitespace behavior
  remains outside the promise until Nushell documents it.

### Representative examples

```nu
# Return paths for the selected profile.
def profile-paths [name: string] {
  $env.HOME | path join $"profiles/($name)" # local profile root
}
```

Both separated hash regions are comments. `profiles#stable` is a bare word.

### Adversarial boundaries

- Negative cases: byte-zero shebang, `foo#bar`, `nixpkgs#hello`, URI fragments,
  all quote/raw forms, hashes in cell paths, and the unrelated Nu language.
- Malformed-input cases: unclosed strings/raw strings, unbalanced delimiters,
  a hash immediately after a closing/opening delimiter, and a trailing escape.
- Line-ending and Unicode cases: LF, CRLF with top-level CR retained, bare CR
  continuing a top-level comment, in-item CR termination, EOF, UTF-8 body text,
  tabs before inline comments, and non-ASCII whitespace treated conservatively.
- Version or dialect counterexamples: NUON and HJSON have their own parsers;
  `.nu` alone cannot disambiguate Nu from Nushell without the dataset label.
- Cleaner preservation cases: command-help paragraphs, blank hash lines,
  payload hashes, inline argument descriptions, and shebang byte preservation.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: remove `nu` from `hash_line_style` and leave that
  separate language unresolved pending its own evidence. Add canonical
  `nushell` with a quote/raw-string and item-boundary-aware hash extractor, a
  byte-zero shebang exclusion, and the lexer's path-specific CR handling.
- Deterministic tests to add: exact raw mapping, explicit non-equality with an
  unsupported `nu`, own-line/inline/tab/EOF comments, bare-word/path/URI/quoted
  negatives, shebang, compound delimiters, both CR paths, grouping, and
  sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## MoonBit

### Identity and scope

- Raw dataset label: `MoonBit` (13,220 files; 209,134,148 tokens)
- Proposed registry key: `moonbit`
- Existing family or aliases checked: `qsharp` / `slash_line_style` has the
  ordinary delimiter but cannot protect MoonBit literals or exclude semantic
  comment-encoded directives.
- Classification: `language`
- Versions or releases checked: language documentation commit
  `24f6b9a0b9ac997119ecd3069825edf65d3473fe` and compiler commit
  `d4ada10d212b5376f7f8bf49cd2fbaa275a395df` (0.10.x source line).
- Dialects checked: ordinary `.mbt` source. Literate `.mbt.md` is separate.
- Intended support scope: non-semantic lexical comments in compiled MoonBit
  source, including ordinary and documentation comments.
- Explicitly excluded scope: literate Markdown containers, `//!` header
  directives, recognized doc-comment pragmas, and marker text in literals.

### Syntax contract

- Line comments: `//`; `///` is a documentation subset, and own-line `///|` is
  an empty documentation separator.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: line comments end at MoonBit
  newline or EOF. The lexical newline set is LF, CR, CRLF, U+2028, and U+2029.
- Inline use: yes for ordinary comments. `///` documentation applies immediately
  before top-level items, and `///|` is an own-line top-level separator.
- Adjacent-line grouping: yes for consecutive ordinary or documentation lines;
  preserve each physical wrapper when determining semantic exclusions.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: normal strings, character/byte literals, and
  raw or interpolated multiline lines (`#|` and `$|`) protect slash pairs.
  Comments are rejected inside string interpolation expressions.
- Conflicts with strings, operators, directives, or embedded languages:
  initial `//!key:value` records are parsed by `Parsing_header_parser` and are
  directives. Attached comment lines whose post-slash text is a recognized
  `@alert`, `@intrinsic`, `@gen_js`, or `@coverage.skip` pragma affect compiler
  behavior. Both forms must be excluded from prose extraction. Slash pairs in
  string and multiline-string content are data.
- Sanitizer line wrappers: longest first, `("///|", "")`, `("///", "")`,
  then `("//", "")`; semantic exclusions are never sanitized as comments.
- Sanitizer block wrappers: none.
- Content-preservation expectations: retain Markdown and doctest fences in doc
  comments, preserve ordinary payload, and reduce `///|` to an empty payload.

### Evidence

- Official documentation permalink:
  [comments, doc comments, and literate files](https://github.com/moonbitlang/moonbit-docs/blob/24f6b9a0b9ac997119ecd3069825edf65d3473fe/next/language/docs.md#L1-L96)
- Documentation version and relevant section: MoonBit documentation state
  retrieved 2026-08-01, `Comments and Documentation`.
- Official implementation permalinks:
  [`COMMENT` token action](https://github.com/moonbitlang/moonbit-compiler/blob/d4ada10d212b5376f7f8bf49cd2fbaa275a395df/src/lex_unicode_lex.ml#L1955-L1977),
  [`//!` header parser](https://github.com/moonbitlang/moonbit-compiler/blob/d4ada10d212b5376f7f8bf49cd2fbaa275a395df/src/parsing_header_parser.ml#L16-L33),
  and [doc pragma parser](https://github.com/moonbitlang/moonbit-compiler/blob/d4ada10d212b5376f7f8bf49cd2fbaa275a395df/src/docstring.ml#L161-L245)
- Implementation version, file, and relevant symbols: `token`,
  `parse_directive`, `parse_pragma`, and `of_comments` at the pinned compiler
  commit.
- Lexical conventions permalink:
  [newlines and literal forms](https://github.com/moonbitlang/moonbit-docs/blob/24f6b9a0b9ac997119ecd3069825edf65d3473fe/next/language/lexical-conventions.md#L15-L98)
- Dataset identity evidence:
  [Linguist MoonBit entry](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L4846-L4853)
- Evidence conflicts or gaps: the lexical-conventions page calls itself
  incomplete, but the comments page and compiler implementation agree. The
  generated lexer source does not retain a readable source regex.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned source and official documentation inspected;
  no MoonBit compiler binary was installed.
- Exact version or commit: compiler `d4ada10d212b5376f7f8bf49cd2fbaa275a395df`.
- Probe method: traced lexer `COMMENT` construction, interpolation rejection,
  header parsing, doc grouping, and pragma recognition.
- Probe input:

```moonbit
//!build:wasm
let url = "https://example.test/a//b"
/// Return one.
/// @coverage.skip
fn one() -> Int { 1 } // ordinary note
```

- Observed result: all slash forms are lexer comments except the quoted pair;
  `//!build` becomes a header directive and the attached recognized `@` line
  becomes pragma metadata.
- Conclusion and limits of the probe: source inspection establishes the
  semantic exclusions; implementation tests must exercise exact source ranges.

### Representative examples

```moonbit
/// Return a stable retry count.
fn retries() -> Int {
  3 // configured default
}
///|
```

The three slash regions are comments. A `//!build:...` header or recognized
attached pragma is deliberately not an extraction match.

### Adversarial boundaries

- Negative cases: normal/byte/character literals, `#|` and `$|` multiline
  content, slash pairs in interpolation strings, `//!` headers, all four
  recognized pragma names, and `.mbt.md` prose/fences.
- Malformed-input cases: unterminated literals, a comment inside interpolation,
  and an unknown `@name` adjacent to a known pragma.
- Line-ending and Unicode cases: all five documented newline encodings, EOF,
  Unicode Markdown, and Unicode immediately around delimiters.
- Version or dialect counterexamples: literate Markdown is not plain `.mbt`;
  unknown doc annotations remain documentation text rather than directives.
- Cleaner preservation cases: `///|`, Markdown fences, payload slashes, blank
  doc lines, doctest labels, and excluded directives left byte-for-byte intact.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `moonbit`, the three sanitizer
  wrappers, and a lexer-aware helper that protects literals and suppresses
  header directives plus recognized attached pragmas.
- Deterministic tests to add: raw lookup; ordinary/doc/separator forms;
  inline/grouped/EOF; every literal category; directive and pragma exclusions;
  all newline forms; and longest-wrapper sanitizer behavior.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## OASv3-json

### Identity and scope

- Raw dataset label: `OASv3-json` (316,369 files; 7,799,403,508 tokens)
- Proposed registry key: `oasv3_json` for explicit unsupported accounting, not
  as an extraction family.
- Existing family or aliases checked: JSON, JSON with Comments, JSON5, and
  JavaScript; only strict JSON is part of the OAS format contract.
- Classification: `document-format`
- Versions or releases checked: OAS 3.0.4, 3.1.1, and 3.2.0 at OAI commit
  `5423da4b0c16a563a7226663018fcd9294be279d`; RFC 8259.
- Dialects checked: conforming JSON serializations across the OAS 3 release
  line.
- Intended support scope: no comment extraction from conforming OAS 3 JSON.
- Explicitly excluded scope: JSONC, JSON5, relaxed editor/tool parsers,
  embedding formats, and comments in code that generates the description.

### Syntax contract

- Line comments: `unsupported`.
- Block comments: `unsupported`.
- Nested comments: `unsupported`.
- Termination at newline, delimiter, or EOF: not applicable.
- Inline use: `unsupported`.
- Adjacent-line grouping: `unsupported`.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: each checked OAS 3 specification defines an
  OpenAPI document as a JSON object represented in JSON or YAML. RFC 8259's
  exhaustive JSON grammar has no comment production.
- Conflicts with strings, operators, directives, or embedded languages:
  marker text is permitted inside JSON strings. A marker outside a string is a
  non-JSON extension or syntax error, even if a particular OAS editor accepts
  it. CommonMark in `description`, schemas, and examples remains JSON value
  content.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: none.
- Content-preservation expectations: byte-preserving no-op for both valid and
  malformed inputs; do not silently convert relaxed JSON into a supported form.

### Evidence

- Official documentation permalinks:
  [OAS 3.0.4 Format](https://github.com/OAI/OpenAPI-Specification/blob/5423da4b0c16a563a7226663018fcd9294be279d/versions/3.0.4.md#L96-L120),
  [OAS 3.1.1 Format](https://github.com/OAI/OpenAPI-Specification/blob/5423da4b0c16a563a7226663018fcd9294be279d/versions/3.1.1.md#L98-L122),
  and [OAS 3.2.0 Format](https://github.com/OAI/OpenAPI-Specification/blob/5423da4b0c16a563a7226663018fcd9294be279d/versions/3.2.0.md#L44-L64)
- Documentation version and relevant section: every checked v3 line requires a
  JSON object represented in JSON or YAML; 3.2 names RFC 8259 directly.
- Official grammar permalink:
  [RFC 8259 section 2](https://www.rfc-editor.org/rfc/rfc8259.html#section-2)
- Implementation version, file, and relevant symbol: immutable ABNF,
  `JSON-text`, `ws`, and the exhaustive token productions.
- Conformance test or official example permalink: the three OAS format sections
  contain conforming JSON examples without an extension grammar.
- Dataset identity evidence:
  [Linguist OASv3-json entry](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L5226-L5236)
- Evidence conflicts or gaps: tools may accept extensions under parser options;
  no OAS version checked standardizes those extensions.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: normative OAS versions and RFC grammar inspected.
- Exact version or commit: OAI `5423da4b0c16a563a7226663018fcd9294be279d`;
  RFC 8259.
- Probe method: compare candidate bytes against the JSON token grammar.
- Probe input:

```json
{
  "openapi": "3.2.0",
  "description": "// text; /* text */; # text",
  "paths": {}
}
```

- Observed result: marker characters are string data. The same bytes between
  members are outside JSON grammar.
- Conclusion and limits of the probe: native comments are absent in every
  checked OAS 3 JSON version; vendor modes remain out of scope.

### Representative examples

```json
{
  "openapi": "3.1.1",
  "info": {"title": "API #1", "version": "1"},
  "paths": {}
}
```

There are no comments; the hash is content.

### Adversarial boundaries

- Negative cases: all marker strings, URI fragments, escaped solidus, regex or
  CommonMark values, JSON Schema annotations, and examples containing code.
- Malformed-input cases: `//`, `#`, or `/* ... */` between JSON tokens must not
  become extraction matches.
- Line-ending and Unicode cases: RFC whitespace, UTF-8 values, escaped line
  endings, BOM handling, and EOF are all preservation cases.
- Version or dialect counterexamples: 3.0, 3.1, and 3.2 agree; JSONC/JSON5 and
  embedding formats require independent labels.
- Cleaner preservation cases: every marker in keys/values and malformed
  extension text remains unchanged.

### Decision

- Recommended action: `unsupported`
- Registry fields to change: none for extraction; keep an explicit
  `oasv3_json` disposition so normalization cannot map it to JavaScript.
- Deterministic tests to add: raw-label lookup raises
  `NotImplementedError`; no-op preservation for marker strings; outside-string
  markers produce no supported comment ranges.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## OASv3-yaml

### Identity and scope

- Raw dataset label: `OASv3-yaml` (562,171 files; 5,807,407,004 tokens)
- Proposed registry key: `oasv3_yaml`
- Existing family or aliases checked: OAS 3 adopts YAML's own presentation
  syntax. The existing `yaml` key is conceptually correct but its broad hash
  regex must be replaced with structural YAML handling first.
- Classification: `document-format`
- Versions or releases checked: OAS 3.0.4, 3.1.1, and 3.2.0 at OAI commit
  `5423da4b0c16a563a7226663018fcd9294be279d`; YAML 1.2.2 at commit
  `1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a`.
- Dialects checked: YAML representation common to the OAS 3 release line.
- Intended support scope: YAML presentation comments in conforming OAS 3
  documents.
- Explicitly excluded scope: JSON serialization, scalars/examples containing
  marker text, templating overlays, and comments in referenced non-YAML media.

### Syntax contract

- Line comments: `#` plus non-break characters outside scalar content, either
  on its own line or separated from a preceding token by YAML whitespace.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: a YAML line break or EOF ends the
  comment. Missing final line break is explicitly accepted.
- Inline use: yes with required separation. `foo#bar` and URI fragments joined
  to a plain scalar are content.
- Adjacent-line grouping: yes for consecutive YAML comment nodes only; scalar
  lines that start with `#` remain scalar data.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: plain, single/double-quoted, literal, and
  folded scalar states protect hashes. Indentation and flow context must be
  parsed sufficiently to distinguish comments from scalar content.
- Conflicts with strings, operators, directives, or embedded languages:
  `%YAML`, `%TAG`, `---`, `...`, anchors, aliases, and tags are YAML structure,
  not comments. OAS `description`, `example`, Schema Object, and extension
  values do not introduce a second source-comment layer inside scalar content.
- Sanitizer line wrappers: `("#", "")` after structural validation.
- Sanitizer block wrappers: none.
- Content-preservation expectations: preserve source indentation and all scalar
  bytes; remove only the verified presentation marker and conventional one
  space from extracted comment text.

### Evidence

- Official documentation permalinks:
  [OAS 3.0.4 Format](https://github.com/OAI/OpenAPI-Specification/blob/5423da4b0c16a563a7226663018fcd9294be279d/versions/3.0.4.md#L96-L120)
  and [OAS 3.2.0 JSON/YAML compatibility](https://github.com/OAI/OpenAPI-Specification/blob/5423da4b0c16a563a7226663018fcd9294be279d/versions/3.2.0.md#L44-L64)
- Documentation version and relevant section: all v3 versions allow JSON or
  YAML; 3.0/3.1 recommend YAML 1.2 and 3.2 retains YAML 1.2 compatibility.
- Official grammar permalink:
  [YAML 1.2.2 comments](https://github.com/yaml/yaml-spec/blob/1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a/spec/1.2.2/spec.md#L2791-L2853)
- Implementation version, file, and relevant symbols: YAML productions
  `c-nb-comment-text`, `b-comment`, `s-b-comment`, and `l-comment`.
- Conformance example permalink:
  [plain-scalar boundary and URI fragment](https://github.com/yaml/yaml-spec/blob/1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a/spec/1.2.2/spec.md#L4074-L4184)
- Dataset identity evidence:
  [Linguist OASv3-yaml entry](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L5237-L5248)
- Evidence conflicts or gaps: OAS constraints narrow YAML data values for JSON
  round-tripping but do not redefine YAML presentation comments.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: OAS version texts and normative YAML grammar
  inspected; no library-specific extension was accepted.
- Exact version or commit: OAI `5423da4b0c16a563a7226663018fcd9294be279d`;
  YAML `1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a`.
- Probe method: traced separation and every scalar style in the grammar.
- Probe input:

```yaml
openapi: 3.2.0 # serialization version
info:
  title: API#blue
  description: >
    # Documentation content, not a source comment.
# Path operations
paths: {}
```

- Observed result: only the separated inline and final own-line hash regions
  are comments. The joined title and folded-scalar line are content.
- Conclusion and limits of the probe: OAS adds no delimiter; correct extraction
  depends on the shared YAML structural scanner.

### Representative examples

```yaml
openapi: 3.1.1 # dialect marker
# Stable public path
paths:
  /status: {}
```

The two separated hash regions are comments.

### Adversarial boundaries

- Negative cases: every scalar style, URI fragments, joined hashes, block
  scalar examples, flow collections, directives/tags, and JSON documents.
- Malformed-input cases: bad indentation, unclosed quotes/flows, invalid scalar
  headers, and an unseparated hash.
- Line-ending and Unicode cases: YAML line-break repertoire, EOF, UTF-8 body and
  scalar text, BOM, and Unicode around separation boundaries.
- Version or dialect counterexamples: all OAS v3 lines share this contract;
  templating products and YAML 1.1-only application behavior are excluded.
- Cleaner preservation cases: indentation, payload hashes, empty comments,
  folded/literal bodies, chomping indicators, and extension values.

### Decision

- Recommended action: `alias`
- Registry fields to change: after moving `yaml` to a YAML-aware contextual
  family, add `oasv3_yaml` as an alias. Share implementation with
  `oasv2_yaml`; add no OpenAPI-specific marker.
- Deterministic tests to add: raw lookup; OAS 3 version samples; own-line,
  separated inline, EOF and grouping; all scalar negatives; directives/flow;
  all line endings; and sanitizer preservation.
- Remaining blocker: none after the shared YAML correction.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Oberon

### Identity and scope

- Raw dataset label: `Oberon` (54,459 files; 18,173,477 tokens)
- Proposed registry key: `oberon`
- Existing family or aliases checked: `mathematica` /
  `nested_star_only_style`; its sole recursively nested `(* ... *)` contract
  matches standard Oberon and Oberon-2, but it cannot distinguish semantic
  compiler-control comments used by some Oberon implementations.
- Classification: `language`
- Versions or releases checked: original Oberon-2 language report (March 1995),
  Revised Oberon report 3.5 (2016), and Project Oberon scanner revision
  15.3.2017, plus Ulm Oberon compiler-control comments.
- Dialects checked: the `.ob2` classifier scope, the common Revised Oberon
  lexical contract, and a documented compiler-control counterexample.
- Intended support scope: unresolved for the aggregate raw label because the
  standard nested form and dialect control comments share an opener.
- Explicitly excluded scope: Active Oberon, Component Pascal, and implementation-
  specific compiler-control comments such as `(*$...*)` where a compiler gives
  the payload semantic meaning.

### Syntax contract

- Line comments: unsupported.
- Block comments: `(*` through the balancing `*)`.
- Nested comments: yes, recursively without a specified depth limit.
- Termination at newline, delimiter, or EOF: comments may span arbitrary line
  breaks and close only when nesting returns to zero.
- Inline use: yes; comments may be inserted between any two symbols.
- Adjacent-line grouping: not applicable as a line-comment operation; adjacent
  block comments remain separate ranges.
- Unclosed delimiter behavior: invalid. The official scanner reports
  `unterminated comment`; do not accept an EOF block.
- Lexical or structural context: strings are scanned as symbols before the
  comment path, so delimiter text inside a string is data. The scanner calls
  its comment routine recursively on each inner `(*`.
- Conflicts with strings, operators, directives, or embedded languages: `(`,
  `*`, `)`, multiplication, and parentheses are ordinary tokens when not paired.
  Standard comments have no meaning, but Ulm permits compiler options after
  `(*` with intervening whitespace, and XDS-compatible dialects also use
  comment-shaped controls. An exact `(*$` exclusion is therefore insufficient.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: `("(*", "*)")`; remove only the outer pair and
  retain every nested delimiter in the payload.
- Content-preservation expectations: preserve nested text, line structure,
  stars/parentheses, Unicode, and spacing; malformed blocks remain unchanged.

### Evidence

- Official documentation permalink:
  [The Programming Language Oberon-2](https://ssw.jku.at/Research/Papers/Oberon2.pdf)
- Documentation version and relevant section: Moessenboeck and Wirth, March
  1995, `Vocabulary`; comments are bracketed by `(*` and `*)` and may be nested.
- Version-matched official specification:
  [Revised Oberon report 3.5](https://people.inf.ethz.ch/wirth/Oberon/Oberon07.Report.pdf)
- Official implementation permalink:
  [Project Oberon scanner](https://people.inf.ethz.ch/wirth/ProjectOberon/Sources/ORS.Mod.txt)
- Official dialect counterexample:
  [Ulm Oberon compiler report](https://www.mathematik.uni-ulm.de/oberon/0.5/articles/oc.report.html)
- Implementation version, file, and relevant symbol: `ORS.Mod`, revision
  15.3.2017, recursive procedure `comment` and `Get` comment dispatch.
- Conformance test or official example permalink: the implementation source is
  itself Oberon and contains representative inline/nested-capable comments.
- Dataset identity evidence:
  [Linguist Oberon `.ob2` entry](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L5289-L5295)
- Evidence conflicts or gaps: Linguist's TextMate scope is Modula-2 and carries
  no compiler identity. Standard sources agree on nesting, while the Ulm
  compiler gives some comment-shaped regions semantic effect. The raw label
  supplies no dialect discriminator, and a single exact-prefix exclusion does
  not cover the documented control grammar.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: official scanner source inspected; no historical
  Oberon compiler was installed.
- Exact version or commit: `ORS.Mod` internal revision 15.3.2017; Oberon report
  revision 3.5/2016.
- Probe method: traced recursive calls at inner `(*` and EOF error path.
- Probe input:

```oberon
MODULE Example;
  (* outer (* nested rationale *) outer *)
BEGIN
END Example.
```

- Observed result: `comment` recursively consumes the inner pair, then closes
  the outer pair; EOF before either closer calls `Mark("unterminated comment")`.
- Conclusion and limits of the probe: the standard and implementation agree;
  compiler-control dialects remain outside the common contract.

### Representative examples

```oberon
MODULE Counter;
  VAR n: INTEGER; (* outer (* migration note *) retained *)
BEGIN
  n := 1
END Counter.
```

The nested block is one comment range.

### Adversarial boundaries

- Negative cases: `"(* literal *)"`, separated `( *`, multiplication followed
  by `)`, stray `*)`, `(*$...*)`, and whitespace-prefixed compiler controls.
- Malformed-input cases: unclosed outer/inner blocks and extra closers after a
  valid block.
- Line-ending and Unicode cases: LF, CRLF, CR, multiline UTF-8 payload, and EOF
  immediately after each delimiter prefix.
- Version or dialect counterexamples: Active Oberon/Component Pascal additions
  and implementation pragmas are not implied by the `.ob2` label.
- Cleaner preservation cases: nested delimiters, repeated stars, empty blocks,
  indentation, and malformed input.

### Decision

- Recommended action: `defer`
- Registry fields to change: none; do not alias `oberon` to
  `nested_star_only_style` until compiler-control regions can be identified
  without treating semantic directives as prose comments.
- Deterministic tests to add after resolution: raw lookup; standard
  inline/multiline/nested comments; strings and operators; unclosed forms;
  exact and whitespace-prefixed control comments; line endings; and sanitizer
  preservation.
- Remaining blocker: a deterministic dialect signal or an evidence-backed
  directive-aware scanner for the aggregate `.ob2` label.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01
