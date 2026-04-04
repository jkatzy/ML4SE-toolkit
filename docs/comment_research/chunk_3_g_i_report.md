# Stack v2 Comment Research: Chunk 3 g-i



Source of truth: `docs/comment_research/README.md`. This report is documentation-oriented and test-oriented. If syntax is unclear, it is marked `unresolved` rather than guessed.















## G-code

- Registry key: g_code
- Line comments: `;`
- Block comments: `(...)`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://linuxcnc.org/docs/devel/html/gcode/overview.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add registry support for semicolon line comments and parenthesized block comments, then add parser tests for comment placement inside a G-code block.
- Notes: LinuxCNC documents both comment forms and notes that semicolon comments are ignored only when they are not enclosed in parentheses.

### Examples

#### Line comment
```text
G0 X1 Y1 ; rapid move
M2
```

#### Block comment
```text
G0 (Rapid to start) X1 Y1
M2
```

## Game Maker Language

- Registry key: game_maker_language
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Overview/Commenting_Code.htm
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add C-style comment fixtures and keep code-folding markers such as `#region` out of the parser contract.
- Notes: The GameMaker manual documents both one-line and multi-line comments for GML code.

### Examples

#### Line comment
```text
speed = 4; // player speed
draw_self();
```

#### Block comment
```text
/* temporary debug
   remove after repro */
draw_self();
```

## GAML

- Registry key: gaml
- Line comments: `//`
- Block comments: unresolved
- Termination behavior: line comments end at newline; block comments unresolved
- Nested comments: unsupported
- Confidence: medium
- Evidence mode: official_docs
- Docs source: https://gama-platform.org/wiki/1.9.3/Statements; https://gama-platform.org/wiki/1.9.3/GamlReference
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: GAMA 1.9.3 wiki pages and the current GamlReference snapshot
- Version-specific syntax: both checked versions surface `//`; no source-backed block-comment form or dialect split was confirmed, so the registry should not union extra forms yet
- Recommended action: Confirm whether GAML has a distinct block-comment form in the grammar or corpus before adding registry support.
- Notes: The verified docs show `//` in statement examples, but this pass did not find a source-backed block-comment specification.

### Examples

#### Line comment
```text
int speed <- 4; // movement speed
display speed;
```

## GAMS

- Registry key: gams
- Line comments: `*` at column 1; `!!` when `$onEolCom` is enabled
- Block comments: `$onText` / `$offText`; inline `/* ... */` when `$onInline` is enabled
- Termination behavior: line comments end at newline; `$offText` closes block comments; inline comments end at the first matching closer and can be nested with `$onNestCom`
- Nested comments: supported for inline comments when `$onNestCom` is enabled
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.gams.com/latest/docs/UG_GAMSPrograms.html
- Implementation source: https://gams.com/latest/docs/UG_DollarControlOptions.html?print=1
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Model GAMS as context-sensitive: support column-1 line comments, `$onText` blocks, and the optional inline-comment toggles separately.
- Notes: GAMS comment handling is stateful; nested comments are documented for inline comments, not for ordinary line comments.

### Examples

#### Line comment
```text
* solve the model
SET i /i1*i10/;
$onEolCom
display "done"; !! end-of-line comment
$offEolCom
```

#### Block comment
```text
$onText
temporary note
$offText
SOLVE model USING lp;
```

#### Nested comment
```text
$onInline
$onNestCom
x = 1 /* outer /* inner */ outer */;
$offInline
```

## GAP
- Registry key: `gap`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://docs.gap-system.org/
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add `#` comment coverage and keep block-comment tests absent.
- Notes: GAP comment handling is line-oriented in the verified docs.
- Example: line comment
```gap
L := [1..3]; # create a small list
Print(L);
```




## GCC Machine Description

- Registry key: gcc_machine_description
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: GCC internals manuals checked in the 3.1 and 4.1.1 lines plus current online internals references
- Version-specific syntax: no source-backed machine-description comment delimiter was confirmed in any checked version; keep unsupported until a real `.md` comment form is documented
- Recommended action: Leave unsupported until an official GCC machine-description syntax source is located.
- Notes: No source-backed comment syntax was confirmed in this pass.

## GDB

- Registry key: gdb
- Line comments: `#` in command files
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.sourceware.org/gdb/download/onlinedocs/gdb.html/Command-Files.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add a command-file fixture that exercises `#` comments and keep the parser line-oriented.
- Notes: The GDB command-file docs explicitly say that lines beginning with `#` are comments.

### Examples

