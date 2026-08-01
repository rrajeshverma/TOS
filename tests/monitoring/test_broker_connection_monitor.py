from monitoring.broker_connection_monitor import (
    BrokerConnectionMonitor,
)


def test_monitor_starts_disconnected():
    monitor = BrokerConnectionMonitor()

    assert monitor.is_connected() is False


def test_connect_sets_connected():
    monitor = BrokerConnectionMonitor()

    monitor.connect()

    assert monitor.is_connected() is True


def test_disconnect_sets_disconnected():
    monitor = BrokerConnectionMonitor()

    monitor.connect()
    monitor.disconnect()

    assert monitor.is_connected() is False


def test_multiple_connect_calls():
    monitor = BrokerConnectionMonitor()

    monitor.connect()
    monitor.connect()

    assert monitor.is_connected()


def test_multiple_disconnect_calls():
    monitor = BrokerConnectionMonitor()

    monitor.disconnect()
    monitor.disconnect()

    assert monitor.is_connected() is False


def test_connect_disconnect_connect():
    monitor = BrokerConnectionMonitor()

    monitor.connect()
    monitor.disconnect()
    monitor.connect()

    assert monitor.is_connected()


def test_disconnect_without_connect():
    monitor = BrokerConnectionMonitor()

    monitor.disconnect()

    assert monitor.is_connected() is False


def test_monitor_instances_are_independent():
    first = BrokerConnectionMonitor()
    second = BrokerConnectionMonitor()

    first.connect()

    assert first.is_connected()
    assert second.is_connected() is False


def test_connection_state_is_boolean():
    monitor = BrokerConnectionMonitor()

    assert isinstance(
        monitor.is_connected(),
        bool,
    )


def test_monitor_can_be_reused():
    monitor = BrokerConnectionMonitor()

    for _ in range(10):
        monitor.connect()
        monitor.disconnect()

    assert monitor.is_connected() is False
