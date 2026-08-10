from decimal import Decimal

import pytest

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


def test_rejects_zero_quantity():
    executor = TradeExecutor(PositionManager())

    order = create_order()

    with pytest.raises(ValueError):
        executor.execute(
            order.trade,
            order,
            0,
            Decimal(25000),
        )


def test_rejects_negative_price():
    executor = TradeExecutor(PositionManager())

    order = create_order()

    with pytest.raises(ValueError):
        executor.execute(
            order.trade,
            order,
            order.quantity,
            Decimal(-1),
        )
