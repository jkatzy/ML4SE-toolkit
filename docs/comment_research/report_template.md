# Comment Syntax Research Record

Create one copy of this template per reviewable research batch. Remove
placeholder text rather than retaining empty claims.

## Dataset provenance

- Dataset/project:
- Immutable revision or checksum:
- Retrieved:
- Inventory source and label column:
- Researcher or agent:
- Review status: `draft` / `reviewed` / `blocked`

## <Exact dataset language label>

### Identity and scope

- Raw dataset label:
- Proposed registry key:
- Existing family or aliases checked:
- Classification: `language` / `dialect` / `template` / `document-format` /
  `generated-format` / `aggregate` / `unknown`
- Versions or releases checked:
- Dialects checked:
- Intended support scope:
- Explicitly excluded scope:

### Syntax contract

- Line comments:
- Block comments:
- Nested comments:
- Termination at newline, delimiter, or EOF:
- Inline use:
- Adjacent-line grouping:
- Unclosed delimiter behavior:
- Lexical or structural context:
- Conflicts with strings, operators, directives, or embedded languages:
- Sanitizer line wrappers:
- Sanitizer block wrappers:
- Content-preservation expectations:

Use `unsupported` when evidence shows a form does not exist and `unresolved`
when evidence is insufficient. Do not use either term interchangeably.

### Evidence

- Official documentation permalink:
- Documentation version and relevant section:
- Official implementation or grammar permalink:
- Implementation version, file, and relevant symbol:
- Conformance test or official example permalink:
- Secondary source, if needed:
- Evidence conflicts or gaps:
- Confidence: `verified` / `cross-checked` / `provisional` / `unresolved`

### Implementation confirmation

- Implementation tested:
- Exact version or commit:
- Probe method:
- Probe input:

```text
<minimal source that distinguishes the disputed behavior>
```

- Observed result:
- Conclusion and limits of the probe:

### Representative examples

#### Line comment

```text
<real surrounding syntax and expected extracted region>
```

#### Block comment

```text
<real surrounding syntax and expected extracted region>
```

#### Nested or contextual comment

```text
<real surrounding syntax and expected extracted region>
```

### Adversarial boundaries

- Negative cases:
- Malformed-input cases:
- Line-ending and Unicode cases:
- Version or dialect counterexamples:
- Cleaner preservation cases:

### Decision

- Recommended action: `implement` / `alias` / `separate-family` /
  `contextual-helper` / `unsupported` / `defer`
- Registry fields to change:
- Deterministic tests to add:
- Remaining blocker:
- Reviewer:
- Review date:
