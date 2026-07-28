"""
Tests:
Live Trade Journal Flow

Flow:

Closed Trade
      |
      ▼
Trade Journal
      |
      ▼
P&L Record
"""


from datetime import datetime


class DummyTradeJournal:

    def __init__(self):
        self.records = []

    def record(
        self,
        trade,
    ):
        self.records.append(
            trade
        )

    def all(self):
        return self.records


def create_trade():

    return {
        "trade_id": "TRADE001",
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
        "entry_price": 25000,
        "exit_price": 25100,
        "pnl": 6500,
        "timestamp": datetime.now(),
    }


def test_closed_trade_can_be_recorded():

    journal = DummyTradeJournal()

    trade = create_trade()

    journal.record(
        trade
    )

    assert len(
        journal.all()
    ) == 1


def test_journal_stores_symbol():

    journal = DummyTradeJournal()

    trade = create_trade()

    journal.record(
        trade
    )

    stored = journal.all()[0]

    assert stored["symbol"] == "NIFTY"


def test_journal_stores_pnl():

    journal = DummyTradeJournal()

    trade = create_trade()

    journal.record(
        trade
    )

    stored = journal.all()[0]

    assert stored["pnl"] == 6500


def test_multiple_trades_are_tracked():

    journal = DummyTradeJournal()

    journal.record(
        create_trade()
    )

    journal.record(
        create_trade()
    )

    assert len(
        journal.all()
    ) == 2


def test_trade_contains_execution_details():

    journal = DummyTradeJournal()

    trade = create_trade()

    journal.record(
        trade
    )

    stored = journal.all()[0]

    assert stored["trade_id"] == "TRADE001"
    assert stored["quantity"] == 65
