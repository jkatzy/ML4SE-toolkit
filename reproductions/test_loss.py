"""Yeom et al. (CSF 2018), Fig. 2b theoretical curve, and the FSE loss baseline."""

from math import erf, sqrt
from statistics import NormalDist

import pytest
from paper_tolerance import within_one_percent

from ml4setk.MIA import MembershipThreshold


@pytest.mark.parametrize("ratio", [1, 2, 4, 8])
def test_yeom_gaussian_advantage(ratio):
    # Deterministic midpoint integration of the two zero-mean error distributions.
    n = 10000
    normal = NormalDist()
    errors = [normal.inv_cdf((i + 0.5) / n) for i in range(n)]
    rule = MembershipThreshold(-1)  # negative squared error, training variance = 1
    rates = [sum(rule.predict_many(-((s * x) ** 2) for x in errors)) / n for s in (1, ratio)]
    observed = rates[0] - rates[1]
    published = erf(1 / sqrt(2)) - erf(1 / (ratio * sqrt(2)))
    print(f"sigma ratio {ratio}: advantage {observed:.4f}, theory {published:.6f}")
    assert within_one_percent(observed, published), (observed, published)


def test_fse_loss(artifact, model_name, fse_cohort, fse_checkpoint, pytestconfig):
    from fse import score_and_compare

    score_and_compare(
        artifact,
        model_name,
        fse_cohort,
        fse_checkpoint,
        "loss",
        pytestconfig,
    )
