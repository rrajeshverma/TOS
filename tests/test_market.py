from datetime import datetime

from domain.market import Market


def make_market(**kwargs):
    data = {
        "symbol": "NIFTY",
        "exchange": "NSE",
        "timeframe": "5m",
        "timestamp": datetime.now(),
        "open": 100.0,
        "high": 110.0,
        "low": 90.0,
        "close": 105.0,
        "volume": 1000,
    }

    data.update(kwargs)
    return Market(**data)


def test_is_bullish():
    assert make_market(close=105, open=100).is_bullish is True


def test_is_bearish():
    assert make_market(close=95, open=100).is_bearish is True


def test_is_not_bullish_when_equal():
    assert make_market(close=100, open=100).is_bullish is False


def test_is_not_bearish_when_equal():
    assert make_market(close=100, open=100).is_bearish is False


def test_body_size():
    assert make_market(open=100, close=105).body_size == 5


def test_body_size_bearish():
    assert make_market(open=105, close=100).body_size == 5


def test_candle_range():
    assert make_market(high=110, low=90).candle_range == 20
