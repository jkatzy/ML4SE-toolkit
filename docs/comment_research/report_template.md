# Comment Research Report Template

Use this template for each language section inside a chunk report.

```md
## <Language>

- Registry key:
- Line comments:
- Block comments:
- Termination behavior:
- Nested comments:
- Confidence:
- Evidence mode:
- Docs source:
- Implementation source:
- Community source:
- Corpus fallback source:
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

Rules:

- Keep the core fields even when evidence is weak so downstream scripts can
  still parse the report.
- `Termination behavior` should explain whether the block form is non-nesting,
  truly nested, or uses depth-qualified delimiters.
- Use `unsupported` when the language clearly lacks a comment form.
- Use `unresolved` when you cannot justify the syntax.
- Use `Community source` for Stack Overflow answers, blog posts, or tutorial
  pages found through search when official docs and implementation evidence
  are not enough on their own.
- If corpus fallback was required, include the raw file or repo URLs in
  `Corpus fallback source`.
