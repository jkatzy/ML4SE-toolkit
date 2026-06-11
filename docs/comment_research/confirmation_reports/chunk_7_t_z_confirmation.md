# Chunk 7 T-Z Implementation Confirmation

## Talon

- Registry key: `talon`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: `.talon` comments use `#` only on their own line; block comments unsupported.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/talon/tree-sitter-talon`
- Implementation version: `tree-sitter-talon` commit `51385e9`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/talon/`
- Designated hello-world source: no official hello-world was found in the grammar repo; parser fixtures in `test/comments.test.js` and corpus files were used as the nearest implementation fixtures.
- Parser command: `tmp/comment_research_confirmation/chunk_7_t_z/.venv/bin/python tmp/comment_research_confirmation/chunk_7_t_z/talon/scripts/parse_talon.py`
- Confirmation verdict: `contradicted`
- Recommended report update: keep the official-doc note that `#` should be own-line, but record that the available implementation grammar accepts trailing `#` as a comment; require policy/dialect review before seeding inline behavior.
- Blockers: no official Talon parser or official hello-world fixture was available.
- Notes: the grammar confirms `#` comments and rejects `/* */`, but it disagrees with the current own-line-only restriction.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| whole-line `#` | `tmp/comment_research_confirmation/chunk_7_t_z/talon/probes/standalone_line.talon` | accepted | accepted | `talon_parse.log`: `standalone_line.talon: error=False` |
| trailing `#` | `tmp/comment_research_confirmation/chunk_7_t_z/talon/probes/trailing_hash.talon` | rejected or not a comment under current report | accepted as `(comment)` | `talon_parse.log`: `trailing_hash.talon: error=False` with trailing `(comment)` |
| block comment | `tmp/comment_research_confirmation/chunk_7_t_z/talon/probes/block_negative.talon` | rejected | rejected | `talon_parse.log`: `block_negative.talon: error=True` |
| nested comment | `unsupported` | unsupported | not tested separately | block syntax is rejected |

### Confirmed Examples

#### Line comment
```talon
# CONFIRM_LINE_COMMENT
-
air: "a"
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

## Tea

- Registry key: `tea`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: unresolved Tea dialect and unresolved comment syntax.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/tea/sublime-tea`
- Implementation version: `pferruggiaro/sublime-tea` commit `62b508c`; reached through Linguist `source.tea` grammar mapping.
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/tea/`
- Designated hello-world source: no implementation hello-world or official parser fixture was found; `README.md` and `tea.JSON-tmlanguage` were the only grammar artifacts.
- Parser command: `node scripts/tokenize_tea.js`
- Confirmation verdict: `partially-confirmed`
- Recommended report update: if the registry key means Linguist's Tea templating grammar, record `//` line comments and `/* ... */` block comments inside Tea code spans; otherwise keep the entry unresolved until the intended dialect is identified.
- Blockers: no official Tea language implementation, syntax manual, or hello-world fixture was found.
- Notes: `#`/`##` appear as operators in this grammar, not comments.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_7_t_z/tea/probes/comments.tea` | tokenized if grammar supports it | tokenized as `comment.line.double-slash.tea` | `tea_tokenize.log`: line 2 comment token |
| block comment | `tmp/comment_research_confirmation/chunk_7_t_z/tea/probes/comments.tea` | tokenized if grammar supports it | tokenized as `comment.block.tea` | `tea_tokenize.log`: line 4 block comment token |
| nested comment | `unsupported` | not tested | not tested | no nesting rule in grammar |
| unsupported form | `tea.JSON-tmlanguage` | `#` not a comment | not tokenized in probe | grammar names `#` patterns as operators |

### Confirmed Examples

#### Line comment
```tea
<%
// CONFIRM_LINE_COMMENT
%>
```

#### Block comment
```tea
<%
/* CONFIRM_BLOCK_COMMENT */
%>
```

#### Nested comment
```text
unsupported
```

## Turing

