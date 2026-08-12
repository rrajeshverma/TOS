"""
Runtime configuration.
"""

from dataclasses import dataclass

from exceptions import InvalidConfigurationError


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    """Runtime configuration for Trading Operating System."""

    broker: str = "paper"
    market_data: str = "paper"
    mode: str = "PAPER"
    portfolio: str = "default"

    dhan_client_id: str | None = None
    dhan_access_token: str | None = None

    def validate(self) -> None:
        if self.broker not in {"paper", "dhan"}:
            raise InvalidConfigurationError(f"Unsupported broker: {self.broker}")

        if self.market_data not in {"paper", "dhan"}:
            raise InvalidConfigurationError(f"Unsupported market data source: {self.market_data}")

        if self.mode not in {"PAPER", "LIVE"}:
            raise InvalidConfigurationError(f"Unsupported mode: {self.mode}")

        if not self.portfolio.strip():
            raise InvalidConfigurationError("Portfolio name cannot be empty.")
