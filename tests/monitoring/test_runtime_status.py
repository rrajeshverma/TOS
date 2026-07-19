from datetime import datetime
from monitoring.runtime_status import RuntimeStatus


def test_initially_stopped():
    rs = RuntimeStatus()
    assert rs.is_running is False


def test_start():
    rs = RuntimeStatus()
    rs.start()
    assert rs.is_running is True


def test_stop():
    rs = RuntimeStatus()
    rs.start()
    rs.stop()
    assert rs.is_running is False


def test_started_time():
    rs = RuntimeStatus()
    rs.start()
    assert isinstance(rs.started_at, datetime)


def test_uptime_non_negative():
    rs = RuntimeStatus()
    rs.start()
    assert rs.uptime_seconds() >= 0


def test_uptime_when_stopped():
    rs = RuntimeStatus()
    assert rs.uptime_seconds() == 0


def test_restart():
    rs = RuntimeStatus()
    rs.start()
    first = rs.started_at

    rs.stop()
    rs.start()

    assert rs.started_at >= first


def test_repr():
    rs = RuntimeStatus()
    assert "RuntimeStatus" in repr(rs)


def test_multiple_stop_calls():
    rs = RuntimeStatus()
    rs.stop()
    rs.stop()
    assert rs.is_running is False


def test_multiple_start_calls():
    rs = RuntimeStatus()
    rs.start()
    rs.start()
    assert rs.is_running is True