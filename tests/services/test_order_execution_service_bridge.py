from services.order_execution_adapter import OrderExecutionAdapter


def test_execution_adapter_registers_order():
    class FakeOrderService:
        def submit(self, order):
            return {
                "order_id": "TOS-001",
                "status": "SUBMITTED",
            }

    adapter = OrderExecutionAdapter(order_service=FakeOrderService())

    assert adapter is not None


def test_adapter_executes_using_order_service():
    class FakeOrderService:
        def place_order(self, order):
            return {
                "order_id": "TOS-001",
                "status": "SUBMITTED",
            }

    adapter = OrderExecutionAdapter(order_service=FakeOrderService())

    result = adapter.execute(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 65,
            "price": 25000,
        }
    )

    assert result["order_id"] == "TOS-001"
