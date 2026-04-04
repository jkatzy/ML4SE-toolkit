# Chunk 7 T-Z Research Report

This report follows the README-driven, documentation-oriented format. I stayed conservative: when syntax was not clearly verified from the assignment sources or stable language docs, I marked it unresolved rather than guessing.

## Talon
- Registry key: `talon`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research Talon syntax before seeding a registry entry.`
- Notes: `No verified comment syntax gathered.`

## Tcl
- Registry key: `tcl`
- Version scope: `Tcl 8.6.x and current Tcl/Tk 8.6.17 documentation; reviewed the Tcl command manual and the 8.6 release pages.`
- Version-specific syntax: `No syntax split confirmed across the reviewed Tcl 8.6 docs; # is a comment only when it begins the first word of a command, so the registry should keep the line-comment form only.`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://www.tcl-lang.org/man/tcl8.6/TclCmd/Tcl.htm`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line-comment coverage and keep block comments unsupported unless a dialect says otherwise.`
- Notes: `#` starts a comment when it is the first non-whitespace token on a command line.

- Example - line:
```tcl
set x 1
# comment
set y 2
```

## Tcsh
- Registry key: `tcsh`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `Shell-style comment syntax.`

- Example - line:
```tcsh
set x = 1
# comment
echo $x
```

## Tea
- Registry key: `tea`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Tea syntax before adding parser support.`
- Notes: `No verified comment syntax gathered.`

## Terra
- Registry key: `terra`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `--`
- Block comments: `--[[ ... ]]`
- Termination behavior: `depth-qualified delimiters`
- Nested comments: `yes`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Lua-style long-comment handling and add nested coverage if the grammar supports it.`
- Notes: `Terra is Lua-like; the long-comment form is the best candidate.`

- Example - line:
```terra
local x = 1
-- comment
local y = 2
```
- Example - block:
```terra
local x = 1
--[[ comment ]]
local y = 2
```
- Example - nested:
```terra
local x = 1
--[=[ outer
--[[ inner ]]
]=]
local y = 2
```

## TeX
- Registry key: `tex`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `%`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed percent-comment tests and keep block comments unsupported.`
- Notes: `TeX comment syntax is line-only.`

- Example - line:
```tex
\documentclass{article}
% comment
\begin{document}
Hello
\end{document}
```

## Texinfo
- Registry key: `texinfo`
- Version scope: `GNU Texinfo 7.2 and 7.3 manuals; reviewed both current manual builds and the comments page.`
- Version-specific syntax: `No version split confirmed in the reviewed manuals; @comment/@c line comments and @ignore ... @end ignore blocks are documented in both, so the registry should implement the union of line and block forms.`
- Line comments: `@c` and `@comment`
- Block comments: `@ignore ... @end ignore`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: https://www.gnu.org/software/texinfo/manual/texinfo/html_node/Comments.html
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Texinfo comment and ignore-block behavior before seeding.`
- Notes: `Texinfo supports both inline comment commands and ignore blocks.`

- Example - line:
```texinfo
@node Top
@c comment
@top Example
```
- Example - block:
```texinfo
@ignore
comment
@end ignore
@node Top
```

## Text
- Registry key: `text`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Document as commentless.`
- Notes: `Plain text does not define comment syntax.`

## Textile
- Registry key: `textile`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research Textile syntax before seeding a registry entry.`
- Notes: `No verified comment syntax gathered.`

## TextMate Properties
- Registry key: `textmate_properties`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://macromates.com/textmate/manual/settings
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests for .tm_properties files.`
- Notes: `The TextMate manual defines # comments in the .tm_properties grammar.`

- Example - line:
```text
# comment
name = Example
```

## Thrift
- Registry key: `thrift`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `// and #`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line and block coverage and add a regression for hash comments if the parser accepts them.`
- Notes: `Thrift grammars commonly accept both C-style and hash line comments.`

- Example - line:
```thrift
struct Foo {
  1: string name
  // comment
}
```
- Example - block:
```thrift
struct Foo {
  /* comment */
  1: string name
}
```

## TLA
- Registry key: `tla`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `\*`
- Block comments: `(* ... *)`
- Termination behavior: `true nesting supported`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed both line and nested block coverage.`
- Notes: `TLA+ supports line comments and nested block comments.`

