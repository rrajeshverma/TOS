"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Executor
Version     : 1.1.0
Author      : Rajesh Varma
Description : Simulates trade execution during backtesting.
=========================================================
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from decimal import Decimal

from domain.risk import Risk
from domain.trade import Trade
from shared.enums import ExitReason, TradeStatus
from utils.id_generator import generate_trade_id


class TradeExecutor:
    """
    Simulates execution of approved trades during backtesting.

    Only one trade can be open at a time.

    Future versions will support:

    - Stop Loss
    - Target
    - Trailing Stop
    - Position Sizing
    - Slippage
    - Brokerage
    """

    def __init__(self) -> None:
        self._current_trade: Trade | None = None

    @property
    def current_trade(self) -> Trade | None:
        """Return currently open trade."""
        return self._current_trade

    @property
    def has_open_trade(self) -> bool:
        """Return True if a trade is open."""
        return self._current_trade is not None

    def open_trade(
        self,
        risk: Risk,
        entry_price: Decimal,
        quantity: int,
        entry_time: datetime,
        stop_loss: Decimal = Decimal(0),
        target: Decimal = Decimal(0),
    ) -> Trade:
        """
        Open a new trade.
        """

        if self.has_open_trade:
            raise RuntimeError("Trade already open.")

        trade = Trade(
            trade_id=generate_trade_id(),
            risk=risk,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target=target,
            quantity=quantity,
            entry_time=entry_time,
            status=TradeStatus.OPEN,
        )

        self._current_trade = trade

        return trade

    def close_trade(
        self,
        exit_price: Decimal,
        exit_time: datetime,
        exit_reason: ExitReason = ExitReason.MANUAL,
    ) -> Trade:
        """
        Close the current trade.
        """

        if self._current_trade is None:
            raise RuntimeError("No open trade.")

        trade = self._current_trade

        signal = trade.risk.decision.signal

        if signal.value == "BUY_CE":
            pnl = (exit_price - trade.entry_price) * trade.quantity
        else:
            pnl = (trade.entry_price - exit_price) * trade.quantity

        closed_trade = replace(
            trade,
            exit_price=exit_price,
            exit_time=exit_time,
            exit_reason=exit_reason,
            pnl=pnl,
            status=TradeStatus.CLOSED,
        )

        self._current_trade = None

        return closed_trade
