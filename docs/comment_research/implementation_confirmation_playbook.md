# Implementation Confirmation Playbook

This playbook defines the second-stage researcher for languages that remain
`needs_research_or_confirmation` after the online-first pass. Its job is to
validate the current syntax hypothesis against a real language implementation
and designated hello-world or example files.

## Mission

For each assigned language:

1. Start from the existing backlog row and chunk report section.
2. Download or clone the language implementation, grammar, lexer, parser, or
   official syntax tool into `tmp/comment_research_confirmation/`.
3. Locate designated hello-world files for the language.
4. Create scratch copies of those files and add comment probes for every
   candidate supported form.
5. Parse or tokenize those scratch files with the downloaded implementation.
6. Confirm, contradict, or block the current research entry with concrete
   command output and source paths.

This workflow is stronger than evidence-only research. A confirmation entry is
not accepted unless it uses a real implementation artifact and a parse/tokenize
check, or explicitly documents why that was impossible.

## Scope

Work only on backlog entries with status `needs_research_or_confirmation`.
Do not spend this pass on `ready_to_implement`, `resolved_non_actionable`, or
implemented registry languages unless a packet explicitly includes them as
context for a dialect split.

## Scratch Space

All downloaded implementations, package caches, built tools, generated
hello-world copies, and command logs belong under:

```text
tmp/comment_research_confirmation/<chunk>/<registry-key>/
```

Do not commit downloaded code, generated parser outputs, build directories, or
command logs. The committed artifact is only the confirmation report.

## Implementation Source Order

Prefer sources in this order:

1. Official compiler, interpreter, parser, lexer, or language server.
2. Official grammar repository or syntax package maintained by the language
   project.
3. Versioned implementation source cited by the existing chunk report.
4. Widely used grammar implementation, such as Tree-sitter or ANTLR, only when
   no official parser is available.

Record the exact URL, tag, commit, release, or archive version used. Do not
confirm a syntax from a generic highlighter when an official implementation is
available.

## Designated Hello-World Files

Use the first available source in this order:

1. A hello-world file or tutorial example explicitly designated by official
   language docs.
2. A hello-world, quickstart, tutorial, smoke-test, sample, or demo file in the
   downloaded implementation repository.
3. A minimal parser or lexer fixture in the implementation test suite that is
   meant to be parsed without executing user code.
4. A minimal hello-world file from an official examples repository.

Search names such as `hello`, `hello_world`, `helloworld`, `quickstart`,
`tutorial`, `sample`, `demo`, and `smoke`. If none exists, mark the language
`blocked` and record the exact locations searched. Do not invent an unofficial
hello-world file and call it designated evidence.

## Probe Construction

For each candidate comment form, add at least these probes to a scratch copy of
the designated file when the syntax allows it:

- standalone comment before executable or declarative code
- inline/trailing comment after code
- block comment between two code statements
- nested block comment when the current hypothesis claims true nesting
- negative probe for a plausible unsupported form when the existing research is
  ambiguous

Keep probes small and label them clearly, for example
`CONFIRM_LINE_COMMENT`, `CONFIRM_BLOCK_COMMENT`, and
`CONFIRM_NESTED_COMMENT`.

## Parse Requirement

Use a parse-only, tokenize-only, syntax-check, compile-without-run, or grammar
test mode. Do not execute downloaded programs unless the language tooling has
no parse-only mode and execution is the only documented way to validate syntax.
If execution is unavoidable, record why and use the smallest official
hello-world example.

Do not install tools globally. Prefer local build commands, package-manager
cache directories under `tmp/`, or source-tree parser commands. If the
implementation cannot be built or run in the current environment, record the
blocker instead of pretending a source inspection is equivalent to a parse
check.

## Verdicts

Use one verdict per language:

- `confirmed`: implementation parser accepts all supported probe forms and
  rejects or ignores unsupported probes consistently with the report.
- `partially-confirmed`: some forms are confirmed, but one or more forms remain
  untested because the implementation, example file, or parser command is
  unavailable.
- `contradicted`: implementation behavior disagrees with the current research.
- `blocked`: no trustworthy implementation parse check could be completed.

When contradicted, state the smallest safe next action: revise the research
entry, split a dialect, keep unsupported, or run a policy review.

## Output

Write a confirmation report using `confirmation_report_template.md`. The report
must include:

- current backlog hypothesis
- implementation artifact and version
- designated hello-world source
- scratch file paths
- exact parser/tokenizer commands
- result for each probe
- final verdict and recommended report update

Do not edit `src/ml4setk/Parsing/Comments/registry.py`, tests, or the original
`chunk_*_report.md` files during this confirmation pass unless the packet
explicitly says otherwise.
