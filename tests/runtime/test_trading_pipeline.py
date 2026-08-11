"""
Tests for TradingPipeline.
"""

import pytest

from runtime.trading_pipeline import TradingPipeline


class FakeMarketEngine:
    def __init__(self):
        self.called = False

    def build_market(self, candle):
        self.called = True
        return "MARKET"


class FakeIndicatorEngine:
    def __init__(self):
        self.called = False

    def calculate(self, candles):
        self.called = True
        return "INDICATORS"


class Dummy:
    pass


def create_pipeline():
    return TradingPipeline(
        market_engine=FakeMarketEngine(),
        indicator_engine=FakeIndicatorEngine(),
        decision_engine=FakeDecisionEngine(),
        trade_quality_engine=FakeTradeQualityEngine(),
        risk_engine=FakeRiskEngine(),
        position_sizing_engine=FakePositionSizingEngine(),
        trade_planning_engine=FakeTradePlanningEngine(),
        trade_management_engine=FakeTradeManagementEngine(),
    )


def test_pipeline_rejects_none_history():
    pipeline = create_pipeline()

    with pytest.raises(ValueError):
        pipeline.run(None)


def test_pipeline_rejects_empty_history():
    pipeline = create_pipeline()

    with pytest.raises(ValueError):
        pipeline.run([])


def test_pipeline_calls_market_engine():
    pipeline = create_pipeline()

    pipeline.run(["CANDLE"])

    assert pipeline._market_engine.called is True


def test_pipeline_calls_indicator_engine():
    pipeline = create_pipeline()

    pipeline.run(["CANDLE"])

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
    ) = pipeline.run(["CANDLE"])

    assert market == "MARKET"
    assert indicators == "INDICATORS"
    assert risk == "RISK"
    assert position_size == "POSITION_SIZE"


class FakeDecisionEngine:
    def __init__(self):
        self.called = False

    def evaluate(self, market, indicators):
        self.called = True
        return "DECISION"


def test_pipeline_calls_decision_engine():
    pipeline = create_pipeline()

    pipeline.run(["CANDLE"])

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
    ) = pipeline.run(["CANDLE"])

    assert market == "MARKET"
    assert indicators == "INDICATORS"
    assert decision == "DECISION"
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

    pipeline.run(["CANDLE"])

    assert pipeline._trade_quality_engine.called


def test_pipeline_returns_trade_quality():
    pipeline = create_pipeline()

    _, _, _, quality, _, _, _, _ = pipeline.run(["CANDLE"])

    assert quality == "QUALITY"


class FakeRiskEngine:
    def __init__(self):
        self.called = False

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

    pipeline.run(["CANDLE"])

    assert pipeline._risk_engine.called


def test_pipeline_returns_risk():
    pipeline = create_pipeline()

    _, _, _, _, risk, _, _, _ = pipeline.run(["CANDLE"])

    assert risk == "RISK"


def test_pipeline_calls_position_sizing_engine():
    pipeline = create_pipeline()

    pipeline.run(["CANDLE"])

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
    ) = pipeline.run(["CANDLE"])

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

    pipeline.run(["CANDLE"])

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
    ) = pipeline.run(["CANDLE"])

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

    pipeline.run(["CANDLE"])

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
    ) = pipeline.run(["CANDLE"])

    assert trade_management == "TRADE_MANAGEMENT"
