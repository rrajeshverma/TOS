from decimal import Decimal

import pytest

from engines.atr_stop_engine import ATRStopEngine


def test_calculate_stop():
    engine = ATRStopEngine()

    stop = engine.calculate(
        entry_price=Decimal("25000"),
        atr=Decimal("100"),
    )

    assert stop == Decimal("24850")


def test_invalid_atr():
    engine = ATRStopEngine()

    with pytest.raises(ValueError):
        engine.calculate(
            entry_price=Decimal("25000"),
            atr=Decimal("0"),
        )


def test_invalid_multiplier():
    engine = ATRStopEngine()

    with pytest.raises(ValueError):
        engine.calculate(
            entry_price=Decimal("25000"),
            atr=Decimal("100"),
            multiplier=Decimal("0"),
        )