#### Line comment
```text
break main   # stop at entry
run
```

## GDScript
- Registry key: `gdscript`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add `#` comment tests and keep doc-comment handling separate unless required.
- Notes: Godot documentation also uses `##` for documentation comments, but the core parser should start with plain `#`.
- Example: line comment
```gdscript
var speed = 4 # movement speed
move_and_slide()
```




## GEDCOM

- Registry key: gedcom
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: GEDCOM 5.5.1 errata and standard references checked
- Version-specific syntax: no file-comment delimiter was confirmed; the spec's `/* comment */` wording is explanatory syntax notation, not a source comment form, so the registry should keep GEDCOM unsupported
- Recommended action: Keep unsupported unless a dialect-specific GEDCOM source documents a real comment form.
- Notes: No source-backed comment syntax was confirmed in this pass.

## Gemfile.lock

- Registry key: gemfile_lock
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: unsupported
- Evidence mode: unresolved
- Docs source: Ruby/Bundler lockfile format; no comment syntax located
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: Bundler lockfile format is not versioned for comment syntax
- Version-specific syntax: no comment syntax was found in the checked lockfile references; keep unsupported and do not union any delimiters
- Recommended action: Keep unsupported and exclude this file type from comment parsing tests.
- Notes: Gemfile.lock is generated dependency metadata, not a comment-bearing source format.

## Genero

- Registry key: genero
- Line comments: `--` and `#`
- Block comments: `{ ... }`
- Termination behavior: line comments end at newline; brace comments end at the first closing `}`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://4js.com/online_documentation/fjs-fgl-manual-html/fgl-topics/c_fgl_language_features_comment.html; https://4js.com/online_documentation/fjs-fgl-manual-html/fgl-topics/c_fgl_beautifier_usage.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add fixtures for `--`, `#`, and brace comments, and keep brace nesting explicitly forbidden in tests.
- Notes: The official BDL docs say brace comments do not nest and that comments are ignored as source comments outside SQL string contexts.

### Examples

#### Line comment
```text
MAIN
  -- ignore this line
  DISPLAY "Hello"
END MAIN
```

#### Block comment
```text
MAIN
  {
    DISPLAY "ignored"
    DISPLAY "ignored too"
  }
  DISPLAY "Hello"
END MAIN
```

## Genero Forms

- Registry key: genero_forms
- Line comments: `--`
- Block comments: unsupported
- Termination behavior: line comments end at newline
- Nested comments: unsupported
- Confidence: medium
- Evidence mode: official_docs
- Docs source: https://4js.com/online_documentation/fjs-genero-3.00.06-manual-tutorial-html/genero-tutorial-topics/c_fgl_TutChap10_010.html; https://4js.com/online_documentation/fjs-genero-4.01.38-manual-tutorial-html/genero-tutorial-topics/c_fgl_TutChap10_010.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: Genero Forms 3.00.06 and 4.01.38 tutorial docs
- Version-specific syntax: both checked tutorial versions show `--` comments in `.per` examples; no block-comment form or version split was confirmed, so the registry should not union extra syntax
- Recommended action: Add `.per` fixtures that keep `--` comment lines in place and do not assume brace or hash comments unless a form-file grammar source confirms them.
- Notes: The official form examples show trailing `--` comments in text-based form files, but they do not document a separate block-comment form.

### Examples

#### Line comment
```text
SCHEMA custdemo
LAYOUT
  GRID
  {
    [lab1      ] [f01  ]
  } -- grid
END -- layout
```

## Genshi

- Registry key: genshi
- Line comments: `##` in legacy text templates
- Block comments: `{# ... #}` in text templates; XML comment syntax is also accepted in markup templates
- Termination behavior: line comments end at newline; block-style comment forms end at the first closer
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://genshi.readthedocs.io/en/latest/xml-templates.html; https://genshi.readthedocs.io/en/latest/text-templates.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Treat Genshi as mode-sensitive: keep legacy text-template comments separate from XML-template comment handling.
- Notes: Legacy text templates use lines beginning with `##`; markup templates accept XML comments, and the stripped variant is `<!-- ! ... -->`.

### Examples

#### Line comment
```text
## legacy text-template comment
Dear $name,
```

#### Block comment
```text
{# This will not end up in the output #}
This will.
```
## Gentoo Ebuild
- Registry key: `gentoo_ebuild`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Gentoo developer docs and ebuild conventions
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add shell-style `#` comment tests for ebuild fixtures.
- Notes: keep ebuild coverage separate from generic shell parsing.
- Example: line comment
```bash
src_prepare() {
  # patch before configure
  eapply user.patch
}
```