- Registry key: `turing`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: `%` line comments and non-nested `/* ... */` block comments.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/turing/OpenTuringCompiler`
- Implementation version: OpenTuringCompiler commit `c643d26`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/turing/`
- Designated hello-world source: `test/test13.t` and other `test/*.t` parser fixtures were located.
- Parser command: not completed; required build tools were unavailable.
- Confirmation verdict: `blocked`
- Recommended report update: keep the report at medium confidence; source inspection supports the hypothesis, but this pass did not complete a parser run.
- Blockers: `cmake`, `dparse`, and `dub` were not available in the environment, so OpenTuringCompiler could not be built or run.
- Notes: `src/Turing.g` contains lexer support for `%` and `/* ... */`, but source inspection is not counted as parser confirmation.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | not created | accepted | not tested | `tool_lookup.log` shows missing build tools |
| block comment | not created | accepted | not tested | `tool_lookup.log` shows missing build tools |
| nested comment | not created | rejected | not tested | parser unavailable |
| unsupported form | not created | rejected | not tested | parser unavailable |

### Confirmed Examples

#### Line comment
```text
not tested
```

#### Block comment
```text
not tested
```

#### Nested comment
```text
not tested
```

## TXL

- Registry key: `txl`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: `%` line comments only; block comments unsupported.
- Implementation artifact: FreeTXL binary archive under `tmp/comment_research_confirmation/chunk_7_t_z/txl/download/`
- Implementation version: `TXL v10.8b (13.7.22)`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/txl/`
- Designated hello-world source: FreeTXL distribution fixture `test/question.txl`
- Parser command: `tmp/comment_research_confirmation/chunk_7_t_z/txl/download/txl10.8b.linux64/bin/txl -q -c <probe>`
- Confirmation verdict: `confirmed`
- Recommended report update: seed `%` line-comment coverage only and keep block/nesting unsupported.
- Blockers: none.
- Notes: both standalone and trailing `%` probes were accepted in the same TXL source fixture.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_7_t_z/txl/probes/question_line.txl` | accepted | accepted | `question_line_compile.log` empty, exit 0 |
| block comment | `tmp/comment_research_confirmation/chunk_7_t_z/txl/probes/question_block_negative.txl` | rejected | rejected | `question_block_negative_compile.log`: `TXL0192E` at `/` |
| nested comment | `unsupported` | unsupported | not tested separately | block syntax rejected |
| unsupported form | same as block probe | rejected | rejected | `TXL0192E` |

### Confirmed Examples

#### Line comment
```txl
% CONFIRM_LINE_COMMENT
define program % CONFIRM_TRAILING_PERCENT_COMMENT
        [expression]
end define
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

## Unix Assembly

- Registry key: `unix_assembly`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: GNU as has target-specific line comments; x86/x86-64 GAS uses `#`, and GAS supports non-nested `/* ... */`.
- Implementation artifact: GNU binutils 2.42 source archive plus system GNU assembler
- Implementation version: `GNU assembler (GNU Binutils for Ubuntu) 2.42`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/unix_assembly/`
- Designated hello-world source: binutils parser fixture `gas/testsuite/gas/i386/quoted.s`
- Parser command: `as --64 -o <out.o> <probe.s>`
- Confirmation verdict: `confirmed`
- Recommended report update: confirm only the x86-64 GAS scope for `#`; keep universal Unix assembly line comments dialect-sensitive.
- Blockers: none for x86-64 GAS; other targets were not checked.
- Notes: this does not prove `#` for every assembler target.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_7_t_z/unix_assembly/probes/quoted_comments.s` | accepted for x86-64 GAS | accepted | `quoted_comments_as.log` empty, exit 0 |
| block comment | same file | accepted | accepted | `quoted_comments_as.log` empty, exit 0 |
| nested comment | `tmp/comment_research_confirmation/chunk_7_t_z/unix_assembly/probes/nested_block_negative.s` | rejected | rejected | `nested_block_negative_as.log`: `no such instruction: 'outer */'` |
| unsupported form | same nested probe | rejected | rejected | first `*/` closes block |

### Confirmed Examples

#### Line comment
```asm
	.text
# CONFIRM_LINE_COMMENT
quoted:
```

#### Block comment
```asm
	.text
