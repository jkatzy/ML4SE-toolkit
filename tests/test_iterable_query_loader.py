import pytest

from ml4setk.Generation.IterableQueryLoader import IterableQueryLoader

pytestmark = pytest.mark.unit


class EvenLoader(IterableQueryLoader):
    def process(self, file, query):
        return file if file % query == 0 else None


def test_iterable_query_loader_limits_output_to_max_samples():
    loader = EvenLoader([1, 2, 3, 4, 5, 6], 2, 2)

    assert list(loader) == [2, 4]


def test_iterable_query_loader_resets_on_new_iteration():
    loader = EvenLoader([1, 2, 3, 4], 2, 1)

    assert list(loader) == [2]
    assert list(loader) == [2]


def test_iterable_query_loader_len_tracks_remaining_requested_samples():
    loader = EvenLoader([1, 2, 3, 4], 2, 2)

    iterator = iter(loader)
    assert len(loader) == 2
    assert next(iterator) == 2
    assert len(loader) == 1


def test_iterable_query_loader_supports_unbounded_iteration():
    loader = EvenLoader([1, 2, 3, 4, 5, 6], 2, None)

    assert list(loader) == [2, 4, 6]


def test_iterable_query_loader_rejects_negative_max_samples():
    with pytest.raises(ValueError):
        EvenLoader([1, 2, 3], 2, -1)
