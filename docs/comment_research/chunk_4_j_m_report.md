# Chunk 4 Research Report: J to M

Scope: `chunk_4_j_m`

This report follows the documentation-oriented structure defined in `docs/comment_research/README.md` and the stronger evidence ladder from `docs/comment_research/online_research_playbook.md`.

## J

- Registry key: `j`
- Line comments: `NB.` at the start of a line or after code
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Version scope: J 6.02 scriptdoc and current J docs checked.
- Version-specific syntax: no dialect split found; `NB.` is the only native comment form confirmed, and consecutive `NB.` lines are documentation grouping rather than a separate block-comment syntax.
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
- Version scope: Jasmin 2.x SourceForge guide and current Jasmin assembler source grammar checked.
- Version-specific syntax: no version split found; `.j` Jasmin assembly uses semicolon line comments only. Registry should implement `;` as a line comment and no block form.
- Line comments: `;`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://jasmin.sourceforge.net/guide.html
- Implementation source: https://github.com/davidar/jasmin
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Jasmin examples and the assembler grammar use JVM-assembly style semicolon comments. No block delimiter was found.

### Examples

#### Line comment
```text
.class public Hello
.super java/lang/Object
; default constructor follows
.method public <init>()V
.end method
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## JavaScript+ERB

- Registry key: `javascript_erb`
- Version scope: ECMAScript lexical grammar current edition plus Ruby ERB 2.3, 3.0, and 3.4 documentation checked.
- Version-specific syntax: ECMAScript `//`, `/* ... */`, and hashbang comments are stable in modern editions; ERB `<%# ... %>` is stable across the Ruby versions checked. Registry should implement the union for this compound syntax but keep ERB comment matching separate from JavaScript string/template contexts.
- Line comments: `//`, ECMAScript hashbang `#!` only at script start, ERB `<%# ... %>` comment tag
- Block comments: `/* ... */`
- Termination behavior: `//` and hashbang terminate at a line break; `/* ... */` terminates at the first `*/`; ERB comments terminate at the next `%>`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://tc39.es/ecma262/#sec-comments ; https://docs.ruby-lang.org/en/3.4/ERB.html
- Implementation source: https://github.com/tc39/ecma262 ; https://github.com/ruby/erb
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Treat this as a layered template language. ERB comments can contain JavaScript-looking delimiters that should not be interpreted as JS comments.

### Examples

#### Line comment
```text
#!/usr/bin/env node
const user = "Ada"; // rendered by ERB
<%# server-side note: do not emit debug data %>
console.log(user);
```

#### Block comment
```text
const total = 1 + 2;
/* client-side note
   kept in the generated script */
console.log(total);
```

#### Nested comment
Unsupported.

## Jest Snapshot

- Registry key: `jest_snapshot`
- Version scope: current Jest snapshot testing documentation and generated `.snap` files using snapshot format version 1 checked.
- Version-specific syntax: generated snapshot files are JavaScript modules headed by a `// Jest Snapshot v1` line. No separate snapshot-format block comment form was confirmed, so registry support should stay line-comment only for snapshot metadata.
- Line comments: `//`
- Block comments: unsupported for generated snapshot syntax
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://jestjs.io/docs/snapshot-testing
- Implementation source: https://github.com/jestjs/jest/tree/main/packages/jest-snapshot
- Community source: not used
- Corpus fallback source: https://github.com/jestjs/jest/search?q=%22Jest+Snapshot+v1%22&type=code
- Recommended action: add
- Notes: `.snap` files are JavaScript-like, but parsing arbitrary JS block comments risks matching inside serialized snapshot text. Only the generated `//` comment is confirmed as snapshot syntax.

### Examples

#### Line comment
```text
// Jest Snapshot v1, https://goo.gl/fbAQLP

exports[`button renders 1`] = `<button>Save</button>`;
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## JetBrains MPS

- Registry key: `jetbrains_mps`
- Version scope: current JetBrains MPS documentation for model persistence and XML-based persisted model files checked.
- Version-specific syntax: MPS editors are projectional and do not define a universal textual comment token. The persisted `.mps`, `.mpl`, and `.msd` files are XML-family artifacts; only XML comments are defensible for persisted files.
- Line comments: unsupported
- Block comments: `<!-- ... -->` for XML persistence files only
- Termination behavior: first closing `-->` wins
- Nested comments: unsupported
- Confidence: medium
- Evidence mode: official_docs
- Docs source: https://www.jetbrains.com/help/mps/custom-persistence-cookbook.html
- Implementation source: https://github.com/JetBrains/MPS
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Registry support should be scoped to persisted XML files, not to MPS projectional language editors in general.

### Examples

#### Line comment
Unsupported.

#### Block comment
```text
<model ref="r:example">
  <!-- persisted-model note -->
  <node concept="jetbrains.mps.baseLanguage.structure.ClassConcept" />
</model>
```

#### Nested comment
Unsupported.

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
- Version scope: current Jison documentation/examples and parser sources checked.
- Version-specific syntax: no version split found. Jison grammar files accept C/JavaScript-style comments in grammar sections; JavaScript action blocks may also contain JavaScript comments, but registry matching should treat both as ordinary comment delimiters.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://gerhobbelt.github.io/jison/docs/
- Implementation source: https://github.com/zaach/jison ; https://github.com/zaach/jison-lex
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Do not infer nested block comments from JavaScript action blocks; JavaScript comments are non-nesting.

### Examples

#### Line comment
```text
%start expressions
// parse a sequence of expressions
%%
expressions
  : e EOF
  ;
```

#### Block comment
```text
/* operator precedence */
%left '+' '-'
%%
e : e '+' e
  | NUMBER
  ;
```

#### Nested comment
Unsupported.

## Jolie

- Registry key: `jolie`
- Version scope: current Jolie documentation and parser sources checked.
- Version-specific syntax: no version-specific delimiter split found; Jolie uses Java/C-style comments.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://docs.jolie-lang.org/
- Implementation source: https://github.com/jolie/jolie
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Jolie examples and parser behavior match C-style comment syntax; no nested form was found.

### Examples

#### Line comment
```text
main
{
  // receive a request
  requestResponse( ping )( response );
}
```

#### Block comment
```text
/* shared service interface */
interface PingInterface {
  RequestResponse: ping( string )( string )
}
```

#### Nested comment
Unsupported.

## JSON with Comments

- Registry key: jsonc
- Line comments: //
- Block comments: /* ... */
- Termination behavior: end of line for line comments; first closing delimiter wins for block comments
- Nested comments: unsupported
- Version scope: current JSON-with-comments references checked.
- Version-specific syntax: unresolved; no version-specific comment split was confirmed in the sources checked.
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
- Version scope: Kaitai Struct user guide and YAML 1.2 comment rules checked for current `.ksy` schema files.
- Version-specific syntax: `.ksy` files are YAML, so `#` comments apply outside scalar content. No Kaitai-specific block or nested comment form exists.
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://doc.kaitai.io/user_guide.html ; https://yaml.org/spec/1.2.2/#61-indentation-spaces
- Implementation source: https://github.com/kaitai-io/kaitai_struct_compiler
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: YAML comments are not part of scalar values; parser fixtures should avoid quoted strings containing `#`.

