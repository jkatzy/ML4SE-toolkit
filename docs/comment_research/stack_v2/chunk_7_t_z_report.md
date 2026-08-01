# Chunk 7 T-Z Research Report

This report follows the README-driven, documentation-oriented format. I stayed conservative: when syntax was not clearly verified from the assignment sources or stable language docs, I marked it unresolved rather than guessing.

## Talon
- Registry key: `talon`
- Version scope: `Talon 0.4-era .talon customization files; current Talon Community Wiki .talon-file page reviewed.`
- Version-specific syntax: `No version split confirmed. .talon comments use # and must be on their own line; this is not a general inline marker.`
- Line comments: `# on its own line`
- Block comments: `unsupported`
- Termination behavior: `line comment ends at the physical line break; block comments unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://talon.wiki/Customization/talon-files/; https://talonvoice.com/docs/`
- Implementation source: `unresolved`
- Community source: `https://talon.wiki/Customization/talon-files/`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed whole-line # comment coverage only; avoid treating inline # as a comment unless a future grammar source confirms it.`
- Notes: `The Talon wiki explicitly says comments start with # and must always be on their own line.`

### Examples

#### Line comment
```talon
# This context applies on Linux.
os: linux
-
# This action runs in the body.
hello talon: app.notify("hello")
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `unresolved; search results did not identify a single stable Tea language/dialect for the Stack v2 registry key.`
- Version-specific syntax: `unresolved; the name collides with unrelated projects and no authoritative comment-syntax page was found.`
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
- Notes: `Do not seed comment syntax until the intended Tea dialect is identified from corpus metadata or a registry owner.`

### Examples

#### Line comment
```text
unresolved
```

#### Block comment
```text
unresolved
```

#### Nested comment
```text
unresolved
```

## Terra
- Registry key: `terra`
- Version scope: `Terra current public docs; Terra is documented as embedded in and meta-programmed by Lua. Lua 5.4 lexical-comment rules used for the comment forms.`
- Version-specific syntax: `No Terra-specific split confirmed. Use Lua comments: -- line comments and --[=*[ ... ]=*] long comments. Depth-qualified long brackets let a block contain lower-depth long-comment delimiters, but plain --[[ ... ]] closes at the first matching ]] delimiter.`
- Line comments: `--`
- Block comments: `--[[ ... ]]` and depth-qualified forms such as `--[=[ ... ]=]`
- Termination behavior: `line comments end at line break; long comments end at the matching long-bracket close with the same equals-sign depth`
- Nested comments: `depth-qualified long-bracket containment only; not arbitrary same-depth nesting`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://terralang.org/; https://www.lua.org/manual/5.4/manual.html#3.1`
- Implementation source: `unresolved`
- Community source: `https://www.lua.org/pil/1.3.html`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed Lua-style line and long-comment coverage, including depth-qualified long-bracket examples.`
- Notes: `Terra docs show top-level code as Lua and describe Terra as embedded in Lua, so Lua lexical comments are the relevant syntax for .t files.`

### Examples

#### Line comment
```terra
local x = 1
-- comment
local y = 2
```

#### Block comment
```terra
local x = 1
--[[ comment ]]
local y = 2
```

#### Nested comment
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
- Version scope: `GNU Texinfo 7.3 current manual, cross-checked against older GNU Texinfo comment documentation.`
- Version-specific syntax: `No version split confirmed. Texinfo supports @comment and its @c abbreviation for source-line comments, plus @ignore ... @end ignore for ignored regions used as long comments.`
- Line comments: `@c` and `@comment`
- Block comments: `@ignore ... @end ignore`
- Termination behavior: `@c/@comment comments end at the physical line break; @ignore regions end at the next @end ignore command on its own line`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://www.gnu.org/software/texinfo/manual/texinfo/html_node/Comments.html; https://ftp.gnu.org/old-gnu/Manuals/texinfo-4.2/html_node/Comments.html`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed @c, @comment, and @ignore/@end ignore coverage; keep nesting unsupported.`
- Notes: `The manual says @ignore and @end ignore should each appear at the beginning of their own line. Ignored text is still parsed enough to find the matching end command.`

### Examples

#### Line comment
```texinfo
@node Top
@c comment
@top Example
```

#### Block comment
```texinfo
@ignore
comment
@end ignore
@node Top
```

#### Nested comment
```text
unsupported
```

## Text
- Registry key: `text`
- Version scope: `IANA text/plain registration and MIME text/plain family; no language grammar layer.`
- Version-specific syntax: `No comment syntax is defined for plain text.`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `not applicable`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://www.iana.org/assignments/media-types/; https://datatracker.ietf.org/doc/html/rfc2646`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Document as commentless.`
- Notes: `Plain text preserves the input characters as content; any comment convention would be application-specific, not part of the format.`

### Examples

#### Line comment
```text
unsupported
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

