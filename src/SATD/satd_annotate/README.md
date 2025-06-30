This directory contains all code for annotating the Java dataset with SATD. Also contains `requirements.txt` with minimal dependencies to replicate the annotations.

Initial annotation was based on SATD bitmasks. Later expanded to include SATD `spans` and `counts` to reduce runtime during repeated experiments. There is also a script included to extract and store these annotations in zipped JSONL format.

### Investigation
- Includes a notebook that investigates the top 100 SATD-heavy files. Output includes: full file code, SATD comment counts, top 10 most common SATD comments per file.
- Also contains the final list of excluded files and their corresponding IDs.