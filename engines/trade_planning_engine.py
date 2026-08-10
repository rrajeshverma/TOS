"""
=========================================================
Trading Operating System (TOS)

Module      : Trade Planning Engine
Version     : 1.0.0
Author      : Rajesh Varma
Description : Creates immutable trade execution plans.
=========================================================
"""

from decimal import Decimal

from domain.decision import Decision
from domain.position_size import PositionSize
from domain.trade_plan import TradePlan


class TradePlanningEngine:
    """
    Creates immutable trade plans.
    """

    def create_plan(
        self,
        decision: Decision,
        position_size: PositionSize,
        entry_price: Decimal,
        stop_loss: Decimal,
        target_price: Decimal,
    ) -> TradePlan:
        """
        Create a fully validated trade plan.
        """

        if stop_loss >= entry_price:
            raise ValueError("Stop loss must be below entry price.")

        if target_price <= entry_price:
            raise ValueError("Target price must be above entry price.")

        return TradePlan(
            decision=decision,
            position_size=position_size,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_price=target_price,
        )
