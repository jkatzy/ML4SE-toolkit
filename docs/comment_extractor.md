# Comment Extractor

The comment extractor turns source text into `QueryMatch(prefix, suffix, match)`
records that can be fed into downstream generation utilities such as
`FIMInput`, `CausalInput`, and `MultiTokenInput`.

## Default entry point

Use `CommentQuery(language)` unless you specifically need only non-nested or
only nested block matching.

```python
from ml4setk import CommentQuery

sample = """\
def classify(x):
    # keep this branch for ablations
    return x > 0
"""

query = CommentQuery("python")

print(query.contains(sample))
match = query.parse(sample)[0]
print(match.prefix)
print(match.match)
print(match.suffix)
```

`contains(text)` returns `True` when the configured language can find at least
one supported comment.

`parse(text)` returns a list of `QueryMatch` objects:

- `prefix`: text before the extracted comment
- `match`: the extracted comment itself
- `suffix`: text after the extracted comment

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

## Which query to use

- `CommentQuery(language_or_languages)`: the default. Combines regex-based
  comments with nested-block comments and returns matches in source order. When
  you pass a list of languages, it returns the union of unique comment matches
  across those parsers.
- `OpeningCommentQuery(language, max_start_row=3)`: extracts one logical
  opening comment block from the top of a file. It skips an initial hashbang
  line, requires the first real comment to start within the first `n` rows, and
  then expands across contiguous top-of-file comments until code appears.
- `LineCommentQuery(language)`: finds line comments and non-nested block
  comments driven by registry regexes or a named contextual extractor.
- `NestedCommentQuery(language)`: finds top-level nested comment regions for
  languages with recursive delimiters such as Haskell, Agda, Racket, or Nim.

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

### Deterministic Unicode fuzzing

Run the property fuzzer across every registry key after changing shared query
or sanitizer behavior:

```bash
make comment-fuzz
```

The default campaign uses a stable seed and exercises delimiter-heavy text,
multiple writing systems, combining marks, bidi controls, Unicode whitespace,
line-separator variants, emoji, NULs, and lone surrogates. Override
`COMMENT_FUZZ_SEED`, `COMMENT_FUZZ_CASES_PER_LANGUAGE`, or
`COMMENT_FUZZ_MAX_LENGTH` to broaden or reproduce a campaign.

This is a contract fuzzer: it validates match bounds, source reconstruction,
ordering, `parse`/iteration/`contains` consistency, and sanitizer totality. It is
not a language-semantics oracle, so retain focused fixtures and differential
tests for syntax and sanitizer normalization behavior.

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

As of this revision, the comment extractor implements `671` language keys.
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

### Legacy tuple API

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
extractor output can be used directly.

## Sanitizing extracted comments

If you need the comment text without the surrounding syntax, use
`CommentSanitizer(language)` or the convenience helper
`sanitize_comment_text(language, comment)`.

```python
from ml4setk import CommentQuery, CommentSanitizer

sample = "value = 1 // keep the legacy path\nreturn value"
match = CommentQuery("java").parse(sample)[0]

text = CommentSanitizer("java").sanitize(match)
assert text == "keep the legacy path"
```

Grouped line comments are sanitized line-by-line:

```python
from ml4setk import sanitize_comment_text

comment = "// first line\n// second line"
assert sanitize_comment_text("java", comment) == "first line\nsecond line"
```

Block comments keep their inner text and drop only the outer syntax:

```python
comment = "/**\n * first line\n * second line\n */"
assert sanitize_comment_text("java", comment) == "first line\nsecond line"
```

## Testing comment behavior

For normal deterministic coverage, run:

```bash
make test
make comment-fuzz
```

Cleaning has one committed JSON oracle for each of the 191 comment syntax
families under `tests/fixtures/comment_cleaning`. The fixture tests apply those
505 explicit raw-to-cleaned cases to all 671 supported language keys. Expected
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
The executable scripts remain versioned with the release so every promoted
regression can be reproduced without keeping raw judge or corpus artifacts on
`main`.

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
