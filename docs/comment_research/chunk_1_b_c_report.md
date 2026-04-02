# Chunk 1 B-C Research Report

This report is documentation-oriented and test-oriented. I kept unresolved items explicit instead of guessing.

## Ballerina
- Registry key: `ballerina`
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
- Recommended action: `Verify against the Beef language reference before seeding.`
- Notes: `Candidate C-like syntax.`

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

## Berry
- Registry key: `berry`
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
- Recommended action: `Verify against Berry docs and add hash-comment tests.`
- Notes: `Candidate hash-comment syntax.`

- Example - line:
```text
x = 1
# comment
y = 2
```

## BibTeX
- Registry key: `bibtex`
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
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: [Bicep file syntax](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/file)
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify the exact doc page and add C-like comment tests.`
- Notes: `Candidate based on Microsoft docs.`

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
- Line comments: `unresolved`
- Block comments: `<!-- ... -->` is the best candidate, but this needs verification.
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported` if HTML comments are the only supported form.
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research Bikeshed's parser/docs before adding a registry entry.`
- Notes: `Bikeshed mixes markup and metadata; comment handling may be inherited from HTML.`

- Example - block:
```text
<p>before</p>
<!-- comment -->
<p>after</p>
```

## BitBake
- Registry key: `bitbake`
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
- Recommended action: `Verify against Yocto/BitBake docs and add hash-comment tests.`
- Notes: `Candidate hash comments.`

- Example - line:
```text
SUMMARY = "Example"
# comment
LICENSE = "MIT"
```

## Blade
- Registry key: `blade`
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
- Recommended action: `Verify against the BlitzBasic reference and add semicolon-comment tests.`
- Notes: `Candidate semicolon comment syntax.`

- Example - line:
```text
Print "hello"
; comment
Print "world"
```

