from runtime.heartbeat import Heartbeat


def test_heartbeat_updates_timestamp():
    hb = Heartbeat()
    hb.beat()
    assert hb.last_heartbeat is not None


def test_heartbeat_detects_timeout():
    hb = Heartbeat(timeout=5)
    assert hb.timeout == 5