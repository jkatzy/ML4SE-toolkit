# AST-PAC reproduction report

*AST-PAC: AST-guided Membership Inference for Code*. Roham Koohestani, Ali Al-Kaswan, Jonathan Katzy, and Maliheh Izadi. FSE Companion 2026. [Paper](https://doi.org/10.1145/3803437.3805588)

Koohestani et al. evaluated AST-PAC alongside two baselines on Java code. [Loss baseline](#loss-baseline) · [PAC baseline](#pac-baseline)

## Coverage of the original paper

**Partial independent reproduction.** Both tables and all three figures have numerical comparisons from the four-model benchmark. Its fresh AST edits came from the authors’ generator. The paper-specific toolkit script separately checks scoring on deposited edits. End-to-end generation and evaluation of fresh AST edits using only the toolkit remain pending. No hardware exception is documented. [Final paper](https://repository.tudelft.nl/file/File_af66d741-b167-4406-9bc1-7f4474f47fed) · [Historical benchmark command](full_benchmark.md#repeat-the-historical-run-with-the-authors-ast-generator) · [Toolkit scoring command](#reproduce-these-measurements)

| Published item | Experiments covered | Measurements and gaps |
| --- | --- | --- |
| Table 1 | Loss and PAC, four models, three membership cohorts, two metrics | All 48 published AUCs are paired below. The printed StarCoder2-7B PAC near-member PR-AUC is 6.74. The deposited notebook gives 0.674191 and the toolkit measured 0.673612. [Loss](#loss-baseline) · [PAC](#pac-baseline) |
| Table 2 | Bucket boundaries from the full Java dataset | All ten numeric cutoffs checked across 12,484 rows. Values below. |
| Figure 1 | Six panels for Loss and PAC, crossing file size, alphanumeric fraction, and AST node count with ROC-AUC and PR-AUC | Fresh estimates and bootstrap endpoints for all four models and three cohort comparisons. [Loss pairs](data/loss_fse.csv) · [PAC pairs](data/pac_fse.csv) |
| Figure 2 | Same six panels for PAC and AST-PAC | Historical fresh-neighbor estimates and interval endpoints available. The fixed-neighbor pilot retained eight paired AUCs. The full fixed-neighbor run retained summary counts, leaving 14 individual comparisons unverified. [PAC pairs](data/pac_fse.csv) · [AST-PAC pairs](data/ast_pac_fse.csv) · [Pilot pairs](data/ast_pac_fixed_pilot.csv) |
| Figure 3 | Change ratio for two methods, four models, and three AST size groups | All 72 medians and quartiles paired in the historical run. Independent AST generation remains pending. [PAC change ratios](data/pac_fse.csv) · [AST-PAC change ratios](data/ast_pac_fse.csv) |

### Table 2 bucket boundaries

| Dimension | Paper cutoffs | Measured cutoffs |
| --- | --- | --- |
| File size | 1074, 1946, 3369, 6844 | 1074, 1946, 3369, 6844 |
| AST node count | 58, 211 | 58, 211 |
| Alphanumeric fraction | 0.2, 0.4, 0.6, 0.8 | 0.1975083, 0.4, 0.6, 0.8 |

## Figure 2 companion table · Scoring the published AST neighbors

On the StarCoder2-3B pilot, the FSE companion table gives **0.610 ROC-AUC and 0.707 PR-AUC**. ML4SETK measured **0.609604 and 0.706842**. The same comparison below covers all four models on 132 exact members and 93 nonmembers in the Mid-Low alphanumeric stratum. Each file was scored with the five AST variants supplied in the deposit. [Koohestani et al., FSE Companion 2026](https://doi.org/10.1145/3803437.3805588) · [RQ3 exact-member companion table](https://doi.org/10.5281/zenodo.18348152)

![Published ROC-AUC and PR-AUC with their 95% intervals and the ML4SETK pilot point estimates for each model.](figures/ast_pac_fixed_pilot.png)

| Model | Reference ROC-AUC | ML4SETK ROC-AUC | Reference PR-AUC | ML4SETK PR-AUC |
| --- | ---: | ---: | ---: | ---: |
| StarCoder2-3B | 0.610 | 0.609604 | 0.707 | 0.706842 |
| StarCoder2-7B | 0.627 | 0.626792 | 0.724 | 0.723929 |
| Mellum-4B | 0.637 | 0.637260 | 0.726 | 0.726284 |
| SmolLM3-3B | 0.585 | 0.585044 | 0.642 | 0.641550 |

The horizontal lines show the authors’ 95% bootstrap intervals. Diamonds show the reproduced point estimates. The four-model fixed-neighbor run also scored all 12,422 files per model, but its full-run logs retained only summary counts. Individual values for the 14 previously flagged comparisons are unavailable from those logs. The pilot supplies the paired numerical values shown here. This experiment checks scoring and calibration using existing syntax edits. [Pilot values and published interval bounds (CSV)](data/ast_pac_fixed_pilot.csv)

## Historical RQ3 run with the authors’ AST generator

An earlier run generated five new neighbors per file with the authors’ Java augmentation function and scored them with ML4SETK. For the **complex-file stratum, exact members versus nonmembers**, the paper’s companion table and this run give the following values. The downloadable table includes the remaining strata and bootstrap endpoints. [FSE artifact, RQ3](https://doi.org/10.5281/zenodo.18348152)

| Model | Reference ROC-AUC | ML4SETK ROC-AUC | Reference PR-AUC | ML4SETK PR-AUC |
| --- | ---: | ---: | ---: | ---: |
| StarCoder2-3B | 0.638 | 0.637354 | 0.603 | 0.601034 |
| StarCoder2-7B | 0.654 | 0.653155 | 0.622 | 0.619708 |
| Mellum-4B | 0.680 | 0.683106 | 0.657 | 0.662257 |
| SmolLM3-3B | 0.567 | 0.563401 | 0.513 | 0.512381 |

[Full FSE comparison table (CSV)](data/ast_pac_fse.csv) · [Four-model protocol and plots](full_benchmark.md)

### Earlier StarCoder2-3B control

The earlier 225-file run used a different model forward call. The last column recomputes areas from the authors’ saved scores. [Forward-pass control and earlier command](full_benchmark.md#forward-pass-control)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.610 | 0.609278267 | 0.609604106 |
| PR-AUC | 0.707 | 0.706530510 | 0.706830917 |

## Loss baseline

### Table 1 · Negative loss on Java

Table 1 compares exact members (4,193), near-members (4,014), and both groups combined with the same 4,215 nonmembers. Each model scored the same 12,422 Java files. PR-AUC uses trapezoidal integration. [FSE Table 1](https://doi.org/10.1145/3803437.3805588) · [Companion tables](https://doi.org/10.5281/zenodo.18348152)

| Model | Members | Reference ROC-AUC | ML4SETK ROC-AUC | Reference PR-AUC | ML4SETK PR-AUC |
| --- | --- | ---: | ---: | ---: | ---: |
| StarCoder2-3B | Both | 0.625 | 0.625275 | 0.750 | 0.750389 |
| StarCoder2-3B | Exact | 0.622 | 0.622010 | 0.600 | 0.599896 |
| StarCoder2-3B | Near | 0.629 | 0.628686 | 0.605 | 0.605224 |
| StarCoder2-7B | Both | 0.635 | 0.635365 | 0.758 | 0.758063 |
| StarCoder2-7B | Exact | 0.634 | 0.633831 | 0.611 | 0.611207 |
| StarCoder2-7B | Near | 0.637 | 0.636967 | 0.614 | 0.614178 |
| Mellum-4B | Both | 0.628 | 0.627965 | 0.764 | 0.763710 |
| Mellum-4B | Exact | 0.629 | 0.629433 | 0.628 | 0.627605 |
| Mellum-4B | Near | 0.626 | 0.626431 | 0.617 | 0.616814 |
| SmolLM3-3B | Both | 0.573 | 0.573088 | 0.701 | 0.700796 |
| SmolLM3-3B | Exact | 0.572 | 0.571522 | 0.539 | 0.538924 |
| SmolLM3-3B | Near | 0.575 | 0.574723 | 0.541 | 0.540711 |

[Full FSE comparison table (CSV)](data/loss_fse.csv) · [Four-model protocol and plots](full_benchmark.md)

### RQ2 · Loss on exact members in the Mid-Low alphanumeric stratum

The pilot independently scored all 132 exact members and 93 nonmembers in this stratum. The reference columns come from the RQ2 companion table.

| Model | Reference ROC-AUC | ML4SETK ROC-AUC | Reference PR-AUC | ML4SETK PR-AUC |
| --- | ---: | ---: | ---: | ---: |
| StarCoder2-3B | 0.622 | 0.621619 | 0.700 | 0.699924 |
| StarCoder2-7B | 0.645 | 0.645080 | 0.717 | 0.716864 |
| Mellum-4B | 0.620 | 0.620479 | 0.684 | 0.684496 |
| SmolLM3-3B | 0.530 | 0.530140 | 0.605 | 0.605098 |

### Earlier StarCoder2-3B Loss control

The earlier 225-file run used a different model forward call. The last column recomputes areas from the authors’ saved scores. [Forward-pass control and earlier command](full_benchmark.md#forward-pass-control)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.622 | 0.621456500 | 0.621537960 |
| PR-AUC | 0.700 | 0.699859994 | 0.699899829 |

## PAC baseline

### Table 1 · Token-swap PAC on Java

Token-swap PAC uses the same Java cohorts and metrics as the loss baseline. [FSE Table 1](https://doi.org/10.1145/3803437.3805588) · [Companion tables](https://doi.org/10.5281/zenodo.18348152)

| Model | Members | Reference ROC-AUC | ML4SETK ROC-AUC | Reference PR-AUC | ML4SETK PR-AUC |
| --- | --- | ---: | ---: | ---: | ---: |
| StarCoder2-3B | Both | 0.662 | 0.662458 | 0.798 | 0.797892 |
| StarCoder2-3B | Exact | 0.662 | 0.662915 | 0.680 | 0.680695 |
| StarCoder2-3B | Near | 0.661 | 0.661981 | 0.664 | 0.663359 |
| StarCoder2-7B | Both | 0.675 | 0.675805 | 0.806 | 0.806272 |
| StarCoder2-7B | Exact | 0.678 | 0.678296 | 0.694 | 0.694400 |
| StarCoder2-7B | Near | 0.672 | 0.673202 | 6.740 | 0.673612 |
| Mellum-4B | Both | 0.696 | 0.695611 | 0.827 | 0.827233 |
| Mellum-4B | Exact | 0.712 | 0.711962 | 0.742 | 0.741737 |
| Mellum-4B | Near | 0.679 | 0.678531 | 0.691 | 0.690885 |
| SmolLM3-3B | Both | 0.578 | 0.578711 | 0.735 | 0.735614 |
| SmolLM3-3B | Exact | 0.579 | 0.579049 | 0.591 | 0.592447 |
| SmolLM3-3B | Near | 0.578 | 0.578357 | 0.579 | 0.579996 |

For StarCoder2-7B near-members, the printed PR-AUC is **6.74**, outside its possible range. The deposited notebook gives **0.674191**, and ML4SETK measured **0.673612**. For the same row, the notebook gives ROC-AUC 0.672786. [Paper and notebook comparison](archived_scores.md)

[Full FSE comparison table (CSV)](data/pac_fse.csv) · [Four-model protocol and plots](full_benchmark.md)

### RQ2 · PAC on exact members in the Mid-Low alphanumeric stratum

The pilot independently scored all 132 exact members and 93 nonmembers in this stratum. The reference columns come from the RQ2 companion table.

| Model | Reference ROC-AUC | ML4SETK ROC-AUC | Reference PR-AUC | ML4SETK PR-AUC |
| --- | ---: | ---: | ---: | ---: |
| StarCoder2-3B | 0.698 | 0.703649 | 0.788 | 0.790301 |
| StarCoder2-7B | 0.717 | 0.719616 | 0.811 | 0.812720 |
| Mellum-4B | 0.726 | 0.730368 | 0.809 | 0.812511 |
| SmolLM3-3B | 0.627 | 0.625204 | 0.714 | 0.703676 |

### Earlier StarCoder2-3B PAC control

The earlier 225-file run used a different model forward call. The last column recomputes areas from the authors’ saved scores. [Forward-pass control and earlier command](full_benchmark.md#forward-pass-control)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.698 | 0.697621375 | 0.697539915 |
| PR-AUC | 0.788 | 0.788430096 | 0.788354407 |

## Reproduce these measurements

The script scores the published AST neighbors and both baselines with ML4SETK. From the repository root, prepare a CUDA environment. [Reproduction script](https://github.com/jkatzy/ML4SE-toolkit/blob/2e976ea/reproductions/test_ast_pac.py)

```bash
uv venv --python 3.13 /tmp/ml4setk-repro
uv pip install --python /tmp/ml4setk-repro/bin/python -e . pytest==9.0.2 \
  torch==2.8.0 transformers==4.55.4 pandas==3.0.6 pyarrow==25.0.0 numpy==2.5.5
```

Download the archive and final paper. Extract the data and tables only. Run the following commands in a fresh directory for the external inputs.

```bash
curl -fL https://zenodo.org/api/records/18348152/files/ast-pac-fse-ivr-submission.zip/content -o fse.zip
echo '2f137cfa98c98f1088d9454485840283  fse.zip' | md5sum -c -
unzip -q fse.zip '*/dataset/full.parquet' '*/results/*_m_worker_0.parquet' '*/analysis/RQ[23]/*.tex'
curl -fL https://repository.tudelft.nl/file/File_af66d741-b167-4406-9bc1-7f4474f47fed -o fse.pdf
export ML4SETK_AST_PAC_ARTIFACT="$PWD/ast-pac-fse-ivr-submission"
export ML4SETK_FSE_PDF="$PWD/fse.pdf"
```

Back at the repository root, run the pytest command below. The full FSE entry points score all 12,422 complete cases per model. Table 1 comparison uses Poppler’s `pdftotext`. For a shorter run, add `--fse-pilot` to score the published 225-file exact-member Mid-Low stratum on each model. Add `--fse-model SC2-3B` to select one model.

```bash
/tmp/ml4setk-repro/bin/python -m pytest -o addopts= -qs reproductions/test_ast_pac.py
```

The earlier runs have separate commands and inputs. [Historical four-model run](full_benchmark.md#repeat-the-historical-run-with-the-authors-ast-generator) · [Archived-score audit](archived_scores.md#repeat-the-comparison)
