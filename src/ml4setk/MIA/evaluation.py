"""Aggregate benchmark metrics used in the AST-PAC evaluation.

Roham Koohestani, Ali Al-Kaswan, Jonathan Katzy, and Maliheh Izadi.
"AST-PAC: AST-guided Membership Inference for Code." FSE Companion 2026.
https://doi.org/10.1145/3803437.3805588
"""

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class MembershipMetrics:
    """Areas under the ROC and precision-recall curves for a labeled benchmark."""

    roc_auc: float
    pr_auc: float
    n_members: int
    n_nonmembers: int


def evaluate_membership_scores(
    *, members: Iterable[float], nonmembers: Iterable[float]
) -> MembershipMetrics:
    """Evaluate two known cohorts of precomputed scores, with members as positives.

    Higher scores indicate stronger evidence of membership. Both cohorts must
    contain at least one finite score, and all supplied scores must be finite.
    Ties enter the curves together. PR-AUC uses trapezoids with precision 1 at
    the initial zero-recall point, as in the AST-PAC RQ3 replication notebook.
    """
    member_counts = Counter(members)
    nonmember_counts = Counter(nonmembers)
    if not member_counts or not nonmember_counts:
        raise ValueError("Both members and nonmembers must contain scores")
    scores = member_counts.keys() | nonmember_counts.keys()
    if not all(isfinite(score) for score in scores):
        raise ValueError("Membership scores must be finite")

    true_positives = false_positives = 0
    previous_precision = 1.0
    twice_roc_area = 0
    twice_pr_area = 0.0
    for score in sorted(scores, reverse=True):
        positives, negatives = member_counts[score], nonmember_counts[score]
        previous_true_positives = true_positives
        true_positives += positives
        false_positives += negatives
        precision = true_positives / (true_positives + false_positives)
        # Accumulate trapezoids in counts, then normalize each axis once.
        twice_roc_area += negatives * (previous_true_positives + true_positives)
        twice_pr_area += positives * (previous_precision + precision)
        previous_precision = precision

    return MembershipMetrics(
        roc_auc=twice_roc_area / (2 * true_positives * false_positives),
        pr_auc=twice_pr_area / (2 * true_positives),
        n_members=true_positives,
        n_nonmembers=false_positives,
    )
