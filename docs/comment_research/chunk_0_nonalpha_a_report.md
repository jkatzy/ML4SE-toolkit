# Chunk 0 Research Report: Nonalpha / A

Scope: `chunk_0_nonalpha_a`

Method: official docs first, implementation/grammar source second, then registry suggestion.


## 1C Enterprise
- Registry key: `onec_enterprise`
- Line comments: `//`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://kb.1ci.com/1C_Enterprise_Platform/Guides/Developer_Guides/1C_Enterprise_8.3.23_Developer_Guide/Chapter_4._1C_Enterprise_language/4.2._Format_of_module_source_text/4.2.4._Module_format/`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Official 1C docs explicitly describe `//` line comments.

### Examples

#### Line comment
```text
Procedure Main()
    Value = 1; // keep the next step explicit
EndProcedure
```

## 2-Dimensional Array
- Registry key: `two_dimensional_array`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: This looks like a corpus label rather than a source language; I could not find a defensible comment grammar.

### Examples
- unsupported or unresolved

## 4D
- Registry key: `four_d`
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://developer.4d.com/docs/code-editor/write-class-method`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: 4D docs say the language supports `//` single-line and `/* */` block comments.

### Examples

#### Line comment
```text
VAR($value; Integer)
$value:=1 // keep the next line explicit
```

#### Block comment
```text
VAR($value; Integer)
/*
keep the next line explicit
*/
$value:=1
```

## ABAP
- Registry key: `abap`
- Line comments: `"` and `*` in column 1
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://help.sap.com/doc/abapdocu_751_index_htm/7.51/en-US/abencomment.htm`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: ABAP supports full-line comments with `*` and inline/end-of-line comments with `"`.

### Examples

#### Line comment
```text
DATA lv_value TYPE i.
lv_value = 1. " keep the next statement explicit
WRITE lv_value.
```

## ActionScript
- Registry key: `actionscript`
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: `https://www.oreilly.com/library/view/actionscript-the-definitive/1565928520/ch14s03.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: I found only secondary documentation in accessible search results, but the syntax is stable and matches common ECMAScript-style comments.

### Examples

#### Line comment
```text
var value:int = 1; // keep the next line explicit
trace(value);
```

#### Block comment
```text
var value:int = 1;
/* keep the next line explicit */
trace(value);
```

## Adobe Font Metrics
- Registry key: `adobe_font_metrics`
- Line comments: `Comment` records
- Block comments: unsupported
- Termination behavior: line records terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: `https://adobe-type-tools.github.io/font-tech-notes/pdfs/5004.AFM_Spec.pdf`
- Implementation source: `https://fonttools.readthedocs.io/en/stable/afmLib.html`
- Community source: `https://typolexikon.de/adobe-font-metrics-file/`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: AFM files are record-oriented text files. In practice, comment-like lines use the `Comment` record rather than a delimiter-based syntax.

### Examples

#### Line comment
```text
StartFontMetrics 4.1
Comment Copyright (c) 1989 Adobe Systems Incorporated. All Rights Reserved.
FontName AGaramondAlt-Regular
```

## AGS Script
- Registry key: `ags_script`
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://adventuregamestudio.github.io/ags-manual/ScriptingLanguage.html`
- Implementation source: `https://github.com/adventuregamestudio/ags`
- Community source: `https://adventuregamestudio.co.uk/forums/engine-development/inconsistency-in-the-ags-language/`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: The AGS manual shows `//` in script examples, and the compiler/highlighter ecosystem treats AGS script as C-like for comments.

### Examples

#### Line comment
```text
function game_start() {
    // keep the next action explicit
    Display("Hello, world");
}
```

#### Block comment
```text
function game_start() {
    /* keep the next action explicit */
    Display("Hello, world");
}
```

## AIDL
- Registry key: `aidl`
- Line comments: `//`
- Block comments: `/* */` and `/** */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://source.android.com/docs/core/architecture/aidl/aidl-language`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Android AIDL is Java-like and accepts Java-style comments; doc comments are also supported.

### Examples

#### Line comment
```text
parcelable Foo {
  int id; // keep the field explicit
}
```

#### Block comment
```text
/**
 * keep the interface documentation explicit
 */
interface IFoo {
  void ping();
}
```

## AL
- Registry key: `al`
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: `https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-programming-in-al`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: candidate
- Notes: I found the language reference, but the accessible page does not foreground comment syntax as clearly as other sources.

### Examples

#### Line comment
```text
procedure Main()
begin
    // keep the next statement explicit
    Message('Hello');
end;
```

#### Block comment
```text
procedure Main()
begin
    /* keep the next statement explicit */
    Message('Hello');
end;
```

