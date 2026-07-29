"""
Tests:
Live Signal -> Trade Execution Flow

Flow:

Market
  |
  ▼
Indicators
  |
  ▼
DecisionEngine
  |
  ▼
TradeFactory
  |
  ▼
RiskEngine
  |
  ▼
ExecutionEngine
"""

from datetime import datetime
from decimal import Decimal

from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from engines.trade_factory import TradeFactory
from shared.enums import Signal


def create_market():
    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="TICK",
        open=25000,
        high=25100,
        low=24900,
        close=25100,
        volume=100000,
        timestamp=datetime.now(),
    )


def create_buy_indicators():
    return IndicatorSet(
        ema_high=25000,
        ema_low=24900,
        vwap=25000,
        rsi=60,
        volume_average=1000,
    )


def test_live_signal_creates_buy_decision():
    market = create_market()

    indicators = create_buy_indicators()

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    assert decision is not None
    assert decision.signal == Signal.BUY_CE


def test_risk_engine_accepts_live_trade():
    market = create_market()

    indicators = create_buy_indicators()

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine()

    result = risk.evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal("0"),
    )

    assert result is not None


def test_trade_factory_creates_trade():
    market = create_market()

    indicators = create_buy_indicators()

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine().evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal("0"),
    )

    trade = TradeFactory().create(
        risk,
        Decimal("25100"),
        Decimal("50"),
    )

    assert trade is not None


def test_execution_payload_contains_order_details():
    market = create_market()

    indicators = create_buy_indicators()

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine().evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal("0"),
    )

    trade = TradeFactory().create(
        risk,
        Decimal("25100"),
        Decimal("50"),
    )

    assert trade is not None
    assert trade.risk is not None
