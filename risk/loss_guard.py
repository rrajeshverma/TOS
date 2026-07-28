"""
TOS Loss Guard

Protects account from excessive losses.
"""

from __future__ import annotations


class LossGuard:
    """
    Validates daily loss limits.
    """

    def __init__(
        self,
        max_loss: float,
    ) -> None:

        if max_loss < 0:
            raise ValueError(
                "Loss limit cannot be negative"
            )

        self.max_loss = max_loss


    def check(
        self,
        current_loss: float,
    ) -> dict:
        """
        Check current loss against limit.
        """

        if current_loss < 0:
            raise ValueError(
                "Loss cannot be negative"
            )

        approved = (
            current_loss
            <= self.max_loss
        )

        return {
            "approved": approved,
            "current_loss": current_loss,
            "max_loss": self.max_loss,
        }
