from execution.order_service import OrderService


def test_broker_order_mapping():
    service = OrderService()

    internal_id = service.submit(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    service.register_broker_order(
        internal_id,
        "DHAN12345",
    )

    assert service.broker_order_id(internal_id) == "DHAN12345"


def test_unknown_mapping_returns_none():
    service = OrderService()

    assert service.broker_order_id(999) is None


def test_register_unknown_internal_order():
    service = OrderService()

    try:
        service.register_broker_order(999, "DHAN1")
    except KeyError:
        pass
    else:
        assert False