"""
Tests for TradingPipeline.
"""

from datetime import datetime
from decimal import Decimal

import pytest

from domain.indicator_set import IndicatorSet
from domain.market import Market
from runtime.trading_pipeline import TradingPipeline
from shared.enums import Signal


class FakeDecision:
    signal = Signal.BUY_CE


class FakeDecisionEngine:
    def __init__(self):
        self.called = False

    def evaluate(self, market, indicators):
        self.called = True
        return FakeDecision()


class FakeMarket:
    symbol = "NIFTY"
    exchange = "NSE"
    timeframe = "5m"
    open = 100
    high = 110
    low = 95
    close = 105
    volume = 1000


class FakeRiskEngine:
    def __init__(self):
        self.called = False
        self.trades_today = None
        self.daily_loss = None

    def evaluate(
        self,
        decision,
        trades_today,
        daily_loss,
    ):
        self.called = True
        self.trades_today = trades_today
        self.daily_loss = daily_loss
        return "RISK"


class FakeIndicatorEngine:
    def __init__(self):
        self.called = False

    def calculate(self, candles):
        self.called = True

        return IndicatorSet(
            ema_high=107.0,
            ema_low=98.0,
            vwap=103.0,
            rsi=60.0,
        )


class FakeTradeJournal:
    def __init__(
        self,
        trades_today=0,
        daily_pnl=Decimal("0"),
    ):
        self.trades_today = trades_today
        self.daily_pnl_value = daily_pnl
        self.count_called = False
        self.pnl_called = False

    def count_today(self):
        self.count_called = True
        return self.trades_today

    def daily_pnl(self):
        self.pnl_called = True
        return self.daily_pnl_value


class Dummy:
    pass


class FakeCandle:
    def __init__(
        self,
        high=110,
        low=95,
        close=105,
    ):
        self.high = high
        self.low = low
        self.close = close


def create_candles():
    return [
        Market(
            symbol="NIFTY",
            exchange="NSE",
            timeframe="5m",
            timestamp=datetime(2026, 8, 11, 9, 15),
            open=100,
            high=108,
            low=96,
            close=104,
            volume=1000,
        ),
        Market(
            symbol="NIFTY",
            exchange="NSE",
            timeframe="5m",
            timestamp=datetime(2026, 8, 11, 9, 20),
            open=104,
            high=110,
            low=95,
            close=105,
            volume=1200,
        ),
    ]


def create_pipeline(trade_journal=None):
    return TradingPipeline(
        indicator_engine=FakeIndicatorEngine(),
        decision_engine=FakeDecisionEngine(),
        trade_quality_engine=FakeTradeQualityEngine(),
        risk_engine=FakeRiskEngine(),
        position_sizing_engine=FakePositionSizingEngine(),
        trade_planning_engine=FakeTradePlanningEngine(),
        trade_management_engine=FakeTradeManagementEngine(),
        trade_journal=trade_journal,
    )


def test_pipeline_rejects_none_history():
    pipeline = create_pipeline()

    with pytest.raises(ValueError):
        pipeline.run(None)


def test_pipeline_rejects_empty_history():
    pipeline = create_pipeline()

    with pytest.raises(ValueError):
        pipeline.run([])


def test_pipeline_calls_indicator_engine():
    pipeline = create_pipeline()

    pipeline.run(create_candles())

    assert pipeline._indicator_engine.called is True


def test_pipeline_returns_market_and_indicators():
    pipeline = create_pipeline()

    (
        market,
        indicators,
        _decision,
        _quality,
        risk,
        position_size,
        _trade_plan,
        _,
    ) = pipeline.run(create_candles())

    assert isinstance(market, Market)
    assert isinstance(indicators, IndicatorSet)
    assert risk == "RISK"
    assert position_size == "POSITION_SIZE"


def test_pipeline_calls_decision_engine():
    pipeline = create_pipeline()

    pipeline.run(create_candles())

    assert pipeline._decision_engine.called is True


def test_pipeline_returns_decision():
    pipeline = create_pipeline()

    (
        market,
        indicators,
        decision,
        quality,
        risk,
        position_size,
        _trade_plan,
        _,
    ) = pipeline.run(create_candles())

    assert isinstance(market, Market)
    assert isinstance(indicators, IndicatorSet)
    assert isinstance(decision, FakeDecision)
    assert quality == "QUALITY"
    assert risk == "RISK"
    assert position_size == "POSITION_SIZE"


