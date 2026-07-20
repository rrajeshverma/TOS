"""
=========================================================
Trading Operating System (TOS)
Module      : Position Manager
Version     : 1.0.0
Author      : Rajesh Varma
Description : Manages paper trading positions.
=========================================================
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from domain.position import Position
from domain.order import Order

from shared.enums import TradeStatus
from shared.logger import get_logger

from utils.id_generator import generate_position_id


class PositionManager:
    """
    Manages the lifecycle of trading positions.
    """

    def __init__(self) -> None:
        self._logger = get_logger(__name__)

    def open_position(
        self,
        order: Order | None,
        quantity: int,
        price: Decimal,
    ) -> Position:

        position = Position(
            position_id=generate_position_id(),
            order=order,
            quantity=quantity,
            average_price=price,
            last_traded_price=price,
            status=TradeStatus.OPEN,
            opened_at=datetime.now(),
        )

        self._logger.info(
            "Position opened: %s",
            position.position_id,
        )

        return position

    @staticmethod
    def update_price(
        position: Position,
        ltp: Decimal,
    ) -> Position:

        return Position(
            position_id=position.position_id,
            order=position.order,
            quantity=position.quantity,
            average_price=position.average_price,
            last_traded_price=ltp,
            status=position.status,
            opened_at=position.opened_at,
            closed_at=position.closed_at,
        )

    @staticmethod
    def close_position(
        position: Position,
        exit_price: Decimal,
    ) -> Position:

        return Position(
            position_id=position.position_id,
            order=position.order,
            quantity=position.quantity,
            average_price=position.average_price,
            last_traded_price=exit_price,
            status=TradeStatus.CLOSED,
            opened_at=position.opened_at,
            closed_at=datetime.now(),
        )

    @staticmethod
    def unrealized_pnl(
        position: Position,
    ) -> Decimal:

        return (position.last_traded_price - position.average_price) * position.quantity

    @staticmethod
    def realized_pnl(
        entry_price: Decimal,
        exit_price: Decimal,
        quantity: int,
    ) -> Decimal:
        return (exit_price - entry_price) * quantity

    @staticmethod
    def is_position_open(
        position: Position,
    ) -> bool:
        return position.status == TradeStatus.OPEN
