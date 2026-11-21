"""Check recorded results from Koohestani et al., doi:10.1145/3803437.3805588.

Inputs: the unpacked Zenodo artifact (doi:10.5281/zenodo.18348152) and the
final proceedings PDF. Only aggregate comparisons are printed.
"""

import argparse
import json
import re
import subprocess
from collections import Counter
from io import StringIO
from pathlib import Path

import pandas as pd

from ml4setk.MIA import evaluate_ast_pac_scores, evaluate_loss_scores, evaluate_pac_scores

MODELS = {"mellum": "mellum", "smollm": "smollm", "SC2-3B": "sc2_3b", "SC2-7B": "sc2_7b"}
MEMBERS = {"MA": ["member", "member_near"], "ME": ["member"], "MN": ["member_near"]}
DIMENSIONS = {
    "Alphanumeric Ratio": "alpha_bucket",
    "File Size": "size_bucket",
    "Syntactic Size (Node Count)": "complexity_bucket",
}
EVALUATE = {
    "loss": evaluate_loss_scores,
    "pac": evaluate_pac_scores,
    "pac_ast": evaluate_ast_pac_scores,
}


def published_table(pdf):
    text = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"], text=True)
    # The model name is centered on the second of each model's three printed rows.
    pattern = (
        r"^[ \t]*(?:(Mellum|SmolLM|SC2 [37]B)[ \t]+)?(All|Exact|Near) vs NM[ \t]+"
        r"(\d+\.\d+) / (\d+\.\d+)[ \t]+(\d+\.\d+) / (\d+\.\d+)"
    )
    cells = re.findall(pattern, text, re.MULTILINE)
    assert len(cells) == 12, "Expected 12 model/scenario rows in the final Table 1"
    for start in range(0, len(cells), 3):
        group = cells[start : start + 3]
        model = group[1][0].replace(" ", "-")
        model = model if model.startswith("SC2") else model.lower()
        assert [row[1] for row in group] == ["All", "Exact", "Near"]
        for scenario, row in zip(("MA", "ME", "MN"), group):
            yield (model, scenario, "loss"), row[2:4]
            yield (model, scenario, "pac"), row[4:6]


def archived_strata(path, *, with_intervals=False):
    labels = ["", "", ""]
    for line in path.read_text().splitlines():
        cells = [part.strip() for part in line.split("&")]
        if len(cells) != 6 or "[" not in cells[4]:
            continue
        for i, field in enumerate(cells[:3]):
            if field:
                labels[i] = re.fullmatch(r"\\multirow\[t\]\{\d+\}\{\*\}\{([^}]+)\}", field)[1]
        method, model, dimension = labels
        yield (
            (model, method, DIMENSIONS[dimension], cells[3]),
            (
                tuple(re.findall(r"\d+\.\d+", " ".join(cells[4:])))
                if with_intervals
                else (cells[4].split()[0], cells[5].split()[0])
            ),
        )


def notebook_table(root, rq, index):
    notebook = root / "analysis" / rq / (rq.lower() + ".ipynb")
    outputs = json.loads(notebook.read_text())["cells"][index]["outputs"]
    html = next(o["data"]["text/html"] for o in outputs if "text/html" in o.get("data", {}))
    return pd.read_html(StringIO("".join(html)), header=0)[0]


def points(group, method):
    scores = group[method + "_score"]
    positive = group["type"].ne("non_member")
    result = EVALUATE[method](members=scores[positive], nonmembers=scores[~positive])
    return result.roc_auc, result.pr_auc


def table2_cutoffs(root):
    # Table 2 gives the observed maxima below the top bucket of each dimension.
    # The alphanumeric fraction is printed to one decimal place in the paper.
    corpus = root / "dataset" / "full.parquet"
    for dim, column, expected, digits in [
        ("size_bucket", "size", (1074, 1946, 3369, 6844), 0),
        ("complexity_bucket", "node_count", (58, 211), 0),
        ("alpha_bucket", "alphanum_fraction", (0.2, 0.4, 0.6, 0.8), 1),
    ]:
        frame = pd.read_parquet(corpus, columns=[dim, column])
        maxima = frame.groupby(dim, observed=True)[column].max().sort_values().iloc[:-1]
        yield dim, maxima, expected, digits


