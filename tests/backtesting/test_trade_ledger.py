from unittest.mock import Mock

from backtesting.trade_ledger import TradeLedger


def test_add_completed_trade():
    ledger = TradeLedger()
    trade = Mock()

    ledger.add(trade)

    assert ledger.total_trades == 1
    assert ledger.trades == [trade]


def test_add_completed_trade_is_silent(capsys):
    ledger = TradeLedger()
    trade = Mock()

    ledger.add(trade)

    captured = capsys.readouterr()

    assert captured.out == ""
    assert captured.err == ""
