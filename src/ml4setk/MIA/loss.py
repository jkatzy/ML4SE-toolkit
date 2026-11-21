"""Evaluation of the Loss baseline in the AST-PAC benchmark.

Samuel Yeom, Irene Giacomelli, Matt Fredrikson, and Somesh Jha.
"Privacy Risk in Machine Learning: Analyzing the Connection to Overfitting."
IEEE CSF 2018. https://doi.org/10.1109/CSF.2018.00027

For language models, the benchmark also credits "Extracting Training Data from
Large Language Models," USENIX Security 2021, by Nicholas Carlini, Florian Tramèr,
Eric Wallace, Matthew Jagielski, Ariel Herbert-Voss, Katherine Lee, Adam Roberts,
Tom Brown, Dawn Song, Úlfar Erlingsson, Alina Oprea, and Colin Raffel.
https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting

The benchmark follows Koohestani et al., FSE Companion 2026,
https://doi.org/10.1145/3803437.3805588, section 2.1 and Table 1.
"""

from collections.abc import Iterable

from .evaluation import MembershipMetrics, evaluate_membership_scores


def evaluate_loss_scores(
    *, members: Iterable[float], nonmembers: Iterable[float]
) -> MembershipMetrics:
    """Evaluate recorded ``loss_score`` values, already oriented as negative loss."""
    return evaluate_membership_scores(members=members, nonmembers=nonmembers)
