# Quantifying Memorization Across Neural Language Models

Nicholas Carlini, Daphne Ippolito, Matthew Jagielski, Katherine Lee, Florian Tramèr, and Chiyuan Zhang. ICLR 2023. [Conference paper](https://openreview.net/forum?id=TatRHT_1cK) · [Toolkit module](https://github.com/jkatzy/ML4SE-toolkit/blob/5373db3/src/ml4setk/Extraction/verbatim.py) · [Reproduction script](https://github.com/jkatzy/ML4SE-toolkit/blob/5373db3/reproductions/ml4setk/Extraction/test_verbatim.py)

## GPT-Neo-2.7B and repeated training examples

The paper reports **53.6%** exact matches for 150 tokens of context and sequences repeated about 100 times. We evaluated the final 50 tokens of each released 200-token reference on GPT-Neo-2.7B. The authors sample in duplication buckets. The nearest released bucket had a median count of 105. Taking “100” literally produces a considerably smaller cohort and a different result. [Paper, §4.2 and the comparison alongside Figure 4](https://openreview.net/pdf?id=TatRHT_1cK)

| Selection from the pinned release | Paper rate | Complete matches / valid examples | ML4SETK rate |
| --- | ---: | ---: | ---: |
| Released duplication bucket nearest 100 (zero-based block 22) | 53.6% | 536 / 999 | 53.6537% |
| Exactly 100 occurrences across the release | Unreported | 28 / 66 | 42.4242% |

One record in the 1,000-row bucket has a zero occurrence count. Following the artifact’s instructions, we excluded it. Depending on that record’s unknown outcome, the complete bucket’s rate would be between 53.6% and 53.7%. The paper leaves the bucket identifier unspecified. The second row checks sensitivity to the cohort choice and overlaps the first.

The model uses float32 evaluation on one NVIDIA A40. A full-reference forward pass checks whether every suffix token is the top choice at its preceding position. This equals exact greedy continuation agreement: before the first mismatch, the model would see the same prefix at every step. The verifier returns only agreement flags. There is no sampled decoding or random seed. [Release instructions and zero-count rule](https://github.com/google-research/google-research/tree/87e25a5ba04d2c4cf0108f0cec96d648fe2b945a/lm_memorization) · [Model revision](https://huggingface.co/EleutherAI/gpt-neo-2.7B/tree/e24fa291132763e59f4a5422741b424fb5d59056)

## Run it

After [installation](../index.md#installation-for-the-reproduction-scripts), the default uses the paper’s GPT-Neo-2.7B configuration. For another model, supply a compatible evaluation-mode causal LM and complete references encoded by its tokenizer.

```python
from transformers import AutoModelForCausalLM
from ml4setk.Extraction import verify_suffixes

rows = [[1, 2, 3, 4]]
print(verify_suffixes(rows, prefix_length=2))  # [False]
model = AutoModelForCausalLM.from_pretrained(
    "EleutherAI/gpt-neo-2.7B", revision="e24fa291132763e59f4a5422741b424fb5d59056"
).eval()
print(verify_suffixes(rows, prefix_length=2, model=model))  # [False]
```

```bash
curl -fL https://github.com/ethz-spylab/lm_memorization_data/releases/download/v1.0/data.zip -o /tmp/lm-memorization-v1.zip
ML4SETK_MEMORIZATION_ZIP=/tmp/lm-memorization-v1.zip \
  python -m pytest -o addopts= -qs reproductions/ml4setk/Extraction/test_verbatim.py
```

The script verifies the archive’s SHA-256 before use. The collaborator’s repository identifies an Apache-2.0 license. The Pile-derived records and model weights remain external. [Data release v1.0](https://github.com/ethz-spylab/lm_memorization_data/releases/tag/v1.0) · [Pinned collaborator repository](https://github.com/ethz-spylab/lm_memorization_data/tree/38d9ca77cdf38f4bed88d675d02e024ece118106)

## Coverage

The fresh run checks one quantitative comparison. Figures 1–2 and 5, and Appendix Table 1, cover broader model-size, context-length, duplication, sampling and model-overlap conditions. Figure 4 covers masked models and deduplication, and Figure 7 covers OPT. These sweeps remain open. The pinned collaborator archive has zero valid rows for lengths 350, 400, 450 and 500, preventing direct evaluation of those strata from this release. Figures 3, 6 and 8–15 present qualitative examples. The report contains aggregate rates.
