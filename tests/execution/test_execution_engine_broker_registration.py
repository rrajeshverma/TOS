from execution.execution_engine import ExecutionEngine
from execution.execution_request import ExecutionRequest
from execution.order_service import OrderStatus


def test_execution_engine_registers_broker_order():
    class FakeOrderService:
        def __init__(self):
            self.registered = None
            self.status = None

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

        def update_status(
            self,
            order_id,
            status,
        ):
            self.status = status

    service = FakeOrderService()

    engine = ExecutionEngine(service)

    result = engine.execute(
        ExecutionRequest(
            symbol="NIFTY",
            side="BUY",
            quantity=65,
        )
    )

    assert result.success is True

    assert service.registered == (
        1,
        "BROKER123",
    )

    assert service.status == OrderStatus.SUBMITTED
