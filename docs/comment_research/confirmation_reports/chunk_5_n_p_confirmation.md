# Chunk 5 N-P Implementation Confirmation

## NL

- Registry key: `nl`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_5_n_p_report.md`
- Current hypothesis: GitHub Linguist `NL` is an unresolved `.nl` data label with line, block, termination, and nesting all marked unsupported.
- Implementation artifact: AMPL Solver Library from `https://github.com/ampl/asl`; Linguist metadata and samples from `https://github.com/github-linguist/linguist`.
- Implementation version: ASL commit `3d477ba78a3392b8b7b05a2fd843ae7f9df70252`, `ASLdate_ASL = 20250727`; Linguist commit `1d7ac7ed569bd6edef5d0cfc73feea2573cb0e03`.
- Local scratch path: `tmp/comment_research_confirmation/chunk_5_n_p/nl/`
- Designated hello-world source: `tmp/comment_research_confirmation/chunk_5_n_p/nl/asl/src/examples/diet.nl`, listed by ASL `src/examples/README` as the Diet problem example generated from AMPL.
- Parser command: `tmp/comment_research_confirmation/chunk_5_n_p/nl/asl/src/examples/nlcopy -g <probe-stub> tmp/comment_research_confirmation/chunk_5_n_p/nl/out/<probe>_copy`
- Confirmation verdict: `contradicted`
- Recommended report update: Identify `NL` as AMPL `.nl` rather than an unresolved data label. Record that ASL accepts trailing `#` record annotations but rejects standalone comment-only lines and C-style block probes; do not implement it as an unrestricted ordinary line comment without a parser-aware restriction.
- Blockers: `cmake` was unavailable, so ASL was built with bundled Unix makefiles: `make -C .../asl/src/solvers -f makefile.u amplsolver.a` and `make -C .../asl/src/examples -f makefile.u S=../solvers nlcopy`.
- Notes: Linguist's `NL` entry is `type: data`, extension `.nl`, `tm_scope: none`, but both Linguist samples and ASL examples contain trailing `#` annotations.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_5_n_p/nl/probes/diet_trailing_hash.nl` | accepted for trailing `#` annotations | accepted | `nlcopy -g .../diet_trailing_hash .../diet_trailing_hash_copy` exited 0; see `tmp/comment_research_confirmation/chunk_5_n_p/nl/probe_results.log`. |
| standalone line comment | `tmp/comment_research_confirmation/chunk_5_n_p/nl/probes/diet_standalone_hash.nl` | rejected | rejected | `nlcopy -g .../diet_standalone_hash .../diet_standalone_hash_copy` printed `jacdim: got M = 0, N = 0, NO = 0` and exited 1. |
| block comment | `tmp/comment_research_confirmation/chunk_5_n_p/nl/probes/diet_block_probe.nl` | rejected | rejected | `nlcopy -g .../diet_block_probe .../diet_block_probe_copy` printed `jacdim: got M = 0, N = 0, NO = 0` and exited 1. |
| nested comment | `tmp/comment_research_confirmation/chunk_5_n_p/nl/probes/diet_nested_block_probe.nl` | rejected | rejected | `nlcopy -g .../diet_nested_block_probe .../diet_nested_block_probe_copy` printed `jacdim: got M = 0, N = 0, NO = 0` and exited 1. |
| unsupported form | `tmp/comment_research_confirmation/chunk_5_n_p/nl/probes/diet_standalone_slashslash.nl` | rejected | rejected | `nlcopy -g .../diet_standalone_slashslash .../diet_standalone_slashslash_copy` printed `jacdim: got M = 0, N = 0, NO = 0` and exited 1. |

### Confirmed Examples

#### Line comment
```text
g3 0 1 0	# problem diet CONFIRM_TRAILING_HASH_COMMENT
 8 4 1 4 0	# vars, constraints, objectives, ranges, eqns
C0	# CONFIRM_RECORD_HASH_COMMENT
n0
```

#### Block comment
```text
unsupported; `/* CONFIRM_BLOCK_COMMENT */` before the NL header was rejected by ASL.
```

#### Nested comment
```text
unsupported; `/* CONFIRM_NESTED_BLOCK_COMMENT outer /* inner */ outer */` before the NL header was rejected by ASL.
```

## ObjDump

- Registry key: `objdump`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_5_n_p_report.md`
- Current hypothesis: GitHub Linguist `ObjDump` is a data/disassembly-output label with no stable source-language version; line, block, termination, and nesting are unsupported.
- Implementation artifact: GNU Binutils source from `https://sourceware.org/git/binutils-gdb.git`; Linguist metadata from `https://github.com/github-linguist/linguist`.
- Implementation version: Binutils-gdb commit `d62f64e17b33fb76653fa0c008c61b782d07f8ec`; local GNU objdump command was GNU Binutils for Ubuntu `2.42`; Linguist commit `1d7ac7ed569bd6edef5d0cfc73feea2573cb0e03`.
- Local scratch path: `tmp/comment_research_confirmation/chunk_5_n_p/objdump/`
- Designated hello-world source: No ObjDump hello-world or parser fixture was present in Linguist samples. Closest official binutils fixture used for generated output was `tmp/comment_research_confirmation/chunk_5_n_p/objdump/binutils-gdb/binutils/testsuite/binutils-all/x86-64/comments.s`.
- Parser command: No parse/tokenize command exists for `.objdump` text in GNU objdump. The attempted command was `objdump -d tmp/comment_research_confirmation/chunk_5_n_p/objdump/probes/comments_with_probes.objdump`.
- Confirmation verdict: `blocked`
- Recommended report update: Keep ObjDump unsupported and add that implementation confirmation was blocked because GNU objdump generates disassembly from object files and does not parse `.objdump` text as a language. Disassembler-emitted `#` annotation text is output decoration, not a lexical comment grammar for input files.
- Blockers: GNU objdump rejected the probed `.objdump` text as `file format not recognized`; Linguist has no `samples/ObjDump` directory.
- Notes: Binutils `objdump.c` describes remaining command arguments as object files processed by BFD, and disassembly text is produced by libopcodes. This supports treating ObjDump as generated output, not a source language with comments.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_5_n_p/objdump/probes/comments_with_probes.objdump` | not tested | blocked | `objdump -d .../comments_with_probes.objdump` exited 1 with `file format not recognized`; see `tmp/comment_research_confirmation/chunk_5_n_p/objdump/probe_results.log`. |
| block comment | `tmp/comment_research_confirmation/chunk_5_n_p/objdump/probes/comments_with_probes.objdump` | not tested | blocked | Same command; no `.objdump` parser/tokenizer was available. |
| nested comment | `tmp/comment_research_confirmation/chunk_5_n_p/objdump/probes/comments_with_probes.objdump` | not tested | blocked | Same command; no `.objdump` parser/tokenizer was available. |
| unsupported form | `tmp/comment_research_confirmation/chunk_5_n_p/objdump/probes/comments_with_probes.objdump` | not tested | blocked | Same command; no `.objdump` parser/tokenizer was available. |

### Confirmed Examples

#### Line comment
```text
unsupported; no parse-capable ObjDump input implementation was found.
```

#### Block comment
```text
unsupported; no parse-capable ObjDump input implementation was found.
```

#### Nested comment
```text
unsupported; no parse-capable ObjDump input implementation was found.
```
