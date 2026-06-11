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
- Version scope: GAMA 1.9.3 wiki examples plus the current GAMA Xtext and generated ANTLR grammars
- Version-specific syntax: the checked docs and current grammar use the same C-style forms; no version split was found
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: line comments end at newline; block comments end at the first `*/`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://gama-platform.org/wiki/1.9.3/Statements; https://gama-platform.org/wiki/1.9.3/GamlReference
- Implementation source: https://github.com/gama-platform/gama/blob/main/gaml.grammar/src/gaml/grammar/Gaml.xtext; https://github.com/gama-platform/gama/blob/main/gaml.compiler/src-gen/gaml/compiler/parser/antlr/internal/InternalGaml.g
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add GAML coverage for `//` and non-nested `/* ... */` comments.
- Notes: The Xtext grammar hides `WS`, `ML_COMMENT`, and `SL_COMMENT`; the generated ANTLR rule for `ML_COMMENT` is non-greedy and therefore closes at the first `*/`.

### Examples

#### Line comment
```text
species pedestrian {
  int speed <- 4; // movement speed
  reflex move { do wander; }
}
```

#### Block comment
```text
/* temporary calibration
   keep disabled while comparing runs */
experiment main type: gui { }
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
- Version scope: current GCC internals manual and current GCC `read-md.cc` reader
- Version-specific syntax: the manual documents semicolon line comments; the current reader also treats C-style block comments as whitespace
- Line comments: `;`
- Block comments: `/* ... */`
- Termination behavior: semicolon comments run to newline unless inside a quoted string; block comments end at the first `*/`
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://gcc.gnu.org/onlinedocs/gccint/Machine-Desc.html
- Implementation source: https://github.com/gcc-mirror/gcc/blob/master/gcc/read-md.cc
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add GCC machine-description fixtures for `;` line comments and non-nested `/* ... */` block comments.
- Notes: `read_skip_spaces` explicitly says Lisp-style and C-style comments are treated as whitespace; a stray `/` that is not followed by `*` is rejected.

### Examples

#### Line comment
```text
;; Integer move pattern
(define_insn "movsi"
  [(set (match_operand:SI 0 "general_operand" "=r")
        (match_operand:SI 1 "general_operand" "r"))]
  ""
  "mov\t%1,%0") ; trailing machine-description comment
```

#### Block comment
```text
/* Disabled while the constraint set is being retuned. */
(define_attr "type" "alu,load,store" (const_string "alu"))
```

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
- Version scope: FamilySearch GEDCOM 7.x specification and GEDCOM 5.5.1 standard references
- Version-specific syntax: no checked GEDCOM version defines lexical source comments; `NOTE` is genealogical data, not a parser comment
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines; https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#structures; https://gedcom.io/specifications/ged551.pdf
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Keep unsupported; do not classify `NOTE`, `CONT`, or spec-metasyntax prose as source comments.
- Notes: GEDCOM lines are hierarchical records with a level, optional pointer, tag, and optional payload. User notes are serialized data and must be preserved.

### Examples

#### Unsupported note data
```text
0 @I1@ INDI
1 NAME Ada /Lovelace/
1 NOTE This is genealogical note data, not a source comment.
```

#### No supported comment form
```text
0 HEAD
1 GEDC
2 VERS 7.0
0 TRLR
```

## Gemfile.lock

- Registry key: gemfile_lock
- Version scope: Bundler lockfile parser sections introduced from Bundler 1.0 through 2.5.0 and current Bundler lockfile documentation
- Version-specific syntax: checked Bundler versions add lockfile sections, not comment syntax; no delimiter union is needed
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://bundler.io/man/bundle-lock.1.html
- Implementation source: https://github.com/rubygems/rubygems/blob/master/bundler/lib/bundler/lockfile_parser.rb
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Keep unsupported and exclude this file type from comment parsing tests.
- Notes: Bundler's parser skips blank lines only, recognizes section headings, and dispatches indented content to section parsers. There is no comment-stripping pass.

### Examples

#### No supported comment form
```text
GEM
  remote: https://rubygems.org/
  specs:
    rake (13.2.1)

DEPENDENCIES
  rake
```

#### Invalid comment-like line
```text
# This is not a Gemfile.lock comment.
GEM
  remote: https://rubygems.org/
