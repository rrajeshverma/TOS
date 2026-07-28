"""
TOS Session Recovery Service

Restores broker session state after runtime restart.
"""

from __future__ import annotations


class SessionRecoveryService:
    """
    Handles broker session recovery.
    """

    def __init__(self) -> None:

        self._session: dict | None = None


    def recover(
        self,
        session_state: dict,
    ) -> dict:
        """
        Recover session state.
        """

        if not session_state:
            raise ValueError(
                "Session state required"
            )

        if "access_token" not in session_state:
            raise ValueError(
                "Access token required"
            )

        self._session = {
            "access_token": session_state[
                "access_token"
            ],
            "authenticated": True,
        }

        return self._session


    def get_session(
        self,
    ) -> dict | None:
        """
        Return recovered session.
        """

        return self._session


    def is_authenticated(
        self,
    ) -> bool:
        """
        Check recovered authentication.
        """

        return (
            self._session is not None
            and self._session.get(
                "authenticated",
                False,
            )
        )


    def clear(
        self,
    ) -> None:
        """
        Clear recovered session.
        """

        self._session = None
