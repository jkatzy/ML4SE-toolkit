"""Check Koohestani et al., doi:10.1145/3803437.3805588, and artifact 10.5281/zenodo.18348152."""

import os
from collections import defaultdict
from pathlib import Path

import pytest

from ml4setk.MIA import evaluate_ast_pac_scores, evaluate_loss_scores, evaluate_pac_scores

pytestmark = pytest.mark.optional_dependency


@pytest.fixture(scope="module")
def artifact_root():
    artifact = os.environ.get("ML4SETK_AST_PAC_ARTIFACT")
    if not artifact:
        pytest.skip("set ML4SETK_AST_PAC_ARTIFACT to the extracted replication package")
    return Path(artifact)


@pytest.fixture(scope="module")
def sc2_rows(artifact_root):
    parquet = pytest.importorskip("pyarrow.parquet")
    rows = parquet.read_table(
        artifact_root / "results/results_sc2_3b_new_approach_orig_m_worker_0.parquet",
        columns=[
            "type",
            "loss_score",
            "pac_score",
            "pac_ast_score",
            "alpha_bucket",
            "size_bucket",
            "complexity_bucket",
        ],
    )
    return rows.drop_null().to_pylist()


def test_ast_pac_matches_rq3_exact_members_sc2_3b(artifact_root, sc2_rows):
    groups = defaultdict(lambda: defaultdict(list))
    for row in sc2_rows:
        if row["type"] in ("member", "non_member"):
            for dimension in ("alpha_bucket", "size_bucket", "complexity_bucket"):
                groups[row[dimension]][row["type"]].append(row["pac_ast_score"])

    # Compare with the printed point estimates, excluding the confidence intervals.
    table = (artifact_root / "analysis/RQ3/rq3_table_ME_vs_NM.tex").read_text(encoding="utf-8")
    ast_pac = table.split("{pac_ast}", 1)[1]
    model = ast_pac.split("{SC2-3B}", 1)[1].split("{SC2-7B}", 1)[0]
    expected = {}
    for line in model.splitlines():
        cells = line.split("&")
        if len(cells) >= 5:
            bucket, roc, pr = cells[-3:]
            expected[bucket.strip()] = (roc.split()[0], pr.split()[0])
    assert len(expected) == 12
    assert {bucket for bucket, cohorts in groups.items() if len(cohorts) == 2} == expected.keys()
    for bucket in expected:
        cohorts = groups[bucket]
        metrics = evaluate_ast_pac_scores(
            members=cohorts["member"], nonmembers=cohorts["non_member"]
        )
        assert (f"{metrics.roc_auc:.3f}", f"{metrics.pr_auc:.3f}") == expected[bucket], bucket


@pytest.mark.parametrize(
    ("member_types", "loss_reference", "pac_reference"),
    [
        (("member", "member_near"), (0.625, 0.750), (0.662, 0.798)),
        (("member",), (0.622, 0.600), (0.662, 0.680)),
        (("member_near",), (0.629, 0.605), (0.661, 0.664)),
    ],
)
def test_baselines_match_paper_table_1_sc2_3b(
    sc2_rows, member_types, loss_reference, pac_reference
):
    for column, evaluate, expected in [
        ("loss_score", evaluate_loss_scores, loss_reference),
        ("pac_score", evaluate_pac_scores, pac_reference),
    ]:
        result = evaluate(
            members=(row[column] for row in sc2_rows if row["type"] in member_types),
            nonmembers=(row[column] for row in sc2_rows if row["type"] == "non_member"),
        )
        assert (round(result.roc_auc, 3), round(result.pr_auc, 3)) == expected, column
