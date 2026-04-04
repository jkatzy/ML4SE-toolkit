# Chunk 2 D-F Comment Research Report

This report follows the online-first research workflow from
`docs/comment_research/online_research_playbook.md` and the section layout in
`docs/comment_research/report_template.md`.

`unresolved` means the syntax was not justified well enough to encode with
confidence. `first closing delimiter wins` means a non-nesting block comment.
`true nesting supported` means comment openers may appear inside the block form
and still resolve correctly.

## Dafny

- Registry key: `dafny`
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `true nesting supported`
- Nested comments: `supported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://dafny.org/v4.6.0/DafnyRef/DafnyRef`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add line, block, and nested-block regression tests.
- Notes: nested block comments are part of the documented language behavior.

### Examples

#### Line comment
```text
method Main() {
  var x := 0; // keep zero
  assert x == 0;
}
```

#### Block comment
```text
method Main() {
  /* prepare state */
  var x := 0;
  assert x == 0;
}
```

#### Nested comment
```text
method Main() {
  /* outer /* inner */ outer */
  var x := 0;
  assert x == 0;
}
```

## DataWeave

- Registry key: `dataweave`
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://docs.mulesoft.com/dataweave/latest/dataweave-language-introduction`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add line and block tests; keep nesting explicitly out of scope.
- Notes: do not infer nesting from C-like syntax.

### Examples

#### Line comment
```text
%dw 2.0
output application/json
---
{
  name: "Ada" // note
}
```

#### Block comment
```text
/* note */
%dw 2.0
output application/json
---
1
```

## Debian Package Control File

- Registry key: `debian_package_control_file`
- Line comments: `#` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.debian.org/doc/debian-policy/ch-controlfields.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one line-comment fixture around a minimal control file.
- Notes: inline `#` inside field values should not be treated as comments unless the policy says so.

### Examples

#### Line comment
```text
Source: demo
# keep this field while testing
Package: demo
Version: 1.0
```

## DenizenScript

- Registry key: `denizenscript`
- Version scope: `Current Denizen Beginner's Guide and Meta Documentation pages; reviewed the maintained DenizenCore/Denizen docs surface rather than an archived legacy release.`
- Version-specific syntax: `No version split confirmed; the current docs use # to comment out whole command lines, so keep the verified line-comment form only and do not infer block syntax.`
- Line comments: `#` likely supported
- Block comments: `unresolved`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `medium`
- Docs source: `https://guide.denizenscript.com/guides/basics/mechanisms.html; https://guide.denizenscript.com/guides/troubleshooting/common-mistakes; https://meta.denizenscript.com/Docs/Commands/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `https://github.com/mcmonkeyprojects/DenizenSampleScripts`
- Corpus fallback source: `https://github.com/mcmonkeyprojects/DenizenSampleScripts`
- Recommended action: verify the comment form against an official parser or docs page before registry changes.
- Notes: sample scripts use leading `#` comment lines, and the current official docs also show `#` used to comment out command lines.

### Examples

#### Line comment
```text
demo_world:
  type: world
  events:
  on server start:
  - narrate "hello"
  # keep the startup narrate
  - narrate "done"
```

## desktop

- Registry key: `desktop`
- Line comments: `#` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://specifications.freedesktop.org/desktop-entry-spec/latest/basic-format.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add a simple `.desktop` line-comment regression test.
- Notes: the spec is INI-like.

### Examples

#### Line comment
```text
[Desktop Entry]
Name=Demo
# keep icon stable
Icon=demo
```

## Dhall

- Registry key: `dhall`
- Line comments: `--` supported
- Block comments: `{- ... -}` supported
- Termination behavior: `true nesting supported`
- Nested comments: `supported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://docs.dhall-lang.org/tutorials/Language-Tour.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add line and nested-block tests.
- Notes: nested block comments are important to lock.

### Examples

#### Line comment
```text
let x = 1 -- keep this binding
in x
```

#### Block comment
```text
{- note -}
let x = 1
in x
```

#### Nested comment
```text
{- outer {- inner -} outer -}
let x = 1
in x
```

## Diff

- Registry key: `diff`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.gnu.org/software/diffutils/manual/html_node/Unified-Format.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: leave unsupported.
- Notes: unified diff is a patch format, not a comment-bearing language.

## DIGITAL Command Language

- Registry key: `digital_command_language`
- Line comments: `!` supported, with `$!` used for whole comment lines in procedures
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://wiki.vmssoftware.com/Comment`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one `!` inline comment fixture and one `$!` full-line fixture.
- Notes: DCL scripts require `$` in column 1 for commands.

