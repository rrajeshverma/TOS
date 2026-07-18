from integration.engine_context import EngineContext
from integration.trading_engine import TradingEngine


class FakeMarketEngine:
    def run(self):
        return ["c1", "c2"]


class FakeIndicatorEngine:
    def run(self, candles):
        return {
            "ema": 100,
            "rsi": 61,
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


def test_strategy_flows_to_decision():
    strategy = FakeStrategyEngine()
    decision = FakeDecisionEngine()
    risk = FakeRiskEngine()

    context = EngineContext(
        market_engine=FakeMarketEngine(),
        indicator_engine=FakeIndicatorEngine(),
        strategy_engine=strategy,
        decision_engine=decision,
        risk_engine=risk,
        trade_factory=object(),
        paper_trading_service=object(),
        position_manager=object(),
        trade_journal=object(),
    )

    engine = TradingEngine(context)

    result = engine.run()

    assert strategy.received == {
        "ema": 100,
        "rsi": 61,
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

    assert result == {
        "symbol": "BTCUSDT",
        "action": "BUY",
        "quantity": 1,
        "entry_price": 62000,
        "stop_loss": 61800,
        "target": 62400,
    }