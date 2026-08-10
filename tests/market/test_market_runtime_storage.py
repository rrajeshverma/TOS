from datetime import datetime

from domain.market import Market
from market.market_runtime import MarketRuntime


def create_market(minute: int = 15) -> Market:
    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="1m",
        timestamp=datetime(2025, 1, 1, 9, minute),
        open=100.0,
        high=105.0,
        low=99.0,
        close=104.0,
        volume=1000,
    )


def test_runtime_has_feed():
    runtime = MarketRuntime()

    assert runtime.feed is None


def test_runtime_accepts_feed():
    runtime = MarketRuntime(feed="dummy")

    assert runtime.feed == "dummy"


def test_runtime_initially_not_running():
    runtime = MarketRuntime()

    assert runtime.is_running() is False


def test_runtime_start_sets_running():
    runtime = MarketRuntime()

    runtime.start()

    assert runtime.is_running() is True


def test_runtime_stop_sets_not_running():
    runtime = MarketRuntime()

    runtime.start()
    runtime.stop()

    assert runtime.is_running() is False


def test_runtime_start_is_idempotent():
    runtime = MarketRuntime()

    runtime.start()
    runtime.start()

    assert runtime.is_running() is True


def test_runtime_stop_is_idempotent():
    runtime = MarketRuntime()

    runtime.stop()
    runtime.stop()

    assert runtime.is_running() is False


def test_runtime_feed_not_modified_by_start():
    runtime = MarketRuntime(feed="feed")

    runtime.start()

    assert runtime.feed == "feed"


def test_runtime_feed_not_modified_by_stop():
    runtime = MarketRuntime(feed="feed")

    runtime.stop()

    assert runtime.feed == "feed"


def test_runtime_start_returns_none():
    runtime = MarketRuntime()

    assert runtime.start() is None


def test_runtime_stop_returns_none():
    runtime = MarketRuntime()

    assert runtime.stop() is None


def test_runtime_can_be_started_after_stop():
    runtime = MarketRuntime()

    runtime.start()
    runtime.stop()
    runtime.start()

    assert runtime.is_running()


def test_runtime_running_state_is_boolean():
    runtime = MarketRuntime()

    assert isinstance(runtime.is_running(), bool)


def test_runtime_has_feed_attribute():
    runtime = MarketRuntime()

    assert hasattr(runtime, "feed")


def test_runtime_has_running_attribute():
    runtime = MarketRuntime()

    assert hasattr(runtime, "running")
