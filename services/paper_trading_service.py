"""
=========================================================
Trading Operating System (TOS)
Module      : Paper Trading Service
Version     : 1.0.0
Author      : Rajesh Varma
Description : Simulates execution of approved trades.
=========================================================
"""

from __future__ import annotations

from datetime import datetime

from domain.position import Position
from domain.trade import Trade
from shared.enums import TradeStatus
from shared.logger import get_logger
from utils.id_generator import generate_position_id


class PaperTradingService:
    """
    Executes trades in paper mode.
    """

    def __init__(self) -> None:
        self._logger = get_logger(__name__)

    def execute(
        self,
        trade: Trade,
    ) -> Position:
        """
        Simulate instant execution of a Trade.
        """

        position = Position(
            position_id=generate_position_id(),
            order=None,
            quantity=trade.quantity,
            average_price=trade.entry_price,
            last_traded_price=trade.entry_price,
            status=TradeStatus.OPEN,
            opened_at=datetime.now(),
        )

        self._logger.info(
            "Paper Position Opened: %s",
            position.position_id,
        )

        return position

    @staticmethod
    def update_price(
        position: Position,
        ltp,
    ) -> Position:
        """
        Return a new Position with updated LTP.
        """

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
    def close(
        position: Position,
        exit_price,
    ) -> Position:
        """
        Close an existing paper position.
        """

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
