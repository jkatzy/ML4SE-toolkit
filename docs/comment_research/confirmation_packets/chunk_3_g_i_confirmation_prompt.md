# Implementation Confirmation Prompt: `chunk_3_g_i`

Use this packet together with:
- [implementation_confirmation_playbook.md](docs/comment_research/implementation_confirmation_playbook.md)
- [confirmation_report_template.md](docs/comment_research/confirmation_report_template.md)

## Mission

Confirm only the `needs_research_or_confirmation` entries in this packet by downloading a real language implementation, locating a designated hello-world or equivalent parser fixture, adding scratch comment probes, and parsing or tokenizing those scratch files with the implementation.

Target output file:
- `docs/comment_research/confirmation_reports/chunk_3_g_i_confirmation.md`

Allowed committed edit scope:
- `docs/comment_research/confirmation_reports/chunk_3_g_i_confirmation.md`

Scratch/output scope:
- `tmp/comment_research_confirmation/chunk_3_g_i/`

Do not edit `src/`, `tests/`, `registry.py`, original chunk reports, backlog/candidate views, or other confirmation reports.

## Required Workflow

1. Read the playbook and template completely.
2. For each language, read the current source report entry first.
3. Download or clone the official implementation, grammar, lexer, parser, or syntax tool into the chunk scratch directory.
4. Locate the designated hello-world file using the playbook's source order. If none exists, record `blocked` with searched paths.
5. Build minimal scratch copies of the hello-world file with line, block, nested, and negative probes as applicable.
6. Run a parse-only, tokenize-only, syntax-check, or compile-without-run command from the downloaded implementation.
7. Record exact commands, local scratch paths, result summaries, and a verdict: `confirmed`, `partially-confirmed`, `contradicted`, or `blocked`.
8. If contradicted, recommend the smallest next action without changing production code or registry entries.

## Language Queue

| Language | Registry key | Confidence | Current version scope | Current version syntax | Current line | Current block | Current termination | Current nested | Source report | Docs source | Implementation source | Current recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Genero Forms | genero_forms | medium | Genero Forms `.per` examples in Genero 3.00.06 and 4.01.38 tutorials | both checked tutorial versions show `--` comments in `.per` form files; no form-file-specific block syntax was confirmed | -- | unsupported | line comments end at newline | unsupported | docs/comment_research/chunk_3_g_i_report.md | https://4js.com/online_documentation/fjs-genero-3.00.06-manual-tutorial-html/genero-tutorial-topics/c_fgl_TutChap10_010.html; https://4js.com/online_documentation/fjs-genero-4.01.38-manual-tutorial-html/genero-tutorial-topics/c_fgl_TutChap10_010.html | unresolved | Add `.per` fixtures that keep `--` comment lines in place and do not assume brace or hash comments unless a form-file grammar source confirms them. |
| Graph Modeling Language | graph_modeling_language | medium | original GML technical report references plus current NetworkX GML parser behavior | the original format uses a `comment` key-value attribute for graph metadata; common parsers such as NetworkX also accept `#` line comments as lexical comments | `#` in NetworkX/common-parser dialects; no semicolon or slash line comments confirmed | unsupported | `#` comments run to the end of the physical line | unsupported | docs/comment_research/chunk_3_g_i_report.md | https://raw.githubusercontent.com/GunterMueller/UNI_PASSAU_FMI_Graph_Drawing/master/GML/gml-technical-report.pdf | https://networkx.org/documentation/stable/_modules/networkx/readwrite/gml.html; https://github.com/networkx/networkx/blob/main/networkx/readwrite/gml.py | Add `#` line-comment support if the registry targets common Graph Modeling Language parser behavior; do not treat the `comment "..."` key as a lexical comment delimiter. |

## Output Constraints

- Use one `## <Language>` section per assigned language.
- Keep every field from `confirmation_report_template.md`, including blocked fields.
- Do not claim confirmation from source inspection alone; the implementation must parse or tokenize the scratch file.
- Keep downloaded implementations and full command logs under `tmp/comment_research_confirmation/`.
- Leave unrelated worktree changes untouched.
