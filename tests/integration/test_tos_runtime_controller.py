"""
Integration Test:

TOS Runtime Controller

Validates:

START
  |
  ▼
Runtime Components
  |
  ▼
Trading Session
  |
  ▼
STOP
"""

from monitoring.runtime_status import RuntimeStatus


class DummyConfig:
    def load(self):
        return {
            "mode": "PAPER",
            "symbol": "NIFTY",
        }


class DummyMarketFeed:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running


class DummyStrategy:
    def __init__(self):
        self.started = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False


class TosRuntimeController:
    def __init__(
        self,
        config,
        feed,
        strategy,
        status,
    ):
        self.config = config
        self.feed = feed
        self.strategy = strategy
        self.status = status

    def start(self):
        self.config.load()

        self.feed.start()

        self.strategy.start()

        self.status.start()

    def stop(self):
        self.feed.stop()

        self.strategy.stop()

        self.status.stop()


def create_runtime():
    return TosRuntimeController(
        DummyConfig(),
        DummyMarketFeed(),
        DummyStrategy(),
        RuntimeStatus(),
    )


def test_runtime_starts_successfully():
    runtime = create_runtime()

    runtime.start()

    assert runtime.status.is_running is True


def test_market_feed_starts_with_runtime():
    runtime = create_runtime()

    runtime.start()

    assert runtime.feed.is_running() is True


def test_strategy_starts_with_runtime():
    runtime = create_runtime()

    runtime.start()

    assert runtime.strategy.started is True


def test_runtime_shutdown():
    runtime = create_runtime()

    runtime.start()

    runtime.stop()

    assert runtime.status.is_running is False


def test_runtime_restart_cycle():
    runtime = create_runtime()

    runtime.start()

    runtime.stop()

    runtime.start()

    assert runtime.status.is_running is True
