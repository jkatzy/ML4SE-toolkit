# Comment Syntax Matrix

Development note: this file tracks Stack v2 comment-syntax expansion evidence.
It is a development artifact under the git workflow; promote only stable code,
tests, and user-facing docs before merging to `main`.

## 2026-07-24 Stack v2 Audit Status

Audit command: `uv run --with datasets python ...` using
`scripts/build_stack_v2_comment_judge_cases.py` against
`bigcode/the-stack-v2`.

- Stack v2 configs: `659`
- Raw Stack v2 configs resolved by the registry: `622`
- Registry keys including aliases: `671`
- Remaining unresolved Stack v2 configs: `37`

The registry only maps formats with documented lexical or structural comment
behavior. The remaining labels are left unsupported rather than represented as
empty syntaxes or broad data-format guesses.

## Source-Backed Additions

| Registry keys | Syntax implemented | Evidence | Status |
| --- | --- | --- | --- |
| `cue_sheet` | `REM` comment commands | CUE sheet specification (`https://wyday.com/cuesharp/specification.php`) | New family |
| `e` | `#` line comments | E language docs and legacy syntax references | Alias added |
| `edje_data_collection`, `eq`, `jest_snapshot`, `type_language` | `//` and `/* ... */` comments | EDC/Linguist C++ scope, EQ C-style samples, Jest snapshot JS scope, Type Language samples | Alias batch added |
| `git_revision_list` | `#` line comments | Git `--ignore-revs-file` docs (`https://git-scm.com/docs/git-blame`) | Alias added |
| `charity` | `%` line comments | Linguist Charity sample | Alias added |
| `jetbrains_mps` | XML comments `<!-- ... -->` | Linguist MPS XML samples | Alias added |
| `object_data_instance_notation` | `--` line comments | openEHR ODIN docs (`https://github.com/openEHR/odin`) | Alias added |
| `pic` | `#` line comments | GNU pic manual excerpts (`https://pikchr.org/home/uv/gpic.pdf`) | Alias added |
| `rouge` | Semicolon comments via Clojure scope | Linguist `source.clojure` language metadata | Alias added |
| `x_bit_map`, `x_bitmap`, `x_pix_map`, `x_pixmap` | C-style comments | XBM/XPM C-source form | Alias batch added |
| `ltspice_symbol` | `;` comments and leading `*` SPICE comments | LTspice symbol guidance and LTspice/SPICE conventions | New family |
| `muse` | Leading `; ` lines and `<comment>...</comment>` regions | GNU Emacs Muse manual (`https://www.gnu.org/software/emacs-muse/manual/muse.txt`) | New family |
| `module_management_system` | `!` and target-line `#` comments | OpenVMS MMS guide | New family |
| `pod`, `pod_6` | Pod/Rakudoc comment directives and comment blocks | Perl and Raku docs | New families |
| `record_jar` | `%%` separator/comment lines | Open-RJ record-jar docs (`https://openrj.sourceforge.net/`) | New family |
| `redirect_rules` | Leading `#` comments | Netlify redirects docs (`https://docs.netlify.com/manage/routing/redirects/overview/`) | New family |
| `regular_expression` | `(?# ... )` in-pattern comments | PCRE pattern docs (`https://www.pcre.org/original/doc/html/pcrepattern.html`) | New family |
| `runoff` | `!` comment flag, `.!` and `.;` comment-control lines | Digital Standard Runoff reference manual | New family |
| `star` | Whitespace-boundary `#` comments | STAR/CIF spec | New family |
| `stringtemplate` | `<! ... !>` and `$! ... !$` comments | StringTemplate docs | New family |
| `ti_program` | Copyright-sign line comments | TI knowledge base (`https://education.ti.com/en/customer-support/knowledge-base/other-graphing/product-usage/11775`) | New family |
| `webvtt` | `NOTE` comment blocks between cue boundaries | W3C WebVTT spec (`https://www.w3.org/TR/webvtt1/`) | New family |
| `win32_message_file` | Leading semicolon comment lines | Microsoft Message Text Files docs | New family |
| `world_of_warcraft_addon_data` | Single-`#` TOC comments, excluding `##` metadata tags | WoW TOC format references | New family |
| `x_font_directory_index` | Leading `!` comment lines in `fonts.alias` | Xorg `mkfontdir` manual (`https://xorg.freedesktop.org/archive/X11R7.5/doc/man/man1/mkfontdir.1.html`) | New family |

## 2026-07-24 Missing-Language Follow-Up

Each addition below was checked against documentation and a local checkout of
the referenced implementation. Formats without a defensible aggregate syntax
remain unresolved.

