import pytest

from ml4setk.Extraction import (
    canary_rank,
    exposure_bits,
    memorization_overlap,
    memorization_score,
    verify_pythia_records,
    verify_suffixes,
)


def test_known_canary_worst_tie_rank():
    rank = canary_rank(1.0, iter([0.5, 1.0, 2.0]))
    assert rank == 3
    assert exposure_bits(6, rank) == pytest.approx(1.0)
    assert exposure_bits(1, 1) == 0.0


@pytest.mark.parametrize("size,rank", [(0, 1), (4, 0), (4, 5), (4, 1.5)])
def test_invalid_rank(size, rank):
    with pytest.raises(ValueError):
        exposure_bits(size, rank)


def test_invalid_loss():
    with pytest.raises(ValueError):
        canary_rank(0, [float("nan")])
    with pytest.raises(ValueError):
        canary_rank(float("inf"), [])


def test_agreement_and_unique_ids():
    assert memorization_score([5, 8], [7, 8]) == 0.5
    assert memorization_overlap([1, 1, 2], [1, 3, 4]) == (0.5, 1 / 3)
    with pytest.raises(ValueError):
        memorization_score([], [])
    with pytest.raises(ValueError):
        memorization_score([0], [0, 1])
    with pytest.raises(ValueError):
        memorization_overlap([], [1])


@pytest.mark.optional_dependency
def test_known_suffix_alignment_and_model_override():
    from types import SimpleNamespace

    torch = pytest.importorskip("torch")

    class Successor(torch.nn.Module):
        device = torch.device("cpu")

        def forward(self, ids, use_cache):
            return SimpleNamespace(logits=torch.nn.functional.one_hot((ids + 1) % 4, 4))

    model = Successor().eval()
    assert verify_suffixes([[3, 2, 3, 0], [3, 2, 1, 2]], prefix_length=2, model=model) == [
        True,
        False,
    ]
    assert verify_pythia_records([[i % 4 for i in range(64)]], model=model) == [True]
    with pytest.raises(ValueError):
        verify_pythia_records([[0, 1]], model=model)
    with pytest.raises(ValueError):
        verify_suffixes([[1, 2]], prefix_length=2, model=model)
    with pytest.raises(ValueError):
        verify_suffixes([[1, 2]], prefix_length=1, model=model.train())