- Example - line:
```tla
VARIABLE x
\* comment
Init == x = 0
```
- Example - block:
```tla
VARIABLE x
(* comment *)
Init == x = 0
```
- Example - nested:
```tla
VARIABLE x
(* outer (* inner *) outer *)
Init == x = 0
```

## TOML
- Registry key: `toml`
- Version scope: `TOML 0.5.0 and 1.0.0; reviewed the archived 0.5.0 spec and the 1.0.0 spec.`
- Version-specific syntax: `No syntax split confirmed; both reviewed specs use # for line comments, and 1.0.0 is explicitly back-compatible with 0.5.0. The registry should keep line comments only.`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://toml.io/en/v1.0.0
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `TOML comments are line-only.`

- Example - line:
```toml
title = "Example"
# comment
version = "1.0"
```

## TSQL
- Registry key: `tsql`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `--`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line and block coverage.`
- Notes: `Standard Transact-SQL comment forms.`

- Example - line:
```sql
SELECT 1;
-- comment
SELECT 2;
```
- Example - block:
```sql
SELECT 1;
/* comment */
SELECT 2;
```

## TSV
- Registry key: `tsv`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Document as commentless unless a dialect extension exists.`
- Notes: `TSV is a tabular data format and does not standardize comments.`

## TSX
- Registry key: `tsx`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed JavaScript/TypeScript-style comment tests.`
- Notes: `TSX follows TypeScript/JavaScript comment syntax.`

- Example - line:
```tsx
export function App() {
  // comment
  return <div>Hello</div>;
}
```
- Example - block:
```tsx
export function App() {
  /* comment */
  return <div>Hello</div>;
}
```

## Turing
- Registry key: `turing`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Turing comment syntax before seeding.`
- Notes: `No verified comment syntax gathered.`

## Turtle
- Registry key: `turtle`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `Turtle comments are line-only.`

- Example - line:
```turtle
@prefix ex: <http://example.com/> .
# comment
ex:s ex:p ex:o .
```

