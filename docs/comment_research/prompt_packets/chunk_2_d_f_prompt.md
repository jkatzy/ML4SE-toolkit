# Online Comment Research Prompt: `chunk_2_d_f`

Use this packet together with:
- [online_research_playbook.md](docs/comment_research/online_research_playbook.md)
- [report_template.md](docs/comment_research/report_template.md)

## Mission

Go online for every language in this chunk. Search official documentation first to find the language's definition of comments. If that fails or remains ambiguous, inspect an implementation source. If that still leaves uncertainty, use a search engine with the language name plus `programming language` and `comment` to find secondary sources such as Stack Overflow answers or blog posts. If that still does not resolve the syntax, download real files for the language and inspect them for likely comments. Do not stop at a single source: reconcile multiple sources and explicitly look for version-specific or dialect-specific differences.

Target output file:
- `docs/comment_research/chunk_2_d_f_report.md`

## Priority Summary

- Assigned languages: `13`
- Needs research or confirmation: `12`
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
| high | DenizenScript | denizenscript | needs_research_or_confirmation | medium | Current Denizen Beginner's Guide and Meta Documentation pages; reviewed the maintained DenizenCore/Denizen docs surface rather than an archived legacy release. | No version split confirmed; the current docs use # to comment out whole command lines, so keep the verified line-comment form only and do not infer block syntax. | `#` likely supported | unresolved | runs to newline | unsupported | https://guide.denizenscript.com/guides/basics/mechanisms.html; https://guide.denizenscript.com/guides/troubleshooting/common-mistakes; https://meta.denizenscript.com/Docs/Commands/ | src/ml4setk/Parsing/Comments/registry.py | verify the comment form against an official parser or docs page before registry changes. |
| high | E | e | needs_research_or_confirmation | unresolved | Original E-on-Java specification pages, current ERights language pages, and 0.9-era examples that use pragma.syntax("0.9"); the exact comment policy was not pinned in the sources checked. | No comment-token split confirmed across the reviewed E materials; the sources expose the E/Kernel-E language family but do not explicitly document a stable comment delimiter, so keep this entry unresolved. | unresolved | unresolved | unresolved | unresolved | https://erights.org/history/original-e/programmers/LanguageSpec.html; https://erights.org/elang/; https://erights.org/elang/quick-ref.html; https://erights.org/history/original-e/programmers/Econcepts.html | src/ml4setk/Parsing/Comments/registry.py | identify the exact language and source manual first. |
| high | Eagle | eagle | needs_research_or_confirmation | medium | Autodesk EAGLE ULP docs in current Fusion Electronics help, plus the 2016 Autodesk ULP blog post and recent forum references to EAGLE 5/9.x behavior. | The reviewed ULP sources present C-like syntax and a sample that uses // comments; no separate block-comment rule was confirmed, so the registry should add only the verified line-comment form until a block form is pinned. | `//` supported | unresolved | runs to newline | unresolved | https://help.autodesk.com/cloudhelp/ENU/Fusion-ECAD/files/ECD-WRITE-ULP-REF.htm; https://help.autodesk.com/cloudhelp/ENU/Fusion-ECAD/files/ECD-USER-LANG-REF.htm; https://www.autodesk.com/products/fusion-360/blog/what-you-didnt-know-about-eagle-user-language-programming/ | src/ml4setk/Parsing/Comments/registry.py | add the verified `//` line-comment fixture now and keep block syntax out of the registry until a source pins it. |
| high | EBNF | ebnf | needs_research_or_confirmation | unresolved | ISO/IEC 14977:1996, the Cambridge ISO EBNF summary, Microsoft's EBNF-M page, and RFC 2234/5234 ABNF material used only for comparison because the Stack label is generic. | No canonical comment syntax was found for generic EBNF; the sources reviewed show that comment conventions are dialect-specific, so keep the label unresolved until a concrete EBNF dialect is pinned. | unresolved | unresolved | unresolved | unresolved | https://iso.org/standard/26153.html; https://www.cl.cam.ac.uk/~mgk25/iso-ebnf.html; https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/8deb6d43-3e71-493b-9465-b84bb3cd3c45; https://datatracker.ietf.org/doc/rfc5234/ | src/ml4setk/Parsing/Comments/registry.py | identify the exact EBNF dialect in scope before adding syntax. |
| high | eC | ec | needs_research_or_confirmation | unresolved | Current Ecere SDK / eC project materials plus the 2017 Ecere overview article; I did not find a versioned grammar page that pinned comment syntax. | No version split or dialect split was confirmed in the reviewed sources; the language is described as C-style, but that is not sufficient to encode a comment token safely without an authoritative reference. | unresolved | unresolved | unresolved | unresolved | https://opensource.com/article/17/9/ecere; https://github.com/ecere/ecere-sdk | src/ml4setk/Parsing/Comments/registry.py | verify the Ecere/eC reference before encoding comment syntax. |
| high | Edje Data Collection | edje_data_collection | needs_research_or_confirmation | medium | Legacy Edje reference material plus current Tizen EDC docs, including the Tizen 2.4+ layouting pages and the newer Tizen 5.x-era EDC editor/deprecation notes. | No version split was confirmed; the reviewed EDC examples use C-style block comments (/* ... */) in current docs, and I did not find an older dialect that changed the delimiter. If the registry targets .edc, add the block form only. | unresolved | `/* ... */` supported | first closing delimiter wins | unresolved | https://docs.tizen.org/application/native/guides/ui/efl/learn-edc-intro/; https://docs.tizen.org/application/native/guides/ui/efl/learn-edc-positioning-parts/; https://www.enlightenment.org/_legacy_embed/edje_main.html; https://docs.tizen.org/application/tizen-studio/native-tools/edc-editor/ | src/ml4setk/Parsing/Comments/registry.py | add a block-comment regression test for .edc and keep line comments unresolved until a source pins them. |
| high | EmberScript | emberscript | needs_research_or_confirmation | medium | unresolved | unresolved | `#` supported | `### ... ###` supported | first closing delimiter wins | unsupported | unresolved | https://github.com/ghempton/ember-script | keep this as a corpus-backed entry until an official syntax page or grammar is pinned. |
| high | EQ | eq | needs_research_or_confirmation | unresolved | The Stack label was not pinned to a unique language or format; I checked generic EQ references and could not isolate an authoritative manual for a specific EQ dialect. | No defensible comment syntax was found; the label remains unresolved until the intended language or file format is identified. | unresolved | unresolved | unresolved | unresolved | https://file.org/extension/eq; https://help.altair.com/compose/help/en_us/topics/reference/oml_language/CoreMinimalInterpreter/eq.htm | src/ml4setk/Parsing/Comments/registry.py | identify the language before adding syntax. |
| high | FIGlet Font | figlet_font | needs_research_or_confirmation | unresolved | FIGlet 2.2.1 FIGfont standard draft 2.0 plus parser docs for figlet v0.3.2; the sources also note that older FIGlet/FIGWin versions motivated the format. | The format uses a counted comment section after the header line rather than a token-based in-band delimiter; no alternate version split was confirmed, so treat the comments as file metadata rather than a source-code comment syntax. | unresolved | unresolved | unresolved | unresolved | https://sources.debian.org/src/figlet/2.2.1-4/figfont.txt; https://www.figlet.org/figlet-man.html; https://hexdocs.pm/figlet/Figlet.Parser.FontFileParser.html | src/ml4setk/Parsing/Comments/registry.py | keep this unresolved unless the stack label is reclassified as FIGfont metadata rather than code comments. |
| high | Filebench WML | filebench_wml | needs_research_or_confirmation | unresolved | Filebench 1.4.9.1 man-page material, the 1.5-alpha1 quick-start docs, and the current filebench GitHub wiki/repo examples. | No comment delimiter was confirmed in the reviewed WML sources; the versioned docs describe the workload structure and commands but do not pin a stable comment token, so keep the entry unresolved. | unresolved | unresolved | unresolved | unresolved | https://github.com/filebench/filebench; https://github-wiki-see.page/m/filebench/filebench/wiki/Workload-model-language; https://www.mankier.com/package/filebench | src/ml4setk/Parsing/Comments/registry.py | verify the WML syntax from Filebench docs first. |
| high | FLUX | flux | needs_research_or_confirmation | unresolved | The label was not pinned to a specific language, file format, or versioned dialect; only the Stack v2 label and the ambiguous name were checked. | No versioned or dialect-specific comment syntax could be established, so leave this unresolved. | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | pin the exact FLUX language or format first. |
| high | Formatted | formatted | needs_research_or_confirmation | unresolved | The label was not pinned to a unique language or file format; the Stack v2 name alone does not identify an authoritative manual or dialect family. | No versioned or dialect-specific comment syntax could be established, so leave this unresolved. | unresolved | unresolved | unresolved | unresolved | unresolved | src/ml4setk/Parsing/Comments/registry.py | determine what "Formatted" refers to in Stack v2. |
| low | Diff | diff | resolved_non_actionable | high | unresolved | unresolved | unsupported | unsupported | unsupported | unsupported | https://www.gnu.org/software/diffutils/manual/html_node/Unified-Format.html | src/ml4setk/Parsing/Comments/registry.py | leave unsupported. |

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
