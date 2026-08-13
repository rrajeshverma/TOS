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


def test_execution_request_is_converted_to_broker_order():
    from brokers.models import Order, OrderSide, OrderType, ProductType
    from execution.execution_request import ExecutionRequest

    class FakeOrderService:
        def __init__(self):
            self.submitted = None
            self.placed = None
            self.registered = None

        def submit(self, request):
            self.submitted = request
            return 1

        def place_order(self, order):
            self.placed = order
            return {
                "orderId": "BROKER-123",
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

    request = ExecutionRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
    )

    result = engine.execute(request)

    assert result.success is True
    assert result.order_id == 1

    assert service.submitted is request

    assert isinstance(service.placed, Order)
    assert service.placed.symbol == "NIFTY"
    assert service.placed.side == OrderSide.BUY
    assert service.placed.quantity == 65
    assert service.placed.order_type == OrderType.MARKET
    assert service.placed.product == ProductType.INTRADAY

    assert service.registered == (
        1,
        "BROKER-123",
    )
