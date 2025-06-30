This directory contains all intermediate outputs and job results used during code generation experiments. See more detailed information in the subfolders.

Most subfolders are organized by:
- **Version-split**: `v2-ds-all-1`, `v2-ds-all-2` Splits were created to ensure one split could run overnight on DelftBlue.
- **Model**: `MellumBase4B`, `StarCoder2_3B`, `SmolLM135M`
- **Setup**: `causal`, `FiM` (Fill in the Middle)
- **Case**: e.g., `in_smell_2000`, `out_smell_2000`