"""Regression for the forward inputs in the FSE reproduction adapter."""

from pathlib import Path
from types import SimpleNamespace

import pytest

pytestmark = pytest.mark.optional_dependency


def test_joint_benchmark_scoring_preserves_tokenizer_attention_mask(monkeypatch):
    torch = pytest.importorskip("torch")
    transformers = pytest.importorskip("transformers")
    pytest.importorskip("numpy")
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    from fse_scoring import BenchmarkScorer

    ids = torch.tensor([[0, 1, 0]])
    mask = torch.ones_like(ids)

    def tokenizer(source, **kwargs):
        return transformers.BatchEncoding({"input_ids": ids, "attention_mask": mask})

    def model(input_ids, attention_mask=None, labels=None, **kwargs):
        assert attention_mask is mask
        assert labels is input_ids
        return SimpleNamespace(logits=torch.zeros(1, 3, 2), loss=torch.tensor(2.0))

    scorer = BenchmarkScorer("loss", {"fixture": ()}, tokenizer, "cpu")
    assert scorer.score_many(model, ["fixture"]) == [-2.0]
