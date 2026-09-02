import csv
from collections.abc import Iterable
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from domain.instrument import Instrument
from providers.base_instrument_provider import BaseInstrumentProvider


class DhanInstrumentProvider(BaseInstrumentProvider):
    """Load instruments from the Dhan scrip master."""

    def __init__(
        self,
        filename: str | Path = "data/instruments/dhan_scrip_master.csv",
    ) -> None:
        self._filename = Path(filename)

    @staticmethod
    def _parse_expiry(value: str) -> datetime | None:
        value = (value or "").strip()

        if not value:
            return None

        # Dhan uses 0001-01-01 as a sentinel for instruments
        # that do not have an expiry, such as the NIFTY index.
        if value.startswith("0001-01-01"):
            return None

        return datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S",
        )

    @staticmethod
    def _parse_strike(value: str) -> Decimal | None:
        value = (value or "").strip()

        if not value:
            return None

        strike = Decimal(value)

        # Dhan uses 0 for non-option/index instruments.
        if strike == 0:
            return None

        return strike

    def load(self) -> Iterable[Instrument]:
        instruments: list[Instrument] = []

        with self._filename.open(
            newline="",
            encoding="utf-8-sig",
        ) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    security_id = row["SEM_SMST_SECURITY_ID"].strip()

                    if not security_id:
                        continue

                    exchange = row["SEM_EXM_EXCH_ID"]
                    segment = row["SEM_SEGMENT"]

                    if exchange == "NSE" and segment == "I":
                        exchange_segment = "IDX_I"
                    elif exchange == "NSE" and segment == "E":
                        exchange_segment = "NSE_EQ"
                    elif exchange == "NSE" and segment == "D":
                        exchange_segment = "NSE_FNO"
                    else:
                        continue

                    instrument_type = row.get("SEM_INSTRUMENT_NAME") or None

                    expiry = self._parse_expiry(
                        row.get("SEM_EXPIRY_DATE", ""),
                    )

                    strike = self._parse_strike(
                        row.get("SEM_STRIKE_PRICE", ""),
                    )

                    option_type = row.get("SEM_OPTION_TYPE") or None

                    instruments.append(
                        Instrument(
                            symbol=row["SEM_TRADING_SYMBOL"],
                            security_id=security_id,
                            exchange_segment=exchange_segment,
                            lot_size=int(float(row["SEM_LOT_UNITS"])),
                            tick_size=Decimal(row["SEM_TICK_SIZE"]),
                            instrument_type=instrument_type,
                            expiry=expiry,
                            strike=strike,
                            option_type=option_type,
                        )
                    )

                except (
                    KeyError,
                    ValueError,
                    TypeError,
                    ArithmeticError,
                ):
                    continue

        return instruments
