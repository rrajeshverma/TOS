"""
Dhan Broker Client

Provides the client interface for interacting with the Dhan broker.
Handles authentication lifecycle and SDK communication.
"""

from __future__ import annotations

from brokers.dhan.session import DhanSession


class DhanClient:
    """
    Dhan broker API client.
    """

    def __init__(
        self,
        client_id: str | object,
        access_token: str | DhanSession,
        session: DhanSession | None = None,
    ) -> None:

        self.client_id = client_id

        if isinstance(access_token, DhanSession):
            self.session = access_token
            self.access_token = None

        else:
            self.access_token = access_token

            self.session = (
                session
                if session is not None
                else DhanSession()
            )

            # Backward compatibility:
            # Existing code passing access_token
            # is considered authenticated.
            if access_token:
                self.session.authenticate(
                    access_token
                )

        self.connected = False
        self._sdk = None

    # =====================================================
    # Authentication
    # =====================================================

    def authenticate(
        self,
        access_token: str,
    ) -> None:
        """
        Authenticate Dhan session.
        """

        self.session.authenticate(
            access_token
        )

        self.access_token = access_token

    def logout(self) -> None:
        """
        Clear authentication session.
        """

        self.session.logout()

        self.access_token = None

    def _ensure_authenticated(self) -> None:
        """
        Validate active authentication.
        """

        if not self.session.is_authenticated:
            raise RuntimeError(
                "Dhan client is not authenticated."
            )

    # =====================================================
    # Connection
    # =====================================================

    def connect(self) -> None:
        """
        Mark client connected.
        """

        self.connected = True

    def disconnect(self) -> None:
        """
        Mark client disconnected.
        """

        self.connected = False

    # =====================================================
    # Profile
    # =====================================================

    def get_profile(self) -> dict:
        """
        Retrieve user profile.
        """

        self._ensure_authenticated()

        if self._sdk is None:
            return {}

        return self._sdk.get_profile()

    # =====================================================
    # Orders
    # =====================================================

    def place_order(
        self,
        order: dict,
    ) -> dict:
        """
        Place an order.
        """

        self._ensure_authenticated()

        if self._sdk is None:
            raise RuntimeError(
                "Dhan SDK is not configured."
            )

        return self._sdk.place_order(
            **order
        )

    def cancel_order(
        self,
        order_id: str,
    ) -> dict:
        """
        Cancel existing order.
        """

        self._ensure_authenticated()

        if self._sdk is None:
            raise RuntimeError(
                "Dhan SDK is not configured."
            )

        return self._sdk.cancel_order(
            order_id
        )

    def modify_order(
        self,
        order_id: str,
        updates: dict,
    ) -> dict:
        """
        Modify existing order.
        """

        self._ensure_authenticated()

        if self._sdk is None:
            raise RuntimeError(
                "Dhan SDK is not configured."
            )

        return self._sdk.modify_order(
            order_id,
            **updates,
        )

    def get_order(
        self,
        order_id: str,
    ) -> dict:
        """
        Retrieve broker order.
        """

        self._ensure_authenticated()

        if self._sdk is None:
            raise RuntimeError(
                "Dhan SDK is not configured."
            )

        return self._sdk.get_order(
            order_id
        )

    # =====================================================
    # Portfolio
    # =====================================================

    def get_positions(self) -> list[dict]:
        """
        Retrieve live positions.
        """

        self._ensure_authenticated()

        if self._sdk is None:
            raise RuntimeError(
                "Dhan SDK is not configured."
            )

        return self._sdk.get_positions()

    def get_holdings(self) -> list[dict]:
        """
        Retrieve holdings.
        """

        self._ensure_authenticated()

        if self._sdk is None:
            raise RuntimeError(
                "Dhan SDK is not configured."
            )

        return self._sdk.get_holdings()

    def get_funds(self) -> dict:
        """
        Retrieve account funds.
        """

        self._ensure_authenticated()

        if self._sdk is None:
            raise RuntimeError(
                "Dhan SDK is not configured."
            )

        return self._sdk.get_funds()