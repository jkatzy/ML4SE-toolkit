"""Evaluation of recorded AST-PAC scores.

Roham Koohestani, Ali Al-Kaswan, Jonathan Katzy, and Maliheh Izadi.
"AST-PAC: AST-guided Membership Inference for Code." FSE Companion 2026,
pp. 1361–1365. https://doi.org/10.1145/3803437.3805588
Replication package by Roham Koohestani: https://doi.org/10.5281/zenodo.18348152
"""

from collections.abc import Iterable

from .evaluation import MembershipMetrics
from .pac import evaluate_pac_scores


def evaluate_ast_pac_scores(
    *, members: Iterable[float], nonmembers: Iterable[float]
) -> MembershipMetrics:
    """Compute RQ3 point estimates from the archive's raw ``pac_ast_score`` values.

    Lower archived scores favor membership. Supply finite scores for the two
    labeled cohorts from the same model and stratum.
    """
    return evaluate_pac_scores(members=members, nonmembers=nonmembers)
