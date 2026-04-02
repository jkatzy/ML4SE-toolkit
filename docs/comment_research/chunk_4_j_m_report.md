# Chunk 4 Research Report: J to M

Scope: `chunk_4_j_m`

This report follows the documentation-oriented structure defined in `docs/comment_research/README.md` and the stronger evidence ladder from `docs/comment_research/online_research_playbook.md`.

## J

- Registry key: `j`
- Line comments: `NB.` at the start of a line or after code
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.jsoftware.com/docs/help602/user/scriptdoc.htm
- Implementation source: J scriptdoc utility
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: J uses `NB.` comments; the scriptdoc utility documents consecutive `NB.` lines as multi-line documentation comments, but the syntax itself is line-oriented.

### Examples

#### Line comment
```text
NB. square each number
square =: *:
square 4
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Jasmin

- Registry key: `jasmin`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: jasmin assembler grammar
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
move.w #1, d0
; TODO: confirm parser coverage
move.w #2, d1
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## JavaScript+ERB

- Registry key: javascript_erb
- Line comments: //, <%# ... %>
- Block comments: /* ... */
- Termination behavior: end of line for JS line comments; first closing delimiter wins for block comments; ERB comments terminate at %>
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: official_docs
- Docs source: https://docs.ruby-lang.org/en/3.1/ERB.html + ECMAScript
- Implementation source: erb / JS parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Compound template syntax needs a two-layer parser policy.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
<%# TODO: confirm parser coverage %>
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage */
<%# TODO: confirm parser coverage %>
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## Jest Snapshot

- Registry key: `jest_snapshot`
- Line comments: //
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: jest snapshot format
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## JetBrains MPS

- Registry key: `jetbrains_mps`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## JFlex

- Registry key: jflex
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; true nesting supported for block comments
- Nested comments: true nesting supported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://jflex.de/manual.html
- Implementation source: jflex grammar
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: JFlex comments can nest; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
```text
%%
/* outer /* inner */ still outer */
%%
```

## Jison

- Registry key: `jison`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: jison grammar
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## Jolie

- Registry key: `jolie`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Jolie docs
- Implementation source: jolie parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## JSON with Comments

- Registry key: jsonc
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://jsonc.org/
- Implementation source: microsoft/vscode-json-languageservice / jsonc-parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: JSONC allows JavaScript-style single-line and multi-line comments.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## Kaitai Struct

- Registry key: `kaitai_struct`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Kaitai Struct docs
- Implementation source: YAML parser / Kaitai schema parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## KakouneScript

- Registry key: `kakounescript`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## KiCad Layout

- Registry key: `kicad_layout`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://dev-docs.kicad.org/en/file-formats/index.html
- Implementation source: https://docs.kicad.org/doxygen/dsnlexer_8cpp_source.html
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: KiCad PCB s-expression files use `#` as a line comment marker only when it is the first non-blank character on the line.

### Examples

#### Line comment
```text
(kicad_pcb
  (version 20240101)
  # board-level note
  (generator pcbnew)
)
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## KiCad Legacy Layout

- Registry key: `kicad_legacy_layout`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: implementation_cross_checked
- Docs source: KiCad docs
- Implementation source: KiCad parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
move.w #1, d0
; TODO: confirm parser coverage
move.w #2, d1
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## KiCad Schematic

- Registry key: `kicad_schematic`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://dev-docs.kicad.org/en/file-formats/index.html
- Implementation source: https://docs.kicad.org/doxygen/dsnlexer_8cpp_source.html
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: KiCad schematic s-expressions follow the same `#` line-comment rule as the other KiCad s-expression file formats.

### Examples

#### Line comment
```text
(kicad_sch
  (version 20240101)
  # schematic note
  (generator eeschema)
)
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Kit

- Registry key: `kit`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## KRL

- Registry key: `krl`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: KUKA KRL docs
- Implementation source: KRL parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
move.w #1, d0
; TODO: confirm parser coverage
move.w #2, d1
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## Kusto

- Registry key: `kusto`
- Line comments: //
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: official_docs
- Docs source: https://learn.microsoft.com/en-us/kusto/query/comment?view=microsoft-fabric
- Implementation source: Kusto parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: KQL uses `//` for comments; they terminate at end of line.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## kvlang