| Registry key | Syntax implemented | Evidence | Status |
| --- | --- | --- | --- |
| `checksums` | Column-zero `#` lines in GNU checksum check files | GNU Coreutils `src/cksum.c` | New family |
| `ecere_projects` | ECON `//` and non-nested `/* ... */`, excluding strings | Ecere SDK `JSON.ec` and `Project.ec` | New family with string-aware masking |
| `figlet_font` | Header-declared `Comment_Lines` region | FIGfont 2 specification and FIGlet `figlet.c` | New contextual extractor |
| `microsoft_visual_studio_solution` | Full-line `#` after optional indentation | MSBuild `SolutionFile.cs` | New family |
| `nl` | End-of-record `#` in text headers and records | AMPL NL specification and AMPL MP `nl-reader` | New family with counted-string and binary-body masking |
| `omgrofl` | Case-insensitive leading `w00t` token | Omgrofl interpreter `ScriptParser.java` | New family |
| `pogoscript` | `//` and non-nested `/* ... */`, including block-to-EOF | PogoScript lexer grammar and compiler tests | New family with multiline string/interpolation masking |

`Public_Key` remains unresolved because the Stack label aggregates OpenSSH
key lists, RFC4716 keys, and OpenPGP armor. A leading-`#` rule would only be
correct for the OpenSSH subset.

## 2026-07-24 Missing-Language Validation

The seven additions and their shared query/sanitizer changes were validated
with deterministic property fuzzing and local reference implementations:

- `make comment-fuzz`: `67,100` cases across all `671` registry keys, with
  zero match-bound, reconstruction, ordering, API-consistency, or sanitizer
  totality failures. This campaign is not a language-semantics oracle.
- Seeded non-English payload mutation: `985` registry examples covering CJK,
  Cyrillic, Arabic, emoji, and combining marks, with zero extraction or
  sanitization failures.
- Language-aware differential fuzzing: `18,146` cases across FIGlet, NL,
  PogoScript, ECON, Omgrofl, Visual Studio Solution, and GNU checksum files,
  with zero residual failures. PogoScript cases were compared with the locally
  checked-out reference lexer.
- `make test`: `11,441 passed, 2 skipped, 29 deselected`, with `93.25%`
  coverage.
- Targeted Ruff checks and `git diff --check` passed.

## 2026-06-20 Validation

Affected-language Codex LLM judge rerun:

- Command family: `make comment-judge-test` with
  `COMMENT_JUDGE_BACKEND=codex`, `COMMENT_JUDGE_CODEX_MODEL=gpt-5.5`,
  `COMMENT_JUDGE_CODEX_PROFILE=xhigh`, and manifest
  `tmp/stack_v2_comment_judge_affected_after_fixes/manifest.jsonl`.
- Result: `140 passed, 1 skipped in 1026.49s`.
- Languages with all affected judge cases passing: `e`, `jsx`,
  `mirc_script`, `xojo`, `yacc`.

Additional local verification:

- Broad comment suite:
  `uv run pytest --no-cov tests/test_comment_queries.py tests/test_comment_registry.py tests/test_comment_sanitizer.py tests/test_stack_v2_comment_regressions.py tests/test_stack_v2_comment_judge.py tests/test_codex_comment_judge.py`
  passed with `5179 passed, 2 skipped`.
- Brainfuck ignored-text coverage smoke passed with
  `COMMENT_JUDGE_LANGUAGES=brainfuck COMMENT_JUDGE_PER_KIND=1 make comment-judge-coverage`.

## Remaining Stack v2 Labels

These labels are intentionally not added in this pass. Most are data files,
logs, prose containers, generated artifacts, serialized binary/text formats, or
formats whose visible marker lines are metadata/directives rather than lexical
comments. Obscure programming labels are left unresolved where no reliable
comment syntax evidence was found.

`default`, `Altium_Designer`, `Befunge`, `C-ObjDump`, `CSV`,
`Cirru`, `Creole`, `Darcs_Patch`, `Diff`,
`Formatted`, `GEDCOM`, `Gemfile.lock`, `Gemini`, `Go_Checksums`, `IRC_log`,
`JAR_Manifest`, `JSON`, `JSONLD`, `Jupyter_Notebook`, `Linux_Kernel_Module`,
`Max`, `Microsoft_Developer_Studio_Project`,
`ObjDump`, `Pickle`,
`Public_Key`, `Pure_Data`, `Python_traceback`,
`Raw_token_data`, `Rich_Text_Format`, `STL`, `STON`,
`Spline_Font_Database`, `SubRip_Text`, `TSV`, `Text`, `Unity3D_Asset`,
`Vim_Help_File`.
