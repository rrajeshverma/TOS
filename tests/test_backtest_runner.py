from datetime import datetime

from backtesting.backtest_runner import BacktestRunner
from backtesting.historical_data_feed import HistoricalDataFeed


class DummyStrategy:
    def on_candle(self, candle):
        return {
            "action": "BUY",
            "price": candle["close"],
        }


def test_runner_returns_signals():
    candles = [
        {
            "timestamp": datetime(2025, 1, 1, 9, 15),
            "close": 100,
        }
    ]

    feed = HistoricalDataFeed(candles)

    runner = BacktestRunner(feed, DummyStrategy())

    results = runner.run()

    assert len(results) == 1
    assert results[0]["action"] == "BUY"

def test_runner_creates_trade_simulator():
    runner = BacktestRunner(
        HistoricalDataFeed([]),
        DummyStrategy(),
    )

    assert runner.trade_simulator is not None