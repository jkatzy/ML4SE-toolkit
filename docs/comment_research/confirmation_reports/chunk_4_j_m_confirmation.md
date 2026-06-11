# Chunk 4 J-M Implementation Confirmation

Scratch root: `tmp/comment_research_confirmation/chunk_4_j_m/`

## JetBrains MPS

- Registry key: `jetbrains_mps`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_4_j_m_report.md`
- Current hypothesis: MPS editors are projectional and do not define a universal textual comment token. Persisted `.mps`, `.mpl`, and `.msd` files are XML-family artifacts; only XML comments are defensible for persisted files.
- Implementation artifact: `https://github.com/JetBrains/MPS`
- Implementation version: `f55d3b50e1675aa62f1d63895644f55d15edf827`
- Local scratch path: `tmp/comment_research_confirmation/chunk_4_j_m/jetbrains_mps/`
- Designated hello-world source: `MPS/jps/testData/makeTests/models/MainJava.mps`, a minimal persisted model fixture in MPS test data.
- Parser command: `xmllint --noout mps_probe.mps`; negative checks used `xmllint --noout mps_nested_bad.mps` and `xmllint --noout mps_slash_bad.mps`.
- Confirmation verdict: `partially-confirmed`
- Recommended report update: Keep the entry scoped to persisted XML-family files: XML comments are accepted by an XML parser on an official MPS persisted-model fixture, while `//` and nested XML comments are rejected. A full MPS model-loader command was not available in this environment.
- Blockers: No local Java runtime or MPS command-line loader was available, so this did not execute the MPS loader itself.
- Notes: This confirms the XML syntax surface, not projectional editor comments.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_4_j_m/jetbrains_mps/mps_slash_bad.mps` | rejected | rejected | `mps_slash_bad_xmllint.log`: start tag expected before `// CONFIRM_UNSUPPORTED_LINE_COMMENT`, exit 4. |
| block comment | `tmp/comment_research_confirmation/chunk_4_j_m/jetbrains_mps/mps_probe.mps` | accepted | accepted | `mps_probe_xmllint.log`: exit 0. |
| nested comment | `tmp/comment_research_confirmation/chunk_4_j_m/jetbrains_mps/mps_nested_bad.mps` | rejected | rejected | `mps_nested_bad_xmllint.log`: double hyphen within comment, exit 4. |
| unsupported form | `tmp/comment_research_confirmation/chunk_4_j_m/jetbrains_mps/mps_slash_bad.mps` | rejected | rejected | Same as line-comment negative probe. |

### Confirmed Examples

#### Line comment
Unsupported.

#### Block comment
```text
<?xml version="1.0" encoding="UTF-8"?>
<!-- CONFIRM_BLOCK_COMMENT before model root -->
<model ref="r:43edf40c-3819-4ead-8c10-8918d564d607(MainJava)">
  <persistence version="9" />
```

#### Nested comment
Unsupported.

## Lasso

