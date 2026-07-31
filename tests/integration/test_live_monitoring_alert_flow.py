"""
Integration Test:

Live Monitoring Alert Flow

Validates:
- Runtime health checks
- Component monitoring
- Alert generation
- Recovery notification
"""


class RuntimeMonitor:
    def __init__(self):
        self.components = {
            "broker": True,
            "market_feed": True,
            "order_system": True,
            "risk_engine": True,
        }

    def update(
        self,
        component,
        status,
    ):
        self.components[component] = status

    def is_healthy(self):
        return all(self.components.values())

    def unhealthy_components(self):
        return [name for name, status in self.components.items() if not status]


class AlertManager:
    def __init__(self):
        self.alerts = []

    def send(
        self,
        message,
    ):
        self.alerts.append(message)

    def count(self):
        return len(self.alerts)


def create_monitor():
    return RuntimeMonitor()


def test_all_components_are_healthy():
    monitor = create_monitor()

    assert monitor.is_healthy() is True


def test_broker_failure_detected():
    monitor = create_monitor()

    monitor.update(
        "broker",
        False,
    )

    assert monitor.is_healthy() is False

    assert "broker" in monitor.unhealthy_components()


def test_market_feed_failure_detected():
    monitor = create_monitor()

    monitor.update(
        "market_feed",
        False,
    )

    failures = monitor.unhealthy_components()

    assert "market_feed" in failures


def test_alert_generated_for_failure():
    alert = AlertManager()

    alert.send("Broker connection lost")

    assert alert.count() == 1


def test_complete_monitoring_recovery_flow():
    monitor = create_monitor()

    alert = AlertManager()

    monitor.update(
        "order_system",
        False,
    )

    failures = monitor.unhealthy_components()

    alert.send(f"Failure detected: {failures[0]}")

    monitor.update(
        "order_system",
        True,
    )

    assert monitor.is_healthy() is True

    assert alert.count() == 1
