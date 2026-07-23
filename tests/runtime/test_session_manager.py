from runtime.session_manager import SessionManager


def test_session_manager_closed():
    manager = SessionManager()
    assert manager.status == "closed"


def test_open_session():
    manager = SessionManager()
    manager.open()
    assert manager.status == "open"


def test_close_session():
    manager = SessionManager()
    manager.open()
    manager.close()
    assert manager.status == "closed"


def test_restart_session():
    manager = SessionManager()
    manager.restart()
    assert manager.status == "open"


def test_session_status():
    manager = SessionManager()
    manager.open()
    assert manager.is_open() is True
