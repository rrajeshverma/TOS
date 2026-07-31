"""
Runtime configuration.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    """Runtime configuration for Trading Operating System."""

    broker: str = "paper"
    mode: str = "PAPER"
    portfolio: str = "default"
