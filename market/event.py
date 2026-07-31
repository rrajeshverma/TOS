"""
TOS Market Event Domain Model

Represents a processed market data event.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from market.tick import Tick


@dataclass(frozen=True)
class MarketEvent:
    """
    Immutable market event.
    """

    event_type: str
    tick: Tick
    source: str
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.event_type:
            raise ValueError("Event type is required")

        if not self.source:
            raise ValueError("Source is required")

        if not isinstance(
            self.tick,
            Tick,
        ):
            raise ValueError("Valid Tick is required")
