from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyMetadata:
    name: str
    version: str
    author: str
    market: str
    timeframe: str
    enabled: bool = True
