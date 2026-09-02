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
from domain.instrument import Instrument
from domain.position_size import PositionSize
from domain.trade_plan import TradePlan
from shared.enums import Signal


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
        instrument: Instrument | None = None,
    ) -> TradePlan:
        """
        Create a fully validated trade plan.
        """

        if decision.signal == Signal.BUY_CE:
            if stop_loss >= entry_price:
                raise ValueError("Stop loss must be below entry price.")

            if target_price <= entry_price:
                raise ValueError("Target price must be above entry price.")

        elif decision.signal == Signal.BUY_PE:
            if stop_loss <= entry_price:
                raise ValueError("Stop loss must be above entry price.")

            if target_price >= entry_price:
                raise ValueError("Target price must be below entry price.")

        return TradePlan(
            decision=decision,
            position_size=position_size,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_price=target_price,
            symbol=instrument.symbol if instrument else None,
            security_id=instrument.security_id if instrument else None,
            exchange_segment=instrument.exchange_segment if instrument else None,
            lot_size=instrument.lot_size if instrument else None,
            expiry=instrument.expiry if instrument else None,
            strike=instrument.strike if instrument else None,
            option_type=instrument.option_type if instrument else None,
        )
