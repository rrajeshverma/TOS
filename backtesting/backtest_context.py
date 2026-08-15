"""
=========================================================
Trading Operating System (TOS)
Module      : Backtest Context
Version     : 1.1.0
Author      : Rajesh Varma
Description : Owns all backtesting state during replay.
=========================================================
"""

from __future__ import annotations

from decimal import Decimal

from backtesting.trade_executor import TradeExecutor
from backtesting.trade_ledger import TradeLedger
from backtesting.trade_recorder import TradeRecorder
from shared.enums import ExitReason


class BacktestContext:
    """
    Holds all runtime objects required during backtesting.

    Live trading never uses this class.
    """

    def __init__(self) -> None:
        self.trade_executor = TradeExecutor()
        self.trade_recorder = TradeRecorder()
        self.trade_ledger = TradeLedger()

    def on_risk(
        self,
        risk,
        market,
        trade_plan=None,
    ) -> None:
        """
        Process a completed Risk evaluation.
        """

        if not risk.is_approved:
            return

        executor = self.trade_executor

        # -------------------------------------------------
        # No open trade -> Open one
        # -------------------------------------------------

        if not executor.has_open_trade:
            if trade_plan is None:
                raise ValueError("Trade plan is required for backtest execution")

            trade = executor.open_trade(
                risk=risk,
                entry_price=trade_plan.entry_price,
                quantity=trade_plan.position_size.quantity,
                entry_time=market.timestamp,
                stop_loss=trade_plan.stop_loss,
                target=trade_plan.target_price,
            )

            self.trade_recorder.record(trade)
            return

        # -------------------------------------------------
        # Existing trade
        # -------------------------------------------------

        current = executor.current_trade

        current_signal = current.risk.decision.signal
        new_signal = risk.decision.signal

        if current_signal == new_signal:
            return

        closed_trade = executor.close_trade(
            exit_price=Decimal(str(market.close)),
            exit_time=market.timestamp,
            exit_reason=ExitReason.MANUAL,
        )

        self.trade_recorder.record(closed_trade)
        self.trade_ledger.add(closed_trade)

        if trade_plan is None:
            raise ValueError("Trade plan is required for backtest execution")

        new_trade = executor.open_trade(
            risk=risk,
            entry_price=trade_plan.entry_price,
            quantity=trade_plan.position_size.quantity,
            entry_time=market.timestamp,
            stop_loss=trade_plan.stop_loss,
            target=trade_plan.target_price,
        )

        self.trade_recorder.record(new_trade)

    def finalize(
        self,
        market,
    ) -> None:
        """
        Close any remaining open trade at the end of replay.
        """

        executor = self.trade_executor

        if not executor.has_open_trade:
            return

        closed_trade = executor.close_trade(
            exit_price=Decimal(str(market.close)),
            exit_time=market.timestamp,
            exit_reason=ExitReason.END_OF_DATA,
        )

        self.trade_recorder.record(closed_trade)
        self.trade_ledger.add(closed_trade)

    def on_market(
        self,
        market,
    ) -> None:
        """
        Evaluate an existing trade against the current candle.
        """

        if not self.trade_executor.has_open_trade:
            return

        closed_trade = self.trade_executor.evaluate_candle(
            high=Decimal(str(market.high)),
            low=Decimal(str(market.low)),
            timestamp=market.timestamp,
        )

        if closed_trade is not None:
            self.trade_recorder.record(closed_trade)
            self.trade_ledger.add(closed_trade)
