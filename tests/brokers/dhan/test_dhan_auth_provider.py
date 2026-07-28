"""
Tests:
Dhan Authentication Provider with TOTP flow
"""

import pytest

from brokers.dhan.auth_provider import DhanAuthProvider
from brokers.dhan.session import DhanSession


class DummyAuthClient:
    """
    Fake Dhan authentication API.
    """

    def authenticate(
        self,
        client_id,
        pin,
        totp_code,
    ):
        return {
            "access_token": "ACCESS_TOKEN_123"
        }


def test_auth_provider_initialization():

    provider = DhanAuthProvider(
        DummyAuthClient()
    )

    assert provider is not None


def test_authenticate_with_totp_returns_token():

    provider = DhanAuthProvider(
        DummyAuthClient()
    )

    token = provider.authenticate(
        client_id="CLIENT001",
        pin="1234",
        totp_code="123456",
    )

    assert token == "ACCESS_TOKEN_123"


def test_auth_provider_updates_session():

    session = DhanSession()

    provider = DhanAuthProvider(
        DummyAuthClient(),
        session,
    )

    provider.authenticate(
        client_id="CLIENT001",
        pin="1234",
        totp_code="123456",
    )

    assert session.is_authenticated is True
    assert session.access_token == "ACCESS_TOKEN_123"


def test_authentication_failure():

    class FailedAuthClient:

        def authenticate(
            self,
            client_id,
            pin,
            totp_code,
        ):
            raise RuntimeError(
                "Authentication failed"
            )

    provider = DhanAuthProvider(
        FailedAuthClient()
    )

    with pytest.raises(RuntimeError):
        provider.authenticate(
            client_id="CLIENT001",
            pin="1234",
            totp_code="000000",
        )
