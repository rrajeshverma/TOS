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
from domain.trade_plan import TradePlan


class TradePlanningEngine:
    """
    Creates immutable trade plans.
    """

    def create_plan(
        self,
        decision: Decision,
        entry_price: Decimal,
        stop_loss: Decimal,
        target_price: Decimal,
        lots: int,
        quantity: int,
    ) -> TradePlan:
        """
        Create a trade plan from a validated decision.
        """

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if lots <= 0:
            raise ValueError("Lots must be greater than zero.")

        if stop_loss >= entry_price:
            raise ValueError("Stop loss must be below entry price.")

        if target_price <= entry_price:
            raise ValueError("Target price must be above entry price.")

        risk_points = entry_price - stop_loss

        reward_points = target_price - entry_price

        risk_amount = risk_points * Decimal(quantity)

        reward_amount = reward_points * Decimal(quantity)

        return TradePlan(
            decision=decision,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_price=target_price,
            lots=lots,
            quantity=quantity,
            risk_amount=risk_amount,
            reward_amount=reward_amount,
        )
