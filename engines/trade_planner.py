"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Planner
Version     : 1.0.0
Author      : Rajesh Varma
Description : Calculates trade parameters after a
              Risk evaluation has been approved.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from domain.market import Market
from domain.risk import Risk


@dataclass(frozen=True, slots=True)
class TradePlan:
    """
    Planned trade parameters.
    """

    entry_price: Decimal
    stop_loss: Decimal


class TradePlanner:
    """
    Generates trade parameters from market data.

    Current implementation:
    - Entry  : Market Close
    - Stop   : Market Low

    This logic can later become strategy-specific.
    """

    def plan(
        self,
        market: Market,
        risk: Risk,
    ) -> TradePlan:
        """
        Build a trade plan for an approved risk.
        """

        if not risk.is_approved:
            raise ValueError("Cannot create TradePlan for rejected Risk.")

        return TradePlan(
            entry_price=Decimal(str(market.close)),
            stop_loss=Decimal(str(market.low)),
        )
