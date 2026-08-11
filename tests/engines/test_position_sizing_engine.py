"""
Tests for PositionSizingEngine.
"""

from decimal import Decimal

import pytest

from engines.position_sizing_engine import PositionSizingEngine


def test_calculate_position_size():
    engine = PositionSizingEngine()

    result = engine.calculate(
        capital=Decimal(100000),
        risk_percent=Decimal(2),
        stop_loss_distance=Decimal(500),
    )

    assert result.risk_amount == Decimal(2000)
    assert result.quantity == 4
    assert result.lots == 4


@pytest.mark.parametrize(
    "capital,risk,sl",
    [
        (Decimal(0), Decimal(2), Decimal(500)),
        (Decimal(100000), Decimal(0), Decimal(500)),
        (Decimal(100000), Decimal(2), Decimal(0)),
    ],
)
def test_invalid_inputs(
    capital,
    risk,
    sl,
):
    engine = PositionSizingEngine()

    with pytest.raises(ValueError):
        engine.calculate(
            capital=capital,
            risk_percent=risk,
            stop_loss_distance=sl,
        )


def test_invalid_lot_size():
    engine = PositionSizingEngine()

    with pytest.raises(ValueError):
        engine.calculate(
            capital=Decimal(100000),
            risk_percent=Decimal(2),
            stop_loss_distance=Decimal(500),
            lot_size=0,
        )


def test_calculate_position_size_with_instrument_lot_size():
    engine = PositionSizingEngine()

    result = engine.calculate(
        capital=Decimal(100000),
        risk_percent=Decimal(2),
        stop_loss_distance=Decimal(10),
        lot_size=65,
    )

    assert result.risk_amount == Decimal(2000)
    assert result.lots == 3
    assert result.quantity == 195
