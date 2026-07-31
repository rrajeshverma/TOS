"""
Tests for Dhan broker order safety.
"""

from unittest.mock import Mock

import pytest

from brokers.dhan_broker import DhanBroker
from brokers.models import (
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    ProductType,
)


class DummyInstrument:
    security_id = "1333"
    exchange_segment = "NSE_EQ"


class DummyInstrumentMapper:
    def get(self, symbol):
        if symbol == "NIFTY":
            return DummyInstrument()

        return None


class DummyClient:
    def __init__(self):
        self.connected = True

    def place_order(self, **kwargs):
        return {
            "data": {
                "orderId": "ORD123",
            }
        }


def create_order():
    return Order(
        symbol="NIFTY",
        side=OrderSide.BUY,
        quantity=65,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )


def test_place_order_success_flow():
    broker = DhanBroker(
        DummyClient(),
        DummyInstrumentMapper(),
    )

    order = create_order()

    result = broker.place_order(order)

    assert result.broker_order_id == "ORD123"
    assert result.status == OrderStatus.PENDING


def test_place_order_missing_instrument():
    broker = DhanBroker(
        DummyClient(),
        DummyInstrumentMapper(),
    )

    order = Order(
        symbol="INVALID",
        side=OrderSide.BUY,
        quantity=65,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )

    with pytest.raises(ValueError):
        broker.place_order(order)


def test_place_order_requires_connection():
    client = DummyClient()
    client.connected = False

    broker = DhanBroker(
        client,
        DummyInstrumentMapper(),
    )

    with pytest.raises(RuntimeError):
        broker.place_order(create_order())


def test_is_connected_without_client_state():
    client = Mock(spec=[])

    broker = DhanBroker(
        client,
        DummyInstrumentMapper(),
    )

    assert broker.is_connected() is False
