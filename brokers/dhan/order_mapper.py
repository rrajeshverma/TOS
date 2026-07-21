"""
Order mapper for Dhan Broker.

Converts TOS domain order data into a broker-compatible payload.
"""

from __future__ import annotations


class OrderMapper:
    """Maps domain orders to Dhan broker payloads."""

    def to_broker_order(
        self,
        *,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str,
        price: float | None = None,
    ) -> dict:
        """
        Convert a domain order into a broker payload.
        """
        payload = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "order_type": order_type,
        }

        if price is not None:
            payload["price"] = price

        return payload