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
            "price": 250.0,
        }


class FakeTradeFactory:
    def create(self, trade_plan):
        return {
            "id": str(uuid.uuid4()),
            "symbol": trade_plan["symbol"],
            "side": trade_plan["side"],
            "qty": trade_plan["qty"],
            "price": trade_plan["price"],
            "status": "CREATED",
        }


def build_engine():
    market = FakeMarketEngine()

    context = EngineContext(
        market_engine=market,
        indicator_engine=FakeIndicatorEngine(),
        strategy_engine=FakeStrategyEngine(),
        decision_engine=FakeDecisionEngine(),
        risk_engine=FakeRiskEngine(),
        trade_factory=FakeTradeFactory(),
        paper_trading_service=None,
        position_manager=None,
        trade_journal=None,
    )

    return TradingEngine(context), market


def test_engine_can_restart():
    engine, _ = build_engine()
    assert engine.run()["status"] == "CREATED"


def test_multiple_restarts():
    for _ in range(10):
        engine, _ = build_engine()
        assert engine.run()["status"] == "CREATED"


def test_restart_returns_trade():
    engine, _ = build_engine()
    trade = engine.run()
    assert trade is not None


def test_restart_preserves_symbol():
    engine, _ = build_engine()
    assert engine.run()["symbol"] == "NIFTY"


def test_restart_preserves_side():
    engine, _ = build_engine()
    assert engine.run()["side"] == "BUY"


def test_restart_preserves_quantity():
    engine, _ = build_engine()
    assert engine.run()["qty"] == 50


def test_restart_preserves_price():
    engine, _ = build_engine()
    assert engine.run()["price"] == 250.0


def test_restart_trade_status():
    engine, _ = build_engine()
    assert engine.run()["status"] == "CREATED"


def test_restart_trade_has_id():
    engine, _ = build_engine()
    assert engine.run()["id"]


def test_restart_market_called_once():
    engine, market = build_engine()
    engine.run()
    assert market.calls == 1


def test_restart_market_called_twice():
    engine, market = build_engine()
    engine.run()
    engine.run()
    assert market.calls == 2


def test_restart_market_called_ten_times():
    engine, market = build_engine()
    for _ in range(10):
        engine.run()
    assert market.calls == 10


def test_trade_ids_are_unique_after_restart():
    ids = set()

    for _ in range(20):
        engine, _ = build_engine()
        ids.add(engine.run()["id"])

    assert len(ids) == 20


def test_restart_returns_dictionary():
    engine, _ = build_engine()
    assert isinstance(engine.run(), dict)


def test_restart_sequence_completes():
    for _ in range(25):
        engine, _ = build_engine()
        trade = engine.run()
        assert trade["status"] == "CREATED"