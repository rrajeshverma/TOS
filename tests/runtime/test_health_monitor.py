from datetime import timedelta
from unittest.mock import patch

from runtime.health_monitor import HealthMonitor


def test_health_monitor_initial_state():
    monitor = HealthMonitor()
    assert monitor.healthy is True


def test_health_monitor_healthy():
    monitor = HealthMonitor()
    monitor.mark_healthy()
    assert monitor.healthy is True


def test_health_monitor_unhealthy():
    monitor = HealthMonitor()
    monitor.mark_unhealthy()
    assert monitor.healthy is False


def test_health_monitor_reset():
    monitor = HealthMonitor()
    monitor.mark_unhealthy()
    monitor.reset()
    assert monitor.healthy is True


def test_health_monitor_timestamp():
    monitor = HealthMonitor()
    monitor.update()
    assert monitor.last_check is not None


def test_reset_clears_timestamp():
    monitor = HealthMonitor()

    monitor.update()

    assert monitor.last_check is not None

    monitor.reset()

    assert monitor.last_check is None


def test_mark_healthy_after_unhealthy():
    monitor = HealthMonitor()

    monitor.mark_unhealthy()

    monitor.mark_healthy()

    assert monitor.healthy is True


def test_update_does_not_change_health():
    monitor = HealthMonitor()

    monitor.mark_unhealthy()

    monitor.update()

    assert monitor.healthy is False


def test_multiple_updates_refresh_timestamp():
    monitor = HealthMonitor()

    monitor.update()

    first = monitor.last_check

    with patch(
        "runtime.health_monitor.datetime",
    ) as mock_datetime:
        mock_datetime.now.return_value = first + timedelta(seconds=1)

        monitor.update()

    assert monitor.last_check > first
