# ml4setk.MIA reproduction reports

Each report pairs one paper’s figures or tables with measurements from ML4SETK. Follow the study link for its scope, plots, comparison data, and reproduction command. The table gives one result from each study.

| Study and comparison | Metric | Paper | ML4SETK |
| --- | --- | ---: | ---: |
| [Loss · Yeom et al., Figure 2b](loss/index.md), standard deviation ratio 8 | Theoretical / measured membership advantage | 0.583213 | 0.5832 |
| [PAC · Ye et al., Table 1](pac/index.md), GPT-Neo on original WikiMIA | ROC-AUC | 0.666 | 0.663491 |
| [AST-PAC · Koohestani et al., RQ3](ast_pac/index.md), StarCoder2-3B, Mid-Low stratum, exact members | ROC-AUC | 0.610 | 0.609604 |

## Coverage across the three papers

All three independent reproductions are partial. None has a documented hardware exception.

| Paper | Available measurements | Outstanding coverage |
| --- | --- | --- |
| [Loss inventory](loss/index.md#coverage-of-the-original-paper) | Four points on the Figure 2b theoretical curve | All empirical panels and Table I |
| [PAC inventory](pac/index.md#coverage-of-the-original-paper) | Two of 224 model-specific Table 1 AUCs and the Table 6 cohort counts | Remaining Table 1 conditions, all seven empirical figures, and other table comparisons |
| [AST-PAC inventory](ast_pac/index.md#coverage-of-the-original-paper) | All published figures and tables have historical comparisons across the benchmark. Four models also scored fixed AST edits. | Fully independent fresh AST generation and individual values for 14 fixed-neighbor comparisons |

To redraw these figures from the included CSVs, run `uv run --with matplotlib python reproductions/ml4setk/MIA/plot_reports.py` from the repository root.
