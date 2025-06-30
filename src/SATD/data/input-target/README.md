For each version-split contains a zipped file with JSONL entries per case, each entry corresponsding to a single input-target pair used for code generation.
- Common fields: `file_name`, `prefix`, `target`, `suffix`
- Case specific fields: 
    - `comment_syntax`: The syntax used for the target comment, this is provided to the model to generate the comment in the correct format.
    - `smell_index`: The index of the SATD smell in the file, used to identify which SATD comment is being targeted (default is 0 for the first SATD comment in files with one SATD comment).
    - `dist`: The distance of the target method from the SATD comment (e.g., `out-smell-distance(-1)` for the last method in the file).
- Also includes logs of skipped methods/comments due to filter criteria (e.g. out-smell-distance(-1) cases must contain ≥3 methods).