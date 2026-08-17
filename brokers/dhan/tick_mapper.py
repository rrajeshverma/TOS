from datetime import datetime, time
from decimal import Decimal

from brokers.dhan.models import BrokerTick
from brokers.instrument_mapper import InstrumentMapper


class DhanTickMapper:
    def __init__(self, instrument_mapper: InstrumentMapper):
        self._instrument_mapper = instrument_mapper

    @staticmethod
    def _parse_timestamp(value) -> datetime:
        if isinstance(value, datetime):
            return value

        if isinstance(value, time):
            return datetime.combine(
                datetime.now().date(),
                value,
            )

        if isinstance(value, str):
            parsed_time = time.fromisoformat(value)

            return datetime.combine(
                datetime.now().date(),
                parsed_time,
            )

        raise TypeError(
            f"Unsupported Dhan timestamp type: {type(value).__name__}",
        )

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
            timestamp=self._parse_timestamp(data["LTT"]),
        )
