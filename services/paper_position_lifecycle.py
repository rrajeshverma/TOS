"""
Paper position lifecycle bridge.

Connects the modern TradePlan + ExecutionResult path
to the existing domain Trade/Order/Position lifecycle.
"""

from __future__ import annotations

from datetime import datetime, time
from decimal import Decimal

from brokers.models import OrderStatus
from engines.order_factory import OrderFactory
from engines.trade_factory import TradeFactory
from journal.trade_journal import TradeJournal
from services.exit_service import ExitService
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
        trade_journal: TradeJournal | None = None,
        exit_service: ExitService | None = None,
        order_service=None,
        broker=None,
    ) -> None:
        self.position_manager = position_manager or PositionManager()
        self.position_book = position_book or PositionBook()
        self.trade_factory = trade_factory or TradeFactory()
        self.order_factory = order_factory or OrderFactory()
        self.trade_journal = trade_journal or TradeJournal()
        self.exit_service = exit_service or ExitService(
            position_manager=self.position_manager,
            trade_journal=self.trade_journal,
        )
        self.order_service = order_service
        self.broker = broker

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

        if self.order_service is not None:
            internal_order_id = execution_result.order_id

            if internal_order_id is None:
                raise ValueError("Successful paper execution requires an order ID")

            self.order_service.record_fill(
                internal_order_id,
                quantity=quantity,
                price=float(trade_plan.entry_price),
            )

            if self.broker is not None:
                broker_order_id = self.order_service.broker_order_id(internal_order_id)

                if broker_order_id is not None:
                    self.broker.modify_order(
                        broker_order_id,
                        status=OrderStatus.COMPLETE,
                    )

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

    def update_positions(
        self,
        current_price: Decimal,
        current_time: time | None = None,
    ) -> list[dict]:
        """Update active paper positions and process exits."""

        if current_price is None:
            raise ValueError("Current price cannot be None")

        if current_time is None:
            current_time = datetime.now().time()

        results: list[dict] = []

        for position in list(self.position_book.get_all_positions()):
            updated_position = self.position_manager.update_price(
                position,
                Decimal(str(current_price)),
            )

            result = self.exit_service.evaluate(
                position=updated_position,
                current_price=Decimal(str(current_price)),
                current_time=current_time,
            )

            if result["closed"]:
                self.position_book.remove_position(
                    position.position_id,
                )
            else:
                self.position_book.add_position(
                    result["position"].position_id,
                    result["position"],
                )

            results.append(result)

        return results
