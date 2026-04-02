# Online Comment Research Prompt: `chunk_3_g_i`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments.

Target output file:
- `docs/comment_research/chunk_3_g_i_report.md`

## Priority Summary

- Assigned languages: `20`
- Needs research or confirmation: `20`
- Ready to implement but should be strengthened with source evidence: `0`
- Resolved non-actionable: `0`

## Required Workflow

1. Search official docs for comment syntax.
2. Cross-check with an implementation source when available.
3. If syntax is still unclear, search the web with the language name and `comment` to find Stack Overflow answers, blog posts, tutorials, or issue threads.
4. If syntax is still unclear after that, download real source files and inspect them directly.
5. For every language, explicitly classify line comments, block comments, and block-comment delimiter behavior.
6. Record whether block comments terminate at the first closer, support true nesting, or use depth-qualified delimiters.
7. Keep real surrounding-code examples for each supported comment form.
8. Do not guess. Mark unresolved when the evidence is not strong enough.

## Language Queue

| Priority | Language | Registry key | Current status | Confidence | Current line | Current block | Current termination | Current nested | Existing docs source | Existing impl source | Current recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high | GAML | gaml | needs_research_or_confirmation | medium | // | unresolved | line comments end at newline; block comments unresolved | unsupported | https://gama-platform.org/wiki/GamlLanguage | unresolved | Confirm whether GAML has a distinct block-comment form in the grammar or corpus before adding registry support. |
| high | GCC Machine Description | gcc_machine_description | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Leave unsupported until an official GCC machine-description syntax source is located. |
| high | GEDCOM | gedcom | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Keep unsupported unless a dialect-specific GEDCOM source documents a real comment form. |
| high | Gemfile.lock | gemfile_lock | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | Ruby/Bundler lockfile format; no comment syntax located | unresolved | Keep unsupported and exclude this file type from comment parsing tests. |
| high | Genero | genero | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the official Genero language manual and grammar before adding support. |
| high | Genero Forms | genero_forms | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Treat this as a separate research target from Genero itself. |
| high | Git Revision List | git_revision_list | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Keep unsupported unless a specific revision-list dialect documents comments. |
| high | Go Checksums | go_checksums | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Keep unsupported and exclude from parser coverage. |
| high | Golo | golo | needs_research_or_confirmation | high | unsupported | ---- ... ---- | first closing `----` wins | unsupported | https://gololang.org/GRP-Documentation-Misc.html | unresolved | Add block-comment fixtures using the `----` delimiter and keep line-comment tests absent unless a second source confirms them. |
| high | Grammatical Framework | grammatical_framework | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the official GF syntax before adding registry entries. |
| high | Graph Modeling Language | graph_modeling_language | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | https://en.wikipedia.org/wiki/Graph_Modelling_Language | https://igraph.org/c/html/develop/igraph-Foreign.html | Keep unsupported; the available references describe `comment` as a data attribute, not a comment delimiter. |
| high | Groovy Server Pages | groovy_server_pages | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research GSP template-comment syntax before adding any parser rule. |
| high | GSC | gsc | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Leave unsupported until a verified GSC syntax source is found. |
| high | Harbour | harbour | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Leave unresolved until a source-backed Harbour syntax reference confirms the comment forms. |
| high | HolyC | holyc | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the official HolyC syntax before adding support. |
| high | HTTP | http | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Keep unsupported unless a formal comment syntax is located in a specific HTTP configuration grammar. |
| high | HyPhy | hyphy | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the official HyPhy syntax before adding registry support. |
| high | IGOR Pro | igor_pro | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research official IGOR Pro syntax before adding support. |
| high | Inform 7 | inform_7 | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Verify bracket-comment syntax and nesting behavior in the official Inform 7 docs before adding support. |
| high | IRC log | irc_log | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Keep unsupported. |

## Search Guidance

For each language, try at least these query patterns before falling back:
- `"<Language> comments syntax"`
- `"<Language> language reference comments"`
- `"<Language> lexical grammar comments"`
- `"<Language> line comment block comment"`
- `"<Language> nested comments"`
- `"<Language> block comment delimiter"`

If the docs are unclear, search for:
- lexer or tokenizer definitions
- parser or grammar rules
- official examples or language test corpora

If official sources are still unclear, run a search-engine pass such as:
- `"<Language> comment"`
- `"<Language> comments"`
- `"<Language> block comment"`
- `"<Language> nested comment"`
- `"site:stackoverflow.com <Language> comment"`
- `"site:stackoverflow.com <Language> block comment"`
- `"site:stackoverflow.com <Language> nested comment"`
- `"<Language> comment blog"`
- `"<Language> comment tutorial"`

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