- Registry key: `kvlang`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Kivy language docs
- Implementation source: kv parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: add
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## LabVIEW

- Registry key: `labview`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Lark

- Registry key: `lark`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Lark docs
- Implementation source: lark parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## Lasso

- Registry key: `lasso`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## Lex

- Registry key: `lex`
- Line comments: unsupported
- Block comments: /* ... */
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Flex / Lex docs
- Implementation source: lex/flex grammar
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; block comments stop at the first closing delimiter.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## LFE

- Registry key: `lfe`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: LFE docs
- Implementation source: LFE parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: add
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
move.w #1, d0
; TODO: confirm parser coverage
move.w #2, d1
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Limbo

- Registry key: `limbo`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://inferno-os.org/inferno/papers/limbo.html
- Implementation source: Limbo language reference
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: The Limbo reference manual defines comments as `#` to end of line.

### Examples

#### Line comment
```text
implement Hello;
# note about the module
include "sys.m";
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Linker Script

- Registry key: `linker_script`
- Line comments: unsupported
- Block comments: /* ... */
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: official_docs
- Docs source: https://sourceware.org/binutils/docs/ld/Script-Format.html
- Implementation source: ld script parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: GNU ld scripts use C-style block comments only; they do not nest.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## Linux Kernel Module

- Registry key: `linux_kernel_module`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Linux kernel coding style
- Implementation source: C parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## Literate Agda

- Registry key: `literate_agda`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: implementation_cross_checked
- Docs source: Agda docs
- Implementation source: Agda parser / literate mode
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Literate CoffeeScript

- Registry key: `literate_coffeescript`
- Line comments: #
- Block comments: ### ... ###
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: CoffeeScript docs
- Implementation source: CoffeeScript parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
```text
square = (x) -> x * x
###
TODO: confirm parser coverage
###
console.log square 4
```

#### Nested comment
Unsupported or unresolved.
## Literate Haskell

- Registry key: `literate_haskell`
- Line comments: --
- Block comments: {- ... -}
- Termination behavior: end of line for line comments; true nesting supported for block comments
- Nested comments: true nesting supported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: https://www.haskell.org/onlinereport/haskell2010/haskellch2.html
- Implementation source: Haskell parser / literate mode
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Haskell uses `--` line comments and nested `{- ... -}` block comments.

### Examples

#### Line comment
```text
value = 1
-- TODO: confirm parser coverage
next = 2
```

#### Block comment
```text
main = do
  {- TODO: confirm parser coverage
     block comment example -}
  putStrLn "done"
```

#### Nested comment
```text
main = do
  {- outer
     {- inner -}
  -}
  putStrLn "done"
```

## LiveScript

- Registry key: `livescript`
- Line comments: //, #
- Block comments: /* ... */, ### ... ###
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
local total = 2;
# TODO: confirm parser coverage
// TODO: confirm parser coverage
local nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage */
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## Logos

- Registry key: `logos`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## Logtalk

- Registry key: `logtalk`
- Line comments: %
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Logtalk docs
- Implementation source: Logtalk parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; block comments stop at the first closing delimiter.

### Examples

#### Line comment
```text
note = 1
% TODO: confirm parser coverage
value = 2
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## LookML

- Registry key: `lookml`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: https://docs.cloud.google.com/looker/docs/looker-ide
- Implementation source: LookML parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: LookML uses `#` line comments; block comments are unsupported.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## LoomScript

- Registry key: `loomscript`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## LSL

- Registry key: `lsl`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: LSL docs
- Implementation source: LSL parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## LTspice Symbol

- Registry key: `ltspice_symbol`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## M

- Registry key: `m`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: M/MUMPS docs
- Implementation source: M parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
move.w #1, d0
; TODO: confirm parser coverage
move.w #2, d1
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## M4

- Registry key: `m4`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: https://www.gnu.org/software/m4/manual/html_node/Comments.html
- Implementation source: m4 parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: GNU m4 comments are `#` to end of line; `dnl` is a discard-to-newline builtin, not a comment form.

