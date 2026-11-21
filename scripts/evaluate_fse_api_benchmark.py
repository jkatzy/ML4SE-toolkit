"""Compare fresh joint API outputs with the FSE paper and deposited notebooks."""

import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from check_mia_reproduction import (
    DIMENSIONS,
    MEMBERS,
    MODELS,
    archived_strata,
    notebook_table,
    published_table,
    table2_cutoffs,
)
from run_fse_api_benchmark import EVALUATORS, complete_cases, run_identity
from sklearn.metrics import (
    accuracy_score,
    auc,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from ml4setk.MIA import MembershipThreshold, evaluate_membership_scores


def checked_areas(frame, method):
    labels = frame.type.ne("non_member")
    scores = frame[method]
    metric = evaluate_membership_scores(members=scores[labels], nonmembers=scores[~labels])
    raw = scores if method == "loss" else -scores
    if metric != EVALUATORS[method](members=raw[labels], nonmembers=raw[~labels]):
        raise AssertionError("Joint and method-specific API results differ")
    precision, recall, _ = precision_recall_curve(labels, scores)
    areas = (metric.roc_auc, metric.pr_auc)
    np.testing.assert_allclose(
        areas, [roc_auc_score(labels, scores), auc(recall, precision)], rtol=0, atol=1e-12
    )
    return areas


def threshold_metrics(frame, method):
    scores = frame[method]
    labels = frame.type.ne("non_member")
    fpr, tpr, thresholds = roc_curve(labels, scores)
    threshold = thresholds[np.argmax(tpr - fpr)]
    preds = MembershipThreshold(float(threshold)).predict_many(scores)
    if not np.array_equal(preds, scores >= threshold):
        raise AssertionError("Threshold predictions differ")
    return (
        accuracy_score(labels, preds),
        precision_score(labels, preds, zero_division=0),
        recall_score(labels, preds, zero_division=0),
        f1_score(labels, preds, zero_division=0),
    )


def bootstrap(frame, method):
    # Sort once, retain ties, and resample rows as in the RQ2/RQ3 notebooks.
    # Forty replicas at a time bound memory. Weights are draws per sorted row.
    ordered = frame.sort_values(method, ascending=False)
    positive = ordered.type.ne("non_member").to_numpy()
    values = ordered[method].to_numpy()
    groups = np.r_[0, 1 + np.flatnonzero(values[:-1] != values[1:])]
    n = len(values)
    rng = np.random.default_rng(42)
    reps = []
    for _ in range(25):
        draws = rng.integers(n, size=(40, n))
        counts = np.bincount(
            (draws + np.arange(40)[:, None] * n).ravel(), minlength=40 * n
        ).reshape(40, n)
        successes = np.add.reduceat(counts * positive, groups, axis=1)
        failures = np.add.reduceat(counts * ~positive, groups, axis=1)
        tp = successes.cumsum(axis=1)
        fp = failures.cumsum(axis=1)
        keep = (tp[:, -1] > 0) & (fp[:, -1] > 0)
        if not keep.any():
            continue
        tp, fp, successes, failures = [arr[keep] for arr in (tp, fp, successes, failures)]
        precision = np.divide(tp, tp + fp, out=np.ones_like(tp, dtype=float), where=(tp + fp) > 0)
        previous = np.column_stack([np.ones(len(tp)), precision[:, :-1]])
        roc = (failures * (2 * tp - successes)).sum(axis=1) / (2 * tp[:, -1] * fp[:, -1])
        pr = (successes * (previous + precision)).sum(axis=1) / (2 * tp[:, -1])
        reps.append(np.column_stack((roc, pr)))
    return np.percentile(np.concatenate(reps), [2.5, 97.5], axis=0).T


def evaluate_model(root, pdf, out, model):
    rows = complete_cases(root, model)
    stamp = run_identity(rows, model)
    meta = rows.drop(columns=["content"])
    slug = MODELS[model]
    path = out / f"{slug}.sqlite"
    with sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True) as db:
        recorded = db.execute("SELECT stamp FROM metadata WHERE id=1").fetchone()
        if recorded is None or json.loads(recorded[0]) != stamp:
            raise ValueError("Score database does not match the model, cohort and forward protocol")
        scores = pd.read_sql_query("SELECT * FROM fresh", db, index_col="row_id")
    if not scores.index.is_unique or set(scores.index) != set(meta.index):
        raise ValueError(f"{model}: {len(scores)} of {len(meta)} complete rows")
    data = meta.join(scores, validate="one_to_one")
    records = []

    def add(section, method, scenario, dimension, bucket, metric, observed, expected, digits):
        records.append(
            dict(
                section=section,
                model=model,
                method=method,
                scenario=scenario,
                dimension=dimension,
                bucket=bucket,
                metric=metric,
                fresh=observed,
                reference=float(expected),
                digits=digits,
                matches=f"{observed:.{digits}f}" == f"{float(expected):.{digits}f}",
            )
        )

    paper = dict(published_table(pdf))
    notebook = notebook_table(root, "RQ1", 8)
    cols = ("ROC-AUC", "PR-AUC", "Accuracy", "Precision", "Recall", "F1")
    for scenario, types in MEMBERS.items():
        subset = data[data.type.isin([*types, "non_member"])]
        for method in ("loss", "pac"):
            areas = checked_areas(subset, method)
            for metric, actual, expected in zip(cols, areas, paper[model, scenario, method]):
                add("Table 1", method, scenario, "all", "all", metric, actual, expected, 3)
            row = notebook[
                (notebook.Model == model)
                & (notebook.Scenario.str.startswith(scenario))
                & (notebook.Attack == method)
            ].iloc[0]
            for metric, value in zip(cols, (*areas, *threshold_metrics(subset, method))):
                add("RQ1 notebook", method, scenario, "all", "all", metric, value, row[metric], 6)

        computed = {}
        for method in EVALUATORS:
            for dim in DIMENSIONS.values():
                for bucket, group in subset.groupby(dim):
                    if group.type.eq("non_member").nunique() != 2:
                        continue
                    areas = checked_areas(group, method)
                    limits = bootstrap(group, method)
                    computed[model, method, dim, bucket] = (
                        areas[0],
                        *limits[0],
                        areas[1],
                        *limits[1],
                    )
        metrics = ("ROC-AUC", "ROC lower", "ROC upper", "PR-AUC", "PR lower", "PR upper")
        for rq, methods in [("RQ2", ("loss", "pac")), ("RQ3", ("pac", "pac_ast"))]:
            path = root / "analysis" / rq / f"{rq.lower()}_table_{scenario}_vs_NM.tex"
            expected = {
                k: v for k, v in archived_strata(path, with_intervals=True) if k[0] == model
            }
            keys = {k for k in computed if k[1] in methods}
            if keys != expected.keys():
                raise ValueError(f"Stratification mismatch in {path}")
            for key in sorted(keys):
                _, method, dim, bucket = key
                if len(expected[key]) != 6:
                    raise ValueError("Malformed interval")
                for metric, value, target in zip(metrics, computed[key], expected[key]):
                    add(rq, method, scenario, dim, bucket, metric, value, target, 3)
    summary = notebook_table(root, "RQ3", 19).dropna(subset=["N"])
    for _, row in summary.iterrows():
        ratio, ref_model, bucket = row.iloc[:3]
        if ref_model != model:
            continue
        group = data.loc[data.complexity_bucket == bucket, ratio]
        if len(group) != int(row.N):
            raise ValueError("Figure 3 cohort size changed")
        for metric, q in [("p25", 0.25), ("median", 0.5), ("p75", 0.75)]:
            add(
                "Figure 3",
                ratio.removesuffix("_change_ratio"),
                "all",
                "complexity_bucket",
                bucket,
                metric,
                group.quantile(q),
                row[metric],
                6,
            )
    result = pd.DataFrame(records)
    if len(result) != 12 + 36 + 864 + 18:
        raise ValueError(f"Unexpected reference coverage: {len(result)}")
    result.to_csv(out / f"{slug}-comparison.csv", index=False)
    print(model, result.groupby("section").matches.agg(["sum", "count"]).to_string(), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path)
    p.add_argument("paper_pdf", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--model", choices=MODELS)
    args = p.parse_args()
    cutoffs = []
    for dimension, maxima, expected, digits in table2_cutoffs(args.artifact):
        if len(maxima) != len(expected):
            raise ValueError("Table 2 bucket coverage differs")
        for (bucket, observed), target in zip(maxima.items(), expected):
            cutoffs.append(
                dict(
                    dimension=dimension,
                    bucket=bucket,
                    fresh=observed,
                    reference=target,
                    matches=f"{observed:.{digits}f}" == f"{target:.{digits}f}",
                )
            )
    if len(cutoffs) != 10:
        raise ValueError("Expected ten Table 2 cutoffs")
    pd.DataFrame(cutoffs).to_csv(args.output / "table2-comparison.csv", index=False)
    for model in [args.model] if args.model else MODELS:
        evaluate_model(args.artifact, args.paper_pdf, args.output, model)
