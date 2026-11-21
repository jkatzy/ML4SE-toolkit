# Loss reproduction on StarCoder2-3B

## Shared API run from original source

On all 225 files in the StarCoder2-3B Mid-Low exact-member comparison, the shared scorer interface and evaluator produced the following results. The experiment implemented the public scorer contract, passed Java source to inherited `score_many`, and evaluated its higher-is-member outputs with `evaluate_membership_scores`.

| Metric | Shared API | Scikit-learn on the same scores | FSE reference |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.621456500 | 0.621456500 | 0.622 |
| PR-AUC | 0.699859994 | 0.699859994 | 0.700 |

PR-AUC agrees at the published precision. ROC-AUC falls just below the rounding boundary. Both independent metric checks agree within an absolute tolerance of `1e-12`. The complete four-model protocol specifies the cohort, model revisions, and fresh-neighbor seed. [Shared API protocol](full_benchmark.md)

## Earlier fixed-input comparison

**PR-AUC matches and ROC-AUC differs from the reference at three decimal places.** This run generated new scores for all 225 Java files in the Mid-Low alphanumeric stratum, comparing 132 exact members with 93 nonmembers. The reference is the StarCoder2-3B row for Loss in `analysis/RQ2/rq2_table_ME_vs_NM.tex`, the companion table for Figure 1 of Koohestani et al., *AST-PAC: AST-guided Membership Inference for Code*. [FSE paper](https://doi.org/10.1145/3803437.3805588) · [Versioned replication package](https://doi.org/10.5281/zenodo.18348152)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.622 | 0.621456500 | 0.621537960 |
| PR-AUC | 0.700 | 0.699859994 | 0.699899829 |

Fresh PR-AUC rounds to 0.700. Fresh ROC-AUC rounds to 0.621. Its difference from the archived ROC-AUC is −0.00008146, equivalent to one member–nonmember pair out of 12,276 in the rank comparison.

Across the 225 paired files, the median absolute difference between fresh and archived raw scores was 0.000066843 and the maximum was 0.001034659. ROC-AUC and trapezoidal PR-AUC use tied scores as a group. The comparison uses the published point estimates.

## Experiment

For each original Java file, ML4SETK computed the mean log probability of the observed next tokens. It applied a float32 log-softmax to the model's logits and accumulated the selected values in float64. Higher scores favor membership. This tests the negative cross-entropy baseline that Koohestani et al. use for code. The earlier CSF experiments use a different setting and remain outside this comparison. [Yeom et al., CSF 2018](https://doi.org/10.1109/CSF.2018.00027) · [Carlini et al., USENIX Security 2021](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting)

The run used two NVIDIA A40 GPUs, float16 StarCoder2-3B weights, and the checkpoint's tokenizer with an 8,192-token cap. The cap applied to 22 original files. The model revision was `733247c55e3f73af49ce8e9c7949bf14af205928`. The authors' archive matched its versioned checksum and the model weights matched their Hub SHA-256. The archive supplies the exact cohort and comparison scores. Only the model-derived scores feed the fresh estimates.

From the repository root in the pinned environment, run the following command. The shared instructions include the artifact download, checksum, Python dependencies, and checkpoint setup. [Reproduction environment](../membership_inference.md#repeat-the-model-run)

```bash
python scripts/reproduce_mia_stratum.py /tmp/ast-pac-fse-ivr-submission --gpus 2
```