def run(root, pdf):
    totals = Counter()
    mismatches = Counter()

    def compare(reference, method, key, expected, actual, digits):
        assert len(expected) == len(actual)
        for label, value, measured in zip(key[-1], expected, actual):
            totals[reference, method] += 1
            if f"{measured:.{digits}f}" != f"{float(value):.{digits}f}":
                mismatches[reference, method] += 1
                print("DIFFERENCE", reference, method, *key[:-1], label, value, f"{measured:.9f}")

    overall, stratified = {}, {}
    changes = {}
    for model, slug in MODELS.items():
        file = root / "results" / f"results_{slug}_new_approach_orig_m_worker_0.parquet"
        raw = pd.read_parquet(file)
        data = raw.dropna()
        print(model, "complete rows", len(data), "of", len(raw))
        for scenario, members in MEMBERS.items():
            subset = data[data["type"].isin([*members, "non_member"])]
            for method in EVALUATE:
                if method != "pac_ast":
                    overall[model, scenario, method] = points(subset, method)
                for dim in DIMENSIONS.values():
                    for bucket, group in subset.groupby(dim, observed=True):
                        if group["type"].eq("non_member").nunique() == 2:
                            stratified[model, scenario, method, dim, bucket] = points(group, method)
        for bucket, group in data.groupby("complexity_bucket", observed=True):
            for method in ("pac", "pac_ast"):
                ratio = method + "_change_ratio"
                changes[ratio, model, bucket] = group[ratio].quantile([0.25, 0.5, 0.75]).tolist()

    areas = ("ROC-AUC", "PR-AUC")
    paper = dict(published_table(pdf))
    assert paper.keys() == overall.keys()
    for (model, scenario, method), expected in paper.items():
        compare(
            "Table 1",
            method,
            (model, scenario, areas),
            expected,
            overall[model, scenario, method],
            3,
        )

    rq1 = notebook_table(root, "RQ1", 8)
    references = {
        (r["Model"], r["Scenario"][:2], r["Attack"]): [r[a] for a in areas]
        for _, r in rq1.iterrows()
    }
    assert references.keys() == overall.keys()
    for (model, scenario, method), expected in references.items():
        compare(
            "RQ1 notebook",
            method,
            (model, scenario, areas),
            expected,
            overall[model, scenario, method],
            6,
        )

    for rq, methods in [("RQ2", ("loss", "pac")), ("RQ3", ("pac", "pac_ast"))]:
        for scenario in MEMBERS:
            path = root / "analysis" / rq / f"{rq.lower()}_table_{scenario}_vs_NM.tex"
            refs = dict(archived_strata(path))
            computed = {
                (model, method, dim, bucket): pair
                for (model, sc, method, dim, bucket), pair in stratified.items()
                if sc == scenario and method in methods
            }
            assert refs.keys() == computed.keys(), f"Stratum coverage differs in {path.name}"
            for key, expected in refs.items():
                model, method, dim, bucket = key
                compare(
                    rq, method, (model, scenario, dim, bucket, areas), expected, computed[key], 3
                )

    fig = notebook_table(root, "RQ3", 19).dropna(subset=["N"])
    quartiles = ["p25", "median", "p75"]
    fig_refs = {tuple(r.iloc[:3]): r[quartiles].tolist() for _, r in fig.iterrows()}
    assert fig_refs.keys() == changes.keys()
    for key, expected in fig_refs.items():
        ratio, model, bucket = key
        compare("Figure 3", ratio, (model, bucket, quartiles), expected, changes[key], 6)

    for dim, maxima, expected, digits in table2_cutoffs(root):
        compare("Table 2", dim, (maxima.index,), expected, maxima, digits)

    for key, total in totals.items():
        print(*key, f"{total - mismatches[key]}/{total}")
    return bool(sum(mismatches.values()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("paper_pdf", type=Path)
    args = parser.parse_args()
    raise SystemExit(run(args.artifact, args.paper_pdf))
