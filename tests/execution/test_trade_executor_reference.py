from decimal import Decimal

from engines.order_factory import OrderFactory
from execution.trade_executor import TradeExecutor
from services.position_manager import PositionManager
from shared.enums import Broker, OrderSide
from tests.test_trade_factory import create_trade


def create_order():
    trade = create_trade()

    return OrderFactory().create(
        trade=trade,
        broker=Broker.DHAN,
        side=OrderSide.BUY,
        price=Decimal(25000),
    )


def test_position_keeps_order_reference():
    executor = TradeExecutor(PositionManager())

    order = create_order()

    position = executor.execute(
        order.trade,
        order,
        quantity=order.quantity,
        price=order.requested_price,
    )

    assert position.order == order
