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
