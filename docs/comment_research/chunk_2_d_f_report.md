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
- Version scope: Current Denizen Beginner's Guide examples and current Denizen-Core script loader source; no older syntax split was found.
- Version-specific syntax: No version split confirmed. The current loader strips lines whose trimmed content starts with `#`; inline `#` in command lines is escaped rather than treated as a comment.
- Line comments: `#` full-line comments supported after optional leading whitespace; inline `#` comments are unsupported.
- Block comments: `unsupported`
- Termination behavior: `runs to newline; only recognized when the trimmed line starts with #`
- Nested comments: `unsupported`
- Evidence mode: `implementation_cross_checked`
- Confidence: `verified`
- Docs source: `https://guide.denizenscript.com/guides/troubleshooting/common-mistakes.html; https://meta.denizenscript.com/Docs/Commands/`
- Implementation source: `https://github.com/DenizenScript/Denizen-Core/blob/31300d6ab58c840a3168bd15bc46caf00b5fc418/src/main/java/com/denizenscript/denizencore/scripts/ScriptHelper.java`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: add a DenizenScript full-line `#` fixture and a regression proving inline `#` inside a command line is not stripped.
- Notes: `ScriptHelper.clearComments` appends a blank line for trimmed `#` lines and preserves command lines, replacing inline `#` with Denizen's escaped `<&ns>` token.

### Examples

#### Line comment
```text
pay_command:
  type: command
  # require permission before commands run
  permission: myscript.pay
  script:
  - narrate "ready # this hash is command text, not a comment"
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
- Version scope: GNU diffutils unified-format documentation, with the registry treating `diff` as a patch/data format rather than a source language.
- Version-specific syntax: No comment syntax was found for diff files; leading `#`, `-`, `+`, and space characters are patch content or metadata depending on context, not comments.
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.gnu.org/software/diffutils/manual/html_node/Unified-Format.html`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `unresolved`
- Recommended action: leave unsupported.
- Notes: unified diff is a patch format, not a comment-bearing language.

### Examples

#### Non-comment patch content
```text
@@ -1 +1 @@
-# removed source line, not a diff comment
+# added source line, not a diff comment
```

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
- Version scope: E-on-Java / E language tutorial material, including 0.9-era examples using `pragma.syntax("0.9")`; no newer syntax split was confirmed.
- Version-specific syntax: `#` line comments are documented for ordinary E source. `/** ... */` is reserved for Edoc documentation comments before `def` or `to`; ordinary `/* ... */` block comments were not confirmed.
- Line comments: `#` supported
- Block comments: `/** ... */` supported only as Edoc documentation comments before function/object or method definitions; ordinary `/* ... */` unresolved/unsupported.
- Termination behavior: `#` runs to newline; Edoc blocks stop at the first `*/`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://www.skyhunter.com/marcs/ewalnut.html; https://erights.org/elang/quick-ref.html`
- Implementation source: `unresolved`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: add `#` line-comment support; add Edoc `/** ... */` only if documentation comments are in parser scope, and do not add ordinary `/* ... */`.
- Notes: the most explicit accessible source states that `#` comments end at the line boundary and that `/** ... */` is reserved for Javadoc-style E comments.

### Examples

#### Line comment
```text
# E sample
# Comment on this piece of code
def a := 3
```

#### Block comment
```text
/**
 * Add 2 numbers together.
 */
def adder(a, b) { return a + b }
```

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
- Version scope: Current Autodesk Fusion Electronics EAGLE ULP syntax reference plus a 2005 CadSoft EAGLE help copy.
- Version-specific syntax: No version split found between current Autodesk ULP docs and the older CadSoft help page; both document `//` line comments and non-nesting `/* ... */` block comments.
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `//` runs to newline; block comments stop at the first `*/`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `verified`
- Docs source: `https://help.autodesk.com/cloudhelp/ENU/Fusion-ECAD/files/ECD-ULP-COMMENT-REF.htm; https://web.mit.edu/xavid/arch/i386_rhel4/help/133.htm`
- Implementation source: `unresolved`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: add EAGLE ULP fixtures for `//`, `/* ... */`, and a non-nesting block termination case.
- Notes: Autodesk explicitly says the first `*/` after `/*` ends the comment.

### Examples

#### Line comment
```text
int i; // some comment text
```