- Registry key: `lasso`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_4_j_m_report.md`
- Current hypothesis: LassoScript uses `//` single-line and `/* ... */` block comments; no versioned nested comment form was found.
- Implementation artifact: Packet source `https://github.com/SublimeText/Lasso` was not publicly cloneable. Fallback grammar/tokenizer artifact used: `https://github.com/bfad/Sublime-Lasso`.
- Implementation version: `c755cf53bed8f81dcfbe937f9feaa9e564f1c2a9`
- Local scratch path: `tmp/comment_research_confirmation/chunk_4_j_m/lasso/`
- Designated hello-world source: No hello-world fixture exists in the package; `Sublime-Lasso/Snippets/local.sublime-snippet` was the minimal package-provided Lasso snippet source.
- Parser command: `node tokenize_lasso.js probe.lasso`; attempted compiler check `Sublime-Lasso/Build/check_syntax.sh probe.lasso`.
- Confirmation verdict: `partially-confirmed`
- Recommended report update: Keep `//` and `/* ... */` as grammar-confirmed Lasso forms, with no nested block support. Do not upgrade to fully confirmed until `/usr/bin/lassoc` or another real Lasso compiler/parser is available.
- Blockers: `Sublime-Lasso/Build/check_syntax.sh` invokes `/usr/bin/lassoc`, which is not installed; the script logged `No such file or directory`.
- Notes: The TextMate tokenizer scoped the supported forms as `comment.*.lasso` and left `#` unscoped as a comment.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_4_j_m/lasso/probe.lasso` | accepted | accepted by grammar tokenizer | `lasso_tokenize.log`: both standalone and trailing `//` scoped as `comment.line.double-slash.lasso`. |
| block comment | `tmp/comment_research_confirmation/chunk_4_j_m/lasso/probe.lasso` | accepted | accepted by grammar tokenizer | `lasso_tokenize.log`: `/* ... */` scoped as `comment.block.lasso`. |
| nested comment | `tmp/comment_research_confirmation/chunk_4_j_m/lasso/probe.lasso` | rejected/non-nesting | first `*/` ended the comment | `lasso_tokenize.log`: nested probe comment scope ended at inner `*/`; remaining text was not comment-scoped. |
| unsupported form | `tmp/comment_research_confirmation/chunk_4_j_m/lasso/probe.lasso` | not a comment | not comment-scoped | `lasso_tokenize.log`: `# CONFIRM_UNSUPPORTED_HASH_COMMENT` scoped only as `file.lasso source.lasso`. |

### Confirmed Examples

#### Line comment
```text
// CONFIRM_LINE_COMMENT standalone
local(myName) = 'Ada' // CONFIRM_LINE_COMMENT trailing
```

#### Block comment
```text
/* CONFIRM_BLOCK_COMMENT before value */
local(total) = 10
```

#### Nested comment
Unsupported.

## LoomScript

- Registry key: `loomscript`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_4_j_m_report.md`
- Current hypothesis: LoomScript is ActionScript/ECMAScript-like and uses `//` and `/* ... */` comments. No nested block form was found.
- Implementation artifact: `https://github.com/LoomSDK/LoomSDK`
- Implementation version: `c6ff83f99b313f402326948c57661908933dabdd`
- Local scratch path: `tmp/comment_research_confirmation/chunk_4_j_m/loomscript/`
- Designated hello-world source: `LoomSDK/docs/examples/HelloQuad/src/HelloQuad.ls`
- Parser command: `node tokenize_loomscript.js probe.ls`
- Confirmation verdict: `partially-confirmed`
- Recommended report update: Keep `//` and `/* ... */` with first-terminator block behavior. The SDK lexer source and bundled grammar agree, but the full LoomScript compiler was not built or run.
- Blockers: The official compiler/lexer sources are not exposed as a small standalone syntax-check command; compiling the full SDK was out of scope for this packet.
- Notes: `loom/script/compiler/lsLexer.cpp` contains `tokenizeSingleLineComment`, `tokenizeMultilineComment`, and slash dispatch matching the grammar-tokenizer result.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_4_j_m/loomscript/probe.ls` | accepted | accepted by SDK grammar tokenizer | `loomscript_tokenize.log`: standalone and trailing `//` scoped as `comment.line.double-slash.loomscript.2`. |
| block comment | `tmp/comment_research_confirmation/chunk_4_j_m/loomscript/probe.ls` | accepted | accepted by SDK grammar tokenizer | `loomscript_tokenize.log`: `/* ... */` scoped as `comment.block.loomscript.2`. |
| nested comment | `tmp/comment_research_confirmation/chunk_4_j_m/loomscript/probe.ls` | rejected/non-nesting | first `*/` ended the comment | `loomscript_tokenize.log`: nested probe comment scope ended at inner `*/`. |
| unsupported form | `tmp/comment_research_confirmation/chunk_4_j_m/loomscript/probe.ls` | not a comment | not comment-scoped | `loomscript_tokenize.log`: `# CONFIRM_UNSUPPORTED_HASH_COMMENT` scoped only as `source.loomscript.2`. |

### Confirmed Examples

