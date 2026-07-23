from unittest.mock import Mock

from live.broker_session import BrokerSession


def test_session_initial_state():
    session = BrokerSession(Mock())

    assert session.is_active() is False


def test_start_session():
    broker = Mock()

    session = BrokerSession(broker)

    session.start()

    broker.connect.assert_called_once()
    assert session.is_active() is True


def test_stop_session():
    broker = Mock()

    session = BrokerSession(broker)

    session.start()
    session.stop()

    broker.disconnect.assert_called_once()
    assert session.is_active() is False


def test_restart_session():
    broker = Mock()

    session = BrokerSession(broker)

    session.restart()

    broker.disconnect.assert_called_once()
    broker.connect.assert_called_once()
    assert session.is_active() is True