```

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
- Version scope: Genero Forms `.per` examples in Genero 3.00.06 and 4.01.38 tutorials
- Version-specific syntax: both checked tutorial versions show `--` comments in `.per` form files; no form-file-specific block syntax was confirmed
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
- Version scope: current Git `blame.ignoreRevsFile` / `--ignore-revs-file` documentation and current `oidset_parse_file_carefully` implementation
- Version-specific syntax: no versioned delimiter split found; the format accepts one object id per line with optional whitespace and `#` comments
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: `#` starts a comment anywhere on the line after the line is read; content after `#` is discarded, then whitespace is trimmed
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://git-scm.com/docs/git-blame
- Implementation source: https://github.com/git/git/blob/master/oidset.c
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add `#` line-comment coverage for Git revision-list files such as `.git-blame-ignore-revs`; do not add block comments.
- Notes: The implementation allows trailing comments, leading whitespace, empty lines, and whitespace-only lines before parsing the object id.

### Examples

#### Line comment
```text
# formatting-only rewrite
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  # formatting pass
```

#### No block comment form
```text
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
```

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
- Version scope: current Go module reference for `go.sum` files and current Go command `readGoSum` implementation
- Version-specific syntax: the `go.sum` format is a fixed three-field line format; no checked Go version allows comments in checksum files
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: https://go.dev/ref/mod#go-sum-files
- Implementation source: https://github.com/golang/go/blob/master/src/cmd/go/internal/modfetch/fetch.go; https://github.com/golang/go/blob/master/src/cmd/go/testdata/script/malformed_gosum_issue62345.txt
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Keep unsupported and exclude checksum files from comment parsing coverage.
- Notes: `readGoSum` skips blank lines only and requires exactly three whitespace-separated fields. A Go test fixture shows `rsc.io/quote v1.5.2 # invalid line` fails as five fields, confirming `#` is not a comment.

### Examples

#### No supported comment form
```text
golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c h1:pvCbr/wm8HzDD3fVywevekufpn6tCGPY3spdHeZJEsw=
golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c/go.mod h1:NqM8EUOU14njkJ3fqMW+pc6Ldnwhi/IjpwHt7yyuwOQ=
```

#### Invalid comment-like line
```text
rsc.io/quote v1.5.2 # invalid line
```

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
- Version scope: archived current branch at 3.4.1-SNAPSHOT and tagged release v2.1.0
- Version-specific syntax: current and v2.1.0 compiler grammars agree on `#` line comments; both tokenize `---- ... ----` separately as documentation
- Line comments: `#`
- Block comments: unsupported
- Termination behavior: runs to newline
- Nested comments: unsupported
- Confidence: verified
- Evidence mode: implementation_cross_checked
- Docs source: https://github.com/eclipse-archived/golo-lang/blob/master/doc/basics.adoc
- Implementation source: https://github.com/eclipse-archived/golo-lang/blob/master/src/main/jjtree/org/eclipse/golo/compiler/parser/Golo.jjt
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Implement `#` line comments only; do not treat Golo documentation blocks as comments.
- Notes: The compiler grammar defines `#` as `COMMENT` and `---- ... ----` as `DOCUMENTATION`; official source files use both forms in those distinct roles.

### Examples

#### Line comment
```text
module demo

function main = {
  # temporary note
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
- Version scope: original GML technical report references plus current NetworkX GML parser behavior
- Version-specific syntax: the original format uses a `comment` key-value attribute for graph metadata; common parsers such as NetworkX also accept `#` line comments as lexical comments
- Line comments: `#` in NetworkX/common-parser dialects; no semicolon or slash line comments confirmed
- Block comments: unsupported
- Termination behavior: `#` comments run to the end of the physical line
- Nested comments: unsupported
- Confidence: medium
- Evidence mode: implementation_cross_checked
- Docs source: https://raw.githubusercontent.com/GunterMueller/UNI_PASSAU_FMI_Graph_Drawing/master/GML/gml-technical-report.pdf
- Implementation source: https://networkx.org/documentation/stable/_modules/networkx/readwrite/gml.html; https://github.com/networkx/networkx/blob/main/networkx/readwrite/gml.py
- Community source: https://jakobandersen.github.io/mod/formats/index.html
- Corpus fallback source: not used
- Recommended action: Add `#` line-comment support if the registry targets common Graph Modeling Language parser behavior; do not treat the `comment "..."` key as a lexical comment delimiter.
- Notes: NetworkX tokenization groups `#.*$` with whitespace and skips it. The `comment` key shown in many GML examples is graph data/metadata, not a delimiter pair.

### Examples

#### Line comment
```text
# created by graph exporter
graph [
  node [ id 1 label "A" ]
]
```

