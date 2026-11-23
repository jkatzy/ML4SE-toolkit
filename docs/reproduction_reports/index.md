# Reproduction reports

Reports follow the Python module path under `src/`. Each paper-backed module has its own report, comparison data, figures, and linked reproduction script.

| Source package | Module reports |
| --- | --- |
| [ml4setk.MIA](ml4setk/MIA/index.md) | [loss](ml4setk/MIA/loss/index.md) · [pac](ml4setk/MIA/pac/index.md) · [ast_pac](ml4setk/MIA/ast_pac/index.md) |

## Adding a paper

For `src/<package>/<module>.py`, put the report in `docs/reproduction_reports/<package>/<module>/index.md` and its runnable script in `reproductions/<package>/test_<module>.py`. Preserve the spelling and case of every package directory. Keep figures, data and appendices beside the report for the paper that produced the comparison. Link the report from the package index and the documentation navigation.

The deliverable is a method users can run through the installed toolkit. Include a minimal working example in the report with installation instructions, the public API call or package command, a representative input, and the output observed when running it. The paper comparisons must exercise that same entry point. Track this runnable example and the paper’s experimental coverage separately.

1. Inventory every experimental figure and table in the paper and its appendices. For each panel or table, list the models, datasets, baselines, sweep values, and repeats that produced its series, cells, and uncertainty estimates. Attribute each baseline experiment to the paper that ran it.
2. Run every listed experiment with the paper’s dedicated toolkit script. When multiple plots use the same measurements, link them to the same run. Record the command, dataset and model revisions, seeds, cohort sizes, metric conventions, and any use of the authors’ code or saved outputs.
3. Show published and measured values side by side with units and source locations. Identify theoretical predictions, fresh measurements, and results calculated from archived scores. Keep partially run panels or tables open and name the outstanding conditions.
4. Allow an exception only for a configuration that cannot fit the available hardware. Record the exact configuration, the limiting resource, available capacity, and the observed failure or calculation establishing the requirement. Run the remaining configurations that fit. Missing data, unavailable checkpoints or APIs, and unfinished runs stay pending. Close the inventory only when every entry has paired measurements or a documented hardware exception.
