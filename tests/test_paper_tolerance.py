from pathlib import Path

import pytest


@pytest.mark.parametrize(
    ("observed", "reference", "expected"),
    [
        (0.594, 0.6, True),
        (0.606, 0.6, True),
        (0.60601, 0.6, False),
        (0.59399, 0.6, False),
        (-1.01, -1, True),
        (0, 0, True),
        (1e-12, 0, False),
        (float("nan"), 0.6, False),
        (float("inf"), float("inf"), False),
    ],
)
def test_published_value_is_the_denominator(monkeypatch, observed, reference, expected):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    from paper_tolerance import within_one_percent

    assert within_one_percent(observed, reference) is expected
