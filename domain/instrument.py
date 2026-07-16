from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class Instrument:
    symbol: str
    security_id: str
    exchange_segment: str
    lot_size: int
    tick_size: Decimal