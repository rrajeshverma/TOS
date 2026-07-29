"""
TOS Position Risk Calculator
"""

from __future__ import annotations


class PositionRiskCalculator:
    """
    Calculates risk for individual positions.
    """

    def calculate(
        self,
        position: dict,
        capital: float,
    ) -> dict:
        """
        Calculate position risk.
        """

        if capital <= 0:
            raise ValueError("Capital must be positive")

        quantity = position.get(
            "quantity",
            0,
        )

        price = position.get(
            "price",
            0,
        )

        stop_loss = position.get(
            "stop_loss",
            price,
        )

        position_value = quantity * price

        risk_amount = quantity * abs(price - stop_loss)

        risk_percentage = (risk_amount / capital) * 100

        return {
            "position_value": position_value,
            "risk_amount": risk_amount,
            "risk_percentage": risk_percentage,
        }