#### Block comment
```text
/* This is a
   multi line comment
*/
int i = 0;
```

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
- Version scope: ISO/IEC 14977:1996(E) Extended BNF, checked against a browsable grammar extraction; ABNF/RFC 5234 and other EBNF-like dialects were checked only to avoid mixing dialects.
- Version-specific syntax: ISO EBNF defines bracketed textual comments using `(* ... *)`; the ISO grammar is recursive, so comments can contain comments. Do not union ABNF `;` line comments or other dialect-specific forms into this key unless the registry explicitly targets those dialects.
- Line comments: `unsupported` in ISO EBNF
- Block comments: `(* ... *)` supported
- Termination behavior: `true nesting supported`
- Nested comments: `supported`
- Evidence mode: `implementation_cross_checked`
- Confidence: `verified`
- Docs source: `https://www.cl.cam.ac.uk/~mgk25/iso-14977.pdf; https://www.cl.cam.ac.uk/~mgk25/iso-ebnf.html`
- Implementation source: `https://slebok.github.io/zoo/%C2%A7wip/metasyntax/ebnf-iso-1/extracted/index.html`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: if `ebnf` means ISO/IEC 14977, add recursive `(* ... *)` support; otherwise split the Stack label by concrete grammar dialect.
- Notes: ISO clause 6.7 and the self-definition make `comment symbol` recursive, which confirms true nested comments.

### Examples

#### Block comment
```text
(* see 7.2 *) letter = 'a' | 'b' | 'c';
```

#### Nested comment
```text
(* outer (* inner *) outer *)
syntax = syntax rule, {syntax rule};
```

## eC

- Registry key: `ec`
- Version scope: Current Ecere SDK/eC project materials and the standalone eC lexer in the `ecere/eC` repository.
- Version-specific syntax: No version split found. The lexer recognizes C/C++-style `//` and `/* ... */`; `#` is handled as preprocessor input, not as an ordinary comment token.
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `//` runs to newline; block comments stop at the first `*/`
- Nested comments: `unsupported`
- Evidence mode: `implementation_cross_checked`
- Confidence: `cross-checked`
- Docs source: `https://github.com/ecere/ecere-sdk; https://opensource.com/article/17/9/ecere`
- Implementation source: `https://github.com/ecere/eC/blob/8a633973133bb007e446bead00f30f5492d5a23b/ectp/src/lexer.l`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: keep eC aligned with the C-style registry family and add an eC-specific fixture if the generated Stack coverage needs the alias pinned.
- Notes: the lexer dispatches `"/*"` to `comment()` and `"//"` to `commentCPP()`; `comment()` stops on the first `*/`.

### Examples

#### Line comment
```text
class Greeter : Window
{
   void OnCreate()
   {
      PrintLn("hello"); // startup message
   }
}
```

#### Block comment
```text
/* window startup hook */
class Greeter : Window
{
   void OnCreate() { PrintLn("hello"); }
}
```

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
- Version scope: Current EFL `edje_cc` parser source, current EFL `.edc` examples, and legacy Edje reference material; current parser carries EFL 1.18 through 1.26 compatibility defines.
- Version-specific syntax: No version split found. The current parser skips `//` single-line comments and `/* ... */` block comments outside quoted strings; `#` is treated as preprocessor line metadata rather than a normal EDC comment.
- Line comments: `//` supported
- Block comments: `/* ... */` supported
- Termination behavior: `//` runs to newline; block comments stop at the first `*/`
- Nested comments: `unsupported`
- Evidence mode: `implementation_cross_checked`
- Confidence: `verified`
- Docs source: `https://www.enlightenment.org/_legacy_embed/edje_main.html; https://github.com/Enlightenment/efl/blob/master/src/examples/edje/entry.edc`
- Implementation source: `https://github.com/Enlightenment/efl/blob/12494e95d4070a32bde155e85fe815900651c9c4/src/bin/edje/edje_cc_parse.c`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: add `.edc` fixtures for `//`, `/* ... */`, and non-nesting block termination; do not treat `#` preprocessor lines as ordinary comments.
- Notes: `next_token` tracks `in_comment_ss` for `//` and `in_comment_sa` for `/* ... */`; the block state is a boolean, so nested blocks are not supported.

### Examples

#### Line comment
```text
collections {
   group {
      name: "example/main";
      // Position text relative to background.
      parts { }
   }
}
```