class FakeTradeQualityEngine:
    def __init__(self):
        self.called = False

    def evaluate(self, decision, trades_today):
        self.called = True
        return "QUALITY"


def test_pipeline_calls_trade_quality_engine():
    pipeline = create_pipeline()

    pipeline.run(create_candles())

    assert pipeline._trade_quality_engine.called


def test_pipeline_returns_trade_quality():
    pipeline = create_pipeline()

    _, _, _, quality, _, _, _, _ = pipeline.run(create_candles())

    assert quality == "QUALITY"

    def evaluate(
        self,
        decision,
        trades_today,
        daily_loss,
    ):
        self.called = True
        return "RISK"


class FakePositionSizingEngine:
    def __init__(self):
        self.called = False

    def calculate(
        self,
        capital,
        risk_percent,
        stop_loss_distance,
        lot_size=1,
    ):
        self.called = True
        return "POSITION_SIZE"


def test_pipeline_calls_risk_engine():
    pipeline = create_pipeline()

    pipeline.run(create_candles())

    assert pipeline._risk_engine.called


def test_pipeline_returns_risk():
    pipeline = create_pipeline()

    _, _, _, _, risk, _, _, _ = pipeline.run(create_candles())

    assert risk == "RISK"


def test_pipeline_calls_position_sizing_engine():
    pipeline = create_pipeline()

    pipeline.run(create_candles())

    assert pipeline._position_sizing_engine.called


def test_pipeline_returns_position_size():
    pipeline = create_pipeline()

    (
        _,
        _,
        _,
        _,
        _,
        position_size,
        _,
        _,
    ) = pipeline.run(create_candles())

    assert position_size == "POSITION_SIZE"


class FakeTradePlanningEngine:
    def __init__(self):
        self.called = False

    def create_plan(
        self,
        decision,
        position_size,
        entry_price,
        stop_loss,
        target_price,
    ):
        self.called = True
        return "TRADE_PLAN"


def test_pipeline_calls_trade_planning_engine():
    pipeline = create_pipeline()

    pipeline.run(create_candles())

    assert pipeline._trade_planning_engine.called


def test_pipeline_returns_trade_plan():
    pipeline = create_pipeline()

    (
        _,
        _,
        _,
        _,
        _,
        _,
        trade_plan,
        _,
    ) = pipeline.run(create_candles())

    assert trade_plan == "TRADE_PLAN"


class FakeTradeManagementEngine:
    def __init__(self):
        self.called = False

    def evaluate(
        self,
        entry_price,
        stop_loss,
        current_price,
    ):
        self.called = True
        return "TRADE_MANAGEMENT"


def test_pipeline_calls_trade_management_engine():
    pipeline = create_pipeline()

    pipeline.run(create_candles())

    assert pipeline._trade_management_engine.called


def test_pipeline_returns_trade_management():
    pipeline = create_pipeline()

    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        trade_management,
    ) = pipeline.run(create_candles())

    assert trade_management == "TRADE_MANAGEMENT"


def test_pipeline_uses_trade_journal_for_daily_risk():
    journal = FakeTradeJournal(
        trades_today=2,
        daily_pnl=Decimal("-1500"),
    )

    pipeline = create_pipeline(
        trade_journal=journal,
    )

    pipeline.run(create_candles())

    assert journal.count_called is True
    assert journal.pnl_called is True


def test_pipeline_passes_journal_risk_values_to_risk_engine():
    journal = FakeTradeJournal(
        trades_today=2,
        daily_pnl=Decimal("-1500"),
    )

    pipeline = create_pipeline(
        trade_journal=journal,
    )

    pipeline.run(create_candles())

    # We'll inspect the fake RiskEngine after the test run.


def test_pipeline_passes_journal_values_to_risk_engine():
    journal = FakeTradeJournal(
        trades_today=2,
        daily_pnl=Decimal("-1500"),
    )

    pipeline = create_pipeline(
        trade_journal=journal,
    )

    pipeline.run(create_candles())

    assert pipeline._risk_engine.trades_today == 2
    assert pipeline._risk_engine.daily_loss == Decimal("1500")


def test_pipeline_does_not_treat_profit_as_daily_loss():
    journal = FakeTradeJournal(
        trades_today=1,
        daily_pnl=Decimal("2500"),
    )

    pipeline = create_pipeline(
        trade_journal=journal,
    )

    pipeline.run(create_candles())

    assert pipeline._risk_engine.trades_today == 1
    assert pipeline._risk_engine.daily_loss == Decimal("0")
