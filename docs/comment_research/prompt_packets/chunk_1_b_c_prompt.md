# Online Comment Research Prompt: `chunk_1_b_c`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name plus `programming language` and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments. Do not stop at a single source: reconcile multiple sources and explicitly look for version-specific or dialect-specific differences.

Target output file:
- `docs/comment_research/chunk_1_b_c_report.md`

## Priority Summary

- Assigned languages: `40`
- Needs research or confirmation: `38`
- Ready to implement but should be strengthened with source evidence: `0`
- Resolved non-actionable: `2`

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
| high | Beef | beef | needs_research_or_confirmation | medium | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against the Beef language reference before seeding. |
| high | Berry | berry | needs_research_or_confirmation | medium | unresolved | unresolved | # | unsupported | unsupported | unsupported | unresolved | unresolved | Verify against Berry docs and add hash-comment tests. |
| high | Bicep | bicep | needs_research_or_confirmation | medium | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | [Bicep file syntax](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/file) | unresolved | Verify the exact doc page and add C-like comment tests. |
| high | Bikeshed | bikeshed | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | `<!-- ... -->` is the best candidate, but this needs verification. | first closing delimiter wins | `unsupported` if HTML comments are the only supported form. | unresolved | unresolved | Research Bikeshed's parser/docs before adding a registry entry. |
| high | BitBake | bitbake | needs_research_or_confirmation | medium | unresolved | unresolved | # | unsupported | unsupported | unsupported | unresolved | unresolved | Verify against Yocto/BitBake docs and add hash-comment tests. |
| high | BlitzBasic | blitzbasic | needs_research_or_confirmation | medium | unresolved | unresolved | ; | unsupported | unsupported | unsupported | unresolved | unresolved | Verify against the BlitzBasic reference and add semicolon-comment tests. |
| high | BlitzMax | blitzmax | needs_research_or_confirmation | medium | unresolved | unresolved | Rem` and `' | unsupported | unsupported | unsupported | [BlitzMax comments](https://blitzmax.org/docs/en/language/comments/) | unresolved | Verify dialect details and add tests for both line-comment forms. |
| high | Bluespec | bluespec | needs_research_or_confirmation | medium | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against the Bluespec language reference and add C-like comment tests. |
| high | Boo | boo | needs_research_or_confirmation | low | unresolved | unresolved | # | unresolved | unresolved | unresolved | unresolved | unresolved | Research Boo comment syntax before seeding. |
| high | Boogie | boogie | needs_research_or_confirmation | medium | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against the Boogie reference and add C-like comment tests. |
| high | BrighterScript | brighterscript | needs_research_or_confirmation | medium | unresolved | unresolved | '` and `REM | unsupported | unsupported | unsupported | unresolved | unresolved | Verify against BrighterScript docs and add BASIC-style comment tests. |
| high | Brightscript | brightscript | needs_research_or_confirmation | medium | unresolved | unresolved | '` and `REM | unsupported | unsupported | unsupported | unresolved | unresolved | Verify against Roku docs and add BASIC-style comment tests. |
| high | Browserslist | browserslist | needs_research_or_confirmation | medium | unresolved | unresolved | # | unsupported | unsupported | unsupported | unresolved | unresolved | Confirm config-file comment handling and add hash-comment tests. |
| high | Cabal Config | cabal_config | needs_research_or_confirmation | medium | unresolved | unresolved | -- | unsupported | unsupported | unsupported | unresolved | unresolved | Verify against Cabal syntax docs and add line-comment tests. |
| high | Cadence | cadence | needs_research_or_confirmation | medium | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against Cadence docs and add C-like comment tests. |
| high | CartoCSS | cartocss | needs_research_or_confirmation | low | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against CartoCSS docs before seeding. |
| high | Ceylon | ceylon | needs_research_or_confirmation | medium | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against Ceylon docs and add C-like comment tests. |
| high | Chapel | chapel | needs_research_or_confirmation | low | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against Chapel docs and add C-like comment tests. |
| high | Checksums | checksums | needs_research_or_confirmation | low | unresolved | unresolved | # | unsupported | unsupported | unsupported | unresolved | unresolved | Confirm the file format before adding a registry entry. |
| high | CIL | cil | needs_research_or_confirmation | low | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against the IL syntax docs and add C-style comment tests. |
| high | Cirru | cirru | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research Cirru syntax before adding registry support. |
| high | Clarion | clarion | needs_research_or_confirmation | low | unresolved | unresolved | ! | unsupported | unsupported | unsupported | unresolved | unresolved | Verify Clarion comment syntax before seeding. |
| high | Classic ASP | classic_asp | needs_research_or_confirmation | low | unresolved | unresolved | unsupported | <!-- ... --> | first closing delimiter wins | unsupported | unresolved | unresolved | Treat as a mixed-language format and verify HTML/script comment handling separately. |
| high | Clean | clean | needs_research_or_confirmation | low | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unresolved | unresolved | unresolved | Verify Clean comment nesting before seeding. |
| high | Click | click | needs_research_or_confirmation | medium | unresolved | unresolved | # | unsupported | unsupported | unsupported | unresolved | unresolved | Add hash-comment tests after confirming the Click parser docs. |
| high | CLIPS | clips | needs_research_or_confirmation | medium | unresolved | unresolved | ; | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify CLIPS comment syntax and add line/block tests. |
| high | Closure Templates | closure_templates | needs_research_or_confirmation | low | unresolved | unresolved | unsupported | {* ... *} | first closing delimiter wins | unsupported | unresolved | unresolved | Verify Soy/Closure Templates comment syntax before seeding. |
| high | CoffeeScript | coffeescript | needs_research_or_confirmation | high | unresolved | unresolved | # | ### ... ### | first closing delimiter wins | unsupported | https://coffeescript.org/ | unresolved | Seed line/block coverage and confirm block-comment stripping in tests. |
| high | Component Pascal | component_pascal | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | (* ... *) | first closing delimiter wins | unsupported | unresolved | unresolved | Verify before seeding; only the block delimiter is tentatively known. |
| high | Cool | cool | needs_research_or_confirmation | medium | unresolved | unresolved | -- | (* ... *) | true nesting supported | yes | unresolved | unresolved | Verify COOL nesting semantics and add line/block tests. |
| high | Creole | creole | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research the wiki syntax before seeding. |
| high | CSON | cson | needs_research_or_confirmation | medium | unresolved | unresolved | # | ### ... ### | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against CSON docs and add CoffeeScript-style comment tests. |
| high | Csound | csound | needs_research_or_confirmation | medium | unresolved | unresolved | ; | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against Csound docs and add line/block tests. |
| high | Csound Document | csound_document | needs_research_or_confirmation | low | unresolved | unresolved | ; | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify the document dialect before seeding. |
| high | Csound Score | csound_score | needs_research_or_confirmation | low | unresolved | unresolved | ; | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify the score dialect before seeding. |
| high | Cue Sheet | cue_sheet | needs_research_or_confirmation | low | unresolved | unresolved | REM` and `# | unsupported | unsupported | unsupported | unresolved | unresolved | Verify cue-sheet syntax before seeding. |
| high | CWeb | cweb | needs_research_or_confirmation | low | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | Research WEB/CWEB comment conventions before seeding. |
| high | Cycript | cycript | needs_research_or_confirmation | medium | unresolved | unresolved | // | /* ... */ | first closing delimiter wins | unsupported | unresolved | unresolved | Verify against Cycript docs and add C-like comment tests. |
| low | Brainfuck | brainfuck | resolved_non_actionable | high | unresolved | unresolved | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Document that non-command characters are ignored rather than treated as comments. |
| low | CSV | csv | resolved_non_actionable | high | unresolved | unresolved | unsupported | unsupported | unsupported | unsupported | unresolved | unresolved | Document as commentless unless a specific dialect is introduced. |

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
