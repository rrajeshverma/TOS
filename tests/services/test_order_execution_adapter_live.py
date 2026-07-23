from services.order_execution_adapter import OrderExecutionAdapter


def test_adapter_requires_broker():
    adapter = OrderExecutionAdapter()

    assert adapter is not None


def test_adapter_executes_order():
    class FakeBroker:
        def place_order(self, order):
            return {
                "order_id": "ABC123",
                "status": "SUBMITTED",
            }

    adapter = OrderExecutionAdapter(broker=FakeBroker())

    result = adapter.execute(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": 1,
            "price": 62000,
        }
    )

    assert result["order_id"] == "ABC123"