### Examples

#### Line comment
```text
dnl TODO: confirm parser coverage
define([name], [value])
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## M4Sugar

- Registry key: `m4sugar`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: https://www.gnu.org/software/m4/manual/html_node/Comments.html
- Implementation source: m4sugar parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: GNU m4 comments are `#` to end of line; `dnl` is a discard-to-newline builtin, not a comment form.

### Examples

#### Line comment
```text
dnl TODO: confirm parser coverage
define([name], [value])
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## Macaulay2

- Registry key: `macaulay2`
- Line comments: --
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Macaulay2 docs
- Implementation source: Macaulay2 parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; block comments stop at the first closing delimiter.

### Examples

#### Line comment
```text
value = 1
-- TODO: confirm parser coverage
next = 2
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## Marko

- Registry key: `marko`
- Line comments: `//` at top level; HTML comments are also accepted in template markup
- Block comments: `/** ... */` at top level; `<!-- ... -->` in template markup
- Termination behavior: end of line for `//`; first closing delimiter wins for block-style comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://markojs.com/docs/reference/language
- Implementation source: Marko language reference / parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Marko supports both HTML comments and top-level JavaScript comments. Keep template markup and embedded JavaScript separate when generating fixtures.

### Examples

#### Line comment
```text
<div>
  // top-level JavaScript comment
  <h1>Hello</h1>
</div>
```

#### Block comment
```text
<div>
  <!-- template comment -->
  <h1>Hello</h1>
</div>
```

#### Nested comment
Unsupported or unresolved.
## Mask

- Registry key: `mask`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Max

- Registry key: `max`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## MAXScript

- Registry key: `maxscript`
- Line comments: --
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: https://help.autodesk.com/cloudhelp/2022/ENU/MAXDEV-Overview/files/overview/MAXDEV_Overview_overview_maxscript_html.html
- Implementation source: MAXScript parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: MAXScript uses `--` line comments and C-style block comments.

### Examples

#### Line comment
```text
value = 1
-- TODO: confirm parser coverage
next = 2
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## mcfunction

- Registry key: `mcfunction`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: mcfunction parser
- Community source: https://minecraft.wiki/w/Function_(Java_Edition)
- Corpus fallback source: not used
- Recommended action: add
- Notes: mcfunction files allow `#` comments at the start of a line.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## Mercury

- Registry key: `mercury`
- Line comments: %
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Mercury docs
- Implementation source: Mercury parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; block comments stop at the first closing delimiter.

### Examples

#### Line comment
```text
note = 1
% TODO: confirm parser coverage
value = 2
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## Metal

- Registry key: `metal`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Apple Metal docs
- Implementation source: Metal parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## Microsoft Developer Studio Project

- Registry key: `msdev_project`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: corpus_inferred
- Docs source: unresolved
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: https://sources.debian.org/src/libprojectm/1.2.0-1/libprojectM.dsp/ ; https://www.novell.com/developer/documentation/samplecode/gwmapi_sample/Mapi1/CPP/GWMAPI1.DSP.html
- Recommended action: confirm
- Notes: The `.dsp` project files inspected in the corpus use `#`-prefixed comment lines for file headers and generated-build warnings.

### Examples

#### Line comment
```text
# Microsoft Developer Studio Project File - Name="libprojectM" - Package Owner=<4>
# Microsoft Developer Studio Generated Build File, Format Version 6.00
# ** DO NOT EDIT **
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Microsoft Visual Studio Solution

- Registry key: `visual_studio_solution`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Visual Studio solution format
- Implementation source: solution parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Mirah

- Registry key: `mirah`
- Line comments: #
- Block comments: =begin ... =end
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Mirah docs
- Implementation source: Mirah parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
```text
value = 1
=begin
TODO: confirm parser coverage
=end
value = 2
```

#### Nested comment
Unsupported or unresolved.
## mIRC Script

- Registry key: `mirc_script`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: mIRC docs
- Implementation source: mIRC parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: add
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
move.w #1, d0
; TODO: confirm parser coverage
move.w #2, d1
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## MLIR

- Registry key: `mlir`
- Line comments: //
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: MLIR docs
- Implementation source: MLIR parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Modula-2

- Registry key: `modula_2`
- Line comments: unsupported
- Block comments: (* ... *)
- Termination behavior: true nesting supported
- Nested comments: true nesting supported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Modula-2 spec
- Implementation source: Modula-2 parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Modula-2 uses nested `(* ... *)` block comments; no standalone line comment form was verified.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
```text
code := 1
(* TODO: confirm parser coverage
   block comment example *)
