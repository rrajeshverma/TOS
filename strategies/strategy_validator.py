from config.config_manager import ConfigManager
from config.validators import (
    validate_required,
    validate_type,
)


class StrategyValidator:
    SUPPORTED_TIMEFRAMES = {
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "4h",
        "1d",
    }

    def __init__(self, manager: ConfigManager):
        self.manager = manager

    def validate(self):
        strategy = self.manager.get("strategy")
        validate_required(strategy)

        name = self.manager.get("strategy.name")
        validate_required(name)
        validate_type(name, str)

        enabled = self.manager.get("strategy.enabled")
        validate_required(enabled)
        validate_type(enabled, bool)

        timeframe = self.manager.get("strategy.timeframe")
        validate_required(timeframe)
        validate_type(timeframe, str)

        if timeframe not in self.SUPPORTED_TIMEFRAMES:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        entry_rules = self.manager.get("strategy.entry_rules")
        validate_required(entry_rules)
        validate_type(entry_rules, list)

        if len(entry_rules) == 0:
            raise ValueError("Entry rules cannot be empty.")

        exit_rules = self.manager.get("strategy.exit_rules")
        validate_required(exit_rules)
        validate_type(exit_rules, list)

        if len(exit_rules) == 0:
            raise ValueError("Exit rules cannot be empty.")

        indicators = self.manager.get("strategy.indicators")
        validate_required(indicators)
        validate_type(indicators, list)

        if len(indicators) == 0:
            raise ValueError("Indicators cannot be empty.")

        position_sizing = self.manager.get("strategy.position_sizing")
        validate_required(position_sizing)
        validate_type(position_sizing, str)

        return True