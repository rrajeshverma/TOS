"""
Broker models for Dhan integration.

These immutable value objects represent broker-level data exchanged
between the adapter layer and the rest of the Trading Operating System.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BrokerOrder:
    """Represents a broker order."""

    symbol: str
    side: str
    quantity: int
    order_type: str
    price: float | None = None


@dataclass(frozen=True, slots=True)
class BrokerPosition:
    """Represents an open broker position."""

    symbol: str
    quantity: int
    average_price: float


@dataclass(frozen=True, slots=True)
class BrokerAccount:
    """Represents broker account information."""

    client_id: str
    available_margin: float
    utilized_margin: float


from datetime import datetime


@dataclass(frozen=True, slots=True)
class BrokerTick:
    """Represents a broker market tick."""

    symbol: str
    ltp: float
    volume: int
    timestamp: datetime
