"""
TOS Exposure Limit Guard
"""

from __future__ import annotations


class ExposureLimitGuard:
    """
    Validates portfolio exposure limits.
    """

    def __init__(
        self,
        max_exposure_percentage: float = 100,
    ) -> None:
        self.max_exposure_percentage = max_exposure_percentage

    def check(
        self,
        exposure: float,
        capital: float,
    ) -> dict:
        if capital <= 0:
            raise ValueError("Capital must be positive")

        exposure_percentage = (exposure / capital) * 100

        approved = exposure_percentage <= self.max_exposure_percentage

        return {
            "approved": approved,
            "exposure_percentage": exposure_percentage,
            "limit": self.max_exposure_percentage,
        }
