"""
TOS Trade Request Object
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TradeRequest:
    """
    Represents a trade request before approval.
    """

    symbol: str
    side: str
    quantity: int
    price: float
    strategy: str
    metadata: dict
