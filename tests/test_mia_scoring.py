import pytest

from ml4setk.MIA import MembershipScorer, MembershipThreshold


class RecordingScorer(MembershipScorer[object]):
    def __init__(self):
        self.calls = []

    def score(self, model, source):
        self.calls.append((model, source))
        return float(len(source))


def test_score_many_delegates_once_per_file_in_order():
    model = object()
    scorer = RecordingScorer()
    files = ["two\nlines", "", "two\nlines"]
    assert scorer.score_many(model, iter(files)) == [9.0, 0.0, 9.0]
    assert scorer.calls == [(model, source) for source in files]
    assert scorer.score_many(model, []) == []
    assert len(scorer.calls) == len(files)


@pytest.mark.parametrize("single_file", ["abc", "", b"abc"])
def test_score_many_rejects_a_bare_string(single_file):
    scorer = RecordingScorer()
    with pytest.raises(TypeError, match="use score for one file"):
        scorer.score_many(object(), single_file)
    assert scorer.calls == []


def test_threshold_returns_an_ordered_inclusive_mask():
    rule = MembershipThreshold(cutoff=-0.5)
    assert rule.predict(-0.5) is True
    assert rule.predict_many(iter([-0.6, -0.5, 0.2, -0.6])) == [False, True, True, False]
    assert rule.predict_many([]) == []


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -float("inf")])
def test_threshold_requires_finite_values(invalid):
    with pytest.raises(ValueError, match="cutoff"):
        MembershipThreshold(cutoff=invalid)
    with pytest.raises(ValueError, match="score"):
        MembershipThreshold(cutoff=0.0).predict_many([invalid])
