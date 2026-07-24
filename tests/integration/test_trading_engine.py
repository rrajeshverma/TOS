from unittest.mock import Mock, call

import pytest

from integration.engine_context import EngineContext
from integration.trading_engine import TradingEngine


class FakeMarketEngine:
    def __init__(self):
        self.called = False

    def run(self):
        self.called = True
        return ["candle1", "candle2"]


class FakeIndicatorEngine:
    def __init__(self):
        self.received = None

    def run(self, market_data):
        self.received = market_data
        return {
            "ema": 100,
            "rsi": 60,
        }


class FakeStrategyEngine:
    def __init__(self):
        self.received = None

    def run(self, indicators):
        self.received = indicators
        return {
            "action": "BUY",
            "symbol": "BTCUSDT",
        }


class FakeDecisionEngine:
    def __init__(self):
        self.received = None

    def run(self, signal):
        self.received = signal
        return {
            "approved": True,
            "action": signal["action"],
            "symbol": signal["symbol"],
        }


class FakeRiskEngine:
    def __init__(self):
        self.received = None

    def run(self, decision):
        self.received = decision
        return {
            "symbol": decision["symbol"],
            "action": decision["action"],
            "quantity": 1,
            "entry_price": 62000,
            "stop_loss": 61800,
            "target": 62400,
        }


class FakeTradeFactory:
    def __init__(self):
        self.received = None

    def create(self, trade_plan):
        self.received = trade_plan

        return {
            "id": "TRADE-001",
            "symbol": trade_plan["symbol"],
            "action": trade_plan["action"],
            "quantity": trade_plan["quantity"],
            "entry_price": trade_plan["entry_price"],
            "stop_loss": trade_plan["stop_loss"],
            "target": trade_plan["target"],
        }


def test_trading_engine_pipeline():
    market = FakeMarketEngine()
    indicator = FakeIndicatorEngine()
    strategy = FakeStrategyEngine()
    decision = FakeDecisionEngine()
    risk = FakeRiskEngine()
    trade_factory = FakeTradeFactory()

    context = EngineContext(
        market_engine=market,
        indicator_engine=indicator,
        strategy_engine=strategy,
        decision_engine=decision,
        risk_engine=risk,
        trade_factory=trade_factory,
        paper_trading_service=object(),
        position_manager=object(),
        trade_journal=object(),
    )

    engine = TradingEngine(context)

    trade = engine.run()

    assert market.called is True

    assert indicator.received == [
        "candle1",
        "candle2",
    ]

    assert strategy.received == {
        "ema": 100,
        "rsi": 60,
    }

    assert decision.received == {
        "action": "BUY",
        "symbol": "BTCUSDT",
    }

    assert risk.received == {
        "approved": True,
        "action": "BUY",
        "symbol": "BTCUSDT",
    }

    assert trade_factory.received == {
        "symbol": "BTCUSDT",
        "action": "BUY",
        "quantity": 1,
        "entry_price": 62000,
        "stop_loss": 61800,
        "target": 62400,
    }

    assert trade == {
        "id": "TRADE-001",
        "symbol": "BTCUSDT",
        "action": "BUY",
        "quantity": 1,
        "entry_price": 62000,
        "stop_loss": 61800,
        "target": 62400,
    }


def test_trading_engine_has_context():
    context = EngineContext(
        market_engine=object(),
        indicator_engine=object(),
        strategy_engine=object(),
        decision_engine=object(),
        risk_engine=object(),
        trade_factory=object(),
        paper_trading_service=object(),
        position_manager=object(),
        trade_journal=object(),
    )

    engine = TradingEngine(context)

    assert engine.context is context

    def create_context():
        context = Mock(spec=EngineContext)

        context.market_engine.run.return_value = "market"
        context.indicator_engine.run.return_value = "indicators"
        context.strategy_engine.run.return_value = "signal"
        context.decision_engine.run.return_value = "decision"
        context.risk_engine.run.return_value = "plan"
        context.trade_factory.create.return_value = "trade"

        return context


    def test_run_returns_trade():
        context = create_context()

        engine = TradingEngine(context)

        assert engine.run() == "trade"


    def test_market_engine_called_once():
        context = create_context()

        TradingEngine(context).run()

        context.market_engine.run.assert_called_once_with()


    def test_indicator_receives_market_data():
        context = create_context()

        TradingEngine(context).run()

        context.indicator_engine.run.assert_called_once_with("market")


    def test_strategy_receives_indicators():
        context = create_context()

        TradingEngine(context).run()

        context.strategy_engine.run.assert_called_once_with("indicators")


    def test_decision_receives_signal():
        context = create_context()

        TradingEngine(context).run()

        context.decision_engine.run.assert_called_once_with("signal")


    def test_risk_receives_decision():
        context = create_context()

        TradingEngine(context).run()

        context.risk_engine.run.assert_called_once_with("decision")


    def test_trade_factory_receives_trade_plan():
        context = create_context()

        TradingEngine(context).run()

        context.trade_factory.create.assert_called_once_with("plan")


    def test_market_exception_propagates():
        context = create_context()

        context.market_engine.run.side_effect = RuntimeError("market failed")

        with pytest.raises(RuntimeError):
            TradingEngine(context).run()


    def test_indicator_exception_propagates():
        context = create_context()

        context.indicator_engine.run.side_effect = ValueError()

        with pytest.raises(ValueError):
            TradingEngine(context).run()


    def test_strategy_exception_propagates():
        context = create_context()

        context.strategy_engine.run.side_effect = RuntimeError()

        with pytest.raises(RuntimeError):
            TradingEngine(context).run()


    def test_decision_exception_propagates():
        context = create_context()

        context.decision_engine.run.side_effect = RuntimeError()

        with pytest.raises(RuntimeError):
            TradingEngine(context).run()


    def test_risk_exception_propagates():
        context = create_context()

        context.risk_engine.run.side_effect = RuntimeError()

        with pytest.raises(RuntimeError):
            TradingEngine(context).run()


    def test_trade_factory_exception_propagates():
        context = create_context()

        context.trade_factory.create.side_effect = RuntimeError()

        with pytest.raises(RuntimeError):
            TradingEngine(context).run()


    def test_trade_factory_called_once():
        context = create_context()

        TradingEngine(context).run()

        assert context.trade_factory.create.call_count == 1


    def test_market_called_before_indicator():
        context = create_context()

        TradingEngine(context).run()

        assert context.mock_calls.index(call.market_engine.run()) < context.mock_calls.index(
            call.indicator_engine.run("market")
        )


    def test_indicator_called_before_strategy():
        context = create_context()

        TradingEngine(context).run()

        assert context.mock_calls.index(
            call.indicator_engine.run("market")
        ) < context.mock_calls.index(call.strategy_engine.run("indicators"))