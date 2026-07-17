from datetime import datetime

from backtesting.historical_data_feed import HistoricalDataFeed


def test_empty_feed():
    feed = HistoricalDataFeed([])

    assert not feed.has_next()


def test_next_candle():
    candles = [
        {
            "timestamp": datetime(2025, 1, 1, 9, 15),
            "open": 100,
            "high": 105,
            "low": 99,
            "close": 104,
            "volume": 1000,
        }
    ]

    feed = HistoricalDataFeed(candles)

    assert feed.has_next()

    candle = feed.next()

    assert candle["close"] == 104

    assert not feed.has_next()

def test_reset_feed():
    candles = [
        {
            "timestamp": datetime(2025, 1, 1, 9, 15),
            "open": 100,
            "high": 105,
            "low": 99,
            "close": 104,
            "volume": 1000,
        }
    ]

    feed = HistoricalDataFeed(candles)

    first = feed.next()

    assert first["close"] == 104
    assert not feed.has_next()

    feed.reset()

    assert feed.has_next()

    second = feed.next()

    assert second["close"] == 104

def test_peek_does_not_advance():
    candles = [
        {
            "timestamp": datetime(2025, 1, 1, 9, 15),
            "open": 100,
            "high": 105,
            "low": 99,
            "close": 104,
            "volume": 1000,
        }
    ]

    feed = HistoricalDataFeed(candles)

    candle = feed.peek()

    assert candle["close"] == 104

    assert feed.has_next()

    candle2 = feed.next()

    assert candle2["close"] == 104

    assert not feed.has_next()

def test_current_index():
    candles = [
        {
            "timestamp": datetime(2025, 1, 1, 9, 15),
            "open": 100,
            "high": 105,
            "low": 99,
            "close": 104,
            "volume": 1000,
        },
        {
            "timestamp": datetime(2025, 1, 1, 9, 20),
            "open": 104,
            "high": 106,
            "low": 103,
            "close": 105,
            "volume": 1200,
        },
    ]

    feed = HistoricalDataFeed(candles)

    assert feed.current_index() == 0

    feed.next()
    assert feed.current_index() == 1

    feed.next()
    assert feed.current_index() == 2

def test_iterates_over_all_candles():
    candles = [
        {
            "timestamp": datetime(2025, 1, 1, 9, 15),
            "close": 100,
        },
        {
            "timestamp": datetime(2025, 1, 1, 9, 20),
            "close": 101,
        },
        {
            "timestamp": datetime(2025, 1, 1, 9, 25),
            "close": 102,
        },
    ]

    feed = HistoricalDataFeed(candles)

    closes = [candle["close"] for candle in feed]

    assert closes == [100, 101, 102]