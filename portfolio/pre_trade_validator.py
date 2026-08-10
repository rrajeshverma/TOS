"""
=========================================================
Trading Operating System (TOS)

Module      : Pre Trade Validator
Description : Validates trades before execution.
=========================================================
"""

from __future__ import annotations


class PreTradeValidator:
    """
    Validates trading conditions before order execution.
    """

    def __init__(
        self,
        risk=None,
        risk_guard=None,
    ):
        self.risk = risk
        self.risk_guard = risk_guard

    def validate(self):
        """
        Return True only when all checks pass.
        """

        if self.risk is not None and not self.risk.can_open_position():
            return False

        return not (self.risk_guard is not None and not self.risk_guard.can_trade())
