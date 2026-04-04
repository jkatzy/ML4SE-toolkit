# Comment Extractor

The comment extractor turns source text into `QueryMatch(prefix, suffix, match)`
records that can be fed into downstream generation utilities such as
`FIMInput`, `CausalInput`, and `MultiTokenInput`.

## Default entry point

Use `CommentQuery(language)` unless you specifically need only regex-based
matching or only nested block matching.

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
  comments driven by registry regexes.
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

As of this revision, the comment extractor implements `333` language keys.
That includes mainstream source languages plus template, markup, config, and
record-oriented syntaxes such as `astro`, `coldfusion`, `g_code`, `gams`,
`genero`, `jsp`, `marko`, `openqasm`, `plantuml`, `q`, `rexx`, `slim`,
`smarty`, `tla`, and `v`.

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
extractor output can be used directly.

## Current limitations

- Regex-based parsing is not fully lexical. Comment-like text inside strings or
  unusual language constructs can still match.
- Only comment forms represented in
  `src/ml4setk/Parsing/Comments/registry.py` are supported.
- Nested parsing is delimiter-based. It is accurate for supported delimiter
  pairs, but it is not a full parser for the host language grammar.

## Extending support

To add a language, update the registry instead of editing branching logic:

1. Add or extend a `CommentSyntax` family in
   `src/ml4setk/Parsing/Comments/registry.py`.
2. Include seeded examples so the generated tests cover the new behavior.
3. Record research evidence under `docs/comment_research/` and promote the
   result into the registry once it is ready.
