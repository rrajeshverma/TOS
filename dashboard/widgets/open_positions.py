from dataclasses import dataclass, field


@dataclass
class OpenPositionsWidget:
    positions: list = field(default_factory=list)
    count: int = 0