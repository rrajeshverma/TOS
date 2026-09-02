from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class Instrument:
    """
    Broker-independent instrument definition.

    Derivative metadata is optional so existing equity/index
    instruments and tests remain backward compatible.
    """

    symbol: str
    security_id: str
    exchange_segment: str
    lot_size: int
    tick_size: Decimal

    # Derivative metadata
    instrument_type: str | None = None
    expiry: datetime | None = None
    strike: Decimal | None = None
    option_type: str | None = None

    @property
    def is_option(self) -> bool:
        return self.instrument_type == "OPTIDX"

    @property
    def is_nifty_option(self) -> bool:
        return (
            self.is_option
            and self.exchange_segment == "NSE_FNO"
            and self.symbol.startswith("NIFTY-")
            and self.option_type in {"CE", "PE"}
            and self.expiry is not None
            and self.strike is not None
        )
