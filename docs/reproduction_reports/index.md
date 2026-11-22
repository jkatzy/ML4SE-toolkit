# Reproduction reports

Each report links to one pytest file. Running that file exercises the named method and prints observed values beside their references. The reproduction suite lives in `reproductions/` so normal unit tests stay independent of model downloads.

| Report | Original paper result checked | Additional FSE evidence |
| --- | --- | --- |
| [Loss](loss.md) | Yeom et al., Figure 2b, theoretical Gaussian curve | Negative-loss ROC-AUC and PR-AUC |
| [PAC](pac.md) | Ye et al., Table 1, GPT-Neo-2.7B on original WikiMIA | Token-swap PAC on Java |
| [AST-PAC](ast_pac.md) | Koohestani et al., RQ3 companion tables, fixed AST-neighbor texts | Four models and three membership comparisons |

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

The FSE tests assert cohort coverage, agreement between the shared and method evaluators, and inclusion of fresh stratum estimates in the published 95% intervals. They print the count of exact matches at three decimals. Add `--exact-fse` to require every printed area to match and return a failing exit status for any difference. The ACL PAC script has a separate strict assertion for the printed Table 1 cell. A failing paper comparison is a reproduction result.

The archived-score audit and the earlier fresh-neighbor experiment document two other comparisons on the same FSE data. The latter used an external Java augmentation implementation for AST-PAC. [Archived-score audit](archived_scores.md) · [Historical four-model protocol](full_benchmark.md)
