# Training-example extraction

`ml4setk.Extraction` measures whether a model remembers a known training example. Each report evaluates a different claim about memorization. A verified suffix means that every reference token is the model’s greedy choice given the preceding reference tokens. A canary exposure is a rank in bits. Precision and recall compare which records two checkpoints memorize.

| Module and study | Published comparison | ML4SETK | Evidence |
| --- | ---: | ---: | --- |
| [exposure · Carlini et al., USENIX Security 2019](exposure/index.md) | About 8 bits after three epochs | 1.77 bits | Fresh training on 10% of Penn Treebank |
| [verbatim · Carlini et al., ICLR 2023](verbatim/index.md) | 53.6% exact 50-token continuations | 53.65% (536/999) | Fresh GPT-Neo-2.7B inference, nearest released duplication bucket |
| [predictable · Biderman et al., NeurIPS 2023](predictable/index.md) | 70M predicts 12B with precision 0.956 and recall 0.197 | 0.956335 and 0.196861 | Recomputed from the authors’ positive record IDs |

Each study has outstanding experiments. The reports give the selected cohorts, paper and toolkit values, exact commands, and coverage by figure and table.

## Installation for the reproduction scripts

From this checkout, install the toolkit in a virtual environment. The three reports use the same environment. The numerical exposure and overlap APIs use the Python standard library. The checkpoint checks additionally use PyTorch and Transformers. The recorded runs used Python 3.13 and one NVIDIA A40 per model run.

```bash
uv venv --python 3.13 /tmp/ml4setk-extraction
source /tmp/ml4setk-extraction/bin/activate
uv pip install -e . pytest==9.2.0 numpy==2.5.5 torch==2.8.0 \
  transformers==4.55.4 huggingface-hub==0.36.2 pyarrow==25.0.0
```

The two verifiers accept batches of integer IDs in the checkpoint’s vocabulary, with a common length and no padding. Both accept a local evaluation-mode model through `model=`. Passing a model uses that instance directly. The measurement returns only a Boolean for each supplied reference. For repeated batches, loading the model once avoids repeated initialization.

## Artifacts and reuse

ML4SETK ships independent implementations, synthetic unit fixtures, aggregate measurements, and original charts. The linked papers, corpora, and model weights remain external. The toolkit’s license file specifies Apache-2.0 and its distribution metadata specifies MIT. Each report identifies its external inputs and their provenance. Charts can be redrawn from the checked-in CSVs with the following command.

```bash
uv run --with matplotlib==3.11.2 python reproductions/ml4setk/Extraction/plot_reports.py
```
