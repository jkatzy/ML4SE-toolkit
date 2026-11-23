# Reproduction reports

Each report pairs one paper’s figures or tables with measurements from ML4SETK. Follow the study link for its scope, plots, comparison data, and reproduction command. The table gives one result from each study.

| Study and comparison | Metric | Paper | ML4SETK |
| --- | --- | ---: | ---: |
| [Loss · Yeom et al., Figure 2b](loss.md), standard deviation ratio 8 | Theoretical / measured membership advantage | 0.583213 | 0.5832 |
| [PAC · Ye et al., Table 1](pac.md), GPT-Neo on original WikiMIA | ROC-AUC | 0.666 | 0.663491 |
| [AST-PAC · Koohestani et al., RQ3](ast_pac.md), StarCoder2-3B, Mid-Low stratum, exact members | ROC-AUC | 0.610 | 0.609604 |

## Adding a paper

1. Inventory every experimental figure and table in the paper and its appendices. For each panel or table, list the models, datasets, baselines, sweep values, and repeats that produced its series, cells, and uncertainty estimates. Attribute each baseline experiment to the paper that ran it.
2. Run every listed experiment with the paper’s dedicated toolkit script. When multiple plots use the same measurements, link them to the same run. Record the command, dataset and model revisions, seeds, cohort sizes, metric conventions, and any use of the authors’ code or saved outputs.
3. Show published and measured values side by side with units and source locations. Identify theoretical predictions, fresh measurements, and results calculated from archived scores. Keep partially run panels or tables open and name the outstanding conditions.
4. Allow an exception only for a configuration that cannot fit the available hardware. Record the exact configuration, the limiting resource, available capacity, and the observed failure or calculation establishing the requirement. Run the remaining configurations that fit. Missing data, unavailable checkpoints or APIs, and unfinished runs stay pending. Close the inventory only when every entry has paired measurements or a documented hardware exception.

To redraw these figures from the included CSVs, run `uv run --with matplotlib python reproductions/plot_reports.py` from the repository root.
