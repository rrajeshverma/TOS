from execution.execution_engine import ExecutionEngine
from execution.execution_request import ExecutionRequest


def test_execution_engine_places_order_after_submission():
    class FakeOrderService:
        def __init__(self):
            self.submitted = False
            self.placed = False

        def submit(self, request):
            self.submitted = True
            return 1

        def place_order(self, order):
            self.placed = True

            return {
                "orderId": "BROKER123",
                "status": "SUBMITTED",
            }

    service = FakeOrderService()

    engine = ExecutionEngine(service)

    result = engine.execute(
        ExecutionRequest(
            symbol="NIFTY",
            side="BUY",
            quantity=65,
        )
    )

    assert service.submitted is True
    assert service.placed is True
    assert result.success is True