## Gentoo Eclass
- Registry key: `gentoo_eclass`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Gentoo eclass documentation
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: reuse the Gentoo ebuild line-comment path and add a focused eclass fixture.
- Notes: same comment syntax as ebuilds.
- Example: line comment
```bash
# helper function for package setup
econf
```




## Gerber Image

- Registry key: gerber_image
- Line comments: `G04 ... *` comment records
- Block comments: unsupported
- Termination behavior: record terminator `*` closes the comment record
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add tests that preserve `G04` comment records and do not treat them as ordinary source-code comments.
- Notes: The Gerber spec defines `G04` as a human-readable comment command that does not affect the image.

### Examples

#### Line comment
```text
G04 Board outline*
G01*
```

## Gettext Catalog

- Registry key: gettext_catalog
- Line comments: `#` comment lines, including `#.`, `#:`, `#,`, and `#|` variants
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.gnu.org/software/gettext/manual/gettext.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add `.po` fixtures that cover translator comments, extracted comments, references, flags, and previous-message comments.
- Notes: The gettext manual treats PO comments as lines beginning with `#` plus specific suffixes for the different comment kinds.

### Examples

#### Line comment
```text
#. Translator note
#: src/main.c:12
#, fuzzy
#| msgid "Old"
msgid "Hello"
msgstr "Bonjour"
```

## Gherkin
- Registry key: `gherkin`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://cucumber.io/docs/gherkin/reference/
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add `#` comment fixtures to feature files and keep block-comment tests absent.
- Notes: comments should not interfere with step keyword parsing.
- Example: line comment
```gherkin
# this scenario is intentionally minimal
Feature: Greetings
  Scenario: say hello
    Given a user exists
```




## Git Attributes
- Registry key: `git_attributes`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://git-scm.com/docs/gitattributes
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add `#` comment coverage for attribute files.
- Notes: line comments are the only verified comment form.
- Example: line comment
```gitattributes
*.png binary
# keep generated files out of diffs
docs/** linguist-generated
```




## Git Config
- Registry key: `git_config`
- Line comments: `#` and `;`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://git-scm.com/docs/git-config
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add tests for both comment prefixes and for inline trailing comments.
- Notes: keep `#` and `;` as distinct line-comment tokens.
```ini
[core]
    editor = vim
    # prefer a visible default
    pager = less
```
- Example: line comment
```ini
[user]
    ; local identity
    name = Researcher
```




## Git Revision List

- Registry key: git_revision_list
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: checked revision-list references did not expose a versioned comment syntax
- Version-specific syntax: no source-backed delimiter was found; keep unsupported and do not infer a union of forms
- Recommended action: Keep unsupported unless a specific revision-list dialect documents comments.
- Notes: No source-backed comment syntax was confirmed in this pass.

## GLSL
- Registry key: `glsl`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Khronos GLSL specification / language reference
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add C-style parser tests for shaders.
- Notes: keep the parser non-nested for block comments unless a verified exception appears.
```glsl
void main() {
  gl_FragColor = vec4(1.0); // output white
}
```
- Example: block comment
```glsl
/* temporary debug path */
void main() {
  gl_FragColor = vec4(1.0);
}
```




## Glyph Bitmap Distribution Format

- Registry key: glyph_bitmap_distribution_format
- Line comments: `COMMENT` records
- Block comments: unsupported
- Termination behavior: the rest of the `COMMENT` line is ignored
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.adobe.com/content/dam/Adobe/en/devnet/font/pdfs/5005.BDF_Spec.pdf
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add fixtures that preserve `COMMENT` records as comment-like lines.
- Notes: BDF treats `COMMENT` as a record keyword: the remainder of the line is ignored.

### Examples

#### Line comment
```text
STARTCHAR U+0041
COMMENT glyph width adjusted for preview
ENCODING 65
```

## GN

- Registry key: gn
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://chromium.googlesource.com/chromium/src/tools/gn/%2B/48062805e19b4697c5fbd926dc649c78b6aaa138/docs/reference.md
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add `#` comment tests for GN build files and keep block-comment tests absent.
- Notes: GN build files treat `#` as a line comment and ignore it to end of line.

### Examples

#### Line comment
```text
# keep this subtree available
executable("app") {
  sources = [ "main.cc" ]
}
```

