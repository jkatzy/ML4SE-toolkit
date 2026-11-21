# PAC reproduction on StarCoder2-3B

**Both metrics match the reference at three decimal places.** This run generated new scores for all 225 Java files in the Mid-Low alphanumeric stratum, comparing 132 exact members with 93 nonmembers. The reference is the StarCoder2-3B row for PAC in `analysis/RQ2/rq2_table_ME_vs_NM.tex`, the companion table for Figure 1 of Koohestani et al., *AST-PAC: AST-guided Membership Inference for Code*. [FSE paper](https://doi.org/10.1145/3803437.3805588) · [Versioned replication package](https://doi.org/10.5281/zenodo.18348152)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.698 | 0.697621375 | 0.697539915 |
| PR-AUC | 0.788 | 0.788430096 | 0.788354407 |

Fresh ROC-AUC and PR-AUC round to 0.698 and 0.788. Both agree at the reference precision even though the per-file scores differ slightly.

Across the 225 paired files, the median absolute difference between fresh and archived raw scores was 0.001186382 and the maximum was 0.006167217. ROC-AUC and trapezoidal PR-AUC use tied scores as a group. The comparison uses the published point estimates.

## Experiment

For each Java file, ML4SETK scored the original source and its five deposited token-swap neighbors. It calculated the gap between the mean of the five highest and 30 lowest next-token log probabilities, scaling these counts down for short sequences as in the FSE artifact. The raw score is the original gap minus the mean neighbor gap. The PAC evaluator uses lower raw scores as stronger membership evidence.

Using the deposited texts fixes the random swaps at the values used for the reference row. This checks model scoring and calibration for the FSE Java application of PAC. Independently sampling swaps and reproducing the original ACL WikiMIA and StackMIAsub results remain separate experiments. [Ye et al., Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.644/)

The run used two NVIDIA A40 GPUs, float16 StarCoder2-3B weights, and the checkpoint's tokenizer with an 8,192-token cap. The cap applied to 22 original files and 100 of 1,125 PAC neighbor texts. The model revision was `733247c55e3f73af49ce8e9c7949bf14af205928`. The authors' archive matched its versioned checksum and the model weights matched their Hub SHA-256. The archive supplies the exact cohort and comparison scores. Only the model-derived scores feed the fresh estimates.

From the repository root in the pinned environment, run the following command. The shared instructions include the artifact download, checksum, Python dependencies, and checkpoint setup. [Reproduction environment](../membership_inference.md#repeat-the-model-run)

```bash
python scripts/reproduce_mia_stratum.py /tmp/ast-pac-fse-ivr-submission --gpus 2
```
