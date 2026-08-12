import csv
from collections.abc import Iterable
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

    def load(self) -> Iterable[Instrument]:
        instruments: list[Instrument] = []

        with self._filename.open(
            newline="",
            encoding="utf-8-sig",
        ) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    if not row["SEM_SMST_SECURITY_ID"]:
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

                    instruments.append(
                        Instrument(
                            symbol=row["SEM_TRADING_SYMBOL"],
                            security_id=row["SEM_SMST_SECURITY_ID"],
                            exchange_segment=exchange_segment,
                            lot_size=int(float(row["SEM_LOT_UNITS"])),
                            tick_size=Decimal(row["SEM_TICK_SIZE"]),
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
