"""
Abstract broker interface.

Every broker implementation (Dhan, Paper, Zerodha, etc.)
must inherit from BaseBroker.
"""

from abc import ABC, abstractmethod


class BaseBroker(ABC):
    """Abstract base class for all broker implementations."""

    @abstractmethod
    def connect(self) -> None:
        """Connect to broker."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from broker."""
        raise NotImplementedError

    @abstractmethod
    def is_connected(self) -> bool:
        """Return broker connection status."""
        raise NotImplementedError

    @abstractmethod
    def get_health(self) -> dict:
        """
        Return broker health information.
        """
        raise NotImplementedError

    @abstractmethod
    def place_order(self, order):
        """Place an order."""
        raise NotImplementedError

    from typing import Any

    @abstractmethod
    def modify_order(
        self,
        order_id: str,
        quantity: int,
        price: float | None = None,
        trigger_price: float | None = None,
    ) -> Any:
        """Modify an existing order."""
        raise NotImplementedError

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order."""
        raise NotImplementedError

    @abstractmethod
    def get_order(self, order_id: str):
        """Fetch a single order."""
        raise NotImplementedError

    @abstractmethod
    def get_orders(self):
        """Fetch all orders."""
        raise NotImplementedError

    @abstractmethod
    def get_positions(self):
        """Fetch current positions."""
        raise NotImplementedError

    @abstractmethod
    def get_holdings(self):
        """Fetch holdings."""
        raise NotImplementedError

    @abstractmethod
    def get_funds(self):
        """Fetch available funds."""
        raise NotImplementedError