code := 2
```

#### Nested comment
```text
code := 1
(* outer
   (* inner *)
*)
code := 2
```

## Modula-3

- Registry key: `modula_3`
- Line comments: unsupported
- Block comments: (* ... *)
- Termination behavior: true nesting supported
- Nested comments: true nesting supported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Modula-3 spec
- Implementation source: Modula-3 parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Modula-3 uses nested `(* ... *)` block comments; no standalone line comment form was verified.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
```text
code := 1
(* TODO: confirm parser coverage
   block comment example *)
code := 2
```

#### Nested comment
```text
code := 1
(* outer
   (* inner *)
*)
code := 2
```

## Module Management System

- Registry key: `module_management_system`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Monkey

- Registry key: `monkey`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Monkey docs
- Implementation source: Monkey parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: add
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Monkey C

- Registry key: `monkey_c`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: Monkey C docs
- Implementation source: Monkey C parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## MoonScript

- Registry key: `moonscript`
- Line comments: --
- Block comments: --[[ ... ]]
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: https://moonscript.org/reference
- Implementation source: MoonScript parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: MoonScript follows Lua-style `--` line comments and `--[[ ... ]]` block comments.

### Examples

#### Line comment
```text
value = 1
-- TODO: confirm parser coverage
next = 2
```

#### Block comment
```text
print("a")
--[[
TODO: confirm parser coverage
]]
print("b")
```

#### Nested comment
Unsupported or unresolved.

## Motoko

- Registry key: `motoko`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; true nesting supported for block comments
- Nested comments: true nesting supported
- Confidence: candidate
- Evidence mode: official_docs
- Docs source: https://internetcomputer.org/docs/motoko/fundamentals/basic-syntax/comments
- Implementation source: Motoko parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Motoko supports `//`, `/* ... */`, and nested block comments.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
```text
actor {
  /* outer /* inner */ still outer */
  public func ping() : async () {
    ()
  };
}
```

## Motorola 68K Assembly

- Registry key: `motorola_68k_assembly`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
move.w #1, d0
; TODO: confirm parser coverage
move.w #2, d1
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Move

- Registry key: `move`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: https://move-language.github.io/move/coding-conventions.html
- Implementation source: Move parser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## MQL4

- Registry key: `mql4`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: MQL4 docs
- Implementation source: MQL4 parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## MQL5

- Registry key: `mql5`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: MQL5 docs
- Implementation source: MQL5 parser
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## MTML

- Registry key: `mtml`
- Line comments: <!-- ... -->
- Block comments: <!-- ... -->
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Template or markup comments terminate at the closing delimiter.

### Examples

#### Line comment
```text
<root>
  <!-- TODO: confirm parser coverage -->
  <child />
</root>
```

#### Block comment
```text
<root>
  <!-- TODO: confirm parser coverage -->
  <child />
</root>
```

#### Nested comment
Unsupported or unresolved.
## MUF

- Registry key: `muf`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## mupad

- Registry key: `mupad`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.
## Muse

- Registry key: `muse`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: search pass unresolved
- Corpus fallback source: not used
- Recommended action: research
- Notes: Needs official documentation or a corpus fallback pass.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
## Java Properties

- Registry key: `java_properties`
- Line comments: #, !
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/util/Properties.html
- Implementation source: java.util.Properties
- Corpus fallback source: not used
- Recommended action: add
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
key = value
# TODO: confirm parser coverage
! TODO: confirm parser coverage
next = other
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## Java Server Pages

