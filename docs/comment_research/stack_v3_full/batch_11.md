# Stack v3 Full Comment Research: batch_11

## Dataset provenance

- Dataset/project: `HuggingFaceCode/stack-v3-full`
- Statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics aggregated from
  `files[].language`
- Researcher or agent: `/root/research_batch_11`
- Review status: `reviewed`

The raw labels and file identities below are pinned to
[Linguist commit `af6f772`](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml).

## Vento

### Identity and scope

- Raw dataset label: `Vento` (3,381 files; 2,578,082 tokens)
- Proposed registry key: `vento`
- Existing family or aliases checked: template families using Jinja, Liquid,
  Handlebars, and Nunjucks delimiters; none uses Vento's complete contract.
- Classification: `template`
- Versions or releases checked: Vento commit
  `90a135acbaabb031382278e0903eea0e2c34857f`
- Dialects checked: standard `.vto` templates with the default trim plugin.
- Intended support scope: Vento template-layer comments, including optional
  left and right whitespace-trim controls.
- Explicitly excluded scope: comments in JavaScript expressions embedded in
  ordinary Vento tags, comments belonging to rendered HTML/JS/CSS, and other
  brace-template dialects.

### Syntax contract

- Line comments: unsupported at the Vento template layer.
- Block comments: `{{#` through the first `#}}`; a `-` immediately after the
  opener or before the closer is a trim control belonging to the wrapper.
- Nested comments: unsupported. An inner `{{#` is payload and the first `#}}`
  closes the outer comment.
- Termination at newline, delimiter, or EOF: comments may span lines and require
  `#}}`; an opener that reaches EOF is an unclosed-tag error.
- Inline use: yes, anywhere the raw template tokenizer encounters `{{#`,
  including within surrounding markup text.
- Adjacent-line grouping: no template-specific grouping beyond returning each
  complete comment in source order.
- Unclosed delimiter behavior: invalid; do not match from an unclosed opener to
  EOF.
- Lexical or structural context: the tokenizer searches raw template text for
  `{{`, then classifies `{{#` as a comment before parsing ordinary tags.
- Conflicts with strings, operators, directives, or embedded languages: quote
  characters and ordinary Vento tags inside a comment are payload. `{{` not
  followed by `#` is a tag, while a literal `{{#` in template output still
  starts a Vento comment unless produced indirectly.
- Sanitizer line wrappers: none.
- Sanitizer block wrappers: `("{{#", "#}}")`, plus the three combinations
  containing the left `{{#-` and/or right `-#}}` trim controls.
- Content-preservation expectations: remove the complete outer wrapper and its
  optional trim-control hyphens, but preserve all body text, braces, hashes,
  Unicode, whitespace, and line structure.

### Evidence

