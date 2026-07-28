from brokers.dhan.session import DhanSession


def test_session_initial_state():

    session = DhanSession()

    assert session.is_authenticated is False


def test_session_authentication():

    session = DhanSession()

    session.authenticate(
        "ACCESS_TOKEN"
    )

    assert session.is_authenticated is True
    assert session.access_token == "ACCESS_TOKEN"


def test_session_logout():

    session = DhanSession()

    session.authenticate(
        "ACCESS_TOKEN"
    )

    session.logout()

    assert session.is_authenticated is False
    assert session.access_token is None
