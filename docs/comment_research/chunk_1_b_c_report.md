# Chunk 1 B-C Research Report

This report is documentation-oriented and test-oriented. I kept unresolved items explicit instead of guessing.

## Ballerina
- Registry key: `ballerina`
- Version scope: `Swan Lake-era Ballerina docs; reviewed the current style guide plus the language/spec surface.`
- Version-specific syntax: `No syntax split confirmed in the reviewed sources; // and /* ... */ remain the documented comment forms, so the registry should keep the union of both.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: [Ballerina comments](https://ballerina.io/learn/style-guide/annotations-documentation-and-comments/)
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed the registry and add line/block regression tests.`
- Notes: `C-like comment syntax.`

- Example - line:
```text
int x = 1;
// comment
int y = 2;
```
- Example - block:
```text
int x = 1;
/* comment */
int y = 2;
```

## BASIC
- Registry key: `basic`
- Version scope: `Classic BASIC family; reviewed QBasic/QuickBASIC, IBM BASIC, and Visual Basic/VBA-style references.`
- Version-specific syntax: `Older BASIC dialects may only support REM, while newer compatible dialects also accept apostrophe comments. Implement the union of REM and apostrophe forms for BASIC-family coverage.`
- Line comments: `'` and `REM`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: [Visual Basic REM statement](https://learn.microsoft.com/en-us/dotnet/visual-basic/language-reference/statements/rem-statement)
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed the registry and add line-comment tests for apostrophe and REM forms.`
- Notes: `BASIC-family syntax varies by dialect, but both forms are common.`

- Example - line:
```text
x = 1
' comment
y = 2
```
- Example - line:
```text
x = 1
REM comment
y = 2
```

## Batchfile
- Registry key: `batchfile`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `REM` and `::`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: [REM command](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/rem)
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed the registry and add tests for REM and label-style comments.`
- Notes: `::` is commonly used as a comment-like label hack in batch files.

- Example - line:
```bat
@echo off
REM comment
echo done
```
- Example - line:
```bat
@echo off
:: comment
echo done
```

## Beef
- Registry key: `beef`
- Version scope: `current master and release 0.42.1`
- Version-specific syntax: `No difference found between current master and release 0.42.1.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `balanced recursive delimiters in native Beef mode`
- Nested comments: `supported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Beef language guide](https://www.beeflang.org/docs/language-guide/)
- Implementation source: [Beef parser](https://github.com/beefytech/Beef/blob/master/IDEHelper/Compiler/BfParser.cpp)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with line and nested examples.`
- Notes: `The parser disables recursive block comments only in its separate C++ compatibility mode. Native Beef mode defaults to recursive block comments.`

- Example - line:
```beef
int value = 1; // note
value++;
```
- Example - nested:
```beef
int value = 1;
/* outer /* note */ outer */
value++;
```

## Berry
- Registry key: `berry`
- Version scope: `current master and release v1.1.0`
- Version-specific syntax: `No comment-syntax difference found between current master and v1.1.0.`
- Line comments: `#`
- Block comments: `#- ... -#`
- Termination behavior: `line comments end at newline; block comments stop at the first -#`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Berry 1.1.0 reference](https://berry.readthedocs.io/en/latest/source/en/Chapter-1.html)
- Implementation source: [Berry lexer](https://github.com/berry-lang/berry/blob/master/src/be_lexer.c)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with line and block examples.`
- Notes: `The line-comment regex excludes #- so block comments are not emitted twice.`

- Example - line:
```berry
value = 1 # note
value += 1
```
- Example - block:
```berry
value = 1
#- note -#
value += 1
```

## BibTeX
- Registry key: `bibtex`
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
- Recommended action: `Seed the registry and add percent-comment tests.`
- Notes: `Standard BibTeX comment marker.`

- Example - line:
```bibtex
@article{key,
  title = {A title} % comment
}
```

## Bicep
- Registry key: `bicep`
- Version scope: `Microsoft Learn Bicep file syntax, reviewed 2026-05-22.`
- Version-specific syntax: `No version split found; Bicep uses C-style line and multiline comments.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `end of line for line comments; first closing delimiter wins for multiline comments`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [Bicep file structure and syntax](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/file)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with line and block fixtures.`
- Notes: `Microsoft documents // for single-line comments and /* ... */ for multiline comments.`

- Example - line:
```text
param name string
// comment
output x string = name
```
- Example - block:
```text
param name string
/* comment */
output x string = name
```

## Bikeshed
- Registry key: `bikeshed`
- Version scope: `current parser and v0.9 regression fixture`
- Version-specific syntax: `HTML comments are present in current documentation/parser behavior and the v0.9 test corpus.`
- Line comments: `unsupported at the document level`
- Block comments: `<!-- ... -->`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Bikeshed big-text docs](https://speced.github.io/bikeshed/#big-text)
- Implementation source: [Bikeshed HTML parser](https://github.com/speced/bikeshed/blob/main/bikeshed/h/parser/parser.py)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with an HTML-comment fixture.`
- Notes: `Hash comments are supported inside Bikeshed's embedded InfoTree format, not as a universal document-level comment marker, so they are excluded.`

- Example - block:
```html
<p>before</p>
<!-- note -->
<p>after</p>
```

## BitBake
- Registry key: `bitbake`
- Version scope: `Yocto Project 5.3.4 recipe syntax, reviewed 2026-05-22.`
- Version-specific syntax: `No version split found for recipe comments.`
- Line comments: `#` at the beginning of a recipe line
- Block comments: `unsupported`
- Termination behavior: `end of line`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [Yocto Project recipe syntax](https://docs.yoctoproject.org/5.3.4/dev-manual/new-recipe.html)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with start-of-line hash fixtures.`
- Notes: `The Yocto recipe guide treats lines beginning with # as comments.`

- Example - line:
```text
SUMMARY = "Example"
# comment
LICENSE = "MIT"
```

## Blade
- Registry key: `blade`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `{{-- ... --}}`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://laravel.com/docs/12.x/blade#comments
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed template-comment tests and keep line comments unsupported.`
- Notes: `Blade comments are template-level and do not use C-style delimiters.`

- Example - line:
```text
<div>
    {{-- comment --}}
    <span>{{ $name }}</span>
</div>
```

## BlitzBasic
- Registry key: `blitzbasic`
- Version scope: `archived master and v1.108b`
- Version-specific syntax: `No comment-syntax difference found between archived master and v1.108b.`
- Line comments: `;`
- Block comments: `unsupported`
- Termination behavior: `end of line`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Blitz3D comments reference](https://github.com/blitz-research/blitz3d/blob/master/_release/help/language/lang_ref_comments.html)
- Implementation source: [Blitz3D tokenizer](https://github.com/blitz-research/blitz3d/blob/master/compiler/toker.cpp)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with an inline semicolon fixture.`
- Notes: `The official reference explicitly permits comments on their own line or following code.`

- Example - line:
```blitzbasic
Function Redraw() ; note
End Function
```

## BlitzMax
- Registry key: `blitzmax`
- Version scope: `current bcc and archived BlitzMax v1.51`
- Version-specific syntax: `No relevant syntax difference found; both accept apostrophe lines and line-oriented Rem blocks.`
- Line comments: `'`
- Block comments: `Rem ... EndRem` or `Rem ... End Rem`
- Termination behavior: `apostrophe comments end at newline; Rem blocks end at the first line beginning with EndRem or End Rem`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [BlitzMax comments](https://blitzmax.org/docs/en/language/comments/)
- Implementation source: [bcc tokenizer](https://github.com/bmx-ng/bcc/blob/master/toker.bmx)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with apostrophe and Rem-block fixtures.`
- Notes: `Rem is a block opener, not a second line-comment marker. The registry requires it at the beginning of a source line after optional horizontal whitespace.`

- Example - line:
```blitzmax
Print "Comment Test"    ' note
Print "done"
```
- Example - block:
```blitzmax
Rem
note
End Rem
Print "done"
```

## Bluespec
- Registry key: `bluespec`
- Version scope: `current bsc main and release 2021.07`
- Version-specific syntax: `No comment-syntax difference found between current main and the 2021.07 preprocessor.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [BSV reference source](https://github.com/B-Lang-org/bsc/blob/main/doc/BSV_ref_guide/BSV_lang.tex)
- Implementation source: [bsc preprocessor](https://github.com/B-Lang-org/bsc/blob/main/src/comp/SystemVerilogPreprocess.lhs)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with line and block fixtures.`
- Notes: `The reference explicitly states that comments do not nest and that /* inside a block has no special significance.`

- Example - line:
```bluespec
rule update;
  // note
  value <= 1;
endrule
```
- Example - block:
```bluespec
rule update;
  /* note */
  value <= 1;
endrule
```

## Boo
- Registry key: `boo`
- Version scope: `current master and archived unstable tag`
- Version-specific syntax: `No comment-syntax difference found between current master and the unstable tag.`
- Line comments: `#` and `//`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at newline; block comments require balanced recursive delimiters`
- Nested comments: `supported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Boo comments guide](https://github.com/boo-lang/boo/wiki/Language-guide%3A-comments)
- Implementation source: [Boo lexer grammar](https://github.com/boo-lang/boo/blob/master/src/Boo.Lang.Parser/boo.g)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with both line markers and a nested block fixture.`
- Notes: `The lexer calls the multiline-comment rule recursively, and the language guide requires proper nesting.`

- Example - line:
```boo
value = 1 # note
value += 1
```
- Example - line:
```boo
value = 1 // note
value += 1
```
- Example - nested:
```boo
value = 1
/* outer /* note */ outer */
value += 1
```

## Boogie
- Registry key: `boogie`
- Version scope: `current master and release v3.5.6`
- Version-specific syntax: `No comment-syntax difference found between current master and v3.5.6.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at newline; block comments require balanced recursive delimiters`
- Nested comments: `supported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Boogie language reference](https://boogie-docs.readthedocs.io/en/latest/LangRef.html#comments)
- Implementation source: [Boogie grammar](https://github.com/boogie-org/boogie/blob/master/Source/Core/BoogiePL.atg)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with line and nested block fixtures.`
- Notes: `The language reference documents only // comments, while the generated scanner and authoritative grammar also recognize recursively nested /* ... */ comments.`

- Example - line:
```boogie
var value:int; // note
assume value > 0;
```
- Example - nested:
```boogie
var value:int;
/* outer /* note */ outer */
assume value > 0;
```

## Brainfuck
- Registry key: `brainfuck`
- Version scope: `Urban Mueller-era Brainfuck as documented by brainfuck.org, plus current community reference behavior.`
- Version-specific syntax: `Current and historical references agree that Brainfuck has eight command characters and ignores every other character; there is no delimiter-based comment syntax to seed.`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: [brainfuck.org reference](https://brainfuck.org/brainfuck.html); [brainfuck.org implementor notes](https://brainfuck.org/epistle.html)
- Implementation source: `unresolved`
- Community source: [Esolangs Brainfuck](https://esolangs.org/wiki/Brainfuck)
- Corpus fallback source: `not used`
- Recommended action: `Document that non-command characters are ignored rather than treated as comments.`
- Notes: `A comment extractor should not treat arbitrary ignored text as a comment, because any of the eight command characters inside that text is still executable Brainfuck.`

- Example - unsupported:
```text
++[>+++<-]>.
hello world
```

## BrighterScript
- Registry key: `brighterscript`
- Version scope: `v0.72.5 and v0.71.1`
- Version-specific syntax: `No comment-syntax difference found between v0.72.5 and v0.71.1.`
- Line comments: `'` and `REM`
- Block comments: `unsupported`
- Termination behavior: `both forms run to the next CR or LF`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [BrighterScript specification](https://github.com/rokucommunity/brighterscript/blob/master/docs/readme.md)
- Implementation source: [BrighterScript lexer](https://github.com/rokucommunity/brighterscript/blob/master/src/lexer/Lexer.ts)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with apostrophe and REM fixtures.`
- Notes: `BrighterScript is a BrightScript superset. REM is case-insensitive, but the lexer preserves rem as an identifier when it follows member-access dot syntax.`

- Example - line:
```brighterscript
value = 1 ' note
value++
```
- Example - line:
```brighterscript
REM note
value = 1
```

## Brightscript
- Registry key: `brightscript`
- Version scope: `current Roku developer documentation`
- Version-specific syntax: `No alternative comment syntax is documented for current BrightScript.`
- Line comments: `'` and `REM`
- Block comments: `unsupported`
- Termination behavior: `both forms run to the end of the line`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Roku expressions and comments](https://developer.roku.com/dev/docs/expressions-variables-types)
- Implementation source: [Compatible BrighterScript lexer](https://github.com/rokucommunity/brighterscript/blob/master/src/lexer/Lexer.ts)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with apostrophe and REM fixtures.`
- Notes: `Roku explicitly documents both line-comment forms and says to use conditional compilation rather than a block-comment delimiter for larger regions.`

- Example - line:
```brightscript
value = 1 ' note
value = value + 1
```
- Example - line:
```brightscript
REM note
value = 1
```

## Browserslist
- Registry key: `browserslist`
- Version scope: `4.28.2 and 4.27.0`
- Version-specific syntax: `No comment-syntax difference found between 4.28.2 and 4.27.0.`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `runs to newline and may follow a query`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Browserslist config docs](https://github.com/browserslist/browserslist#browserslistrc)
- Implementation source: [Browserslist config parser](https://github.com/browserslist/browserslist/blob/main/node.js)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with an inline hash-comment fixture.`
- Notes: `The parser removes # through newline before splitting config queries; official examples include both full-line and trailing comments.`

- Example - line:
```browserslist
defaults # note
last 2 versions
```

## C2hs Haskell
- Registry key: `c2hs_haskell`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `--`
- Block comments: `{- ... -}`
- Termination behavior: `true nesting supported`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: [Haskell comments in the 2010 report](https://www.haskell.org/onlinereport/haskell2010/haskellch2.html#x7-200002.5)
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed nested-block coverage and add Haskell-style comment tests.`
- Notes: `C2hs follows Haskell comment rules.`

- Example - line:
```text
foo = 1
-- comment
bar = 2
```
- Example - block:
```text
foo = 1
{- comment -}
bar = 2
```
- Example - nested:
```text
foo = 1
{- outer {- inner -} outer -}
bar = 2
```

## Cabal Config
- Registry key: `cabal_config`
- Version scope: `current master and cabal-install 3.14.2.0`
- Version-specific syntax: `No comment-syntax difference found between current master and 3.14.2.0.`
- Line comments: `--`
- Block comments: `unsupported`
- Termination behavior: `runs to newline or EOF on a comment-only field line`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Cabal configuration](https://cabal.readthedocs.io/en/stable/config.html)
- Implementation source: [Cabal field lexer](https://github.com/haskell/cabal/blob/master/Cabal-syntax/src/Distribution/Fields/Lexer.x)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with a line-anchored dash-comment fixture.`
- Notes: `The field lexer permits optional leading whitespace before --. Cabal documentation warns against ordinary trailing comments because field values may contain program options.`

- Example - line:
```cabal
-- note
remote-repo-cache: /tmp/cabal
```

## Cadence
- Registry key: `cadence`
- Version scope: `current master and v1.8.9`
- Version-specific syntax: `No comment-syntax difference found between current master and v1.8.9.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at newline; block comments require balanced recursive delimiters`
- Nested comments: `supported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Cadence syntax](https://cadence-lang.org/docs/language/syntax#comments)
- Implementation source: [Cadence comment parser](https://github.com/onflow/cadence/blob/master/parser/comment.go)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with line and nested block fixtures.`
- Notes: `Cadence documentation explicitly describes comments as nested and balanced; the parser increments and decrements a block-comment depth counter. Documentation comments use /// and /** ... **/, which are covered by the regular delimiters.`

- Example - line:
```cadence
let value = 1 // note
log(value)
```
- Example - nested:
```cadence
let value = 1
/* outer /* note */ outer */
log(value)
```

## CAP CDS
- Registry key: `cap_cds`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://cap.cloud.sap/docs/cds/cdl
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line and block comment tests, plus doc-comment coverage if needed.`
- Notes: `CDL explicitly documents line-end, block, and doc comments.`

- Example - line:
```text
entity Books {
  // comment
  key ID : Integer;
}
```
- Example - block:
```text
entity Books {
  /* comment */
  key ID : Integer;
}
```

## Cap'n Proto
- Registry key: `capn_proto`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: [Cap'n Proto language reference](https://capnproto.org/language.html)
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed the registry and add hash-comment tests.`
- Notes: `Standard Cap'n Proto comment marker.`

- Example - line:
```text
@0xabcdefabcdefabcd;
# comment
struct Foo {}
```

## CartoCSS
- Registry key: `cartocss`
- Version scope: `v1.3.1 and v1.2.0`
- Version-specific syntax: `No comment-syntax difference found between v1.3.1 and v1.2.0.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [CartoCSS language elements](https://cartocss.readthedocs.io/en/latest/language_elements.html)
- Implementation source: [CartoCSS parser](https://github.com/cartocss/carto/blob/master/lib/carto/parser.js)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with line and non-nested block fixtures.`
- Notes: `The reference parser skips Less-style // comments silently and creates comment nodes for CSS /* ... */ comments. Its block regex stops at the first close.`

- Example - line:
```cartocss
#layer {
  line-color: #fff; // note
}
```
- Example - block:
```cartocss
#layer {
  /* note */
  line-color: #fff;
}
```

## Ceylon
- Registry key: `ceylon`
- Version scope: `Ceylon 1.3 specification and archived 1.3.4-SNAPSHOT compiler`
- Version-specific syntax: `No comment-syntax difference found between the final 1.3 specification and archived compiler grammar.`
- Line comments: `//`, `#!`
- Block comments: `/* ... */`
- Termination behavior: `line comments run to newline or EOF; block comments use balanced recursive delimiters`
- Nested comments: `true nesting supported`
- Confidence: `high`
- Evidence mode: `official_spec_plus_implementation`
- Docs source: [Ceylon 1.3 specification](https://web.mit.edu/ceylon_v1.3.3/ceylon-1.3.3/doc/en/spec/html_single/#comments)
- Implementation source: [Ceylon compiler grammar](https://github.com/eclipse-archived/ceylon/blob/master/typechecker/antlr/org/eclipse/ceylon/compiler/typechecker/parser/Ceylon.g)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with slash, shebang, and nested-block fixtures.`
- Notes: `The specification explicitly defines // and #! end-of-line comments and recursively nested /* ... */ blocks.`

- Example - line:
```ceylon
shared void run() {
  print("hi"); // note
}
```
- Example - shebang:
```ceylon
#!/usr/bin/ceylon
shared void run() {}
```
- Example - block:
```ceylon
shared void run() {
  /* outer /* note */ outer */
}
```

## Chapel
- Registry key: `chapel`
- Version scope: `Chapel 2.8 current documentation, Chapel 0.98 specification, and current compiler scanner`
- Version-specific syntax: `No comment-syntax difference found across the checked historical and current specifications.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `line comments run to newline or EOF; block comments use balanced recursive delimiters`
- Nested comments: `true nesting supported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Chapel 2.8 lexical structure](https://chapel-lang.org/docs/language/spec/lexical-structure.html#comments); [Chapel 0.98 specification](https://chapel-lang.org/spec/spec-0.98.pdf)
- Implementation source: [Chapel scanner](https://github.com/chapel-lang/chapel/blob/main/frontend/lib/parsing/lexer-help.h)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with slash-line and nested-block fixtures.`
- Notes: `The current scanner increments and decrements a nesting depth for block delimiters.`

- Example - line:
```chapel
proc main() {
  writeln("hello"); // note
}
```
- Example - block:
```chapel
proc main() {
  /* outer /* note */ outer */
}
```

## Checksums
- Registry key: `checksums`
- Version scope: `GitHub Linguist 9.6.0 Checksums data family and language-etc grammar at 182cc8d`
- Version-specific syntax: `The label intentionally unions GNU-style, BSD-style, and isolated digest records; no shared comment delimiter is defined.`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [GitHub Linguist Checksums definition](https://github.com/github-linguist/linguist/blob/main/lib/linguist/languages.yml)
- Implementation source: [language-etc Checksums grammar](https://github.com/Alhadis/language-etc/blob/master/grammars/checksums.cson)
- Community source: `unresolved`
- Corpus fallback source: [GitHub Linguist Checksums samples](https://github.com/github-linguist/linguist/tree/main/samples/Checksums)
- Recommended action: `Keep unsupported; do not infer hash comments for the generic data family.`
- Notes: `The grammar recognizes checksum records only. A leading # is not a shared comment form across the GNU, BSD, and isolated formats represented by this label.`

- Example - GNU-style data:
```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  empty.txt
```

## ChucK
- Registry key: `chuck`
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
- Recommended action: `Seed the registry and add C-like comment tests.`
- Notes: `Standard C-like syntax.`

- Example - line:
```text
// comment
1 => int x;
```
- Example - block:
```text
/* comment */
1 => int x;
```

## CIL
- Registry key: `cil`
- Version scope: `.NET runtime ILAsm lexer in .NET 6, .NET 10, and current main`
- Version-specific syntax: `No comment-syntax difference found across the checked runtime versions.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Microsoft ILAsm overview](https://learn.microsoft.com/en-us/archive/msdn-magazine/2001/may/bugslayer-ildasm-is-your-new-best-friend)
- Implementation source: [.NET ILAsm lexer](https://github.com/dotnet/runtime/blob/main/src/coreclr/ilasm/grammar_after.cpp)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with line and non-nested block fixtures.`
- Notes: `The lexer uses one state bit for end-of-line comments and one for block comments. A block opener encountered while already inside a block does not increase depth.`

- Example - line:
```cil
.method public static void Main() cil managed {
  ret // note
}
```
- Example - block:
```cil
.method public static void Main() cil managed {
  /* note */
  ret
}
```

## Cirru
- Registry key: `cirru`
- Version scope: `Cirru parser 0.2.5 at 14f9a9b7`
- Version-specific syntax: `The parser preserves ; and ;; as ordinary leaf tokens; only expression consumers interpret a list headed by either token as a comment.`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [Cirru syntax documentation](https://text.cirru.org/)
- Implementation source: [Cirru parser](https://github.com/Cirru/parser.rs)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Keep unsupported in the lexical registry; comment expressions require a Cirru parse tree.`
- Notes: `The lexer accepts semicolons inside ordinary tokens. Cirru::is_comment recognizes only leaf values equal to ; or ;;, and format_to_lisp applies that predicate to the head of a parsed list. Regex delimiter matching would overmatch ordinary semicolon tokens and cannot determine the indentation-defined extent of a comment expression.`

- Example - expression comment:
```cirru
defn main ()
  ; this parsed expression is treated as a comment
  println |ready
```

## Clarion
- Registry key: `clarion`
- Version scope: `Clarion .clw source documented by the current online language reference`
- Version-specific syntax: `Clarion# adds separate multiline and XML documentation forms; those are excluded from the Clarion Stack key.`
- Line comments: `!`
- Block comments: `unsupported`
- Termination behavior: `end of line`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Clarion special characters](https://clarion.help/doku.php?id=special_characters.htm)
- Implementation source: [SublimeClarion language configuration](https://github.com/fushnisoft/SublimeClarion/blob/master/clarion.configuration.json)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with an inline line-comment fixture.`
- Notes: `The reference states that ! begins a source-code comment and its PROGRAM and MEMBER examples use both whole-line and trailing forms. The editor configuration also declares ! as the line-comment token.`

- Example - line:
```clarion
PROGRAM ! note
CODE
```

## Classic ASP
- Registry key: `classic_asp`
- Version scope: `Classic ASP on IIS, including configurable page and application scripting languages`
- Version-specific syntax: `A page may use VBScript, JScript, or another installed COM scripting engine, including multiple languages in one .asp file.`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [Microsoft Working with Scripting Languages](https://learn.microsoft.com/en-us/previous-versions/iis/6.0-sdk/ms525153%28v%3Dvs.90%29)
- Implementation source: [TextMate HTML-ASP grammar](https://github.com/textmate/asp.tmbundle/blob/master/Syntaxes/HTML-ASP.plist)
- Community source: `unresolved`
- Corpus fallback source: [Microsoft ASP include directives](https://learn.microsoft.com/en-us/previous-versions/iis/6.0-sdk/ms524876%28v%3Dvs.90%29)
- Recommended action: `Keep unsupported in the lexical registry; extraction requires an ASP-aware parser that tracks script regions and directives.`
- Notes: `VBScript apostrophe comments and JScript slash comments are valid only inside regions assigned to those languages. HTML comments are returned as page markup rather than removed as server comments, and the same <!-- ... --> delimiters carry executable #include directives. A global regex would therefore overmatch HTML text, URLs, string apostrophes, or server-side directives.`

- Example - context-dependent forms:
```asp
<%@ LANGUAGE="JScript" %>
<% // JScript comment %>
<!-- #include file="header.inc" -->
```

## Clean
- Registry key: `clean`
- Version scope: `Clean 2.2 language report and compiler master at 0db3c25`
- Version-specific syntax: `No comment-syntax difference found between the language report and current compiler.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at newline; block comments use balanced delimiter matching`
- Nested comments: `supported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Clean 2.2 language report](https://clean.cs.ru.nl/download/doc/CleanLangRep.2.2.pdf)
- Implementation source: [Clean compiler scanner](https://gitlab.science.ru.nl/clean-compiler-and-rts/compiler/-/blob/master/frontend/scanner.icl)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with line and nested block fixtures.`
- Notes: `The report grammar recursively embeds Comment inside /* ... */. The compiler scanner likewise calls ScanComment recursively for a nested /* opener and resumes the outer scan after the nested close.`

- Example - line:
```clean
Start = 0 // note
```
- Example - nested block:
```clean
/* outer /* note */ outer */
Start = 0
```

## Click
- Registry key: `click`
- Version scope: `Click master at 9197a59 and the bundled click(5) language manual`
- Version-specific syntax: `The manual and lexer agree; column-zero hash forms are line directives rather than comments.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at newline; block comments stop at the first closing delimiter`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Click language manual](https://github.com/kohler/click/blob/master/doc/click.5)
- Implementation source: [Click lexer](https://github.com/kohler/click/blob/master/lib/lexer.cc)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with line and non-nested block fixtures.`
- Notes: `The lexer skips // to the line ending and scans /* until the first */ without maintaining nesting depth. Hash-prefixed lines are parsed by process_line_directive and must not be extracted as comments.`

- Example - line:
```click
src -> queue; // note
queue -> sink;
```
- Example - block:
```click
src -> /* note */ queue;
```

## CLIPS
- Registry key: `clips`
- Version scope: `CLIPS 6.4 Basic Programming Guide and CLIPS 6.40 scanner mirror`
- Version-specific syntax: `No block-comment syntax is documented or implemented.`
- Line comments: `;`
- Block comments: `unsupported`
- Termination behavior: `end of line`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [CLIPS 6.4 Basic Programming Guide](https://www.clipsrules.net/documentation/v642/bpg642.pdf)
- Implementation source: [CLIPS scanner](https://github.com/noxdafox/clips/blob/master/core/scanner.c)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with semicolon line-comment fixtures.`
- Notes: `The 6.4 guide says a semicolon starts a comment and also acts as a delimiter. GetToken removes semicolon comments while skipping whitespace and has no logic for CLIPS block comments.`

- Example - line:
```text
; note
(defrule example)
```

## Clojure
- Registry key: `clojure`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `;`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://clojure.org/reference/reader
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line-comment and reader-comment tests.`
- Notes: `Reader comments use #_ and discard the next form rather than acting like a block comment.`

- Example - line:
```clojure
; comment
(def x 1)
```
- Example - reader comment:
```clojure
#_(def x 1)
(def y 2)
```

## Closure Templates
- Registry key: `closure_templates`
- Version scope: `Closure Templates master at 7f50e1f`
- Version-specific syntax: `The current Soy reference documents slash comments; the older {* ... *} form is not used by the current parser.`
- Line comments: `// after whitespace or at the start of a Soy lexical context`
- Block comments: `/* ... */`
- Termination behavior: `line comments end at newline; block comments stop at the first closing delimiter`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs_plus_implementation`
- Docs source: [Soy comments reference](https://github.com/google/closure-templates/blob/master/documentation/reference/comments.md)
- Implementation source: [Soy parser grammar](https://github.com/google/closure-templates/blob/master/java/src/com/google/template/soy/soyparse/SoyFileParser.jj)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Implemented in the registry with Soy line and non-nested block fixtures.`
- Notes: `SoyFileParser.jj treats // as a comment only in parser states where it cannot be confused with URI schemes, requiring leading whitespace in template text. Multiline and SoyDoc comments enter comment states on /* or /** and close on the first */.`

- Example - line:
```soy
{template .main}
  // note
{/template}
```
- Example - block:
```soy
{template .main}
  /* note */
{/template}
```

## Cloud Firestore Security Rules
- Registry key: `cloud_firestore_security_rules`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://firebase.google.com/docs/firestore/security/rules-structure
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line-comment coverage only; the reviewed docs do not document block comments.`
- Notes: `Official rules examples use // comments inside security rules.`

- Example - line:
```text
// comment
match /databases/{database}/documents {
  allow read: if true;
}
```

## CMake
- Registry key: `cmake`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `#[[ ... ]]` with depth-qualified bracket comments
- Termination behavior: `depth-qualified delimiters`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://cmake.org/cmake/help/latest/manual/cmake-language.7.html
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed both line and bracket-comment coverage, including nested bracket depth.`
- Notes: `Bracket comments can use increasing = depth to avoid delimiter collisions.`

- Example - line:
```cmake
# comment
set(VAR value)
```
- Example - block:
```cmake
#[[ comment ]]
set(VAR value)
```
- Example - nested:
```cmake
#[=[
outer
#[[ inner ]]
]=]
set(VAR value)
```

## CODEOWNERS
- Registry key: `codeowners`
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
- Recommended action: `Seed hash-comment tests and keep the parser minimal.`
- Notes: `Comments are configuration-only.`

- Example - line:
```text
# comment
* @owner
```

## CodeQL
- Registry key: `codeql`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://codeql.github.com/docs/ql-language-reference/
- Implementation source: https://codeql.github.com/docs/ql-language-reference/ql-language-specification/
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed one-line and multiline comment tests; keep QLDoc separate if you need doc-comment fixtures.`
- Notes: `The QL docs distinguish standard comments from QLDoc comments.`

- Example - line:
```text
// comment
select 1
```
- Example - block:
```text
/* comment */
select 1
```

## CoffeeScript
- Registry key: `coffeescript`
- Version scope: `CoffeeScript reference site, reviewed 2026-05-22.`
- Version-specific syntax: `No comment-token split confirmed between 1.x and 2.x.`
- Line comments: `#`
- Block comments: `### ... ###`
- Termination behavior: `end of line for #; first closing ### wins for block comments`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `official_docs`
- Docs source: [CoffeeScript language reference](https://coffeescript.org/)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with line and block fixtures.`
- Notes: `The reference examples use # comments and triple-hash block comments.`

- Example - line:
```coffee
x = 1
# comment
y = 2
```
- Example - block:
```coffee
x = 1
###
comment
###
y = 2
```

## ColdFusion
- Registry key: `coldfusion`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `<!--- ... --->`
- Termination behavior: `true nesting supported`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://helpx.adobe.com/coldfusion/developing-applications/the-cfml-programming-language/elements-of-cfml/comments.html
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed nested CFML block-comment coverage.`
- Notes: `Adobe documents nested CFML comments and inline placement inside tags and expressions.`

- Example - block:
```text
<!--- comment --->
<cfset x = 1>
```
- Example - nested:
```text
<!--- disable this code
<!--- display error message --->
<cfset errormessage1="Oops!">
<cfoutput>
#errormessage1#
</cfoutput>
--->
```

## ColdFusion CFC
- Registry key: `coldfusion_cfc`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `<!--- ... --->`
- Termination behavior: `true nesting supported`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://helpx.adobe.com/coldfusion/developing-applications/the-cfml-programming-language/elements-of-cfml/comments.html
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed nested CFML block-comment coverage for component files.`
- Notes: `CFC files share the CFML comment rules documented by Adobe.`

- Example - block:
```text
<cfcomponent>
  <!--- comment --->
</cfcomponent>
```
- Example - nested:
```text
<cfcomponent>
  <!--- disable this code
  <!--- display error message --->
  <cfset errormessage1="Oops!">
  <cfoutput>
  #errormessage1#
  </cfoutput>
  --->
</cfcomponent>
```

## COLLADA
- Registry key: `collada`
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
- Recommended action: `Seed XML-comment tests for COLLADA assets.`
- Notes: `XML-based file format.`

- Example - block:
```xml
<COLLADA>
  <!-- comment -->
</COLLADA>
```

## Common Workflow Language
- Registry key: `common_workflow_language`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://www.commonwl.org/user_guide/introduction/quick-start.html
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed hash-comment tests in YAML-backed CWL sources.`
- Notes: `The official CWL guide explicitly says comments start with #.`

- Example - line:
```text
# comment
cwlVersion: v1.2
```

## Component Pascal
- Registry key: `component_pascal`
- Version scope: `Oberon microsystems Component Pascal language report for BlackBox/Component Pascal.`
- Version-specific syntax: `No dialect split found in the checked language report; Component Pascal uses only Oberon-family nested (* ... *) comments, not Pascal { ... } comments or // line comments.`
- Line comments: `unsupported`
- Block comments: `(* ... *)`
- Termination behavior: `block comments require balanced nested delimiters`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: [Component Pascal language report](https://blackbox.oberon.org/cp-lang.pdf)
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Seed nested (* ... *) block comments only; keep line comments and Pascal brace comments unsupported.`
- Notes: `The language report explicitly says comments may be nested, so a non-recursive Pascal-style matcher would be wrong for Component Pascal.`

- Example - block:
```text
(* comment *)
MODULE Example;
```
- Example - nested:
```text
(* outer (* inner *) outer *)
MODULE Example;
```

## CoNLL-U
- Registry key: `conll_u`
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
- Recommended action: `Seed hash-comment tests for annotation lines.`
- Notes: `Standard CoNLL-U comment marker.`

- Example - line:
```text
# comment
1	This	_	PRON	_	_	0	root	_	_
```

## Cool
- Registry key: `cool`
- Version scope: `Stanford Cool reference manual and Stanford cooldist lexer assignment skeleton.`
- Version-specific syntax: `No version split found; the reference manual defines -- line comments and nested (* ... *) comments.`
- Line comments: `--`
- Block comments: `(* ... *)`
- Termination behavior: `line comments run to newline or EOF; block comments require balanced nested delimiters and cannot cross file boundaries`
- Nested comments: `yes`
- Confidence: `verified`
- Evidence mode: `implementation_cross_checked`
- Docs source: [The Cool Reference Manual](https://theory.stanford.edu/~aiken/software/cool/cool-manual.pdf)
- Implementation source: [Stanford cool.flex skeleton](https://theory.stanford.edu/~aiken/software/cooldist/assignments/PA2/cool.flex.SKEL)
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Seed -- line comments and recursively nested (* ... *) block comments.`
- Notes: `The manual states that -- runs to newline or EOF, block comments may nest, and comments cannot cross file boundaries.`

- Example - line:
```text
-- comment
class Main inherits IO {
}
```
- Example - block:
```text
(* comment *)
class Main inherits IO {
}
```
- Example - nested:
```text
(* outer (* inner *) outer *)
class Main inherits IO {
}
```

## Creole
- Registry key: `creole`
- Version scope: `WikiCreole 1.0 final specification and published WikiCreole 1.0 ANTLR grammar without extensions.`
- Version-specific syntax: `The checked 1.0 specification and grammar define wiki markup constructs but no comment delimiters; engine-specific macro names such as "Comment" are not Creole comments.`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [WikiCreole home/spec site](https://www.wikicreole.org/)
- Implementation source: [WikiCreole 1.0 ANTLR grammar without extensions](https://dirkriehle.com/wp-content/uploads/2008/01/creole10_wout_extension.g)
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Keep unsupported unless a specific wiki-engine dialect with comment markup is split into its own registry key.`
- Notes: `The grammar has tokens for headings, lists, tables, links, images, nowiki, and escapes, but no comment token.`

- Example - unsupported:
```text
This is ordinary Creole text.
//this is emphasis, not a comment//
```

## CSON
- Registry key: `cson`
- Version scope: `bevry/cson 8.4.0 README, groupon/cson-parser 4.0.9 package, and CoffeeScript 1.x/2.x comment syntax.`
- Version-specific syntax: `CSON is CoffeeScript Object Notation; no CSON-specific syntax split found. Implement the CoffeeScript comment union used by CSON parsers: # line comments and ### ... ### block comments.`
- Line comments: `#`
- Block comments: `### ... ###`
- Termination behavior: `line comments run to newline; block comments stop at the first closing ###`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [bevry CSON README](https://github.com/bevry/cson); [CoffeeScript comments reference](https://coffeescript.org/#comments)
- Implementation source: [groupon cson-parser package](https://www.npmjs.com/package/cson-parser); [cson-parser 4.0.9 tarball](https://registry.npmjs.org/cson-parser/-/cson-parser-4.0.9.tgz)
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Seed # line and non-nested ### block comments.`
- Notes: `The CSON README demonstrates # comments and describes CSON as CoffeeScript object notation; cson-parser builds a CoffeeScript AST, so CoffeeScript's herecomment form is the block-comment source of truth.`

- Example - line:
```text
# comment
key: value
```
- Example - block:
```text
###
comment
###
key: value
```

## Csound
- Registry key: `csound`
- Version scope: `Csound 6.18 canonical manual, current Csound 7 score/orchestra docs, and language-csound grammar master.`
- Version-specific syntax: `Current orchestra docs add // line comments alongside the traditional semicolon form; current score docs also add the score-only c comment statement. For the generic Csound/orchestra key, implement ;, //, and /* ... */.`
- Line comments: `;` and `//`
- Block comments: `/* ... */`
- Termination behavior: `line comments run to newline; block comments stop at the first closing */`
- Nested comments: `unsupported`
- Confidence: `verified`
- Evidence mode: `implementation_cross_checked`
- Docs source: [Csound orchestra syntax](https://csound.com/docs/manual/OrchTop.html); [Csound get started comments](https://csound.com/get-started.html)
- Implementation source: [language-csound grammar](https://github.com/nwhetsell/language-csound/blob/master/grammars/csound.cson)
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Seed ;, //, and non-nested /* ... */ tests for orchestra-style Csound.`
- Notes: `The syntax-highlighting grammar uses a simple begin/end rule for block comments, so there is no evidence of nested /* ... */ support. Score-only c comments belong under the Csound Score key.`

- Example - line:
```text
; comment
instr 1
endin
```
- Example - line:
```text
instr 1
  a1 oscili 0.5, 440 // comment
endin
```
- Example - block:
```text
/* comment */
instr 1
endin
```

## Csound Document
- Registry key: `csound_document`
- Version scope: `Csound 6.18 unified .csd manual, current Csound 7 docs, and language-csound document grammar master.`
- Version-specific syntax: `.csd files are sectioned documents: CsOptions allows line-start # or ;, CsInstruments uses orchestra comments, and CsScore uses score comments. Do not treat XML/HTML comments as a universal Csound-document delimiter unless an HTML/XML-aware parser is in use.`
- Line comments: `;` and `//`; line-start `#` in `<CsOptions>`; score statement `c` in `<CsScore>`
- Block comments: `/* ... */`
- Termination behavior: `line comments run to newline; block comments stop at the first closing */`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [Csound unified file format](https://csound.com/docs/manual/CommandUnifile.html); [Csound getting started .csd example](https://csound.com/docs/manual/PrefaceGettingStarted.html); [Csound score statements](https://csound.com/docs/manual/ScoreStatements.html)
- Implementation source: [language-csound document grammar](https://github.com/nwhetsell/language-csound/blob/master/grammars/csound-document.cson); [language-csound score grammar](https://github.com/nwhetsell/language-csound/blob/master/grammars/csound-score.cson); [language-csound orchestra grammar](https://github.com/nwhetsell/language-csound/blob/master/grammars/csound.cson)
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Seed semicolon, double-slash, and block comments; add context-aware or line-anchored coverage for CsOptions # and CsScore c if the registry can express those restrictions.`
- Notes: `A global # or c comment rule would overmatch outside the documented sections; the document grammar embeds Csound and Csound Score grammars by tag context.`

- Example - line:
```text
<CsoundSynthesizer>
<CsOptions>
# comment
</CsOptions>
</CsoundSynthesizer>
```
- Example - line:
```text
<CsoundSynthesizer>
<CsInstruments>
instr 1
  a1 oscili 0.5, 440 ; comment
endin
</CsInstruments>
</CsoundSynthesizer>
```
- Example - block:
```text
<CsoundSynthesizer>
<CsInstruments>
/* comment */
instr 1
endin
</CsInstruments>
</CsoundSynthesizer>
```

## Csound Score
- Registry key: `csound_score`
- Version scope: `Legacy Csound 3.48 score manual, Csound 6.18 manual, current Csound 7 score statements, and language-csound score grammar master.`
- Version-specific syntax: `Older score docs document semicolon-only comments; current score docs document semicolon, //, and c-to-newline comments plus C-style block comments. Implement the current union for the score key.`
- Line comments: `;`, `//`, and score comment statement `c`
- Block comments: `/* ... */`
- Termination behavior: `line comments run to newline; block comments stop at the first closing */`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [Current Csound score statements](https://csound.com/docs/manual/ScoreStatements.html); [Legacy numeric score syntax](https://www.classes.cs.uchicago.edu/archive/1999/spring/CS295/Computing_Resources/Csound/CsManual3.48b1.HTML/NumScore/scsynt.html)
- Implementation source: [language-csound score grammar](https://github.com/nwhetsell/language-csound/blob/master/grammars/csound-score.cson); [language-csound shared comments grammar](https://github.com/nwhetsell/language-csound/blob/master/grammars/csound.cson)
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Seed ;, //, line-start c, and non-nested /* ... */ coverage for score files.`
- Notes: `The current official score docs are stronger than the TextMate grammar for the score-only c form, so tests should line-anchor c to avoid overmatching ordinary p-field text.`

- Example - line:
```text
; comment
f 1 0 1024 10 1
```
- Example - line:
```text
// comment
i 1 0 1
```
- Example - line:
```text
c comment
i 1 0 1
```
- Example - block:
```text
/* comment */
i 1 0 1
```

## CSS
- Registry key: `css`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `unsupported`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: [MDN CSS comments](https://developer.mozilla.org/en-US/docs/Web/CSS/Comments)
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed block-comment tests and keep line-comments unsupported.`
- Notes: `CSS does not define line comments.`

- Example - block:
```css
body {
  /* comment */
  color: black;
}
```

## CSV
- Registry key: `csv`
- Version scope: `RFC 4180 CSV, RFC 7111 URI fragments for CSV, and Python 3 csv module dialect surface.`
- Version-specific syntax: `Core CSV has records, fields, quoting, and line breaks but no comment delimiter; some tools add dialect-specific comment options, which should not be unioned into the generic CSV key.`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180); [RFC 7111](https://www.rfc-editor.org/rfc/rfc7111)
- Implementation source: [Python csv module](https://docs.python.org/3/library/csv.html)
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Document as commentless unless a specific dialect is introduced.`
- Notes: `A leading #, semicolon, or slash sequence is ordinary field data in generic CSV.`

- Example - unsupported:
```text
# not a standard CSV comment
name,value
```

## CUE
- Registry key: `cue`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://cuelang.org/docs/reference/spec/
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line/block tests and keep nesting unsupported unless spec evidence changes.`
- Notes: `Candidate verified against the CUE spec.`

- Example - line:
```cue
x: 1
// comment
y: 2
```
- Example - block:
```cue
x: 1
/* comment */
y: 2
```

## Cue Sheet
- Registry key: `cue_sheet`
- Version scope: `CDRWIN-derived cue-sheet syntax as summarized by cue-sheet references, libcue 2.3.0 parser, and libodraw cue-sheet format notes.`
- Version-specific syntax: `REM is the standard cue-sheet remark command. Some parsers/documentation also mention semicolon and // comments as non-standard/cdrdao-style variants. No reviewed source confirms # as a cue-sheet comment marker, so do not seed #.`
- Line comments: `REM`; dialect candidates `;` and `//`
- Block comments: `unsupported`
- Termination behavior: `line comments run to newline`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [Hydrogenaudio cue sheet reference](https://wiki.hydrogenaudio.org/index.php?title=Cue_sheet); [CUE sheet format notes](https://github.com/libyal/libodraw/blob/main/documentation/CUE%20sheet%20format.asciidoc)
- Implementation source: [libcue scanner](https://github.com/lipnitsk/libcue/blob/master/cue_scanner.l); [libcue parser](https://github.com/lipnitsk/libcue/blob/master/cue_parser.y)
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Seed line-anchored REM only for the generic key; consider ; and // only if the registry intentionally targets permissive cue-sheet dialects.`
- Notes: `REM is parsed as a command, not a free-form delimiter, and some applications reject a bare REM line. The packet's # candidate was not corroborated.`

- Example - line:
```text
REM comment
TRACK 01 AUDIO
```
- Example - dialect line:
```text
; comment
TRACK 01 AUDIO
```

## Curry
- Registry key: `curry`
- Version scope: `unresolved`
- Version-specific syntax: `unresolved`
- Line comments: `--`
- Block comments: `{- ... -}`
- Termination behavior: `true nesting supported`
- Nested comments: `yes`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed nested block coverage and add Haskell-like comment tests.`
- Notes: `Curry follows Haskell-style comment delimiters.`

- Example - line:
```text
-- comment
main :: IO ()
```
- Example - block:
```text
{- comment -}
main :: IO ()
```
- Example - nested:
```text
{- outer {- inner -} outer -}
main :: IO ()
```

## CWeb
- Registry key: `cweb`
- Version scope: `Knuth/Levy CWEB 4.12.2 manual, CWEBx manual notes, and mirrored CWEB source behavior.`
- Version-specific syntax: `CWEB mixes TeX text, C/C++/Java code, and CWEB control text. CWEB-specific @q ... @> control text is ignored by CTANGLE and CWEAVE; C/C++ comments are valid only in C text; TeX % comments are valid only in TeX text. Do not implement an unconditional union without a CWEB-aware parser.`
- Line comments: `// in C++/Java code fragments; % in TeX text`
- Block comments: `@q ... @>` on one source line; `/* ... */` in C/C++/Java code fragments`
- Termination behavior: `@q control text ends at the next @> on the same line; C block comments stop at the first closing delimiter; line comments end at newline`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `implementation_cross_checked`
- Docs source: [CWEB manual 4.12.2](https://mirrors.ctan.org/web/c_cpp/cweb/cwebman.pdf); [Knuth CWEB page](https://www-cs-faculty.stanford.edu/~knuth/cweb.html); [CWEBx manual](https://ctan.math.illinois.edu/web/c_cpp/cwebx/manual.pdf)
- Implementation source: [CWEB CTANGLE source mirror](https://github.com/ascherer/cweb/blob/master/ctangle.w)
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Prefer a CWEB-aware extractor. If a lexical registry entry is required, seed @q ... @> as the CWEB-specific comment form and document C/TeX comments as context-dependent.`
- Notes: `The manual warns that C comments inside CWEB must be valid TeX text for CWEAVE, and comments are not permitted in inline |...| C text.`

- Example - block:
```text
@q source-only note@>
@* Introduction.
```
- Example - block:
```text
@c
int value = 1; /* C fragment comment */
```
- Example - line:
```text
This TeX text is copied by CWEAVE. % TeX comment
@c
int value = 1; // C++ fragment comment
```

## Cycript
- Registry key: `cycript`
- Version scope: `Cycript 0.9.594 official site/manual plus ECMAScript and Objective-C/C-family comment syntax.`
- Version-specific syntax: `No Cycript-specific comment delimiter split found. Cycript is a JavaScriptCore-backed JavaScript console with Objective-C++ syntax, so C-family // and /* ... */ comments are the supported lexical forms.`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `line comments run to line terminator; block comments stop at the first closing */`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: [Cycript manual](https://www.cycript.org/manual/); [Cycript official site](https://www.cycript.org/); [ECMAScript lexical grammar](https://tc39.es/ecma262/#sec-comments)
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `not used`
- Recommended action: `Seed // and non-nested /* ... */ tests.`
- Notes: `The manual describes the REPL input as JavaScript executed by JavaScriptCore and syntax-highlighted by Cycript's lexer; Objective-C++ fragments use the same C-family comment forms.`

- Example - line:
```text
// comment
var x = 1;
```
- Example - block:
```text
/* comment */
var x = 1;
```

## Cython
- Registry key: `cython`
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
- Recommended action: `Seed hash-comment tests and keep block comments unsupported.`
- Notes: `Python-style comment syntax.`

- Example - line:
```cython
cdef int x = 1
# comment
cdef int y = 2
```
