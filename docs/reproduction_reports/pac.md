# PAC reproduction report

## Ye et al., Table 1 · GPT-Neo-2.7B on WikiMIA

The paper reports a ROC-AUC increase of **0.050** from perplexity to PAC. ML4SETK measured an increase of **0.047805** on the same original-text WikiMIA benchmark. The comparison pools 861 members and 789 nonmembers across the four length groups in Table 6. [Ye et al., Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.644/)

| Method | Paper ROC-AUC | ML4SETK ROC-AUC |
| --- | ---: | ---: |
| Perplexity | 0.616 | 0.615686950 |
| PAC | 0.666 | 0.663491475 |

![WikiMIA ROC-AUC for perplexity and PAC in the paper and the ML4SETK run.](figures/pac_table1.png)

The run used float32 weights, five word-swap variants per text, and the highest 5% and lowest 30% of next-token log probabilities. ML4SETK used seed 42. The authors’ realized draws were unavailable. [Table 1 comparison data (CSV)](data/pac_table1.csv) · [Dataset revision](https://huggingface.co/datasets/swj0419/WikiMIA/tree/a89ab76d88f704e9bc5870ac39cc9d458a2a70ac) · [Model revision](https://huggingface.co/EleutherAI/gpt-neo-2.7B/tree/e24fa291132763e59f4a5422741b424fb5d59056)

## FSE Table 1 · Token-swap PAC on Java

Table 1 compares exact members (4,193), near-members (4,014), and both groups combined with the same 4,215 nonmembers. Each model scored the same 12,422 Java files. PR-AUC uses trapezoidal integration. [FSE Table 1](https://doi.org/10.1145/3803437.3805588) · [Companion tables](https://doi.org/10.5281/zenodo.18348152)

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

## RQ2 · Exact members in the Mid-Low alphanumeric stratum

The pilot independently scored all 132 exact members and 93 nonmembers in this stratum. The reference columns come from the RQ2 companion table.

| Model | Reference ROC-AUC | ML4SETK ROC-AUC | Reference PR-AUC | ML4SETK PR-AUC |
| --- | ---: | ---: | ---: | ---: |
| StarCoder2-3B | 0.698 | 0.703649 | 0.788 | 0.790301 |
| StarCoder2-7B | 0.717 | 0.719616 | 0.811 | 0.812720 |
| Mellum-4B | 0.726 | 0.730368 | 0.809 | 0.812511 |
| SmolLM3-3B | 0.627 | 0.625204 | 0.714 | 0.703676 |

### Earlier StarCoder2-3B control

The earlier 225-file run used a different model forward call. The last column recomputes areas from the authors’ saved scores. [Forward-pass control and earlier command](full_benchmark.md#forward-pass-control)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.698 | 0.697621375 | 0.697539915 |
| PR-AUC | 0.788 | 0.788430096 | 0.788354407 |

## Reproduce these measurements

[Reproduction script](https://github.com/jkatzy/ML4SE-toolkit/blob/1293774/reproductions/test_pac.py) · [Environment and inputs](index.md)

```bash
/tmp/ml4setk-repro/bin/python -m pytest -o addopts= -qs reproductions/test_pac.py
```
