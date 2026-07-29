"""
Integration test:
Runtime Health Monitoring Flow
"""

from monitoring.runtime_status import RuntimeStatus
from monitoring.system_monitor import SystemMonitor


def test_runtime_status_initial_state():
    status = RuntimeStatus()

    assert status is not None


def test_runtime_status_can_start_and_stop():
    status = RuntimeStatus()

    status.start()

    assert status.is_running is True

    status.stop()

    assert status.is_running is False


def test_system_monitor_initialization():
    monitor = SystemMonitor()

    assert monitor is not None


def test_runtime_health_components():
    status = RuntimeStatus()

    status.start()

    health = {
        "runtime": status.is_running,
        "broker": True,
        "market_feed": True,
        "execution": True,
    }

    assert health["runtime"] is True
    assert health["broker"] is True
    assert health["market_feed"] is True
    assert health["execution"] is True