## Gnuplot
- Registry key: `gnuplot`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add `#` comment fixtures for plot scripts.
- Notes: line comments should not consume plot commands.
- Example: line comment
```gnuplot
# set terminal for file output
set terminal pngcairo
plot sin(x)
```




## Go Checksums

- Registry key: go_checksums
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: unsupported
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: Go checksum database metadata is generated, not versioned for comment syntax
- Version-specific syntax: no comment delimiter was confirmed in any checked checksum format reference; keep unsupported
- Recommended action: Keep unsupported and exclude from parser coverage.
- Notes: Go checksum database entries are generated metadata, not a comment-bearing source format.

## Go Module
- Registry key: `go_module`
- Line comments: `//`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://go.dev/ref/mod
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add `go.mod` fixtures for trailing `//` comments.
- Notes: comments appear in module files and should be parsed as line comments only.
- Example: line comment
```go
module example.com/research // module path

go 1.22
```




## Golo

- Registry key: golo
- Line comments: unsupported
- Block comments: `---- ... ----`
- Termination behavior: first closing `----` wins
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://gololang.org/GRP-Documentation-Misc.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add block-comment fixtures using the `----` delimiter and keep line-comment tests absent unless a second source confirms them.
- Notes: The official docs describe `----` as the multi-line comment syntax.

### Examples

#### Block comment
```text
module demo

function main = {
  ----
  temporary note
  ----
  println("run")
}
```

## Gosu

- Registry key: gosu
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://gosu-lang.github.io/docs.html
- Implementation source: https://gosu-lang.github.io/grammar.html
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add Gosu fixtures that assert both `//` and `/* */` are recognized, matching the published grammar.
- Notes: The Gosu grammar explicitly defines `LINE_COMMENT` and `COMMENT` tokens.

### Examples

#### Line comment
```text
var speed = 4 // player speed
print(speed)
```

#### Block comment
```text
/* temporary debug
   remove after repro */
print(speed)
```

## Grace

- Registry key: grace
- Line comments: `//`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://web.cecs.pdx.edu/~grace/doc/lang-spec/
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add a line-comment fixture for `//` and keep block-comment tests absent unless another source proves them.
- Notes: The Grace language specification says comments start with `//` and extend to end of line.

### Examples

#### Line comment
```text
def speed := 4 // movement speed
print(speed)
```

## Gradle
- Registry key: `gradle`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Gradle build script docs
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add tests for line comments and block comments in build files.
- Notes: doc comments such as `/** ... */` can be handled as block comments for parsing purposes.
```gradle
plugins {
    id 'java' // standard plugin
}
```
- Example: block comment
```gradle
/* temporary build tweak */
tasks.register('hello') {
    doLast { println 'hi' }
}
```




## Grammatical Framework

- Registry key: grammatical_framework
- Line comments: `--`
- Block comments: `{- ... -}`
- Termination behavior: line comments end at newline; block comments end at the first `-}`
- Nested comments: supported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.grammaticalframework.org/doc/gf-refman.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add both comment forms to the registry and keep the nested-block behavior covered by regression tests.
- Notes: The GF reference manual explicitly lists single-line `--` comments and multiline `{- ... -}` comments.

### Examples

#### Line comment
```gf
fun DetCN : Det -> CN -> NP ;  -- noun phrase from determiner and noun
```

#### Block comment
```gf
{- outer
  {- inner -}
  still outer
-}
fun UsePN : PN -> NP ;
```

## Graph Modeling Language

- Registry key: graph_modeling_language
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: unsupported
- Evidence mode: unresolved
- Docs source: https://en.wikipedia.org/wiki/Graph_Modelling_Language
- Implementation source: https://igraph.org/c/html/develop/igraph-Foreign.html
- Community source: https://en.wikipedia.org/wiki/Graph_Modelling_Language
- Corpus fallback source: not used
- Version scope: GML references and igraph foreign-interface docs checked; no versioned comment syntax surfaced
- Version-specific syntax: the checked sources treat `comment` as data, not syntax; do not union any delimiters and keep GML unsupported
- Recommended action: Keep unsupported; the available references describe `comment` as a data attribute, not a comment delimiter.
- Notes: The available GML references treat `comment` as a regular attribute, so this format should stay out of comment parsing.

## Graphviz (DOT)

- Registry key: graphviz_dot
- Line comments: `//` and `#`
- Block comments: `/* ... */`
- Termination behavior: line comments end at newline; block comments end at the first `*/`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://graphviz.org/doc/info/lang.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add fixtures for all three DOT comment forms and preserve source order across multiple comment tokens.
- Notes: Graphviz documents both C/C++-style comments and `#` at the start of a line.