#### Block comment
```text
collections {
   /* Main visible group. */
   group {
      name: "example/main";
   }
}
```

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
- Version scope: EmberScript master / npm 0.0.14 project source, its CoffeeScript-derived grammar and preprocessor, and current CoffeeScript reference documentation.
- Version-specific syntax: No EmberScript-specific split found. EmberScript inherits CoffeeScript-style comments, and its own grammar defines `#` single-line comments and `### ... ###` block comments.
- Line comments: `#` supported
- Block comments: `### ... ###` supported
- Termination behavior: `first closing delimiter wins`
- Nested comments: `unsupported`
- Evidence mode: `implementation_cross_checked`
- Confidence: `verified`
- Docs source: `https://github.com/ghempton/ember-script; https://coffeescript.org/`
- Implementation source: `https://github.com/ghempton/ember-script/blob/master/src/grammar.pegjs; https://github.com/ghempton/ember-script/blob/master/src/preprocessor.coffee`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: keep EmberScript aligned with the CoffeeScript-style registry family and include a language-alias fixture if needed.
- Notes: `src/grammar.pegjs` defines `singleLineComment = "#" ...` and `blockComment = "###" ... "###"`; the preprocessor also tracks `#` and `###` comment contexts.

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
- Version scope: Search pass over the Stack label, `.eq` file-extension references, Altair Compose `eq` function documentation, and generic programming-language search results.
- Version-specific syntax: No unique source language or format was identified; `EQ` collides with operators, file extensions, product names, and mathematical/equality terminology.
- Line comments: `unresolved`
- Block comments: `unresolved`
- Termination behavior: `unresolved`
- Nested comments: `unresolved`
- Evidence mode: `unresolved`
- Confidence: `unresolved`
- Docs source: `https://file.org/extension/eq; https://help.altair.com/compose/help/en_us/topics/reference/oml_language/CoreMinimalInterpreter/eq.htm`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: identify the language before adding syntax.
- Notes: the name collides with multiple unrelated EQ concepts, so I did not treat any of them as the intended language.

### Examples

#### Unresolved label sample
```text
eq(value1, value2)
```

This is a representative equality/function spelling from one EQ collision, not a parser-safe comment example for an `eq` language.

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
- Version scope: `Current FStar master lexer and tagged release v2025.12.15; both use the same comment rules.`
- Version-specific syntax: `Current and reviewed tagged release agree: // line comments and truly nested (* ... *) block comments.`
- Line comments: `//` supported
- Block comments: `(* ... *)` supported
- Termination behavior: `true nesting supported`
- Nested comments: `supported`
- Evidence mode: `implementation_cross_checked`
- Confidence: `verified`
- Docs source: `https://fstar-lang.org/tutorial/book/part1/part1_getting_off_the_ground.html`
- Implementation source: `https://github.com/FStarLang/FStar/blob/master/src/ml/FStarC_Parser_LexFStar.ml`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: implement `//` line comments and nested `(* ... *)` comments in the registry.
- Notes: the lexer enters a recursive comment rule when it encounters another `(*`, which confirms true nesting rather than first-delimiter termination.

### Examples

#### Line comment
```text
let x = 1 // keep this binding
in x
```

#### Block comment
```text
let x = 1
(* outer (* inner *) outer *)
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
- Version scope: `Fennel reference, reviewed 2026-05-22.`
- Version-specific syntax: `No version split found for comment tokens.`
- Line comments: `;`
- Block comments: `unsupported`
- Termination behavior: `end of line`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `verified`
- Docs source: [Fennel reference](https://raw.githubusercontent.com/bakpakin/Fennel/main/reference.md)
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: `Implemented in the registry with semicolon line fixtures.`
- Notes: `The reference states that a semicolon starts a comment through end of line.`

### Examples

#### Line comment
```text
; keep the example readable
(print "hello")
```

## FIGlet Font

- Registry key: `figlet_font`
- Version scope: FIGfont Version 2 / FIGlet 2.2.1 standard material plus figlet parser documentation for font files.
- Version-specific syntax: No token-delimited source comments were found. FIGfont files use a counted comment section immediately after the header line, with the count stored in the `Comment_Lines` header field.
- Line comments: `unsupported` as token syntax; counted FIGfont metadata comment lines are supported by the format.
- Block comments: `unsupported`
- Termination behavior: `counted metadata lines, not delimiter-based`
- Nested comments: `unsupported`
- Evidence mode: `implementation_cross_checked`
- Confidence: `verified`
- Docs source: `https://sources.debian.org/src/figlet/2.2.1-4/figfont.txt; https://www.figlet.org/figlet-man.html; https://hexdocs.pm/figlet/Figlet.Parser.FontFileParser.html`
- Implementation source: `https://hexdocs.pm/figlet/Figlet.Parser.FontFileParser.html`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: leave source-comment extraction unsupported unless a future feature explicitly parses FIGfont header metadata.
- Notes: the FIGfont standard says comment lines are after the header and that blank lines count; this is structural metadata rather than an in-band comment token.

