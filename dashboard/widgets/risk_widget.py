from dataclasses import dataclass


@dataclass
class RiskWidget:
    max_drawdown: float = 0.0
    current_risk: float = 0.0
    risk_reward_ratio: float = 0.0
