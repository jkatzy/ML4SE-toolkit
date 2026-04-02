# Chunk 6 Research Report: Q to S

Scope: `chunk_6_q_s`

Method: official docs first, implementation/grammar source second, then registry suggestion.


## q
- Registry key: `q`
- Line comments: `/`
- Block comments: `/ ... \`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at the matching standalone `\`
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://code.kx.com/q4m3/10_Execution_Control/`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: q supports trailing `/` comments and multi-line block comments delimited by a line containing `/` and a line containing `\`.

### Examples

#### Line comment
```text
a:42 / keep the next assignment explicit
b:0
```

#### Block comment
```text
a:42
/
keep the next assignment explicit
\
b:0
```

## Q#
- Registry key: `qsharp`
- Line comments: //
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://learn.microsoft.com/en-us/azure/quantum/user-guide/language/programstructure/comments
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Q# supports line comments and documentation comments, but not block comments.

### Examples

#### Line comment
```text
operation Hello() : Unit {
    // keep the quantum call explicit
    Message("Hello");
}
```

## QMake
- Registry key: `qmake`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: https://doc.qt.io/qt-6/qmake-project-files.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Project files are line-oriented; use hash comments in .pro files.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## QML
- Registry key: `qml`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://doc.qt.io/qt-6.8/qtqml-syntax-basics.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: QML comments follow JavaScript syntax.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## Qt Script
- Registry key: `qt_script`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Qt Script is JavaScript-like; confirm against the exact Qt Script reference if you need higher confidence.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## Quake
- Registry key: `quake`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Likely C-like if this Stack label maps to QuakeC, but I did not find a direct authoritative source here.

### Examples
- unsupported or unresolved

## Racket
- Registry key: `racket`
- Line comments: ;
- Block comments: #| |#
- Termination behavior: line comments terminate at end-of-line; block comments support true nesting
- Nested comments: yes
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://docs.racket-lang.org/style/Choosing_the_Right_Construct.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Racket uses semicolon line comments plus nested #| |# block comments.

### Examples

#### Line comment
```text
(define x 1) ; keep the next form explicit
(define y 2)
```

#### Block comment
```text
#| keep the next form hidden |#
(define y 2)
```

#### Nested comment
```text
#| outer #| inner |# outer |#
(define y 2)
```

## Ragel
- Registry key: `ragel`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Ragel comment syntax depends on the exact embedded mode; I did not validate a defensible source.

### Examples
- unsupported or unresolved

## RAML
- Registry key: `raml`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: RAML inherits YAML-style hash comments.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## Rascal
- Registry key: `rascal`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Rascal is commonly treated as Java/C-like in syntax highlighters.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## Raw token data
- Registry key: `raw_token_data`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unresolved
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: This is not a language with a normal comment grammar.

### Examples
- unsupported or unresolved

## RDoc
- Registry key: `rdoc`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: RDoc is documentation-oriented; comment handling depends on the host language and parser mode.

### Examples
- unsupported or unresolved

## Readline Config
- Registry key: `readline_config`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.gnu.org/software/readline/manual/html_node/Readline-Init-File-Syntax.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Hash comments only.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## REALbasic
- Registry key: `realbasic`
- Line comments: `'`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: medium
- Evidence mode: implementation_cross_checked
- Docs source: `https://docs.xojo.com/api/language/introspection/constructorinfo.html`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: candidate
- Notes: Xojo/Realbasic examples in the online documentation show apostrophe comments in code blocks. I did not confirm a separate block-comment delimiter.

### Examples

#### Line comment
```text
Var value As Integer = 1 ' keep the next statement explicit
```

## Reason
- Registry key: `reason`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Reason follows OCaml/JavaScript-style comment forms in practice.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## Rebol
- Registry key: `rebol`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://www.rebol.com/r3/docs/guide/code-syntax.html`
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: The REBOL 3 guide explicitly documents semicolon line comments. I did not confirm a delimiter-based block comment form.

### Examples

#### Line comment
```text
x := 1
; keep the next step explicit
x := 2
```

## Red
- Registry key: `red`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Red keeps the Rebol semicolon comment form.

### Examples

#### Line comment
```text
x := 1
; keep the next step explicit
x := 2
```

## Redcode
- Registry key: `redcode`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Redcode comments are conventionally semicolon-based.

### Examples

#### Line comment
```text
x := 1
; keep the next step explicit
x := 2
```