## Textile
- Registry key: `textile`
- Version scope: `Textile Markup Language documentation, Textile 2-era block syntax.`
- Version-specific syntax: `No version split confirmed. Textile has paragraph-style comments starting with ###. and extended comments starting with ###..; Textile can also pass through HTML comments.`
- Line comments: `unsupported`
- Block comments: `###. comment paragraph`, `###.. multi-paragraph comment ... p. normal paragraph`, and HTML `<!-- ... -->`
- Termination behavior: `###. comments remove one Textile block; ###.. comments continue until another block signature such as p.; HTML comments end at the first -->`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://textile-lang.com/doc/textile-comments`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed Textile block-comment coverage for ###. and ###..; treat HTML comments as a secondary markup form if the parser supports embedded HTML.`
- Notes: `Textile comments are block-level markup, not arbitrary inline line comments. Multi-paragraph comments require a following explicit block marker to resume rendered content.`

### Examples

#### Line comment
```text
unsupported
```

#### Block comment
```textile
Some text here.

###. This is a Textile comment block.
It will be removed from output.

More text to follow.
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `IANA text/tab-separated-values registration.`
- Version-specific syntax: `No comment syntax is defined for the registered TSV media type.`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `not applicable`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://www.iana.org/assignments/media-types/text/tab-separated-values`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Document as commentless unless a dialect extension exists.`
- Notes: `The registered format describes records as lines and fields as tab-separated text; treating #, ;, or other prefixes as comments would be dialect-specific.`

### Examples

#### Line comment
```text
unsupported
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `Turing language as described in the ACM language paper and Open Turing-era compatible implementations.`
- Version-specific syntax: `No version split confirmed for comments. Turing supports % line comments and /* ... */ block comments.`
- Line comments: `%`
- Block comments: `/* ... */`
- Termination behavior: `% comments end at line break; block comments end at the first */`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: `https://dl.acm.org/doi/pdf/10.1145/53580.53581`
- Implementation source: `unresolved`
- Community source: `https://en.wikipedia.org/wiki/Turing_(programming_language); https://tristan.hume.ca/openturing/`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed % line comments and /* ... */ non-nested block comments; keep confidence medium until an official manual or lexer source is archived with the report.`
- Notes: `The ACM paper snippet explicitly describes both forms. Community examples also show % comments in ordinary Turing code.`

### Examples

#### Line comment
```turing
put "hello"
% comment
put "world"
```

#### Block comment
```turing
put "hello"
/* comment */
put "world"
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `TXL programming language reference/cookbook sources for modern TXL.`
- Version-specific syntax: `No version split confirmed. TXL source comments begin with % and continue to the end of line.`
- Line comments: `%`
- Block comments: `unsupported`
- Termination behavior: `% comments end at line break`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: `https://txl.ca/; https://queensu.scholaris.ca/bitstreams/740d54b6-94f6-4f8d-bd12-6e2b717b452e/download`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed percent line-comment coverage only.`
- Notes: `TXL can parse and preserve comments in target input languages via grammars, but TXL program-source comments are percent-to-EOL.`

### Examples

#### Line comment
```txl
% Syntax specification
define program
    [repeat number]
end define
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

## Type Language
- Registry key: `type_language`
- Version scope: `Telegram TL / TON TL-B Type Language family; TON TL-B syntax page explicitly reviewed for comment forms.`
- Version-specific syntax: `TL/TL-B schemas use C++-style comments: // line comments and /* ... */ block comments.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `// comments end at line break; block comments end at the first */`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://core.telegram.org/mtproto/TL; https://docs.ton.org/blockchain-basics/languages/tl-b/syntax-and-semantics`
- Implementation source: `unresolved`
- Community source: `https://docs.telethon.dev/en/stable/developing/understanding-the-type-language.html`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed C++-style // and /* ... */ coverage, but label the entry as Telegram/TON Type Language if the registry can disambiguate the broad name.`
- Notes: `The TON TL-B documentation states that comments follow C++ conventions. Telegram TL docs establish the Type Language context but are less explicit about comments.`

### Examples

#### Line comment
```tl
// comment
user id:int name:string = User;
```

#### Block comment
```tl
/* comment */
user id:int name:string = User;
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `Unity text serialized scene/asset files documented as UnityYAML; current Unity 6000.4 manual checked with YAML syntax rules.`
- Version-specific syntax: `Unity text serialization is YAML-like/YAML 1.1. Comments use YAML # line comments; YAML does not define block comments.`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `# comments end at line break`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://docs.unity3d.com/6000.4/Documentation/Manual/TextSceneFormat.html; https://docs.unity3d.com/6000.4/Documentation/Manual/YAMLSceneExample.html; https://yaml.org/spec/1.2.2/`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed YAML-style # line comments only.`
- Notes: `Unity serialized files contain Unity-specific tags and directives, but comments are inherited from the YAML text layer.`

### Examples

