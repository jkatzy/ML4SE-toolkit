# Comment Testing Workflow

This directory holds a development-only adversarial testing workflow for the
comment parser.

The workflow is intentionally agent-oriented:

- a breaker agent writes inputs that try to fail the current parser or expose
  missing contracts
- a fixer agent validates those findings, adds regression tests, and patches
  the parser or registry when needed

## Canonical command

Generate the current prompt packets and chunk assignments with:

```bash
make comment-test-prompts
```

That command rebuilds:

- `docs/comment_testing/agent_chunk_assignments.json`
- `docs/comment_testing/prompt_packets/`

It also creates missing breaker/fixer thread files under
`docs/comment_testing/threads/` without overwriting existing findings.

## Layout

- `adversarial_playbook.md`: how the breaker and fixer roles should work
- `thread_template.md`: reference structure for per-chunk findings and
  resolutions
- `agent_chunk_assignments.json`: current chunk-to-language map
- `prompt_packets/`: generated breaker and fixer prompts per chunk
- `threads/`: breaker findings and fixer resolution logs

## Intended loop

1. Generate prompt packets.
2. Spawn one breaker and one fixer per chunk.
3. The breaker records only high-value failing or ambiguous cases, including
   internet-sourced probes for scenarios that research previously marked as
   unsupported or absent. Those sources are not limited to Stack Overflow;
   GitHub, SourceForge, project docs, issue trackers, blogs, tutorials, and
   similar sources are all in scope.
4. The fixer turns confirmed cases into regression tests and minimal code
   changes.
5. Regenerate packets as the supported-language set changes.

## Scope

This workflow exists to improve tests for already-implemented languages. It is
not the same as the comment-research workflow under `docs/comment_research`,
which is for discovering and validating new language syntaxes.