## Redirect Rules
- Registry key: `redirect_rules`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Likely hash comments in rule/config files, but I did not verify the exact file family.

### Examples
- unsupported or unresolved

## Regular Expression
- Registry key: `regular_expression`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Regex comment syntax is flavor-dependent, so do not normalize this without a flavor-specific spec.

### Examples
- unsupported or unresolved

## Ren'Py
- Registry key: `renpy`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Ren'Py scripts follow Python-style hash comments.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## RenderScript
- Registry key: `renderscript`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: RenderScript is C-like for comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## ReScript
- Registry key: `rescript`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: ReScript uses JS/C-style comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## reStructuredText
- Registry key: `restructuredtext`
- Line comments: unsupported
- Block comments: ..
- Termination behavior: block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Comments are explicit markup blocks that begin with .. and an indented body.

### Examples

#### Block comment
```text
Heading
=======

.. keep the next paragraph hidden

Visible text.
```

## REXX
- Registry key: `rexx`
- Line comments: unsupported
- Block comments: `/* */`
- Termination behavior: block comments terminate at the matching `*/`
- Nested comments: yes
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://www.ibm.com/docs/en/cics-ts/5.6.0?topic=syntax-comments`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: IBM documents REXX comments as `/* ... */` and explicitly states that nested comments are allowed.

### Examples

#### Block comment
```text
/* keep the next statement explicit */
say 'Hello'
```

#### Nested comment
```text
/* outer /* inner */ outer */
say 'Hello'
```

## Rich Text Format
- Registry key: `rich_text_format`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unresolved
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: RTF is a document format; I did not confirm a stable comment syntax for this label.

### Examples
- unsupported or unresolved

## Ring
- Registry key: `ring`
- Line comments: # or //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://ring-lang.github.io/doc/getting_started.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Ring documents both # and // line comments, plus /* */ blocks.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

#### Block comment
```text
/*
Program Name : My first program using Ring
Author       : Ring Team
*/
see "What is your name?"
```

## RMarkdown
- Registry key: `rmarkdown`
- Line comments: unsupported
- Block comments: <!-- -->
- Termination behavior: block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: https://spec.commonmark.org/0.31.2/
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: RMarkdown comments are typically HTML comments embedded in Markdown.

### Examples

#### Block comment
```text
<root>
  <!-- keep the next element explicit -->
  <value>1</value>
</root>
```

## RobotFramework
- Registry key: `robotframework`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Robot Framework uses hash comments in test data files.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## robots.txt
- Registry key: `robots_txt`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://datatracker.ietf.org/doc/rfc9309/
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: robots.txt comments start with #.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## Roff
- Registry key: `roff`
- Line comments: \"
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://man7.org/linux/man-pages/man7/roff.7.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: The groff manual documents \" as the comment escape.

### Examples

#### Line comment
```text
.TH TEST 1
.\" keep the next request explicit
.SH NAME
```

## Roff Manpage
- Registry key: `roff_manpage`
- Line comments: \"
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://man7.org/linux/man-pages/man7/roff.7.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Manpage roff shares the same \" comment form.

### Examples

#### Line comment
```text
.TH TEST 1
.\" keep the next request explicit
.SH NAME
```

## Rouge
- Registry key: `rouge`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unresolved
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: Rouge is a highlighter, not a source language with a stable comment grammar.

### Examples
- unsupported or unresolved

## RPC
- Registry key: `rpc`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: RPC is ambiguous as a Stack label; I could not confirm a canonical comment syntax.

### Examples
- unsupported or unresolved

## RPGLE
- Registry key: `rpgle`
- Line comments: `//`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: medium
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: `GitHub Linguist languages.yml`
- Community source: `https://stackoverflow.com/questions/76369915/convert-a-ds-from-fixed-to-free-form-in-rpgle`
- Corpus fallback source: unresolved
- Recommended action: candidate
- Notes: The evidence I found is specific to free-form RPGLE, where `//` comments are used. I did not confirm a delimiter-based block comment form.

### Examples

#### Line comment
```text
dcl-s value int(10) inz(1);
// keep the next statement explicit
dsply value;
```