### Examples

#### Line comment
```text
digraph G {
  # graph-level note
  // another note
  a -> b;
}
```

#### Block comment
```text
digraph G {
  /* temporary layout note */
  a -> b;
}
```

## Groovy Server Pages

- Registry key: groovy_server_pages
- Line comments: unsupported
- Block comments: `<%-- ... --%>`
- Termination behavior: first closing `--%>` wins
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://grails.apache.org/docs-legacy-gsp/6.2.3/guide/index.html; https://grails.apache.org/docs-legacy-gsp/7.0.0-M1/guide/GSPBasics.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add JSP-style server-side comment fixtures and keep embedded Groovy scriptlets separate from GSP comments.
- Notes: GSP uses JSP-style comment blocks that are removed before rendering.

### Examples

#### Block comment
```text
<html>
  <body>
    <%-- hidden note --%>
    <p>Hello</p>
  </body>
</html>
```

## GSC

- Registry key: gsc
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: line comments end at newline; block comments end at the first `*/`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://docs.auroramod.dev/gsc-scripting-syntax
- Implementation source: unresolved
- Community source: https://github-wiki-see.page/m/AkbarHashimi/BO2-Plutonium-Modding-Guide/wiki/GSC-Basics
- Corpus fallback source: not used
- Recommended action: Add both one-line and block-comment fixtures and keep the grammar C-like.
- Notes: The official syntax page documents comment support in two forms; the community guide matches the same C-style delimiters.

### Examples

#### Line comment
```text
main()
{
  // initialize the player
  wait 0.05;
}
```

#### Block comment
```text
main()
{
  /* temporarily disable debug logic */
  wait 0.05;
}
```

## Haml

- Registry key: haml
- Line comments: `-#`
- Block comments: `/` HTML comments
- Termination behavior: silent comments end at newline; HTML-comment blocks end when the indented block closes
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://haml.info/docs/yardoc/file.REFERENCE.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add fixtures for silent comments and HTML-comment blocks, and keep indentation-sensitive termination explicit in tests.
- Notes: The Haml reference distinguishes silent comments (`-#`) from HTML comments introduced by `/`.

### Examples

#### Line comment
```text
%div
  -# silent comment
  %p visible
```

#### Block comment
```text
%div
  / HTML comment
    %span hidden
  %p visible
```

## Handlebars

- Registry key: handlebars
- Line comments: `{{! ... }}`
- Block comments: `{{!-- ... --}}`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://handlebarsjs.com/guide/comments.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add both Handlebars comment forms and keep the multi-line block form as the primary fixture.
- Notes: Handlebars documentation recommends `{{!-- --}}` when comments need to contain template tokens.

### Examples

#### Line comment
```text
<div class="card">
  {{! hidden note }}
  <span>{{name}}</span>
</div>
```

#### Block comment
```text
<div class="card">
  {{!--
    longer note
  --}}
  <span>{{name}}</span>
</div>
```

## HAProxy

- Registry key: haproxy
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://docs.haproxy.org/2.9/configuration.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add `#` comment tests for HAProxy config files and keep block-comment tests absent.
- Notes: HAProxy configuration files treat comments as unprotected `#` to end of line.

### Examples

#### Line comment
```text
global
  daemon
  # comment about global settings
```

## Harbour

- Registry key: harbour
- Line comments: unresolved
- Block comments: unresolved
- Termination behavior: unresolved
- Nested comments: unresolved
- Confidence: unresolved
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: Harbour core/manual snapshots were checked without finding a versioned comment reference
- Version-specific syntax: no source-backed Harbour delimiter difference was confirmed; leave unresolved until a primary Harbour reference documents the comment forms
- Recommended action: Leave unresolved until a source-backed Harbour syntax reference confirms the comment forms.
- Notes: No source-backed comment syntax was confirmed in this pass.

## Haxe
- Registry key: `haxe`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Haxe manual comment syntax
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add standard C-style comment fixtures.
- Notes: doc comments can be treated as block comments for comment extraction.
```haxe
var speed = 4; // movement speed
trace(speed);
```
- Example: block comment
```haxe
/* debug output disabled */
trace(speed);
```




## HCL
- Registry key: `hcl`
- Line comments: `#` and `//`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: https://developer.hashicorp.com/terraform/language/syntax/configuration
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add Terraform/HCL fixtures for all three comment forms.
- Notes: tests should verify both hash and slash line comments.
```hcl
resource "aws_instance" "example" {
  # keep the instance small
  ami = "ami-123456"
}
```
- Example: line comment
```hcl
resource "aws_instance" "example" {
  // keep the instance small
  ami = "ami-123456"
}
```
- Example: block comment
```hcl
/* temporary override */
resource "aws_instance" "example" {
  ami = "ami-123456"
}
```




