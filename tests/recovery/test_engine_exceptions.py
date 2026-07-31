import pytest

from integration.engine_context import EngineContext
from integration.trading_engine import TradingEngine


class MarketException(Exception):
    pass


class IndicatorException(Exception):
    pass


class StrategyException(Exception):
    pass


class DecisionException(Exception):
    pass


class RiskException(Exception):
    pass


class TradeFactoryException(Exception):
    pass


class MarketEngineFailure:
    def run(self):
        raise MarketException("Market Engine Failed")


class IndicatorEngineFailure:
    def run(self, market):
        raise IndicatorException("Indicator Engine Failed")


class StrategyEngineFailure:
    def run(self, indicators):
        raise StrategyException("Strategy Engine Failed")


class DecisionEngineFailure:
    def run(self, signal):
        raise DecisionException("Decision Engine Failed")


class RiskEngineFailure:
    def run(self, decision):
        raise RiskException("Risk Engine Failed")


class TradeFactoryFailure:
    def create(self, trade_plan):
        raise TradeFactoryException("Trade Factory Failed")


class FakeMarketEngine:
    def run(self):
        return [{"symbol": "NIFTY"}]


class FakeIndicatorEngine:
    def run(self, market):
        return market


class FakeStrategyEngine:
    def run(self, indicators):
        return indicators


class FakeDecisionEngine:
    def run(self, signal):
        return signal


class FakeRiskEngine:
    def run(self, decision):
        return {
            "symbol": "NIFTY",
            "side": "BUY",
            "qty": 50,
            "price": 250,
        }


class FakeTradeFactory:
    def create(self, trade_plan):
        return trade_plan


def build(
    market,
    indicator,
    strategy,
    decision,
    risk,
    trade_factory,
):
    context = EngineContext(
        market_engine=market,
        indicator_engine=indicator,
        strategy_engine=strategy,
        decision_engine=decision,
        risk_engine=risk,
        trade_factory=trade_factory,
        paper_trading_service=None,
        position_manager=None,
        trade_journal=None,
    )

    return TradingEngine(context)


def test_market_engine_exception():
    engine = build(
        MarketEngineFailure(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        FakeRiskEngine(),
        FakeTradeFactory(),
    )

    with pytest.raises(MarketException):
        engine.run()


def test_indicator_engine_exception():
    engine = build(
        FakeMarketEngine(),
        IndicatorEngineFailure(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        FakeRiskEngine(),
        FakeTradeFactory(),
    )

    with pytest.raises(IndicatorException):
        engine.run()


def test_strategy_engine_exception():
    engine = build(
        FakeMarketEngine(),
        FakeIndicatorEngine(),
        StrategyEngineFailure(),
        FakeDecisionEngine(),
        FakeRiskEngine(),
        FakeTradeFactory(),
    )

    with pytest.raises(StrategyException):
        engine.run()


def test_decision_engine_exception():
    engine = build(
        FakeMarketEngine(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        DecisionEngineFailure(),
        FakeRiskEngine(),
        FakeTradeFactory(),
    )

    with pytest.raises(DecisionException):
        engine.run()


def test_risk_engine_exception():
    engine = build(
        FakeMarketEngine(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        RiskEngineFailure(),
        FakeTradeFactory(),
    )

    with pytest.raises(RiskException):
        engine.run()


def test_trade_factory_exception():
    engine = build(
        FakeMarketEngine(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        FakeRiskEngine(),
        TradeFactoryFailure(),
    )

    with pytest.raises(TradeFactoryException):
        engine.run()


def test_empty_market_data():
    class EmptyMarket:
        def run(self):
            return []

    engine = build(
        EmptyMarket(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        FakeRiskEngine(),
        FakeTradeFactory(),
    )

    assert engine.run()["symbol"] == "NIFTY"


def test_none_market_data():
    class NoneMarket:
        def run(self):
            return None

    engine = build(
        NoneMarket(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        FakeRiskEngine(),
        FakeTradeFactory(),
    )

    assert engine.run()["side"] == "BUY"


def test_empty_indicator_result():
    class EmptyIndicator:
        def run(self, market):
            return []

    engine = build(
        FakeMarketEngine(),
        EmptyIndicator(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        FakeRiskEngine(),
        FakeTradeFactory(),
    )

    assert engine.run()["qty"] == 50


def test_none_strategy_signal():
    class NoneStrategy:
        def run(self, indicators):
            return None

    engine = build(
        FakeMarketEngine(),
        FakeIndicatorEngine(),
        NoneStrategy(),
        FakeDecisionEngine(),
        FakeRiskEngine(),
        FakeTradeFactory(),
    )

    assert engine.run()["price"] == 250


def test_none_decision_result():
    class NoneDecision:
        def run(self, signal):
            return None

    engine = build(
        FakeMarketEngine(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        NoneDecision(),
        FakeRiskEngine(),
        FakeTradeFactory(),
    )

    assert engine.run()["side"] == "BUY"


def test_none_trade_plan():
    class NoneRisk:
        def run(self, decision):
            return None

    class AcceptNoneTradeFactory:
        def create(self, trade_plan):
            return {"status": "CREATED"}

    engine = build(
        FakeMarketEngine(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        NoneRisk(),
        AcceptNoneTradeFactory(),
    )

    assert engine.run()["status"] == "CREATED"


def test_invalid_trade_plan_type():
    class InvalidRisk:
        def run(self, decision):
            return "INVALID"

    class AcceptStringTradeFactory:
        def create(self, trade_plan):
            return {"trade_plan": trade_plan}

    engine = build(
        FakeMarketEngine(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        InvalidRisk(),
        AcceptStringTradeFactory(),
    )

    assert engine.run()["trade_plan"] == "INVALID"


def test_trade_factory_returns_none():
    class NoneTradeFactory:
        def create(self, trade_plan):
            return None

    engine = build(
        FakeMarketEngine(),
        FakeIndicatorEngine(),
        FakeStrategyEngine(),
        FakeDecisionEngine(),
        FakeRiskEngine(),
        NoneTradeFactory(),
    )

    assert engine.run() is None


def test_exception_sequence_completes():
    for _ in range(10):
        engine = build(
            FakeMarketEngine(),
            FakeIndicatorEngine(),
            FakeStrategyEngine(),
            FakeDecisionEngine(),
            FakeRiskEngine(),
            FakeTradeFactory(),
        )

        assert engine.run()["symbol"] == "NIFTY"
