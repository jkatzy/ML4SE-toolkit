# Loss reproduction report

[Reproduction script](https://github.com/jkatzy/ML4SE-toolkit/blob/1293774/reproductions/test_loss.py) · [Environment and inputs](index.md)

```bash
/tmp/ml4setk-repro/bin/python -m pytest -o addopts= -qs reproductions/test_loss.py
```

## Original paper

Yeom, Giacomelli, Fredrikson, and Jha’s Figure 2b gives the theoretical membership advantage when only the training standard deviation is known. The script evaluates the toolkit’s inclusive loss threshold on 10,000 deterministic Gaussian quantiles per cohort. The reference is the paper’s closed form. The bound of 0.0002 follows from midpoint integration at the two interval boundaries in each cohort. [CSF 2018 paper](https://doi.org/10.1109/CSF.2018.00027) · [Figure 2b and derivation](https://par.nsf.gov/servlets/purl/10060215)

| Population / training standard deviation | ML4SETK advantage | Theoretical advantage |
| ---: | ---: | ---: |
| 1 | 0.0000 | 0.000000 |
| 2 | 0.2996 | 0.299765 |
| 4 | 0.4852 | 0.485277 |
| 8 | 0.5832 | 0.583213 |

All four theoretical comparisons pass the 1% rule. The zero-reference case matched exactly. All four also satisfied the integration bound. This verifies the theoretical curve. The plotted empirical points require training the paper’s regression and tree models. The later FSE benchmark evaluates negative next-token loss on code and reports ROC-AUC and PR-AUC.

## FSE baseline check

The new comparison code rechecked all 49,688 stored model–file scores for this baseline from the preceding ML4SETK run. All 24 Table 1 areas and all 288 RQ2 stratified areas pass at 1% relative tolerance. At three decimals the match counts were 24/24 and 285/288. All 288 stratified estimates fell inside the published intervals. Running this report’s pytest script regenerates scores from the Java source.

The per-method script also scored the complete 225-file pilot on each model. The pilot compares 132 exact members with 93 nonmembers in the Mid-Low alphanumeric stratum. 8/8 pilot areas pass the 1% rule. All eight fell inside their reference intervals.

| Model | Pilot ROC-AUC, observed / paper | Pilot PR-AUC, observed / paper |
| --- | ---: | ---: |
| StarCoder2-3B | 0.621619 / 0.622 | 0.699924 / 0.700 |
| StarCoder2-7B | 0.645080 / 0.645 | 0.716864 / 0.717 |
| Mellum-4B | 0.620479 / 0.620 | 0.684496 / 0.684 |
| SmolLM3-3B | 0.530140 / 0.530 | 0.605098 / 0.605 |

## Earlier four-model FSE run with fresh scores

This run used newly generated scores for 12,422 Java files on each of four models. Exact members, near-members, and both member groups together were each compared with the same nonmembers. Every evaluated ROC-AUC and PR-AUC agreed with scikit-learn on the fresh scores within an absolute tolerance of `1e-12`. The shared and method-specific evaluators agreed for every comparison. [Protocol and reproduction command](full_benchmark.md)

| Reference | Within 1% of reference | At reference precision | Maximum absolute difference |
| --- | ---: | ---: | ---: |
| Printed Table 1, aggregate areas | 24/24 | 24/24 | 0.000478 |
| RQ1 notebook, aggregate areas | 24/24 | 19/24 | 0.000006 |
| RQ1 notebook, threshold metrics | 48/48 | 36/48 | 0.000249 |
| RQ2 stratified areas | 288/288 | 285/288 | 0.000536 |
| RQ2 bootstrap endpoints | 570/576 | 145/576 | 0.009204 |

Area estimates and interval endpoints in the deposited tables are rounded to three decimals. The notebooks report six decimals. The fresh bootstrap intervals use 1,000 resamples per comparison.

All 288 fresh stratified area estimates fall inside the corresponding published 95% bootstrap intervals. These intervals describe sampling uncertainty for the authors’ evaluation cohort.

| Model | Positive cohort | ROC-AUC, fresh / paper | PR-AUC, fresh / paper |
| --- | --- | ---: | ---: |
| StarCoder2-3B | Both | 0.625275 / 0.625 | 0.750389 / 0.75 |
| StarCoder2-3B | Exact | 0.622010 / 0.622 | 0.599896 / 0.6 |
| StarCoder2-3B | Near | 0.628686 / 0.629 | 0.605224 / 0.605 |
| StarCoder2-7B | Both | 0.635365 / 0.635 | 0.758063 / 0.758 |
| StarCoder2-7B | Exact | 0.633831 / 0.634 | 0.611207 / 0.611 |
| StarCoder2-7B | Near | 0.636967 / 0.637 | 0.614178 / 0.614 |
| Mellum-4B | Both | 0.627965 / 0.628 | 0.763710 / 0.764 |
| Mellum-4B | Exact | 0.629433 / 0.629 | 0.627605 / 0.628 |
| Mellum-4B | Near | 0.626431 / 0.626 | 0.616814 / 0.617 |
| SmolLM3-3B | Both | 0.573088 / 0.573 | 0.700796 / 0.701 |
| SmolLM3-3B | Exact | 0.571522 / 0.572 | 0.538924 / 0.539 |
| SmolLM3-3B | Near | 0.574723 / 0.575 | 0.540711 / 0.541 |

The three stratified areas that rounded differently all came from StarCoder2-3B. With both member groups combined, Mid-Low alphanumeric ROC-AUC was 0.641536 (paper 0.641) and Very Large file PR-AUC was 0.727502 (paper 0.727). With exact members, Medium file ROC-AUC was 0.685518 (paper 0.685).

### Agreement on individual files

Each row compares 12,422 fresh Loss scores with the corresponding archived scores after aligning score direction. The last column compares the two rankings of the same files.

| Model | Median absolute score difference | Largest absolute score difference | Spearman correlation |
| --- | ---: | ---: | ---: |
| StarCoder2-3B | 6.327033e-05 | 0.0036132336 | 0.9999998344 |
| StarCoder2-7B | 0 | 0 | 1.0000000000 |
| Mellum-4B | 0 | 0 | 1.0000000000 |
| SmolLM3-3B | 0 | 0 | 1.0000000000 |

## StarCoder2-3B pilot on 225 files

The corrected benchmark adapter supplied the authors' forward inputs and freshly scored all 225 Java files in the StarCoder2-3B Mid-Low exact-member comparison. The runner passed original source to inherited `MembershipScorer.score_many`, then evaluated its higher-is-member outputs with `evaluate_membership_scores`.

| Metric | Shared API | Scikit-learn on the same scores | FSE reference |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.621619420 | 0.621619420 | 0.622 |
| PR-AUC | 0.699924464 | 0.699924464 | 0.700 |

Both estimates agree with the FSE table at its published three-decimal precision. Both metric checks against scikit-learn passed at an absolute tolerance of `1e-12`. The complete four-model protocol records the per-file score control, the attention-mask correction and the seed used to generate each file's neighbors. [Shared API protocol](full_benchmark.md)

## Earlier fixed-input comparison

**PR-AUC matches and ROC-AUC differs from the reference at three decimal places.** This run generated new scores for all 225 Java files in the Mid-Low alphanumeric stratum, comparing 132 exact members with 93 nonmembers. The reference is the StarCoder2-3B row for Loss in `analysis/RQ2/rq2_table_ME_vs_NM.tex`, the companion table for Figure 1 of Koohestani et al., *AST-PAC: AST-guided Membership Inference for Code*. [FSE paper](https://doi.org/10.1145/3803437.3805588) · [Versioned replication package](https://doi.org/10.5281/zenodo.18348152)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.622 | 0.621456500 | 0.621537960 |
| PR-AUC | 0.700 | 0.699859994 | 0.699899829 |

Fresh PR-AUC rounds to 0.700. Fresh ROC-AUC rounds to 0.621. Its difference from the archived ROC-AUC is −0.00008146, equivalent to one member–nonmember pair out of 12,276 in the rank comparison.

Across the 225 paired files, the median absolute difference between fresh and archived raw scores was 0.000066843 and the maximum was 0.001034659. ROC-AUC and trapezoidal PR-AUC use tied scores as a group. The comparison uses the published point estimates.

### Earlier fixed-input protocol

For each original Java file, ML4SETK computed the mean log probability of the observed next tokens. It applied a float32 log-softmax to the model's logits and accumulated the selected values in float64. Higher scores favor membership. This tests the negative cross-entropy baseline that Koohestani et al. use for code. The earlier CSF experiments use a different setting and remain outside this comparison. [Yeom et al., CSF 2018](https://doi.org/10.1109/CSF.2018.00027) · [Carlini et al., USENIX Security 2021](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting)

The run used two NVIDIA A40 GPUs, float16 StarCoder2-3B weights, and the checkpoint's tokenizer with an 8,192-token cap. The cap applied to 22 original files. The model revision was `733247c55e3f73af49ce8e9c7949bf14af205928`. The authors' archive matched its versioned checksum and the model weights matched their Hub SHA-256. The archive supplies the exact cohort and comparison scores. Only the model-derived scores feed the fresh estimates. [Earlier fixed-input command](full_benchmark.md#repeat-the-earlier-fixed-input-pilot)
