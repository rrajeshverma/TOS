"""
Runtime configuration.
"""

from dataclasses import dataclass

from exceptions import InvalidConfigurationError


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    """Runtime configuration for Trading Operating System."""

    broker: str = "paper"
    mode: str = "PAPER"
    portfolio: str = "default"

    def validate(self) -> None:
        if self.broker not in {"paper", "dhan"}:
            raise InvalidConfigurationError(f"Unsupported broker: {self.broker}")

        if self.mode not in {"PAPER", "LIVE"}:
            raise InvalidConfigurationError(f"Unsupported mode: {self.mode}")

        if not self.portfolio.strip():
            raise InvalidConfigurationError("Portfolio name cannot be empty.")
