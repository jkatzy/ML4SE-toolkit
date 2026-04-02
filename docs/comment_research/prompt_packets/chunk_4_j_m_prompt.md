# Online Comment Research Prompt: `chunk_4_j_m`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name plus `programming language` and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments.

Target output file:
- `docs/comment_research/chunk_4_j_m_report.md`

## Priority Summary

- Assigned languages: `70`
- Needs research or confirmation: `60`
- Ready to implement but should be strengthened with source evidence: `5`
- Resolved non-actionable: `5`

## Required Workflow

1. Search official docs for comment syntax.
2. Cross-check with an implementation source when available.
3. If syntax is still unclear, search the web with the language name plus `programming language` and `comment` to find Stack Overflow answers, blog posts, tutorials, or issue threads.
4. If syntax is still unclear after that, download real source files and inspect them directly.
5. For every language, explicitly classify line comments, block comments, and block-comment delimiter behavior.
6. Record whether block comments terminate at the first closer, support true nesting, or use depth-qualified delimiters.
7. Keep real surrounding-code examples for each supported comment form.
8. Do not guess. Mark unresolved when the evidence is not strong enough.

## Language Queue

| Priority | Language | Registry key | Current status | Confidence | Current line | Current block | Current termination | Current nested | Existing docs source | Existing impl source | Current recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high | Jasmin | jasmin | needs_research_or_confirmation | candidate | ; | unsupported | end of line | unsupported | unresolved | jasmin assembler grammar | confirm |
| high | JavaScript+ERB | javascript_erb | needs_research_or_confirmation | candidate | //, <%# ... %> | /* ... */ | end of line for JS line comments; first closing delimiter wins for block comments; ERB comments terminate at %> | unsupported | https://docs.ruby-lang.org/en/3.1/ERB.html + ECMAScript | erb / JS parser | confirm |
| high | Jest Snapshot | jest_snapshot | needs_research_or_confirmation | candidate | // | unsupported | end of line | unsupported | unresolved | jest snapshot format | confirm |
| high | JetBrains MPS | jetbrains_mps | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research |
| high | Jison | jison | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | unresolved | jison grammar | confirm |
| high | Jolie | jolie | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | Jolie docs | jolie parser | confirm |
| high | Kaitai Struct | kaitai_struct | needs_research_or_confirmation | candidate | # | unsupported | end of line | unsupported | Kaitai Struct docs | YAML parser / Kaitai schema parser | add |
| high | KakouneScript | kakounescript | needs_research_or_confirmation | unresolved | # | unsupported | end of line | unsupported | unresolved | unresolved | research |
| high | KiCad Legacy Layout | kicad_legacy_layout | needs_research_or_confirmation | unresolved | ; | unsupported | end of line | unsupported | KiCad docs | KiCad parser | research |
| high | Kit | kit | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research |
| high | KRL | krl | needs_research_or_confirmation | candidate | ; | unsupported | end of line | unsupported | KUKA KRL docs | KRL parser | confirm |
| high | Kusto | kusto | needs_research_or_confirmation | candidate | // | unsupported | end of line | unsupported | https://learn.microsoft.com/en-us/kusto/query/comment?view=microsoft-fabric | Kusto parser | confirm |
| high | kvlang | kvlang | needs_research_or_confirmation | candidate | # | unsupported | end of line | unsupported | Kivy language docs | kv parser | add |
| high | LabVIEW | labview | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research |
| high | Lark | lark | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | Lark docs | lark parser | confirm |
| high | Lasso | lasso | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | unresolved | unresolved | confirm |
| high | Lex | lex | needs_research_or_confirmation | candidate | unsupported | /* ... */ | first closing delimiter wins | unsupported | Flex / Lex docs | lex/flex grammar | confirm |
| high | LFE | lfe | needs_research_or_confirmation | candidate | ; | unsupported | end of line | unsupported | LFE docs | LFE parser | add |
| high | Linker Script | linker_script | needs_research_or_confirmation | candidate | unsupported | /* ... */ | first closing delimiter wins | unsupported | https://sourceware.org/binutils/docs/ld/Script-Format.html | ld script parser | confirm |
| high | Linux Kernel Module | linux_kernel_module | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | Linux kernel coding style | C parser | confirm |
| high | Literate Agda | literate_agda | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | Agda docs | Agda parser / literate mode | research |
| high | Literate CoffeeScript | literate_coffeescript | needs_research_or_confirmation | candidate | # | ### ... ### | end of line for line comments; first closing delimiter wins for block comments | unsupported | CoffeeScript docs | CoffeeScript parser | confirm |
| high | Literate Haskell | literate_haskell | needs_research_or_confirmation | candidate | -- | {- ... -} | end of line for line comments; true nesting supported for block comments | true nesting supported | https://www.haskell.org/onlinereport/haskell2010/haskellch2.html | Haskell parser / literate mode | confirm |
| high | LiveScript | livescript | needs_research_or_confirmation | candidate | //, # | /* ... */, ### ... ### | end of line for line comments; first closing delimiter wins for block comments | unsupported | unresolved | unresolved | confirm |
| high | Logos | logos | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | unresolved | unresolved | confirm |
| high | Logtalk | logtalk | needs_research_or_confirmation | candidate | % | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | Logtalk docs | Logtalk parser | add |
| high | LookML | lookml | needs_research_or_confirmation | candidate | # | unsupported | end of line | unsupported | https://docs.cloud.google.com/looker/docs/looker-ide | LookML parser | add |
| high | LoomScript | loomscript | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research |
| high | LSL | lsl | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | LSL docs | LSL parser | add |
| high | LTspice Symbol | ltspice_symbol | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research |
| high | M | m | needs_research_or_confirmation | candidate | ; | unsupported | end of line | unsupported | M/MUMPS docs | M parser | confirm |
| high | M4 | m4 | needs_research_or_confirmation | candidate | # | unsupported | end of line | unsupported | https://www.gnu.org/software/m4/manual/html_node/Comments.html | m4 parser | confirm |
| high | M4Sugar | m4sugar | needs_research_or_confirmation | candidate | # | unsupported | end of line | unsupported | https://www.gnu.org/software/m4/manual/html_node/Comments.html | m4sugar parser | confirm |
| high | Macaulay2 | macaulay2 | needs_research_or_confirmation | candidate | -- | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | Macaulay2 docs | Macaulay2 parser | confirm |
| high | Mask | mask | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research |
| high | Max | max | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | unresolved | unresolved | confirm |
| high | MAXScript | maxscript | needs_research_or_confirmation | candidate | -- | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | https://help.autodesk.com/cloudhelp/2022/ENU/MAXDEV-Overview/files/overview/MAXDEV_Overview_overview_maxscript_html.html | MAXScript parser | add |
| high | mcfunction | mcfunction | needs_research_or_confirmation | candidate | # | unsupported | end of line | unsupported | unresolved | mcfunction parser | add |
| high | Mercury | mercury | needs_research_or_confirmation | candidate | % | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | Mercury docs | Mercury parser | confirm |
| high | Metal | metal | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | Apple Metal docs | Metal parser | confirm |
| high | Microsoft Developer Studio Project | msdev_project | needs_research_or_confirmation | candidate | # | unsupported | end of line | unsupported | unresolved | unresolved | confirm |
| high | Microsoft Visual Studio Solution | visual_studio_solution | needs_research_or_confirmation | candidate | # | unsupported | end of line | unsupported | Visual Studio solution format | solution parser | confirm |
| high | Mirah | mirah | needs_research_or_confirmation | candidate | # | =begin ... =end | end of line for line comments; first closing delimiter wins for block comments | unsupported | Mirah docs | Mirah parser | confirm |
| high | mIRC Script | mirc_script | needs_research_or_confirmation | candidate | ; | unsupported | end of line | unsupported | mIRC docs | mIRC parser | add |
| high | MLIR | mlir | needs_research_or_confirmation | candidate | // | unsupported | end of line | unsupported | MLIR docs | MLIR parser | add |
| high | Modula-2 | modula_2 | needs_research_or_confirmation | candidate | unsupported | (* ... *) | true nesting supported | true nesting supported | Modula-2 spec | Modula-2 parser | add |
| high | Modula-3 | modula_3 | needs_research_or_confirmation | candidate | unsupported | (* ... *) | true nesting supported | true nesting supported | Modula-3 spec | Modula-3 parser | add |
| high | Module Management System | module_management_system | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research |
| high | Monkey | monkey | needs_research_or_confirmation | candidate | # | unsupported | end of line | unsupported | Monkey docs | Monkey parser | add |
| high | Monkey C | monkey_c | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | Monkey C docs | Monkey C parser | add |
| high | MoonScript | moonscript | needs_research_or_confirmation | candidate | -- | --[[ ... ]] | end of line for line comments; first closing delimiter wins for block comments | unsupported | https://moonscript.org/reference | MoonScript parser | add |
| high | Motoko | motoko | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; true nesting supported for block comments | true nesting supported | https://internetcomputer.org/docs/motoko/fundamentals/basic-syntax/comments | Motoko parser | add |
| high | Motorola 68K Assembly | motorola_68k_assembly | needs_research_or_confirmation | unresolved | ; | unsupported | end of line | unsupported | unresolved | unresolved | research |
| high | Move | move | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | https://move-language.github.io/move/coding-conventions.html | Move parser | add |
| high | MQL4 | mql4 | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | MQL4 docs | MQL4 parser | add |
| high | MQL5 | mql5 | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | MQL5 docs | MQL5 parser | add |
| high | MTML | mtml | needs_research_or_confirmation | unresolved | <!-- ... --> | <!-- ... --> | end of line for line comments; first closing delimiter wins for block comments | unsupported | unresolved | unresolved | research |
| high | MUF | muf | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research |
| high | mupad | mupad | needs_research_or_confirmation | candidate | // | /* ... */ | end of line for line comments; first closing delimiter wins for block comments | unsupported | unresolved | unresolved | confirm |
| high | Muse | muse | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research |
| medium | J | j | ready_to_implement | verified | `NB.` at the start of a line or after code | unsupported | end of line | unsupported | https://www.jsoftware.com/docs/help602/user/scriptdoc.htm | J scriptdoc utility | add |
| medium | KiCad Layout | kicad_layout | ready_to_implement | verified | # | unsupported | end of line | unsupported | https://dev-docs.kicad.org/en/file-formats/index.html | https://docs.kicad.org/doxygen/dsnlexer_8cpp_source.html | add |
| medium | KiCad Schematic | kicad_schematic | ready_to_implement | verified | # | unsupported | end of line | unsupported | https://dev-docs.kicad.org/en/file-formats/index.html | https://docs.kicad.org/doxygen/dsnlexer_8cpp_source.html | add |
| medium | Limbo | limbo | ready_to_implement | verified | # | unsupported | end of line | unsupported | https://inferno-os.org/inferno/papers/limbo.html | Limbo language reference | add |
| medium | Marko | marko | ready_to_implement | verified | `//` at top level; HTML comments are also accepted in template markup | `/** ... */` at top level; `<!-- ... -->` in template markup | end of line for `//`; first closing delimiter wins for block-style comments | unsupported | https://markojs.com/docs/reference/language | Marko language reference / parser | add |
| low | JAR Manifest | jar_manifest | resolved_non_actionable | verified | unsupported | unsupported | unsupported | unsupported | https://docs.oracle.com/en/java/javase/25/docs/specs/jar/jar.html | java.util.jar.Manifest / JAR parser | unsupported |
| low | JSON | json | resolved_non_actionable | verified | unsupported | unsupported | unsupported | unsupported | https://www.rfc-editor.org/rfc/rfc8259.html | json parser | unsupported |
| low | JSONLD | jsonld | resolved_non_actionable | verified | unsupported | unsupported | unsupported | unsupported | https://www.w3.org/TR/json-ld11/ | json parser | unsupported |
| low | Jupyter Notebook | jupyter_notebook | resolved_non_actionable | verified | unsupported | unsupported | unsupported | unsupported | https://nbformat.readthedocs.io/en/latest/format_description.html | nbformat parser | unsupported |
| low | Markdown | markdown | resolved_non_actionable | verified | unsupported | unsupported | unsupported | unsupported | https://spec.commonmark.org/0.31.2/ | markdown parser | unsupported |

