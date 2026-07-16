from dataclasses import dataclass, field


@dataclass
class EquityCurveWidget:
    points: list = field(default_factory=list)
    starting_equity: float = 0.0
    current_equity: float = 0.0