#### Line comment
```text
%YAML 1.1
# comment
--- !u!1 &1
GameObject:
  m_Name: Example
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

## Unix Assembly
- Registry key: `unix_assembly`
- Version scope: `GNU as / Unix assembler family, with x86 GAS examples; GNU as target-specific line comment characters reviewed.`
- Version-specific syntax: `GNU as supports /* ... */ block comments across targets; line comment characters are target-specific. On i386/x86-64 GAS the line comment character is #.`
- Line comments: `target-specific; # for i386/x86-64 GNU as`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at line break; block comments end at the first */`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: `https://sourceware.org/binutils/docs-2.17/as/Comments.html`
- Implementation source: `unresolved`
- Community source: `https://en.wikibooks.org/wiki/X86_Assembly/Comments`
- Corpus fallback source: `unresolved`
- Recommended action: `Do not seed a single universal line-comment marker without corpus architecture metadata; if scoped to GAS/x86, seed # plus /* ... */.`
- Notes: `The GNU assembler manual states that the line comment character is target-specific. Treat the registry key as dialect-sensitive unless Stack v2 metadata scopes it further.`

### Examples

#### Line comment
```asm
movl $1, %eax
# comment for GNU as on x86
ret
```

#### Block comment
```asm
movl $1, %eax
/* comment */
ret
```

#### Nested comment
```text
unsupported
```

## Uno
- Registry key: `uno`
- Version scope: `Fuse Open Uno language reference; Uno described as a dialect of C# with mostly identical syntax.`
- Version-specific syntax: `No Uno-specific comment split confirmed. Use C# lexical comment forms: // line comments and /* ... */ block comments.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://fuseopen.com/docs/uno/uno-lang.html; https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/tokens/comments`
- Implementation source: `unresolved`
- Community source: `https://github.com/fuse-open/uno`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed C#-style line and block comment coverage.`
- Notes: `Uno documentation describes the language as a C# dialect and says syntax is mostly identical to C# aside from documented deviations.`

### Examples

#### Line comment
```uno
namespace Example
{
    // comment
    public class Program {}
}
```

#### Block comment
```uno
namespace Example
{
    /* comment */
    public class Program {}
}
```

#### Nested comment
```text
unsupported
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
- Version scope: `Ur/Web public manual.`
- Version-specific syntax: `No version split confirmed. Ur/Web comments begin with (* and end with *), and comments nest.`
- Line comments: `unsupported`
- Block comments: `(* ... *)`
- Termination behavior: `balanced nested block comments; outer comment ends after matching final *)`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://enn.github.io/urweb-doc/manual.html`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed nested (* ... *) block-comment coverage and keep line comments unsupported.`
- Notes: `The manual explicitly states that comments nest.`

### Examples

#### Line comment
```text
unsupported
```

#### Block comment
```urweb
val x = 1
(* comment *)
val y = 2
```

#### Nested comment
```urweb
val x = 1
(* outer (* inner *) outer *)
val y = 2
```

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
- Version scope: `Valve KeyValues / VDF text format as documented by Valve Developer Community and checked against common parser implementations.`
- Version-specific syntax: `No versioned grammar split confirmed. Text VDF/KeyValues commonly uses // line comments; block comments are not consistently documented for the format.`
- Line comments: `//`
- Block comments: `unsupported`
- Termination behavior: `// comments end at line break`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `implementation_cross_checked`
- Docs source: `https://developer.valvesoftware.com/wiki/VDF; https://developer.valvesoftware.com/wiki/KeyValues`
- Implementation source: `https://github.com/ValvePython/vdf`
- Community source: `https://pkg.go.dev/github.com/benlubar/vdf`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed // line comments only; leave block comments unsupported unless a target parser explicitly accepts them.`
- Notes: `Some parsers are permissive around slash-prefixed lines, but // is the portable VDF/KeyValues comment form to test.`

### Examples

#### Line comment
```text
"root"
{
    // comment
    "key" "value"
}
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
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
- Version scope: `Varnish Configuration Language (VCL), Varnish/Fastly-derived syntax; current Varnish docs and Varnish developer tutorial reviewed.`
- Version-specific syntax: `No version split confirmed for comment forms. VCL supports // and # line comments, plus /* ... */ block comments.`
- Line comments: `//` and `#`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at line break; block comments end at the first */`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://varnish-cache.readthedocs.io/reference/vcl.html; https://www.varnish-software.com/developers/tutorials/varnish-configuration-language-vcl/`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed Varnish VCL //, #, and /* ... */ coverage; avoid applying this result to other VCL acronyms without a separate registry key.`
- Notes: `VCL is ambiguous, but Stack language keys typically mean Varnish Configuration Language for this name.`

### Examples

#### Line comment
```vcl
sub vcl_recv {
    // comment
    # another comment
}
```

