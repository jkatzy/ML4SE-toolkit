"""Shared interfaces for scoring source files and interpreting recorded scores."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from math import isfinite
from typing import Generic, TypeVar

ModelT = TypeVar("ModelT")


class MembershipScorer(ABC, Generic[ModelT]):
    """Score complete source files with a caller-supplied model and its tokenizer."""

    @abstractmethod
    def score(self, model: ModelT, source: str) -> float:
        """Return one finite score. Higher scores indicate stronger evidence of membership."""

    def score_many(self, model: ModelT, sources: Iterable[str]) -> list[float]:
        """Call score once per file, preserving the input order and duplicates."""
        if isinstance(sources, (str, bytes)):
            raise TypeError("Pass an iterable of source strings, or use score for one file")
        return [self.score(model, source) for source in sources]


@dataclass(frozen=True)
class MembershipThreshold:
    """Predict membership when an oriented score reaches the supplied cutoff."""

    cutoff: float

    def __post_init__(self) -> None:
        if not isfinite(self.cutoff):
            raise ValueError("cutoff must be finite")

    def predict(self, score: float) -> bool:
        """Return True for a finite score at or above the cutoff."""
        if not isfinite(score):
            raise ValueError("score must be finite")
        return bool(score >= self.cutoff)

    def predict_many(self, scores: Iterable[float]) -> list[bool]:
        """Return one prediction per score, in input order."""
        return [self.predict(score) for score in scores]
