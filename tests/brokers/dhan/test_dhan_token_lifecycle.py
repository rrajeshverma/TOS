"""
Tests:
Dhan token lifecycle management
"""

from datetime import datetime, timedelta

from brokers.dhan.session import DhanSession


def test_session_token_has_creation_time():
    session = DhanSession()

    session.authenticate("TOKEN123")

    assert session.access_token == "TOKEN123"
    assert session.created_at is not None


def test_session_token_expiry():
    session = DhanSession()

    session.authenticate("TOKEN123")

    session.expires_at = datetime.now() - timedelta(minutes=1)

    assert session.is_expired is True


def test_active_token_is_not_expired():
    session = DhanSession()

    session.authenticate("TOKEN123")

    session.expires_at = datetime.now() + timedelta(hours=1)

    assert session.is_expired is False


def test_revoke_token():
    session = DhanSession()

    session.authenticate("TOKEN123")

    session.revoke()

    assert session.access_token is None
    assert session.is_authenticated is False


def test_refresh_token():
    session = DhanSession()

    session.authenticate("OLD_TOKEN")

    session.refresh("NEW_TOKEN")

    assert session.access_token == "NEW_TOKEN"
    assert session.is_authenticated is True