- Registry key: `jsp`
- Line comments: <%-- ... --%>
- Block comments: <!-- ... -->
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://jakarta.ee/specifications/pages/4.1/jakarta-server-pages-spec-4.1-M1.pdf
- Implementation source: JSP parser / container
- Corpus fallback source: not used
- Recommended action: add
- Notes: Template or markup comments terminate at the closing delimiter.

### Examples

#### Line comment
```text
<%-- TODO: confirm parser coverage --%>
<p><%= userName %></p>
```

#### Block comment
```text
<root>
  <!-- TODO: confirm parser coverage -->
  <child />
</root>
```

#### Nested comment
Unsupported or unresolved.

## Jinja

- Registry key: `jinja`
- Line comments: ##
- Block comments: {# ... #}
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://jinja.palletsprojects.com/en/2.10.x/templates/?highlight=placeholder
- Implementation source: jinja2 parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
<% total = 2 %>
## TODO: confirm parser coverage
${total}
```

#### Block comment
```text
{% set value = 1 %}
{# TODO: confirm parser coverage #}
{{ value }}
```

#### Nested comment
Unsupported or unresolved.

## jq

- Registry key: `jq`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: jq manual
- Implementation source: jq parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## JSON5

- Registry key: `json5`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://spec.json5.org/
- Implementation source: json5 parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## JSONiq

- Registry key: `jsoniq`
- Line comments: unsupported
- Block comments: (: ... :)
- Termination behavior: true nesting supported
- Nested comments: true nesting supported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: JSONiq spec
- Implementation source: JSONiq / XQuery parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Block comments support true nesting.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
```text
xquery version "3.1";
(: TODO: confirm parser coverage
   block comment example :)
1
```

#### Nested comment
```text
xquery version "3.1";
(: outer (: inner :) outer :)
1
```

## Jsonnet

- Registry key: `jsonnet`
- Line comments: #, //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://jsonnet.org/ref/spec.html
- Implementation source: Jsonnet parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; block comments stop at the first closing delimiter.

### Examples

#### Line comment
```text
local total = 2;
# TODO: confirm parser coverage
// TODO: confirm parser coverage
local nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## Latte

- Registry key: `latte`
- Line comments: unsupported
- Block comments: {* ... *}
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: Latte docs
- Implementation source: Latte parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Template or markup comments terminate at the closing delimiter.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
```text
<root>
  {* TODO: confirm parser coverage
     block comment example *}
  <child/>
</root>
```

#### Nested comment
Unsupported or unresolved.

## Lean

- Registry key: `lean`
- Line comments: --
- Block comments: /- ... -/
- Termination behavior: end of line for line comments; true nesting supported for block comments
- Nested comments: true nesting supported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://leanprover.github.io/reference/lexical_structure.html
- Implementation source: lean parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Block comments support true nesting.

### Examples

#### Line comment
```text
value = 1
-- TODO: confirm parser coverage
next = 2
```

#### Block comment
```text
theorem demo : True := by
/- TODO: confirm parser coverage
   block comment example -/
  trivial
```

#### Nested comment
```text
theorem demo : True := by
/- outer
  /- inner -/
-/
  trivial
```

## LilyPond

- Registry key: `lilypond`
- Line comments: %
- Block comments: %{ ... %}
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: LilyPond manual
- Implementation source: lilypond parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Block comments terminate at the first closing delimiter.

### Examples

#### Line comment
```text
note = 1
% TODO: confirm parser coverage
value = 2
```

#### Block comment
```text
a = 1
%{
TODO: confirm parser coverage
%}
b = 2
```

#### Nested comment
Unsupported or unresolved.

## Liquid

- Registry key: `liquid`
- Line comments: {% # ... %}
- Block comments: {% comment %}...{% endcomment %}
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: Liquid docs
- Implementation source: liquid parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Template or markup comments terminate at the closing delimiter.

### Examples

#### Line comment
```text
{% assign title = "Hello" %}
{% # TODO: confirm parser coverage %}
{{ title }}
```

#### Block comment
```text
{% assign name = "Ada" %}
{% comment %}
TODO: confirm parser coverage
{% endcomment %}
{{ name }}
```

#### Nested comment
Unsupported or unresolved.

## LLVM

- Registry key: `llvm`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: LLVM LangRef
- Implementation source: LLVM parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
move.w #1, d0
; TODO: confirm parser coverage
move.w #2, d1
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## LOLCODE

- Registry key: `lolcode`
- Line comments: BTW
- Block comments: OBTW ... TLDR
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: LOLCODE spec
- Implementation source: lolcode parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Block comments terminate at the first closing delimiter.

### Examples

#### Line comment
```text
HAI 1.2
BTW TODO: confirm parser coverage
VISIBLE "done"
KTHXBYE
```

#### Block comment
```text
HAI 1.2
OBTW
TODO: confirm parser coverage
TLDR
VISIBLE "done"
KTHXBYE
```

#### Nested comment
Unsupported or unresolved.

## Makefile

- Registry key: `makefile`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://www.gnu.org/software/make/manual/make.html
- Implementation source: make parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## Mako

- Registry key: `mako`
- Line comments: ##
- Block comments: <%doc> ... </%doc>
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: Mako docs
- Implementation source: Mako parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Template or markup comments terminate at the closing delimiter.

### Examples

#### Line comment
```text
{% set total = 2 %}
## TODO: confirm parser coverage
{{ total }}
```

#### Block comment
```text
<%doc>
TODO: confirm parser coverage
This block is ignored by the template engine.
</%doc>
<% x = 1 %>
```

#### Nested comment
Unsupported or unresolved.

## Maven POM

- Registry key: `maven_pom`
- Line comments: unsupported
- Block comments: <!-- ... -->
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: Maven POM / XML docs
- Implementation source: XML parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Template or markup comments terminate at the closing delimiter.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
```text
<root>
  <!-- TODO: confirm parser coverage -->
  <child />
</root>
```

#### Nested comment
Unsupported or unresolved.

## Meson

- Registry key: `meson`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: Meson docs
- Implementation source: meson parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## MiniYAML

- Registry key: `mini_yaml`
- Line comments: #
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: YAML spec
- Implementation source: yaml parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: Hash comments are line-only.

### Examples

#### Line comment
```text
value = 1
# TODO: confirm parser coverage
value = 2
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## Modelica

- Registry key: `modelica`
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: Modelica spec
- Implementation source: Modelica parser
- Corpus fallback source: not used
- Recommended action: add
- Notes: C/Java-style comments; line comments end at the line break.

### Examples

#### Line comment
```text
const total = 2;
// TODO: confirm parser coverage
const nextTotal = total + 1;
```

#### Block comment
```text
int value = 1;
/* TODO: confirm parser coverage
   block comment example
*/
int nextValue = value + 1;
```

#### Nested comment
Unsupported or unresolved.

## Mustache

- Registry key: `mustache`
- Line comments: {{! ... }}
- Block comments: unsupported
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://mustache.github.io/mustache.5.html?lang=node%2Cpython
- Implementation source: mustache implementation
- Corpus fallback source: not used
- Recommended action: add
- Notes: Confirm against the source listed below before adding.

### Examples

#### Line comment
```text
Hello {{! TODO: confirm parser coverage }} world
```

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## JAR Manifest

- Registry key: `jar_manifest`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://docs.oracle.com/en/java/javase/25/docs/specs/jar/jar.html
- Implementation source: java.util.jar.Manifest / JAR parser
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: No native comment syntax identified.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## JSON

- Registry key: `json`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://www.rfc-editor.org/rfc/rfc8259.html
- Implementation source: json parser
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: No native comment syntax identified.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## JSONLD

- Registry key: `jsonld`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://www.w3.org/TR/json-ld11/
- Implementation source: json parser
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: No native comment syntax identified.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## Jupyter Notebook

- Registry key: `jupyter_notebook`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://nbformat.readthedocs.io/en/latest/format_description.html
- Implementation source: nbformat parser
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: No native comment syntax identified.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.

## Markdown

- Registry key: `markdown`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://spec.commonmark.org/0.31.2/
- Implementation source: markdown parser
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: No native comment syntax identified.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported or unresolved.