### Examples

#### Line comment
```text
$ write sys$output "hello" ! keep this output
$! This whole line is ignored
$ write sys$output "done"
```

## dircolors

- Registry key: `dircolors`
- Line comments: `#` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.gnu.org/software/coreutils/manual/html_node/dircolors-invocation.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one config-file comment fixture.
- Notes: treat it like a shell-style config file.

### Examples

#### Line comment
```text
# color rules for testing
TERM xterm
DIR 01;34
```

## DirectX 3D File

- Registry key: `directx_3d_file`
- Line comments: `//` and `#` supported in text files
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://learn.microsoft.com/en-us/windows/win32/direct3d9/reserved-words--header--and-comments`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one `//` example and one `#` example for text `.x` files.
- Notes: comments are applicable only to text-encoded `.x` files.

### Examples

#### Line comment
```text
Frame Root {
  // keep the mesh root
  Mesh demo {
  }
}
```

#### Line comment
```text
Frame Root {
  # keep the mesh root
  Mesh demo {
  }
}
```

## DM

- Registry key: `dm`
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `true nesting supported`
- Nested comments: `supported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.byond.com/docs/ref/info.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add line, block, and nested-block tests.
- Notes: the BYOND reference explicitly says multi-line comments may be nested.

### Examples

#### Line comment
```text
var/x = 1
// keep the next assignment
var/y = 2
```

#### Block comment
```text
var/x = 1
/* note */
var/y = 2
```

#### Nested comment
```text
var/x = 1
/* outer /* inner */ outer */
var/y = 2
```

## DNS Zone

- Registry key: `dns_zone`
- Line comments: `;` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.rfc-editor.org/rfc/rfc1035`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one minimal zone-file line-comment test.
- Notes: semicolon comments are standard zone-file syntax.

### Examples

#### Line comment
```text
$ORIGIN example.com.
@   IN SOA ns1.example.com. hostmaster.example.com. (
        1   ; serial
        3600 ; refresh
)
```

## Dockerfile

- Registry key: `dockerfile`
- Line comments: `#` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://docs.docker.com/reference/dockerfile/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add a line-comment regression test around a minimal Dockerfile.
- Notes: keep instruction arguments separate from comments.

### Examples

#### Line comment
```text
FROM alpine:3.20
# install the toolchain
RUN apk add --no-cache build-base
```

## DTrace

- Registry key: `dtrace`
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/dtrace-guide/dtrace.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: add line and block tests and keep nested blocks out of scope.
- Notes: the DTrace guide documents the comment delimiters directly.

### Examples

#### Line comment
```text
BEGIN
{
  printf("start\n"); // trace setup
}
```

#### Block comment
```text
/* note */
BEGIN
{
  printf("start\n");
}
```

## Dylan

- Registry key: `dylan`
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `true nesting supported`
- Nested comments: `supported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://opendylan.org/books/drm/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add line, block, and nested-comment tests.
- Notes: nested block comments are the key regression case.

### Examples

#### Line comment
```text
define method main ()
  // keep entry point
  format-out("hi\n");
end method;
```

#### Block comment
```text
define method main ()
  /* note */
  format-out("hi\n");
end method;
```

#### Nested comment
```text
define method main ()
  /* outer /* inner */ outer */
  format-out("hi\n");
end method;
```

## E

- Registry key: `e`
- Version scope: `Original E-on-Java specification pages, current ERights language pages, and 0.9-era examples that use pragma.syntax("0.9"); the exact comment policy was not pinned in the sources checked.`
- Version-specific syntax: `No comment-token split confirmed across the reviewed E materials; the sources expose the E/Kernel-E language family but do not explicitly document a stable comment delimiter, so keep this entry unresolved.`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Evidence mode: `unresolved`
- Confidence: `unresolved`
- Docs source: `https://erights.org/history/original-e/programmers/LanguageSpec.html; https://erights.org/elang/; https://erights.org/elang/quick-ref.html; https://erights.org/history/original-e/programmers/Econcepts.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: identify the exact language and source manual first.
- Notes: the language family is documented, but I did not find a defensible comment-token rule in the pages checked.

## E-mail