## Search Guidance

For each language, try at least these query patterns before falling back:
- `"<Language> programming language comments syntax"`
- `"<Language> programming language reference comments"`
- `"<Language> programming language lexical grammar comments"`
- `"<Language> programming language line comment block comment"`
- `"<Language> programming language nested comments"`
- `"<Language> programming language block comment delimiter"`

If the docs are unclear, search for:
- lexer or tokenizer definitions
- parser or grammar rules
- official examples or language test corpora

If official sources are still unclear, run a search-engine pass such as:
- `"<Language> programming language comment"`
- `"<Language> programming language comments"`
- `"<Language> programming language block comment"`
- `"<Language> programming language nested comment"`
- `"site:stackoverflow.com <Language> programming language comment"`
- `"site:stackoverflow.com <Language> programming language block comment"`
- `"site:stackoverflow.com <Language> programming language nested comment"`
- `"<Language> programming language comment blog"`
- `"<Language> programming language comment tutorial"`

When you use Stack Overflow or blog posts:
- prefer answers with concrete code examples
- treat them as corroboration, not as the strongest source
- note contradictions with official docs explicitly

If you still cannot resolve the syntax, download multiple real files and inspect them.

## Output Constraints

- Preserve the per-language markdown section format from `report_template.md`.
- Every language entry must state line comments, block comments, termination behavior, and nested-comment support explicitly.
- Keep the core fields used by the backlog scripts: `Registry key`, `Line comments`, `Block comments`, `Nested comments`, `Confidence`, `Docs source`, `Implementation source`, `Recommended action`, and `Notes`.
- You may add `Evidence mode`, `Community source`, and `Corpus fallback source`; downstream scripts will ignore those extra fields safely.
- You may also add `Termination behavior`; downstream scripts will ignore that extra field safely.
- Prefer direct source URLs over generic site homepages.
