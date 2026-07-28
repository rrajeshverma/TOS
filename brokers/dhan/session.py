"""
Dhan authentication session management.

Handles:
- Access token lifecycle
- Expiry tracking
- Token refresh
- Token revocation
"""

from __future__ import annotations

from datetime import datetime, timedelta


class DhanSession:
    """
    Maintains Dhan broker authentication state.
    """

    DEFAULT_TOKEN_VALIDITY = timedelta(
        hours=24
    )

    def __init__(self) -> None:

        self.access_token: str | None = None

        self.created_at: datetime | None = None

        self.expires_at: datetime | None = None

    @property
    def is_authenticated(self) -> bool:
        """
        Returns True when a valid token exists.
        """

        return (
            self.access_token is not None
            and not self.is_expired
        )

    @property
    def is_expired(self) -> bool:
        """
        Check token expiry status.
        """

        if self.expires_at is None:
            return False

        return datetime.now() >= self.expires_at

    def authenticate(
        self,
        access_token: str,
    ) -> None:
        """
        Create authenticated session.
        """

        self.access_token = access_token

        self.created_at = datetime.now()

        self.expires_at = (
            self.created_at
            + self.DEFAULT_TOKEN_VALIDITY
        )

    def refresh(
        self,
        access_token: str,
    ) -> None:
        """
        Replace existing token.
        """

        self.authenticate(
            access_token
        )

    def revoke(self) -> None:
        """
        Remove authentication state.
        """

        self.access_token = None

        self.created_at = None

        self.expires_at = None

    def logout(self) -> None:
        """
        Logout current session.
        """

        self.revoke()