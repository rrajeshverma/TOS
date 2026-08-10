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
        quantity=50,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )


def test_place_order_assigns_id():
    broker = PaperBroker()

    order = broker.place_order(create_order())

    assert order.broker_order_id is not None


def test_initial_status_pending():
    broker = PaperBroker()

    order = broker.place_order(create_order())

    assert order.status == OrderStatus.PENDING


def test_order_preserves_symbol():
    broker = PaperBroker()

    order = broker.place_order(create_order())

    assert order.symbol == "NIFTY"


def test_order_preserves_side():
    broker = PaperBroker()

    order = broker.place_order(create_order())

    assert order.side == OrderSide.BUY


def test_order_preserves_quantity():
    broker = PaperBroker()

    order = broker.place_order(create_order())

    assert order.quantity == 50


def test_get_order_returns_same_instance():
    broker = PaperBroker()

    placed = broker.place_order(create_order())

    fetched = broker.get_order(placed.broker_order_id)

    assert fetched == placed


def test_get_orders_initially_empty():
    broker = PaperBroker()

    assert broker.get_orders() == []


def test_get_orders_after_place():
    broker = PaperBroker()

    broker.place_order(create_order())

    assert len(broker.get_orders()) == 1


def test_get_positions_initially_empty():
    broker = PaperBroker()

    assert broker.get_positions() == []


def test_get_holdings_initially_empty():
    broker = PaperBroker()

    assert broker.get_holdings() == []


def test_funds_available_cash():
    broker = PaperBroker()

    assert broker.get_funds().available_cash == Decimal(1000000)


def test_connect():
    broker = PaperBroker()

    broker.connect()

    assert broker.is_connected()


def test_disconnect():
    broker = PaperBroker()

    broker.connect()
    broker.disconnect()

    assert not broker.is_connected()


def test_unique_order_ids():
    broker = PaperBroker()

    a = broker.place_order(create_order())
    b = broker.place_order(create_order())

    assert a.broker_order_id != b.broker_order_id


def test_cancel_changes_status():
    broker = PaperBroker()

    order = broker.place_order(create_order())

    broker.cancel_order(order.broker_order_id)

    cancelled = broker.get_order(order.broker_order_id)

    assert cancelled.status == OrderStatus.CANCELLED


def test_get_health():
    broker = PaperBroker()

    health = broker.get_health()

    assert health == {
        "broker": "PaperBroker",
        "connected": False,
        "latency_ms": 0,
        "heartbeat": "UNKNOWN",
    }
