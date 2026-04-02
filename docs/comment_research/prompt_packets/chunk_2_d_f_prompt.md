# Online Comment Research Prompt: `chunk_2_d_f`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments.

Target output file:
- `docs/comment_research/chunk_2_d_f_report.md`

## Priority Summary

- Assigned languages: `16`
- Needs research or confirmation: `15`
- Ready to implement but should be strengthened with source evidence: `0`
- Resolved non-actionable: `1`

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
| high | DenizenScript | denizenscript | needs_research_or_confirmation | medium | `#` likely supported | unresolved | runs to newline | unsupported | unresolved | src/ml4setk/Parsing/Comments/registry.py | verify the comment form against an official parser or docs page before registry changes. |
| high | E | e | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | identify the exact language and source manual first. |
| high | Eagle | eagle | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | identify the exact format or language before adding syntax. |
| high | EBNF | ebnf | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | identify the exact EBNF dialect in scope before adding syntax. |
| high | eC | ec | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | verify the Ecere/eC reference before encoding comment syntax. |
| high | Edje Data Collection | edje_data_collection | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | confirm the `.edc` syntax before adding a registry entry. |
| high | EmberScript | emberscript | needs_research_or_confirmation | medium | `#` supported | `### ... ###` supported | first closing delimiter wins | unsupported | unresolved | https://github.com/ghempton/ember-script | keep this as a corpus-backed entry until an official syntax page or grammar is pinned. |
| high | EQ | eq | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | identify the language before adding syntax. |
| high | F* | f_star | needs_research_or_confirmation | medium | `//` supported | `(* ... *)` supported | first closing delimiter wins | unresolved | https://fstar-lang.org/tutorial/book/part1/part1_getting_off_the_ground.html | https://github.com/FStarLang/FStar | add line and block tests now; confirm nesting before encoding it as supported. |
| high | Fennel | fennel | needs_research_or_confirmation | medium | `;` supported | unsupported | runs to newline | unsupported | unresolved | https://github.com/bakpakin/Fennel | keep the corpus-backed line-comment rule and avoid inventing block syntax. |
| high | FIGlet Font | figlet_font | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | identify the exact font-file format before adding syntax. |
| high | Filebench WML | filebench_wml | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | verify the WML syntax from Filebench docs first. |
| high | FLUX | flux | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | pin the exact FLUX language or format first. |
| high | Formatted | formatted | needs_research_or_confirmation | unresolved | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | determine what "Formatted" refers to in Stack v2. |
| high | Frege | frege | needs_research_or_confirmation | medium | `--` supported | `{- ... -}` supported | first closing delimiter wins | unresolved | https://www.frege-lang.org/doc/frege/Prelude.html | https://github.com/Frege/frege | keep the Haskell-like line and block forms, then confirm nesting against a parser or lexer before registry changes. |
| low | Diff | diff | resolved_non_actionable | high | unsupported | unsupported | unsupported | unsupported | https://www.gnu.org/software/diffutils/manual/html_node/Unified-Format.html | src/ml4setk/Parsing/Comments/registry.py | leave unsupported. |

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
