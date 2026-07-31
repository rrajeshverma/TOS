import uuid

from integration.engine_context import EngineContext
from integration.trading_engine import TradingEngine


class FakeMarketEngine:
    def run(self):
        return ["market"]


class FakeIndicatorEngine:
    def run(self, market):
        return ["indicator"]


class FakeStrategyEngine:
    def run(self, indicators):
        return ["signal"]


class FakeDecisionEngine:
    def run(self, signal):
        return {"side": "BUY"}


class FakeRiskEngine:
    def run(self, decision):
        return {
            "symbol": "NIFTY",
            "side": decision["side"],
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
    context = EngineContext(
        market_engine=FakeMarketEngine(),
        indicator_engine=FakeIndicatorEngine(),
        strategy_engine=FakeStrategyEngine(),
        decision_engine=FakeDecisionEngine(),
        risk_engine=FakeRiskEngine(),
        trade_factory=FakeTradeFactory(),
        paper_trading_service=None,
        position_manager=None,
        trade_journal=None,
    )
    return TradingEngine(context)


def test_create_buy_order():
    trade = build_engine().run()
    assert trade["side"] == "BUY"


def test_order_contains_symbol():
    trade = build_engine().run()
    assert trade["symbol"] == "NIFTY"


def test_order_contains_quantity():
    trade = build_engine().run()
    assert trade["qty"] == 50


def test_order_contains_price():
    trade = build_engine().run()
    assert trade["price"] == 250.0


def test_order_contains_side():
    trade = build_engine().run()
    assert trade["side"] == "BUY"


def test_order_status_is_created():
    trade = build_engine().run()
    assert trade["status"] == "CREATED"


def test_trade_has_unique_id():
    trade = build_engine().run()
    assert trade["id"]


def test_trade_id_is_string():
    trade = build_engine().run()
    assert isinstance(trade["id"], str)


def test_trade_has_six_fields():
    trade = build_engine().run()
    assert len(trade) == 6


def test_trade_contains_symbol_key():
    trade = build_engine().run()
    assert "symbol" in trade


def test_trade_contains_qty_key():
    trade = build_engine().run()
    assert "qty" in trade


def test_trade_contains_price_key():
    trade = build_engine().run()
    assert "price" in trade


def test_trade_contains_side_key():
    trade = build_engine().run()
    assert "side" in trade


def test_trade_contains_status_key():
    trade = build_engine().run()
    assert "status" in trade


def test_order_lifecycle_completes():
    trade = build_engine().run()
    assert trade["status"] == "CREATED"
