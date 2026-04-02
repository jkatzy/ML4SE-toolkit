# Online Comment Research Prompt: `chunk_3_g_i`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name plus `programming language` and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments.

Target output file:
- `docs/comment_research/chunk_3_g_i_report.md`

## Priority Summary

- Assigned languages: `20`
- Needs research or confirmation: `13`
- Ready to implement but should be strengthened with source evidence: `7`
- Resolved non-actionable: `0`

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
| high | GAML | gaml | needs_research_or_confirmation | medium | // | unresolved | line comments end at newline; block comments unresolved | unsupported | https://gama-platform.org/wiki/1.9.3/Statements; https://gama-platform.org/wiki/1.9.3/GamlReference | unresolved | Confirm whether GAML has a distinct block-comment form in the grammar or corpus before adding registry support. |
| high | GCC Machine Description | gcc_machine_description | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Leave unsupported until an official GCC machine-description syntax source is located. |
| high | GEDCOM | gedcom | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Keep unsupported unless a dialect-specific GEDCOM source documents a real comment form. |
| high | Gemfile.lock | gemfile_lock | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | Ruby/Bundler lockfile format; no comment syntax located | unresolved | Keep unsupported and exclude this file type from comment parsing tests. |
| high | Genero Forms | genero_forms | needs_research_or_confirmation | medium | -- | unsupported | line comments end at newline | unsupported | https://4js.com/online_documentation/fjs-genero-3.00.06-manual-tutorial-html/genero-tutorial-topics/c_fgl_TutChap10_010.html; https://4js.com/online_documentation/fjs-genero-4.01.38-manual-tutorial-html/genero-tutorial-topics/c_fgl_TutChap10_010.html | unresolved | Add `.per` fixtures that keep `--` comment lines in place and do not assume brace or hash comments unless a form-file grammar source confirms them. |
| high | Git Revision List | git_revision_list | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Keep unsupported unless a specific revision-list dialect documents comments. |
| high | Go Checksums | go_checksums | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Keep unsupported and exclude from parser coverage. |
| high | Golo | golo | needs_research_or_confirmation | high | unsupported | ---- ... ---- | first closing `----` wins | unsupported | https://gololang.org/GRP-Documentation-Misc.html | unresolved | Add block-comment fixtures using the `----` delimiter and keep line-comment tests absent unless a second source confirms them. |
| high | Graph Modeling Language | graph_modeling_language | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | https://en.wikipedia.org/wiki/Graph_Modelling_Language | https://igraph.org/c/html/develop/igraph-Foreign.html | Keep unsupported; the available references describe `comment` as a data attribute, not a comment delimiter. |
| high | Harbour | harbour | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Leave unresolved until a source-backed Harbour syntax reference confirms the comment forms. |
| high | HolyC | holyc | needs_research_or_confirmation | medium | // | unresolved | line comments end at newline; block comments unresolved | unresolved | unresolved | https://github.com/Ma11ock/holyc | Keep the `//` line-comment fixture and leave block comments unresolved until a source-backed HolyC reference confirms them. |
| high | HTTP | http | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Keep unsupported unless a formal comment syntax is located in a specific HTTP configuration grammar. |
| high | IRC log | irc_log | needs_research_or_confirmation | unsupported | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Keep unsupported. |
| medium | Genero | genero | ready_to_implement | high | --` and `# | { ... } | line comments end at newline; brace comments end at the first closing `}` | unsupported | https://4js.com/online_documentation/fjs-fgl-manual-html/fgl-topics/c_fgl_language_features_comment.html; https://4js.com/online_documentation/fjs-fgl-manual-html/fgl-topics/c_fgl_beautifier_usage.html | unresolved | Add fixtures for `--`, `#`, and brace comments, and keep brace nesting explicitly forbidden in tests. |
| medium | Grammatical Framework | grammatical_framework | ready_to_implement | high | -- | {- ... -} | line comments end at newline; block comments end at the first `-}` | supported | https://www.grammaticalframework.org/doc/gf-refman.html | unresolved | Add both comment forms to the registry and keep the nested-block behavior covered by regression tests. |
| medium | Groovy Server Pages | groovy_server_pages | ready_to_implement | high | unsupported | <%-- ... --%> | first closing `--%>` wins | unsupported | https://grails.apache.org/docs-legacy-gsp/6.2.3/guide/index.html; https://grails.apache.org/docs-legacy-gsp/7.0.0-M1/guide/GSPBasics.html | unresolved | Add JSP-style server-side comment fixtures and keep embedded Groovy scriptlets separate from GSP comments. |
| medium | GSC | gsc | ready_to_implement | high | // | /* ... */ | line comments end at newline; block comments end at the first `*/` | unsupported | https://docs.auroramod.dev/gsc-scripting-syntax | unresolved | Add both one-line and block-comment fixtures and keep the grammar C-like. |
| medium | HyPhy | hyphy | ready_to_implement | high | // | /* ... */ | line comments end at newline; block comments end at the first `*/` | unsupported | https://hyphy.org/resources/Getting_Started_With_HyPhy.pdf | https://github.com/veg/hyphy | Add HBL fixtures for both comment forms and keep nested block comments absent. |
| medium | IGOR Pro | igor_pro | ready_to_implement | high | // | unsupported | line comments end at newline | unsupported | https://docs.wavemetrics.com/igorpro/programming/procedure-windows; https://docs.wavemetrics.com/igorpro/programming/commands | unresolved | Add `//` fixtures for procedure windows and keep block-comment tests absent. |
| medium | Inform 7 | inform_7 | ready_to_implement | high | unsupported | [ ... ] | comments end at the first closing `]` | unsupported | https://ganelson.github.io/inform-website/book/WI_2_3.html; https://ganelson.github.io/inform-website/book/general_index.html | https://github.com/ganelson/inform | Add bracket-comment fixtures and keep text-substitution handling separate from comments. |

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
