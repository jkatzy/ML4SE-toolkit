# Online Comment Research Playbook

This playbook defines the stronger research workflow for comment-syntax
discovery. The goal is to replace "best guess" entries with evidence-backed
entries that can safely drive registry updates and generated tests.

## Mission

For each assigned language:

1. Find the language's comment syntax from official documentation whenever
   possible.
2. Cross-check it against an implementation source such as a lexer, parser,
   grammar, or syntax highlighter when available.
3. If documentation or implementation sources are missing, vague, or
   contradictory, use a search engine to find secondary sources such as
   Stack Overflow answers, blog posts, tutorials, or issue threads that may
   explain the language's comment rules in practice.
4. If secondary sources still do not resolve the syntax, download real source
   files for that language and inspect them for likely comment forms.
5. Produce documentation-oriented output with evidence, confidence, and real
   code snippets that can later be turned into parser fixtures and tests.

## Evidence Ladder

Use this order of preference:

1. Official language spec, manual, or reference documentation.
2. Official implementation source:
   compiler, interpreter, lexer, parser, grammar, or reference tooling.
3. Search-engine-discovered community explanations:
   Stack Overflow, well-cited blog posts, tutorial pages, issue discussions,
   or language-community Q&A that directly address comment syntax.
4. Widely used grammar implementations:
   Tree-sitter, ANTLR, GitHub Linguist, editor grammars, or parser repos.
5. Corpus fallback:
   downloaded source files from real public repositories or official example
   repositories for that language.

Do not skip directly to corpus inference if an official or community source is
available.

## Phase 1: Docs-First Search

Start with targeted web queries such as:

- `<Language> programming language comments syntax`
- `<Language> programming language comment`
- `<Language> programming language reference comments`
- `<Language> programming language lexical grammar comments`
- `<Language> programming language line comment block comment`
- `site:stackoverflow.com <Language> programming language comment`
- `site:stackoverflow.com <Language> programming language block comment`
- `site:stackoverflow.com <Language> programming language nested comments`
- `<Language> programming language comment tutorial`
- `<Language> programming language comment blog`

When the language has a known project or foundation site, prefer that domain.
When the docs are versioned, capture the exact URL you used.

You are looking for:

- line comment markers
- block comment delimiters
- how block comments terminate
- whether nested comments are supported
- whether there are depth-qualified or escape-like delimiter variants
- any dialect restrictions
- whether comment syntax is context-sensitive

For every language, explicitly classify:

1. line comments
2. block comments
3. delimiter behavior:
   does the block comment terminate at the first closing delimiter, can nested
   openers appear safely, or does the language support true nesting / depth-
   qualified forms

## Phase 2: Implementation Cross-Check

If the docs are incomplete or ambiguous, inspect an implementation source:

- official lexer or tokenizer
- grammar or parser rules
- syntax definition from a language-maintained tool

Record the implementation source even when the docs were sufficient. A cross-
check materially raises confidence.

## Phase 3: Search-Engine Community Fallback

If official docs or implementation sources still leave uncertainty, use a
search engine with the language name plus `programming language` and `comment`
to find community explanations.

Target source types:

- Stack Overflow questions and accepted answers
- official issue trackers or language RFC discussions
- blog posts from language maintainers or well-known ecosystem authors
- tutorial pages that show real code examples with comments

Recommended query patterns:

- `<Language> programming language comment`
- `<Language> programming language comments`
- `<Language> programming language block comment`
- `<Language> programming language nested comment`
- `site:stackoverflow.com <Language> programming language comment`
- `site:stackoverflow.com <Language> programming language block comment`
- `site:stackoverflow.com <Language> programming language nested comment`

Rules for using community sources:

- Treat them as corroborating evidence, not as the strongest source.
- Prefer answers with concrete code examples over vague prose.
- Prefer sources that mention the exact language and not a similarly named
  tool or framework.
- Do not conclude that nesting is supported from a blog post unless an
  implementation, grammar, or multiple independent sources support it.
- If community sources contradict official docs, prefer official docs and
  note the contradiction.

## Phase 4: Corpus Fallback

If docs and implementation sources still do not resolve the syntax, download
real files for that language and inspect them directly.

Use this procedure:

1. Find 3 to 5 representative public repositories or official example repos.
2. Download raw source files for the language's common file extension.
3. Inspect multiple files, not just one.
4. Search for likely comment tokens such as:
   `//`, `#`, `--`, `;`, `%`, `!`, `/* */`, `(* *)`, `{- -}`, `<!-- -->`.
5. Look for repeated patterns with surrounding code context.
6. Only infer syntax from corpus when at least two independent files support
   the same interpretation.

Do not infer nested-comment support from a single file unless an implementation
or doc source confirms it.
Do not infer unusual termination behavior from a single file unless an
implementation or doc source confirms it.

## Confidence Rubric

Use one of these values:

- `verified`: official docs plus implementation cross-check
- `cross-checked`: implementation plus corpus or grammar corroboration
- `high`: clear official docs or multiple strong implementation sources
- `medium`: partial evidence, likely correct, still needs confirmation
- `candidate`: plausible corpus-backed inference, not yet strong enough
- `low`: weak evidence, ambiguous, or conflicting sources
- `unresolved`: no defensible syntax found

## Evidence Mode

Set one of these in the report:

- `official_docs`
- `implementation_cross_checked`
- `corpus_inferred`
- `unresolved`

## Stop Conditions

Mark the language unresolved when:

- official docs do not expose comment syntax
- implementation sources are missing or contradictory
- corpus files do not show stable comment forms
- the format is not meaningfully source code and may be commentless

Never guess to fill the table.

## Output Requirements

Every language section must include:

- line comments
- block comments
- termination behavior
- nested comments
- confidence
- evidence mode
- docs source
- implementation source
- community source when used
- corpus fallback source when used
- recommended action
- notes
- real example code for each supported comment form

If a comment form is unsupported, say `unsupported`. If it is unknown, say
`unresolved`.
For termination behavior, use concise values such as:

- `first closing delimiter wins`
- `true nesting supported`
- `depth-qualified delimiters`
- `unsupported`
- `unresolved`
