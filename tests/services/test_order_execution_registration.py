from services.order_execution_adapter import OrderExecutionAdapter


def test_execution_registers_broker_order():
    class FakeOrderService:
        def __init__(self):
            self.registered = None

        def place_order(self, order):
            return {
                "orderId": "BROKER123",
                "status": "SUBMITTED",
            }

        def register_broker_order(
            self,
            order_id,
            broker_order_id,
        ):
            self.registered = (
                order_id,
                broker_order_id,
            )

    service = FakeOrderService()

    adapter = OrderExecutionAdapter(order_service=service)

    result = adapter.execute(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 65,
            "price": 25000,
            "order_id": 1,
        }
    )

    assert result["orderId"] == "BROKER123"
