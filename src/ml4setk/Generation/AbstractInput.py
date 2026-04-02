from abc import ABC, abstractmethod

from ..Parsing.Query import QueryMatch


def unpack_query_match(query_match):
    """Normalize a QueryMatch or tuple-like object into its three string parts."""

    if isinstance(query_match, QueryMatch):
        return query_match.prefix, query_match.suffix, query_match.match

    try:
        prefix, suffix, match = query_match
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Expected a QueryMatch or a 3-item tuple of (prefix, suffix, match)."
        ) from exc

    return prefix, suffix, match

class AbstractInput(ABC):

    """
    Generates model-ready inputs from a parsed query match.

    Concrete implementations should document their accepted input shape when it
    differs from ``QueryMatch(prefix, suffix, match)``.
    """

    @abstractmethod
    def generate(self, query_match):
        """Return a tuple of ``(model_input, ground_truth)``."""
