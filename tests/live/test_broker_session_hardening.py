from live.broker_session import BrokerSession


def test_session_initial_state():

    session = BrokerSession()

    assert session.is_connected() is False


def test_session_connect():

    session = BrokerSession()

    session.connect()

    assert session.is_connected()


def test_session_disconnect():

    session = BrokerSession()

    session.connect()
    session.disconnect()

    assert session.is_connected() is False


def test_session_reconnect():

    session = BrokerSession()

    session.reconnect()

    assert session.is_connected()


def test_session_reset():

    session = BrokerSession()

    session.connect()
    session.reset()

    assert session.is_connected() is False