- Registry key: `e_mail`
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: parenthesized header comments are supported
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.rfc-editor.org/rfc/rfc5322`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one RFC 5322 header fixture with nested comments.
- Notes: this is header syntax, not programming-language comment syntax.

### Examples

#### Nested comment
```text
From: Alice (team (platform)) <alice@example.com>
Subject: status
```

## Eagle

- Registry key: `eagle`
- Version scope: `Autodesk EAGLE ULP docs in current Fusion Electronics help, plus the 2016 Autodesk ULP blog post and recent forum references to EAGLE 5/9.x behavior.`
- Version-specific syntax: `The reviewed ULP sources present C-like syntax and a sample that uses // comments; no separate block-comment rule was confirmed, so the registry should add only the verified line-comment form until a block form is pinned.`
- Line comments: `//` supported
- Block comments: `unresolved`
- Termination behavior: `runs to newline`
- Nested comments: `unresolved`
- Evidence mode: `official_docs`
- Confidence: `medium`
- Docs source: `https://help.autodesk.com/cloudhelp/ENU/Fusion-ECAD/files/ECD-WRITE-ULP-REF.htm; https://help.autodesk.com/cloudhelp/ENU/Fusion-ECAD/files/ECD-USER-LANG-REF.htm; https://www.autodesk.com/products/fusion-360/blog/what-you-didnt-know-about-eagle-user-language-programming/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: add the verified `//` line-comment fixture now and keep block syntax out of the registry until a source pins it.
- Notes: ULP is explicitly described as C-like, and the sample docs show `//` comments in actual ULP code.

## Easybuild

- Registry key: `easybuild`
- Line comments: `#` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://docs.easybuild.io/writing-easyconfig-files/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add a simple easyconfig comment test.
- Notes: keep it shell-like.

### Examples

#### Line comment
```text
# easyconfig test
name = "Demo"
version = "1.0"
```

## EditorConfig

- Registry key: `editorconfig`
- Line comments: `#` and `;` supported at the beginning of a line
- Block comments: `unsupported`
- Termination behavior: `runs to newline; inline comments are not part of the current spec`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `verified`
- Docs source: `https://spec.editorconfig.org/`
- Implementation source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: add one fixture for each line-comment prefix and a regression that inline `#` and `;` remain part of values.
- Notes: the current spec treats `#` or `;` as comments only at the beginning of a line; older parsers may still allow inline comments, but the modern spec rejects them.

### Examples

#### Line comment
```text
# top-level comment
; legacy-style comment
[*]
indent_style = space
```

## EBNF

- Registry key: `ebnf`
- Version scope: `ISO/IEC 14977:1996, the Cambridge ISO EBNF summary, Microsoft's EBNF-M page, and RFC 2234/5234 ABNF material used only for comparison because the Stack label is generic.`
- Version-specific syntax: `No canonical comment syntax was found for generic EBNF; the sources reviewed show that comment conventions are dialect-specific, so keep the label unresolved until a concrete EBNF dialect is pinned.`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Evidence mode: `unresolved`
- Confidence: `unresolved`
- Docs source: `https://iso.org/standard/26153.html; https://www.cl.cam.ac.uk/~mgk25/iso-ebnf.html; https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/8deb6d43-3e71-493b-9465-b84bb3cd3c45; https://datatracker.ietf.org/doc/rfc5234/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: identify the exact EBNF dialect in scope before adding syntax.
- Notes: EBNF is a grammar notation family, so the comment forms are dialect-specific rather than standardized by the family name alone.

## eC

- Registry key: `ec`
- Version scope: `Current Ecere SDK / eC project materials plus the 2017 Ecere overview article; I did not find a versioned grammar page that pinned comment syntax.`
- Version-specific syntax: `No version split or dialect split was confirmed in the reviewed sources; the language is described as C-style, but that is not sufficient to encode a comment token safely without an authoritative reference.`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Evidence mode: `unresolved`
- Confidence: `unresolved`
- Docs source: `https://opensource.com/article/17/9/ecere; https://github.com/ecere/ecere-sdk`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: verify the Ecere/eC reference before encoding comment syntax.
- Notes: the source material confirms the language family and its C-style framing, but not a specific comment rule.

## ECL

- Registry key: `ecl`
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://hpccsystems.com/wp-content/uploads/_documents/ECLR_EN_US/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: add line and block tests.
- Notes: the ECL language reference explicitly documents both comment forms.

### Examples

#### Line comment
```text
EXPORT Demo := FUNCTION
  // keep result stable
  RETURN 1;
END;
```

#### Block comment
```text
EXPORT Demo := FUNCTION
  /* note */
  RETURN 1;
END;
```

## ECLiPSe

