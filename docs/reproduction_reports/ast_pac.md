# AST-PAC reproduction report

[Reproduction script](https://github.com/jkatzy/ML4SE-toolkit/blob/79b61dc/reproductions/test_ast_pac.py) · [Environment and inputs](index.md)

```bash
/tmp/ml4setk-repro/bin/python -m pytest -o addopts= -qs reproductions/test_ast_pac.py
```

## Original paper

Koohestani, Al-Kaswan, Katzy, and Izadi report stratified ROC-AUC and PR-AUC in the RQ3 companion tables for Figure 2. The reproduction scores the Java source and its five deposited AST variants through ML4SETK on the four pinned models. The artifact supplies the labeled inputs and reference tables as data. The test calls the toolkit’s scorer and both public evaluators. [FSE Companion 2026 paper](https://doi.org/10.1145/3803437.3805588) · [Versioned RQ3 tables and neighbor texts](https://doi.org/10.5281/zenodo.18348152)

Fixing the five neighbor texts tests tokenization, the model forward pass, score calibration, and the reported areas independently of the authors’ Python implementation. Independently generating the syntax edits in Algorithm 1 remains outside this check. The earlier fresh-neighbor run below used the authors’ implementation for that step.

## Earlier four-model FSE run with fresh scores

This earlier run called the authors’ Java neighbor generator and used newly generated scores for 12,422 Java files on each of four models. Exact members, near-members, and both member groups together were each compared with the same nonmembers. Every evaluated ROC-AUC and PR-AUC agreed with scikit-learn on the fresh scores within an absolute tolerance of `1e-12`. The shared and method-specific evaluators agreed for every comparison. [Protocol and reproduction command](full_benchmark.md)

| Reference | Metric values matching at reference precision | Maximum absolute difference |
| --- | ---: | ---: |
| RQ3 stratified areas | 34/288 | 0.010223 |
| RQ3 bootstrap endpoints | 62/576 | 0.015133 |
| Figure 3 change-ratio quartiles and medians | 0/36 | 0.002962 |

Area estimates and interval endpoints in the deposited tables are rounded to three decimals. The notebooks report six decimals. The fresh bootstrap intervals use 1,000 resamples per comparison.

All 288 fresh stratified area estimates fall inside the corresponding published 95% bootstrap intervals. These intervals describe sampling uncertainty for the authors’ evaluation cohort.

For the exact-member comparison, the RQ3 complex-files stratum gave the following values.

| Model | ROC-AUC, fresh / reference | PR-AUC, fresh / reference |
| --- | ---: | ---: |
| StarCoder2-3B | 0.637354 / 0.638 | 0.601034 / 0.603 |
| StarCoder2-7B | 0.653155 / 0.654 | 0.619708 / 0.622 |
| Mellum-4B | 0.683106 / 0.680 | 0.662257 / 0.657 |
| SmolLM3-3B | 0.563401 / 0.567 | 0.512381 / 0.513 |

With both member groups combined, AST-PAC had higher complex-file ROC-AUC than PAC on SmolLM3-3B (0.556 versus 0.518). PAC had higher complex-file ROC-AUC on Mellum and both StarCoder2 models. The same ordering appears for each model in the deposited RQ3 table.

### Agreement on individual files

Each row compares 12,422 fresh AST-PAC scores with the corresponding archived scores after aligning score direction. The last column compares the two rankings of the same files.

| Model | Median absolute score difference | Largest absolute score difference | Spearman correlation |
| --- | ---: | ---: | ---: |
| StarCoder2-3B | 0.12994472 | 1.7710032 | 0.9621466697 |
| StarCoder2-7B | 0.13544278 | 1.667259 | 0.9622107848 |
| Mellum-4B | 0.1447654 | 2.6817513 | 0.9649197228 |
| SmolLM3-3B | 0.13642001 | 1.9597005 | 0.9546170826 |

## StarCoder2-3B pilot on 225 files

The corrected benchmark adapter supplied the authors' forward inputs and freshly scored all 225 Java files in the StarCoder2-3B Mid-Low exact-member comparison. The runner passed original source to inherited `MembershipScorer.score_many`, then evaluated its higher-is-member outputs with `evaluate_membership_scores`.

| Metric | Shared API | Scikit-learn on the same scores | FSE reference |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.606875204 | 0.606875204 | 0.610 |
| PR-AUC | 0.704637610 | 0.704637610 | 0.707 |

Fresh ROC-AUC falls below the reference by 0.00312 and PR-AUC by 0.00236. Both are inside the RQ3 reference intervals (0.538–0.683 and 0.631–0.784). Both metric checks against scikit-learn passed at an absolute tolerance of `1e-12`. The complete four-model protocol records the per-file score control, the attention-mask correction and the seed used to generate each file's neighbors. [Shared API protocol](full_benchmark.md)

## Earlier fixed-input comparison

**PR-AUC matches and ROC-AUC differs from the reference at three decimal places.** This run generated new scores for all 225 Java files in the Mid-Low alphanumeric stratum, comparing 132 exact members with 93 nonmembers. The reference is the StarCoder2-3B row for AST-PAC in `analysis/RQ3/rq3_table_ME_vs_NM.tex`, the companion table for Figure 2 of Koohestani et al., *AST-PAC: AST-guided Membership Inference for Code*. [FSE paper](https://doi.org/10.1145/3803437.3805588) · [Versioned replication package](https://doi.org/10.5281/zenodo.18348152)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.610 | 0.609278267 | 0.609604106 |
| PR-AUC | 0.707 | 0.706530510 | 0.706830917 |

Fresh PR-AUC rounds to 0.707. Fresh ROC-AUC rounds to 0.609. Its difference from the archived ROC-AUC is −0.00032584, equivalent to four member–nonmember pairs out of 12,276 in the rank comparison.

Across the 225 paired files, the median absolute difference between fresh and archived raw scores was 0.000819997 and the maximum was 0.006344064. ROC-AUC and trapezoidal PR-AUC use tied scores as a group. The comparison uses the published point estimates.

### Earlier fixed-input protocol

For each Java file, ML4SETK rescored the original text and its five archived AST-guided neighbors. It calculated the mean log-probability gap between the five highest and 30 lowest next-token predictions, scaling the counts down for short texts. It subtracted the mean neighbor gap from the original gap. The evaluator treats a lower calibrated score as stronger evidence of membership.

Holding the five AST-guided permutations fixed makes the model and scoring comparison repeatable. This experiment tests the score for a published set of syntax-aware edits. Independently parsing and generating edits, and the paper's comparison across complexity levels, remain outside its scope.

The run used two NVIDIA A40 GPUs, float16 StarCoder2-3B weights, and the checkpoint's tokenizer with an 8,192-token cap. The cap applied to 22 original files and 110 of 1,125 AST-PAC neighbor texts. The model revision was `733247c55e3f73af49ce8e9c7949bf14af205928`. The authors' archive matched its versioned checksum and the model weights matched their Hub SHA-256. The archive supplies the exact cohort and comparison scores. Only the model-derived scores feed the fresh estimates. [Earlier fixed-input command](full_benchmark.md#repeat-the-earlier-fixed-input-pilot)
