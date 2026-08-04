"""
=========================================================
Trading Operating System (TOS)

Module      : Trade Management Engine
Version     : 1.0.0
Author      : Rajesh Varma
Description : Manages open trades.
=========================================================
"""

from __future__ import annotations

from decimal import Decimal

from domain.trade_management import TradeManagement


class TradeManagementEngine:
    """
    Handles trade management decisions.
    """

    def evaluate(
        self,
        *,
        entry_price: Decimal,
        stop_loss: Decimal,
        current_price: Decimal,
    ) -> TradeManagement:
        """
        Move stop loss to breakeven after 1R.
        """

        risk = entry_price - stop_loss

        reward = current_price - entry_price

        if reward >= risk:
            return TradeManagement(
                move_stop_loss=True,
                new_stop_loss=entry_price,
                exit_trade=False,
            )

        return TradeManagement(
            move_stop_loss=False,
            new_stop_loss=None,
            exit_trade=False,
        )
