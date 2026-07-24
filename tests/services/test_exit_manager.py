"""
Tests for Exit Manager.
"""

from datetime import datetime, time
from decimal import Decimal

from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.order import Order
from domain.risk import Risk
from domain.trade import Trade
from services.exit_manager import ExitManager
from shared.enums import (
    Broker,
    DecisionStatus,
    ExitReason,
    OrderSide,
    TradeStatus,
    Signal,
)
from utils.id_generator import (
    generate_decision_id,
    generate_order_id,
    generate_trade_id,
)


def create_position(
    entry_price=Decimal("100"),
    stop_loss=Decimal("95"),
    target=Decimal("120"),
):
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5M",
        timestamp=datetime.now(),
        open=100,
        high=105,
        low=99,
        close=102,
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
        entry_price=entry_price,
        stop_loss=stop_loss,
        target=target,
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
        requested_price=entry_price,
        status=TradeStatus.OPEN,
    )

    from domain.position import Position
    from utils.id_generator import generate_position_id

    return Position(
        position_id=generate_position_id(),
        order=order,
        quantity=65,
        average_price=entry_price,
        last_traded_price=entry_price,
        status=TradeStatus.OPEN,
        opened_at=datetime.now(),
    )


def test_target_hit_returns_target():
    manager = ExitManager()

    position = create_position()

    result = manager.check_exit(
        position,
        Decimal("121"),
        time(10, 0),
    )

    assert result == ExitReason.TARGET


def test_stop_loss_hit_returns_stop_loss():
    manager = ExitManager()

    position = create_position()

    result = manager.check_exit(
        position,
        Decimal("94"),
        time(10, 0),
    )

    assert result == ExitReason.STOP_LOSS


def test_force_exit_returns_force_exit():
    manager = ExitManager()

    position = create_position()

    result = manager.check_exit(
        position,
        Decimal("105"),
        time(15, 16),
    )

    assert result == ExitReason.FORCE_EXIT


def test_no_exit_returns_none():
    manager = ExitManager()

    position = create_position()

    result = manager.check_exit(
        position,
        Decimal("110"),
        time(10, 0),
    )

    assert result == ExitReason.NONE
