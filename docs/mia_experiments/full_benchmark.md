# Full FSE benchmark through the shared scoring API

This experiment tests whether a benchmark implementation of `MembershipScorer` can score Java source through `score_many`, whether the shared and method-specific evaluators agree, and how accurately fresh measurements recover the FSE results. The reference study is Roham Koohestani, Ali Al-Kaswan, Jonathan Katzy, and Maliheh Izadi, *AST-PAC: AST-guided Membership Inference for Code*, FSE Companion 2026. [Proceedings paper](https://doi.org/10.1145/3803437.3805588) · [Versioned replication package](https://doi.org/10.5281/zenodo.18348152)

## Protocol

For each of the four models, the notebooks' complete-case filter selects 12,422 of the 12,423 recorded observations. The runner joins their identifiers to `dataset/full.parquet` using ID, repository, path, and membership type. Each model sees 4,193 exact members, 4,014 near-members, and 4,215 nonmembers. The artifact supplies cohort selection and reference values. The new scoring path receives the original source and locally generated neighbors.

The experiment adapter implements `score(model, source)`. The inherited `score_many` dispatches each source in order. Loss returns mean next-token log probability. PAC and AST-PAC return the mean neighbor polarized gap minus the original gap, giving the joint API its higher-is-member convention. The method-specific evaluators for archived PAC data take the opposite sign. Each model runs in evaluation mode, with float16 weights, scaled dot-product attention, and the artifact's 8,192-token cap. The original source and all five neighbors per perturbation method are tokenized independently.

For each file the experiment derives a seed from the first eight bytes of the SHA-256 digest of its UTF-8 contents, interpreted as an unsigned big-endian integer. PAC uses the model tokenizer and the artifact's token-swap sampling rule. AST-PAC calls the external authors' Java augmentation function with that seed. The authors' draw sequence was unavailable. A difference in the final paper cells can arise even when two implementations of the metrics agree on identical inputs.

| Model | Pinned checkpoint and tokenizer |
| --- | --- |
| StarCoder2-3B | [733247c](https://huggingface.co/bigcode/starcoder2-3b/tree/733247c55e3f73af49ce8e9c7949bf14af205928) |
| StarCoder2-7B | [bb9afde](https://huggingface.co/bigcode/starcoder2-7b/tree/bb9afde76d7945da5745592525db122d4d729eb1) |
| Mellum-4B | [83cce26](https://huggingface.co/JetBrains/Mellum-4b-base/tree/83cce2605fbdf6a3868627e9b0a5924e0072b94d) |
| SmolLM3-3B | [a07cc9a](https://huggingface.co/HuggingFaceTB/SmolLM3-3B/tree/a07cc9a04f16550a088caea529712d1d335b0ac1) |

## Comparisons

- **API agreement.** For each eligible aggregate and stratified comparison, the analysis checks both API outputs against scikit-learn's ROC-AUC and trapezoidal PR-AUC, with absolute tolerance `1e-12`. For the RQ1 threshold metrics, it selects Youden's cutoff as in the notebook and checks `MembershipThreshold.predict_many` against the inclusive array comparison.
- **Table 1 and RQ1.** Compare the 48 aggregate area estimates for PAC and Loss to the final PDF at three decimals. Compare areas, accuracy, precision, recall, and F1 to the saved RQ1 notebook at six decimals.
- **Table 2.** Check the ten dataset cutoffs using the complete 12,484-row input dataset.
- **RQ2 and RQ3.** Check the full set of eligible strata across three membership scenarios and three grouping dimensions. Compare all 1,152 area estimates in the six deposited tables at three decimals. PAC appears in both comparisons. Compute 95% percentile intervals with 1,000 row-wise bootstrap resamples, using seed 42. The authors' unseeded intervals are stochastic.
- **Figure 3.** Recompute the 72 median and quartile values for the PAC and AST-PAC character change ratios from newly generated neighbors. Compare to the saved RQ3 notebook at six decimals.

As an analysis control, feeding the authors' saved scores and ratios into the same evaluator reproduced all 1,152 stratified point estimates, 144 RQ1 notebook metrics, and 72 Figure 3 statistics. The two discrepancies in printed Table 1 were the previously documented StarCoder2-7B PAC cells. [Archived-score comparison](../mia_reproduction_report.md)

## Repeat the run

Use Python 3.13, a CUDA-capable GPU, and Poppler's `pdftotext`. From the repository root, extract the **entire** Zenodo archive after checking its MD5 (`2f137cfa98c98f1088d9454485840283`). Download the final proceedings PDF. The external Java augmentation dependency is `attacks/pac_ast_attack.py` in the pinned CC BY 4.0 deposit. ML4SETK imports it from the extracted artifact. The dependency, Java corpus, checkpoints, and per-file results remain external to the distribution. [Artifact and license](https://doi.org/10.5281/zenodo.18348152) · [Proceedings PDF](https://repository.tudelft.nl/file/File_af66d741-b167-4406-9bc1-7f4474f47fed)

```bash
uv venv --python 3.13 /tmp/fse-api-env
uv pip install --python /tmp/fse-api-env/bin/python -e . \
    torch==2.8.0 transformers==4.55.4 numpy==2.5.5 pandas==3.0.6 \
    pyarrow==25.0.0 scikit-learn==1.9.1 tree-sitter==0.25.2 \
    tree-sitter-java==0.23.5 Levenshtein==0.27.3 lxml==6.1.3
artifact=/tmp/ast-pac-fse-ivr-submission
output=tmp/mia_full_api
for model in SC2-3B SC2-7B mellum smollm; do
    /tmp/fse-api-env/bin/python scripts/run_fse_api_benchmark.py "$artifact" "$output" "$model" || exit 1
done
/tmp/fse-api-env/bin/python scripts/evaluate_fse_api_benchmark.py "$artifact" /tmp/paper.pdf "$output"
```

Each model saves completed batches in a separate SQLite file in the output directory. Repeating a command there resumes that run. An empty output directory starts a new experiment. The analysis requires complete per-model cohort coverage and writes one aggregate comparison CSV per model.
