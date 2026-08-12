"""
Runtime configuration loader.
"""

from __future__ import annotations

import os

from config.runtime_config import RuntimeConfig


class RuntimeConfigLoader:
    """Loads runtime configuration."""

    def load(self) -> RuntimeConfig:
        """Load runtime configuration."""

        config = RuntimeConfig(
            broker=os.getenv("TOS_BROKER", "paper"),
            market_data=os.getenv("TOS_MARKET_DATA", "paper"),
            mode=os.getenv("TOS_MODE", "PAPER"),
            portfolio=os.getenv("TOS_PORTFOLIO", "default"),
            dhan_client_id=os.getenv("DHAN_CLIENT_ID"),
            dhan_access_token=os.getenv("DHAN_ACCESS_TOKEN"),
        )

        config.validate()

        return config
