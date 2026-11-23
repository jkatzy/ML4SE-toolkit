"""Min-K% Prob, Equation (1) of Shi et al., ICLR 2024.

Weijia Shi, Anirudh Ajith, Mengzhou Xia, Yangsibo Huang, Daogao Liu,
Terra Blevins, Danqi Chen, and Luke Zettlemoyer.
"Detecting Pretraining Data from Large Language Models."
https://openreview.net/forum?id=ZLJ6XRbdaC
"""

from collections.abc import Iterable
from math import isfinite
from statistics import fmean


def min_k_score(token_log_probs: Iterable[float], *, k_percent: float = 20.0) -> float:
    """Mean of the lowest k percent of one example's observed-token log probabilities.

    Supply one finite, nonpositive natural log probability per predicted token.
    Omit padding and positions without a prediction. Higher scores favor membership.
    The tail size is rounded down, as in the published artifact. An empty tail
    has no mean and raises ValueError.
    """
    if not 0 < k_percent <= 100:
        raise ValueError("k_percent must be in (0, 100]")
    values = list(token_log_probs)
    if any(not isfinite(value) or value > 0 for value in values):
        raise ValueError("token log probabilities must be finite and nonpositive")
    count = int(len(values) * k_percent / 100)
    if count == 0:
        raise ValueError("The selected percentage must include at least one predicted token")
    return fmean(sorted(values)[:count])
