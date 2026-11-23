"""Known-canary exposure, Carlini et al., The Secret Sharer, USENIX Security 2019.

https://www.usenix.org/conference/usenixsecurity19/presentation/carlini
"""

from math import isfinite, log2


def canary_rank(canary_loss, alternative_losses):
    """Rank a known canary by loss. Count tied alternatives as equally or more likely."""
    if not isfinite(canary_loss):
        raise ValueError("Expected a finite canary loss")
    rank = 1
    for loss in alternative_losses:
        if not isfinite(loss):
            raise ValueError("Expected finite alternative losses")
        rank += int(loss <= canary_loss)
    return rank


def exposure_bits(space_size: int, rank: int) -> float:
    """Compute exact exposure in bits for a one-based rank in a finite space."""
    if not isinstance(space_size, int) or not isinstance(rank, int) or not 1 <= rank <= space_size:
        raise ValueError("Expected integer values with 1 <= rank <= space_size")
    return log2(space_size) - log2(rank)
