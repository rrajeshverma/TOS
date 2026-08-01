from monitoring.broker_connection_monitor import (
    BrokerConnectionMonitor,
)
from monitoring.broker_reconnect_manager import (
    BrokerReconnectManager,
)
from monitoring.reconnect_policy import ReconnectPolicy


def create_manager(max_attempts: int = 3):
    return BrokerReconnectManager(
        BrokerConnectionMonitor(),
        ReconnectPolicy(max_attempts=max_attempts),
    )


def test_disconnected_monitor_can_reconnect():
    manager = create_manager()

    assert manager.should_reconnect()


def test_connected_monitor_does_not_reconnect():
    monitor = BrokerConnectionMonitor()
    monitor.connect()

    manager = BrokerReconnectManager(
        monitor,
        ReconnectPolicy(),
    )

    assert manager.should_reconnect() is False


def test_retry_limit_prevents_reconnect():
    manager = create_manager(max_attempts=1)

    manager.record_failure()

    assert manager.should_reconnect() is False


def test_reset_restores_reconnect():
    manager = create_manager(max_attempts=1)

    manager.record_failure()
    manager.reset()

    assert manager.should_reconnect()


def test_multiple_failures_respect_limit():
    manager = create_manager(max_attempts=2)

    manager.record_failure()
    manager.record_failure()

    assert manager.should_reconnect() is False


def test_connected_after_reset_still_not_reconnect():
    monitor = BrokerConnectionMonitor()
    monitor.connect()

    manager = BrokerReconnectManager(
        monitor,
        ReconnectPolicy(),
    )

    manager.reset()

    assert manager.should_reconnect() is False


def test_record_failure_is_repeatable():
    manager = create_manager()

    manager.record_failure()
    manager.record_failure()

    assert manager.should_reconnect()


def test_reset_is_repeatable():
    manager = create_manager()

    manager.reset()
    manager.reset()

    assert manager.should_reconnect()


def test_manager_uses_supplied_monitor():
    monitor = BrokerConnectionMonitor()

    manager = BrokerReconnectManager(
        monitor,
        ReconnectPolicy(),
    )

    assert manager.should_reconnect()


def test_manager_uses_supplied_policy():
    policy = ReconnectPolicy(max_attempts=5)

    manager = BrokerReconnectManager(
        BrokerConnectionMonitor(),
        policy,
    )

    assert manager.should_reconnect()
