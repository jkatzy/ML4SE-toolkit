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
- Docs source: `https://code.kx.com/q/learn/tour/scripts/`
- Implementation source: `GitHub Linguist languages.yml`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: q supports `/` line comments, trailing comments, and multiline comment blocks opened by `/` and closed by `\`.

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
- Version scope: Qt Script as shipped with Qt 4/5 and documented as an ECMAScript-based scripting language; comments cross-checked against current ECMAScript lexical grammar
- Version-specific syntax: no Qt Script-specific comment delimiter split found; use the ECMAScript `//` and `/* */` forms
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://doc.qt.io/archives/qt-5.15/qtscript-index.html; https://tc39.es/ecma262/multipage/ecmascript-language-lexical-grammar.html#sec-comments`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Qt Script is an ECMAScript host environment; no separate Qt Script lexical comment syntax was found.

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
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://usdqc.github.io/quakec-resources/qcmanual.html`
- Implementation source: `GitHub Linguist languages.yml`
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: The available QuakeC manual explicitly describes `//` and `/* */`; the Stack label is likely the QuakeC family.

### Examples

#### Line comment
```text
float health;
// keep the next assignment explicit
health = 100;
```

#### Block comment
```text
float health;
/* keep the next assignment explicit */
health = 100;
```

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
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Version scope: Ragel 5.17, 6.1, and 6.6 guides
- Version-specific syntax: no Ragel-specific version split found; the checked guides consistently show `#` line comments in Ragel blocks
- Docs source: `https://www.colm.net/open-source/ragel/; https://www.colm.net/files/ragel/ragel-guide-5.17.pdf; https://www.colm.net/files/ragel/ragel-guide-6.1.pdf; https://www.colm.net/files/ragel/ragel-guide-6.6.pdf`
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Ragel FSM-spec blocks use `#` comments to newline. I checked multiple guides and did not find a versioned delimiter change.

### Examples

#### Line comment
```text
%%{
machine example;
# keep the transition explicit
main := 'a';
}%%
```

## RAML
- Registry key: `raml`
- Version scope: RAML 1.0 API description files, which use YAML syntax for the surrounding document structure
- Version-specific syntax: no RAML-version-specific delimiter split found; RAML inherits YAML `#` comments
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://github.com/raml-org/raml-spec/blob/master/versions/raml-10/raml-10.md; https://yaml.org/spec/1.2.2/#comments`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: Rascal documentation current around 0.42.x plus the Rascal syntax library source
- Version-specific syntax: no version split found; Rascal sources and docs use Java/C-style comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://www.rascal-mpl.org/docs/Rascal/Declarations/SyntaxDefinition/`
- Implementation source: `https://github.com/usethesource/rascal/blob/6b23b1a0624a94ecad422564fa5eb136e3ed2497/src/org/rascalmpl/library/lang/rascal/syntax/Rascal.rsc; GitHub Linguist languages.yml`
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: The official docs show `//` in Rascal examples; the syntax library source confirms both `//` and `/* */` are accepted in Rascal code.

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
- Version scope: GitHub Linguist data label for `.raw` token-data files; no source-language standard found
- Version-specific syntax: unsupported; this appears to be a data artifact label rather than a language with lexical comments
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unresolved
- Nested comments: unsupported
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: This is not a language with a normal comment grammar.

### Examples
- unsupported or unresolved

## RDoc
- Registry key: `rdoc`
- Line comments: `#` in Ruby sources
- Block comments: `=begin` / `=end` in Ruby sources; `/* */` in C sources
- Termination behavior: line comments terminate at end-of-line; Ruby block comments terminate at `=end`; C-style comment blocks terminate at `*/`
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://ruby.github.io/rdoc/doc/markup_reference/rdoc_rdoc.html`
- Implementation source: `https://ruby.github.io/rdoc/RDoc/Parser/Ruby.html`
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: RDoc is host-language dependent. The parser docs show Ruby `#` comments and C-style `/* */` comment blocks as inputs to documentation extraction.

### Examples

#### Line comment
```text
# :call-seq:
#   hello(name) -> String
def hello(name)
  "Hello #{name}"
end
```

