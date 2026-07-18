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