#### Line comment
```text
// CONFIRM_LINE_COMMENT standalone
import loom.Application; // CONFIRM_LINE_COMMENT trailing
```

#### Block comment
```text
/* CONFIRM_BLOCK_COMMENT before imports */
import loom.Application;
```

#### Nested comment
Unsupported.

## LTspice Symbol

- Registry key: `ltspice_symbol`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_4_j_m_report.md`
- Current hypothesis: No official textual comment delimiter was confirmed for `.asy` symbol files. The format is record-oriented, and public examples do not show a stable comment token.
- Implementation artifact: Proprietary LTspice parser; no public parser source found.
- Implementation version: unavailable
- Local scratch path: `tmp/comment_research_confirmation/chunk_4_j_m/ltspice_symbol/`
- Designated hello-world source: not found
- Parser command: not run
- Confirmation verdict: `blocked`
- Recommended report update: Leave unresolved and do not add a delimiter. A future confirmation needs an installed LTspice parser, documented command-line syntax check, or another trusted `.asy` parser.
- Blockers: No LTspice executable, Wine runtime, or public parser source was available. The packet docs URL returned HTTP 404 in `curl_symbol_editor.log`.
- Notes: `ltspice_tool_availability.log` records `wine=None`, `LTspice=None`, `ltspice=None`, `XVIIx64.exe=None`, and `XVIIx86.exe=None`.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `unsupported` | not tested | not tested | No parser command available. |
| block comment | `unsupported` | unsupported | not tested | No parser command available. |
| nested comment | `unsupported` | unsupported | not tested | No parser command available. |
| unsupported form | `unsupported` | not tested | not tested | No parser command available. |

### Confirmed Examples

#### Line comment
Unsupported or unresolved.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## Mask

- Registry key: `mask`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_4_j_m_report.md`
- Current hypothesis: Mask templates use JavaScript/CSS-style `//` line comments and `/* ... */` block comments in template source. No nested form was confirmed.
- Implementation artifact: `https://github.com/atmajs/maskjs`; parser executed from local npm package `maskjs@0.73.3`.
- Implementation version: Git checkout `f3951546aa9b5ada57fe66a35e7fa4809108f6c2`; npm package `0.73.3`.
- Local scratch path: `tmp/comment_research_confirmation/chunk_4_j_m/mask/`
- Designated hello-world source: `maskjs/examples/components/foo.mask`
- Parser command: `node parse_mask_probe.js foo_probe.mask`; negative checks used `foo_nested_bad.mask` and `foo_hash_bad.mask`.
- Confirmation verdict: `confirmed`
- Recommended report update: Mark ready to implement with `//` and `/* ... */`, first closing `*/` wins, no nested block comments.
- Blockers: none for the published parser package.
- Notes: The first harness version missed MaskJS event diagnostics; `parse_mask_probe.js` now treats emitted `error` and `warn` events as parser rejection.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_4_j_m/mask/foo_probe.mask` | accepted | accepted | `mask_parse_foo_positive.log`: `foo_probe.mask: accepted: nodes=2`, exit 0. |
| block comment | `tmp/comment_research_confirmation/chunk_4_j_m/mask/foo_probe.mask` | accepted | accepted | Same positive parser log. |
| nested comment | `tmp/comment_research_confirmation/chunk_4_j_m/mask/foo_nested_bad.mask` | rejected | rejected | `mask_parse_foo_nested_bad.log`: unexpected `/` after first `*/`, exit 1. |
| unsupported form | `tmp/comment_research_confirmation/chunk_4_j_m/mask/foo_hash_bad.mask` | rejected | rejected | `mask_parse_foo_hash.log`: string expected after `#`, exit 1. |

### Confirmed Examples

#### Line comment
```text
// CONFIRM_LINE_COMMENT standalone
define foo extends Panel {
	@title > 'Foo title' // CONFIRM_LINE_COMMENT trailing
```

#### Block comment
```text
define foo extends Panel {
	@title > 'Foo title'
	/* CONFIRM_BLOCK_COMMENT between nodes */
	@body {
```

