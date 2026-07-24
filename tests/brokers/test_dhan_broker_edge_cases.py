from decimal import Decimal
from unittest.mock import Mock

import pytest

from brokers.dhan_broker import DhanBroker
from brokers.models import (
    Order,
    OrderSide,
    OrderType,
    ProductType,
)


# ---------------------------------------------------------
# Empty Response Handling
# ---------------------------------------------------------


class EmptyFundsClient:
    def get_fund_limits(self):
        return {
            "status": "success",
            "data": {
                "availabelBalance": 0,
                "utilizedAmount": 0,
            },
        }


def test_get_funds_zero_balance():
    broker = DhanBroker(
        EmptyFundsClient(),
        Mock(),
    )

    funds = broker.get_funds()

    assert funds.available_cash == Decimal("0")
    assert funds.utilised_margin == Decimal("0")


class EmptyOrdersClient:
    def get_order_list(self):
        return {
            "status": "success",
            "data": [],
        }


def test_get_orders_empty():
    broker = DhanBroker(
        EmptyOrdersClient(),
        Mock(),
    )

    assert broker.get_orders() == []


class EmptyPositionsClient:
    def get_positions(self):
        return {
            "status": "success",
            "data": [],
        }


def test_get_positions_empty():
    broker = DhanBroker(
        EmptyPositionsClient(),
        Mock(),
    )

    assert broker.get_positions() == []


class EmptyHoldingsClient:
    def get_holdings(self):
        return {
            "status": "success",
            "data": [],
        }


def test_get_holdings_empty():
    broker = DhanBroker(
        EmptyHoldingsClient(),
        Mock(),
    )

    assert broker.get_holdings() == []


# ---------------------------------------------------------
# Decimal Conversion
# ---------------------------------------------------------


def test_funds_decimal_conversion():
    client = Mock()

    client.get_fund_limits.return_value = {
        "data": {
            "availabelBalance": "100000.55",
            "utilizedAmount": "5000.25",
        }
    }

    broker = DhanBroker(
        client,
        Mock(),
    )

    funds = broker.get_funds()

    assert isinstance(
        funds.available_cash,
        Decimal,
    )


# ---------------------------------------------------------
# Order Side Tests
# ---------------------------------------------------------


class DummyInstrument:
    security_id = "13"
    exchange_segment = "NSE_FNO"


class DummyMapper:
    def get(self, symbol):
        return DummyInstrument()


class DummySellClient:

    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True

    def place_order(self, **kwargs):
        assert kwargs["transaction_type"] == "SELL"

        return {
            "data": {
                "orderId": "SELL001",
            }
        }


def test_place_sell_order():
    broker = DhanBroker(
        DummySellClient(),
        DummyMapper(),
    )

    broker.connect()
    
    order = Order(
        symbol="NIFTY",
        side=OrderSide.SELL,
        quantity=65,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )

    result = broker.place_order(order)

    assert result.broker_order_id == "SELL001"


# ---------------------------------------------------------
# Invalid Instrument
# ---------------------------------------------------------


class InvalidMapper:
    def get(self, symbol):
        return None


def test_place_order_invalid_instrument():
    broker = DhanBroker(
        Mock(),
        InvalidMapper(),
    )

    order = Order(
        symbol="UNKNOWN",
        side=OrderSide.BUY,
        quantity=1,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )

    with pytest.raises(ValueError):
        broker.place_order(order)
