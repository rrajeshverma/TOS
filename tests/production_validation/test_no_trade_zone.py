"""
Production Validation

RC3 Validation 2

RSI Neutral Zone

Trading Rule:

RSI > 55  -> Bullish
RSI < 45  -> Bearish
RSI 45-55 -> NO TRADE
"""

from decimal import Decimal

from tests.helpers.domain_factory import (
    make_indicator_set,
    make_market,
)

from engines.strategy_engine import StrategyEngine

from shared.enums import Signal


def test_rsi_44_allows_bearish_signal():
    market = make_market(
        close=Decimal("100"),
    )

    indicators = make_indicator_set(
        ema_high=Decimal("110"),
        ema_low=Decimal("105"),
        vwap=Decimal("108"),
        rsi=44,
    )

    decision = StrategyEngine().decide(
        market,
        indicators,
    )

    assert decision.signal == Signal.BUY_PE


def test_rsi_45_is_no_trade():
    market = make_market(
        close=Decimal("120"),
    )

    indicators = make_indicator_set(
        ema_high=Decimal("110"),
        ema_low=Decimal("100"),
        vwap=Decimal("105"),
        rsi=45,
    )

    decision = StrategyEngine().decide(
        market,
        indicators,
    )

    assert decision.signal == Signal.NONE


def test_rsi_50_is_no_trade():
    market = make_market(
        close=Decimal("120"),
    )

    indicators = make_indicator_set(
        ema_high=Decimal("110"),
        ema_low=Decimal("100"),
        vwap=Decimal("105"),
        rsi=50,
    )

    decision = StrategyEngine().decide(
        market,
        indicators,
    )

    assert decision.signal == Signal.NONE


def test_rsi_55_is_no_trade():
    market = make_market(
        close=Decimal("120"),
    )

    indicators = make_indicator_set(
        ema_high=Decimal("110"),
        ema_low=Decimal("100"),
        vwap=Decimal("105"),
        rsi=55,
    )

    decision = StrategyEngine().decide(
        market,
        indicators,
    )

    assert decision.signal == Signal.NONE


def test_rsi_56_allows_bullish_signal():
    market = make_market(
        close=Decimal("120"),
    )

    indicators = make_indicator_set(
        ema_high=Decimal("110"),
        ema_low=Decimal("100"),
        vwap=Decimal("105"),
        rsi=56,
    )

    decision = StrategyEngine().decide(
        market,
        indicators,
    )

    assert decision.signal == Signal.BUY_CE
