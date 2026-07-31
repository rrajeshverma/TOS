"""
Integration tests:
DhanClient + DhanSession lifecycle
"""

import pytest

from brokers.dhan.client import DhanClient
from brokers.dhan.session import DhanSession


class DummyTransport:
    """
    Fake API transport.
    """

    def __init__(self):
        self.last_token = None

    def set_access_token(
        self,
        token,
    ):
        self.last_token = token


def test_client_initial_state():
    session = DhanSession()
    transport = DummyTransport()

    client = DhanClient(
        transport,
        session,
    )

    assert client.session.is_authenticated is False


def test_client_authentication():
    session = DhanSession()
    transport = DummyTransport()

    client = DhanClient(
        transport,
        session,
    )

    client.authenticate("TOKEN123")

    assert session.is_authenticated is True
    assert session.access_token == "TOKEN123"


def test_client_rejects_api_without_authentication():
    session = DhanSession()
    transport = DummyTransport()

    client = DhanClient(
        transport,
        session,
    )

    with pytest.raises(RuntimeError):
        client.get_profile()


def test_client_logout_clears_session():
    session = DhanSession()
    transport = DummyTransport()

    client = DhanClient(
        transport,
        session,
    )

    client.authenticate("TOKEN123")

    client.logout()

    assert session.is_authenticated is False
    assert session.access_token is None
