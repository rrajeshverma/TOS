from datetime import datetime
from unittest.mock import Mock

from shared.enums import Signal
from strategies.ema_vwap_rsi_strategy import EMAVWAPRSIStrategy


def market(close, hour=11, minute=0):
    obj = Mock()
    obj.close = close
    obj.timestamp = datetime(2026, 8, 18, hour, minute)
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

    result = strategy.analyze(
        market(110),
        indicators(),
    )

    assert result.signal == Signal.BUY_CE
    assert result.has_signal
    assert len(result.reasons) > 0


def test_sell_signal():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(80),
        indicators(rsi=40),
    )

    assert result.signal == Signal.BUY_PE
    assert result.has_signal
    assert len(result.reasons) > 0


def test_hold_when_rsi_between_45_and_55():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(110),
        indicators(rsi=50),
    )

    assert result.signal == Signal.NONE
    assert not result.has_signal


def test_hold_when_price_below_vwap():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(94),
        indicators(rsi=60),
    )

    assert result.signal == Signal.NONE
    assert not result.has_signal


def test_hold_when_price_below_ema_high():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(99),
        indicators(),
    )

    assert result.signal == Signal.NONE
    assert not result.has_signal


def test_hold_when_price_above_ema_low_for_sell():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(91),
        indicators(rsi=40),
    )

    assert result.signal == Signal.NONE
    assert not result.has_signal


def test_hold_when_price_above_vwap_for_sell():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(96),
        indicators(rsi=40),
    )

    assert result.signal == Signal.NONE
    assert not result.has_signal


def test_strategy_returns_reasons():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(110),
        indicators(),
    )

    assert isinstance(result.reasons, tuple)
    assert len(result.reasons) > 0


def test_hold_before_entry_window():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(110, hour=10, minute=14),
        indicators(),
    )

    assert result.signal == Signal.NONE
    assert result.reasons == ("Outside trading window",)


def test_entry_allowed_at_window_start():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(110, hour=10, minute=15),
        indicators(),
    )

    assert result.signal == Signal.BUY_CE


def test_entry_allowed_at_window_end():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(110, hour=14, minute=30),
        indicators(),
    )

    assert result.signal == Signal.BUY_CE


def test_hold_after_entry_window():
    strategy = EMAVWAPRSIStrategy()

    result = strategy.analyze(
        market(110, hour=14, minute=31),
        indicators(),
    )

    assert result.signal == Signal.NONE
    assert result.reasons == ("Outside trading window",)
