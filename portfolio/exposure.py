"""
TOS Portfolio Exposure Calculator

Calculates total portfolio exposure
and capital utilization.
"""

from __future__ import annotations


class ExposureCalculator:
    """
    Calculates portfolio exposure.
    """

    def calculate(
        self,
        positions,
        capital=0,
    ):
        """
        Calculate exposure metrics.
        """

        if capital < 0:
            raise ValueError(
                "Capital cannot be negative"
            )

        total_exposure = 0

        for position in positions:
            total_exposure += (
                position["quantity"]
                * position["price"]
            )

        exposure_percentage = 0

        if capital > 0:
            exposure_percentage = (
                total_exposure / capital
            ) * 100

        return {
            "total_exposure": total_exposure,
            "exposure_percentage": exposure_percentage,
            "available_capacity": (
                capital - total_exposure
            ),
        }
