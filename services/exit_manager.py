"""
=========================================================
Trading Operating System (TOS)
Module      : Exit Manager
Version     : 1.0.0
Description : Evaluates exit conditions for positions.
=========================================================
"""

from datetime import time
from decimal import Decimal

from shared.enums import ExitReason


class ExitManager:
    """
    Determines whether an open position should exit.
    """

    FORCE_EXIT_TIME = time(15, 15)

    def check_exit(
        self,
        position,
        current_price: Decimal,
        current_time: time,
    ) -> ExitReason:

        trade = position.order.trade

        if current_price >= trade.target:
            return ExitReason.TARGET

        if current_price <= trade.stop_loss:
            return ExitReason.STOP_LOSS

        if current_time >= self.FORCE_EXIT_TIME:
            return ExitReason.FORCE_EXIT

        return ExitReason.NONE
