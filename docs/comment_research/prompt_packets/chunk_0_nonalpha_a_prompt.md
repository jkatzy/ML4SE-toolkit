# Online Comment Research Prompt: `chunk_0_nonalpha_a`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments.

Target output file:
- `docs/comment_research/chunk_0_nonalpha_a_report.md`

## Priority Summary

- Assigned languages: `6`
- Needs research or confirmation: `6`
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
| high | 2-Dimensional Array | two_dimensional_array | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | unresolved | needs manual research |
| high | Altium Designer | altium_designer | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unknown | https://www.altium.com/documentation/altium-designer/document-commenting | unresolved | needs manual research |
| high | API Blueprint | api_blueprint | needs_research_or_confirmation | medium | unsupported | <!-- --> | line comments unsupported; block comments terminate at first closing delimiter | no | https://apiblueprint.org/documentation/specification.html | https://github.com/apiaryio/drafter | candidate |
| high | Apollo Guidance Computer | apollo_guidance_computer | needs_research_or_confirmation | candidate | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | https://www.ibiblio.org/apollo/assembly_language_manual.html | https://www.ibiblio.org/apollo/yaYUL.html | candidate |
| high | Arc | arc | needs_research_or_confirmation | candidate | ; | unsupported | line comments terminate at end-of-line; block comments unsupported | no | https://www.paulgraham.com/arc.html | GitHub Linguist languages.yml | candidate |
| high | ASP.NET | aspnet | needs_research_or_confirmation | candidate | `//` in embedded C# / `'` in embedded VB | `@* *@` in Razor; `/* */` in embedded C#; `<!-- -->` in markup | line comments terminate at end-of-line; Razor comments terminate at the first closing `*@`; HTML comments terminate at the first closing `-->` | no | https://learn.microsoft.com/en-us/aspnet/web-pages/overview/getting-started/introducing-razor-syntax-c | GitHub Linguist languages.yml | candidate |

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
