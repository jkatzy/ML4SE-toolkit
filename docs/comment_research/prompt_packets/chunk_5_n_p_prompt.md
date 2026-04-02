# Online Comment Research Prompt: `chunk_5_n_p`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name plus `programming language` and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments.

Target output file:
- `docs/comment_research/chunk_5_n_p_report.md`

## Priority Summary

- Assigned languages: `54`
- Needs research or confirmation: `48`
- Ready to implement but should be strengthened with source evidence: `5`
- Resolved non-actionable: `1`

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
| high | nanorc | nanorc | needs_research_or_confirmation | medium | # | unsupported | newline | unsupported | unresolved | unresolved | add a line-comment fixture and verify the nano manual before registry changes. |
| high | Nasal | nasal | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research official Nasal docs before registry updates. |
| high | NASL | nasl | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research official NASL docs before registry updates. |
| high | NCL | ncl | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | research official NCL docs before registry updates. |
| high | Nearley | nearley | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Nearley grammar comment syntax from official docs or grammar sources. |
| high | Nemerle | nemerle | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Nemerle comment syntax before adding fixtures. |
| high | nesC | nesc | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | add C-style fixtures and verify against the nesC reference. |
| high | NetLinx | netlinx | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify NetLinx comment syntax from official docs. |
| high | NewLisp | newlisp | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify newLISP comment syntax from the reference manual. |
| high | Nit | nit | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Nit comment syntax before registry updates. |
| high | NL | nl | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | clarify what Stack v2 means by NL before further research. |
| high | NWScript | nwscript | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | add C-style fixtures and verify against the NWScript reference. |
| high | ObjDump | objdump | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | identify the exact Stack v2 syntax flavor for this entry. |
| high | Object Data Instance Notation | object_data_instance_notation | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify whether the format supports comments at all. |
| high | ooc | ooc | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | add C-family fixtures and verify against ooc docs. |
| high | Opa | opa | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify the Stack v2 Opa entry before assuming any syntax family. |
| high | OpenEdge ABL | openedge_abl | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify ABL comment syntax from the official reference. |
| high | OpenRC runscript | openrc_runscript | needs_research_or_confirmation | medium | # | unsupported | newline | unsupported | unresolved | unresolved | add line-comment fixtures and confirm against the runscript reference. |
| high | OpenStep Property List | openstep_property_list | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify whether the plist variant supports comments at all. |
| high | OpenType Feature File | opentype_feature_file | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify feature-file comment syntax from the OpenType feature syntax docs. |
| high | Org | org | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Org comment syntax separately from source comments. |
| high | Ox | ox | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Ox comment syntax from the official reference. |
| high | Oz | oz | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Oz comment syntax from the language reference. |
| high | P4 | p4 | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | add C-style fixtures if the P4 reference confirms this syntax. |
| high | Pan | pan | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Pan comment syntax from the language reference. |
| high | Papyrus | papyrus | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Papyrus comment syntax from the language reference. |
| high | Parrot Assembly | parrot_assembly | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Parrot Assembly comment syntax from the official reference. |
| high | Parrot Internal Representation | parrot_internal_representation | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify PIR comment syntax from the official reference. |
| high | Pascal | pascal | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify the specific Pascal dialect before adding fixtures. |
| high | Pawn | pawn | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | add C-style fixtures and confirm against the Pawn reference. |
| high | PEG.js | peg_js | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify PEG.js grammar comment syntax from the grammar docs. |
| high | Pep8 | pep8 | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify the Pep8 dialect comment syntax before registry work. |
| high | Pic | pic | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Pic comment syntax from the language reference. |
| high | Pickle | pickle | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Pickle syntax before adding fixtures. |
| high | PicoLisp | picolisp | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify PicoLisp comment syntax from the official docs. |
| high | PigLatin | piglatin | needs_research_or_confirmation | medium | -- | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | add SQL-like fixtures and confirm the PigLatin comment rules. |
| high | Pike | pike | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | add C-family fixtures and verify against Pike docs. |
| high | Pod | pod | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify whether this is Perl POD or a different source format. |
| high | Pod 6 | pod_6 | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Pod 6 / Raku docs before registry changes. |
| high | PogoScript | pogoscript | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify PogoScript syntax from official docs. |
| high | Pony | pony | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Pony comment syntax from the language reference. |
| high | Portugol | portugol | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify the Stack v2 Portugol dialect before adding fixtures. |
| high | POV-Ray SDL | pov_ray_sdl | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify POV-Ray SDL comment syntax from the language reference. |
| high | PowerBuilder | powerbuilder | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify PowerBuilder comment syntax from the official reference. |
| high | Prisma | prisma | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Prisma schema comment syntax before adding fixtures. |
| high | Promela | promela | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | add C-style fixtures and confirm against the SPIN reference. |
| high | Propeller Spin | propeller_spin | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify Spin comment syntax from the official reference. |
| high | Pure Data | pure_data | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | verify whether the format has true comments or only directives. |
| medium | NEON | neon | ready_to_implement | verified | # | unsupported | newline | unsupported | https://doc.nette.org/en/neon/format | https://github.com/nette/neon | add hash-comment fixtures and keep block comments unsupported. |
| medium | ObjectScript | objectscript | ready_to_implement | verified | `//`, `;`, `##;` (`#;` in column 1) | /* ... */ | `newline` for line comments; `first closing delimiter wins` for block comments | unsupported | https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=GCOS_syntax | https://docs.rs/crate/tree-sitter-objectscript/1.6.3 | add fixtures for `//`, `;`, `##;`, and `/* */`, but keep nested comments unsupported. |
| medium | OpenQASM | openqasm | ready_to_implement | verified | // | /* ... */ | `newline` for line comments; `first closing delimiter wins` for block comments | unsupported | https://openqasm.com/versions/3.0/language/comments.html | https://github.com/openqasm/openqasm | add line and block fixtures and keep nested comments unsupported. |
| medium | PlantUML | plantuml | ready_to_implement | verified | ' | /' ... '/ | `newline` for line comments; `first closing delimiter wins` for block comments | unsupported | https://plantuml.com/en/commons | https://github.com/plantuml/plantuml | add apostrophe-comment fixtures and keep nested comments unsupported. |
| medium | PureBasic | purebasic | ready_to_implement | verified | ; | unsupported | newline | unsupported | https://www.purebasic.com/documentation/reference/general_rules.html | unresolved | add semicolon-comment fixtures and keep block comments unsupported. |
| low | Public Key | public_key | resolved_non_actionable | high | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | keep this entry unsupported unless a formal spec changes. |

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
