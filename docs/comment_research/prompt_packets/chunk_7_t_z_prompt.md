# Online Comment Research Prompt: `chunk_7_t_z`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name plus `programming language` and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments.

Target output file:
- `docs/comment_research/chunk_7_t_z_report.md`

## Priority Summary

- Assigned languages: `44`
- Needs research or confirmation: `40`
- Ready to implement but should be strengthened with source evidence: `2`
- Resolved non-actionable: `2`

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
| high | Talon | talon | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research Talon syntax before seeding a registry entry. |
| high | Tea | tea | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Verify Tea syntax before adding parser support. |
| high | Terra | terra | needs_research_or_confirmation | medium | -- | --[[ ... ]] | depth-qualified delimiters | yes | unresolved | unresolved | Verify Lua-style long-comment handling and add nested coverage if the grammar supports it. |
| high | Texinfo | texinfo | needs_research_or_confirmation | medium | @c` and `@comment | @ignore ... @end ignore | first closing delimiter wins | unsupported | https://www.gnu.org/software/texinfo/manual/texinfo/html_node/Comments.html | unresolved | Verify Texinfo comment and ignore-block behavior before seeding. |
| high | Textile | textile | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research Textile syntax before seeding a registry entry. |
| high | Turing | turing | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Verify Turing comment syntax before seeding. |
| high | TXL | txl | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Verify TXL syntax before adding a registry entry. |
| high | Type Language | type_language | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the specific Stack v2 dialect before seeding. |
| high | Unity3D Asset | unity3d_asset | needs_research_or_confirmation | medium | # | unsupported | unsupported | unsupported | unresolved | unresolved | Verify the YAML-like asset format and keep block comments unsupported unless the grammar says otherwise. |
| high | Unix Assembly | unix_assembly | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Verify the exact assembly dialect before seeding. |
| high | Uno | uno | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Seed C-like comment tests after confirming the Uno grammar. |
| high | UrWeb | urweb | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research Ur/Web syntax before seeding. |
| high | Valve Data Format | valve_data_format | needs_research_or_confirmation | medium | // | unresolved | unresolved | unresolved | unresolved | unresolved | Verify the exact VDF variant before seeding. |
| high | VCL | vcl | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the exact VCL dialect before seeding. |
| high | Vim Help File | vim_help_file | needs_research_or_confirmation | low | unresolved | unsupported | unsupported | unsupported | unresolved | unresolved | Verify help-file markup rules before seeding. |
| high | Vim Snippet | vim_snippet | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the snippet dialect used in Stack v2 before seeding. |
| high | Volt | volt | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research Volt syntax before seeding. |
| high | Web Ontology Language | web_ontology_language | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the specific serialization used in Stack v2 before seeding. |
| high | WebVTT | webvtt | needs_research_or_confirmation | medium | unsupported | NOTE ... blank line | first blank line wins | unsupported | https://www.w3.org/TR/webvtt1/ | unresolved | Treat NOTE blocks as WebVTT comments and add parser tests for blank-line termination. |
| high | Whiley | whiley | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify Whiley syntax before seeding. |
| high | Win32 Message File | win32_message_file | needs_research_or_confirmation | medium | ; | unsupported | unsupported | unsupported | unresolved | unresolved | Verify message-file syntax and add semicolon-comment tests if confirmed. |
| high | Witcher Script | witcher_script | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify Witcher Script syntax before seeding. |
| high | Wollok | wollok | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify Wollok syntax before seeding. |
| high | World of Warcraft Addon Data | world_of_warcraft_addon_data | needs_research_or_confirmation | medium | -- | --[[ ... ]] | depth-qualified delimiters | yes | unresolved | unresolved | Seed Lua-style comment coverage and verify long-comment handling. |
| high | Wren | wren | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify Wren comment syntax before seeding. |
| high | X BitMap | x_bit_map | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the exact XBM representation before seeding. |
| high | X PixMap | x_pix_map | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the exact XPM representation before seeding. |
| high | X10 | x10 | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify X10 syntax before seeding. |
| high | xBase | xbase | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research xBase syntax before seeding. |
| high | XC | xc | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify XC syntax before seeding. |
| high | Xojo | xojo | needs_research_or_confirmation | medium | '` and `Rem | unsupported | unsupported | unsupported | unresolved | unresolved | Verify Xojo comment forms before seeding. |
| high | XPages | xpages | needs_research_or_confirmation | medium | unsupported | <!-- ... --> | first closing delimiter wins | unsupported | unresolved | unresolved | Verify whether the Stack v2 corpus uses the XML layer or a scripting layer. |
| high | XS | xs | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the exact XS dialect before seeding. |
| high | Yacc | yacc | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify the exact parser-generator dialect used in Stack v2. |
| high | YANG | yang | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | https://www.rfc-editor.org/rfc/rfc7950.html | unresolved | Verify YANG comment syntax before seeding. |
| high | YASnippet | yasnippet | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the snippet format before seeding. |
| high | ZenScript | zenscript | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify ZenScript syntax before seeding. |
| high | Zephir | zephir | needs_research_or_confirmation | medium | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify Zephir syntax before seeding. |
| high | ZIL | zil | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research ZIL syntax before seeding. |
| high | Zimpl | zimpl | needs_research_or_confirmation | medium | # | unsupported | unsupported | unsupported | unresolved | unresolved | Seed hash-comment tests. |
| medium | TextMate Properties | textmate_properties | ready_to_implement | high | # | unsupported | unsupported | unsupported | https://macromates.com/textmate/manual/settings | unresolved | Seed hash-comment tests for .tm_properties files. |
| medium | wdl | wdl | ready_to_implement | high | # | unsupported | unsupported | unsupported | https://docs.openwdl.org/reference/stdlib/numeric.html | unresolved | Seed hash-comment tests in WDL fixtures. |
| low | Text | text | resolved_non_actionable | high | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Document as commentless. |
| low | TSV | tsv | resolved_non_actionable | high | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Document as commentless unless a dialect extension exists. |

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