/* CONFIRM_BLOCK_COMMENT */
quoted:
```

#### Nested comment
```text
unsupported
```

## Valve Data Format

- Registry key: `valve_data_format`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: `//` line comments only; block comments unsupported.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/valve_data_format/vdf`
- Implementation version: ValvePython/vdf commit `d762926`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/valve_data_format/`
- Designated hello-world source: parser fixture `tests/test_vdf.py`, including its comment parsing fixture around lines 276-293
- Parser command: `python tmp/comment_research_confirmation/chunk_7_t_z/valve_data_format/scripts_parse_vdf.py`
- Confirmation verdict: `confirmed`
- Recommended report update: seed `//` line comments only; do not treat `/* ... */` as VDF comments.
- Blockers: none.
- Notes: the block probe was accepted as parseable VDF data, but its inner line was retained as a key/value pair, proving it was not treated as an ignored block comment.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_7_t_z/valve_data_format/probes/line.vdf` | accepted and ignored | accepted as `{'root': {'key': 'value'}}` | `vdf_parse.log` |
| trailing line comment | `tmp/comment_research_confirmation/chunk_7_t_z/valve_data_format/probes/trailing.vdf` | accepted and ignored | accepted as `{'root': {'key': 'value'}}` | `vdf_parse.log` |
| block comment | `tmp/comment_research_confirmation/chunk_7_t_z/valve_data_format/probes/block_negative.vdf` | not treated as a comment | accepted as data with `{'still': 'block */'}` | `vdf_parse.log` |
| nested comment | `unsupported` | unsupported | not tested separately | no block support |

### Confirmed Examples

#### Line comment
```text
"root"
{
    // CONFIRM_LINE_COMMENT
    "key" "value"
}
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

## Vim Help File

- Registry key: `vim_help_file`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: no formal help-file comment syntax.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/vim_help_file/vim/runtime/syntax/help.vim` plus local Vim
- Implementation version: Vim source commit `affd4b5`; local `VIM - Vi IMproved 9.1`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/vim_help_file/`
- Designated hello-world source: scratch help file based on Vim help markup and checked with `helptags`
- Parser command: `vim -Nu NONE -n -es -c 'helptags ...' -c qa`; `vim -Nu NONE -n -es -S tmp/comment_research_confirmation/chunk_7_t_z/vim_help_file/scripts/check_help_syntax.vim`
- Confirmation verdict: `confirmed`
- Recommended report update: keep `vim_help_file` commentless; keep Vimscript quote comments scoped to `vim_script`.
- Blockers: none.
- Notes: `helptags` accepted the help file, and syntax inspection found no `Comment` group for quote, hash, or block-like lines.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| quote-like line | `tmp/comment_research_confirmation/chunk_7_t_z/vim_help_file/probes/help_probe.txt` | content, not comment | no comment syntax group | `help_syntax_probe.log`: `quote=` |
| hash-like line | same file | content, not comment | no comment syntax group | `help_syntax_probe.log`: `hash=` |
| block-like line | same file | content, not comment | no comment syntax group | `help_syntax_probe.log`: `block=` |
| syntax check | copied to `helpdoc/help_probe.txt` | accepted by help tooling | `helptags` exit 0 | `helptags.log` empty |

### Confirmed Examples

#### Line comment
```text
unsupported
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

## Vim Snippet

- Registry key: `vim_snippet`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: `#` whole-line comments outside snippet bodies; no block comments; `#` inside a snippet body is literal.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/vim_snippet/ultisnips`
- Implementation version: UltiSnips commit `403da03`; snipMate docs commit `1331cfe`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/vim_snippet/`
- Designated hello-world source: snipMate and UltiSnips snippet documentation examples; scratch file parsed with UltiSnips parser.
- Parser command: `python tmp/comment_research_confirmation/chunk_7_t_z/vim_snippet/scripts/parse_ultisnips.py`
- Confirmation verdict: `confirmed`
- Recommended report update: seed `#` whole-line comments only outside snippet bodies; parser support must be context-aware.
- Blockers: none for UltiSnips-style parsing.
- Notes: the top-level `#` line produced no snippet event, while the body `#` remained in `_value`.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| outside `#` line | `tmp/comment_research_confirmation/chunk_7_t_z/vim_snippet/probes/snippet_probe.snippets` | ignored as comment/header | no event emitted | `ultisnips_parse.log`: two snippet events only |
| body `#` line | same file | literal snippet text | `_value='hello\n# CONFIRM_HASH_LITERAL_INSIDE_SNIPPET'` | `ultisnips_parse.log` |
| block comment | same file | rejected or invalid | emitted invalid-line error event | `ultisnips_parse.log`: `Invalid line '/* CONFIRM_BLOCK_UNSUPPORTED */'` |
| nested comment | `unsupported` | unsupported | not tested separately | no block syntax |

### Confirmed Examples

#### Line comment
```snippets
# CONFIRM_HASH_COMMENT_OUTSIDE_SNIPPET
snippet hello
hello
endsnippet
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```

## X BitMap