## Alloy
- Registry key: `alloy`
- Line comments: `//` and `--`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://alloytools.org/tutorials/online/sidenote-format-comments.html`
- Implementation source: `GitHub Linguist languages.yml`
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Alloy documents three comment forms; `//` and `--` are both accepted as line comments.

### Examples

#### Line comment
```text
sig Person {}
// keep the next fact explicit
fact { some Person }
```

#### Block comment
```text
sig Person {}
/* keep the next fact explicit */
fact { some Person }
```

## Alpine Abuild
- Registry key: `alpine_abuild`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: `https://wiki.alpinelinux.org/wiki/Include:Abuild-configure`
- Implementation source: `GitHub Linguist languages.yml`
- Community source: `https://wiki.alpinelinux.org/wiki/APKBUILD_Reference`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Alpine abuild configuration and APKBUILD files are shell-like; hash comments are the stable comment form used in the ecosystem.

### Examples

#### Line comment
```text
pkgname=example
# keep the next setting explicit
pkgver=1.0
```

## Altium Designer
- Registry key: `altium_designer`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: `https://www.altium.com/documentation/altium-designer/document-commenting`
- Implementation source: unresolved
- Community source: `https://my.altium.com/altium-designer/getting-started/commenting-your-design`
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: The available Altium documentation is about design-review annotations and tasks, not source-language comment delimiters.

### Examples
- unsupported or unresolved

## AMPL
- Registry key: `ampl`
- Line comments: `#`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://dev.ampl.com/ampl/best-practices/style-guide.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: AMPL docs explicitly show `#` and `/*...*/` comments.

### Examples

#### Line comment
```text
param demand;
# keep the next declaration explicit
var x;
```

#### Block comment
```text
param demand;
/* keep the next declaration explicit */
var x;
```

## AngelScript
- Registry key: `angelscript`
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: `https://www.angelcode.com/angelscript/documentation.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: AngelScript is officially documented in the SDK manual; the common comment forms are C/C++-style.

### Examples

#### Line comment
```text
void main() {
  // keep the next call explicit
  Print("Hello");
}
```

#### Block comment
```text
void main() {
  /* keep the next call explicit */
  Print("Hello");
}
```

## Ant Build System
- Registry key: `ant_build_system`
- Line comments: unsupported
- Block comments: `<!-- -->`
- Termination behavior: block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://ant.apache.org/manual/using.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Ant build files are XML; XML comments are the relevant syntax.

### Examples

#### Block comment
```text
<project name="demo">
  <!-- keep the next target explicit -->
  <target name="build"/>
