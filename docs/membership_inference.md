# Membership inference

`ml4setk.MIA` provides a shared model-and-source scoring interface and
evaluates scores for examples with known training membership. The FSE
benchmark adapter implements this interface for Loss, PAC, and AST-PAC.

## Reproduction reports

Each report pairs an original paper’s results with ML4SETK measurements and links to the script and inputs for that study.

- [Yeom et al. (CSF 2018), loss threshold and the Figure 2b theoretical curve](reproduction_reports/ml4setk/MIA/loss/index.md)
- [Shi et al. (ICLR 2024), Min-K% Prob on WikiMIA](reproduction_reports/ml4setk/MIA/min_k/index.md)
- [Ye et al. (Findings of ACL 2024), PAC and perplexity on WikiMIA](reproduction_reports/ml4setk/MIA/pac/index.md)
- [Koohestani et al. (FSE Companion 2026), AST-PAC and both Java baselines](reproduction_reports/ml4setk/MIA/ast_pac/index.md)

## Shared scoring API

Subclass `ml4setk.MIA.MembershipScorer` and implement
`score(model, source: str) -> float`. The source string holds one file's
complete contents. The caller supplies the model together with any tokenizer
the method needs. Method-specific settings belong on the scorer instance.
Return a finite score with higher values indicating stronger evidence of
membership.

The inherited `score_many(model, sources)` calls `score` once per file and
returns a list in input order, including duplicates. It accepts generators
and dataset columns such as `dataset["content"]`. An empty iterable produces
an empty list. A method with native batching can override `score_many` while
preserving these semantics.

`MembershipThreshold` applies an explicit inclusive cutoff to scores in
this orientation. For benchmark comparisons, choose the cutoff on a separate
calibration split and use the same value on the evaluation split.

```python
from ml4setk.MIA import MembershipThreshold

rule = MembershipThreshold(cutoff=0.3)
rule.predict_many([0.4, 0.2, 0.3])  # [True, False, True]
```

## Recorded-score evaluators

The three paper-specific functions below accept their respective raw archive
values. The PAC and AST-PAC archive columns use the opposite direction to
the shared scorer contract.

| Method | Benchmark input | Entry point |
| --- | --- | --- |
| AST-PAC | Recorded `pac_ast_score` | `evaluate_ast_pac_scores` |
| PAC | Recorded `pac_score` | `evaluate_pac_scores` |
| Loss | Recorded `loss_score` (negative loss) | `evaluate_loss_scores` |

```python
from ml4setk.MIA import evaluate_ast_pac_scores

# Illustrative recorded scores for two known cohorts.
result = evaluate_ast_pac_scores(members=[0.1, 0.3], nonmembers=[0.2, 0.4])
print(result.roc_auc, result.n_members, result.n_nonmembers)  # 0.75 2 2
```

Pass finite scores from one model and comparison at a time. Each cohort must
have at least one observation. The entry points handle the archived score
directions. For another benchmark with higher scores favoring membership,
use `evaluate_membership_scores` directly. Tied scores enter the curves
together. PR-AUC uses trapezoidal integration, starting at recall zero and
precision one. The returned values are point estimates.

## AST-PAC

