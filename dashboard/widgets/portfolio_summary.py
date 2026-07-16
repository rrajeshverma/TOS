from dataclasses import dataclass


@dataclass
class PortfolioSummary:
    total_value: float = 0.0
    cash: float = 0.0
    invested: float = 0.0
    pnl: float = 0.0