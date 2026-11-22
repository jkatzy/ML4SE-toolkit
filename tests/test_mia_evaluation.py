import pytest

from ml4setk.MIA import (
    evaluate_ast_pac_scores,
    evaluate_loss_scores,
    evaluate_membership_scores,
    evaluate_pac_scores,
)


@pytest.mark.parametrize(
    ("members", "nonmembers", "roc_auc", "pr_auc"),
    [
        ([2, 3], [0, 1], 1, 1),
        ([-1], [1], 0, 1 / 4),
        ([1], [1, 1, 1], 1 / 2, 5 / 8),
        ([1, 3], [1, 2], 5 / 8, 3 / 4),
    ],
)
def test_benchmark_curves(members, nonmembers, roc_auc, pr_auc):
    result = evaluate_membership_scores(members=iter(members), nonmembers=iter(nonmembers))
    assert result.roc_auc == pytest.approx(roc_auc)
    assert result.pr_auc == pytest.approx(pr_auc)
    assert (result.n_members, result.n_nonmembers) == (len(members), len(nonmembers))


@pytest.mark.parametrize("members, nonmembers", [([], [1]), ([1], []), ([], [])])
def test_both_cohorts_are_required(members, nonmembers):
    with pytest.raises(ValueError, match="Both members and nonmembers"):
        evaluate_membership_scores(members=members, nonmembers=nonmembers)


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_scores_are_rejected(invalid):
    with pytest.raises(ValueError, match="finite"):
        evaluate_membership_scores(members=[0, 1], nonmembers=[invalid, 0])


@pytest.mark.parametrize("evaluate", [evaluate_ast_pac_scores, evaluate_pac_scores])
def test_raw_pac_scores_favor_lower_values(evaluate):
    result = evaluate(members=[-2, 0], nonmembers=[1, 2])
    assert (result.roc_auc, result.pr_auc) == (1, 1)


def test_archived_loss_scores_are_already_oriented():
    result = evaluate_loss_scores(members=[-2, -1], nonmembers=[-4, -3])
    assert (result.roc_auc, result.pr_auc) == (1, 1)


def test_polarized_distance_uses_requested_tail_sizes():
    from ml4setk.MIA.pac import _polarized_distance

    values = [-1, -40, -2, -1, -5, -3]
    assert _polarized_distance(iter(values), low_count=2, high_count=2) == 21.5
    assert _polarized_distance(values, low_count=1, high_count=1) == 39
    with pytest.raises(ValueError, match="tail counts"):
        _polarized_distance(values, low_count=7, high_count=1)