#### Nested comment
Unsupported.

## Microsoft Developer Studio Project

- Registry key: `msdev_project`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_4_j_m_report.md`
- Current hypothesis: `.dsp` files use `#`-prefixed lines for generated file headers, section markers, and comments. No block syntax was found.
- Implementation artifact: `https://github.com/Kitware/CMake`
- Implementation version: Current checkout `ee9b10bc72e8b3a0de745d59bf1b929f0d21dd6c`; historical tags `v3.0.0` and `v2.8.12` checked for `.dsp` fixtures.
- Local scratch path: `tmp/comment_research_confirmation/chunk_4_j_m/msdev_project/`
- Designated hello-world source: `CMake/Utilities/cmbzip2/libbz2.dsp` from CMake `v3.0.0`, plus `CMake/Modules/CompilerId/VS-6.dsp.in`.
- Parser command: not run
- Confirmation verdict: `blocked`
- Recommended report update: Keep as candidate, but do not call this implementation-confirmed until Visual Studio Developer Studio, `msdev`, or another real `.dsp` parser is available. The corpus/templates continue to support `#` lines as a candidate syntax.
- Blockers: The packet-cited `Source/cmDSPParser.cxx` is absent from current CMake and from checked historical tags; local `devenv`, `VCExpress`, `msdev`, `cmake`, and `nmake` are unavailable.
- Notes: `v2812_dsp_paths.log` and `msdev_tool_availability.log` record the fixture paths and unavailable parser tools.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `CMake/Utilities/cmbzip2/libbz2.dsp` | accepted | not tested | No parser command available; fixture contains generated `#` header and section lines. |
| block comment | `unsupported` | unsupported | not tested | No parser command available. |
| nested comment | `unsupported` | unsupported | not tested | No parser command available. |
| unsupported form | `unsupported` | not tested | not tested | No parser command available. |

### Confirmed Examples

#### Line comment
Not implementation-confirmed.

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## MUF

- Registry key: `muf`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_4_j_m_report.md`
- Current hypothesis: MUF uses parenthesized comments `( ... )` and backslash line comments in common Forth-derived implementations. No true nested comment support was confirmed.
- Implementation artifact: `https://github.com/fuzzball-muck/fuzzball`
- Implementation version: `139ae88b1044ac80e5d068966c633423d4971178`
- Local scratch path: `tmp/comment_research_confirmation/chunk_4_j_m/muf/`
- Designated hello-world source: `fuzzball/tests/command-cases/p_misc.yml` and sibling command-case fixtures containing minimal `@program test.muf` compile/run examples.
- Parser command: Fuzzball was configured with local PCRE and built with `make`; parser probes used pty command runs such as `script -q -c "env LD_LIBRARY_PATH=... fuzzball/src/fbmuck -dbin .../minimal.db -dbout dbout -gamedir ... -console -parmfile test_parm_file" manual_muf_pty_block.log < manual_game6/input.txt`.
- Confirmation verdict: `contradicted`
- Recommended report update: Remove `\` as a Fuzzball MUF line comment. Confirm parenthesized `( ... )` comments. Default `muf_comments_strict=yes` rejects nested comments, but `$pragma comment_recurse` enables recursive parenthesized comments; either document that version/dialect nuance or keep registry support to the default non-nesting form.
- Blockers: none after local PCRE install; prompt-based Python test harness timed out with pipe I/O, so pty `script` was used.
- Notes: `configure_pcre.log` and `make.log` show successful local build. `manual_muf_pty_positive.log` shows `\` rejected as an unrecognized word. `manual_muf_pty_block.log`, `manual_muf_pty_nested.log`, and `manual_muf_pty_recurse.log` show block, default nested, and pragma-recursive behavior.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_4_j_m/muf/manual_game5/input.txt` | accepted per current hypothesis | rejected | `manual_muf_pty_positive.log`: compiler error `Unrecognized word \`; action later reports unable to compile. |
| block comment | `tmp/comment_research_confirmation/chunk_4_j_m/muf/manual_game6/input.txt` | accepted | accepted | `manual_muf_pty_block.log`: program compiled successfully and action printed `Block complete.` |
| nested comment | `tmp/comment_research_confirmation/chunk_4_j_m/muf/manual_game7/input.txt` | rejected by default | rejected by default | `manual_muf_pty_nested.log`: compiler error `Unrecognized word still.` |
| unsupported form | `tmp/comment_research_confirmation/chunk_4_j_m/muf/manual_game8/input.txt` | not in current hypothesis | accepted with pragma | `manual_muf_pty_recurse.log`: `$pragma comment_recurse` compiled successfully and action printed `Recurse complete.` |

### Confirmed Examples

#### Line comment
Unsupported in Fuzzball MUF.

#### Block comment
```text
( CONFIRM_BLOCK_COMMENT standalone )
: main
  1 pop
  ( CONFIRM_BLOCK_COMMENT between statements )
  me @ "Block complete." notify