</project>
```

## Antlers
- Registry key: `antlers`
- Line comments: unsupported
- Block comments: `{{# ... #}}`
- Termination behavior: block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://statamic.dev/frontend/antlers`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Statamic’s Antlers docs show the comment delimiter form explicitly.

### Examples

#### Block comment
```text
{{ title }}
{{# keep the next section out of output #}}
{{ body }}
```

## ApacheConf
- Registry key: `apacheconf`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://httpd.apache.org/docs/current/en/configuring.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Apache HTTP Server config lines starting with `#` are comments.

### Examples

#### Line comment
```text
Listen 80
# keep the next directive explicit
ServerName example.test
```

## API Blueprint
- Registry key: `api_blueprint`
- Line comments: unsupported
- Block comments: `<!-- -->`
- Termination behavior: line comments unsupported; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: medium
- Evidence mode: implementation_cross_checked
- Docs source: `https://apiblueprint.org/documentation/specification.html`
- Implementation source: `https://github.com/apiaryio/drafter`
- Community source: `https://stackoverflow.com/questions/50613231/adding-plain-text-headers-in-api-blueprint`
- Corpus fallback source: unresolved
- Recommended action: candidate
- Notes: API Blueprint is Markdown/GFM-based; HTML comments are the defensible comment-like form here, but the spec does not define a dedicated comment grammar.

### Examples

#### Block comment
```text
FORMAT: 1A

# My API

<!-- keep the next resource group out of the rendered page -->
## Users [/users]
```

## APL
- Registry key: `apl`
- Line comments: `⍝`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://docs.dyalog.com/20.0/programming-reference-guide/defined-functions-and-operators/traditional-functions-and-operators/statements/`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Dyalog APL docs explicitly define comments as starting with `⍝`.

### Examples

#### Line comment
```text
value ← 1 ⍝ keep the next expression explicit
value ← value + 1
```

## Apollo Guidance Computer
- Registry key: `apollo_guidance_computer`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: candidate
- Evidence mode: corpus_inferred
- Docs source: `https://www.ibiblio.org/apollo/assembly_language_manual.html`
- Implementation source: `https://www.ibiblio.org/apollo/yaYUL.html`
- Community source: `https://stackoverflow.com/questions/62289017/how-does-this-apollo-guidance-computer-code-work-out-sine-and-cosine`
- Corpus fallback source: `https://www.ibiblio.org/apollo/listings/Sunburst120/ASSEMBLY_AND_OPERATION_INFORMATION.agc.html`
- Recommended action: candidate
- Notes: The corpus shows `#`-prefixed comments in AGC listings. I did not find a direct official syntax statement, so keep this tentative.

### Examples

#### Line comment
```text
SPCOS       AD  HALF        # ARGUMENTS SCALED AT PI
            TS  TEMK
```

## AppleScript
- Registry key: `applescript`
- Line comments: `--` and `#`
- Block comments: `(* *)`
- Termination behavior: line comments terminate at end-of-line; block comments support true nesting
- Nested comments: yes
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/conceptual/ASLR_lexical_conventions.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Apple’s language guide explicitly documents `--`, `#` (v2+), and nested block comments.

### Examples

#### Line comment
```text
set value to 1 -- keep the next statement explicit
display dialog "Hello"
```

#### Block comment
```text
(*
keep the next statement explicit
*)
set value to 1
```

#### Nested comment
```text
(* outer (* inner *) outer *)
set value to 1
```

## Arc
- Registry key: `arc`
- Line comments: `;`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: candidate
- Evidence mode: implementation_cross_checked
- Docs source: `https://www.paulgraham.com/arc.html`
- Implementation source: `GitHub Linguist languages.yml`
- Community source: `https://stackoverflow.com/questions/7838727/when-why-did-lisps-start-using-semicolons-for-comments`
- Corpus fallback source: unresolved
- Recommended action: candidate
- Notes: Arc is a Lisp dialect, and the semicolon line-comment form matches the family convention.

### Examples

#### Line comment
```text
(do
  ; keep the next form explicit
  (println "hello"))
```

## AsciiDoc
- Registry key: `asciidoc`
- Line comments: `//`
- Block comments: `////` or `[comment]--`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://docs.asciidoctor.org/asciidoc/latest/comments/`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: AsciiDoc has line comments and block comments; the docs also show the alternate `[comment]--` form.

### Examples

#### Line comment
```text
= Title

// keep the next paragraph explicit
Paragraph text.
```

#### Block comment
```text
= Title

////
keep the next paragraph explicit
////
Paragraph text.
```

## ASL
- Registry key: `asl`
- Line comments: unsupported
- Block comments: `/* */`
- Termination behavior: block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: `https://www.cs.columbia.edu/~sedwards/classes/2007/w4115-spring/lrms/ASL.pdf`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: candidate
- Notes: The accessible ASL manual says comments are all characters between `/*` and `*/`; the language name is ambiguous, so keep this low confidence.

### Examples

#### Block comment
```text
action main()
begin
  /* keep the next action explicit */
  x := 1;
end
```

## ASN.1
- Registry key: `asn1`
- Line comments: `-- ... --` or `-- ...`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://www.gnu.org/software/libtasn1/manual/html_node/ASN_002e1-syntax.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: GNU libtasn1’s syntax reference says comments begin with `--` and end with another `--` or end-of-line.

### Examples

#### Line comment
```text
MyModule DEFINITIONS ::= BEGIN
-- keep the next type explicit
INTEGER ::= INTEGER
END
```

## ASP.NET
- Registry key: `aspnet`
- Line comments: `//` in embedded C# / `'` in embedded VB
- Block comments: `@* *@` in Razor; `/* */` in embedded C#; `<!-- -->` in markup
- Termination behavior: line comments terminate at end-of-line; Razor comments terminate at the first closing `*@`; HTML comments terminate at the first closing `-->`
- Nested comments: no
- Confidence: candidate
- Evidence mode: official_docs
- Docs source: `https://learn.microsoft.com/en-us/aspnet/web-pages/overview/getting-started/introducing-razor-syntax-c`
- Implementation source: `GitHub Linguist languages.yml`
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: candidate
- Notes: ASP.NET is host-syntax dependent. This classification applies to Razor `.cshtml`/`.vbhtml` pages and their embedded code/markup, not to every ASP.NET file type.

### Examples

#### Line comment
```text
@{ 
    // keep the next line explicit
    var value = 1;
}
```

#### Block comment
```text
@* keep the next Razor block out of the rendered page *@
<p>Hello</p>
```

## AspectJ
- Registry key: `aspectj`
- Line comments: `//`
- Block comments: `/* */` and `/** */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: `https://eclipse.dev/aspectj/doc/latest/progguide/language.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: AspectJ inherits Java-style comments; use Java-like syntax in the registry.

### Examples

#### Line comment
```text
aspect Logging {
  // keep the next advice explicit
  before(): call(* *(..)) {}
}
```

#### Block comment
```text
/**
 * keep the aspect documentation explicit
 */
aspect Logging {
  before(): call(* *(..)) {}
}
```

## Astro
- Registry key: `astro`
- Line comments: `//` in frontmatter, `<!-- -->` in templates
- Block comments: `/* */` in frontmatter, `<!-- -->` in templates
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://docs.astro.build/en/basics/astro-components/`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Astro supports HTML comments in templates and JS-style comments in the frontmatter script.

### Examples

#### Line comment
```text
---
// keep the next import explicit
import Layout from '../layouts/Layout.astro';
---
<Layout />
```

#### Block comment
```text
<main>
  <!-- keep the next section explicit -->
  <p>Hello</p>
</main>
```

## Asymptote
- Registry key: `asymptote`
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: `https://asymptote.sourceforge.io/FAQ/section1.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: The official docs describe Asymptote as C++-like; comment syntax matches that family.

### Examples

#### Line comment
```text
real value = 1; // keep the next drawing explicit
draw((0,0)--(value,0));
```

#### Block comment
```text
real value = 1;
/* keep the next drawing explicit */
draw((0,0)--(value,0));
```

## ATS
- Registry key: `ats`
- Line comments: `//` and `////`
- Block comments: `(* *)`
- Termination behavior: line comments terminate at end-of-line; block comments support true nesting
- Nested comments: yes
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://ats-lang.sourceforge.net/htdocs-old/TUTORIAL/contents/tutorial_all.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: ATS supports line comments, rest-of-file comments, and nested enclosed comments.

### Examples

#### Line comment
```text
val x = 1 // keep the next value explicit
val y = x + 1
```

#### Block comment
```text
val x = 1
(*
keep the next value explicit
*)
val y = x + 1
```

#### Nested comment
```text
val x = 1
(* outer (* inner *) outer *)
val y = x + 1
```

## Augeas
- Registry key: `augeas`
- Line comments: unsupported
- Block comments: `(* *)`
- Termination behavior: block comments support true nesting
- Nested comments: yes
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://augeas.net/docs/language.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Augeas docs explicitly say comments are enclosed in `(*` and `*)` and can nest.

### Examples

#### Block comment
```text
let x = 1
(* keep the next lens explicit *)
let y = 2
```

#### Nested comment
```text
let x = 1
(* outer (* inner *) outer *)
let y = 2
```

## AutoHotkey
- Registry key: `autohotkey`
- Line comments: `;`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://documentation.help/AutoHotkey-en/Language.htm`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: AutoHotkey docs and the syntax reference page both confirm semicolon line comments and block comments.

### Examples

#### Line comment
```text
x := 1
; keep the next command explicit
MsgBox x
```

#### Block comment
```text
x := 1
/*
keep the next command explicit
*/
MsgBox x
```

## AutoIt
- Registry key: `autoit`
- Line comments: `;`
- Block comments: `#cs ... #ce`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://documentation.help/AutoIt/Script_File_Syntax.htm`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: AutoIt’s script syntax uses semicolon line comments and `#cs`/`#ce` block comments.

### Examples

#### Line comment
```text
Local $x = 1
; keep the next command explicit
MsgBox(0, "", $x)
```

#### Block comment
```text
Local $x = 1
#cs
keep the next command explicit
#ce
MsgBox(0, "", $x)
```

## Avro IDL
- Registry key: `avro_idl`
- Line comments: `//`
- Block comments: `/* */` and `/** */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://avro.apache.org/docs/1.12.0/idl-language/`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Avro IDL supports all Java-style comments, with `/**` used as documentation comments.

### Examples

#### Line comment
```text
protocol Hello {
  // keep the next record explicit
  record Ping { string value; }
}
```

#### Block comment
```text
protocol Hello {
  /**
   * keep the next record explicit
   */
  record Ping { string value; }
}
```

## Awk
- Registry key: `awk`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://www.gnu.org/software/gawk/manual/html_node/Comments.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: GNU awk comments start with `#` and continue to end-of-line.

### Examples

#### Line comment
```text
BEGIN {
  # keep the next action explicit
  print "hello"
}
```


## Summary

This chunk still contains unresolved or unsupported labels that should remain out of the registry until a defensible source is found.

Unresolved or unsupported languages: `2-Dimensional Array`, `Altium Designer`.