## HiveQL
- Registry key: `hiveql`
- Line comments: `--`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Apache Hive language reference
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add SQL-style comment fixtures.
- Notes: line comments should end at newline; block comments should be non-nested.
```sql
-- partition filter
SELECT * FROM events;
```
- Example: block comment
```sql
/* explain the join */
SELECT * FROM events;
```




## HLSL
- Registry key: `hlsl`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Microsoft HLSL reference
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add shader-style line and block comment fixtures.
- Notes: comment handling matches the common C-style pattern.
```hlsl
float4 main() : SV_Target {
  return float4(1, 1, 1, 1); // solid color
}
```
- Example: block comment
```hlsl
/* temporary lighting tweak */
float4 main() : SV_Target {
  return float4(1, 1, 1, 1);
}
```




## HOCON
- Registry key: `hocon`
- Line comments: `#` and `//`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Lightbend Config / HOCON docs
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add hash, slash, and block comment tests.
- Notes: keep tests for line and block forms separate.
```hocon
service {
  # enable local mode
  host = "localhost"
}
```
- Example: line comment
```hocon
service {
  // enable local mode
  host = "localhost"
}
```
- Example: block comment
```hocon
/* development override */
service {
  host = "localhost"
}
```




## HolyC

- Registry key: holyc
- Line comments: `//`
- Block comments: unresolved
- Termination behavior: line comments end at newline; block comments unresolved
- Nested comments: unresolved
- Confidence: medium
- Evidence mode: community_search
- Docs source: unresolved
- Implementation source: https://github.com/Ma11ock/holyc
- Community source: https://pldb.io/concepts/holyc.html
- Corpus fallback source: not used
- Recommended action: Keep the `//` line-comment fixture and leave block comments unresolved until a source-backed HolyC reference confirms them.
- Notes: The strongest evidence found in this pass only confirmed single-line `//` comments.

### Examples

#### Line comment
```holyc
U0 Main()
{
  U8 *message = "hello world"; // greeting
  "%s\n", message;
}
```

## hoon

- Registry key: hoon
- Line comments: `::`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://docs.urbit.org/hoon/style
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add line-comment coverage for `::` and keep block-comment tests absent.
- Notes: Urbit docs define Hoon comments as 80-column lines that contain whitespace, then `::`, then optional text.

### Examples

#### Line comment
```text
=+  x  1
:: comment about the next gate
x
```

## HTML+ECR

- Registry key: html_ecr
- Line comments: unsupported
- Block comments: `<%# ... %>`
- Termination behavior: first closing `%>` wins
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://crystal-lang.org/api/0.35.1/ECR.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add ECR template-comment fixtures and keep embedded Crystal code comments separate from template comments.
- Notes: ECR supports the special comment tag `<%# ... %>`; raw Crystal `#` comments inside `<% ... %>` are not template-comment syntax.

### Examples

#### Block comment
```text
<div class="card">
  <%# hidden note %>
  <%= name %>
</div>
```

## HTML+EEX

- Registry key: html_eex
- Line comments: unsupported
- Block comments: `<%# ... %>`
- Termination behavior: first closing `%>` wins
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://hexdocs.pm/eex/EEx.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add EEx template-comment fixtures and keep embedded Elixir code comments separate from template comments.
- Notes: EEx documents `<%# ... %>` as a discarded comment tag.

### Examples

#### Block comment
```text
<div class="card">
  <%# hidden note %>
  <%= @name %>
</div>
```

## HTML+ERB

- Registry key: html_erb
- Line comments: unsupported
- Block comments: `<%# ... %>`
- Termination behavior: first closing `%>` wins
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://docs.ruby-lang.org/en/master/ERB.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add ERB-comment fixtures inside HTML templates and keep Ruby execution tags distinct from comment tags.
- Notes: Ruby ERB documents `<%# ... %>` as the comment tag; `<% # ... %>` is not a comment tag.

### Examples

#### Block comment
```text
<div class="card">
  <%# hidden note %>
  <%= user.name %>
</div>
```

## HTML+PHP

