from brokers.paper_broker import PaperBroker
from brokers.models import (
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    ProductType,
)


def test_initial_state():
    broker = PaperBroker()
    assert broker.is_connected() is False


def test_connect():
    broker = PaperBroker()
    broker.connect()
    assert broker.is_connected() is True


def test_disconnect():
    broker = PaperBroker()
    broker.connect()
    broker.disconnect()
    assert broker.is_connected() is False


def test_place_order():
    broker = PaperBroker()

    order = Order(
        symbol="NIFTY",
        side=OrderSide.BUY,
        quantity=75,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )

    placed = broker.place_order(order)

    assert placed.broker_order_id is not None
    assert placed.status == OrderStatus.PENDING


def test_get_order():
    broker = PaperBroker()

    order = Order(
        symbol="NIFTY",
        side=OrderSide.BUY,
        quantity=75,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )

    placed = broker.place_order(order)

    fetched = broker.get_order(placed.broker_order_id)

    assert fetched == placed


def test_get_orders():
    broker = PaperBroker()

    broker.place_order(
        Order(
            symbol="NIFTY",
            side=OrderSide.BUY,
            quantity=75,
            order_type=OrderType.MARKET,
            product=ProductType.INTRADAY,
        )
    )

    assert len(broker.get_orders()) == 1


def test_cancel_order():
    broker = PaperBroker()

    order = broker.place_order(
        Order(
            symbol="NIFTY",
            side=OrderSide.BUY,
            quantity=75,
            order_type=OrderType.MARKET,
            product=ProductType.INTRADAY,
        )
    )

    broker.cancel_order(order.broker_order_id)

    assert broker.get_order(order.broker_order_id).status == OrderStatus.CANCELLED