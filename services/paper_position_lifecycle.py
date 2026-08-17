"""
Paper position lifecycle bridge.

Connects the modern TradePlan + ExecutionResult path
to the existing domain Trade/Order/Position lifecycle.
"""

from __future__ import annotations

from engines.order_factory import OrderFactory
from engines.trade_factory import TradeFactory
from services.position_book import PositionBook
from services.position_manager import PositionManager
from shared.enums import Broker, OrderSide


class PaperPositionLifecycle:
    def __init__(
        self,
        position_manager: PositionManager | None = None,
        position_book: PositionBook | None = None,
        trade_factory: TradeFactory | None = None,
        order_factory: OrderFactory | None = None,
    ) -> None:
        self.position_manager = position_manager or PositionManager()
        self.position_book = position_book or PositionBook()
        self.trade_factory = trade_factory or TradeFactory()
        self.order_factory = order_factory or OrderFactory()

    def open_from_execution(
        self,
        risk,
        trade_plan,
        execution_result,
    ):
        if risk is None:
            raise ValueError("Risk cannot be None")

        if trade_plan is None:
            raise ValueError("Trade plan cannot be None")

        if execution_result is None:
            raise ValueError("Execution result cannot be None")

        if not execution_result.success:
            return None

        quantity = trade_plan.position_size.quantity

        trade = self.trade_factory.create(
            risk=risk,
            entry_price=trade_plan.entry_price,
            stop_loss=trade_plan.stop_loss,
            quantity=quantity,
        )

        order = self.order_factory.create(
            trade=trade,
            broker=Broker.DHAN,
            side=OrderSide.BUY,
            price=trade_plan.entry_price,
        )

        position = self.position_manager.open_position(
            order=order,
            quantity=quantity,
            price=trade_plan.entry_price,
        )

        self.position_book.add_position(
            position.position_id,
            position,
        )

        return position