## BlitzMax
- Registry key: `blitzmax`
- Line comments: `Rem` and `'`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `official_docs`
- Docs source: [BlitzMax comments](https://blitzmax.org/docs/en/language/comments/)
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify dialect details and add tests for both line-comment forms.`
- Notes: `BASIC-like comment forms.`

- Example - line:
```text
Print "hello"
' comment
Print "world"
```
- Example - line:
```text
Print "hello"
Rem comment
Print "world"
```

## Bluespec
- Registry key: `bluespec`
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
- Recommended action: `Verify against the Bluespec language reference and add C-like comment tests.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```text
rule r;
  // comment
  x <= 1;
endrule
```
- Example - block:
```text
rule r;
  /* comment */
  x <= 1;
endrule
```

## Boo
- Registry key: `boo`
- Line comments: `#`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Research Boo comment syntax before seeding.`
- Notes: `Hash comments are likely; block comments need confirmation.`

- Example - line:
```text
x = 1
# comment
y = 2
```

## Boogie
- Registry key: `boogie`
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
- Recommended action: `Verify against the Boogie reference and add C-like comment tests.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```text
var x:int;
// comment
assume x > 0;
```
- Example - block:
```text
var x:int;
/* comment */
assume x > 0;
```

## Brainfuck
- Registry key: `brainfuck`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Document that non-command characters are ignored rather than treated as comments.`
- Notes: `Brainfuck does not define comment syntax; arbitrary non-instruction characters are ignored.`

- Example - unsupported:
```text
++[>+++<-]>.
This text is ignored by the interpreter.
```

## BrighterScript
- Registry key: `brighterscript`
- Line comments: `'` and `REM`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify against BrighterScript docs and add BASIC-style comment tests.`
- Notes: `BrightScript family syntax.`

- Example - line:
```text
x = 1
' comment
y = 2
```

## Brightscript
- Registry key: `brightscript`
- Line comments: `'` and `REM`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify against Roku docs and add BASIC-style comment tests.`
- Notes: `BrightScript family syntax.`

- Example - line:
```text
x = 1
' comment
y = 2
```

## Browserslist
- Registry key: `browserslist`
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
- Recommended action: `Confirm config-file comment handling and add hash-comment tests.`
- Notes: `Config-file syntax, not a general-purpose programming language.`

- Example - line:
```text
# comment
defaults
last 2 versions
```

## C2hs Haskell
- Registry key: `c2hs_haskell`
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
- Line comments: `--`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify against Cabal syntax docs and add line-comment tests.`
- Notes: `Cabal configuration files are Haskell-like, but block comments are not confirmed here.`

- Example - line:
```text
name: example
-- comment
version: 1.0
```

## Cadence
- Registry key: `cadence`
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
- Recommended action: `Verify against Cadence docs and add C-like comment tests.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```text
pub fun main() {
  // comment
  log("hello")
}
```
- Example - block:
```text
pub fun main() {
  /* comment */
  log("hello")
}
```

## CAP CDS
- Registry key: `cap_cds`
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
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify against CartoCSS docs before seeding.`
- Notes: `CSS-like syntax is likely, but line comments need confirmation.`

- Example - line:
```text
#layer {
  // comment
  line-color: #fff;
}
```

## Ceylon
- Registry key: `ceylon`
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
- Recommended action: `Verify against Ceylon docs and add C-like comment tests.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```text
shared void run() {
  // comment
  print("hi");
}
```
- Example - block:
```text
shared void run() {
  /* comment */
  print("hi");
}
```

## Chapel
- Registry key: `chapel`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify against Chapel docs and add C-like comment tests.`
- Notes: `Candidate C-like syntax.`

- Example - line:
```text
var x = 1;
// comment
var y = 2;
```
- Example - block:
```text
var x = 1;
/* comment */
var y = 2;
```

## Checksums
- Registry key: `checksums`
- Line comments: `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Confirm the file format before adding a registry entry.`
- Notes: `This looks like a data/config format; comment support is not standardized.`

- Example - line:
```text
# comment
deadbeef  file.txt
```

## ChucK
- Registry key: `chuck`
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
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify against the IL syntax docs and add C-style comment tests.`
- Notes: `Candidate based on IL assembly conventions.`

- Example - line:
```text
.method public static void Main() cil managed {
  // comment
}
```

## Cirru
- Registry key: `cirru`
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
- Recommended action: `Research Cirru syntax before adding registry support.`
- Notes: `No verified comment syntax gathered.`

## Clarion
- Registry key: `clarion`
- Line comments: `!`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Clarion comment syntax before seeding.`
- Notes: `Candidate Clarion comment marker.`

- Example - line:
```text
! comment
CODE
```

## Classic ASP
- Registry key: `classic_asp`
- Line comments: `unsupported`
- Block comments: `<!-- ... -->`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Treat as a mixed-language format and verify HTML/script comment handling separately.`
- Notes: `ASP pages can contain HTML, VBScript, and JScript; comment syntax depends on the embedded language.`

- Example - block:
```text
<html>
<!-- comment -->
<body>hello</body>
</html>
```

## Clean
- Registry key: `clean`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unresolved`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Clean comment nesting before seeding.`
- Notes: `C-like syntax is likely, but nesting was not verified.`

- Example - line:
```text
// comment
Start
```
- Example - block:
```text
/* comment */
Start
```

## Click
- Registry key: `click`
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
- Recommended action: `Add hash-comment tests after confirming the Click parser docs.`
- Notes: `Python-like command-line config syntax.`

- Example - line:
```text
# comment
@click.command()
def main():
    pass
```

## CLIPS
- Registry key: `clips`
- Line comments: `;`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify CLIPS comment syntax and add line/block tests.`
- Notes: `Candidate semicolon and block comment syntax.`

- Example - line:
```text
; comment
(defrule example)
```
- Example - block:
```text
/* comment */
(defrule example)
```

## Clojure
- Registry key: `clojure`
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
- Line comments: `unsupported`
- Block comments: `{* ... *}`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify Soy/Closure Templates comment syntax before seeding.`
- Notes: `Template comments are likely block-delimited.`

- Example - block:
```text
{namespace example}
{* comment *}
{template .main}
{/template}
```

## Cloud Firestore Security Rules
- Registry key: `cloud_firestore_security_rules`
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
- Line comments: `#`
- Block comments: `### ... ###`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `official_docs`
- Docs source: https://coffeescript.org/
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Seed line/block coverage and confirm block-comment stripping in tests.`
- Notes: `Block comments are triple-hash delimited.`

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
- Line comments: `unresolved`
- Block comments: `(* ... *)`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify before seeding; only the block delimiter is tentatively known.`
- Notes: `Pascal-family syntax often uses `(* ... *)`.`

- Example - block:
```text
(* comment *)
MODULE Example;
```

## CoNLL-U
- Registry key: `conll_u`
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
- Line comments: `--`
- Block comments: `(* ... *)`
- Termination behavior: `true nesting supported`
- Nested comments: `yes`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify COOL nesting semantics and add line/block tests.`
- Notes: `Candidate based on COOL language conventions.`

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
- Recommended action: `Research the wiki syntax before seeding.`
- Notes: `No verified comment syntax gathered.`

## CSON
- Registry key: `cson`
- Line comments: `#`
- Block comments: `### ... ###`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify against CSON docs and add CoffeeScript-style comment tests.`
- Notes: `CSON generally follows CoffeeScript conventions.`

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
- Line comments: `;`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `medium`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify against Csound docs and add line/block tests.`
- Notes: `Candidate semicolon and block comment syntax.`

- Example - line:
```text
; comment
instr 1
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
- Line comments: `;`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify the document dialect before seeding.`
- Notes: `Likely shares Csound comment forms.`

- Example - line:
```text
; comment
```

## Csound Score
- Registry key: `csound_score`
- Line comments: `;`
- Block comments: `/* ... */`
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify the score dialect before seeding.`
- Notes: `Likely shares Csound comment forms.`

- Example - line:
```text
; comment
f 1 0 1024 10 1
```

## CSS
- Registry key: `css`
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
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `high`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Document as commentless unless a specific dialect is introduced.`
- Notes: `CSV does not standardize comment syntax.`

## CUE
- Registry key: `cue`
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
- Line comments: `REM` and `#`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Confidence: `low`
- Evidence mode: `unresolved`
- Docs source: `unresolved`
- Implementation source: `unresolved`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: `Verify cue-sheet syntax before seeding.`
- Notes: `Audio cue sheets often use REM-style comments.`

- Example - line:
```text
REM comment
TRACK 01 AUDIO
```

## Curry
- Registry key: `curry`
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
- Recommended action: `Research WEB/CWEB comment conventions before seeding.`
- Notes: `TeX and C fragments make comment handling format-specific.`

## Cycript
- Registry key: `cycript`
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
- Recommended action: `Verify against Cycript docs and add C-like comment tests.`
- Notes: `Candidate C-like syntax.`

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
