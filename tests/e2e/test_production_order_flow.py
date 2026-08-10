from decimal import Decimal

from engines.order_factory import OrderFactory
from execution.order_service import OrderService
from services.order_execution_adapter import OrderExecutionAdapter
from shared.enums import Broker, OrderSide
from tests.test_trade_factory import create_trade


def create_order():
    return OrderFactory().create(
        trade=create_trade(),
        broker=Broker.DHAN,
        side=OrderSide.BUY,
        price=Decimal(25000),
    )


def test_real_order_flow():
    order = create_order()

    payload = OrderExecutionAdapter().to_execution_order(order)

    service = OrderService()

    order_id = service.submit(payload)

    assert order_id == 1

    assert service.order_count == 1
