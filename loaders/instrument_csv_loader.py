import csv
from decimal import Decimal
from pathlib import Path

from domain.instrument import Instrument


class InstrumentCSVLoader:
    def load(self, filename: str | Path) -> list[Instrument]:
        instruments: list[Instrument] = []

        with open(filename, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    instrument = Instrument(
                        symbol=row["symbol"],
                        security_id=row["security_id"],
                        exchange_segment=row["exchange_segment"],
                        lot_size=int(row["lot_size"]),
                        tick_size=Decimal(row["tick_size"]),
                    )

                    instruments.append(instrument)

                except (KeyError, ValueError, TypeError, ArithmeticError):
                    continue

        return instruments