- Registry key: `x_bit_map`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: XBM is C source; portable comments are C89 `/* ... */`; `//` depends on a modern C/C++ carrier.
- Implementation artifact: X.Org `xbitmaps-1.1.3` fixture plus GCC syntax checks
- Implementation version: `xbitmaps-1.1.3`; GCC `13.3.0`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/x_bit_map/`
- Designated hello-world source: `xbitmaps-1.1.3/dot`
- Parser command: `gcc -std=c89 -pedantic-errors -fsyntax-only -x c <probe>` and `gcc -std=c99 -pedantic-errors -fsyntax-only -x c <probe>`
- Confirmation verdict: `confirmed`
- Recommended report update: seed `/* ... */` for portable XBM; treat `//` as dialect-dependent.
- Blockers: none.
- Notes: C89/C99 warnings about `char` overflow are unrelated to comment syntax; the syntax-check exit code distinguishes accepted and rejected comment forms.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| block comment | `tmp/comment_research_confirmation/chunk_7_t_z/x_bit_map/probes/dot_block_probe.xbm` | accepted under C89 | accepted | `dot_block_c89.log`, exit 0 |
| `//` line comment in C89 | `tmp/comment_research_confirmation/chunk_7_t_z/x_bit_map/probes/dot_line_probe.xbm` | rejected in strict C89 | rejected | `dot_line_c89.log`: `C++ style comments are not allowed in ISO C90` |
| `//` line comment in C99 | same file | accepted in modern C | accepted | `dot_line_c99.log`, exit 0 |
| nested block | `tmp/comment_research_confirmation/chunk_7_t_z/x_bit_map/probes/dot_nested_negative.xbm` | rejected | rejected | `dot_nested_c89.log`: `unknown type name 'outer'` |

### Confirmed Examples

#### Line comment
```c
// CONFIRM_LINE_COMMENT
#define dot_width 16
```

#### Block comment
```c
/* CONFIRM_BLOCK_COMMENT */
#define dot_width 16
```

#### Nested comment
```text
unsupported
```

## X PixMap

- Registry key: `x_pix_map`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: XPM3/C-style XPM supports C `/* ... */`; `//` depends on the carrier dialect; XPM2 should not inherit C comments without format detection.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/x_pix_map/libxpm`
- Implementation version: libXpm commit `90f573b`; GCC `13.3.0`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/x_pix_map/`
- Designated hello-world source: libXpm fixture `test/pixmaps/good/plaid-v3.xpm`
- Parser command: `gcc -std=c89 -pedantic-errors -fsyntax-only -x c <probe>` and `gcc -std=c99 -pedantic-errors -fsyntax-only -x c <probe>`
- Confirmation verdict: `confirmed`
- Recommended report update: seed `/* ... */` for XPM3/C-style files; keep `//` dialect-dependent and keep nesting unsupported.
- Blockers: none for XPM3/C-style files.
- Notes: the fixture itself begins with the common `/* XPM */` block comment.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| block comment | `tmp/comment_research_confirmation/chunk_7_t_z/x_pix_map/probes/plaid_v3_block_probe.xpm` | accepted under C89 | accepted | `plaid_v3_block_c89.log` empty, exit 0 |
| `//` line comment in C89 | `tmp/comment_research_confirmation/chunk_7_t_z/x_pix_map/probes/plaid_v3_line_probe.xpm` | rejected in strict C89 | rejected | `plaid_v3_line_c89.log`: `C++ style comments are not allowed in ISO C90` |
| `//` line comment in C99 | same file | accepted in modern C | accepted | `plaid_v3_line_c99.log` empty, exit 0 |
| nested block | `tmp/comment_research_confirmation/chunk_7_t_z/x_pix_map/probes/plaid_v3_nested_negative.xpm` | rejected | rejected | `plaid_v3_nested_c89.log`: `unknown type name 'outer'` |

### Confirmed Examples

#### Line comment
```c
// CONFIRM_LINE_COMMENT
/* XPM */
```

#### Block comment
```c
/* XPM */
/* CONFIRM_BLOCK_COMMENT */
static char * plaid[] = {
```

#### Nested comment
```text
unsupported
```

## X10

