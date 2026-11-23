# Loss reproduction report

## Yeom et al., Figure 2b · Membership advantage

As the population standard deviation increases from one to eight times the training standard deviation, the paper’s theoretical membership advantage rises from 0 to 0.583213. The toolkit gives 0 to 0.5832. The line is the Gaussian curve from Figure 2b of *Privacy Risk in Machine Learning*. The four points come from applying ML4SETK’s loss threshold to 10,000 deterministic Gaussian quantiles per cohort. The empirical results for trained regression and tree models are outside this run. [Yeom et al., CSF 2018](https://par.nsf.gov/servlets/purl/10060215)

![The theoretical advantage curve through ratios one to eight, overlaid with the four ML4SETK measurements.](figures/loss_figure2b.png)

| Population / training standard deviation | Paper advantage (theory) | ML4SETK advantage |
| ---: | ---: | ---: |
| 1 | 0.000000 | 0.0000 |
| 2 | 0.299765 | 0.2996 |
| 4 | 0.485277 | 0.4852 |
| 8 | 0.583213 | 0.5832 |

[Figure 2b comparison data (CSV)](data/loss_figure2b.csv)

## FSE Table 1 · Negative loss on Java

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

## RQ2 · Exact members in the Mid-Low alphanumeric stratum

The pilot independently scored all 132 exact members and 93 nonmembers in this stratum. The reference columns come from the RQ2 companion table.

| Model | Reference ROC-AUC | ML4SETK ROC-AUC | Reference PR-AUC | ML4SETK PR-AUC |
| --- | ---: | ---: | ---: | ---: |
| StarCoder2-3B | 0.622 | 0.621619 | 0.700 | 0.699924 |
| StarCoder2-7B | 0.645 | 0.645080 | 0.717 | 0.716864 |
| Mellum-4B | 0.620 | 0.620479 | 0.684 | 0.684496 |
| SmolLM3-3B | 0.530 | 0.530140 | 0.605 | 0.605098 |

### Earlier StarCoder2-3B control

The earlier 225-file run used a different model forward call. The last column recomputes areas from the authors’ saved scores. [Forward-pass control and earlier command](full_benchmark.md#forward-pass-control)

| Metric | FSE companion table | Run with fresh model scores | Evaluator on archived scores |
| --- | ---: | ---: | ---: |
| ROC-AUC | 0.622 | 0.621456500 | 0.621537960 |
| PR-AUC | 0.700 | 0.699859994 | 0.699899829 |

## Reproduce these measurements

[Reproduction script](https://github.com/jkatzy/ML4SE-toolkit/blob/1293774/reproductions/test_loss.py) · [Environment and inputs](index.md)

```bash
/tmp/ml4setk-repro/bin/python -m pytest -o addopts= -qs reproductions/test_loss.py
```
