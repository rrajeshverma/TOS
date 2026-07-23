from analytics.trade_journal import TradeJournal


def test_empty_journal():
    journal = TradeJournal([])

    assert journal.rows == []


def test_trade_journal():
    trades = [
        {
            "symbol": "NIFTY",
            "entry": 25000,
            "exit": 25100,
            "qty": 50,
            "pnl": 100,
        },
        {
            "symbol": "BANKNIFTY",
            "entry": 56000,
            "exit": 55900,
            "qty": 25,
            "pnl": -50,
        },
    ]

    journal = TradeJournal(trades)

    assert len(journal.rows) == 2
    assert journal.rows[0]["symbol"] == "NIFTY"
    assert journal.rows[1]["pnl"] == -50