- Registry key: `eclipse`
- Line comments: `%` supported
- Block comments: `/* ... */` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://eclipseclp.org/doc/bips/kernel/directives/comment-2.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add percent-line and slash-block tests.
- Notes: the docs explicitly distinguish comment directives from normal `%` and `/* ... */` comments.

### Examples

#### Line comment
```text
goal :-
    % keep the test deterministic
    write(hello).
```

#### Block comment
```text
goal :-
    /* note */
    write(hello).
```

## Edje Data Collection

- Registry key: `edje_data_collection`
- Version scope: `Legacy Edje reference material plus current Tizen EDC docs, including the Tizen 2.4+ layouting pages and the newer Tizen 5.x-era EDC editor/deprecation notes.`
- Version-specific syntax: `No version split was confirmed; the reviewed EDC examples use C-style block comments (/* ... */) in current docs, and I did not find an older dialect that changed the delimiter. If the registry targets .edc, add the block form only.`
- Line comments: `unresolved`
- Block comments: `/* ... */` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unresolved`
- Evidence mode: `official_docs`
- Confidence: `medium`
- Docs source: `https://docs.tizen.org/application/native/guides/ui/efl/learn-edc-intro/; https://docs.tizen.org/application/native/guides/ui/efl/learn-edc-positioning-parts/; https://www.enlightenment.org/_legacy_embed/edje_main.html; https://docs.tizen.org/application/tizen-studio/native-tools/edc-editor/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: add a block-comment regression test for .edc and keep line comments unresolved until a source pins them.
- Notes: the reviewed docs show /* ... */ inside EDC examples; I did not find a verified line-comment token.

## edn

- Registry key: `edn`
- Line comments: `;` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://github.com/edn-format/edn`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add a line-comment fixture.
- Notes: EDN keeps comment syntax minimal.

### Examples

#### Line comment
```text
{:name "Ada" ; keep metadata
 :lang "clj"}
```

## Eiffel

- Registry key: `eiffel`
- Line comments: `--` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.eiffel.org/doc/eiffel/Eiffel_Code_Comments`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one line-comment fixture and keep block-comment tests out of scope.
- Notes: the source I found documents line comments and comment markup, not block comments.

### Examples

#### Line comment
```text
class
  DEMO
feature
  run
    do
      -- keep the test simple
    end
end
```

## EJS

- Registry key: `ejs`
- Line comments: `unsupported`
- Block comments: `<%# ... %>` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://ejs.co/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add a template-comment test.
- Notes: EJS uses template tags rather than ordinary source-code comments.

### Examples

#### Block comment
```text
<ul>
  <%# template note %>
  <li><%= user.name %></li>
</ul>
```

## Elvish

- Registry key: `elvish`
- Line comments: `#` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://elv.sh/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add a single line-comment fixture.
- Notes: no block syntax was confirmed.

### Examples

#### Line comment
```text
put hello
# keep the output visible
put world
```

## Emacs Lisp

- Registry key: `emacs_lisp`
- Line comments: `;` supported
- Block comments: `#| ... |#` supported
- Termination behavior: `true nesting supported`
- Nested comments: `supported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.gnu.org/software/emacs/manual/html_node/elisp/Comments.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add line, block, and nested-block tests.
- Notes: nested block comments are the key behavior to lock.

### Examples

#### Line comment
```text
;; load the package
(setq x 1)
```

#### Block comment
```text
#| comment block |#
(setq x 1)
```

#### Nested comment
```text
#| outer #| inner |# outer |#
(setq x 1)
```

## EmberScript

- Registry key: `emberscript`
- Line comments: `#` supported
- Block comments: `### ... ###` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `corpus_inferred`
- Confidence: `medium`
- Docs source: `unresolved`
- Implementation source: `https://github.com/ghempton/ember-script`
- Community source: `https://packagecontrol.io/packages/EmberScript`
- Corpus fallback source: `https://packagecontrol.io/packages/EmberScript`
- Recommended action: keep this as a corpus-backed entry until an official syntax page or grammar is pinned.
- Notes: the corpus examples and package metadata show CoffeeScript-style semicolon-compatible line comments and triple-hash block comments.

### Examples

#### Line comment
```text
# keep the task simple
console.log user.name
```

#### Block comment
```text
###
template note
###
console.log user.name
```

## EQ