;
```

#### Nested comment
```text
$pragma comment_recurse
: main
  ( CONFIRM_NESTED_COMMENT outer ( inner ) still outer )
  me @ "Recurse complete." notify
;
```

## Muse

- Registry key: `muse`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_4_j_m_report.md`
- Current hypothesis: No stable, language-level comment delimiter was confirmed for Muse markup. HTML comments may occur in emitted/embedded HTML, but that is HTML rather than Muse-native syntax.
- Implementation artifact: `https://git.savannah.gnu.org/git/emacs/elpa.git`, branch `externals/muse`
- Implementation version: `8710adde8fef5fb570e23383900f5cfa1d39060c`
- Local scratch path: `tmp/comment_research_confirmation/chunk_4_j_m/muse/`
- Designated hello-world source: `muse-external/examples/QuickStart.muse`
- Parser command: `EMACS=.../emacs-env/bin/emacs SITEFLAG=--no-site-file ../scripts/publish html QuickStart_probe.muse`; nested check used `QuickStart_nested_probe.muse`.
- Confirmation verdict: `contradicted`
- Recommended report update: Replace unresolved Muse entry with native Muse comments: line comments are `; ` only at the beginning of a line, and block/region comments use `<comment> ... </comment>`. Nested `<comment>` regions are unsupported; the first `</comment>` ends the region.
- Blockers: none after local scratch-only Emacs install.
- Notes: The Muse manual section “Lines to omit from published output” and `muse-publish.el` agree with the publisher behavior. `//` remained published as paragraph text, confirming it is unsupported.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_4_j_m/muse/muse-external/examples/QuickStart_probe.muse` | unresolved in current hypothesis | accepted and removed from output | `muse_publish_probe.log`: publish exit 0; `CONFIRM_LINE_COMMENT` absent from HTML. |
| block comment | `tmp/comment_research_confirmation/chunk_4_j_m/muse/muse-external/examples/QuickStart_probe.muse` | unresolved in current hypothesis | accepted and removed from output | `muse_publish_probe.log`: publish exit 0; `CONFIRM_BLOCK_COMMENT` absent from HTML. |
| nested comment | `tmp/comment_research_confirmation/chunk_4_j_m/muse/muse-external/examples/QuickStart_nested_probe.muse` | unsupported | first closing `</comment>` ended the region | `muse_publish_nested_probe.log`: `still outer` remained in HTML while inner text was removed. |
| unsupported form | `tmp/comment_research_confirmation/chunk_4_j_m/muse/muse-external/examples/QuickStart_probe.muse` | unsupported | published as ordinary text | `muse_publish_probe.log`: `// CONFIRM_UNSUPPORTED_SLASH_COMMENT` appears in generated HTML. |

### Confirmed Examples

#### Line comment
```text
#author John Wiegley and Michael Olson
#title The Emacs Muse
; CONFIRM_LINE_COMMENT standalone
```

#### Block comment
```text
<comment>
CONFIRM_BLOCK_COMMENT region
</comment>
```

#### Nested comment
Unsupported.
