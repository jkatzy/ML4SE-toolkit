Contains the code allowing for smenatic labeling of code generation outputs, as well as the plot for RQ3 (qualitative analysis).

We have 3 groups of files containing method generations:
- out-smell: this contains the three out-smell cases with distances 0,1,-1.
- no-smell: this contains the no-smell case.
- multi-out-smell: this contains the multi-out-smell case with distances 0,-1 and their accompying preprocessed cases.

For every group we analysed 20 files which contains all method generations for the respective cases. In order to analyze the generations effectively, we made use of three files per file:
- output_contexts: This includes the full file context, this is used to analyze the surrounding context of the method generation.
- output_generations: This includes all the method generations, targets and scores. This is used to compare the method generations with the targets.
- annotations: This includes a json file with extra fields for each method generation:
    - `classification`: This is the semantic classification of the method generation, it can be either `correct`, `partial`, or `incorrect`.
    - `comment`: This is a comment on the method generation, it can be used to explain the classification.