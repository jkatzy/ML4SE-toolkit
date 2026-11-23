# Reproduction reports

Each report pairs one paper’s figures or tables with measurements from ML4SETK. Follow the study link for its scope, plots, comparison data, and reproduction command. The table gives one result from each study.

| Study and comparison | Metric | Paper | ML4SETK |
| --- | --- | ---: | ---: |
| [Loss · Yeom et al., Figure 2b](loss.md), standard deviation ratio 8 | Theoretical / measured membership advantage | 0.583213 | 0.5832 |
| [PAC · Ye et al., Table 1](pac.md), GPT-Neo on original WikiMIA | ROC-AUC | 0.666 | 0.663491 |
| [AST-PAC · Koohestani et al., RQ3](ast_pac.md), StarCoder2-3B, Mid-Low stratum, exact members | ROC-AUC | 0.610 | 0.609604 |

## Adding a paper

1. Identify the original claim, figure or table, and the inputs and metric needed to reproduce it. Attribute a baseline experiment to the paper that ran it.
2. Link a dedicated script that runs the toolkit on that paper’s inputs. Record dataset and model revisions, seeds, cohort sizes, metric conventions, and any use of the authors’ code or saved outputs.
3. Show the published and measured values side by side with units and source locations. Distinguish theoretical predictions, measurements from fresh inputs, and evaluations of archived scores. Identify untested claims and missing measurements.

To redraw these figures from the included CSVs, run `uv run --with matplotlib python reproductions/plot_reports.py` from the repository root.
