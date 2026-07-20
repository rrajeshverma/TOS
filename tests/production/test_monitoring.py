import time

from monitoring.health_check import HealthCheck
from monitoring.runtime_status import RuntimeStatus
from monitoring.diagnostics import Diagnostics


# ---------------------------------------------------------------------
# HealthCheck
# ---------------------------------------------------------------------

def test_health_check_empty_is_healthy():
    health = HealthCheck()
    assert health.overall_status() is True


def test_health_check_register():
    health = HealthCheck()
    health.register("database")
    assert health.status("database") is True


def test_health_check_register_false():
    health = HealthCheck()
    health.register("broker", False)
    assert health.status("broker") is False


def test_health_check_update():
    health = HealthCheck()
    health.register("broker")
    health.update("broker", False)
    assert health.status("broker") is False


def test_health_check_count():
    health = HealthCheck()
    health.register("a")
    health.register("b")
    assert health.count() == 2


def test_health_check_failed_checks():
    health = HealthCheck()
    health.register("broker", False)
    health.register("database")
    assert health.failed_checks() == ["broker"]


def test_health_check_clear():
    health = HealthCheck()
    health.register("database")
    health.clear()
    assert len(health) == 0


def test_health_check_repr():
    health = HealthCheck()
    assert "HealthCheck" in repr(health)


# ---------------------------------------------------------------------
# RuntimeStatus
# ---------------------------------------------------------------------

def test_runtime_initial_state():
    runtime = RuntimeStatus()
    assert runtime.is_running is False


def test_runtime_start():
    runtime = RuntimeStatus()
    runtime.start()

    assert runtime.is_running is True
    assert runtime.started_at is not None


def test_runtime_stop():
    runtime = RuntimeStatus()

    runtime.start()
    runtime.stop()

    assert runtime.is_running is False


def test_runtime_uptime_zero_before_start():
    runtime = RuntimeStatus()
    assert runtime.uptime_seconds() == 0


def test_runtime_uptime_after_start():
    runtime = RuntimeStatus()
    runtime.start()

    time.sleep(1)

    assert runtime.uptime_seconds() >= 1


def test_runtime_repr():
    runtime = RuntimeStatus()
    assert "RuntimeStatus" in repr(runtime)


# ---------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------

def test_diagnostics_default_report():
    diagnostics = Diagnostics()

    report = diagnostics.report()

    assert report["healthy"] is True
    assert report["running"] is False


def test_diagnostics_failed_check():
    diagnostics = Diagnostics()

    diagnostics.health.register("broker", False)

    report = diagnostics.report()

    assert report["healthy"] is False
    assert report["failed_checks"] == ["broker"]


def test_diagnostics_runtime_running():
    diagnostics = Diagnostics()

    diagnostics.runtime.start()

    report = diagnostics.report()

    assert report["running"] is True


def test_diagnostics_report_contains_system():
    diagnostics = Diagnostics()

    report = diagnostics.report()

    assert "system" in report


def test_diagnostics_report_keys():
    diagnostics = Diagnostics()

    report = diagnostics.report()

    assert set(report.keys()) == {
        "healthy",
        "running",
        "uptime",
        "system",
        "failed_checks",
    }


def test_diagnostics_repr():
    diagnostics = Diagnostics()
    assert "Diagnostics" in repr(diagnostics)