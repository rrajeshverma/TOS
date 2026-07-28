"""
TOS Portfolio Engine

Coordinates portfolio evaluation.
"""

from __future__ import annotations

from portfolio.exposure import ExposureCalculator
from portfolio.allocation.allocation_engine import AllocationEngine


class PortfolioEngine:
    """
    Coordinates portfolio intelligence components.
    """

    def __init__(self) -> None:

        self.exposure_calculator = (
            ExposureCalculator()
        )


    def evaluate(
        self,
        context,
    ):
        """
        Evaluate portfolio state.
        """

        if context is None:
            return None


        positions = context.get(
            "positions",
            [],
        )

        capital = context.get(
            "capital",
            0,
        )


        exposure_result = (
            self.exposure_calculator.calculate(
                positions=positions,
                capital=capital,
            )
        )


        allocation_result = {}

        allocation = context.get(
            "allocation"
        )

        if allocation:

            allocation_engine = (
                AllocationEngine()
            )

            allocation_result = (
                allocation_engine.allocate(
                    capital=capital,
                    allocations=allocation,
                )
            )


        return {
            "exposure": (
                exposure_result["total_exposure"]
            ),
            "allocation": allocation_result,
            "status": "READY",
        }
