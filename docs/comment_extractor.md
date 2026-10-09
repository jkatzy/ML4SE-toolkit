# Comment Extraction and Cleaning

ML4SE-toolkit pulls comments out of source files in two stages:

1. **Extraction** finds where each comment is. A query such as
   `CommentQuery("java")` scans source text and returns one
   `QueryMatch(prefix, suffix, match)` per comment, where `match` is the raw
   comment exactly as written, and `prefix` and `suffix` are the source text
   before and after it.
2. **Cleaning** turns one raw comment into its content. `CommentSanitizer`
   removes the comment syntax (`//`, `/* */`, `#`, a ` * ` gutter, and so on)
   and keeps the words, code, and layout a reader needs.

Both stages read the same per-language registry, so a language key that works
for one works for the other. The input formatters take a `QueryMatch`
directly, so extracted comments can become model inputs without conversion
(see [Input formatting](input_formatting.md)).

## Quick start

Install the package (`pip install ml4setk`), then run:

```python
from ml4setk import CommentQuery, CommentSanitizer

source = '''\
/*
 * Copyright 2026 Example Corp.
 */
package demo;

public class Greeter {
    /**
     * Builds a greeting.
     *
     * @param name who to greet
     */
    public String greet(String name) {
        // Keep the URL below intact:
        // it is a string, not a comment.
        String url = "https://example.com"; // inline note
        return "Hello, " + name;
    }
}
'''

query = CommentQuery("java")
cleaner = CommentSanitizer("java")

for match in query.parse(source):
    line = match.prefix.count("\n") + 1
    print(f"line {line}: {match.match!r}")
    print(f"  cleaned: {cleaner.sanitize(match)!r}")
```

Output:

```text
line 1: '/*\n * Copyright 2026 Example Corp.\n */'
  cleaned: 'Copyright 2026 Example Corp.'
line 7: '/**\n     * Builds a greeting.\n     *\n     * @param name who to greet\n     */'
  cleaned: 'Builds a greeting.\n\n@param name who to greet'
line 13: '// Keep the URL below intact:\n        // it is a string, not a comment.'
  cleaned: 'Keep the URL below intact:\nit is a string, not a comment.'
line 15: '// inline note'
  cleaned: 'inline note'
```

The example shows the main behaviors:

- The `//` inside `"https://example.com"` is not reported, because it starts
  inside a string.
- The two consecutive `//` lines come back as one match, and cleaning removes
  the marker from each line.
- The inline `// inline note` stays a separate match; it is never grouped with
  the comment lines above it.
- Cleaning the Javadoc block drops the `/** */` delimiters and the ` * `
  gutter but keeps the blank line and the `@param` tag.
- `match.prefix` holds everything before the comment, so its newline count
  gives the line number.

## How it works

### Extraction

Every language key resolves to a `CommentSyntax` entry in
`src/ml4setk/Parsing/Comments/registry.py`. An entry lists the language's
line and block comment regexes, its nesting delimiter pairs, prefixes that look
like comments but are not (such as MySQL `/*!` hints in SQL), and seeded examples
that the test suite runs. Many languages share one syntax family; `java`,
`c`, and `javascript`, for example, are aliases of the same C-style family.
Adding or correcting a language normally means changing registry data; parser
code holds only the scanners that delimiters alone cannot express.

For each language, `CommentQuery.parse(text)` then:

1. **Marks protected ranges.** It finds string literals (and, for some
   languages, other literals such as raw strings or IRIs) in one left-to-right
   pass that skips over complete comments. A comment candidate that starts
   inside a protected range is rejected.
2. **Runs the line and block scanner** (`LineCommentQuery`). Every registry
   regex is applied to the text. For formats whose comments depend on file
   structure rather than a delimiter, a named contextual extractor supplies
   the ranges instead. When two candidates start at the same offset, the
   longest wins, and a candidate that starts inside an earlier match is
   dropped, so a `//` inside a `/* */` block is not reported twice.
3. **Runs the nested scanner** (`NestedCommentQuery`). For languages with
   recursive delimiters such as Haskell's `{- -}`, it counts opening and
   closing delimiters and reports each complete top-level region once, with
   inner comments included. Unclosed regions are ignored.
