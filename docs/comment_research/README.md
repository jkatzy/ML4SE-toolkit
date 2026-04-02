# Stack v2 Comment Research

This directory is the staging area for expanding comment parsing coverage to
the public Stack v2 language inventory derived from:

`https://huggingface.co/spaces/bigcode/stack-v2-extensions/resolve/main/stackv2_languages_freq.csv`

## Files

- `stackv2_public_language_inventory.csv`: normalized public language list with
  current registry coverage.
- `agent_chunk_assignments.json`: deterministic chunking of currently uncovered
  languages.
- `chunk_*_report.md`: per-agent research output for one chunk.
- `online_research_playbook.md`: stronger online-first research method with
  a docs-first, search-engine community fallback, and corpus-fallback workflow.
- `report_template.md`: report skeleton for the stronger worker output.
- `prompt_packets/`: generated per-chunk prompt files for stronger workers.
- `not_done_backlog.md` and `not_done_backlog.csv`: generated backlog for every
  still-unimplemented Stack v2 language, split by implementation readiness.
- `registry_ready_candidates.md` and `registry_ready_candidates.csv`: generated
  high-confidence subset that can be turned into registry entries and tests next.

## Regeneration

Run:

```bash
uv run python scripts/build_comment_research_views.py
uv run python scripts/build_comment_research_packets.py
```

The script reads the chunk reports, cross-checks them against the Stack v2
inventory, and rebuilds the backlog and candidate views.
The packet builder creates stronger online-first worker prompts for each chunk.

## Worker contract

Each worker owns exactly one `chunk_*_report.md` file.

For the stronger workflow, start from:

- `online_research_playbook.md`
- `report_template.md`
- the relevant file in `prompt_packets/`

The output should be documentation-oriented and test-oriented at the same time.
Do not just list tokens. For each assigned language, include:

- Stack v2 name
- Suggested registry key
- Line comment syntax
- Block comment syntax
- Termination behavior for block-style comments
- Whether nested comments are supported
- One real demo code snippet for each supported case:
  line comment, block comment, and nested comment when applicable
- Official docs source
- Implementation or grammar source
- Community source when Stack Overflow, blog posts, or tutorial pages were
  needed to clarify the syntax
- Corpus fallback source when needed
- Confidence
- Recommended action
- Notes or ambiguities

Use a per-language markdown section that can be copied directly into later
documentation. A good structure is:

```md
## <Language>

- Registry key:
- Line comments:
- Block comments:
- Termination behavior:
- Nested comments:
- Confidence:
- Docs source:
- Implementation source:
- Recommended action:
- Notes:

### Examples

#### Line comment
```text
real surrounding code here
```

#### Block comment
```text
real surrounding code here
```

#### Nested comment
```text
real surrounding code here
```
```

If a language does not support one of the categories, state that explicitly.
Prefer official language documentation first and implementation or grammar
sources second. When you need a search-engine fallback, include `programming
language` in the query so ambiguous names bias toward language results instead
of tools, frameworks, or products. If the syntax is unclear, mark it as
unresolved instead of guessing.