#### Comment attribute, not lexical comment
```text
graph [
  comment "This string is a GML attribute value."
  directed 1
]
```

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
- Version scope: current Harbour core preprocessor and Harbour test corpus
- Version-specific syntax: current Harbour supports Clipper-compatible line forms plus C-style multiline comments; strict Clipper mode changes one `NOTE` placement nuance but not the delimiter set
- Line comments: `//`; `&&`; `*` only at the first token on a line; `NOTE` at the start of a new statement
- Block comments: `/* ... */`
- Termination behavior: line comments end at newline; block comments end at the first `*/`; unterminated block comments are reported as errors
- Nested comments: unsupported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: https://github.com/harbour/core/blob/master/src/pp/ppcore.c; https://github.com/harbour/core/blob/master/include/hbpp.h
- Community source: not used
- Corpus fallback source: https://github.com/harbour/core/blob/master/tests/comments.prg
- Recommended action: Add Harbour fixtures for all four line forms and non-nested `/* ... */` blocks; keep `*` and `NOTE` position-sensitive.
- Notes: The preprocessor strips `//` and `&&` for the rest of a line, strips `*` only when no tokens precede it, and strips `NOTE` only as a first/new-statement token. Semicolon is a command separator, not a comment.

### Examples

#### Line comment
```text
// file header comment
* legacy full-line comment
NOTE old-style full-line comment
PROCEDURE Main()
   QOut( "Ok!" )  && inline legacy comment
RETURN
```

#### Block comment
```text
PROCEDURE Main()
   /* multiple
      lines */
   QOut( "Ok!" )
RETURN
```

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
- Version scope: TempleOS archive lexer and current ZealOS lexer
- Version-specific syntax: both checked lexers use the same C-style line comment and nested block-comment handling
- Line comments: `//`
- Block comments: `/* ... */`
- Termination behavior: line comments end at newline; block comments maintain depth and close only after the matching outer `*/`
- Nested comments: supported
- Confidence: high
- Evidence mode: implementation_cross_checked
- Docs source: unresolved
- Implementation source: https://github.com/cia-foundation/TempleOS/blob/archive/Compiler/Lex.HC; https://github.com/Zeal-Operating-System/ZealOS/blob/master/src/Compiler/Lex.ZC
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Add HolyC fixtures for `//` and nested `/* ... */` block comments.
- Notes: Both lexers increment comment depth on nested `/*` and decrement on `*/`; EOF inside a comment returns EOF rather than finding a synthetic closer.

### Examples

#### Line comment
```holyc
U0 Main()
{
  U8 *message = "hello world"; // greeting
  "%s\n", message;
}
```

#### Nested comment
```holyc
/* outer note
   /* nested disabled code */
   still inside outer */
U0 Main() {}
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
- Version scope: HTTP Semantics RFC 9110 field-value grammar, with older RFC 7230-compatible behavior considered through the same ABNF concept
- Version-specific syntax: RFC 9110 defines parenthesized comments only inside specific HTTP field grammars that include `comment`; HTTP messages do not have generic source comments
- Line comments: unsupported
- Block comments: context-sensitive `(...)` field-value comments only where a header field definition allows `comment`
- Termination behavior: generic source-comment termination is unsupported; HTTP field comments use balanced parentheses, allow quoted-pair escapes, and can nest recursively
- Nested comments: supported only inside the RFC field-value `comment` production
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.rfc-editor.org/rfc/rfc9110.html#section-5.6.5; https://www.rfc-editor.org/rfc/rfc9110.html#section-5.6.4
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Keep generic HTTP files unsupported unless the parser becomes context-aware for specific header field grammars; do not add a global parenthesized block delimiter.
- Notes: Treating all parenthesized HTTP text as comments would corrupt valid field values and message bodies. The RFC comment production is protocol grammar, not a free-standing file comment.

### Examples

#### Context-sensitive field comment
```http
User-Agent: ExampleClient/1.0 (compatible; local test)
```

#### Nested field comment production
```http
Example-Field: token (outer (inner) text)
```

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
- Version scope: IRC RFC 2812 message grammar, modern IRC client protocol documentation, and common transcript/log interpretation
- Version-specific syntax: IRC messages/logs are line-oriented transcript data; no checked IRC protocol or log reference defines source comments
- Line comments: unsupported
- Block comments: unsupported
- Termination behavior: unsupported
- Nested comments: unsupported
- Confidence: high
- Evidence mode: official_docs
- Docs source: https://www.rfc-editor.org/rfc/rfc2812#section-2.3.1; https://modern.ircdocs.horse/#message-format
- Implementation source: unresolved
- Community source: not used
- Corpus fallback source: not used
- Recommended action: Keep unsupported.
- Notes: IRC protocol parameters named `comment` are message payload fields such as reasons for KICK/KILL/SQUIT, not lexical comments. Semicolons in RFC examples are explanatory prose formatting, not log syntax.

### Examples

#### No supported comment form
```text
[12:00] <alice> #channel is text in the transcript, not a comment marker
[12:01] *** bob has quit (Quit: leaving)
```

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
