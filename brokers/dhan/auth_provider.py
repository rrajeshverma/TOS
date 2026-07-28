"""
Dhan Authentication Provider

Handles Dhan user authentication flow
and updates session state.
"""

from __future__ import annotations

from brokers.dhan.session import DhanSession


class DhanAuthProvider:
    """
    Provides authentication abstraction for Dhan.

    Flow:
        Client ID
            |
        PIN + TOTP
            |
        Access Token
            |
        DhanSession
    """

    def __init__(
        self,
        auth_client,
        session: DhanSession | None = None,
    ) -> None:

        self.auth_client = auth_client

        self.session = (
            session
            if session is not None
            else DhanSession()
        )

    def authenticate(
        self,
        *,
        client_id: str,
        pin: str,
        totp_code: str,
    ) -> str:
        """
        Authenticate user and create session.
        """

        response = self.auth_client.authenticate(
            client_id,
            pin,
            totp_code,
        )

        access_token = response["access_token"]

        self.session.authenticate(
            access_token
        )

        return access_token
