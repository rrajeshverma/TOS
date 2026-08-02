"""
Production Validation

RC3 Validation 2

Trading Window Validation
"""

from datetime import time

from strategies.filters.time_filter import TimeFilter


time_filter = TimeFilter(
    time(10, 15),
    time(14, 30),
)


def test_0930_is_not_trading_time():
    assert time_filter.allow(time(9, 30)) is False


def test_1014_is_not_trading_time():
    assert time_filter.allow(time(10, 14)) is False


def test_1015_is_trading_time():
    assert time_filter.allow(time(10, 15)) is True


def test_1130_is_trading_time():
    assert time_filter.allow(time(11, 30)) is True


def test_1430_is_trading_time():
    assert time_filter.allow(time(14, 30)) is True


def test_1431_is_not_trading_time():
    assert time_filter.allow(time(14, 31)) is False


def test_1500_is_not_trading_time():
    assert time_filter.allow(time(15, 0)) is False
