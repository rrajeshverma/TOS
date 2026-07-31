import uuid

from integration.engine_context import EngineContext
from integration.trading_engine import TradingEngine


class FakeMarketEngine:
    def __init__(self, symbol):
        self.symbol = symbol

    def run(self):
        return [{"symbol": self.symbol}]


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
            "symbol": decision[0]["symbol"],
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


def build_engine(symbol):
    context = EngineContext(
        market_engine=FakeMarketEngine(symbol),
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


def test_nifty_symbol():
    assert build_engine("NIFTY").run()["symbol"] == "NIFTY"


def test_banknifty_symbol():
    assert build_engine("BANKNIFTY").run()["symbol"] == "BANKNIFTY"


def test_finnifty_symbol():
    assert build_engine("FINNIFTY").run()["symbol"] == "FINNIFTY"


def test_midcpnifty_symbol():
    assert build_engine("MIDCPNIFTY").run()["symbol"] == "MIDCPNIFTY"


def test_sensex_symbol():
    assert build_engine("SENSEX").run()["symbol"] == "SENSEX"


def test_bankex_symbol():
    assert build_engine("BANKEX").run()["symbol"] == "BANKEX"


def test_symbol_preserved():
    trade = build_engine("NIFTY").run()
    assert trade["symbol"] == "NIFTY"


def test_trade_side_preserved():
    trade = build_engine("NIFTY").run()
    assert trade["side"] == "BUY"


def test_quantity_preserved():
    trade = build_engine("NIFTY").run()
    assert trade["qty"] == 50


def test_price_preserved():
    trade = build_engine("NIFTY").run()
    assert trade["price"] == 250.0


def test_trade_status_created():
    trade = build_engine("NIFTY").run()
    assert trade["status"] == "CREATED"


def test_trade_has_unique_id():
    trade1 = build_engine("NIFTY").run()
    trade2 = build_engine("NIFTY").run()
    assert trade1["id"] != trade2["id"]


def test_multiple_engine_runs():
    for symbol in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
        trade = build_engine(symbol).run()
        assert trade["symbol"] == symbol


def test_engine_returns_trade():
    assert isinstance(build_engine("NIFTY").run(), dict)


def test_multiple_symbols_complete():
    symbols = [
        "NIFTY",
        "BANKNIFTY",
        "FINNIFTY",
        "MIDCPNIFTY",
        "SENSEX",
        "BANKEX",
    ]

    for symbol in symbols:
        trade = build_engine(symbol).run()
        assert trade["symbol"] == symbol
