# ML4SE Toolkit — SATD Analysis

This repository contains the code and data used in the paper:

**["Analyzing the Impact of Self-Admitted Technical Debt on the Code Completion Performance of Large Language Models"](https://repository.tudelft.nl/record/uuid:72b68f89-197e-49fd-a254-af47ff7b4e4f)**

---

## Repository Structure

Each directory contains a `README.md` with more detailed information:

```
/data/               - Intermediate outputs and DelftBlue job scripts
├── codegen/         - Code generation outputs
├── delftblue/       - Job scripts + outputs from DelftBlue cluster
├── input-target/    - Input/target pairs used for generation
├── Java/            - SATD spans and count annotations for Java dataset
├── scores/          - Code generation scores + plots
└── thresholds/      - Mean + 2 standard deviation thresholds of comments/methods

/input-target/       - Notebook for generating input/target pairs + target complexity plot
/mean_2std/          - Scripts to compute thresholds on DelftBlue
/results/            - Code and plots for results in the paper
├── code_gen/        - Code for code generation on DelftBlue
├── presence/        - Code + plot for RQ1 (SATD presence analysis)
└── qualitative/     - Semantic labeling + plot for RQ3 (qualitative analysis)

/satd_annotate/      - SATD bitmask, spans, and count annotation code + investigation

satd_detector.jar    - Java SATD detector used for annotation
SATDDetector.java    - Wrapper class to invoke the SATD detector
scores.ipynb         - Notebook for calculating generation scores + plots for RQ2
```

---

## Requirements

- All **notebooks** were written in **Python 3.12**
- All **Python scripts** were written in **Python 3.10**, run on **DelftBlue**

To install dependencies for local use:

```bash
pip install -r requirements.txt
```

For `/satd_annotate/` and `/results/code_gen/`, additional minimal `requirements.txt` files are provided in those folders.

---

## Notes

* Not all notebooks are fully reproducible out-of-the-box due to modified paths or experiment-specific configuration.
* All Python scripts were run on the DelftBlue cluster, so they do not run out of the box.
* The full annotated version of **The Heap** dataset is not included due to size. You can regenerate it using:

  * The annotations in `/data/Java/`
  * The beginning code of the notebook `satd_annotate/investigate_annotations.ipynb`