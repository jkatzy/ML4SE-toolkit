# AST-PAC reproduction on StarCoder2-3B

**PR-AUC matches and ROC-AUC differs from the reference at three decimal places.** This run generated new scores for all 225 Java files in the Mid-Low alphanumeric stratum, comparing 132 exact members with 93 nonmembers. The reference is the StarCoder2-3B row for AST-PAC in `analysis/RQ3/rq3_table_ME_vs_NM.tex`, the companion table for Figure 2 of Koohestani et al., *AST-PAC: AST-guided Membership Inference for Code*. [FSE paper](https://doi.org/10.1145/3803437.3805588) · [Versioned replication package](https://doi.org/10.5281/zenodo.18348152)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.610 | 0.609278267 | 0.609604106 |
| PR-AUC | 0.707 | 0.706530510 | 0.706830917 |

Fresh PR-AUC rounds to 0.707. Fresh ROC-AUC rounds to 0.609. Its difference from the archived ROC-AUC is −0.00032584, equivalent to four member–nonmember pairs out of 12,276 in the rank comparison.

Across the 225 paired files, the median absolute difference between fresh and archived raw scores was 0.000819997 and the maximum was 0.006344064. ROC-AUC and trapezoidal PR-AUC use tied scores as a group. The comparison uses the published point estimates.

## Experiment

For each Java file, ML4SETK rescored the original text and its five archived AST-guided neighbors. It calculated the mean log-probability gap between the five highest and 30 lowest next-token predictions, scaling the counts down for short texts. It subtracted the mean neighbor gap from the original gap. The evaluator treats a lower calibrated score as stronger evidence of membership.

Holding the five AST-guided permutations fixed makes the model and scoring comparison repeatable. This experiment tests the score for a published set of syntax-aware edits. Independently parsing and generating edits, and the paper's comparison across complexity levels, remain outside its scope.

The run used two NVIDIA A40 GPUs, float16 StarCoder2-3B weights, and the checkpoint's tokenizer with an 8,192-token cap. The cap applied to 22 original files and 110 of 1,125 AST-PAC neighbor texts. The model revision was `733247c55e3f73af49ce8e9c7949bf14af205928`. The authors' archive matched its versioned checksum and the model weights matched their Hub SHA-256. The archive supplies the exact cohort and comparison scores. Only the model-derived scores feed the fresh estimates.

From the repository root in the pinned environment, run the following command. The shared instructions include the artifact download, checksum, Python dependencies, and checkpoint setup. [Reproduction environment](../membership_inference.md#repeat-the-model-run)

```bash
python scripts/reproduce_mia_stratum.py /tmp/ast-pac-fse-ivr-submission --gpus 2
```
