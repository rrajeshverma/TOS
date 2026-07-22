"""
=========================================================
Trading Operating System (TOS)

Module      : Trade Executor
Description : Converts trades into positions.
=========================================================
"""

from __future__ import annotations

from services.position_manager import PositionManager
from services.position_book import PositionBook


class TradeExecutor:

    def __init__(
        self,
        position_manager: PositionManager,
        position_book: PositionBook | None = None,
    ):
        self.position_manager = position_manager
        self.position_book = position_book


    def execute(
        self,
        trade,
        order=None,
        quantity=None,
        price=None,
    ):

        if trade is None:
            raise ValueError(
                "Trade cannot be None"
            )

        if quantity is None or quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero"
            )

        if price is None or price <= 0:
            raise ValueError(
                "Price must be greater than zero"
            )

        # Backward compatibility:
        # If order is not supplied, use trade reference.
        if order is None:
            order = getattr(
                trade.risk.decision,
                "order",
                None,
            )

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