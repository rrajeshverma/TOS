import pytest

from reporting.reports.streak_statistics import (
    StreakStatistics,
)


class DummyTrade:
    def __init__(self, pnl=0):
        self.pnl = pnl


def test_empty_trades():
    stats = StreakStatistics()

    assert stats.max_consecutive_wins([]) == 0
    assert stats.max_consecutive_losses([]) == 0


def test_single_win():
    stats = StreakStatistics()

    trades = [DummyTrade(100)]

    assert stats.max_consecutive_wins(trades) == 1
    assert stats.max_consecutive_losses(trades) == 0


def test_single_loss():
    stats = StreakStatistics()

    trades = [DummyTrade(-100)]

    assert stats.max_consecutive_wins(trades) == 0
    assert stats.max_consecutive_losses(trades) == 1


def test_all_wins():
    stats = StreakStatistics()

    trades = [
        DummyTrade(10),
        DummyTrade(20),
        DummyTrade(30),
    ]

    assert stats.max_consecutive_wins(trades) == 3
    assert stats.max_consecutive_losses(trades) == 0


def test_all_losses():
    stats = StreakStatistics()

    trades = [
        DummyTrade(-10),
        DummyTrade(-20),
        DummyTrade(-30),
    ]

    assert stats.max_consecutive_wins(trades) == 0
    assert stats.max_consecutive_losses(trades) == 3


def test_alternating_trades():
    stats = StreakStatistics()

    trades = [
        DummyTrade(10),
        DummyTrade(-10),
        DummyTrade(20),
        DummyTrade(-20),
        DummyTrade(30),
    ]

    assert stats.max_consecutive_wins(trades) == 1
    assert stats.max_consecutive_losses(trades) == 1


def test_longest_win_streak():
    stats = StreakStatistics()

    trades = [
        DummyTrade(10),
        DummyTrade(20),
        DummyTrade(-5),
        DummyTrade(30),
        DummyTrade(40),
        DummyTrade(50),
        DummyTrade(-10),
    ]

    assert stats.max_consecutive_wins(trades) == 3


def test_longest_loss_streak():
    stats = StreakStatistics()

    trades = [
        DummyTrade(-10),
        DummyTrade(-20),
        DummyTrade(5),
        DummyTrade(-30),
        DummyTrade(-40),
        DummyTrade(-50),
    ]

    assert stats.max_consecutive_losses(trades) == 3


def test_zero_pnl_breaks_streak():
    stats = StreakStatistics()

    trades = [
        DummyTrade(10),
        DummyTrade(20),
        DummyTrade(0),
        DummyTrade(30),
    ]

    assert stats.max_consecutive_wins(trades) == 2


def test_realistic_sequence():
    stats = StreakStatistics()

    trades = [
        DummyTrade(100),
        DummyTrade(50),
        DummyTrade(-20),
        DummyTrade(-10),
        DummyTrade(-30),
        DummyTrade(40),
        DummyTrade(60),
        DummyTrade(80),
        DummyTrade(-15),
    ]

    assert stats.max_consecutive_wins(trades) == 3
    assert stats.max_consecutive_losses(trades) == 3