- Registry key: `x10`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: Java-style `//`, `/* ... */`, and `/** ... */`; nested block comments unsupported.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/x10/x10`
- Implementation version: x10 repository commit `5412ae0`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/x10/`
- Designated hello-world source: `x10.dist/samples/HelloWorld.x10`
- Parser command: not completed; no local Java/X10 build tool was available.
- Confirmation verdict: `blocked`
- Recommended report update: keep existing medium-confidence implementation-cross-checked text, but do not mark final-confirmed from this pass.
- Blockers: `java`, `javac`, `ant`, and `gradle` were unavailable in the environment.
- Notes: source search found `HelloWorld.x10` and `X10Lexer.java`, but source inspection alone is not parser confirmation.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | not created | accepted | not tested | `tool_lookup.log` shows missing build tools |
| block comment | not created | accepted | not tested | parser unavailable |
| docblock | not created | accepted | not tested | parser unavailable |
| nested block | not created | rejected | not tested | parser unavailable |

### Confirmed Examples

#### Line comment
```text
not tested
```

#### Block comment
```text
not tested
```

#### Nested comment
```text
not tested
```

## xBase

- Registry key: `xbase`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: Harbour/Clipper-compatible union of `//`, `&&`, leading statement `*`, `NOTE`/`NOTE*`, and non-nested `/* ... */`.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/xbase/harbour-core`
- Implementation version: Harbour commit `0d3b439`; built as `Harbour 3.2.0dev (r2605141250)`, ChangeLog ID `d63137680d74e8ad68e2ce65f7eea13908bb8d08`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/xbase/`
- Designated hello-world source: Harbour fixture `tests/hello.prg`
- Parser command: `tmp/comment_research_confirmation/chunk_7_t_z/xbase/harbour-core/bin/linux/gcc/harbour <probe.prg> -s -q0 -itmp/comment_research_confirmation/chunk_7_t_z/xbase/harbour-core/include`
- Confirmation verdict: `confirmed`
- Recommended report update: confirm the Harbour/Clipper implementation scope; keep the recommendation to split dialects if the registry key should not be a broad xBase union.
- Blockers: none.
- Notes: the positive syntax-only run accepted all tested line/statement/block forms; the nested block probe failed at the second `*`.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| `//` line | `tmp/comment_research_confirmation/chunk_7_t_z/xbase/probes/hello_comments.prg` | accepted | accepted | `hello_comments_syntax.log` empty, exit 0 |
| `&&` trailing line | same file | accepted | accepted | `hello_comments_syntax.log` empty, exit 0 |
| leading `*` | same file | accepted | accepted | `hello_comments_syntax.log` empty, exit 0 |
| `NOTE`/`NOTE*` | same file | accepted | accepted | `hello_comments_syntax.log` empty, exit 0 |
| block comment | same file | accepted | accepted | `hello_comments_syntax.log` empty, exit 0 |
| nested block | `tmp/comment_research_confirmation/chunk_7_t_z/xbase/probes/hello_nested_negative.prg` | rejected | rejected | `hello_nested_negative_syntax.log`: syntax error at `*` |

### Confirmed Examples

#### Line comment
```xbase
* CONFIRM_STAR_LINE_COMMENT
NOTE CONFIRM_NOTE_COMMENT
NOTE* CONFIRM_NOTESTAR_COMMENT
? "Goodbye!" && CONFIRM_AMPERSAND_LINE_COMMENT
```

#### Block comment
```xbase
/* CONFIRM_BLOCK_COMMENT */
RETURN
```

#### Nested comment
```text
unsupported
```

## XC

