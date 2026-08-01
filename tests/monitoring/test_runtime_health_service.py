from monitoring.broker_connection_monitor import (
    BrokerConnectionMonitor,
)
from monitoring.broker_reconnect_manager import (
    BrokerReconnectManager,
)
from monitoring.reconnect_policy import ReconnectPolicy
from monitoring.runtime_health_report import RuntimeHealthReport
from monitoring.runtime_health_service import (
    RuntimeHealthService,
)


def create_service():
    monitor = BrokerConnectionMonitor()

    manager = BrokerReconnectManager(
        monitor,
        ReconnectPolicy(),
    )

    return RuntimeHealthService(
        monitor,
        manager,
    )


def test_status_returns_runtime_health_report():
    assert isinstance(
        create_service().status(),
        RuntimeHealthReport,
    )


def test_status_contains_broker():
    assert create_service().status().broker == "DISCONNECTED"


def test_status_contains_reconnect():
    assert create_service().status().reconnect == "AVAILABLE"


def test_disconnected_broker_status():
    assert create_service().status().broker == "DISCONNECTED"


def test_connected_broker_status():
    monitor = BrokerConnectionMonitor()
    monitor.connect()

    manager = BrokerReconnectManager(
        monitor,
        ReconnectPolicy(),
    )

    service = RuntimeHealthService(
        monitor,
        manager,
    )

    assert service.status().broker == "CONNECTED"


def test_reconnect_available():
    assert create_service().status().reconnect == "AVAILABLE"


def test_reconnect_blocked_after_limit():
    monitor = BrokerConnectionMonitor()

    policy = ReconnectPolicy(max_attempts=1)

    manager = BrokerReconnectManager(
        monitor,
        policy,
    )

    manager.record_failure()

    service = RuntimeHealthService(
        monitor,
        manager,
    )

    assert service.status().reconnect == "BLOCKED"


def test_report_is_healthy_when_connected():
    monitor = BrokerConnectionMonitor()
    monitor.connect()

    manager = BrokerReconnectManager(
        monitor,
        ReconnectPolicy(),
    )

    service = RuntimeHealthService(
        monitor,
        manager,
    )

    assert service.status().healthy


def test_report_is_not_healthy_when_disconnected():
    assert create_service().status().healthy is False


def test_multiple_status_calls():
    service = create_service()

    service.status()
    service.status()

    assert service.status().broker == "DISCONNECTED"