#### Block comment
```vcl
sub vcl_recv {
    /* comment */
}
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `Vim help file documentation/markup as shipped with Vim help and help syntax highlighting.`
- Version-specific syntax: `No formal source-comment syntax identified for Vim help files. Vim help is documentation markup; Vimscript " comments do not apply to help text.`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `not applicable`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `implementation_cross_checked`
- Docs source: `https://vimhelp.org/helphelp.txt.html`
- Implementation source: `https://raw.githubusercontent.com/vim/vim/master/runtime/syntax/help.vim`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Do not seed comment syntax for vim-help files; keep Vimscript comments scoped to the vim_script key.`
- Notes: `Help files can contain examples and modelines, but those are content/markup rather than ignored help-file comments.`

### Examples

#### Line comment
```text
unsupported
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `Vim snippet file dialects, especially snipMate and UltiSnips-style .snippets files.`
- Version-specific syntax: `Dialect-specific. snipMate documents # comments as whole lines outside snippet definitions; UltiSnips also uses # comment/header lines. # inside a snippet body may be literal snippet text.`
- Line comments: `# whole-line comments outside snippet bodies`
- Block comments: `unsupported`
- Termination behavior: `# comments end at line break; comment recognition depends on being outside a snippet body for snipMate`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: `https://github.com/garbas/vim-snipmate/blob/master/doc/SnipMate.txt; https://github.com/SirVer/ultisnips/blob/master/doc/UltiSnips.txt`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed # whole-line comments only if the parser can distinguish snippet headers/outside-body lines; otherwise split by snippet dialect.`
- Notes: `snipMate explicitly warns that # lines inside snippet definitions are not comments.`

### Examples

