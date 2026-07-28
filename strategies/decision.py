"""
TOS Strategy Decision Object

Structured output from strategy plugins.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class StrategyDecision:
    """
    Represents a strategy-generated decision.
    """

    strategy: str
    signal: str
    confidence: int
    metadata: dict = field(
        default_factory=dict
    )


    def __post_init__(self) -> None:

        if not self.strategy:
            raise ValueError(
                "Strategy is required"
            )

        if not self.signal:
            raise ValueError(
                "Signal is required"
            )

        if (
            self.confidence < 0
            or self.confidence > 100
        ):
            raise ValueError(
                "Confidence must be between 0 and 100"
            )
