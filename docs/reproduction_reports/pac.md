# PAC reproduction report

*Data Contamination Calibration for Black-box LLMs*. Wentao Ye, Jiaqi Hu, Liyao Li, Haobo Wang, Gang Chen, and Junbo Zhao. Findings of ACL 2024. [Paper](https://doi.org/10.18653/v1/2024.findings-acl.644)

## Ye et al., Table 1 · GPT-Neo-2.7B on WikiMIA

The paper reports a ROC-AUC increase of **0.050** from perplexity to PAC. ML4SETK measured an increase of **0.047805** on the same original-text WikiMIA benchmark. The comparison pools 861 members and 789 nonmembers across the four length groups in Table 6. [Ye et al., Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.644/)

| Method | Paper ROC-AUC | ML4SETK ROC-AUC |
| --- | ---: | ---: |
| Perplexity | 0.616 | 0.615686950 |
| PAC | 0.666 | 0.663491475 |

![WikiMIA ROC-AUC for perplexity and PAC in the paper and the ML4SETK run.](figures/pac_table1.png)

The run used float32 weights, five word-swap variants per text, and the highest 5% and lowest 30% of next-token log probabilities. The script computes scores from model outputs and calls ML4SETK’s PAC and loss evaluators for ROC-AUC. It used seed 42. The authors’ realized draws were unavailable. [Table 1 comparison data (CSV)](data/pac_table1.csv) · [Dataset revision](https://huggingface.co/datasets/swj0419/WikiMIA/tree/a89ab76d88f704e9bc5870ac39cc9d458a2a70ac) · [Model revision](https://huggingface.co/EleutherAI/gpt-neo-2.7B/tree/e24fa291132763e59f4a5422741b424fb5d59056)

## Coverage of the original paper

**Partial reproduction.** The comparison above covers two of the 224 model-specific AUC values in Table 1. Each dataset has eight evaluated models, two text variants and seven methods. The mean rows and improvement percentages are derived summaries. The script also checks WikiMIA cohort counts against Table 6. The chart above visualizes the Table 1 cells. All seven empirical figures in the paper still have experiments pending. No hardware exception has been established. [Published figures, tables, and appendices](https://aclanthology.org/2024.findings-acl.644.pdf)

| Published item | Experiment or evidence | Current coverage |
| --- | --- | --- |
| Figure 1 | Diagram of the PAC method | Schematic |
| Figure 2 | Member and nonmember confidence distributions before and after calibration for davinci-002 on WikiMIA | Pending |
| Figure 3 | AUC by training exposure count, number of adjacent samples, sample length, and model size | All four sweeps pending |
| Figure 4 | Whole-sample and output-only detection after five epochs of LLaMA-13B fine-tuning on Platypus | Pending |
| Figure 5 | GPT-3 contamination estimates for selected TOXIGEN examples | Pending |
| Figure 6 | Detection score and sentiment on WikiMIA and StackMIA | Pending |
| Figure 7 | WikiMIA AUC by model, method, and text length | Per-length series pending. Only the pooled GPT-Neo perplexity and PAC values are available from the Table 1 run. |
| Figure 8 | StackMIAsub AUC by model, method, and text length | Pending. The panel labels include davinci-002 and babbage-002, whose StackMIAsub cells in Table 1 are blank. |
| Table 1 | Detection AUC across models, methods, datasets, and original or rewritten inputs | Two cells measured. The remaining published cells are pending. |
| Table 2 | Five augmentation settings and five score choices on each dataset | Both ablations pending |
| Table 3 | Threshold selection on subsets from 10% to 50% in five-percentage-point steps | Accuracy and threshold variability pending |
| Table 4 | Four GPT models on GSM8K, AQuA, and TOXIGEN | Pending |
| Table 5 | StackMIAsub composition by length and membership | Pending |
| Table 6 | WikiMIA composition by length and membership | All four groups independently counted below |
| Table 7 | Examples of original and rewritten texts | Qualitative examples. Rewrite comparison pending. |

### Table 6 cohort check

The reproduction script checks the labels in the pinned original-text files before it loads the model. Counts below are in members / nonmembers. [Dataset revision](https://huggingface.co/datasets/swj0419/WikiMIA/tree/a89ab76d88f704e9bc5870ac39cc9d458a2a70ac) · [Run the check](#reproduce-these-measurements)

| Text length | Paper | Counted |
| --- | ---: | ---: |
| 32 | 387 / 389 | 387 / 389 |
| 64 | 284 / 258 | 284 / 258 |
| 128 | 139 / 111 | 139 / 111 |
| 256 | 51 / 31 | 51 / 31 |
| Total | 861 / 789 | 861 / 789 |

## Reproduce these measurements

Run from the repository root with a CUDA GPU. The script downloads the pinned WikiMIA texts and GPT-Neo checkpoint on first use. [Reproduction script](https://github.com/jkatzy/ML4SE-toolkit/blob/2e976ea/reproductions/test_pac.py)

```bash
uv venv --python 3.13 /tmp/ml4setk-repro
uv pip install --python /tmp/ml4setk-repro/bin/python -e . pytest==9.0.2 \
  torch==2.8.0 transformers==4.55.4 pandas==3.0.6 pyarrow==25.0.0 numpy==2.5.5
/tmp/ml4setk-repro/bin/python -m pytest -o addopts= -qs reproductions/test_pac.py
```
