# Reproduction agent

Use this role to run, extend, or audit a paper reproduction for any module
under `src/ml4setk/`. Start with the original paper and the owning source
module. The same role applies when the task starts at a reproduction script,
a report, or an individual figure. A completed reproduction delivers a method
that a user can run from an installed ML4SE-TK package on their own inputs.

1. Find the module’s report and runnable script using the
   [report layout and coverage rules](../../docs/reproduction_reports/index.md#adding-a-paper).
   Use the owning module’s API documentation for its inputs, conventions, and
   metrics. Identify the public entry point that runs the paper's method. If
   essential logic exists only in a notebook or benchmark script, implement
   it under `src/ml4setk/` using the [implementation workflow](implementation.md),
   then resume the reproduction. Use that same public entry point in the
   reproduction script for the paper comparisons.
2. Inventory the paper’s figures, tables, and appendices. Run each experiment
   that fits the available hardware using the toolkit. Attribute baselines to
   the paper that evaluated them. Record the exact command and pair the
   published values with the observed measurements for each configuration.
3. When auditing an existing report, trace its numbers to the run outputs
   and check which panels and conditions the linked script covers. Distinguish
   fresh measurements, calculations on archived outputs, and results that
   depend on the authors’ implementation.
4. Publish the report, script link, figures, and comparison data at the module
   paths specified in the coverage rules. Record any verified hardware limit
   for the affected configuration. Leave unfinished experiments pending.
5. Before marking the reproduction complete, install the toolkit with the
   documented dependencies and run the public entry point on a representative
   input outside the test harness. Put the exact invocation, input or input
   reference, and observed output in the report so a user can repeat it.
   When auditing, record package runnability and paper coverage separately.

The [MIA reports](../../docs/reproduction_reports/ml4setk/MIA/index.md)
show how one package uses this shared role for three independent papers.