#### Block comment
```text
=begin
keep the following method documented
=end
def hello(name)
  "Hello #{name}"
end
```

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
- Version scope: Xojo / REALbasic successor language documentation current at the Xojo API language reference
- Version-specific syntax: current Xojo docs document both `//` and apostrophe line comments; no delimiter-based block comment was confirmed
- Line comments: `//` or `'`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://documentation.xojo.com/api/language/commenting.html`
- Implementation source: `GitHub Linguist languages.yml`
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Xojo documents comments entered with `//` or `'`, including comments on their own line and at the end of executable code.

### Examples

#### Line comment
```text
Var value As Integer = 1 ' keep the next statement explicit
// keep the next statement explicit
```

## Reason
- Registry key: `reason`
- Version scope: Reason syntax cheatsheet documentation for current Reason syntax
- Version-specific syntax: no version split found in checked docs; Reason documents both `//` line comments and `/* */` block comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://reasonml.github.io/docs/en/syntax-cheatsheet`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: The official cheatsheet lists both comment forms explicitly.

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
- Version scope: Red language family and Red/System specification; Red/System comment forms verified directly
- Version-specific syntax: `;` line comments are stable; Red/System also documents `comment { ... }` multiline comments, which are keyword/braced forms rather than simple paired delimiters
- Line comments: `;`
- Block comments: `comment { }` in Red/System; unresolved for a simple Red-language delimiter
- Termination behavior: semicolon comments terminate at end-of-line; Red/System `comment { ... }` terminates at the matching brace expression
- Nested comments: no
- Confidence: high
- Evidence mode: official_docs
- Docs source: `https://static.red-lang.org/red-system-specs.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: candidate
- Notes: Implementing only `;` is straightforward. Treat `comment { ... }` as a keyword form requiring balanced-brace awareness before adding a block extractor.

### Examples

#### Line comment
```text
x := 1
; keep the next step explicit
x := 2
```

#### Block comment
```text
comment {
    keep this Red/System note out of compiled code
}
value: 2
```

## Redcode
- Registry key: `redcode`
- Version scope: ICWS '88 and annotated ICWS '94 Redcode/Core War standards
- Version-specific syntax: no version split found; checked Redcode standards and references use semicolon line comments
- Line comments: `;`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://corewar.co.uk/standards/icws94.htm; https://corewar.co.uk/standards/icws88.txt`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: The ICWS '94 draft says all comments begin with a semicolon.

### Examples

#### Line comment
```text
x := 1
; keep the next step explicit
x := 2
```

## Redirect Rules
- Registry key: `redirect_rules`
- Version scope: Netlify `_redirects` and Cloudflare Pages `_redirects`, matching GitHub Linguist's `_redirects` filename label
- Version-specific syntax: both checked redirect-rule dialects use `#` line comments; no block-comment form found
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://docs.netlify.com/manage/routing/redirects/redirect-options/#comments; https://developers.cloudflare.com/pages/configuration/redirects/`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: The GitHub label maps to `_redirects`; do not generalize this to unrelated redirect configuration formats.

### Examples
#### Line comment
```text
# keep old links working
/old-page /new-page 301
```

