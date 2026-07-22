from execution.order_recovery import OrderRecovery


class FakeBroker:

    def get_orders(self):
        return [
            {
                "order_id": "ABC123",
                "status": "PENDING",
            }
        ]


def test_recovery_fetches_broker_orders():

    recovery = OrderRecovery(
        broker=FakeBroker()
    )

    orders = recovery.recover()

    assert len(orders) == 1
    assert orders[0]["order_id"] == "ABC123"


def test_recovery_requires_broker():

    try:
        OrderRecovery().recover()

        assert False

    except RuntimeError:
        assert True