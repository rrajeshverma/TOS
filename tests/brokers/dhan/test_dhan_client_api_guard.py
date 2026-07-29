"""
Tests:
DhanClient API access guards
"""

import pytest

from brokers.dhan.client import DhanClient
from brokers.dhan.session import DhanSession


class DummySDK:
    def __init__(self):
        self.called = False

    def get_positions(self):
        self.called = True
        return []


def create_client():
    session = DhanSession()

    client = DhanClient(
        "CLIENT001",
        "",
        session,
    )

    client._sdk = DummySDK()

    return client


def test_api_call_requires_authentication():
    client = create_client()

    with pytest.raises(RuntimeError):
        client.get_positions()


def test_authenticated_api_call_reaches_sdk():
    client = create_client()

    client.authenticate("TOKEN001")

    result = client.get_positions()

    assert result == []


def test_logout_blocks_future_api_calls():
    client = create_client()

    client.authenticate("TOKEN001")

    client.logout()

    with pytest.raises(RuntimeError):
        client.get_positions()


def test_sdk_missing_raises_error():
    session = DhanSession()

    client = DhanClient(
        "CLIENT001",
        "TOKEN001",
        session,
    )

    client.authenticate("TOKEN001")

    with pytest.raises(RuntimeError):
        client.get_positions()
