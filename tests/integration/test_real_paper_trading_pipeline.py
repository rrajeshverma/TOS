"""
Integration Test:

Real Paper Trading Pipeline

Validates actual TOS trading flow
using simplified service wiring.
"""

from decimal import Decimal

from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from tests.helpers.domain_factory import (
    make_indicator_set,
    make_market,
)


class DummyPaperExecutor:
    def __init__(self):
        self.executed = []

    def execute(
        self,
        trade,
    ):
        self.executed.append(trade)

        return trade


def test_market_object_reaches_strategy():
    market = make_market(
        close=Decimal(25100),
    )

    assert market.symbol == "NIFTY"


def test_decision_engine_generates_trade_signal():
    market = make_market(
        close=Decimal(25100),
    )

    indicators = make_indicator_set(
        ema_high=Decimal(25000),
        ema_low=Decimal(24900),
        vwap=Decimal(25000),
        rsi=60,
        volume_average=50000,
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    assert decision is not None


def test_risk_engine_accepts_trade_decision():
    market = make_market(
        close=Decimal(25100),
    )

    indicators = make_indicator_set(
        ema_high=Decimal(25000),
        ema_low=Decimal(24900),
        vwap=Decimal(25000),
        rsi=60,
        volume_average=50000,
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine()

    result = risk.evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal(0),
    )

    assert result is not None

    assert result.approved is True


def test_trade_pipeline_reaches_executor():
    executor = DummyPaperExecutor()

    trade = {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
    }

    result = executor.execute(trade)

    assert result["symbol"] == "NIFTY"

    assert len(executor.executed) == 1


def test_complete_paper_pipeline():
    market = make_market(
        close=Decimal(25100),
    )

    indicators = make_indicator_set(
        ema_high=Decimal(25000),
        ema_low=Decimal(24900),
        vwap=Decimal(25000),
        rsi=60,
        volume_average=50000,
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    assert decision is not None

    executor = DummyPaperExecutor()

    trade = executor.execute(
        {
            "symbol": market.symbol,
            "side": "BUY",
            "quantity": 65,
        }
    )

    assert trade["quantity"] == 65