### Examples

#### Counted metadata comments
```text
flf2a$ 6 5 20 15 2 0 143
Example font by Ada
Permission notice
<FIGcharacter data starts here>
```

## Filebench WML

- Registry key: `filebench_wml`
- Version scope: Current Filebench repository, Filebench 1.5-alpha1+ quick-start documentation, current WML lexer, and shipped `.f` workload personalities.
- Version-specific syntax: No version split found. The lexer skips `#.*` in the initial state; no block-comment rule is present for WML.
- Line comments: `#` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `implementation_cross_checked`
- Confidence: `verified`
- Docs source: `https://github.com/filebench/filebench; https://github-wiki-see.page/m/filebench/filebench/wiki/Workload-model-language; https://www.usenix.org/system/files/login/articles/login_spring16_02_tarasov.pdf`
- Implementation source: `https://github.com/filebench/filebench/blob/master/parser_lex.l`
- Community source: `not used`
- Corpus fallback source: `https://github.com/filebench/filebench/blob/master/workloads/filemicro_create.f`
- Recommended action: add `#` line-comment support for Filebench WML and keep block syntax unsupported.
- Notes: `parser_lex.l` has an `<INITIAL>#.*` skip rule; shipped workload files use leading `#` header and explanatory comments.

### Examples

#### Line comment
```text
# Simple way to create a file.
set $dir=/tmp
set $count=1024
run 60
```

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
- Version scope: InfluxData Flux v0 language specification and the current `influxdata/flux` scanner source.
- Version-specific syntax: No version split found in the checked Flux v0 sources. Flux supports `//` line comments only; requests for multiline comments were tracked separately and not reflected in the scanner grammar.
- Line comments: `//` supported
- Block comments: `unsupported`
- Termination behavior: `runs to newline`
- Nested comments: `unsupported`
- Evidence mode: `implementation_cross_checked`
- Confidence: `verified`
- Docs source: `https://docs.influxdata.com/flux/v0/spec/lexical-elements/; https://docs.influxdata.com/flux/v0/spec/`
- Implementation source: `https://github.com/influxdata/flux/blob/master/libflux/flux-core/src/scanner/scanner.rl; https://github.com/influxdata/flux/blob/0573ed7ea2e000b3dc4314f37f66cf3a57b3bd34/libflux/flux-core/src/scanner/mod.rs`
- Community source: `https://github.com/influxdata/flux/issues/4911`
- Corpus fallback source: `not used`
- Recommended action: add Flux `//` line-comment support and keep block syntax unsupported.
- Notes: the spec says comments cannot start inside string or regexp literals and act like newlines; `scanner.rl` defines `single_line_comment = "//" [^\n]* newline?`.

### Examples

#### Line comment
```text
from(bucket: "example")
  // keep the range small for testing
  |> range(start: -1h)
```

## Formatted

- Registry key: `formatted`
- Version scope: Stack Exchange/Stack Overflow formatted code-block documentation and local registry/test treatment of `formatted` as a non-language label.
- Version-specific syntax: `Formatted` is not a source language or file format with its own lexical grammar; no versioned comment syntax applies.
- Line comments: `unsupported`
- Block comments: `unsupported`
- Termination behavior: `unsupported`
- Nested comments: `unsupported`
- Evidence mode: `official_docs`
- Confidence: `high`
- Docs source: `https://meta.stackoverflow.com/questions/251361/how-do-i-format-my-code-blocks; https://meta.stackexchange.com/questions/108171/how-do-i-get-code-to-show-up-with-color-syntax-highlighting`
- Implementation source: `src/ml4setk/Parsing/Comments/registry.py`
- Community source: `not used`
- Corpus fallback source: `not used`
- Recommended action: leave unsupported unless Stack v2 can map `formatted` to a concrete language label.
- Notes: local tests already group `formatted` with no-comment/non-language labels; do not infer comments from the code content inside formatted blocks.

### Examples

#### Non-comment formatted content
```text
# This is only formatted text until a concrete embedded language is known.
/* This is also only formatted text for the `formatted` label. */
```

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
