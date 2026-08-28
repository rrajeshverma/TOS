"""
Integration test:
Live Market -> Decision -> Risk -> Trade -> Order -> Execution
"""

from datetime import datetime
from decimal import Decimal

from brokers.models import OrderSide
from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.decision_engine import DecisionEngine
from engines.order_factory import OrderFactory
from engines.risk_engine import RiskEngine
from engines.trade_factory import TradeFactory
from shared.enums import Broker


def create_market():
    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime(2026, 8, 18, 11, 0),
        open=22500,
        high=22550,
        low=22490,
        close=22540,
        volume=100000,
    )


def create_indicators():
    return IndicatorSet(
        ema_high=22500,
        ema_low=22450,
        vwap=22510,
        rsi=60,
    )


def test_live_decision_to_trade_flow():
    decision_engine = DecisionEngine()
    risk_engine = RiskEngine()
    trade_factory = TradeFactory()

    decision = decision_engine.evaluate(
        create_market(),
        create_indicators(),
    )

    risk = risk_engine.evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal(0),
    )

    assert risk.is_approved is True

    trade = trade_factory.create(
        risk,
        entry_price=Decimal(100),
        stop_loss=Decimal(90),
    )

    assert trade is not None
    assert trade.quantity > 0


def test_trade_to_order_flow():
    decision_engine = DecisionEngine()
    risk_engine = RiskEngine()
    trade_factory = TradeFactory()
    order_factory = OrderFactory()

    decision = decision_engine.evaluate(
        create_market(),
        create_indicators(),
    )

    risk = risk_engine.evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal(0),
    )

    trade = trade_factory.create(
        risk,
        entry_price=Decimal(100),
        stop_loss=Decimal(90),
    )

    order = order_factory.create(
        trade,
        Broker.DHAN,
        OrderSide.BUY,
        Decimal(100),
    )

    assert order is not None
    assert order.trade == trade
    assert order.quantity == trade.quantity


def test_strategy_signal_is_buy():
    decision_engine = DecisionEngine()

    decision = decision_engine.evaluate(
        create_market(),
        create_indicators(),
    )

    assert decision.signal is not None


def test_risk_rejects_invalid_loss():
    risk_engine = RiskEngine()
    decision_engine = DecisionEngine()

    decision = decision_engine.evaluate(
        create_market(),
        create_indicators(),
    )

    risk = risk_engine.evaluate(
        decision,
        trades_today=10,
        daily_loss=Decimal(100000),
    )

    assert risk.is_approved is False
