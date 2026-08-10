"""
Trading Operating System (TOS)
"""

from __future__ import annotations

from services.position_book import PositionBook
from services.position_manager import PositionManager


class TradeExecutor:
    def __init__(
        self,
        position_manager: PositionManager,
        position_book: PositionBook | None = None,
        order_service=None,  # ✅ added
    ):
        self.position_manager = position_manager
        self.position_book = position_book
        self.order_service = order_service  # ✅ added

    def execute(
        self,
        trade,
        order=None,
        quantity=None,
        price=None,
    ):
        if trade is None:
            raise ValueError("Trade cannot be None")

        if quantity is None or quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if price is None or price <= 0:
            raise ValueError("Price must be greater than zero")

        # -----------------------------------
        # Resolve order (existing logic)
        # -----------------------------------
        if order is None:
            order = getattr(
                trade.risk.decision,
                "order",
                None,
            )

        # -----------------------------------
        # 🔥 LIVE ORDER EXECUTION (FINAL)
        # -----------------------------------
        if self.order_service is not None:
            if order is None:
                raise ValueError("Order is required for live execution")

            # ✅ ONLY responsibility: send order
            self.order_service.submit(order)

        # -----------------------------------
        # 🔥 LIVE MODE → DO NOT OPEN POSITION
        # -----------------------------------
        if self.order_service is not None:
            # position will be created by poller
            return None

        # -----------------------------------
        # BACKTEST / PAPER MODE → OPEN POSITION
        # -----------------------------------
        position = self.position_manager.open_position(
            order=order,
            quantity=quantity,
            price=price,
        )

        if self.position_book is not None:
            self.position_book.add_position(
                position.position_id,
                position,
            )

        return position
