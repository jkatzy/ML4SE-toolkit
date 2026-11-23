"""Compare independently scored, labeled FSE cohorts with the published tables."""

import hashlib

import pandas as pd
from check_mia_reproduction import (
    DIMENSIONS,
    EVALUATE,
    MEMBERS,
    MODELS,
    archived_strata,
    published_table,
)
from fse_cohort import KEYS, complete_cases
from fse_scoring import BenchmarkScorer, token_neighbors
from paper_tolerance import within_one_percent

from ml4setk.MIA import evaluate_membership_scores


def source_rows(root, model_name, pilot):
    rows = complete_cases(root, model_name)
    if pilot:
        rows = rows[rows.alpha_bucket.eq("Mid-Low") & rows.type.isin(["member", "non_member"])]
        assert rows.type.value_counts().to_dict() == {"member": 132, "non_member": 93}
    return rows


def score_and_compare(root, model_name, rows, checkpoint, method, config):
    """Select original texts by file identity and score only the requested method."""
    pilot = config.getoption("--fse-pilot")
    exact = config.getoption("--exact-fse")
    paper = {}
    if not pilot and method in ("loss", "pac"):
        pdf = config.getoption("--fse-paper")
        if not pdf:
            raise ValueError("Supply the final FSE PDF with --fse-paper or ML4SETK_FSE_PDF")
        paper = dict(published_table(pdf))
    model, tokenizer = checkpoint
    if method == "pac_ast":
        path = (
            root / "results" / f"results_{MODELS[model_name]}_new_approach_orig_m_worker_0.parquet"
        )
        fixed = pd.read_parquet(path, columns=[*KEYS, "pac_ast_perturbed_samples"])
        rows = rows.merge(fixed, on=KEYS, how="left", validate="one_to_one")
    scores = []
    for i, row in enumerate(rows.itertuples(), start=1):
        text = row.content
        neighbors = ()
        if method == "pac":
            seed = int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")
            neighbors = token_neighbors(text, tokenizer, seed)
        elif method == "pac_ast":
            neighbors = row.pac_ast_perturbed_samples
        if method != "loss":
            assert len(neighbors) == 5 and all(isinstance(n, str) for n in neighbors)
        scorer = BenchmarkScorer(method, {text: neighbors}, tokenizer, "cuda")
        scores.extend(scorer.score_many(model, [text]))
        if i % 1000 == 0:
            print(f"{model_name} {method} scored {i}/{len(rows)} files", flush=True)
    compare_scores(root, model_name, rows.assign(score=scores), method, pilot, exact, paper)


def checked_areas(group, method):
    is_member = group.type.ne("non_member")
    pos, neg = group.score[is_member], group.score[~is_member]
    joint = evaluate_membership_scores(members=pos, nonmembers=neg)
    sign = 1 if method == "loss" else -1
    assert EVALUATE[method](members=sign * pos, nonmembers=sign * neg) == joint
    return joint


def compare_scores(root, model_name, rows, method, pilot, exact, paper):
    rq = "RQ3" if method == "pac_ast" else "RQ2"
    matched = total = 0
    outside_intervals = 0
    differences = []
    within = 0
    aggregate_matches = 0
    aggregate_within = 0
    for scenario in ["ME"] if pilot else MEMBERS:
        subset = rows[rows.type.isin(["non_member", *MEMBERS[scenario]])]
        if paper:
            joint = checked_areas(subset, method)
            expected = paper[model_name, scenario, method]
            actual = (joint.roc_auc, joint.pr_auc)
            aggregate_matches += sum(f"{v:.3f}" == ref for v, ref in zip(actual, expected))
            for label, value, ref in zip(("ROC-AUC", "PR-AUC"), actual, expected):
                if within_one_percent(value, ref):
                    aggregate_within += 1
                else:
                    differences.append(("Table 1", scenario, label, value, ref))
            print(
                f"Table 1 {model_name} {scenario}: {actual[0]!r}/{actual[1]!r}, "
                f"paper {expected[0]}/{expected[1]}"
            )
        table = root / "analysis" / rq / f"{rq.lower()}_table_{scenario}_vs_NM.tex"
        reference = {
            (dimension, bucket): list(map(float, values))
            for (model_id, name, dimension, bucket), values in archived_strata(
                table, with_intervals=True
            )
            if (model_id, name) == (model_name, method)
        }
        groups = {
            (dim, bucket): group
            for dim in DIMENSIONS.values()
            for bucket, group in subset.groupby(dim)
            if group.type.eq("non_member").nunique() == 2
        }
        if pilot:
            key = ("alpha_bucket", "Mid-Low")
            groups = {key: groups[key]}
        else:
            assert groups.keys() == reference.keys() and len(groups) == 12
        for key, group in groups.items():
            joint = checked_areas(group, method)
            roc, lo_roc, hi_roc, pr, lo_pr, hi_pr = reference[key]
            for label, fresh, ref, lo, hi in [
                ("ROC-AUC", joint.roc_auc, roc, lo_roc, hi_roc),
                ("PR-AUC", joint.pr_auc, pr, lo_pr, hi_pr),
            ]:
                total += 1
                matched += round(fresh, 3) == ref
                print(
                    f"{model_name} {scenario} {key} {label}: {fresh!r}, "
                    f"published {ref:.3f} [{lo}, {hi}]"
                )
                outside_intervals += int(not lo <= fresh <= hi)
                if within_one_percent(fresh, ref):
                    within += 1
                else:
                    differences.append((rq, scenario, key, label, fresh, ref))
    assert total == (2 if pilot else 72)
    print(
        f"{model_name} {method}: {within}/{total} within 1%, "
        f"{matched}/{total} equal at three decimals, "
        f"{total - outside_intervals}/{total} inside reported intervals"
    )
    if paper:
        print(
            f"{model_name} {method}: {aggregate_within}/6 Table 1 areas within 1%, "
            f"{aggregate_matches}/6 equal at printed precision"
        )
        if exact:
            assert aggregate_matches == 6
    assert not differences, f"Outside 1% of the published value: {differences}"
    if exact:
        assert matched == total, f"{matched}/{total} stratified areas match at printed precision"
