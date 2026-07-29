"""
Market tick domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class MarketTick:
    """
    Broker-independent market tick.
    """

    symbol: str
    ltp: Decimal
    volume: int = 0
    timestamp: str | None = None