## Regular Expression
- Registry key: `regular_expression`
- Version scope: Python 3.9-3.14 `re`, Perl 5.6+ `perlre`, PCRE2 current, ECMAScript 2026 regular expressions
- Version-specific syntax: Python `re.X`/`(?x)` and Perl `/x` use `#` line comments; Perl and PCRE2 also accept `(?#...)`; ECMAScript RegExp does not define a native comment syntax. The label is flavor-dependent, so a single union key would be misleading.
- Line comments: `#` in verbose / extended modes
- Block comments: `(?#...)` inline comments in Perl and PCRE2 only; otherwise unsupported
- Termination behavior: line comments terminate at the next newline in verbose / extended modes; Perl and PCRE2 also support inline `(?#...)` comments that terminate at `)`
- Nested comments: no
- Confidence: cross-checked
- Evidence mode: implementation_cross_checked
- Docs source: `https://docs.python.org/3/library/re.html; https://perldoc.perl.org/perlre; https://www.pcre.org/current/doc/html/pcre2pattern.html; https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Regex comment syntax is flavor-dependent across Python, Perl, PCRE2, and ECMAScript. Do not normalize this without splitting by flavor.

### Examples

#### Line comment
```text
\d+  # the integral part
\.\d*  # the fractional part
```

#### Block comment
```text
\d+(?# integral part)\.\d*
```

## Ren'Py
- Registry key: `renpy`
- Version scope: current Ren'Py language basics documentation
- Version-specific syntax: no version split found; Ren'Py script comments are Python-style hash comments
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://www.renpy.org/doc/html/language_basics.html#comments`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: Android RenderScript `.rs` files, now deprecated but historically C99-like source files
- Version-specific syntax: no RenderScript-specific comment delimiter split found; use the C99/C++-style `//` and `/* */` forms accepted by the RenderScript toolchain
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://developer.android.com/guide/topics/renderscript/compute`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: current ReScript language syntax lookup documentation
- Version-specific syntax: no version split found; ReScript documents `//` line comments and `/* */` block comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: `https://rescript-lang.org/docs/manual/latest/overview#comments`
- Implementation source: `https://github.com/rescript-lang/rescript-lang.org/blob/02f7b35815c6020ed09f11e20d44a2e8ff250fba/apps/docs/markdown-pages/syntax-lookup/language_line_comment.mdx; https://github.com/rescript-lang/rescript-lang.org/blob/02f7b35815c6020ed09f11e20d44a2e8ff250fba/apps/docs/markdown-pages/syntax-lookup/language_block_comment.mdx; GitHub Linguist languages.yml`
- Community source: unresolved
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
- Version scope: RTF document-format specifications and Microsoft RTF protocol references
- Version-specific syntax: unsupported; RTF has control words, groups, destinations, and ignorable destinations, but no general lexical comment delimiter
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unresolved
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: `https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxrtfcp/`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: GitHub Linguist `.rg` language label only; no authoritative Rouge language specification found in this pass
- Version-specific syntax: unresolved; do not infer a grammar from syntax-highlighter mode aliases alone
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: The Linguist label is not enough to distinguish a real `.rg` source language from unrelated Rouge names.

### Examples
- unsupported or unresolved

## RPC
- Registry key: `rpc`
- Version scope: ONC RPC / XDR `.x` interface files, matching GitHub Linguist aliases `rpcgen`, `oncrpc`, and `xdr`
- Version-specific syntax: RFC 4506 XDR specifies only `/* ... */` comments; no `//` line-comment form is defined in the checked standard
- Line comments: unsupported
- Block comments: `/* */`
- Termination behavior: block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://datatracker.ietf.org/doc/html/rfc4506#section-6.1`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Scope this to RPC/XDR interface definitions, not arbitrary RPC framework configuration files.

### Examples
#### Block comment
```text
/* keep the constant explicit */
const MAX_VALUE = 10;
```

## RPGLE
- Registry key: `rpgle`
- Version scope: free-form IBM i RPGLE examples and community conversion examples; fixed-form RPG comment columns were not fully reverified in this pass
- Version-specific syntax: free-form RPGLE uses `//`; fixed-form comment forms should be researched before broadening the registry entry
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
- Version scope: RPM 4.x spec-file manual
- Version-specific syntax: no version split found in checked RPM manual; spec comments are hash-prefixed lines
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://rpm-software-management.github.io/rpm/manual/spec.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: SageMath `.sage` preparsed source files and current Sage tutorial documentation
- Version-specific syntax: no Sage-specific delimiter split found; `.sage` code is Python-derived and uses Python `#` comments
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://doc.sagemath.org/html/en/tutorial/programming.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: Salt SLS files rendered with the default YAML + Jinja stack
- Version-specific syntax: YAML contributes `#` line comments; Jinja templating contributes `{# ... #}` template comments. The registry should support the union for rendered SaltStack state files.
- Line comments: `#`
- Block comments: `{# #}`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://docs.saltproject.io/en/latest/topics/tutorials/starting_states.html; https://jinja.palletsprojects.com/en/stable/templates/#comments; https://yaml.org/spec/1.2.2/#comments`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: GNU sed script syntax and POSIX-like sed script comments
- Version-specific syntax: GNU sed uses `#` comments; a first-line `#n` has special meaning because it can disable automatic printing
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://www.gnu.org/software/sed/manual/html_node/Common-Commands.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Line comments: unsupported
- Block comments: `" ... "`
- Termination behavior: block comments terminate at the closing double quote
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Version scope: Self 4.5.0 handbook
- Version-specific syntax: no version split found; comments are still delimited by double quotes in the checked handbook
- Docs source: `https://handbook.selflanguage.org/4.5/langref.html`
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Self comments are double-quoted and may span multiple lines.

### Examples

#### Block comment
```text
" keep the next step explicit
  and leave the code readable "
```

## SELinux Policy
- Registry key: `selinux_policy`
- Version scope: SELinux reference-policy style `.te` / `.if` / policy source files checked against Red Hat guidance and refpolicy sources
- Version-specific syntax: no version split found; policy sources use `#` line comments
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: medium
- Evidence mode: implementation_cross_checked
- Docs source: `https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/using_selinux/writing-a-custom-selinux-policy`
- Implementation source: `https://github.com/SELinuxProject/refpolicy`
- Community source: `https://github.com/SELinuxProject/selint`
- Corpus fallback source: unresolved
- Recommended action: candidate
- Notes: SELinux policy sources and SELint both treat `#` as the comment form in `.te` / `.if` files. I did not confirm a delimiter-based block comment form.

### Examples

#### Line comment
```text
policy_module(example, 1.0)

# keep the next rule explicit
allow example_t self:process signal;
```

## ShaderLab
- Registry key: `shaderlab`
- Version scope: Unity ShaderLab shader files and embedded shader program blocks
- Version-specific syntax: no version split found; ShaderLab examples and syntax highlighters use C/C++-style comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://docs.unity3d.com/Manual/SL-Shader.html; https://docs.unity3d.com/Manual/SL-ShaderPrograms.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: SingularityCE / Apptainer definition files
- Version-specific syntax: no version split found; definition files use shell-like `#` comments outside section content
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://docs.sylabs.io/guides/latest/user-guide/definition_files.html; https://apptainer.org/docs/user/latest/definition_files.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Version scope: current Slash book / structure docs
- Version-specific syntax: no version split found; the checked Slash docs consistently use `#` line comments
- Docs source: `https://slashlang.org/book/structure; https://slashlang.org/book/intro`
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Slash comments are hash-prefixed and can appear inline or on their own line.

### Examples

#### Line comment
```text
println("Hello")
# keep the next statement explicit
println("World")
```

## Slice
- Registry key: `slice`
- Version scope: ZeroC Ice Slice language reference, current Slice definition files
- Version-specific syntax: no version split found; Slice supports C++-style `//` and `/* */` comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://docs.zeroc.com/ice/latest/slice/slice-language-reference`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Line comments: `/`
- Block comments: `/!`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at dedent
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://github.com/slim-template/slim`
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Slim treats `/` as a code comment and `/!` as the HTML-comment form. The comments are indentation-scoped rather than delimiter-nested.

### Examples

#### Line comment
```text
body
  / This line won't get displayed.
    Neither does this line.
  p Visible content.
```

#### Block comment
```text
body
  /! This will get displayed as html comments.
  p Visible content.
```

## Smali
- Registry key: `smali`
- Version scope: smali/dex assembly files as parsed by the public smali toolchain
- Version-specific syntax: no version split found; smali examples and grammar sources use `#` comments
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: `https://github.com/google/smali; GitHub Linguist languages.yml`
- Community source: unresolved
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
- Line comments: unsupported
- Block comments: `{* *}`
- Termination behavior: block comments terminate at the first closing `*}`
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://www.smarty.net/docsv2/pt_BR/language.basic.syntax.tpl`
- Implementation source: GitHub Linguist languages.yml
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Smarty comments are template-delimited and can span multiple lines, but they do not nest.

### Examples

#### Block comment
```text
<body>
{* this multiline
   comment is
   not sent to browser *}
{include file='header.tpl'}
</body>
```

## SmPL
- Registry key: `smpl`
- Version scope: Coccinelle Semantic Patch Language (SmPL) grammar and examples
- Version-specific syntax: no version split found; SmPL follows C source comment forms in semantic patches
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://coccinelle.gitlabpages.inria.fr/website/docs/main_grammar.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: SMT-LIB 2.x language standard
- Version-specific syntax: no version split found in checked SMT-LIB 2.x references; comments begin with semicolon and run to end-of-line
- Line comments: `;`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://smt-lib.org/language.shtml`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: Solidity latest language documentation and NatSpec documentation comments
- Version-specific syntax: no version split found for lexical comments; Solidity supports `//` and `/* */`, with NatSpec variants `///` and `/** */` treated as documentation comments
- Line comments: `//`; documentation line comments `///`
- Block comments: `/* */`; documentation block comments `/** */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://docs.soliditylang.org/en/latest/layout-of-source-files.html#comments; https://docs.soliditylang.org/en/latest/natspec-format.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: Android Soong / Blueprint `Android.bp` files
- Version-specific syntax: no version split found; Blueprint parser source accepts Go/C-style line and block comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://source.android.com/docs/setup/build`
- Implementation source: `https://android.googlesource.com/platform/build/blueprint/+/refs/heads/main/parser/lexer.go; GitHub Linguist languages.yml`
- Community source: unresolved
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
- Version scope: SourcePawn 1.7+ transitional syntax documentation
- Version-specific syntax: no version split found in checked SourcePawn docs; SourcePawn supports `//` and `/* */`
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://wiki.alliedmods.net/Introduction_to_SourcePawn_1.7`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: FontForge SFD format reference, including SFD 3.0 examples
- Version-specific syntax: unsupported; the checked SFD spec documents `Comments:` data fields but no general lexical comment delimiter such as `#`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: `https://fontforge.org/docs/techref/sfdformat.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: `Comments:` and `UComments:` are font metadata keys, not ignored source comments.

### Examples
- unsupported or unresolved

## SQF
- Registry key: `sqf`
- Version scope: Bohemia Interactive SQF syntax documentation current through Arma 3-era SQF
- Version-specific syntax: no version split found; SQF supports `//` line comments and `/* */` block comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://community.bistudio.com/wiki/SQF_Syntax`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: IBM Db2 SQL procedural language / SQL comments in Db2 for z/OS and Db2 11.x family docs
- Version-specific syntax: SQL PL supports `--` simple comments and `/* */` bracketed comments; Db2 docs allow nested bracketed comments
- Line comments: `--`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; bracketed comments terminate at the matching `*/` when nested
- Nested comments: yes
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=statements-sql-comments; https://www.ibm.com/docs/en/db2/11.5.x?topic=statements-comments`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Preserve the Db2 nested-block behavior instead of assuming generic SQL first-closer semantics.

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

#### Nested comment
```text
SELECT 1;
/* outer /* inner */ outer */
SELECT 2;
```

## Squirrel
- Registry key: `squirrel`
- Version scope: Squirrel 3 language reference
- Version-specific syntax: no version split found; Squirrel 3 documents C/C++-style comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `http://squirrel-lang.org/doc/squirrel3.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: GNU Emacs SRecode manual and CEDET template examples
- Version-specific syntax: unresolved; examples suggest Lisp-style semicolon comments in some template files, but I did not find a stable language-wide delimiter definition
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unknown
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: `https://www.gnu.org/software/emacs/manual/html_node/srecode/Template-Naming-Conventions.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: needs manual research
- Notes: Template comment syntax should be verified against the parser or exact `.srt` template documentation before adding registry support.

### Examples
- unsupported or unresolved

## SSH Config
- Registry key: `ssh_config`
- Version scope: OpenSSH `ssh_config(5)` client configuration files
- Version-specific syntax: no version split found; OpenSSH config comments use `#` to end-of-line
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://man.openbsd.org/ssh_config`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: current Stan language reference manual
- Version-specific syntax: no version split found; Stan supports C++-style `//` and `/* */` comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://mc-stan.org/docs/reference-manual/syntax.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: Standard ML '97 language definition and SML/NJ-family implementation behavior
- Version-specific syntax: no line-comment syntax in the core language; `(* ... *)` comments are nested in Standard ML
- Line comments: unsupported
- Block comments: (* *)
- Termination behavior: block comments support true nesting
- Nested comments: yes
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: `https://smlfamily.github.io/sml97-defn.pdf`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: STAR/CIF data files as mapped by GitHub Linguist's `.star` data-language label
- Version-specific syntax: checked CIF/STAR syntax references use `#` comments; no block-comment form found
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line comments terminate at end-of-line; block comments unsupported
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://www.iucr.org/resources/cif/spec/version1.1/cifsyntax; https://www.iucr.org/resources/cif/spec/version2.0/cifsyntax`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Scope this to STAR/CIF data syntax, not unrelated languages named Star.

### Examples
#### Line comment
```text
# keep source metadata visible
data_example
```

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
- Version scope: ASCII and binary STL mesh file formats
- Version-specific syntax: unsupported; STL has header/name fields and facet data but no comment delimiter
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: `https://www.loc.gov/preservation/digital/formats/fdd/fdd000505.shtml`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: STL files can contain arbitrary text in some name/header slots, but those are data fields rather than ignored comments.

### Examples
- unsupported or unresolved

## STON
- Registry key: `ston`
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unresolved; STON does not define a native comment delimiter
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Version scope: STON reference docs in Pharo Enterprise and the STON implementation docs
- Version-specific syntax: no native comment syntax found; comments are handled only by helper streams such as `STONCStyleCommentsSkipStream` and `fromStringWithComments:`
- Docs source: `https://book.huihoo.com/smalltalk/pharo/enterprise-pharo/book-result/STON/STON.html; https://files.pharo.org/books-pdfs/entreprise-pharo/2016-10-06-EnterprisePharo.pdf`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: STON explicitly says comments are not part of the format; comment stripping is an external helper, not native syntax.

### Examples
- unsupported or unresolved

## StringTemplate
- Registry key: `stringtemplate`
- Version scope: StringTemplate 4 with default `<` / `>` delimiters; older API pages checked for comment token support
- Version-specific syntax: ST4 template comments use `<!...!>` with the active start/stop delimiters; no `//` line comment form found
- Line comments: unsupported
- Block comments: `<! !>`
- Termination behavior: block comments terminate at first `!>` for the default delimiter pair
- Nested comments: no
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: `https://www.stringtemplate.org/; https://github.com/antlr/stringtemplate4/blob/master/doc/cheatsheet.md`
- Implementation source: `https://github.com/antlr/stringtemplate4/blob/master/src/org/stringtemplate/v4/compiler/STLexer.java; GitHub Linguist languages.yml`
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: STLexer recognizes comments after the start delimiter followed by `!` and consumes until `!` plus the stop delimiter.

### Examples
#### Block comment
```text
Hello, <name>
<! keep this note out of output !>
```

## Stylus
- Registry key: `stylus`
- Version scope: current Stylus comments documentation
- Version-specific syntax: Stylus supports `//`, `/* */`, and preserved `/*! */` comments; no version split found
- Line comments: `//`
- Block comments: `/* */`; preserved block comments `/*! */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://stylus-lang.com/docs/comments.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: SubRip Subtitle `.srt` text format as described by Library of Congress and Matroska references
- Version-specific syntax: unsupported; SRT consists of numbered timed caption blocks and does not define a native comment delimiter
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: `https://loc.gov/preservation/digital/formats/fdd/fdd000569.shtml; https://www.matroska.org/technical/subtitles.html#srt-subtitles`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: unsupported
- Notes: SubRip subtitle files do not have a stable programming-style comment syntax.

### Examples
- unsupported or unresolved

## SugarSS
- Registry key: `sugarss`
- Version scope: PostCSS SugarSS README for current `.sss` syntax
- Version-specific syntax: SugarSS supports `//` inline comments and `/* */` multiline comments; no silent-comment variant exists
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://github.com/postcss/sugarss`
- Implementation source: `https://github.com/postcss/sugarss; GitHub Linguist languages.yml`
- Community source: unresolved
- Corpus fallback source: unresolved
- Recommended action: implement
- Notes: Output CSS keeps all comments from `.sss` source unless a downstream plugin removes them.

### Examples

#### Line comment
```text
// keep the next rule visible
.button
  color: blue
```

#### Block comment
```text
/*
 keep the next rule visible
 */
.button
  color: blue
```

## SuperCollider
- Registry key: `supercollider`
- Version scope: current SuperCollider language reference / syntax docs
- Version-specific syntax: no version split found; SuperCollider supports `//` and `/* */`
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://doc.sccode.org/Reference/Syntax-Shortcuts.html`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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
- Version scope: SWIG interface files, SWIG 1.3 manual through current SWIG interface conventions
- Version-specific syntax: no version split found for lexical comments; SWIG interface files allow C and C++ style comments
- Line comments: `//`
- Block comments: `/* */`
- Termination behavior: line comments terminate at end-of-line; block comments terminate at first closing delimiter
- Nested comments: no
- Confidence: verified
- Evidence mode: official_docs
- Docs source: `https://www.swig.org/Doc1.3/SWIG.html#n5`
- Implementation source: GitHub Linguist languages.yml
- Community source: unresolved
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

Assigned unresolved, unsupported, or candidate labels: `Raw token data`, `Red`, `Regular Expression`, `Rich Text Format`, `Rouge`, `RPGLE`, `SELinux Policy`, `Spline Font Database`, `SRecode Template`, `STL`, `STON`, `SubRip Text`.
