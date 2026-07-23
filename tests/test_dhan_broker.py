from decimal import Decimal
from unittest.mock import Mock

import pytest

from brokers.dhan_broker import DhanBroker
from brokers.models import (
    Funds,
    Holding,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    Position,
    ProductType,
)

from domain.instrument import Instrument


class DummyClient:
    def get_fund_limits(self):
        return {
            "status": "success",
            "data": {
                "availabelBalance": 100000.00,
                "utilizedAmount": 5000.00,
            },
        }


class DummyPositionClient:
    def get_positions(self):
        return {
            "status": "success",
            "data": [
                {
                    "securityId": "13",
                    "tradingSymbol": "NIFTY",
                    "netQty": 65,
                    "costPrice": 245.50,
                    "lastTradedPrice": 250.25,
                }
            ],
        }


def test_get_funds():
    broker = DhanBroker(DummyClient(), Mock())

    funds = broker.get_funds()

    assert isinstance(funds, Funds)
    assert funds.available_cash == Decimal("100000.00")
    assert funds.utilised_margin == Decimal("5000.00")
    assert funds.available_margin == Decimal("95000.00")


def test_get_positions():
    broker = DhanBroker(DummyPositionClient(), Mock())

    positions = broker.get_positions()

    assert len(positions) == 1

    assert isinstance(positions[0], Position)

    assert positions[0].symbol == "NIFTY"
    assert positions[0].quantity == 65
    assert positions[0].average_price == Decimal("245.50")
    assert positions[0].last_price == Decimal("250.25")
    assert positions[0].pnl == Decimal("0")


class DummyHoldingClient:
    def get_holdings(self):
        return {
            "status": "success",
            "data": [
                {
                    "tradingSymbol": "RELIANCE",
                    "totalQty": 10,
                    "avgCostPrice": 2500.50,
                }
            ],
        }


def test_get_holdings():
    broker = DhanBroker(DummyHoldingClient(), Mock())

    holdings = broker.get_holdings()

    assert len(holdings) == 1

    assert isinstance(holdings[0], Holding)

    assert holdings[0].symbol == "RELIANCE"
    assert holdings[0].quantity == 10
    assert holdings[0].average_price == Decimal("2500.50")


class DummyOrderClient:
    def get_order_list(self):
        return {
            "status": "success",
            "data": [
                {
                    "orderId": "ORD123",
                    "tradingSymbol": "NIFTY",
                    "transactionType": "BUY",
                    "quantity": 65,
                    "orderType": "MARKET",
                    "productType": "INTRADAY",
                    "orderStatus": "PENDING",
                }
            ],
        }


def test_get_orders():
    broker = DhanBroker(DummyOrderClient(), Mock())

    orders = broker.get_orders()

    assert len(orders) == 1

    order = orders[0]

    assert isinstance(order, Order)
    assert order.symbol == "NIFTY"
    assert order.quantity == 65
    assert order.side == OrderSide.BUY
    assert order.order_type == OrderType.MARKET
    assert order.product == ProductType.INTRADAY
    assert order.status == OrderStatus.PENDING
    assert order.broker_order_id == "ORD123"


class DummyPlaceOrderClient:
    def place_order(self, **kwargs):
        return {
            "status": "success",
            "data": {
                "orderId": "ORD999",
            },
        }


class DummyInstrumentMapper:
    def get(self, symbol):
        return Instrument(
            symbol="NIFTY",
            security_id="13",
            exchange_segment="NSE_FNO",
            lot_size=65,
            tick_size=Decimal("0.05"),
        )


def test_place_order():
    broker = DhanBroker(
        DummyPlaceOrderClient(),
        DummyInstrumentMapper(),
    )

    order = Order(
        symbol="NIFTY",
        side=OrderSide.BUY,
        quantity=65,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )

    placed = broker.place_order(order)

    assert placed.broker_order_id == "ORD999"
    assert placed.status == OrderStatus.PENDING


def test_cancel_order():
    client = Mock()
    client.cancel_order.return_value = {
        "status": "success",
    }

    broker = DhanBroker(client, Mock())

    response = broker.cancel_order("ORD123")

    client.cancel_order.assert_called_once_with("ORD123")
    assert response["status"] == "success"


def test_connect_not_implemented():
    broker = DhanBroker(Mock(), Mock())

    with pytest.raises(NotImplementedError):
        broker.connect()


def test_disconnect_not_implemented():
    broker = DhanBroker(Mock(), Mock())

    with pytest.raises(NotImplementedError):
        broker.disconnect()


def test_is_connected_not_implemented():
    broker = DhanBroker(Mock(), Mock())

    with pytest.raises(NotImplementedError):
        broker.is_connected()


def test_modify_order():
    client = Mock()

    client.modify_order.return_value = {
        "status": "success",
    }

    broker = DhanBroker(client, Mock())

    response = broker.modify_order(
        "ORD123",
        quantity=25,
        price=25010,
    )

    client.modify_order.assert_called_once_with(
        "ORD123",
        {
            "quantity": 25,
            "price": 25010,
        },
    )

    assert response["status"] == "success"


def test_get_order():
    client = Mock()

    client.get_order.return_value = {
        "orderId": "ORD123",
        "tradingSymbol": "NIFTY",
        "transactionType": "BUY",
        "quantity": 65,
        "orderType": "MARKET",
        "productType": "INTRADAY",
        "orderStatus": "PENDING",
    }

    broker = DhanBroker(client, Mock())

    order = broker.get_order("ORD123")

    client.get_order.assert_called_once_with("ORD123")

    assert isinstance(order, Order)
    assert order.broker_order_id == "ORD123"
    assert order.symbol == "NIFTY"
    assert order.side == OrderSide.BUY
    assert order.quantity == 65
    assert order.order_type == OrderType.MARKET
    assert order.product == ProductType.INTRADAY
    assert order.status == OrderStatus.PENDING
