"""
=========================================================
Trading Operating System (TOS)
Module      : Execution Plan
Version     : 1.0.0
Author      : Rajesh Varma
Description : Execution plan generated after risk approval.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from domain.risk import Risk
from shared.enums import OrderSide


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    """
    Represents the execution instructions for an approved trade.

    Generated after RiskEngine approval and consumed by the
    execution layer (paper, live, or backtesting).
    """

    # =====================================================
    # Reference
    # =====================================================

    risk: Risk

    # =====================================================
    # Order Details
    # =====================================================

    side: OrderSide

    quantity: int

    # =====================================================
    # Execution Levels
    # =====================================================

    entry_price: Decimal

    stop_loss: Decimal

    target: Decimal

    @property
    def is_buy(self) -> bool:
        """Return True when this is a BUY order."""
        return self.side == OrderSide.BUY

    @property
    def is_sell(self) -> bool:
        """Return True when this is a SELL order."""
        return self.side == OrderSide.SELL
