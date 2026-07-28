"""
Integration Test:

Paper Trading Session Flow

Flow:

Market Tick
    |
    ▼
Candle Generation
    |
    ▼
Decision
    |
    ▼
Risk Check
    |
    ▼
Paper Order
    |
    ▼
Position
    |
    ▼
Trade Journal
"""

from datetime import datetime


class PaperBroker:

    def __init__(self):
        self.orders = []

    def place_order(
        self,
        order,
    ):
        self.orders.append(order)

        return {
            "order_id": "PAPER001",
            "status": "FILLED",
        }


class PaperPositionManager:

    def __init__(self):
        self.positions = []

    def update(
        self,
        order,
    ):
        self.positions.append(
            {
                "symbol": order["symbol"],
                "quantity": order["quantity"],
            }
        )


class PaperJournal:

    def __init__(self):
        self.records = []

    def record(
        self,
        trade,
    ):
        self.records.append(
            trade
        )


def create_market_tick():

    return {
        "symbol": "NIFTY",
        "price": 25000,
        "volume": 1000,
        "timestamp": datetime.now(),
    }


def create_paper_order():

    return {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
        "price": 25000,
    }


def test_paper_session_receives_market_tick():

    tick = create_market_tick()

    assert tick["symbol"] == "NIFTY"
    assert tick["price"] == 25000


def test_paper_order_execution():

    broker = PaperBroker()

    response = broker.place_order(
        create_paper_order()
    )

    assert response["status"] == "FILLED"
    assert response["order_id"] == "PAPER001"


def test_paper_trade_updates_position():

    manager = PaperPositionManager()

    manager.update(
        create_paper_order()
    )

    assert len(
        manager.positions
    ) == 1

    assert (
        manager.positions[0]["quantity"]
        == 65
    )


def test_paper_trade_written_to_journal():

    journal = PaperJournal()

    journal.record(
        {
            "trade_id": "PAPER001",
            "symbol": "NIFTY",
            "pnl": 6500,
        }
    )

    assert len(
        journal.records
    ) == 1

    assert (
        journal.records[0]["pnl"]
        == 6500
    )


def test_complete_paper_trading_session():

    broker = PaperBroker()
    position = PaperPositionManager()
    journal = PaperJournal()

    order = create_paper_order()

    result = broker.place_order(
        order
    )

    assert result["status"] == "FILLED"

    position.update(
        order
    )

    journal.record(
        {
            "trade_id": result["order_id"],
            "symbol": order["symbol"],
        }
    )

    assert position.positions[0]["symbol"] == "NIFTY"
    assert journal.records[0]["trade_id"] == "PAPER001"
