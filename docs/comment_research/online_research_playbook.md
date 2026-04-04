# Online Comment Research Playbook

This playbook defines the stronger research workflow for comment-syntax
discovery. The goal is to replace "best guess" entries with evidence-backed
entries that can safely drive registry updates and generated tests.

## Mission

For each assigned language:

1. Find the language's comment syntax from official documentation whenever
   possible.
2. Check multiple sources, not just one page. Whenever possible, confirm the
   syntax with at least two independent sources, one of which is official
   documentation or implementation.
3. Explicitly look for version-specific or dialect-specific differences in the
   language's comment syntax and record them.
4. Cross-check it against an implementation source such as a lexer, parser,
   grammar, or syntax highlighter when available.
5. If documentation or implementation sources are missing, vague, or
   contradictory, use a search engine to find secondary sources such as
   Stack Overflow answers, blog posts, tutorials, or issue threads that may
   explain the language's comment rules in practice.
6. If secondary sources still do not resolve the syntax, download real source
   files for that language and inspect them for likely comment forms.
7. Produce documentation-oriented output with evidence, confidence, version
   scope, and real
   code snippets that can later be turned into parser fixtures and tests.

## Evidence Ladder

Use this order of preference:

1. Official language spec, manual, or reference documentation.
2. Official documentation for more than one version, release stream, or
   dialect when versioned docs exist.
3. Official implementation source:
   compiler, interpreter, lexer, parser, grammar, or reference tooling.
4. Search-engine-discovered community explanations:
   Stack Overflow, well-cited blog posts, tutorial pages, issue discussions,
   or language-community Q&A that directly address comment syntax.
5. Widely used grammar implementations:
   Tree-sitter, ANTLR, GitHub Linguist, editor grammars, or parser repos.
6. Corpus fallback:
   downloaded source files from real public repositories or official example
   repositories for that language.

Do not skip directly to corpus inference if an official or community source is
available.
Do not stop after a single source if the language has visible versioning,
archived manuals, dialects, or conflicting syntax references.

## Phase 1: Docs-First Search

Start with targeted web queries such as:

- `<Language> programming language comments syntax`
- `<Language> programming language comment`
- `<Language> programming language reference comments`
- `<Language> programming language lexical grammar comments`
- `<Language> programming language line comment block comment`
- `<Language> programming language legacy comment syntax`
- `<Language> programming language old version comments`
- `<Language> programming language comment syntax version`
- `site:stackoverflow.com <Language> programming language comment`
- `site:stackoverflow.com <Language> programming language block comment`
- `site:stackoverflow.com <Language> programming language nested comments`
- `<Language> programming language comment tutorial`
- `<Language> programming language comment blog`

When the language has a known project or foundation site, prefer that domain.
When the docs are versioned, capture the exact URL you used.
When the language has multiple language editions, standards, or major versions,
inspect at least the latest documentation plus one older or alternate version
source when available.

You are looking for:

- line comment markers
- block comment delimiters
- how block comments terminate
- whether nested comments are supported
- whether there are depth-qualified or escape-like delimiter variants
- any dialect restrictions
- whether the syntax changed between versions
- whether comment syntax is context-sensitive

For every language, explicitly classify:

1. line comments, including version-specific variants
2. block comments, including version-specific variants
3. delimiter behavior per version:
   does the block comment terminate at the first closing delimiter, can nested
   openers appear safely, or does the language support true nesting / depth-
   qualified forms
4. whether the registry should implement the union of all confirmed version
   forms or whether the differences are dialect-level and should be split

## Phase 2: Implementation Cross-Check

If the docs are incomplete or ambiguous, inspect an implementation source:

- official lexer or tokenizer
- grammar or parser rules
- syntax definition from a language-maintained tool

Record the implementation source even when the docs were sufficient. A cross-
check materially raises confidence.
When the syntax appears version-dependent, prefer implementations or grammars
from more than one tagged release or versioned branch if available.

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
- `<Language> programming language legacy comment syntax`
- `<Language> programming language older version comment syntax`
- `<Language> programming language version comment syntax`
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
7. When possible, sample files that appear to come from different eras,
   versions, or official example repositories so historical syntax differences
   are visible.

Do not infer nested-comment support from a single file unless an implementation
or doc source confirms it.
Do not infer unusual termination behavior from a single file unless an
implementation or doc source confirms it.

## Confidence Rubric

Use one of these values:

- `verified`: official docs across versions plus implementation cross-check
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

- version scope
- version-specific syntax summary
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

Minimum evidence target:

- at least two independent sources for each supported syntax when possible
- at least one official or implementation source
- for versioned languages, at least two version-aware sources or one current
  source plus one older/alternate version source when available

If a comment form is unsupported, say `unsupported`. If it is unknown, say
`unresolved`.
For termination behavior, use concise values such as:

- `first closing delimiter wins`
- `true nesting supported`
- `depth-qualified delimiters`
- `unsupported`
- `unresolved`

For version-specific syntax, use concise summaries such as:

- `current and legacy agree`
- `older versions only support line comments; newer versions add block comments`
- `v1 uses --, v2 adds //`
- `dialect split; do not union`
