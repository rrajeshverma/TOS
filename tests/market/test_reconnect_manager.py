from market.reconnect_manager import ReconnectManager


def test_reconnect_manager_initial_state():
    manager = ReconnectManager()

    assert manager.is_connected() is False
    assert manager.retry_count() == 0


def test_reconnect_manager_connect():
    manager = ReconnectManager()

    manager.connect()

    assert manager.is_connected() is True


def test_reconnect_manager_disconnect():
    manager = ReconnectManager()

    manager.connect()
    manager.disconnect()

    assert manager.is_connected() is False


def test_reconnect_manager_retry_count():
    manager = ReconnectManager()

    manager.reconnect()
    manager.reconnect()

    assert manager.retry_count() == 2


def test_reconnect_manager_reset():
    manager = ReconnectManager()

    manager.reconnect()

    manager.reset()

    assert manager.is_connected() is False
    assert manager.retry_count() == 0
