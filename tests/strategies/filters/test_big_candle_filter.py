from decimal import Decimal

from strategies.filters.big_candle_filter import (
    BigCandleFilter,
)


def test_normal_candle_allowed():
    f = BigCandleFilter()

    assert f.allowed(
        Decimal(40),
        Decimal(30),
    )


def test_exactly_two_times_allowed():
    f = BigCandleFilter()

    assert f.allowed(
        Decimal(60),
        Decimal(30),
    )


def test_big_candle_rejected():
    f = BigCandleFilter()

    assert not f.allowed(
        Decimal(70),
        Decimal(30),
    )


def test_zero_average_allowed():
    f = BigCandleFilter()

    assert f.allowed(
        Decimal(100),
        Decimal(0),
    )
