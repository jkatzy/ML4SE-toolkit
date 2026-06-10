# Online Comment Research Prompt: `chunk_0_nonalpha_a`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name plus `programming language` and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments. Do not stop at a single source: reconcile multiple sources and explicitly look for version-specific or dialect-specific differences.

Target output file:
- `docs/comment_research/chunk_0_nonalpha_a_report.md`

## Priority Summary

- Assigned languages: `1`
- Needs research or confirmation: `0`
- Ready to implement but should be strengthened with source evidence: `0`
- Resolved non-actionable: `1`

## Required Workflow

1. Search official docs for comment syntax.
2. Check more than one source whenever possible.
3. If the language has versioned docs, historical manuals, standards, or dialects, compare current syntax with at least one older or alternate version source.
4. Cross-check with an implementation source when available.
5. If syntax is still unclear, search the web with the language name plus `programming language` and `comment` to find Stack Overflow answers, blog posts, tutorials, or issue threads.
6. If syntax is still unclear after that, download real source files and inspect them directly.
7. For every language, explicitly classify line comments, block comments, block-comment delimiter behavior, and version-specific variants.
8. Record whether block comments terminate at the first closer, support true nesting, or use depth-qualified delimiters.
9. When versions differ, record the exact version scope and recommend whether the registry should implement the union of all confirmed forms.
10. Keep real surrounding-code examples for each supported comment form.
11. Do not guess. Mark unresolved when the evidence is not strong enough.

## Language Queue

| Priority | Language | Registry key | Current status | Confidence | Current version scope | Current version syntax | Current line | Current block | Current termination | Current nested | Existing docs source | Existing impl source | Current recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| low | Altium Designer | altium_designer | resolved_non_actionable | cross-checked | current Altium Designer documentation for Output Job and scripting files, plus the current GitHub Linguist language mapping | no source-comment syntax applies to the Stack label; Linguist maps `.OutJob`, `.PcbDoc`, `.PrjPCB`, and `.SchDoc` data files, while Altium documents DelphiScript separately as `.pas` | unsupported | unsupported | unsupported | unsupported | https://www.altium.com/documentation/altium-designer/preparing-for-manufacture/output-jobs; https://www.altium.com/documentation/altium-designer/scripting/writing-scripts | https://github.com/github-linguist/linguist/blob/main/lib/linguist/languages.yml | leave unsupported |

## Search Guidance

For each language, try at least these query patterns before falling back:
- `"<Language> programming language comments syntax"`
- `"<Language> programming language reference comments"`
- `"<Language> programming language lexical grammar comments"`
- `"<Language> programming language line comment block comment"`
- `"<Language> programming language nested comments"`
- `"<Language> programming language block comment delimiter"`
- `"<Language> programming language version comment syntax"`
- `"<Language> programming language legacy comment syntax"`
- `"<Language> programming language old version comments"`

If the docs are unclear, search for:
- lexer or tokenizer definitions
- parser or grammar rules
- archived docs or versioned manuals
- release notes or standards editions
- official examples or language test corpora

If official sources are still unclear, run a search-engine pass such as:
- `"<Language> programming language comment"`
- `"<Language> programming language comments"`
- `"<Language> programming language block comment"`
- `"<Language> programming language nested comment"`
- `"<Language> programming language version comment syntax"`
- `"<Language> programming language legacy comment syntax"`
- `"site:stackoverflow.com <Language> programming language comment"`
- `"site:stackoverflow.com <Language> programming language block comment"`
- `"site:stackoverflow.com <Language> programming language nested comment"`
- `"<Language> programming language comment blog"`
- `"<Language> programming language comment tutorial"`

When you use Stack Overflow or blog posts:
- prefer answers with concrete code examples
- treat them as corroboration, not as the strongest source
- note contradictions with official docs explicitly
- note which version or dialect the answer is describing

If you still cannot resolve the syntax, download multiple real files and inspect them.

## Output Constraints

- Preserve the per-language markdown section format from `report_template.md`.
- Every language entry must state line comments, block comments, termination behavior, nested-comment support, version scope, and version-specific differences explicitly.
- Keep the core fields used by the backlog scripts: `Registry key`, `Version scope`, `Version-specific syntax`, `Line comments`, `Block comments`, `Nested comments`, `Confidence`, `Docs source`, `Implementation source`, `Recommended action`, and `Notes`.
- You may add `Evidence mode`, `Community source`, and `Corpus fallback source`; downstream scripts will ignore those extra fields safely.
- You may also add `Termination behavior`; downstream scripts will ignore that extra field safely.
- Prefer direct source URLs over generic site homepages.
