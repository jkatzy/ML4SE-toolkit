# Comment Testing Threads

This directory stores the live handoff files for the adversarial comment
testing workflow.

- `*_findings.md` files are breaker-owned
- `*_resolution.md` files are fixer-owned

Breaker agents may also edit their assigned language files under
`tests/fixtures/comment_languages/`. Those fixture additions must be cases that
the current parser is expected to parse correctly. If a candidate exposes a
current parser failure, record it in the findings thread instead of leaving a
failing fixture edit behind.

When a finding is sanitizer-focused, record both the raw extracted match and
the sanitized output, plus a short note about what should be removed as syntax
noise and what must be preserved as meaningful content.

Record reviewed coverage even when no issue is found. The goal is to leave a
per-language trail of what was checked, not only a shortlist of the most
interesting failures.

After fixture edits, run
`uv run pytest tests/test_comment_language_fixtures.py -q --no-cov` and record
the command result in the relevant findings or resolution entry.

These files are generated if missing by `make comment-test-prompts`, but the
generator does not overwrite existing thread content.