- Official documentation permalink:
  [Vento comment and trim syntax](https://github.com/ventojs/vento/blob/90a135acbaabb031382278e0903eea0e2c34857f/docs/4.syntax/8.comments.md#L1-L24)
- Documentation version and relevant section: pinned Vento documentation,
  `Comments` and `Trimming spaces`.
- Official implementation or grammar permalink:
  [comment branch in `tokenize`](https://github.com/ventojs/vento/blob/90a135acbaabb031382278e0903eea0e2c34857f/core/tokenizer.ts#L11-L42)
- Implementation version, file, and relevant symbol: commit above,
  `core/tokenizer.ts`, `tokenize`; unclosed-token rejection is in
  [`Environment.compile`](https://github.com/ventojs/vento/blob/90a135acbaabb031382278e0903eea0e2c34857f/core/environment.ts#L136-L147).
- Conformance test or official example permalink:
  [comment and trim tests](https://github.com/ventojs/vento/blob/90a135acbaabb031382278e0903eea0e2c34857f/test/comment.test.ts#L3-L37)
- Dataset identity evidence:
  [Linguist Vento entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8392-L8399)
- Evidence conflicts or gaps: none. The implementation's first-closer search
  makes non-nesting explicit.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned tokenizer, compiler guard, trim preprocessor,
  and official tests inspected; Deno was not installed for a runtime probe.
- Exact version or commit: `90a135acbaabb031382278e0903eea0e2c34857f`
- Probe method: traced the `string -> comment -> string` tokenizer states and
  the final-token validation.
- Probe input:

```vto
<h1>{{#- outer {{# inner #}} suffix -#}}</h1>
```

- Observed result: the first `#}}` closes the comment; ` suffix -#}}` is
  template text, demonstrating that comments do not nest.
- Conclusion and limits of the probe: source inspection fixes delimiters,
  trimming, first-close, and malformed-EOF behavior; it does not assert comment
  syntax for JavaScript embedded in non-comment tags.

### Representative examples

```vto
<h1>
  {{#- This heading is intentionally hidden. -#}}
  {{ title }}
</h1>
```

The complete `{{#- ... -#}}` region is one comment. `{{ title }}` is an
ordinary Vento tag and is not a comment.

### Adversarial boundaries

- Negative cases: `{{ value }}`, `{{ #}}`, a rendered string containing braces
  but no `{{#`, HTML `<!-- -->`, and JavaScript `//` or `/* */` in a tag.
- Malformed-input cases: missing `#}}`, `{{ #`, stray `#}}`, an inner opener,
  and mismatched trim-control placement.
- Line-ending and Unicode cases: LF, CRLF, CR, multiline Unicode payload, and
  an exact match that excludes surrounding line endings.
- Version or dialect counterexamples: Nunjucks `{# #}`, Jinja `{# #}`, and
  Handlebars `{{! }}` must not be inherited.
- Cleaner preservation cases: the valid empty comment `{{##}}`,
  body-leading/trailing hyphens that are not trim controls, nested-looking
  tags, hashes, blank lines, and indentation.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: add canonical `vento`, one complete non-greedy
  `{{# ... #}}` pattern, the four base/trim sanitizer wrapper pairs ordered
  most-specific first, and a seeded trim example.
- Deterministic tests to add: exact-label lookup; empty, inline/multiline, and
  trim combinations; first-close non-nesting; ordinary tags;
  embedded-language negatives; unclosed EOF; CRLF; exact slices; and sanitizer
  preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Visual Basic 6.0

### Identity and scope

- Raw dataset label: `Visual Basic 6.0` (980,267 files; 4,415,086,465 tokens)
- Proposed registry keys: `visual_basic_6_0` and `vb6`
- Existing family or aliases checked: `apostrophe_style`, canonical
  `visual_basic_net`, including the existing Visual Basic `Rem` contextual
  extractor.
- Classification: `dialect`
- Versions or releases checked: classic Visual Basic/VBA reference material
  carrying the legacy `vblr6.chm` help identifier and Microsoft VBA lexical
  specification revision 2021-02-16.
- Dialects checked: Visual Basic 6.0 source modules and the common VB6/VBA
  apostrophe and `Rem` forms; VB.NET documentation comments are excluded.
- Intended support scope: classic VB source comments in code portions of
  `.bas`, `.cls`, `.ctl`, `.Dsr`, and `.frm` files.
- Explicitly excluded scope: designer/resource serialization outside VB code,
  VB.NET XML documentation comments, and unverified host-specific preprocessor
  behavior.

### Syntax contract

- Line comments: an apostrophe starts a comment through the physical line end
  or EOF. Case-insensitive `Rem` is a comment statement at a statement start;
  a payload after `Rem` requires separating whitespace.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: the common verified contract ends
  at CRLF, CR, LF, or EOF. Microsoft formal VBA grammar also admits a
  `line-continuation` inside `comment-body`; that edge needs a VB6 executable
  probe before the VB6 key promises a multi-physical-line match.
- Inline use: apostrophe comments may directly follow a statement. An inline
  `Rem` statement must follow a colon; line-start `Rem` may follow whitespace,
  a line number, or a label boundary.
- Adjacent-line grouping: yes for adjacent independently marked apostrophe or
  `Rem` lines.
- Unclosed delimiter behavior: not applicable; EOF closes a line comment.
- Lexical or structural context: apostrophes and `Rem` inside double-quoted
  strings are data. `Rem` must be a complete case-insensitive keyword at a
  statement boundary, not the prefix of an identifier.
- Conflicts with strings, operators, directives, or embedded languages:
  doubled `""` escapes remain inside strings; `Remember`, `RemValue`, and
  `x = 1 Rem text` without a colon are not comments.
- Sanitizer line wrappers: `("'", "")` and case-insensitive `("Rem", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove only the verified marker and one
  syntactic separator after `Rem`; preserve apostrophes, colons, indentation,
  and all remaining body text.

### Evidence

- Official documentation permalink:
  [Microsoft `Rem` statement source](https://github.com/MicrosoftDocs/VBA-Docs/blob/b2cda886ea91e36c62eb1cb177133ad024ecd345/Language/Reference/User-Interface-Help/rem-statement.md#L12-L38)
- Documentation version and relevant section: legacy help topic
  `vblr6.chm1009000`, `Syntax`, `Remarks`, and `Example`; it specifies the
  apostrophe alternative, the space after `Rem`, and colon requirement.
- Official language specification:
  [MS-VBAL separator and special tokens](https://learn.microsoft.com/en-us/openspecs/microsoft_general_purpose_programming_languages/ms-vbal/7ef9ae86-dfdb-47f1-b53b-ef0c2ea9f8ed)
- Implementation version, file, and relevant symbol: no redistributable VB6
  lexer is available; the pinned Microsoft source and formal grammar are the
  primary evidence.
- Dataset identity evidence:
  [Linguist VB6 entry and aliases](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8478-L8494)
- Evidence conflicts or gaps: formal VBA permits a continuation sequence in an
  apostrophe `comment-body`, while later Visual Basic documentation says a
  comment cannot be continued. The common single-physical-line VB6 behavior is
  implemented; the extension remains explicitly outside this intake scope.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: pinned documentation and the branch's contextual
  `Rem` scanner inspected; no licensed VB6 compiler was available.
- Exact version or commit: documentation commit
  `b2cda886ea91e36c62eb1cb177133ad024ecd345`
- Probe method: applied the documented statement-boundary rules to minimal
  source and checked them against the local contextual scanner contract.
- Probe input:

```vb
100 Rem numbered note
value = "Rem and ' are data": Rem trailing note
other = "Remember" ' apostrophe note
Rem
```

- Observed result: the line-numbered and colon-separated `Rem` regions and the
  trailing apostrophe region are comments; the bare final `Rem` is also a valid
  empty comment statement. Both marker-looking string regions are data.
- Conclusion and limits of the probe: the primary forms and boundaries are
  conclusive; multi-physical-line comment continuation is not claimed.

### Representative examples

```vb
Private Sub Form_Load()
    Rem Initialize the form state.
    Caption = "Ready" ' Visible window title.
    Refresh: Rem Force the first paint.
End Sub
```

### Adversarial boundaries

- Negative cases: `Remember = True`, `RemValue`, `x = 1 Rem invalid`,
  `"Rem text"`, `"don't"`, and apostrophes in serialized designer strings.
- Malformed-input cases: `Rem:` and `Rem'payload` without required payload
  whitespace, a colon in a string, and an unterminated string before a marker.
- Line-ending and Unicode cases: LF, CRLF, CR, EOF, case variants, non-ASCII
  prose, line numbers, and labels.
- Version or dialect counterexamples: VB.NET `'''` XML documentation is outside
  VB6 scope; the unresolved VBA continuation form must not silently expand the
  key.
- Cleaner preservation cases: contractions and apostrophes in the body,
  colon-rich text, mixed marker blocks, and exact indentation.

### Decision

- Recommended action: `alias`
- Registry fields to change: keep `visual_basic_6_0` and `vb6` in the Visual
  Basic apostrophe family with the contextual `Rem` extractor; require
  whitespace or EOL after `Rem` and preserve line-number handling.
- Deterministic tests to add: exact-label and compact-alias lookup; apostrophe;
  line-start, numbered, colon-start, and bare `Rem`; string and identifier
  negatives; required whitespace before a nonempty `Rem` payload;
  CR/LF/CRLF/EOF; and sanitizer body preservation.
- Remaining blocker: a licensed/runtime VB6 probe is required only before
  adding the disputed multi-physical-line continuation extension.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## WebAssembly Interface Type

### Identity and scope

- Raw dataset label: `WebAssembly Interface Type` (57,122 files; 116,710,455
  tokens)
- Proposed registry keys: `webassembly_interface_type` and `wit`
- Existing family or aliases checked: `webassembly` is incompatible because
  WebAssembly text uses `;;` and nested `(; ;)`; C-style and Kotlin families do
  not carry WIT's exact line, string, documentation, and Unicode contract.
- Classification: `document-format`
- Versions or releases checked: Component Model WIT specification and
  `wit-parser` 0.255.0 from `wasm-tools` 1.255.0, commit
  `606b4cc5503015ce539e6d6a7ec39a774710e114`.
- Dialects checked: Component Model `.wit` source, including documentation
  comment forms.
- Intended support scope: lexical and documentation comments in valid WIT text.
- Explicitly excluded scope: core/component WebAssembly text, WAVE values,
  generated bindings, and marker text in WIT string literals.

### Syntax contract

- Line comments: `//` through the next LF or EOF; CRLF is folded to one LF by
  the official tokenizer.
- Block comments: `/* ... */`.
- Nested comments: yes, recursively and to arbitrary balanced depth.
- Termination at newline, delimiter, or EOF: line comments accept EOF; a block
  must have a balancing `*/` or the tokenizer returns `UnterminatedComment`.
- Inline use: yes for both forms wherever whitespace is accepted.
- Adjacent-line grouping: yes for consecutive `//` lines, including `///`
  documentation lines.
- Unclosed delimiter behavior: invalid and must not be returned as a complete
  verified block.
- Lexical or structural context: comments are whitespace tokens. `///` line
  docs and `/** ... */` block docs are comment subforms attached to following
  items, not new delimiter contracts.
- Conflicts with strings, operators, directives, or embedded languages:
  double-quoted core-name strings protect marker text; a lone `/` is an
  operator. UTF-8 BOM is accepted only at input start, while prohibited control
  and bidi code points invalidate the input even when visually hidden.
- Sanitizer line wrappers: `("//", "")`, retaining the third slash as doc
  payload unless a reviewed documentation-cleaning rule removes it.
- Sanitizer block wrappers: `("/*", "*/")`; nested inner delimiters remain
  payload.
- Content-preservation expectations: strip only one verified outer wrapper and
  preserve nested delimiters, doc-marker content, Unicode, and line structure.

### Evidence

- Official specification permalink:
  [WIT lexical comments](https://github.com/WebAssembly/component-model/blob/73b7ad51d3b5d6f1ef53c923d8c585e28b242bcc/design/mvp/WIT.md#L1017-L1039)
- Documentation version and relevant section: Component Model `WIT.md`,
  `Lexical structure`, `Whitespace`, and `Comments`; the
  [Component Model guide](https://component-model.bytecodealliance.org/design/wit.html#comments)
  separately documents nested and documentation forms.
- Official implementation or grammar permalink:
  [`wit-parser` comment scanner](https://github.com/bytecodealliance/wasm-tools/blob/606b4cc5503015ce539e6d6a7ec39a774710e114/crates/wit-parser/src/ast/lex.rs#L246-L285)
- Implementation version, file, and relevant symbol: `wit-parser` 0.255.0,
  `Tokenizer::next_raw`, `CrlfFold`, and `Error::UnterminatedComment`.
- Conformance test or official example permalink:
  [line, inline, and nested comments](https://github.com/bytecodealliance/wasm-tools/blob/606b4cc5503015ce539e6d6a7ec39a774710e114/crates/wit-parser/tests/ui/comments.wit#L1-L25)
- Dataset identity evidence:
  [Linguist WIT entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8580-L8591)
- Evidence conflicts or gaps: none affecting delimiters. The tokenizer's token
  span consumes a folded line ending while the language-level comment ends at
  the line boundary; extraction should exclude the physical terminator.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official scanner and UI fixture inspected; the Rust
  crate was not built locally.
- Exact version or commit: `606b4cc5503015ce539e6d6a7ec39a774710e114`
- Probe method: traced depth increments/decrements and the EOF error path.
- Probe input:

```wit
package demo:comments;
/* outer /* inner */ outer */
interface api { run: func(); } // line
```

- Observed result: the block remains one balanced comment at depth two and the
  final line region is a comment through the line end.
- Conclusion and limits of the probe: source inspection establishes nesting,
  EOF failure, and CRLF folding; it does not run package resolution.

### Representative examples

```wit
package demo:logging;

/// Writes one message.
interface logger {
    /* Kept nested: /* rationale */ end. */
    write: func(message: string);
}
```

### Adversarial boundaries

- Negative cases: WebAssembly `;;` and `(; ;)`, `"// literal"`,
  `"/* literal */"`, a lone slash, package paths, and generated host code.
- Malformed-input cases: unclosed block at every depth, stray `*/`, invalid
  string escapes before a marker, and misplaced BOM.
- Line-ending and Unicode cases: LF, CRLF, EOF line comment, bare CR behavior,
  UTF-8 prose, prohibited bidi/control points, and byte-exact slices.
- Version or dialect counterexamples: WAT and WAVE must retain their own
  delimiters; documentation subforms must not become separate overlapping
  matches.
- Cleaner preservation cases: nested delimiter text, `///` documentation body,
  `/**` content, blank lines, and Unicode.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: add canonical `webassembly_interface_type`, alias
  `wit`, line pattern `//` through the WIT line boundary, nested delimiter
  `("/*", "*/")`, standard wrappers, and line/nested/doc seeds.
- Deterministic tests to add: raw and `wit` lookup; inline, docs, nesting depth,
  strings, slash operator, WAT negatives, unclosed blocks, CRLF/EOF, forbidden
  code points, ordering/non-overlap, and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## WGSL

### Identity and scope

- Raw dataset label: `WGSL` (556,663 files; 396,418,509 tokens)
- Proposed registry key: `wgsl`
- Existing family or aliases checked: `c_style`, `kotlin_style`, and
  `nested_c_style`; only the delimiter shape overlaps, while WGSL has a
  normative Unicode line-break set and no string literal syntax.
- Classification: `language`
- Versions or releases checked: W3C WGSL Editor's Draft at GPUWeb commit
  `d390da5f80f18e82d9535a40c6f2f1f65e6884ae` and GPUWeb tree-sitter grammar
  commit `52e3c620a9c316cc8c1d504dd1908eb8cebe255b`.
- Dialects checked: standard WebGPU Shading Language module text.
- Intended support scope: all WGSL line-ending and recursively nested block
  comments in source modules.
- Explicitly excluded scope: GLSL/HLSL/MSL, comments in host-language strings
  containing WGSL, and non-WGSL shader preprocessing.

### Syntax contract

- Line comments: `//` through but not including the next WGSL line break or
  end of program.
- Block comments: `/* ... */`.
- Nested comments: yes, recursively and with balanced delimiters.
- Termination at newline, delimiter, or EOF: line comments accept EOF. WGSL
  line breaks are LF, VT, FF, CR, CRLF, NEL, LS, and PS. Block comments require
  all closing delimiters.
- Inline use: yes for line and block forms; a comment can separate tokens.
- Adjacent-line grouping: yes across consecutive `//` lines separated by one
  recognized WGSL line break and indentation.
- Unclosed delimiter behavior: invalid by the normative recursive definition;
  do not match an unclosed block through EOF.
- Lexical or structural context: comments are removed before template-list
  discovery and parsing. WGSL literals are numeric or Boolean, so there is no
  source string/character literal that can protect marker-looking text.
- Conflicts with strings, operators, directives, or embedded languages: `/`
  and `/=` are operators unless followed by `/` or `*`; host-language strings
  are outside a `.wgsl` module. Comments may occur between template tokens.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")` with nested delimiters preserved.
- Content-preservation expectations: remove one outer wrapper only; retain
  nesting markers, Unicode, exact internal line breaks, and indentation.

### Evidence

- Official specification permalink:
  [WGSL comments](https://github.com/gpuweb/gpuweb/blob/d390da5f80f18e82d9535a40c6f2f1f65e6884ae/wgsl/index.bs#L1059-L1094)
- Documentation version and relevant section: WGSL Editor's Draft,
  `Textual Structure`, `Blankspace and Line Breaks`, and `Comments`.
- Official implementation or grammar permalink:
  [GPUWeb nested-comment scanner](https://github.com/gpuweb/tree-sitter-wgsl/blob/52e3c620a9c316cc8c1d504dd1908eb8cebe255b/src/scanner.c#L655-L677)
- Implementation version, file, and relevant symbol: tree-sitter-wgsl 0.0.9,
  `lexer_match_block_comment`; generated grammar `_comment` handles `//`.
- Conformance example permalink: the normative
  [nested example](https://github.com/gpuweb/gpuweb/blob/d390da5f80f18e82d9535a40c6f2f1f65e6884ae/wgsl/index.bs#L1084-L1093).
- Dataset identity evidence:
  [Linguist WGSL entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L8536-L8543)
- Evidence conflicts or gaps: the tree-sitter scanner returns a block token at
  EOF even when depth remains nonzero, but the normative specification requires
  matching `*/`. The registry must follow the specification, not that recovery
  behavior.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: normative source and GPUWeb scanner inspected; no
  shader compiler was run.
- Exact version or commit: spec `d390da5f80f18e82d9535a40c6f2f1f65e6884ae`;
  scanner `52e3c620a9c316cc8c1d504dd1908eb8cebe255b`.
- Probe method: traced recursive grammar and scanner nesting counter, resolving
  malformed EOF in favor of the normative grammar.
- Probe input:

```wgsl
const f = 1.5; // line
const g = 2.5; /* outer /* inner */ outer */
```

- Observed result: one line comment and one depth-two block comment separate
  otherwise valid tokens.
- Conclusion and limits of the probe: delimiters, nesting, and line-break
  semantics are normative; compiler-specific diagnostic recovery is excluded.

### Representative examples

```wgsl
@fragment
fn main() -> @location(0) vec4f {
    // Keep the output opaque.
    return vec4f(1.0 /* red */, 0.0, 0.0, 1.0);
}
```

### Adversarial boundaries

- Negative cases: division, `/=`, host JavaScript `"// shader text"`, GLSL
  preprocessor directives, URLs outside comments, and a lone slash.
- Malformed-input cases: unclosed block at multiple depths, stray closer,
  nested opener just before EOF, NUL, and BOM.
- Line-ending and Unicode cases: every normative WGSL line break, CRLF as one
  break, EOF, Unicode payload, left/right marks as blankspace, and exact slices.
- Version or dialect counterexamples: GLSL and HLSL blocks are non-nested and
  must not share the WGSL contract.
- Cleaner preservation cases: inner `/* */`, token-like payload, Unicode,
  blank lines, and line-break code points other than LF.

### Decision

- Recommended action: `separate-family`
- Registry fields to change: add canonical `wgsl`, a line matcher ending at the
  full normative line-break class, nested `("/*", "*/")`, standard wrappers,
  and seeded line/nested examples.
- Deterministic tests to add: exact-label lookup; inline/adjacent comments;
  nested depth; operators; all line-break forms; EOF; unclosed blocks; NUL/BOM;
  ordering/exact ranges; and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Xmake

### Identity and scope

- Raw dataset label: `Xmake` (35,817 files; 26,632,940 tokens)
- Proposed registry key: `xmake`
- Existing family or aliases checked: `lua_style`, canonical `lua`; its short
  and equal-level long-comment delimiters match Xmake's bundled Lua lexer.
- Classification: `language`
- Versions or releases checked: Xmake commit
  `b41ed3acf227011f4904d95a439a30be9580e5cf` with bundled xmake-core-lua commit
  `a5522f06d2679b8f18534fd6a9968f7eb539dc31` (Lua 5.5.0).
- Dialects checked: `xmake.lua` project scripts executed by Xmake's sandboxed
  Lua runtime; bundled LuaJIT retains the same comment forms.
- Intended support scope: Lua lexical comments in Xmake project files.
- Explicitly excluded scope: comments in C/C++ source built by Xmake, shell
  installation scripts, generated build backends, and editor-only annotations.

### Syntax contract

- Line comments: `--` through CR, LF, CRLF, or EOF, except when followed by a
  well-formed long-bracket opener.
- Block comments: `--[=*[ ... ]=*]`, with the closer using exactly the same
  number of `=` characters as the opener.
- Nested comments: no. A nested-looking opener is ordinary body text until the
  matching equal-level closer.
- Termination at newline, delimiter, or EOF: short comments accept EOF; a long
  comment requires its level-matched closer and otherwise raises an unfinished
  long-comment error.
- Inline use: yes for short and long forms.
- Adjacent-line grouping: yes for consecutive short `--` lines.
- Unclosed delimiter behavior: invalid long comment; do not consume to EOF.
- Lexical or structural context: quoted Lua strings and long-bracket strings
  protect comment-looking text. `--[foo` and malformed `--[=` are short
  comments, because only `[=*[` selects long-comment mode.
- Conflicts with strings, operators, directives, or embedded languages: minus
  and subtraction are not comments without the second `-`; `[[-- text]]` and
  `[=[--[[ text ]]]=]` are long strings, not comments. An interpreter shebang
  is not an Xmake source-comment form.
- Sanitizer line wrappers: `("--", "")`.
- Sanitizer block wrappers: the matched `--[=*[` opener and `]=*]` closer at the
  same level.
- Content-preservation expectations: strip one outer, level-matched wrapper;
  retain nested-looking delimiters, leading newline semantics, Unicode, and
  all body text.

### Evidence

- Official documentation permalink:
  [Xmake is Lua-based and uses `xmake.lua`](https://github.com/xmake-io/xmake/blob/b41ed3acf227011f4904d95a439a30be9580e5cf/README.md#L51-L58)
- Documentation version and relevant section: pinned Xmake `Introduction` and
  `Simple Project Description`.
- Official implementation or grammar permalink:
  [bundled Lua short/long comment scanner](https://github.com/xmake-io/xmake-core-lua/blob/a5522f06d2679b8f18534fd6a9968f7eb539dc31/llex.c#L470-L496)
- Implementation version, file, and relevant symbol: bundled Lua 5.5.0,
  `llex.c`, `llex`, `skip_sep`, and `read_long_string`; the latter reports
  unfinished long comments at
  [EOF](https://github.com/xmake-io/xmake-core-lua/blob/a5522f06d2679b8f18534fd6a9968f7eb539dc31/llex.c#L276-L326).
- Official source example:
  [Xmake's own long comment](https://github.com/xmake-io/xmake/blob/b41ed3acf227011f4904d95a439a30be9580e5cf/core/src/luajit/xmake.lua#L43-L49).
- Dataset identity evidence:
  [Linguist Xmake filename entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L9001-L9008)
- Evidence conflicts or gaps: none. Sandboxing changes APIs, not lexical
  comment rules.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: Xmake's pinned runtime build files and bundled lexer
  inspected; Xmake was not built locally.
- Exact version or commit: Xmake
  `b41ed3acf227011f4904d95a439a30be9580e5cf`; lexer submodule
  `a5522f06d2679b8f18534fd6a9968f7eb539dc31`.
- Probe method: traced `--` dispatch, equal-count delimiter parsing, and EOF
  error construction.
- Probe input:

```lua
target("demo") -- short
--[=[ long --[[ not nested ]] body ]=]
local literal = [=[-- not a comment]=]
```

- Observed result: the first two regions are comments; the third marker remains
  inside a level-one long string.
- Conclusion and limits of the probe: exact lexical behavior is established;
  Xmake sandbox API behavior is irrelevant to comment extraction.

### Representative examples

```lua
target("console")
    set_kind("binary") -- build an executable
    --[=[
    Keep this rationale even if it contains --[[ nested-looking text ]].
    ]=]
```

### Adversarial boundaries

- Negative cases: subtraction, one dash, quoted `--`, zero/equal-level long
  strings, shebang text, and comments in built source files.
- Malformed-input cases: unclosed long comments at several equal levels,
  mismatched closers, `--[=`, `--[foo`, and stray `]=]`.
- Line-ending and Unicode cases: LF, CRLF, CR, EOF short comment, Unicode body,
  and first-newline handling inside a long comment.
- Version or dialect counterexamples: MoonScript/Terra extensions and Xmake's
  generated Ninja/Make syntax do not expand this key.
- Cleaner preservation cases: equal signs, inner bracket sequences, body lines
  beginning with `--`, and long-comment indentation.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `xmake` to `lua_style.aliases`, attach a pinned
  Xmake seed, and add Lua/Xmake-aware long-bracket string masking so `--` inside
  `[=*[ ... ]=*]` strings is never extracted.
- Deterministic tests to add: exact-label lookup; short inline/adjacent/EOF;
  equal levels zero through several; non-nesting; malformed/mismatched blocks;
  quoted and long strings; CRLF/CR; and dynamic-wrapper sanitation.
- Remaining blocker: none, provided long-bracket string masking lands with the
  alias.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Zmodel

### Identity and scope

- Raw dataset label: `Zmodel` (1,316 files; 1,224,190 tokens)
- Proposed registry key: `zmodel`
- Existing family or aliases checked: `c_style`, which already contains the
  related `prisma` label and has identical line and non-nested block forms.
- Classification: `document-format`
- Versions or releases checked: ZenStack 2.9.4 commit
  `251c699095eb9a6885c14fc179a8a9221529add6` and ZenStack 3.9.0 commit
  `19f082016d9e74ab7131d5c7620b2323656f42cb`.
- Dialects checked: ZenStack ZModel v2 and v3 schema files, including
  triple-slash documentation comments.
- Intended support scope: lexical and documentation comments in valid
  `.zmodel` schemas across the checked major versions.
- Explicitly excluded scope: Prisma files not classified as Zmodel, generated
  Prisma/TypeScript, and comments in embedded string values.

### Syntax contract

- Line comments: `//` through but not including CR, LF, or EOF. `///` is a
  grammar-visible documentation-comment subtype with the same termination.
- Block comments: `/* ... */`, including `/** ... */` documentation style.
- Nested comments: no; the first `*/` closes the token.
- Termination at newline, delimiter, or EOF: line comments accept EOF; block
  comments require `*/`.
- Inline use: ordinary `//` and block comments are hidden lexer tokens and may
  occur where whitespace is legal. `///` is valid only at grammar positions
  that accept documentation for a following declaration.
- Adjacent-line grouping: yes for consecutive `//` or `///` lines.
- Unclosed delimiter behavior: the Langium `ML_COMMENT` terminal does not match
  an unclosed block; do not consume it through EOF.
- Lexical or structural context: single- and double-quoted strings with
  backslash escapes protect comment-looking text. Triple-slash tokens are kept
  in the AST for documentation while ordinary comments are hidden.
- Conflicts with strings, operators, directives, or embedded languages: URLs
  and markers in quoted datasource/plugin values are data. Attribute prefixes
  `@`, `@@`, and `@@@` are not comments.
- Sanitizer line wrappers: `("//", "")`; preserve the third slash as
  documentation payload unless a reviewed doc-cleaning rule handles it.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: remove one outer wrapper while retaining
  documentation text, stars, Unicode, whitespace, and line structure.

### Evidence

- Official implementation or grammar permalink:
  [ZenStack 3.9.0 terminals](https://github.com/zenstackhq/zenstack/blob/19f082016d9e74ab7131d5c7620b2323656f42cb/packages/language/src/zmodel.langium#L286-L295)
- Implementation version, file, and relevant symbol: `@zenstackhq/language`
  3.9.0, `STRING`, `TRIPLE_SLASH_COMMENT`, `ML_COMMENT`, and `SL_COMMENT`.
- Cross-version grammar permalink:
  [ZenStack 2.9.4 identical terminals](https://github.com/zenstackhq/zenstack/blob/251c699095eb9a6885c14fc179a8a9221529add6/packages/language/src/zmodel.langium#L274-L283)
- Official implementation example:
  [ZModel comment provider emits `/** ... */`](https://github.com/zenstackhq/zenstack/blob/19f082016d9e74ab7131d5c7620b2323656f42cb/packages/language/src/zmodel-comment-provider.ts#L5-L20)
- Dataset identity evidence:
  [Linguist Zmodel entry](https://github.com/github-linguist/linguist/blob/af6f772786199696e4d07d618c9c5b625a1a03f0/lib/linguist/languages.yml#L9178-L9185)
- Evidence conflicts or gaps: none. V2 and V3 terminal definitions agree.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: both pinned Langium grammars, VS Code language
  configuration, and comment provider inspected; the Node parser was not run.
- Exact version or commit: `251c699095eb9a6885c14fc179a8a9221529add6`
  and `19f082016d9e74ab7131d5c7620b2323656f42cb`.
- Probe method: compared terminal regexes across majors and traced which
  triple-slash tokens are attached to declarations.
- Probe input:

```zmodel
/// Account visible to the API.
model Account {
    id String @id // stable key
    note String @default("/* literal */")
}
```

- Observed result: the triple-slash and trailing line regions are comments;
  the block-looking string content is a `STRING` token.
- Conclusion and limits of the probe: delimiter and cross-version behavior are
  conclusive; semantic schema validation was not exercised.

### Representative examples

```zmodel
/** Persistent account record. */
model Account {
    /// Public identifier.
    id String @id // generated by the caller
}
```

### Adversarial boundaries

- Negative cases: single/double-quoted URLs and markers, `/` in expressions,
  attribute prefixes, Prisma generated output, and marker text in plugin data.
- Malformed-input cases: unclosed block, stray closer, invalid `///` placement,
  and an unterminated string before a delimiter.
- Line-ending and Unicode cases: LF, CRLF, CR, EOF line comment, Unicode docs,
  and exact exclusion of terminators.
- Version or dialect counterexamples: Prisma schema extensions not accepted by
  ZModel and generated TypeScript comments remain outside this key.
- Cleaner preservation cases: `///` and `/**` documentation payload, leading
  stars, blank lines, URL text, and Unicode.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `zmodel` to `c_style.aliases`, attach the
  pinned v2/v3 grammar evidence, and add ZModel-specific line/block/doc seeds.
- Deterministic tests to add: exact-label lookup; `//`, `///`, `/*`, and `/**`;
  first-close non-nesting; both quote styles and escapes; attributes; unclosed
  blocks; CR/LF/CRLF/EOF; ordering; and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01
