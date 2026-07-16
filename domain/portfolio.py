from dataclasses import dataclass, asdict


@dataclass
class Portfolio:
    account_id: str
    cash: float
    available_margin: float
    used_margin: float
    equity: float
    realized_pnl: float
    unrealized_pnl: float
    positions: int
    holdings: int

    def total_funds(self) -> float:
        """Return total account funds."""
        return self.cash

    def free_margin(self) -> float:
        """Return available trading margin."""
        return self.available_margin

    def to_dict(self) -> dict:
        """Convert portfolio to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Portfolio":
        """Create Portfolio from dictionary."""
        return cls(**data)