#### Line comment
```snippets
# comment outside a snippet definition
snippet log
console.log(${1:value})
endsnippet
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `Phalcon Volt template engine docs, Phalcon 3.4 through 5.11.`
- Version-specific syntax: `No version split confirmed. Volt comments use {# ... #} template-comment delimiters.`
- Line comments: `unsupported`
- Block comments: `{# ... #}`
- Termination behavior: `block comments end at the first #}`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://docs.phalcon.io/5.11/volt/; https://docs.phalcon.io/3.4/volt/`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed {# ... #} template-comment coverage and keep line comments unsupported.`
- Notes: `Volt comments may span multiple lines and the text is ignored in final output.`

### Examples

#### Line comment
```text
unsupported
```

#### Block comment
```volt
{# comment #}
{{ name }}
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `OWL 2 Web Ontology Language; W3C document overview and common concrete syntaxes reviewed.`
- Version-specific syntax: `OWL is not a single concrete surface syntax. RDF/XML uses XML comments, Turtle serialization uses # line comments, and Manchester/XML syntaxes have their own lexical layers.`
- Line comments: `serialization-dependent; # in Turtle`
- Block comments: `serialization-dependent; <!-- ... --> in RDF/XML/XML serialization`
- Termination behavior: `Turtle # comments end at line break; XML comments end at the first -->`
- Nested comments: `unsupported for Turtle/XML comment forms`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://www.w3.org/TR/owl2-overview/; https://www.w3.org/TR/turtle/; https://www.w3.org/TR/rdf-syntax-grammar/; https://www.w3.org/TR/owl2-manchester-syntax/`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Do not seed a generic OWL syntax unless corpus serialization is known; prefer serialization-specific keys or fixtures.`
- Notes: `The W3C overview states that OWL 2 has multiple concrete syntaxes, with RDF/XML as the primary exchange syntax and Turtle/Manchester as alternatives.`

### Examples

#### Line comment
```turtle
@prefix ex: <http://example.com/> .
# Turtle serialization comment
ex:s a ex:Class .
```

#### Block comment
```xml
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <!-- RDF/XML serialization comment -->
</rdf:RDF>
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `W3C WebVTT 1 Recommendation.`
- Version-specific syntax: `No version split confirmed. WebVTT comments are NOTE blocks, not prefix line comments.`
- Line comments: `unsupported`
- Block comments: `NOTE ... blank line`
- Termination behavior: `first blank line wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://www.w3.org/TR/webvtt1/`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Treat NOTE blocks as WebVTT comments and add parser tests for blank-line termination.`
- Notes: `A NOTE block may contain multiple lines, but a blank line terminates the block and returns parsing to cues or other data blocks.`

### Examples

#### Line comment
```text
unsupported
```

#### Block comment
```webvtt
WEBVTT

NOTE comment

00:00.000 --> 00:01.000
Hello
```

#### Nested comment
```text
unsupported
```

## Whiley
- Registry key: `whiley`
- Version scope: `Whiley Language Specification PDF for current 0.6-era language documentation.`
- Version-specific syntax: `No version split confirmed in the reviewed spec. Whiley supports // line comments and /* ... */ block comments.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://whiley.org/pdfs/WhileyLanguageSpec.pdf`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed // and /* ... */ coverage; keep nested blocks unsupported.`
- Notes: `The specification lists line comments and block comments in section 2.3.`

### Examples

#### Line comment
```whiley
// comment
function f() -> int:
    return 1
```

#### Block comment
```whiley
/* comment */
function f() -> int:
    return 1
```

#### Nested comment
```text
unsupported
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
- Version scope: `Microsoft Message Compiler .mc message text files.`
- Version-specific syntax: `No version split confirmed. Message text file comments are semicolon-prefixed lines.`
- Line comments: `;`
- Block comments: `unsupported`
- Termination behavior: `; comments end at line break`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://learn.microsoft.com/en-us/windows/win32/wes/message-compiler--mc-exe-; https://learn.microsoft.com/en-us/windows/win32/eventlog/message-files`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `https://github.com/MicrosoftDocs/win32/blob/docs/desktop-src/EventLog/sample-message-text-file.md`
- Recommended action: `Seed semicolon line-comment coverage only.`
- Notes: `Microsoft sample message files begin comments with ;, including header-comment lines in .mc files.`

### Examples

#### Line comment
```text
; comment
MessageId=1
Severity=Informational
Facility=Application
SymbolicName=MSG_EXAMPLE
Language=English
Example message.
.
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
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
- Version scope: `The Witcher 3 REDkit Witcher Script / WS Language Guide.`
- Version-specific syntax: `No version split confirmed. Witcher Script supports // single-line comments and /* ... */ multi-line comments.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://cdprojektred.atlassian.net/wiki/spaces/W3REDkit/pages/36307090/WS+Language+Guide`
- Implementation source: `unresolved`
- Community source: `https://witcherscript.readthedocs.io/en/latest/basics.html`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed // and /* ... */ coverage; keep nested blocks unsupported.`
- Notes: `The official REDkit language guide includes a comments section with single-line and multi-line examples.`

### Examples

#### Line comment
```witcherscript
// comment
function main() {
}
```

#### Block comment
```witcherscript
/* comment */
function main() {
}
```

#### Nested comment
```text
unsupported
```

## Wollok
- Registry key: `wollok`
- Version scope: `Current Wollok language documentation.`
- Version-specific syntax: `No version split confirmed. Wollok supports // single-line comments, /* ... */ multi-line comments, and /** ... */ Wollok-doc comments.`
- Line comments: `//`
- Block comments: `/* ... */` and documentation `/** ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://www.wollok.org/en/documentation/introduction/`
- Implementation source: `unresolved`
- Community source: `https://github.com/uqbar-project/wollok-language`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed //, /* ... */, and optionally /** ... */ doc-comment fixtures as the same block-comment family.`
- Notes: `The official introduction lists all three comment types explicitly.`

### Examples

#### Line comment
```wollok
// comment
object Example {
}
```

#### Block comment
```wollok
/* comment */
object Example {
}
```

#### Nested comment
```text
unsupported
```

## World of Warcraft Addon Data
- Registry key: `world_of_warcraft_addon_data`
- Version scope: `World of Warcraft addon .toc metadata files, current community-maintained TOC format documentation.`
- Version-specific syntax: `This key is addon TOC data, not Lua source. TOC comments use # at the start of the line; leading whitespace before # makes the line a filename, not a comment.`
- Line comments: `# at column 1 / start of line`
- Block comments: `unsupported`
- Termination behavior: `# comments end at line break`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://warcraft.wiki.gg/wiki/TOC_format`
- Implementation source: `unresolved`
- Community source: `https://addonstudio.org/wiki/WoW:TOC_format`
- Corpus fallback source: `unresolved`
- Recommended action: `Replace Lua-style assumptions with TOC # line-comment coverage for this registry key; keep Lua parsing under Lua source keys.`
- Notes: `The TOC format distinguishes comments, metadata tags, file paths, and blank lines. Indented # is not portable as a comment.`

### Examples

#### Line comment
```toc
## Interface: 110200
# comment
MyAddon.lua
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

## Wren
- Registry key: `wren`
- Version scope: `Current Wren language syntax documentation and compiler source.`
- Version-specific syntax: `No version split confirmed. Wren supports // line comments and /* ... */ block comments; unlike C, block comments can nest.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `// comments end at line break; block comments use balanced nesting and end when nesting depth returns to zero`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: `https://wren.io/syntax.html`
- Implementation source: `https://raw.githubusercontent.com/wren-lang/wren/main/src/vm/wren_compiler.c`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line, block, and nested block-comment coverage.`
- Notes: `The public syntax page explicitly says block comments can nest, and the compiler source uses a nesting counter.`

### Examples

#### Line comment
```wren
// comment
class Example {}
```

#### Block comment
```wren
/* comment */
class Example {}
```

#### Nested comment
```wren
/* outer /* inner */ outer */
class Example {}
```

## X BitMap
- Registry key: `x_bit_map`
- Version scope: `XBM / X BitMap files represented as C source arrays, per X11-era file format references.`
- Version-specific syntax: `XBM is stored as C source text. Historical XBM examples are C89-like, so /* ... */ block comments are portable; // line comments depend on accepting a modern C/C++ carrier dialect.`
- Line comments: `carrier-dialect dependent; // only in modern C/C++ interpretations`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at line break where accepted; block comments end at the first */`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: `https://www.x.org/archive/X11R7.6/doc/man/man1/bitmap.1.xhtml`
- Implementation source: `unresolved`
- Community source: `https://www.fileformat.info/format/xbm/egff.htm`
- Corpus fallback source: `https://en.wikipedia.org/wiki/X_BitMap`
- Recommended action: `Seed /* ... */ only for portable XBM; consider // only if the parser intentionally treats XBM as modern C source.`
- Notes: `Do not treat #define lines as comments; they are part of the C-source representation.`

### Examples

#### Line comment
```c
// dialect-dependent in modern C-style XBM
#define sample_width 8
```

#### Block comment
```c
/* XBM comment */
#define sample_width 8
static unsigned char sample_bits[] = { 0x00 };
```

#### Nested comment
```text
unsupported
```

## X PixMap
- Registry key: `x_pix_map`
- Version scope: `XPM / X PixMap, especially XPM3 C-array representation used by libXpm.`
- Version-specific syntax: `XPM3 reintroduces a C wrapper around XPM data, so C block comments such as /* XPM */ are part of common files. XPM2 is a plain text variant and should not inherit arbitrary C comments.`
- Line comments: `carrier-dialect dependent; // only in modern C/C++ wrapped files`
- Block comments: `/* ... */ in C-style XPM/XPM3 files`
- Termination behavior: `line comments end at line break where accepted; block comments end at the first */`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `implementation_cross_checked`
- Docs source: `https://www.x.org/releases/current/doc/libXpm/libXpm.html`
- Implementation source: `unresolved`
- Community source: `https://gitlab.freedesktop.org/xorg/lib/libxpm; https://en.wikipedia.org/wiki/X_PixMap`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed /* ... */ for XPM3/C-style XPM; avoid applying C comments to XPM2/plain-text data without format detection.`
- Notes: `The common magic header is itself a C block comment, /* XPM */.`

### Examples

#### Line comment
```c
// dialect-dependent in modern C-style XPM
static char *sample_xpm[] = {
};
```

#### Block comment
```c
/* XPM */
static char *sample_xpm[] = {
"1 1 1 1",
". c #000000",
"."
};
```

#### Nested comment
```text
unsupported
```

## X10
- Registry key: `x10`
- Version scope: `X10 programming language 2.x, official x10-lang documentation and compiler repository examples.`
- Version-specific syntax: `No version split confirmed. X10 is Java-like and public X10 examples/compiler source use //, /* ... */, and /** ... */ comments.`
- Line comments: `//`
- Block comments: `/* ... */` and documentation `/** ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `implementation_cross_checked`
- Docs source: `https://x10-lang.org/; https://github.com/x10-lang/x10-documentation`
- Implementation source: `https://raw.githubusercontent.com/x10-lang/x10/master/x10.compiler/src/x10/parser/X10Lexer.java`
- Community source: `https://en.wikipedia.org/wiki/X10_(programming_language)`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed Java/C-style line and block coverage, including docblock-as-block-comment cases.`
- Notes: `The public X10 example corpus uses Java-style // and /** ... */ comments; no nested block behavior was found.`

### Examples

#### Line comment
```x10
// comment
class Example {}
```

#### Block comment
```x10
/* comment */
class Example {}
```

#### Nested comment
```text
unsupported
```

## xBase
- Registry key: `xbase`
- Version scope: `Broad xBase/Clipper family, with Harbour used as the concrete open implementation reference.`
- Version-specific syntax: `Dialect-dependent. Harbour/Clipper-compatible sources support // and && to end of line, * as a full-line comment when it is the first token, NOTE/NOTE* statement comments, and /* ... */ stream comments.`
- Line comments: `//`, `&&`, `*` at beginning of a statement line, and `NOTE`/`NOTE*` statement comments`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at line break; block comments end at the first */`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `implementation_cross_checked`
- Docs source: `https://harbour.github.io/doc/harbour.html`
- Implementation source: `https://raw.githubusercontent.com/harbour/core/master/src/pp/ppcore.c`
- Community source: `https://troubleshooters.com/codecorn/harbour/harbour_intro.htm`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed a broad xBase union only if the registry key intentionally spans dialects; otherwise split Harbour/Clipper/FoxPro variants.`
- Notes: `Harbour source explicitly strips // and && rest-of-line comments, handles * line comments, recognizes NOTE, and reports unterminated /* */ comments.`

### Examples

#### Line comment
```xbase
* full-line comment
? "hello" && inline comment
// Harbour comment
NOTE statement comment
```

#### Block comment
```xbase
/* block comment */
? "done"
```

#### Nested comment
```text
unsupported
```

## XC
- Registry key: `xc`
- Version scope: `XMOS XC language as documented in XTC Tools programming guide; C-family syntax layer.`
- Version-specific syntax: `No XC-specific split confirmed. XC extends C, so C/C++ comment forms apply: // line comments and /* ... */ block comments.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: `https://www.xmos.com/documentation/XM-014363-PC/pdf/xtc_prog_guide_v15.3.pdf; https://www.xmos.com/documentation/XM-014363-PC/html/prog-guide/prog-ref/c-lang-ref/clangref.html`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed C/C++ line and block comment coverage.`
- Notes: `XMOS docs describe XC as a C-based language; no evidence of nested block comments was found.`

### Examples

#### Line comment
```xc
// comment
void main() {}
```

#### Block comment
```xc
/* comment */
void main() {}
```

#### Nested comment
```text
unsupported
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
- Version scope: `Current Xojo language documentation, API/language commenting page.`
- Version-specific syntax: `Current official docs list // and apostrophe (') comments. Older BASIC-style Rem was not confirmed in current docs and should be treated as legacy/unverified for this key.`
- Line comments: `//` and `'`
- Block comments: `unsupported`
- Termination behavior: `line comments end at line break`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://documentation.xojo.com/api/language/commenting.html`
- Implementation source: `unresolved`
- Community source: `https://blog.xojo.com/2022/04/05/using-the-new-user-code-assistants-feature/`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed // and apostrophe comments for current Xojo; do not seed Rem unless legacy corpus evidence requires it.`
- Notes: `The Xojo code editor can toggle comments and the current documentation says the compiler ignores comments entered with // or '.`

### Examples

#### Line comment
```xojo
// comment
Dim x As Integer
```

#### Line comment
```xojo
' comment
Dim x As Integer
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
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
- Version scope: `IBM/HCL Domino Designer XPages .xsp XML source layer.`
- Version-specific syntax: `XPages are XML documents interpreted by Domino/Notes. The source layer uses XML comments; embedded JavaScript or formula code has sublanguage-specific comments.`
- Line comments: `unsupported`
- Block comments: `<!-- ... -->`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://www.ibm.com/docs/en/domino-designer/8.5.3?topic=overview-understanding-xpages; https://www.w3.org/TR/xml/`
- Implementation source: `unresolved`
- Community source: `https://help.hcl-software.com/dom_designer/11.0.0/xpage_user_guide/builds/wpd_data_sources.html`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed XML comment coverage for .xsp/XPages files; handle embedded script comments only in sublanguage-aware parsing.`
- Notes: `IBM describes an XPage as XML interpreted by Domino or Notes. XML comments cannot nest.`

### Examples

#### Line comment
```text
unsupported
```

#### Block comment
```xml
<xp:view>
  <!-- comment -->
</xp:view>
```

#### Nested comment
```text
unsupported
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
- Version scope: `Perl XS language reference manual (perlxs), current and blead perldoc behavior.`
- Version-specific syntax: `XS comment lines start with # as the first non-whitespace character when not recognized as C preprocessor directives. C sections and embedded code can also use C comments.`
- Line comments: `# as first non-whitespace in XS sections`
- Block comments: `/* ... */ in C/code sections`
- Termination behavior: `# XS comments end at line break; C block comments end at the first */`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://perldoc.perl.org/perlxs; https://perldoc.perl.org/blead/perlxs`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed XS # comment lines with preprocessor-guard awareness; optionally seed C block comments only for code/C sections.`
- Notes: `perlxs warns to avoid confusing XS # comments with C preprocessor directives. Lines such as #include are not comments.`

### Examples

#### Line comment
```xs
MODULE = Example  PACKAGE = Example

  # XS comment line
void
hello()
```

#### Block comment
```xs
MODULE = Example  PACKAGE = Example

/* C block comment in embedded C/code context */
void
hello()
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `POSIX yacc and GNU Bison/Yacc-family grammars.`
- Version-specific syntax: `POSIX yacc specifies C-style /* ... */ comments. GNU Bison also accepts C++-style // comments, so line-comment support is dialect-specific.`
- Line comments: `dialect-specific; // in GNU Bison`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://pubs.opengroup.org/onlinepubs/9699919799/utilities/yacc.html; https://www.gnu.org/software/bison/manual/html_node/Comments.html`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed /* ... */ for portable yacc; include // only if the corpus/registry key covers GNU Bison.`
- Notes: `Bison treats comments as whitespace and permits them wherever whitespace is allowed, but POSIX yacc does not require // comments.`

### Examples

#### Line comment
```yacc
%token NUMBER
// comment
%%
```

#### Block comment
```yacc
%token NUMBER
/* comment */
%%
```

#### Nested comment
```text
unsupported
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
- Version scope: `YANG 1.1, RFC 7950; older YANG 1.0 RFC 6020 compatible for comment tokens.`
- Version-specific syntax: `No token split across YANG 1.0/1.1 found. YANG comments follow C++ style: // and /* ... */, outside quoted strings.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `// comments end at line break; block comments end at the nearest following */`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://www.rfc-editor.org/rfc/rfc7950.html#section-6.1.1; https://www.rfc-editor.org/rfc/rfc6020.html#section-6.1.1`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed // and /* ... */ coverage, with fixtures ensuring delimiters inside quoted strings are ignored.`
- Notes: `RFC 7950 says comments are syntactically equivalent to whitespace and must not occur within quoted strings.`

### Examples

#### Line comment
```yang
module example {
  // comment
  namespace "urn:example";
}
```

#### Block comment
```yang
module example {
  /* comment */
  namespace "urn:example";
}
```

#### Nested comment
```text
unsupported
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
- Version scope: `YASnippet snippet file format documented by the current project manual.`
- Version-specific syntax: `Snippet files use # directive/comment lines in the header before the # -- separator. After # --, text is snippet body content and # is literal unless handled by embedded snippet syntax.`
- Line comments: `# header/comment lines before # --`
- Block comments: `unsupported`
- Termination behavior: `# header comments end at line break; # -- terminates the header area rather than acting as a comment`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://joaotavora.github.io/yasnippet/snippet-development.html`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed # header/comment coverage only when the parser can detect the header/body boundary.`
- Notes: `The manual describes the first line not beginning with # as the beginning of the template, with # -- as an optional explicit separator.`

### Examples

#### Line comment
```snippet
# name: log
# key: log
# --
console.log($1)
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

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
- Version scope: `CraftTweaker ZenScript documentation for current and recent Minecraft versions.`
- Version-specific syntax: `No split confirmed across reviewed CraftTweaker docs. ZenScript supports // line comments, # line comments, and /* ... */ block comments.`
- Line comments: `//` and `#`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://docs.blamejared.com/1.20.1/en/tutorial/IntroductionToScripting/; https://docs.blamejared.com/1.12/en/Getting_Started/`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed //, #, and /* ... */ coverage; keep nested block comments unsupported.`
- Notes: `CraftTweaker docs show # comments commonly in examples and describe single-line and multi-line comments.`

### Examples

#### Line comment
```zenscript
// comment
# also a comment
val x = 1;
```

#### Block comment
```zenscript
/* comment */
val x = 1;
```

#### Nested comment
```text
unsupported
```

## Zephir
- Registry key: `zephir`
- Version scope: `Zephir 0.17 language documentation.`
- Version-specific syntax: `No version split confirmed. Zephir docs state C/C++-style comments: // line comments, /* ... */ multi-line comments, and docblocks.`
- Line comments: `//`
- Block comments: `/* ... */` and documentation `/** ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: `https://docs.zephir-lang.com/0.17/language/`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed // and /* ... */ coverage, with /** ... */ treated as the same block-comment family.`
- Notes: `The Zephir language guide explicitly lists single-line, multi-line, and documentation comments.`

### Examples

#### Line comment
```zephir
// comment
let x = 1;
```

#### Block comment
```zephir
/* comment */
let x = 1;
```

#### Nested comment
```text
unsupported
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
- Version scope: `ZIL/ZILF source as represented in the ZILF reference examples and VS Code grammar.`
- Version-specific syntax: `ZIL uses a semicolon prefix to comment the following expression; common source comments are written as ;"comment text". This is not a simple to-end-of-line comment marker.`
- Line comments: `;"..." as a common single string-comment expression; not plain semicolon-to-EOL`
- Block comments: `; before a following ZIL expression, which can span multiple lines if the expression spans`
- Termination behavior: `ends after the next complete commented expression; ;"..." ends at the string's closing quote`
- Nested comments: `structural expression nesting only; no separate nested comment delimiter`
- Confidence: `medium`
- Evidence mode: `implementation_cross_checked`
- Docs source: `https://github.com/heasm66/ZILF-Reference-Guide`
- Implementation source: `https://raw.githubusercontent.com/tclem/vscode-zil-language/master/grammars/zil.cson`
- Community source: `unresolved`
- Corpus fallback source: `https://raw.githubusercontent.com/heasm66/ZILF-Reference-Guide/master/Examples/FlowControl.zil`
- Recommended action: `Do not implement ZIL as semicolon-to-EOL. Either support ;"..." string comments conservatively or use a ZIL expression parser for semicolon-prefix comments.`
- Notes: `The editor grammar names semicolon comments as comment.block.zil and includes unstyled expressions inside the comment scope; corpus examples overwhelmingly use ;"..." trailing and standalone comments.`

### Examples

#### Line comment
```zil
;"A standalone comment string"
<ROUTINE GO () <TELL "hi">>
```

#### Block comment
```zil
<SETG X 0> ;"initialize global"
<ROUTINE GO () <TELL "hi">>
```

#### Nested comment
```text
unsupported as a separate delimiter; expression nesting is parser-dependent
```

## Zimpl
- Registry key: `zimpl`
- Version scope: `SCIP/Zimpl current repository examples and Zimpl language manual family.`
- Version-specific syntax: `No version split confirmed. Zimpl source files use # line comments. No block-comment syntax was found.`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `# comments end at line break`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `corpus_inferred`
- Docs source: `https://zimpl.zib.de/; https://scipopt.org/doc/html/ZIMPL.php`
- Implementation source: `https://raw.githubusercontent.com/scipopt/zimpl/master/src/zimpl/mmlscan.l`
- Community source: `unresolved`
- Corpus fallback source: `https://raw.githubusercontent.com/scipopt/zimpl/master/check/condit.zpl; https://raw.githubusercontent.com/scipopt/zimpl/master/example/tsp.zpl`
- Recommended action: `Seed hash-comment tests.`
- Notes: `The public Zimpl examples use # and #* banner lines as line comments. The scanner also has a COMMENT token for the keyword "comment", which is not the source-comment marker.`

### Examples

#### Line comment
```zimpl
# comment
set x := 1;
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```
