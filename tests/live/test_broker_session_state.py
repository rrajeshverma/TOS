from live.broker_session import BrokerSession


def test_connect_is_idempotent():

    session = BrokerSession()

    session.connect()
    session.connect()

    assert session.is_connected() is True



def test_disconnect_is_safe_multiple_times():

    session = BrokerSession()

    session.disconnect()
    session.disconnect()

    assert session.is_connected() is False



def test_reconnect_after_connection():

    session = BrokerSession()

    session.connect()
    session.reconnect()

    assert session.is_connected() is True



def test_session_status():

    session = BrokerSession()

    status = session.status()

    assert status["connected"] is False