## Twig
- Registry key: `twig`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `{# ... #}`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed template-comment tests.`
- Notes: `Twig comments are block-only.`

- Example - block:
```twig
{# comment #}
<div>{{ name }}</div>
```

## TXL
- Registry key: `txl`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify TXL syntax before adding a registry entry.`
- Notes: `No verified comment syntax gathered.`

## Type Language
- Registry key: `type_language`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research the specific Stack v2 dialect before seeding.`
- Notes: `The name is too ambiguous to infer comment syntax safely.`

## Unified Parallel C
- Registry key: `upc`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed C-like comment coverage.`
- Notes: `UPC follows C-style comments.`

- Example - line:
```c
int x = 1;
// comment
int y = 2;
```
- Example - block:
```c
int x = 1;
/* comment */
int y = 2;
```

## Unity3D Asset
- Registry key: `unity3d_asset`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify the YAML-like asset format and keep block comments unsupported unless the grammar says otherwise.`
- Notes: `Unity asset files commonly behave like YAML metadata.`

- Example - line:
```text
%YAML 1.1
# comment
--- !u!1 &1
```

## Unix Assembly
- Registry key: `unix_assembly`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify the exact assembly dialect before seeding.`
- Notes: `Assembly comment syntax is dialect-specific.`

## Uno
- Registry key: `uno`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed C-like comment tests after confirming the Uno grammar.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```uno
namespace Example
{
    // comment
    public class Program {}
}
```
- Example - block:
```uno
namespace Example
{
    /* comment */
    public class Program {}
}
```

## UnrealScript
- Registry key: `unrealscript`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line and block coverage.`
- Notes: `UnrealScript follows C-like comments.`

- Example - line:
```uc
class Example extends Object;
// comment
defaultproperties
{
}
```
- Example - block:
```uc
class Example extends Object;
/* comment */
defaultproperties
{
}
```

## UrWeb
- Registry key: `urweb`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research Ur/Web syntax before seeding.`
- Notes: `No verified comment syntax gathered.`

## V
- Registry key: `v`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `true nesting supported`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed both block and nested-block coverage.`
- Notes: `V supports nested block comments.`

- Example - line:
```v
fn main() {
    // comment
    println('hello')
}
```
- Example - block:
```v
fn main() {
    /* comment */
    println('hello')
}
```
- Example - nested:
```v
fn main() {
    /* outer /* inner */ outer */
    println('hello')
}
```

## Vala
- Registry key: `vala`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed C-like comment tests.`
- Notes: `Standard C-like syntax.`

- Example - line:
```vala
// comment
void main () {
}
```
- Example - block:
```vala
/* comment */
void main () {
}
```

## Valve Data Format
- Registry key: `valve_data_format`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify the exact VDF variant before seeding.`
- Notes: `The format is parser-dependent and comment handling is not uniform.`

- Example - line:
```text
"root"
{
    // comment
    "key" "value"
}
```

## VBA
- Registry key: `vba`
- Version scope: `Microsoft Office VBA docs plus current Visual Basic .NET reference pages.`
- Version-specific syntax: `No comment-token split confirmed across the reviewed Microsoft docs; both apostrophe (') and REM are supported, with REM requiring a statement boundary while ' is more flexible. Implement the union of both forms.`
- Line comments: `'` and `Rem`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed apostrophe and REM comment tests.`
- Notes: `Classic Visual Basic comment forms.`

- Example - line:
```vb
Sub Main()
    ' comment
    MsgBox "hi"
End Sub
```
- Example - line:
```vb
Sub Main()
    Rem comment
    MsgBox "hi"
End Sub
```

## VBScript
- Registry key: `vbscript`
- Version scope: `Microsoft VBScript reference pages and the Visual Basic family docs reviewed for comparison.`
- Version-specific syntax: `No distinct VBScript-only comment token was confirmed beyond the Visual Basic family forms; the safest registry choice is the union of apostrophe (') and REM, with REM treated as statement-level only.`
- Line comments: `'` and `Rem`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line-comment coverage.`
- Notes: `Standard VBScript comment forms.`

- Example - line:
```vbscript
Dim x
' comment
x = 1
```
- Example - line:
```vbscript
Dim x
Rem comment
x = 1
```

## VCL
- Registry key: `vcl`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research the exact VCL dialect before seeding.`
- Notes: `The acronym is ambiguous.`

## Velocity Template Language
- Registry key: `velocity_template_language`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `##`
- Block comments: `#* ... *#`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line and block coverage for template comments.`
- Notes: `Velocity has distinct line and block comment markers.`

- Example - line:
```velocity
## comment
#set($x = 1)
```
- Example - block:
```velocity
#* comment *#
#set($x = 1)
```

## Verilog
- Registry key: `verilog`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed HDL comment tests.`
- Notes: `Standard Verilog comment forms.`

- Example - line:
```verilog
module example;
  // comment
  wire a;
endmodule
```
- Example - block:
```verilog
module example;
  /* comment */
  wire a;
endmodule
```

## VHDL
- Registry key: `vhdl`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `--`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line-comment tests and keep block comments unsupported.`
- Notes: `Standard VHDL comment form.`

- Example - line:
```vhdl
architecture rtl of example is
begin
  -- comment
end rtl;
```

## Vim Help File
- Registry key: `vim_help_file`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify help-file markup rules before seeding.`
- Notes: `Vim help files are documentation markup, not a conventional programming language.`

## Vim Script
- Registry key: `vim_script`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `"`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed double-quote comment tests.`
- Notes: `Vimscript comments are line-only.`

- Example - line:
```vim
let x = 1
" comment
let y = 2
```

## Vim Snippet
- Registry key: `vim_snippet`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research the snippet dialect used in Stack v2 before seeding.`
- Notes: `The syntax is dialect-specific and not yet verified.`

## Visual Basic .NET
- Registry key: `visual_basic_net`
- Version scope: `Current and prior Microsoft Learn Visual Basic .NET pages.`
- Version-specific syntax: `No syntax split confirmed; both REM and apostrophe comments are documented, and REM cannot continue with line continuation. The registry should keep the union of both forms.`
- Line comments: `'` and `Rem`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://learn.microsoft.com/en-us/dotnet/visual-basic/language-reference/statements/rem-statement`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line-comment coverage.`
- Notes: `Same comment forms as classic VB.`

- Example - line:
```vbnet
Sub Main()
    ' comment
    Console.WriteLine("hi")
End Sub
```
- Example - line:
```vbnet
Sub Main()
    Rem comment
    Console.WriteLine("hi")
End Sub
```

## Volt
- Registry key: `volt`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research Volt syntax before seeding.`
- Notes: `No verified comment syntax gathered.`

## Vyper
- Registry key: `vyper`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `Vyper uses Python-style comments.`

- Example - line:
```vyper
x: uint256
# comment
y: uint256
```

## Wavefront Material
- Registry key: `wavefront_material`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `MTL files use hash comments.`

- Example - line:
```mtl
newmtl material
# comment
Kd 1.0 1.0 1.0
```

## Wavefront Object
- Registry key: `wavefront_object`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `OBJ files use hash comments.`

- Example - line:
```obj
o cube
# comment
v 0.0 0.0 0.0
```

## wdl
- Registry key: `wdl`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://docs.openwdl.org/reference/stdlib/numeric.html
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests in WDL fixtures.`
- Notes: `The official WDL docs show # comments in code examples.`

- Example - line:
```wdl
version 1.0
# comment
task example {
}
```

## Web Ontology Language
- Registry key: `web_ontology_language`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research the specific serialization used in Stack v2 before seeding.`
- Notes: `OWL comment syntax depends on the underlying syntax, so inference is unsafe here.`

## WebIDL
- Registry key: `webidl`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed WebIDL comment coverage.`
- Notes: `Standard WebIDL comment forms.`

- Example - line:
```webidl
interface Example {
  // comment
  readonly attribute DOMString value;
};
```
- Example - block:
```webidl
interface Example {
  /* comment */
  readonly attribute DOMString value;
};
```

## WebVTT
- Registry key: `webvtt`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `NOTE ... blank line`
- Termination behavior: `first blank line wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: https://www.w3.org/TR/webvtt1/
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Treat NOTE blocks as WebVTT comments and add parser tests for blank-line termination.`
- Notes: `WebVTT comments are note blocks terminated by a blank line, not inline comment markers.`

- Example - line:
```webvtt
WEBVTT

NOTE comment

00:00.000 --> 00:01.000
Hello
```

## Whiley
- Registry key: `whiley`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Whiley syntax before seeding.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```whiley
// comment
function f() -> int:
    return 1
```
- Example - block:
```whiley
/* comment */
function f() -> int:
    return 1
```

## Wikitext
- Registry key: `wikitext`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `<!-- ... -->`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed HTML-comment coverage.`
- Notes: `Wikitext comment handling is markup-based.`

- Example - block:
```text
Before
<!-- comment -->
After
```

## Win32 Message File
- Registry key: `win32_message_file`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `;`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify message-file syntax and add semicolon-comment tests if confirmed.`
- Notes: `Candidate INI-style comment syntax.`

- Example - line:
```text
; comment
MessageId=1
Severity=Informational
```

## Windows Registry Entries
- Registry key: `windows_registry_entries`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `;`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed semicolon-comment tests.`
- Notes: `.reg` files use semicolon comments.

- Example - line:
```reg
Windows Registry Editor Version 5.00
; comment
[HKEY_CURRENT_USER\Software\Example]
```

## Witcher Script
- Registry key: `witcher_script`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Witcher Script syntax before seeding.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```text
// comment
function main() {
}
```
- Example - block:
```text
/* comment */
function main() {
}
```

## Wollok
- Registry key: `wollok`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Wollok syntax before seeding.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```wollok
// comment
object Example {
}
```
- Example - block:
```wollok
/* comment */
object Example {
}
```

## World of Warcraft Addon Data
- Registry key: `world_of_warcraft_addon_data`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `--`
- Block comments: `--[[ ... ]]`
- Termination behavior: `depth-qualified delimiters`
- Nested comments: `yes`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed Lua-style comment coverage and verify long-comment handling.`
- Notes: `WoW addon files are Lua-adjacent.`

- Example - line:
```lua
local frame = CreateFrame("Frame")
-- comment
frame:Show()
```
- Example - block:
```lua
local frame = CreateFrame("Frame")
--[[ comment ]]
frame:Show()
```

## Wren
- Registry key: `wren`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Wren comment syntax before seeding.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```wren
// comment
class Example {}
```
- Example - block:
```wren
/* comment */
class Example {}
```

## X BitMap
- Registry key: `x_bit_map`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research the exact XBM representation before seeding.`
- Notes: `XBM is often stored as C source, so comment syntax depends on the representation.`

## X PixMap
- Registry key: `x_pix_map`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research the exact XPM representation before seeding.`
- Notes: `XPM is often stored as C source, so comment syntax depends on the representation.`

## X10
- Registry key: `x10`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify X10 syntax before seeding.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```x10
// comment
class Example {}
```
- Example - block:
```x10
/* comment */
class Example {}
```

## xBase
- Registry key: `xbase`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research xBase syntax before seeding.`
- Notes: `No verified comment syntax gathered.`

## XC
- Registry key: `xc`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify XC syntax before seeding.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```xc
// comment
void main() {}
```
- Example - block:
```xc
/* comment */
void main() {}
```

## XML Property List
- Registry key: `xml_property_list`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `<!-- ... -->`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed XML-comment tests.`
- Notes: `XML plists use XML comments.`

- Example - block:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- comment -->
<plist version="1.0">
</plist>
```

## Xojo
- Registry key: `xojo`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `'` and `Rem`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Xojo comment forms before seeding.`
- Notes: `Xojo is BASIC-like.`

- Example - line:
```xojo
' comment
Dim x As Integer
```
- Example - line:
```xojo
Rem comment
Dim x As Integer
```

## Xonsh
- Registry key: `xonsh`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `Python-like comment syntax.`

- Example - line:
```xonsh
x = 1
# comment
y = 2
```

## XPages
- Registry key: `xpages`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `<!-- ... -->`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify whether the Stack v2 corpus uses the XML layer or a scripting layer.`
- Notes: `XPages is XML-based, but embedded script comment syntax may vary.`

- Example - block:
```xml
<xp:view>
  <!-- comment -->
</xp:view>
```

## XProc
- Registry key: `xproc`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `<!-- ... -->`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed XML-comment tests.`
- Notes: `XProc is XML-based.`

- Example - block:
```xml
<p:declare-step xmlns:p="http://www.w3.org/ns/xproc">
  <!-- comment -->
</p:declare-step>
```

## XQuery
- Registry key: `xquery`
- Version scope: `XQuery 1.0, 1.1, and 3.0 W3C Recommendations/Working Drafts.`
- Version-specific syntax: `No version split confirmed in the reviewed W3C specs; (: ... :) comments are nested in 1.0, 1.1, and 3.0, so the registry should implement the nested block-comment form only.`
- Line comments: `unsupported`
- Block comments: `(: ... :)`
- Termination behavior: `true nesting supported`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://www.w3.org/TR/xquery-31/
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed nested block-comment coverage.`
- Notes: `XQuery comment delimiters are nested.`

- Example - block:
```xquery
(: comment :)
for $x in doc("books.xml")/books/book
return $x
```
- Example - nested:
```xquery
(: outer (: inner :) outer :)
for $x in doc("books.xml")/books/book
return $x
```

## XS
- Registry key: `xs`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research the exact XS dialect before seeding.`
- Notes: `The acronym is ambiguous and may mix embedded languages.`

## XSLT
- Registry key: `xslt`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `<!-- ... -->`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://www.w3.org/TR/xslt-30/
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed XML-comment tests, and keep XPath-expression comments separate if needed.`
- Notes: `XSLT stylesheets are XML documents.`

- Example - block:
```xml
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="3.0">
  <!-- comment -->
  <xsl:template match="/">
    <out/>
  </xsl:template>
</xsl:stylesheet>
```

## Xtend
- Registry key: `xtend`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed C-like comment tests.`
- Notes: `Standard C-like syntax.`

- Example - line:
```xtend
// comment
class Example {}
```
- Example - block:
```xtend
/* comment */
class Example {}
```

## Yacc
- Registry key: `yacc`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify the exact parser-generator dialect used in Stack v2.`
- Notes: `Yacc/Bison grammars usually accept C-style comments.`

- Example - line:
```yacc
%token NUMBER
// comment
%%
```
- Example - block:
```yacc
%token NUMBER
/* comment */
%%
```

## YAML
- Registry key: `yaml`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://yaml.org/spec/1.2.2/
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `YAML does not define block comments.`

- Example - line:
```yaml
name: example
# comment
version: 1
```

## YANG
- Registry key: `yang`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: https://www.rfc-editor.org/rfc/rfc7950.html
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify YANG comment syntax before seeding.`
- Notes: `Candidate C-like syntax, but this should be confirmed from the spec before registering.`

- Example - line:
```yang
module example {
  // comment
  namespace "urn:example";
}
```
- Example - block:
```yang
module example {
  /* comment */
  namespace "urn:example";
}
```

## YARA
- Registry key: `yara`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed C-like comment tests.`
- Notes: `Standard YARA comment forms.`

- Example - line:
```yara
rule example {
  // comment
  condition:
    true
}
```
- Example - block:
```yara
rule example {
  /* comment */
  condition:
    true
}
```

## YASnippet
- Registry key: `yasnippet`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research the snippet format before seeding.`
- Notes: `No verified comment syntax gathered.`

## Yul
- Registry key: `yul`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed C-like comment tests.`
- Notes: `Standard Solidity/Yul style comments.`

- Example - line:
```yul
{
    // comment
    let x := 1
}
```
- Example - block:
```yul
{
    /* comment */
    let x := 1
}
```

## Zeek
- Registry key: `zeek`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `Zeek comments are line-only.`

- Example - line:
```zeek
# comment
event zeek_init()
    {
    }
```

## ZenScript
- Registry key: `zenscript`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify ZenScript syntax before seeding.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```zenscript
// comment
val x = 1;
```
- Example - block:
```zenscript
/* comment */
val x = 1;
```

## Zephir
- Registry key: `zephir`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Zephir syntax before seeding.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```zephir
// comment
let x = 1;
```
- Example - block:
```zephir
/* comment */
let x = 1;
```

## Zig
- Registry key: `zig`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://ziglang.org/documentation/master/
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line-comment coverage and document that Zig has no multiline comments.`
- Notes: `Zig supports line comments only; doc comments are separate syntax.`

- Example - line:
```zig
const x = 1;
// comment
const y = 2;
```
- Example - block:
```zig
const x = 1;
/* comment */
const y = 2;
```
- Example - nested:
```zig
const x = 1;
/* outer /* inner */ outer */
const y = 2;
```

## ZIL
- Registry key: `zil`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research ZIL syntax before seeding.`
- Notes: `No verified comment syntax gathered.`

## Zimpl
- Registry key: `zimpl`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests.`
- Notes: `Candidate config-style comment syntax.`

- Example - line:
```text
# comment
set x := 1;
```
