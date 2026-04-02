from abc import ABC, abstractmethod
from typing import NamedTuple


class QueryMatch(NamedTuple):
    """Represents one match with its surrounding context."""

    prefix: str
    suffix: str
    match: str


class Query(ABC):
    """Base interface for query implementations."""

    @abstractmethod
    def contains(self, string):
        """Return ``True`` when the query matches within ``string``."""

    @abstractmethod
    def parse(self, string):
        """Return ``QueryMatch(prefix, suffix, match)`` values in source order."""
