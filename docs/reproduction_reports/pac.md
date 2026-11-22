# PAC reproduction report

[Reproduction script](https://github.com/jkatzy/ML4SE-toolkit/blob/d2d6958/reproductions/test_pac.py) · [Environment and inputs](index.md)

```bash
/tmp/ml4setk-repro/bin/python -m pytest -o addopts= -qs reproductions/test_pac.py
```

## Original paper

Ye, Hu, Li, Wang, Chen, and Zhao report a ROC-AUC of 0.666 for PAC and 0.616 for perplexity in the GPT-Neo row of Table 1 on original WikiMIA text. Our check scores all 861 labeled members and 789 labeled nonmembers from the four length groups in Table 6 with GPT-Neo-2.7B. It verifies the two cohorts in each length group before scoring. [ACL 2024 paper](https://aclanthology.org/2024.findings-acl.644/) · [Dataset revision](https://huggingface.co/datasets/swj0419/WikiMIA/tree/a89ab76d88f704e9bc5870ac39cc9d458a2a70ac) · [Model revision](https://huggingface.co/EleutherAI/gpt-neo-2.7B/tree/e24fa291132763e59f4a5422741b424fb5d59056)

The reproduction uses float32 model weights, five word-swap variants per text, and the top 5% and bottom 30% of next-token log probabilities. The random draws use seed 42. The authors did not publish their realized draws. We pool the four original-text splits and use the toolkit evaluators for both ROC-AUCs. Negative mean loss gives the same ranking as inverse perplexity. The test checks both the PAC advantage over perplexity and equality with the printed PAC area at three decimals. Other Table 1 models, synonymous rewrites, and StackMIAsub remain untested here.

| Original WikiMIA, GPT-Neo-2.7B | Fresh ROC-AUC | ACL Table 1 |
| --- | ---: | ---: |
| PAC | 0.663491475 | 0.666 |
| Perplexity baseline | 0.615686950 | 0.616 |

The baseline matched at the paper’s precision. PAC exceeded it by 0.047805, reproducing the reported ordering. The strict PAC area check failed by 0.002509. The reproduction keeps the published target of 0.666 in the assertion.

## FSE baseline check

The new comparison code rechecked all 49,688 stored model–file scores for this baseline from the preceding ML4SETK run. Thirteen of 24 Table 1 areas and 60 of 288 RQ2 stratified areas matched at three decimals. All 288 stratified estimates fell inside the published intervals. Running this report’s pytest script regenerates scores from the Java source.

## Earlier four-model FSE run with fresh scores

This run used newly generated scores for 12,422 Java files on each of four models. Exact members, near-members, and both member groups together were each compared with the same nonmembers. Every evaluated ROC-AUC and PR-AUC agreed with scikit-learn on the fresh scores within an absolute tolerance of `1e-12`. The shared and method-specific evaluators agreed for every comparison. [Protocol and reproduction command](full_benchmark.md)

| Reference | Metric values matching at reference precision | Maximum absolute difference |
| --- | ---: | ---: |
| Printed Table 1, aggregate areas | 13/24 | 6.066388 |
| RQ1 notebook, aggregate areas | 0/24 | 0.001141 |
| RQ1 notebook, threshold metrics | 0/48 | 0.067763 |
| RQ2 stratified areas | 60/288 | 0.010324 |
| RQ2 bootstrap endpoints | 99/576 | 0.013290 |
| RQ3 stratified areas | 60/288 | 0.010324 |
| RQ3 bootstrap endpoints | 98/576 | 0.013848 |
| Figure 3 change-ratio quartiles and medians | 0/36 | 0.000554 |

Area estimates and interval endpoints in the deposited tables are rounded to three decimals. The notebooks report six decimals. The fresh bootstrap intervals use 1,000 resamples per comparison.

The same 288 PAC area estimates appear in RQ2 and RQ3. All 288 fresh estimates fall inside the published 95% bootstrap intervals in both tables. These intervals describe sampling uncertainty for the authors’ evaluation cohort.

| Model | Positive cohort | ROC-AUC, fresh / paper | PR-AUC, fresh / paper |
| --- | --- | ---: | ---: |
| StarCoder2-3B | Both | 0.662458 / 0.662 | 0.797892 / 0.798 |
| StarCoder2-3B | Exact | 0.662915 / 0.662 | 0.680695 / 0.68 |
| StarCoder2-3B | Near | 0.661981 / 0.661 | 0.663359 / 0.664 |
| StarCoder2-7B | Both | 0.675805 / 0.675 | 0.806272 / 0.806 |
| StarCoder2-7B | Exact | 0.678296 / 0.678 | 0.694400 / 0.694 |
| StarCoder2-7B | Near | 0.673202 / 0.672 | 0.673612 / 6.74 |
| Mellum-4B | Both | 0.695611 / 0.696 | 0.827233 / 0.827 |
| Mellum-4B | Exact | 0.711962 / 0.712 | 0.741737 / 0.742 |
| Mellum-4B | Near | 0.678531 / 0.679 | 0.690885 / 0.691 |
| SmolLM3-3B | Both | 0.578711 / 0.578 | 0.735614 / 0.735 |
| SmolLM3-3B | Exact | 0.579049 / 0.579 | 0.592447 / 0.591 |
| SmolLM3-3B | Near | 0.578357 / 0.578 | 0.579996 / 0.579 |

Two printed values for StarCoder2-7B near-members differ from the deposited notebook. The paper gives ROC-AUC 0.672 and PR-AUC 6.74, which exceeds the PR-AUC range. The notebook gives 0.672786 and 0.674191. The fresh run gives 0.673202 and 0.673612, respectively. Both fresh values agree with the notebook at three decimals.

### Agreement on individual files

Each row compares 12,422 fresh PAC scores with the corresponding archived scores after aligning score direction. The last column compares the two rankings of the same files.

| Model | Median absolute score difference | Largest absolute score difference | Spearman correlation |
| --- | ---: | ---: | ---: |
| StarCoder2-3B | 0.13459531 | 1.11127 | 0.9900079532 |
| StarCoder2-7B | 0.1280542 | 1.2454369 | 0.9910630066 |
| Mellum-4B | 0.15250542 | 1.1034914 | 0.9903950333 |
| SmolLM3-3B | 0.20385208 | 1.6416078 | 0.9754493956 |

## StarCoder2-3B pilot on 225 files

The corrected benchmark adapter supplied the authors' forward inputs and freshly scored all 225 Java files in the StarCoder2-3B Mid-Low exact-member comparison. The runner passed original source to inherited `MembershipScorer.score_many`, then evaluated its higher-is-member outputs with `evaluate_membership_scores`.

| Metric | Shared API | Scikit-learn on the same scores | FSE reference |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.703649397 | 0.703649397 | 0.698 |
| PR-AUC | 0.790301282 | 0.790301282 | 0.788 |

Fresh ROC-AUC exceeds the reference by 0.00565 and fresh PR-AUC by 0.00230. Both are inside the RQ2 reference intervals (0.632–0.758 and 0.713–0.849). Both metric checks against scikit-learn passed at an absolute tolerance of `1e-12`. The complete four-model protocol records the per-file score control, the attention-mask correction and the seed used to generate each file's neighbors. [Shared API protocol](full_benchmark.md)

## Earlier fixed-input comparison

**Both metrics match the reference at three decimal places.** This run generated new scores for all 225 Java files in the Mid-Low alphanumeric stratum, comparing 132 exact members with 93 nonmembers. The reference is the StarCoder2-3B row for PAC in `analysis/RQ2/rq2_table_ME_vs_NM.tex`, the companion table for Figure 1 of Koohestani et al., *AST-PAC: AST-guided Membership Inference for Code*. [FSE paper](https://doi.org/10.1145/3803437.3805588) · [Versioned replication package](https://doi.org/10.5281/zenodo.18348152)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.698 | 0.697621375 | 0.697539915 |
| PR-AUC | 0.788 | 0.788430096 | 0.788354407 |

Fresh ROC-AUC and PR-AUC round to 0.698 and 0.788. Both agree at the reference precision even though the per-file scores differ slightly.

Across the 225 paired files, the median absolute difference between fresh and archived raw scores was 0.001186382 and the maximum was 0.006167217. ROC-AUC and trapezoidal PR-AUC use tied scores as a group. The comparison uses the published point estimates.

### Earlier fixed-input protocol

For each Java file, ML4SETK scored the original source and its five deposited token-swap neighbors. It calculated the gap between the mean of the five highest and 30 lowest next-token log probabilities, scaling these counts down for short sequences as in the FSE artifact. The raw score is the original gap minus the mean neighbor gap. The PAC evaluator uses lower raw scores as stronger membership evidence.

Using the deposited texts fixes the random swaps at the values used for the reference row. This checks model scoring and calibration for the FSE Java application of PAC. Independently sampling swaps and reproducing the original ACL WikiMIA and StackMIAsub results remain separate experiments. [Ye et al., Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.644/)

The run used two NVIDIA A40 GPUs, float16 StarCoder2-3B weights, and the checkpoint's tokenizer with an 8,192-token cap. The cap applied to 22 original files and 100 of 1,125 PAC neighbor texts. The model revision was `733247c55e3f73af49ce8e9c7949bf14af205928`. The authors' archive matched its versioned checksum and the model weights matched their Hub SHA-256. The archive supplies the exact cohort and comparison scores. Only the model-derived scores feed the fresh estimates. [Earlier fixed-input command](full_benchmark.md#repeat-the-earlier-fixed-input-pilot)
