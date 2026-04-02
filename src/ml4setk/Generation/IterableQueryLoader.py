"""
Iterable dataset that generates samples based on a query.
"""

try:
    from torch.utils.data import IterableDataset
except ModuleNotFoundError:
    class IterableDataset:  # pragma: no cover - simple fallback for optional torch dependency
        """Fallback base class when PyTorch is not installed."""


class IterableQueryLoader(IterableDataset):
    def __init__(self, source_dataset, query, max_samples):
        super().__init__()
        if max_samples is not None and max_samples < 0:
            raise ValueError("max_samples must be None or a non-negative integer.")

        self.source_dataset = source_dataset
        self.query = query
        self.max_samples = max_samples

        self.iterator = iter(self.source_dataset)

        self.i = 0
   
    def __iter__(self):
        self.iterator = iter(self.source_dataset)
        self.i = 0
        return self

    def __next__(self):
        if self.max_samples is not None and self.i >= self.max_samples:
            raise StopIteration

        returnable = None
        while returnable is None:
            file = next(self.iterator)
            returnable = self.process(file, self.query)

        self.i += 1
        return returnable

    def __len__(self):
        if self.max_samples is None:
            return len(self.source_dataset)

        if hasattr(self.source_dataset, "__len__"):
            return max(0, min(len(self.source_dataset), self.max_samples) - self.i)

        return max(0, self.max_samples - self.i)

    def process(self, file, query):
        raise NotImplementedError("Subclasses must implement process(file, query).")