- Registry key: `eq`
- Version scope: `The Stack label was not pinned to a unique language or format; I checked generic EQ references and could not isolate an authoritative manual for a specific EQ dialect.`
- Version-specific syntax: `No defensible comment syntax was found; the label remains unresolved until the intended language or file format is identified.`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Evidence mode: `unresolved`
- Confidence: `unresolved`
- Docs source: `https://file.org/extension/eq; https://help.altair.com/compose/help/en_us/topics/reference/oml_language/CoreMinimalInterpreter/eq.htm`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: identify the language before adding syntax.
- Notes: the name collides with multiple unrelated EQ concepts, so I did not treat any of them as the intended language.

## Euphoria

- Registry key: `euphoria`
- Line comments: `--` supported
- Block comments: `/* ... */` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://openeuphoria.org/docs/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add line and block tests.
- Notes: nested blocks were not confirmed in the docs I checked.

### Examples

#### Line comment
```text
-- keep this branch
if x then
    puts(1, "hello")
end if
```

#### Block comment
```text
/* note */
if x then
    puts(1, "hello")
end if
```

## F*

- Registry key: `f_star`
- Line comments: `//` supported
- Block comments: `(* ... *)` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unresolved`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://fstar-lang.org/tutorial/book/part1/part1_getting_off_the_ground.html`
- Implementation source: `https://github.com/FStarLang/FStar`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: add line and block tests now; confirm nesting before encoding it as supported.
- Notes: the official tutorial explicitly documents both line and block comment delimiters.

### Examples

#### Line comment
```text
let x = 1 // keep this binding
in x
```

#### Block comment
```text
let x = 1
(* note *)
in x
```

## Factor

- Registry key: `factor`
- Line comments: `!` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://docs.factorcode.org/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one line-comment fixture.
- Notes: keep the syntax minimal.

### Examples

#### Line comment
```text
: add1 ( n -- n+1 )
  ! keep the stack example
  1 + ;
```

## Fantom

- Registry key: `fantom`
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://fantom.org/doc/docLang/CompilationUnits`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add line and block parse tests.
- Notes: the compilation-unit docs cover ordinary comment forms.

### Examples

#### Line comment
```text
class Demo {
  Void main() {
    // keep the example stable
    echo("hi")
  }
}
```

#### Block comment
```text
class Demo {
  /* note */
  Void main() {
    echo("hi")
  }
}
```

## Faust

- Registry key: `faust`
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://faustdoc.grame.fr/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add line and block tests.
- Notes: no nesting was confirmed.

### Examples

#### Line comment
```text
process = _; // keep this rule
```

#### Block comment
```text
/* note */
process = _;
```

## Fennel

- Registry key: `fennel`
- Line comments: `;` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `corpus_inferred`
- Confidence: `medium`
- Docs source: `unresolved`
- Implementation source: `https://github.com/bakpakin/Fennel`
- Community source: `https://github.com/bakpakin/Fennel`
- Corpus fallback source: `https://gist.github.com/technomancy/9bb2be6bd1a5d8a242be4124306a63c7`
- Recommended action: keep the corpus-backed line-comment rule and avoid inventing block syntax.
- Notes: the corpus examples show semicolon-style comments in real `.fnl` files.

### Examples

#### Line comment
```text
; keep the example readable
(print "hello")
```

## FIGlet Font

- Registry key: `figlet_font`
- Version scope: `FIGlet 2.2.1 FIGfont standard draft 2.0 plus parser docs for figlet v0.3.2; the sources also note that older FIGlet/FIGWin versions motivated the format.`
- Version-specific syntax: `The format uses a counted comment section after the header line rather than a token-based in-band delimiter; no alternate version split was confirmed, so treat the comments as file metadata rather than a source-code comment syntax.`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Evidence mode: `unresolved`
- Confidence: `unresolved`
- Docs source: `https://sources.debian.org/src/figlet/2.2.1-4/figfont.txt; https://www.figlet.org/figlet-man.html; https://hexdocs.pm/figlet/Figlet.Parser.FontFileParser.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: keep this unresolved unless the stack label is reclassified as FIGfont metadata rather than code comments.
- Notes: the "comments" are a counted section in the font file, not a token-delimited comment form.

## Filebench WML

- Registry key: `filebench_wml`
- Version scope: `Filebench 1.4.9.1 man-page material, the 1.5-alpha1 quick-start docs, and the current filebench GitHub wiki/repo examples.`
- Version-specific syntax: `No comment delimiter was confirmed in the reviewed WML sources; the versioned docs describe the workload structure and commands but do not pin a stable comment token, so keep the entry unresolved.`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Evidence mode: `unresolved`
- Confidence: `unresolved`
- Docs source: `https://github.com/filebench/filebench; https://github-wiki-see.page/m/filebench/filebench/wiki/Workload-model-language; https://www.mankier.com/package/filebench`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: verify the WML syntax from Filebench docs first.
- Notes: the reviewed WML docs describe workload structure and versioning, but not a defensible comment syntax.

