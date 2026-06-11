# Implementation Confirmation Prompt: `chunk_2_d_f`

Use this packet together with:
- [implementation_confirmation_playbook.md](docs/comment_research/implementation_confirmation_playbook.md)
- [confirmation_report_template.md](docs/comment_research/confirmation_report_template.md)

## Mission

Confirm only the `needs_research_or_confirmation` entries in this packet by downloading a real language implementation, locating a designated hello-world or equivalent parser fixture, adding scratch comment probes, and parsing or tokenizing those scratch files with the implementation.

Target output file:
- `docs/comment_research/confirmation_reports/chunk_2_d_f_confirmation.md`

Allowed committed edit scope:
- `docs/comment_research/confirmation_reports/chunk_2_d_f_confirmation.md`

Scratch/output scope:
- `tmp/comment_research_confirmation/chunk_2_d_f/`

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
| EQ | eq | unresolved | Search pass over the Stack label, `.eq` file-extension references, Altair Compose `eq` function documentation, and generic programming-language search results. | No unique source language or format was identified; `EQ` collides with operators, file extensions, product names, and mathematical/equality terminology. | unresolved | unresolved | unresolved | unresolved | docs/comment_research/chunk_2_d_f_report.md | https://file.org/extension/eq; https://help.altair.com/compose/help/en_us/topics/reference/oml_language/CoreMinimalInterpreter/eq.htm | src/ml4setk/Parsing/Comments/registry.py | identify the language before adding syntax. |

## Output Constraints

- Use one `## <Language>` section per assigned language.
- Keep every field from `confirmation_report_template.md`, including blocked fields.
- Do not claim confirmation from source inspection alone; the implementation must parse or tokenize the scratch file.
- Keep downloaded implementations and full command logs under `tmp/comment_research_confirmation/`.
- Leave unrelated worktree changes untouched.
