from unittest.mock import Mock

from shared.enums import Signal
from strategies.ema_vwap_rsi_strategy import (
    EMAVWAPRSIStrategy,
)


def market(close):
    obj = Mock()
    obj.close = close
    return obj


def indicators(
    ema_high=100,
    ema_low=90,
    vwap=95,
    rsi=60,
):
    obj = Mock()
    obj.ema_high = ema_high
    obj.ema_low = ema_low
    obj.vwap = vwap
    obj.rsi = rsi
    return obj


def test_strategy_name():
    strategy = EMAVWAPRSIStrategy()

    assert strategy.name() == "EMA_VWAP_RSI"


def test_buy_signal():
    strategy = EMAVWAPRSIStrategy()

    signal = strategy.generate_signal(
        market(110),
        indicators(),
    )

    assert signal == Signal.BUY_CE


def test_sell_signal():
    strategy = EMAVWAPRSIStrategy()

    signal = strategy.generate_signal(
        market(80),
        indicators(
            rsi=40,
        ),
    )

    assert signal == Signal.BUY_PE


def test_hold_when_rsi_between_45_and_55():
    strategy = EMAVWAPRSIStrategy()

    signal = strategy.generate_signal(
        market(110),
        indicators(
            rsi=50,
        ),
    )

    assert signal == Signal.NONE


def test_hold_when_price_below_vwap():
    strategy = EMAVWAPRSIStrategy()

    signal = strategy.generate_signal(
        market(94),
        indicators(
            rsi=60,
        ),
    )

    assert signal == Signal.NONE


def test_hold_when_price_below_ema_high():
    strategy = EMAVWAPRSIStrategy()

    signal = strategy.generate_signal(
        market(99),
        indicators(),
    )

    assert signal == Signal.NONE


def test_hold_when_price_above_ema_low_for_sell():
    strategy = EMAVWAPRSIStrategy()

    signal = strategy.generate_signal(
        market(91),
        indicators(
            rsi=40,
        ),
    )

    assert signal == Signal.NONE


def test_hold_when_price_above_vwap_for_sell():
    strategy = EMAVWAPRSIStrategy()

    signal = strategy.generate_signal(
        market(96),
        indicators(
            rsi=40,
        ),
    )

    assert signal == Signal.NONE


def test_analyze_returns_market():
    strategy = EMAVWAPRSIStrategy()

    m = market(100)
    i = indicators()

    result = strategy.analyze(
        m,
        i,
    )

    assert result["market"] is m


def test_analyze_returns_indicators():
    strategy = EMAVWAPRSIStrategy()

    m = market(100)
    i = indicators()

    result = strategy.analyze(
        m,
        i,
    )

    assert result["indicators"] is i


def test_buy_uses_filters():
    strategy = EMAVWAPRSIStrategy()

    signal = strategy.generate_signal(
        market(110),
        indicators(),
    )

    assert signal == Signal.BUY_CE


def test_sell_uses_filters():
    strategy = EMAVWAPRSIStrategy()

    signal = strategy.generate_signal(
        market(80),
        indicators(
            rsi=40,
        ),
    )

    assert signal == Signal.BUY_PE
