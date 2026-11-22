"""Evaluation of the Polarized Augment Calibration (PAC) baseline.

Wentao Ye, Jiaqi Hu, Liyao Li, Haobo Wang, Gang Chen, and Junbo Zhao.
"Data Contamination Calibration for Black-box LLMs." Findings of ACL 2024.
https://doi.org/10.18653/v1/2024.findings-acl.644

The archived score convention follows Koohestani et al., FSE Companion 2026,
https://doi.org/10.1145/3803437.3805588. Artifact: https://doi.org/10.5281/zenodo.18348152
"""

from collections.abc import Iterable
from statistics import fmean

from .evaluation import MembershipMetrics, evaluate_membership_scores


def _polarized_distance(log_probs: Iterable[float], *, low_count: int, high_count: int) -> float:
    """Mean of the highest minus mean of the lowest recorded token log probabilities."""
    ordered = sorted(log_probs)
    if not (1 <= low_count <= len(ordered) and 1 <= high_count <= len(ordered)):
        raise ValueError("Both tail counts must be between one and the number of predictions")
    return fmean(ordered[-high_count:]) - fmean(ordered[:low_count])


def evaluate_pac_scores(
    *, members: Iterable[float], nonmembers: Iterable[float]
) -> MembershipMetrics:
    """Evaluate raw archive PAC scores, where lower values favor membership."""
    return evaluate_membership_scores(
        members=(-score for score in members),
        nonmembers=(-score for score in nonmembers),
    )
