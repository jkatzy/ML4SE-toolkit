# Deterministic Comment Fuzzing

`scripts/fuzz_comment_parsers.py` runs Unicode-heavy property campaigns over
all supported registry keys. Its random streams are stable per language and
campaign, so adding or reordering languages does not shift an existing
language's cases.

## Campaigns

Run both parser and sanitizer contracts with the repository defaults:

```bash
make comment-fuzz
```

Run only sanitizer contracts, including structured mutations of registered
examples and wrappers:

```bash
make comment-cleaner-fuzz
```

The Make defaults are seed `0xC0FFEE`, 100 random cases per language, maximum
length 128, and four sanitizer payloads per registered example. Override them
explicitly for a larger recorded campaign:

```bash
make comment-fuzz \
  COMMENT_FUZZ_SEED=0x5EED2026 \
  COMMENT_FUZZ_CASES_PER_LANGUAGE=1000 \
  COMMENT_FUZZ_MAX_LENGTH=512 \
  COMMENT_FUZZ_SANITIZER_PAYLOADS_PER_EXAMPLE=12
```

For a focused reproduction or one campaign, call the runner directly:

```bash
uv run python scripts/fuzz_comment_parsers.py \
  --campaign parser \
  --languages python,java \
  --seed 0x5EED2026 \
  --cases-per-language 1000 \
  --max-length 512
```

## Checked properties

The parser campaign checks API parity, range bounds and ordering, exact source
slices, prefix/suffix correctness, source reconstruction, and agreement between
`contains`, `parse`, `parse_ranges`, and `iter_ranges`.

The sanitizer campaign checks deterministic output, public API parity, newline
normalization, non-expansion, raw-mode behavior, and exact expected output for
structured mutations of registry examples, nested wrappers, unclosed wrappers,
and CR/LF variants.

These are structural and metamorphic contracts. They cannot prove that a
delimiter is valid for a language or that arbitrary cleaned prose is
semantically correct. Research and exact fixtures provide those oracles.

## Reproduction and reduction

The runner prints each failure as JSON with `campaign`, `language`,
`language_seed`, `case_index`, `mutation`, `text_repr`, `invariant`, and detail,
then prints a summary. Preserve the invocation and failure row under an ignored
`tmp/` investigation directory.

1. Rerun with the same top-level seed, campaign, language list, case count, and
   maximum length.
2. Confirm the same `language_seed`, `case_index`, and invariant.
3. Reduce the decoded input or structured mutation manually to a readable
   deterministic case.
4. Add that case to the appropriate test or fixture before changing code.
5. Rerun the original seed after the fix to detect related failures.

Do not commit raw fuzz logs. The minimized regression is the durable record.

## Seed policy

- CI and routine local checks use the fixed default seed.
- A pull request may add recorded fixed seeds for broader campaigns.
- Never report an unrecorded random campaign as reproducible evidence.
- Treat every unique failing input as a failure requiring a disposition.
- Equivalent failures may share one parameterized regression only when all
  source case IDs or failure hashes are enumerated in its provenance.

See [regression tests](regressions.md) for placement and
[failure dispositions](failure_dispositions.md) for closure rules.
