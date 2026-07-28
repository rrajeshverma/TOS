"""
Integration Test:

Full Paper Trading Day Flow

Validates complete simulated trading lifecycle.
"""

from datetime import datetime


class MarketRuntime:

    def __init__(self):
        self.ticks = []

    def receive_tick(
        self,
        tick,
    ):
        self.ticks.append(
            tick
        )


class DummyStrategy:

    def evaluate(
        self,
        tick,
    ):

        if tick["price"] > 25000:

            return {
                "symbol": tick["symbol"],
                "side": "BUY",
                "quantity": 65,
            }

        return None


class DummyRiskEngine:

    def approve(
        self,
        decision,
    ):

        return (
            decision["quantity"] <= 65
        )


class PaperExecutor:

    def __init__(self):

        self.orders = []

    def execute(
        self,
        decision,
    ):

        order = {
            "order_id": "PAPER001",
            "symbol": decision["symbol"],
            "side": decision["side"],
            "quantity": decision["quantity"],
        }

        self.orders.append(
            order
        )

        return order


class PositionBook:

    def __init__(self):

        self.positions = {}

    def update(
        self,
        trade,
    ):

        self.positions[
            trade["symbol"]
        ] = trade["quantity"]


class TradeJournal:

    def __init__(self):

        self.entries = []

    def record(
        self,
        trade,
    ):

        self.entries.append(
            trade
        )


def create_trading_day():

    return {
        "market": MarketRuntime(),
        "strategy": DummyStrategy(),
        "risk": DummyRiskEngine(),
        "executor": PaperExecutor(),
        "positions": PositionBook(),
        "journal": TradeJournal(),
    }


def create_tick():

    return {
        "symbol": "NIFTY",
        "price": 25050,
        "volume": 1000,
        "timestamp": datetime.now(),
    }


def test_market_receives_tick():

    system = create_trading_day()

    system["market"].receive_tick(
        create_tick()
    )

    assert len(
        system["market"].ticks
    ) == 1


def test_strategy_generates_signal():

    system = create_trading_day()

    decision = system["strategy"].evaluate(
        create_tick()
    )

    assert decision is not None

    assert (
        decision["side"]
        == "BUY"
    )


def test_risk_engine_approves_trade():

    system = create_trading_day()

    decision = system["strategy"].evaluate(
        create_tick()
    )

    assert (
        system["risk"].approve(
            decision
        )
        is True
    )


def test_paper_order_execution():

    system = create_trading_day()

    decision = system["strategy"].evaluate(
        create_tick()
    )

    trade = system["executor"].execute(
        decision
    )

    assert (
        trade["order_id"]
        == "PAPER001"
    )


def test_position_updates_after_trade():

    system = create_trading_day()

    trade = system["executor"].execute(
        system["strategy"].evaluate(
            create_tick()
        )
    )

    system["positions"].update(
        trade
    )

    assert (
        system["positions"].positions["NIFTY"]
        == 65
    )


def test_trade_journal_records_execution():

    system = create_trading_day()

    trade = system["executor"].execute(
        system["strategy"].evaluate(
            create_tick()
        )
    )

    system["journal"].record(
        trade
    )

    assert len(
        system["journal"].entries
    ) == 1


def test_complete_paper_trading_day_flow():

    system = create_trading_day()

    tick = create_tick()

    system["market"].receive_tick(
        tick
    )

    decision = system["strategy"].evaluate(
        tick
    )

    assert system["risk"].approve(
        decision
    )

    trade = system["executor"].execute(
        decision
    )

    system["positions"].update(
        trade
    )

    system["journal"].record(
        trade
    )

    assert len(
        system["journal"].entries
    ) == 1

    assert (
        system["positions"].positions["NIFTY"]
        == 65
    )