### Examples

#### Line comment
```text
meta:
  id: png
  endian: be # multi-byte fields are big-endian
seq:
  - id: signature
    size: 8
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## KakouneScript

- Registry key: `kakounescript`
- Version scope: current Kakoune scripting docs and command parser sources checked.
- Version-specific syntax: no version split found; comments are `#` line comments in Kakoune command/script files.
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://github.com/mawww/kakoune/blob/master/doc/pages/command-parsing.asciidoc
- Implementation source: https://github.com/mawww/kakoune
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: The command language is shell-like; comments should not be recognized inside strings or quoted command arguments.

### Examples

#### Line comment
```text
# load project options
declare-option str project_root %sh{pwd}
map global normal <c-p> ': edit %opt{project_root}/'
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

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
- Version scope: KiCad legacy PCB board file format V1/V2 documentation and legacy PCB parser sources checked.
- Version-specific syntax: legacy V2 examples use `#` header/comment lines; no semicolon comment form was confirmed. Registry should implement `#` line comments for legacy board files and not `;`.
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/ ; https://dev-docs.kicad.org/en/file-formats/legacy-pcb/
- Implementation source: https://gitlab.com/kicad/code/kicad
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Existing packet semicolon candidate was not confirmed for KiCad legacy layout.

### Examples

#### Line comment
```text
PCBNEW-BOARD Version 2 date 2024-01-01
# Created by KiCad
$GENERAL
LayerCount 2
$EndGENERAL
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

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
- Version scope: current kit-lang.org documentation version 2026.6.9 checked; legacy `kitlang/kit` material did not expose a stronger current comment reference.
- Version-specific syntax: current Kit uses `#` line comments, with `##` used for doc comments. No block form was documented.
- Line comments: `#`, including doc-comment form `##`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://kit-lang.org/docs/2026.6.9/index.html
- Implementation source: https://github.com/kitlang/kit
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Scope this to the current documented Kit language. If the registry intends the older pre-alpha Kit implementation, split the dialect before adding syntax.

### Examples

#### Line comment
```text
# normal comment
##Documentation for the next definition
let answer = 42
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## KRL

- Registry key: `krl`
- Version scope: KUKA Robot Language references for KSS-era KRL and open parser grammars checked.
- Version-specific syntax: no version split found; KRL comments begin with `;` and continue to the end of the physical line.
- Line comments: `;`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://support.industry.siemens.com/cs/attachments/109477421/KUKA_KRL_Reference_en.pdf
- Implementation source: https://github.com/tree-sitter-grammars/tree-sitter-krl
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: KRL declarations often use semicolon comments after motion commands.

### Examples

#### Line comment
```text
DEF pick_part()
  PTP HOME ; move to start position
  LIN XP1
END
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Kusto

