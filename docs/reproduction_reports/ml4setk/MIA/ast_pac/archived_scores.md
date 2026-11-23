# Historical comparison using archived Loss, PAC, and AST-PAC scores

This report records the archived-score experiment at revision `8155474`.
The subsequent four-model experiment starts from Java source and generates
fresh scores through the shared API. [Four-model FSE benchmark](full_benchmark.md)

This historical check supplied the authors’ saved per-file scores to the toolkit evaluators. It tests the ROC-AUC and PR-AUC calculations. The paper report compares fresh model scores with the FSE tables for all three methods. [AST-PAC paper report](index.md)

## PAC on StarCoder2-7B near-members

The printed cells were checked visually in the final proceedings PDF on
page 1362. The printed PR-AUC is outside the metric's range of zero to one.
[Paper, Table 1](https://repository.tudelft.nl/file/File_af66d741-b167-4406-9bc1-7f4474f47fed)

| Metric | Printed Table 1 | Deposited RQ1 notebook | ML4SETK on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.672 | 0.672786 | 0.672786233 |
| PR-AUC | 6.74 | 0.674191 | 0.674190972 |

The notebook agrees with both recomputed values. The available evidence
locates the discrepancies in the published table and does not establish
how they arose.

## What was compared

- **Inputs.** The four result files cover Mellum-4B, SmolLM3-3B,
  StarCoder2-3B, and StarCoder2-7B. Each contains 12,423 rows. Applying the
  notebooks' complete-row filter leaves 12,422 rows per model. The positive
  cohort is either exact members, near-members, or both. Each comparison
  uses the labeled nonmembers as the negative cohort.
- **Metrics.** The check calls the three public `ml4setk.MIA` evaluators on the
  original score columns. It compares ROC-AUC and trapezoidal PR-AUC, with
  tied scores entering each curve together. It checks all six RQ2/RQ3
  reference tables across file size, alphanumeric fraction, and AST node
  count. A stratum must contain both classes. The check also verifies that
  the set of computed strata equals the set in each reference table.
- **Table 2.** All ten numeric cutoffs match at the paper's precision on the
  12,484-row input dataset. The maximum alphanumeric fraction in the lowest
  bucket is 0.1975083, which prints as 0.2. The artifact names five
  alphanumeric buckets including `Low`. The paper lists four bucket labels
  alongside four cutoffs.
- **Figure 3.** All 72 underlying summary values matched the saved RQ3 notebook
  at six decimals: the median and two quartiles of the recorded change ratio
  for two methods, four models, and three complexity strata. This checks the
  descriptive statistics derived from the archived ratios.

**Limits.** Figures 1 and 2 were checked through the stratified point estimates
in their companion tables. Figure rendering, newly generated perturbations,
and model-derived score generation were outside the comparison. The module
does not return bootstrap confidence intervals. The RQ2 and RQ3 notebooks use
1,000 resamples and do not set a seed in their saved code, so the archived
interval endpoints remain unverified. The supplementary RQ1 classification
metrics were also outside the ROC-AUC and PR-AUC comparison.

## Original studies and attribution

The numerical results above belong to **Roham Koohestani, Ali Al-Kaswan,
Jonathan Katzy, and Maliheh Izadi**, *AST-PAC: AST-guided Membership Inference
for Code*, FSE Companion 2026, pp. 1361–1365. Roham Koohestani deposited the
versioned replication package. The paper and deposit declare CC BY 4.0. The
audit reads external reference files and redistributes no model outputs,
source dataset, or upstream implementation. [Paper](https://doi.org/10.1145/3803437.3805588) · [Deposit](https://doi.org/10.5281/zenodo.18348152)

- **PAC.** Wentao Ye, Jiaqi Hu, Liyao Li, Haobo Wang, Gang Chen, and Junbo Zhao,
  *Data Contamination Calibration for Black-box LLMs*, Findings of ACL 2024.
  The FSE comparison verifies PAC's evaluation for four models on a Java
  benchmark. The [ACL paper report](../pac/index.md) covers GPT-Neo on original WikiMIA. The pinned authors' repository contains no saved score file.
  [Original paper](https://doi.org/10.18653/v1/2024.findings-acl.644) · [Original artifact](https://github.com/yyy01/PAC/tree/79c6eca14fed3a64a7a4201cdca263de52501dae)
- **Loss.** Samuel Yeom, Irene Giacomelli, Matt Fredrikson, and Somesh Jha,
  *Privacy Risk in Machine Learning: Analyzing the Connection to Overfitting*,
  IEEE CSF 2018. The FSE comparison verifies the archived negative-loss
  baseline. The [CSF paper report](../loss/index.md) covers the theoretical curve in Figure 2b. The CSF artifact contains
  input data and scripts that generate results. [Original paper](https://doi.org/10.1109/CSF.2018.00027) · [Original artifact](https://github.com/sam-yeom/ml-privacy-csf18/tree/7b302fb80b853b040941eb90b37c0491f55e4928) · [Language-model reference](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting)

## Repeat the comparison

Run from the repository root with Poppler's `pdftotext` available. Supply
the extracted `ast-pac-fse-ivr-submission` directory and the final proceedings
PDF. The complete Zenodo ZIP matched the deposit's MD5 checksum
`2f137cfa98c98f1088d9454485840283`. This run used Python 3.12.3, PyArrow
26.0.0, and the two audit-only dependencies pinned below.
[Archive](https://doi.org/10.5281/zenodo.18348152) · [Proceedings PDF](https://repository.tudelft.nl/file/File_af66d741-b167-4406-9bc1-7f4474f47fed)

```bash
uv run --locked --extra datasets --with pandas==2.3.3 --with lxml==6.0.2 \
  python scripts/check_mia_reproduction.py /path/to/ast-pac-fse-ivr-submission /path/to/paper.pdf
```

The checker reports counts both at printed precision and at 1% relative tolerance. At 1%, it exits with status 1 for the printed PAC PR-AUC of 6.74 and the Table 2 low alphanumeric cutoff (observed 0.1975083, published 0.2). The MIA and smoke
test suites, including the existing artifact regression tests, passed all
27 cases in the same checkout.
