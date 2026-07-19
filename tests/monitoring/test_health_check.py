from monitoring.health_check import HealthCheck


def test_initially_healthy():
    hc = HealthCheck()
    assert hc.overall_status() is True


def test_register_check():
    hc = HealthCheck()
    hc.register("Database")
    assert hc.count() == 1


def test_register_failed_check():
    hc = HealthCheck()
    hc.register("API", False)
    assert hc.status("API") is False


def test_update_check():
    hc = HealthCheck()
    hc.register("API", False)
    hc.update("API", True)
    assert hc.status("API") is True


def test_overall_status_false():
    hc = HealthCheck()
    hc.register("API", True)
    hc.register("Database", False)
    assert hc.overall_status() is False


def test_failed_checks():
    hc = HealthCheck()
    hc.register("API", False)
    hc.register("DB", True)
    assert hc.failed_checks() == ["API"]


def test_clear():
    hc = HealthCheck()
    hc.register("API")
    hc.clear()
    assert hc.count() == 0


def test_len():
    hc = HealthCheck()
    hc.register("API")
    hc.register("DB")
    assert len(hc) == 2


def test_unknown_status():
    hc = HealthCheck()
    assert hc.status("Missing") is None


def test_repr():
    hc = HealthCheck()
    hc.register("API")
    assert "HealthCheck" in repr(hc)