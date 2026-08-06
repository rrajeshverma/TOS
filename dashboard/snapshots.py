"""
Dashboard snapshot models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RuntimeSnapshot:
    """
    Runtime snapshot for dashboard rendering.
    """

    status: str
    mode: str
    running: bool
    metrics: dict[str, int]


@dataclass(slots=True, frozen=True)
class BrokerSnapshot:
    """
    Broker connection snapshot.
    """

    broker: str
    connected: bool
    latency_ms: int
    heartbeat: str


@dataclass(slots=True, frozen=True)
class MarketSnapshot:
    """
    Market snapshot.
    """

    market: str
    session: str
    connected: bool


@dataclass(slots=True, frozen=True)
class PortfolioSnapshot:
    """
    Portfolio snapshot.
    """

    total_value: float
    cash: float
    invested: float
    pnl: float


@dataclass(slots=True, frozen=True)
class RiskSnapshot:
    """
    Risk snapshot.
    """

    status: str
    daily_loss: float
    kill_switch: bool
    circuit_breaker: bool
