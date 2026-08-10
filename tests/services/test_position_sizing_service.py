"""
=========================================================
Trading Operating System (TOS)

Position Sizing Service Tests
=========================================================
"""

from decimal import Decimal

import pytest

from services.position_sizing_service import (
    PositionSizingService,
)


def test_calculate_one_lot():
    service = PositionSizingService()

    result = service.calculate(
        risk_per_trade=Decimal(1000),
        stop_distance=Decimal(20),
        lot_size=50,
    )

    assert result.lots == 1
    assert result.quantity == 50
    assert result.risk_amount == Decimal(1000)


def test_calculate_two_lots():
    service = PositionSizingService()

    result = service.calculate(
        risk_per_trade=Decimal(2500),
        stop_distance=Decimal(20),
        lot_size=50,
    )

    assert result.lots == 2
    assert result.quantity == 100
    assert result.risk_amount == Decimal(2000)


def test_rounds_down_fractional_lots():
    service = PositionSizingService()

    result = service.calculate(
        risk_per_trade=Decimal(2900),
        stop_distance=Decimal(20),
        lot_size=50,
    )

    assert result.lots == 2
    assert result.quantity == 100


def test_zero_risk_per_trade_raises_error():
    service = PositionSizingService()

    with pytest.raises(ValueError):
        service.calculate(
            risk_per_trade=Decimal(0),
            stop_distance=Decimal(20),
            lot_size=50,
        )


def test_negative_risk_per_trade_raises_error():
    service = PositionSizingService()

    with pytest.raises(ValueError):
        service.calculate(
            risk_per_trade=Decimal(-100),
            stop_distance=Decimal(20),
            lot_size=50,
        )


def test_zero_stop_distance_raises_error():
    service = PositionSizingService()

    with pytest.raises(ValueError):
        service.calculate(
            risk_per_trade=Decimal(1000),
            stop_distance=Decimal(0),
            lot_size=50,
        )


def test_negative_stop_distance_raises_error():
    service = PositionSizingService()

    with pytest.raises(ValueError):
        service.calculate(
            risk_per_trade=Decimal(1000),
            stop_distance=Decimal(-10),
            lot_size=50,
        )


def test_zero_lot_size_raises_error():
    service = PositionSizingService()

    with pytest.raises(ValueError):
        service.calculate(
            risk_per_trade=Decimal(1000),
            stop_distance=Decimal(20),
            lot_size=0,
        )


def test_negative_lot_size_raises_error():
    service = PositionSizingService()

    with pytest.raises(ValueError):
        service.calculate(
            risk_per_trade=Decimal(1000),
            stop_distance=Decimal(20),
            lot_size=-50,
        )


def test_quantity_equals_lots_multiplied_by_lot_size():
    service = PositionSizingService()

    result = service.calculate(
        risk_per_trade=Decimal(5000),
        stop_distance=Decimal(20),
        lot_size=50,
    )

    assert result.quantity == result.lots * 50
