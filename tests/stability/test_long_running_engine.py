import uuid

from integration.engine_context import EngineContext
from integration.trading_engine import TradingEngine


class FakeMarketEngine:
    def __init__(self):
        self.calls = 0

    def run(self):
        self.calls += 1
        return [{"symbol": "NIFTY"}]


class FakeIndicatorEngine:
    def __init__(self):
        self.calls = 0

    def run(self, market):
        self.calls += 1
        return market


class FakeStrategyEngine:
    def __init__(self):
        self.calls = 0

    def run(self, indicators):
        self.calls += 1
        return indicators


class FakeDecisionEngine:
    def __init__(self):
        self.calls = 0

    def run(self, signal):
        self.calls += 1
        return signal


class FakeRiskEngine:
    def __init__(self):
        self.calls = 0

    def run(self, decision):
        self.calls += 1
        return {
            "symbol": "NIFTY",
            "side": "BUY",
            "qty": 50,
            "price": 250.0,
        }


class FakeTradeFactory:
    def __init__(self):
        self.calls = 0

    def create(self, trade_plan):
        self.calls += 1
        return {
            "id": str(uuid.uuid4()),
            "symbol": trade_plan["symbol"],
            "side": trade_plan["side"],
            "qty": trade_plan["qty"],
            "price": trade_plan["price"],
            "status": "CREATED",
        }


def build():
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
        paper_trading_service=None,
        position_manager=None,
        trade_journal=None,
    )

    return (
        TradingEngine(context),
        market,
        indicator,
        strategy,
        decision,
        risk,
        trade_factory,
    )


def test_engine_runs_10_times():
    engine, *_ = build()
    for _ in range(10):
        assert engine.run()["status"] == "CREATED"


def test_engine_runs_50_times():
    engine, *_ = build()
    for _ in range(50):
        assert engine.run()["status"] == "CREATED"


def test_engine_runs_100_times():
    engine, *_ = build()
    for _ in range(100):
        assert engine.run()["status"] == "CREATED"


def test_market_engine_called_every_run():
    engine, market, *_ = build()
    for _ in range(20):
        engine.run()
    assert market.calls == 20


def test_indicator_engine_called_every_run():
    engine, _, indicator, *_ = build()
    for _ in range(20):
        engine.run()
    assert indicator.calls == 20


def test_strategy_engine_called_every_run():
    engine, _, _, strategy, *_ = build()
    for _ in range(20):
        engine.run()
    assert strategy.calls == 20


def test_decision_engine_called_every_run():
    engine, _, _, _, decision, *_ = build()
    for _ in range(20):
        engine.run()
    assert decision.calls == 20


def test_risk_engine_called_every_run():
    engine, _, _, _, _, risk, _ = build()
    for _ in range(20):
        engine.run()
    assert risk.calls == 20


def test_trade_factory_called_every_run():
    engine, _, _, _, _, _, trade_factory = build()
    for _ in range(20):
        engine.run()
    assert trade_factory.calls == 20


def test_trade_status_always_created():
    engine, *_ = build()
    for _ in range(50):
        assert engine.run()["status"] == "CREATED"


def test_trade_symbol_consistent():
    engine, *_ = build()
    for _ in range(50):
        assert engine.run()["symbol"] == "NIFTY"


def test_trade_side_consistent():
    engine, *_ = build()
    for _ in range(50):
        assert engine.run()["side"] == "BUY"


def test_trade_quantity_consistent():
    engine, *_ = build()
    for _ in range(50):
        assert engine.run()["qty"] == 50


def test_trade_price_consistent():
    engine, *_ = build()
    for _ in range(50):
        assert engine.run()["price"] == 250.0


def test_long_running_engine_completes():
    engine, *_ = build()

    trade = None
    for _ in range(200):
        trade = engine.run()

    assert trade is not None
    assert trade["status"] == "CREATED"