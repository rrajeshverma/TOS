from dataclasses import dataclass


@dataclass
class UnrealizedPnLWidget:
    unrealized_pnl: float = 0.0
    position_count: int = 0