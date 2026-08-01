# Comment Syntax Research

Use this workflow when a dataset revision introduces new language labels or
changes the frequency and coverage of existing labels. This directory holds
curated method documentation, not dataset snapshots, generated prompt packets,
raw model output, or one-off worker reports.

Start one research record from [the template](report_template.md) for each
unresolved label. Keep large inputs and investigation artifacts outside the
tracked tree.

## 1. Identify the dataset revision

Record enough provenance to reproduce the inventory:

- dataset name and owning project
- immutable revision, commit, release, or content checksum
- retrieval date
- source table or split and the column containing the language label
- the exact label, including punctuation and capitalization
- the observed record count, when it affects prioritization

Never document a moving `main`, `latest`, or default dataset revision as if it
were immutable. If the provider exposes no revision identifier, record a
checksum for the downloaded inventory.

## 2. Reconcile labels with the registry

Get the currently supported keys from the package rather than copying a count
from documentation:

```bash
uv run python -c \
  'from ml4setk import get_supported_comment_languages as g; print("\\n".join(g()))'
```

For every new label:

1. Preserve the raw dataset label in the research record.
2. Test whether registry lookup already resolves it through case-insensitive or
   Stack-style normalization.
3. Propose a stable lowercase key only after checking for collisions and
   existing aliases.
4. Classify the label as a language, dialect, embedded-language container,
   template, document format, generated format, aggregate, or unknown.
5. Mark aggregate or ambiguous labels unresolved unless the dataset defines a
   single comment contract for them.

An alias is appropriate only when extraction and cleaning semantics match an
existing family. Similar spelling, ancestry, or file extensions are not enough.

## 3. Establish syntax from evidence

Research in this order:

1. Versioned official language or format specification.
2. Lexer, tokenizer, parser, or grammar from the official implementation.
3. Official conformance tests and version-matched example source.
4. Maintainer documentation or a widely used independent implementation.
5. Community material only to locate stronger evidence or document a known
   ambiguity.

Use permalinks pinned to a release tag or commit when citing source. Inspect the
actual lexer action, not only the token declaration: termination at EOF, nested
delimiters, escapes, columns, whitespace, preprocessing, and lexical modes can
change the meaning of a marker.

For an executable implementation, confirm uncertain behavior with the smallest
possible probe through its parser, tokenizer, compiler, or syntax checker.
Record the implementation version, command class, exit result, and what the
probe proves. Keep downloaded implementations and probe output untracked.

Do not infer source comments from rendered comments, documentation annotations,
shebangs, pragmas, string literals, host-language blocks, or a related language.
When primary sources disagree, record the disagreement and leave the entry
unresolved.

## 4. Handle versions and dialects

State the versions and dialects examined and the scope the registry key will
promise. Compare at least the dataset's relevant version with the current
implementation when syntax may have changed.

- Use one family with aliases when all supported forms and exclusions agree.
- Use distinct families when delimiters, nesting, termination, or lexical rules
  differ materially.
- Use language-specific exclusions only for a documented dialect-specific
  directive or operator within an otherwise shared family.
- Scope mixed template and markup formats to the layer represented by the
  dataset label. Do not automatically inherit comments from embedded code.
- If the dataset does not carry version metadata, implement only a defensible
  common contract and describe what is intentionally excluded.

## 5. Convert evidence into implementation

Before coding, the report must state:

- line, block, nested, contextual, or unsupported behavior
- exact delimiters and termination rules
- whether inline and adjacent-line grouping are valid
- false-positive boundaries, including strings, operators, directives, and
  format structure
- sanitizer wrappers and content-preservation expectations
- documentation and implementation evidence with confidence

Then update `COMMENT_SYNTAXES` and add a representative seed for every
implemented feature. Prefer data in the registry. Add a focused helper only for
syntax whose validity depends on lexical or file structure that a delimiter
pattern cannot represent.

Verify the new language with focused tests:

```bash
uv run pytest \
  tests/test_comment_registry.py \
  tests/test_comment_queries.py \
  tests/test_comment_generated_cases.py \
  tests/test_comment_language_fixtures.py \
  tests/test_comment_sanitizer.py \
  -q --no-cov
make comment-fuzz
make comment-cleaner-fuzz
```

Add explicit negative fixtures for every researched boundary that generated
registry tests cannot prove. Follow `docs/comment_testing/README.md` for
adversarial testing, judge-assisted discovery, and regression intake. Every
confirmed failure must be minimized into a deterministic test before the code
fix is considered complete.

## Completion criteria

A label is ready to implement only when its identity, version scope, syntax,
termination and nesting behavior, false-positive boundaries, and cleaning
contract are supported by pinned evidence. Otherwise, mark it `unresolved` with
a concrete next check. "Likely", syntax-highlighter behavior, or an LLM answer
alone is not implementation evidence.