Roham Koohestani, Ali Al-Kaswan, Jonathan Katzy, and Maliheh Izadi.
“AST-PAC: AST-guided Membership Inference for Code.” *FSE Companion 2026*,
Ideas, Visions and Reflections, pp. 1361–1365. The authors compare a
syntax-aware variant of PAC with two existing baselines. [Conference paper](https://doi.org/10.1145/3803437.3805588)

**Reproduction.** The entry evaluates the raw scores from the authors' RQ3
notebook. Across the 12 reported StarCoder2-3B strata for exact members versus
nonmembers, both area estimates match the archived table to three decimal
places. For example, the complex-files stratum yields ROC-AUC 0.638 and
PR-AUC 0.603 for 1,063 members and 1,189 nonmembers. The observed agreement
covers the archived scores and point estimates. A separate report checks fresh model scores on the deposited neighbor texts. [AST-PAC reproduction report](reproduction_reports/ml4setk/MIA/ast_pac/index.md) · [Versioned replication package, deposited by Roham Koohestani](https://doi.org/10.5281/zenodo.18348152)

**Rights and reuse.** The final paper and the Zenodo software deposit each
declare CC BY 4.0. The ZIP contains no separate LICENSE, COPYING, or NOTICE
entry. Its README and the AST-PAC source file contain no separate license
declaration. ML4SETK's evaluator is independently written. The optional test
reads external scores and a results table. The source code, datasets, model
outputs, and notebooks from the deposit are not bundled. Direct redistribution
of covered material would require attribution, a license link and change
indications where applicable. The deposit's grant extends only to rights its
licensor can grant. [Paper and rights](https://research.tudelft.nl/en/publications/ast-pac-ast-guided-membership-inference-for-code/) · [Software rights record](https://api.datacite.org/dois/10.5281/zenodo.18348152) · [CC BY 4.0 terms](https://creativecommons.org/licenses/by/4.0/)

## Min-K% Prob

Weijia Shi, Anirudh Ajith, Mengzhou Xia, Yangsibo Huang, Daogao Liu, Terra Blevins, Danqi Chen, and Luke Zettlemoyer introduced Min-K% Prob in *Detecting Pretraining Data from Large Language Models*, ICLR 2024. Ye et al. later evaluated it as a baseline for PAC. [Original paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e32ad85fa27be4a9868d55703f01323e-Abstract-Conference.html) · [PAC paper](https://aclanthology.org/2024.findings-acl.644/)

Pass one example’s observed-token natural log probabilities, omitting padding and positions without a prediction. The function returns the mean of the lowest k percent, with a higher score favoring membership. It defaults to the paper’s 20%. Use `evaluate_membership_scores` to compare scores from labeled cohorts. [Min-K% reproduction report](reproduction_reports/ml4setk/MIA/min_k/index.md)

```python
from ml4setk.MIA import min_k_score

log_probs = [-0.25, -4, -0.5, -2, -1, -0.75, -3, -1.5, -0.1, -0.8]
print(min_k_score(log_probs))  # -3.5
```

**Rights and reuse.** ML4SETK implements Equation 1 independently. The unit fixtures are original synthetic values. The authors’ Apache-2.0 repository supplies the rounding and evaluation conventions. The toolkit license file declares Apache-2.0 and its distribution metadata declares MIT. This addition ships original code, original plots, and aggregate comparisons. The reproduction fetches WikiMIA (dataset card: MIT) and Pythia-2.8B (model card: Apache-2.0) externally. [Pinned authors’ code and license](https://github.com/swj0419/detect-pretrain-code/tree/a5048f93c4fa6491aab0638bb3e6fd5a662d7698) · [Dataset card](https://huggingface.co/datasets/swj0419/WikiMIA/blob/a89ab76d88f704e9bc5870ac39cc9d458a2a70ac/README.md) · [Model card](https://huggingface.co/EleutherAI/pythia-2.8b/blob/2a259cdd96a4beb1cdf467512e3904197345f6a9/README.md)

## PAC baseline

Wentao Ye, Jiaqi Hu, Liyao Li, Haobo Wang, Gang Chen, and Junbo Zhao.
“Data Contamination Calibration for Black-box LLMs.” *Findings of ACL 2024*,
pp. 10845–10861. This is the source of Polarized Augment Calibration.
[Original paper](https://doi.org/10.18653/v1/2024.findings-acl.644)

**Reproduction.** The PAC entry evaluates the recorded scores in the AST-PAC
study. Lower raw PAC scores favor membership. The three StarCoder2-3B
comparisons agree with both metrics in Table 1 at the printed precision.
The separate reproduction report checks Ye et al.’s original GPT-Neo row on WikiMIA. The pinned PAC repository contains no
saved score file, and the linked StackMIAsub benchmark provides snippets and
labels. [PAC reproduction report](reproduction_reports/ml4setk/MIA/pac/index.md) · [FSE evaluation](https://doi.org/10.1145/3803437.3805588) · [Original benchmark revision](https://huggingface.co/datasets/darklight03/StackMIAsub/tree/c87c55d8b93fcf525fbf5fbf9b3bff6808b30ac6)

**Rights and reuse.** The authors' PAC repository carries MIT, copyright
2024 Wentao Ye, at commit `79c6eca`. The MIT terms permit incorporation
under either of ML4SETK's current license declarations if its copyright
and permission notices accompany copies or substantial portions. This entry
uses original toolkit code and reads the FSE deposit's scores externally.
[Pinned PAC license](https://github.com/yyy01/PAC/blob/79c6eca14fed3a64a7a4201cdca263de52501dae/LICENSE)

## Loss baseline

Samuel Yeom, Irene Giacomelli, Matt Fredrikson, and Somesh Jha.
“Privacy Risk in Machine Learning: Analyzing the Connection to Overfitting.”
*IEEE Computer Security Foundations Symposium*, 2018, pp. 268–282.
[Original paper](https://doi.org/10.1109/CSF.2018.00027)

For the language-model setting, AST-PAC §2.1 also credits Nicholas Carlini,
Florian Tramèr, Eric Wallace, Matthew Jagielski, Ariel Herbert-Voss,
Katherine Lee, Adam Roberts, Tom Brown, Dawn Song, Úlfar Erlingsson,
Alina Oprea, and Colin Raffel. “Extracting Training Data from Large Language
Models.” *USENIX Security 2021*. [Proceedings](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting)

**Reproduction.** The Loss entry accepts the FSE artifact's signed
`loss_score`. The three StarCoder2-3B comparisons agree with both metrics
in Table 1 at the printed precision. This verifies the FSE benchmark's use of
Loss. The separate reproduction report checks the theoretical curve in Yeom et al.’s Figure 2b. The empirical private-data extraction experiment in the 2021 paper remains outside its scope.
Yeom's pinned repository contains experiment scripts and input data. Its
README describes generating the result files locally. [Loss reproduction report](reproduction_reports/ml4setk/MIA/loss/index.md) · [FSE evaluation](https://doi.org/10.1145/3803437.3805588) · [CSF artifact README](https://github.com/sam-yeom/ml-privacy-csf18/blob/7b302fb80b853b040941eb90b37c0491f55e4928/README.md)

**Rights and reuse.** Yeom's CSF artifact carries MIT, copyright 2019 Samuel
Yeom, at commit `7b302fb`. The same MIT notice obligations apply to reuse of
that code. Both Loss papers receive scholarly credit. This implementation
incorporates no code or data from either original study.
[Pinned CSF artifact license](https://github.com/sam-yeom/ml-privacy-csf18/blob/7b302fb80b853b040941eb90b37c0491f55e4928/LICENSE)

## Reproduce the checks

With the `datasets` extra installed, point `ML4SETK_AST_PAC_ARTIFACT` at the
directory containing `results/` and `analysis/` in the Zenodo archive.
Only two archived files are needed for the comparison.

- `results/results_sc2_3b_new_approach_orig_m_worker_0.parquet`
- `analysis/RQ3/rq3_table_ME_vs_NM.tex`

```bash
ML4SETK_AST_PAC_ARTIFACT=/path/to/ast-pac-fse-ivr-submission \
  uv run --extra datasets pytest tests/test_ast_pac_artifact.py -q --no-cov
```

The baseline tests check all members, exact members, and near members against
the nonmember cohort. The AST-PAC test checks the exact-member comparison by
file size, alphanumeric ratio, and AST node count. A stratum containing only
one class has no ROC-AUC. The small unit tests run independently of the
archive in `tests/test_mia_evaluation.py`.

**Toolkit licensing decision.** At the revision reviewed, the repository
license is Apache-2.0 and the Python distribution declares MIT. The code in
these three entries is original to ML4SETK. The baseline tests cite the paper
for the published reference numbers. The MIT baseline licenses permit reuse
with their notices under either declaration. The FSE deposit grants CC BY 4.0
rights to covered material. Crediting its authors alone would not turn a copy
into MIT- or Apache-2.0-only source. A future port needs a file-level reuse
decision and the applicable terms shipped with the distribution.
[Toolkit LICENSE](https://github.com/jkatzy/ML4SE-toolkit/blob/f2e72fd78627e17fba874cfa0e1e3202479a196b/LICENSE) · [Package metadata](https://github.com/jkatzy/ML4SE-toolkit/blob/f2e72fd78627e17fba874cfa0e1e3202479a196b/pyproject.toml#L13)
