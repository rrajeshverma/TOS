from decimal import Decimal

from engines.order_factory import OrderFactory
from services.position_manager import PositionManager
from services.order_execution_adapter import OrderExecutionAdapter
from execution.order_service import OrderService, OrderStatus

from shared.enums import Broker, OrderSide

from tests.test_trade_factory import create_trade


def create_order():
    return OrderFactory().create(
        trade=create_trade(),
        broker=Broker.DHAN,
        side=OrderSide.BUY,
        price=Decimal("25000"),
    )


def test_trade_to_position_flow():
    order = create_order()

    payload = OrderExecutionAdapter().to_execution_order(order)

    service = OrderService()

    order_id = service.submit(payload)

    service.record_fill(
        order_id,
        quantity=order.quantity,
        price=float(order.requested_price),
    )

    assert service.status(order_id) == OrderStatus.FILLED


def test_filled_order_opens_position():
    order = create_order()

    position = PositionManager().open_position(
        order=order,
        quantity=order.quantity,
        price=order.requested_price,
    )

    assert position.order == order
    assert position.quantity == order.quantity
    assert position.average_price == order.requested_price
    assert position.is_open
