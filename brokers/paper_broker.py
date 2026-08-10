import uuid
from dataclasses import replace
from decimal import Decimal

from brokers.base_broker import BaseBroker
from brokers.models import Funds, OrderStatus


class PaperBroker(BaseBroker):
    """In-memory paper broker implementation."""

    def __init__(self) -> None:
        self._is_connected = False
        self._orders = {}
        self._positions = []
        self._holdings = []

        self._funds = Funds(
            available_cash=Decimal(1000000),
            utilised_margin=Decimal(0),
            available_margin=Decimal(1000000),
        )

    def connect(self) -> None:
        self._is_connected = True

    def disconnect(self) -> None:
        self._is_connected = False

    def is_connected(self) -> bool:
        return self._is_connected

    def get_health(self) -> dict:
        return {
            "broker": "PaperBroker",
            "connected": self.is_connected(),
            "latency_ms": 0,
            "heartbeat": "UNKNOWN",
        }

    def place_order(self, order):
        broker_order = replace(
            order,
            broker_order_id=uuid.uuid4().hex,
        )

        self._orders[broker_order.broker_order_id] = broker_order

        return broker_order

    def modify_order(self, order_id: str, **kwargs):
        order = self._orders[order_id]

        updated_order = replace(order, **kwargs)

        self._orders[order_id] = updated_order

        return updated_order

    def cancel_order(self, order_id: str) -> bool:
        order = self._orders[order_id]

        self._orders[order_id] = replace(
            order,
            status=OrderStatus.CANCELLED,
        )

        return True

    def get_order(self, order_id: str):
        return self._orders[order_id]

    def get_orders(self):
        return list(self._orders.values())

    def get_positions(self):
        return list(self._positions)

    def get_holdings(self):
        return list(self._holdings)

    def get_funds(self):
        return self._funds
