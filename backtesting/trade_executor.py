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
from engines.trade_management_engine import TradeManagementEngine
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
        self._trade_management_engine = TradeManagementEngine()

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

    def evaluate_candle(
        self,
        *,
        high: Decimal,
        low: Decimal,
        timestamp: datetime,
    ) -> Trade | None:
        """
        Evaluate the current candle against the open trade.

        Existing stop-loss and target are evaluated first.
        A breakeven stop moved during this candle becomes effective
        from the next candle.
        """

        if self._current_trade is None:
            return None

        trade = self._current_trade

        # -------------------------------------------------
        # Existing SL / Target
        # -------------------------------------------------

        if trade.risk.decision.signal.value == "BUY_CE":
            if low <= trade.stop_loss:
                return self.close_trade(
                    exit_price=trade.stop_loss,
                    exit_time=timestamp,
                    exit_reason=ExitReason.STOP_LOSS,
                )

            if high >= trade.target:
                return self.close_trade(
                    exit_price=trade.target,
                    exit_time=timestamp,
                    exit_reason=ExitReason.TARGET,
                )

            current_price = high

        else:
            if low <= trade.target:
                return self.close_trade(
                    exit_price=trade.target,
                    exit_time=timestamp,
                    exit_reason=ExitReason.TARGET,
                )

            if high >= trade.stop_loss:
                return self.close_trade(
                    exit_price=trade.stop_loss,
                    exit_time=timestamp,
                    exit_reason=ExitReason.STOP_LOSS,
                )

            current_price = low

        # -------------------------------------------------
        # Trade management
        # -------------------------------------------------

        management = self._trade_management_engine.evaluate(
            entry_price=trade.entry_price,
            stop_loss=trade.stop_loss,
            current_price=current_price,
        )

        if management.move_stop_loss:
            self._current_trade = replace(
                trade,
                stop_loss=management.new_stop_loss,
            )

        return None

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
