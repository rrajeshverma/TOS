"""
=========================================================
Trading Operating System (TOS)

Module      : Strategy Result
Version     : 1.0.0
Author      : Rajesh Varma
Description : Result produced by a trading strategy.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from shared.enums import Signal


@dataclass(frozen=True, slots=True)
class StrategyResult:
    """
    Represents the outcome of strategy evaluation.
    """

    signal: Signal

    reasons: tuple[str, ...]

    @property
    def has_signal(self) -> bool:
        return self.signal != Signal.NONE