- Registry key: `kusto`
- Version scope: `Microsoft Learn KQL comment syntax, reviewed 2026-05-22.`
- Version-specific syntax: `Applies across Kusto Query Language surfaces listed by Microsoft Learn.`
- Line comments: `//`
- Block comments: `unsupported`
- Termination behavior: `end of line`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [Add a comment in KQL](https://learn.microsoft.com/en-us/kusto/query/comment?view=microsoft-fabric)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with slash-line fixtures.`
- Notes: `KQL uses // comments on separate lines or after query text.`

### Examples

#### Line comment
```text
StormEvents
// Return the count
| count
```

#### Block comment
Unsupported.

## kvlang

- Registry key: `kvlang`
- Version scope: current Kivy language documentation and `kivy.lang.parser` source checked.
- Version-specific syntax: Kivy strips comment lines only when the first non-whitespace character is `#`; `#:` introduces directives such as `#:import` and is not a comment. Inline trailing `#` is not a general kvlang comment form.
- Line comments: `#` only as the first non-whitespace character on a line
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://kivy.org/doc/stable/guide/lang.html
- Implementation source: https://github.com/kivy/kivy/blob/master/kivy/lang/parser.py
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Keep `#:` directives out of generated comment fixtures.

### Examples

#### Line comment
```text
#:import dp kivy.metrics.dp
# This label is shown on the home screen
Label:
    text: 'Hello'
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## LabVIEW

- Registry key: `labview`
- Version scope: current NI LabVIEW documentation for block-diagram documentation and file formats checked.
- Version-specific syntax: LabVIEW G source is graphical rather than a line-oriented text language. It supports free labels and descriptions as diagram/documentation objects, not lexical line or block comment delimiters.
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.ni.com/docs/en-US/bundle/labview/page/documenting-vis.html
- Implementation source: proprietary LabVIEW environment; no public lexer source found
- Community source: not used
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: Do not add delimiter-based parser support for LabVIEW binary/graphical VI files. Textual project files should be handled by their underlying XML parser, not this language key.

### Examples

#### Line comment
Unsupported.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Lark

- Registry key: `lark`
- Version scope: Lark latest grammar reference and release note for 1.1.6 checked.
- Version-specific syntax: Lark grammars support `//` line comments; `#` line comments were added in Lark 1.1.6. No native `/* ... */` grammar comment form was confirmed.
- Line comments: `//`; `#` in Lark 1.1.6 and later
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://lark-parser.readthedocs.io/en/latest/grammar.html ; https://github.com/lark-parser/lark/releases/tag/1.1.6
- Implementation source: https://github.com/lark-parser/lark
- Community source: not used
- Corpus fallback source: not used
- Recommended action: update
- Notes: Existing C-style block candidate should be removed for Lark grammar files.

### Examples

#### Line comment
```text
start: item+
// comment supported by baseline Lark grammar
# comment supported in Lark 1.1.6+
item: WORD
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Lasso

- Registry key: `lasso`
- Version scope: Lasso 9 language guide references and syntax-highlighting grammars checked.
- Version-specific syntax: LassoScript uses `//` single-line and `/* ... */` block comments; no versioned nested comment form was found.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: medium
- Evidence mode: implementation_cross_checked
- Docs source: https://lassoguide.com/
- Implementation source: https://github.com/SublimeText/Lasso
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Public official docs are fragmented; syntax grammars corroborate the C-style forms.

### Examples

#### Line comment
```text
local(myName = 'Ada')
// show the current user
myName
```

#### Block comment
```text
/* setup values used by the page */
local(total = 10)
$total
```

#### Nested comment
Unsupported.

## Lex

- Registry key: `lex`
- Version scope: historical Lex behavior and current flex manual checked.
- Version-specific syntax: Lex/flex input files support C-style `/* ... */` comments where whitespace is allowed. No standalone `//` comment form is documented for lex grammar syntax.
- Line comments: unsupported
- Block comments: `/* ... */`
- Termination behavior: first closing `*/` wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.gnu.org/software/flex/manual/html_node/Comments-in-the-Input.html
- Implementation source: https://github.com/westes/flex
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Code copied inside `%{ ... %}` or action blocks is C and may contain C comments, but the lex-file comment delimiter is still the C block form.

### Examples

#### Line comment
Unsupported.

#### Block comment
```text
%{
#include <stdio.h>
%}
/* scanner rules for identifiers */
%%
[a-zA-Z_][a-zA-Z0-9_]*  return ID;
```

#### Nested comment
Unsupported.

## LFE

- Registry key: `lfe`
- Version scope: `Current LFE programming rules, reviewed 2026-05-22.`
- Version-specific syntax: `No version split found for semicolon comments.`
- Line comments: `;` with repeated semicolons used as style levels
- Block comments: `unsupported`
- Termination behavior: `end of line`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [LFE programming rules: comments](https://docs.lfe.io/current/prog-rules/8.html)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with semicolon line fixtures.`
- Notes: `The LFE rules distinguish one, two, three, and four semicolon comment styles.`

### Examples

#### Line comment
```text
(defun ping ()
  ; inline comment
  'pong)
```

#### Block comment
Unsupported.

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
- Version scope: current GNU binutils `ld` linker-script documentation checked.
- Version-specific syntax: GNU ld scripts use only C-style block comments; no versioned line-comment form was confirmed.
- Line comments: unsupported
- Block comments: `/* ... */`
- Termination behavior: first closing `*/` wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://sourceware.org/binutils/docs/ld/Script-Format.html
- Implementation source: https://sourceware.org/git/?p=binutils-gdb.git
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: The official manual states linker-script comments are syntactically equivalent to whitespace.

### Examples

#### Line comment
Unsupported.

#### Block comment
```text
/* place text first */
SECTIONS
{
  .text : { *(.text) }
}
```

#### Nested comment
Unsupported.

## Linux Kernel Module

- Registry key: `linux_kernel_module`
- Version scope: current Linux kernel C coding style plus C99/C11/C23 comment syntax checked.
- Version-specific syntax: kernel modules are C source files; `/* ... */` and `//` are accepted by modern kernel toolchains. Coding style favors block comments for multi-line explanatory text, but this is style guidance rather than a syntax restriction.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://docs.kernel.org/process/coding-style.html ; https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
- Implementation source: GCC/Clang C preprocessors used for kernel builds
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Treat module files as C for comment extraction.

### Examples

#### Line comment
```text
static int demo_init(void)
{
	// short local note
	return 0;
}
```

#### Block comment
```text
/* Module initialization entry point. */
module_init(demo_init);
```

#### Nested comment
Unsupported.

## Literate Agda

- Registry key: `literate_agda`
- Version scope: current Agda lexical syntax and literate programming documentation checked.
- Version-specific syntax: Agda code uses `--` line comments and nested `{- ... -}` block comments. Literate Agda additionally distinguishes prose from code blocks, but comments inside Agda code use the same Agda delimiters.
- Line comments: `--`
- Block comments: `{- ... -}`
- Termination behavior: `--` terminates at a line break; `{- ... -}` supports balanced nesting.
- Nested comments: true nesting supported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://agda.readthedocs.io/en/latest/language/lexical-structure.html ; https://agda.readthedocs.io/en/latest/tools/literate-programming.html
- Implementation source: https://github.com/agda/agda
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Literate prose is not a comment delimiter; fixtures should include code-fenced or bird-style Agda where the delimiters occur in code.

### Examples

#### Line comment
```text
\begin{code}
module Demo where
-- visible only to Agda readers
\end{code}
```

#### Block comment
```text
\begin{code}
{- explanation of the next declaration -}
id : Set -> Set
id A = A
\end{code}
```

#### Nested comment
```text
\begin{code}
{- outer {- inner -} outer -}
postulate A : Set
\end{code}
```

## Literate CoffeeScript

- Registry key: `literate_coffeescript`
- Version scope: CoffeeScript 1.x/2.x documentation for comments and literate mode checked.
- Version-specific syntax: CoffeeScript uses `#` line comments and `### ... ###` block comments; literate CoffeeScript changes code/prose recognition but not the comment delimiters inside code.
- Line comments: `#`
- Block comments: `### ... ###`
- Termination behavior: `#` terminates at a line break; `### ... ###` terminates at the first closing `###`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://coffeescript.org/#comments ; https://coffeescript.org/#literate
- Implementation source: https://github.com/jashkenas/coffeescript
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: A literate document's prose is not a lexical comment; only CoffeeScript code comments should be extracted.

### Examples

#### Line comment
```text
This paragraph is prose.

    square = (x) -> x * x
    # code comment
```

#### Block comment
```text
    ###
    block comment in literate CoffeeScript code
    ###
    answer = 42
```

#### Nested comment
Unsupported.

## Literate Haskell

- Registry key: `literate_haskell`
- Version scope: Haskell 2010 Report lexical syntax and GHC literate source behavior checked.
- Version-specific syntax: Haskell uses `--` line comments and nested `{- ... -}` comments. Literate Haskell changes how code is selected from prose, not the Haskell comment delimiters inside code.
- Line comments: `--`
- Block comments: `{- ... -}`
- Termination behavior: `--` terminates at a line break; `{- ... -}` supports balanced nesting.
- Nested comments: true nesting supported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.haskell.org/onlinereport/haskell2010/haskellch2.html ; https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/literate_haskell.html
- Implementation source: https://gitlab.haskell.org/ghc/ghc
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Bird-track `>` and LaTeX `\begin{code}` literate regions are code-selection mechanisms, not comments.

### Examples

#### Line comment
```text
> main = do
>   -- print a greeting
>   putStrLn "hello"
```

#### Block comment
```text
\begin{code}
main = do
  {- block note -}
  putStrLn "hello"
\end{code}
```

#### Nested comment
```text
> value = {- outer {- inner -} outer -} 1
```

## LiveScript

- Registry key: `livescript`
- Version scope: LiveScript 1.6.0 language documentation checked.
- Version-specific syntax: LiveScript single-line comments start with `#`; multiline comments use `/* ... */` and are preserved in compiled JavaScript. The docs explicitly say CoffeeScript `### ... ###` block comments were changed to `/* ... */`.
- Line comments: `#`
- Block comments: `/* ... */`
- Termination behavior: `#` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://livescript.net/#literals-comments
- Implementation source: https://github.com/gkz/LiveScript
- Community source: not used
- Corpus fallback source: not used
- Recommended action: update
- Notes: Existing `//` and `### ... ###` candidates are not LiveScript comments in the current docs; `//` is used for regular-expression literals and generated JavaScript examples.

### Examples

#### Line comment
```text
# compute a total
total = 1 + 2
```

#### Block comment
```text
/* this comment is preserved
   in generated JavaScript */
total = 1 + 2
```

#### Nested comment
Unsupported.

## Logos

- Registry key: `logos`
- Version scope: current Theos Logos syntax documentation and Logos processor sources checked.
- Version-specific syntax: Logos embeds Objective-C/C-like code and examples use Objective-C `//` and `/* ... */` comments. No Logos-specific nested or alternate comment form was found.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://theos.dev/docs/logos-syntax
- Implementation source: https://github.com/theos/logos
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Logos directives begin with `%`; do not confuse them with comments.

### Examples

#### Line comment
```text
%hook SpringBoard
// called when SpringBoard finishes launching
- (void)applicationDidFinishLaunching:(id)application {
  %orig;
}
%end
```

#### Block comment
```text
/* hook only for this tweak group */
%group Enabled
%end
```

#### Nested comment
Unsupported.

## Logtalk

- Registry key: `logtalk`
- Version scope: current Logtalk manuals and parser sources checked.
- Version-specific syntax: Logtalk follows Prolog comment syntax with `%` line comments and `/* ... */` block comments. No nested block comments were confirmed.
- Line comments: `%`
- Block comments: `/* ... */`
- Termination behavior: `%` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://logtalk.org/manuals/refman/syntax.html
- Implementation source: https://github.com/LogtalkDotOrg/logtalk3
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Logtalk documentation comments are conventions layered on Prolog-style delimiters.

### Examples

#### Line comment
```text
:- object(counter).
  % public predicate
  :- public(value/1).
:- end_object.
```

#### Block comment
```text
/* example object used in tests */
:- object(example).
:- end_object.
```

#### Nested comment
Unsupported.

## LookML

- Registry key: `lookml`
- Version scope: current Google Cloud Looker LookML documentation checked.
- Version-specific syntax: LookML files use `#` comments. No block or nested comment form was confirmed.
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://cloud.google.com/looker/docs/lookml-terms-and-concepts ; https://cloud.google.com/looker/docs/reference/param-model-include
- Implementation source: proprietary Looker parser; public LookML examples in Google Cloud docs
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Examples show both full-line and trailing `#` comments.

### Examples

#### Line comment
```text
# file: ecommerce.model.lookml
connection: order_database
include: "*.view" # include all the views
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## LoomScript

- Registry key: `loomscript`
- Version scope: archived Loom SDK / LoomScript documentation and grammar sources checked.
- Version-specific syntax: LoomScript is ActionScript/ECMAScript-like and uses `//` and `/* ... */` comments. No nested block form was found.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: medium
- Evidence mode: implementation_cross_checked
- Docs source: https://github.com/LoomSDK/LoomSDK/wiki
- Implementation source: https://github.com/LoomSDK/LoomSDK
- Community source: not used
- Corpus fallback source: https://github.com/LoomSDK/LoomSDK/tree/master/docs/examples
- Recommended action: confirm
- Notes: Official web docs are archived; source and examples corroborate C/AS3-style comments.

### Examples

#### Line comment
```text
class Player {
    // update position each frame
    public function tick():void {}
}
```

#### Block comment
```text
/* component state shared with native code */
class Component {
}
```

#### Nested comment
Unsupported.

## LSL

- Registry key: `lsl`
- Version scope: current Second Life LSL portal/wiki references and open LSL parser/highlighter sources checked.
- Version-specific syntax: LSL uses C-style `//` line comments and `/* ... */` block comments; no versioned nested syntax was confirmed.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://wiki.secondlife.com/wiki/LSL_Portal
- Implementation source: https://github.com/buildersbrewery/lsl-parser
- Community source: https://wiki.secondlife.com/wiki/LSL_Style_Guide
- Corpus fallback source: not used
- Recommended action: add
- Notes: Linden Lab's wiki is the practical language reference; parser sources match C-style comments.

### Examples

#### Line comment
```text
default
{
    state_entry()
    {
        // say hello when rezzed
        llSay(0, "hello");
    }
}
```

#### Block comment
```text
/* listen handler disabled during setup */
default
{
    touch_start(integer total_number) { }
}
```

#### Nested comment
Unsupported.

## LTspice Symbol

- Registry key: `ltspice_symbol`
- Version scope: LTspice `.asy` symbol examples and syntax references checked for current ASCII symbol files.
- Version-specific syntax: no official textual comment delimiter was confirmed for `.asy` symbol files. The format is record-oriented, and public examples do not show a stable comment token.
- Line comments: unresolved
- Block comments: unsupported
- Termination behavior: unresolved for line comments; no block terminator
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: https://ltwiki.org/LTspiceHelp/LTspiceHelp/Symbol_Editor.htm
- Implementation source: proprietary LTspice parser; no public parser source found
- Community source: https://ltwiki.org/index.php?title=Components_Library_and_Circuits
- Corpus fallback source: https://github.com/search?q=extension%3Aasy+%22Version+4%22+%22SymbolType%22&type=code
- Recommended action: research
- Notes: Do not add the current unresolved delimiter guesses. A larger corpus pass may still find tool-specific comment records, but none were confirmed here.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## M

- Registry key: `m`
- Version scope: MUMPS/M language references and GT.M/YottaDB implementation documentation checked.
- Version-specific syntax: M line comments begin with `;`; no block syntax is part of the language. Implement the semicolon line form.
- Line comments: `;`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://mumps.sourceforge.net/docs.html ; https://docs.yottadb.com/ProgrammersGuide/langfeat.html
- Implementation source: https://gitlab.com/YottaDB/DB/YDB
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: In M source, labels and commands can precede a semicolon comment on the same physical line.

### Examples

#### Line comment
```text
HELLO ; entry point
 WRITE "hello",!
 QUIT ; done
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## M4

- Registry key: `m4`
- Version scope: `GNU m4 1.4.20 manual, reviewed 2026-05-22.`
- Version-specific syntax: `Default delimiters are # and newline; changecom can alter delimiters at runtime.`
- Line comments: `#`
- Block comments: `unsupported by default`
- Termination behavior: `end of line`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [GNU m4 comments](https://www.gnu.org/software/m4/manual/html_node/Comments.html)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with default # fixtures.`
- Notes: `dnl discards input to newline but is a macro, not the default comment delimiter.`

### Examples

#### Line comment
```text
define([name], [value])
# comment
name
```

#### Block comment
Unsupported by the default delimiter configuration.

## M4Sugar

- Registry key: `m4sugar`
- Version scope: `GNU m4 default comment behavior used by M4Sugar inputs, reviewed 2026-05-22.`
- Version-specific syntax: `Default delimiters are # and newline; changecom can alter delimiters at runtime.`
- Line comments: `#`
- Block comments: `unsupported by default`
- Termination behavior: `end of line`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [GNU m4 comments](https://www.gnu.org/software/m4/manual/html_node/Comments.html)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented as an m4 syntax alias with default # fixtures.`
- Notes: `The registry models the default m4 comment delimiter; project-specific changecom use remains out of scope.`

### Examples

#### Line comment
```text
define([name], [value])
# comment
name
```

#### Block comment
Unsupported by the default delimiter configuration.

## Macaulay2

- Registry key: `macaulay2`
- Version scope: `Current Macaulay2 language documentation, reviewed 2026-05-22.`
- Version-specific syntax: `No version split found for -- and -* ... *- comments.`
- Line comments: `--`
- Block comments: `-* ... *-`
- Termination behavior: `end of line for --; first closing *- wins for enclosed comments`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [Macaulay2 comments](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_comments.html)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with line and enclosed-comment fixtures.`
- Notes: `The previous candidate block form was corrected from C-style syntax to -* ... *-.`

### Examples

#### Line comment
```text
x = 1 -- this is a comment
```

#### Block comment
```text
y = -* this is an enclosed comment *- 2
```

#### Nested comment
Unsupported.

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
- Version scope: MaskJS/mask template documentation and parser sources checked.
- Version-specific syntax: Mask templates use JavaScript/CSS-style `//` line comments and `/* ... */` block comments in template source. No nested form was confirmed.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: medium
- Evidence mode: implementation_cross_checked
- Docs source: https://github.com/atmajs/maskjs/wiki
- Implementation source: https://github.com/atmajs/maskjs
- Community source: not used
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: Public docs are wiki-based and sparse; parser/tokenizer sources are the stronger evidence.

### Examples

#### Line comment
```text
// template header
h1 > 'Dashboard'
section > 'Body'
```

#### Block comment
```text
/* hide this region while testing */
section.debug > 'debug'
```

#### Nested comment
Unsupported.

## Max

- Registry key: `max`
- Version scope: Cycling '74 Max patcher JSON (`.maxpat`, `.maxhelp`) and text/code boxes checked.
- Version-specific syntax: serialized Max patcher files are JSON and do not support native comments. C-style comments occur inside embedded JavaScript, genexpr, or codebox text, but those are embedded languages rather than Max patcher syntax.
- Line comments: unsupported for Max patcher files
- Block comments: unsupported for Max patcher files
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://docs.cycling74.com/max8/vignettes/maxpat_json ; https://docs.cycling74.com/max8/vignettes/javascriptinmax
- Implementation source: proprietary Max parser; JSON patcher format documentation
- Community source: not used
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: Existing C-style candidate should be scoped to embedded JavaScript/genexpr, not the `max` language key for patcher files.

### Examples

#### Line comment
Unsupported.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## MAXScript

- Registry key: `maxscript`
- Version scope: Autodesk 3ds Max MAXScript documentation through current online help checked.
- Version-specific syntax: MAXScript supports `--` single-line comments and `/* ... */` block comments. No nested block syntax was documented.
- Line comments: `--`
- Block comments: `/* ... */`
- Termination behavior: `--` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://help.autodesk.com/cloudhelp/2022/ENU/MAXDEV-Overview/files/overview/MAXDEV_Overview_overview_maxscript_html.html
- Implementation source: Autodesk MAXScript interpreter; https://github.com/tree-sitter-grammars/tree-sitter-maxscript
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: MAXScript comments resemble SQL/Ada line comments plus C-style block comments.

### Examples

#### Line comment
```text
-- create a box
b = box length:10 width:10 height:10
```

#### Block comment
```text
/* assign a material later */
b = sphere radius:5
```

#### Nested comment
Unsupported.

## mcfunction

- Registry key: `mcfunction`
- Version scope: Minecraft Java Edition function files since Java Edition 1.12 and current data-pack references checked.
- Version-specific syntax: function files use `#` comments on comment lines. Commands themselves cannot have trailing arbitrary comments because the line is parsed as a command.
- Line comments: `#` when it is the first non-whitespace character on a line
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://minecraft.wiki/w/Function_(Java_Edition)
- Implementation source: Mojang command-function loader is not public; syntax corroborated by data-pack tooling grammars such as https://github.com/SpyglassMC/Spyglass
- Community source: https://minecraft.wiki/w/Function_(Java_Edition)
- Corpus fallback source: not used
- Recommended action: add
- Notes: Use community/docs evidence because Mojang's implementation source is not public. Treat inline `#` inside a command as command text unless the command grammar says otherwise.

### Examples

#### Line comment
```text
# Give the player a starter item
give @p minecraft:stone 1
say setup complete
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Mercury

- Registry key: `mercury`
- Version scope: Mercury reference manual and compiler sources checked.
- Version-specific syntax: Mercury uses `%` line comments and `/* ... */` block comments. No nested block syntax was confirmed.
- Line comments: `%`
- Block comments: `/* ... */`
- Termination behavior: `%` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://www.mercurylang.org/information/doc-release/mercury_ref/Lexical-syntax.html
- Implementation source: https://github.com/Mercury-Language/mercury
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Mercury syntax is Prolog-like for line comments and C-like for block comments.

### Examples

#### Line comment
```text
:- module hello.
% exported predicate
:- interface.
```

#### Block comment
```text
/* implementation details */
:- implementation.
```

#### Nested comment
Unsupported.

## Metal

- Registry key: `metal`
- Version scope: Apple Metal Shading Language specification for Metal 2/3-era language checked.
- Version-specific syntax: Metal is C++14-based for lexical comments: `//` and `/* ... */`, with non-nesting block comments.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf
- Implementation source: https://github.com/tree-sitter-grammars/tree-sitter-metal
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Treat `.metal` source as C++-family for comment extraction.

### Examples

#### Line comment
```text
kernel void fill(device float *out [[buffer(0)]]) {
  // write the first value
  out[0] = 1.0;
}
```

#### Block comment
```text
/* shared utility used by kernels */
float twice(float x) { return x * 2.0; }
```

#### Nested comment
Unsupported.

## Microsoft Developer Studio Project

- Registry key: `msdev_project`
- Version scope: Visual C++ 5/6 `.dsp` Developer Studio project files checked via corpus and parser references.
- Version-specific syntax: `.dsp` files use `#`-prefixed lines for generated file headers, section markers, and comments. No block syntax was found.
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: candidate
- Evidence mode: corpus_inferred
- Docs source: unresolved
- Implementation source: https://github.com/Kitware/CMake/blob/master/Source/cmDSPParser.cxx
- Community source: not used
- Corpus fallback source: https://sources.debian.org/src/libprojectm/1.2.0-1/libprojectM.dsp/ ; https://www.novell.com/developer/documentation/samplecode/gwmapi_sample/Mapi1/CPP/GWMAPI1.DSP.html
- Recommended action: add
- Notes: Strong official docs were not found, but independent `.dsp` files and CMake parser behavior support `#` line handling.

### Examples

#### Line comment
```text
# Microsoft Developer Studio Project File - Name="Sample" - Package Owner=<4>
# Microsoft Developer Studio Generated Build File, Format Version 6.00
# ** DO NOT EDIT **
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Microsoft Visual Studio Solution

- Registry key: `visual_studio_solution`
- Version scope: Visual Studio solution-file format documentation for VS 2010 through VS 2022 and solution parsers checked.
- Version-specific syntax: `.sln` files contain required header records beginning with `# Visual Studio Version ...`; this is not a general comment grammar. No arbitrary comment syntax was confirmed.
- Line comments: unsupported as a general comment syntax
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://learn.microsoft.com/en-us/visualstudio/extensibility/internals/solution-dot-sln-file
- Implementation source: https://github.com/dotnet/msbuild/blob/main/src/Build/Construction/Solution/SolutionFile.cs
- Community source: not used
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: Do not treat the `# Visual Studio Version` header as a comment fixture unless downstream explicitly wants file-format metadata lines.

### Examples

#### Line comment
Unsupported.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Mirah

- Registry key: `mirah`
- Version scope: Mirah language docs/examples and compiler parser sources checked.
- Version-specific syntax: Mirah follows Ruby-style `#` line comments and `=begin`/`=end` block comments. No nested block form was found.
- Line comments: `#`
- Block comments: `=begin ... =end`
- Termination behavior: `#` terminates at a line break; block comments terminate at the first line containing `=end` at the block-comment boundary.
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://github.com/mirah/mirah/wiki
- Implementation source: https://github.com/mirah/mirah
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Keep block examples line-oriented like Ruby comments.

### Examples

#### Line comment
```text
class Greeter
  # print a greeting
  def hello
  end
end
```

#### Block comment
```text
=begin
Class used in parser examples.
=end
class Greeter
end
```

#### Nested comment
Unsupported.

## mIRC Script

- Registry key: `mirc_script`
- Version scope: current mIRC scripting help and script examples checked.
- Version-specific syntax: mIRC script files use semicolon line comments and also support C-style `/* ... */` block comments in scripts. No nested block form was confirmed.
- Line comments: `;`
- Block comments: `/* ... */`
- Termination behavior: `;` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.mirc.com/help/html/index.html
- Implementation source: proprietary mIRC interpreter; no public lexer source found
- Community source: https://en.wikichip.org/wiki/mirc/scripting/comments
- Corpus fallback source: not used
- Recommended action: add
- Notes: Existing line-only candidate should be expanded to include the confirmed block form.

### Examples

#### Line comment
```text
alias hello {
  ; show a message
  echo -a hello
}
```

#### Block comment
```text
/* disabled while testing
alias oldhello { echo -a old }
*/
alias hello { echo -a hello }
```

#### Nested comment
Unsupported.

## MLIR

- Registry key: `mlir`
- Version scope: current MLIR language reference and LLVM MLIR lexer sources checked.
- Version-specific syntax: MLIR supports BCPL-style `//` line comments only. No block comment form was documented.
- Line comments: `//`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://mlir.llvm.org/docs/LangRef/
- Implementation source: https://github.com/llvm/llvm-project/tree/main/mlir/lib/AsmParser
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: The language reference explicitly notes `//` comments; `#` has other grammar roles and is not a comment.

### Examples

#### Line comment
```text
// A function that returns its argument.
func.func @id(%arg0: i32) -> i32 {
  return %arg0 : i32
}
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Modula-2

- Registry key: `modula_2`
- Version scope: Wirth/PIM-style Modula-2 references, ISO-family descriptions, and GNU Modula-2 docs checked.
- Version-specific syntax: standard Modula-2 uses `(* ... *)` comments, and comments may nest. Some compilers add dialect extensions, but no portable line-comment form should be added under the generic key.
- Line comments: unsupported
- Block comments: `(* ... *)`
- Termination behavior: balanced nested comments; the outer comment terminates only after matching nested `*)` closers.
- Nested comments: true nesting supported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.modula2.org/reference/lexical.html ; https://gcc.gnu.org/onlinedocs/gm2/Comments.html
- Implementation source: https://gcc.gnu.org/git/?p=gcc.git;a=tree;f=gcc/m2
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Avoid adding GNU/dialect-specific comment extensions unless a separate dialect key is introduced.

### Examples

#### Line comment
Unsupported.

#### Block comment
```text
MODULE Demo;
(* module-level note *)
BEGIN
END Demo.
```

#### Nested comment
```text
MODULE Demo;
(* outer (* inner *) outer *)
BEGIN
END Demo.
```

## Modula-3

- Registry key: `modula_3`
- Version scope: Modula-3 language definition and implementation references checked.
- Version-specific syntax: Modula-3 uses `(* ... *)` comments and supports nesting. No line-comment form was found in the language definition.
- Line comments: unsupported
- Block comments: `(* ... *)`
- Termination behavior: balanced nested comments; the outer comment terminates only after matching nested `*)` closers.
- Nested comments: true nesting supported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.cs.purdue.edu/homes/hosking/m3/reference/lexical.html
- Implementation source: https://github.com/modula3/cm3
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Same delimiter family as Modula-2, with true nesting.

### Examples

#### Line comment
Unsupported.

#### Block comment
```text
MODULE Demo;
(* module-level note *)
BEGIN
END Demo.
```

#### Nested comment
```text
MODULE Demo;
(* outer (* inner *) outer *)
BEGIN
END Demo.
```

## Module Management System

- Registry key: `module_management_system`
- Version scope: OpenVMS Module Management System (MMS) description-file manuals checked.
- Version-specific syntax: MMS description files use `!` for comments to the end of line. No block or nested form was confirmed.
- Line comments: `!`
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://docs.vmssoftware.com/vsi-decset-for-openvms-guide-to-the-module-management-system/
- Implementation source: proprietary OpenVMS MMS; no public lexer source found
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: MMS is make-like but uses exclamation comments rather than Makefile `#` comments.

### Examples

#### Line comment
```text
! Build the image from object files
program.exe : main.obj util.obj
    LINK main.obj,util.obj
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Monkey

- Registry key: `monkey`
- Version scope: Monkey/Monkey X language documentation and parser examples checked.
- Version-specific syntax: Monkey uses apostrophe line comments and `#Rem ... #End` block comments. Existing `#` line-comment candidate was not confirmed as the generic comment form.
- Line comments: `'`
- Block comments: `#Rem ... #End`
- Termination behavior: apostrophe comments terminate at end of line; `#Rem` blocks terminate at the first matching `#End` directive line.
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://monkeycoder.co.nz/Community/posts.php?topic=3441 ; https://github.com/blitz-research/monkey
- Implementation source: https://github.com/blitz-research/monkey
- Community source: https://en.wikibooks.org/wiki/BlitzMax/Comments
- Corpus fallback source: not used
- Recommended action: update
- Notes: `#` also introduces preprocessor/directive syntax, so do not treat all `#` lines as comments.

### Examples

#### Line comment
```text
Function Main()
    ' show a greeting
    Print "hello"
End
```

#### Block comment
```text
#Rem
Temporary notes for this module.
#End
Function Main()
End
```

#### Nested comment
Unsupported.

## Monkey C

- Registry key: `monkey_c`
- Version scope: current Garmin Connect IQ Monkey C documentation checked.
- Version-specific syntax: Monkey C uses C/Java-style `//` and `/* ... */` comments. No nested block form was confirmed.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://developer.garmin.com/connect-iq/core-topics/monkey-c/
- Implementation source: Garmin Connect IQ compiler; no public lexer source found
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Documentation comments such as `//!` or `/** ... */` are comment variants over the same delimiters.

### Examples

#### Line comment
```text
function initialize() {
    // configure the view
}
```

#### Block comment
```text
/* shared helper for drawing */
function compute() {
}
```

#### Nested comment
Unsupported.

## MoonScript

- Registry key: `moonscript`
- Version scope: current MoonScript reference and lexer sources checked.
- Version-specific syntax: MoonScript follows Lua-style comments with `--` line comments and long block comments beginning `--[[`. Lua-style equal-delimited long comments such as `--[=[ ... ]=]` should be considered a dialect-compatible variant if the parser supports them.
- Line comments: `--`
- Block comments: `--[[ ... ]]`; Lua long-bracket variants `--[=[ ... ]=]` when supported
- Termination behavior: `--` terminates at a line break; long comments terminate at the matching long-bracket closer for the same equals depth.
- Nested comments: unsupported as true nesting; equal-depth delimiters can contain other long-bracket text safely when depths differ.
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://moonscript.org/reference/#comments
- Implementation source: https://github.com/leafo/moonscript
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Implement the simple `--[[ ... ]]` form first unless the registry supports depth-qualified Lua long brackets.

### Examples

#### Line comment
```text
-- compute a total
total = 1 + 2
```

#### Block comment
```text
--[[
Notes about generated Lua.
]]
print total
```

#### Nested comment
Unsupported as true nesting.

## Motoko

- Registry key: `motoko`
- Version scope: `Motoko language manual, reviewed 2026-05-22.`
- Version-specific syntax: `No version split found for comment tokens.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `end of line for line comments; balanced nesting for block comments`
- Nested comments: `true nesting supported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [Motoko language manual: comments](https://docs.internetcomputer.org/motoko/language-manual/)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with line and nested block fixtures.`
- Notes: `Motoko treats all comments as whitespace and permits nested /* ... */ comments.`

### Examples

#### Line comment
```text
actor {
  // comment
}
```

#### Block comment
```text
actor {
  /* outer /* inner */ still outer */
}
```

#### Nested comment
```text
actor {
  /* outer /* inner */ still outer */
}
```

## Motorola 68K Assembly

- Registry key: `motorola_68k_assembly`
- Version scope: Motorola/Freescale 68000-family assembler references and common Motorola-syntax assembler grammars checked.
- Version-specific syntax: Motorola-style 68K assembly commonly supports `;` trailing comments and `*` whole-line comments in column 1. Dialects vary, so registry should include both confirmed line forms and no block form.
- Line comments: `;` anywhere outside operands/strings; `*` when it is the first character of a source line
- Block comments: unsupported
- Termination behavior: end of line
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://www.nxp.com/docs/en/reference-manual/M68000PRM.pdf
- Implementation source: https://sourceware.org/git/?p=binutils-gdb.git ; https://github.com/vasm-assembler/vasm
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Some assemblers support additional comment conventions. `*` should be column-sensitive to avoid matching multiplication expressions or labels.

### Examples

#### Line comment
```text
* reset vector table
        move.w  #1,d0      ; load flag
        rts
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Move

- Registry key: `move`
- Version scope: `Move Book coding conventions, reviewed 2026-05-22.`
- Version-specific syntax: `No version split found for standard and doc comment tokens.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `end of line for //; first closing delimiter wins for block comments`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [Move Book coding conventions](https://move-language.github.io/move/coding-conventions.html)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with line and block fixtures.`
- Notes: `The Move Book lists regular and doc forms: //, /* */, ///, and /** */.`

### Examples

#### Line comment
```text
module 0x1::m {
// comment
}
```

#### Block comment
```text
module 0x1::m {
/* comment */
}
```

## MQL4

- Registry key: `mql4`
- Version scope: current MQL4 syntax documentation checked.
- Version-specific syntax: MQL4 supports `//` single-line comments and `/* ... */` multi-line comments; multi-line comments cannot nest. The docs allow single-line comments inside multi-line comments as text.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a newline; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://docs.mql4.com/basis/syntax/commentaries
- Implementation source: MetaQuotes MQL4 compiler; no public lexer source found
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: Official docs explicitly state multi-line comments cannot be nested.

### Examples

#### Line comment
```text
//--- Single-line comment
int total = 0;
```

#### Block comment
```text
/* Multi-
   line comment */
int total = 1;
```

#### Nested comment
Unsupported.

## MQL5

- Registry key: `mql5`
- Version scope: current MQL5 syntax documentation checked.
- Version-specific syntax: MQL5 supports `//` single-line comments and `/* ... */` multi-line comments; multi-line comments cannot nest.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a newline; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.mql5.com/en/docs/basis/syntax/commentaries
- Implementation source: MetaQuotes MQL5 compiler; no public lexer source found
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: MQL5 mirrors the documented MQL4 comment behavior.

### Examples

#### Line comment
```text
//--- Single-line comment
int total = 0;
```

#### Block comment
```text
/* Multi-
   line comment */
int total = 1;
```

#### Nested comment
Unsupported.

## MTML

- Registry key: `mtml`
- Version scope: Movable Type Markup Language template documentation checked.
- Version-specific syntax: MTML templates can use HTML comments and the Movable Type `<mt:Ignore> ... </mt:Ignore>` block to hide template content from output. No line-comment form was confirmed.
- Line comments: unsupported
- Block comments: `<!-- ... -->`; `<mt:Ignore> ... </mt:Ignore>`
- Termination behavior: HTML comments terminate at the first `-->`; MT ignore blocks terminate at the first matching `</mt:Ignore>` tag.
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.movabletype.org/documentation/appendices/tags/ ; https://www.movabletype.org/documentation/appendices/tags/ignore.html
- Implementation source: https://github.com/movabletype/movabletype
- Community source: not used
- Corpus fallback source: not used
- Recommended action: add
- Notes: HTML comments may still be emitted as HTML depending on template context; `<mt:Ignore>` is the MTML-specific comment-like block.

### Examples

#### Line comment
Unsupported.

#### Block comment
```text
<!-- HTML comment in template output -->
<mt:Ignore>
Template-only note ignored by Movable Type.
</mt:Ignore>
<mt:Entries><$mt:EntryTitle$></mt:Entries>
```

#### Nested comment
Unsupported.

## MUF

- Registry key: `muf`
- Version scope: TinyMUCK/FuzzBall MUF programmer references and source examples checked.
- Version-specific syntax: MUF uses parenthesized comments `( ... )` and backslash line comments in common Forth-derived implementations. No true nested comment support was confirmed.
- Line comments: `\`
- Block comments: `( ... )`
- Termination behavior: backslash comments terminate at end of line; parenthesized comments terminate at the first `)`.
- Nested comments: unsupported
- Confidence: medium
- Evidence mode: implementation_cross_checked
- Docs source: https://www.mufarchive.com/programming/mufman/
- Implementation source: https://github.com/fuzzball-muck/fuzzball
- Community source: https://www.mufarchive.com/
- Corpus fallback source: not used
- Recommended action: confirm
- Notes: MUF dialects vary across MUCK servers; verify target dialect before broad registry rollout.

### Examples

#### Line comment
```text
: main
  \ greet the caller
  "hello" .tell
;
```

#### Block comment
```text
: main
  ( setup message )
  "hello" .tell
;
```

#### Nested comment
Unsupported.

## mupad

- Registry key: `mupad`
- Version scope: MuPAD language documentation and MATLAB Symbolic Math Toolbox archived references checked.
- Version-specific syntax: MuPAD supports `//` line comments and `/* ... */` block comments. No nested block form was confirmed.
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `//` terminates at a line break; `/* ... */` terminates at the first `*/`.
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.mathworks.com/help/symbolic/mupad_programming.html
- Implementation source: proprietary MuPAD engine; no public lexer source found
- Community source: https://en.wikibooks.org/wiki/MuPAD/Comments
- Corpus fallback source: not used
- Recommended action: add
- Notes: MuPAD has been removed from recent MATLAB releases, so scope is archived/legacy MuPAD notebooks and code.

### Examples

#### Line comment
```text
// compute a symbolic result
f := x -> x^2:
```

#### Block comment
```text
/* helper expression used in examples */
g := x -> x + 1:
```

#### Nested comment
Unsupported.

## Muse

- Registry key: `muse`
- Version scope: Emacs Muse / Muse markup references and examples checked.
- Version-specific syntax: no stable, language-level comment delimiter was confirmed for Muse markup. HTML comments may occur in emitted/embedded HTML, but that is HTML rather than Muse-native syntax.
- Line comments: unresolved
- Block comments: unresolved for Muse-native syntax; embedded HTML may use `<!-- ... -->`
- Termination behavior: unresolved for native Muse comments; embedded HTML comments terminate at first `-->`.
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: https://www.gnu.org/software/emacs-muse/manual/
- Implementation source: https://git.savannah.gnu.org/cgit/emacs/elpa.git/tree/packages/muse
- Community source: not used
- Corpus fallback source: not used
- Recommended action: research
- Notes: Do not add generic HTML comments under the Muse key unless the parser intentionally extracts embedded markup comments.

### Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported or unresolved.

#### Nested comment
Unsupported.

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
- Version scope: Jinja 2.10.x, 3.1.x, and 3.2.x docs checked.
- Version-specific syntax: `{# ... #}` is stable; line-comment support via `line_comment_prefix` was added in version 2.2. Registry should keep the union of confirmed forms and treat `##` as versioned support rather than the baseline in older releases.
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
- Version scope: current Liquid docs, Shopify Liquid docs, and Liquid variation docs checked.
- Version-specific syntax: no conflicting delimiter split was confirmed among the sources checked; the current docs add inline comments, while `{% comment %}...{% endcomment %}` remains stable across the variants reviewed. Registry should keep the union of the confirmed forms used by the supported Liquid variants.
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
- Version scope: Mako 1.3.x docs checked.
- Version-specific syntax: no syntax split confirmed across the docs checked; `##` and `<%doc>... </%doc>` are stable. Registry should implement the union of the confirmed forms.
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
- Version scope: GNU Make 3.80 and 4.4.1 manuals checked.
- Version-specific syntax: no comment-syntax split confirmed; `#` remains the only native comment syntax in the manuals checked.
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
- Version scope: JAR File Specification for Java SE 25 and `java.util.jar.Manifest` behavior checked.
- Version-specific syntax: manifest files are RFC 822-style name/value sections with continuation lines; no native comment field or delimiter is defined.
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://docs.oracle.com/en/java/javase/25/docs/specs/jar/jar.html
- Implementation source: https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/jar/Manifest.java
- Community source: not used
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: Lines beginning with `#` or other markers are not comments in the JAR manifest grammar.

### Examples

#### Line comment
Unsupported.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## JSON

- Registry key: `json`
- Version scope: RFC 8259 and ECMA-404 JSON grammar checked.
- Version-specific syntax: JSON has no comment productions. Comments are intentionally outside the grammar.
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.rfc-editor.org/rfc/rfc8259.html ; https://www.ecma-international.org/publications-and-standards/standards/ecma-404/
- Implementation source: standard JSON parsers
- Community source: not used
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: Use JSONC/JSON5 keys for comment-bearing JSON variants, not `json`.

### Examples

#### Line comment
Unsupported.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## JSONLD

- Registry key: `jsonld`
- Version scope: JSON-LD 1.1 W3C Recommendation and JSON grammar dependency checked.
- Version-specific syntax: JSON-LD documents use JSON syntax, so no native comment delimiters are defined.
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.w3.org/TR/json-ld11/ ; https://www.rfc-editor.org/rfc/rfc8259.html
- Implementation source: JSON-LD processors over JSON parsers
- Community source: not used
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: Comments can appear only in non-JSON transports or string values, not as JSON-LD syntax.

### Examples

#### Line comment
Unsupported.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Jupyter Notebook

- Registry key: `jupyter_notebook`
- Version scope: nbformat 4.x/current notebook JSON format checked.
- Version-specific syntax: `.ipynb` is JSON and has no native file-level comments. Individual code cells use their own kernel language syntax, which should be handled by that language key after cell extraction.
- Line comments: unsupported at notebook JSON level
- Block comments: unsupported at notebook JSON level
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://nbformat.readthedocs.io/en/latest/format_description.html ; https://www.rfc-editor.org/rfc/rfc8259.html
- Implementation source: https://github.com/jupyter/nbformat
- Community source: not used
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: Do not treat Python `#` comments inside code-cell strings as notebook-format comments.

### Examples

#### Line comment
Unsupported.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Markdown

- Registry key: `markdown`
- Version scope: CommonMark 0.31.2 checked.
- Version-specific syntax: CommonMark has no Markdown-native comment delimiter. It can pass through raw HTML comments as HTML blocks/inlines, but those belong to embedded HTML rather than Markdown syntax.
- Line comments: unsupported for Markdown-native syntax
- Block comments: unsupported for Markdown-native syntax; embedded HTML may use `<!-- ... -->`
- Termination behavior: unsupported for Markdown-native syntax; embedded HTML comments terminate at first `-->`.
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://spec.commonmark.org/0.31.2/
- Implementation source: https://github.com/commonmark/cmark
- Community source: not used
- Corpus fallback source: not used
- Recommended action: unsupported
- Notes: Keep the generic Markdown key non-actionable unless the registry adds explicit embedded-HTML comment support.

### Examples

#### Line comment
Unsupported.

#### Block comment
Unsupported for Markdown-native syntax.

#### Nested comment
Unsupported.
