from execution.execution_engine import ExecutionEngine
from execution.execution_result import ExecutionResult


def test_execution_engine_places_order_with_broker():
    class FakeOrderService:
        def __init__(self):
            self.registered = None

        def submit(self, request):
            return 1

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

    engine = ExecutionEngine(service)

    result = engine.execute(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 65,
        }
    )

    assert isinstance(
        result,
        ExecutionResult,
    )

    assert result.success is True
