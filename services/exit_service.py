"""
=========================================================
Trading Operating System (TOS)
Module      : Exit Service
Version     : 1.0.0
Description : Executes position exit lifecycle.
=========================================================
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, time
from decimal import Decimal

from journal.trade_journal import TradeJournal
from services.exit_manager import ExitManager
from services.position_manager import PositionManager
from shared.enums import ExitReason, TradeStatus


class ExitService:
    """
    Handles exit decision and position closure.
    """

    def __init__(
        self,
        exit_manager: ExitManager | None = None,
        position_manager: PositionManager | None = None,
        trade_journal: TradeJournal | None = None,
    ) -> None:
        self.exit_manager = exit_manager or ExitManager()

        self.position_manager = position_manager or PositionManager()

        self.trade_journal = trade_journal or TradeJournal()

    def evaluate(
        self,
        position,
        current_price: Decimal,
        current_time: time,
    ):
        """
        Evaluate exit condition and close position.
        """

        reason = self.exit_manager.check_exit(
            position,
            current_price,
            current_time,
        )

        if reason == ExitReason.NONE:
            return {
                "closed": False,
                "reason": reason,
                "position": position,
            }

        closed_position = self.position_manager.close_position(
            position,
            current_price,
        )

        trade = position.order.trade

        pnl = (current_price - trade.entry_price) * trade.quantity

        closed_trade = replace(
            trade,
            exit_price=current_price,
            exit_time=datetime.now(),
            exit_reason=reason,
            pnl=pnl,
            status=TradeStatus.CLOSED,
        )

        self.trade_journal.record(
            closed_trade,
        )

        return {
            "closed": True,
            "reason": reason,
            "position": closed_position,
            "trade": closed_trade,
        }
