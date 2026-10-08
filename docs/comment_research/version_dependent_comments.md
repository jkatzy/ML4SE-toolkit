# Version-dependent comment syntax

This record lists the registry languages whose comment syntax changed between
language versions, and what the registry does about each one. It backs the
`language_versions` tables in `src/ml4setk/Parsing/Comments/registry.py`
and the user-facing table in [`docs/comment_extractor.md`](../comment_extractor.md#language-versions).

## Method

Every registry family was checked for comment rules that differ by version.
Each claim was verified against a pinned primary source (a tagged lexer,
grammar, specification, or changelog), and each confirmed claim came with a
differential source whose exact comment slices differ between versions. The
run confirmed 108 keys, left 9 uncertain, and refuted 2.

A language gets a version table only when valid code written for a
non-default version is extracted differently by the default rules. When a
newer version only added comment forms that older code never contains, the
default rules are a superset and need no table. Such a language is either
already handled by the base registry entry or tracked as an open regression.

The default version is the one the base registry entry implements, normally
the current release. Non-default versions overlay only the fields they
change: patterns, nested delimiters, exclusions, contextual extractor,
literal-rule profile, or sanitizer wrappers.

## Implemented version tables

| Languages | Versions (default in bold) | Evidence |
| --- | --- | --- |
| `c`, `objective-c` | c89, c99, **c23** | ISO/IEC 9899:1990 6.1.9 and 9899:1999 6.4.9; <https://github.com/gcc-mirror/gcc/blob/releases/gcc-14.2.0/libcpp/init.cc> |
| `c++`, `objective_cpp`, `objective_c_plus_plus`, `cuda` | cpp98, cpp11, cpp14, **cpp17**, cpp23 | <https://github.com/cplusplus/draft/blob/n4140/source/compatibility.tex> |
| `glsl` | **glsl110**, glsl420 | <https://github.com/KhronosGroup/OpenGL-Registry/blob/6af574a14089ccfee87efe230ebcdd8742859813/specs/gl/GLSLangSpec.4.20.pdf> |
| `hack` | hhvm4.131, **hhvm4.133** | <https://github.com/facebook/hhvm/blob/HHVM-4.131.0/hphp/hack/src/parser/core/lexer.rs> |
| `stan` | 2.32, **2.33** | <https://github.com/stan-dev/stanc3/blob/v2.32.2/src/frontend/lexer.mll> |
| `jq` | **1.7**, 1.8 | <https://github.com/jqlang/jq/blob/jq-1.8.0/src/lexer.l#L24-L46> |
| `ssh_config` | 8.4, 8.5, **8.7** | <https://github.com/openssh/openssh-portable/blob/V_8_4_P1/readconf.c#L1930-L1935> |
| `fluent` | 0.4, **1.0** | <https://github.com/projectfluent/fluent/blob/v0.4.0/spec/fluent.ebnf#L6> |
| `org` | 7.8, **8.0** | <https://github.com/bzg/org-mode/blob/release_7.8.11/doc/org.texi#L8985-L8995> |
| `mcfunction` | 1.20.1, **1.20.2** | <https://github.com/SpyglassMC/Spyglass/blob/c1c7894a864c1397a1ec281227e25e71a20a8ea1/packages/mcfunction/src/parser/entry.ts#L57-L65>; decompiled 1.20.1 and 1.21.1 `CommandFunction.fromLines` (third-party mirrors) |
| `picolisp` | 2.3.6, 2.3.7, **18.6** | <https://github.com/picolisp/picolisp/blob/master/CHANGES> |
| `ocaml` | 4.01, 4.02, **4.11** | <https://github.com/ocaml/ocaml/blob/4.01.0/parsing/lexer.mll> |
| `julia` | 0.2, **0.3** | <https://github.com/JuliaLang/julia/blob/v0.2.0/src/julia-parser.scm#L323> |
| `markdown` | commonmark-0.30, **commonmark-0.31** | <https://github.com/commonmark/commonmark-spec/blob/0.30/spec.txt#L8983> |
| `lua` | 4.0, 5.0, **5.1** | <https://github.com/lua/lua/blob/v4.0/llex.c> |
| `vim_script`, `viml` | **legacy**, vim9 | <https://github.com/vim/vim/blob/v9.0.0000/runtime/doc/vim9.txt#L120-L146> |
| `editorconfig` | pre-0.15, **0.15** | <https://github.com/editorconfig/editorconfig-core-c/blob/v0.12.5/src/lib/ini.c#L64-L75> |
| `html_php`, `html_plus_php` | php7.4, **php8.0** | <https://github.com/php/php-src/blob/php-7.4.0/Zend/zend_language_scanner.l#L2147> |
| `cmake` | 2.8, **3.0** | <https://cmake.org/cmake/help/v3.0/release/3.0.0.html> |
| `php` | php7.2, php7.3, **php8.0** | <https://github.com/php/php-src/blob/php-7.3.0/UPGRADING> |
| `supercollider` | 3.8, **3.9** | <https://github.com/supercollider/supercollider/blob/Version-3.8.0/lang/LangSource/PyrLexer.cpp#L840-L852> |
| `macaulay2` | 1.10, 1.11, **1.13** | <https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/packages/Macaulay2Doc/changes.m2> |
| `caddyfile` | 2.0, **2.1** | <https://github.com/caddyserver/caddy/blob/v2.0.0/caddyconfig/caddyfile/lexer.go#L141-L146> |
| `cairo_zero` | 0.9, **0.10** | <https://github.com/starkware-libs/cairo-lang/blob/v0.9.1/src/starkware/cairo/lang/compiler/cairo.ebnf#L143> |
| `dotenv` | 13, 14.0, 14.3.2, 15, **16** | <https://github.com/motdotla/dotenv/blob/v13.0.1/lib/main.js> |
| `imba` | **imba1**, imba2 | <https://github.com/imba/imba/blob/9eaa35332461a3dde4342e67cd1f1e40fb16400e/packages/imba/src/compiler/lexer.mjs#L215-L217> |
| `mdx` | mdx1, **mdx2** | <https://github.com/mdx-js/mdx/blob/v1.6.22/packages/mdx/test/index.test.js#L141> |
| `mermaid` | 10.0, **10.1** | <https://github.com/mermaid-js/mermaid/blob/v10.0.2/packages/mermaid/src/diagrams/flowchart/parser/flow.jison#L30-L31> |
| `nushell` | 0.76, 0.77, **0.94** | <https://github.com/nushell/nushell/blob/0.76.0/crates/nu-parser/src/lex.rs#L62> |
| `templ` | 0.2.364, **0.2.408** | <https://github.com/a-h/templ/blob/v0.2.364/parser/v2/templateparser.go#L63> |

Base fixes made with these tables:

- `html_php` and `html_plus_php` default to PHP 8, where `#[` opens an attribute.
- `fluent`, `org`, `mcfunction`, and `picolisp` left `hash_line_style` for their own
  families: their comments start only at line start, nest, or continue, which the
  shared family's inline example cannot express.
- `ssh_config` follows OpenSSH 8.7 and later instead of the 8.5/8.6 first-`#` cut.
- `ocaml` lexes quoted strings and quoted extensions in and outside comments, as
  OCaml 4.11 and later do.
- `nushell` keeps the rest of a word literal after a mid-word `#`, as Nushell 0.77
  and later do.

## Superset changes tracked as open regressions

The newer version added a comment form the registry does not implement yet.
Each case is a strict `xfail` in `tests/test_comment_spec_breaker_regressions.py`.

| Language | Open case |
| --- | --- |
| `factor` | `factor-bang-inside-word` |
| `fortran` | `fortran-fixed-form-column-one-comments` |
| `handlebars` | `handlebars-3-whitespace-control-comment` |
| `javascript` | `javascript-es2023-hashbang-comment` |
| `lfe` | `lfe-block-comment` |
| `makefile` | `makefile-43-hash-inside-function-call` |
| `mini_yaml` | `mini-yaml-escaped-hash` |
| `mirc_script` | `mirc-61-block-comment` |
| `openedge_abl` | `openedge-116-line-comment` |
| `python` | `python-312-fstring-field-comment` |
| `rpm_spec` | `rpm-415-dnl-comment` |
| `scheme` | `scheme-nested-block-comment` |
| `twig` | `twig-315-inline-expression-comment` |
| `typescript` | `typescript-shebang-trivia` |

## Superset changes already handled

The base registry entry already accepts the newer forms, and older code never
contains them, so no table is needed:

`applescript`, `asn1`, `autohotkey`, `c#`, `coffeescript`, `csound`, `csound_document`, `csound_score`, `cue`, `cython`, `dhall`, `ejs`, `euphoria`, `forth`, `freebasic`, `groff`, `hiveql`, `html_eex`, `lark`, `liquid`, `ncl`, `noir`, `openqasm`, `pascal`, `perl`, `plpgsql`, `powershell`, `ron`, `scenic`, `scilab`, `shell`, `snakemake`, `sql`, `stata`, `svelte`, `sway`, `texinfo`, `textile`, `toml`, `vhdl`.

## Excluded

These differences are real but have no realistic corpus, or would need a
table that misrepresents the language.

| Language | Reason |
| --- | --- |
| `arduino` | gnu++98 and gnu++11 differ only through raw strings inside macro arguments, which no realistic sketch exercises. |
| `bitbake` | Only BitBake 1.12-1.16 layers with a # line ending in a backslash differ; modern BitBake rejects such lines. |
| `dylan` | Prefix Dylan (1992) is a different surface syntax with no realistic corpus. |
| `erlang` | OTP 26 and 27 differ only for adjacent empty strings written as """; no realistic corpus. |
| `graphql` | The October 2016 edition differs only for comma-free """ sequences inside lists. |
| `hip` | HIP keeps its reviewed HIP-Clang scanner; the C++ edition split is not modelled for it. |
| `html` | Browsers never implemented SGML comment declarations, so HTML4-era pages are tokenized by HTML5 rules in practice. |
| `kdl` | KDL v1 and v2 differ only on empty // comments and slashdash placement; the registry keeps the common forms. |
| `matlab` | MATLAB R13 (2002) differs only for %{ or %} alone on a line. |
| `nim` | Nim 0.12 (2015) differs only when a line comment starts with #[; no realistic corpus. |
| `reason` | Reason 3.3 differs only for a user-defined // operator. |
| `shen` | Shen kernels before 10 and the S-series tab rule have no realistic corpus. |
| `x_pixmap` | XPM2 comment syntax depends on a per-file type keyword (natural, C, Lisp); XPM2 files are rare in code corpora. |

## Deferred

These need parsing beyond the registry's delimiter and contextual-helper
model for every version, so they are deferred rather than approximated.

| Language | Reason |
| --- | --- |
| `cobol` | COBOL-85 comment-entries need fixed-format paragraph parsing. |
| `f#` | ML-compatibility (*IF-FSHARP ... *) markers need conditional-region parsing. |
| `isabelle` | Formal comments (`--`, `\<comment>`) are not modelled for any Isabelle version. |
| `isabelle_root` | ROOT formal comments are not modelled for any Isabelle version. |
| `praat` | Form, procedure, and block-keyword comment rules need a Praat script parser. |
| `sass` | Indentation-scoped loud and silent comments across five releases need a Sass parser. |
| `terraform_template` | HIL and HCL2 template comments need template-expression parsing. |

## Uncertain

No primary source could be fetched to confirm or refute these claims.
Revisit them when a source becomes available.

| Language | Open question |
| --- | --- |
| `logos` | Logos (Theos) is a % directive layer over Objective-C (.x/.xi) or Objective-C++ (.xm/.xmi). Its comments would therefore inherit the c table or the c++ table depending on the file type; no Logos release changed comments. One key cannot carry both tables unless it is split by extension. The registry key currently lexes like gnu++98 (no raw strings, no digit separators, no trigraphs). |
| `lolcode` | The 1.2 and 1.3 specs (justinmeza/lolcode-spec) give identical BTW and OBTW...TLDR rules marked '(from 1.1)'. That repository has no 1.0 or 1.1 spec (the v1.0 and v1.1 paths return 404), so it is not verified whether 1.0 lacked OBTW...TLDR. |
| `maxscript` | The probe returns ['/* blk */', '-- line']. Block comments are believed to have been added in a particular 3ds Max release, which would be a version of the same language. The only source is Autodesk's MAXScript help, which is unreachable (help.autodesk.com is blocked), and there is no public MAXScript lexer. The claim can be neither confirmed nor refuted. |
| `metal` | The Metal Shading Language is specified on top of a C++ edition that changed across MSL versions: C++14 for MSL 1-3 and C++17 for MSL 4, per Apple's specification, which could not be fetched. That change would toggle trigraphs, but Apple's compiler behavior for trigraphs and raw strings could not be checked. The registry key is a generic C-style alias (no raw strings, no digit separators), which already deviates from a C++14 base. |
| `mupad` | MuPAD is closed source and its manuals could not be fetched. It is not confirmed whether older releases accepted #...# comments in addition to // and /* */. |
| `objectscript` | InterSystems ObjectScript gained comment forms over Cache/IRIS releases (;, ;;, //, /* */, #;, ##;), but no fetchable primary source dates each form. |
| `rpgle` | ILE RPG comment forms did change by release: fixed-form '*' in position 7 and positions 81-100, // comments in /FREE blocks from V5R1, and fully free `**FREE` source in the 7.2/7.3 TRs. IBM's ILE RPG reference could not be fetched, so the exact boundaries are not verified. Separately from versioning, the registry's c_style rpgle extracts /* */, which RPG never had; it returned C block comments for C input. |
| `sqlpl` | The probe returns ['/* blk */', '-- line']; sqlpl is an alias of sql_style. A Db2 release adding bracketed `/* */` comments to SQL PL would qualify as a version of the same language, but the release boundary (reportedly around Db2 9.7 LUW or 10 for z/OS) is documented only in IBM's documentation. ibm.com/docs is unreachable from this environment and there is no public Db2 lexer. Neither the change nor its release could be verified, and nothing contradicts it either. |
| `xbase` | The key is a family label: Linguist xBase has the aliases advpl, clipper and foxpro. The registry implements the union of `*`, NOTE, `&&`, `//` and `/* */`; the probe returns all five. Differences between dBase, Clipper and FoxPro are vendor dialects. Because `clipper` is an alias of the key, though, a release boundary inside one product would count as versioning. Plausible examples are Clipper Summer '87 versus 5.0 (`//`, `/* */`) and dBase II versus III (`&&`). All of these are proprietary, have no reachable primary source (vendor manuals blocked; no public lexer for the old releases), and could not be confirmed or refuted. |

## Refuted

- `awk`: V7 awk already accepted trailing `#` comments (`awk.lx.l` line 104), so awk is invariant.
- `cairo`: the `#` to `//` change belongs to Cairo Zero (`cairo_zero`, cairo-lang 0.10); Cairo 1.x and 2.x have used only `//`.

## Adding a version table

1. Pin the evidence for each side of the change: a tagged lexer, grammar, or
   specification, not a moving branch.
2. Write a differential source and the exact comment slices under each version.
3. Add the `CommentLanguageVersions` table to the family entry. The default is
   the version the entry implements; every other version needs an overlay and a
   seeded example whose extraction differs from the default.
4. Add the differential source to the matching
   `tests/test_comment_language_versions_*.py` file and a row to the table in
   `docs/comment_extractor.md`; `test_extractor_docs_list_every_version_table`
   checks that row.
5. Run `make comment-fuzz` and `make comment-cleaner-fuzz`; both fuzz every
   language version.