## RPM Spec
- Registry key: `rpm_spec`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: RPM spec files use hash comments and macro directives.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## Sage
- Registry key: `sage`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Sage code is Python-derived for comments.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## SaltStack
- Registry key: `saltstack`
- Line comments: #
- Block comments: {# #}
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Salt states use hash comments; templated files also accept Jinja {# #} comments.

### Examples

#### Line comment
```text
pkg_installed:
  pkg.installed:
    - name: vim
# keep the next state explicit
```

#### Block comment
```text
pkg_installed:
  pkg.installed:
    - name: vim
{# keep the next state hidden #}
```

## SAS
- Registry key: `sas`
- Line comments: * ... ;
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/a000289375.htm
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SAS supports *...; statement comments and /* */ block comments.

### Examples

#### Line comment
```text
data work.example;
  x = 1;
  * keep the next statement explicit;
  y = 2;
run;
```

#### Block comment
```text
data work.example;
  x = 1;
  /* keep the next statement explicit */
  y = 2;
run;
```

## Sass
- Registry key: `sass`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://sass-lang.com/documentation/syntax/comments/
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Sass and SCSS both support // and /* */; indented Sass treats block extent by indentation.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## SCSS
- Registry key: `scss`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://sass-lang.com/documentation/syntax/comments/
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SCSS comments are the same as Sass comments in SCSS mode.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## sed
- Registry key: `sed`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: GNU sed accepts hash comments in script files.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## Self
- Registry key: `self`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Self comment delimiters were not confirmed from a stable official source here.

### Examples
- unsupported or unresolved

## SELinux Policy
- Registry key: `selinux_policy`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Policy files are usually treated as C-like by tooling, but I did not confirm the exact grammar here.

### Examples
- unsupported or unresolved

## ShaderLab
- Registry key: `shaderlab`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: ShaderLab is treated as C-like by highlighters.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## Shell
- Registry key: `shell`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.gnu.org/s/bash/manual/html_node/Comments.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Shell comments begin with # in non-interactive or comment-enabled shells.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## Sieve
- Registry key: `sieve`
- Line comments: #
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.rfc-editor.org/rfc/rfc5228
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Sieve supports hash comments and bracketed /* */ comments; bracketed comments do not nest.

### Examples

#### Line comment
```text
if size :over 100K { # keep the next action explicit
    discard;
}
```

#### Block comment
```text
if size :over 100K { /* keep the next action explicit
  still comment */
    discard;
}
```

## Singularity
- Registry key: `singularity`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Singularity definition files use hash comments.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## Slash
- Registry key: `slash`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Slash is ambiguous; I did not validate its comment grammar.

### Examples
- unsupported or unresolved

## Slice
- Registry key: `slice`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Slice follows C++-style comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## Slim
- Registry key: `slim`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Slim comment delimiters vary by mode; confirm against the exact template syntax before adding support.

### Examples
- unsupported or unresolved

## Smali
- Registry key: `smali`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Smali comments are hash-prefixed.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## Smalltalk
- Registry key: `smalltalk`
- Line comments: "
- Block comments: "
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: https://www.gnu.org/software/smalltalk/manual/html_node/Syntax.html
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Smalltalk uses double quotes for comments.

### Examples

#### Line comment
```text
| value |
value := 1.
"keep the next message explicit"
value := value + 1.
```

#### Block comment
- unsupported or unresolved

## Smarty
- Registry key: `smarty`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Smarty uses template comment delimiters rather than ordinary code comments.

### Examples
- unsupported or unresolved

## SmPL
- Registry key: `smpl`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SmPL is commonly treated as C-like for comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## SMT
- Registry key: `smt`
- Line comments: ;
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SMT-LIB uses semicolon comments.

### Examples

#### Line comment
```text
x := 1
; keep the next step explicit
x := 2
```

## Solidity
- Registry key: `solidity`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Solidity follows C/C++-style comments and doc comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## Soong
- Registry key: `soong`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Soong/Blueprint files are parsed as C-like config files for comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## SourcePawn
- Registry key: `sourcepawn`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SourcePawn uses C-style comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## SPARQL
- Registry key: `sparql`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: https://www.w3.org/TR/sparql11-query/
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SPARQL queries use # comments.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## Spline Font Database
- Registry key: `spline_font_database`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Font database text files use hash comments in common tooling.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## SQF
- Registry key: `sqf`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SQF uses C-style comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## SQLPL
- Registry key: `sqlpl`
- Line comments: --
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SQL PL uses -- and /* */ comments.

### Examples

#### Line comment
```text
SELECT 1;
-- keep the next query fragment explicit
SELECT 2;
```

#### Block comment
```text
SELECT 1;
/* keep the next query fragment explicit */
SELECT 2;
```

## Squirrel
- Registry key: `squirrel`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Squirrel uses C-like comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## SRecode Template
- Registry key: `srecode_template`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Template comment syntax should be verified against the template engine documentation.

### Examples
- unsupported or unresolved

## SSH Config
- Registry key: `ssh_config`
- Line comments: #
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: OpenSSH config files use hash comments.

### Examples

#### Line comment
```text
value = 1
# keep the next step explicit
value = 2
```

## Stan
- Registry key: `stan`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Stan is typically treated as C-like for comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## Standard ML
- Registry key: `standard_ml`
- Line comments: unsupported
- Block comments: (* *)
- Termination behavior: block comments support true nesting
- Nested comments: yes
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SML uses nested (* *) comments; line comments are not part of the core syntax.

### Examples

#### Block comment
```text
let value = 1
(* keep the next binding explicit *)
value + 1
```

#### Nested comment
```text
let value = 1
(* outer (* inner *) outer *)
value + 1
```

## STAR
- Registry key: `star`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: STAR is ambiguous as a corpus label; I could not confirm a comment grammar.

### Examples
- unsupported or unresolved

## Stata
- Registry key: `stata`
- Line comments: * or //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.stata.com/manuals/m-2comments.pdf
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Stata supports * line comments, // rest-of-line comments, and /* */ block comments in do-files and Mata.

### Examples

#### Line comment
```text
data work.example;
  x = 1;
// keep the next command explicit
summarize price
```

#### Block comment
```text
sysuse auto
/* keep the next command explicit */
summarize mpg
```

## STL
- Registry key: `stl`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unresolved
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: STL is ambiguous as a Stack label; do not infer comments without a spec.

### Examples
- unsupported or unresolved

## STON
- Registry key: `ston`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: STON comment handling was not confirmed from a stable source.

### Examples
- unsupported or unresolved

## StringTemplate
- Registry key: `stringtemplate`
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: StringTemplate comment syntax is template-specific and should be checked against the official docs for the exact version.

### Examples
- unsupported or unresolved

## Stylus
- Registry key: `stylus`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Stylus uses C-like comments; line comments may be stripped depending on output mode.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## SubRip Text
- Registry key: `subrip_text`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unresolved
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: SubRip subtitle files do not have a stable programming-style comment syntax.

### Examples
- unsupported or unresolved

## SugarSS
- Registry key: `sugarss`
- Line comments: unsupported
- Block comments: /* */
- Termination behavior: block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SugarSS follows CSS comment forms and uses block comments.

### Examples

#### Block comment
```text
x = 1;
/* keep the next statement hidden */
x = 2;
```

## SuperCollider
- Registry key: `supercollider`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SuperCollider uses C-style comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## Svelte
- Registry key: `svelte`
- Line comments: unsupported
- Block comments: <!-- -->
- Termination behavior: block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: https://html.spec.whatwg.org/multipage/syntax.html#comments
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Svelte templates accept HTML comments.

### Examples

#### Block comment
```text
<root>
  <!-- keep the next element explicit -->
  <value>1</value>
</root>
```

## SVG
- Registry key: `svg`
- Line comments: unsupported
- Block comments: <!-- -->
- Termination behavior: block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://www.w3.org/TR/xml/#sec-comments
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SVG is XML-based, so XML comments apply.

### Examples

#### Block comment
```text
<root>
  <!-- keep the next element explicit -->
  <value>1</value>
</root>
```

## SWIG
- Registry key: `swig`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: seeded-from-implementation
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SWIG interface files are commonly treated as C/C++-like for comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```

## SystemVerilog
- Registry key: `systemverilog`
- Line comments: //
- Block comments: /* */
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: https://ieeexplore.ieee.org/document/8299595
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: SystemVerilog uses C/C++-style comments and documentation comments.

### Examples

#### Line comment
```text
int value = 1;
// keep the next step explicit
return value;
```

#### Block comment
```text
int value = 1;
/* keep the next step explicit */
return value;
```


## Summary

This chunk still contains unresolved or unsupported labels that should remain out of the registry until a defensible source is found.

Unresolved or unsupported languages: `q`, `Quake`, `Ragel`, `Raw token data`, `RDoc`, `REALbasic`, `Redirect Rules`, `Regular Expression`, `REXX`, `Rich Text Format`, `Rouge`, `RPC`, `RPGLE`, `Self`, `SELinux Policy`, `Slash`, `Slim`, `Smarty`, `SRecode Template`, `STAR`, `STL`, `STON`, `StringTemplate`, `SubRip Text`.
