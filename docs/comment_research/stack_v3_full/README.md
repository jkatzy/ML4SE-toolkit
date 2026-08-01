# Stack v3 Full Comment-Syntax Intake

This directory contains reviewed research records for exact labels in the full
Stack v3 corpus. Research records are development-only inputs to implementation;
they are not parser support claims by themselves.

## Dataset provenance

- Dataset: `HuggingFaceCode/stack-v3-full`
- Published statistics repository: `HuggingFaceCode/stack-v3-train`
- Immutable revision: `716a043a6c2adc34a2032b159364908a09ffe4ec`
- Full statistics path: `stats/full/stats_by_language.json`
- Full statistics SHA-256:
  `804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45`
- Retrieved: `2026-08-01`
- Exact labels: `770`
- Registry-resolved labels at intake: `618`
- Unresolved labels at intake: `152`
- New-or-renamed unresolved queue under the official v2 config comparison: `116`
- Total intake decisions including the original v2 public inventory discrepancy: `121`

The statistics table aggregates the exact `files[].language` labels emitted by
go-enry. A label may identify a programming language, dialect, template,
document format, serialized data, generated output, or container. Presence in
the dataset does not establish that source comments exist.

## Intake outcome

- Registry-resolved labels after implementation: `716` of `770`
- Accepted reviewed decisions: `99` (`32` aliases, `47` contextual helpers,
  `18` separate families, and `2` direct implementations)
- Reviewed labels kept unresolved: `22` (`11` unsupported and `11` deferred)
- Pre-existing unresolved carryover outside the new-or-renamed intake: `32`

All `116` labels in the pinned new-or-renamed intake and all `5` inventory
discrepancies have a reviewed decision. The remaining carryover labels are not
silently treated as completed: they continue to raise `NotImplementedError`
until they receive their own evidence-backed intake. The `Nu` collision among
those carryovers is separately documented in `batch_06.md`; the other `31`
carryovers were not part of this release's new-language scope.

## Reproduce the queue

```bash
make research-prompts
```

This writes the verified inventory, assignments, and prompt packets below
`tmp/stack_v3_comment_research/`. Those files are ignored run artifacts. The
generator compares the pinned inventory through the runtime registry resolver,
so punctuation and Stack-style normalization are exercised exactly as users
encounter them.

## Batch ledger

| Batch | Labels | Research | Review | Implementation |
| --- | ---: | --- | --- | --- |
| `batch_00` | 10 | complete | complete | complete |
| `batch_01` | 10 | complete | complete | complete |
| `batch_02` | 10 | complete | complete | complete |
| `batch_03` | 10 | complete | complete | complete |
| `batch_04` | 10 | complete | complete | complete |
| `batch_05` | 10 | complete | complete | complete |
| `batch_06` | 10 | complete | complete | complete |
| `batch_07` | 10 | complete | complete | complete |
| `batch_08` | 10 | complete | complete | complete |
| `batch_09` | 10 | complete | complete | complete |
| `batch_10` | 10 | complete | complete | complete |
| `batch_11` | 6 | complete | complete | complete |
| `inventory_discrepancy_00` | 5 | complete | complete | complete |

Researchers write one record per batch using the repository template. A
separate reviewer must accept each label as `alias`, `implement`,
`separate-family`, `contextual-helper`, `unsupported`, or `defer` before an
implementation agent changes code.

## Implementation gate

An implementation agent must preserve the exact raw dataset label in a lookup
regression, add representative seeded examples for every syntax form, and add
adversarial negatives for relevant strings, directives, operators, malformed
input, line endings, and embedded-language boundaries. Confirmed failures become
ordinary deterministic tests before their fixes.

Formats proven to lack source comments remain unsupported. Containers and
aggregate labels remain unresolved unless the dataset representation supplies a
single defensible extraction contract.