4. **Groups adjacent line comments.** Line comments that each occupy a whole
   line, use the same marker, and are separated by exactly one line break
   become one match. A comment that shares its line with code is never
   grouped.
5. **Returns matches in source order** as `QueryMatch` values.

When you pass several languages, steps 1 to 4 run once per language and the
results are merged, keeping one copy of each identical source range.

`OpeningCommentQuery` reuses the same scanners but keeps only the first
comment block of a file, and only when nothing but white space (and an
optional `#!` line) comes before it. A leading UTF-8 byte order mark is
ignored, a `#![` line is a Rust-style inner attribute rather than a hashbang,
and the `\r` of a CRLF line ending is never part of the match.

Some languages changed their comment syntax between releases. Those carry a
version table, and every query and the sanitizer take a `version` argument;
see [Language versions](#language-versions).

### Cleaning

`CommentSanitizer(language)` builds the list of comment wrappers for the
language from the same registry entry: line openers such as `//` or `#`,
block delimiter pairs, and documentation variants such as `///` or `/**`.
`sanitize(comment)` accepts a raw string or a `QueryMatch` and:

1. Normalizes line endings to `\n`.
2. Removes the outer delimiters of a block comment, or the line marker from
   each line of a grouped line comment.
3. Removes a gutter that every line shares, such as the ` * ` column of a
   Javadoc block, and decorative rulers or box frames made of one repeated
   character.
4. Removes the shared indentation and one padding space after the opener and
   before the closer, while keeping indentation relative to the comment body.

Cleaning decisions depend on the comment's layout and the language syntax,
never on the words in the comment, and uncertain cases keep text rather than
drop it. Comments that start with an excluded directive prefix are returned
unchanged. The full contract, with examples of what is removed and what is
kept, is in the [comment cleaning policy](comment_cleaning_policy.md).

## API reference

All names below are importable from `ml4setk`.

| API | Returns | Use it for |
| --- | --- | --- |
| `CommentQuery(language, version=None)` | query object | The default extractor. `language` is one key or a list of keys. |
| `OpeningCommentQuery(language, max_start_row=3, skip_hashbang=True, version=None)` | query object | The file header comment only. |
| `LineCommentQuery(language, version=None)` | query object | Line comments and non-nested block comments only, without grouping. |
| `NestedCommentQuery(language, version=None)` | query object | Nested block comments only. |
| `query.parse(text)` | `list[QueryMatch]` | All matches in source order. |
| `query.contains(text)` | `bool` | A quick check that at least one comment exists. |
| `QueryMatch(prefix, suffix, match)` | named tuple | The shared result type; `prefix + match + suffix` is the original text. |
| `CommentSanitizer(language, version=None)` | sanitizer object | Reusable cleaner for one language; call `.sanitize(comment)`. |
| `sanitize_comment(language, comment, version=None)` | `str` | One-off cleaning. `sanitize_comment_text` is an alias. |
| `get_supported_comment_languages()` | `list[str]` | Every registry key. |
| `comment_language_requires_version(language)` | `bool` | Whether a language has a version table. |
| `get_comment_language_versions(language)` | `tuple[str, ...]` | Its supported versions, oldest first. |
| `get_default_comment_language_version(language)` | `str` | The version used when none is given. |

Errors:

- An unknown language key raises `NotImplementedError` when the query or
  sanitizer is constructed.
- An unknown version raises `UnsupportedCommentLanguageVersionError`.
- Omitting the version of a versioned language emits one
  `CommentLanguageVersionWarning` per language and process.

Build a query or sanitizer once and reuse it across files: construction
compiles the language's patterns.

## Using the extractor

`contains(text)` returns `True` when the configured language can find at least
one supported comment.

`parse(text)` returns a list of `QueryMatch` objects:

- `prefix`: text before the extracted comment
- `match`: the extracted comment itself
- `suffix`: text after the extracted comment

```python
from ml4setk import CommentQuery

sample = """\
def classify(x):
    # keep this branch for ablations
    return x > 0
"""

query = CommentQuery("python")

assert query.contains(sample)
match = query.parse(sample)[0]
assert match.match == "# keep this branch for ablations"
```

If the language is uncertain, `CommentQuery` also accepts a list of language
keys and returns the union of unique matches from all of them:

```python
from ml4setk import CommentQuery

sample = "value = 1 # note\n/* block */\nreturn value\n"
query = CommentQuery(["python", "java"])

matches = query.parse(sample)
assert [match.match for match in matches] == ["# note", "/* block */"]
```

Only identical source ranges are deduplicated. Ambiguous multi-language queries
can return overlapping matches, which callers that need a non-overlapping token
stream must resolve.

## Language versions

Some languages changed their comment syntax between versions. CMake before 3.0,
for example, treats `#[[ note ]] set(x 1)` as one line comment, while CMake 3.0
and later read a bracket comment followed by code. Such languages carry a
version table, and every query accepts a `version` keyword:

```python
from ml4setk import CommentQuery, comment_language_requires_version

assert comment_language_requires_version("cmake")

source = "#[[ note ]] set(x 1)\n"
assert [m.match for m in CommentQuery("cmake", version="2.8").parse(source)] == [
    "#[[ note ]] set(x 1)"
]
assert [m.match for m in CommentQuery("cmake", version="3.0").parse(source)] == [
    "#[[ note ]]"
]
```

- A version may be given by its name, one of its aliases, or (for languages
  versioned by release number) any dotted release: `version="3.18"` selects
  the range that starts at 3.0. Lookup ignores case and a leading `v`.
- Without a version, a versioned language uses its default version and emits
  one `CommentLanguageVersionWarning` per language and process. The message
  names the assumed default and every supported version. Pass the version
  explicitly, or filter the warning, to silence it.
- An unknown version raises `UnsupportedCommentLanguageVersionError`, whose
  message and `supported_versions` attribute list the language's versions.
  Passing a version for a language whose comments do not depend on its version
  raises the same error. The error subclasses both `NotImplementedError` and
  `ValueError`.
- `CommentQuery([...])` over several languages takes a mapping, for example
  `version={"c": "c89"}`; unmapped languages use their defaults.
- `get_comment_syntax(language, version)`, `CommentSanitizer(language,
  version=...)`, and `sanitize_comment(language, comment, version=...)`
  resolve versions the same way.

`comment_language_requires_version(language)` is the version flag.
`get_comment_language_versions(language)` lists the supported versions in
chronological order, `get_default_comment_language_version(language)` names
the default, and `VERSIONED_COMMENT_LANGUAGES` lists every flagged language.

<!-- versioned-language-table:start -->
The default version of each language is in bold. Versions are listed oldest first.

| Languages | Versions | What changes |
| --- | --- | --- |
| `c`, `objective-c` | c89, c99, **c23** | `//` comments from C99; trigraph `??/` splices until C23, which also adds `'` digit separators. |
| `c++`, `objective_cpp`, `objective_c_plus_plus`, `cuda` | cpp98, cpp11, cpp14, **cpp17**, cpp23 | Raw strings from C++11, `'` digit separators from C++14, no trigraphs from C++17, and white space before a splicing backslash from C++23. |
| `glsl` | **glsl110**, glsl420 | From GLSL 4.20 a trailing backslash continues a `//` comment. |
| `hack` | hhvm4.131, **hhvm4.133** | `#` comments end at HHVM 4.133. |
| `stan` | 2.32, **2.33** | `#` comments end at Stan 2.33. |
| `cmake` | 2.8, **3.0** | Bracket comments `#[[ ]]` and bracket arguments from 3.0. |
| `php` | php7.2, php7.3, **php8.0** | Flexible heredoc closers from 7.3; `#[` is an attribute, not a comment, from 8.0. |
| `html_php`, `html_plus_php` | php7.4, **php8.0** | `#[` is an attribute, not a comment, from PHP 8.0. |
| `vim_script`, `viml` | **legacy**, vim9 | Vim9 script uses `#` comments and `"` strings. |
| `editorconfig` | pre-0.15, **0.15** | Inline `;` and `#` comments end at specification 0.15. |
| `cairo_zero` | 0.9, **0.10** | The comment marker changes from `#` to `//` at cairo-lang 0.10. |
| `macaulay2` | 1.10, 1.11, **1.13** | Block comments change from `{* *}` to `-* *-` (both in 1.11 and 1.12). |
| `julia` | 0.2, **0.3** | Nested `#= =#` block comments from 0.3. |
| `jq` | **1.7**, 1.8 | From 1.8 a trailing backslash continues a comment. |
| `ssh_config` | 8.4, 8.5, **8.7** | Full-line comments only until 8.4; 8.5 and 8.6 cut every line at its first `#`; from 8.7 `#` starts a comment at the start of an argument. |
| `fluent` | 0.4, **1.0** | The comment sigil changes from `//` to `#` at Fluent Syntax 0.5. |
| `org` | 7.8, **8.0** | From 7.9.2 a comment line needs white space after `#` and may be indented. |
| `mcfunction` | 1.20.1, **1.20.2** | From 1.20.2 a trailing backslash continues a comment line. |
| `picolisp` | 2.3.6, 2.3.7, **18.6** | `#{ }#` block comments from 2.3.7; they nest from 18.6. |
| `lua` | 4.0, 5.0, **5.1** | Nesting `--[[ ]]` long comments in 5.0; leveled, non-nesting `--[=[ ]=]` from 5.1. |
| `ocaml` | 4.01, 4.02, **4.11** | Quoted strings `{id\|...\|id}` are lexed inside comments from 4.02, quoted extensions `{%ext\|...\|}` from 4.11. |
| `markdown` | commonmark-0.30, **commonmark-0.31** | Inline HTML comments may contain `--` from CommonMark 0.31. |
| `nushell` | 0.76, 0.77, **0.94** | A mid-word `#` stops starting a comment at 0.77; raw strings `r#'...'#` from 0.94. |
| `caddyfile` | 2.0, **2.1** | From 2.1 `#` starts a comment only at the start of a token. |
| `dotenv` | 13, 14.0, 14.3.2, 15, **16** | Inline comments from Node dotenv 14.0, multi-line quoted values from 15, and backtick quotes from 16. |
| `templ` | 0.2.364, **0.2.408** | `//` and `/* */` inside component bodies are comments from v0.2.408. |
| `mermaid` | 10.0, **10.1** | From 10.1 only own-line `%%` comments are removed; a trailing `%%` after flowchart code is not a comment. |
| `imba` | **imba1**, imba2 | Imba 2 adds `//` and `/* */` comments. |
| `supercollider` | 3.8, **3.9** | Before 3.9 nested comment delimiters overlap, so `*/*/` reopens a comment. |
| `mdx` | mdx1, **mdx2** | MDX 1 has HTML comments; MDX 2 has JavaScript comments in `{...}` expressions. |
<!-- versioned-language-table:end -->

## Behavior that matters

### Adjacent single-line comments are grouped

`CommentQuery` coalesces consecutive standalone line comments into one logical
match when they are separated only by a newline.

```python
from ml4setk import CommentQuery

sample = """\
// first line
// second line
int value = 1;
"""

match = CommentQuery("java").parse(sample)[0]
assert match.match == "// first line\n// second line"
```

This is useful when a training target should preserve a multi-line comment
block instead of splitting it into per-line matches.

### Inline comments are preserved as-is

```python
from ml4setk import CommentQuery

sample = "value = 1 // keep the legacy path\nreturn value"
match = CommentQuery("java").parse(sample)[0]
assert match.match == "// keep the legacy path"
```

### Nested comments are matched at top level

```python
from ml4setk import CommentQuery

sample = "answer = 42 {- outer {- inner -} outer -} done"
match = CommentQuery("haskell").parse(sample)[0]
assert match.match == "{- outer {- inner -} outer -}"
```

### Structural formats can declare comment regions

FIGfont files store their comment count in the header rather than using a
delimiter. The `figlet_font` parser returns exactly the declared physical lines
including blank lines, permits the last declared line to end at EOF, and does
not scan later glyph data for comment-like markers.

```python
from ml4setk import CommentQuery

sample = "flf2a$ 1 1 1 0 1\nfont attribution\n@glyph\n"
match = CommentQuery("figlet_font").parse(sample)[0]
assert match.match == "font attribution"
```

Because FIGfont header comments have no delimiter, sanitization preserves their
content and indentation apart from newline normalization.

### Opening file headers can be extracted directly

```python
from ml4setk import OpeningCommentQuery

sample = """\
#!/usr/bin/env bash
# project header
# another header line

echo hi
"""

match = OpeningCommentQuery("shell").parse(sample)[0]
assert match.match == "# project header\n# another header line"
```

The initial `#!...` line is skipped automatically when `skip_hashbang=True`
which is the default.

If your repository keeps header comments lower in the file, increase the row
limit:

```python
from ml4setk import OpeningCommentQuery

query = OpeningCommentQuery("python", max_start_row=5)
```

## Supported languages

The registry is the source of truth. To inspect the exact current set:

```python
from ml4setk import get_supported_comment_languages

languages = get_supported_comment_languages()

print(len(languages))
print(languages[:10])
```

As of this revision, the comment extractor implements `776` language keys.
That includes mainstream source languages plus template, markup, config, and
record-oriented syntaxes such as `astro`, `coldfusion`, `g_code`, `gams`,
`genero`, `jsp`, `marko`, `openqasm`, `plantuml`, `q`, `rexx`, `slim`,
`smarty`, `tla`, and `v`.

The format-aware keys `checksums`, `ecere_projects`, `figlet_font`,
`microsoft_visual_studio_solution`, `nl`, `omgrofl`, and `pogoscript` have
additional scope constraints:

- `checksums` implements GNU Coreutils check-file comments, not `go.sum`; `#`
  must be in column zero because an indented hash is checksum data.
- `figlet_font` reads the header-declared `Comment_Lines` region.
- `nl` recognizes an end-of-record `#`, not a standalone `#`, protects counted
  raw strings, and scans only a complete 10-line textual header before a binary
  payload.
- `ecere_projects` masks double-quoted ECON values before finding comments.
- `pogoscript` masks quoted strings and `r/.../` literals while leaving comments
  in `#(...)` interpolation code visible.
- `microsoft_visual_studio_solution` accepts Unicode indentation before a
  full-line `#`.
- `omgrofl` recognizes a complete, case-insensitive `w00t` token when it is the
  first Java Scanner token on a physical line, including Java whitespace and
  U+0085, U+2028, and U+2029 line separators; it has no inline form.

Language keys are lowercase registry identifiers such as `java`, `python`,
`qml`, `dockerfile`, `powershell`, `jinja`, and `xquery`.

If a language is not implemented yet, the query raises `NotImplementedError`:

```python
from ml4setk import CommentQuery

try:
    CommentQuery("some_future_language")
except NotImplementedError:
    pass
```

## Feeding matches into generation

```python
from ml4setk import CommentQuery, FIMInput

sample = "prefix\n// explain this branch\nsuffix"
match = CommentQuery("java").parse(sample)[0]

model_input, ground_truth = FIMInput(
    "<fim_prefix>",
    "<fim_suffix>",
    "<fim_middle>",
).generate(match)
```

The generation classes operate on the same `QueryMatch` contract, so the
extractor output can be used directly. See [Input formatting](input_formatting.md)
for the other formats and for picking a model's own tokens.

## Using the sanitizer

If you need the comment text without the surrounding syntax, use
`CommentSanitizer(language)` or the convenience helper
`sanitize_comment(language, comment)`. The
[comment cleaning policy](comment_cleaning_policy.md) defines what cleaning
removes and what it keeps.

```python
from ml4setk import CommentQuery, CommentSanitizer

sample = "value = 1 // keep the legacy path\nreturn value"
match = CommentQuery("java").parse(sample)[0]

text = CommentSanitizer("java").sanitize(match)
assert text == "keep the legacy path"
```

Grouped line comments are sanitized line-by-line:

```python
from ml4setk import sanitize_comment

comment = "// first line\n// second line"
assert sanitize_comment("java", comment) == "first line\nsecond line"
```

Block comments keep their inner text and drop only the outer syntax:

```python
from ml4setk import sanitize_comment

comment = "/**\n * first line\n * second line\n */"
assert sanitize_comment("java", comment) == "first line\nsecond line"
```

## Legacy tuple API

Existing dataset code can continue to use
`ml4setk.Comment_util.parse_comment.extract_comments`. It returns historical
`((start, end), text, kind)` tuples and now accepts registry-only language keys:

```python
from ml4setk.Comment_util.parse_comment import extract_comments

comments = extract_comments("value // note\n", ["jsonc"])
assert comments == [((6, 13), "// note", "line")]
```

Candidate languages are processed independently, so their order and duplicate
matches are preserved; unknown names are ignored. Exact names supported by the
original compatibility table retain their historical behavior, while newer keys
use the registry-backed parser. New code should prefer `CommentQuery` and its
`QueryMatch` contract.

## Testing comment behavior

For normal deterministic coverage, run:

```bash
make test
make comment-fuzz
```

Cleaning has one committed JSON oracle for each of the 271 comment syntax
families under `tests/fixtures/comment_cleaning`. The fixture tests apply those
1,004 explicit raw-to-cleaned cases to all 776 supported language keys, producing
2,400 alias-expanded checks. Expected
cleaned text is derived from registry syntax rather than by calling the
sanitizer under test. Regenerate and verify the files with:

```bash
make comment-cleaner-fixtures
uv run pytest \
  tests/test_comment_cleaning_fixtures.py \
  tests/test_comment_sanitizer.py
```

`make comment-fuzz` runs both parser and sanitizer campaigns and defaults to 100
random cases per registry key, plus structured sanitizer mutations built from
registry examples. Run only the cleaner campaign with:

```bash
make comment-cleaner-fuzz
```

The seed, random input size, and structured payload count are configurable
through `COMMENT_FUZZ_SEED`, `COMMENT_FUZZ_MAX_LENGTH`, and
`COMMENT_FUZZ_SANITIZER_PAYLOADS_PER_EXAMPLE`, so failures are reproducible.

Corpus research, adversarial test generation, fuzz campaigns, and LLM judges
are development operations. Their current commands, evidence rules, and
failure-to-regression workflow live in the
[`dev` branch comment-testing guide](https://github.com/jkatzy/ML4SE-toolkit/tree/dev/docs/comment_testing).
The judge and prompt-packet scripts live on `dev` with that guide. Every
promoted regression lands on `main` as a deterministic test or fixture, so it
can be reproduced without them.

### Deterministic Unicode fuzzing

Run `make comment-fuzz` after changing shared query or sanitizer behavior. The
default campaign uses a stable seed and exercises delimiter-heavy text,
multiple writing systems, combining marks, bidi controls, Unicode whitespace,
line-separator variants, emoji, NULs, and lone surrogates. Override
`COMMENT_FUZZ_SEED`, `COMMENT_FUZZ_CASES_PER_LANGUAGE`, or
`COMMENT_FUZZ_MAX_LENGTH` to broaden or reproduce a campaign.

This is a contract fuzzer: it validates match bounds, source reconstruction,
ordering, `parse`/iteration/`contains` consistency, and sanitizer totality. It is
not a language-semantics oracle, so retain focused fixtures and differential
tests for syntax and sanitizer normalization behavior.

## Current limitations

- Regex-based parsing is not fully lexical. Comment-like text inside strings or
  unusual language constructs can still match.
- Only comment forms represented in
  `src/ml4setk/Parsing/Comments/registry.py` are supported.
- Nested parsing is delimiter-based. It is accurate for supported delimiter
  pairs, but it is not a full parser for the host language grammar.
- Multi-language queries deduplicate only identical ranges and can return
  overlapping matches.

## Extending support

To add a language, update the registry instead of editing branching logic:

1. Add or extend a `CommentSyntax` family in
   `src/ml4setk/Parsing/Comments/registry.py`.
2. Include seeded examples so the generated tests cover the new behavior.
3. Record research evidence using the
   [`dev` branch research workflow](https://github.com/jkatzy/ML4SE-toolkit/tree/dev/docs/comment_research)
   and promote only confirmed behavior into the registry.
4. Run `make comment-fuzz` and add a minimized regression for every confirmed
   failure.
