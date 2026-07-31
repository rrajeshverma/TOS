"""
Integration Test:

Dhan Live Session Bootstrap Flow

Flow:

Auth Client
      |
      ▼
DhanAuthProvider
      |
      ▼
DhanSession
      |
      ▼
Authenticated State
"""

from brokers.dhan.auth_provider import DhanAuthProvider
from brokers.dhan.session import DhanSession


class DummyAuthClient:
    def authenticate(
        self,
        client_id,
        pin,
        totp_code,
    ):
        return {"access_token": "TEST_TOKEN"}


def create_provider():
    return DhanAuthProvider(DummyAuthClient())


def test_dhan_auth_provider_exists():
    provider = create_provider()

    assert provider is not None


def test_dhan_authentication_creates_session():
    provider = create_provider()

    token = provider.authenticate(
        client_id="CLIENT001",
        pin="1234",
        totp_code="000000",
    )

    assert token == "TEST_TOKEN"


def test_session_contains_access_token():
    session = DhanSession()

    session.authenticate("TEST_TOKEN")

    assert session.access_token == "TEST_TOKEN"


def test_authenticated_session_state():
    session = DhanSession()

    session.authenticate("TEST_TOKEN")

    assert session.is_authenticated is True
    assert session.is_expired is False


def test_live_session_bootstrap_flow():
    provider = create_provider()

    token = provider.authenticate(
        client_id="CLIENT001",
        pin="1234",
        totp_code="000000",
    )

    session = provider.session

    assert token == session.access_token
    assert session.created_at is not None
    assert session.expires_at is not None
