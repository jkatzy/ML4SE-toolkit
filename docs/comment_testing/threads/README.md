# Comment Testing Threads

This directory stores the live handoff files for the adversarial comment
testing workflow.

- `*_findings.md` files are breaker-owned
- `*_resolution.md` files are fixer-owned

These files are generated if missing by `make comment-test-prompts`, but the
generator does not overwrite existing thread content.
