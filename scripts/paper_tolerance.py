"""Acceptance rule for comparisons with published numerical results."""

from decimal import Decimal


def within_one_percent(observed, reference):
    """Use the magnitude of the published value as denominator. Zero must match exactly."""
    value = Decimal(str(observed))
    target = Decimal(str(reference))
    return value.is_finite() and target.is_finite() and abs(value - target) <= abs(target) / 100