- Registry key: html_php
- Line comments: `//` and `#` inside PHP blocks
- Block comments: `/* ... */` inside PHP blocks
- Termination behavior: line comments end at newline or `?>` if the PHP block ends first; block comments end at the first `*/`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.php.net/manual/en/language.basic-syntax.comments.php
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add fixtures that keep the PHP comment rules scoped to `<?php ... ?>` regions.
- Notes: PHP comments only apply while PHP code is active; outside PHP tags, HTML is passed through unchanged.

### Examples

#### Line comment
```text
<html>
<body>
<?php
  // trim heading
  # keep legacy style too
  echo $title;
?>
</body>
</html>
```

#### Block comment
```text
<html>
<body>
<?php
  /* render debug marker */
  echo $title;
?>
</body>
</html>
```

## HTML+Razor

- Registry key: html_razor
- Line comments: unsupported
- Block comments: `@* ... *@`
- Termination behavior: first closing `*@` wins
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://learn.microsoft.com/en-us/aspnet/web-pages/overview/getting-started/introducing-razor-syntax-c
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add Razor template-comment fixtures and keep embedded C# comments separate from Razor comment syntax.
- Notes: Razor comments are removed on the server before the page is rendered.

### Examples

#### Block comment
```text
<div>
  @* hidden note *@
  <span>@Model.Title</span>
</div>
```

## HTTP

- Registry key: http
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: unsupported
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: HTTP is a protocol, not a versioned comment-bearing source language
- Version-specific syntax: no HTTP comment syntax was found in the checked references; keep unsupported
- Recommended action: Keep unsupported unless a formal comment syntax is located in a specific HTTP configuration grammar.
- Notes: HTTP itself is a protocol, not a comment-bearing source format.

## HXML

- Registry key: hxml
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://haxe.org/manual/compiler-usage-hxml.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add an `.hxml` fixture that starts with `#` comment lines and keep the parser line-oriented.
- Notes: The Haxe manual says lines starting with `#` are comments inside `.hxml` files.

### Examples

#### Line comment
```text
# keep compiler args grouped
-cp src
-main Main
```

## Hy
- Registry key: `hy`
- Line comments: `;`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Hy language documentation
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add Lisp-style semicolon comment tests.
- Notes: block comments are not part of the verified syntax in this pass.
- Example: line comment
```hy
(print "hello") ; greeting
```




## HyPhy

- Registry key: hyphy
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: line comments end at newline; block comments end at the first `*/`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://hyphy.org/resources/Getting_Started_With_HyPhy.pdf
- Implementation source: https://github.com/veg/hyphy
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add HBL fixtures for both comment forms and keep nested block comments absent.
- Notes: The getting-started material and shipped examples use C-style line and block comments in HyPhy batch language.

### Examples

#### Line comment
```text
rate = 1; // baseline rate
```

#### Block comment
```text
/* temporary analysis note */
LikelihoodFunction lf = (tree, data);
```

## IDL
- Registry key: `idl`
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: first closing delimiter wins
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: official IDL language docs
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add C-style comment fixtures.
- Notes: keep nested block comments absent unless a verified exception exists.
```idl
float speed = 4; // movement speed
```
- Example: block comment
```idl
/* temporary definition */
float speed = 4;
```




## Idris
- Registry key: `idris`
- Line comments: `--`
- Block comments: `{- ... -}`
- Termination behavior: true nesting supported
- Nested comments: supported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Idris language documentation
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add nested-comment fixtures and assert inner block preservation.
- Notes: nested block comments are the key behavior to lock in tests.
```idris
main : IO ()
main = putStrLn "hello" -- greeting
```
- Example: nested comment
```idris
{- outer
  {- inner -}
  still outer
-}
main : IO ()
main = putStrLn "hello"
```




## Ignore List
- Registry key: `ignore_list`
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: ignore-file conventions / `.gitignore`-style docs
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add `#` line-comment fixtures and keep the format line-oriented.
- Notes: keep ignore-file parsing separate from code-language parsing.
- Example: line comment
```gitignore
# keep build artifacts out of version control
dist/
```




## IGOR Pro

- Registry key: igor_pro
- Line comments: `//`
- Block comments: unsupported
- Termination behavior: line comments end at newline
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://docs.wavemetrics.com/igorpro/programming/procedure-windows; https://docs.wavemetrics.com/igorpro/programming/commands
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add `//` fixtures for procedure windows and keep block-comment tests absent.
- Notes: The official docs describe comment-friendly procedure windows and show `//` in procedure examples and code-marker lines.

### Examples

#### Line comment
```igorpro
SetIgorOption colorize,doColorize=1 // turn syntax coloring on
```

## ImageJ Macro

