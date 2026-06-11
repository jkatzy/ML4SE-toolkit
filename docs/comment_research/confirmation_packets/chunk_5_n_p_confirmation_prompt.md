# Implementation Confirmation Prompt: `chunk_5_n_p`

Use this packet together with:
- [implementation_confirmation_playbook.md](docs/comment_research/implementation_confirmation_playbook.md)
- [confirmation_report_template.md](docs/comment_research/confirmation_report_template.md)

## Mission

Confirm only the `needs_research_or_confirmation` entries in this packet by downloading a real language implementation, locating a designated hello-world or equivalent parser fixture, adding scratch comment probes, and parsing or tokenizing those scratch files with the implementation.

Target output file:
- `docs/comment_research/confirmation_reports/chunk_5_n_p_confirmation.md`

Allowed committed edit scope:
- `docs/comment_research/confirmation_reports/chunk_5_n_p_confirmation.md`

Scratch/output scope:
- `tmp/comment_research_confirmation/chunk_5_n_p/`

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
| NL | nl | low | GitHub Linguist `NL` data label as used by corpus metadata. | no language version identified; the label is classified as data with no TextMate scope. | unsupported | unsupported | unsupported | unsupported | docs/comment_research/chunk_5_n_p_report.md | unresolved | https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml | keep unsupported/unresolved until Stack v2 identifies a concrete NL format and syntax. |
| ObjDump | objdump | medium | GitHub Linguist `ObjDump` data/disassembly-output label. | no stable source-language version identified; objdump output varies by architecture and options. | unsupported | unsupported | unsupported | unsupported | docs/comment_research/chunk_5_n_p_report.md | unresolved | https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml | keep unsupported until the registry has a specific objdump flavor with a defensible comment convention. |

## Output Constraints

- Use one `## <Language>` section per assigned language.
- Keep every field from `confirmation_report_template.md`, including blocked fields.
- Do not claim confirmation from source inspection alone; the implementation must parse or tokenize the scratch file.
- Keep downloaded implementations and full command logs under `tmp/comment_research_confirmation/`.
- Leave unrelated worktree changes untouched.
