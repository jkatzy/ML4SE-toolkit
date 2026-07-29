# Comment-cleaning corpus fixture provenance

The repaired, manual-adjudication, policy-oracle, final-validation, and family
regression fixtures under this directory derive from comment candidates sampled from
`bigcode/the-stack-v2-dedup`. The source content is archived by Software Heritage.

Executable cases retain only the raw and expected comment text needed for a
regression. Accounting-only cases retain hashes, UTF-8 byte lengths, and
dispositions without reconstructing source literals. The repaired fixture index
records the available 40-hex source identifier, source-excerpt SHA-256, and
source-record SHA-256. Every family regression case records its 40-hex source
identifier and source-excerpt SHA-256 from the same hash-pinned manifest.
Repository names, paths, surrounding source context, and judge/reviewer prose
are intentionally omitted.

The frozen inputs did not include exact per-file license metadata. Treat retained
literals as test-only excerpts and consult the recorded Stack v2/Software
Heritage source before reuse outside regression testing.

Final-validation cases record a 40-hex source identifier and source-excerpt
SHA-256 from the exact, hash-pinned all-language source manifest; they do not
commit repository names, paths, surrounding context, or full source text.
