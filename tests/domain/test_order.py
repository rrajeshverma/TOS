from dataclasses import FrozenInstanceError, is_dataclass, replace
from datetime import datetime
from decimal import Decimal

import pytest

from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.order import Order
from domain.risk import Risk
from domain.trade import Trade
from shared.enums import (
    Broker,
    DecisionStatus,
    OrderSide,
    OrderStatus,
    Signal,
)


def create_order():
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=24100,
        high=24125,
        low=24095,
        close=24120,
        volume=100000,
    )

    indicators = IndicatorSet(
        ema_high=24150,
        ema_low=24130,
        vwap=24120,
        rsi=55,
    )

    decision = Decision(
        decision_id="D001",
        timestamp=datetime.now(),
        market=market,
        indicator_set=indicators,
        signal=Signal.BUY_CE,
        status=DecisionStatus.VALID,
        reasons=("Valid",),
    )

    risk = Risk(
        decision=decision,
        approved=True,
        reasons=("Approved",),
    )

    trade = Trade(
        trade_id="T001",
        risk=risk,
        entry_price=Decimal("248.35"),
        stop_loss=Decimal("242.10"),
        target=Decimal("260.85"),
        quantity=400,
        entry_time=datetime.now(),
    )

    return Order(
        order_id="ORD001",
        broker_order_id=None,
        trade=trade,
        broker=Broker.DHAN,
        side=OrderSide.BUY,
        quantity=400,
        requested_price=Decimal("248.35"),
    )


def test_order_is_dataclass():
    assert is_dataclass(Order)


def test_order_id():
    assert create_order().order_id == "ORD001"


def test_default_status():
    assert create_order().status == OrderStatus.CREATED


def test_order_default_is_not_pending():
    assert not create_order().is_pending


def test_order_not_executed():
    assert not create_order().is_executed


def test_order_broker():
    assert create_order().broker == Broker.DHAN


def test_order_side():
    assert create_order().side == OrderSide.BUY


def test_requested_price_decimal():
    assert create_order().requested_price == Decimal("248.35")


def test_optional_broker_order_id():
    assert create_order().broker_order_id is None


def test_order_is_immutable():
    order = create_order()

    with pytest.raises(FrozenInstanceError):
        order.quantity = 100


def test_order_is_pending():
    order = replace(
        create_order(),
        status=OrderStatus.PENDING,
    )

    assert order.is_pending