## fish

- Registry key: `fish`
- Line comments: `#` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://fishshell.com/docs/4.0/language.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add a shell-function line-comment fixture.
- Notes: shell-style `#` comments are the baseline.

### Examples

#### Line comment
```text
function greet
  # keep the function body
  echo hello
end
```

## Fluent

- Registry key: `fluent`
- Line comments: `#`, `##`, and `###` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://projectfluent.org/fluent/guide/comments.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one test for each comment prefix.
- Notes: the marker count is meaningful.

### Examples

#### Line comment
```text
# translator note
brand-name = Example
```

#### Line comment
```text
## reviewer note
brand-name = Example
```

#### Line comment
```text
### document note
brand-name = Example
```

## FLUX

- Registry key: `flux`
- Version scope: `The label was not pinned to a specific language, file format, or versioned dialect; only the Stack v2 label and the ambiguous name were checked.`
- Version-specific syntax: `No versioned or dialect-specific comment syntax could be established, so leave this unresolved.`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Evidence mode: `unresolved`
- Confidence: `unresolved`
- Docs source: `unresolved`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: pin the exact FLUX language or format first.
- Notes: the name is ambiguous.

## Formatted

- Registry key: `formatted`
- Version scope: `The label was not pinned to a unique language or file format; the Stack v2 name alone does not identify an authoritative manual or dialect family.`
- Version-specific syntax: `No versioned or dialect-specific comment syntax could be established, so leave this unresolved.`
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Evidence mode: `unresolved`
- Confidence: `unresolved`
- Docs source: `unresolved`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `unresolved`
- Corpus fallback source: `unresolved`
- Recommended action: determine what "Formatted" refers to in Stack v2.
- Notes: no safe syntax assumptions can be made from the label alone.

## Fortran Free Form

- Registry key: `fortran_free_form`
- Line comments: `!` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://gcc.gnu.org/onlinedocs/gfortran/`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one line-comment fixture.
- Notes: keep block and nesting out of scope.

### Examples

#### Line comment
```text
program demo
  ! keep this print
  print *, "hi"
end program demo
```

## FreeBasic

- Registry key: `freebasic`
- Line comments: `'` and `Rem` supported
- Block comments: `/' ... '/` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unresolved`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://freebasic.net/wiki/ProPgComments`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add separate tests for apostrophe and `Rem` plus one block-comment fixture.
- Notes: nesting was not confirmed in the source I checked.

### Examples

#### Line comment
```text
' keep the print
print "hi"
```

#### Line comment
```text
REM keep the print
print "hi"
```

#### Block comment
```text
/' note '/
print "hi"
```

## FreeMarker

- Registry key: `freemarker`
- Line comments: `unsupported`
- Block comments: `<#-- ... -->` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://freemarker.apache.org/docs/dgui_quickstart_template.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add a template-comment test.
- Notes: comment syntax is template-tag based.

### Examples

#### Block comment
```text
<#-- template note -->
<#if user??>
  ${user}
</#if>
```

## Frege

- Registry key: `frege`
- Line comments: `--` supported
- Block comments: `{- ... -}` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `supported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.frege-lang.org/doc/Language.pdf`
- Implementation source: `https://github.com/Frege/frege`
- Community source: `https://www.frege-lang.org/doc/fregedoc.html`
- Corpus fallback source: `unresolved`
- Recommended action: add line, block, and nested-block tests.
- Notes: the Frege language draft states that block comments nest and that line comments extend to end of line.

### Examples

#### Line comment
```text
-- keep the example stable
main = putStrLn "hi"
```

#### Block comment
```text
{- note -}
main = putStrLn "hi"
```

#### Nested comment
```text
{- outer {- inner -} outer -}
main = putStrLn "hi"
```

## Futhark

- Registry key: `futhark`
- Line comments: `--` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://futhark.readthedocs.io/en/v0.25.25/language-reference.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Corpus fallback source: `unresolved`
- Recommended action: add one line-comment test and keep block/nesting out of scope.
- Notes: doc comments use the same line prefix.

### Examples

#### Line comment
```text
-- keep the binding stable
let x = 1
```
