from strategies.filters.trade_limit_filter import (
    TradeLimitFilter,
)


def test_zero_trades_allowed():
    assert TradeLimitFilter().allow(0)


def test_one_trade_allowed():
    assert TradeLimitFilter().allow(1)


def test_two_trades_not_allowed():
    assert not TradeLimitFilter().allow(2)


def test_three_trades_not_allowed():
    assert not TradeLimitFilter().allow(3)


def test_custom_limit():
    filt = TradeLimitFilter(
        max_trades=3,
    )

    assert filt.allow(2)
    assert not filt.allow(3)