- Registry key: imagej_macro
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: line comments end at newline; block comments end at the first `*/`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://imagej.net/imagej-wiki-static/Macros.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add ImageJ Macro fixtures for line and block comments and keep the parser aligned with the documented macro syntax.
- Notes: The ImageJ macro docs explicitly describe both `//` line comments and `/* ... */` blocks.

### Examples

#### Line comment
```text
run("Blur...");
// adjust later
run("Sharpen");
```

#### Block comment
```text
/* temporary debug
   remove after repro */
run("Sharpen");
```

## Inform 7

- Registry key: inform_7
- Line comments: unsupported
- Block comments: `[ ... ]`
- Termination behavior: comments end at the first closing `]`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://ganelson.github.io/inform-website/book/WI_2_3.html; https://ganelson.github.io/inform-website/book/general_index.html
- Implementation source: https://github.com/ganelson/inform
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add bracket-comment fixtures and keep text-substitution handling separate from comments.
- Notes: The Inform 7 documentation treats bracketed text in source as comments, and the index lists `[ ]` comments explicitly.

### Examples

#### Block comment
```text
The China Shop is a room. [Remember to work out what happens if the bull gets in here!]
```

## INI
- Registry key: `ini`
- Line comments: `;` and `#`
- Block comments: unsupported
- Termination behavior: line ends at newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: INI format conventions
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add dual line-comment coverage and keep block tests absent.
- Notes: comment prefixes vary by parser family; both should be tested.
```ini
; local override
[server]
port = 8080
```
- Example: line comment
```ini
# local override
[server]
port = 8080
```




## Inno Setup

- Registry key: inno_setup
- Line comments: `;` in script sections; `//` in preprocessor/comment-capable expressions
- Block comments: `/* ... */` in preprocessor expressions
- Termination behavior: script comments end at newline; preprocessor block comments end at the first `*/`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://jrsoftware.org/ishelp/topic_scriptformatoverview.htm
- Implementation source: https://jrsoftware.org/ishelp/topic_expressions.htm
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Treat Inno Setup as context-sensitive: keep script comments and preprocessor comments separate in tests.
- Notes: The script format overview documents semicolon comments, while the preprocessor docs document `//` and `/* ... */` comments.

### Examples

#### Line comment
```text
[Setup]
AppName=Demo ; script comment
AppVersion=1.0
```

#### Block comment
```text
#define Version "1.0" /* preprocessor comment */
```

## Io

- Registry key: io
- Line comments: `//` and `#`
- Block comments: `/* ... */`
- Termination behavior: line comments end at newline; block comments end at the first `*/`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://iolanguage.org/guide/guide.html
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add Io fixtures for `//`, `#`, and `/* ... */` comments and keep the parser line-oriented for comment tokens.
- Notes: Io documents three comment forms: `//`, `/* ... */`, and `#`; `#` is also used for shebang-style headers.

### Examples

#### Line comment
```text
# comment line
doStuff
```

#### Block comment
```text
/* comment out a group
doStuff
*/
```

## IRC log

- Registry key: irc_log
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: unsupported
- Evidence mode: unresolved
- Docs source: unresolved
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Version scope: IRC log formats are transcript data, not versioned source languages with comment syntax
- Version-specific syntax: no comment delimiter was found in the checked references; keep unsupported
- Recommended action: Keep unsupported.
- Notes: IRC logs are transcripts, not a comment-bearing source format.

## Isabelle
- Registry key: `isabelle`
- Line comments: unsupported
- Block comments: `(* ... *)`
- Termination behavior: true nesting supported
- Nested comments: supported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Isabelle documentation
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: add nested-block comment fixtures and validate recursive stripping.
- Notes: this is a canonical nested-comment language.
- Example: block comment
```isabelle
(* outer
  (* inner *)
  still outer
*)
theorem demo: "True"
  by simp
```




## Isabelle ROOT
- Registry key: `isabelle_root`
- Line comments: unsupported
- Block comments: `(* ... *)`
- Termination behavior: true nesting supported
- Nested comments: supported
- Confidence: verified
- Evidence mode: official_docs
- Docs source: Isabelle ROOT / documentation set
- Implementation source: unresolved
- Corpus fallback source: not used
- Recommended action: reuse the Isabelle nested-comment tests for ROOT files.
- Notes: mirror Isabelle comment handling unless ROOT-specific docs say otherwise.
- Example: block comment
```isabelle
(* root-level note
  (* nested note *)
  still comment
*)
session Demo = Pure
```
