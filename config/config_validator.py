from config.config_manager import ConfigManager
from config.validators import (
    validate_range,
    validate_required,
    validate_type,
)


class ConfigValidator:
    from typing import ClassVar

    VALID_MODES: ClassVar[set[str]] = {"LIVE", "PAPER", "BACKTEST"}

    def __init__(self, manager: ConfigManager):
        self.manager = manager

    def validate(self):
        # Broker
        broker = self.manager.get("broker")
        validate_required(broker)

        broker_name = self.manager.get("broker.name")
        validate_required(broker_name)

        api_key = self.manager.get("broker.api_key")
        validate_required(api_key)

        # Risk
        risk = self.manager.get("risk")
        validate_required(risk)

        capital = self.manager.get("risk.capital")
        validate_required(capital)
        validate_type(capital, (int, float))

        if capital <= 0:
            raise ValueError("Capital must be greater than zero.")

        risk_percent = self.manager.get("risk.risk_percent")
        validate_required(risk_percent)
        validate_type(risk_percent, (int, float))
        validate_range(risk_percent, 0, 100)

        # Trading
        trading = self.manager.get("trading")
        validate_required(trading)

        mode = self.manager.get("trading.mode")
        validate_required(mode)

        if mode not in self.VALID_MODES:
            raise ValueError(f"Unsupported trading mode: {mode}")

        return True
