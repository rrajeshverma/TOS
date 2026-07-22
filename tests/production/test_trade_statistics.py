import pytest

from reporting.reports.trade_statistics import TradeStatistics


class DummyTrade:
    def __init__(self, pnl=0.0):
        self.pnl = pnl


def test_total_trades():
    stats = TradeStatistics()

    trades = [
        DummyTrade(),
        DummyTrade(),
        DummyTrade(),
    ]

    assert stats.total_trades(trades) == 3


def test_total_trades_empty():
    stats = TradeStatistics()

    assert stats.total_trades([]) == 0


def test_winning_trades():
    stats = TradeStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(-50),
        DummyTrade(75),
        DummyTrade(0),
    ]

    assert stats.winning_trades(trades) == 2


def test_losing_trades():
    stats = TradeStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(-50),
        DummyTrade(-25),
        DummyTrade(0),
    ]

    assert stats.losing_trades(trades) == 2


def test_gross_profit():
    stats = TradeStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(50),
        DummyTrade(-20),
    ]

    assert stats.gross_profit(trades) == 150


def test_gross_loss():
    stats = TradeStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(-40),
        DummyTrade(-20),
    ]

    assert stats.gross_loss(trades) == 60


def test_largest_win():
    stats = TradeStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(80),
        DummyTrade(150),
    ]

    assert stats.largest_win(trades) == 150


def test_largest_loss():
    stats = TradeStatistics()

    trades = [
        DummyTrade(-25),
        DummyTrade(-75),
        DummyTrade(-40),
    ]

    assert stats.largest_loss(trades) == 75


def test_average_win():
    stats = TradeStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(50),
    ]

    assert stats.average_win(trades) == 75


def test_average_loss():
    stats = TradeStatistics()

    trades = [
        DummyTrade(-20),
        DummyTrade(-40),
    ]

    assert stats.average_loss(trades) == 30


def test_win_rate():
    stats = TradeStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(-50),
        DummyTrade(60),
        DummyTrade(-20),
    ]

    assert stats.win_rate(trades) == 50.0


def test_profit_factor():
    stats = TradeStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(-25),
        DummyTrade(50),
        DummyTrade(-25),
    ]

    assert stats.profit_factor(trades) == pytest.approx(3.0)


def test_expectancy():
    stats = TradeStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(50),
        DummyTrade(-20),
        DummyTrade(-40),
    ]

    assert stats.expectancy(trades) == pytest.approx(22.5)
