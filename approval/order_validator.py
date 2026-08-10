"""
TOS Order Validator

Validates trade requests before execution.
"""

from __future__ import annotations

from typing import ClassVar


class OrderValidator:
    """
    Validates incoming trade requests.
    """

    from typing import ClassVar

    VALID_SIDES: ClassVar[set[str]] = {
        "BUY",
        "SELL",
    }

    VALID_BROKERS: ClassVar[set[str]] = {
        "DHAN",
        "DELTA",
        "ZERODHA",
        "PAPER",
    }

    def validate(
        self,
        request,
    ) -> dict:
        """
        Validate trade request.
        """

        errors = []

        if not request.symbol:
            errors.append("Symbol is required")

        if request.side not in self.VALID_SIDES:
            errors.append("Invalid side")

        if request.quantity <= 0:
            errors.append("Quantity must be positive")

        if request.price <= 0:
            errors.append("Price must be positive")

        if not request.strategy:
            errors.append("Strategy is required")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }
