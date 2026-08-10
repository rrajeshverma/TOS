"""
Production Validation

RC3 Validation 3

Daily Trade Limit

Trading Rule

Maximum 2 trades per day.
"""

from strategies.filters.trade_limit_filter import (
    TradeLimitFilter,
)

trade_limit = TradeLimitFilter(
    max_trades=2,
)


def test_zero_trades_allowed():
    assert trade_limit.allow(0) is True


def test_first_trade_allowed():
    assert trade_limit.allow(1) is True


def test_second_trade_blocked():
    assert trade_limit.allow(2) is False


def test_more_than_limit_blocked():
    assert trade_limit.allow(3) is False


def test_large_trade_count_blocked():
    assert trade_limit.allow(100) is False
