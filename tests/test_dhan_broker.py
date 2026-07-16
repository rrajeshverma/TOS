from decimal import Decimal

from brokers.dhan_broker import DhanBroker
from brokers.models import (
    Funds,
    Position,
    Holding,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    ProductType,
)

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
    broker = DhanBroker(DummyClient())

    funds = broker.get_funds()

    assert isinstance(funds, Funds)
    assert funds.available_cash == Decimal("100000.00")
    assert funds.utilised_margin == Decimal("5000.00")
    assert funds.available_margin == Decimal("95000.00")


def test_get_positions():
    broker = DhanBroker(DummyPositionClient())

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

    broker = DhanBroker(DummyHoldingClient())

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

    broker = DhanBroker(DummyOrderClient())

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


def test_place_order():

    broker = DhanBroker(DummyPlaceOrderClient())

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