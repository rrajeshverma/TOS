import pytest

from paper.paper_order_service import PaperOrderService


def request():
    return {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 50,
        "price": 25000.0,
    }


def test_can_create_service():
    assert PaperOrderService() is not None


def test_submit_returns_order_id():
    service = PaperOrderService()

    order_id = service.submit(request())

    assert order_id.startswith("PAPER-")


def test_submit_generates_unique_ids():
    service = PaperOrderService()

    first = service.submit(request())
    second = service.submit(request())

    assert first != second


def test_orders_are_stored():
    service = PaperOrderService()

    order_id = service.submit(request())

    assert order_id in service.orders


def test_order_count():
    service = PaperOrderService()

    service.submit(request())
    service.submit(request())

    assert len(service.orders) == 2


def test_rejects_none():
    service = PaperOrderService()

    with pytest.raises(ValueError):
        service.submit(None)


def test_repeatable():
    service = PaperOrderService()

    assert service.submit(request()).startswith("PAPER-")


def test_returns_same_order():
    service = PaperOrderService()

    order_id = service.submit(request())

    assert service.orders[order_id]["symbol"] == "NIFTY"


def test_preserves_quantity():
    service = PaperOrderService()

    order_id = service.submit(request())

    assert service.orders[order_id]["quantity"] == 50


def test_preserves_price():
    service = PaperOrderService()

    order_id = service.submit(request())

    assert service.orders[order_id]["price"] == 25000.0
