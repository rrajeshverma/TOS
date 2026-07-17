from datetime import datetime

from backtesting.backtest_engine import BacktestEngine
from backtesting.historical_data_feed import HistoricalDataFeed


def test_create_backtest_engine():
    feed = HistoricalDataFeed([])

    engine = BacktestEngine(feed)

    assert engine.feed is feed

def test_run_empty_feed():
    feed = HistoricalDataFeed([])

    engine = BacktestEngine(feed)

    result = engine.run()

    assert result == []

def test_run_consumes_all_candles():
    candles = [
        {
            "timestamp": datetime(2025, 1, 1, 9, 15),
            "close": 100,
        },
        {
            "timestamp": datetime(2025, 1, 1, 9, 20),
            "close": 101,
        },
    ]

    feed = HistoricalDataFeed(candles)

    engine = BacktestEngine(feed)

    engine.run()

    assert feed.current_index() == 2

class DummyStrategy:
    def __init__(self):
        self.count = 0

    def on_candle(self, candle):
        self.count += 1


def test_strategy_receives_every_candle():
    candles = [
        {"timestamp": datetime(2025, 1, 1, 9, 15), "close": 100},
        {"timestamp": datetime(2025, 1, 1, 9, 20), "close": 101},
        {"timestamp": datetime(2025, 1, 1, 9, 25), "close": 102},
    ]

    feed = HistoricalDataFeed(candles)
    strategy = DummyStrategy()

    engine = BacktestEngine(feed, strategy)

    engine.run()

    assert strategy.count == 3

class SignalStrategy:
    def on_candle(self, candle):
        return {
            "action": "BUY",
            "price": candle["close"],
        }


def test_run_collects_strategy_signals():
    candles = [
        {
            "timestamp": datetime(2025, 1, 1, 9, 15),
            "close": 100,
        },
        {
            "timestamp": datetime(2025, 1, 1, 9, 20),
            "close": 101,
        },
    ]

    feed = HistoricalDataFeed(candles)

    engine = BacktestEngine(feed, SignalStrategy())

    results = engine.run()

    assert len(results) == 2
    assert results[0]["action"] == "BUY"
    assert results[0]["price"] == 100
    assert results[1]["price"] == 101