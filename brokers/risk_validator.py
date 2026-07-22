from config.config_manager import ConfigManager
from config.validators import (
    validate_required,
    validate_type,
    validate_range,
)


class RiskValidator:
    def __init__(self, manager: ConfigManager):
        self.manager = manager

    def validate(self):
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
        if risk_percent <= 0:
            raise ValueError("Risk percent must be greater than zero.")

        daily_loss_limit = self.manager.get("risk.daily_loss_limit")
        validate_required(daily_loss_limit)
        validate_type(daily_loss_limit, (int, float))
        if daily_loss_limit <= 0:
            raise ValueError("Daily loss limit must be greater than zero.")

        max_trades = self.manager.get("risk.max_trades")
        validate_required(max_trades)
        validate_type(max_trades, int)
        if max_trades <= 0:
            raise ValueError("Max trades must be greater than zero.")

        max_open_positions = self.manager.get("risk.max_open_positions")
        validate_required(max_open_positions)
        validate_type(max_open_positions, int)
        if max_open_positions <= 0:
            raise ValueError("Max open positions must be greater than zero.")

        risk_reward_ratio = self.manager.get("risk.risk_reward_ratio")
        validate_required(risk_reward_ratio)
        validate_type(risk_reward_ratio, (int, float))
        if risk_reward_ratio <= 0:
            raise ValueError("Risk reward ratio must be greater than zero.")

        return True