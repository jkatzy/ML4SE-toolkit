import random
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


def _select(matches, select, seed):
    """Return the sorted indices of ``matches`` picked by ``select``."""

    if select is None:
        return list(range(len(matches)))
    if callable(select):
        return [i for i, match in enumerate(matches) if select(match)]
    if isinstance(select, int):
        return sorted(random.Random(seed).sample(range(len(matches)), select))
    return sorted({range(len(matches))[i] for i in select})


class AbstractInput(ABC):
    """
    Generates model-ready inputs from a parsed query match.

    Concrete implementations should document their accepted input shape when it
    differs from ``QueryMatch(prefix, suffix, match)``.
    """

    @abstractmethod
    def generate(self, query_match):
        """Return a tuple of ``(model_input, ground_truth)``."""

    # Formats that can mask several spans of one source in a single input
    # override ``_join_spans`` and set this flag.
    multi_span = False

    def generate_many(self, matches, select=None, seed=None):
        """Turn the matches of one query into ``(model_input, ground_truth)`` pairs.

        ``select`` picks the matches to mask: ``None`` for all of them, an
        ``int`` for that many sampled with ``seed``, an iterable of indices,
        or a predicate called on each match. Single-span formats return one
        pair per selected match. Multi-span formats return one pair that masks
        every selected match, with the ground truths as a list in source order.
        """

        matches = list(matches)
        chosen = _select(matches, select, seed)
        if not self.multi_span:
            return [self.generate(matches[i]) for i in chosen]
        if not chosen:
            return []

        spans = []
        for i in chosen:
            prefix, suffix, middle = unpack_query_match(matches[i])
            spans.append((len(prefix), len(prefix) + len(middle), prefix + middle + suffix))
        spans.sort()
        text = spans[0][2]
        segments, middles, cursor = [], [], 0
        for start, end, source in spans:
            if source != text:
                raise ValueError("generate_many needs matches from the same source text.")
            if start < cursor:
                raise ValueError("Selected matches overlap; select non-overlapping matches.")
            segments.append(text[cursor:start])
            middles.append(text[start:end])
            cursor = end
        segments.append(text[cursor:])
        return [(self._join_spans(segments, middles), middles)]

    def _join_spans(self, segments, middles):
        """Return the model input with each middle masked between ``segments``."""

        raise NotImplementedError
