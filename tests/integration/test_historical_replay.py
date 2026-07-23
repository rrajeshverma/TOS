from unittest.mock import Mock

from runtime.replay_runner import ReplayRunner
from market.replay_market_feed import ReplayMarketFeed


def test_historical_replay_processes_complete_session():
    ticks = [
        {"symbol": "NIFTY", "price": 25000},
        {"symbol": "NIFTY", "price": 25005},
        {"symbol": "NIFTY", "price": 25010},
        {"symbol": "NIFTY", "price": 25015},
        {"symbol": "NIFTY", "price": 25020},
    ]

    feed = ReplayMarketFeed(ticks)

    engine_runner = Mock()

    runner = ReplayRunner()
    runner.set_engine_runner(engine_runner)

    runner.run(feed)

    assert runner.completed is True
    assert runner.cycles == 5
    assert engine_runner.run_cycle.call_count == 5
