from services.order_execution_adapter import OrderExecutionAdapter
from execution.order_idempotency import OrderIdempotency


class FakeBroker:
    def __init__(self):
        self.calls = 0

    def place_order(self, order):
        self.calls += 1

        return {
            "order_id": "ABC123",
            "status": "SUBMITTED",
        }


def test_duplicate_order_not_sent_to_broker():
    broker = FakeBroker()

    adapter = OrderExecutionAdapter(
        broker=broker,
        idempotency=OrderIdempotency(),
    )

    order = {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
        "price": 25000,
    }

    adapter.execute(order)

    adapter.execute(order)

    assert broker.calls == 1
