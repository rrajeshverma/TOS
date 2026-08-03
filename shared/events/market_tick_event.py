"""
Market Tick Event.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class MarketTickEvent:
    """Represents a market tick."""

    market: Any
    history: list[Any]