- Registry key: `xc`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: XMOS XC extends C, so `//` and `/* ... */` apply; nested block comments unsupported.
- Implementation artifact: no runnable XC compiler artifact obtained; XMOS software tools page downloaded to scratch.
- Implementation version: unresolved.
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/xc/`
- Designated hello-world source: none located.
- Parser command: not completed.
- Confirmation verdict: `blocked`
- Recommended report update: keep current docs-based recommendation, but do not mark implementation-confirmed until an XTC/XCC parse run is completed.
- Blockers: `xcc`, `xrun`, and `xmake` were unavailable; no noninteractive official compiler download was found from the software tools page during this pass.
- Notes: this pass did not test XC syntax with a compiler.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | not created | accepted | not tested | `tool_lookup.log`: no `xcc`/`xrun`/`xmake` |
| block comment | not created | accepted | not tested | compiler unavailable |
| nested block | not created | rejected | not tested | compiler unavailable |
| unsupported form | not created | rejected | not tested | compiler unavailable |

### Confirmed Examples

#### Line comment
```text
not tested
```

#### Block comment
```text
not tested
```

#### Nested comment
```text
not tested
```

## ZIL

- Registry key: `zil`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: semicolon comments the following ZIL expression; common `;"..."` string comments are not simple semicolon-to-EOL comments.
- Implementation artifact: ZILF release under `tmp/comment_research_confirmation/chunk_7_t_z/zil/release/`; ZILF source and reference guide also cloned.
- Implementation version: ZILF release `1.8`; source commit `ab9898e`; reference guide commit `d3bc624`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/zil/`
- Designated hello-world source: ZILF release sample `sample/hello/hello.zil`
- Parser command: `tmp/comment_research_confirmation/chunk_7_t_z/zil/release/zilf-1.8.0-linux-x64/bin/zilf build <probe.zil> <probe.zap>`
- Confirmation verdict: `confirmed`
- Recommended report update: keep the warning not to implement ZIL as semicolon-to-EOL; either support conservative `;"..."` comments or use expression-aware handling for `;` comments.
- Blockers: none.
- Notes: generated ZAP for `hello_expression_scope.zil` retained `PRINTI "CONFIRM_AFTER_SAME_LINE"` after a preceding commented expression on the same physical line.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| `;"..."` standalone | `tmp/comment_research_confirmation/chunk_7_t_z/zil/probes/hello_comments.zil` | accepted and omitted from output | accepted | `hello_comments_build.log` exit 0; generated ZAP omits marker |
| `;"..."` trailing | same file | accepted | accepted | `hello_comments_build.log` exit 0 |
| semicolon expression comment | same file | accepted and omitted | accepted | generated ZAP omits `CONFIRM_EXPRESSION_COMMENT` |
| same-line expression scope | `tmp/comment_research_confirmation/chunk_7_t_z/zil/probes/hello_expression_scope.zil` | following expression remains active | accepted; ZAP contains only `CONFIRM_AFTER_SAME_LINE` | `hello_expression_scope_build.log`; `hello_expression_scope.zap` |
| nested comment delimiter | `unsupported` | unsupported | not tested separately | no separate delimiter exists |

### Confirmed Examples

#### Line comment
```zil
;"CONFIRM_STRING_COMMENT"
<ROUTINE GO ()
    <PRINTI "Hello, world!">>
```

#### Block comment
```zil
<ROUTINE GO ()
    ;<PRINTI "CONFIRM_COMMENTED_EXPRESSION"> <PRINTI "CONFIRM_AFTER_SAME_LINE">
    <CRLF>>
```

#### Nested comment
```text
unsupported as a separate delimiter; expression nesting is parser-dependent
```

## Zimpl

- Registry key: `zimpl`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_7_t_z_report.md`
- Current hypothesis: `#` line comments only; block comments unsupported.
- Implementation artifact: `tmp/comment_research_confirmation/chunk_7_t_z/zimpl/zimpl`
- Implementation version: Zimpl commit `c3f9d4d`; built binary reports `3.8.0`
- Local scratch path: `tmp/comment_research_confirmation/chunk_7_t_z/zimpl/`
- Designated hello-world source: Zimpl repository example `example/ex1.zpl`
- Parser command: `ASAN_OPTIONS=detect_leaks=0 tmp/comment_research_confirmation/chunk_7_t_z/zimpl/zimpl/bin/zimpl-3.8.0.linux.x86_64.gnu.static.dbg -v0 -t lp -o <out> <probe.zpl>`
- Confirmation verdict: `confirmed`
- Recommended report update: seed hash line-comment tests and keep block/nesting unsupported.
- Blockers: none after local dependency build; `ASAN_OPTIONS=detect_leaks=0` was required in this container.
- Notes: block syntax produced a scanner syntax error at `/*`.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| standalone `#` | `tmp/comment_research_confirmation/chunk_7_t_z/zimpl/probes/ex1_hash.zpl` | accepted | accepted | `ex1_hash.log` empty, exit 0 |
| trailing `#` | same file | accepted | accepted | `ex1_hash.log` empty, exit 0 |
| block comment | `tmp/comment_research_confirmation/chunk_7_t_z/zimpl/probes/ex1_block_negative.zpl` | rejected | rejected | `ex1_block_negative.log`: `Syntax Error` at `/*` |
| nested comment | `unsupported` | unsupported | not tested separately | block syntax rejected |

### Confirmed Examples

#### Line comment
```zimpl
# CONFIRM_HASH_LINE_COMMENT
maximize profit: 25 * XB + 30 * XC; # CONFIRM_TRAILING_HASH_COMMENT
```

#### Block comment
```text
unsupported
```

#### Nested comment
```text
unsupported
```
