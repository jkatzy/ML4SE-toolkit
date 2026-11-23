# Reproduction reports

Each report opens with the original study’s figure or table and the corresponding ML4SETK measurements. The plots use published values, saved observations, and labeled axes. The linked CSVs provide the numbers for reuse.

| Study and comparison | Metric | Paper | ML4SETK |
| --- | --- | ---: | ---: |
| [Loss · Yeom et al., Figure 2b](loss.md), standard deviation ratio 8 | Theoretical / measured membership advantage | 0.583213 | 0.5832 |
| [PAC · Ye et al., Table 1](pac.md), GPT-Neo on original WikiMIA | ROC-AUC | 0.666 | 0.663491 |
| [AST-PAC · Koohestani et al., RQ3](ast_pac.md), StarCoder2-3B, Mid-Low stratum, exact members | ROC-AUC | 0.610 | 0.609604 |

The reports also link to their individual pytest scripts. The four-model FSE comparison includes a plot and downloadable paired values for every measured stratum in the earlier benchmark. [FSE plots and comparison tables](full_benchmark.md#four-model-results)

## Run a reproduction

From the repository root, install the reproduction dependencies. The GPU checks use CUDA. The Loss theory check runs on CPU with just the toolkit and pytest. The model and dataset loaders use pinned Hub revisions.

```bash
uv venv --python 3.13 /tmp/ml4setk-repro
uv pip install --python /tmp/ml4setk-repro/bin/python -e . pytest==9.0.2 \
  torch==2.8.0 transformers==4.55.4 pandas==3.0.6 pyarrow==25.0.0 numpy==2.5.5
```

For the FSE tests, download the archive and final paper. Extract the data and tables only. Run the following commands in a fresh directory for the external inputs.

```bash
curl -fL https://zenodo.org/api/records/18348152/files/ast-pac-fse-ivr-submission.zip/content -o fse.zip
echo '2f137cfa98c98f1088d9454485840283  fse.zip' | md5sum -c -
unzip -q fse.zip '*/dataset/full.parquet' '*/results/*_m_worker_0.parquet' '*/analysis/RQ[23]/*.tex'
curl -fL https://repository.tudelft.nl/file/File_af66d741-b167-4406-9bc1-7f4474f47fed -o fse.pdf
export ML4SETK_AST_PAC_ARTIFACT="$PWD/ast-pac-fse-ivr-submission"
export ML4SETK_FSE_PDF="$PWD/fse.pdf"
```

Back at the repository root, run the command in the method report. The full FSE entry points score all 12,422 complete cases per model. Table 1 comparison uses Poppler’s `pdftotext`. For a shorter run, add `--fse-pilot` to score the published 225-file exact-member Mid-Low stratum on each model. Add `--fse-model SC2-3B` to select one model.

To redraw the report plots from the included aggregate CSVs, run `uv run --with matplotlib python reproductions/plot_reports.py` from the repository root. Model inference is only needed to generate new measurements.

The reproduction tests also check cohort coverage, evaluator agreement, and the paper comparisons using the project’s 1% relative tolerance. The reports display the measurements directly.

The archived-score audit and the earlier fresh-neighbor experiment document two other comparisons on the same FSE data. The latter used an external Java augmentation implementation for AST-PAC. [Archived-score audit](archived_scores.md) · [Historical four-model protocol](full_benchmark.md)
