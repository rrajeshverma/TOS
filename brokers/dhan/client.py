"""
Dhan Broker Client

Provides the basic client interface for interacting with the Dhan broker.
"""

from __future__ import annotations


class DhanClient:
    """Basic Dhan broker client."""

    def __init__(self, client_id: str, access_token: str) -> None:
        self.client_id = client_id
        self.access_token = access_token
        self.connected = False
        self._sdk = None

    def connect(self) -> None:
        """Mark the client as connected."""
        self.connected = True

    def disconnect(self) -> None:
        """Mark the client as disconnected."""
        self.connected = False
    
    def place_order(
        self,
        order: dict,
    ) -> dict:
        """
        Place an order through the Dhan SDK.
        """
        if self._sdk is None:
            raise RuntimeError("Dhan SDK is not configured.")

        return self._sdk.place_order(**order)
    
    def cancel_order(
        self,
        order_id: str,
    ) -> dict:
        """
        Cancel an existing broker order.
        """
        if self._sdk is None:
            raise RuntimeError("Dhan SDK is not configured.")

        return self._sdk.cancel_order(order_id)
    
    def modify_order(
        self,
        order_id: str,
        updates: dict,
    ) -> dict:
        """
        Modify an existing broker order.
        """
        if self._sdk is None:
            raise RuntimeError("Dhan SDK is not configured.")

        return self._sdk.modify_order(
            order_id,
            **updates,
        )
    
    def get_order(
        self,
        order_id: str,
    ) -> dict:
        """
        Retrieve a broker order by its ID.
        """
        if self._sdk is None:
            raise RuntimeError("Dhan SDK is not configured.")

        return self._sdk.get_order(order_id)
    
    def get_positions(self) -> list[dict]:
        """
        Retrieve all live broker positions.
        """
        if self._sdk is None:
            raise RuntimeError("Dhan SDK is not configured.")

        return self._sdk.get_positions()
    
    def get_holdings(self) -> list[dict]:
        """
        Retrieve all holdings from the broker.
        """
        if self._sdk is None:
            raise RuntimeError("Dhan SDK is not configured.")

        return self._sdk.get_holdings()
    
    def get_funds(self) -> dict:
        """
        Retrieve account funds and margin information.
        """
        if self._sdk is None:
            raise RuntimeError("Dhan SDK is not configured.")

        return self._sdk.get_funds()