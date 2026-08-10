from decimal import Decimal

from brokers.models import (
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    ProductType,
)
from brokers.paper_broker import PaperBroker


def create_order():
    return Order(
        symbol="NIFTY",
        side=OrderSide.BUY,
        quantity=65,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
        price=Decimal(25000),
        status=OrderStatus.PENDING,
    )


def test_paper_broker_connect():
    broker = PaperBroker()

    broker.connect()

    assert broker.is_connected()


def test_paper_broker_disconnect():
    broker = PaperBroker()

    broker.connect()
    broker.disconnect()

    assert broker.is_connected() is False


def test_place_order_creates_broker_id():
    broker = PaperBroker()

    order = create_order()

    result = broker.place_order(order)

    assert result.broker_order_id is not None


def test_place_order_saved():
    broker = PaperBroker()

    result = broker.place_order(create_order())

    orders = broker.get_orders()

    assert len(orders) == 1
    assert orders[0].broker_order_id == result.broker_order_id


def test_get_order():
    broker = PaperBroker()

    result = broker.place_order(create_order())

    fetched = broker.get_order(result.broker_order_id)

    assert fetched.symbol == "NIFTY"


def test_multiple_orders():
    broker = PaperBroker()

    broker.place_order(create_order())
    broker.place_order(create_order())

    assert len(broker.get_orders()) == 2


def test_cancel_order():
    broker = PaperBroker()

    result = broker.place_order(create_order())

    broker.cancel_order(result.broker_order_id)

    cancelled = broker.get_order(result.broker_order_id)

    assert cancelled.status == OrderStatus.CANCELLED


def test_get_funds():
    broker = PaperBroker()

    funds = broker.get_funds()

    assert funds.available_cash == Decimal(1000000)


def test_empty_positions():
    broker = PaperBroker()

    assert broker.get_positions() == []


def test_empty_holdings():
    broker = PaperBroker()

    assert broker.get_holdings() == []
