from decimal import Decimal

from brokers.dhan.models import BrokerTick
from brokers.instrument_mapper import InstrumentMapper


class DhanTickMapper:
    def __init__(self, instrument_mapper: InstrumentMapper):
        self._instrument_mapper = instrument_mapper

    def to_broker_tick(self, data: dict) -> BrokerTick:
        security_id = str(data["security_id"])

        exchange_segment = {
            0: "IDX_I",
            1: "NSE_EQ",
            2: "NSE_FNO",
            3: "NSE_CURRENCY",
            4: "BSE_EQ",
            5: "MCX_COMM",
            7: "BSE_CURRENCY",
            8: "BSE_FNO",
        }[int(data["exchange_segment"])]

        instrument = self._instrument_mapper.get_by_security_id(
            security_id,
            exchange_segment,
        )

        return BrokerTick(
            symbol=instrument.symbol,
            ltp=float(Decimal(str(data["LTP"]))),
            volume=0,
            timestamp=data["LTT"],
        )
