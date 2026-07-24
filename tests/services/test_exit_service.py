"""
Tests for Exit Service.
"""

from datetime import datetime, time
from decimal import Decimal

from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.order import Order
from domain.position import Position
from domain.risk import Risk
from domain.trade import Trade
from services.exit_service import ExitService
from shared.enums import (
    Broker,
    DecisionStatus,
    ExitReason,
    OrderSide,
    OrderStatus,
    Signal,
    TradeStatus,
)
from utils.id_generator import (
    generate_decision_id,
    generate_order_id,
    generate_position_id,
    generate_trade_id,
)


def create_position():
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=1000,
    )

    indicators = IndicatorSet(
        ema_high=100,
        ema_low=90,
        vwap=100,
        rsi=60,
        volume_average=1000,
    )

    decision = Decision(
        decision_id=generate_decision_id(),
        timestamp=datetime.now(),
        market=market,
        indicator_set=indicators,
        signal=Signal.BUY_CE,
        status=DecisionStatus.VALID,
        reasons=("test",),
    )

    risk = Risk(
        decision=decision,
        approved=True,
        reasons=(),
    )

    trade = Trade(
        trade_id=generate_trade_id(),
        risk=risk,
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        target=Decimal("120"),
        quantity=65,
        entry_time=datetime.now(),
        status=TradeStatus.OPEN,
    )

    order = Order(
        order_id=generate_order_id(),
        broker_order_id="BRK001",
        trade=trade,
        broker=Broker.DHAN,
        side=OrderSide.BUY,
        quantity=65,
        requested_price=Decimal("100"),
        status=OrderStatus.EXECUTED,
    )

    return Position(
        position_id=generate_position_id(),
        order=order,
        quantity=65,
        average_price=Decimal("100"),
        last_traded_price=Decimal("100"),
        status=TradeStatus.OPEN,
        opened_at=datetime.now(),
    )


def test_exit_service_closes_position_on_target():
    service = ExitService()

    position = create_position()

    result = service.evaluate(
        position,
        Decimal("121"),
        time(10, 0),
    )

    assert result["closed"] is True
    assert result["reason"] == ExitReason.TARGET
    assert result["position"].is_closed


def test_exit_service_closes_position_on_stop_loss():
    service = ExitService()

    position = create_position()

    result = service.evaluate(
        position,
        Decimal("89"),
        time(10, 0),
    )

    assert result["closed"] is True
    assert result["reason"] == ExitReason.STOP_LOSS
    assert result["position"].is_closed


def test_exit_service_closes_position_on_force_exit():
    service = ExitService()

    position = create_position()

    result = service.evaluate(
        position,
        Decimal("105"),
        time(15, 16),
    )

    assert result["closed"] is True
    assert result["reason"] == ExitReason.FORCE_EXIT
    assert result["position"].is_closed


def test_exit_service_keeps_position_open_when_no_exit():
    service = ExitService()

    position = create_position()

    result = service.evaluate(
        position,
        Decimal("110"),
        time(10, 0),
    )

    assert result["closed"] is False
    assert result["reason"] == ExitReason.NONE
    assert result["position"].is_open
