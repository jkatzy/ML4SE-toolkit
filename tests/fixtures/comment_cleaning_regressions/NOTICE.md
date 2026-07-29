# Comment-cleaning regression fixture provenance

These fixtures were generated from comment candidates sampled from
`bigcode/the-stack-v2-dedup`. Its source content is archived by Software Heritage.
The manifest pins the frozen run, candidate set, and reviewed oracle inputs by
SHA-256.

Every case stores the 40-hex Stack v2 source ID and the SHA-256 of its source
excerpt selected from the pinned source manifest.
Executable sanitizer cases keep exact raw and expected comment text. Invalid
extraction cases retain the original raw SHA-256 and UTF-8 byte length but use
small synthetic structural probes instead of source-sized overcaptures.
Accounting-only cases retain hashes and dispositions without raw literals.
Repository names, paths, surrounding source, and judge/reviewer prose are
intentionally omitted.

The frozen run did not include exact per-file license metadata. Treat retained
literals as test-only excerpts and consult the underlying Stack v2/Software
Heritage record before reuse outside regression testing.
