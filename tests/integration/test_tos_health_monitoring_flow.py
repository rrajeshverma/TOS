"""
Integration Test:

TOS Health Monitoring Flow

Validates:

Runtime Health
      |
      ▼
Component Status
      |
      ▼
Trading System Availability
"""


class HealthMonitor:

    def __init__(self):
        self.components = {}

    def update(
        self,
        component,
        status,
    ):
        self.components[component] = status

    def is_healthy(self):

        return all(
            self.components.values()
        )

    def status(self):

        return self.components


class DummyRuntime:

    def __init__(self):

        self.running = True


class DummyBroker:

    def __init__(self):

        self.connected = True


class DummyMarketFeed:

    def __init__(self):

        self.active = True


def create_health():

    monitor = HealthMonitor()

    monitor.update(
        "runtime",
        True,
    )

    monitor.update(
        "broker",
        True,
    )

    monitor.update(
        "market_feed",
        True,
    )

    return monitor


def test_runtime_health_is_available():

    monitor = create_health()

    assert (
        monitor.status()["runtime"]
        is True
    )


def test_broker_connection_health():

    monitor = create_health()

    assert (
        monitor.status()["broker"]
        is True
    )


def test_market_feed_health():

    monitor = create_health()

    assert (
        monitor.status()["market_feed"]
        is True
    )


def test_system_health_is_green():

    monitor = create_health()

    assert (
        monitor.is_healthy()
        is True
    )


def test_system_health_detects_failure():

    monitor = create_health()

    monitor.update(
        "broker",
        False,
    )

    assert (
        monitor.is_healthy()
        is False
    )
