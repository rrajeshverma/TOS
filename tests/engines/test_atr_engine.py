from decimal import Decimal

import pytest

from engines.atr_engine import ATREngine


def test_calculate_atr():
    engine = ATREngine()

    atr = engine.calculate(
        [
            Decimal("10"),
            Decimal("20"),
            Decimal("30"),
        ],
        period=3,
    )

    assert atr.period == 3
    assert atr.value == Decimal("20")


def test_invalid_period():
    engine = ATREngine()

    with pytest.raises(ValueError):
        engine.calculate(
            [Decimal("10")],
            period=0,
        )


def test_not_enough_values():
    engine = ATREngine()

    with pytest.raises(ValueError):
        engine.calculate(
            [Decimal("10")],
            period=14,
        )
