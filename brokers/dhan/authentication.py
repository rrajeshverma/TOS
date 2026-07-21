"""
Authentication service for the Dhan broker.
"""

from __future__ import annotations

from brokers.dhan.exceptions import AuthenticationError


class AuthenticationService:
    """Handles validation of Dhan authentication credentials."""

    def authenticate(
        self,
        client_id: str | None,
        access_token: str | None,
    ) -> bool:
        """
        Validate the supplied credentials.

        Returns:
            True if credentials are valid.

        Raises:
            AuthenticationError: If either credential is missing.
        """
        if not client_id:
            raise AuthenticationError("Client ID is required.")

        if not access_token:
            raise AuthenticationError("Access token is required.")

        return True