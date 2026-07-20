from monitoring.diagnostics import Diagnostics


def test_initial_report():
    d = Diagnostics()

    report = d.report()

    assert report["healthy"] is True
    assert report["running"] is False


def test_running_status():
    d = Diagnostics()

    d.runtime.start()

    assert d.report()["running"] is True


def test_failed_health():
    d = Diagnostics()

    d.health.register("Broker", False)

    report = d.report()

    assert report["healthy"] is False
    assert "Broker" in report["failed_checks"]


def test_system_info_exists():
    d = Diagnostics()

    report = d.report()

    assert "system" in report
    assert "python_version" in report["system"]


def test_uptime_exists():
    d = Diagnostics()

    d.runtime.start()

    assert d.report()["uptime"] >= 0


def test_repr():
    d = Diagnostics()

    assert "Diagnostics" in repr(d)


def test_report_contains_keys():
    report = Diagnostics().report()

    expected = {
        "healthy",
        "running",
        "uptime",
        "system",
        "failed_checks",
    }

    assert expected.issubset(report.keys())


def test_multiple_failed_checks():
    d = Diagnostics()

    d.health.register("API", False)
    d.health.register("Database", False)

    report = d.report()

    assert len(report["failed_checks"]) == 2


def test_health_recovery():
    d = Diagnostics()

    d.health.register("API", False)
    d.health.update("API", True)

    assert d.report()["healthy"] is True


def test_empty_failed_checks():
    assert Diagnostics().report()["failed_checks"] == []
