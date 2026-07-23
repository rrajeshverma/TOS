from domain.indicator_set import IndicatorSet


def make_indicator_set(rsi=50.0):
    return IndicatorSet(
        ema_high=100.0,
        ema_low=95.0,
        vwap=98.0,
        rsi=rsi,
        volume_average=1000.0,
    )


def test_is_bullish_above_threshold():
    indicators = make_indicator_set(rsi=56.0)

    assert indicators.is_bullish is True
    assert indicators.is_bearish is False


def test_is_bearish_below_threshold():
    indicators = make_indicator_set(rsi=44.0)

    assert indicators.is_bearish is True
    assert indicators.is_bullish is False


def test_is_neutral_at_45():
    indicators = make_indicator_set(rsi=45.0)

    assert indicators.is_bullish is False
    assert indicators.is_bearish is False


def test_is_neutral_at_55():
    indicators = make_indicator_set(rsi=55.0)

    assert indicators.is_bullish is False
    assert indicators.is_bearish is False


def test_is_neutral_between_thresholds():
    indicators = make_indicator_set(rsi=50.0)

    assert indicators.is_bullish is False
    assert indicators.is_bearish is False


def test_indicator_values_are_preserved():
    indicators = IndicatorSet(
        ema_high=123.45,
        ema_low=120.12,
        vwap=121.55,
        rsi=61.3,
        volume_average=9876.5,
    )

    assert indicators.ema_high == 123.45
    assert indicators.ema_low == 120.12
    assert indicators.vwap == 121.55
    assert indicators.rsi == 61.3
    assert indicators.volume_average == 9876.5
