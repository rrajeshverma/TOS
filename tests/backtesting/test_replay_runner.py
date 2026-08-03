from unittest.mock import MagicMock

from backtesting.replay_runner import ReplayRunner
from backtesting.historical_data_feed import HistoricalDataFeed
from domain.market import Market

from datetime import datetime


def test_replay_runner_feeds_runtime():
    runtime = MagicMock()

    markets = [
        Market(
            symbol="BTCUSDT",
            exchange="BINANCE",
            timeframe="30m",
            timestamp=datetime(2026, 1, 1, 0, 0),
            open=100,
            high=105,
            low=99,
            close=104,
            volume=1000,
        ),
        Market(
            symbol="BTCUSDT",
            exchange="BINANCE",
            timeframe="30m",
            timestamp=datetime(2026, 1, 1, 0, 30),
            open=104,
            high=106,
            low=103,
            close=105,
            volume=1200,
        ),
    ]

    feed = HistoricalDataFeed(markets)

    runner = ReplayRunner(
        runtime=runtime,
        feed=feed,
    )

    runner.run()

    assert runtime.on_market_tick.call_count == 2
