import pytest

from ml4setk.MIA import evaluate_membership_scores, min_k_score


def test_equation_one_uses_bottom_tail_and_floor():
    values = [-1.0, -8.0, 0.0, -4.0, -1.0, -3.0, -2.0, -9.0, -7.0, -1.0, -2.0]
    assert min_k_score(iter(values)) == -8.5
    assert min_k_score(values, k_percent=100) == pytest.approx(sum(values) / len(values))


def test_score_orientation_and_ties():
    member = min_k_score([-2.0, -2.0, 0.0], k_percent=70)
    nonmember = min_k_score([-4.0, -3.0, 0.0], k_percent=70)
    assert (member, nonmember) == (-2.0, -3.5)
    assert evaluate_membership_scores(members=[member], nonmembers=[nonmember]).roc_auc == 1


@pytest.mark.parametrize("k", [0, -1, 101, float("nan"), float("inf")])
def test_invalid_percentage(k):
    with pytest.raises(ValueError, match="k_percent"):
        min_k_score([-1.0], k_percent=k)


@pytest.mark.parametrize("values", [[], [-1.0] * 4])
def test_undefined_empty_tail(values):
    with pytest.raises(ValueError, match="at least one"):
        min_k_score(values)


@pytest.mark.parametrize("value", [0.01, float("-inf"), float("inf"), float("nan")])
def test_invalid_log_probability(value):
    with pytest.raises(ValueError, match="finite and nonpositive"):
        min_k_score([-1.0] * 5 + [value])
