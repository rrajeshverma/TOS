"""
=========================================================
Trading Operating System (TOS)
Module      : Risk
Version     : 1.0.0
Author      : Rajesh Varma
Description : Risk evaluation domain object.
=========================================================
"""

from dataclasses import dataclass

from domain.decision import Decision


@dataclass(frozen=True, slots=True)
class Risk:
    """
    Represents the outcome of risk evaluation.

    A Risk object answers one question:

    "Is this decision allowed to become a trade?"
    """

    decision: Decision

    approved: bool

    reasons: tuple[str, ...]

    @property
    def is_approved(self) -> bool:
        """
        Returns True if risk evaluation passed.
        """
        return self.approved

    @property
    def reason_count(self) -> int:
        """
        Number of risk evaluation reasons.
        """
        return len(self.reasons)
