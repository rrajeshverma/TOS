"""
=========================================================
Trading Operating System (TOS)

Module      : Trade Planning Service
Version     : 1.0.0
Author      : Rajesh Varma
Description : Coordinates trade planning workflow.
=========================================================
"""

from decimal import Decimal

from domain.decision import Decision
from domain.trade_plan import TradePlan
from engines.trade_planning_engine import (
    TradePlanningEngine,
)
from services.position_sizing_service import (
    PositionSizingService,
)


class TradePlanningService:
    """
    Coordinates trade planning.
    """

    def __init__(
        self,
        trade_planning_engine: TradePlanningEngine | None = None,
        position_sizing_service: PositionSizingService | None = None,
    ) -> None:
        self._trade_planning_engine = trade_planning_engine or TradePlanningEngine()

        self._position_sizing_service = (
            position_sizing_service or PositionSizingService()
        )

    def create_trade_plan(
        self,
        decision: Decision,
        entry_price: Decimal,
        stop_loss: Decimal,
        target_price: Decimal,
        risk_per_trade: Decimal,
        lot_size: int,
    ) -> TradePlan:
        """
        Create a complete trade plan.
        """

        stop_distance = entry_price - stop_loss

        position = self._position_sizing_service.calculate(
            risk_per_trade=risk_per_trade,
            stop_distance=stop_distance,
            lot_size=lot_size,
        )

        return self._trade_planning_engine.create_plan(
            decision=decision,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_price=target_price,
            lots=position.lots,
            quantity=position.quantity,
        )
