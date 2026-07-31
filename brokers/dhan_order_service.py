"""
Dhan Order Service.
"""

from __future__ import annotations

from brokers.clients.dhan_client import DhanClient


class DhanOrderService:
    """Adapter between ExecutionEngine and DhanClient."""

    def __init__(self, client: DhanClient) -> None:
        self.client = client

    def get_positions(self):
        return self.client.get_positions()

    def get_orders(self):
        return self.client.get_orders()

    def get_holdings(self):
        return self.client.get_holdings()

    def get_fund_limits(self):
        return self.client.get_fund_limits()

    def get_order(self, order_id):
        return self.client.get_order(order_id)

    def place_order(self, **kwargs):
        return self.client.place_order(**kwargs)

    def modify_order(self, order_id, **kwargs):
        return self.client.modify_order(
            order_id,
            **kwargs,
        )

    def cancel_order(self, order_id):
        return self.client.cancel_order(order_id)
