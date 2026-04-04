# Online Comment Research Prompt: `chunk_6_q_s`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name plus `programming language` and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments. Do not stop at a single source: reconcile multiple sources and explicitly look for version-specific or dialect-specific differences.

Target output file:
- `docs/comment_research/chunk_6_q_s_report.md`

## Priority Summary

- Assigned languages: `51`
- Needs research or confirmation: `51`
- Ready to implement but should be strengthened with source evidence: `0`
- Resolved non-actionable: `0`

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
| high | Qt Script | qt_script | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Ragel | ragel | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | RAML | raml | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Rascal | rascal | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Raw token data | raw_token_data | needs_research_or_confirmation | unresolved | unresolved | unresolved | unsupported | unsupported | unresolved | unsupported | unresolved | GitHub Linguist languages.yml | unsupported |
| high | REALbasic | realbasic | needs_research_or_confirmation | medium | unresolved | unresolved | ' | unsupported | line comments terminate at end-of-line; block comments unsupported | no | https://docs.xojo.com/api/language/introspection/constructorinfo.html | GitHub Linguist languages.yml | candidate |
| high | Reason | reason | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Red | red | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | ; | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Redcode | redcode | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | ; | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Redirect Rules | redirect_rules | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | Regular Expression | regular_expression | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | Ren'Py | renpy | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | RenderScript | renderscript | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | ReScript | rescript | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Rich Text Format | rich_text_format | needs_research_or_confirmation | unresolved | unresolved | unresolved | unsupported | unsupported | unresolved | unsupported | unresolved | GitHub Linguist languages.yml | unsupported |
| high | Rouge | rouge | needs_research_or_confirmation | unresolved | unresolved | unresolved | unsupported | unsupported | unresolved | unsupported | unresolved | GitHub Linguist languages.yml | unsupported |
| high | RPC | rpc | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | RPGLE | rpgle | needs_research_or_confirmation | medium | unresolved | unresolved | // | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | candidate |
| high | RPM Spec | rpm_spec | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Sage | sage | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SaltStack | saltstack | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | {# #} | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | sed | sed | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Self | self | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | SELinux Policy | selinux_policy | needs_research_or_confirmation | medium | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/using_selinux/writing-a-custom-selinux-policy | https://github.com/SELinuxProject/refpolicy | candidate |
| high | ShaderLab | shaderlab | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Singularity | singularity | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Slash | slash | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | Slice | slice | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Smali | smali | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SmPL | smpl | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SMT | smt | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | ; | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Solidity | solidity | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Soong | soong | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SourcePawn | sourcepawn | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Spline Font Database | spline_font_database | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SQF | sqf | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SQLPL | sqlpl | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | -- | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Squirrel | squirrel | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SRecode Template | srecode_template | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | SSH Config | ssh_config | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Stan | stan | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | Standard ML | standard_ml | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | unsupported | (* *) | block comments support true nesting | yes | unresolved | GitHub Linguist languages.yml | implement |
| high | STAR | star | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | STL | stl | needs_research_or_confirmation | unresolved | unresolved | unresolved | unsupported | unsupported | unresolved | unsupported | unresolved | GitHub Linguist languages.yml | unsupported |
| high | STON | ston | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | StringTemplate | stringtemplate | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | unknown | unresolved | GitHub Linguist languages.yml | needs manual research |
| high | Stylus | stylus | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SubRip Text | subrip_text | needs_research_or_confirmation | unresolved | unresolved | unresolved | unsupported | unsupported | unresolved | unsupported | unresolved | GitHub Linguist languages.yml | unsupported |
| high | SugarSS | sugarss | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | unsupported | /* */ | block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SuperCollider | supercollider | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |
| high | SWIG | swig | needs_research_or_confirmation | seeded-from-implementation | unresolved | unresolved | // | /* */ | line comments terminate at end-of-line; block comments terminate at first closing delimiter | no | unresolved | GitHub Linguist languages.yml | implement |

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
