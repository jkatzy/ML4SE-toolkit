# Comment Implementation Confirmation Template

Use this template for each language section inside a confirmation report.

```md
## <Language>

- Registry key:
- Backlog status:
- Source report:
- Current hypothesis:
- Implementation artifact:
- Implementation version:
- Local scratch path:
- Designated hello-world source:
- Parser command:
- Confirmation verdict:
- Recommended report update:
- Blockers:
- Notes:

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/...` | accepted | accepted | command/output summary |
| block comment | `tmp/...` | accepted | accepted | command/output summary |
| nested comment | `tmp/...` | accepted/rejected | accepted/rejected | command/output summary |
| unsupported form | `tmp/...` | rejected/ignored | rejected/ignored | command/output summary |

### Confirmed Examples

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

Rules:

- Keep every core field even when the confirmation is blocked.
- Use `unsupported` for probe categories that the language clearly lacks.
- Use `not tested` for probe categories that should exist but could not be
  checked with the implementation.
- Keep command output short. Link or name the full scratch log under `tmp/`
  instead of pasting long logs into the report.
- Do not claim `confirmed` unless an implementation command parsed or tokenized
  the scratch hello-world file.
